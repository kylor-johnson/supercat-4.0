# WORKER — Phase 4 · Betting / GO brief · Admin Feature Usage

You are a **Program agent** (or Orchestrator if Kylor says “Orchestrator, write this”).  
Write a short **ready-for-table / GO brief** for **Admin Console — eCat Feature Usage Report**. You do **not** implement Rails, apply BQ, or unlock isolation.

## Isolation (hard)

- **Write only** under `PM/Admin-console/`
- No `supercat-code/` edits, no BQ apply, no Friday-demo edits, no Jira writes
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage` — the brief **names** the unlock phrase for Kylor to use later

## Mandatory reads

1. `00-PROJECT-SPINE.md`
2. `PITCH-feature-usage.md`
3. `AC-feature-usage-v0.md` + eng rows AC-3a / AC-4a in `TECHNICAL-PLAN-feature-usage.md` §6
4. `TAXONOMY-events.md` · `BOUNDARY-vs-portal-bet-e-bet-f.md`
5. `TECHNICAL-PLAN-feature-usage.md` — especially §8 open questions + §11 PR order
6. `PHASE3-DEMO-RUNBOOK.md` + open the demo once (interaction is the visual bet)
7. `00-ORCHESTRATOR.md`

## Orchestrator carry-forwards into the brief

| ID | Item |
|---|---|
| Q-ORG | COALESCE include `current_organization_shortname`? (plan recommends **yes**) |
| Q-TZ | Activity date TZ |
| Q-MV | MV refresh + IAM owner |
| Q-NAV | Admin nav label/placement (not Portal, not Bet E Settings) |
| Q-ACL | Confirm `User#is_admin?` for AC-9 |
| Q-TAX | Taxonomy vs raw CTO paste still unverified |
| Q-HIST / Q-CRED | Sync window + BQ credentials |
| Demo | Phase 3b HTML is the ST-4 interaction target (filters, drill, range recompute) — cite path |

## Deliverable

### `BETTING-BRIEF.md` (required)

Keep it **short** (≈1–2 pages). Sections:

1. **Bet one-liner** — Admin Console · SuperCat-admin · org Feature Usage  
2. **Problem / appetite** — CSV/export → operational Admin tool; F7 “No Portal Usage”  
3. **Done when** — AC-1…AC-9 + AC-3a/AC-4a; ST-1→ST-4; demo interaction parity  
4. **Architecture lock** — Mixpanel → 3 MVs → nightly Postgres → Chart.js (cite plan)  
5. **Not betting** — Portal strip · Bet E · Bet F build · client self-serve · benchmarks/realtime/alerting/WoW · Admin 2.0 · Insightful CEO report  
6. **Open decisions for the table** — table of Q-ORG…Q-TAX with recommended defaults  
7. **Eng wave / PR order** — ST-1…ST-4 from plan §11  
8. **Demo pointer** — `design-system/app/admin-feature-usage-demo.html` + runbook  
9. **GO phrase** — exact: `ISOLATION OFF — GO on Admin Feature Usage`  
10. **Risks** — sparse `organization_shortname`, OrgUser ACL trap, Chart.js pin, taxonomy paste gap  

### Update `00-PROJECT-SPINE.md`

- Phase 3 → **Done (3b PASS)**  
- Phase 4 → **Done / awaiting Orchestrator Final PASS** (or done if Orchestrator authored)  
- Link `BETTING-BRIEF.md`

## Do not

- Expand scope  
- Write migrations / MV SQL as “done”  
- Post to Jira  
- Soft-unlock isolation  

## When finished

Reply with path · 5-bullet summary ·  
`Ready for Orchestrator Review Card — Phase 4` · stop.
