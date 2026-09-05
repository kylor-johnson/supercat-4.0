# Program roadmap — Sales Analytics (Cycle 03)

**Shaped program — Cycle 03 · Not a single GO document**

**Status:** `Bet A GO 2026-07-24 · ISOLATION OFF — GO on EBR-40 · Other bets still shaped / triage only`
**Owner:** Kylor · **Date:** 2026-07-20 · **Updated:** 2026-07-24

> **Bet A is in sprint.** CTO go-ahead: ready for EBR→SERV (`CTO-FEEDBACK-2026-07-24.md`). Everything else below stays shaped and sequenced after Bet A unless a separate GO lands. Sprint pack: `SPRINT-PACK-bet-a.md`. Triage: `BET-TRIAGE-BOARD.md`.

---

## 1. Program thesis

One program, one order of operations: **trust first, then modern UX, then computational intelligence, then inferential later.** Reps won't act on a number they can't trust, so the first job is making a filtered total mean the same thing on screen, in the export, and in the report (Bet A). Once the total is trustworthy, the portal gets answer-first surfaces so the answer is the first thing on the page, not buried in a grid (Bet B). On top of that spine, the portal surfaces the computational intelligence the market keeps asking for — deterministic first, reconciling to the invoiced ledger, not an LLM guess (Bet C). Only after that surface is trusted do we consider talk-to-data (Bet D, parked). Running underneath is the control plane that lets clients self-serve portal settings instead of filing a ticket (Bet E).

The discipline that keeps this honest: **structural fixes & modern UX → computational insights → inferential / talk-to-data.** We don't skip a rung.

## 2. Architecture spine

One spine, two presentations — the portal and the existing intelligence factory read the same invoiced ledger:

```
ERP invoice_data / order_data
        │ ACL
        ▼
portal_invoices.net_amount  ←── Insightful query library (C1, S1, economic preflight)
login_events / orders / Mixpanel ←── team-pulse + leaderboard queries
        │
        ├── Sales Portal Intelligence surface (Bet C UI)
        └── Insightful CEO report (existing factory)
```

The warehouse dashboard rollup is **not** the validation ground truth — it's labeled "invoiced ledger." The team strip is ERP-optional; the dollar answers require the invoice feed.

## 3. Bet map

| Bet | What it is | Lane | Sequence | GO phrase | Artifacts |
|---|---|---|---|---|---|
| **A** | Filter truth — territory limits the total, export matches the screen, quotes ≠ sales | 0 Trust/Fix | **First (this GO)** | `ISOLATION OFF — GO on EBR-40` | `TRD-Bet-A-filter-truth.md`, `FILTER-TRUTH-AC.md`, `PITCH-phase1-filter-metric-law.md` |
| **B** | Answer-first list tabs (Invoices/Customers/Orders/Reports) | 1 Legible/UX | **Rides with A** (proof surfaces, not stubs) | with A | `LIST-TABS-AC.md`, `DEMO-SURFACE-CONTRACT.md` |
| **C** | Computational Intelligence Report v1 (invoiced sales + accounts fading + team strip) | 2 Computational | **After A** | `ISOLATION OFF — GO on EBR-775` | `INSIGHT-IR-v1-AC.md`, `IR-v1-QUERIES.md`, `SHIP-READINESS-bet-c.md` |
| **D** | LLM / talk-to-data | 3 Later | **Parked** | none | `PARK-llm-ebr-772-776.md` |
| **E** | Portal & Access control plane (settings hub) | 0→1 | **Shaped; Wave 0–1 may ride with A** | `ISOLATION OFF — GO on Bet E` (or Wave 0) | `SETTINGS-hub-v1-AC.md`, `SHIP-READINESS-bet-e.md`, `PORTAL-SETTINGS-CONTROL-PLANE.md` |
| **F** | Persona-priority IA — role-aware defaults over one shared surface (who sees what first) | 1 Legible/UX | **Parallel research→shaped** (not a build GO; informs B ordering + E ops home) | none — does not unlock GO | `IA-RECOMMENDATION-v0.md`, `IA-PRIORITY-MATRIX.md`, `PERSONA-ONE-PAGERS.md`, `SURFACE-PLACEMENT.md`, `PITCH-bet-f-persona-ia.md` |

## 4. Bet C — shaped summary (after Bet A)

Bet C surfaces the computational reporting under EBR-775 — deterministic answers off the invoiced ledger, not an inference layer. The portal can honestly surface ~16 deterministic answers now plus ~13 more that are real but gated per-org; v1 picks the three that travel widest and matter most:

- **C1 — invoiced sales (ledger total).** The one number that reconciles to the dollar: trailing-12-month invoiced net, report-through-date clamped, at a STRONG single-feed ceiling. Live reference: ~$16.0M on sarreid, ~$71.23M on cci.
- **S1 — accounts fading (EBR-198).** Accounts down materially versus the prior six months (equal 6-vs-prior-6 windows, so an accelerating account doesn't get false-flagged); the dollar shown is the trailing-12-month invoiced still on the account, and who-to-call is the rep. Live reference: 25 flagged accounts on sarreid.
- **Team strip.** Seats and login cadence always; an eCat GMV leaderboard where orders exist, otherwise an engagement fallback. No named rep→revenue leaderboard in the v1 default.

Concentration is optional and org-specific — where one account is under ~20% of invoiced sales it degrades to "spread across accounts" rather than a warning. **Ship gate:** AC is graded on cci + kll (a re-stamp is required before build) and demoed on sarreid + ufi; details in `SHIP-READINESS-bet-c.md`. Bet C does not build until Bet A's spine is trustworthy — those answers reconcile to the filtered total.

## 5. Bet E — control plane (condensed)

Portal behavior hides in **134 settings across 6 layers (39 YAML flags), with no admin screen.** Every non-trivial portal change is a SuperCat ticket, and some access rules — like `territory_access_via_rep_number`, the flag behind one org's territory behavior — live in deploy config where no client or support person can see them. Bet E collapses that into one **Portal & Access hub** so clients self-serve and support can answer "why can't this user see the portal?" from an in-product decision tree.

Six sections:

| Section | Who edits | What lands here |
|---|---|---|
| Enablement | Client admin | The whole "can this user see the portal?" chain in one place |
| Territory & data access | SuperCat (match mode) · client (synch/totals) | Where the territory access rule gets fixed structurally |
| Portal display | Client self-service | Currency, quantity columns, customer graph, backlog label |
| Reports & export | Client admin | The 3–4 overlapping export toggles unified into one |
| Revenue definitions 🔒 | SuperCat + INSIGHT only | Metric-law settings, visible but locked |
| Experiments | SuperCat superadmin | Canary flags with owner + ticket + sunset date |

**Waves 0–5:** Wave 0 deletes 5 dead flag entries (zero code reads — safe); Wave 1 graduates named stable flags to labeled settings; Waves 2–3 build the hub UI (enablement tree, then territory & data access, then display self-service); **Wave 4 (territory match mode) must pair with Bet A / SERV-2178 — never ships alone**; Wave 5 stands up the locked revenue-definitions section behind INSIGHT sign-off. **Wave 0–1 is the small-batch down-payment that may ride with Bet A if the betting table says so.** The win: 134 settings / 6 layers → ~1 hub with ~30 survivors, ~18 client self-service, 5 deleted, ~11 sunset-dated experiments. Full inventory and receipts: `PORTAL-SETTINGS-CONTROL-PLANE.md`; build AC: `SETTINGS-hub-v1-AC.md`.

## 5b. Bet F — persona-priority IA (parallel, shaped, no GO)

Bet F answers **who sees what first** in the portal. Today it is one shared "god view" — one sidebar, every persona lands on the same Dashboard — so a scoped rep picks a territory, still sees the whole org, distrusts the number and rebuilds it in Excel (F1); an owner genuinely wants the whole org; and an admin/ops person just needs the portal on for the right people and the export to match the screen (F10). The shaped recommendation is **role-aware defaults over one shared surface** (hero-priority-per-surface, not a nav fork): the portal keeps its seven surfaces and one nav, and Bet F adds a recommended default home plus a hero-priority order per persona, governed by five fail-closed rules.

- **Three personas (locked):** Sales rep · CEO/Owner (portal seat = Owner/VP Sales; the deep CEO factory stays Insightful) · Admin/ops (one persona, permission tier: client org-admin vs SuperCat). Manager folds under CEO/Owner for v0.
- **Priority matrix** — must/nice/hide per persona per surface — is the ordering law Bet B reads for each surface's lead answer (`IA-PRIORITY-MATRIX.md`).
- **Five fail-closed rules R1–R5** (assigned-book default · suppress named rep→revenue below Tier 2 · revenue definitions visible-but-locked · client vs SuperCat gates · STRONG-not-FULL) each inherit a standing AC — **no new metric law, no new Bet A AC**.
- **Placement frozen:** Portal = transactional + a thin Intelligence subset; Insightful = deep CEO factory; Admin Console = config (Bet E) + an adoption/feature-usage report as a *placement candidate only — no build spec*.

**Sequencing posture:** Bet F is **parallel research→shaped**, not a sequenced build GO. It reinforces Bet A's appetite, **informs Bet B's surface ordering and confirms Bet E as the ops home**, and does **not** replace "Bet A first." It does **not** unlock `ISOLATION OFF — GO`; Bet A validation (Track 1) does. Default homes (rep → Customers · owner → Intelligence · ops → Settings hub) are **HYPOTHESIS pending customer A/B**. Betting-table read-in-5: `IA-RECOMMENDATION-v0.md`.

## 6. Affinity F1–F12

The mechanism-named themes behind the bets (from spine §4):

| # | Theme (mechanism) | Lane |
|---|---|---|
| F1 | Reps treat the portal as the KPI shelf — trust breaks when territory filters lie | 0 |
| F2 | Customers say "most metrics are in the portal" — the ask is surface + execute, not a new warehouse | 1→2 |
| F3 | Manual Excel + Claude + Power BI work is the spec — automate the computational truth first | 2 |
| F4 | Modern UX demand — the App kit is the overlay language for wireframes + feedback | 1 |
| F5 | The feature pile is a grab-bag unless shaped against named report answers | 2 |
| F6 | LLM / NL query is wanted but explicitly downstream of the computational foundation | 3 / no-go now |
| F7 | "No portal usage" is scored in decks — adoption is a GTM metric, not just UI | Program |
| F8 | Commerce-universal ≠ only the invoiced total — invoiced arithmetic travels 55/55; concentration is org-specific | 2 |
| F9 | Three data universes — don't collapse; tier gates kill rep→revenue only, not team intelligence | 2 |
| F10 | Portal behavior hides in 134 toggles / 6 layers / 39 YAML flags with no admin surface | 0→1 |
| F11 | Territory filter truth is a multi-year EBR sprawl (EBR-40 + 212 stalled since 2022) | 0 |
| F12 | Metric/totals-truth EBRs are old and open (EBR-91 reconcile, EBR-87 quote exclusion, EBR-7 close) | 0/2/3 |

## 7. EBR inventory (router)

| Lane | Keys | Note |
|---|---|---|
| **0 — Structural** | EBR-40, EBR-212, EBR-91, EBR-87 | Bet A in-scope. EBR-7 = close via invoiced-net doctrine. EBR-180 = XL shelf. |
| **1 — UX** | EBR-687 | Drill-down = the report UX pattern, later. |
| **2 — Computational** | EBR-775 (epic), EBR-198 | EBR-198 = the accounts-fading answer (S1). |
| **3 — LLM (parked)** | EBR-772, EBR-776 | Parked behind the computational surface. |

Deferred cluster (not v1, one line): EBR-38, 110, 197, 213, 278, 279, 325, 471, 474≈601, 629, 699, 745, 756 — see `EBR-AFFINITY-PORTAL.md`. SERV tickets are downstream eng footnotes (SERV-2178/2180 = EBR-180 XL; SERV-2196/2214 = territory access/empty master; SERV-2254 = Bet E anchor), not betting-table work.

## 8. Demo strategy for Friday

Open the **Bet A pitch demo first** (`../../../design-system/app/sales-portal-bet-a-pitch-demo.html`): Invoices → Customers → Orders → What's broken. It proves the one thing that matters — territory limits the total, export matches the screen, quotes aren't sales. Only if Bet A lands, walk the **full internal demo** (`../../../design-system/app/sales-portal-internal-demo.html`) for a preview of the intelligence view; skip the settings hub unless asked. Both mocks were rewritten to manufacturer/rep language per `COPY-AUDIT-portal-mocks.md` — the list is "the list," the big number is the "invoiced total," fading accounts are "accounts fading" — so what the room reads on screen matches how a sales-ops person actually talks.

## 9. Human gates still open

From `SPEC-GAP-CHECKLIST.md`:

- **G4 — betting table:** confirm A then C; decide whether to include Bet E, and whether Wave 0–1 rides with A this cycle.
- **C4 — grade-org re-stamp:** re-stamp the Bet C answers on cci + kll before that build.
- **E5–E7:** finalize the ~47 deferred Org settings rows (Confluence, before the hub wave, none metric-critical); make the ship/cut call on the 4 dormant-wired flags; confirm Bet E is in the betting table.
- **Isolation lift:** Kylor writes the verbatim `ISOLATION OFF — GO on …` phrase; AC freeze is not isolation lift.

## 10. Suggested sequencing (after Bet A GO)

1. **Bet A** trust core + answer-first list tabs (Bet B rides along) — the fix and its proof surfaces.
2. **Bet E Wave 0–1** *optional this cycle* — delete dead flags + graduate stable settings, if the betting table says ride with A.
3. **Bet C** — re-stamp on cci + kll, then the intelligence surface (invoiced sales + accounts fading + team strip), then the Customers→fading deep link.
4. **Bet E Waves 2–3** — the hub UI (enablement tree, territory & data access, display self-service).
5. **Bet E Wave 4** — territory match mode, only in a cycle with a confirmed Bet A path.
6. **Bet E Wave 5** — locked revenue definitions, after INSIGHT sign-off.
7. **Bet D** — revisit only after Bet C ships and feedback validates.

## 11. Annex index

| File | Role |
|---|---|
| `TRD-Bet-A-filter-truth.md` | **Current decision artifact** — the one GO on the table Friday |
| `CTO-PREREAD-friday-show-and-tell.md` | 3-minute pre-read for the meeting |
| `00-PROGRAM-SPINE.md` | Program router — lanes, bets, F1–F12, prevalence stats |
| `PITCH-phase1-filter-metric-law.md` | Bet A pitch / appetite |
| `FILTER-TRUTH-AC.md` | Bet A acceptance criteria (AC-A1…A4) |
| `LIST-TABS-AC.md` | Bet B answer-first list tabs (Given/When/Then) |
| `ENG-HANDOFF-bet-a-b-c-e.md` | Single eng entrypoint — build spec for A+B+C+E (after GO) |
| `TECHNICAL-PLAN.md` | Architecture/shaping companion |
| `INSIGHT-IR-v1-AC.md` + `IR-v1-QUERIES.md` | Bet C answers + stamped queries |
| `SHIP-READINESS-bet-c.md` | Bet C ship gate |
| `PORTAL-CAPABILITY-MAP.md` | What the portal can/can't honestly claim (CTO one-screen) |
| `PORTAL-SETTINGS-CONTROL-PLANE.md` | Bet E full 134-toggle triage + migration |
| `SETTINGS-hub-v1-AC.md` + `SHIP-READINESS-bet-e.md` | Bet E build AC + ship gate |
| `PARK-llm-ebr-772-776.md` | Bet D park |
| `IA-RECOMMENDATION-v0.md` | **Bet F** betting-table memo (read-in-5) — role-aware defaults, default homes, 5 rules |
| `IA-PRIORITY-MATRIX.md` + `PERSONA-ONE-PAGERS.md` + `SURFACE-PLACEMENT.md` | Bet F priority matrix + personas + placement |
| `PITCH-bet-f-persona-ia.md` / `IA-PERSONA-TRACK.md` | Bet F Shape Up pitch / Track-2 status (Phase 3 wired) |
| `SPEC-GAP-CHECKLIST.md` | Open human gates |
| `COPY-AUDIT-portal-mocks.md` | Approved manufacturer/rep phrase list |
| `BET-A-PITCH-DEMO-RUNBOOK.md` / `INTERNAL-DEMO-RUNBOOK.md` | Demo walks |

---

*Program context for Friday. The only decision requested this cycle is Bet A — see `TRD-Bet-A-filter-truth.md`. Everything else here is shaped and sequenced, not a combined GO.*
