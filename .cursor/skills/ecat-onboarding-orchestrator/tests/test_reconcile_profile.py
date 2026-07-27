"""Tests for reconcile/profile.py — pure functions only (no DB required).

Covers:
  - LiveState: from_dict / to_dict round-trip, is_stale, age_str
  - read_profile_block: parses the reconcile:start JSON block
  - write_profile_block: embeds or replaces the Live state section
  - diff_report: drift detection, STALE flagging, formatting
  - _make_block: rendered table has expected rows

The CLI itself (profile.py main()) requires a live DB and is not tested here.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from reconcile.profile import (
    LiveState,
    _DRIFT,
    _FRESH,
    _NEW,
    _STALE,
    _make_block,
    diff_report,
    read_profile_block,
    write_profile_block,
)


# ---------------------------------------------------------------------------
# LiveState: from_dict / to_dict
# ---------------------------------------------------------------------------

class TestLiveState:
    def test_round_trip_basic(self):
        d = {
            "products_active": 683,
            "products_with_images": 671,
            "customers": 3418,
            "inventory_rows": 694,
            "orphan_inventory": 11,
            "price_level_codes": ["mldn", "mllist", "nsldn", "nsllist"],
            "options": 2,
            "option_groups": 2,
            "lifecycle": "active",
            "queried_at": "2026-07-27T20:00:00Z",
        }
        state = LiveState.from_dict(d)
        assert state.products_active == 683
        assert state.customers == 3418
        assert sorted(state.price_level_codes) == ["mldn", "mllist", "nsldn", "nsllist"]
        assert state.lifecycle == "active"

    def test_price_levels_as_csv_string(self):
        """from_dict must handle a comma-separated string (from the block JSON)."""
        state = LiveState.from_dict({"price_level_codes": "mldn, mllist"})
        assert sorted(state.price_level_codes) == ["mldn", "mllist"]

    def test_to_dict_excludes_none(self):
        state = LiveState(products_active=683)
        d = state.to_dict()
        assert "products_active" in d
        assert "customers" not in d  # None fields excluded

    def test_to_dict_sorts_price_levels(self):
        state = LiveState(price_level_codes=["z", "a", "m"])
        assert state.to_dict()["price_level_codes"] == ["a", "m", "z"]

    def test_int_conversion_from_string(self):
        """DB rows may come back as strings; from_dict must coerce."""
        state = LiveState.from_dict({"products_active": "683", "customers": "3418"})
        assert state.products_active == 683
        assert state.customers == 3418

    def test_invalid_int_becomes_none(self):
        state = LiveState.from_dict({"products_active": "not_a_number"})
        assert state.products_active is None

    def test_is_stale_no_queried_at(self):
        state = LiveState()
        assert state.is_stale() is True

    def test_is_stale_old_timestamp(self):
        state = LiveState(queried_at="2020-01-01T00:00:00Z")
        assert state.is_stale(stale_days=7) is True

    def test_is_stale_fresh_timestamp(self):
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        state = LiveState(queried_at=ts)
        assert state.is_stale(stale_days=7) is False

    def test_age_str_never(self):
        assert LiveState().age_str() == "never"

    def test_age_str_recent(self):
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        result = LiveState(queried_at=ts).age_str()
        assert "h ago" in result or "< 1h ago" in result

    def test_age_str_days(self):
        state = LiveState(queried_at="2020-01-01T00:00:00Z")
        result = state.age_str()
        assert "d ago" in result


# ---------------------------------------------------------------------------
# read_profile_block
# ---------------------------------------------------------------------------

class TestReadProfileBlock:
    def test_no_file(self, tmp_path):
        state, ts = read_profile_block(str(tmp_path / "missing.md"))
        assert state is None
        assert ts is None

    def test_no_block(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Client\n\n## Identity\n- **Org shortname:** `test`\n")
        state, ts = read_profile_block(str(p))
        assert state is None

    def test_parses_block(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        block = (
            "## Live state (reconciled)\n\n"
            '<!-- reconcile:start {"queried_at": "2026-07-27T20:00:00Z", '
            '"products_active": 683, "customers": 3418} -->\n\n'
            "| Field | DB live | Queried |\n"
            "<!-- reconcile:end -->\n"
        )
        p.write_text(block, encoding="utf-8")
        state, ts = read_profile_block(str(p))
        assert state is not None
        assert state.products_active == 683
        assert state.customers == 3418
        assert ts == "2026-07-27T20:00:00Z"

    def test_parses_full_block(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        import json
        payload = json.dumps({
            "queried_at": "2026-07-21T10:00:00Z",
            "products_active": 832,
            "products_with_images": 823,
            "customers": 231,
            "inventory_rows": 912,
            "orphan_inventory": 83,
            "price_level_codes": ["dn", "list"],
            "options": 0,
            "option_groups": 0,
            "lifecycle": "onboarding",
        })
        p.write_text(
            f"# Lib & Co\n\n## Live state (reconciled)\n\n"
            f"<!-- reconcile:start {payload} -->\n\n<!-- reconcile:end -->\n",
            encoding="utf-8",
        )
        state, ts = read_profile_block(str(p))
        assert state.products_active == 832
        assert state.customers == 231
        assert sorted(state.price_level_codes) == ["dn", "list"]
        assert state.lifecycle == "onboarding"
        assert ts == "2026-07-21T10:00:00Z"

    def test_malformed_json_returns_none(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text(
            "## Live state (reconciled)\n"
            "<!-- reconcile:start {not valid json} -->\n"
            "<!-- reconcile:end -->\n",
            encoding="utf-8",
        )
        state, ts = read_profile_block(str(p))
        assert state is None


# ---------------------------------------------------------------------------
# write_profile_block and _make_block
# ---------------------------------------------------------------------------

class TestWriteProfileBlock:
    def _fresh_state(self):
        return LiveState(
            products_active=683,
            products_with_images=671,
            customers=3418,
            inventory_rows=694,
            orphan_inventory=11,
            price_level_codes=["mllist", "mldn"],
            options=2,
            option_groups=2,
            lifecycle="active",
            queried_at="2026-07-27T20:00:00Z",
        )

    def test_writes_block_to_profile(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text(
            "# Magic Lite\n\n## Identity\n- **Org shortname:** `mali`\n",
            encoding="utf-8",
        )
        state = self._fresh_state()
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")
        assert "## Live state (reconciled)" in text
        assert "reconcile:start" in text
        assert "reconcile:end" in text

    def test_block_contains_queried_at(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Test\n", encoding="utf-8")
        state = self._fresh_state()
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")
        assert "2026-07-27" in text

    def test_block_contains_product_count(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Test\n", encoding="utf-8")
        state = self._fresh_state()
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")
        assert "683" in text

    def test_replaces_existing_block(self, tmp_path):
        import json
        old_payload = json.dumps({
            "queried_at": "2026-07-01T00:00:00Z",
            "products_active": 500,
        })
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text(
            f"# Test\n\n## Live state (reconciled)\n\n"
            f"<!-- reconcile:start {old_payload} -->\n\n<!-- reconcile:end -->\n",
            encoding="utf-8",
        )
        state = self._fresh_state()
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")

        # Old value must be gone; new value must be present
        assert "500" not in text
        assert "683" in text

        # Only one reconcile block allowed
        assert text.count("## Live state (reconciled)") == 1
        assert text.count("<!-- reconcile:end -->") == 1

    def test_round_trip(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Test\n", encoding="utf-8")
        state = self._fresh_state()
        write_profile_block(str(p), state)
        recovered, ts = read_profile_block(str(p))
        assert recovered is not None
        assert recovered.products_active == state.products_active
        assert recovered.customers == state.customers
        assert ts == "2026-07-27T20:00:00Z"

    def test_returns_false_if_file_missing(self, tmp_path):
        result = write_profile_block(str(tmp_path / "missing.md"), self._fresh_state())
        assert result is False

    def test_orphan_inventory_warning_flag(self, tmp_path):
        """Non-zero orphan_inventory should show a warning in the rendered table."""
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Test\n", encoding="utf-8")
        state = LiveState(
            products_active=683,
            orphan_inventory=247,
            queried_at="2026-07-27T20:00:00Z",
        )
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")
        assert "247" in text

    def test_zero_orphan_inventory_no_flag(self, tmp_path):
        p = tmp_path / "CLIENT_PROFILE.md"
        p.write_text("# Test\n", encoding="utf-8")
        state = LiveState(orphan_inventory=0, queried_at="2026-07-27T20:00:00Z")
        write_profile_block(str(p), state)
        text = p.read_text(encoding="utf-8")
        # Verify no warning marker when count is zero
        lines = [l for l in text.splitlines() if "Orphan" in l]
        assert all("⚠" not in l for l in lines)


# ---------------------------------------------------------------------------
# diff_report
# ---------------------------------------------------------------------------

class TestDiffReport:
    def _state(self, **kw):
        defaults = {
            "queried_at": "2026-07-27T20:00:00Z",
            "products_active": 683,
            "customers": 3418,
            "lifecycle": "active",
        }
        return LiveState.from_dict({**defaults, **kw})

    def test_no_drift_shows_match(self):
        db = self._state()
        profile = self._state()
        report, drift = diff_report(db, profile, "mali")
        assert drift == 0
        assert "MATCH" in report

    def test_drift_shows_drift(self):
        db = self._state(customers=3418)
        profile = self._state(customers=346)
        report, drift = diff_report(db, profile, "tcd")
        assert drift >= 1
        assert "DRIFT" in report

    def test_drift_count_accurate(self):
        db = self._state(customers=3418, products_active=700)
        profile = self._state(customers=346, products_active=600)
        _, drift = diff_report(db, profile, "test")
        assert drift == 2

    def test_no_profile_shows_new(self):
        db = self._state()
        report, drift = diff_report(db, None, "mali")
        assert _NEW in report or drift > 0

    def test_stale_profile_flagged(self):
        db = self._state()
        profile = self._state(queried_at="2020-01-01T00:00:00Z")
        report, _ = diff_report(db, profile, "mali", stale_days=7)
        assert "STALE" in report.upper() or "stale" in report.lower()

    def test_report_contains_shortname(self):
        db = self._state()
        report, _ = diff_report(db, None, "libco")
        assert "libco" in report

    def test_report_has_all_field_labels(self):
        db = self._state(
            products_active=683,
            products_with_images=671,
            customers=3418,
            inventory_rows=694,
            orphan_inventory=11,
            price_level_codes=["dn"],
            options=0,
            option_groups=0,
        )
        report, _ = diff_report(db, None, "mali")
        for label in ("products", "customers", "inventory", "lifecycle"):
            assert label in report.lower(), f"'{label}' missing from diff report"

    def test_emit_live_state_hint_in_report(self):
        db = self._state()
        report, _ = diff_report(db, None, "mali")
        assert "--emit-live-state" in report

    def test_warnings_shown_in_report(self):
        db = self._state()
        warnings = ["custom_fields.products: table does not exist"]
        report, _ = diff_report(db, None, "mali", warnings=warnings)
        assert "table does not exist" in report

    def test_terracotta_drift_scenario(self):
        """Reproduces the doc-vs-live drift that motivated the reconciler.

        Profile said '0 customers'; live DB had 346. The reconciler should flag this.
        """
        db = self._state(customers=346)
        profile = self._state(customers=0)
        report, drift = diff_report(db, profile, "tcd")
        assert drift >= 1
        assert "0" in report  # old value visible

    def test_pebl_drift_scenario(self):
        """Pebl: profile said '0 price levels, 0 customers'; live had 8 + 171."""
        db = self._state(
            customers=171,
            price_level_codes=["n", "dn", "list", "pro", "dist", "a", "b", "c"],
        )
        profile = self._state(customers=0, price_level_codes=[])
        _, drift = diff_report(db, profile, "pebl")
        assert drift >= 1


# ---------------------------------------------------------------------------
# _make_block rendering
# ---------------------------------------------------------------------------

class TestMakeBlock:
    def test_contains_section_header(self):
        state = LiveState(products_active=683, queried_at="2026-07-27T20:00:00Z")
        block = _make_block(state)
        assert "## Live state (reconciled)" in block

    def test_contains_start_and_end(self):
        state = LiveState(queried_at="2026-07-27T20:00:00Z")
        block = _make_block(state)
        assert "reconcile:start" in block
        assert "reconcile:end" in block

    def test_json_payload_parseable(self):
        import json, re
        state = LiveState(
            products_active=683, customers=3418,
            queried_at="2026-07-27T20:00:00Z",
        )
        block = _make_block(state)
        match = re.search(r"<!-- reconcile:start (\{.*?\}) -->", block, re.S)
        assert match, "No JSON payload found in block"
        data = json.loads(match.group(1))
        assert data["products_active"] == 683
        assert data["queried_at"] == "2026-07-27T20:00:00Z"

    def test_only_present_fields_in_table(self):
        """Fields not set should not appear as rows in the markdown table."""
        state = LiveState(products_active=683, queried_at="2026-07-27T20:00:00Z")
        block = _make_block(state)
        assert "683" in block
        # customers is None — should not appear as a data row
        lines_with_customers = [l for l in block.splitlines() if "Customers" in l]
        assert not lines_with_customers

    def test_image_percentage_shown(self):
        state = LiveState(
            products_active=683,
            products_with_images=671,
            queried_at="2026-07-27T20:00:00Z",
        )
        block = _make_block(state)
        assert "98%" in block

    def test_lifecycle_shown_as_code(self):
        state = LiveState(lifecycle="active", queried_at="2026-07-27T20:00:00Z")
        block = _make_block(state)
        assert "`active`" in block
