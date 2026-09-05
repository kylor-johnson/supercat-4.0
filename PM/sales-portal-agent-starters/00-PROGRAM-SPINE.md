# Sales Analytics (Portal & Reporting) — Program Spine
**Date:** 2026-07-16 · **Cycle-03 update:** 2026-07-18 (eng-handoff A+B+C+E written; Bet E AC + ship-readiness frozen; EBR-only scope 2026-07-17) · **2026-07-24** Bet F shaped · **Bet A GO** (`ISOLATION OFF — GO on EBR-40` — see `CTO-FEEDBACK-2026-07-24.md`)  
**Owner:** Kylor  
**Working hypothesis:** Destination **C** — structural fixes & modern UX in portal → computational Intelligence Reports → inferential / talk-to-data later.  
**Ticket scope:** Program work is **EBR-keyed**. SERV = downstream eng footnotes only (Appendix A). iPad / non-portal eOL EBRs are out of this program.

## ISOLATION MODE

### Bet A — LIFTED 2026-07-24

**Verbatim GO:** `ISOLATION OFF — GO on EBR-40`

| Allowed for Bet A | Still forbidden |
|---|---|
| Implement EBR-40 / 212 / 91 (+ doctrine close EBR-7) in `supercat-code/` against `FILTER-TRUTH-AC.md` + `ENG-HANDOFF-bet-a-b-c-e.md` §C | Expanding into Bet C / E / F / LLM without a separate GO |
| SERV stories linked from keep EBRs (`SPRINT-PACK-bet-a.md`) | EBR-180 XL, EBR-87 dedicated build, iPad tickets |
| PRs / staging verify on **wwjc** | Claiming territory truth on sarreid until SERV-2196-class is honest |

### Other bets — still isolated

Bet C / D / E / F remain **spec / triage only** until their own GO phrases. See `BET-TRIAGE-BOARD.md`.

**Jira:** Prefer description + link + board moves for sprint handoff. Do **not** post hygiene/noise comments on EBR tickets (that is why `jira-read-only` exists for other chats).

This file is the **router**. Fresh agents get a starter from this folder — not this whole pile again.

---

## 1. What this program is

One program, three lanes:

| Lane | Name | Job | Ships when |
|---|---|---|---|
| **0** | Trust / Fix | Broken portal access, filters, feed/config bugs | Customer can trust the numbers & see the right book |
| **1** | Legible / UX | Design overlay + structural modern UX (wireframes → feedback → AC) | Portal feels modern, answer-first paths for top jobs |
| **2** | Smart / Computational | Insightful 4.0–grade Intelligence Reports *surfaced* (deterministic first) | One hero answer reconciles to invoiced truth |
| **3** | Later | Inferential / LLM / talk-to-data ([EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772)) | Only after Lane 2 is trusted |

**WIP progression (hard rule):**  
`structural fixes & modern UX > computational insights > inferential OR talk to your data`

**Process (every bet):**  
Stories → features → specs / AC → prototype/demo → customer feedback → update AC → build → staging → verify → prod → verify & document & promote

---

## 2. Path map (what “@SuperCat Ops/…” means)

In this workspace, those folders live under **SuperCat 4.0**:

| Mention | Absolute path |
|---|---|
| Insightful Product 4.0 | `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Insightful Product 4.0/` |
| design-system | `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/design-system/` |
| EBR 2.0 (theme source) | `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/EBR 2.0/` |
| Portal product handoff | `.../SuperCat 4.0/sales-portal-analytics-handoff-2026-07-16.md` |
| Rails code | `/Users/kylorjohnson/supercat-code/supercat_server/` |
| PM home (this program) | `SuperCat 4.0/PM/sales-portal-agent-starters/` |
| PM doctrine | `…/PM/sales-portal-agent-starters/00a-DOCTRINE-shapeup-ddd-affinity.md` |
| Product handoff (copy) | `…/PM/sales-portal-agent-starters/00b-PRODUCT-HANDOFF-analytics.md` |

Frozen: Insightful Product / 2.0 / 3.0 — do not touch unless asked.

---

## 3. Production truth (do not rediscover)

- Sales Portal = mature eOL feature: Dashboard / Orders / Invoices / Customers / Reports  
- Same URL space & `layouts/ecat` as catalog → **layout coupling risk**  
- Data: `portal_orders` / `portal_invoices` (+ warehouse sales facts for dashboard)  
- Imports: `order_data.csv` / `invoice_data.csv` (ERP reporting imports — not iPad orders)  
- Phase 3 chrome / answer-first / Omni explore = **mockups only** (not in Rails)  
- Insightful 4.0 already runs CEO reports off the same tables; **invoiced `net_amount` = total business**; portal UI ≠ validation ground truth  
- Live density orgs for comps: `sarreid`, `cci`
- **Scale (cycle-02 recount):** **55 orgs** carry `portal_invoices` = **4.88M rows** (`PORTAL-ORG-MATRIX.md`; supersedes the earlier 4.68M estimate). Canonical LTM topline: **sarreid $15.98M**, **cci $71.23M** (RTD-clamped, $5M cap). Production book ≈ **44 orgs** (excl. ~11 test/demo).
- **Cycle-02 gather artifacts are the standing authority** for capability / feasibility / settings, in `cycle-02-outputs/`: `PORTAL-CAPABILITY-MAP.md` (16 computable-now / 13 gated / hard-gaps), `PORTAL-ORG-MATRIX.md` (all 55 profiled), `PORTAL-SETTINGS-CONTROL-PLANE.md` (134 toggles triaged).

---

## 4. EBR consolidation — affinity findings (from Jira + EBR 2.0 + Insightful)

Mechanism-named themes (not topic labels). Each maps to a lane.

| # | Finding (mechanism) | Evidence | Lane | Decision it supports |
|---|---|---|---|---|
| F1 | **Reps / CSMs treat Sales Portal as the KPI shelf — but trust breaks when territory filters lie** | [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40), [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212); XL shelf [EBR-180](https://supercatsolutions.atlassian.net/browse/EBR-180) | **0** | Shape filter truth on EBR-40/212 before new metrics; XL multi-territory model is a separate appetite |
| F2 | **Customers already say “most metrics are in Sales Portal” — the ask is *surface + execute*, not invent a new data warehouse** | [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775); portal-first (iPad channel EBRs out of program) | **1→2** | Wireframe portal-first answers under EBR-775 |
| F3 | **Manual Insightful work (Excel + Claude + Power BI) is the product spec — automation must replace that grind with computational truth first** | [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775), Jamie Young / Renwil signals; Money Map heroes C1–C4; [EBR-198](https://supercatsolutions.atlassian.net/browse/EBR-198) = S1 | **2** | Ship computational Intelligence Reports before LLM layer |
| F4 | **Modern UX demand — design-system App kit (`.kshell`) is the overlay language for wireframes + feedback, not a new brand** | EBR-687 drill-down; `design-system/docs/SURFACES.md` Product 2 | **1** | Overlay prototypes on App kit; Rails reface is downstream eng, not this plan’s primary ticket |
| F5 | **Feature ask pile is a grab-bag unless shaped against F3 heroes** | EBR-197/198/213/278/629/687 + deferred cluster in affinity | **2 after shape** | Only bet features that feed a named Intelligence Report answer |
| F6 | **LLM / NL query / anomaly agent for portal is desired but explicitly downstream of computational foundation** | [EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772) + [EBR-776](https://supercatsolutions.atlassian.net/browse/EBR-776) under EBR-775 | **3 / no-go now** | Park talk-to-data until computational surface is trusted |
| F7 | **EBR decks already score “No Portal Usage” — adoption is a GTM metric, not just a UI project** | EBR Metrics Framework §4–5, §11 risk flags | Program | Pair every ship with enablement / EBR talking points |
| F8 | **Commerce-universal ≠ “only Topline.”** True Topline (invoiced net + RTD + $5M) travels **55/55**; ~16 invoice-arithmetic metrics in `PORTAL-CAPABILITY-MAP` §1 also travel. Concentration is org-specific (sarreid top-1 ≈ 30% vs median ≈ 8%) — degrade to "healthy diversification." **S1 (quietly dying / EBR-198) may be the better second commerce hero** (wider travel; rep naming degrades gracefully). | `PORTAL-ORG-MATRIX.md`; `PORTAL-CAPABILITY-MAP.md`; reboot §2.1 | **2** | v1 = C1 + S1 (or C3 with degrade) + team strip — not topline+concentration alone |
| F9 | **Three universes — do not collapse.** (A) Invoice arithmetic 55/55. (B–D) Behavior floor (Q-R1/R2/R4, Q-18, Q-01, Mixpanel) is ERP-optional and includes Tier-0 ufi/kll. (E) Invoiced named-rep→revenue is Tier-2 only (~11 fresh / 12 Tier-0 impossible). Tier gates kill **rep→revenue only**, not team intelligence. | `provenance_map_rep.md`; `PORTAL-ORG-MATRIX.md`; affinity §4 | **2** | Lead team strip on behavior; never lead RS-01; relabel gross-only as "returns not represented" |
| F10 | **Portal behavior hides in 134 toggles / 6 layers / 39 YAML flags with no admin surface** | `PORTAL-SETTINGS-CONTROL-PLANE.md` (cycle-02) | **0→1** | Bet E — self-service control plane (downstream eng implements) |
| F11 | **Territory filter truth is a multi-year EBR sprawl** — EBR-40 + EBR-212 (stalled IP since 2022) are the portal filter story; EBR-180 is XL multi-territory (downstream SERV). Empty territory master on **32/55** orgs data-gates territory rollups. | `EBR-AFFINITY-PORTAL.md`; prevalence audit | **0** | Bet A = shape EBR-40/212 (+ metric-law 91/87); shelf EBR-180 |
| F12 | **Metric/totals-truth EBRs are old and open.** EBR-7 Prod-Council-denied yet open (`net_amount` answers it); EBR-91 period drift **validated keep**; EBR-87 **parked** (not universal). **EBR-776** is a 2nd LLM ticket beside EBR-772. | Cycle-03 affinity | **0/2/3** | Gate heroes on EBR-91 AC; park EBR-87 build; close EBR-7 via doctrine; park 772+776 |

### Cycle-02 prevalence audit (Postgres, read-only, 2026-07-17) — turns tickets into counts

**Comma-rep / SERV-2178+2180 blast radius** — only **5 orgs** have any comma in `rep_number`; live footprint is **2 production orgs**:
- **wwjc** — 31,275 comma invoice rows (55% of its book), current, **runs 2 brand sites** (Chelsea House + Wildwood).
- **asi** — 6,730 comma rows (12%), current. *(jyc = 111k rows but future-dated/suspect; wwtest/ctest = test.)*
- Decision: SERV-2178 is a **2-customer bet (wwjc + asi)**, not a kill and not universal. Go/no-go needs the flag state (below).

**Empty territory master / SERV-2214+2180** — **32 of 55 portal orgs (58%) have zero `territories` rows** → any territory rollup/name feature is data-gated on the majority.

**Ship-to over-grant / SERV-2196 exposure surface** (multi-territory bill-tos, realizable where users hold territory grants):

| Org | Portal invoices | Multi-territory bill-tos | % | Users w/ territory | Note |
|---|---|---|---|---|---|
| shl | 449,870 | 1,222 | **100%** | 100 | **reporter of SERV-2196 — confirmed** |
| sarreid | 43,715 | 4,249 | **99.8%** | 77 | **golden demo org — pervasively exposed** |
| ufi | 120,663 | 6,757 | **100%** | 42 | biggest raw surface (Tier-0) |
| wwjc | 56,719 | 8,791 | 72.9% | 53 | **double bug** (also #1 comma-rep) |
| ta / bri / gl / jyc | — | 1.2k–7.5k | 55–99% | 62–133 | exposed |
| ~34 other portal orgs | — | **0** | 0% | — | **structurally immune** |

**Honest limits (both require `supercat_server`, isolation-frozen):**
- **Confirmed unauthorized-view count is NOT computable from Postgres** — the invoice↔bridge join + "home territory = `ship_to_code IS NULL`" assumption over-counts (sarreid → 100%, shl → 0 match). Exact leak needs the portal's access query. → FIX-lane code task.
- **`territory_access_via_rep_number` is not in Postgres** (no table/column; absent from `mobile_sites.properties.flags` on all 9 checked orgs) — it lives in **code/YAML deploy config**, confirming F10. SERV-2178 go/no-go needs a code read.

**Demo de-risk:** because **sarreid has 99.8% multi-territory bill-tos**, any territory-scoped view in a Bet B/C demo on sarreid can surface the over-grant live — fix SERV-2196 first or demo territory scoping on a zero-exposure org. **wwjc is the trust flagship** (only org at the intersection of both territory bugs).

### EBR theme consolidation → program bullets

| Your theme | Spine mapping |
|---|---|
| EBR consolidation of themes | This §4 table (refresh from Jira/EBR as needed) |
| Surface Intelligence Reports (computational to start) | Lane 2 — C1 + S1 (EBR-198) + team strip under EBR-775 |
| Wireframe prototypes + feedback | Lane 1 — design-system App surfaces |
| Output spec + acceptance criteria | Per-bet AC after PROGRAM shapes |
| Inferential / talk-to-data | Lane 3 — EBR-772 — explicit later |

---

## 5. Shaped bets (appetites — draft for betting table)

### Bet A — Territory & filter truth (Lane 0) · Small→Big (cycle-03 EBR-shaped, F11/F12)
- **Problem:** Portal users pick a territory on invoice list / dashboard and still see the wrong book → Excel workarounds; Customers period/export drifts from on-screen.  
- **Validation (2026-07-21):** **Complete** — see filled `BUG-VALIDATION-PACK.md`.  
- **GO (2026-07-24):** `ISOLATION OFF — GO on EBR-40` — CTO ready for EBR→SERV (`CTO-FEEDBACK-2026-07-24.md`).  
- **EBR in-scope (locked):** [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) + [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) paired; [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) period drift (AC-A2 rewritten). [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) = doctrine close.  
- **Parked:** [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87) — not universal; no dedicated build.  
- **XL shelf (separate appetite):** [EBR-180](https://supercatsolutions.atlassian.net/browse/EBR-180) multi-territory RepNumber — downstream eng footnote SERV-2178/2180. Do not start without separate GO.  
- **Dedupe/reroute:** EBR-474↔EBR-601; EBR-36/655/743/329/527 out of program (see affinity).  
- **No-gos:** New metrics, LLM, full reface / Dashboard redesign as the Bet A story; starting XL EBR-180 without appetite; iPad tickets; dedicated EBR-87 build.  
- **Done:** Territory filter on Sales Portal invoice list + dashboard (when enabled) correct on **wwjc**; Customers selected-range + export share one period; “sales” = invoiced `net_amount`.  
- **Pitch / brief:** `cycle-03-outputs/PITCH-phase1-filter-metric-law.md` · `CEO-CTO-FRIDAY-SHARE.md` · `TRD-Bet-A-filter-truth.md`  
- **AC:** `cycle-03-outputs/FILTER-TRUTH-AC.md`  
- **Sprint / eng:** `SPRINT-PACK-bet-a.md` · `ENG-HANDOFF-bet-a-b-c-e.md`  
- **Post-CTO pack:** `CTO-FEEDBACK-2026-07-20.md` · `CTO-FEEDBACK-2026-07-24.md` · `BUG-VALIDATION-PACK.md` (filled) · `IA-PERSONA-TRACK.md` · `BET-TRIAGE-BOARD.md`

### Bet B — Design overlay wireframes (Lane 1) · Small batch (1–2 w shaping/prototype)
- **Problem:** Classic portal feels dated; stakeholders need something to react to before Rails.  
- **Elements:** HTML wireframes on `.kshell` / App kit; answer-first for **C1 True Topline + S1 (EBR-198) + team strip** (Q-R1 always; Q-18 or Q-01; not RS-01). Sarreid + opposite (cci/ufi).  
- **No-gos:** Implementing Phase-3 Rails without GO; catalog paint; talking to data; leading with named invoiced-rep revenue.  
- **Done:** Feedback session → updated AC for Bet C.  
- **Brief:** `cycle-03-outputs/UX-brief-c1-s1-team-strip.md`

### Bet C — Computational Intelligence Report surface v1 (Lane 2) · Big batch · under [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775)
- **Problem:** Owners/reps need computational heroes without Excel; Insightful already computes — portal doesn’t surface them.  
- **v1 scope (cycle-03 locked — F8/F9):**  
  1. **True Topline (C1)** — invoiced `net_amount`, 55/55, RTD + $5M.  
  2. **S1 quietly dying accounts (EBR-198)** — preferred second commerce hero; concentration (C3) optional with **"healthy diversification" degrade**.  
  3. **Team strip** — Q-R1 pulse (always) + Q-18 eCat leaderboard **or** Q-01 engagement fallback; conditional Mixpanel depth; **do not lead RS-01**.  
  4. Fill leakage noted as next hero, not v1.  
- **Grade AC on `cci` + `kll`** (Tier-0); **demo `sarreid` + `ufi`**.  
- **Rabbit holes:** warehouse ≠ Insightful truth — label spine; named rep→revenue Tier-2 only; RTD not `CURRENT_DATE`.  
- **No-gos:** EBR-772/776, peer benchmarks, margin, FULL completeness; "$0 returns" on gross-only.  
- **Done:** Spec + AC + prototype that reconciles to invoice math.  
- **Artifacts:** `cycle-03-outputs/INSIGHT-IR-v1-AC.md`, `IR-v1-QUERIES.md`, `TECHNICAL-PLAN.md`

### Bet D — (Parked) Agentic insights layer · EBR-772 + EBR-776 under EBR-775
- Explicit **no-go for current cycle**. See `cycle-03-outputs/PARK-llm-ebr-772-776.md`. Revive only after Bet C ships and feedback validates.

### Bet E — “Portal & Access” control plane (Lane 0→1) · Big batch (Wave 0–1 = small-batch down-payment) · **AC frozen 2026-07-18**
- **Problem (F10):** 134 toggles / 6 layers / 39 YAML flags, no admin surface — every non-trivial portal change is a SuperCat ticket, and access rules (SERV-2178's `territory_access_via_rep_number`) hide in deploy config.  
- **Elements:** delete **5 dead flags** → graduate ~23 stable flags to labeled settings → build a **6-section hub** (Enablement / Territory & data access / Portal display / Reports & export / **Revenue definitions [locked]** / Experiments) → move display toggles to client self-service → lock revenue definitions (SuperCat + INSIGHT).  
- **Win:** 134 toggles / 6 layers → ~30 survivors in 1 hub, ~18 client self-service, ~11 sunset-dated YAML.  
- **Ship-with:** `territory_access_via_rep_number` graduation ships alongside the Lane-0 SERV-2178 / Bet A fix (**Wave 4 — not alone**). Wave 0–1 **may ride with Bet A** if betting table says so. `pf` ($44.7M, clean, Tier 2) is a demo unlock — blocked only by `enable_sales_portal = false`.  
- **No-gos:** exposing revenue-definition settings to clients; deleting the 4 dormant-wired flags without a product ship/cut call; changing metric meaning without INSIGHT sign-off; applying anything while ISOLATION is on; implying filter truth is fixed when Bet A isn’t.  
- **Done = deployed hub:** a client org-admin can enable the portal, set territory/data access, and adjust display without a ticket; support answers "why can't this user see the portal?" from the in-product decision tree.  
- **AC:** `cycle-03-outputs/SETTINGS-hub-v1-AC.md` · **Ship gate:** `cycle-03-outputs/SHIP-READINESS-bet-e.md` · Demo: `SETTINGS-hub-v1-DEMO-SPEC.md`  
- **Open human gates:** betting table include E?; Confluence 1813676033 ~47 Org rows before Wave 2; dormant-wired ship/cut; `ISOLATION OFF — GO on Bet E`.

### Bet F — Persona-priority IA (Lane 1) · Small batch (docs SoT; optional HTML later) · **parallel to Bet A — does not unlock GO**
- **Problem (god-view / who sees what first):** the portal is one shared "god view" — one sidebar, one org switcher, every persona lands on the same Dashboard. A scoped rep picks a territory and still sees the whole org (F1), so they distrust the number and rebuild it in Excel; an owner genuinely wants the whole org; an admin/ops person just needs the portal on for the right people and the export to match the screen (F10). The fix is not one more filter — it is **whose defaults win on which surface** once Bet A makes the total trustworthy.
- **Appetite:** small batch — the deliverable is the **docs shape pack**, not code or a UI. Research is done and PASSED (Phase 1). Optional HTML illustration is Phase 4; a Phase 5 betting brief is stubbed.
- **Elements:** **3 personas** (Sales rep · CEO/Owner = Owner/VP portal seat · Admin/ops, permission tier; Manager folded under CEO/Owner) → `PERSONA-ONE-PAGERS.md`; a **persona × surface priority matrix** (must/nice/hide) that is the ordering law Bet B reads → `IA-PRIORITY-MATRIX.md`; **five fail-closed rules R1–R5** (assigned-book default · suppress named rep→revenue < Tier 2 · revenue definitions visible-but-locked · client vs SuperCat gates · STRONG-not-FULL) that inherit standing ACs (no new metric law); and **surface placement** (Portal / Insightful / Admin Console candidate) → `SURFACE-PLACEMENT.md`.
- **Recommendation:** **role-aware defaults over one shared surface** (hero-priority-per-surface, not a nav fork). Default homes are **HYPOTHESIS** pending customer A/B: rep → Customers · owner → Intelligence · ops → Settings hub → `IA-RECOMMENDATION-v0.md`.
- **No-gos:** no `ISOLATION OFF — GO` unlock on EBR-40 / Bet A / Bet E; no Dashboard redesign; no Admin Console rebuild or feature-usage build spec (placement candidate only); no nav fork / forked role-based product; no LLM; no new metrics / margin / RS-01 lead / FULL claim; no rewrite of `FILTER-TRUTH-AC` body or the Bet A TRD; no Friday-demo HTML edits.
- **Bet F informs, does not replace:** it reinforces Bet A's appetite (rep/ops trust failures as evidence), gives Bet B the surface ordering, and confirms Bet E as the ops home — **Bet A stays the only GO on the table**; validation (Track 1) unlocks GO, not this pack.
- **Phase 2 artifacts (`cycle-03-outputs/`):** `PITCH-bet-f-persona-ia.md` · `PERSONA-ONE-PAGERS.md` · `IA-PRIORITY-MATRIX.md` · `SURFACE-PLACEMENT.md` · `IA-RECOMMENDATION-v0.md` · Track doc: `IA-PERSONA-TRACK.md` (Phase 3 SoT wire complete).

> **Router note (F1/F7 + IA track):** Bet F operationalizes **F1** (rep trust breaks on the god-view) and **F7** (adoption is a GTM metric — the feature-usage/adoption report is an Admin Console *placement candidate*, no build) as a persona-priority IA layer, and is the shaped home of the Track-2 persona/IA work from `IA-PERSONA-TRACK.md`. No new finding letter needed — Bet F is the section that carries it.

---

## 6. Jira inventory (router) — EBR-primary

> **Cycle-03 (2026-07-17):** Program tracks **EBR only**. Full affinity = [`cycle-03-outputs/EBR-AFFINITY-PORTAL.md`](cycle-03-outputs/EBR-AFFINITY-PORTAL.md). SERV = Appendix A (downstream). Most EBR = `Triaging`.

### Epic
| Key | Summary | Status / note |
|---|---|---|
| [EBR-775](https://supercatsolutions.atlassian.net/browse/EBR-775) | Insightful Product analytics / reporting | Submitted — **umbrella**; computational first |

### Lane 0 — Structural (Sales Portal)

| Key | Summary | Status / note |
|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | Territory filter not working on invoice list | Triaging — **Bet A in** |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | Territory filter on sales portal dashboard | In Progress **since 2022** — stalled; **Bet A in** |
| [EBR-180](https://supercatsolutions.atlassian.net/browse/EBR-180) | RepNumber multiple territory codes | Triaging — **XL shelf**; eng → SERV-2178/2180 |
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | Export ≠ displayed totals | Triaging — reconciliation AC |
| [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87) | Exclude quotes from portal totals | Triaging — **parked from Bet A GO** (2026-07-21) |
| [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) | Sales totals should reflect discounts | Triaging — **close via `net_amount` doctrine** |

### Lane 1 — UX / wireframe feedback

| Key | Summary | Status / note |
|---|---|---|
| [EBR-687](https://supercatsolutions.atlassian.net/browse/EBR-687) | Drill-down on portal dashboard | Submitted — IR UX pattern |

### Lane 2 — Computational (shape before build)

| Key | Summary | Status / note |
|---|---|---|
| [EBR-198](https://supercatsolutions.atlassian.net/browse/EBR-198) | Hot/cold **customers** | Triaging — **= S1 v1 hero** |
| [EBR-197](https://supercatsolutions.atlassian.net/browse/EBR-197) | Hot/cold **items** | Triaging — post-v1 |
| [EBR-278](https://supercatsolutions.atlassian.net/browse/EBR-278) | Territory view – analytics | Triaging — seed; data-gated |
| [EBR-213](https://supercatsolutions.atlassian.net/browse/EBR-213) | Quota/budget (Sarreid) | In Progress — one-org only |
| [EBR-629](https://supercatsolutions.atlassian.net/browse/EBR-629) | Trade Name filter | Triaging — defer |

**Deferred cluster (not v1):** EBR-38, 110, 279, 325, 471, 474≈601, 699, 745, 756 — see affinity.

### Lane 3 — LLM (PARKED)

| Key | Summary | Status / note |
|---|---|---|
| [EBR-772](https://supercatsolutions.atlassian.net/browse/EBR-772) | LLM agentic insights for Sales Portal | Submitted — **PARK** |
| [EBR-776](https://supercatsolutions.atlassian.net/browse/EBR-776) | LLM rep reporting / activity summaries | Submitted — **PARK** (sibling of 772) |

### Out of program (do not route here)

EBR-36, EBR-655 (iPad / order-email) · EBR-743 (iPad analytics) · EBR-329 (invoice email) · EBR-527 (eCat→portal push) · EBR-503, EBR-524 (search / custom tab). Hygiene comments in `cycle-03-outputs/JIRA-HYGIENE-COMMENTS.md`.

### Appendix A — Downstream eng (SERV — out of betting table)

Implement only after `ISOLATION OFF — GO on …`. Not program work items.

| SERV | Relates to EBR / note |
|---|---|
| SERV-2178 / 2180 | EBR-180 XL — comma / many-many territory |
| SERV-2196 / 2214 | Territory access / empty master — demo trust |
| SERV-2337 | Rails reface — optional after Bet B feedback |
| SERV-2382 / 2388 / 1587 | Absorb into IR heroes when shaped |
| SERV-2254 | Bet E self-service anchor |
| SERV-2421 / 2336 | Parallel Mixpanel adoption — de-conflict, not Lane 2 IR |
| SERV-2395 / 278 | iPad / eOL date-filter — **out of this Sales Portal EBR plan** |

---

## 7. Artifact map by lane

### Eng entrypoint (all bets — the implementation SoT)
- **`cycle-03-outputs/ENG-HANDOFF-bet-a-b-c-e.md`** — single CTO/eng-ready spec for **Bet A + Bet B shell + Bet C IR v1 + Bet E**. Sections A–H (scope/GO, metric law, per-bet mapping, IR JSON read-model, test plan, PR batches). Cites the ACs below; build gated on per-bet `ISOLATION OFF — GO on …`. `TECHNICAL-PLAN.md` is the shaping companion and points here.

### Doctrine (all lanes)
- `PM/sales-portal-agent-starters/00a-DOCTRINE-shapeup-ddd-affinity.md`
- `PM/sales-portal-agent-starters/00b-PRODUCT-HANDOFF-analytics.md`

### Lane 0
- `cycle-03-outputs/PITCH-phase1-filter-metric-law.md`  
- **`cycle-03-outputs/FILTER-TRUTH-AC.md`** — EBR-40/212/91/87 done criteria  
- **`cycle-03-outputs/CTO-FEEDBACK-2026-07-20.md`** — leadership feedback → validation-before-GO  
- **`cycle-03-outputs/BUG-VALIDATION-PACK.md`** — live repro + keep/narrow/park  
- **`cycle-03-outputs/IA-PERSONA-TRACK.md`** — Track 2 persona/IA (not Bet A GO)  
- **`cycle-03-outputs/SETTINGS-hub-v1-AC.md`** — Bet E Portal & Access (E0–E6)  
- **`cycle-03-outputs/SHIP-READINESS-bet-e.md`** — Bet E GO gate  
- `cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md` — triage (consume)  
- EBR-40, EBR-212, EBR-91 (EBR-87 parked · EBR-180 shelf) · SERV-2254 / 2395 (eng footnotes)  

### Lane 1
- `design-system/START-HERE.md`, `docs/SURFACES.md`, `ds/tokens/`  
- **`design-system/app/sales-portal-internal-demo.html`** — Dashboard default; answer-first list tabs; What’s broken last  
- **`cycle-03-outputs/DEMO-SURFACE-CONTRACT.md`** — demo→Rails shell contract for tech spec  
- **`cycle-03-outputs/LIST-TABS-AC.md`** — Given/When/Then for Customers/Orders/Invoices/Reports (Bet A+B)  
- `cycle-03-outputs/UX-brief-c1-s1-team-strip.md`  
- EBR-687  

### Lane 2
- `Insightful Product 4.0/CANON.md`  
- `foundation/provenance_spine.md`, `provenance_map_rep.md`, `WHAT_ACTUALLY_RUNS.md`, `query_library_v2.md`  
- `cycle-02-outputs/PORTAL-CAPABILITY-MAP.md`  
- `cycle-03-outputs/INSIGHT-IR-v1-AC.md`, **`IR-v1-QUERIES.md`**, `TECHNICAL-PLAN.md`, `SHIP-READINESS-bet-c.md`  
- EBR-775 · EBR-198  

### Program / affinity
- `cycle-03-outputs/EBR-AFFINITY-PORTAL.md`  
- `cycle-03-outputs/JIRA-HYGIENE-COMMENTS.md`  
- `cycle-03-outputs/PARK-llm-ebr-772-776.md`  
- `05d-ORCHESTRATOR-REBOOT-cycle03.md` — **paste to boot fresh Orchestrator**  
- `EBR 2.0/Frameworks & Templates/Metrics_Framework_QBR_EBR_Full_Surface_Area_v5.md`  
- Jira project **EBR** only for this program

---

## 8. How to run agents (elite)

See `README-RUN-ORDER.md` for the full diagram.

| Chat file | Mode | Open with |
|---|---|---|
| `05-ORCHESTRATOR.md` | Plan (Opus 4.8) | **First** — stays open; reviews + routes |
| `01-PROGRAM.md` | Plan | Shape / re-affinity / betting table |
| `02-FIX.md` | Agent | One Jira ticket at a time (diagnose only while isolated) |
| `03-UX.md` | Agent | Wireframes / overlay / feedback AC |
| `04-INSIGHT.md` | Agent | Computational report surface + specs |

**Rule:** Mission blurb (in starter) + only listed `@` files. Paste lane outputs back into Orchestrator for Review Cards.

**Your job as PM:** pick Bet A/B/C order this cycle; run feedback on UX; say GO before Rails (`ISOLATION OFF — GO on …`).

---

## 9. Elite order (cycle-03 locked)

1. **Affinity + spine cleanup** — `EBR-AFFINITY-PORTAL.md` (done)  
2. **Bet A AC** — `FILTER-TRUTH-AC.md` (done) · Trust/Fix in internal demo  
3. **IR v1 AC + stamped queries** — `INSIGHT-IR-v1-AC.md` + `IR-v1-QUERIES.md` (done)  
4. **Bet E AC + ship-readiness** — `SETTINGS-hub-v1-AC.md` + `SHIP-READINESS-bet-e.md` (done)  
5. **Betting table** — confirm A then C; **decide include E** (Wave 0–1 may ride with A)  
6. **Combined tech-spec / eng-handoff** — `ENG-HANDOFF-bet-a-b-c-e.md` (A+B+C+E cite AC packs) — **done 2026-07-18**  
7. **Computational / filter / control-plane ship** — `ISOLATION OFF — GO on …`  
8. **Park** EBR-772 / EBR-776 (done)  
9. Optional customer feedback anytime — does not block internal AC  

Fresh Orchestrator boot: paste `05d-ORCHESTRATOR-REBOOT-cycle03.md`.

WIP: structural + modern UX → computational → inferential.  
Process: Stories → features → specs/AC → prototype → feedback → update AC → build → staging → verify → prod → document/promote.

---

*Spine generated 2026-07-16; cycle-03 EBR-only rescope 2026-07-17; Bet E AC freeze 2026-07-18; Bet F persona-priority IA wired 2026-07-24 (parallel to Bet A, does not unlock GO).*
