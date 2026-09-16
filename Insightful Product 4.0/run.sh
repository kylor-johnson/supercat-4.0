#!/usr/bin/env bash
# run.sh — single entry point for the Insightful 4.0 CEO report pipeline.
#
# Usage:
#   ./run.sh {org}                        # full run → SHIP or REDIRECT
#   ./run.sh {org} --date YYYY-MM-DD      # pinned cache date
#   ./run.sh {org} --preview              # draft-profile run, labeled PREVIEW
#   ./run.sh --cohort org1,org2,...        # batch (delegates to run_cohort.sh)
#   ./run.sh {org} --populate-cache       # populate cache before running
#
# Exit codes:
#   0  SHIP, PREVIEW, or REDIRECT handled cleanly
#   1  smoke_check or step10_check failure
#   2  REDIRECT (zero-signal org — no invoices AND no eCat)
#   3  hard failure (missing cache, Python error)
#
# Outcomes:
#   SHIP        Default for every org that has cache data — profile is
#               auto-derived if missing → full CEO Brief HTML
#   PREVIEW     Only when --preview is explicitly passed → internal HTML
#   REDIRECT    Zero signal → no HTML, internal Gate-STOP MD only

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PY="$ROOT/.venv-renderer/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "ERROR: Python not found at $PY" >&2
  echo "  Set up the venv: python3 -m venv .venv-renderer && .venv-renderer/bin/pip install -r requirements-pipeline.txt" >&2
  exit 3
fi

# ─── Parse args ─────────────────────────────────────────────────────────────
ORG=""
DATE="$(date -u +%Y-%m-%d)"
PREVIEW=0
COHORT=""
POPULATE_CACHE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date)          DATE="$2"; shift 2 ;;
    --preview)       PREVIEW=1; shift ;;
    --cohort)        COHORT="$2"; shift 2 ;;
    --populate-cache) POPULATE_CACHE=1; shift ;;
    -h|--help)
      sed -n '2,/^$/{ s/^# \?//; p; }' "$0"
      exit 0
      ;;
    -*)              echo "Unknown flag: $1" >&2; exit 3 ;;
    *)
      if [[ -z "$ORG" ]]; then
        ORG="$1"; shift
      else
        echo "ERROR: unexpected positional arg: $1" >&2; exit 3
      fi
      ;;
  esac
done

# ─── Cohort mode (delegate and exit) ───────────────────────────────────────
if [[ -n "$COHORT" ]]; then
  COHORT_ARGS=(--orgs "$COHORT" --date "$DATE")
  [[ "$POPULATE_CACHE" -eq 1 ]] && COHORT_ARGS+=(--populate-cache)
  exec "$ROOT/pipeline/run_cohort.sh" "${COHORT_ARGS[@]}"
fi

if [[ -z "$ORG" ]]; then
  echo "ERROR: org required. Usage: ./run.sh {org} [--date YYYY-MM-DD] [--preview]" >&2
  exit 3
fi

# ─── Resolve profile ───────────────────────────────────────────────────────
PROFILE_RATIFIED="$ROOT/profiles/${ORG}.md"
PROFILE_DRAFT="$ROOT/profiles/${ORG}.draft.md"

if [[ -f "$PROFILE_RATIFIED" ]]; then
  PROFILE="$PROFILE_RATIFIED"
  PROFILE_TYPE="ratified"
elif [[ -f "$PROFILE_DRAFT" ]]; then
  PROFILE="$PROFILE_DRAFT"
  PROFILE_TYPE="draft"
else
  PROFILE=""
  PROFILE_TYPE="none"
fi

# ─── Determine pipeline flags ──────────────────────────────────────────────
# No branching on profile state: the pipeline auto-derives profiles/{org}.md
# internally when it's missing, so no flag is needed here.
PIPELINE_FLAGS=(--org "$ORG" --date "$DATE")

# ─── Populate cache if requested ────────────────────────────────────────────
if [[ "$POPULATE_CACHE" -eq 1 ]]; then
  echo "── Populating cache for $ORG ($DATE) ──"
  "$PY" -m pipeline.populate_cache --org "$ORG" --date "$DATE" || {
    echo "ERROR: cache population failed" >&2
    exit 3
  }
  # If populate_cache fell back to MCP mode, it wrote .sql files but no CSVs.
  # The agent needs to run those through MCP execute_sql first.
  CACHE_DIR="$ROOT/pipeline/cache/$ORG/$DATE"
  CSV_COUNT=$(find "$CACHE_DIR" -maxdepth 1 -name "*.csv" 2>/dev/null | wc -l | tr -d ' ')
  SQL_COUNT=$(find "$CACHE_DIR" -maxdepth 1 -name "*.sql" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$SQL_COUNT" -gt 0 && "$CSV_COUNT" -lt 3 ]]; then
    echo ""
    echo "ERROR: cache has $CSV_COUNT CSVs but $SQL_COUNT pending .sql files" >&2
    echo "  The .sql files need to be run through MCP execute_sql first." >&2
    echo "  See the populate_cache output above for instructions." >&2
    exit 3
  fi
fi

# ─── Clean stale outputs (prevents cross-run confusion) ──────────────────
rm -f "$ROOT/outputs/${ORG}_GATESTOP_${DATE}.md"
rm -f "$ROOT/outputs/${ORG}_DRAFT_${DATE}.md"

# ─── Run pipeline ──────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  Insightful 4.0 — $ORG — $DATE"
echo "══════════════════════════════════════════════════════════════"
echo ""

PIPELINE_OUT=$("$PY" -m pipeline.run_report "${PIPELINE_FLAGS[@]}" 2>&1) || {
  RC=$?
  echo "$PIPELINE_OUT"
  if [[ $RC -eq 2 ]]; then
    echo "ERROR: pipeline exited 2 (missing cache)" >&2
    exit 3
  fi
  echo "ERROR: pipeline failed (exit $RC)" >&2
  exit 1
}
echo "$PIPELINE_OUT"

# ─── Check outcome: GATESTOP → REDIRECT (zero-signal only) ────────────────
GATESTOP_MD="$ROOT/outputs/${ORG}_GATESTOP_${DATE}.md"
DRAFT_MD="$ROOT/outputs/${ORG}_DRAFT_${DATE}.md"

if [[ -f "$GATESTOP_MD" ]]; then
  echo ""
  echo "┌──────────────────────────────────────────────────────────┐"
  echo "│  REDIRECT                                                │"
  echo "│                                                          │"
  echo "│  $ORG has zero commerce signal (no invoices, no eCat).   │"
  echo "│  No HTML report created.                                 │"
  echo "│                                                          │"
  echo "│  Next step: operators/rep_copilot_operator.md             │"
  echo "│  Internal artifact: outputs/${ORG}_GATESTOP_${DATE}.md   │"
  echo "└──────────────────────────────────────────────────────────┘"
  exit 2
fi

if [[ ! -f "$DRAFT_MD" ]]; then
  echo "ERROR: expected output at $DRAFT_MD but not found" >&2
  exit 3
fi

# ─── Re-resolve profile (the pipeline may have just auto-derived it) ───────
if [[ -f "$PROFILE_RATIFIED" ]]; then
  PROFILE="$PROFILE_RATIFIED"
  PROFILE_TYPE="ratified"
fi

# ─── Derive output paths (canonical naming) ────────────────────────────────
HTML_OUT=$("$PY" -c "
import sys
sys.path.insert(0, '$ROOT')
from pathlib import Path
from report_render.naming import (
    parse_display_name_from_profile_text,
    ship_html_filename,
    preview_html_filename,
)

org = '${ORG}'
date = '${DATE}'
preview = ${PREVIEW} != 0
profile_path = Path('${PROFILE:-}')

if preview:
    print('PREVIEW|' + preview_html_filename(org, date))
else:
    text = profile_path.read_text(encoding='utf-8') if profile_path.exists() else ''
    display = parse_display_name_from_profile_text(text, org)
    print('SHIP|' + ship_html_filename(display, date))
" 2>/dev/null) || { echo "ERROR: failed to derive output path" >&2; exit 3; }

OUTCOME="${HTML_OUT%%|*}"
HTML_OUT="$ROOT/outputs/${HTML_OUT#*|}"

RENDER_ARGS=(--md "$DRAFT_MD" --out "$HTML_OUT")
[[ -n "${PROFILE:-}" ]] && RENDER_ARGS+=(--profile "$PROFILE")

"$PY" -m report_render.html_renderer "${RENDER_ARGS[@]}" || {
  echo "ERROR: HTML render failed" >&2
  exit 3
}

# ─── Step-10 quality audit ─────────────────────────────────────────────────
STEP10_ARGS=(--html "$HTML_OUT")
[[ -f "$DRAFT_MD" ]] && STEP10_ARGS+=(--md "$DRAFT_MD")

"$PY" -m report_render.step10_check "${STEP10_ARGS[@]}" || {
  echo ""
  echo "┌──────────────────────────────────────────────────────────┐"
  echo "│  FAIL — step10_check did not pass                        │"
  echo "│  Review the violations above.                            │"
  echo "└──────────────────────────────────────────────────────────┘"
  exit 1
}

# ─── Final outcome ─────────────────────────────────────────────────────────
echo ""
if [[ "$OUTCOME" == "SHIP" ]]; then
  echo "┌──────────────────────────────────────────────────────────┐"
  echo "│  SHIP                                                    │"
  echo "│                                                          │"
  echo "│  Client-ready CEO Brief:                                 │"
  echo "│  $(basename "$HTML_OUT")"
  echo "│                                                          │"
  echo "│  smoke_check: PASS  ·  step10: PASS                     │"
  echo "└──────────────────────────────────────────────────────────┘"
else
  echo "┌──────────────────────────────────────────────────────────┐"
  echo "│  PREVIEW (not client-facing)                             │"
  echo "│                                                          │"
  echo "│  Internal preview:                                       │"
  echo "│  $(basename "$HTML_OUT")"
  echo "│                                                          │"
  echo "│  --preview was passed — profile: $PROFILE_TYPE.          │"
  echo "│  smoke_check: PASS  ·  step10: PASS                     │"
  echo "└──────────────────────────────────────────────────────────┘"
fi

exit 0
