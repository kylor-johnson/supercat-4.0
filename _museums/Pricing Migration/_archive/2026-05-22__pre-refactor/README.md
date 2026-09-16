# SuperCat 2026 Pricing Migration — Communications Work Product
*Last updated: 2026-05-20*

---

## What This Is

A fully operational communications system for the 2026 pricing migration across 109 accounts. Four formats are built and production-ready. Work is ongoing — CEO Pre-Call accounts (9) and HOLD accounts (51) are not yet drafted.

For full agent orientation, read `_handoff-prompt.md`.

---

## Folder Structure

```
format-a-notices/           ≤10% delta — CS-sent, no CEO involvement
format-b-notices/           >10% delta — CS-sent with CEO awareness flag
ceo-letter-notices/         High-delta / high-value — CEO co-authored, meeting required
good-news-notices/          Price decreases — CS-sent, no meeting, no justification needed
_master-account-data-v6.2.csv   Authoritative account data (health, drivers, flags)
migration_comm_tiers_2026-05-19.csv   All 109 accounts bucketed with comm_action
_handoff-prompt.md          Fresh agent orientation — read this first
_roadmap.md                 Current project status and next actions
_current-state.md           Artifact inventory and decision log
_template-test-prompt.md    QA verification prompt — run to confirm template integrity
```

Each format folder contains:
- `_brief-template.md` — the standard template for that format
- `_delivery-email-template.md` — delivery email template (Format B and CEO Letter)
- `_fresh-agent-prompt.md` — paste into a new Agent chat to generate any account in that format
- `[ord_id]__[slug]__brief.md` — drafted account briefs
- `[ord_id]__[slug]__delivery-email.md` — drafted delivery emails

---

## Format Overview

### Good News Notice — Tailwind Accounts (Price Decrease)
Accounts where the 2026 rate is lower than current. No justification, no meeting, no co-sign. CS sends it directly.
- **Template:** `good-news-notices/_brief-template.md`
- **Calibration examples:** `good-news-notices/pf__palecek/`, `good-news-notices/rw__renwil/`, `good-news-notices/jyc__jamie-young/`, `good-news-notices/dccl__donald-choi-canada/` (Option A = email with inline table is the default)

### Format A — ≤10% Delta
Near-flat increases. CS sends without CEO involvement. 60-day notice window.
- **Template:** `format-a-notices/_brief-template.md`
- **Agent prompt:** `format-a-notices/_fresh-agent-prompt.md`
- **Calibration:** `kal` (Kalco/Allegri Crystal), `gc` (voice reference)

### Format B — >10% Delta
Larger increases. CS-sent, but CEO is flagged for awareness before send.
- **Template:** `format-b-notices/_brief-template.md`
- **Agent prompt:** `format-b-notices/_fresh-agent-prompt.md`
- **Calibration:** `kal` (Format A voice reference), `cci` (pricing math and table structure)

### CEO Letter — High-Delta / High-Value
CEO co-authors with CS. Meeting required. Used for the highest-impact accounts or accounts requiring executive handling.
- **Template:** `ceo-letter-notices/_brief-template.md`
- **Agent prompt:** `ceo-letter-notices/_fresh-agent-prompt.md`

---

## Key Rules (baked into every template)

1. Never lead with a percentage — always lead with the dollar amount and effective date
2. Never say "we're adjusting your pricing"
3. Never apologize for the change
4. "Everything stays the same except the invoice" — verbatim, every notice
5. No expansion language in any migration notice — Format C is a separate document, sent only after a confirmed positive signal
6. Health scores and dimension data are internal-only — never in client copy
7. 60-day contractual minimum — default effective date July 19, 2026 (90 days for annual contracts)
8. `support_fire = TRUE` is a flag, not a blocker — draft always proceeds, operator decides send timing

---

## Account Routing Reference

`_master-account-data-v6.2.csv` — authoritative source for health scores, migration drivers, flags, and legacy billing breakdown.

`migration_comm_tiers_2026-05-19.csv` — all 109 accounts with `comm_action`, `delta_pct`, `delta_mrr`, `health_band`, and routing flags.
