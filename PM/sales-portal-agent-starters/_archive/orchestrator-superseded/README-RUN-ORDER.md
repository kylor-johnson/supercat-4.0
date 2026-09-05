# Run order — Sales Analytics agent starters

**Folder:** `SuperCat 4.0/PM/sales-portal-agent-starters/`  
**Isolation:** ON until you type `ISOLATION OFF — GO on <ticket-or-path>`

---

## Order of operations

```
STEP 0  — Open 05-ORCHESTRATOR.md     (Opus 4.8 · Plan Mode)
          Keep this chat open for the whole program.
              │
              ▼
STEP 1  — Open 01-PROGRAM.md          (Plan Mode)  ← once / when themes change
          Confirm bets A/B/C, WIP, AC for top bet.
              │
              ├──────────────────────┬─────────────────────┐
              ▼                      ▼                     ▼
STEP 2a       STEP 2b                STEP 2c
02-FIX.md     03-UX.md               04-INSIGHT.md
(Agent)       (Agent)                (Agent)
one ticket    wireframes             computational AC
              │                      │
              └──────────┬───────────┘
                         ▼
STEP 3  — Paste outputs back into ORCHESTRATOR chat
          Get Review Cards (PASS / FAIL)
                         │
                         ▼
STEP 4  — Customer feedback on UX / Insight prototypes
          Then: UPDATE SPINE if needed → re-run PROGRAM or lane starters
                         │
                         ▼
STEP 5  — Only later: ISOLATION OFF — GO on …
          Fresh Agent chat for implementation (not Orchestrator)
```

---

## Single vs parallel

| Chat | When | Parallel with |
|---|---|---|
| **05 Orchestrator** | Always first; stays open | Reviews everything; doesn’t build |
| **01 Program** | After orchestrator Session Brief; again when themes/bets change | Not while mid-rewrite of same AC UX is using |
| **02 Fix** | After Program (or immediately if trust is on fire) | UX and/or Insight |
| **03 UX** | After Program locks heroes | Fix and/or Insight |
| **04 Insight** | After Program locks heroes | Fix and/or UX |
| **Implement Rails** | Only after isolation lifted + Review PASS | Never parallel with “explore Lane 3” |

### Do in parallel (recommended first cycle)

- `02-FIX` (SERV-2178 diagnosis) **∥** `03-UX` (Topline + Concentration wireframes)  
- Optionally **∥** `04-INSIGHT` (AC + computational prototype plan for same two heroes)

### Never parallel

- Two different FIX tickets in one chat  
- Lane 3 / EBR-772 “just exploring” while isolation ON  
- Rails implementation while Orchestrator still says isolation ON  

---

## Copy-paste cheat

1. New chat → paste **05** → get Session Brief  
2. New chat → paste **01** → lock bets  
3. New chat(s) → paste **02** / **03** / **04** as Brief allows  
4. Return outputs → **05** for Review Cards  
5. Repeat  

---

## Cycle 02 — capability / feasibility / settings fan-out

After cycle-01 (FIX/UX/INSIGHT reviewed + stamped), three **gather** agents run in parallel, then the
Orchestrator synthesizes the technical plan. Different sources → safe to run at once.

```
05b-ORCHESTRATOR-REBOOT.md   (Plan · state-loaded; boot here if the live orchestrator chat is heavy)
        │  fan out (parallel)
        ├─ 06-CAPABILITY.md      (Agent) → cycle-02-outputs/PORTAL-CAPABILITY-MAP.md
        ├─ 07-DATA-PROFILE.md    (Agent) → cycle-02-outputs/PORTAL-ORG-MATRIX.md   (all 55 orgs)
        └─ 08-SETTINGS-AUDIT.md  (Agent) → cycle-02-outputs/PORTAL-SETTINGS-CONTROL-PLANE.md
        │  paste each back → Orchestrator Review Cards
        ▼
   Orchestrator authors TECHNICAL-PLAN.md (Stories → features → specs/AC → prototype → feedback → update AC)
```

- Settings source of truth preserved at `cycle-02-inputs/settings-inventory-source.md` (134 toggles).
- Only ONE orchestrator chat is live at a time (this chat OR a 05b reboot) — the gather agents report to it.

---

## Cycle 03 — Bet F persona-priority IA (parallel lane, no GO)

Bet F runs **parallel to Bet A** and does **not** unlock `ISOLATION OFF — GO`. Phased, docs-first:

```
Phase 1  Persona research  → PERSONA-RESEARCH-v0.md (PASS)
Phase 2  Shape pack        → PITCH-bet-f-persona-ia / PERSONA-ONE-PAGERS /
                             IA-PRIORITY-MATRIX / SURFACE-PLACEMENT / IA-RECOMMENDATION-v0
Phase 3  SoT wire (DONE)   → spine §5 Bet F + roadmap §5b/bet map + SPEC-GAP + contract/AC footnotes
Phase 4  (optional) HTML   → illustration of role-aware defaults — NOT built, not required for done
Phase 5  Betting brief     → stub in IA-RECOMMENDATION-v0.md; Orchestrator owns final PASS
```

Paste Phase-3/4/5 outputs back into **05 Orchestrator** for Review Cards, same as every other lane. Customer A/B on default homes (rep Customers-vs-Invoices; is CEO a portal end-user; IA depth; adoption/feature-usage boundary; Manager fold-vs-split) stays open. Status: `IA-PERSONA-TRACK.md`.

---

## File index

| File | Purpose |
|---|---|
| `00-PROGRAM-SPINE.md` | Bets, Jira, lanes |
| `00a-DOCTRINE-shapeup-ddd-affinity.md` | Shape Up × DDD × Affinity |
| `00b-PRODUCT-HANDOFF-analytics.md` | Product / destination handoff |
| `01` … `05` | Cycle-01 starters (Program / Fix / UX / Insight / Orchestrator) |
| `05b-ORCHESTRATOR-REBOOT.md` | State-loaded orchestrator (cycle-02) |
| `06` / `07` / `08` | Cycle-02 gather agents (Capability / Data-profile / Settings) |
| `cycle-01-outputs/`, `cycle-02-inputs/`, `cycle-02-outputs/` | Artifacts |
| `README-RUN-ORDER.md` | This file |
