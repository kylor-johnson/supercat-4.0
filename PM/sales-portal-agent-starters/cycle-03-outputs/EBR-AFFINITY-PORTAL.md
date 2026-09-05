# EBR Affinity — Sales Portal / Reporting only

**Date:** 2026-07-17 · **Cycle:** 03 · **Decision this serves:** Which open EBR tickets are the Sales Analytics program, and which are noise?
**Doctrine:** affinity → mechanism clusters → Shape Up bets ([00a-DOCTRINE](../00a-DOCTRINE-shapeup-ddd-affinity.md)).
**Scope lock:** Sales Portal reporting / dashboard / Intelligence Reports. iPad, catalog eOL, order-email = out. SERV = downstream footnotes only.

---

## 1. Keep — mechanism clusters

### C0 — Epic umbrella
| Key | Summary | Status | Role |
|---|---|---|---|
| [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775) | Insightful Product: LLM-powered analytics and reporting | Submitted | **Program epic** — computational first; LLM children parked |

### C1 — Territory filter truth (portal structural)
| Key | Summary | Status | Role |
|---|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | Territory filter isn't working for invoice list | Triaging | **In** Phase-1 pitch |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | Territory filter on sales portal dashboard | In Progress (stalled since 2022) | **In** Phase-1 pitch |
| [EBR-180](https://supercatsolutions.atlassian.net/browse/EBR-180) | Allow RepNumber multiple territory codes | Triaging | **XL shelf** — downstream SERV-2178/2180; separate appetite |

**Problem story (verbatim shape):** Rep opens Sales Portal invoice list / dashboard, picks a territory, and still sees the wrong book (all / none / other territories) → exports to Excel.

### C2 — Metric / totals truth (AC inputs for every hero)
| Key | Summary | Status | Role |
|---|---|---|---|
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | Exported sales don't add up to displayed totals | Triaging | Reconciliation AC — invoiced spine must match UI |
| [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87) | Exclude quotes from eOL portal totals | Triaging | **Parked from Bet A GO** (2026-07-21) — not universal; metric-law copy only |
| [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) | Sales totals should reflect discounts | Triaging | **Doctrine-answered** by `net_amount` (Prod-Council denied 2022) — recommend close |

**Problem story:** Owner exports Customers.csv; sum ≠ on-screen total. Or quotes inflate "sales."

### C3 — Intelligence Report heroes (computational / UX)
| Key | Summary | Status | Role |
|---|---|---|---|
| [EBR-198](https://supercatsolutions.atlassian.net/browse/EBR-198) | Sales dashboard – hot/cold customers | Triaging | **= S1** quietly-dying — v1 second commerce hero |
| [EBR-197](https://supercatsolutions.atlassian.net/browse/EBR-197) | Sales dashboard – hot/cold items | Triaging | Product vitality — post-v1 |
| [EBR-278](https://supercatsolutions.atlassian.net/browse/EBR-278) | Territory view – analytics | Triaging | Lane-2 seed — gated on territory data |
| [EBR-687](https://supercatsolutions.atlassian.net/browse/EBR-687) | Allow drill-down on portal dashboard | Submitted | UX pattern for IR surface |

**Problem story:** Owner wants "who is quietly dying?" without Excel + Claude grind (F3 / EBR-775).

### C4 — One-org / deferred (shape later, not v1)
| Key | Note |
|---|---|
| EBR-213 | Quota/budget — sarreid-only (`sales_quotas`) |
| EBR-629 | Trade Name filter — grouping opaque |
| EBR-38 | Large datasets — infra rabbit hole |
| EBR-325 | Default date range "All Available" |
| EBR-471 | Keyword search invoices/orders |
| EBR-474 ≈ EBR-601 | Portal invoice status (Savoy) — **dup pair** |
| EBR-699 | Customize customer exports |
| EBR-756 | Parts / credit memos on order view |
| EBR-279 | Sales Portal Mapping — idea dump |
| EBR-745 | MPC Sales Portal enablement — GTM, not IR |
| EBR-110 | Territory favorites — likely defunct |

### C5 — LLM (parked under 775)
| Key | Role |
|---|---|
| [EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772) | Agentic insights for Sales Portal — **PARK** |
| [EBR-776](https://supercatsolutions.atlassian.net/browse/EBR-776) | LLM rep reporting — **dup cluster with 772** — **PARK** |

---

## 2. Remove from program (reroute)

| Key | Why out of Sales Analytics |
|---|---|
| EBR-36 | iPad shared-drafts by territory — not portal reporting |
| EBR-655 | Order-email CC by territory — not reporting |
| EBR-743 | iPad real-time analytics — later channel; portal-first |
| EBR-329 | Invoice email recipients — not analytics |
| EBR-527 | Push eCat orders → portal orders — integration |
| EBR-503 | Option/fabric search on eOL lists — not IR bet |
| EBR-524 | Custom eOL customer dashboard tab — not IR bet |

---

## 3. Dup / link pairs

| Pair | Action |
|---|---|
| EBR-474 ≈ EBR-601 | Keep one canonical (601 Waiting for Client); link 474 as dup |
| EBR-772 ≈ EBR-776 | Park both under EBR-775; 776 = sibling of 772 |
| EBR-180 → SERV-2178 | EBR stays product ask; eng = downstream SERV footnote |
| EBR-40 / EBR-212 | Same mechanism — one Phase-1 pitch |

---

## 4. Cross-org universes (reboot §2.1 — do not collapse)

| Universe | Travels | Program implication |
|---|---|---|
| **A — Invoice arithmetic** | C1, S1, YoY, concentration… | 55/55 where feed not DEAD |
| **B–D — Behavior floor** | Q-R1/R2/R4, Q-18, Q-01, Mixpanel depth | ERP-optional team strip |
| **E — Invoiced rep→revenue** | RS-01, Q-R5, Q-51 | Narrow Tier-2 — do not lead v1 |

---

## 5. Elite order (locked)

1. This affinity + spine cleanup  
2. Shape C1+C2 (EBR-40/212 + 91/87)  
3. Wireframe + feedback (C1 + S1 + team strip)  
4. IR v1 AC under EBR-775  
5. Computational ship (on GO)  
6. Park EBR-772/776  

---

## 6. Downstream eng (out of this plan)

SERV tickets that may implement EBR asks after `ISOLATION OFF` — see spine Appendix A. Not betting-table work here.

---

*Affinity complete 2026-07-17. Paste into Orchestrator; drives spine §6.*
