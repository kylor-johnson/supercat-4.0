#!/usr/bin/env bash
# regression.sh — golden-set cohort regression for Insightful 4.0 (v9 split verification)
#
# Split verification model:
#   Gate 1 — deterministic_core_sha256: report with LLM slots replaced by stable
#            placeholders must be byte-identical across runs
#   Gate 2 — prose_conformance: LLM slot prose must pass validate_slot() against
#            the run's serialized fact bundles
#   Gate 3 — ship_html_bytes_range: total file size within expected range (handles
#            LLM prose length variation)
#
# Usage:
#   ./regression.sh              # run full golden set, verify both gates
#   ./regression.sh --verify     # checksum only (skip re-run; use after manual runs)
#   ./regression.sh --update     # re-run and PRINT new checksums (does NOT write
#                                 the manifest). To actually re-stamp, review
#                                 ./tools/cohort_diff.sh --full first, then run
#                                 ./tools/restamp_golden.py --note "..."
#
# Exit: 0 all pass, 1 any failure

set -uo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PY="$ROOT/.venv-renderer/bin/python"
MANIFEST="$ROOT/config/golden_set.json"
MODE="run"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --verify) MODE="verify"; shift ;;
    --update) MODE="update"; shift ;;
    -h|--help)
      sed -n '2,/^$/{ s/^# \?//; p; }' "$0"
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -x "$PY" ]]; then
  echo "ERROR: venv not found at $PY" >&2
  exit 2
fi

sha256_file() {
  shasum -a 256 "$1" | awk '{print $1}'
}

deterministic_core_sha() {
  "$PY" -m pipeline.extract_deterministic_core "$1" | shasum -a 256 | awk '{print $1}'
}

deterministic_core_bytes() {
  "$PY" -m pipeline.extract_deterministic_core "$1" | wc -c | tr -d ' '
}

FAIL=0
PASS=0

echo "══════════════════════════════════════════════════════════════"
echo "  Insightful 4.0 — Golden-set regression (v9 split verification)"
echo "  manifest: config/golden_set.json"
echo "  mode: $MODE"
echo "══════════════════════════════════════════════════════════════"
echo ""

ORGS=$("$PY" -c "
import json
from pathlib import Path
data = json.loads(Path('$MANIFEST').read_text())
for row in data['orgs']:
    print(row['org'])
")

while IFS= read -r ORG; do
  [[ -z "$ORG" ]] && continue

  ROW=$("$PY" -c "
import json
from pathlib import Path
data = json.loads(Path('$MANIFEST').read_text())
for row in data['orgs']:
    if row['org'] == '$ORG':
        import json as j
        print(j.dumps(row))
        break
")

  OUTCOME=$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['outcome'])")
  EXPECT_EXIT=$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['exit_code'])")
  DATE=$(echo "$ROW" | "$PY" -c "import json,sys; r=json.load(sys.stdin); print(r.get('cache_date', json.load(open('$MANIFEST'))['cache_date']))")

  echo "── $ORG ($OUTCOME, date=$DATE) ──"

  if [[ "$MODE" != "verify" ]]; then
    set +e
    "$ROOT/run.sh" "$ORG" --date "$DATE" > /tmp/insightful_regression_${ORG}.log 2>&1
    ACTUAL_EXIT=$?
    set -e
    if [[ "$ACTUAL_EXIT" -ne "$EXPECT_EXIT" ]]; then
      echo "  FAIL exit code: expected $EXPECT_EXIT, got $ACTUAL_EXIT"
      tail -5 /tmp/insightful_regression_${ORG}.log | sed 's/^/    /'
      FAIL=$((FAIL + 1))
      continue
    fi
    echo "  exit code: $ACTUAL_EXIT ✓"
  fi

  case "$OUTCOME" in
    SHIP|PREVIEW)
      if [[ "$OUTCOME" == "SHIP" ]]; then
        FILE="$ROOT/outputs/$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['ship_html'])")"
      else
        FILE="$ROOT/outputs/$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['preview_html'])")"
      fi
      ;;
    REDIRECT)
      FILE="$ROOT/outputs/$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['gatestop_md'])")"
      EXPECT_SHA=$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin).get('gatestop_md_sha256',''))")
      EXPECT_BYTES=$(echo "$ROW" | "$PY" -c "import json,sys; print(json.load(sys.stdin).get('gatestop_md_bytes',0))")
      FORBIDDEN=$(ls "$ROOT/outputs/"*_CEO_intelligence_report_${DATE}.html 2>/dev/null | grep -i sca || true)
      if [[ -n "$FORBIDDEN" ]]; then
        echo "  FAIL REDIRECT: forbidden SHIP HTML exists: $FORBIDDEN"
        FAIL=$((FAIL + 1))
        continue
      fi
      # REDIRECT files are fully deterministic (no LLM slots) — check full SHA
      if [[ -f "$FILE" ]]; then
        ACTUAL_SHA=$(sha256_file "$FILE")
        ACTUAL_BYTES=$(wc -c < "$FILE" | tr -d ' ')
        if [[ "$MODE" == "update" ]]; then
          echo "  $(basename "$FILE"): bytes=$ACTUAL_BYTES sha256=$ACTUAL_SHA"
          PASS=$((PASS + 1))
        elif [[ -n "$EXPECT_SHA" && "$ACTUAL_SHA" != "$EXPECT_SHA" ]]; then
          echo "  FAIL checksum: $(basename "$FILE")"
          echo "    expected: $EXPECT_BYTES bytes, $EXPECT_SHA"
          echo "    actual:   $ACTUAL_BYTES bytes, $ACTUAL_SHA"
          FAIL=$((FAIL + 1))
        else
          echo "  $(basename "$FILE"): $ACTUAL_BYTES bytes, sha256 match ✓"
          PASS=$((PASS + 1))
        fi
      else
        echo "  FAIL missing: $(basename "$FILE")"
        FAIL=$((FAIL + 1))
      fi
      continue
      ;;
    *)
      echo "  FAIL unknown outcome: $OUTCOME"
      FAIL=$((FAIL + 1))
      continue
      ;;
  esac

  if [[ ! -f "$FILE" ]]; then
    echo "  FAIL missing: $(basename "$FILE")"
    FAIL=$((FAIL + 1))
    continue
  fi

  ACTUAL_BYTES=$(wc -c < "$FILE" | tr -d ' ')

  # ─── Gate 1: Deterministic core checksum ───
  ACTUAL_CORE_SHA=$(deterministic_core_sha "$FILE")
  ACTUAL_CORE_BYTES=$(deterministic_core_bytes "$FILE")
  EXPECT_CORE_SHA=$(echo "$ROW" | "$PY" -c "import json,sys; r=json.load(sys.stdin); print(r.get('deterministic_core_sha256', r.get('ship_html_sha256', r.get('preview_html_sha256',''))))")

  if [[ "$MODE" == "update" ]]; then
    echo "  $(basename "$FILE"):"
    echo "    deterministic_core_sha256=$ACTUAL_CORE_SHA"
    echo "    deterministic_core_bytes=$ACTUAL_CORE_BYTES"
    echo "    ship_html_bytes=$ACTUAL_BYTES"

    # Gate 2 (update mode): just run conformance and report
    BUNDLES="$ROOT/outputs/${ORG}_bundles_${DATE}.json"
    if [[ -f "$BUNDLES" ]]; then
      set +e
      "$PY" -m pipeline.prose_conformance_check "$FILE" "$BUNDLES" 2>&1 | tail -3 | sed 's/^/    /'
      set -e
    else
      echo "    (no bundles file — prose conformance skipped)"
    fi
    PASS=$((PASS + 1))
    continue
  fi

  # Gate 1 check
  if [[ -n "$EXPECT_CORE_SHA" && "$ACTUAL_CORE_SHA" != "$EXPECT_CORE_SHA" ]]; then
    echo "  FAIL deterministic core: $(basename "$FILE")"
    echo "    expected: $EXPECT_CORE_SHA"
    echo "    actual:   $ACTUAL_CORE_SHA"
    FAIL=$((FAIL + 1))
    continue
  fi
  echo "  deterministic core: $ACTUAL_CORE_BYTES bytes, sha256 match ✓"

  # ─── Gate 2: Prose conformance ───
  BUNDLES="$ROOT/outputs/${ORG}_bundles_${DATE}.json"
  if [[ -f "$BUNDLES" ]]; then
    set +e
    PROSE_RESULT=$("$PY" -m pipeline.prose_conformance_check "$FILE" "$BUNDLES" 2>&1)
    PROSE_EXIT=$?
    set -e
    if [[ $PROSE_EXIT -ne 0 ]]; then
      echo "  FAIL prose conformance:"
      echo "$PROSE_RESULT" | tail -5 | sed 's/^/    /'
      FAIL=$((FAIL + 1))
      continue
    fi
    echo "  prose conformance: PASS ✓"
  else
    echo "  prose conformance: skipped (no bundles file)"
  fi

  # ─── Gate 3: Total bytes within range ───
  EXPECT_MIN=$(echo "$ROW" | "$PY" -c "import json,sys; r=json.load(sys.stdin); rng=r.get('ship_html_bytes_range', r.get('preview_html_bytes_range',[0,999999999])); print(rng[0])")
  EXPECT_MAX=$(echo "$ROW" | "$PY" -c "import json,sys; r=json.load(sys.stdin); rng=r.get('ship_html_bytes_range', r.get('preview_html_bytes_range',[0,999999999])); print(rng[1])")

  if [[ "$ACTUAL_BYTES" -lt "$EXPECT_MIN" || "$ACTUAL_BYTES" -gt "$EXPECT_MAX" ]]; then
    echo "  FAIL bytes range: $ACTUAL_BYTES not in [$EXPECT_MIN, $EXPECT_MAX]"
    FAIL=$((FAIL + 1))
    continue
  fi
  echo "  total bytes: $ACTUAL_BYTES (range [$EXPECT_MIN, $EXPECT_MAX]) ✓"

  PASS=$((PASS + 1))
done <<< "$ORGS"

echo ""
echo "══════════════════════════════════════════════════════════════"
if [[ "$FAIL" -eq 0 ]]; then
  if [[ "$MODE" == "update" ]]; then
    echo "  GOLDEN SET: printed $PASS row(s) — MANIFEST NOT WRITTEN"
    echo "  re-stamp with: ./tools/restamp_golden.py --note \"...\""
  else
    echo "  GOLDEN SET: PASS ($PASS/$((PASS + FAIL)))"
  fi
  exit 0
else
  echo "  GOLDEN SET: FAIL ($PASS passed, $FAIL failed)"
  exit 1
fi
