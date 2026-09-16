"""
Insightful Product 3.0 — Batch Runner

Runs data_gather + detect_signals + build_context for multiple clients in
parallel. Outputs a manifest of clients ready for section agents.

The LLM-dependent work (section agents + signal summary) must still be
triggered separately — this script handles all the deterministic prep.

Usage:
    python batch_run.py --shortnames cci,kal,shl,mlc --parallel 4
    python batch_run.py --file client_list.txt --parallel 3
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path


def resolve_org_id(shortname: str) -> int | None:
    """Resolve org_id from shortname via Postgres MCP. Returns None on failure."""
    try:
        result = subprocess.run(
            ["python", "-c", f"""
import sys
sys.path.insert(0, '.')
from data_gather import McpSessionManager, MCP_PG_URL, run_pg
mgr = McpSessionManager(MCP_PG_URL)
mgr.start()
try:
    rows = run_pg("SELECT id FROM organizations WHERE shortname = %s LIMIT 1", ('{shortname}',))
    if rows:
        print(rows[0]['id'])
    else:
        print('NONE')
finally:
    mgr.close()
"""],
            capture_output=True, text=True, timeout=30,
            cwd=Path(__file__).resolve().parent,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            return int(result.stdout.strip())
    except Exception:
        pass
    return None


def run_client_pipeline(shortname: str, org_id: int, run_date: str, scripts_dir: Path) -> dict:
    """Run the full deterministic pipeline for one client."""
    result = {"shortname": shortname, "org_id": org_id, "status": "ok", "errors": [], "elapsed": 0.0}
    start = time.monotonic()

    # Step 1: data_gather.py
    cmd = [
        sys.executable, str(scripts_dir / "data_gather.py"),
        "--shortname", shortname,
        "--org-id", str(org_id),
        "--run-date", run_date,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=str(scripts_dir))
    if proc.returncode != 0:
        result["status"] = "failed_data_gather"
        result["errors"].append(proc.stderr[-500:] if proc.stderr else "Unknown error")
        result["elapsed"] = time.monotonic() - start
        return result

    # Step 2: detect_signals.py
    cmd = [
        sys.executable, str(scripts_dir / "detect_signals.py"),
        "--shortname", shortname,
        "--run-date", run_date,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(scripts_dir))
    if proc.returncode != 0:
        result["status"] = "failed_signals"
        result["errors"].append(proc.stderr[-500:] if proc.stderr else "Unknown error")
        result["elapsed"] = time.monotonic() - start
        return result

    # Step 3: build_context.py
    cmd = [
        sys.executable, str(scripts_dir / "build_context.py"),
        "--shortname", shortname,
        "--run-date", run_date,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(scripts_dir))
    if proc.returncode != 0:
        result["status"] = "failed_context"
        result["errors"].append(proc.stderr[-500:] if proc.stderr else "Unknown error")
        result["elapsed"] = time.monotonic() - start
        return result

    result["elapsed"] = time.monotonic() - start
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Insightful 3.0 — Batch Runner")
    parser.add_argument("--shortnames", help="Comma-separated list of shortnames")
    parser.add_argument("--file", help="Path to file with one shortname per line")
    parser.add_argument("--run-date", default=date.today().isoformat(), help="Run date (default: today)")
    parser.add_argument("--parallel", type=int, default=3, help="Max parallel clients (default: 3)")
    parser.add_argument("--org-ids", help="Comma-separated org_ids matching shortnames (optional)")
    args = parser.parse_args()

    if args.shortnames:
        shortnames = [s.strip() for s in args.shortnames.split(",") if s.strip()]
    elif args.file:
        shortnames = [l.strip() for l in Path(args.file).read_text().splitlines() if l.strip() and not l.startswith("#")]
    else:
        print("ERROR: Provide --shortnames or --file")
        sys.exit(1)

    org_ids: dict[str, int] = {}
    if args.org_ids:
        ids = [int(x.strip()) for x in args.org_ids.split(",")]
        if len(ids) == len(shortnames):
            org_ids = dict(zip(shortnames, ids))

    scripts_dir = Path(__file__).resolve().parent
    run_date = args.run_date

    print(f"{'='*60}")
    print(f"  Insightful 3.0 — Batch Run")
    print(f"  Clients: {len(shortnames)} | Parallel: {args.parallel} | Date: {run_date}")
    print(f"{'='*60}\n")

    if not org_ids:
        print("Resolving org_ids... (provide --org-ids to skip this step)")
        print("  NOTE: org_id resolution requires VPN + MCP. If unavailable,")
        print("  provide --org-ids explicitly.\n")

    results: list[dict] = []
    batch_start = time.monotonic()

    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futures = {}
        for shortname in shortnames:
            oid = org_ids.get(shortname, 0)
            if oid == 0:
                oid = 1  # placeholder — data_gather.py will resolve from shortname
            future = pool.submit(run_client_pipeline, shortname, oid, run_date, scripts_dir)
            futures[future] = shortname

        for future in as_completed(futures):
            shortname = futures[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"shortname": shortname, "status": "exception", "errors": [str(e)], "elapsed": 0}
            results.append(result)
            status_icon = "✓" if result["status"] == "ok" else "✗"
            print(f"  {status_icon} {shortname:12s} {result['status']:20s} ({result['elapsed']:.1f}s)")

    batch_elapsed = time.monotonic() - batch_start

    print(f"\n{'='*60}")
    print(f"  Batch Complete — {batch_elapsed:.1f}s total")
    print(f"{'='*60}\n")

    ready = [r for r in results if r["status"] == "ok"]
    failed = [r for r in results if r["status"] != "ok"]

    print(f"  Ready for section agents: {len(ready)}/{len(results)}")
    if failed:
        print(f"  Failed: {len(failed)}")
        for f in failed:
            print(f"    - {f['shortname']}: {f['status']} — {f['errors'][0][:80] if f['errors'] else '?'}")

    # Write manifest
    manifest_path = scripts_dir.parent / "runs" / f"batch_{run_date}_manifest.md"
    manifest_lines = [
        f"# Batch Manifest — {run_date}",
        f"- **Clients processed**: {len(results)}",
        f"- **Ready for section agents**: {len(ready)}",
        f"- **Failed**: {len(failed)}",
        f"- **Total elapsed**: {batch_elapsed:.1f}s",
        "",
        "## Ready for LLM Section Agents",
        "",
        "| Shortname | Elapsed | Bundles Dir |",
        "| --- | --- | --- |",
    ]
    for r in sorted(ready, key=lambda x: x["shortname"]):
        bundle_dir = f"runs/{r['shortname']}_{run_date}/cache/"
        manifest_lines.append(f"| {r['shortname']} | {r['elapsed']:.1f}s | `{bundle_dir}` |")

    if failed:
        manifest_lines.extend(["", "## Failed", ""])
        for f in failed:
            manifest_lines.append(f"- **{f['shortname']}**: {f['status']} — {f['errors'][0][:100] if f['errors'] else '?'}")

    manifest_lines.extend(["", "## Next Steps", "",
        "For each ready client, spawn a fresh agent with the orchestrator prompt.",
        "The agent only needs to:",
        "1. Spawn 5 section agents (parallel) using section_build_prompt.md",
        "2. Build Signal Summary (§1) from highlights + signal_rank",
        "3. Run: `python scripts/assemble_report.py --shortname X --run-date Y`",
        "4. Run: `python scripts/audit_report.py --shortname X --run-date Y`",
    ])

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("\n".join(manifest_lines), encoding="utf-8")
    print(f"\n  Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
