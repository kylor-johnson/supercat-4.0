# TTFV Analysis Report - All Active Clients
**Generated:** August 4, 2026

---

## Executive Summary

This report calculates the **Time to First Value (TTFV)** for all active SuperCat clients. TTFV measures the number of days from subscription start to the first time a **non-admin sales rep** performed a value-generating action:
- **Presentation/Stack**: Added a product via magic button (`item_added_via_magic_button`)
- **Email Draft**: Drafted an email from the platform (`document_email_drafted` / `item_email_drafted`)

### Start Date Methodology
- **Source of truth**: Postgres `subscriptions.start_date` (`MIN(start_date)` per org where `status = 'active'`)
- HubSpot deal close dates and `organizations.created_at` are **not** used

### Important Caveat — August 2025 Subscription Provisioning
Most active orgs (92 of 107 with valid TTFV) share a subscription `start_date` in **August 2025** (bulk billing provisioning). Many of those orgs had Mixpanel value activity earlier (tracking ~Nov 2024+), so **TTFV is negative** for the majority of the book. Negative TTFV means first value occurred *before* the subscription row's start date — useful as an activity signal, not as onboarding latency.

For onboarding performance, prioritize:
1. Orgs with **non-negative TTFV**
2. Orgs with `start_date` **on/after 2025-09-01** (post-bulk)
3. Orgs with **no valid TTFV / no events**

**Note:** TTFV is only valid when performed by a non-admin user (`org_users.is_admin = FALSE`). Users with Mixpanel events but no `org_users` record are excluded.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Active Orgs** | 114 |
| **Orgs with Valid TTFV** | 107 |
| **Orgs with No Valid TTFV** | 4 |
| **Orgs with No TTFV Events** | 3 |
| **Start Date Reference** | `subscriptions.start_date` (all) |
| **Average TTFV (all valid)** | -251 days |
| **Median TTFV (all valid)** | -295 days |
| **Negative TTFV count** | 98 |
| **Non-negative TTFV count** | 9 |
| **Avg TTFV (non-negative only)** | 107.3 days |
| **Median TTFV (non-negative only)** | 49 days |
| **Post-bulk orgs (start ≥ 2025-09-01)** | 15 |
| **Avg TTFV (post-bulk, non-negative)** | 76.6 days |
| **Median TTFV (post-bulk, non-negative)** | 40 days |

---

## Non-Negative TTFV (Most Actionable)

These orgs recorded first non-admin value **on or after** their subscription start date:

| Organization Name | TTFV (Days) | Action Type | Start Date | First Action Date | Start Date Reference |
|-------------------|-------------|-------------|------------|-------------------|----------------------|
| Globalux Lighting & Fans | **17** | Email Draft | 2025-11-25 | 2025-12-12 | subscriptions.start_date |
| Dorell Fabrics | **30** | Presentation (Stack) | 2026-06-01 | 2026-07-01 | subscriptions.start_date |
| Lib and Co. | **35** | Presentation (Stack) | 2026-05-20 | 2026-06-24 | subscriptions.start_date |
| Coleto Brands / Progress Lighting | **40** | Presentation (Stack) | 2025-12-01 | 2026-01-10 | subscriptions.start_date |
| Coaster Furniture | **49** | Email Draft | 2025-12-01 | 2026-01-19 | subscriptions.start_date |
| Jonathan Charles Fine Furniture | **119** | Email Draft | 2025-11-25 | 2026-03-24 | subscriptions.start_date |
| Sabine Pools, Spas, & Furnitur | **187** | Presentation (Stack) | 2025-08-29 | 2026-03-04 | subscriptions.start_date |
| Butler Specialty Company | **243** | Email Draft | 2025-08-25 | 2026-04-25 | subscriptions.start_date |
| Skyard Furniture Co Ltd. | **246** | Email Draft | 2025-10-09 | 2026-06-12 | subscriptions.start_date |

#### Non-Negative TTFV Statistics
- **Best TTFV:** 17 days (Globalux Lighting & Fans)
- **Average TTFV:** 107.3 days
- **Median TTFV:** 49 days
- **Slowest:** 246 days (Skyard Furniture Co Ltd.)

---

## Post-Bulk Cohort (start_date ≥ 2025-09-01)

| Organization Name | TTFV (Days) | Action Type | Start Date | First Action Date | Notes |
|-------------------|-------------|-------------|------------|-------------------|-------|
| Groupe Courchesne | **-606** | Email Draft | 2026-06-30 | 2024-11-01 | Pre-start activity |
| Charleston Forge | **-467** | Email Draft | 2026-02-11 | 2024-11-01 | Pre-start activity |
| Kennedy International, Inc. | **-424** | Email Draft | 2026-01-01 | 2024-11-03 | Pre-start activity |
| Arabela Lighting | **-403** | Presentation (Stack) | 2026-07-01 | 2025-05-24 | Pre-start activity |
| Moda at Home Enterprises Ltd | **-386** | Email Draft | 2025-12-10 | 2024-11-19 | Pre-start activity |
| Lucas McKearn | **-369** | Email Draft | 2026-07-01 | 2025-06-27 | Pre-start activity |
| Theodore Alexander Manhasset | **-27** | Email Draft | 2025-09-01 | 2025-08-05 | Pre-start activity |
| Terracotta Designs | **-8** | Email Draft | 2026-05-01 | 2026-04-23 | Pre-start activity |
| Globalux Lighting & Fans | **17** | Email Draft | 2025-11-25 | 2025-12-12 |  |
| Dorell Fabrics | **30** | Presentation (Stack) | 2026-06-01 | 2026-07-01 |  |
| Lib and Co. | **35** | Presentation (Stack) | 2026-05-20 | 2026-06-24 |  |
| Coleto Brands / Progress Lighting | **40** | Presentation (Stack) | 2025-12-01 | 2026-01-10 |  |
| Coaster Furniture | **49** | Email Draft | 2025-12-01 | 2026-01-19 |  |
| Jonathan Charles Fine Furniture | **119** | Email Draft | 2025-11-25 | 2026-03-24 | Needs attention |
| Skyard Furniture Co Ltd. | **246** | Email Draft | 2025-10-09 | 2026-06-12 | Needs attention |

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
| Visual Comfort - Studio /Fans | fms | **-299** | Presentation (Stack) | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Summer Classics | scw | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Visual Comfort - Modern | tla | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Visual Comfort Signature | vcg | **-299** | Email Draft | 2025-08-27 | 2024-11-01 | subscriptions.start_date |
| Corbett Lighting | cl | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Dainolite Ltd. | da | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Fine Art Handcrafted Lighting | fal | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Furniture Classics | fc | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Four Seasons Furniture | fsf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Gabby | gh | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Golden Lighting | gl | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Godinger Silver Art Co. | gsa | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Hooker Furnishings | hf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Hubbardton Forge | hfg | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Interlude Home | ih | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Interlude Furniture | ihw | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Kalco Lighting / Allegri Crystal | kal | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Kuzco Lighting Inc. | kll | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Linon/Powell Furniture | lpf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Maxim Lighting | mli | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Palecek | pf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Ricci Argentieri Company | rac | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Rowe Furniture | rf | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Sarreid, Ltd. | sarreid | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Schonbek Lighting | sbl | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Somerset Bay and Modern History | sbmh | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Silver One | soi | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Theodore Alexander | ta | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Troy Lighting | tl | **-298** | Presentation (Stack) | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Universal Furniture | ufi | **-298** | Email Draft | 2025-08-26 | 2024-11-01 | subscriptions.start_date |
| Alfresco Home | ah | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Accord Lighting | all | **-297** | Presentation (Stack) | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Alden Home | ap | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Braxton Culler | bcf | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Bassett Mirror | bmc | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Currey & Company | cci | **-297** | Presentation (Stack) | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Capital Lighting Fixture Co. | clc | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Craftmade | clli | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Crystorama | clm | **-297** | Email Draft | 2025-08-25 | 2024-11-01 | subscriptions.start_date |
| Jamie Young Company | jyc | **-297** | Email Draft | 2025-08-26 | 2024-11-02 | subscriptions.start_date |
| Magnussen Home | mh | **-297** | Email Draft | 2025-08-26 | 2024-11-02 | subscriptions.start_date |
| Donald Choi Canada | dccl | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Elegant Furniture & Lighting | eli | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| ELICO LTD. | etl | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Morgan Fabrics Corporation | mfc | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Millennium Lighting | ml | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Pioneer Morton | mpc | **-295** | Email Draft | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Sauder Woodworking | swc | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
| Ciana Varaluz LLC | vl | **-295** | Presentation (Stack) | 2025-08-26 | 2024-11-04 | subscriptions.start_date |
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
| Visual Comfort Europe | vce | **-287** | Presentation (Stack) | 2025-08-27 | 2024-11-13 | subscriptions.start_date |
| Designer's Fountain | df | **-286** | Email Draft | 2025-08-26 | 2024-11-13 | subscriptions.start_date |
| Bulbrite | bri | **-283** | Email Draft | 2025-08-25 | 2024-11-15 | subscriptions.start_date |
| Highland House | hh | **-278** | Email Draft | 2025-08-25 | 2024-11-20 | subscriptions.start_date |
| Abaline Supply Inc. | asi | **-274** | Email Draft | 2025-08-25 | 2024-11-24 | subscriptions.start_date |
| Gabriella White | sc | **-273** | Email Draft | 2025-08-01 | 2024-11-01 | subscriptions.start_date |
| Studio Silversmiths, Inc. | ssi | **-273** | Email Draft | 2025-08-26 | 2024-11-26 | subscriptions.start_date |
| Coleto Brands / Kichler | kl | **-272** | Presentation (Stack) | 2025-08-26 | 2024-11-27 | subscriptions.start_date |
| Vaxcel International Corporation | vic | **-263** | Email Draft | 2025-08-26 | 2024-12-06 | subscriptions.start_date |
| Yutzy Woodworking | yw | **-263** | Email Draft | 2025-08-26 | 2024-12-06 | subscriptions.start_date |
| Uniware Housewares Corp. | uhc | **-260** | Email Draft | 2025-08-26 | 2024-12-09 | subscriptions.start_date |
| PageOne Lighting | pol | **-251** | Email Draft | 2025-08-26 | 2024-12-18 | subscriptions.start_date |
| RENWIL | rw | **-231** | Email Draft | 2025-08-26 | 2025-01-07 | subscriptions.start_date |
| Eglo USA Inc. | eglo | **-225** | Email Draft | 2025-08-26 | 2025-01-13 | subscriptions.start_date |
| EGLO Canada | eglo_can | **-224** | Email Draft | 2025-08-26 | 2025-01-14 | subscriptions.start_date |
| Lifestyle Solutions | lss | **-221** | Email Draft | 2025-08-26 | 2025-01-17 | subscriptions.start_date |
| America's Backyards | abol | **-202** | Email Draft | 2025-08-25 | 2025-02-04 | subscriptions.start_date |
| International Home Miami | ihm | **-180** | Presentation (Stack) | 2025-08-26 | 2025-02-27 | subscriptions.start_date |
| Buster & Punch | bp | **-178** | Presentation (Stack) | 2025-08-25 | 2025-02-28 | subscriptions.start_date |
| Wendover Art Group | wag | **-165** | Email Draft | 2025-08-26 | 2025-03-14 | subscriptions.start_date |
| Alfonso Marina | am | **-136** | Email Draft | 2025-08-25 | 2025-04-11 | subscriptions.start_date |
| Philip Whitney | pw | **-134** | Email Draft | 2025-08-26 | 2025-04-14 | subscriptions.start_date |
| Minka Lighting Group | mlg | **-124** | Presentation (Stack) | 2025-08-26 | 2025-04-24 | subscriptions.start_date |
| Theodore Alexander Manhasset | tam | **-27** | Email Draft | 2025-09-01 | 2025-08-05 | subscriptions.start_date |
| Terracotta Designs | tcd | **-8** | Email Draft | 2026-05-01 | 2026-04-23 | subscriptions.start_date |
| Globalux Lighting & Fans | gblx | **17** | Email Draft | 2025-11-25 | 2025-12-12 | subscriptions.start_date |
| Dorell Fabrics | drf | **30** | Presentation (Stack) | 2026-06-01 | 2026-07-01 | subscriptions.start_date |
| Lib and Co. | libco | **35** | Presentation (Stack) | 2026-05-20 | 2026-06-24 | subscriptions.start_date |
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
| Magic Lite / NSL | mali | - | - | 2025-11-11 | - | No TTFV Events |
| Abroad Home Furnishings | aa | - | - | 2026-03-01 | - | No TTFV Events |
| The CopperSmith | tcs | - | - | 2026-04-15 | - | No TTFV Events |

---

## Orgs Without Valid TTFV

| Organization Name | Org | Start Date | Reason |
|-------------------|-----|------------|--------|
| Oly Studio | ol | 2025-08-26 | Admin-only TTFV activity (or event users lack `org_users` / are admin) |
| Sixtrees Limited | st | 2025-08-26 | Admin-only TTFV activity (or event users lack `org_users` / are admin) |
| Bliss Studio | blh | 2025-08-29 | Admin-only TTFV activity (or event users lack `org_users` / are admin) |
| Kaleen Rugs & Broadloom | krb | 2025-11-25 | Admin-only TTFV activity (or event users lack `org_users` / are admin) |
| Magic Lite / NSL | mali | 2025-11-11 | No TTFV events recorded |
| Abroad Home Furnishings | aa | 2026-03-01 | No TTFV events recorded |
| The CopperSmith | tcs | 2026-04-15 | No TTFV events recorded |

---

## Key Insights

### 1. Bulk start dates dominate the book
- **92** orgs have August 2025 subscription start dates from billing provisioning.
- **98** orgs show negative TTFV (first value before `start_date`).
- Treat book-wide average/median TTFV as **not comparable** to pre-subscription-migration reports that used HubSpot close dates.

### 2. Non-negative TTFV (true post-start adoption)
- **9** orgs have non-negative TTFV.
- **Average: 107.3 days** | **Median: 49 days**
- **Best:** Globalux Lighting & Fans (17d), Dorell Fabrics (30d), Lib and Co. (35d)
- **>60 days:** Jonathan Charles Fine Furniture (119d), Sabine Pools, Spas, & Furnitur (187d), Butler Specialty Company (243d), Skyard Furniture Co Ltd. (246d)

### 3. Clients needing attention
- **4** admin-only / no valid non-admin TTFV: Oly Studio, Sixtrees Limited, Bliss Studio, Kaleen Rugs & Broadloom
- **3** no TTFV events: Magic Lite / NSL, Abroad Home Furnishings, The CopperSmith
- **Slow non-negative TTFV (>60d):** Jonathan Charles Fine Furniture (119d), Sabine Pools, Spas, & Furnitur (187d), Butler Specialty Company (243d), Skyard Furniture Co Ltd. (246d)

### 4. Action-type mix (valid TTFV)
- Email Draft: **84** (78.5%)
- Presentation (Stack): **23** (21.5%)

---

## Methodology Notes

1. **Start Date:** Postgres `subscriptions.start_date` (`MIN` per org, `status = 'active'` only).
2. **Active org filter:** Excludes demo/test/staging shortnames and a hard-coded exclusion list from `TTFV_Analysis_Prompt.md`.
3. **Admin Exclusion:** Users with `is_admin = TRUE` in Postgres `org_users` are excluded. Users with Mixpanel events but no `org_users` row are also excluded; the next earliest qualifying user is used.
4. **Value Actions Tracked:**
   - `item_added_via_magic_button` → Presentation (Stack)
   - `document_email_drafted` / `item_email_drafted` → Email Draft
5. **Data Sources:**
   - Start dates / admins: SuperCat Postgres (`organizations`, `subscriptions`, `org_users`, `users`)
   - TTFV events: BigQuery `supercat-data-pipeline.mixpanel.events`

---

*Report generated using SuperCat TTFV Analysis methodology (`subscriptions.start_date`).*
