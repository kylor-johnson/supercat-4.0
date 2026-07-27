#!/usr/bin/env python3
"""Apply Magic Lite / NSL dual Library via Admin Console session.

Creates NSL sections + link entries from pdf_links, removes Sale, flips
brand user-group Library auth to Selected with correct entry IDs.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

BASE = "https://supercat.supercatsolutions.com"
ORG = "mali"
CREDS = Path.home() / ".supercat" / "mcp-credentials.json"
PLAN = Path("/tmp/mali_library_plan.json")
MAGIC_ROOT = Path(__file__).resolve().parents[1]
PDF_LINKS = MAGIC_ROOT / "07_Data_Scraping" / "pdf_links"

NSL_SECTIONS = [
    "NSL — Catalogues & Selection Guides",
    "NSL — Installation Instructions",
    "NSL — Product Cut Sheets",
]

NSL_CATALOGUES = [
    (
        "National Specialty Lighting Catalog 2025",
        "https://www.nslusa.com/wp-content/uploads/2025/04/National-Specialty-Lighting-Catalog_May-2025.pdf",
    ),
    (
        "Landscape Lineup 2024",
        "https://www.nslusa.com/wp-content/uploads/2024/08/Landscape-Lineup_2024_NSL_v3.0.pdf",
    ),
    (
        "Tape Selection Chart & Replacement Guide",
        "https://www.nslusa.com/wp-content/uploads/2024/12/Tape-Selection-Chart-and-Replacement-Guide_NSL.pdf",
    ),
]

ML_GROUP_NAMES = {"ML Reps", "eOL  ML Public Site"}
NSL_GROUP_NAMES = {"NSL Reps", "eOL  NSL Public Site"}
# ids from live Postgres 2026-07-20
GROUP_IDS = {
    "ML Reps": 2781,
    "NSL Reps": 2782,
    "eOL  ML Public Site": 2836,
    "eOL  NSL Public Site": 2841,
}


class AdminSession:
    def __init__(self) -> None:
        creds = json.loads(CREDS.read_text())
        self.username = creds["username"]
        self.password = creds["password"]
        self.cj = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [("User-Agent", "MaliLibraryBrandSplit/1.0")]

    def get(self, path: str) -> str:
        with self.opener.open(BASE + path, timeout=90) as resp:
            return resp.read().decode("utf-8", "replace")

    def post(self, path: str, fields: dict, *, multipart: bool = False):
        html = self.get(f"/{ORG}/shared_resources")
        tok = self._token(html)
        data = dict(fields)
        data["authenticity_token"] = tok
        body = urllib.parse.urlencode(data, doseq=True).encode()
        req = urllib.request.Request(BASE + path, data=body, method="POST")
        try:
            with self.opener.open(req, timeout=90) as resp:
                return resp.status, resp.geturl(), resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, getattr(e, "url", path), e.read().decode("utf-8", "replace")

    @staticmethod
    def _token(html: str) -> str:
        m = re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', html)
        if not m:
            m = re.search(r'value="([^"]+)"[^>]*name="authenticity_token"', html)
        if not m:
            raise RuntimeError("No authenticity_token found")
        return m.group(1)

    def login(self) -> None:
        html = self.get("/supercat/sessions/new")
        tok = self._token(html)
        body = urllib.parse.urlencode(
            {
                "authenticity_token": tok,
                "username": self.username,
                "password": self.password,
            }
        ).encode()
        req = urllib.request.Request(BASE + "/supercat/sessions", data=body, method="POST")
        with self.opener.open(req, timeout=90) as resp:
            url = resp.geturl()
            page = resp.read().decode("utf-8", "replace")
        if "passkey_setup_prompt" in url:
            tok = self._token(page) if "authenticity_token" in page else tok
            body = urllib.parse.urlencode({"authenticity_token": tok}).encode()
            req = urllib.request.Request(
                BASE + "/supercat/passkeys/dismiss_passkey_setup_prompt",
                data=body,
                method="POST",
            )
            with self.opener.open(req, timeout=90) as resp:
                print("dismissed passkey prompt ->", resp.geturl())
        # warm library
        self.get(f"/{ORG}/shared_resources")
        print("logged in as", self.username)

    def list_resources(self) -> list[dict]:
        """Parse index page for section/entry ids (fallback). Prefer Postgres for truth."""
        html = self.get(f"/{ORG}/shared_resources")
        # anchors like #section-37717 / #resource-36606
        sections = {
            int(i): None
            for i in re.findall(r'id="section-(\d+)"', html)
        }
        # also from new-link URLs
        for m in re.finditer(
            r'shared_resources/(\d+)(?:/edit|/)?|"section-(\d+)"|resource-(\d+)',
            html,
        ):
            pass
        return html

    def create_directory(self, name: str) -> int | None:
        status, url, html = self.post(
            f"/{ORG}/shared_resources",
            {
                "resource_type": "directory",
                "shared_resource[value]": name,
            },
        )
        m = re.search(r"#section-(\d+)", url)
        if m:
            print(f"  directory ok id={m.group(1)} {name}")
            return int(m.group(1))
        # maybe already exists — scrape index for name
        print(f"  directory create status={status} url={url} name={name}")
        return self.find_directory_id(name)

    def find_directory_id(self, name: str) -> int | None:
        html = self.get(f"/{ORG}/shared_resources")
        # look for heading near section id
        for m in re.finditer(
            r'id="section-(\d+)"[\s\S]{0,800}?' + re.escape(name),
            html,
        ):
            return int(m.group(1))
        # reverse: name then nearby section
        for m in re.finditer(
            re.escape(name) + r'[\s\S]{0,400}?section-(\d+)',
            html,
        ):
            return int(m.group(1))
        # edit links under directory
        pat = re.compile(
            rf'directory_id=(\d+)[^>]*>[\s\S]{{0,40}}{re.escape(name)}|'
            rf'{re.escape(name)}[\s\S]{{0,200}}directory_id=(\d+)'
        )
        m = pat.search(html)
        if m:
            return int(m.group(1) or m.group(2))
        return None

    def create_link(self, parent_id: int, label: str, url: str) -> int | None:
        status, loc, html = self.post(
            f"/{ORG}/shared_resources",
            {
                "resource_type": "link",
                "shared_resource[parent_id]": str(parent_id),
                "shared_resource[label]": label,
                "shared_resource[value]": url,
                "shared_resource[shareable]": "1",
            },
        )
        m = re.search(r"#(?:resource|entry|section)-(\d+)", loc)
        # index anchors for entries vary; parse flash/location
        m2 = re.search(r"#resource-(\d+)", loc) or re.search(r"/(\d+)/edit", loc)
        rid = int((m or m2).group(1)) if (m or m2) else None
        if rid:
            print(f"  link ok id={rid} {label[:60]}")
            return rid
        # success redirect to index with anchor sometimes section parent
        if status == 200 and "shared_resources" in loc:
            print(f"  link saved (no id in url) {label[:60]}")
            return -1
        print(f"  LINK FAIL status={status} loc={loc} label={label[:60]}")
        return None

    def destroy(self, resource_id: int) -> None:
        html = self.get(f"/{ORG}/shared_resources")
        tok = self._token(html)
        body = urllib.parse.urlencode(
            {"authenticity_token": tok, "_method": "delete"}
        ).encode()
        req = urllib.request.Request(
            BASE + f"/{ORG}/shared_resources/{resource_id}",
            data=body,
            method="POST",
        )
        try:
            with self.opener.open(req, timeout=90) as resp:
                print(f"  destroyed {resource_id} -> {resp.geturl()}")
        except urllib.error.HTTPError as e:
            print(f"  destroy fail {resource_id}: {e.code}")

    def update_user_type_library(
        self, user_type_id: int, auth: str, resource_ids: list[int]
    ) -> None:
        """POST user type edit with shared_resources_auth + selected IDs only.

        Loads edit form so other fields are preserved.
        """
        html = self.get(f"/{ORG}/user_types/{user_type_id}/edit")
        tok = self._token(html)
        fields: list[tuple[str, str]] = [("authenticity_token", tok), ("_method", "patch")]

        # Capture existing user_type[...] inputs/selects/textareas
        for m in re.finditer(
            r'<(?:input|textarea|select)[^>]*name="(user_type\[[^\]]+\])"[^>]*>',
            html,
            re.I,
        ):
            name = m.group(1)
            tag = m.group(0)
            if 'type="checkbox"' in tag or 'type="radio"' in tag:
                continue
            if 'type="hidden"' in tag or 'type="text"' in tag or 'type="number"' in tag or "textarea" in tag.lower() or "<select" in tag.lower():
                vm = re.search(r'value="([^"]*)"', tag)
                if vm:
                    # skip duplicates we'll override
                    if name.startswith("user_type["):
                        fields.append((name, vm.group(1)))

        # Also grab checked checkboxes for non-library associations carefully —
        # safer: only send shared_resources_auth + shared_resources[id] and name.
        # Re-parse name field
        name_m = re.search(
            r'name="user_type\[name\]"[^>]*value="([^"]*)"', html
        ) or re.search(
            r'value="([^"]*)"[^>]*name="user_type\[name\]"', html
        )
        ut_name = name_m.group(1) if name_m else ""

        # Minimal safe payload used by BuildsUserTypes.receive_children
        payload: dict = {
            "_method": "patch",
            "user_type[name]": ut_name,
            "shared_resources_auth": auth,
        }
        if auth == "c":
            for rid in resource_ids:
                payload[f"shared_resources[{rid}]"] = "1"

        status, loc, body = self.post(
            f"/{ORG}/user_types/{user_type_id}",
            payload,
        )
        # post() refreshes token from shared_resources; user_types need own token —
        # redo with direct token from edit page
        data = dict(payload)
        data["authenticity_token"] = tok
        body_bytes = urllib.parse.urlencode(data, doseq=True).encode()
        req = urllib.request.Request(
            BASE + f"/{ORG}/user_types/{user_type_id}",
            data=body_bytes,
            method="POST",
        )
        try:
            with self.opener.open(req, timeout=90) as resp:
                print(
                    f"  user_type {user_type_id} ({ut_name}) auth={auth} "
                    f"n_entries={len(resource_ids)} -> {resp.status} {resp.geturl()}"
                )
        except urllib.error.HTTPError as e:
            print(f"  user_type FAIL {user_type_id}: {e.code} {e.read()[:200]}")


def load_entries_from_plan(phase: str) -> tuple[list[dict], list[dict]]:
    plan = json.loads(PLAN.read_text())
    if phase == "1":
        return plan["phase1_nsl_cutsheets"], plan["phase1_nsl_instructions"]
    return plan["phase2_nsl_cutsheets"], plan["phase2_nsl_instructions"]


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    # modes: clean | phase1 | phase2 | auth | all
    sess = AdminSession()
    sess.login()

    section_ids: dict[str, int] = {}

    if mode in ("all", "phase1", "phase2", "sections"):
        for name in NSL_SECTIONS:
            existing = sess.find_directory_id(name)
            if existing:
                print(f"section exists {existing} {name}")
                section_ids[name] = existing
            else:
                sid = sess.create_directory(name)
                if sid:
                    section_ids[name] = sid
                time.sleep(0.2)

    if mode in ("all", "clean"):
        # Sale directory 34788 — destroy children first then directory
        print("Cleaning Sale section…")
        sess.destroy(34789)  # Products list file
        time.sleep(0.2)
        sess.destroy(34788)  # Sale directory
        time.sleep(0.2)

    if mode in ("all", "phase1"):
        cat_id = section_ids.get(NSL_SECTIONS[0]) or sess.find_directory_id(NSL_SECTIONS[0])
        ins_id = section_ids.get(NSL_SECTIONS[1]) or sess.find_directory_id(NSL_SECTIONS[1])
        cut_id = section_ids.get(NSL_SECTIONS[2]) or sess.find_directory_id(NSL_SECTIONS[2])
        assert cat_id and ins_id and cut_id, f"missing sections {section_ids}"
        print("Phase 1 catalogues…")
        for label, url in NSL_CATALOGUES:
            sess.create_link(cat_id, label, url)
            time.sleep(0.15)
        cs, ins = load_entries_from_plan("1")
        print(f"Phase 1 cut sheets ({len(cs)})…")
        for e in cs:
            sess.create_link(cut_id, e["label"], e["url"])
            time.sleep(0.12)
        print(f"Phase 1 instructions ({len(ins)})…")
        for e in ins:
            # Prefer shorter instruction labels
            label = e["label"] + " — Instructions"
            sess.create_link(ins_id, label, e["url"])
            time.sleep(0.12)

    if mode in ("all", "phase2"):
        ins_id = section_ids.get(NSL_SECTIONS[1]) or sess.find_directory_id(NSL_SECTIONS[1])
        cut_id = section_ids.get(NSL_SECTIONS[2]) or sess.find_directory_id(NSL_SECTIONS[2])
        assert ins_id and cut_id
        cs, ins = load_entries_from_plan("2")
        print(f"Phase 2 cut sheets ({len(cs)})…")
        for e in cs:
            sess.create_link(cut_id, e["label"], e["url"])
            time.sleep(0.12)
        print(f"Phase 2 instructions ({len(ins)})…")
        for e in ins:
            label = e["label"] + " — Instructions"
            sess.create_link(ins_id, label, e["url"])
            time.sleep(0.12)

    if mode in ("all", "auth"):
        print(
            "Auth flip expects Postgres ID lists passed via /tmp/mali_auth_ids.json"
        )
        auth_path = Path("/tmp/mali_auth_ids.json")
        if not auth_path.exists():
            print("MISSING /tmp/mali_auth_ids.json — generate from Postgres first")
            return 2
        ids = json.loads(auth_path.read_text())
        for gname, gid in GROUP_IDS.items():
            if gname in ML_GROUP_NAMES:
                sess.update_user_type_library(gid, "c", ids["ml"])
            else:
                sess.update_user_type_library(gid, "c", ids["nsl"])
            time.sleep(0.3)

    print("done mode=", mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
