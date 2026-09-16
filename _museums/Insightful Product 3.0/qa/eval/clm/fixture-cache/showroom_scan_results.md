# Showroom / Operational Account Scan — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-12 | **Source**: Postgres `orders` (LTM, submitted, not deleted)
- **Confirmed exclusions**: 1 | **Aggregate excluded GMV**: $8,084.00 (2 orders)

## Pass 1 — Keyword scan (showroom/admin/marketing/training/test/demo/helper/office)

| rep_name | order_count | gmv | Classification |
|---|---|---|---|
| HighPoint Showroom | 2 | $8,084.00 | **Confirmed operational** — "Showroom" keyword + physical-venue naming + 1 unique customer. Exclude from rep leaderboard/archetype; orders still count in org eCat GMV. |

## Pass 1b — Non-person entity scan (across Q-01 Step 2 rep names)

| rep_name | order_count | gmv | Classification |
|---|---|---|---|
| Dunn Lighting | 1 | $316.00 | **Ambiguous — flagged for CSM review** — contains "Lighting" (non-person pattern) but could be a multi-line rep agency. Name alone insufficient → **retained** in leaderboard. |

## Pass 2 — Brand-name showroom scan (ILIKE '%Crystorama%')

- No rep_first_name/last_name matches on the org brand name "Crystorama". No additional showroom records found.

## Outcome

- `SHOWROOM_EXCLUSIONS` = 1 (HighPoint Showroom).
- HighPoint Showroom is excluded from the §2 rep leaderboard and archetype analysis; its orders remain in total org eCat GMV.
- Dunn Lighting retained (ambiguous, CSM review flag only).
