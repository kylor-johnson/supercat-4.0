"""Cohort orchestrator: run the pipeline across a list of orgs, write a
status.csv per date-stamped run, and produce the four-bucket
segmentation the sales workflow lives on.

Two modes:

  # Loop mode: run the pipeline for each org, append a row to status.csv.
  # (This is what run_cohort.sh calls per-org.)
  python -m pipeline.run_cohort --org X --date YYYY-MM-DD --run-id RUN_ID

  # Summarize mode: read status.csv from a run and print the 4-bucket
  # taxonomy (Mode-1 STRONG / Mode-1 degraded / Mode-2 / Gate-STOP).
  python -m pipeline.run_cohort --summarize --run-id RUN_ID

Design notes:
  - Loop mode is single-org so each run's exit code and status row are
    isolated. The bash wrapper (run_cohort.sh) fans out per org so a
    single org's failure doesn't kill the cohort.
  - status.csv is APPENDED to (not rewritten), so partial cohort runs
    are recoverable — re-run just the missing orgs.
  - We do not populate cache from here; the caller decides whether to
    run populate_cache.py first (needed for orgs whose cache is stale
    or absent). This module is orchestration only.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import subprocess
import sys
from collections import Counter
from pathlib import Path

from . import config


# ─── Status CSV ────────────────────────────────────────────────────────────
STATUS_COLUMNS = [
    "org",
    "report_through_date",
    "report_mode",
    "commerce_confidence",
    "rep_identity_tier",
    "channel_posture",
    "exit_code",
    "draft_path",
    "notes",
]


def cohort_run_dir(run_id: str) -> Path:
    return config.PIPELINE_DIR / "cohort_runs" / run_id


def status_csv_path(run_id: str) -> Path:
    return cohort_run_dir(run_id) / "status.csv"


def _append_status_row(run_id: str, row: dict) -> None:
    """Append one row to status.csv, creating the file (with header) if needed."""
    path = status_csv_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=STATUS_COLUMNS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in STATUS_COLUMNS})


# ─── Loop mode: run one org, append a status row ───────────────────────────
def _run_one(org: str, date: str, run_id: str) -> int:
    """Invoke run_report.py --cohort-validation for a single org, capture
    the emitted posture from stdout, append one row to status.csv.

    Returns the exit code (0 = success). Never raises — cohort runs must
    tolerate per-org failure without killing the whole cohort.
    """
    cmd = [
        sys.executable,
        "-m",
        "pipeline.run_report",
        "--org", org,
        "--date", date,
        "--cohort-validation",
    ]
    row: dict = {"org": org, "report_through_date": date, "notes": ""}
    # Mode 1 writes _DRAFT_, Mode 2 / Gate-STOP writes _GATESTOP_. Check
    # both; whichever exists after the run is the artifact.
    draft_path = config.OUTPUTS_DIR / f"{org}_DRAFT_{date}.md"
    gatestop_path = config.OUTPUTS_DIR / f"{org}_GATESTOP_{date}.md"
    try:
        result = subprocess.run(
            cmd,
            cwd=str(config.WORKSPACE_ROOT),
            capture_output=True,
            text=True,
            timeout=300,  # 5 min per org
        )
        row["exit_code"] = result.returncode
        for p in (draft_path, gatestop_path):
            if p.exists():
                row["draft_path"] = str(p.relative_to(config.WORKSPACE_ROOT))
                break
        else:
            row["draft_path"] = ""
        # Parse the "preflight: mode=... confidence=... tier=..." line from stdout
        for line in result.stdout.splitlines():
            if line.startswith("preflight:"):
                # preflight: mode=Mode 1 - Standard confidence=STRONG tier=2
                # We split by " confidence=" and " tier=" to keep the mode string intact.
                try:
                    mode_part, rest = line.split(" confidence=", 1)
                    conf, tier = rest.split(" tier=", 1)
                    row["report_mode"] = mode_part.replace("preflight: mode=", "").strip()
                    row["commerce_confidence"] = conf.strip()
                    row["rep_identity_tier"] = tier.strip()
                except ValueError:
                    row["notes"] = f"unparseable preflight line: {line!r}"
        if result.returncode != 0:
            row["notes"] = (row.get("notes") or "") + f" stderr: {result.stderr.strip()[:400]}"
        # channel_posture: try to load from posture if the draft exists — cheap re-import
        try:
            score_date = dt.date.fromisoformat(date)
            from . import preflight  # local import to keep top import list clean
            posture = preflight.run(org, score_date, cohort_validation=True)
            row["channel_posture"] = posture.channel_posture
        except Exception as e:
            row["notes"] = (row.get("notes") or "") + f" (posture re-read failed: {type(e).__name__})"
    except subprocess.TimeoutExpired:
        row["exit_code"] = 124
        row["notes"] = "TIMEOUT after 300s"
    except Exception as e:
        row["exit_code"] = 1
        row["notes"] = f"orchestrator error: {type(e).__name__}: {e}"

    _append_status_row(run_id, row)
    return int(row.get("exit_code") or 0)


# ─── Summarize mode: 4-bucket taxonomy ─────────────────────────────────────
def _bucket(mode: str, confidence: str) -> str:
    """Assign one of the four sales-workflow buckets.

    Bucket semantics (from the plan):
      Mode-1 STRONG      → premium pitch (full CEO Intelligence Report)
      Mode-1 degraded    → mid pitch, gap called out (some suppressions)
      Mode-2             → Rep Copilot pitch (Activation report)
      Gate-STOP          → sales-conversation only (no report ships)
    """
    m = (mode or "").strip()
    c = (confidence or "").strip().upper()
    if m == "Gate-STOP":
        return "Gate-STOP"
    if m.startswith("Mode 2"):
        return "Mode-2 (Rep Copilot pitch)"
    if m == "Mode 1 - Standard" and c == "STRONG":
        return "Mode-1 STRONG (premium pitch)"
    if m.startswith("Mode 1"):
        return "Mode-1 degraded (mid pitch with gap)"
    return "UNKNOWN"


def summarize(run_id: str) -> int:
    """Read status.csv for `run_id`, print the 4-bucket segmentation table
    to stdout. Returns process exit code (0 always; missing file is a
    warn-and-continue).
    """
    path = status_csv_path(run_id)
    if not path.exists():
        print(f"summarize: no status.csv at {path}", file=sys.stderr)
        return 2

    rows = list(csv.DictReader(path.open("r", encoding="utf-8")))
    if not rows:
        print(f"summarize: status.csv empty at {path}", file=sys.stderr)
        return 2

    buckets: Counter = Counter()
    by_bucket: dict[str, list[str]] = {}
    exit_failures: list[str] = []
    for r in rows:
        bucket = _bucket(r.get("report_mode", ""), r.get("commerce_confidence", ""))
        buckets[bucket] += 1
        by_bucket.setdefault(bucket, []).append(r["org"])
        if str(r.get("exit_code", "0")) != "0":
            exit_failures.append(f"{r['org']} (exit={r.get('exit_code')})")

    print(f"# Cohort segmentation — run_id={run_id}  |  n_orgs={len(rows)}")
    print()
    order = [
        "Mode-1 STRONG (premium pitch)",
        "Mode-1 degraded (mid pitch with gap)",
        "Mode-2 (Rep Copilot pitch)",
        "Gate-STOP",
        "UNKNOWN",
    ]
    print("| Bucket | Count | Orgs |")
    print("|---|---:|---|")
    for b in order:
        if buckets.get(b, 0) == 0:
            continue
        orgs = ", ".join(sorted(by_bucket[b]))
        print(f"| {b} | {buckets[b]} | {orgs} |")
    print()
    if exit_failures:
        print(f"## Failures ({len(exit_failures)})")
        for f in exit_failures:
            print(f"- {f}")
    print()
    print(f"status.csv: {path.relative_to(config.WORKSPACE_ROOT)}")
    return 0


# ─── CLI ───────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="python -m pipeline.run_cohort",
        description="Cohort orchestrator: run pipeline across N orgs + emit status/segmentation.",
    )
    p.add_argument("--org", help="single org to run (loop mode)")
    p.add_argument("--date", help="report-through date (YYYY-MM-DD)")
    p.add_argument("--run-id", required=True, help="run identifier (used to group status.csv)")
    p.add_argument("--summarize", action="store_true", help="print the 4-bucket segmentation for --run-id")
    args = p.parse_args(argv)

    if args.summarize:
        return summarize(args.run_id)

    if not args.org or not args.date:
        p.error("--org and --date required in loop mode")
    return _run_one(args.org, args.date, args.run_id)


if __name__ == "__main__":
    sys.exit(main())
