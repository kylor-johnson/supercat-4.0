# Section 02 Build Plan — Account Intelligence

Run: Designer's Fountain (df), 2026-06-17
Confidence tier (SECTION_CONFIDENCE_2): **STRONG** — but `HAS_PORTAL_ORDERS=False`
and no `{{LAST_PORTAL_ORDER_DATE}}` resolvable → per guide fallback rule, use the
`§2-PARTIAL` template with label "PARTIAL VIEW".

## Gate evaluation

Key flags: HAS_PORTAL_ORDERS=False, PORTAL_CUSTOMER_DATA_PRESENT=False,
HAS_BUYER_DATA=False, HAS_INVENTORY=True, HAS_SALES_DATA=False.
Data present: Q-12 (1 row), Q-14 (1 row), Q-17 (3 rows), Q-17-atrisk (3 rows),
Q-40 (4 rows), Q-41 (rep-acquired buyers). top_accounts.md = ZERO rows.
All Q-ORG-* empty/0 rows. Q-52/53/54/57/66/67/68 all "(not present)".

## Pre-Build Gate Check (mandatory-when-gate-met table)

| Cache File | Gate Condition | Status | Subsection | Will Render |
|---|---|---|---|---|
| Q-52 | PORTAL_CUSTOMER_DATA_PRESENT=true | NOT MET (false; file absent) | 3b eCat Penetration | NO |
| Q-14b | HAS_PORTAL_ORDERS=true | NOT MET (false; file absent) | 8b Deceleration Alert | NO |
| Q-57 | HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT | NOT MET (both false; file absent) | 9 Cross-Sell Whitespace | NO |
| Q-67 | HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT | NOT MET (both false; file absent) | 11 Geographic Trends | NO |
| Q-68 | HAS_PORTAL_ORDERS + PORTAL_CUSTOMER_DATA_PRESENT | NOT MET (both false; file absent) | 12 Spending Contraction | NO |

## Full subsection manifest

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| 1. Header Metrics (Q-12) | MANDATORY | MET (Q-12 has data) | YES |
| 2. Data Confidence Header | MANDATORY | MET (always) | YES |
| 3. Top 10 Mini-Briefs | MANDATORY | MET (top_accounts empty → fall back to active eCat account from Q-14/Q-40) | YES (1 brief: Staggs Interiors) |
| 3b. eCat Penetration (Q-52) | MANDATORY-when-gate-met | NOT MET | NO |
| 4. Dormant High-Value (Q-17) | CONDITIONAL | MET (Q-17 + Q-17-atrisk have 3 dormant eCat accounts, 259–362d silent) | YES |
| 5. Unactivated High-Value (Q-53) | CONDITIONAL | NOT MET (file absent) | NO |
| 5b. Enterprise Channel Accounts | CONDITIONAL | NOT MET (no ENTERPRISE_CHANNEL set) | NO |
| 6. Geographic Distribution (Q-40) | CONDITIONAL | MET (MS = 77.5% of eCat GMV > 30%; 4 rows) | YES |
| 7. Velocity Deceleration (Q-ORG-CONTRACTION) | CONDITIONAL | NOT MET (0 rows) | NO |
| 8. Reorder Velocity (Q-14) | MANDATORY | MET (Q-14 has 1 active reorder account) | YES |
| 8b. Deceleration Alert (Q-14b) | MANDATORY-when-gate-met | NOT MET (file absent; HAS_PORTAL_ORDERS=false) | NO |
| 9. Untapped Category (Q-57) | MANDATORY-when-gate-met | NOT MET | NO |
| 10. Buyer-Within-Account (Q-66) | CONDITIONAL | NOT MET (HAS_BUYER_DATA=false; file absent) | NO |
| 11. Geographic Revenue Trends (Q-67) | MANDATORY-when-gate-met | NOT MET | NO |
| 12. Spending Contraction (Q-68) | MANDATORY-when-gate-met | NOT MET | NO |

## Rendering notes

- This org is early in eCat adoption: 778 total customers, 13 ever ordered via
  eCat, only 4 active in trailing 12mo. Account data is eCat-only — no all-channel
  /total-business feed connected → drives the PARTIAL-fallback confidence header.
- Mini-briefs: top_accounts.md is empty (signal detection surfaced 0 signal-density
  accounts), so the mandatory core renders from the one account with real reorder
  data — Staggs Interiors (Q-14: 7 eCat orders, $7,119 LTM, avg 52.7-day cadence,
  MS per Q-40, last order 2026-05-14). Engagement Score computed below. No YoY data
  (no prior-year eCat baseline) → omit YoY metric-note. No companion/decay/stockout/
  displacement signals fired → those mini-brief components silently omitted.
- Engagement Score (Staggs): Recency 25 (last order ~34d ago, ≤ linear high),
  Frequency ~20 (7 orders, top of a thin active set), Monetary ~12 (only active
  buyer of size; thin org baseline), Trajectory 10 (no YoY → neutral/cooling default)
  → ~67 → "Strong" `.badge.ok`. Treated conservatively.
- Dollar figures: all eCat-only, all carry "LTM" qualifier. Avg LTM rev/active =
  ($7,119+$935+$850+$276) / 4 = $9,180 / 4 ≈ $2,295.
- Dormant (sub 4): Q-17-atrisk gives days_since_last_ecat_order for the "Silence
  vs Normal" column. Historical GMV is small ($276–$935) — framed as re-activation,
  not high-value alarm. No SIG-RISK-02 $15K+ accounts exist; rendered as the real
  dormant set with honest framing.
- Geographic (sub 6): MS dominates (77.5% of eCat GMV). 4 rows, 1 customer each.
  Rendered compact. customer_count column kept (all =1 but meaningful for context);
  no empty columns to suppress.
- Reorder Velocity (sub 8): 1 row (Staggs). Mandatory always-render; presented as
  the table the spec specifies. Q-14b absent → no Deceleration Alert.
- All-caps cache names title-cased: STAGGS INTERIORS → Staggs Interiors,
  BEST LIGHTING & ACCESSORIES INC → Best Lighting & Accessories Inc, etc.
- section-contents middot list: Top account briefs · Dormant accounts ·
  Geographic distribution · Reorder velocity.
- Section-level what-this-means required (max 3 sentences, Action-led).
