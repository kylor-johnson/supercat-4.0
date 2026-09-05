# Jira hygiene — PM-doc log ONLY (do NOT post to Jira)

> **⚠️ REVERTED 2026-07-17.** Jira is **read-only** for this program (see
> `.cursor/rules/jira-read-only.mdc`). The comments below were auto-posted to Jira
> in an earlier session under Kylor's account and are being **deleted**. Do **not**
> re-post them. These bodies are retained here **only** as a PM-side record of how
> each ticket maps to the refresh — they must live in `PM/`, never on the ticket.

**Date:** 2026-07-17 · **Status:** Log only — **never** call `addCommentToJiraIssue`.  
**Rule:** No Jira writes of any kind. Capture ticket resolution/mapping in PM docs.

Program authority: `cycle-03-outputs/EBR-AFFINITY-PORTAL.md` · spine §6.

---

## Dup / link pairs

### EBR-474 (comment)
```
Sales Analytics program (2026-07-17): Duplicate of EBR-601 (Portal invoice status — Savoy). Canonical = EBR-601. Keep this ticket linked; do not shape separately for Intelligence Report v1.
```

### EBR-601 (comment)
```
Sales Analytics program (2026-07-17): Canonical for portal invoice status (Savoy). EBR-474 is the duplicate. Deferred from IR v1 — one-org / deferred cluster. See SuperCat 4.0/PM/sales-portal-agent-starters/cycle-03-outputs/EBR-AFFINITY-PORTAL.md
```

### EBR-180 (comment)
```
Sales Analytics program (2026-07-17): Product ask for multi-territory RepNumber stays on this EBR. Engineering implementation is downstream SERV-2178 (+ SERV-2180). XL shelf — separate appetite; not in Phase-1 filter-truth pitch (that is EBR-40 + EBR-212).
```

### EBR-772 (comment)
```
Sales Analytics program (2026-07-17): PARKED under EBR-775 until computational Intelligence Report v1 ships and is trusted. Sibling: EBR-776. Do not schedule Lane-3 / talk-to-data work this cycle. See cycle-03-outputs/PARK-llm-ebr-772-776.md
```

### EBR-776 (comment)
```
Sales Analytics program (2026-07-17): PARKED with EBR-772 under epic EBR-775. Same LLM/agentic cluster — not a separate bet. Revive only after computational surface is trusted.
```

### EBR-775 (comment)
```
Sales Analytics program (2026-07-17): Umbrella for portal Intelligence Reports. Sequence: computational IR v1 first (C1 True Topline + S1/EBR-198 + team strip); LLM children EBR-772 + EBR-776 remain parked. Spine: PM/sales-portal-agent-starters/00-PROGRAM-SPINE.md
```

---

## Out of program (Sales Portal reporting)

Use the same body on each key, swapping the reason line.

### EBR-36
```
Out of Sales Analytics (Portal & Reporting) program scope (2026-07-17): iPad shared-drafts / territory sharing — not Sales Portal reporting. Reroute to iPad product owner. Affinity: cycle-03-outputs/EBR-AFFINITY-PORTAL.md §2.
```

### EBR-655
```
Out of Sales Analytics (Portal & Reporting) program scope (2026-07-17): order-email CC by territory — not portal reporting / Intelligence Reports. Reroute to order-notifications owner.
```

### EBR-743
```
Out of Sales Analytics (Portal & Reporting) program scope for this cycle (2026-07-17): iPad real-time analytics is a later channel. Portal-first computational surface is under EBR-775. Keep Approved; do not pull into portal IR v1 shaping.
```

### EBR-329
```
Out of Sales Analytics (Portal & Reporting) program scope (2026-07-17): invoice email recipients — not analytics/reporting.
```

### EBR-527
```
Out of Sales Analytics (Portal & Reporting) program scope (2026-07-17): eCat→portal orders push is integration/ETL, not Intelligence Report surface.
```

### EBR-503
```
Out of Sales Analytics (Portal & Reporting) IR program scope (2026-07-17): option/fabric search on eOL lists — not computational Intelligence Report bet.
```

### EBR-524
```
Out of Sales Analytics (Portal & Reporting) IR program scope (2026-07-17): custom eOL customer dashboard tab — not IR v1.
```

---

## Phase-1 / doctrine notes (optional paste)

### EBR-40
```
Sales Analytics Bet A (2026-07-17): In-scope with EBR-212 as one territory filter-truth pitch for Sales Portal. See cycle-03-outputs/PITCH-phase1-filter-metric-law.md
```

### EBR-212
```
Sales Analytics Bet A (2026-07-17): In-scope with EBR-40 (dashboard half of portal territory filter truth). Stalled In Progress since 2022 — reshape, don't silently extend.
```

### EBR-7
```
Sales Analytics (2026-07-17): Recommend close / decline. Prod-Council denied 2022. Doctrine: portal "sales" = SUM(portal_invoices.net_amount) which already nets discounts/credits. No separate build. See provenance_spine + INSIGHT-IR-v1-AC.md
```

### EBR-91 / EBR-87
```
Sales Analytics (2026-07-17): Metric-law AC inputs for every Intelligence Report hero (reconcile export↔UI; never include quotes in sales). Locked in PITCH-phase1 + INSIGHT-IR-v1-AC.
```

### EBR-198
```
Sales Analytics Bet C (2026-07-17): Maps to Insightful S1 (quietly dying accounts) — preferred second commerce hero for IR v1 under EBR-775.
```

---

## Removal checklist (these were wrongly auto-posted — delete them)

Comment IDs to delete (all authored by Kylor's account, 2026-07-17 15:15):

| Ticket | Comment ID | Ticket | Comment ID |
|---|---|---|---|
| EBR-474 | 38148 | EBR-527 | 38158 |
| EBR-601 | 38149 | EBR-503 | 38159 |
| EBR-180 | 38150 | EBR-524 | 38160 |
| EBR-772 | 38151 | EBR-40 | 38161 |
| EBR-776 | 38152 | EBR-212 | 38162 |
| EBR-775 | 38153 | EBR-7 | 38163 |
| EBR-36 | 38154 | EBR-91 | 38164 |
| EBR-655 | 38155 | EBR-87 | 38165 |
| EBR-743 | 38156 | EBR-198 | 38166 |
| EBR-329 | 38157 | | |

- [ ] All 19 comments deleted (UI trash icon, or token DELETE `/issue/{key}/comment/{id}`)
- [x] Read-only rule added: `.cursor/rules/jira-read-only.mdc`

*Do NOT re-post. Jira is read-only for this program.*
