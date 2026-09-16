# Client Review Implementation Log

**Date**: 2026-06-16
**Source**: `Customer Intelligence/runs/02_client_perspective_review_output.md`
**Scope**: 26 changes across 4 phases, implemented in 12 file-batched steps

---

## Per-Change Status

### Phase 1: Cut the Fat (C.1–C.7)

| ID | Change | Status | File(s) Modified |
|----|--------|--------|------------------|
| C.1 | Replace Data Pipeline Health monthly table with pass/fail | **Completed** | `section_08_platform.md` (subsumed by F.4 health-check card) |
| C.2 | Replace Smart Stack names/dates table with engagement framing | **Completed** | `section_08_platform.md` (subsumed by F.4 health-check card) |
| C.3 | Rename §6 from Portal Engagement to Demand Signal Intelligence | **Completed** | `section_06_portal.md`, `html_report_template.html`, `stage4_assembly.md`, `shared_rules.md`, all DOES NOT COVER refs |
| C.4 | Add spread gate to Selling vs Admin Time (>20pp spread required) | **Completed** | `section_02_sales_team.md` |
| C.5 | Rewrite Order Type subsection — lead with quote premium, table in `<details>` | **Completed** | `section_05_commerce.md` |
| C.6 | Collapse New eCat Buyer Acquisition from monthly table to single stat | **Completed** | `section_03_customers.md` |
| C.7 | Rewrite Wallet Share methodology — historical peak comparison replaces peer avg | **Completed** | `section_03_customers.md`, `authority/query_library.md` (Q-68 SQL rewritten) |

### Phase 2: Eliminate Redundancy (E.1–E.5)

| ID | Change | Status | File(s) Modified |
|----|--------|--------|------------------|
| E.1 | Add anti-repetition rule to Section G (highlights) | **Completed** | `shared_rules.md` |
| E.2 | Add anti-restatement rule to WHAT-THIS-MEANS quality bar | **Completed** | `section_02_sales_team.md` |
| E.3 | Merge Total Business Context + Capture Rate into Channel Mix & Capture Rate | **Completed** | `section_05_commerce.md` (subsections 6+7 → 6, renumbered 8–10 → 7–9) |
| E.4 | Merge Selling Archetypes into Coaching Opportunities (archetype = badge) | **Completed** | `section_02_sales_team.md` (subsections 3+4 → 3, renumbered 5–10 → 4–9) |
| E.5 | Add §8 ownership note for catalog completeness; §4 cross-reference | **Completed** | `section_08_platform.md`, `section_04_product.md` |

### Phase 3: Reframe (F.1–F.7)

| ID | Change | Status | File(s) Modified |
|----|--------|--------|------------------|
| F.1 | Dollar-first rule for executive summary highlights | **Completed** | `stage4_assembly.md` |
| F.2 | PARTIAL-tier "what you'd see" teaser template | **Completed** | `shared_rules.md` (new §J.4b) |
| F.3 | §6 reframe to engagement-first demand signals | **Completed** | `section_06_portal.md` (combined with C.3) |
| F.4 | §8 collapse to single health-check card with traffic lights | **Completed** | `section_08_platform.md` (6 subsections → 1 card with `<details>` fallback) |
| F.5 | Team-level coaching rollup ("Combined coaching upside: $X across N reps") | **Completed** | `section_02_sales_team.md` (inside merged §2.3) |
| F.6 | Peer section competitive framing with stakes | **Completed** | `section_07_peer.md` |
| F.7 | "Patterns that warrant a conversation" block in executive summary | **Completed** | `stage4_assembly.md` |

### Phase 4: Missing Killer Insights (D.1–D.7)

| ID | Change | Status | File(s) Modified |
|----|--------|--------|------------------|
| D.1 | "Biggest customers don't use eCat" framing (Q-53) | **Completed** | `section_03_customers.md` (§3.4 framing enhancement) |
| D.2 | Rep-level capture rate competitive dynamic (Q-51) | **Completed** | `section_02_sales_team.md` (§2.1b framing enhancement) |
| D.3 | Products browsed but never ordered (Mixpanel) | **Deferred** | Needs Mixpanel introspection to verify product-level event payloads contain item identifiers. `product_search` events exist but SKU-level attribution unconfirmed. |
| D.4 | Customer-level + geographic eCat penetration framing (Q-52/Q-54) | **Completed** | `section_03_customers.md` (§3.2 + §3.5 framing enhancement, "Go win [State]" narrative) |
| D.5 | Revenue lost to order timing (day-of-week/hour) | **Completed** | `authority/query_library.md` (new Q-69), `section_05_commerce.md` (new §5.10 subsection) |
| D.6 | Seasonal demand forecasting | **Deferred to Phase 5** | Needs multi-year data validation across enough orgs. Complex query + uncertain data availability. |
| D.7 | Reps who don't log in (with territory revenue) | **Completed** | `authority/query_library.md` (new Q-70), `section_02_sales_team.md` (new §2.10 subsection) |

---

## Files Modified

| File | Changes Applied | One-Line Summary |
|------|----------------|------------------|
| `shared_rules.md` | E.1, F.2, cascade (§2.3 coaching ref, §6 rename in hard rules) | Anti-repetition rule, PARTIAL-tier teaser template, coaching exception update |
| `stage4_assembly.md` | F.1, F.7, cascade (§6 rename in pre-flight) | Dollar-first highlights, conversation-starter block, TOC title update |
| `section_08_platform.md` | C.1, C.2, F.4, E.5 | Collapsed 6 subsections into health-check card with traffic lights |
| `section_06_portal.md` | C.3, F.3 | Renamed to Demand Signal Intelligence, engagement-first framing |
| `section_05_commerce.md` | C.5, E.3, D.5 | Quote premium lead, merged Channel Mix & Capture Rate, new order timing subsection |
| `section_02_sales_team.md` | C.4, E.2, E.4, F.5, D.2, D.7 | Spread gate, anti-restatement, merged coaching+archetypes, team rollup, capture framing, inactive reps |
| `section_03_customers.md` | C.6, C.7, D.1, D.4 | Collapsed new buyer table, historical peak methodology, activation framing, geographic narrative |
| `section_04_product.md` | E.5 | §8 cross-reference, sales-impact framing for catalog completeness |
| `section_07_peer.md` | F.6 | Competitive framing with stakes, fixable-gap narrative |
| `authority/html_report_template.html` | cascade | §6 title, section-contents, gating flag comments updated |
| `authority/query_library.md` | C.7, D.5, D.7 | Q-68 rewritten (historical peak), Q-69 new (order timing), Q-70 new (inactive reps) |

---

## New Queries Added

| Query | VM | Purpose | Section Owner | Status |
|-------|-----|---------|---------------|--------|
| Q-69 | VM-69 | Order timing distribution (day-of-week, hour) | §5 Commerce (subsection 10) | Defined — needs `data_gather.py` integration |
| Q-70 | VM-70 | Inactive reps with territory revenue (90d+ no login) | §2 Sales Team (subsection 10) | Defined — needs `data_gather.py` integration + per-org name-match validation |

## Modified Queries

| Query | Change | Reason |
|-------|--------|--------|
| Q-68 | Rewritten from peer-group-average to historical-peak comparison | Client review found peer averages clustered ($10,400–$10,530) creating data artifacts. Historical peak comparison uses account's own demonstrated spending capacity. |

---

## Subsection Merges / Renumbering

### §2 Sales Team Performance
- **Merge**: §2.3 (Selling Archetypes) + §2.4 (Coaching Opportunities) → §2.3 (Coaching Opportunities & Selling Archetypes)
- **Renumber**: 5→4, 6→5, 7→6, 8→7, 9→8, 10→9
- **New**: §2.10 (Inactive Reps with Territory Revenue, Q-70)
- **Result**: 1, 1b, 2, 3, 4, 5, 6, 7, 8, 9, 10 (10 distinct slots, was 11)

### §5 Commerce Analytics
- **Merge**: §5.6 (Total Business Context) + §5.7 (eCat Capture Rate) → §5.6 (Channel Mix & Capture Rate)
- **Renumber**: 8→7, 9→8, 10→9
- **New**: §5.10 (Order Timing Patterns, Q-69)
- **Result**: 1A, 1B, 2, 3, 4, 5, 6, 7, 8, 9, 10 (was 1A, 1B, 2–10 with 10 distinct)

### §8 Platform & Feature Utilization
- **Collapse**: 6 subsections → 1 health-check card with `<details>` fallback
- **Result**: Single "Platform Health Check" card

---

## Deferred Items

| Item | Reason | Prerequisite |
|------|--------|-------------|
| D.3 (Products browsed but never ordered) | Mixpanel `product_search` events exist but product-level item identifiers in event payload unconfirmed | Run targeted Mixpanel introspection on a known-active org to check for `item_number` or `product_id` in event properties |
| D.6 (Seasonal demand forecasting) | Requires multi-year data and validation across enough orgs. Complex query + uncertain availability | Accumulate 2+ years of order data across 10+ orgs before attempting |

---

## Re-Run Recommendations

Recommend re-running reports for these orgs to validate the changes:

1. **CCI** — Gold standard org with full data enrichment (portal_orders, Mixpanel, Clicky). Tests: merged Channel Mix & Capture Rate, health-check card, demand signal intelligence, coaching rollup, all Phase 4 framing enhancements. Most complete validation.

2. **RW (Renwil)** — Data-poor test (no portal_orders, limited Mixpanel). Tests: PARTIAL-tier teaser rendering, graceful degradation of merged subsections when gates are false, spread gate for Selling vs Admin Time.

3. **HFG** — Mid-tier with Clicky data. Tests: §6 Demand Signal Intelligence rename and engagement-first framing, geographic penetration narrative, Q-68 historical peak methodology.

**Before re-run**: Integrate Q-69 and Q-70 into `data_gather.py` if those new subsections should be validated in the same pass. Otherwise, they will silently skip (no cache files = no render).
