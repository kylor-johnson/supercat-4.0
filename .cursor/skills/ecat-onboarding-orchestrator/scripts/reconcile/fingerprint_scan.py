#!/usr/bin/env python3
"""Cross-tenant fingerprint scan.

After identifying a root cause at one org, sweep all orgs for the same
signature.  This found Savoy House for free when Golden Lighting's Cloudflare
misconfiguration was diagnosed — the scan costs nothing and has already paid for
itself once.

  python scripts/reconcile/fingerprint_scan.py --check orphan_inventory
  python scripts/reconcile/fingerprint_scan.py --check orphan_options --lifecycle all
  python scripts/reconcile/fingerprint_scan.py --list-checks

Provenance
  IMPLEMENTATION_PLAN.md §7 Phase 5:
    "Add a cross-tenant fingerprint scan: after any root cause, sweep all orgs
    for the same signature."

Design
  • Each built-in check maps to a named query from queries.py (never raw SQL here).
  • Registry flags suppress inapplicable checks with an explicit SKIP — never silence.
  • If the REGISTRY.yaml is absent or yields no matches, the scan falls back to
    querying the DB for orgs at the requested lifecycle.
  • All queries are READ-ONLY.  This script never writes to the database.

Connection
  export DATABASE_URL="postgresql://user:pass@host:5432/supercat_production"
  (Same credentials as the supercat-postgres-vpn MCP server.)

Available checks (run --list-checks for full table):
  orphan_inventory     Inventory rows whose BaseItemCode has no matching active product.
                       Signature: mali/leg inventory wipe (Appendix B).
  orphan_options       Option groups with zero product references.
                       Signature: tcd / leg POC residue — permanent until options.csv re-sent.
  placeholder_prices   Products with price 0.0 or 1.0 — probable placeholder.
  missing_images       Active products where image_exists = false.
                       Signature: libco portal outage (eOL suppresses imageless products).
  single_customer      Orgs with fewer than 5 customer rows.
                       Signature: leg awaiting real customer file.
"""

import argparse
import datetime
import os
import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
_SCRIPTS_DIR = os.path.normpath(os.path.join(HERE, ".."))
_REPO_ROOT   = os.path.normpath(os.path.join(_SCRIPTS_DIR, "..", "..", ".."))
sys.path.insert(0, _SCRIPTS_DIR)

try:
    from reconcile.queries import (
        connect,
        Executor,
        ORG_BY_SHORTNAME,
        ORPHAN_INVENTORY,
        ORPHAN_OPTIONS,
        MISSING_IMAGES,
        PLACEHOLDER_PRICES,
        CUSTOMER_COUNT,
    )
except ImportError as exc:
    print(
        f"Import error: {exc}\n"
        "Run from scripts/ or set PYTHONPATH to the scripts/ directory.",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class ScanResult:
    """One org's outcome for one check."""
    shortname:  str
    org_id:     int
    check:      str
    matched:    bool
    value:      object = None          # scalar or dict; None = check didn't run
    error:      Optional[str] = None
    skipped:    Optional[str] = None   # populated when a registry flag suppresses the check


@dataclass
class ScanRun:
    """All results from a single scan execution."""
    check:    str
    run_at:   str
    results:  List[ScanResult] = field(default_factory=list)

    @property
    def hits(self) -> List[ScanResult]:
        return [r for r in self.results if r.matched]

    @property
    def skips(self) -> List[ScanResult]:
        return [r for r in self.results if r.skipped]

    @property
    def errors(self) -> List[ScanResult]:
        return [r for r in self.results if r.error]

    @property
    def clean(self) -> List[ScanResult]:
        return [r for r in self.results if not r.matched and not r.skipped and not r.error]


# ---------------------------------------------------------------------------
# Built-in checks
#
# Each check(executor, org_id) → ScanResult with shortname / org_id / check
# left blank (the runner fills those in).
# ---------------------------------------------------------------------------

def check_orphan_inventory(executor: Executor, org_id: int) -> ScanResult:
    """Inventory rows with no matching active product.

    Root-cause signature: mali had 1,194 orphan rows the day of the wrong-org
    import.  Live 2026-07-27: leg=247, libco=83, tcd=30, mali=11.
    Hard-deletes on clean import — an Error tier leaves orphans permanently.
    """
    row = executor.one(ORPHAN_INVENTORY, {"org_id": org_id})
    count = int(row["orphan_inventory_rows"]) if row else 0
    return ScanResult(shortname="", org_id=org_id, check="orphan_inventory",
                      matched=count > 0, value=count)


def check_orphan_options(executor: Executor, org_id: int) -> ScanResult:
    """Option groups with zero product references (orphaned POC residue).

    Root-cause signature: tcd (222 opts / 98 groups / 0 refs) and
    leg (29 opts / 11 groups / 0 refs — all pre-cutover 2025-07-08).
    Permanent until you re-send options.csv (which hard-deletes and reloads).
    """
    row = executor.one(ORPHAN_OPTIONS, {"org_id": org_id})
    if not row:
        return ScanResult(shortname="", org_id=org_id, check="orphan_options",
                          matched=False, value={"groups": 0, "options": 0, "product_refs": 0})
    groups = int(row["total_option_groups"])
    options = int(row["total_options"])
    refs = int(row["products_referencing_options"])
    matched = groups > 0 and refs == 0
    return ScanResult(shortname="", org_id=org_id, check="orphan_options",
                      matched=matched,
                      value={"groups": groups, "options": options, "product_refs": refs})


def check_placeholder_prices(executor: Executor, org_id: int) -> ScanResult:
    """Products whose price JSONB contains 0.0 or 1.0 — probable placeholder.

    Common early-build state: real prices not yet imported.  Also catches a
    round-number sweep from an ERP export that didn't map price codes.
    """
    rows = executor.all(PLACEHOLDER_PRICES, {"org_id": org_id})
    count = len(rows)
    return ScanResult(shortname="", org_id=org_id, check="placeholder_prices",
                      matched=count > 0, value=count)


def check_missing_images(executor: Executor, org_id: int) -> ScanResult:
    """Active products where image_exists = false.

    Root-cause signature: libco portal outage — eOL suppresses imageless
    products from search.  image_exists tracks only the FIRST filename in
    images_json; alternates do not satisfy it.
    """
    rows = executor.all(MISSING_IMAGES, {"org_id": org_id})
    count = len(rows)
    return ScanResult(shortname="", org_id=org_id, check="missing_images",
                      matched=count > 0, value=count)


def check_single_customer(executor: Executor, org_id: int) -> ScanResult:
    """Fewer than 5 customer rows — may indicate awaiting real customer file.

    Root-cause signature: leg has exactly 1 customer (eCat Test) while waiting
    for the client to send their real file.  Threshold of 5 avoids flagging
    test-only setups while catching the "forgot to import" case.
    """
    row = executor.one(CUSTOMER_COUNT, {"org_id": org_id})
    count = int(row["total_customers"]) if row else 0
    return ScanResult(shortname="", org_id=org_id, check="single_customer",
                      matched=count < 5, value=count)


#: Registry of built-in checks: name → (description, function)
CHECKS: Dict[str, Tuple[str, Callable]] = {
    "orphan_inventory":   ("Inventory rows with no matching active product",      check_orphan_inventory),
    "orphan_options":     ("Option groups with zero product references",           check_orphan_options),
    "placeholder_prices": ("Products with placeholder price values (0.0 / 1.0)",  check_placeholder_prices),
    "missing_images":     ("Active products with image_exists = false",            check_missing_images),
    "single_customer":    ("Orgs with fewer than 5 customer rows",                 check_single_customer),
}


# ---------------------------------------------------------------------------
# Applicability: registry flags that suppress checks
#
# Rule from IMPLEMENTATION_PLAN §2.4 / PHASE_GATES §2.3:
#   A suppressed check emits SKIP (flag: <name>), never silence or a false pass.
# ---------------------------------------------------------------------------

#: flag → list of check names it suppresses
FLAG_SUPPRESSIONS: Dict[str, List[str]] = {
    "pricing_na":    ["placeholder_prices"],
    "inventory_na":  ["orphan_inventory", "placeholder_prices"],
    "options_none":  ["orphan_options"],
    "manual_review": [],            # annotates but suppresses nothing automatically
    "churned":       [],            # annotates but suppresses nothing automatically
}


def _skip_reason(check_name: str, flags: List[str]) -> Optional[str]:
    """Return the first suppression reason, or None if the check should run."""
    for flag in flags:
        if check_name in FLAG_SUPPRESSIONS.get(flag, []):
            return f"flag: {flag}"
    return None


# ---------------------------------------------------------------------------
# Registry loading  (eCat_Onboarding/REGISTRY.yaml)
# ---------------------------------------------------------------------------

def _default_registry_path() -> str:
    return os.path.join(_REPO_ROOT, "eCat_Onboarding", "REGISTRY.yaml")


def load_registry(registry_path: str) -> List[Dict]:
    """Load REGISTRY.yaml and return the clients list.

    Degrades gracefully to empty list when the file or PyYAML is absent —
    the scan falls back to querying the DB for orgs at the requested lifecycle.
    """
    try:
        import yaml
        with open(registry_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data.get("clients", []) if data else []
    except FileNotFoundError:
        print(
            f"WARN: REGISTRY.yaml not found at {registry_path}. "
            "Falling back to live DB query for cohort.",
            file=sys.stderr,
        )
        return []
    except ImportError:
        print(
            "WARN: PyYAML not installed (pip install pyyaml). "
            "Registry filtering skipped; all orgs in DB queried.",
            file=sys.stderr,
        )
        return []


def filter_registry(clients: List[Dict], lifecycle_filter: Optional[str]) -> List[Dict]:
    """Return only the clients matching the lifecycle filter."""
    if lifecycle_filter is None:
        return clients
    return [c for c in clients if c.get("lifecycle") == lifecycle_filter]


# ---------------------------------------------------------------------------
# DB fallback: discover cohort directly from Postgres
# ---------------------------------------------------------------------------

_COHORT_BY_LIFECYCLE_SQL = """
SELECT id, shortname
FROM organizations
WHERE properties->>'status' = %(lifecycle)s
ORDER BY shortname
"""
# NOTE: properties->>'status' is lifecycle (onboarding / active / fully_suspended).
#       organizations.state is GEOGRAPHIC (CA, TX, Ontario) — NOT lifecycle.
#       Verified IMPLEMENTATION_PLAN Appendix A.


def fetch_cohort_from_db(executor: Executor, lifecycle: str) -> List[Dict]:
    """Query Postgres for all orgs at the given lifecycle.

    Used as fallback when REGISTRY.yaml is absent or yields no entries.
    Returns a list of dicts with keys shortname, org_id, flags=[].
    """
    rows = executor.all(_COHORT_BY_LIFECYCLE_SQL, {"lifecycle": lifecycle})
    return [{"shortname": r["shortname"], "org_id": r["id"], "flags": []} for r in rows]


# ---------------------------------------------------------------------------
# Scan execution
# ---------------------------------------------------------------------------

def run_scan(
    check_name: str,
    executor: Executor,
    clients: List[Dict],
) -> ScanRun:
    """Run a named check against each client in the cohort list.

    For each client:
      1. Resolve org_id if not already present (via ORG_BY_SHORTNAME).
      2. Apply registry flag suppressions → SKIP if applicable.
      3. Call the check function; capture any exception as an error row.
    """
    if check_name not in CHECKS:
        raise ValueError(
            f"Unknown check '{check_name}'. "
            f"Available: {', '.join(sorted(CHECKS))}"
        )
    _, check_fn = CHECKS[check_name]

    run = ScanRun(
        check=check_name,
        run_at=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )

    for client in clients:
        shortname = client.get("shortname", "")
        flags = client.get("flags") or []
        if isinstance(flags, str):
            flags = [f.strip() for f in flags.split(",") if f.strip()]

        # Resolve org_id — may already be set from fetch_cohort_from_db
        org_id = client.get("org_id")
        if org_id is None:
            org_row = executor.one(ORG_BY_SHORTNAME, {"shortname": shortname})
            if not org_row:
                run.results.append(ScanResult(
                    shortname=shortname, org_id=0, check=check_name, matched=False,
                    error=f"org '{shortname}' not found in organizations table — "
                          f"check shortname spelling",
                ))
                continue
            org_id = org_row["id"]

        # Suppress if a registry flag says so
        skip_reason = _skip_reason(check_name, flags)
        if skip_reason:
            run.results.append(ScanResult(
                shortname=shortname, org_id=org_id, check=check_name, matched=False,
                skipped=f"SKIP ({skip_reason})",
            ))
            continue

        # Execute the check
        try:
            result = check_fn(executor, org_id)
            result.shortname = shortname
            result.org_id = org_id
            run.results.append(result)
        except Exception as exc:
            run.results.append(ScanResult(
                shortname=shortname, org_id=org_id, check=check_name, matched=False,
                error=str(exc),
            ))

    return run


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_run(run: ScanRun, verbose: bool = False) -> str:
    desc = CHECKS.get(run.check, (run.check,))[0]
    lines = [
        f"fingerprint_scan  check={run.check}  run_at={run.run_at}",
        f"  {desc}",
        "",
    ]

    hits   = run.hits
    skips  = run.skips
    errors = run.errors
    clean  = run.clean

    if hits:
        lines.append(f"  MATCHES ({len(hits)}):")
        for r in hits:
            lines.append(f"    {r.shortname:<10}  value={r.value}")
    else:
        lines.append("  MATCHES: none")

    if skips:
        lines.append(f"  SKIPPED ({len(skips)}):")
        for r in skips:
            lines.append(f"    {r.shortname:<10}  {r.skipped}")

    if errors:
        lines.append(f"  ERRORS ({len(errors)}):")
        for r in errors:
            lines.append(f"    {r.shortname:<10}  {r.error}")

    if clean:
        if verbose:
            lines.append(f"  CLEAN  ({len(clean)}):")
            for r in clean:
                lines.append(f"    {r.shortname:<10}  value={r.value}")
        else:
            lines.append(
                f"  CLEAN  ({len(clean)}): {', '.join(r.shortname for r in clean)}"
            )

    lines.append(
        f"\n  {len(hits)} hit(s)  {len(skips)} skip(s)  "
        f"{len(errors)} error(s)  {len(clean)} clean"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli_main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Cross-tenant fingerprint scan — run a named check across all "
            "active onboarding orgs.  Reads eCat_Onboarding/REGISTRY.yaml for "
            "the cohort; falls back to a live DB query if the registry is absent."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "--check", choices=sorted(CHECKS),
        help="check to run across all orgs in the cohort",
    )
    ap.add_argument(
        "--lifecycle",
        default="onboarding",
        choices=["onboarding", "active", "fully_suspended", "all"],
        help=(
            "lifecycle filter applied to REGISTRY.yaml (default: onboarding). "
            "'all' includes every client in the registry regardless of lifecycle."
        ),
    )
    ap.add_argument(
        "--registry",
        default=_default_registry_path(),
        help="path to eCat_Onboarding/REGISTRY.yaml (default: auto-detected from script location)",
    )
    ap.add_argument(
        "--db-url", default=None,
        help="Postgres connection URL (default: DATABASE_URL env var)",
    )
    ap.add_argument(
        "--verbose", "-v", action="store_true",
        help="also print clean orgs individually instead of a summary line",
    )
    ap.add_argument(
        "--list-checks", action="store_true",
        help="list all available checks with descriptions and exit",
    )
    args = ap.parse_args(argv)

    if args.list_checks:
        print(f"{'Check':<22}  Description")
        print("-" * 22 + "  " + "-" * 55)
        for name, (desc, _) in sorted(CHECKS.items()):
            print(f"{name:<22}  {desc}")
        return 0

    if not args.check:
        ap.error("--check is required (or use --list-checks to see options)")

    # Load and filter registry
    clients_all = load_registry(args.registry)
    lifecycle   = None if args.lifecycle == "all" else args.lifecycle
    clients     = filter_registry(clients_all, lifecycle)

    # Connect to DB
    try:
        conn     = connect(args.db_url)
        executor = Executor(conn)
    except (EnvironmentError, ImportError) as exc:
        print(f"DB connection failed: {exc}", file=sys.stderr)
        return 2

    # Fall back to a DB cohort query when registry yields nothing
    if not clients:
        fallback_lifecycle = args.lifecycle if args.lifecycle != "all" else "onboarding"
        print(
            f"No registry entries matched lifecycle={args.lifecycle!r}. "
            f"Querying DB for lifecycle={fallback_lifecycle!r}.",
            file=sys.stderr,
        )
        clients = fetch_cohort_from_db(executor, fallback_lifecycle)
        if not clients:
            print(
                f"No orgs found for lifecycle={fallback_lifecycle!r}. "
                "Check VPN connectivity and the lifecycle value.",
                file=sys.stderr,
            )
            return 1

    run = run_scan(args.check, executor, clients)
    print(format_run(run, verbose=args.verbose))
    # Exit non-zero only on hard errors (not on MATCH or SKIP)
    return 1 if run.errors else 0


if __name__ == "__main__":
    sys.exit(_cli_main())
