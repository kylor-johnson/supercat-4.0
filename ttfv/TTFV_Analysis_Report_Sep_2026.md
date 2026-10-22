# TTFV Analysis Report - September 2026
**Generated:** October 22, 2026

---

## Executive Summary

September 2026 trailing 90-day TTFV is **86 days**, from one client: **Legrand US (`leg`)**.

**111Mercer (`mer`)** was evaluated in the same pass. It stays out of the September average. Submitted orders are real and they are in October, after the window closed on 2026-09-30. No non-admin on `mer` has a stack or email-draft event, which is what this metric counts.

No active org has a subscription `start_date` in September 2026. `leg` and `mer` have organization rows and no `subscriptions` row, so this run clocks them from the HubSpot closed-won date. The 86-day figure is live Mixpanel plus that close date. A subscription-clock TTFV cannot be computed until those rows exist.

[from-live] Mixpanel `supercat-data-pipeline.mixpanel.events`; Postgres `org_users.is_admin`; HubSpot `deal.properties_closedate`. Confidence **STRONG** on the HubSpot clock. Subscription-clock TTFV for these two orgs is **NONE**.

### What counted

TTFV is days from the closed-won date to the first qualifying event by a user with `org_users.is_admin = false`:

- **Presentation (Stack):** `item_added_via_magic_button`
- **Email Draft:** `document_email_drafted` or `item_email_drafted`

Users with events and no `org_users` row are excluded. The September window is first-value dates from **2026-07-02** through **2026-09-30**.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **September 2026 subscription starts** | 0 |
| **Orgs evaluated by request** | 2 (`leg`, `mer`) |
| **Orgs with valid TTFV** | 1 (`leg`) |
| **Orgs with no stack/email TTFV** | 1 (`mer`; submitted orders are in October) |
| **Clients in the Sep-26 trailing window** | 1 |
| **Trailing 90-day TTFV** | **86 days** (`=86/1`) |
| **Start date reference** | HubSpot closed-won (no subscription row) |

August 2026 was missing from the series and uses the same three clients as July. Their recorded first-value dates still sit inside the August window (2026-06-02 through 2026-08-31): `=(329+35+92)/3` = **152 days** (`pebl+libco+drf`).

---

## September window

| Organization Name | Org | TTFV (Days) | Action Type | Close Date | First Action Date | TTFV user | In window |
|-------------------|-----|-------------|-------------|------------|-------------------|-----------|-----------|
| Legrand US | leg | **86** | Email Draft | 2026-06-11 | 2026-09-05 | `sschwartz1` | Yes |
| 111Mercer | mer | - | - | 2026-08-04 | - | - | No |

The `mer` row is the stack/email clock. Submitted orders are in the section below: 25 orders on October 16–20, including 4 by non-admin `rmcollected` on October 17–18.

`sschwartz1` is on `leg` with `is_admin = false`. The event is `document_email_drafted` on 2026-09-05. Earlier `leg` events are `jonv`, `kjael`, and `kylor_johnson` (admins) and `swt` (no `org_users` row).

HubSpot deal for `leg`: **Legrand - Showroom TIER 1**, closed won 2026-06-11, `properties_existing_client_org_id = leg`.

---

## 111Mercer (`mer`)

`mer` submitted **25 orders** from 2026-10-16 through 2026-10-20. [from-live] Postgres `orders`, `is_submitted = true`, `submit_date`.

| Week | Dates | Orders | Who |
|------|-------|--------|-----|
| Last week | 2026-10-16 to 2026-10-18 | **21** | Jen Dolan (`jendolan`, admin) 17; Maria Oloffo (`rmcollected`, non-admin) 4 |
| This week | 2026-10-19 to 2026-10-20 | **4** | Jen Dolan (`jendolan`, admin) 4 |

| Date | User | Admin | Submitted orders |
|------|------|-------|------------------|
| 2026-10-16 | `jendolan` | yes | 3 |
| 2026-10-17 | `jendolan` | yes | 2 |
| 2026-10-17 | `rmcollected` | no | 2 |
| 2026-10-18 | `jendolan` | yes | 12 |
| 2026-10-18 | `rmcollected` | no | 2 |
| 2026-10-19 | `jendolan` | yes | 1 |
| 2026-10-20 | `jendolan` | yes | 3 |

The first non-admin submitted order is Maria Oloffo on **2026-10-17**. From the 2026-08-04 close date that is **74 days**. That date is inside an October trailing window and outside September.

Stack and email-draft events on `mer` are still only admins (`kylor_johnson` on 2026-08-27, `jonv` on 2026-10-15). `jamiegatto` drafted an email on 2026-10-16 under org `wwjc`, so that event is not `mer`.

The closed-won deal **111 Mercer- TIER 1** (2026-08-04) has a blank `properties_existing_client_org_id`. It is mapped here by deal name to shortname `mer`. That field should be set to `mer` in HubSpot.

---

## Who left the trailing window

Recorded first-value dates from the existing series. All three are before 2026-07-02, so they are in August and out of September.

| Org | Recorded TTFV (days) | Recorded first-value date | August window | September window |
|-----|----------------------|---------------------------|---------------|------------------|
| pebl | 329 | 2026-06-12 | In | Out |
| libco | 35 | 2026-06-24 | In | Out |
| drf | 92 | 2026-07-01 | In | Out |

`drf`'s recorded July 1 event belongs to `kateg`, who has no `org_users` row now. Every other `drf` event user is an admin. That does not move a valid `drf` date into September. Prior-month cells were left as recorded.

---

## Key insights

1. **September average is Legrand only.** 86 days, Email Draft, first non-admin action 2026-09-05. Under the 150-day review flag.
2. **111Mercer wrote orders on October 16–20.** 25 submitted orders: 21 by Jen Dolan (`jendolan`, admin) and 4 by Maria Oloffo (`rmcollected`, non-admin) on October 17–18. Those orders sit after the September window. The September cell stays `leg` only.
3. **Neither org is billable in the subscription table.** No `subscriptions` row for `leg` or `mer`. The analysis prompt would drop them until a subscription is provisioned. They are in this run because they were requested.
4. **August held at 152 days.** `pebl`, `libco`, and `drf` had not aged out yet. They age out together in September, and Legrand is the only replacement.

---

## Methodology notes

1. **Window.** A client is in month M when their first valid value date falls from the last day of M minus 90 days through the last day of M. September 2026 is 2026-07-02 through 2026-09-30.
2. **Start date.** HubSpot closed-won `properties_closedate`, earliest won deal that is the initial engagement. `leg` uses 2026-06-11. `mer` uses 2026-08-04. `subscriptions.start_date` is the analysis-prompt clock and is absent for both orgs.
3. **Admin exclusion.** Postgres `org_users.is_admin = true` is excluded. A Mixpanel user with no `org_users` row is excluded (`swt` on `leg`).
4. **Value actions.** `item_added_via_magic_button` → Presentation (Stack). `document_email_drafted` and `item_email_drafted` → Email Draft.
5. **Series files.** `ttfv/2026_clients_trailing_90day_ttfv.csv` and `ttfv/2026_clients_trailing_90day_ttfv_calculation_detail.csv` now have `Aug-26` and `Sep-26`. September clients cell is `leg` only. `mer` is documented in this report and is not in the average.

---

*Report generated using the SuperCat TTFV event rules. Start dates for `leg` and `mer` are HubSpot closed-won dates because no subscription row exists.*
