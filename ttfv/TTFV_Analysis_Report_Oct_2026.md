# TTFV Monthly Report — October 2026
**Generated:** November 4, 2026
**Run:** November 1 monthly update, for the October window
**Universe:** every org with Organization Status Active as of 2026-11-04, after demo, test, staging, sandbox, and template shortnames are removed. That is 120 orgs. `leg` was set to Active for this run. Finance still has to add the subscription rows for `leg` and `mer`. A missing subscription did not keep either org out of this run.

**Confidence:** STRONG on the October cell. [from-live] as of 2026-11-04. Qualifying events are a non-admin presentation, email draft, or `order_submitted`, whichever comes first. Columns through Sep-26 do not include orders.

## Result

October trailing 90-day TTFV is **80 days**, from two clients.

`=(86+74)/2`

| | |
|---|---|
| Window | 2026-08-02 through 2026-10-31 |
| Legrand US (`leg`) | 86 days. HubSpot close 2026-06-11. First value `sschwartz1`, `document_email_drafted`, 2026-09-05, not an admin. No non-admin has submitted an order on `leg`. |
| 111Mercer (`mer`) | 74 days. HubSpot close 2026-08-04, deal "111 Mercer- TIER 1", org id still blank. First value `rmcollected`, `order_submitted`, 2026-10-17. `is_admin` false, user group Sales Reps. Postgres has the submitted iPad orders `161700-101726-17` and `161700-101726-1` that same day. |

`sschwartz1` is the earliest valid user. Earlier events on `leg` are admins (`jonv`, `kjael`, `kylor_johnson`, `abriggs`) or `swt`, who has no `org_users` row.

Legrand's email draft was already inside the September window, so they carry into October at 86 days. Their only order submissions are from admins (`jonv` on 2025-12-12, `kylor_johnson` on 2026-09-03), so the order rule does not move Legrand's date. Pebble, Lib & Co, and Dorell already had a first value before August 2. Other Active orgs that submitted an order in this window already had an earlier non-admin presentation or email, so the new order does not pull them in. 111Mercer is the one that enters because of the order.

## Newly onboarded clients

`libco` and `drf` already have active subscriptions, so they are on the MAL. Both already had a first value before this window (`libco` 2026-06-26, `drf` 2026-07-01), so they are in earlier columns and not in October.

`leg` and `mer` are the ones still missing a subscription row in admin.

| Org | Subscription | October |
|---|---|---|
| Lib and Co. (`libco`) | active, start 2026-05-20 | Already counted in Jul-26 and Aug-26. First value 2026-06-26 is outside this window. |
| Dorell Fabrics (`drf`) | active, start 2026-06-01 | Already counted in Aug-26. First value 2026-07-01 is outside this window. |
| Legrand US (`leg`) | none yet. Status is Active as of 2026-11-04. Finance still needs to add the subscription. | They are the October average. |
| 111Mercer (`mer`) | none yet. Status is Active, created 2026-08-10. | In the October average at 74 days, from `rmcollected` submitting an order on 2026-10-17. `jendolan` submitted more orders starting 2026-10-16 and is flagged admin, so those do not count. |

## Who was checked and left out

Demos whose first qualifying event falls inside the window stay out: Kurt S. Adler (`ksa`, 2026-08-18), `pf_test` (2026-08-25), ADRIANA HOYOS (`adho`, 2026-08-28), Transformer Table (`ttb`, 2026-10-28).

Older Active orgs that the subscription list also missed (`cff`, `hmi`, `gf`, `gg`, `bscc`, `hvusa`, `khi`, `opame`) have first values well before August 2, or no qualifying events. They do not enter October.

`aa`, `blh`, `bmc`, `pol`, and `tcs` are fully suspended and still have an active subscription, so they stay on the MAL. None of them has a first value in the October window.

## Series

Oct-26 on both CSVs: 80.0 days, 2 clients, 160.0 total days, clients `leg+mer`. Formula `=(86+74)/2`.
