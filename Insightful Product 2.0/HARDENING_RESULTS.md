# Insightful Product 2.0 — Hardening Run & Comparative Analysis

**Run date**: 2026-06-16 (v3 runs)
**Comparison baselines**: v1 (2026-06-15), v2 (2026-06-15_v2)
**Orgs tested**: UFI (Universal Furniture), CCI (Currey & Company), MLI (Maitland-Smith), WWJC (Wildwood Lamps)

---

## Run Summary

| Org | Mode | Report Size | Static Check | New Gates Fired | Key Issues |
|-----|------|-------------|-------------|-----------------|------------|
| **UFI** | Mode 1 | 119.6 KB | PASS | MIXPANEL=True (was False) | org_id corrected 79→18; Q-63/64/65 not in script |
| **CCI** | Mode 1 | 90.6 KB | PASS | MIXPANEL=True, HAS_NEW_ITEMS=True (369), HAS_BUYER_DATA=True (3,199) | Q-51–54 failed (conn pool); Q-63/64/65 not in script |
| **MLI** | Mode 1 | 113.6 KB | PASS | MIXPANEL=True (91 users), HAS_BUYER_DATA=True (181) | Q-66/67/68 failed (conn pool); VM45=False; org resolved as "Interlude Furniture" |
| **WWJC** | **Mode 2** | 47.0 KB | PASS | None (zero orders) | org_id=78 incorrect — should be 8; Mode 2 produced activation report |

### Gate Firing Matrix (v3 runs)

| Gate | CCI v1→v3 | UFI v1→v3 | MLI v3 | WWJC v3 |
|------|-----------|-----------|--------|---------|
| MIXPANEL_USER_DATA_PRESENT | **False→True** ✅ | **False→True** ✅ | True | N/A |
| HAS_NEW_ITEMS (new) | True (369) | False (0) | False (0) | N/A |
| HAS_BUYER_DATA (new) | True (3,199) | False (0) | True (181) | N/A |
| HAS_PORTAL_ORDERS | True | True | True | N/A |
| HAS_COMMITMENT_DATA | False | True | False | N/A |
| VM45_RENDER | True | True | **False** | N/A |
| SECTION_CONFIDENCE_2 | **PARTIAL→FULL** | **PARTIAL→STRONG** | FULL | N/A |

**Mixpanel bug fix confirmed**: `MIXPANEL_USER_DATA_PRESENT` now correctly fires `true` for CCI (76 users), UFI (103 users), and MLI (91 users). In v1, all three were incorrectly `false`.

---

## Per-Subsection Evaluation

### Q-58b — Uncommitted Market Items In Stock (§5.9 enhancement)

| Question | Answer |
|----------|--------|
| **Did it fire?** | Partially. UFI has the gate (HAS_COMMITMENT_DATA + HAS_INVENTORY), and cache file exists, but 0 rows returned. CCI/MLI lack commitment data. |
| **Holy shit quality?** | Cannot evaluate — no data rendered. The concept is excellent (committed items sitting in warehouse = zero-friction revenue). |
| **Integrates well?** | Designed as Part B of subsection 9 (Market Commitments). Natural fit. |
| **Additive or replacing?** | ENHANCE — adds actionable in-stock detail below existing commitment conversion table. |
| **Loses anything from v1?** | No — this is purely additive. |

**Recommendation**: **Keep as-is** (ship when data exists). Needs a test org with actual uncommitted-in-stock items.

---

### Q-60 — Price Erosion / Trade-Down Detection (§5.10)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ Yes — CCI (20 rows), UFI (20 rows). Both rendered in §5 fragment. |
| **Holy shit quality?** | **Yes (UFI)**: Wayfair at $2.4M current quarter with -6.4% avg price decline. City Furniture -33.3%. A VP of Sales would immediately want to investigate. CCI data has duplicate rows (see below) reducing impact. |
| **Integrates well?** | Yes — fits naturally after Capture Rate and before the confidence footer. Badge styling (`.badge.danger`) creates visual urgency. |
| **Additive or replacing?** | **Stand alone** — new subsection with no v1 equivalent. |
| **Loses anything from v1?** | No. |

**Data quality issue (CCI)**: Elmington Capital appears 5 times with different `prior_avg_price` values ($2,810, $2,173, $5,226, $2,755, $3,289) but identical `current_avg_price` ($1,916). Same for Bending the Rules (4 rows) and Kasamia Interiors (3 rows). The query is comparing each prior-quarter average against current quarter individually rather than aggregating. Fix the SQL to use a single prior-period avg per account.

**Recommendation**: **Ship it** after fixing the duplicate-row issue in Q-60's SQL. The UFI output is publication-ready. The CCI output needs the query deduplication fix.

---

### Q-61 — New Introduction Adoption Gap (§4.6)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ CCI only (369 new items). UFI and MLI both have HAS_NEW_ITEMS=False. |
| **Holy shit quality?** | **Yes**: 369 new items, only 30 with any orders (8% adoption). 339 items at zero traction. Magnum Opus Chandelier leads at $80K from 22 buyers. Immediately actionable. |
| **Integrates well?** | Excellent. Placed after "What's Selling" in §4. Callout + table + zero-traction details section. |
| **Additive or replacing?** | **Complements** Q-42 (New Introduction Performance count). Q-42 gives the "how many," Q-61 gives the "which ones and how are they doing." |
| **Loses anything from v1?** | No — purely additive. |

**Recommendation**: **Ship it**. One of the strongest new insights. The 8% adoption rate with specific item-level data is exactly what product leadership wants to see.

---

### Q-62 — Product Launch Velocity by Rep (§2.7)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ CCI only (20 rows, same HAS_NEW_ITEMS gate). |
| **Holy shit quality?** | **Good, not holy shit**: Shows Vivi Mira-Culmer at 43.9% adoption (162 of 369 items) vs bottom quartile at ~12%. Coaching value is clear. "HOUSE ACCOUNT" at 54.5% adoption needs exclusion — it's not a person. |
| **Integrates well?** | Fits in §2 after Coaching Opportunities. Listed in section_contents header. |
| **Additive or replacing?** | **Stand alone** — new subsection. Consider making **collapsible** to avoid §2 information overload. |
| **Loses anything from v1?** | No. |

**Data quality issue**: "HOUSE ACCOUNT" appears as a rep at rank 6 with 54.5% adoption. Should be excluded from rep-level analysis (same treatment as showroom accounts).

**Recommendation**: **Ship as collapsible**. Good data but secondary to archetypes and coaching. Exclude HOUSE ACCOUNT from Q-62 results or add to showroom exclusion logic.

---

### Q-63 — Presentation-to-Order Conversion (§2.8, BigQuery)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ❌ **Not executed** — query exists in library but `data_gather.py` does not run it. No cache file for any org. |
| **Holy shit quality?** | Unknown — no output to evaluate. |
| **Assessment** | The Mixpanel gate is now True (bug fixed), so the gate condition is met. But the script doesn't execute Q-63. |

**Recommendation**: **Wire into data_gather.py** before next evaluation. This is one of the most promising behavioral queries.

---

### Q-64 — Rep Engagement vs Account Revenue (§2.9, BigQuery)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ❌ **Not executed** — same pipeline gap as Q-63. |

**Recommendation**: **Wire into data_gather.py**.

---

### Q-65 — Selling vs Admin Time (§2.10, BigQuery)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ❌ **Not executed** — same pipeline gap as Q-63/64. |

**Recommendation**: **Wire into data_gather.py**.

---

### Q-66 — Buyer-Within-Account Intelligence (§3.9)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ CCI (20 rows). MLI gate met (HAS_BUYER_DATA=True, 181 buyers) but **query failed** (connection pool exhaustion). UFI gate false (HAS_BUYER_DATA=False). |
| **Holy shit quality?** | **Yes**: The Treasure Chest has a new buyer who placed $175,944 in the last 90 days. Alerie Garrett: $112K from a brand-new buyer. This is expansion detection — decision-maker turnover or new procurement contacts — that nobody was tracking. |
| **Integrates well?** | Good. Placed after New Buyer Acquisition in §3. Callout opens with "X of your accounts have new buyer names." |
| **Additive or replacing?** | **Stand alone** — completes the customer intelligence picture. New buyer acquisition (Q-13) tracks account-level activation; Q-66 tracks buyer-within-account expansion. |
| **Loses anything from v1?** | No. |

**Recommendation**: **Ship it**. Fix the connection pool issue so it fires for MLI too.

---

### Q-67 — Geographic Revenue Trends (§3.10)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ CCI (25 rows). UFI cache file exists. MLI **failed** (connection pool). |
| **Holy shit quality?** | **Absolutely yes**: Virginia +102% QoQ ($361K→$730K), North Carolina +69.6%, Tennessee +66.3%. Utah **declining -35.6%**. California flat at -5.1%. A VP of Sales would immediately reassign territory attention based on this. |
| **Integrates well?** | Separate from the static geographic distribution map (§3 subsection 5). This adds QoQ trend analysis — movement, not just position. |
| **Additive or replacing?** | **Complements** existing geographic distribution. The static map shows "where" — Q-67 shows "what's changing." Consider placing AFTER the existing geo subsection. |
| **Loses anything from v1?** | No — enhances significantly. |

**Recommendation**: **Ship it**. One of the strongest new insights in the entire batch. The combination of growing states (territory opportunity) and declining states (competitive threat) is immediately actionable.

---

### Q-68 — Wallet Share Estimation (§3.11)

| Question | Answer |
|----------|--------|
| **Did it fire?** | ✅ CCI (20 rows). UFI cache file exists. MLI **failed** (connection pool). |
| **Holy shit quality?** | **No — needs adjustment**: All 20 CCI accounts show identical `peer_avg_spend` ($29,506.30) and similar `wallet_share_pct` (~35%). The peer grouping is too coarse — all accounts land in `spend_tier=5` with the same benchmark. Output is repetitive and not actionable in its current form. |
| **Integrates well?** | Concept fits well in §3 after Geographic Trends. |
| **Additive or replacing?** | Could **enhance** or partially **replace** Q-57 (Cross-Sell Whitespace), which also measures gap-to-potential. But Q-57 does it by category while Q-68 does it by account. Both are valuable if Q-68's tiering is fixed. |
| **Loses anything from v1?** | No. |

**Recommendation**: **Needs adjustment**. Refine the `spend_tier` bucketing to produce more granular peer groups (e.g., by state+tier, or by category affinity). Current uniform output would not impress a client.

---

## Specific Comparison Points

### §2 Sales Team: Do Q-62/63/64/65 ADD to the archetype story or create overload?

**Assessment**: The behavioral subsections (Scorecard, Archetypes, Coaching Opportunities) that now render thanks to the Mixpanel fix are **transformative**. UFI's §2 went from a bare leaderboard + trajectory (8KB) to a rich behavioral analysis with archetypes like "Customer-First Closer" and "Catalog Explorer" (17KB). This is the single biggest quality improvement in v3.

Q-62 (launch velocity by rep) adds useful coaching context but is **secondary** to archetypes — should be collapsible. Q-63/64/65 couldn't be evaluated (not in pipeline), but their concepts (presentation conversion, engagement vs revenue, selling vs admin time) would complete the behavioral story. Risk of overload is real if all 4 fire — recommend Q-63 and Q-65 as standalone, Q-64 as collapsible.

### §3 Customers: Do Q-66/67/68 complete the picture or overwhelm?

**Assessment**: Q-67 (geographic trends) is the clear winner — it completes the picture by adding temporal dynamics to the static geographic distribution. Q-66 (buyer intelligence) adds a unique signal nobody else provides. Q-68 (wallet share) in its current form is too uniform to add value.

Recommendation: Q-67 standalone, Q-66 standalone, Q-68 collapsible (after fix). No overwhelm risk — these are genuinely different lenses on the customer base.

**Q-57 vs Q-68**: Q-57 (Cross-Sell Whitespace by category) is more actionable than Q-68 in its current form because it tells you *what categories* to push. Q-68 tells you *which accounts* are under-spending but doesn't say on what. Both should ship, but Q-57 has proven value while Q-68 needs refinement.

### §4 Product: Does Q-61 compete with Q-42?

**Assessment**: Q-61 (adoption gap) **complements** Q-42 (new intro performance) perfectly. Q-42 gives the count and aggregate revenue. Q-61 gives per-item detail with buyer counts, revenue, and zero-traction identification. Together they tell a complete new-product story. No competition, no redundancy.

### §5 Commerce: Does Q-60 feel urgent or alarmist?

**Assessment**: Q-60 (price erosion) strikes the right tone when rendered correctly. CCI's fragment uses `.callout.insight` with "Price erosion can signal competitive pressure, changing buyer mix, or shifting product interest" — appropriate hedging. The `.badge.danger` styling on percentage declines creates visual urgency without being alarmist. The "what this tells you" prose frames it as investigative, not accusatory.

One risk: if a client sees -55% (Designer Furniture Galleries) they might panic. The context callout adequately addresses this, but worth monitoring client reactions.

---

## Fragment Size Comparison

| Section | CCI v1 | CCI v2 | CCI v3 | Δ v1→v3 | UFI v1 | UFI v3 | Δ v1→v3 | MLI v3 |
|---------|--------|--------|--------|---------|--------|--------|---------|--------|
| §2 | 8,519 | 16,430 | 12,800 | +50% | 8,018 | 17,269 | **+115%** | 19,957 |
| §3 | 16,280 | 20,450 | 16,082 | -1% | 18,337 | 20,369 | +11% | 20,178 |
| §4 | 12,990 | 24,685 | 10,516 | -19% | 2,220 | 14,643 | **+560%** | 11,955 |
| §5 | 16,597 | 13,764 | 9,857 | -41% | 12,850 | 15,299 | +19% | 16,192 |
| §6 | — | — | — | — | 4,099 | 3,842 | -6% | — |
| §7 | 8,127 | — | — | — | 5,964 | — | — | — |
| §8 | 13,363 | 18,593 | 8,336 | -38% | 21,352 | 15,017 | -30% | 10,484 |
| **Total** | **75,876** | **93,922** | **57,591** | **-24%** | **72,840** | **86,439** | **+19%** | **78,766** |

**CCI v3 shrank vs v1** — this is a regression driven by Q-51/52/53/54 connection pool failures (these rendered in v1/v2). The new queries (Q-60, Q-61, Q-62, Q-66, Q-67, Q-68) didn't fully compensate for the lost ERP enrichment subsections.

**UFI v3 grew significantly (+19%)** — the Mixpanel fix added behavioral scorecard, archetypes, and coaching to §2 (+115%). §4 exploded from 2.2KB to 14.6KB (+560%) with fill rate, category/collection analysis, and OOS data that was apparently missing in v1.

---

## Top 5 "Holy Shit" Moments

1. **UFI Behavioral Scorecard & Archetypes (§2)**: For the first time, we see that 15 power users average 8,750 events each, Neil Phillips has 1,081 order submissions, and Mason OConnor has 9,035 product discovery events but only 4 orders. The archetype classification (Customer-First Closer, Volume Seller, Catalog Explorer, Digital Presenter, Library Researcher) is immediately actionable for a VP of Sales. This was INVISIBLE in v1 due to the Mixpanel bug.

2. **CCI Geographic Revenue Trends (Q-67)**: Virginia grew **102% QoQ** ($361K→$730K), North Carolina +69.6%, Tennessee +66.3%. Utah **declining -35.6%**. This is territory allocation intelligence that drives real strategic decisions.

3. **UFI Price Erosion (Q-60)**: Wayfair at $2.4M current quarter with -6.4% avg price decline. City Furniture dropping -33.3%. This immediately flags competitive pressure at the biggest accounts and creates urgency for rep follow-up.

4. **CCI New Introduction Adoption (Q-61)**: 369 new items, only 30 with ANY orders (8% adoption rate). 339 items at zero traction. Magnum Opus Chandelier leads at $80K. This is the "new product launch" accountability metric that product teams have been asking for.

5. **CCI Buyer-Within-Account Intelligence (Q-66)**: The Treasure Chest account has a new buyer who placed $175,944 in the last 90 days. This is expansion detection — new decision-makers or new procurement contacts — that nobody was tracking before.

---

## Top 5 Regressions from v1

1. **Q-51/52/53/54 (ERP Enrichment) failed in CCI v3** due to Postgres connection pool exhaustion. The v2 subsection showing Wayfair at $4.7M total with 0% eCat penetration was one of the most powerful insights in any report — it's gone in v3. **Must fix the connection pool issue.**

2. **Q-63/64/65 (BigQuery behavioral queries) not wired into `data_gather.py`** — The Mixpanel bug fix unlocked these gates, but the queries themselves aren't executed by the script. These would add Presentation-to-Order Conversion, Rep Engagement vs Revenue, and Selling vs Admin Time — three of the most anticipated new subsections that are completely absent from all v3 reports.

3. **CCI v3 total fragment size decreased 24%** (75,876→57,591) — Despite adding new subsections, the CCI report is actually smaller than v1 because the lost Q-51–54 subsections and connection pool failures weren't offset by new content. The report feels thinner.

4. **Q-60 duplicate-row issue** — CCI's price erosion data has Elmington Capital appearing 5 times with different prior_avg_price values. The SQL compares against multiple prior-quarter windows individually rather than aggregating to a single prior-period average per account. The duplicates dilute the impact and waste table real estate.

5. **WWJC ran as Mode 2** — org_id=78 (specified) vs org_id=8 (correct). The test produced a valid activation report but was wasted as a hardening test case for the new queries. All commerce/behavioral gates were False.

---

## Recommendations Summary

### Ship as-is
| Query | Section | Rationale |
|-------|---------|-----------|
| Q-61 | §4.6 New Introduction Adoption Gap | Strong data, clean rendering, complements Q-42 |
| Q-67 | §3.10 Geographic Revenue Trends | Best new insight in the batch — actionable geographic intelligence |
| Q-66 | §3.9 Buyer-Within-Account Intelligence | Unique signal, clean rendering when it fires |

### Needs adjustment
| Query | Section | What to fix |
|-------|---------|-------------|
| Q-60 | §5.10 Price Erosion | Fix SQL to deduplicate accounts (aggregate prior-period avg per customer) |
| Q-68 | §3.11 Wallet Share | Refine spend_tier bucketing for more granular peer groups |
| Q-62 | §2.7 Launch Velocity by Rep | Exclude HOUSE ACCOUNT from rep analysis |

### Should be collapsible
| Query | Section | Rationale |
|-------|---------|-----------|
| Q-62 | §2.7 Launch Velocity by Rep | Good data but secondary to archetypes; §2 overload risk |
| Q-58b | §5.9 Part B | Supplementary to market commitment table |

### Missing / not executable
| Query | Section | Blocker |
|-------|---------|---------|
| Q-63 | §2.8 Presentation-to-Order | Not wired into `data_gather.py` |
| Q-64 | §2.9 Rep Engagement vs Revenue | Not wired into `data_gather.py` |
| Q-65 | §2.10 Selling vs Admin Time | Not wired into `data_gather.py` |

### Infrastructure fixes required
| Issue | Impact | Priority |
|-------|--------|----------|
| **Postgres connection pool exhaustion** | Q-51–54 failed (CCI), Q-66–68 failed (MLI). Loses proven-value subsections. | **P0** — blocks shipping |
| **Q-63/64/65 not in data_gather.py** | Three BigQuery behavioral queries completely absent | **P0** — blocks evaluation |
| **org_id lookup needs validation** | WWJC used wrong org_id; UFI subagent had to self-correct | **P1** — add shortname→org_id verification in script |
| **Q-60 SQL deduplication** | Duplicate customer rows in price erosion output | **P1** — fix before CCI delivery |

---

## Gaps Discovered

1. **No org with Q-58b data**: None of the 4 orgs produced non-empty Q-58b results. Need to test against an org with both commitment data AND inventory that includes uncommitted items (try HFG or another commitment-data org).

2. **HAS_NEW_ITEMS gate too restrictive?**: Only CCI (369 items) fired this gate. UFI and MLI both had 0 new items flagged. The gate depends on `new_item=true` in the products table — check whether client data imports actually set this flag. If most clients don't set `new_item`, Q-61 and Q-62 will rarely fire.

3. **HAS_BUYER_DATA gate depends on portal_order_items**: UFI had 0 distinct buyers despite having $137M in portal_orders. This suggests `portal_order_items.buyer_name` is not populated for UFI. The gate definition may need broadening or the field dependency should be documented.

4. **Section §7 (Peer Benchmarking) disabled in all v3 runs**: The manifest shows "Disabled" for §7 across all orgs. Was this intentional? The v1 runs had §7 rendering (CCI: 8,127 bytes, UFI: 5,964 bytes). This is a significant content loss if unintentional.

5. **MLI org identity mismatch**: org_id=107 resolves to "Interlude Furniture," not "Maitland-Smith / Theodore Alexander." The report was built for the correct database org but the client name in the original request was wrong. Need to verify the intended org.
