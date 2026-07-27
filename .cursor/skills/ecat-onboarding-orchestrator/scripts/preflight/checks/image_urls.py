#!/usr/bin/env python3
"""Image URL census (IMPLEMENTATION_PLAN.md 4.7) — the undocumented delivery path.

`ImageFileName` accepts a full HTTPS URL, not just a filename; eCat fetches the bytes
itself, which makes FTP optional. Nobody at SuperCat knew this five weeks into an
engagement — weeks of manual scraping preceded the CTO mentioning it mid-call.

`CdnImageSync` runs **two** gates and needs both to pass:

    unless valid_image_content_type?(image_url) && valid_image_filename?(image_filename)
      log(:error, "Skipping invalid #{image_url}")

`valid_image_content_type?` accepts only `image/jpeg` or `image/jpg`.
`valid_image_filename?` requires a `.jpg`/`.jpeg` extension **and** a match on
`Product::VALID_IMAGE_REGEX`. A `.png` URL fails both, the product keeps pointing at a
file that never downloads, and it renders stale or blank. That was 23 PNG URLs affecting
54 option rows, live for weeks, behind the client's question *"I see VERY old image file
names, so I am wondering if we are pulling images from the live Catsy links at all?"*

Two consequences that outlast the bug:

* **The failure logs at `:error`.** Per the delete semantics, an error row makes the
  importer skip *all* deletes of omitted records — so a catalog with PNG URLs is probably
  also failing to soft-delete discontinued products, silently.
* **eCat caches at import; it does not live-render.** The download is conditional on the
  CDN's last-modified beating the stored timestamp, so replacing bytes at the same URL
  changes nothing until a re-import. The workaround is a versioned filename (`-v2`).

Pattern classification is free and always runs. `--check-urls` adds one HEAD request per
distinct URL, which is the difference between an eight-week failure and a day-one one.
"""
import json
import os
from concurrent.futures import ThreadPoolExecutor
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import urlparse

from ..core import fail, get, is_url, split_codes, warn
from ..limits import IMAGE_RULES, image_filename_is_valid

CHECK = "image-urls"
SUBSYSTEM = "images-url"

# Hosts whose share links serve an HTML interstitial, never image bytes. Two SKUs sat
# broken for a month on exactly these.
SHARE_LINK_HOSTS = ("drive.google.com", "dropbox.com", "www.dropbox.com",
                    "docs.google.com", "1drv.ms", "onedrive.live.com",
                    "sharepoint.com", "wetransfer.com")

BUCKETS = ("jpg-ok", "png", "wrong-type", "dead", "non-http", "share-link", "unchecked")
DEFAULT_TIMEOUT = 10
DEFAULT_WORKERS = 8


def extract_urls(rows, lookup, field="ImageFileName"):
    """url -> list of BaseItemCodes referencing it (deduplicated by URL)."""
    urls = {}
    for row in rows:
        bic = get(row, lookup, "BaseItemCode") or get(row, lookup, "Code") or "?"
        for token in split_codes(get(row, lookup, field)):
            if is_url(token):
                urls.setdefault(token, []).append(bic)
    return urls


def classify_offline(url):
    """Bucket a URL on pattern alone. Returns (bucket, reason)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return "non-http", f"scheme '{parsed.scheme or '(none)'}' is not fetchable"
    host = parsed.netloc.lower()
    if any(host == h or host.endswith("." + h) for h in SHARE_LINK_HOSTS):
        return "share-link", (
            f"{host} share links serve an HTML page, never image bytes — they can never "
            f"resolve"
        )
    filename = os.path.basename(parsed.path)
    if filename.lower().endswith(".png"):
        return "png", (
            "PNG fails BOTH CdnImageSync gates (extension and Content-Type) and logs at "
            ":error, which also suppresses every delete in the same import"
        )
    ok, why = image_filename_is_valid(filename or url)
    if not ok:
        return "wrong-type", why
    return "jpg-ok", ""


def head(url, timeout=DEFAULT_TIMEOUT):
    """HEAD one URL. Returns (status, content_type, error_message)."""
    req = urlrequest.Request(url, method="HEAD")
    try:
        with urlrequest.urlopen(req, timeout=timeout) as resp:
            return resp.status, (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower(), None
    except urlerror.HTTPError as exc:
        return exc.code, None, f"HTTP {exc.code}"
    except (urlerror.URLError, OSError, ValueError) as exc:
        return None, None, str(getattr(exc, "reason", exc))


def _load_cache(path):
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _save_cache(path, cache):
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=1, sort_keys=True)
    except OSError:
        pass


def census(urls, check_network=False, timeout=DEFAULT_TIMEOUT, workers=DEFAULT_WORKERS,
           cache_path=None):
    """url -> (bucket, reason). Offline classification, optionally confirmed by HEAD."""
    results = {url: classify_offline(url) for url in urls}
    if not check_network:
        return {
            url: (bucket if bucket != "jpg-ok" else "unchecked",
                  reason or "pattern looks fetchable; not confirmed without --check-urls")
            for url, (bucket, reason) in results.items()
        }

    cache = _load_cache(cache_path)
    # Only spend requests on URLs that could still pass; the rest already failed a gate.
    candidates = [u for u, (b, _r) in results.items() if b == "jpg-ok" and u not in cache]

    def probe(url):
        status, content_type, err = head(url, timeout)
        if err and status is None:
            return url, ["dead", f"unreachable: {err}"]
        if status is None or status >= 400:
            return url, ["dead", f"HTTP {status} — the product points at nothing"]
        if content_type not in IMAGE_RULES["content_types"]:
            return url, ["wrong-type", (
                f"Content-Type '{content_type or 'none'}' not in "
                f"{IMAGE_RULES['content_types']} — CdnImageSync skips it at :error tier")]
        return url, ["jpg-ok", f"HTTP {status}, {content_type}"]

    if candidates:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for url, outcome in pool.map(probe, candidates):
                cache[url] = outcome
        _save_cache(cache_path, cache)

    for url, (bucket, reason) in list(results.items()):
        if bucket == "jpg-ok" and url in cache:
            results[url] = tuple(cache[url])
    return results


def run(rows, lookup, field="ImageFileName", check_network=False, timeout=DEFAULT_TIMEOUT,
        workers=DEFAULT_WORKERS, cache_path=None, max_listed=15):
    urls = extract_urls(rows, lookup, field)
    if not urls:
        return [warn(
            CHECK,
            f"no URLs in {field} — this catalog uses FTP-uploaded filenames. Worth "
            f"knowing that {field} also accepts a full HTTPS URL that eCat fetches "
            f"itself, which makes FTP optional",
        )]

    results = census(urls, check_network, timeout, workers, cache_path)
    counts = {b: 0 for b in BUCKETS}
    for bucket, _reason in results.values():
        counts[bucket] = counts.get(bucket, 0) + 1

    findings = [warn(
        CHECK,
        f"URL census over {len(urls)} distinct URL(s): "
        + ", ".join(f"{b}={counts[b]}" for b in BUCKETS if counts.get(b))
        + ("" if check_network else
           " (pattern only — pass --check-urls to HEAD each one and catch dead links "
           "and wrong Content-Type)"),
    )]

    broken = sorted(
        (url, bucket, reason) for url, (bucket, reason) in results.items()
        if bucket in ("png", "dead", "non-http", "share-link", "wrong-type")
    )
    for url, bucket, reason in broken[:max_listed]:
        skus = ", ".join(sorted(set(urls[url]))[:4])
        findings.append(fail(
            CHECK, f"[{bucket}] {url} — {reason}. Referenced by: {skus}"))
    if len(broken) > max_listed:
        findings.append(fail(
            CHECK, f"...and {len(broken) - max_listed} more unfetchable URL(s)"))

    if counts.get("jpg-ok") or counts.get("unchecked"):
        findings.append(warn(
            CHECK,
            "eCat caches image bytes at import rather than live-rendering: the download "
            "is conditional on the CDN's last-modified beating the stored timestamp, so "
            "replacing bytes at the same URL changes nothing until a re-import. Use a "
            "versioned filename (-v2) when an image is corrected",
        ))
    return findings
