# WORKER — Phase 3c · Thin “so what” layer · Admin Feature Usage demo

You are a **UX / product illustration agent**. Enhance **in place** the existing elite Admin Feature Usage demo with a **small actionable layer** for SuperCat CS/GTM admins. Do **not** expand into Insightful CEO VMs, Sales Portal Intelligence, or new Mixpanel event families.

## Isolation (hard)

- **Edit only:**
  - `design-system/app/admin-feature-usage-demo.html`
  - `PM/Admin-console/PHASE3-DEMO-RUNBOOK.md`
  - `PM/Admin-console/00-PROJECT-SPINE.md` (Phase 3c status line + link this worker)
- **Never** edit Sales Portal Friday demos, `supercat-code/`, BQ, Jira, or Insightful report HTML
- **Never** add GMV, AOV, peer benchmarks, Portal Q-R1/Q-18, named-rep→revenue, or WoW chart products
- Does **not** unlock `ISOLATION OFF — GO on Admin Feature Usage`

## Mandatory reads (before editing)

1. `PM/Admin-console/BOUNDARY-vs-portal-bet-e-bet-f.md`
2. `PM/Admin-console/AC-feature-usage-v0.md` + `TAXONOMY-events.md`
3. `PM/Admin-console/PHASE3-DEMO-RUNBOOK.md` (current 3b walk — keep working)
4. Open and understand `design-system/app/admin-feature-usage-demo.html` (FACTS store, filters, drill)
5. Skim only for *question* borrow (do not implement these queries):
   - `Insightful Product 4.0/foundation/query_library_v2.md` — Q-22 depth, Q-04 non-selling *idea*, Q-06 trajectory *shape* (ignore GMV side)
   - Do **not** pull Q-01 scorecard, Q-R1, Q-18, VM-02 archetypes, peer medians

## Goal (small — do not go hard)

Add Admin-only **actionable / so-what** affordances on top of the existing demo. Same surfaces, same taxonomy, same fact-store model — richer status language.

### 1. People status chips (leaderboard) — required

Replace or extend the single High/Med/Low tier display with a clear **status chip** per user:

| Status | Rule (Mixpanel-only, fictional facts OK) |
|---|---|
| **Excelling** | High engagement tier **and** active days/actions ≥ prior comparable window |
| **Steady** | Mid activity; not clearly up or down |
| **Declining** | Active days or actions **down** vs prior window (same length) — **no GMV** |
| **Quiet/Cold** | ≤1 active day in current range (keep visual emphasis you already have) |

Implementation notes:
- Extend `FACTS` so each user (per range) has enough prior-window fields to compute status, **or** precompute `status: 'excelling'|'steady'|'declining'|'cold'` in the fact store (honest either way).
- Keep High/Med/Low if useful as secondary (e.g. tooltip or mono sublabel) — **status chip is the primary “so what.”**
- Optional: filter chip / KPI focus for “Declining” or “Quiet/Cold” only — nice if cheap; not required.

### 2. Org “so what” strip — required

Upgrade the existing ops callout (or replace it) to **2–3 short lines** an admin would say on a CS call, recomputed when **range** (and optionally category filter) changes. Examples of content (use real computed demo facts):

- `2 quiet/cold seats`
- `Sell thin vs Search` (Sell share clearly low vs Search/Find)
- `3 users on app version older than X` (from drill device/version fields)

Rules:
- Mixpanel / adoption language only — **never dollars**
- No peer org comparison
- Must update when date range changes
- Keep tone: coaching / at-risk / call prep — not manufacturer Owner portal copy

### 3. Non-seller hint on drill — optional but preferred

On user drill-down, if user has meaningful Search/Share/Serve activity but **~0 orders submitted** (`order_submitted` / Sell signal ≈ 0), show a quiet hint:

> Busy in catalog · not submitting orders

Mixpanel-only. Do not build a full Q-04 role taxonomy UI.

## Preserve (do not break)

- Range recompute (q3 / q2 / 30d)
- Category bar + % filter chain + Clear
- KPI filters / focus
- Logins chart + leaderboard → drill
- Feature row toast
- URL hash
- Admin Console chrome · SuperCat-admin only · no Portal nav
- AC-2, AC-3, AC-3a, AC-4, AC-4a, AC-5, AC-6, AC-7 affordances

## Out of scope (hard no)

- Insightful CEO report layout / signals / $
- Sales Portal Intelligence strip
- Bet E Settings
- New event categories beyond `TAXONOMY-events.md`
- Cross-org benchmarks, realtime, alerting, WoW line charts
- Eng ST-1…ST-4 implementation

## Deliverables

1. Updated `design-system/app/admin-feature-usage-demo.html`
2. Updated `PHASE3-DEMO-RUNBOOK.md` — add a short “so what” step to the ≤2 min walk; note status rules; restate zero Portal / zero $
3. `00-PROJECT-SPINE.md` — Phase 3c awaiting Review Card; link this worker

## Done criteria

- Leaderboard shows Excelling / Steady / Declining / Quiet-Cold with visible differences across users
- Org strip shows 2–3 computed so-what lines that change with range
- Non-seller hint appears on at least one drill user in the demo data
- Prior 3b click path still works
- Isolation held

## When finished

Reply with: paths · 5-bullet summary ·  
`Ready for Orchestrator Review Card — Phase 3c` · stop (do not start Phase 4).
