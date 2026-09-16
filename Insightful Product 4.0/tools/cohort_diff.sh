#!/usr/bin/env bash
# cohort_diff.sh — re-run the cohort and diff CLIENT-VISIBLE TEXT vs _baseline/.
#
# THE gate command. A template refactor that changes markup but no copy must
# print "no change"; a copy or number change must print a readable diff.
#
#   ./tools/cohort_diff.sh            summary table
#   ./tools/cohort_diff.sh --full     + full unified diff per changed org
#
# Exit 0 = cohort identical to baseline. Exit 1 = something moved (which is
# often correct — read the diff, then re-baseline deliberately).
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FULL=0
[[ "${1:-}" == "--full" ]] && FULL=1

[[ -d _baseline ]] || { echo "ERROR: no _baseline/. Run ./tools/cohort_run.sh _baseline" >&2; exit 2; }

rm -rf _current
./tools/cohort_run.sh _current > /tmp/cohort_current.log 2>&1 || true

printf '\n%-8s %-10s %-9s %-10s %s\n' ORG TEXT CORE-SHA OUTCOME NOTE
printf '%s\n' "----------------------------------------------------------------------"

CHANGED=0
while IFS=$'\t' read -r ORG DATE; do
  [[ -z "${ORG:-}" || "$ORG" == \#* ]] && continue
  B="_baseline/$ORG.txt"; C="_current/$ORG.txt"
  [[ -f "$B" && -f "$C" ]] || { printf '%-8s %-10s %-9s %-10s %s\n' "$ORG" "MISSING" "-" "-" "no baseline/current"; CHANGED=1; continue; }

  ADD=$(diff "$B" "$C" | grep -c '^>' || true)
  DEL=$(diff "$B" "$C" | grep -c '^<' || true)
  BSHA=$(awk -F'\t' -v o="$ORG" '$1==o{print $7}' _baseline/MANIFEST.tsv)
  CSHA=$(awk -F'\t' -v o="$ORG" '$1==o{print $7}' _current/MANIFEST.tsv)
  BOUT=$(awk -F'\t' -v o="$ORG" '$1==o{print $4}' _baseline/MANIFEST.tsv)
  COUT=$(awk -F'\t' -v o="$ORG" '$1==o{print $4}' _current/MANIFEST.tsv)

  if [[ "$ADD" == "0" && "$DEL" == "0" ]]; then TEXT="same"; else TEXT="+$ADD/-$DEL"; CHANGED=1; fi
  if [[ "$BSHA" == "$CSHA" ]]; then SHAS="same"; else SHAS="CHANGED"; CHANGED=1; fi
  NOTE=""; [[ "$BOUT" != "$COUT" ]] && { NOTE="outcome $BOUT → $COUT"; CHANGED=1; }

  printf '%-8s %-10s %-9s %-10s %s\n' "$ORG" "$TEXT" "$SHAS" "$COUT" "$NOTE"
  if [[ $FULL -eq 1 && "$TEXT" != "same" ]]; then
    printf '\n───── %s ─────\n' "$ORG"; diff -u "$B" "$C" | sed -n '3,200p'; printf '\n'
  fi
done < <(grep -E $'^[^#[:space:]]+\t' tools/cohort.conf)

printf '%s\n' "----------------------------------------------------------------------"
if [[ $CHANGED -eq 0 ]]; then echo "COHORT: no change vs baseline"; else
  echo "COHORT: CHANGED — read the diff (./tools/cohort_diff.sh --full), then re-baseline deliberately"; fi
exit $CHANGED
