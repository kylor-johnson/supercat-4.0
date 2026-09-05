# Orchestrator Session — Cycle-03 reboot end-to-end

**Date:** 2026-07-17 · **Isolation:** ON · **Owner:** Kylor  
**Boot source:** `05d-ORCHESTRATOR-REBOOT-cycle03.md`

---

# Session Brief — 2026-07-17

## Isolation
**ON** — no Rails / `supercat-code/` edits. Mockup + PM docs only.

## Mandatory reads confirmed
1. `00-PROGRAM-SPINE.md` — EBR-only scope, F8/F9 three-universe, bets A–E  
2. `00a-DOCTRINE-shapeup-ddd-affinity.md` — Shape Up / DDD / Affinity law  
3. `00b-PRODUCT-HANDOFF-analytics.md` — product state  
4. `05-ORCHESTRATOR.md` — review rubric  
5. Cycle-03 pack (all artifacts in `cycle-03-outputs/`)  
6. Cycle-02 commerce authority (`PORTAL-CAPABILITY-MAP`, `PORTAL-ORG-MATRIX`, `PORTAL-SETTINGS-CONTROL-PLANE`)

## Lane status
| Lane | Hill | Note |
|---|---|---|
| 0 Trust | downhill (shaped) | Bet A pitch done; EBR-40/212 build blocked |
| 1 UX | downhill | Cycle-03 mockup done; **feedback session pending** |
| 2 Computational | downhill (AC) | IR v1 AC + tech plan under EBR-775 |
| 3 Inferential | **PARKED** | EBR-772/776 |

## Open bets (EBR-only program)

| Bet | Appetite | Status | Blocker |
|---|---|---|---|
| **A** — Filter + metric law | Small batch | Pitched | Isolation; betting-table GO |
| **B** — Wireframe + feedback | Small batch | Mockup done | Customer feedback session |
| **C** — IR v1 (EBR-775) | Big batch | AC shaped | Feedback → AC freeze → GO |
| **D** — LLM layer | — | **PARKED** | Bet C must ship first |
| **E** — Control plane | Big (Wave 0–1 small) | Downstream | Not this cycle's primary |

## Three-universe map (F8/F9 — do not re-litigate)

| Universe | Travels | v1 role |
|---|---|---|
| **A — Invoice arithmetic** | C1, S1, YoY… | **Heroes** (C1 + S1) |
| **B–D — Behavior floor** | Q-R1, Q-18/Q-01, Mixpanel | **Team strip** |
| **E — Invoiced named-rep $** | RS-01, Q-R5, Q-51 | **Do not lead** |

**Metric law (locked):** `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap, `customer_bill_to_number` grain. Ceiling **STRONG**. Quotes ≠ sales (EBR-87). Export must reconcile to UI (EBR-91). EBR-7 answered by `net_amount`.

**Scale (cycle-02):** 55 orgs / 4.88M invoice rows; sarreid ~$15.98M LTM; cci ~$71.23M.

## Ship readiness (Bet C)
**NOT READY TO BUILD.** Gate order: feedback session → AC freeze → betting table → `ISOLATION OFF — GO on EBR-775`.

## What ran this session
1. Orchestrator boot from `05d-ORCHESTRATOR-REBOOT-cycle03.md`  
2. HTML mockup pass — two artifacts: `design-system/app/sales-portal-cycle03-mockup.html` (customer feedback, wireframe rail) + `design-system/app/sales-portal-cycle03-chrome.html` (internal demo, shared `<sc-app-sidebar>` chrome)  
3. UX brief + feedback script updated to point at cycle-03 mockup  
4. Ship-readiness checklist updated (mockup gate = done)  
5. This session log + betting-table draft

## What to run next (elite order §4)

| # | Action | Starter / artifact | Parallel? |
|---|---|---|---|
| 1 | **Run feedback session** | `FEEDBACK-SESSION-SCRIPT.md` + cycle-03 mockup | Human — Kylor |
| 2 | Fill post-feedback table | `UX-brief-c1-s1-team-strip.md` | After #1 |
| 3 | Patch IR AC if must-haves change | `INSIGHT-IR-v1-AC.md` | After #2 |
| 4 | Freeze AC + update ship readiness | `SHIP-READINESS-bet-c.md` | After #3 |
| 5 | Betting table confirm appetite | `01-PROGRAM.md` or this chat | After #4 |
| 6 | Jira status (close EBR-7, dup links) | Atlassian MCP | **Kylor OK only** |
| 7 | Build | Eng after verbatim GO | Blocked |

## Do not run
- Rails / migrations / PRs (isolation ON)  
- Unpark EBR-772/776  
- Pull iPad EBRs (36, 655, 743, 329, 527, 503, 524) back into program  
- Lead with RS-01 / named invoiced-rep revenue  

## Decisions needed from Kylor
1. **Schedule feedback session now** — who from sarreid/cci/ufi? (script + mockup ready)  
2. **Betting table appetite** — confirm Bet C big batch + Bet A small-batch parallel?  
3. **Jira hygiene** — OK to close EBR-7 and post formal dup links?

---

# Review Card — Cycle-03 HTML mockup pass

## Verdict
**PASS**

## Isolation check
Did anyone touch Rails? **N** — mockup-only under `design-system/app/`.

## Shape Up check
- [x] Problem is answer-first (three panels, one job each)  
- [x] Appetite = Bet B wireframe slice  
- [x] Elements at breadboard level (C1, S1, team strip)  
- [x] Rabbit holes called out (RS-01 absent, C3 degrade optional)  
- [x] No-gos listed in footnote  
- [x] Not a grab-bag  

## DDD check
- [x] Invoiced ≠ booked ≠ quote  
- [x] Portal Reporting context  
- [x] Metric spine = net_amount (C1)  
- [x] Team strip labeled behavior floor, not Universe E  

## Affinity / evidence
- [x] C1 topline verified live — sarreid $16.02M LTM / 11,729 inv / 1,417 custs (mockup shows $15.98M, reconciles within 0.25%)  
- [~] S1 **aggregate** grounded live — 671 accounts down ≥30%; top-55 by LTM = $2.38M at risk (mockup headline corrected from impossible $1.12M). Per-account rows remain illustrative/masked.  
- [~] Team strip uses Q-R1/Q-18 labels per AC; counts are illustrative (behavior queries pending; "77" is not a verified active-seat figure)  

## Lane / WIP
- [x] Lane 1 mockup supports Lane 2 AC — same heroes  
- [x] No Lane 3 / LLM content  

## Craft check
- [x] Real density — C1 verified live ($16.02M); S1 aggregate grounded ($2.38M/55), rows illustrative  
- [x] App kit `.kshell` + portal rail  
- [x] One job per panel  

## Promote?
Ready for **customer feedback session** — not production build.

---

# Betting table draft (for Kylor confirm)

## Recommended appetites

| Bet | Appetite | Rationale |
|---|---|---|
| **A** | Small batch (1–2 wk shape + AC; eng after GO) | Filter truth blocks trust on every hero; pitch done |
| **B** | Small batch (feedback only — mockup done) | Unblocks Bet C AC freeze |
| **C** | **Big batch** (6 wk eng after GO) | Umbrella EBR-775; C1 + S1 + team strip scoped |
| **D** | **No bet** | Parked |
| **E** | Defer to next cycle | Control plane is real but not gate for C |

## Parallel OK?
**Yes:** Bet A diagnosis (FIX starter, read-only) ∥ Bet B feedback ∥ Bet C AC freeze after feedback.  
**No:** Build before feedback + GO.

## Circuit breakers
- If feedback picks C3 over S1 as hero 2 → patch AC-2/AC-4 only; do not expand scope  
- If feedback cuts team strip → degrade to C1 + S1 only; still ships under EBR-775  
- If sarreid demo needs territory scoping → use zero-exposure org or fix SERV-2196 first (spine §4 prevalence)

---

# Invite blurb (ready to send)

See `FEEDBACK-SESSION-SCRIPT.md` §Invite — open cycle-03 mockup in browser before the call.

---

*Session log from Orchestrator reboot `05d`. Supersedes nothing in `ORCHESTRATOR-review-cycle03.md` — extends it with mockup pass + session brief.*
