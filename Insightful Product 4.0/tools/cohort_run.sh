#!/usr/bin/env bash
# cohort_run.sh <outdir> — run the pinned verification cohort, capture what
# a client would READ (visible text) plus the deterministic-core checksum.
#
# Fully offline: every org is run with a pinned --date against on-disk cache.
# An org whose cache dir is missing is SKIPPED loudly, never silently, and
# never allowed to fall through to populate_cache (which needs VPN + Postgres).
#
# Writes: <outdir>/<org>.txt  and  <outdir>/MANIFEST.tsv
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv-renderer/bin/python"
CONF="$ROOT/tools/cohort.conf"
OUTDIR="${1:-_current}"

[[ -x "$PY" ]] || { echo "ERROR: venv missing at $PY" >&2; exit 2; }
[[ -f "$CONF" ]] || { echo "ERROR: $CONF missing" >&2; exit 2; }

mkdir -p "$OUTDIR"
MANIFEST="$OUTDIR/MANIFEST.tsv"
printf 'org\tdate\texit\toutcome\toutfile\tbytes\tcore_sha\ttext_lines\n' > "$MANIFEST"

printf '%-8s %-12s %-5s %-12s %-9s %s\n' ORG DATE EXIT OUTCOME LINES FILE
printf '%s\n' "------------------------------------------------------------------------"

RUN=0; SKIP=0; BAD=0
while IFS=$'\t' read -r ORG DATE; do
  [[ -z "${ORG:-}" || "$ORG" == \#* ]] && continue

  if [[ ! -d "pipeline/cache/$ORG/$DATE" ]]; then
    printf '%-8s %-12s %-5s %-12s %-9s %s\n' "$ORG" "$DATE" "-" "NO-CACHE" "-" "(skipped)"
    printf '%s\t%s\t\tNO-CACHE\t\t\t\t\n' "$ORG" "$DATE" >> "$MANIFEST"
    SKIP=$((SKIP+1)); continue
  fi

  LOG="$(./run.sh "$ORG" --date "$DATE" 2>&1)"; CODE=$?

  # Outcome + artifact. run.sh prints "rendered X → /abs/path.html (N bytes)".
  OUT="$(printf '%s\n' "$LOG" | sed -n 's/^rendered .* → \(.*\) ([0-9,]* bytes)$/\1/p' | tail -1)"
  if [[ -z "$OUT" ]]; then
    for CAND in "outputs/${ORG}_GATESTOP_${DATE}.md" "outputs/${ORG}_DRAFT_${DATE}.md"; do
      [[ -f "$CAND" ]] && { OUT="$ROOT/$CAND"; break; }
    done
  fi
  OUTCOME="$(printf '%s\n' "$LOG" | grep -oE '^\│ *(SHIP|ACTIVATION|PREVIEW|REDIRECT|GATE-STOP)' | tr -d '│ ' | tail -1)"
  [[ -z "$OUTCOME" ]] && OUTCOME="$(printf '%s\n' "$LOG" | grep -oE '\b(SHIP|ACTIVATION|PREVIEW|REDIRECT|GATE-STOP)\b' | tail -1)"
  [[ -z "$OUTCOME" ]] && OUTCOME="exit${CODE}"

  if [[ -n "$OUT" && -f "$OUT" ]]; then
    "$PY" tools/html_to_text.py "$OUT" > "$OUTDIR/$ORG.txt" 2>/dev/null
    SHA="$("$PY" -m pipeline.extract_deterministic_core "$OUT" 2>/dev/null | shasum -a 256 | awk '{print $1}')"
    BYTES="$(wc -c < "$OUT" | tr -d ' ')"
    LINES="$(wc -l < "$OUTDIR/$ORG.txt" | tr -d ' ')"
    BASE="$(basename "$OUT")"
  else
    : > "$OUTDIR/$ORG.txt"; SHA="-"; BYTES=0; LINES=0; BASE="(no artifact)"
    BAD=$((BAD+1))
  fi

  printf '%-8s %-12s %-5s %-12s %-9s %s\n' "$ORG" "$DATE" "$CODE" "$OUTCOME" "$LINES" "$BASE"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$ORG" "$DATE" "$CODE" "$OUTCOME" "$BASE" "$BYTES" "$SHA" "$LINES" >> "$MANIFEST"
  RUN=$((RUN+1))
done < <(grep -P '^\S+\t\S+' "$CONF" 2>/dev/null || grep -E $'^[^#[:space:]]+\t' "$CONF")

printf '%s\n' "------------------------------------------------------------------------"
echo "ran=$RUN  skipped=$SKIP  no-artifact=$BAD  →  $OUTDIR/"
