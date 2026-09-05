# Cursor Prompt: Executive Business Review (EBR) Generator
## SuperCat / eCat · EBR Deck Generator — v3
## Updated: 2026-03-04 with Gabby + Crystorama pipeline findings

---

## Overview

Generate a self-contained HTML presentation and a Markdown reference document
for a SuperCat / eCat Executive Business Review. The output is a scroll-snap
HTML deck used live in customer meetings — not slides in PowerPoint. Dense,
professional, data-rich with zero wasted whitespace.

**Outputs:**
1. `EBR_[AccountName].html` — the live presentation deck
2. `EBR_[AccountName]_reference.md` — structured reference document

---

## DATA SOURCE HIERARCHY — READ THIS FIRST, NEVER DEVIATE

| Metric | Primary Source | Fallback | Never Use |
|--------|---------------|----------|-----------|
| Order count, revenue, AOV | Postgres `orders` table | — | BigQuery |
| Rep attribution (who ordered) | Postgres `orders.rep_first_name + rep_last_name` | BQ only if PG rep fields are null | BQ `order_submitted` as primary |
| Customer names | Postgres `orders.bill_to_company_name` | — | BigQuery |
| Feature adoption (searches, scans, portal, kits) | BigQuery `mixpanel__events` | — | Postgres |
| Logins / active users | BigQuery `selected_org` events | — | Postgres |
| Rep concentration % | Derived from Postgres rep revenue | — | BQ event counts |
| Licensed user count | Postgres `org_users` + `user_types` | — | Any other source |

**Why this matters:** Not all orgs fire Mixpanel `order_submitted` reliably.
Crystorama (clm) had 149 Postgres orders but only 2 BQ `order_submitted` events.
BQ is telemetry. Postgres `orders` is the system of record.
Always trust Postgres for anything order or revenue related.

### Rep Attribution Validation Gate

After pulling data, always compare:
- Postgres order count (from canonical query)
- BQ `order_submitted` count (from mixpanel__events)

**Rule:** If BQ `order_submitted` < 50% of Postgres order count →
use Postgres `rep_first_name + rep_last_name` for ALL rep slides.
BQ is still valid for feature adoption metrics only.

---

## TTM DATE RANGE — ALWAYS USE THIS LOGIC

TTM = last 12 **complete** months ending on the last complete month.
Never include a partial current month in client-facing revenue figures.

```python
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

_today = date.today()
_end_of_last_month = _today.replace(day=1) - timedelta(days=1)
_start_of_ttm = _end_of_last_month.replace(day=1) - relativedelta(months=11)

START_DATE = _start_of_ttm.isoformat()       # e.g. "2025-03-01"
END_DATE = (_end_of_last_month + timedelta(days=1)).isoformat()  # e.g. "2026-03-01"
```

For a March 2026 run: `START_DATE = "2025-03-01"`, `END_DATE = "2026-03-01"`
Never use `date.today()` as END_DATE. Never use `{year}-01-01` as START_DATE.
Never label anything "YTD" — always "TTM" or named window.

---

## LICENSED USER FILTER — ALWAYS USE THIS LOGIC

Licensed users = sales reps who actively use the iPad app.
The denominator for adoption rate. Must be tight.

**Include:**
- `ut.allow_ipad_logins = true`
- `u.disabled = false`
- Exclude internal SuperCat accounts

**Always exclude these user type patterns:**
```sql
AND ut.name NOT IN ('z-SuperCat', 'Automation', 'Meridian')
AND ut.name NOT LIKE 'Employee%'
AND ut.name NOT LIKE 'Customer%'
AND ut.name NOT LIKE 'Touchscreen%'
AND ut.name NOT LIKE 'IMAP%'
AND ut.name NOT LIKE 'eCat%'
AND u.email NOT IN ('kylor@supercat.io','brent@supercat.io','cwiebe@supercat.io')
```

**Exception:** Some orgs use location-based user types for retail store reps
(e.g. SC Retail uses "Pelham Outlet", "Atlanta", "Nashville" etc. as user types).
These ARE real reps and should be included. The filter above handles this correctly
since they don't match any exclusion pattern.

**Validation:** After filtering, licensed count should feel right for the team size.
If adoption rate shows > 100% or < 50% something is wrong — check the denominator.

---

## REVENUE QUERY — CANONICAL (never change this)

Always use line-item `extended_price` from `order_items` JSON blob.
Never use `orders.total` (includes shipping/tax — inflated).
Always deduplicate order revisions via suffix logic.

```sql
WITH base_orders AS (
  SELECT
    o.id, o.order_number, o.submit_date::text AS submit_date,
    o.order_type, o.order_source,
    COALESCE(o.rep_first_name,'') || ' ' || COALESCE(o.rep_last_name,'') AS rep_name,
    o.customer_num, o.bill_to_company_name,
    COALESCE(
      (SELECT SUM((item->>'extended_price')::numeric)
       FROM jsonb_array_elements(o.order_items::jsonb) AS item
       WHERE item->>'extended_price' IS NOT NULL), 0
    ) AS line_item_revenue,
    SPLIT_PART(o.order_number,'-',1)||'-'||
      SPLIT_PART(o.order_number,'-',2)||'-'||
      SPLIT_PART(o.order_number,'-',3) AS main_part,
    CASE
      WHEN array_length(string_to_array(o.order_number,'-'),1) <= 3 THEN -1
      WHEN SPLIT_PART(o.order_number,'-',4) ~ '^\d+$'
        THEN SPLIT_PART(o.order_number,'-',4)::int
      ELSE 0
    END AS suffix_ord
  FROM orders o
  JOIN organizations org ON o.organization_id = org.id
  WHERE org.shortname = '[SHORTNAME]'
    AND o.submit_date >= '[START_DATE]'
    AND o.submit_date < '[END_DATE]'
    AND o.is_submitted = true
    AND COALESCE(o.is_marked_deleted, false) = false
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY main_part ORDER BY suffix_ord DESC) AS rn
  FROM base_orders
)
SELECT id, submit_date, order_type, order_source, rep_name,
       customer_num, bill_to_company_name, line_item_revenue
FROM ranked WHERE rn = 1
```

---

## ACCOUNT DISCOVERY — RUN BEFORE EVERY NEW ACCOUNT

Before generating any deck for a new org shortname, run these:

```sql
-- 1. Org identity
SELECT id, name, shortname, created_at
FROM organizations WHERE shortname = '[SHORTNAME]'

-- 2. User types (determines licensed filter and product usage)
SELECT ut.name, ut.allow_ipad_logins, COUNT(*) as cnt
FROM org_users ou
JOIN users u ON ou.user_id = u.id
JOIN user_types ut ON ou.user_type_id = ut.id
JOIN organizations o ON ou.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]' AND u.disabled = false
GROUP BY ut.name, ut.allow_ipad_logins ORDER BY cnt DESC

-- 3. Do they have orders?
SELECT COUNT(*) as order_count, MAX(submit_date) as last_order
FROM orders o JOIN organizations org ON o.organization_id = org.id
WHERE org.shortname = '[SHORTNAME]'
  AND o.is_submitted = true
  AND COALESCE(o.is_marked_deleted, false) = false

-- 4. eCat Online?
SELECT enabled, public_enabled FROM mobile_sites ms
JOIN organizations o ON ms.organization_id = o.id
WHERE o.shortname = '[SHORTNAME]'
```

**Deck type from results:**
- Has orders + iPad users → full deck (revenue + engagement)
- No orders, has BQ events → engagement-only (skip revenue slides)
- Neither → stop and flag

---

## SINGLE ORG vs MULTI-ORG DECK RULES

### Single org (most clients)
- Remove cross-entity comparison language from all slide titles and content
- Slide 7 "Four Divisions, Four Patterns" → "Performance — Trailing 12 Months"
- Slide 8 cross-entity rep table → single org top reps leaderboard
- Slide 11 "How Your Divisions Compare" → "Feature Usage — Trailing 12 Months"
- Slide 17 "Cross-Entity Playbook" → "What Good Looks Like" or remove

### Multi-org (e.g. Gabby / Summer Classics = gh, sc, scw, sccon)
- All cross-entity slides active
- Cross-entity rep deduplication required (same rep may appear in multiple orgs)
- Account-level totals = sum across all orgs
- Licensed user total = sum across all orgs (no dedup needed — different org accounts)

### CRITICAL: No hardcoded entity names in HTML generation code
Every entity reference in the HTML output must use dynamic variables
(`entity_labels[code]`, `entity_codes`, etc). Never hardcode "Gabby",
"SC Wholesale", "SC Retail", "SC Contract" or any client name in the
generation logic. These must come from the `ENTITIES` config.

---

## Design System

### Colors
```css
--dk: #1E3A2F        /* dark green */
--md: #4A7C59        /* medium green */
--gold: #C9A84C      /* gold */
--cream: #F7F5F0     /* cream */
--wh: #FFFFFF        /* white */
--red: #C45D5D       /* red */
--dk-text: #E8E4DC   /* off-white */
--lt-text: #2A2A2A   /* near-black */
--muted: #7A7A6E     /* muted gray */
```

### Typography
- Headings: Georgia serif
- Body: DM Sans
- Mono / Labels: DM Mono
- Google Fonts: `DM Sans (400,500,700) + DM Mono (400,500)`

### Slide Themes
- `.s-dk` — dark green, off-white text
- `.s-lt` — cream, dark text
- `.s-wh` — white, dark text

---

## HTML Architecture

```css
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }
section.slide { min-height: 100vh; scroll-snap-align: start; scroll-snap-stop: always; }
```

### Navigation
- Arrow keys / Space / PageDown → next slide
- Arrow Up / PageUp → previous slide
- `N` key → toggle presenter notes overlay
- Slide counter fixed bottom-right, theme-aware

---

## Deck Structure (17 slides + TOC)

1. Title (`.s-dk`)
2. TOC — scroll-snap point, between slide 1 and 2
3. Industry & Company Context (`.s-dk`) — STUB
4. Partnership Overview (`.s-lt`)
5. Platform Coverage (`.s-wh`)
6. Opening Discovery (`.s-dk`) — 3 questions before data
7. Platform Impact (`.s-wh`) — hero numbers
8. Entity Performance + Growth (`.s-lt`) — CONSOLIDATED
9. Sales Team Intelligence (`.s-wh`) — CONSOLIDATED
10. Feature Intelligence (`.s-lt`) — CONSOLIDATED
11. Customer Intelligence (`.s-wh`)
12. Data-Anchored Discovery (`.s-dk`)
13. Growth Opportunities + Cross-Entity Playbook (`.s-wh`) — CONSOLIDATED
14. Feature Roadmap (`.s-lt`)
15. Housekeeping + Next Steps (`.s-wh`) — CONSOLIDATED
16. Closing (`.s-dk`)
17. Appendix A1: Instance Health (`.s-lt`) — STUB
18. Appendix A2: Rep Activity Detail (`.s-wh`)

---

## Strict Rules

1. **No YTD anywhere** — TTM or named window only
2. **No Flipbook** — deprecated, remove from all slides
3. **No hardcoded entity names** — all dynamic from config
4. **No assumption-based framing** — "first time we've..." etc.
5. **Postgres wins for orders/revenue/reps** — always
6. **Rep attribution validation gate** — run it, document result in GenerationNotes
7. **TTM ends on last complete month** — never today's date
8. **Licensed users = sales reps only** — exclude Employee%, Customer%, Touchscreen%, IMAP%, eCat%, z-SuperCat, Automation, Meridian
9. **Stubs over fabrication** — missing data = labeled stub, never invented value
10. **Every slide has presenter notes** — timing + talking points
11. **Single org decks adapt** — remove/rename cross-entity slides

---

## Market Calendar (apply to every growth metric)

```
PRIORITY 1 — Always flag when comparison window overlaps:
Atlanta Market:            Jan 13–19 | Jul 14–20
Dallas Total Home & Gift:  Jan 7–13  | Jun 24–30
Artisan Resource @ NY NOW: Feb 1–3   | Aug 2–4
NeoCon:                    Jun 8–10
High Point Market (Fall):  Oct 17–21
Furniture Today:           December

STANDARD — Note when relevant:
Las Vegas Market:          Jan 25–29 | Jul 26–30
High Point Market (Spring): Apr 25–29
ICFF:                      May 17–19
LightFair:                 May
BDNY:                      Nov 8–9
```

**Rules:**
- Every growth % shown → check if window overlaps Priority 1 event → add `[Market-Driven]` tag
- Every decline → check if prior period had Priority 1 event → label `[Post-Market Normalization]`
- Never imply structural trend from seasonal data

---

## Variable Inputs

| Token | Description | Example |
|-------|-------------|---------|
| `[SHORTNAME]` | Org shortname(s) | `clm` or `gh,sc,scw,sccon` |
| `[AccountName]` | Display name | `Crystorama` |
| `[Month Year]` | Presentation month | `March 2026` |
| `[START_DATE]` | TTM start | `2025-03-01` |
| `[END_DATE]` | TTM end (exclusive) | `2026-03-01` |

---

## Output Quality Checklist

- [ ] All 17 slides present and in correct order
- [ ] TOC between slide 1 and 2, scroll-snap point
- [ ] No "YTD" anywhere
- [ ] No Flipbook references
- [ ] No hardcoded entity names in HTML generation
- [ ] TTM dates = last 12 complete months ending last complete month
- [ ] Licensed users filtered correctly (reps only, ~94% adoption expected)
- [ ] Rep data source validated — Postgres vs BQ gate passed
- [ ] Rep concentration from Postgres revenue, not BQ events
- [ ] Every slide has presenter notes
- [ ] Market calendar checked on every growth metric
- [ ] No fabricated data — stubs for missing fields
- [ ] GenerationNotes shows data sources, rep attribution source, no CSVs
