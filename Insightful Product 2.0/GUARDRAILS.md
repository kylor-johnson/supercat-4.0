# Insightful Product 2.0 — Guardrails

**Version**: 1.0 | **Last reviewed**: 2026-06-16 | **Next review**: 2026-09-15

This document is the canonical reference for preventing semantic errors, structural
drift, and boundary violations across all Insightful Product 2.0 deliverables.
Every operator, section guide, and script should reference this file.

### Documentation map (three layers)

| Layer | File | Purpose |
|-------|------|---------|
| **Map** | [`README.md`](README.md) | Onboarding: how to run, authority hierarchy, output paths. |
| **Inventory** | [`ARTIFACT_CATALOG.md`](ARTIFACT_CATALOG.md) | File-to-role inventory (keep in sync when adding files). |
| **Law** | This file | Hard rules, boundaries, ownership, review schedule. |

---

## 1. AUTHORITY HIERARCHY

These files form a single dependency chain. Each is derived from the one above it.
If there is a conflict, the higher-ranked file wins.

| # | File | Role |
|---|------|------|
| 1 | `authority/value_moment_catalog.md` | **Semantic authority** — VM definitions, allowed/forbidden claims. Never modified at runtime. |
| 2 | `authority/external_vm_index.md` | Runtime-safe VM lookup table — compact derivative of the catalog. |
| 3 | `authority/external_report_blueprint.md` | Assembly rules: section order, conditional logic, universal rules. |
| 4 | `authority/query_library.md` | Audited SQL reference, schema-grounded, audience-tagged. |
| 5 | `authority/peer_benchmark.md` | Lean guide for consuming Peer Benchmark system outputs. |
| 6 | `authority/html_report_template.html` | Parameterized HTML layout — presentation authority. |
| 7 | `operators/external/guides/{shared_rules, stage1_preflight_and_queries, stage4_assembly, section_01..08}.md` | Runtime guides — consumed by entry prompts. |

**Entry points** (consume everything above; execute these to generate output):
- External: `operators/external/run_prompt.md`
- Internal: `operators/internal/generate_internal_brief.md`

**Gold references** (layout/tone oracles — do not override catalog, blueprint, or query library):

| File | Role |
|------|------|
| `authority/gold/clm_2026-04-14_deep_intelligence_report.html` | **Primary layout oracle** — cleanest validated rendered output. |
| `authority/gold/clm_2026-04-14_executive_intelligence_report.html` | Historical layout/tone oracle. |
| `authority/gold/jyc_2026-04-14_executive_intelligence_report_v2.html` | Historical second-org layout oracle. |

Do not treat the HTML template or query library as independent authorities. They are
implementations of the blueprint and catalog, not design sources.

---

## 2. SEMANTIC GUARDRAILS

### Commerce terms

| Term | Correct Meaning | Never Use For |
|------|----------------|---------------|
| `orders` | eCat-originated orders only (`orders` table) | ERP or total-business data |
| `orders.order_source = 'ipad'` | Rep-submitted iPad orders | Online/self-service orders |
| `orders.order_source = 'server'` | B2B Cart buyer self-service orders | Rep orders |
| `portal_orders` | ERP-synced all-channel total business | Buyer activity, portal ordering, self-service |
| `Sales Portal` | Internal BI dashboard for the client's own team | A buyer-facing ordering channel |
| `self-service` | B2B Cart / eCat Online ordering only | Sales Portal, `portal_orders` |
| Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | Internal classification only — never in external output | Every section including Peer Benchmarking — in §7, use plain-language cohort framing derived from `peer_group_id_effective` |
| Health score | Internal only — never in Phase 1 external report | Any external output |
| `benchmark_confidence` | Internal rendering signal only — governs section inclusion and phrasing | Never as a visible label in client output |
| `peer_group_level` | Internal gating signal only | Never in client output (not even paraphrased as "tier 1/2/3") |
| `peer_group_n` | Internal calibration signal — governs framing strength | Never as a raw count in client-facing output |

---

## 3. HARD RULES

Invariant. No exception, no workaround, no soft reference:

1. Never surface health score, health band, or health classification in any external output.
2. Never surface VM-27, VM-28, VM-29, VM-36, VM-48 content externally.
3. If `has_clicky = false`, the Portal Engagement section does not exist. No placeholder. No mention of Clicky anywhere.
4. `portal_orders` is never buyer activity. Never "portal ordering adoption."
5. Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) are internal classification terms and must never appear anywhere in the external report — including Peer Benchmarking. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective`.
6. Executive Summary is always written last.
7. Every metric must include a time qualifier (e.g., "trailing 12 months," "last 90 days").
8. Every projection must be hedged with appropriate language ("potential," "estimated," "projected," "roughly," "could," "up to") in client-facing HTML. The literal tags `[HYPOTHETICAL]` and `[ESTIMATED]` are internal pipeline markers only — they must never appear as visible text in HTML fragments.
9. Every extrapolation must be hedged with appropriate language in client-facing HTML (same rule as #8).
10. Do not improvise around missing data — mark as N/A or omit per blueprint rules.
11. `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal signals only. Never expose these as labels in client-facing HTML.

---

## 4. FORBIDDEN PHRASES

> **Canonical tripwire list (single source of truth).** The runtime copy in
> `shared_rules.md §C` and the HARD/REVIEW token sets in `qa/eval/check_static.sh`
> mirror this list. If you add or remove a forbidden phrase here, update those
> two consumers.

Never in client-facing HTML:

- "health score" / "health scores"
- "portal orders" / "portal ordering" as buyer activity or entity label
- "net-new customers" — use "first-time eCat orderers"
- "ERP" in any client-facing text — use "total business," "all-channel sales," "your business system," "your account base"
- "Mixpanel" — use "platform engagement data" or "engagement events"
- "Clicky" — never in delivered HTML
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs, dataset paths
- "bounce_rate"
- `order_source = 'ipad'` and similar code literals in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels
- Literal `[HYPOTHETICAL]` or `[ESTIMATED]` tags

---

## 5. LOCKED DECISIONS

These are design decisions, not per-run judgment calls. Do not reopen them.

1. `portal_orders` = total-business context only — never buyer self-service.
2. Internal segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) = never in external output. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective`.
3. Clicky gating = binary — absent means the entire Portal Engagement section is absent, not soft-referenced.
4. Health score = internal only — never in the external report in any form.
5. Cost-of-inaction math = optional — only when quantified data directly supports it.

---

## 6. READ-ONLY DATA POSTURE

The report pipeline only ever *reads* data — every query is a `SELECT`. It never
writes, updates, or deletes in Postgres or BigQuery. The BigQuery connection is
named `user-bigquery-admin` for provisioning/history reasons; the report flow uses
it strictly read-only (results bounded by `LIMIT`). If any step appears to require
a write, that is a defect — stop and escalate rather than mutating client data.

### SQL guardrails (apply to every query touching `orders`)

```sql
-- 1. Nullable delete column — do not use = false alone
AND (is_marked_deleted = false OR is_marked_deleted IS NULL)

-- 2. NOT IN with NULLs — always exclude NULLs from the subquery list
AND customer_num IS NOT NULL
```

Violating either guardrail will silently return wrong row counts.

---

## 7. GATING FLAG CONTRACT

Each gate flag determines which sections and subsections are active. All must be
resolved in Stage 1 (Preflight) before any data queries.

| Flag | Source | Effect When False |
|------|--------|-------------------|
| `HAS_CLICKY` | `org_summary.has_clicky_portal` + table confirmation | Entire §6 absent; Clicky not mentioned anywhere |
| `HAS_CART` | `mobile_sites` B2B Cart + confirmed server order count > 0 | No channel mix section; no B2B Cart column |
| `HAS_PORTAL_ORDERS` | `portal_orders` row count > 0 AND GMV > 0 | ERP enrichment queries (Q-51–Q-54) N/A; per-section confidence tiers degrade to PARTIAL |
| `HAS_INVENTORY` | `inventories` row count > 0 | §4 Product & Inventory conditional |
| `HAS_SALES_DATA` | `sales_data` row count > 0 | VM-37, VM-39, VM-42 N/A |
| `HAS_SALES_SECTION` | ≥ 5 qualifying iPad reps with ≥ 10 orders LTM | §2 Sales Team omitted |
| `HAS_PEER_DATA` | Org in peer benchmark CSV AND `benchmark_eligible = True` | §7 Peer Benchmarking omitted |

### MCP failure & resume policy

MCP calls can fail mid-run — VPN drop, timeout, transient connection error.
Handle failures deterministically so a run is always either complete or cleanly
resumable. **Never fabricate, estimate, or carry forward stale data to cover a
failed call.**

- The cache dir is the resume ledger. A query is "done" only when its `cache/Q-*_results.md`
  exists with a complete header and body.
- Empty result (0 rows) IS done — write the file with `Row count: 0`.
- A query that errors out is NOT done — do not write its file.
- Gate integrity: only write `gate_flags.md` once every gate-source query has a complete
  result file. Stage 2–4 must never run on a partial gate set.

---

## 8. QUERY OWNERSHIP TABLE

Every query has one **primary owner** (the section responsible for rendering it)
and zero or more **cross-reference** consumers. If a query appears in two sections,
the primary owner renders the full analysis; the cross-referencer enriches an
existing subsection.

### Always-Run Queries

| Query | Description | Primary Owner | May Reference | Data Surface |
|-------|-------------|---------------|---------------|--------------|
| Q-07 | Catalog completeness | §4 Product | §8 Platform | Product catalog fields |
| Q-08 | Data freshness timestamps | §8 Platform | — | Entity last-updated dates |
| Q-09 | Import pipeline health | §8 Platform | — | Import logs |
| Q-10 | Catalog counts / smart stacks | §8 Platform | — | Catalog metrics |
| Q-11 | Configuration completeness | §8 Platform | — | Feature flags + config |
| Q-12 | Customer activation | §3 Customers | — | Customer network health |
| Q-13 | Top-buyer concentration | §5 Commerce | — | Customer eCat GMV share |
| Q-14 | Reorder velocity | §3 Customers | — | Order frequency patterns |
| Q-17 | Dormant high-value accounts | §3 Customers | — | Dormant customer list |
| Q-18 | eCat order trend (Part A) | §5 Commerce | — | Order trend + channel |
| Q-20 | AOV by segment | §5 Commerce | — | Order value segments |
| Q-21 | Order type & workflow | §5 Commerce | — | Order type distribution |
| Q-22 | Feature usage depth | §8 Platform | — | Mixpanel feature events |
| Q-40 | Geographic distribution | §3 Customers | — | eCat orders by state |
| Q-41 | New eCat buyer acquisition | §3 Customers | — | New buyer counts |

### Conditional Queries

| Query | Gate | Description | Primary Owner | May Reference | Data Surface |
|-------|------|-------------|---------------|---------------|--------------|
| Q-01 | HAS_SALES_SECTION | Rep leaderboard + behavioral | §2 Sales | — | Rep orders + Mixpanel |
| Q-02 | (derived from Q-01) | Selling archetypes | §2 Sales | — | Behavioral classification |
| Q-03 | (derived from Q-01) | Funnel gap analysis | §2 Sales | — | Behavioral ratios |
| Q-06 | HAS_SALES_SECTION | Rep engagement trajectory | §2 Sales | — | Rep engagement trend |
| Q-14b | HAS_PORTAL_ORDERS | Account velocity deceleration | §3 Customers | — | Order frequency shift |
| Q-16 | HAS_PORTAL_ORDERS | Total business visibility | §5 Commerce | — | All-channel GMV |
| Q-18B | HAS_PORTAL_ORDERS | eCat share of total trend | §5 Commerce | — | Share trend |
| Q-37 | HAS_INVENTORY + HAS_SALES_DATA | Top sellers OOS | §4 Product | — | Inventory + sales |
| Q-38a | HAS_PORTAL_ORDERS | Product velocity trend | §4 Product | — | Item velocity |
| Q-39 | HAS_SALES_DATA | Line analysis | §4 Product | — | Category/collection sales |
| Q-42 | HAS_SALES_DATA | New introduction perf | §4 Product | — | New item revenue |
| Q-43 | HAS_SALES_SECTION | Territory coverage | §2 Sales | — | Territory metrics |
| Q-45 | HAS_PORTAL_ORDERS + VM45 | eCat capture rate | §5 Commerce | — | Capture % |
| Q-46 | Mixpanel present | Workflow maturity | §8 Platform | — | Submit-through rate |
| Q-47 | Smart stacks > 0 | Smart stack metadata | §8 Platform | — | Stack freshness |
| Q-50 | Library present | Document engagement | §8 Platform | — | Library inventory |
| Q-51 | PORTAL_REP_DATA_PRESENT | Rep eCat capture | §2 Sales | — | Rep-level ERP enrichment |
| Q-52 | PORTAL_CUSTOMER_DATA_PRESENT | Customer eCat penetration | **§3 Customers** | §5 Commerce (top-buyer enrichment) | Customer-level penetration |
| Q-53 | PORTAL_CUSTOMER_DATA_PRESENT | Unactivated high-value | §3 Customers | — | Zero-eCat ERP accounts |
| Q-54 | PORTAL_CUSTOMER_DATA_PRESENT | Geographic penetration | §3 Customers | — | State-level enrichment |
| Q-55 | HAS_PORTAL_ORDERS | Category displacement | §5 Commerce | — | Category share shift |
| Q-56 | PORTAL_REP_DATA_PRESENT | Rep capture trend | §5 Commerce | — | Rep capture decline |
| Q-57 | HAS_PORTAL_ORDERS + PCUST | Cross-sell whitespace | §3 Customers | — | Category gaps |
| Q-58 | HAS_COMMITMENT_DATA | Market commitment | §5 Commerce | — | Market conversion |
| Q-58b | HAS_COMMITMENT + INVENTORY | In-stock actionable items | §5 Commerce | — | Warehouse opportunity |
| Q-59 | HAS_PORTAL_ORDERS | Fill rate & backorder | §4 Product | — | Fulfillment metrics |
| Q-60 | HAS_PORTAL_ORDERS | Price erosion detection | §5 Commerce | — | Avg unit price decline |
| Q-61 | HAS_PORTAL_ORDERS + NEW_ITEMS | New intro adoption gap | §4 Product | — | Adopted items list |
| Q-62 | HAS_PORTAL_ORDERS + NEW_ITEMS | Launch velocity by rep | §2 Sales | — | Rep new-item adoption |
| Q-63 | MIXPANEL_USER_DATA_PRESENT | Presentation→order conversion | §2 Sales | — | Rep conversion rate |
| Q-64 | MIXPANEL + PORTAL_ORDERS | Rep engagement vs revenue | §2 Sales | — | Engagement depth |
| Q-65 | MIXPANEL_USER_DATA_PRESENT | Selling vs admin time | §2 Sales | — | Time allocation |
| Q-66 | HAS_PORTAL_ORDERS + BUYER | Buyer-within-account | §3 Customers | — | New decision-makers |
| Q-67 | HAS_PORTAL_ORDERS + PCUST | Geographic revenue trends | §3 Customers | — | QoQ state shifts |
| Q-68 | HAS_PORTAL_ORDERS + PCUST | Wallet share estimation | §3 Customers | — | Peer-group gap |
| Q-CL-01 | HAS_CLICKY | Portal traffic trend | §6 Portal | — | Clicky page views |
| Q-CL-03 | HAS_CLICKY | Geographic portal demand | §6 Portal | — | Clicky geo data |
| Q-CL-05 | HAS_CLICKY | Traffic sources | §6 Portal | — | Clicky referrers |
| Q-CI-02 | HAS_PEER_DATA | Peer comparison | §7 Peer | — | Segment benchmark |
| Q-CI-03 | HAS_PEER_DATA | Feature adoption benchmark | §7 Peer | — | Peer feature table |
| Q-CI-05/06 | HAS_PEER_DATA | Top-performer patterns | §7 Peer | — | Behavioral patterns |

**Cross-reference note:** Q-52 is the only query with a true cross-section consumer.
§3 is the primary owner (renders the full penetration table). §5 uses Q-52 data
to enrich the Top Buyers table (subsection 4) with "Total Business" and "eCat
Share" columns. If Q-52 fails, §3 loses subsection 2 and §5 loses the enrichment
but both sections still render.

---

## 9. SECTION BOUNDARY CONTRACTS

Every section guide in `operators/external/guides/` includes a `DOES NOT COVER`
block listing what it refuses to produce and where that content belongs. Per-section
detail lives in the individual guides; this section provides the summary.

| Section | Owns | Does Not Cover |
|---------|------|----------------|
| §2 Sales Team | Rep performance, archetypes, coaching, behavioral, territory | Customer analysis, commerce channels, product catalog, portal traffic, platform features, health score |
| §3 Customers | Activation, penetration, dormancy, velocity, whitespace, buyer detection, geographic trends, wallet share | Rep coaching, channel mix, product catalog, portal traffic, peer benchmarking, health score |
| §4 Product | Catalog health, inventory, sales lines, fill rate, velocity, new introductions | Customer analysis, rep performance, order trends, portal traffic, peer benchmarking, health score |
| §5 Commerce | Order trends, channel mix, capture rate, concentration, displacement, market attribution, price erosion | Rep coaching, customer activation, product catalog, portal traffic, peer benchmarking, health score |
| §6 Portal | Traffic health, trend, geographic demand, traffic sources | Commerce analysis, rep performance, customer analysis, product inventory, peer benchmarking, health score |
| §7 Peer | Cohort comparison, hero stat, metric breakdown, top-performer patterns, feature adoption | Individual rep coaching, customer analysis, product catalog, commerce trends, portal traffic, health score |
| §8 Platform | Catalog health, feature usage, data freshness, pipeline health, config alerts, smart stacks | Rep performance, customer analysis, product sales, order trends, portal traffic, peer benchmarking, health score |

---

## 10. QUARTERLY CONTRACT REVIEW

Every 90 days, run a diagnostic comparing actual output against contracts.
This prevents silent drift between documentation and reality.

### Review Checklist

- [ ] Does each section guide's output match its stated scope?
- [ ] Does each section guide's DOES NOT COVER match reality (no cross-boundary content)?
- [ ] Have any queries been added to `authority/query_library.md` without updating section guides?
- [ ] Do gate flags in `stage1_preflight_and_queries.md` match `data_gather.py` implementation?
- [ ] Has the authority hierarchy been respected (no downstream file contradicting upstream)?
- [ ] Are gold references still representative of current output format?
- [ ] Has any section guide grown >30% in line count since last review?
- [ ] Are confidence tier formulas still accurate for the current gate set?
- [ ] Does the `ARTIFACT_CATALOG.md` match the actual file tree?
- [ ] Does the Query Ownership Table (§8 above) match actual query-to-section mappings?
- [ ] Has the forbidden phrase list (§4) been updated to match `shared_rules.md §C` and `check_static.sh`?
- [ ] Are golden-set eval fixtures (CLM, WWJC, UFI, PF, CCI) still passing in static mode?

### Schedule

| Review | Date | Status |
|--------|------|--------|
| Q3 2026 | 2026-09-15 | Scheduled |
| Q4 2026 | 2026-12-15 | Scheduled |
| Q1 2027 | 2027-03-15 | Scheduled |

### How to Run

1. Compare all section guides against this guardrails document and the artifact catalog.
2. Run `check_static.sh` on the most recent output for each golden-set org.
3. Verify the file tree matches `ARTIFACT_CATALOG.md` (new files? deleted files?).
4. Produce a drift score per dimension (0–3: Absent / Ad hoc / Defined / Robust).
5. Document recommended corrections and update this file's "Last reviewed" date.

---

*Last updated: 2026-06-16 | Maintainer: Insightful Product 2.0*
