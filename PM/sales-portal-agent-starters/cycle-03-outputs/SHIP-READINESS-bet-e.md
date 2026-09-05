# Ship readiness — Bet E Portal & Access control plane

**Date:** 2026-07-18 · **Status:** NOT READY TO BUILD  
**Isolation:** ON — no Rails until Kylor writes verbatim:  
`ISOLATION OFF — GO on Bet E`  
(or narrower: `ISOLATION OFF — GO on Bet E Wave 0` / `ISOLATION OFF — GO on SERV-2254`)

---

## Checklist

| Gate | Status |
|---|---|
| Control-plane triage (134 toggles / 6 layers) | Done — `cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md` |
| Demo hub IA (6 sections) | Done — `SETTINGS-hub-v1-DEMO-SPEC.md` |
| Internal demo Settings view | Done — `design-system/app/sales-portal-internal-demo.html` (Later nav; not default landing) |
| Build AC (E0–E6 + no-gos + verify) | Done — **`SETTINGS-hub-v1-AC.md`** |
| Eng handoff (implementability summary — cites AC, no re-triage) | Done — **`ENG-HANDOFF-bet-a-b-c-e.md` §F** (waves 0–5, Wave 0 delete list, E1–E6 one-liners + Rails cites) |
| Technical plan §8 waves | Done — `TECHNICAL-PLAN.md` §8 (points at AC) |
| Wave appetite freeze (Small 0–1 / Big 2–5) | Done — AC-E0 |
| Bet E ↔ Bet A pairing (Wave 4 match mode) | Done — AC-E4 + FILTER-TRUTH / FIX-diagnosis |
| Revenue lock ↔ INSIGHT | Done — AC-E3 (sign-off still human at change time) |
| Confluence 1813676033 ~47 Org row finalize | **Pending** — human; before Wave 2 hub (none metric-critical) |
| Dormant-wired flags ship/cut (4 flags) | **Pending** — product call |
| Betting table includes Bet E (with A/C) | **Pending** — human |
| Orchestrator Review Card on Bet E shape | This chat |
| Isolation lift | **Blocked** — needs explicit GO phrase below |

---

## Explicit GO phrases

| Intent | Phrase (verbatim) |
|---|---|
| Full Bet E (hub + waves as shaped) | `ISOLATION OFF — GO on Bet E` |
| Small-batch only (dead flags + graduate) | `ISOLATION OFF — GO on Bet E Wave 0` (Wave 1 may be named in same message) |
| Eng footnote path | `ISOLATION OFF — GO on SERV-2254` (must still honor AC-E0 waves / no-gos) |

Until one of those is written: **NOT READY TO BUILD.**

---

## Elite order remaining for E

1. **👤 Betting table** — confirm whether Wave 0–1 rides with Bet A this cycle; whether Big hub (2–5) is in or next.  
2. **👤** Finalize Confluence 1813676033 deferred Org rows (bucket triage already done).  
3. **👤** Ship/cut call on 4 dormant-wired flags.  
4. **👤** Kylor GO phrase (above).  
5. Eng: Wave 0 deletes → Wave 1 graduate → Wave 2 Enablement tree → … → Wave 4 **only with Bet A path** → Wave 5 after INSIGHT.  
6. Staging verify per AC-E verify checklist (sarreid / cci enablement + backlog lock; Wave 0 regression).

## Cross-link (hard)

- **Do not ship Wave 4** (Territory match mode) without Bet A / `FILTER-TRUTH-AC.md` path (same-cycle GO or explicit dependency).  
- Enablement tree does not replace list-tab filter honesty.  
- Demo Wave badges / Delete buttons ≠ eng directive (`DEMO-SURFACE-CONTRACT.md`).

## Do not

- Start Rails / migrations / PRs while isolation ON.  
- Expose revenue definitions as client-editable.  
- Delete dormant-wired flags without ship/cut.  
- Unpark EBR-772 / EBR-776.  
- Re-triage 134 toggles from scratch.  
- Recentering the whole program on Settings forever — WIP stays structural trust → shell → IR.

---

*Ship readiness artifact — Bet E is shaped (AC + demo honesty), not shipping.*
