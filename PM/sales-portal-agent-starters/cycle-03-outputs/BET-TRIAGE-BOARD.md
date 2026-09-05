# Bet triage board — Sales Analytics (post Bet A GO)

**Date:** 2026-07-24 · **CTO:** `CTO-FEEDBACK-2026-07-24.md`  
**Bet A format template:** Problem · Acceptance · Evidence · Out of scope (bug vs feature variance OK)

---

## Board

| Bet | Disposition | Story type | Format ready? | Build GO? | Artifacts |
|---|---|---|---|---|---|
| **A** Filter truth | **Keep — in sprint** | Bug-heavy | ✅ | **Yes** — `ISOLATION OFF — GO on EBR-40` | `SPRINT-PACK-bet-a.md` · `FILTER-TRUTH-AC.md` · `ENG-HANDOFF` §C |
| **B** List tabs | **Rides with A** | Shell / UX | ✅ | With A (optional polish) | `STORY-PACK-bet-b.md` · `LIST-TABS-AC.md` |
| **C** IR v1 | **After A** | Feature | ✅ shaped pack | **No** until `GO on EBR-775` + cci/kll re-stamp | `STORY-PACK-bet-c.md` · `INSIGHT-IR-v1-AC.md` |
| **D** LLM | **Park** | — | ✅ parked | No | `PARK-llm-ebr-772-776.md` |
| **E** Settings hub | **Shaped; Wave 0–1 optional** | Feature | ✅ shaped pack | **No** until `GO on Bet E` | `STORY-PACK-bet-e.md` · `SETTINGS-hub-v1-AC.md` |
| **F** Persona IA | **Parallel research** | Research | ✅ for betting table | No — does not unlock Rails | `IA-RECOMMENDATION-v0.md` · Track 2 |

---

## Sequencing (unchanged thesis)

```
A trust (GO now) → B proof shell (rides) → C computational (after A)
                 ↘ E Wave 0–1 optional parallel
D LLM only after C trusted
F informs B/E ordering; never substitutes for A
```

---

## Human calls still open

1. Does Bet E **Wave 0–1** ride with Bet A this cycle?  
2. When to schedule Bet C GO (after A verify on wwjc)?  
3. Bet F customer A/B (rep default home) — recruit wwjc/sarreid/cci/ufi  

---

## Jira posture

| Action | Now | Later |
|---|---|---|
| Create/link SERV for A keep EBRs | **Done** — SERV-2447/2448/2449 · sprint June 2026 | — |
| Rewrite EBR-775 description → computational IR v1 | Optional description edit when C is next | Before C GO |
| SERV for B/C/E | Only if eng wants separate stories | After triage decisions |
| Hygiene comments on EBR cluster | **Never** | — |
| Close EBR-7 / park EBR-87 transitions | PM recommended | Kylor OK |

---

*Triage board. Story packs: `STORY-PACK-bet-b.md` · `STORY-PACK-bet-c.md` · `STORY-PACK-bet-e.md`.*
