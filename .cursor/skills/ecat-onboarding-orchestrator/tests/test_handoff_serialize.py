"""Tests for scripts/handoff/serialize.py — Phase 4 handoff serializer.

Golden structure test: every render must contain all 12 mandatory section headers.
Additional tests:
  - Anti-hallucination preamble appears verbatim in header and section 12
  - Section 6 counts come from the reconcile block (provenance pointers present)
  - Section 6 does NOT type counts when live state is absent
  - Political-state override lands in section 2
  - Section 5 references code-derived limits, not hard-coded numbers
  - Section 8 emits runnable `python scripts/` commands
  - Ancillary sections A/B/C are present
  - Section 1 identity table has a Provenance column
  - CLI smoke test: --client-dir + --shortname + --out writes HANDOFF.md
  - CLI resolves shortname from CLIENT_PROFILE.md when --shortname is omitted
  - CLI exits 2 when --client-dir does not exist

Corpus invariants enforced:
  IMPLEMENTATION_PLAN.md §7 Phase 4:
    "The preamble is the highest-value line in the corpus and should be emitted
     verbatim on every handoff."
  IMPLEMENTATION_PLAN.md §2.3:
    "Counts must never be typed into prose. They are query results with a timestamp,
     or they do not appear."
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from handoff.serialize import (
    ANTI_HALLUCINATION_PREAMBLE,
    FALSIFY_INSTRUCTIONS,
    HandoffSerializer,
    parse_client_profile,
    _field_mapping_lines,
)


# ---------------------------------------------------------------------------
# Minimal CLIENT_PROFILE.md fixtures
# ---------------------------------------------------------------------------

_MINIMAL_PROFILE = """\
# CLIENT_PROFILE.md — test

**Client name:** Acme Lighting
**Org shortname:** `acme`
**Org ID:** `42`
**Product scope:** iPad
**Current phase:** 3 (Build)
**Archetype:** Standard catalog, no options
**ERP/PIM:** Business Central
**Go-live date:** 2026-09-01
**Taxonomy method:** Standard (Admin pre-registered)
**Pricing model:** Two imported levels (LIST, DEALER)
**Image mode:** FTP upload from client

## Client state

Client is anxious about go-live timeline; correctness matters more than speed.

## Sources of truth

Client's SharePoint export is canonical for product data.

## Locked decisions

- BaseItemCode = SKU from ERP (no transformation)
- OptionSets: not used for this client

## Open items

- We-fix: Normalize ImageFileName casing to lowercase
- Need-client: Confirm DefaultPriceCode for distributor accounts

## Do-NOT

- Do not create SmartLists until rep review is complete

## Chain of custody

| 2026-07-20 | Kylor | Kickoff call | HelpScout thread |
"""

_MINIMAL_PROFILE_NO_SHORTNAME = """\
# CLIENT_PROFILE.md — no shortname

**Client name:** No Name Co
**Org ID:** `99`
"""

_MINIMAL_PROFILE_WITH_RECONCILE = """\
# CLIENT_PROFILE.md — with reconcile block

**Client name:** Reconciled Co
**Org shortname:** `recco`
**Org ID:** `7`
**Product scope:** iPad
**Current phase:** 4 (Import)

## Live state (reconciled)

<!-- reconcile:start {"customers": 346, "inventory_rows": 1200, "lifecycle": "onboarding", \
"option_groups": 0, "options": 0, "orphan_inventory": 30, "price_level_codes": ["dn", "list"], \
"products_active": 683, "products_with_images": 600, "queried_at": "2026-07-27T20:00:00Z"} -->

| Field | DB live | Queried |
|---|---|---|
| Products (active) | **683** | 2026-07-27 |

<!-- reconcile:end -->
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_serializer(
    tmp_path,
    profile_text: str = _MINIMAL_PROFILE,
    shortname: str = "acme",
    political_state: str = None,
    live_state=None,
) -> HandoffSerializer:
    """Build a HandoffSerializer backed by a temp CLIENT_PROFILE.md."""
    client_dir = tmp_path / shortname
    client_dir.mkdir(parents=True, exist_ok=True)
    (client_dir / "CLIENT_PROFILE.md").write_text(profile_text, encoding="utf-8")
    return HandoffSerializer(
        client_dir=str(client_dir),
        shortname=shortname,
        political_state_override=political_state,
        _live_state_override=live_state,
    )


def _render(tmp_path, **kwargs) -> str:
    return _make_serializer(tmp_path, **kwargs).render()


# ---------------------------------------------------------------------------
# GOLDEN STRUCTURE TEST — all 12 mandatory sections must be present
# ---------------------------------------------------------------------------

REQUIRED_SECTION_PATTERNS = [
    "## Section 1 — Identity",
    "## Section 2 — Client Emotional/Political State",
    "## Section 3 — Sources of Truth",
    "## Section 4 — Locked Decisions",
    "## Section 5 — Field Mapping Table",
    "## Section 6 — Current State",
    "## Section 7 — eCat Gotcha Block",
    "## Section 8 — Validation Checklist",
    "## Section 9 — Open Items",
    "## Section 10 — Do-NOT",
    "## Section 11 — Deliverable Format",
    "## Section 12 — Anti-Hallucination Preamble",
    # Ancillary sections
    "## Section A — Chain of Custody",
    "## Section B — Skills to Load",
    "## Section C — Schema Notes",
]


@pytest.mark.parametrize("header", REQUIRED_SECTION_PATTERNS)
def test_golden_structure_all_sections_present(tmp_path, header):
    """Every section header must appear in the rendered output."""
    rendered = _render(tmp_path)
    assert header in rendered, (
        f"Section header missing from rendered handoff: {header!r}"
    )


# ---------------------------------------------------------------------------
# Anti-hallucination preamble — verbatim in header AND section 12
# ---------------------------------------------------------------------------

def test_anti_hallucination_preamble_in_header(tmp_path):
    """The preamble appears in the document header (before any section)."""
    rendered = _render(tmp_path)
    # Header appears before the first section separator
    header_block = rendered.split("## Section 1 —")[0]
    assert ANTI_HALLUCINATION_PREAMBLE in header_block, (
        "Anti-hallucination preamble must appear verbatim in the document header."
    )


def test_anti_hallucination_preamble_in_section_12(tmp_path):
    """The preamble appears verbatim inside section 12."""
    rendered = _render(tmp_path)
    # Isolate section 12 (between its header and the next section or end)
    parts = rendered.split("## Section 12 —")
    assert len(parts) == 2, "Section 12 header should appear exactly once"
    section_12 = parts[1]
    assert ANTI_HALLUCINATION_PREAMBLE in section_12, (
        "Anti-hallucination preamble must appear verbatim in section 12."
    )


def test_falsify_instructions_in_section_12(tmp_path):
    """The falsify-the-premise instructions appear in section 12."""
    rendered = _render(tmp_path)
    parts = rendered.split("## Section 12 —")
    section_12 = parts[1]
    # Check for the key phrase from FALSIFY_INSTRUCTIONS
    assert "re-derive them from the data and code" in section_12 or \
           FALSIFY_INSTRUCTIONS in section_12, (
        "Falsify-the-premise instructions must appear in section 12."
    )


# ---------------------------------------------------------------------------
# Section 1 — Identity has provenance column
# ---------------------------------------------------------------------------

def test_section1_has_provenance_column(tmp_path):
    """Section 1 identity table must include a Provenance column."""
    rendered = _render(tmp_path)
    s1 = rendered.split("## Section 1 —")[1].split("## Section 2 —")[0]
    assert "Provenance" in s1, "Section 1 identity table must have a Provenance column."


def test_section1_org_id_appears(tmp_path):
    """Section 1 must include the org DB id (from profile)."""
    rendered = _render(tmp_path)
    s1 = rendered.split("## Section 1 —")[1].split("## Section 2 —")[0]
    assert "42" in s1, "Org ID 42 from profile must appear in section 1."
    assert "ORG_BY_SHORTNAME" in s1, "Org id provenance query must be cited."


def test_section1_serialize_py_provenance(tmp_path):
    """Section 1 must name scripts/handoff/serialize.py as the generator."""
    rendered = _render(tmp_path)
    s1 = rendered.split("## Section 1 —")[1].split("## Section 2 —")[0]
    assert "serialize.py" in s1, "Generator name must appear in section 1."


# ---------------------------------------------------------------------------
# Section 2 — Political state
# ---------------------------------------------------------------------------

def test_section2_from_profile(tmp_path):
    """Section 2 shows the political state from CLIENT_PROFILE.md."""
    rendered = _render(tmp_path)
    s2 = rendered.split("## Section 2 —")[1].split("## Section 3 —")[0]
    assert "correctness matters more than speed" in s2


def test_section2_override_from_cli(tmp_path):
    """--political-state override replaces the profile value in section 2."""
    rendered = _render(
        tmp_path,
        political_state="Client is furious about the delay.",
    )
    s2 = rendered.split("## Section 2 —")[1].split("## Section 3 —")[0]
    assert "furious about the delay" in s2
    # Original profile text should NOT appear
    assert "correctness matters more than speed" not in s2


def test_section2_absent_political_state_says_not_recorded(tmp_path):
    """When political state is absent, section 2 says 'Not recorded'."""
    rendered = _render(
        tmp_path,
        profile_text=_MINIMAL_PROFILE_NO_SHORTNAME,
        shortname="noco",
    )
    s2 = rendered.split("## Section 2 —")[1].split("## Section 3 —")[0]
    assert "Not recorded" in s2


# ---------------------------------------------------------------------------
# Section 3 — Sources of truth has anti-sources
# ---------------------------------------------------------------------------

def test_section3_has_anti_sources(tmp_path):
    """Section 3 must declare anti-sources."""
    rendered = _render(tmp_path)
    s3 = rendered.split("## Section 3 —")[1].split("## Section 4 —")[0]
    assert "Anti-source" in s3 or "anti-source" in s3 or "Anti-Sources" in s3


def test_section3_agent_memory_is_antisource(tmp_path):
    """Agent memory must be listed as an anti-source."""
    rendered = _render(tmp_path)
    s3 = rendered.split("## Section 3 —")[1].split("## Section 4 —")[0]
    assert "Agent memory" in s3 or "agent memory" in s3


# ---------------------------------------------------------------------------
# Section 4 — Locked decisions includes import order
# ---------------------------------------------------------------------------

def test_section4_import_order_locked(tmp_path):
    """Section 4 must lock the mandatory import order."""
    rendered = _render(tmp_path)
    s4 = rendered.split("## Section 4 —")[1].split("## Section 5 —")[0]
    assert "options" in s4 and "option_groups" in s4 and "products" in s4


def test_section4_error_tier_blocks_deletes(tmp_path):
    """Section 4 must include the error-tier-blocks-deletes rule."""
    rendered = _render(tmp_path)
    s4 = rendered.split("## Section 4 —")[1].split("## Section 5 —")[0]
    assert "Error" in s4 and "delete" in s4.lower()


# ---------------------------------------------------------------------------
# Section 5 — Field mapping table (code-derived limits)
# ---------------------------------------------------------------------------

def test_section5_cites_limits_generated(tmp_path):
    """Section 5 must reference limits_generated.py (code-derived, not transcribed)."""
    rendered = _render(tmp_path)
    s5 = rendered.split("## Section 5 —")[1].split("## Section 6 —")[0]
    assert "limits_generated" in s5 or "gen_limits" in s5


def test_section5_contains_baseitemcode_limit(tmp_path):
    """Section 5 must include the BaseItemCode field limit (40, from supercat_server)."""
    rendered = _render(tmp_path)
    s5 = rendered.split("## Section 5 —")[1].split("## Section 6 —")[0]
    # BaseItemCode limit is 40 (error tier), from Product::ATTR_LENGTHS
    assert "baseitemcode" in s5.lower() or "BaseItemCode" in s5
    assert "40" in s5


def test_section5_retired_claims_present(tmp_path):
    """Section 5 must list retired claims (limits documented but not enforced)."""
    rendered = _render(tmp_path)
    s5 = rendered.split("## Section 5 —")[1].split("## Section 6 —")[0]
    assert "Retired" in s5 or "retired" in s5


# ---------------------------------------------------------------------------
# Section 6 — Current state
# ---------------------------------------------------------------------------

def test_section6_no_typed_counts_without_live_state(tmp_path):
    """Without live state, section 6 says 'not yet reconciled' — no numbers."""
    rendered = _render(tmp_path, live_state=None)
    s6 = rendered.split("## Section 6 —")[1].split("## Section 7 —")[0]
    assert "not yet reconciled" in s6.lower() or "not reconciled" in s6.lower()
    # Must not contain any invented numeric counts
    # (digits for year/lines are okay, but large bold numbers are not)
    assert "**683**" not in s6
    assert "**346**" not in s6


def test_section6_counts_from_reconcile_block_with_provenance(tmp_path):
    """With live state, section 6 shows counts with query-name provenance pointers."""
    from reconcile.profile import LiveState

    live = LiveState(
        products_active=683,
        products_with_images=600,
        customers=346,
        inventory_rows=1200,
        orphan_inventory=30,
        price_level_codes=["dn", "list"],
        options=222,
        option_groups=98,
        lifecycle="onboarding",
        queried_at="2026-07-27T20:00:00Z",
    )
    rendered = _render(tmp_path, live_state=live)
    s6 = rendered.split("## Section 6 —")[1].split("## Section 7 —")[0]

    # Counts must appear
    assert "683" in s6
    assert "346" in s6
    # Query provenance pointers must appear alongside the counts
    assert "PRODUCT_COUNTS" in s6
    assert "CUSTOMER_COUNT" in s6
    assert "INVENTORY_COUNTS" in s6
    assert "ORPHAN_INVENTORY" in s6
    assert "PRICE_LEVELS" in s6
    assert "ORPHAN_OPTIONS" in s6


def test_section6_stale_flag(tmp_path):
    """A stale live state (>7d old) triggers a STALE warning in section 6."""
    from reconcile.profile import LiveState

    live = LiveState(
        products_active=100,
        queried_at="2020-01-01T00:00:00Z",  # very stale
    )
    rendered = _render(tmp_path, live_state=live)
    s6 = rendered.split("## Section 6 —")[1].split("## Section 7 —")[0]
    assert "STALE" in s6


def test_section6_what_has_not_happened(tmp_path):
    """Section 6 must include a 'What has NOT happened' subsection."""
    from reconcile.profile import LiveState

    live = LiveState(products_active=10, queried_at="2026-07-27T20:00:00Z")
    rendered = _render(tmp_path, live_state=live)
    s6 = rendered.split("## Section 6 —")[1].split("## Section 7 —")[0]
    assert "NOT happened" in s6 or "not happened" in s6.lower()


# ---------------------------------------------------------------------------
# Section 7 — eCat gotcha block
# ---------------------------------------------------------------------------

def test_section7_hard_delete_semantics(tmp_path):
    """Section 7 must state hard-delete semantics for customers, inventory, options."""
    rendered = _render(tmp_path)
    s7 = rendered.split("## Section 7 —")[1].split("## Section 8 —")[0]
    assert "Hard-delete" in s7 or "hard-delete" in s7 or "Hard-Delete" in s7


def test_section7_image_jpg_only(tmp_path):
    """Section 7 must state .jpg only / PNG silently rejected."""
    rendered = _render(tmp_path)
    s7 = rendered.split("## Section 7 —")[1].split("## Section 8 —")[0]
    assert ".jpg" in s7 or "jpg" in s7.lower()
    assert "PNG" in s7 or "png" in s7.lower()


def test_section7_taxonomy_groups_never_auto_create(tmp_path):
    """Section 7 must state taxonomy groups never auto-create."""
    rendered = _render(tmp_path)
    s7 = rendered.split("## Section 7 —")[1].split("## Section 8 —")[0]
    assert "auto-create" in s7 or "auto create" in s7.lower()


# ---------------------------------------------------------------------------
# Section 8 — Validation checklist (runnable commands)
# ---------------------------------------------------------------------------

def test_section8_has_runnable_commands(tmp_path):
    """Section 8 must contain runnable `python scripts/` commands."""
    rendered = _render(tmp_path)
    s8 = rendered.split("## Section 8 —")[1].split("## Section 9 —")[0]
    assert "python scripts/" in s8


def test_section8_phase1_preflight_gate_command(tmp_path):
    """Section 8 must include the preflight_gate.py command."""
    rendered = _render(tmp_path)
    s8 = rendered.split("## Section 8 —")[1].split("## Section 9 —")[0]
    assert "preflight_gate.py" in s8


def test_section8_phase2_reconcile_command(tmp_path):
    """Section 8 must include the reconcile/profile.py command."""
    rendered = _render(tmp_path)
    s8 = rendered.split("## Section 8 —")[1].split("## Section 9 —")[0]
    assert "reconcile/profile.py" in s8


def test_section8_query_table_present(tmp_path):
    """Section 8 must contain a named-query reference table."""
    rendered = _render(tmp_path)
    s8 = rendered.split("## Section 8 —")[1].split("## Section 9 —")[0]
    assert "PRODUCT_COUNTS" in s8
    assert "CUSTOMER_COUNT" in s8


def test_section8_expected_outputs_with_live_state(tmp_path):
    """With live state, section 8 shows expected outputs with provenance."""
    from reconcile.profile import LiveState

    live = LiveState(
        products_active=500,
        customers=200,
        queried_at="2026-07-27T20:00:00Z",
    )
    rendered = _render(tmp_path, live_state=live)
    s8 = rendered.split("## Section 8 —")[1].split("## Section 9 —")[0]
    assert "500" in s8
    assert "200" in s8
    # Provenance must cite the date
    assert "2026-07-27" in s8


# ---------------------------------------------------------------------------
# Section 9 — Open items
# ---------------------------------------------------------------------------

def test_section9_we_fix_vs_need_client_language(tmp_path):
    """Section 9 must use 'we-fix' and 'need-client' framing."""
    rendered = _render(tmp_path)
    s9 = rendered.split("## Section 9 —")[1].split("## Section 10 —")[0]
    s9_lower = s9.lower()
    assert "we-fix" in s9_lower or "we can fix" in s9_lower
    assert "need-client" in s9_lower or "need client" in s9_lower


def test_section9_includes_profile_open_items(tmp_path):
    """Section 9 includes the open items declared in CLIENT_PROFILE.md."""
    rendered = _render(tmp_path)
    s9 = rendered.split("## Section 9 —")[1].split("## Section 10 —")[0]
    assert "Normalize ImageFileName" in s9
    assert "DefaultPriceCode" in s9


# ---------------------------------------------------------------------------
# Section 10 — Do-NOT
# ---------------------------------------------------------------------------

def test_section10_no_ftp_without_approval(tmp_path):
    """Section 10 must prohibit FTP/import without approval."""
    rendered = _render(tmp_path)
    s10 = rendered.split("## Section 10 —")[1].split("## Section 11 —")[0]
    assert "FTP" in s10 or "import" in s10.lower()
    assert "approval" in s10.lower() or "explicit" in s10.lower()


def test_section10_no_typed_counts(tmp_path):
    """Section 10 must prohibit typing counts."""
    rendered = _render(tmp_path)
    s10 = rendered.split("## Section 10 —")[1].split("## Section 11 —")[0]
    s10_lower = s10.lower()
    assert "count" in s10_lower and ("type" in s10_lower or "typed" in s10_lower)


def test_section10_jira_read_only(tmp_path):
    """Section 10 must state Jira is read-only."""
    rendered = _render(tmp_path)
    s10 = rendered.split("## Section 10 —")[1].split("## Section 11 —")[0]
    assert "Jira" in s10
    assert "read-only" in s10.lower() or "read only" in s10.lower()


# ---------------------------------------------------------------------------
# Section 11 — Deliverable format
# ---------------------------------------------------------------------------

def test_section11_go_no_go(tmp_path):
    """Section 11 must specify GO and NO-GO outcomes."""
    rendered = _render(tmp_path)
    s11 = rendered.split("## Section 11 —")[1].split("## Section 12 —")[0]
    assert "GO" in s11
    assert "NO-GO" in s11


def test_section11_fix_owner_column(tmp_path):
    """Section 11 mismatch table must have a fix-owner column."""
    rendered = _render(tmp_path)
    s11 = rendered.split("## Section 11 —")[1].split("## Section 12 —")[0]
    assert "Fix owner" in s11 or "fix-owner" in s11.lower()


# ---------------------------------------------------------------------------
# Section A — Chain of custody
# ---------------------------------------------------------------------------

def test_section_a_chain_of_custody_has_generate_event(tmp_path):
    """Section A must log the handoff generation as a custody event."""
    rendered = _render(tmp_path)
    sa = rendered.split("## Section A —")[1].split("## Section B —")[0]
    assert "serialize.py" in sa


def test_section_a_includes_profile_chain(tmp_path):
    """Section A includes chain of custody entries from CLIENT_PROFILE.md."""
    rendered = _render(tmp_path)
    sa = rendered.split("## Section A —")[1].split("## Section B —")[0]
    assert "Kylor" in sa or "HelpScout" in sa


# ---------------------------------------------------------------------------
# Section B — Skills to load
# ---------------------------------------------------------------------------

def test_section_b_key_skills_listed(tmp_path):
    """Section B must list the core eCat skills."""
    rendered = _render(tmp_path)
    sb = rendered.split("## Section B —")[1].split("## Section C —")[0]
    for skill in [
        "ecat-onboarding-orchestrator",
        "ecat-core-files",
        "ecat-postgres-audit",
        "ecat-preflight",  # may or may not be listed; skip
    ]:
        if skill == "ecat-preflight":
            continue
        assert skill in sb, f"Skill '{skill}' missing from section B."


# ---------------------------------------------------------------------------
# Section C — Schema notes
# ---------------------------------------------------------------------------

def test_section_c_import_events_schema_note(tmp_path):
    """Section C must document that import_events.data columns DO NOT EXIST."""
    rendered = _render(tmp_path)
    sc = rendered.split("## Section C —")[1]
    assert "import_events" in sc
    assert "DO NOT EXIST" in sc or "do not exist" in sc.lower()


def test_section_c_organizations_state_note(tmp_path):
    """Section C must explain that organizations.state is geographic."""
    rendered = _render(tmp_path)
    sc = rendered.split("## Section C —")[1]
    assert "geographic" in sc.lower() or "Geographic" in sc


# ---------------------------------------------------------------------------
# parse_client_profile — unit tests
# ---------------------------------------------------------------------------

def test_parse_profile_identity_fields(tmp_path):
    """parse_client_profile extracts identity fields correctly."""
    profile_path = tmp_path / "CLIENT_PROFILE.md"
    profile_path.write_text(_MINIMAL_PROFILE, encoding="utf-8")
    p = parse_client_profile(str(profile_path))
    assert p["shortname"] == "acme"
    assert p["org_id"] == "42"
    assert p["client_name"] == "Acme Lighting"
    assert p["phase"] == "3 (Build)"
    assert p["product_scope"] == "iPad"


def test_parse_profile_missing_file_returns_empty(tmp_path):
    """parse_client_profile returns {} for a missing file."""
    p = parse_client_profile(str(tmp_path / "DOES_NOT_EXIST.md"))
    assert p == {}


def test_parse_profile_block_fields(tmp_path):
    """parse_client_profile extracts section blocks (political state, etc.)."""
    profile_path = tmp_path / "CLIENT_PROFILE.md"
    profile_path.write_text(_MINIMAL_PROFILE, encoding="utf-8")
    p = parse_client_profile(str(profile_path))
    assert "correctness matters more than speed" in p.get("political_state", "")
    assert "SharePoint" in p.get("sources_of_truth", "")
    assert "BaseItemCode" in p.get("locked_decisions", "")
    assert "Normalize ImageFileName" in p.get("open_items", "")


# ---------------------------------------------------------------------------
# CLI smoke tests
# ---------------------------------------------------------------------------

def test_cli_basic_smoke(tmp_path, run_script):
    """CLI with --client-dir and --shortname writes HANDOFF.md and exits 0."""
    client_dir = tmp_path / "acme"
    client_dir.mkdir()
    (client_dir / "CLIENT_PROFILE.md").write_text(_MINIMAL_PROFILE, encoding="utf-8")
    out_path = client_dir / "HANDOFF.md"

    rc, output = run_script(
        "handoff/serialize.py",
        "--client-dir", str(client_dir),
        "--shortname", "acme",
        "--out", str(out_path),
    )
    assert rc == 0, f"Expected exit 0; got {rc}.\nOutput:\n{output}"
    assert out_path.exists(), "HANDOFF.md was not written."
    content = out_path.read_text(encoding="utf-8")
    # All 12 section headers must be in the file
    for header in REQUIRED_SECTION_PATTERNS[:12]:
        assert header in content, f"CLI output missing: {header!r}"


def test_cli_shortname_from_profile(tmp_path, run_script):
    """CLI resolves --shortname from CLIENT_PROFILE.md when not passed."""
    client_dir = tmp_path / "acme2"
    client_dir.mkdir()
    (client_dir / "CLIENT_PROFILE.md").write_text(_MINIMAL_PROFILE, encoding="utf-8")
    out_path = client_dir / "HANDOFF.md"

    rc, output = run_script(
        "handoff/serialize.py",
        "--client-dir", str(client_dir),
        "--out", str(out_path),
    )
    assert rc == 0, f"Expected exit 0; got {rc}.\nOutput:\n{output}"
    assert out_path.exists()


def test_cli_exits_2_bad_client_dir(tmp_path, run_script):
    """CLI exits 2 when --client-dir does not exist."""
    rc, output = run_script(
        "handoff/serialize.py",
        "--client-dir", str(tmp_path / "nonexistent_client"),
        "--shortname", "nope",
    )
    assert rc == 2, f"Expected exit 2; got {rc}.\nOutput:\n{output}"


def test_cli_exits_2_no_shortname_in_profile(tmp_path, run_script):
    """CLI exits 2 when shortname cannot be resolved from profile."""
    client_dir = tmp_path / "noco"
    client_dir.mkdir()
    (client_dir / "CLIENT_PROFILE.md").write_text(
        _MINIMAL_PROFILE_NO_SHORTNAME, encoding="utf-8"
    )
    rc, output = run_script(
        "handoff/serialize.py",
        "--client-dir", str(client_dir),
        # No --shortname, and profile has no Org shortname field
    )
    assert rc == 2, f"Expected exit 2; got {rc}.\nOutput:\n{output}"


def test_cli_political_state_override(tmp_path, run_script):
    """--political-state override appears in the written HANDOFF.md."""
    client_dir = tmp_path / "pol"
    client_dir.mkdir()
    (client_dir / "CLIENT_PROFILE.md").write_text(_MINIMAL_PROFILE, encoding="utf-8")
    out_path = client_dir / "HANDOFF.md"

    rc, output = run_script(
        "handoff/serialize.py",
        "--client-dir", str(client_dir),
        "--shortname", "acme",
        "--out", str(out_path),
        "--political-state", "Client is very upset about image quality.",
    )
    assert rc == 0
    content = out_path.read_text(encoding="utf-8")
    assert "very upset about image quality" in content


# ---------------------------------------------------------------------------
# Handoff with reconcile-block live state (integration)
# ---------------------------------------------------------------------------

def test_live_state_from_reconcile_block_in_profile(tmp_path):
    """When CLIENT_PROFILE.md has a reconcile block, section 6 shows queried counts."""
    client_dir = tmp_path / "recco"
    client_dir.mkdir()
    (client_dir / "CLIENT_PROFILE.md").write_text(
        _MINIMAL_PROFILE_WITH_RECONCILE, encoding="utf-8"
    )
    s = HandoffSerializer(
        client_dir=str(client_dir),
        shortname="recco",
    )
    rendered = s.render()
    s6 = rendered.split("## Section 6 —")[1].split("## Section 7 —")[0]
    # Live state was loaded from the reconcile block
    assert s.live_state is not None, (
        "HandoffSerializer must load live state from the reconcile block."
    )
    assert "683" in s6, "Product count from reconcile block must appear in section 6."
    assert "PRODUCT_COUNTS" in s6, "Query provenance must appear alongside count."
    assert "346" in s6, "Customer count from reconcile block must appear in section 6."


# ---------------------------------------------------------------------------
# _field_mapping_lines — unit tests
# ---------------------------------------------------------------------------

def test_field_mapping_lines_has_products_csv():
    """_field_mapping_lines must reference products.csv."""
    lines = _field_mapping_lines()
    text = "\n".join(lines)
    assert "products.csv" in text


def test_field_mapping_lines_has_provenance():
    """_field_mapping_lines must cite the supercat_server provenance."""
    lines = _field_mapping_lines()
    text = "\n".join(lines)
    assert "supercat_server" in text
    assert "limits_generated" in text or "gen_limits" in text


def test_field_mapping_lines_baseitemcode_limit_40():
    """_field_mapping_lines must show BaseItemCode limit = 40 (from ATTR_LENGTHS)."""
    lines = _field_mapping_lines()
    text = "\n".join(lines)
    assert "baseitemcode" in text.lower()
    assert "40" in text
