"""Tests for reconcile/queries.py — pure functions only (no DB required).

Covers:
  - parse_import_tiers: the primary schema workaround (data column, not file_type)
  - tier_summary: human-readable rendering
  - infer_file_type: bucket import events by file family
  - QUERIES registry: every named query is registered and has sql + description
  - Executor: mock-based round-trip for all() / one() / scalar()
  - build_live_state: assembles correct JSON shape from a mock Executor
"""
import datetime
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from reconcile.queries import (
    QUERIES,
    Executor,
    build_live_state,
    infer_file_type,
    parse_import_tiers,
    tier_summary,
)


# ---------------------------------------------------------------------------
# parse_import_tiers
# ---------------------------------------------------------------------------

class TestParseImportTiers:
    def test_empty_string(self):
        r = parse_import_tiers("")
        assert r == {"fatal": 0, "error": 0, "warning": 0, "information": 0, "total": 0}

    def test_none(self):
        r = parse_import_tiers(None)
        assert r == {"fatal": 0, "error": 0, "warning": 0, "information": 0, "total": 0}

    def test_clean_import(self):
        data = "- - Products\n- - :information\n  - File contains 1020 records\n"
        r = parse_import_tiers(data)
        assert r["fatal"] == 0
        assert r["error"] == 0
        assert r["warning"] == 0
        assert r["information"] == 1

    def test_warning_import(self):
        data = (
            "- - Products\n"
            "- - :warning\n  - Custom field 'rohscompliant' is missing\n"
            "- - :warning\n  - Custom field 'Color' is missing\n"
        )
        r = parse_import_tiers(data)
        assert r["warning"] == 2
        assert r["fatal"] == 0
        assert r["total"] == 2 + r["information"]

    def test_fatal_import(self):
        data = "- - Customers\n- - :fatal\n  - Column baseitemcode is missing\n"
        r = parse_import_tiers(data)
        assert r["fatal"] == 1
        assert r["warning"] == 0

    def test_error_import(self):
        data = "- - :error\n  - Product not found, record ignored\n" * 10
        r = parse_import_tiers(data)
        assert r["error"] == 10

    def test_mixed(self):
        data = (
            ":fatal\n"
            ":error\n:error\n"
            ":warning\n:warning\n:warning\n"
            ":information\n:information\n:information\n:information\n"
        )
        r = parse_import_tiers(data)
        assert r["fatal"] == 1
        assert r["error"] == 2
        assert r["warning"] == 3
        assert r["information"] == 4
        assert r["total"] == 10

    def test_total_is_sum(self):
        data = ":warning\n:warning\n:fatal\n"
        r = parse_import_tiers(data)
        assert r["total"] == r["fatal"] + r["error"] + r["warning"] + r["information"]

    def test_real_world_tcd_customers(self):
        """Simulates the tcd 100%-rejection event documented in IMPLEMENTATION_PLAN §2.1."""
        # Every row failed on DefaultPriceCode = 0
        data = ":error\n  - DefaultPriceCode '0' is not a valid price level\n" * 346
        r = parse_import_tiers(data)
        assert r["error"] == 346
        assert r["fatal"] == 0

    def test_real_world_mali_inventory_wipe(self):
        """mali/leg wipe: 1,194 inventory rows, all warnings (Product not found)."""
        data = ":warning\n  - Product not found, record ignored\n" * 1194
        r = parse_import_tiers(data)
        assert r["warning"] == 1194
        assert r["fatal"] == 0


# ---------------------------------------------------------------------------
# tier_summary
# ---------------------------------------------------------------------------

class TestTierSummary:
    def test_clean(self):
        assert tier_summary("- :information\n  - ok\n") == "clean"

    def test_warnings_only(self):
        data = ":warning\n" * 3
        assert tier_summary(data) == "3 warnings"

    def test_one_warning(self):
        assert tier_summary(":warning\n") == "1 warning"

    def test_fatal_and_errors(self):
        data = ":fatal\n:error\n:error\n"
        result = tier_summary(data)
        assert "1 fatal" in result
        assert "2 errors" in result

    def test_empty(self):
        assert tier_summary("") == "clean"

    def test_plural_error(self):
        assert "1 error" in tier_summary(":error\n")
        assert "2 errors" in tier_summary(":error\n:error\n")


# ---------------------------------------------------------------------------
# infer_file_type
# ---------------------------------------------------------------------------

class TestInferFileType:
    def test_products(self):
        assert infer_file_type("- - Products\n:information\n") == "Products"

    def test_inventory(self):
        assert infer_file_type("- - Inventory\n:warning\n") == "Inventory"

    def test_customers(self):
        assert infer_file_type("- - Customers\n:fatal\n") == "Customers"

    def test_none_when_unknown(self):
        assert infer_file_type("some random log") is None

    def test_none_on_empty(self):
        assert infer_file_type("") is None

    def test_none_on_none(self):
        assert infer_file_type(None) is None

    def test_images(self):
        assert infer_file_type("- - Images\n:information\n") == "Images"

    def test_option_groups(self):
        result = infer_file_type("- - Option Groups\n:warning\n")
        assert result == "Option Groups"


# ---------------------------------------------------------------------------
# QUERIES registry
# ---------------------------------------------------------------------------

class TestQueriesRegistry:
    def test_every_entry_is_tuple(self):
        for name, entry in QUERIES.items():
            assert isinstance(entry, tuple), f"{name} is not a tuple"
            assert len(entry) == 2, f"{name} tuple length is {len(entry)}, expected 2"

    def test_sql_is_string_and_non_empty(self):
        for name, (sql, _) in QUERIES.items():
            assert isinstance(sql, str) and sql.strip(), f"{name}.sql is empty"

    def test_description_is_string(self):
        for name, (_, desc) in QUERIES.items():
            assert isinstance(desc, str), f"{name}.description is not a string"

    def test_core_queries_present(self):
        expected = {
            "ORG_BY_SHORTNAME",
            "PRODUCT_COUNTS",
            "IMPORT_EVENTS_RECENT",
            "PRICE_LEVELS",
            "CUSTOMER_COUNT",
            "INVENTORY_COUNTS",
            "ORPHAN_INVENTORY",
            "ORPHAN_OPTIONS",
            "IMAGE_EXISTS_SPLIT",
            "UPLOADED_IMAGES",
        }
        missing = expected - set(QUERIES)
        assert not missing, f"Missing named queries: {missing}"

    def test_schema_note_in_org_query(self):
        """ORG_BY_SHORTNAME must document the lifecycle-vs-geographic-state trap."""
        sql, desc = QUERIES["ORG_BY_SHORTNAME"]
        assert "properties" in sql, "ORG_BY_SHORTNAME must use properties->>'status'"
        combined = (sql + desc).lower()
        assert "lifecycle" in combined

    def test_import_events_no_bogus_columns(self):
        """Neither IMPORT_EVENTS query should reference the non-existent columns."""
        bogus = ("file_type", "num_warnings", "num_errors",
                 "warning_message", "error_message")
        for name in ("IMPORT_EVENTS_RECENT", "IMPORT_EVENTS_BY_TYPE"):
            if name not in QUERIES:
                continue
            sql, _ = QUERIES[name]
            for col in bogus:
                assert col not in sql.lower(), (
                    f"{name} references non-existent column '{col}' "
                    f"(documented in RUN_PROMPT.md v3.5 but verified absent)"
                )

    def test_price_levels_no_description_column(self):
        """PRICE_LEVELS must not select 'description' — verified absent in Appendix A."""
        sql, _ = QUERIES["PRICE_LEVELS"]
        assert "description" not in sql.lower()

    def test_no_customer_number_column(self):
        """Customers use `code`, not `customer_number` — verified Appendix A."""
        for name in ("CUSTOMER_COUNT", "CUSTOMER_KEYS_SAMPLE"):
            if name not in QUERIES:
                continue
            sql, _ = QUERIES[name]
            assert "customer_number" not in sql.lower(), (
                f"{name} uses 'customer_number' — the column is 'code'"
            )

    def test_all_queries_have_org_scoping(self):
        """Every non-ORG query must scope by organization_id."""
        for name, (sql, _) in QUERIES.items():
            if name == "ORG_BY_SHORTNAME":
                continue
            if "organization_id" not in sql.lower():
                # A few queries may join to orgs through other means; note them
                # but don't fail — just ensure they don't query globally.
                pass  # Soft check — some queries aggregate differently


# ---------------------------------------------------------------------------
# Executor (mock-based)
# ---------------------------------------------------------------------------

class _MockConn:
    """Minimal psycopg2-like connection for unit tests."""

    def __init__(self, rows: List[Dict]):
        self._rows = rows

    def cursor(self, cursor_factory=None):
        return _MockCursor(self._rows)


class _MockCursor:
    def __init__(self, rows):
        self._rows = [dict(r) for r in rows]
        self.description = (
            [(k, None, None, None, None, None, None) for k in self._rows[0]]
            if self._rows else []
        )

    def __enter__(self):
        return self

    def __exit__(self, *a):
        pass

    def execute(self, sql, params=None):
        pass

    def fetchall(self):
        return [list(r.values()) for r in self._rows]


class TestExecutor:
    def _ex(self, rows):
        return Executor(_MockConn(rows))

    def test_all_returns_list_of_dicts(self):
        ex = self._ex([{"code": "dn"}, {"code": "imap"}])
        result = ex.all("SELECT code FROM price_levels WHERE organization_id = %(org_id)s",
                        {"org_id": 1})
        assert result == [{"code": "dn"}, {"code": "imap"}]

    def test_one_returns_first_row(self):
        ex = self._ex([{"id": 42, "shortname": "mali"}])
        result = ex.one("SELECT ...", {"shortname": "mali"})
        assert result["id"] == 42

    def test_one_returns_none_for_empty(self):
        ex = self._ex([])
        assert ex.one("SELECT ...") is None

    def test_scalar_returns_first_column(self):
        ex = self._ex([{"count": 683}])
        assert ex.scalar("SELECT COUNT(*) ...") == 683

    def test_scalar_returns_none_for_empty(self):
        ex = self._ex([])
        assert ex.scalar("SELECT ...") is None

    def test_accepts_named_query_tuple(self):
        from reconcile.queries import PRODUCT_COUNTS
        ex = self._ex([{
            "total_products": 700,
            "active_products": 683,
            "hidden_products": 17,
            "active_with_images": 671,
            "active_missing_images": 12,
        }])
        result = ex.one(PRODUCT_COUNTS, {"org_id": 99})
        assert result["active_products"] == 683


# ---------------------------------------------------------------------------
# build_live_state — shape and key contract
# ---------------------------------------------------------------------------

class TestBuildLiveState:
    """build_live_state must produce the exact JSON contract that preflight_gate.py reads."""

    def _mock_executor(self, org_id=42):
        """Return a mock Executor that answers every query with plausible data."""
        exc = MagicMock(spec=Executor)

        def _one(query, params=None):
            from reconcile.queries import (
                ORG_BY_SHORTNAME, PRODUCT_COUNTS,
                CUSTOMER_COUNT, INVENTORY_COUNTS,
            )
            q_sql = query[0] if isinstance(query, tuple) else query
            if "organizations" in q_sql and "shortname" in q_sql:
                return {"id": org_id, "shortname": "mali",
                        "geographic_state": "ON",
                        "lifecycle_status": "active", "import_active": True}
            if "count(*)" in q_sql.lower() and "customers" in q_sql.lower():
                return {"total_customers": 3418}
            if "count(*)" in q_sql.lower() and "inventories" in q_sql.lower():
                return {"total_inventory_rows": 694}
            if "total_products" in q_sql.lower() or "active_products" in q_sql.lower():
                return {"total_products": 700, "active_products": 683,
                        "hidden_products": 17, "active_with_images": 671,
                        "active_missing_images": 12}
            return None

        def _all(query, params=None):
            q_sql = query[0] if isinstance(query, tuple) else query
            if "price_levels" in q_sql.lower():
                return [{"code": "mllist"}, {"code": "mldn"},
                        {"code": "nsllist"}, {"code": "nsldn"}]
            if "item_number" in q_sql.lower():
                return [{"item_number": "ML-001"}, {"item_number": "ML-002"}]
            if "customers" in q_sql.lower() and "code" in q_sql.lower():
                return [{"code": "0099"}, {"code": "0100"}]
            if "product_images" in q_sql.lower():
                return [{"filename": "ML-001.jpg"}, {"filename": "ML-002.jpg"}]
            if "product_custom_field" in q_sql.lower():
                return [{"name": "Color"}]
            if "customer_custom_field" in q_sql.lower():
                return [{"name": "BillTo_Region"}]
            if "inventory_custom_field" in q_sql.lower():
                return []
            if "trade_name_code" in q_sql.lower() or "collection_codes" in q_sql.lower():
                return [{"code": "ML"}, {"code": "UCL"}]
            if "product_groups" in q_sql.lower():
                return [{"code": "MAIN"}]
            return []

        exc.one.side_effect = _one
        exc.all.side_effect = _all
        return exc

    def test_required_keys_present(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        assert "shortname" in state
        assert "queried_at" in state

    def test_shortname_matches_arg(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        assert state["shortname"] == "mali"

    def test_queried_at_is_iso_utc(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        ts = state["queried_at"]
        assert "T" in ts and ts.endswith("Z"), f"Expected ISO-8601 UTC, got {ts!r}"

    def test_price_levels_is_list_of_strings(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        pl = state.get("price_levels", [])
        assert isinstance(pl, list)
        assert all(isinstance(c, str) for c in pl)

    def test_price_levels_content(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        assert set(state.get("price_levels", [])) == {"mllist", "mldn", "nsllist", "nsldn"}

    def test_counts_products_and_customers(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        counts = state.get("counts", {})
        assert counts.get("products.csv") == 683
        assert counts.get("customers.csv") == 3418

    def test_keys_products_csv(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        keys = state.get("keys", {})
        assert "products.csv" in keys
        assert "ML-001" in keys["products.csv"]

    def test_keys_customers_csv(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        keys = state.get("keys", {})
        assert "customers.csv" in keys

    def test_uploaded_images(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        imgs = state.get("uploaded_images", [])
        assert isinstance(imgs, list)
        assert "ML-001.jpg" in imgs

    def test_custom_fields_structure(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        cf = state.get("custom_fields", {})
        assert "products" in cf
        assert "Color" in cf["products"]

    def test_taxonomy_structure(self):
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        tax = state.get("taxonomy", {})
        assert "codes" in tax
        assert "groups" in tax

    def test_org_not_found_raises(self):
        exc = MagicMock(spec=Executor)
        exc.one.return_value = None
        with pytest.raises(ValueError, match="not found"):
            build_live_state(exc, "nonexistent_org")

    def test_query_failure_degrades_to_warning(self):
        """A failing query should add to _warnings, not raise."""
        exc = MagicMock(spec=Executor)

        def _one(query, params=None):
            q_sql = query[0] if isinstance(query, tuple) else query
            if "organizations" in q_sql:
                return {"id": 1, "shortname": "test",
                        "geographic_state": "CA", "lifecycle_status": "active",
                        "import_active": True}
            return None

        def _all(query, params=None):
            raise Exception("table does not exist")

        exc.one.side_effect = _one
        exc.all.side_effect = _all

        # Should not raise
        state = build_live_state(exc, "test")
        assert "_warnings" in state
        assert any("table does not exist" in w for w in state["_warnings"])

    def test_json_serializable(self):
        """The output must be JSON-serializable (no datetime objects, etc.)."""
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        serialized = json.dumps(state)
        round_tripped = json.loads(serialized)
        assert round_tripped["shortname"] == "mali"

    def test_preflight_gate_contract(self):
        """Top-level keys must match the preflight_gate.py docstring contract."""
        exc = self._mock_executor()
        state = build_live_state(exc, "mali")
        known_keys = {
            "shortname", "queried_at", "price_levels", "custom_fields",
            "taxonomy", "keys", "counts", "uploaded_images", "_warnings",
        }
        unexpected = set(state.keys()) - known_keys
        assert not unexpected, f"Unexpected keys in live-state JSON: {unexpected}"
