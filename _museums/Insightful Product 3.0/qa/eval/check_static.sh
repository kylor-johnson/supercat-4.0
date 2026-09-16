#!/usr/bin/env bash
# Static eval — forbidden-phrase + structural-integrity checks on an output HTML.
# No MCP / no network. Safe to run anytime.
#
# Usage:  ./check_static.sh <output.html> [expected_section_count] [gate_flags_path]
# Exit:   0 = PASS, 1 = FAIL, 2 = usage/file error
#
# This is the cheap half of the golden-set eval. Run it after ANY change to the
# HTML template, section guides, shared_rules, or stage4 assembly. For changes
# that touch gates/queries/blueprint/catalog, run the FULL eval (see run_eval.md),
# which re-runs Stage 1 and then calls this script on the produced output.
#
# SOURCE OF TRUTH for the token lists below: operators/external/guides/shared_rules.md §C
# (Forbidden Phrases). If you change that list, update HARD/REVIEW here to match.
# See also: GUARDRAILS.md §4 (canonical forbidden phrase list).

set -uo pipefail

html="${1:-}"
expect_sections="${2:-}"
gate_flags="${3:-}"

[ -z "$html" ] && { echo "usage: check_static.sh <output.html> [expected_section_count] [gate_flags_path]"; exit 2; }
[ -f "$html" ] || { echo "FILE NOT FOUND: $html"; exit 2; }

fail=0
pass(){ printf "  PASS  %s\n" "$1"; }
bad(){  printf "  FAIL  %s\n" "$1"; fail=1; }
warn(){ printf "  WARN  %s\n" "$1"; }
count(){ grep -iEo "$1" "$html" 2>/dev/null | wc -l | tr -d ' '; }

echo "Static eval: $html"

# 1. Hard-forbidden tokens — must never appear in delivered external HTML.
HARD='\[HYPOTHETICAL\]|\[ESTIMATED\]|health score|Mixpanel|Clicky|bounce_rate|order_source|benchmark_confidence|peer_group_level|peer_group_n|Platform-Embedded|Commerce-Active|Catalog-Focused|<!--'
hn=$(count "$HARD")
if [ "${hn:-0}" -eq 0 ]; then
  pass "no hard-forbidden tokens"
else
  bad "hard-forbidden tokens present ($hn occurrences):"
  grep -iEo "$HARD" "$html" | sort | uniq -c | sort -rn | sed 's/^/        /'
fi

# 2. Review tokens — report only (legit hedging like "estimated"/"your ERP" is allowed;
#    a literal tag or buyer-activity "ERP" framing is not). Human/agent confirms.
REVIEW='\bERP\b|\bestimated\b|\bhypothetical\b'
rn=$(count "$REVIEW")
if [ "${rn:-0}" -eq 0 ]; then pass "no review tokens"; else warn "review tokens present ($rn) — confirm hedging usage, not tags/labels"; fi

# 3. Unsubstituted template tokens — must be 0.
tn=$(grep -Eo '\{\{' "$html" 2>/dev/null | wc -l | tr -d ' ')
if [ "${tn:-0}" -eq 0 ]; then pass "no unsubstituted {{ tokens"; else bad "$tn unsubstituted {{ tokens"; fi

# 4. Collapsible section blocks.
sc=$(grep -Eo '<details class="section-collapse"' "$html" 2>/dev/null | wc -l | tr -d ' ')
echo "  INFO  section-collapse blocks: $sc"
if [ -n "$expect_sections" ]; then
  if [ "$sc" -eq "$expect_sections" ]; then pass "section count == expected ($expect_sections)"; else bad "section count $sc != expected $expect_sections"; fi
fi

# 5. <details> tag balance (broken HTML guard).
open=$(grep -Eo '<details' "$html" 2>/dev/null | wc -l | tr -d ' ')
close=$(grep -Eo '</details>' "$html" 2>/dev/null | wc -l | tr -d ' ')
if [ "$open" -eq "$close" ]; then pass "<details> balanced ($open/$close)"; else bad "<details> unbalanced: $open open / $close close"; fi

# 6. What-this-means count vs subsection count validation.
wtm=$(grep -co 'what-this-means' "$html" 2>/dev/null | tr -d ' ')
sub=$(grep -co 'class="subsection"' "$html" 2>/dev/null | tr -d ' ')
wtm=${wtm:-0}
sub=${sub:-0}
if [ "$sub" -gt 0 ]; then
  if [ "$wtm" -ge "$sub" ] || [ $((sub - wtm)) -le 2 ]; then
    pass "what-this-means count ($wtm) vs subsection count ($sub) — within tolerance"
  else
    bad "what-this-means count ($wtm) far below subsection count ($sub) — missing close blocks"
  fi
else
  echo "  INFO  no subsection divs detected (subsection count: $sub)"
fi

# 7. Conditional subsection completeness (requires gate_flags_path).
if [ -n "$gate_flags" ] && [ -f "$gate_flags" ]; then
  echo "  INFO  gate-aware checks enabled (gate_flags: $gate_flags)"

  _gate_val() {
    grep -E "^\| $1 " "$gate_flags" 2>/dev/null | head -1 | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/,"",$3); print $3}'
  }

  # 7a. Q-52 penetration subsection: if PORTAL_CUSTOMER_DATA_PRESENT=True and
  #     section_collapse for customers exists, check for penetration indicators.
  pcust=$(_gate_val "PORTAL_CUSTOMER_DATA_PRESENT")
  if [ "$pcust" = "True" ]; then
    has_customers=$(grep -c 'id="customers"' "$html" 2>/dev/null || echo 0)
    if [ "$has_customers" -gt 0 ]; then
      has_penetration=$(grep -ci 'penetration' "$html" 2>/dev/null || echo 0)
      if [ "${has_penetration:-0}" -gt 0 ]; then
        pass "Q-52 penetration content present (PORTAL_CUSTOMER_DATA_PRESENT=True)"
      else
        bad "Q-52 penetration content MISSING — PORTAL_CUSTOMER_DATA_PRESENT=True but no penetration text in §3"
      fi
    fi
  fi

  # 7b. Admin disclosure: if ADMIN_REPS_IN_LEADERBOARD=True and sales section
  #     exists, check for admin disclosure text.
  admin_lb=$(_gate_val "ADMIN_REPS_IN_LEADERBOARD")
  if [ "$admin_lb" = "True" ]; then
    has_sales=$(grep -c 'id="sales"' "$html" 2>/dev/null || echo 0)
    if [ "$has_sales" -gt 0 ]; then
      has_disclosure=$(grep -ci 'internal or administrative roles' "$html" 2>/dev/null || echo 0)
      if [ "${has_disclosure:-0}" -gt 0 ]; then
        pass "admin disclosure present (ADMIN_REPS_IN_LEADERBOARD=True)"
      else
        bad "admin disclosure MISSING — ADMIN_REPS_IN_LEADERBOARD=True but no disclosure text in §2"
      fi
    fi
  fi
else
  echo "  INFO  gate-aware checks skipped (no gate_flags_path provided)"
fi

echo
if [ "$fail" -eq 0 ]; then echo "RESULT: PASS"; exit 0; else echo "RESULT: FAIL"; exit 1; fi
