# TTFV Monthly Report — October 2026
**Generated:** November 4, 2026
**Run:** November 1 monthly update, for the October window
**Universe:** every org with Organization Status Active as of 2026-11-04, after demo, test, staging, sandbox, and template shortnames are removed. That is 120 orgs. `leg` was set to Active for this run. Finance still has to add the subscription rows for `leg` and `mer`. A missing subscription did not keep either org out of this run.

**Confidence:** STRONG on the October cell. [from-live] as of 2026-11-04. The other 119 Active orgs do not have a first valid non-admin value inside this window, so they are not in the average.

## Result

October trailing 90-day TTFV is **86 days**, from one client.

`=86/1`

| | |
|---|---|
| Window | 2026-08-02 through 2026-10-31 |
| Client | Legrand US (`leg`) |
| Clock | HubSpot close 2026-06-11, deal "Legrand - Showroom TIER 1" |
| First value | `sschwartz1`, `document_email_drafted`, 2026-09-05, `is_admin` false |
| Days | 86 |

`sschwartz1` is the earliest valid user. Earlier events on `leg` are admins (`jonv`, `kjael`, `kylor_johnson`, `abriggs`) or `swt`, who has no `org_users` row.

That first-value date was already inside the September window, so Legrand carries into October. Pebble (`pebl`, 2026-06-12), Lib & Co (`libco`, 2026-06-26), and Dorell (`drf`, 2026-07-01) are already outside it. The October cell matches September because the same one client is still inside the window and nobody new qualified.

## Newly onboarded clients

`libco` and `drf` already have active subscriptions, so they are on the MAL. Both already had a first value before this window (`libco` 2026-06-26, `drf` 2026-07-01), so they are in earlier columns and not in October.

`leg` and `mer` are the ones still missing a subscription row in admin.

| Org | Subscription | October |
|---|---|---|
| Lib and Co. (`libco`) | active, start 2026-05-20 | Already counted in Jul-26 and Aug-26. First value 2026-06-26 is outside this window. |
| Dorell Fabrics (`drf`) | active, start 2026-06-01 | Already counted in Aug-26. First value 2026-07-01 is outside this window. |
| Legrand US (`leg`) | none yet. Status is Active as of 2026-11-04. Finance still needs to add the subscription. | They are the October average. |
| 111Mercer (`mer`) | none yet. Status is active, created 2026-08-10. | Closed won 2026-08-04, deal "111 Mercer- TIER 1", HubSpot org id still blank. The only qualifying users through 2026-10-31 are admins: `kylor_johnson` (2026-08-27) and `jonv` (2026-10-15). No valid TTFV yet, so they are not in the average. |

## Who was checked and left out

Demos whose first qualifying event falls inside the window stay out: Kurt S. Adler (`ksa`, 2026-08-18), `pf_test` (2026-08-25), ADRIANA HOYOS (`adho`, 2026-08-28), Transformer Table (`ttb`, 2026-10-28).

`mer` is the only real client whose first qualifying event is inside the window, and both of its users are admins, so it stays out of the average.

Older Active orgs that the subscription list also missed (`cff`, `hmi`, `gf`, `gg`, `bscc`, `hvusa`, `khi`, `opame`) have first values well before August 2, or no qualifying events. They do not enter October.

`aa`, `blh`, `bmc`, `pol`, and `tcs` are fully suspended and still have an active subscription, so they stay on the MAL. None of them has a first value in the October window.

## Series

Oct-26 is now on both CSVs. Detail row: 86.0 days, 1 client, 86.0 total days, client `leg`.
