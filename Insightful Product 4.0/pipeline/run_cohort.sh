#!/usr/bin/env bash
# Cohort runner: fan out `python -m pipeline.run_cohort --org X` across a
# list of orgs so a single org's failure doesn't kill the cohort. When
# done, invoke the summarizer to print the 4-bucket segmentation.
#
# Usage:
#   pipeline/run_cohort.sh --orgs sarreid,cci,hfg,kal,sca [--date YYYY-MM-DD] [--run-id ID] [--populate-cache]
#
# Defaults:
#   --date       today (UTC)
#   --run-id     $DATE
#   --populate-cache  skipped by default (cache must already exist);
#                     pass this to run pipeline.populate_cache first.
#
# Output:
#   pipeline/cohort_runs/{run-id}/status.csv   (appended per org)
#   stdout: 4-bucket segmentation table at end
#
# Notes:
#   - Cache population is a separate concern; when DB creds are set, pass
#     --populate-cache. When cache is loaded through MCP (dev flow), leave
#     it off and just run the loop.
#   - The pipeline uses --cohort-validation for every org (draft profile
#     emitted for un-ratified orgs; ratified orgs use their profile).

set -uo pipefail

# ─── Locate ourselves so this script works from any CWD ────────────────────
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
WORKSPACE_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"
PYTHON="$WORKSPACE_ROOT/.venv-renderer/bin/python"

# ─── Args ──────────────────────────────────────────────────────────────────
ORGS=""
DATE="$( date -u +%Y-%m-%d )"
RUN_ID=""
POPULATE_CACHE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --orgs) ORGS="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --run-id) RUN_ID="$2"; shift 2 ;;
    --populate-cache) POPULATE_CACHE=1; shift ;;
    -h|--help)
      grep -E '^# ' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$ORGS" ]]; then
  echo "ERROR: --orgs required (e.g. --orgs sarreid,cci,hfg,kal,sca)" >&2
  exit 2
fi
RUN_ID="${RUN_ID:-$DATE}"

STATUS_DIR="$WORKSPACE_ROOT/pipeline/cohort_runs/$RUN_ID"
mkdir -p "$STATUS_DIR"
LOG="$STATUS_DIR/run.log"

echo "cohort run: id=$RUN_ID date=$DATE orgs=$ORGS" | tee -a "$LOG"
echo "status.csv: $STATUS_DIR/status.csv"           | tee -a "$LOG"

# ─── Loop per org ──────────────────────────────────────────────────────────
IFS=',' read -ra ORG_ARR <<< "$ORGS"
N=${#ORG_ARR[@]}
i=0
for ORG in "${ORG_ARR[@]}"; do
  i=$((i+1))
  ORG="$(echo "$ORG" | tr -d '[:space:]')"
  [[ -z "$ORG" ]] && continue
  echo ""                                                              | tee -a "$LOG"
  echo "── [$i/$N] $ORG ────────────────────────────────────────────"  | tee -a "$LOG"

  if [[ "$POPULATE_CACHE" -eq 1 ]]; then
    echo "  populating cache…" | tee -a "$LOG"
    "$PYTHON" -m pipeline.populate_cache --org "$ORG" --date "$DATE" 2>&1 | tee -a "$LOG" || {
      echo "  populate_cache FAILED for $ORG — will still try to run against existing cache" | tee -a "$LOG"
    }
  fi

  "$PYTHON" -m pipeline.run_cohort --org "$ORG" --date "$DATE" --run-id "$RUN_ID" 2>&1 | tee -a "$LOG"
  # continue on non-zero exit; the per-org row is already appended to status.csv
done

# ─── Summarize ─────────────────────────────────────────────────────────────
echo ""                                                                | tee -a "$LOG"
echo "── SUMMARY ─────────────────────────────────────────────────"    | tee -a "$LOG"
"$PYTHON" -m pipeline.run_cohort --summarize --run-id "$RUN_ID"        | tee -a "$LOG"
