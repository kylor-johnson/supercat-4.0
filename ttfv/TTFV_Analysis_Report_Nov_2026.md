# TTFV Analysis Report - All Active Clients
**Generated:** November 4, 2026

---

## Executive Summary

This report calculates **Time to First Value (TTFV)** for every active SuperCat client. TTFV is the number of days from subscription start to the first time a **non-admin sales rep** performed a value-generating action:
- **Presentation/Stack**: Added a product via magic button (`item_added_via_magic_button`)
- **Email Draft**: Drafted an email from the platform (`document_email_drafted` / `item_email_drafted`)

### Start Date Methodology
- **Source of truth**: Postgres `subscriptions.start_date` (`MIN(start_date)` per org where `status = 'active'`)
- HubSpot deal close dates and `organizations.created_at` are not used

### Important Caveat — August 2025 Subscription Provisioning
Most orgs with a valid TTFV (92 of 106) share a subscription `start_date` in **August 2025** (bulk billing provisioning). Many of those orgs had Mixpanel value activity earlier (tracking from about November 2024), so **TTFV is negative** for most of the book. Negative TTFV means first value occurred before the subscription row's start date. It is an activity signal, not onboarding latency.

For onboarding performance, prioritize:
1. Orgs with **non-negative TTFV**
2. Orgs with `start_date` **on or after 2025-09-01** (post-bulk)
3. Orgs with **no valid TTFV / no events**

**Confidence:** STRONG, from live Postgres and Mixpanel on November 4, 2026. The book-wide average inherits the August 2025 clock distortion, so it is not an onboarding KPI. The non-negative and post-bulk figures are the ones to use.

**Note:** TTFV is valid only for a user with `org_users.is_admin = FALSE`. A Mixpanel user with no `org_users` row for that org is excluded, and the next earliest qualifying user is used.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Active Orgs** | 114 |
| **Orgs with Valid TTFV** | 106 |
| **Orgs with No Valid TTFV** | 5 |
| **Orgs with No TTFV Events** | 3 |
| **Start Date Reference** | `subscriptions.start_date` (all) |
| **Average TTFV (all valid)** | -253.7 days |
| **Median TTFV (all valid)** | -295 days |
| **Negative TTFV count** | 98 |
| **Non-negative TTFV count** | 8 |
| **Avg TTFV (non-negative only)** | 117.3 days |
| **Median TTFV (non-negative only)** | 84 days |
| **Post-bulk orgs (start ≥ 2025-09-01)** | 19 |
| **Post-bulk with valid TTFV** | 14 |
| **Avg TTFV (post-bulk, non-negative)** | 84.7 days |
| **Median TTFV (post-bulk, non-negative)** | 44.5 days |

The non-negative median is the midpoint of 49 and 119. The post-bulk non-negative median is the midpoint of 40 and 49.

---

## Non-Negative TTFV (Most Actionable)

These orgs recorded first non-admin value **on or after** their subscription start date:

| Organization Name | TTFV (Days) | Action Type | Start Date | First Action Date | Start Date Reference |
|-------------------|-------------|-------------|------------|-------------------|----------------------|
| Globalux Lighting & Fans | **17** | Email Draft | 2025-11-25 | 2025-12-12 | subscriptions.start_date |
| Lib and Co. | **37** | Presentation (Stack) | 2026-05-20 | 2026-06-26 | subscriptions.start_date |
| Coleto Brands / Progress Lighting | **40** | Presentation (Stack) | 2025-12-01 | 2026-01-10 | subscriptions.start_date |
| Coaster Furniture | **49** | Email Draft | 2025-12-01 | 2026-01-19 | subscriptions.start_date |
| Jonathan Charles Fine Furniture | **119** | Email Draft | 2025-11-25 | 2026-03-24 | subscriptions.start_date |
| Sabine Pools, Spas, & Furnitur | **187** | Presentation (Stack) | 2025-08-29 | 2026-03-04 | subscriptions.start_date |
| Butler Specialty Company | **243** | Email Draft | 2025-08-25 | 2026-04-25 | subscriptions.start_date |
| Skyard Furniture Co Ltd. | **246** | Email Draft | 2025-10-09 | 2026-06-12 | subscriptions.start_date |

#### Non-Negative TTFV Statistics
- **Best TTFV:** 17 days (Globalux Lighting & Fans)
- **Average TTFV:** 117.3 days
- **Median TTFV:** 84 days (midpoint of 49 and 119)
- **Slowest:** 246 days (Skyard Furniture Co Ltd.)

---

## Post-Bulk Cohort (start_date ≥ 2025-09-01)

| Organization Name | Org | TTFV (Days) | Action Type | Start Date | First Action Date | Notes |
|-------------------|-----|-------------|-------------|------------|-------------------|-------|
| Groupe Courchesne | gc | **-606** | Email Draft | 2026-06-30 | 2024-11-01 | Pre-start activity |
| Charleston Forge | cfg | **-467** | Email Draft | 2026-02-11 | 2024-11-01 | Pre-start activity |
| Kennedy International, Inc. | kii | **-424** | Email Draft | 2026-01-01 | 2024-11-03 | Pre-start activity |
| Arabela Lighting | arl | **-403** | Presentation (Stack) | 2026-07-01 | 2025-05-24 | Pre-start activity |
| Moda at Home Enterprises Ltd | mah | **-386** | Email Draft | 2025-12-10 | 2024-11-19 | Pre-start activity |
| Lucas McKearn | luc | **-369** | Email Draft | 2026-07-01 | 2025-06-27 | Pre-start activity |
| Theodore Alexander Manhasset | tam | **-27** | Email Draft | 2025-09-01 | 2025-08-05 | Pre-start activity |
| Terracotta Designs | tcd | **-8** | Email Draft | 2026-05-01 | 2026-04-23 | Pre-start activity |
| Globalux Lighting & Fans | gblx | **17** | Email Draft | 2025-11-25 | 2025-12-12 |  |
| Lib and Co. | libco | **37** | Presentation (Stack) | 2026-05-20 | 2026-06-26 |  |
| Coleto Brands / Progress Lighting | prog | **40** | Presentation (Stack) | 2025-12-01 | 2026-01-10 |  |
| Coaster Furniture | cst | **49** | Email Draft | 2025-12-01 | 2026-01-19 |  |
| Jonathan Charles Fine Furniture | jc | **119** | Email Draft | 2025-11-25 | 2026-03-24 | Needs attention |
| Skyard Furniture Co Ltd. | pebl | **246** | Email Draft | 2025-10-09 | 2026-06-12 | Needs attention |
| Abroad Home Furnishings | aa | — | — | 2026-03-01 | — | No TTFV events |
| Dorell Fabrics | drf | — | — | 2026-06-01 | — | Admin-only or no org membership on event users |
| Kaleen Rugs & Broadloom | krb | — | — | 2025-11-25 | — | Admin-only or no org membership on event users |
| Magic Lite / NSL | mali | — | — | 2025-11-11 | — | No TTFV events |
| The CopperSmith | tcs | — | — | 2026-04-15 | — | No TTFV events |

---

## Complete TTFV Results

| Organization Name | Org | TTFV (Days) | Action Type | Start Date | First Action Date | Start Date Reference |
|-------------------|-----|-------------|-------------|------------|-------------------|----------------------|
| Groupe Courchesne | gc | **-606** | Email Draft | 2026-06-30 | 2024-11-01 | subscriptions.start_date |
| Charleston Forge | cfg | **-467** | Email Draft | 2026-02-11 | 2024-11-01 | subscriptions.start_date |
| Kennedy International, Inc. | kii | **-424** | Email Draft | 2026-01-01 | 2024-11-03 | subscriptions.start_date |
| Arabela Lighting | arl | **-403** | Presentation (Stack) | 2026-07-01 | 2025-05-24 | subscriptions.start_date |
| Moda at Home Enterprises Ltd | mah | **-386** | Email Draft | 2025-12-10 | 2024-11-19 | subscriptions.start_date |
| Lucas McKearn | luc | **-369** | Email Draft | 2026-07-01 | 2025-06-27 | subscriptions.start_date |
| Baker-McGuire | big | **-301** | Email Draft | 2025-08-29 | 2024-11-01 | subscriptions.start_date |
| Hudson Valley Lighting | hvl | **-301** | Presentation (Stack) | 2025-08-29 | 2024-11-01 | subscriptions.start_date |
| Wildwood/Chelsea House | wwjc | **-301** | Email Draft | 2025-08-29 | 2024-11-01 | subscriptions.start_date |
| Gabriella White | sc | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Summer Classics | scw | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Visual Comfort - Modern | tla | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Visual Comfort - Studio /Fans | fms | **-299** | Presentation (Stack) | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Visual Comfort Signature | vcg | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Corbett Lighting | cl | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Dainolite Ltd. | da | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Fine Art Handcrafted Lighting | fal | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Four Seasons Furniture | fsf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Furniture Classics | fc | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Gabby | gh | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Godinger Silver Art Co. | gsa | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Golden Lighting | gl | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Hooker Furnishings | hf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Hubbardton Forge | hfg | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Interlude Furniture | ihw | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Interlude Home | ih | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Kalco Lighting / Allegri Crystal | kal | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Kuzco Lighting Inc. | kll | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Linon/Powell Furniture | lpf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Maxim Lighting | mli | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Palecek | pf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Ricci Argentieri Company | rac | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Rowe Furniture | rf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Sarreid, Ltd. | sarreid | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Schonbek Lighting | sbl | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Silver One | soi | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Somerset Bay and Modern History | sbmh | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Theodore Alexander | ta | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Troy Lighting | tl | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Universal Furniture | ufi | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Accord Lighting | all | **-297** | Presentation (Stack) | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Alfresco Home | ah | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Bassett Mirror | bmc | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Braxton Culler | bcf | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Capital Lighting Fixture Co. | clc | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Craftmade | clli | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Crystorama | clm | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Currey & Company | cci | **-297** | Presentation (Stack) | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Banner House | mh | **-297** | Email Draft | 2025-08-26 | 2024-11-02 | subscriptions.start_date |
| Jamie Young Company | jyc | **-297** | Email Draft | 2025-08-26 | 2024-11-02 | subscriptions.start_date |
| Ciana Varaluz LLC | vl | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Donald Choi Canada | dccl | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| ELICO LTD. | etl | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Elegant Furniture & Lighting | eli | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Millennium Lighting | ml | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Morgan Fabrics Corporation | mfc | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Pioneer Morton | mpc | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Sauder Woodworking | swc | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| WAC/Modern Forms Lighting | wac | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Summer Classics Contract | sccon | **-295** | Email Draft | 2025-08-27 | 2024-11-05 | subscriptions.start_date |
| Access Lighting | ali | **-294** | Presentation (Stack) | 2025-08-25 | 2024-11-04 | subscriptions.start_date |
| Eurofase Inc. | el | **-294** | Email Draft | 2025-08-26 | 2024-11-05 | subscriptions.start_date |
| Savoy House Lighting | shl | **-294** | Email Draft | 2025-08-26 | 2024-11-05 | subscriptions.start_date |
| Century Furniture | cf | **-293** | Email Draft | 2025-08-25 | 2024-11-05 | subscriptions.start_date |
| DALS Lighting | dals | **-293** | Email Draft | 2025-08-26 | 2024-11-06 | subscriptions.start_date |
| Home Essentials & Beyond | heb | **-292** | Email Draft | 2025-08-26 | 2024-11-07 | subscriptions.start_date |
| AFX, Inc. | afx | **-291** | Email Draft | 2025-08-25 | 2024-11-07 | subscriptions.start_date |
| Geo Contemporary | gcl | **-291** | Email Draft | 2025-08-26 | 2024-11-08 | subscriptions.start_date |
| Jonathan Charles Designs Inc. | jcusa | **-291** | Email Draft | 2025-08-26 | 2024-11-08 | subscriptions.start_date |
| Kindel Karges Furniture | kkc | **-289** | Email Draft | 2025-08-29 | 2024-11-13 | subscriptions.start_date |
| Matteo Lighting | mlc | **-288** | Email Draft | 2025-08-26 | 2024-11-11 | subscriptions.start_date |
| Ratana International Ltd. | ril | **-288** | Email Draft | 2025-08-26 | 2024-11-11 | subscriptions.start_date |
| Shadow Catchers | sca | **-288** | Email Draft | 2025-08-26 | 2024-11-11 | subscriptions.start_date |
| Visual Comfort & Co. | vce | **-287** | Presentation (Stack) | 2025-08-27 | 2024-11-13 | subscriptions.start_date |
| Designer's Fountain | df | **-286** | Email Draft | 2025-08-26 | 2024-11-13 | subscriptions.start_date |
| Bulbrite | bri | **-283** | Email Draft | 2025-08-25 | 2024-11-15 | subscriptions.start_date |
| Highland House | hh | **-278** | Email Draft | 2025-08-25 | 2024-11-20 | subscriptions.start_date |
| Abaline Supply Inc. | asi | **-274** | Email Draft | 2025-08-25 | 2024-11-24 | subscriptions.start_date |
| Alden Home | ap | **-273** | Email Draft | 2025-08-25 | 2024-11-25 | subscriptions.start_date |
| Studio Silversmiths, Inc. | ssi | **-273** | Email Draft | 2025-08-26 | 2024-11-26 | subscriptions.start_date |
| Coleto Brands / Kichler | kl | **-272** | Presentation (Stack) | 2025-08-26 | 2024-11-27 | subscriptions.start_date |
| Vaxcel International Corporation | vic | **-263** | Email Draft | 2025-08-26 | 2024-12-06 | subscriptions.start_date |
| Yutzy Woodworking | yw | **-263** | Email Draft | 2025-08-26 | 2024-12-06 | subscriptions.start_date |
| Uniware Housewares Corp. | uhc | **-260** | Email Draft | 2025-08-26 | 2024-12-09 | subscriptions.start_date |
| PageOne Lighting | pol | **-251** | Email Draft | 2025-08-26 | 2024-12-18 | subscriptions.start_date |
| RENWIL | rw | **-231** | Email Draft | 2025-08-26 | 2025-01-07 | subscriptions.start_date |
| Thesis USA | eglo | **-225** | Email Draft | 2025-08-26 | 2025-01-13 | subscriptions.start_date |
| Thesis Canada | eglo_can | **-224** | Email Draft | 2025-08-26 | 2025-01-14 | subscriptions.start_date |
| Lifestyle Solutions | lss | **-221** | Email Draft | 2025-08-26 | 2025-01-17 | subscriptions.start_date |
| America's Backyards | abol | **-202** | Email Draft | 2025-08-25 | 2025-02-04 | subscriptions.start_date |
| International Home Miami | ihm | **-180** | Presentation (Stack) | 2025-08-26 | 2025-02-27 | subscriptions.start_date |
| Buster & Punch | bp | **-178** | Presentation (Stack) | 2025-08-25 | 2025-02-28 | subscriptions.start_date |
| Wendover Art Group | wag | **-165** | Email Draft | 2025-08-26 | 2025-03-14 | subscriptions.start_date |
| Alfonso Marina & CIA | am | **-136** | Email Draft | 2025-08-25 | 2025-04-11 | subscriptions.start_date |
| Philip Whitney | pw | **-134** | Email Draft | 2025-08-26 | 2025-04-14 | subscriptions.start_date |
| Minka Lighting | mlg | **-124** | Presentation (Stack) | 2025-08-26 | 2025-04-24 | subscriptions.start_date |
| Theodore Alexander Manhasset | tam | **-27** | Email Draft | 2025-09-01 | 2025-08-05 | subscriptions.start_date |
| Terracotta Designs | tcd | **-8** | Email Draft | 2026-05-01 | 2026-04-23 | subscriptions.start_date |
| Globalux Lighting & Fans | gblx | **17** | Email Draft | 2025-11-25 | 2025-12-12 | subscriptions.start_date |
| Lib and Co. | libco | **37** | Presentation (Stack) | 2026-05-20 | 2026-06-26 | subscriptions.start_date |
| Coleto Brands / Progress Lighting | prog | **40** | Presentation (Stack) | 2025-12-01 | 2026-01-10 | subscriptions.start_date |
| Coaster Furniture | cst | **49** | Email Draft | 2025-12-01 | 2026-01-19 | subscriptions.start_date |
| Jonathan Charles Fine Furniture | jc | **119** | Email Draft | 2025-11-25 | 2026-03-24 | subscriptions.start_date |
| Sabine Pools, Spas, & Furnitur | sp | **187** | Presentation (Stack) | 2025-08-29 | 2026-03-04 | subscriptions.start_date |
| Butler Specialty Company | bsc | **243** | Email Draft | 2025-08-25 | 2026-04-25 | subscriptions.start_date |
| Skyard Furniture Co Ltd. | pebl | **246** | Email Draft | 2025-10-09 | 2026-06-12 | subscriptions.start_date |
| Oly Studio | ol | - | - | 2025-08-26 | - | No Valid TTFV |
| Sixtrees Limited | st | - | - | 2025-08-26 | - | No Valid TTFV |
| Bliss Studio | blh | - | - | 2025-08-29 | - | No Valid TTFV |
| Kaleen Rugs & Broadloom | krb | - | - | 2025-11-25 | - | No Valid TTFV |
| Dorell Fabrics | drf | - | - | 2026-06-01 | - | No Valid TTFV |
| Magic Lite / NSL | mali | - | - | 2025-11-11 | - | No TTFV Events |
| Abroad Home Furnishings | aa | - | - | 2026-03-01 | - | No TTFV Events |
| The CopperSmith | tcs | - | - | 2026-04-15 | - | No TTFV Events |

---

## Orgs Without Valid TTFV

| Organization Name | Org | Start Date | Reason |
|-------------------|-----|------------|--------|
| Oly Studio | ol | 2025-08-26 | Admin-only or event users have no `org_users` row on this org |
| Sixtrees Limited | st | 2025-08-26 | Earliest event user has no `org_users` row; the other event user is admin |
| Bliss Studio | blh | 2025-08-29 | Only qualifying event user is an admin |
| Kaleen Rugs & Broadloom | krb | 2025-11-25 | Only qualifying event user is an admin |
| Dorell Fabrics | drf | 2026-06-01 | August TTFV user `KateG` no longer has an `org_users` row. Remaining event users are admins or have no membership |
| Magic Lite / NSL | mali | 2025-11-11 | No TTFV events recorded |
| Abroad Home Furnishings | aa | 2026-03-01 | No TTFV events recorded |
| The CopperSmith | tcs | 2026-04-15 | No TTFV events recorded |

---

## Key Insights

### 1. Bulk start dates still dominate the book
- **92** orgs with a valid TTFV have an August 2025 subscription start date from billing provisioning.
- **98** orgs show negative TTFV (first value before `start_date`).
- Treat the book-wide average and median as **not comparable** to reports that used HubSpot close dates, and not as onboarding latency.
- Many of those first-action dates sit on **2024-11-01**. That is the Mixpanel tracking floor for these events, not evidence the rep's first real selling day was November 1.

### 2. Non-negative TTFV (true post-start adoption)
- **8** orgs have non-negative TTFV.
- **Average: 117.3 days** | **Median: 84 days** (midpoint of 49 and 119)
- **Best:** Globalux Lighting & Fans (17d), Lib and Co. (37d), Coleto Brands / Progress Lighting (40d)
- **Over 60 days:** Jonathan Charles Fine Furniture (119d), Sabine Pools, Spas, & Furnitur (187d), Butler Specialty Company (243d), Skyard Furniture Co Ltd. (246d)

### 3. What changed since the August 4, 2026 report
The active-org set is the same 114 shortnames. No org gained an active subscription after 2026-07-01 (newest starts remain Arabela Lighting and Lucas McKearn).

| Org | What changed | Effect on TTFV |
|-----|----------------|----------------|
| Dorell Fabrics (`drf`) | August user `KateG` has a `users` row and no `org_users` row. Other event users are admins (`kyla`, `kylor_johnson`, `suzf`, `chrissoh`) or have no membership (`jonv`). | Was **30 days** (Presentation). Now **no valid TTFV**. |
| Lib and Co. (`libco`) | August user `rparker2` is no longer a member of `libco` (still a non-admin on other orgs). Next valid user is `davidgarcia`. | **35 → 37 days**. First action 2026-06-24 → 2026-06-26. Still Presentation (Stack). |
| Alden Home (`ap`) | `RaeFisher` is now `is_admin = true`. Next non-admin is `lcrotts`. | Still negative. First action 2024-11-01 → 2024-11-25. Days **-297 → -273**. |
| Gabriella White (`sc`) | The 2025-08-01 subscription row is `canceled`. The active row starts 2025-08-27. Same rep and same first action (2024-11-01, `sc-shiraza`). | Days **-273 → -299** because the clock moved, not because activity changed. |

Live org names also differ from the August report for Thesis USA (`eglo`, previously Eglo USA), Thesis Canada (`eglo_can`), Banner House (`mh`, previously Magnussen Home), Visual Comfort & Co. (`vce`), Minka Lighting (`mlg`), and Alfonso Marina & CIA (`am`). Tables write Coleto Brands / Kichler, Coleto Brands / Progress Lighting, and Magic Lite / NSL. The live `organizations.name` uses a vertical bar in those three names; the JSON and CSV keep that bar.

### 4. Clients needing attention
- **5** admin-only / no valid non-admin TTFV: Oly Studio, Sixtrees Limited, Bliss Studio, Kaleen Rugs & Broadloom, Dorell Fabrics
- **3** no TTFV events: Magic Lite / NSL, Abroad Home Furnishings, The CopperSmith
- **Slow non-negative TTFV (>60 days):** Jonathan Charles Fine Furniture (119d), Sabine Pools, Spas, & Furnitur (187d), Butler Specialty Company (243d), Skyard Furniture Co Ltd. (246d)
- Dorell Fabrics is the new gap. In August it was a 30-day onboarding. The rep who produced that event is no longer on the org.

### 5. Action-type mix (valid TTFV)
- Email Draft: **84** (79.2%)
- Presentation (Stack): **22** (20.8%)

### 6. Legrand US and 111Mercer stay outside this run
`leg` and `mer` have organization rows and no `subscriptions` row. The analysis prompt excludes them until a subscription is active. That was still true on November 4, 2026. The September trailing report clocked those two from HubSpot close dates. This report does not.

---

## Methodology Notes

1. **Start Date:** Postgres `subscriptions.start_date` (`MIN` per org, `status = 'active'` only). Canceled rows are ignored. Gabriella White is the case this rule changes: the older 2025-08-01 row is canceled.
2. **Active org filter:** Excludes demo/test/staging shortnames and the hard-coded exclusion list in `TTFV_Analysis_Prompt.md`. The prompt's `SIMILAR TO` pattern was applied as a case-insensitive regex on `shortname` with the same tokens (`test`, `demo`, `staging`, `sandbox`, `template`).
3. **Admin exclusion:** Users with `is_admin = TRUE` in Postgres `org_users` are excluded. Users with Mixpanel events but no `org_users` row on that org are excluded. The next earliest qualifying user is used. This was checked per candidate user, not assumed from the August file.
4. **Value actions:**
   - `item_added_via_magic_button` → Presentation (Stack)
   - `document_email_drafted` / `item_email_drafted` → Email Draft
5. **Event org key:** `current_organization_shortname` on `supercat-data-pipeline.mixpanel.events`, as specified in the analysis prompt.
6. **Data sources:**
   - Start dates and admin status: SuperCat Postgres (`organizations`, `subscriptions`, `org_users`, `users`)
   - TTFV events: BigQuery `supercat-data-pipeline.mixpanel.events`
7. **Report template:** `TTFV_Report_Format_Template.md` still describes the retired HubSpot / `created_at` clock. This report follows the current prompt and the August 2026 full-book report: one clock, `subscriptions.start_date`. The September 2026 file is the trailing 90-day series, which is a different cohort and clock.

---

*Report generated using SuperCat TTFV Analysis methodology (`subscriptions.start_date`). Figures are [from-live] as of November 4, 2026. Confidence: STRONG for the defined metric. The book-wide average is not an onboarding latency.*
