#!/usr/bin/env python3
"""Handoff serializer — Phase 4 (IMPLEMENTATION_PLAN.md §7 Phase 4).

Emits HANDOFF.md in twelve sections.  Every factual count is sourced from the
reconciled live-state block in CLIENT_PROFILE.md (written by reconcile/profile.py),
never from agent memory or typed prose.

Twelve mandatory sections:
  1.  Identity — shortname + org id + product scope + phase
  2.  Client emotional/political state
  3.  Sources of truth ranked + anti-sources
  4.  Locked decisions
  5.  Field mapping table (code-derived limits via gen_limits)
  6.  Current state — from reconcile/profile.py, NOT typed counts
  7.  eCat gotcha block
  8.  Validation checklist — runnable commands + expected outputs
  9.  Open items: we-fix vs need-client
  10. Do-NOT / out-of-scope
  11. Deliverable format (GO/NO-GO or mismatch table with fix-owner)
  12. Anti-hallucination preamble (verbatim from IMPLEMENTATION_PLAN.md §7 Phase 4)

Additional sections from later corpus specimens:
  A. Chain of custody
  B. Skills to load
  C. Schema notes

CLI:
    python scripts/handoff/serialize.py \\
        --client-dir eCat_Onboarding/mali \\
        --shortname mali \\
        --out eCat_Onboarding/mali/HANDOFF.md

    # Override section 2 (client emotional/political state):
        --political-state "Client frustrated about wrong images; correctness over speed."

Every fact carries a provenance pointer: query name, file path, or code path.
Rule: IMPLEMENTATION_PLAN.md §2.3 — counts must never be typed into prose.
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Path setup — allow running from any directory
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent   # scripts/handoff/
_SCRIPTS = _HERE.parent                   # scripts/
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


# ---------------------------------------------------------------------------
# Anti-hallucination preamble — verbatim from IMPLEMENTATION_PLAN.md §7 Phase 4
# ---------------------------------------------------------------------------

ANTI_HALLUCINATION_PREAMBLE = (
    "You are a fresh agent with no prior context. "
    "Do NOT trust this document's claims — re-derive them from the data and code. "
    "Find anything wrong and fix it."
)

FALSIFY_INSTRUCTIONS = (
    "Before acting on any claim in this document: "
    "(1) open the source file or DB query named in the provenance pointer and confirm "
    "the value directly; "
    "(2) if the code says otherwise, the document is wrong — flag it and stop; "
    "(3) you have explicit authorization to stop and say 'I cannot confirm this' "
    "rather than guessing."
)


# ---------------------------------------------------------------------------
# CLIENT_PROFILE.md parser
# ---------------------------------------------------------------------------

def _re_field(text: str, pattern: str, default: str = "") -> str:
    """Return the first capture group from a regex match, or default."""
    m = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return m.group(1).strip() if m else default


def _re_block(text: str, header_pattern: str) -> str:
    """Extract a markdown section body (text between header and the next ## or end)."""
    m = re.search(
        header_pattern + r"\s*\n+(.*?)(?=\n##|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    return m.group(1).strip() if m else ""


def parse_client_profile(path: str) -> Dict[str, Any]:
    """Parse CLIENT_PROFILE.md into a structured dict.

    Provenance: CLIENT_PROFILE.md at path.
    All keys are absent (empty string) when the field is not present — never None,
    so callers can use `.get("key") or "fallback"` safely.
    """
    try:
        text = open(path, "r", encoding="utf-8-sig").read()
    except OSError:
        return {}

    p: Dict[str, Any] = {"_raw": text, "_path": path}

    # Identity
    p["shortname"] = _re_field(text, r"\*\*Org shortname:\*\*\s*`?([A-Za-z0-9_-]+)`?")
    p["org_id"] = _re_field(text, r"\*\*Org (?:ID|id):\*\*\s*`?(\d+)`?")
    p["client_name"] = _re_field(
        text, r"\*\*Client(?:\s+name)?:\*\*\s*(.+?)(?:\n|$)"
    )
    p["phase"] = _re_field(
        text, r"\*\*(?:Current\s+)?[Pp]hase:\*\*\s*(.+?)(?:\n|$)"
    )
    p["product_scope"] = _re_field(
        text, r"\*\*Product scope:\*\*\s*(.+?)(?:\n|$)"
    )
    p["go_live_date"] = _re_field(
        text, r"\*\*Go.?live date:\*\*\s*(.+?)(?:\n|$)"
    )
    p["taxonomy_method"] = _re_field(
        text, r"\*\*Taxonomy method:\*\*\s*(.+?)(?:\n|$)"
    )
    p["pricing_model"] = _re_field(
        text, r"\*\*Pricing model:\*\*\s*(.+?)(?:\n|$)"
    )
    p["image_mode"] = _re_field(
        text, r"\*\*Image mode:\*\*\s*(.+?)(?:\n|$)"
    )
    p["erp_system"] = _re_field(
        text, r"\*\*ERP(?:/PIM)?:\*\*\s*(.+?)(?:\n|$)"
    )
    p["archetype"] = _re_field(
        text, r"\*\*Archetype(?:\s*&\s*applicability)?:\*\*\s*(.+?)(?:\n|$)"
    )

    # Section blocks
    p["political_state"] = _re_block(
        text, r"##\s*Client\s*(?:state|[Ss]tatus|[Cc]ontext)"
    )
    p["sources_of_truth"] = _re_block(text, r"##\s*Sources?\s+of\s+[Tt]ruth")
    p["locked_decisions"] = _re_block(text, r"##\s*Locked\s+[Dd]ecisions?")
    p["open_items"] = _re_block(text, r"##\s*Open\s+[Ii]tems?")
    p["do_not"] = _re_block(text, r"##\s*Do.NOT")
    p["chain_of_custody"] = _re_block(text, r"##\s*Chain\s+of\s+[Cc]ustody")

    return p


# ---------------------------------------------------------------------------
# Live state loader (from reconcile block in CLIENT_PROFILE.md)
# ---------------------------------------------------------------------------

def _load_live_state(profile_path: str):
    """Return a LiveState from the reconciled block in CLIENT_PROFILE.md.

    Provenance: reconcile/profile.py:read_profile_block().
    Returns None if not available (no DB, no block written yet).
    IMPLEMENTATION_PLAN.md §2.3: counts come from this function only.
    """
    try:
        from reconcile.profile import read_profile_block
        state, _ = read_profile_block(profile_path)
        return state
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# Field mapping table (code-derived limits from gen_limits)
# ---------------------------------------------------------------------------

def _field_mapping_lines(files: Optional[List[str]] = None) -> List[str]:
    """Render the field mapping table from limits_generated.py.

    Provenance: preflight/limits_generated.py — generated by tools/gen_limits.py
    from supercat_server.  Numbers are never transcribed here.
    """
    try:
        from preflight import limits_generated as gen
        from preflight.limits import RETIRED_CLAIMS
        limits = gen.LIMITS
        advisory = gen.ADVISORY_LIMITS
        gen_at = gen.GENERATED_AT[:10]
        sha = gen.SOURCE_GIT_SHA[:8]
        provenance_line = (
            f"supercat_server @ `{sha}` (generated {gen_at}) — "
            f"never transcribed; regenerate: "
            f"`python scripts/tools/gen_limits.py --server-root <path>`"
        )
        retired = RETIRED_CLAIMS
    except ImportError:
        return [
            "_Field limits unavailable — `preflight/limits_generated.py` not found._",
            "",
            "Regenerate: `python scripts/tools/gen_limits.py --server-root <path-to-supercat_server>`",
        ]

    out: List[str] = [f"_Provenance: {provenance_line}_", ""]

    target_files = files or sorted(limits.keys())
    for csv_file in target_files:
        file_limits = limits.get(csv_file, {})
        adv_limits = advisory.get(csv_file, {})
        if not file_limits and not adv_limits:
            continue
        out.append(f"**{csv_file}**")
        out.append("")
        out.append("| CSV header | eCat attr | Tier | Limit | Notes |")
        out.append("|---|---|---|---|---|")
        all_headers = sorted(set(file_limits) | set(adv_limits))
        for header in all_headers:
            if header in file_limits:
                meta = file_limits[header]
                attr = meta.get("attr", "—")
                model = meta.get("model", "")
                tier = "REJECT-row" if meta["tier"] == "error" else "WARN+truncate"
                lim = str(meta["limit"])
                note = f"{model}::ATTR_LENGTHS[:{attr}]" if model and attr != "—" else ""
            else:
                meta = adv_limits[header]
                attr = "—"
                tier = "advisory"
                lim = str(meta["limit"])
                note = (meta.get("note") or meta.get("source") or "")[:80]
            out.append(f"| `{header}` | `{attr}` | {tier} | {lim} | {note} |")
        out.append("")

    out += [
        "**Retired claims (documented limits that do NOT exist in code — do not enforce):**",
        "",
    ]
    for claim, why in retired.items():
        out.append(f"- `{claim}`: {why}")
    out.append("")

    return out


# ---------------------------------------------------------------------------
# Validation commands (section 8)
# ---------------------------------------------------------------------------

def _validation_commands(
    shortname: str,
    client_dir: str,
    live_state: Any,
) -> List[str]:
    """Generate runnable validation commands for this client.

    Integrates Phase 1 (preflight_gate.py) and Phase 2 (reconcile/profile.py).
    Provenance: preflight_gate.py, reconcile/profile.py, reconcile/queries.py.
    """
    import_dir = os.path.join(client_dir, "00_Import_Files", "Ready_For_Import")
    out: List[str] = [
        "Run each command and compare output to the expected result. "
        "Do NOT proceed to FTP upload if any exits non-zero.",
        "",
        "**Phase 2 — reconcile live state against CLIENT_PROFILE.md:**",
        "",
        "```bash",
        "# 1. Check for drift (requires DATABASE_URL or VPN)",
        f"python scripts/reconcile/profile.py \\",
        f"    --shortname {shortname} \\",
        f"    --client-dir {client_dir}",
        f"# Expected: MATCH  (or a list of DRIFT fields to resolve)",
        "",
        "# 2. Generate live-state JSON for the gate",
        f"python scripts/reconcile/profile.py \\",
        f"    --shortname {shortname} \\",
        f"    --emit-live-state \\",
        f"    > live_{shortname}.json",
        f"# Expected: exit 0; live_{shortname}.json written with queried_at timestamp",
        "```",
        "",
        "**Phase 1 — pre-import gate (run before every FTP upload):**",
        "",
        "```bash",
        f"python scripts/preflight_gate.py \\",
        f"    --client-dir {client_dir} \\",
        f"    --dir {import_dir} \\",
        f"    --live-state live_{shortname}.json \\",
        f"    --ack-deletes",
        "# Expected: exit 0; all checks PASS or SKIP (no FAIL, no unexplained WARNING)",
        "```",
        "",
        "**Named queries for manual verification via MCP `supercat-postgres-vpn`:**",
        "",
    ]

    try:
        from reconcile.queries import QUERIES
        priority = [
            "ORG_BY_SHORTNAME",
            "PRODUCT_COUNTS",
            "CUSTOMER_COUNT",
            "INVENTORY_COUNTS",
            "ORPHAN_INVENTORY",
            "PRICE_LEVELS",
            "ORPHAN_OPTIONS",
            "IMPORT_EVENTS_RECENT",
            "IMAGE_EXISTS_SPLIT",
        ]
        out.append("| Query name | Purpose | Key param |")
        out.append("|---|---|---|")
        for qname in priority:
            if qname in QUERIES:
                _, desc = QUERIES[qname]
                short = desc.split(".")[0][:75]
                param = (
                    f"`%(shortname)s` → `{shortname}`"
                    if qname == "ORG_BY_SHORTNAME"
                    else f"`%(org_id)s` → org DB id for `{shortname}`"
                )
                out.append(f"| `{qname}` | {short} | {param} |")
        out.append("")
        out.append(
            "_Print full SQL: `python scripts/reconcile/queries.py --print QUERY_NAME`_"
        )
    except ImportError:
        out.append(
            "_Query registry not available — run from the `scripts/` directory._"
        )

    out += ["", "**Expected live-DB outputs at time of this handoff:**", ""]

    if live_state is not None:
        ts = live_state.queried_at or "UNKNOWN — re-query"
        out.append(f"_Queried: {ts}_")
        out.append("")

        pairs = [
            ("products_active",      "PRODUCT_COUNTS → active_products"),
            ("products_with_images", "IMAGE_EXISTS_SPLIT → active_with_images"),
            ("customers",            "CUSTOMER_COUNT → total_customers"),
            ("inventory_rows",       "INVENTORY_COUNTS → total_inventory_rows"),
            ("orphan_inventory",     "ORPHAN_INVENTORY → orphan_inventory_rows"),
            ("options",              "ORPHAN_OPTIONS → total_options"),
            ("option_groups",        "ORPHAN_OPTIONS → total_option_groups"),
        ]
        for attr, label in pairs:
            val = getattr(live_state, attr, None)
            if val is not None:
                out.append(f"- {label} = **{val:,}**  _(provenance: {ts[:10]})_")

        if live_state.price_level_codes is not None:
            codes = ", ".join(f"`{c}`" for c in sorted(live_state.price_level_codes))
            out.append(
                f"- PRICE_LEVELS → {codes or '_none_'}  _(provenance: {ts[:10]})_"
            )
    else:
        out.append(
            "_Live state not available. "
            f"Run `python scripts/reconcile/profile.py --shortname {shortname} "
            f"--client-dir {client_dir} --update` to populate._"
        )

    return out


# ---------------------------------------------------------------------------
# eCat gotcha block (section 7)
# ---------------------------------------------------------------------------

_GOTCHA_LINES = [
    "**Import order (mandatory — violating this nulls option group membership):**",
    "",
    "`options.csv` → `option_groups.csv` → `products.csv` → `stories.csv` → "
    "`inventory.csv` → `customers.csv`",
    "",
    "Always re-send `option_groups.csv` immediately after `options.csv` — "
    "importing options **nulls group membership**.",
    "",
    "**Delete semantics per file:**",
    "",
    "| File | Omitted record | Deletes run when |",
    "|---|---|---|",
    "| `products.csv` | Soft-delete (`deleted=true`) | Clean import only (zero errors) |",
    "| `stories.csv` | Sets `story=null` (product survives) | Clean import only |",
    "| `inventory.csv` | **Hard-delete ALL inventory**, then reload | Clean import only |",
    "| `customers.csv` | **Hard-delete ALL customers + ship-tos**, then reload | Clean import only |",
    "| `options.csv` | **Hard-delete ALL options** + null group membership | Clean import only |",
    "| `option_groups.csv` | **Hard-delete ALL groups**, then reload | Clean import only |",
    "| `matrix_options.csv` / `contract_prices.csv` | **Hard-delete ALL**, then reload | Clean import only |",
    "",
    "_Provenance: ecat-ground-truth workspace rule, supercat_server importer code._",
    "",
    "**Error-tier blocks deletes:**  If the import has any `Error` rows, omitted records "
    "are NOT removed — only good rows import and obsolete records stay. An unexplained "
    "'record still exists' is almost always an Error row blocking the delete. Check "
    "**Tools → Admin Reports → File Import Status** (blue link = problems).",
    "",
    "**Image rules:**",
    "- `.jpg` / `.jpeg` only — PNG is silently rejected by `CdnImageSync` "
    "(no error message; images just never appear)",
    "- Flat `/images` FTP root only — subfolders are ignored",
    "- Primary image first in `ImageFileName`; `image_exists` tracks only the primary",
    "- Max 6 images by default (12 only with `enable_twelve_product_images` flag)",
    "",
    "**Taxonomy groups never auto-create from a product import.** A missing group → "
    "fatal import error. Create groups in Admin first (Products → Groups).",
    "",
    "**Schema traps (verified from supercat_server + live DB, Appendix A):**",
    "- `organizations.state` is **geographic** (TX/CA/Ontario) — NOT lifecycle. "
    "Lifecycle is `properties->>'status'` = `onboarding` | `active` | `fully_suspended`.",
    "- `customers` key column is `code`, NOT `customer_number`.",
    "- `import_events.data` is a YAML text blob — columns `file_type`/`num_warnings`/"
    "`num_errors` (older runbooks) **DO NOT EXIST**. Parse with "
    "`reconcile.queries.parse_import_tiers()`.",
    "- `product_images` has **no `product_id` FK** — flat, filename-keyed only.",
    "- `products.options` is serialized YAML — NOT separate OptionSet1..5 DB columns.",
    "- `price_levels` has no `description` column.",
    "",
    "_Provenance: queries.py module docstring, ecat-ground-truth, ecat-import-ops._",
]

# ---------------------------------------------------------------------------
# Skills to load (section B)
# ---------------------------------------------------------------------------

_SKILLS = [
    ("ecat-onboarding-orchestrator", "Phase routing, state load/persist"),
    ("ecat-core-files", "products.csv / stories.csv / inventory.csv build"),
    ("ecat-customers-build", "customers.csv, DefaultPriceCode, bill-to/ship-to"),
    ("ecat-pricing-levels", "Price levels, price columns, user-group visibility"),
    ("ecat-options-and-mapping", "options.csv, option_groups.csv, Admin Option Mapping"),
    ("ecat-images-ftp", "FTP upload, ImageFileName, missing image diagnosis"),
    ("ecat-go-live", "User groups, reps, territories, go-live readiness"),
    ("ecat-smartlists", "SmartList queries and hand-picked item lists"),
    ("ecat-postgres-audit", "Live DB audits via supercat-postgres-vpn MCP"),
    ("ecat-support-triage", "Ad-hoc support outside a full onboarding build"),
    ("ecat-client-email", "Client-facing emails in Kylor's voice"),
    ("ecat-session-handoff", "End-of-session handoff generation (invokes this serializer)"),
]

# ---------------------------------------------------------------------------
# Schema notes (section C)
# ---------------------------------------------------------------------------

_SCHEMA_NOTES: List[Tuple[str, str, str]] = [
    (
        "`import_events.data`",
        "YAML text blob. "
        "Columns `file_type` / `num_warnings` / `num_errors` (per older runbooks) "
        "**DO NOT EXIST**. "
        "Parse with `reconcile.queries.parse_import_tiers()` for "
        "`:fatal` / `:error` / `:warning` / `:information` counts.",
        "queries.py:parse_import_tiers()",
    ),
    (
        "`organizations.state`",
        "Geographic state (TX, CA, Ontario) — NOT lifecycle. "
        "Lifecycle is `properties->>'status'` = `onboarding` | `active` | `fully_suspended`. "
        "`WHERE o.state = 'onboarding'` returns 0 rows.",
        "queries.py:ORG_BY_SHORTNAME",
    ),
    (
        "`products.options`",
        "Serialized YAML — NOT separate OptionSet1..5 columns. "
        "No options → `---\\n:custom: false\\n`. "
        "Smart SKU builder → `properties->>'configured_item_number_builder'`.",
        "queries.py:PRODUCTS_WITH_OPTIONS",
    ),
    (
        "`product_images`",
        "Flat table, filename-keyed, **no `product_id` FK**. "
        "`image_exists` on the `products` row tracks only whether the primary filename "
        "from `images_json` is present in `product_images`.",
        "queries.py:UPLOADED_IMAGES",
    ),
    (
        "`price_levels`",
        "Columns: `code`, `name`, `pl_type`, `factor`. "
        "No `description` column. "
        "`DefaultPriceCode` in customers.csv must exactly match `price_levels.code`.",
        "queries.py:PRICE_LEVELS",
    ),
    (
        "`customers.code`",
        "Key column is `code`, NOT `customer_number`.",
        "queries.py:CUSTOMER_KEYS_SAMPLE",
    ),
    (
        "`option_groups.options`",
        "YAML id array of option IDs. "
        "Importing options.csv nulls group membership — "
        "always re-send option_groups.csv immediately after.",
        "ecat-ground-truth rule",
    ),
    (
        "`organizations.properties`",
        "JSON column. Org-level feature flags live here, e.g. "
        "`properties->>'enable_twelve_product_images'`, "
        "`properties->>'status'` (lifecycle), "
        "`properties->>'configured_item_number_builder'` (Smart SKU).",
        "queries.py:ORG_BY_SHORTNAME",
    ),
]


# ---------------------------------------------------------------------------
# Serializer — 12 sections + A/B/C ancillary
# ---------------------------------------------------------------------------

class HandoffSerializer:
    """Render HANDOFF.md in 12 mandatory sections plus ancillary sections A/B/C.

    Every factual count flows through live_state (from reconcile/profile.py),
    never typed inline. Fields from CLIENT_PROFILE.md are narrative context only.
    """

    def __init__(
        self,
        client_dir: str,
        shortname: str,
        political_state_override: Optional[str] = None,
        _profile_override: Optional[Dict[str, Any]] = None,
        _live_state_override: Any = None,
    ):
        self.client_dir = os.path.abspath(client_dir)
        self.shortname = shortname
        self.political_state_override = political_state_override
        self.generated_at = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        profile_path = os.path.join(self.client_dir, "CLIENT_PROFILE.md")
        self.profile_path = profile_path
        self.profile: Dict[str, Any] = (
            _profile_override
            if _profile_override is not None
            else parse_client_profile(profile_path)
        )
        self.live_state = (
            _live_state_override
            if _live_state_override is not None
            else _load_live_state(profile_path)
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _section(number: str, title: str, body: List[str]) -> List[str]:
        return [
            "",
            "---",
            "",
            f"## Section {number} — {title}",
            "",
            *body,
        ]

    @staticmethod
    def _p(d: Dict, key: str, fallback: str = "_not set_") -> str:
        v = d.get(key) or ""
        return v.strip() or fallback

    # ------------------------------------------------------------------
    # Section 1 — Identity
    # ------------------------------------------------------------------

    def _s1_identity(self) -> List[str]:
        p = self.profile
        sn = self.shortname or self._p(p, "shortname")
        return [
            "| Field | Value | Provenance |",
            "|---|---|---|",
            f"| Client name | {self._p(p, 'client_name')} | CLIENT_PROFILE.md |",
            f"| Org shortname | `{sn}` | CLIENT_PROFILE.md |",
            f"| Org DB id | `{self._p(p, 'org_id')}` | ORG_BY_SHORTNAME query |",
            f"| Product scope | {self._p(p, 'product_scope', 'iPad')} | CLIENT_PROFILE.md |",
            f"| Current phase | {self._p(p, 'phase')} | CLIENT_PROFILE.md |",
            f"| Archetype | {self._p(p, 'archetype')} | CLIENT_PROFILE.md |",
            f"| ERP/PIM | {self._p(p, 'erp_system')} | CLIENT_PROFILE.md |",
            f"| Go-live date | {self._p(p, 'go_live_date')} | CLIENT_PROFILE.md |",
            f"| Taxonomy method | {self._p(p, 'taxonomy_method')} | CLIENT_PROFILE.md |",
            f"| Pricing model | {self._p(p, 'pricing_model')} | CLIENT_PROFILE.md |",
            f"| Image mode | {self._p(p, 'image_mode')} | CLIENT_PROFILE.md |",
            f"| Handoff generated | {self.generated_at} | scripts/handoff/serialize.py |",
        ]

    # ------------------------------------------------------------------
    # Section 2 — Client emotional/political state
    # ------------------------------------------------------------------

    def _s2_political_state(self) -> List[str]:
        if self.political_state_override:
            text = self.political_state_override
            source = "--political-state CLI flag"
        else:
            text = (self.profile.get("political_state") or "").strip()
            source = "CLIENT_PROFILE.md § Client state"

        intro = [
            "_Load-bearing context — sets the speed/accuracy trade-off for every "
            "decision in this session._",
            "",
        ]
        if text:
            return intro + [text, "", f"_Source: {source}_"]

        return intro + [
            "_Not recorded. Add a `## Client state` section to CLIENT_PROFILE.md "
            "or pass `--political-state` on the CLI._",
            "",
            f"_Source: {source} (absent)_",
        ]

    # ------------------------------------------------------------------
    # Section 3 — Sources of truth ranked + anti-sources
    # ------------------------------------------------------------------

    def _s3_sources_of_truth(self) -> List[str]:
        import_dir = os.path.join(
            self.client_dir, "00_Import_Files", "Ready_For_Import"
        )
        out = [
            "| Rank | Source | What it proves | Beats |",
            "|---|---|---|---|",
            "| 1 | Live DB (supercat-postgres-vpn MCP) | What is actually live for reps | Everything |",
            "| 2 | `import_events.data` (Admin → File Import Status) | What actually imported, with tier | Local CSV files |",
            f"| 3 | `{import_dir}/` | What we built and sent | Older drafts, email attachments |",
            "| 4 | Client's source export (most recent) | Field names and row structure | Older revisions |",
            "| 5 | `CLIENT_PROFILE.md` reconcile block only | Declared configuration | Typed prose anywhere |",
            "",
            "**Anti-sources (do not treat as ground truth):**",
            "",
            "- Agent memory or prior session chat — re-derive from data and code on every session",
            "- Typed counts in any markdown file (including this one) — re-query via `reconcile/profile.py`",
            "- Catalog screenshots / visual inspection — non-reproducible between agents; "
            "caused a regression at Magic Lite",
            "- CLIENT_PROFILE.md prose outside the `<!-- reconcile:start … -->` block — may be stale",
            "- Files outside `Ready_For_Import/` — may be drafts or superseded revisions",
            "",
            f"_Provenance: IMPLEMENTATION_PLAN.md §2, ecat-ground-truth, SKILL.md §Source of truth._",
        ]

        extra = (self.profile.get("sources_of_truth") or "").strip()
        if extra:
            out += ["", "**Additional sources from CLIENT_PROFILE.md:**", "", extra]

        return out

    # ------------------------------------------------------------------
    # Section 4 — Locked decisions
    # ------------------------------------------------------------------

    def _s4_locked_decisions(self) -> List[str]:
        p = self.profile
        out = [
            "These decisions must **not** be re-litigated. "
            "If any seems wrong, flag it and ask Kylor — do not silently override.",
            "",
            "| Decision | Locked value | Provenance |",
            "|---|---|---|",
            "| Import order | options → option_groups → products → stories → "
            "inventory → customers | ecat-ground-truth |",
            "| Error-tier blocks deletes | Any Error row → omitted records NOT removed | ecat-ground-truth |",
            "| Image format | .jpg / .jpeg only; PNG silently rejected by CdnImageSync | limits_generated.py |",
            "| Taxonomy groups | Never auto-create from product import | ecat-ground-truth |",
            "| Counts in prose | Typed counts are forbidden; use reconcile/profile.py | IMPLEMENTATION_PLAN §2.3 |",
        ]
        for label, key in [
            ("Taxonomy method", "taxonomy_method"),
            ("Pricing model",   "pricing_model"),
            ("Image mode",      "image_mode"),
            ("Archetype",       "archetype"),
        ]:
            val = (p.get(key) or "").strip()
            if val:
                out.append(f"| {label} | {val} | CLIENT_PROFILE.md |")

        out.append("")
        extra = (p.get("locked_decisions") or "").strip()
        if extra:
            out += ["**Additional locked decisions from CLIENT_PROFILE.md:**", "", extra, ""]

        return out

    # ------------------------------------------------------------------
    # Section 5 — Field mapping table (code-derived limits)
    # ------------------------------------------------------------------

    def _s5_field_mapping(self) -> List[str]:
        return [
            "Field limits are **code-derived** (never transcribed) from "
            "`scripts/preflight/limits_generated.py`, generated by "
            "`scripts/tools/gen_limits.py` from `supercat_server`.",
            "",
            *_field_mapping_lines(),
        ]

    # ------------------------------------------------------------------
    # Section 6 — Current state (live-queried, not typed)
    # ------------------------------------------------------------------

    def _s6_current_state(self) -> List[str]:
        live = self.live_state

        if live is None:
            return [
                "**Live state not yet reconciled.**",
                "",
                "```bash",
                "python scripts/reconcile/profile.py \\",
                f"    --shortname {self.shortname} \\",
                f"    --client-dir {self.client_dir} \\",
                "    --update",
                "```",
                "",
                "_Until reconciled this section is intentionally blank — "
                "IMPLEMENTATION_PLAN.md §2.3: counts must never be typed into prose._",
            ]

        ts = live.queried_at or "UNKNOWN"
        stale = live.is_stale()
        stale_note = "  ⚠ **STALE** — re-run `reconcile/profile.py --update`" if stale else ""

        out = [
            f"_Provenance: `reconcile/profile.py:read_profile_block()` + "
            f"PRODUCT_COUNTS / CUSTOMER_COUNT / INVENTORY_COUNTS / "
            f"PRICE_LEVELS / ORPHAN_OPTIONS queries._",
            f"_Queried: `{ts}`{stale_note}_",
            "",
            "| Metric | DB live | Queried | Query |",
            "|---|---|---|---|",
        ]
        date_str = ts[:10]

        def _row(label: str, value: Any, query: str) -> str:
            if value is None:
                v = "—"
            elif isinstance(value, list):
                v = ", ".join(f"`{c}`" for c in sorted(value)) or "_none_"
            elif isinstance(value, int):
                v = f"**{value:,}**"
            else:
                v = f"`{value}`"
            return f"| {label} | {v} | {date_str} | `{query}` |"

        if live.products_active is not None:
            out.append(_row("Products (active)", live.products_active, "PRODUCT_COUNTS"))
        if live.products_with_images is not None:
            if live.products_active:
                pct = live.products_with_images / live.products_active * 100
                out.append(
                    f"| With images | **{live.products_with_images:,}** ({pct:.0f}%) "
                    f"| {date_str} | `IMAGE_EXISTS_SPLIT` |"
                )
            else:
                out.append(_row("With images", live.products_with_images, "IMAGE_EXISTS_SPLIT"))
        if live.customers is not None:
            out.append(_row("Customers", live.customers, "CUSTOMER_COUNT"))
        if live.inventory_rows is not None:
            out.append(_row("Inventory rows", live.inventory_rows, "INVENTORY_COUNTS"))
        if live.orphan_inventory is not None:
            flag = " ⚠" if live.orphan_inventory > 0 else ""
            out.append(
                f"| Orphan inventory | **{live.orphan_inventory:,}**{flag} "
                f"| {date_str} | `ORPHAN_INVENTORY` |"
            )
        if live.price_level_codes is not None:
            codes = ", ".join(f"`{c}`" for c in sorted(live.price_level_codes))
            out.append(
                f"| Price levels | {codes or '_none_'} | {date_str} | `PRICE_LEVELS` |"
            )
        if live.options is not None:
            out.append(_row("Options", live.options, "ORPHAN_OPTIONS"))
        if live.option_groups is not None:
            out.append(_row("Option groups", live.option_groups, "ORPHAN_OPTIONS"))
        if live.lifecycle is not None:
            out.append(_row("Lifecycle", live.lifecycle, "ORG_BY_SHORTNAME"))

        out += [
            "",
            "**What has NOT happened yet (as of above timestamp):**",
            "",
            "_Fill from `import_events` (IMPORT_EVENTS_RECENT query) + "
            "CLIENT_PROFILE.md phase tracking. If unknown, write: "
            "'NOT VERIFIED — check import_events via IMPORT_EVENTS_RECENT query'._",
        ]
        return out

    # ------------------------------------------------------------------
    # Section 7 — eCat gotcha block
    # ------------------------------------------------------------------

    def _s7_gotchas(self) -> List[str]:
        return list(_GOTCHA_LINES)

    # ------------------------------------------------------------------
    # Section 8 — Validation checklist
    # ------------------------------------------------------------------

    def _s8_validation_checklist(self) -> List[str]:
        return _validation_commands(
            shortname=self.shortname,
            client_dir=self.client_dir,
            live_state=self.live_state,
        )

    # ------------------------------------------------------------------
    # Section 9 — Open items: we-fix vs need-client
    # ------------------------------------------------------------------

    def _s9_open_items(self) -> List[str]:
        out = [
            "Split every open item into **we-fix** (agent can act without client) "
            "vs **need-client** (blocked on client data, decision, or access).",
            "",
            "| Item | Owner | Blocked on | Provenance |",
            "|---|---|---|---|",
            "| _(fill from CLIENT_PROFILE.md open items and live state)_ "
            "| — | — | — |",
            "",
        ]
        extra = (self.profile.get("open_items") or "").strip()
        if extra:
            out += ["**Open items from CLIENT_PROFILE.md:**", "", extra, ""]
        else:
            out += [
                "_No open items recorded in CLIENT_PROFILE.md. "
                "Add a `## Open items` section with a we-fix / need-client split._"
            ]
        return out

    # ------------------------------------------------------------------
    # Section 10 — Do-NOT / out-of-scope
    # ------------------------------------------------------------------

    def _s10_do_not(self) -> List[str]:
        out = [
            "**Universal do-nots (every client, every session):**",
            "",
            "- Do NOT FTP or import any file without explicit Kylor approval",
            "- Do NOT type counts into prose — run `scripts/reconcile/profile.py`",
            "- Do NOT trust agent memory or prior handoffs as ground truth — re-derive",
            "- Do NOT skip the pre-import gate (`preflight_gate.py`)",
            "- Do NOT re-litigate locked decisions (Section 4) without Kylor sign-off",
            "- Do NOT comment, create, transition, or edit Jira tickets "
            "(Jira is read-only per workspace rule `jira-read-only`)",
            "- Do NOT write factual counts to CLIENT_PROFILE.md except via "
            "`reconcile/profile.py --update`",
            "- Do NOT assume a local CSV reflects the live catalog — check `import_events`",
            "- Do NOT use vision/screenshot output as a primary data source "
            "(Magic Lite: declared 3 SKUs broken; screenshots proved them correct)",
            "- Do NOT use the `Insightful Product 2.0` or `3.0` folders "
            "(frozen per `insightful-legacy-frozen` rule)",
            "",
        ]
        extra = (self.profile.get("do_not") or "").strip()
        if extra:
            out += ["**Client-specific do-nots from CLIENT_PROFILE.md:**", "", extra, ""]
        return out

    # ------------------------------------------------------------------
    # Section 11 — Deliverable format
    # ------------------------------------------------------------------

    def _s11_deliverable_format(self) -> List[str]:
        return [
            "Every session ends with one of:",
            "",
            "**GO** — all pre-import gate checks pass, live state reconciled "
            "(`queried_at` < 7 days old), no CONTRADICTED claims in any client-facing draft.",
            "",
            "**NO-GO** — one or more checks fail. Emit a mismatch table:",
            "",
            "| Check | Expected | Actual | Fix owner | Action |",
            "|---|---|---|---|---|",
            "| ORPHAN_INVENTORY | 0 | N | We-fix | Re-send inventory.csv with corrected rows |",
            "| Gate exit code | 0 | 1 | We-fix | Resolve FAIL findings in gate output |",
            "| Live state | queried | STALE | We-fix | Run reconcile/profile.py --update |",
            "| DefaultPriceCode | in price_levels | missing | Need-client | Client to confirm price level codes |",
            "",
            "**Fix-owner rules:**",
            "- `We-fix` — resolvable without client input (agent action)",
            "- `Need-client` — blocked on data, a decision, or access only the client has",
            "- `Kylor-decision` — judgment call above agent authority; surface, never decide",
            "",
            "_Provenance: IMPLEMENTATION_PLAN.md §7 Phase 4 §11._",
        ]

    # ------------------------------------------------------------------
    # Section 12 — Anti-hallucination preamble
    # ------------------------------------------------------------------

    def _s12_anti_hallucination(self) -> List[str]:
        return [
            f"> {ANTI_HALLUCINATION_PREAMBLE}",
            "",
            f"> {FALSIFY_INSTRUCTIONS}",
            "",
            "**Falsify-the-premise examples from the corpus:**",
            "",
            '- "Open `cdn_image_sync.rb` and confirm it rejects PNG; if the code '
            'says otherwise the whole premise is wrong — flag it."',
            '- "Run ORPHAN_INVENTORY and confirm the count — '
            'do not assume the handoff number is current."',
            '- "Check `import_events` for the actual last-import tier before '
            'attributing a root cause."',
            "",
            "_This preamble is verbatim from IMPLEMENTATION_PLAN.md §7 Phase 4. "
            "It caught a prior agent's false claim both times it was used. "
            "It must appear verbatim on every handoff._",
        ]

    # ------------------------------------------------------------------
    # Ancillary section A — Chain of custody
    # ------------------------------------------------------------------

    def _sa_chain_of_custody(self) -> List[str]:
        out = [
            "| When | Who / What | Action | Provenance |",
            "|---|---|---|---|",
            f"| {self.generated_at} | `scripts/handoff/serialize.py` "
            f"| Generated this handoff | Phase 4 serializer |",
        ]
        extra = (self.profile.get("chain_of_custody") or "").strip()
        if extra:
            out += ["", "**History from CLIENT_PROFILE.md:**", "", extra]
        else:
            out += ["| _(add entries as actions occur)_ | — | — | — |"]
        return out

    # ------------------------------------------------------------------
    # Ancillary section B — Skills to load
    # ------------------------------------------------------------------

    def _sb_skills_to_load(self) -> List[str]:
        out = [
            "Load at the start of any session for this client:",
            "",
            "| Skill | Use for |",
            "|---|---|",
        ]
        for skill, use in _SKILLS:
            out.append(f"| `{skill}` | {use} |")
        out += [
            "",
            "_Load: invoke the `<skill>` skill_",
        ]
        return out

    # ------------------------------------------------------------------
    # Ancillary section C — Schema notes
    # ------------------------------------------------------------------

    def _sc_schema_notes(self) -> List[str]:
        out = [
            "Verified from `supercat_server` source and live DB (Appendix A of "
            "IMPLEMENTATION_PLAN.md). Do not re-discover these in a session.",
            "",
            "| Entity | Verified fact | Provenance |",
            "|---|---|---|",
        ]
        for entity, fact, prov in _SCHEMA_NOTES:
            safe_fact = fact.replace("|", "\\|")
            out.append(f"| {entity} | {safe_fact} | `{prov}` |")
        return out

    # ------------------------------------------------------------------
    # Top-level render
    # ------------------------------------------------------------------

    def render(self) -> str:
        sn = self.shortname or self.profile.get("shortname") or "UNKNOWN"
        client_name = self.profile.get("client_name") or sn.upper()

        lines: List[str] = [
            f"# HANDOFF — {client_name} (`{sn}`)",
            "",
            f"_Generated: `{self.generated_at}`_  ",
            f"_Generator: `scripts/handoff/serialize.py`_  ",
            f"_Shortname: `{sn}`_  ",
            f"_Client dir: `{self.client_dir}`_  ",
            f"_Profile: `{self.profile_path}`_  ",
            "",
            "> **" + ANTI_HALLUCINATION_PREAMBLE + "**",
            "",
        ]

        twelve = [
            ("1",  "Identity",                                    self._s1_identity),
            ("2",  "Client Emotional/Political State",            self._s2_political_state),
            ("3",  "Sources of Truth (ranked) + Anti-Sources",   self._s3_sources_of_truth),
            ("4",  "Locked Decisions",                           self._s4_locked_decisions),
            ("5",  "Field Mapping Table (code-derived limits)",  self._s5_field_mapping),
            ("6",  "Current State (live-queried, not typed)",    self._s6_current_state),
            ("7",  "eCat Gotcha Block",                          self._s7_gotchas),
            ("8",  "Validation Checklist (runnable commands)",   self._s8_validation_checklist),
            ("9",  "Open Items: We-Fix vs Need-Client",          self._s9_open_items),
            ("10", "Do-NOT / Out-of-Scope",                      self._s10_do_not),
            ("11", "Deliverable Format (GO / NO-GO)",            self._s11_deliverable_format),
            ("12", "Anti-Hallucination Preamble",                self._s12_anti_hallucination),
        ]
        ancillary = [
            ("A", "Chain of Custody",      self._sa_chain_of_custody),
            ("B", "Skills to Load",        self._sb_skills_to_load),
            ("C", "Schema Notes (Verified)", self._sc_schema_notes),
        ]

        for num, title, fn in twelve + ancillary:
            lines.extend(self._section(num, title, fn()))

        lines += [
            "",
            "---",
            "",
            f"_End of handoff. Generated {self.generated_at}._",
            "",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--client-dir", required=True,
        help="eCat_Onboarding/<client>/ root; CLIENT_PROFILE.md must exist here",
    )
    ap.add_argument(
        "--shortname", default=None,
        help="eCat org shortname (e.g. mali, tcd, leg); "
             "falls back to 'Org shortname' in CLIENT_PROFILE.md",
    )
    ap.add_argument(
        "--out", default=None,
        help="output path (default: HANDOFF.md inside --client-dir)",
    )
    ap.add_argument(
        "--political-state", default=None, dest="political_state",
        help="override section 2 (client emotional/political state)",
    )
    args = ap.parse_args()

    client_dir = os.path.abspath(args.client_dir)
    if not os.path.isdir(client_dir):
        print(f"ERROR: --client-dir '{client_dir}' is not a directory.", file=sys.stderr)
        return 2

    shortname = args.shortname
    if not shortname:
        profile_path = os.path.join(client_dir, "CLIENT_PROFILE.md")
        p = parse_client_profile(profile_path)
        shortname = p.get("shortname") or ""
    if not shortname:
        print(
            "ERROR: --shortname not supplied and not found in CLIENT_PROFILE.md. "
            "Pass --shortname <code>.",
            file=sys.stderr,
        )
        return 2

    out_path = args.out or os.path.join(client_dir, "HANDOFF.md")

    serializer = HandoffSerializer(
        client_dir=client_dir,
        shortname=shortname,
        political_state_override=args.political_state,
    )
    content = serializer.render()

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as exc:
        print(f"ERROR: cannot write '{out_path}': {exc}", file=sys.stderr)
        return 2

    print(f"Wrote {len(content):,} bytes → {out_path}", file=sys.stderr)

    if serializer.live_state is None:
        print(
            "WARNING: live state not loaded — run:\n"
            f"  python scripts/reconcile/profile.py "
            f"--shortname {shortname} --client-dir {client_dir} --update",
            file=sys.stderr,
        )
    elif serializer.live_state.is_stale():
        print(
            "WARNING: live state is STALE (>7d old) — re-run reconcile/profile.py.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
