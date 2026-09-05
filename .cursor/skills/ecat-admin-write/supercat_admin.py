#!/usr/bin/env python3
"""
SuperCat Admin Console write client — org-agnostic.

Lifted from Legrand/Build/rebuild_library.py `class Admin`, which was written
against `leg` with ORG/BASE hardcoded. Three scripts carried near-identical
copies (rebuild_library, add_missing_library_files, merge_brand_folders); this
is the shared one. Those scripts still work and are deliberately left alone.

WHY THIS EXISTS AT ALL — read before reaching for SQL:

    Changes go through the Rails controllers as a logged-in user because the
    controllers fire callbacks that the database does not. SharedResourcesController
    calls force_org_users_synch! on create/update/destroy, which is what pushes a
    Library change to reps' iPads. Raw SQL skips it, leaves every device stale, and
    corrupts acts_as_list positions on top of that.

    The read-only Postgres MCP is not an obstacle being worked around. It is the
    read half of a correct split: SELECT to find out what is wrong, controllers to
    change it.

Usage:

    from supercat_admin import Admin

    adm = Admin("leg", dry_run=not args.go)
    adm.login()
    res = adm.post("/shared_resources", {...})
    if not res.ok:
        sys.exit(res.explain())

Dry-run is the default. Nothing mutates unless dry_run=False.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("pip install requests")

BASE_DEFAULT = "https://supercat.supercatsolutions.com"
CREDS_PATH = Path.home() / ".supercat" / "mcp-credentials.json"

# A destructive batch at or above this many rows needs a snapshot and an
# explicit confirmed=True. See Admin.destructive().
BULK_THRESHOLD = 3


def credentials():
    """Read the on-disk credentials. Never prompt, never accept a pasted password."""
    if not CREDS_PATH.exists():
        sys.exit(f"missing {CREDS_PATH} — cannot authenticate")
    d = json.loads(CREDS_PATH.read_text())
    return d["username"], d["password"]


@dataclass
class WriteResult:
    """A write's outcome, judged by redirect target rather than status code.

    The trap: with allow_redirects=True, r.status_code is the status of the page
    we LANDED on, not of the write itself. A Rails #update redirects to the index
    only when save returned true; on failure it re-renders :edit. So the honest
    signal is where we ended up, not the number.
    """
    ok: bool
    status: int
    final_url: str
    method: str
    url: str

    def explain(self):
        if self.ok:
            return f"OK   {self.method} {self.url} -> {self.status} {self.final_url}"
        return (f"FAILED {self.method} {self.url}\n"
                f"       status {self.status}, landed on {self.final_url}\n"
                f"       landing back on an edit/new form means the save was rejected; "
                f"check for a validation error or a required field wiped by strong params")


class Admin:
    def __init__(self, org, dry_run=True, base=BASE_DEFAULT,
                 user_agent="supercat-admin/1.0"):
        if not org:
            raise ValueError("org shortname is required")
        self.org = org
        self.base = base.rstrip("/")
        self.dry = dry_run
        self.s = requests.Session()
        self.s.headers["User-Agent"] = user_agent
        self._snapshots = []

    # -- auth ---------------------------------------------------------------

    def _token(self, url):
        r = self.s.get(url, timeout=60)
        r.raise_for_status()
        m = (re.search(r'name="authenticity_token"[^>]*value="([^"]+)"', r.text)
             or re.search(r'name="csrf-token"[^>]*content="([^"]+)"', r.text))
        if not m:
            raise RuntimeError(f"no authenticity_token on {url}")
        return m.group(1)

    def login(self, username=None, password=None):
        """Form login. A FAILED LOGIN RETURNS HTTP 200 — raise_for_status will not
        catch it, so detect it by where we landed and by the flash text."""
        if username is None or password is None:
            username, password = credentials()
        token = self._token(f"{self.base}/supercat/sessions/new")
        r = self.s.post(f"{self.base}/supercat/sessions",
                        data={"authenticity_token": token,
                              "username": username, "password": password},
                        allow_redirects=True, timeout=60)
        r.raise_for_status()
        if "sessions/new" in r.url or "Invalid" in r.text[:4000]:
            sys.exit(f"login failed — check {CREDS_PATH}")
        print(f"OK   logged in as {username}")
        return self

    # -- requests -----------------------------------------------------------

    def _url(self, path):
        return f"{self.base}/{self.org}{path}"

    def request(self, path, data=None, files=None, method="POST",
                token_from=None, timeout=180):
        """One mutating request. Rails receives PATCH/DELETE as a POST carrying
        _method in the body."""
        url = self._url(path)
        if self.dry:
            keys = sorted((data or {}).keys())
            fname = f" +file {list(files)[0]}" if files else ""
            print(f"  [dry-run] {method} {url}  {keys}{fname}")
            return WriteResult(True, 0, url, method, url)

        token = self._token(token_from or self._url("/shared_resources"))
        payload = dict(data or {})
        payload["authenticity_token"] = token
        if method != "POST":
            payload["_method"] = method.lower()

        r = self.s.post(url, data=payload, files=files,
                        allow_redirects=True, timeout=timeout)
        landed = r.url.rstrip("/")
        ok = (r.status_code < 400
              and not landed.endswith("/edit")
              and not landed.endswith("/new"))
        return WriteResult(ok, r.status_code, r.url, method, url)

    def post(self, path, data=None, files=None, **kw):
        return self.request(path, data, files, "POST", **kw)

    def patch(self, path, data=None, files=None, **kw):
        return self.request(path, data, files, "PATCH", **kw)

    def delete(self, path, data=None, **kw):
        return self.request(path, data, None, "DELETE", **kw)

    def get_text(self, path, timeout=60):
        r = self.s.get(self._url(path), timeout=timeout)
        r.raise_for_status()
        return r.text

    # -- guards -------------------------------------------------------------

    def snapshot(self, kind, content, out_dir="."):
        """Dump current state before a destructive step. Returns the path."""
        stamp = _dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        p = Path(out_dir) / f"snapshot_{self.org}_{kind}_{stamp}.txt"
        p.write_text(content)
        self._snapshots.append(str(p))
        print(f"OK   snapshot -> {p}")
        return p

    def destructive(self, targets, confirmed=False):
        """Gate for bulk deletes/moves. Creates, updates and uploads never call this.

        Once a batch reaches BULK_THRESHOLD rows it requires (a) a snapshot already
        taken this run and (b) confirmed=True.
        """
        n = len(targets)
        if n < BULK_THRESHOLD:
            return True
        if not self._snapshots:
            sys.exit(f"REFUSING: {n} destructive targets with no snapshot — "
                     f"call adm.snapshot(...) first")
        if not confirmed:
            print(f"\n  {n} rows would be destroyed/moved:")
            for t in targets:
                print(f"    - {t}")
            print(f"  snapshot: {self._snapshots[-1]}")
            sys.exit("  STOPPING for confirmation — re-run with confirmed=True to apply.")
        return True

    # -- verification -------------------------------------------------------

    @staticmethod
    def verify_sql(table, row_id, org_id=None, columns="*"):
        """The SELECT to run through supercat-postgres-vpn after a write.
        Verification is not optional — WriteResult.ok means Rails accepted the
        form, not that the column holds what you intended."""
        where = f"id = {row_id}"
        if org_id is not None:
            where += f" AND organization_id = {org_id}"
        return f"SELECT {columns} FROM {table} WHERE {where};"

    @staticmethod
    def audit_sql(loggable_type, row_id, limit=5):
        """Controllers call log_change! on success. This is server-side proof,
        independent of anything this script prints about itself. Confirm the
        change_logs table/column names against the schema on first use."""
        return (f"SELECT * FROM change_logs "
                f"WHERE loggable_type = '{loggable_type}' AND loggable_id = {row_id} "
                f"ORDER BY created_at DESC LIMIT {limit};")
