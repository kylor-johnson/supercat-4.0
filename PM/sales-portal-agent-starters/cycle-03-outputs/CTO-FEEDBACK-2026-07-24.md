# CTO feedback — Bet A ready for SERV (2026-07-24)

**Source:** CTO next-step guidance after Bet A validation pack + shaped EBR bodies.  
**Owner:** Kylor · **Captured:** 2026-07-24  
**Related:** `CTO-FEEDBACK-2026-07-20.md` · `TRD-Bet-A-filter-truth.md` · `SPRINT-PACK-bet-a.md` · `BET-TRIAGE-BOARD.md`

---

## What landed

Bet A is **actionable and ready to pull into sprint / eng via EBR**. Story write-up can vary by type (bug-heavy vs new functionality). Other bets need the **same format** and triage — not an immediate build GO.

| # | CTO guidance (paraphrase) | Action |
|---|---|---|
| 1 | Bet A already actionable — ready for sprint | `ISOLATION OFF — GO on EBR-40` · package SERV stories · link EBR↔SERV |
| 2 | Story format may vary (bug vs feature) | Bug template for 40/212/91; feature template for C/E; park/close for 87/7 |
| 3 | Other bets → same format + triage | `BET-TRIAGE-BOARD.md` — not all ready to build |
| 4 | Jira MCP links tickets; move into SERV board | Focused writes only — create/link/move; **no** hygiene/noise comments |

---

## Gate status (2026-07-24)

```
Validation pack COMPLETE (2026-07-21)
        │
        ▼
CTO: Bet A ready for EBR → SERV
        │
        ▼
ISOLATION OFF — GO on EBR-40
        │
        ▼
SERV board stories linked · eng builds against FILTER-TRUTH-AC
```

**In GO:** EBR-40 + EBR-212 (paired) + EBR-91 · close EBR-7 by doctrine · park EBR-87.  
**Not in GO:** Bet C / D / E / F builds (triage + format only).

---

## Success checklist

- [x] This file on disk  
- [x] Supersedes open “readout / GO ask” boxes in `CTO-FEEDBACK-2026-07-20.md`  
- [x] `SPRINT-PACK-bet-a.md` + `ENG-HANDOFF` Bet A section  
- [x] `BET-TRIAGE-BOARD.md` for B–F  
- [x] SERV issues created + linked: SERV-2447←EBR-40 · SERV-2448←EBR-212 · SERV-2449←EBR-91  


---

*Authorizes Bet A eng work after GO phrase is recorded in spine/TRD. Does not authorize random Jira comments.*
