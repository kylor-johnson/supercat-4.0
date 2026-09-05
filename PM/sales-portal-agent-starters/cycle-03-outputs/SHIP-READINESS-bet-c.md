# Ship readiness — Bet C Computational IR (under EBR-775)

**Date:** 2026-07-17 · **Status:** NOT READY TO BUILD  
**Isolation:** ON — no Rails until Kylor writes verbatim:  
`ISOLATION OFF — GO on EBR-775` (or named path).

---

## Checklist

| Gate | Status |
|---|---|
| Affinity / EBR scope locked | Done — `EBR-AFFINITY-PORTAL.md` |
| Spine EBR-primary | Done — `00-PROGRAM-SPINE.md` §6 |
| Phase-1 pitch (filter + metric law) | Done — `PITCH-phase1-filter-metric-law.md` |
| IR v1 AC (C1 + S1 + team strip) | Done — `INSIGHT-IR-v1-AC.md` |
| Technical plan | Done — `TECHNICAL-PLAN.md` |
| UX brief + feedback questions | Done — `UX-brief-c1-s1-team-strip.md` |
| Feedback session script | Done — `FEEDBACK-SESSION-SCRIPT.md` |
| HTML mockup — wireframe (customer feedback) | Done — `design-system/app/sales-portal-cycle03-mockup.html` (use this for the customer feedback session; low "is this built?" risk) |
| HTML mockup — chrome-fidelity (Intelligence-only) | Done — `design-system/app/sales-portal-cycle03-chrome.html` (shared `<sc-app-sidebar>`) |
| HTML — Dashboard + list substance + Intelligence | Done — default Dashboard; answer-first list tabs; What’s broken last; `DEMO-SURFACE-CONTRACT.md` + `LIST-TABS-AC.md` |
| Stamped SQL | Done — `IR-v1-QUERIES.md` (sarreid 2026-07-17) |
| Eng handoff (JSON read-model C6 + Mixpanel degrade C5) | Done — **`ENG-HANDOFF-bet-a-b-c-e.md` §E** (org_id→heroes+provenance schema; degrade-default) |
| Bet A AC (gate for filter honesty) | Done — `FILTER-TRUTH-AC.md` |
| Customer feedback | Optional — not blocking internal AC freeze |
| Grade-org re-stamp (cci/kll) | **Pending** before build |
| Orchestrator Review Card PASS | See `ORCHESTRATOR-review-cycle03.md` |
| LLM parked | Done — EBR-772/776 comments + `PARK-llm-ebr-772-776.md` |
| Isolation lift | **Blocked** — needs explicit GO |

---

## Elite order remaining

1. Betting table confirms Bet A then Bet C.  
2. Re-stamp `IR-v1-QUERIES.md` on cci + kll.  
3. Kylor: `ISOLATION OFF — GO on EBR-775` (and/or EBR-40 for filter).  
4. Build → staging → verify → prod → document/promote.

## Do not

- Start Rails / migrations / PRs while isolation ON.  
- Schedule EBR-772/776.  
- Expand v1 to deferred EBR cluster.

---

*Ship readiness artifact — computational surface bet is shaped, not shipping.*
