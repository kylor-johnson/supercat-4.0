# TTFV Monthly Report — October 2026
**Generated:** November 4, 2026
**Run:** November 1 monthly update, for the October window
**Confidence:** STRONG on the October cell. Every figure below is [from-live] as of 2026-11-04.

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

## Orgs the old list missed

The previous full-book run (`TTFV_Analysis_Report_Nov_2026.md`) kept only orgs with an active subscription. These three are in the Organization Status universe and have no subscription row. None of them changes the October average.

| Org | Status | Why they are not in the October average |
|---|---|---|
| Legrand US (`leg`) | onboarding | They are the average. First value 2026-09-05 is inside the window. |
| 111Mercer (`mer`) | active, created 2026-08-10 | Closed won 2026-08-04, deal "111 Mercer- TIER 1", HubSpot org id still blank. The only qualifying users through 2026-10-31 are admins: `kylor_johnson` (2026-08-27) and `jonv` (2026-10-15). No valid TTFV yet. |
| Wind River (`wr`) | active, created 2026-07-08 | No closed-won deal. "Wind River Ceiling Fans - TIER 1" closed 2026-07-23 and is not won, org id blank. The only value event is `jonv` on 2026-07-09, and `jonv` has no `org_users` row on `wr`. That date is also before the window. |

## Who was checked and left out

The org universe for this run is Organization Status `active` or `onboarding`, `sandbox_of_id` null, shortname not matching test/demo/staging/sandbox/template, plus the junk list in the monthly readme. Querying that on 2026-11-04 returns 120 orgs. `leg` is the only real Onboarding org after the junk filter.

Orgs whose first qualifying Mixpanel event falls inside 2026-08-02 through 2026-10-31, and that the status rule correctly excludes:

| Org | Status | First qualifying event |
|---|---|---|
| Kurt S. Adler (`ksa`) | demo | 2026-08-18 |
| `pf_test` | test | 2026-08-25 |
| ADRIANA HOYOS (`adho`) | demo | 2026-08-28 |
| Transformer Table (`ttb`) | demo | 2026-10-28 |

`mer` is the only real client whose first qualifying event is inside the window, and both of its users are admins, so it stays out of the average.

Older Active orgs that the subscription list also missed (`cff`, `hmi`, `gf`, `gg`, `bscc`, `hvusa`, `khi`, `opame`) have first values well before August 2, or no qualifying events. They do not enter October.

Fully suspended orgs drop out of this universe even if they still have a subscription row: `aa`, `blh`, `bmc`, `pol`, `tcs`. None of them has a first value in the October window.

## Series

Oct-26 is now on both CSVs. Detail row: 86.0 days, 1 client, 86.0 total days, client `leg`.
