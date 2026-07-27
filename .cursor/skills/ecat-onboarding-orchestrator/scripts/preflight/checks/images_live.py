#!/usr/bin/env python3
"""Primary-image set diff — the check that would have kept Lib & Co on the portal.

`audit_images.py` reads local disk, which is the wrong surface for most clients: their
images live in FTP/Admin and were never staged in the repo. mali had 691 images live
against 17 staged locally, so a local audit says almost nothing.

Verified mechanism, zero exceptions across 832 products:

| `image_exists` | primary file present in `product_images` | products |
|---|---|---|
| false | no | 9 |
| true | yes | 823 |

**`image_exists` tracks only the FIRST filename in the reference list.** An alternate
(`-1.jpg`) does not satisfy it. eOL suppresses imageless products from search, so
"products aren't showing up" was literally true on the portal while the same products
browsed fine on the iPad — the single most confusing bug shape in the corpus.

`product_images` is a flat, filename-keyed table with no product reference, so the diff
is pure set arithmetic: primary tokens from the CSV vs uploaded filenames from the org.
Pass the uploaded list in with `--live-images`; this script never touches the DB.
"""
from ..core import fail, get, is_url, split_codes, warn

CHECK = "images-live"
SUBSYSTEM = "images-local"

MAX_LISTED = 15


def primary_tokens(rows, lookup):
    """BaseItemCode -> (primary, alternates), skipping URL-delivered rows."""
    out = {}
    for row in rows:
        bic = get(row, lookup, "BaseItemCode") or "?"
        names = [n for n in split_codes(get(row, lookup, "ImageFileName"))
                 if not is_url(n)]
        if names:
            out[bic] = (names[0], names[1:])
    return out


def run(rows, lookup, live_images=None, hideable_field="Hideable"):
    if "imagefilename" not in lookup:
        return [warn(CHECK, "no ImageFileName column — nothing to diff")]

    refs = primary_tokens(rows, lookup)
    if not refs:
        return [warn(
            CHECK,
            "every image reference is a URL, so there are no uploaded filenames to diff. "
            "Use the image URL census instead",
        )]

    if live_images is None:
        return [warn(
            CHECK,
            f"no --live-images list supplied: could not confirm any of the {len(refs)} "
            f"primary image(s) exist for the org. This is the authoritative image check "
            f"— local disk is not, since most clients upload straight to FTP/Admin. Pull "
            f"the filename list from the org's product_images",
        )]

    uploaded = {str(n).strip() for n in live_images if str(n).strip()}
    uploaded_lower = {n.lower(): n for n in uploaded}
    visible_of = {
        get(r, lookup, "BaseItemCode"): get(r, lookup, hideable_field) for r in rows
    }

    missing_primary, case_mismatch, missing_alt = [], [], []
    for bic, (primary, alternates) in sorted(refs.items()):
        if primary in uploaded:
            pass
        elif primary.lower() in uploaded_lower:
            case_mismatch.append((bic, primary, uploaded_lower[primary.lower()]))
        else:
            has_alt = any(a in uploaded for a in alternates)
            missing_primary.append((bic, primary, has_alt))
        for alt in alternates:
            if alt not in uploaded and alt.lower() not in uploaded_lower:
                missing_alt.append((bic, alt))

    findings = [warn(
        CHECK,
        f"{len(refs) - len(missing_primary) - len(case_mismatch)}/{len(refs)} products "
        f"have their PRIMARY image uploaded ({len(uploaded)} filenames live for the org)",
    )]

    for bic, primary, has_alt in missing_primary[:MAX_LISTED]:
        visible = visible_of.get(bic, "") != "Y"
        extra = (
            " — an ALTERNATE for this SKU IS uploaded, which does NOT satisfy "
            "image_exists; only the first filename counts" if has_alt else ""
        )
        stakes = (
            " This product is visible, so eOL will suppress it from search while it "
            "still browses fine on the iPad." if visible else ""
        )
        findings.append(fail(
            CHECK,
            f"primary image '{primary}' is not uploaded for the org -> "
            f"image_exists=false{extra}.{stakes}",
            bic,
        ))
    if len(missing_primary) > MAX_LISTED:
        findings.append(fail(
            CHECK,
            f"...and {len(missing_primary) - MAX_LISTED} more products whose primary "
            f"image is not uploaded",
        ))

    for bic, primary, actual in case_mismatch[:MAX_LISTED]:
        findings.append(fail(
            CHECK,
            f"primary image '{primary}' differs from the uploaded '{actual}' by case "
            f"only. The match is case-sensitive, so this counts as missing",
            bic,
        ))

    if missing_alt:
        shown = ", ".join(f"{b}:{a}" for b, a in missing_alt[:5])
        findings.append(warn(
            CHECK,
            f"{len(missing_alt)} alternate image(s) not uploaded (does not affect "
            f"image_exists or portal visibility): {shown}"
            + (" ..." if len(missing_alt) > 5 else ""),
        ))

    return findings
