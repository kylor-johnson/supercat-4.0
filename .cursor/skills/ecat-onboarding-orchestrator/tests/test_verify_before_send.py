"""Tests for verify/before_send.py — Phase 3 pre-send checker.

Two corpus-backed scenarios are the load-bearing cases:

  1. tcd / DefaultPriceCode=0  — ERP placeholder code caused 100% customer rejection.
     A draft that names a price code not in the org's price_levels must be flagged
     CONTRADICTED. (IMPLEMENTATION_PLAN.md §2.1, Appendix B)

  2. Magic Lite image false-positive — agent declared GDL-6, DL-FR, RGL-FR broken
     from catalog text; screenshots proved all three correct. A draft claiming a SKU
     image is broken when UPLOADED_IMAGES already has the file must be flagged
     CONTRADICTED. (IMPLEMENTATION_PLAN.md §5.3)

Additional tests cover:
  - The 9-step contract is present in rendered output
  - Verified claims (live count matches draft)
  - Unverifiable claims (no live state)
  - Exit code contract (0=safe, 1=not-safe, 2=could-not-complete)
  - CLI smoke tests
  - Prior-error-pattern detection
  - Entity disambiguation (four states)
"""

import json
import sys
import textwrap
from pathlib import Path
from typing import Dict, List

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from verify.before_send import (
    CONTRADICTED,
    KIND_COUNT,
    KIND_IMAGE_STATUS,
    KIND_PRICE_CODE,
    UNVERIFIABLE,
    VERIFIED,
    PreSendChecker,
    PreSendReport,
    _PRIOR_ERROR_PATTERNS,
    _detect_magic_lite_image_false_positive,
    _detect_tcd_default_price_code,
    extract_claims,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_checker(draft_text: str, live: Dict, client_dir=None, shortname=None):
    return PreSendChecker(
        draft_path="test_draft.md",
        draft_text=draft_text,
        client_dir=client_dir,
        shortname=shortname,
        live=live,
    )


def _claims_of_kind(claims, kind):
    return [c for c in claims if c.kind == kind]


def _by_status(claims):
    out = {}
    for c in claims:
        out.setdefault(c.status, []).append(c)
    return out


# ---------------------------------------------------------------------------
# CORPUS SCENARIO 1: tcd / DefaultPriceCode=0
#
# Context: Terracotta's ERP exported DefaultPriceCode=0.  The importer
# rejected every customer row because '0' is not a price level code.
# A draft that asserts 'DefaultPriceCode=0' or a price level that does not
# exist for this org must be caught as CONTRADICTED.
# IMPLEMENTATION_PLAN.md §2.1, Appendix B.
# ---------------------------------------------------------------------------


class TestTcdDefaultPriceCode:
    """tcd / DefaultPriceCode=0 — the canonical 100%-customer-rejection scenario."""

    LIVE_TCD = {
        "shortname": "tcd",
        "queried_at": "2026-07-27T20:00:00Z",
        "price_levels": ["dn", "tcnet", "list"],
        "counts": {"customers.csv": 346},
    }

    def test_draft_asserting_zero_code_is_contradicted(self):
        """DefaultPriceCode=0 is named in draft; 0 is not in tcd's price levels."""
        draft = textwrap.dedent("""\
            Hi Team,

            We've set your customer file to use DefaultPriceCode=0 for all accounts.
            This matches your ERP export. Please re-import and let us know if it works.
        """)
        claims = extract_claims(draft, self.LIVE_TCD)
        price_claims = _claims_of_kind(claims, KIND_PRICE_CODE)
        assert price_claims, "Expected at least one price_code claim to be extracted"
        contradicted = [c for c in price_claims if c.status == CONTRADICTED]
        assert contradicted, (
            "DefaultPriceCode=0 should be CONTRADICTED — '0' is not in tcd price levels "
            f"({self.LIVE_TCD['price_levels']})"
        )
        # Evidence must name the query, not a typed count
        for c in contradicted:
            assert "PRICE_LEVELS" in c.query_name or "PRICE_LEVELS" in c.evidence

    def test_draft_asserting_net_price_level_is_contradicted(self):
        """Draft names 'NET' price code; tcd's levels are dn/tcnet/list."""
        draft = "Please ensure DefaultPriceCode=NET is set for all customers."
        claims = extract_claims(draft, self.LIVE_TCD)
        price_claims = _claims_of_kind(claims, KIND_PRICE_CODE)
        contradicted = [c for c in price_claims if c.status == CONTRADICTED]
        assert contradicted, "'NET' is not a valid price level for tcd"
        assert any("NET" in c.text.upper() or "net" in c.evidence.lower()
                   for c in contradicted)

    def test_draft_asserting_valid_code_is_verified(self):
        """DefaultPriceCode=dn is a real tcd price level — must be VERIFIED."""
        draft = "All customers should use DefaultPriceCode=dn going forward."
        claims = extract_claims(draft, self.LIVE_TCD)
        price_claims = _claims_of_kind(claims, KIND_PRICE_CODE)
        verified = [c for c in price_claims if c.status == VERIFIED]
        assert verified, "'dn' is a valid tcd price level and should be VERIFIED"

    def test_verdict_is_not_safe_when_price_code_contradicted(self):
        """A CONTRADICTED price code claim produces a not-safe-to-send verdict."""
        draft = "Set DefaultPriceCode=0 for all customers in the file."
        checker = _make_checker(draft, self.LIVE_TCD, shortname="tcd")
        report = checker.run()
        assert report.verdict_label == "not-safe-to-send"
        assert report.exit_code == 1

    def test_tcd_prior_pattern_fires_for_zero_code(self):
        """The tcd/DefaultPriceCode pattern detector fires on '0'."""
        draft = "DefaultPriceCode=0 is set in the exported file."
        assert _detect_tcd_default_price_code(draft, self.LIVE_TCD)

    def test_tcd_prior_pattern_does_not_fire_for_valid_code(self):
        """Pattern must not fire when the code IS in the org's price levels."""
        draft = "DefaultPriceCode=dn is used throughout the customer file."
        assert not _detect_tcd_default_price_code(draft, self.LIVE_TCD)

    def test_tcd_pattern_fires_in_report_prior_errors_section(self):
        """Step 4 of the report must name the tcd pattern when '0' appears."""
        draft = "We've set DefaultPriceCode=0 for all bill-to rows."
        checker = _make_checker(draft, self.LIVE_TCD, shortname="tcd")
        report = checker.run()
        rendered = report.render()
        assert "tcd/DefaultPriceCode" in rendered
        assert "Step 4" in rendered

    def test_success_claim_contradicted_when_customer_count_is_zero(self):
        """Draft says import succeeded; live shows 0 customers → CONTRADICTED."""
        live_zero = {
            "shortname": "tcd",
            "queried_at": "2026-07-27T20:00:00Z",
            "price_levels": ["dn"],
            "counts": {"customers.csv": 0},
        }
        draft = textwrap.dedent("""\
            Good news — we have successfully imported your customer file.
            All 346 customers are now live in your eCat account.
        """)
        claims = extract_claims(draft, live_zero)
        # Both the count claim (346 customers) and the success claim should fire
        contradicted = [c for c in claims if c.status == CONTRADICTED]
        assert contradicted, (
            "Draft claims 346 customers but live shows 0; should be CONTRADICTED"
        )

    def test_count_claim_verified_when_live_matches(self):
        """346 customers in draft matches live count → VERIFIED."""
        draft = "Your catalog now shows 346 customers loaded into eCat."
        claims = extract_claims(draft, self.LIVE_TCD)
        count_claims = _claims_of_kind(claims, KIND_COUNT)
        customer_claims = [c for c in count_claims if "customer" in c.text.lower()
                           or "346" in c.text]
        verified = [c for c in customer_claims if c.status == VERIFIED]
        assert verified, "346 customers matches LIVE_TCD count and should be VERIFIED"
        # Must cite a query name, not a typed count
        assert all("CUSTOMER_COUNT" in c.query_name or "CUSTOMER_COUNT" in c.evidence
                   for c in verified)


# ---------------------------------------------------------------------------
# CORPUS SCENARIO 2: Magic Lite image false-positive
#
# Context: An agent read the live catalog text and declared GDL-6, DL-FR, and
# RGL-FR images "broken." Hours later a second agent with per-SKU screenshots
# found all three already correct. The uploaded_images in the live org already
# contained the files. A draft claiming these images need re-upload is
# CONTRADICTED by UPLOADED_IMAGES evidence.
# IMPLEMENTATION_PLAN.md §5.3.
# ---------------------------------------------------------------------------


class TestMagicLiteImageFalsePositive:
    """Magic Lite image false-positive — catalog text vs. live upload state."""

    LIVE_MALI = {
        "shortname": "mali",
        "queried_at": "2026-07-27T20:00:00Z",
        "uploaded_images": ["GDL-6.jpg", "DL-FR.jpg", "RGL-FR.jpg", "ML-001.jpg"],
        "counts": {"products.csv": 683},
        "price_levels": ["mllist", "mldn"],
    }

    def test_broken_image_claim_for_uploaded_sku_is_contradicted(self):
        """Claiming GDL-6 image is broken while GDL-6.jpg IS uploaded → CONTRADICTED."""
        draft = textwrap.dedent("""\
            Hi Magic Lite team,

            We identified the following SKUs with broken images that need re-uploading:
            - GDL-6 image is missing from the iPad catalog
            - DL-FR image is broken and not displaying
            - RGL-FR image is not showing up for reps

            We will re-upload these three files.
        """)
        claims = extract_claims(draft, self.LIVE_MALI)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        assert image_claims, "Expected image-status claims for GDL-6, DL-FR, RGL-FR"
        contradicted = [c for c in image_claims if c.status == CONTRADICTED]
        assert contradicted, (
            "GDL-6, DL-FR, RGL-FR are all in uploaded_images — "
            "broken claims must be CONTRADICTED"
        )
        # All three SKUs should be contradicted
        contradicted_texts = " ".join(c.text.lower() for c in contradicted)
        assert "gdl-6" in contradicted_texts or "gdl" in contradicted_texts

    def test_evidence_cites_uploaded_images_query(self):
        """Contradiction evidence must cite UPLOADED_IMAGES query, not a typed count."""
        draft = "The GDL-6 image is broken and needs re-uploading."
        claims = extract_claims(draft, self.LIVE_MALI)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        contradicted = [c for c in image_claims if c.status == CONTRADICTED]
        assert contradicted
        for c in contradicted:
            assert "UPLOADED_IMAGES" in c.query_name or "UPLOADED_IMAGES" in c.evidence

    def test_broken_claim_for_absent_sku_is_verified(self):
        """Claiming a NOT-uploaded image is broken is VERIFIED, not CONTRADICTED."""
        live_partial = {**self.LIVE_MALI, "uploaded_images": ["ML-001.jpg"]}
        draft = "The GDL-6 image is missing from the iPad."
        claims = extract_claims(draft, live_partial)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        verified = [c for c in image_claims if c.status == VERIFIED]
        assert verified, (
            "GDL-6.jpg is NOT in uploaded_images — 'missing' claim should be VERIFIED"
        )

    def test_verdict_not_safe_for_false_broken_image_claim(self):
        """A CONTRADICTED image claim makes the draft not-safe-to-send."""
        draft = "GDL-6 image is broken. Please re-upload immediately."
        checker = _make_checker(draft, self.LIVE_MALI, shortname="mali")
        report = checker.run()
        assert report.verdict_label == "not-safe-to-send"
        assert report.exit_code == 1

    def test_magic_lite_pattern_fires_for_uploaded_broken_claim(self):
        """The Mali/MagicLite pattern detector fires when uploaded file is called broken."""
        draft = "The GDL-6 image is broken and not showing on the iPad."
        assert _detect_magic_lite_image_false_positive(draft, self.LIVE_MALI)

    def test_magic_lite_pattern_does_not_fire_when_image_absent(self):
        """Pattern must not fire when the image genuinely is absent from uploads."""
        live_empty = {**self.LIVE_MALI, "uploaded_images": []}
        draft = "The GDL-6 image is broken and not showing on the iPad."
        assert not _detect_magic_lite_image_false_positive(draft, live_empty)

    def test_magic_lite_pattern_fires_in_report_step4(self):
        """Step 4 must name the Magic Lite pattern when it fires."""
        draft = "DL-FR image is missing and needs re-upload."
        checker = _make_checker(draft, self.LIVE_MALI, shortname="mali")
        report = checker.run()
        rendered = report.render()
        assert "mali/MagicLite" in rendered or "MagicLite" in rendered
        assert "Step 4" in rendered

    def test_no_false_positive_when_no_broken_keyword(self):
        """Mentioning a SKU without a 'broken/missing' keyword must NOT trigger image claim."""
        draft = "We have GDL-6 in the catalog with a hero image."
        claims = extract_claims(draft, self.LIVE_MALI)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        # Should produce no image-status contradiction (no broken keyword)
        contradicted = [c for c in image_claims if c.status == CONTRADICTED]
        assert not contradicted, (
            "SKU mention without 'broken/missing' keyword should not fire image contradiction"
        )


# ---------------------------------------------------------------------------
# Contract: 9-step report structure
# ---------------------------------------------------------------------------


class TestNineStepContract:
    """Every run must produce all 9 required sections."""

    LIVE = {
        "shortname": "test",
        "queried_at": "2026-07-27T20:00:00Z",
        "price_levels": ["dn"],
        "counts": {"products.csv": 100},
    }

    def _report(self, draft="Hello team, all products are imported."):
        checker = _make_checker(draft, self.LIVE, shortname="test")
        return checker.run()

    def test_step1_stakes_present(self):
        assert "Step 1" in self._report().render()
        assert "Stakes" in self._report().render()

    def test_step2_void_prior_analysis(self):
        rendered = self._report().render()
        assert "Step 2" in rendered
        assert "Prior Analysis" in rendered

    def test_step3_three_evidence_tiers(self):
        rendered = self._report().render()
        assert "Step 3" in rendered
        assert "Tier 1" in rendered
        assert "Tier 2" in rendered
        assert "Tier 3" in rendered

    def test_step4_prior_errors_section(self):
        rendered = self._report().render()
        assert "Step 4" in rendered

    def test_step5_files_enumerated(self):
        rendered = self._report().render()
        assert "Step 5" in rendered
        assert "Files Enumerated" in rendered

    def test_step6_entity_disambiguation(self):
        rendered = self._report().render()
        assert "Step 6" in rendered
        assert "Disambiguation" in rendered

    def test_step7_full_draft_text(self):
        draft = "Hello team."
        report = _make_checker(draft, self.LIVE).run()
        rendered = report.render()
        assert "Step 7" in rendered
        assert "Hello team." in rendered

    def test_step8_claim_analysis_table(self):
        rendered = self._report().render()
        assert "Step 8" in rendered
        assert "Claim Analysis" in rendered

    def test_step9_verdict(self):
        rendered = self._report().render()
        assert "Step 9" in rendered
        assert "SAFE-TO-SEND" in rendered or "NOT-SAFE-TO-SEND" in rendered

    def test_tier2_rules_cite_code_authority(self):
        """Tier 2 must reference importer code, not just documentation."""
        rendered = self._report().render()
        assert "cdn_image_sync" in rendered or "ATTR_LENGTHS" in rendered or \
               "validate_customers" in rendered

    def test_report_names_shortname_and_query_timestamp(self):
        rendered = self._report().render()
        assert "test" in rendered
        assert "2026-07-27T20:00:00Z" in rendered


# ---------------------------------------------------------------------------
# Claim classification rules
# ---------------------------------------------------------------------------


class TestClaimClassification:
    """Unit tests for extract_claims() — all classification branches."""

    def test_no_claims_from_empty_draft(self):
        assert extract_claims("", {}) == []

    def test_no_claims_without_live_state(self):
        # Claims are extracted but status is UNVERIFIABLE
        claims = extract_claims("We have 100 products ready to import.", {})
        assert claims
        assert all(c.status == UNVERIFIABLE for c in claims)

    def test_count_claim_verified_exact_match(self):
        live = {"counts": {"products.csv": 100}}
        claims = extract_claims("Your catalog now has 100 products.", live)
        count_claims = _claims_of_kind(claims, KIND_COUNT)
        assert any(c.status == VERIFIED for c in count_claims)

    def test_count_claim_contradicted_on_mismatch(self):
        live = {"counts": {"products.csv": 50}}
        claims = extract_claims("Your catalog now has 100 products.", live)
        count_claims = _claims_of_kind(claims, KIND_COUNT)
        assert any(c.status == CONTRADICTED for c in count_claims)

    def test_count_claim_unverifiable_when_no_count_in_live(self):
        live = {"price_levels": ["dn"]}  # no counts
        claims = extract_claims("You have 100 products in the catalog.", live)
        count_claims = _claims_of_kind(claims, KIND_COUNT)
        assert any(c.status == UNVERIFIABLE for c in count_claims)

    def test_price_code_claim_verified(self):
        live = {"price_levels": ["dn", "list"]}
        claims = extract_claims("Use DefaultPriceCode=dn for all customers.", live)
        price_claims = _claims_of_kind(claims, KIND_PRICE_CODE)
        assert any(c.status == VERIFIED for c in price_claims)

    def test_price_code_claim_contradicted(self):
        live = {"price_levels": ["dn", "list"]}
        claims = extract_claims("Use DefaultPriceCode=net for all customers.", live)
        price_claims = _claims_of_kind(claims, KIND_PRICE_CODE)
        assert any(c.status == CONTRADICTED for c in price_claims)

    def test_image_status_contradicted_when_uploaded(self):
        live = {"uploaded_images": ["ABC-1.jpg"]}
        claims = extract_claims("The ABC-1 image is broken.", live)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        assert any(c.status == CONTRADICTED for c in image_claims)

    def test_image_status_verified_when_absent(self):
        live = {"uploaded_images": ["OTHER.jpg"]}
        claims = extract_claims("The ABC-1 image is missing.", live)
        image_claims = _claims_of_kind(claims, KIND_IMAGE_STATUS)
        assert any(c.status == VERIFIED for c in image_claims)

    def test_query_name_cited_for_live_state_evidence(self):
        """Live-state evidence must cite a QUERY_NAME, not a typed count."""
        live = {"counts": {"customers.csv": 346}}
        claims = extract_claims("You have 346 customers imported.", live)
        count_claims = _claims_of_kind(claims, KIND_COUNT)
        for c in count_claims:
            if c.status in (VERIFIED, CONTRADICTED):
                assert c.query_name, (
                    f"Live-state evidence must cite a query_name, not a typed count. "
                    f"Found: status={c.status}, evidence={c.evidence}"
                )


# ---------------------------------------------------------------------------
# Verdict and exit codes
# ---------------------------------------------------------------------------


class TestVerdictAndExitCodes:
    """Exit codes: 0=safe, 1=not-safe, 2=could-not-complete."""

    def test_safe_to_send_exit_0(self):
        live = {"counts": {"products.csv": 10}}
        draft = "You have 10 products in your catalog."
        checker = _make_checker(draft, live)
        report = checker.run()
        assert report.exit_code == 0
        assert report.verdict_label == "safe-to-send"

    def test_not_safe_exit_1_on_contradicted_claim(self):
        live = {"price_levels": ["dn"]}
        draft = "Use DefaultPriceCode=INVALID for all customers."
        checker = _make_checker(draft, live)
        report = checker.run()
        assert report.exit_code == 1
        assert report.verdict_label == "not-safe-to-send"

    def test_rewrite_guidance_present_when_not_safe(self):
        live = {"price_levels": ["dn"]}
        draft = "Use DefaultPriceCode=INVALID."
        report = _make_checker(draft, live).run()
        assert report.rewrite_guidance
        rendered = report.render()
        assert "Rewrite guidance" in rendered or "rewrite" in rendered.lower()

    def test_safe_report_includes_no_blocking_language(self):
        live = {"counts": {"products.csv": 5}}
        draft = "You have 5 products."
        report = _make_checker(draft, live).run()
        rendered = report.render()
        assert "SAFE-TO-SEND" in rendered

    def test_not_safe_report_includes_contradicted_language(self):
        live = {"price_levels": ["dn"]}
        draft = "DefaultPriceCode=WRONG is the correct value."
        report = _make_checker(draft, live).run()
        rendered = report.render()
        assert "CONTRADICTED" in rendered
        assert "NOT-SAFE-TO-SEND" in rendered


# ---------------------------------------------------------------------------
# Prior error pattern registry
# ---------------------------------------------------------------------------


class TestPriorErrorPatternRegistry:
    def test_two_registered_patterns(self):
        assert len(_PRIOR_ERROR_PATTERNS) >= 2

    def test_tcd_pattern_registered(self):
        names = [p[0] for p in _PRIOR_ERROR_PATTERNS]
        assert any("tcd" in n.lower() for n in names)

    def test_magic_lite_pattern_registered(self):
        names = [p[0] for p in _PRIOR_ERROR_PATTERNS]
        assert any("mali" in n.lower() or "magic" in n.lower() for n in names)

    def test_pattern_descriptions_are_non_empty(self):
        for name, desc, _ in _PRIOR_ERROR_PATTERNS:
            assert desc.strip(), f"Pattern '{name}' has empty description"

    def test_pattern_detect_fn_is_callable(self):
        for name, _, detect_fn in _PRIOR_ERROR_PATTERNS:
            assert callable(detect_fn), f"Pattern '{name}' detect_fn is not callable"


# ---------------------------------------------------------------------------
# Entity disambiguation
# ---------------------------------------------------------------------------


class TestEntityDisambiguation:
    LIVE = {
        "shortname": "mali",
        "queried_at": "2026-07-27T20:00:00Z",
        "keys": {"products.csv": ["ML-001", "ML-002", "NSL-010"]},
        "uploaded_images": ["ML-001.jpg", "ML-002.jpg"],
    }

    def test_active_product_flagged_verified(self):
        draft = "ML-001 is in the catalog."
        claims = extract_claims(draft, self.LIVE)
        from verify.before_send import KIND_ENTITY
        entity_claims = _claims_of_kind(claims, KIND_ENTITY)
        ml_claims = [c for c in entity_claims if "ML-001" in c.text]
        assert ml_claims
        assert ml_claims[0].status == VERIFIED

    def test_unknown_code_flagged_unverifiable_with_four_states(self):
        """An unrecognized code must note all four possible states."""
        draft = "GHOST-99 should be in the catalog."
        claims = extract_claims(draft, self.LIVE)
        from verify.before_send import KIND_ENTITY
        entity_claims = _claims_of_kind(claims, KIND_ENTITY)
        ghost_claims = [c for c in entity_claims if "GHOST" in c.text.upper()]
        assert ghost_claims
        assert ghost_claims[0].status == UNVERIFIABLE
        # The four states must be named
        evidence = ghost_claims[0].evidence.lower()
        assert "active product" in evidence
        assert "deleted" in evidence or "option" in evidence or "group" in evidence

    def test_step6_section_lists_entity_codes(self):
        draft = "ML-001 and ML-002 are both live."
        checker = _make_checker(draft, self.LIVE)
        report = checker.run()
        rendered = report.render()
        assert "Step 6" in rendered
        # Entity codes should appear in step 6
        assert "ML-001" in rendered or "ML-002" in rendered


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestCLI:
    """Smoke tests for the CLI entry point."""

    def _run(self, run_script, *args):
        return run_script("verify/before_send.py", *args)

    def test_no_args_is_error(self, run_script):
        rc, out = self._run(run_script)
        assert rc == 2

    def test_missing_draft_file_exits_2(self, run_script, tmp_path):
        rc, out = self._run(run_script, "--draft", str(tmp_path / "nope.md"))
        assert rc == 2
        assert "cannot read draft" in out or "ERROR" in out

    def test_safe_draft_exits_0(self, run_script, tmp_path):
        draft = tmp_path / "draft.md"
        draft.write_text("Hello team, we're making progress.", encoding="utf-8")
        rc, out = self._run(run_script, "--draft", str(draft))
        assert rc == 0
        assert "SAFE-TO-SEND" in out

    def test_contradicted_draft_exits_1(self, run_script, tmp_path):
        draft = tmp_path / "draft.md"
        draft.write_text(
            "Please set DefaultPriceCode=INVALID for all customers.",
            encoding="utf-8",
        )
        live = tmp_path / "live.json"
        live.write_text(json.dumps({
            "shortname": "tcd",
            "queried_at": "2026-07-27T20:00:00Z",
            "price_levels": ["dn", "list"],
        }), encoding="utf-8")
        rc, out = self._run(run_script, "--draft", str(draft),
                            "--live-state", str(live), "--shortname", "tcd")
        assert rc == 1
        assert "CONTRADICTED" in out
        assert "NOT-SAFE-TO-SEND" in out

    def test_report_written_to_out_file(self, run_script, tmp_path):
        draft = tmp_path / "draft.md"
        draft.write_text("All 50 products are imported.", encoding="utf-8")
        live = tmp_path / "live.json"
        live.write_text(json.dumps({
            "shortname": "test",
            "queried_at": "2026-07-27T20:00:00Z",
            "counts": {"products.csv": 50},
        }), encoding="utf-8")
        out_file = tmp_path / "report.md"
        rc, _ = self._run(run_script, "--draft", str(draft),
                          "--live-state", str(live), "--out", str(out_file))
        assert rc == 0
        assert out_file.exists()
        content = out_file.read_text(encoding="utf-8")
        assert "Pre-Send Review" in content

    def test_tcd_corpus_scenario_end_to_end(self, run_script, tmp_path):
        """End-to-end: tcd DefaultPriceCode=0 → exit 1 with tcd pattern named."""
        draft = tmp_path / "tcd_email.md"
        draft.write_text(textwrap.dedent("""\
            Hi Terracotta team,

            We've configured your customer file with DefaultPriceCode=0
            as exported from your ERP. All 346 customers are set up.

            Please re-import and confirm everything looks correct.
        """), encoding="utf-8")
        live = tmp_path / "live_tcd.json"
        live.write_text(json.dumps({
            "shortname": "tcd",
            "queried_at": "2026-07-27T20:00:00Z",
            "price_levels": ["dn", "tcnet", "list"],
            "counts": {"customers.csv": 346},
        }), encoding="utf-8")
        rc, out = self._run(run_script, "--draft", str(draft),
                            "--live-state", str(live), "--shortname", "tcd")
        assert rc == 1, f"Expected exit 1 for DefaultPriceCode=0 claim\n{out}"
        assert "CONTRADICTED" in out
        assert "tcd/DefaultPriceCode" in out

    def test_magic_lite_corpus_scenario_end_to_end(self, run_script, tmp_path):
        """End-to-end: Magic Lite broken-image claim for uploaded file → exit 1."""
        draft = tmp_path / "mali_email.md"
        draft.write_text(textwrap.dedent("""\
            Hi Magic Lite team,

            We found that the GDL-6 image is broken and not showing for reps.
            DL-FR image is also missing from the iPad catalog.

            We'll re-upload both files right away.
        """), encoding="utf-8")
        live = tmp_path / "live_mali.json"
        live.write_text(json.dumps({
            "shortname": "mali",
            "queried_at": "2026-07-27T20:00:00Z",
            "uploaded_images": ["GDL-6.jpg", "DL-FR.jpg", "RGL-FR.jpg", "ML-001.jpg"],
            "counts": {"products.csv": 683},
        }), encoding="utf-8")
        rc, out = self._run(run_script, "--draft", str(draft),
                            "--live-state", str(live), "--shortname", "mali")
        assert rc == 1, f"Expected exit 1 for false broken-image claim\n{out}"
        assert "CONTRADICTED" in out
        # GDL-6 or DL-FR should appear in the report as contradicted
        assert "GDL-6" in out or "gdl-6" in out.lower() or "DL-FR" in out

    def test_all_nine_steps_in_cli_output(self, run_script, tmp_path):
        """CLI output must contain all 9 step headings."""
        draft = tmp_path / "draft.md"
        draft.write_text("Hello team, 10 products are ready.", encoding="utf-8")
        rc, out = self._run(run_script, "--draft", str(draft))
        for step in range(1, 10):
            assert f"Step {step}" in out, f"Step {step} missing from CLI output"

    def test_bom_in_draft_is_handled(self, run_script, tmp_path):
        """A BOM-prefixed draft must not crash the checker."""
        draft = tmp_path / "bom_draft.md"
        draft.write_bytes(b"\xef\xbb\xbfHello team, all good.")
        rc, out = self._run(run_script, "--draft", str(draft))
        # Should not crash — BOM is stripped by utf-8-sig
        assert rc in (0, 1)
        assert "Step 1" in out
