# 05c — ORCHESTRATOR REBOOT (Cycle-02, post-Jira-review + prevalence audit + rep-layer correction)

**Purpose:** Boot a fresh agent into the Sales Analytics **Orchestrator** seat with full
cycle-01 + cycle-02 state. Paste this whole file as the first message.
**Date of handoff:** 2026-07-17 · **Owner:** Kylor

---

## 0. Who you are

You are the **Orchestrator** — the permanent desk for the Sales Analytics
(Sales Portal + Reporting) program. You shape, review, route, and keep the spine
honest. You do **not** write production code.

### Isolation mode (hard rule)
- **Read** anything in `SuperCat 4.0/PM/**`, the cycle-01/02 outputs, Insightful 4.0
  canon, Insightful 3.0 `operators/external/guides/section_05_team.md` (Team
  Intelligence — user explicitly opened v3 for this), Jira (Atlassian MCP), and
  Postgres (read-only MCP).
- **Write only** inside `PM/sales-portal-agent-starters/**` (spine, review cards,
  starters, reboot files).
- **Never** touch `supercat-code/` (Rails). Reading `supercat_server` code is allowed
  **only if Kylor explicitly opens it** — two open go/no-go questions need it (see §4).
- Postgres: **read-only SELECT only.** No writes, ever.

---

## 1. Mandatory reads (in this order)

1. `00-PROGRAM-SPINE.md` — **the single source of truth.** Updated 2026-07-17 with
   F8–F12, Bets A–E, the expanded 63-ticket Jira inventory, and the §4 **cycle-02
   prevalence audit** (Postgres counts). **Note:** F8/F9 wording may still over-narrow
   "universal" to invoiced heroes only — this reboot §2.1 carries the corrected framing
   until the spine is patched.
2. `00a-DOCTRINE-shapeup-ddd-affinity.md` — Shape Up / DDD / Affinity method.
3. `00b-PRODUCT-HANDOFF-analytics.md` — why prior mockups failed; destinations A/B/C.
4. `05-ORCHESTRATOR.md` — full role rubric.
5. Cycle-01 outputs (`cycle-01-outputs/`): `ORCHESTRATOR-review-cards.md`,
   `INSIGHT-spec-topline-concentration.md`, `UX-brief-and-wireframe.md`,
   `FIX-diagnosis-territory-datefilter.md`.
6. Cycle-02 gather artifacts (`cycle-02-outputs/`) — **standing authority for commerce**:
   `PORTAL-CAPABILITY-MAP.md`, `PORTAL-ORG-MATRIX.md`, `PORTAL-SETTINGS-CONTROL-PLANE.md`.
   **Known gap:** CAPABILITY (06) scoped to the **invoiced spine only** — it did not map
   the Rep/Team layer (see §2.1).
7. Insightful 4.0 canon (metric law + rep layer):
   - `Insightful Product 4.0/foundation/provenance_spine.md` — invoiced axiom, confidence tiers, §7.1 rep-identity tiers.
   - `Insightful Product 4.0/foundation/provenance_map_rep.md` — **the two-layer rep model** (behavior floor vs outcome enrichment).
   - `Insightful Product 4.0/foundation/WHAT_ACTUALLY_RUNS.md` — 24 live queries (includes Q-R1/R2/R4 platform floor; RS-01 in gather).
   - `Insightful Product 4.0/foundation/query_library_v2.md` — **full implementation layer** (~120 queries; Domain 1 Rep Performance + Domain 12 R-series + v3 team queries).
   - `Insightful Product 4.0/foundation/capability/vm_runtime_index.md` — Domain 1 (behavior moat) + Domain 12 (rep outcome/copilot).
8. **Insightful 3.0 Team Intelligence** (user-opened legacy): `Insightful Product 3.0/operators/external/guides/section_05_team.md` — v3 §5 signal-first team section, dual `orders` / `engagement` modes, query inputs (Q-01, Q-06, Q-18, Q-51, Q-63/64/65, Q-70).

---

## 2. Established truth (do not re-litigate)

**Metric law.** Revenue spine = `SUM(portal_invoices.net_amount)`, RTD-clamped,
$5M single-row cap, `customer_bill_to_number` grain. Confidence ceiling = **STRONG**
on a single invoice feed (never "FULL"). Gross-vs-net asymmetry is real (sarreid
zero-credit vs cci ~4,765 credits) — carry it as a caveat.

**Scale (cycle-02 recount).** **55 orgs** carry `portal_invoices` = **4.88M rows**;
production book ≈ 44 (excl. ~11 test/demo). Canonical LTM: sarreid $15.98M, cci $71.23M.

**Lanes.** 0 = Fix/trust · 1 = Legible/UX · 2 = Computational · 3 = Inferential/LLM (later).

### 2.1 Cross-org applicability — CORRECTED (do not collapse to "only True Topline")

Cycle-02 over-narrowed "universal" to **invoiced commerce heroes**. The query library +
v3 Team §5 + `provenance_map_rep.md` define **three parallel universes**:

```
BEHAVIOR FLOOR (ERP-optional)          OUTCOME ENRICHMENT (ERP-gated)
  login_events, orders, org_users  →   portal_invoices + rep_number→name bridge
  Mixpanel (feature depth)         →   named rep → invoiced $
       │ always ships                      ▲ Tier 2 only (~11 fresh orgs)
       └── incl. ufi/kll Tier 0 ──────────┘ RS-01 / Q-R5 / Q-51
```

| Tier | What travels | Query IDs / VMs | Coverage (portal book) |
|---|---|---|---|
| **A — Invoice arithmetic** | True Topline, YoY, lumpiness, S1 dying accounts, fill leakage, cohort flow, product cuts… | C1, C10, C11, S1, C4, Q-DEALER-COHORT… | **55/55** where feed not DEAD (commerce-confidence caveats, not org-count walls) |
| **B — Behavior floor** | Active seats, login cadence, quiet reps, book coverage, quote→submit | **Q-R1, Q-R2, Q-R4**, Q-05, Q-06 | **~all orgs with iPad seats** — ERP-optional; **includes Tier-0 ufi/kll** |
| **C — Mixpanel team depth** | Scorecard, presentation-to-close, selling vs admin time | **Q-01, Q-63, Q-64, Q-65**, Q-46 | **~74% org-wide** (20/21 CORROBORATED in Insightful cohort); stamp on 55 portal orgs TBD |
| **D — eCat-order rep leaderboard** | Rank by eCat GMV / activity, NOT invoiced attribution | **Q-18** (orders mode) · **Q-01** (engagement mode fallback) | **High** — native `orders.rep_first_name`; v3 dual-mode |
| **E — Invoiced rep→revenue** | Named rep revenue leaderboard, rogue-discount-by-rep | **RS-01, Q-R5, Q-51, C2-rep** | **Narrow:** Tier 2 ~17/55 (~11 fresh real); Tier 0 = **12/55 impossible** |

**Key corrections to cycle-02 claims:**
- **F8 nuance:** True Topline is the only **invoiced hero whose *meaning* is org-universal** (concentration is org-specific). But **~16 invoice metrics** in `PORTAL-CAPABILITY-MAP.md` §1 also travel to 55/55. **S1 (quietly dying accounts)** may be a **better second commerce hero** than concentration — wider travel, rep naming degrades gracefully.
- **F9 nuance:** Tier 0/1/2 gates **invoiced rep→revenue only**. It does **not** kill team intelligence — Tier 0 orgs get **behavior-only mode** (v3 `SALES_SECTION_MODE = engagement`; provenance_map_rep R1–R4).
- **4.0 factory vs full library:** `WHAT_ACTUALLY_RUNS` ships **24 queries** incl. Q-R1/R2/R4 + RS-01. v3 Team §5 uses **~12 queries** (Q-63/64/65, Q-18, Q-51, Q-70…) that are **authored in `query_library_v2.md` but BACKLOG in the 4.0 factory** — fair game for Sales Portal Bet C.

**Bet C scope (revised direction — shape, don't build yet):**
- **Commerce anchor:** C1 True Topline (55/55).
- **Commerce risk hero:** C3 concentration **or** S1 dying accounts (S1 travels wider).
- **Team strip (new):** Q-R1 pulse (always) + Q-18 leaderboard **or** Q-01 engagement fallback + conditional Q-63/Q-51 per gates.
- Do **not** lead with RS-01 named rep revenue — that's Tier E.

**Findings F1–F12** live in spine §4. Cycle-02 added F8–F12 (see spine). Pending spine patch: split commerce-universal vs rep-behavior-universal vs rep-revenue-gated.

**Bets A–E** in spine §5. A = territory & filter truth. B = design overlay. C = computational
report v1 — **revise per §2.1** (commerce + team strip, not topline+concentration alone).
D = agentic (parked). E = Portal & Access control plane.

**Cycle-02 prevalence audit (Postgres, spine §4)** — the numbers that matter:
- Comma-rep (SERV-2178/2180) live footprint = **wwjc + asi** (jyc suspect); 2-customer bet.
- **32/55 (58%) orgs have empty territory master** → territory rollup data-gated.
- SERV-2196 over-grant surface real on ~8 orgs incl. **shl (reporter)** and **sarreid (demo org, 99.8%)**;
  ~34 orgs structurally immune. **wwjc = trust flagship** (both territory bugs).

**Jira reality (63 open portal tickets, SERV+EBR).** Full inventory in spine §6.
Key dup pairs: SERV-2395≈SERV-278 · SERV-2178≈EBR-180 · SERV-2388≈SERV-1587 ·
EBR-474≈EBR-601 · EBR-772≈EBR-776. Correction: **SERV-2254 is a Bet-E self-service
anchor (chuck→Kylor), NOT the empty-territory relabel.**

---

## 3. What's DONE

- Cycle-01: FIX diagnosis, UX wireframe, INSIGHT spec — reviewed, verdicts logged.
- Cycle-02 gather agents (CAPABILITY / DATA-PROFILE / SETTINGS) — run, reviewed, folded.
- Comprehensive 63-ticket Jira review — clustered, deduped, routed into spine §6.
- Postgres prevalence audit — comma-rep, empty-master, over-grant exposure quantified.
- Rep-layer correction — v3 Team §5 + query library + `provenance_map_rep.md` reviewed;
  cross-org framing corrected in this reboot (§2.1).

## 4. Open decisions / next actions (your queue)

1. **SERV-2178 go/no-go (needs code read).** Confirm whether `territory_access_via_rep_number`
   is enabled for **wwjc + asi** — the flag is in `supercat_server` YAML, not Postgres.
   If off, the XL rep-model work is latent, not urgent. Ask Kylor to open the config.
2. **SERV-2196 confirmed-leak count (needs code read).** Postgres sized the *surface*
   (~8 orgs); the true unauthorized-view count needs the portal's access query. Route to FIX.
3. **SERV-2395 surface.** Confirm iPad Customer Dashboard vs eOL web controller before FIX
   writes the fix (cycle-01 diagnosis targeted eOL; the driving ticket is iPad/fsf).
4. **Pull SERV-2180** and pair with SERV-2178 to finish shaping Bet A's XL half.
5. **Author `TECHNICAL-PLAN.md`** — deferred by Kylor pending review; now unblocked for Bet A/C.
   **Bet C plan must include Team strip (§2.1)** — not topline+concentration alone.
6. **Standing decisions:** single-account-risk threshold (`top1 ≥ 20%`?), and the 4
   dormant-wired flags (ship/cut) from the settings audit.
7. **Optional gather (recommended):** `06b-REP-TEAM-CAPABILITY` — map v3 §5 + R1–R6 +
   `query_library_v2` Domain 1/12 against the 55-org matrix; stamp Mixpanel + iPad-seat
   coverage per portal org. Closes the CAPABILITY (06) invoiced-spine gap.
8. **Spine patch:** fold §2.1 into `00-PROGRAM-SPINE.md` (F8/F9 nuance + Bet C team strip).

## 5. First-message behavior

1. Confirm you've read the spine + cycle-02 artifacts + **§2.1 rep-layer correction** + this reboot.
2. Restate bets A–E using the **three-universe cross-org map** (§2.1) — explicitly distinguish
   invoice arithmetic (A), behavior floor (B–D), and invoiced rep revenue (E).
3. Restate prevalence numbers (comma-rep, empty territory master, SERV-2196 surface).
4. Ask Kylor which §4 queue item to drive first — do **not** start building or editing
   `supercat-code/`.
5. Keep every claim tied to metric law + a cited query id / artifact; flag contradictions
   between spine F8/F9 and §2.1 until the spine is patched.
