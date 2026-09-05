# TTFV Analysis Report - February 2026 (All Active Clients)
**Generated:** March 9, 2026

---

## Executive Summary

This report calculates the **Time to First Value (TTFV)** for all active SuperCat clients. TTFV measures the number of days from a baseline date to the first time a **non-admin sales rep** performed a value-generating action:
- **Presentation/Stack**: Added a product via magic button
- **Email Draft**: Drafted an email from the platform

### Start Date Methodology (Hybrid Approach)
- **Primary**: HubSpot deal close date (when available)
- **Fallback**: Organization `created_at` date from Postgres (for legacy clients without HubSpot data)

**Note:** TTFV is only valid when performed by a non-admin user, as admin activity during implementation doesn't represent true sales adoption.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Active Orgs** | 127 |
| **Orgs with Valid TTFV** | 116 |
| **Orgs with No Valid TTFV** | 7 |
| **Orgs with No TTFV Events** | 4 |
| **Orgs Using HubSpot (Start Date)** | 27 |
| **Orgs Using Created_At (Start Date)** | 89 |

---

## Complete TTFV Results

| Organization Name | TTFV (Days) | Action Type | Start Date | First Action Date | Start Date Reference |
|-------------------|-------------|-------------|------------|-------------------|----------------------|
| Kuzco Lighting Inc. | **-336** | Email Draft | 2025-10-03 | 2024-11-01 | HubSpot |
| Universal Furniture | **-237** | Email Draft | 2025-06-26 | 2024-11-01 | HubSpot |
| Jonathan Charles Designs Inc. | **-217** | Email Draft | 2025-06-13 | 2024-11-08 | HubSpot |
| DEBRAH FURNITURE USA | **-81** | Email Draft | 2025-02-28 | 2024-12-09 | HubSpot |
| Golden Lighting | **35** | Email Draft | 2024-09-27 | 2024-11-01 | HubSpot |
| Wendover Art Group | **35** | Email Draft | 2025-02-07 | 2025-03-14 | HubSpot |
| Oly Studio | **40** | Email Draft | 2025-03-19 | 2025-04-28 | HubSpot |
| RENWIL | **61** | Email Draft | 2024-11-07 | 2025-01-07 | HubSpot |
| Buster & Punch | **70** | Presentation (Stack) | 2024-12-20 | 2025-02-28 | HubSpot |
| Arabela Lighting | **72** | Presentation (Stack) | 2025-03-13 | 2025-05-24 | HubSpot |
| Hooker Furnishings | **73** | Email Draft | 2024-08-20 | 2024-11-01 | HubSpot |
| Ratana International Ltd. | **83** | Email Draft | 2024-08-20 | 2024-11-11 | HubSpot |
| International Home Miami | **89** | Email Draft | 2024-11-18 | 2025-02-15 | HubSpot |
| Fine Art Handcrafted Lighting | **92** | Email Draft | 2024-08-01 | 2024-11-01 | HubSpot |
| Theodore Alexander Manhasset | **92** | Email Draft | 2025-05-05 | 2025-08-05 | created_at |
| Minka Lighting Group | **94** | Presentation (Stack) | 2025-01-20 | 2025-04-24 | HubSpot |
| Elk Home | **111** | Email Draft | 2024-07-13 | 2024-11-01 | HubSpot |
| Lucas McKearn | **119** | Email Draft | 2025-02-28 | 2025-06-27 | HubSpot |
| Sanders Collection Inc | **134** | Presentation (Stack) | 2024-06-20 | 2024-11-01 | HubSpot |
| Access Lighting | **144** | Email Draft | 2024-06-13 | 2024-11-04 | HubSpot |
| Donald Choi Canada | **153** | Email Draft | 2024-06-04 | 2024-11-04 | HubSpot |
| Groupe Courchesne | **156** | Email Draft | 2024-05-29 | 2024-11-01 | HubSpot |
| Designer's Fountain | **163** | Email Draft | 2024-06-03 | 2024-11-13 | HubSpot |
| Alfonso Marina | **172** | Email Draft | 2024-10-21 | 2025-04-11 | HubSpot |
| Yutzy Woodworking | **210** | Email Draft | 2024-05-10 | 2024-12-06 | HubSpot |
| BOBO Intriguing Objects | **232** | Email Draft | 2024-03-27 | 2024-11-14 | created_at |
| Geo Contemporary | **252** | Email Draft | 2024-03-01 | 2024-11-08 | created_at |
| Silver One | **255** | Email Draft | 2024-02-20 | 2024-11-01 | created_at |
| EGLO Canada | **265** | Presentation (Stack) | 2024-03-13 | 2024-12-03 | created_at |
| America's Backyards and Outdoor Living | **312** | Email Draft | 2024-03-29 | 2025-02-04 | HubSpot |
| Ideal Living | **330** | Email Draft | 2024-03-11 | 2025-02-04 | HubSpot |
| Four Seasons Furniture | **360** | Email Draft | 2023-11-07 | 2024-11-01 | created_at |
| Capital Lighting Fixture Co. | **406** | Email Draft | 2023-09-22 | 2024-11-01 | HubSpot |
| Accord Lighting | **409** | Presentation (Stack) | 2023-09-19 | 2024-11-01 | created_at |
| Karat Home Inc. | **435** | Email Draft | 2024-01-03 | 2025-03-13 | created_at |
| Bulbrite | **439** | Email Draft | 2023-08-23 | 2024-11-04 | created_at |
| Matteo Lighting | **446** | Email Draft | 2023-08-23 | 2024-11-11 | created_at |
| DALS Lighting | **447** | Email Draft | 2023-08-17 | 2024-11-06 | created_at |
| Lifestyle Solutions | **480** | Email Draft | 2023-09-25 | 2025-01-17 | created_at |
| AFX, Inc. | **596** | Email Draft | 2023-03-22 | 2024-11-07 | created_at |
| Magnussen Home | **619** | Email Draft | 2023-02-22 | 2024-11-02 | created_at |
| Schonbek Lighting | **631** | Email Draft | 2023-02-09 | 2024-11-01 | created_at |
| WAC/Modern Forms Lighting | **634** | Email Draft | 2023-02-09 | 2024-11-04 | created_at |
| Vaxcel International Corporation | **741** | Email Draft | 2022-10-26 | 2024-11-05 | created_at |
| Braxton Culler | **780** | Email Draft | 2022-09-13 | 2024-11-01 | created_at |
| Visual Comfort Europe | **933** | Presentation (Stack) | 2022-04-25 | 2024-11-13 | created_at |
| Eglo USA Inc. | **979** | Presentation (Stack) | 2022-05-05 | 2025-01-08 | created_at |
| Hubbardton Forge | **1,008** | Email Draft | 2022-01-28 | 2024-11-01 | created_at |
| Interlude Home | **1,067** | Email Draft | 2021-11-30 | 2024-11-01 | created_at |
| Rowe Furniture | **1,096** | Email Draft | 2021-11-01 | 2024-11-01 | created_at |
| Currey & Company | **1,195** | Presentation (Stack) | 2021-07-25 | 2024-11-01 | created_at |
| Uniware Housewares Corp. | **1,252** | Email Draft | 2021-07-06 | 2024-12-09 | created_at |
| Millennium Lighting | **1,564** | Presentation (Stack) | 2020-07-24 | 2024-11-04 | created_at |
| Eurofase Inc. | **1,723** | Email Draft | 2020-02-17 | 2024-11-05 | created_at |
| PageOne Lighting | **1,748** | Email Draft | 2020-03-06 | 2024-12-18 | created_at |
| Craftmade | **1,829** | Presentation (Stack) | 2019-10-30 | 2024-11-01 | created_at |
| Stoneline Designs by Charleston Forge | **1,847** | Email Draft | 2019-10-30 | 2024-11-19 | created_at |
| Varaluz Lighting & Varaluz Casa | **1,865** | Presentation (Stack) | 2019-09-27 | 2024-11-04 | created_at |
| Kalco Lighting / Allegri Crystal | **1,880** | Email Draft | 2019-09-09 | 2024-11-01 | created_at |
| Visual Comfort Signature | **2,024** | Email Draft | 2019-04-18 | 2024-11-01 | created_at |
| ELICO LTD. | **2,037** | Email Draft | 2019-04-08 | 2024-11-04 | created_at |
| ET2 Lighting | **2,052** | Email Draft | 2019-03-21 | 2024-11-01 | created_at |
| Linon/Powell Furniture | **2,052** | Email Draft | 2019-03-21 | 2024-11-01 | created_at |
| Maxim Lighting | **2,052** | Presentation (Stack) | 2019-03-21 | 2024-11-01 | created_at |
| Moda at Home Enterprises Ltd | **2,092** | Email Draft | 2019-02-27 | 2024-11-19 | created_at |
| Hancock & Moore / Jessica Charles | **2,275** | Presentation (Stack) | 2018-09-06 | 2024-11-28 | created_at |
| Baker-McGuire | **2,367** | Email Draft | 2018-05-10 | 2024-11-01 | created_at |
| Alfresco Home | **2,412** | Presentation (Stack) | 2018-03-26 | 2024-11-01 | created_at |
| Furniture Classics | **2,530** | Email Draft | 2017-11-28 | 2024-11-01 | created_at |
| Visual Comfort - Modern | **2,734** | Email Draft | 2017-05-08 | 2024-11-01 | created_at |
| Sabine Pools, Spas, & Furnitur | **2,736** | Presentation (Stack) | 2018-09-06 | 2026-03-04 | created_at |
| Theodore Alexander | **2,901** | Presentation (Stack) | 2016-11-22 | 2024-11-01 | created_at |
| Visual Comfort - Studio /Fans | **2,948** | Presentation (Stack) | 2016-10-06 | 2024-11-01 | created_at |
| Art Trends & Prestige Arts | **2,970** | Presentation (Stack) | 2016-11-08 | 2024-12-26 | created_at |
| Interlude Furniture | **2,984** | Email Draft | 2016-08-31 | 2024-11-01 | created_at |
| Kindel Karges Furniture | **3,298** | Presentation (Stack) | 2015-11-03 | 2024-11-13 | created_at |
| Fine Furniture Design | **3,340** | Email Draft | 2015-09-11 | 2024-11-02 | created_at |
| Kennedy International, Inc. | **3,419** | Email Draft | 2015-06-25 | 2024-11-03 | created_at |
| Pioneer Morton | **3,472** | Email Draft | 2015-05-04 | 2024-11-04 | created_at |
| Summer Classics | **3,475** | Email Draft | 2015-04-28 | 2024-11-01 | created_at |
| Shadow Catchers | **3,478** | Email Draft | 2015-05-05 | 2024-11-11 | created_at |
| Summer Classics Contract | **3,479** | Email Draft | 2015-04-28 | 2024-11-05 | created_at |
| Tomlinson Companies | **3,525** | Email Draft | 2015-03-30 | 2024-11-22 | created_at |
| Charleston Forge | **3,558** | Email Draft | 2015-02-04 | 2024-11-01 | created_at |
| Highland House | **3,725** | Email Draft | 2014-09-09 | 2024-11-20 | created_at |
| Jamie Young Company | **3,736** | Email Draft | 2014-08-11 | 2024-11-02 | created_at |
| Corbett Lighting | **3,854** | Presentation (Stack) | 2014-04-14 | 2024-11-01 | created_at |
| Hudson Valley Lighting | **3,854** | Email Draft | 2014-04-14 | 2024-11-01 | created_at |
| Troy Lighting | **3,858** | Email Draft | 2014-04-10 | 2024-11-01 | created_at |
| Ateliers Davoy | **3,902** | Email Draft | 2014-07-07 | 2025-03-13 | created_at |
| Summer Classics Retail | **3,922** | Email Draft | 2014-02-05 | 2024-11-01 | created_at |
| Elegant Furniture & Lighting | **3,982** | Presentation (Stack) | 2013-12-10 | 2024-11-04 | created_at |
| Crystorama | **4,054** | Email Draft | 2013-09-26 | 2024-11-01 | created_at |
| Dainolite Ltd. | **4,076** | Email Draft | 2013-09-04 | 2024-11-01 | created_at |
| Godinger Group | **4,148** | Email Draft | 2013-06-24 | 2024-11-01 | created_at |
| Sauder Woodworking | **4,188** | Presentation (Stack) | 2013-05-18 | 2024-11-04 | created_at |
| Gabby | **4,209** | Email Draft | 2013-04-24 | 2024-11-01 | created_at |
| Morgan Fabrics Corporation | **4,378** | Email Draft | 2012-11-09 | 2024-11-04 | created_at |
| Kichler Lighting | **4,380** | Presentation (Stack) | 2012-11-30 | 2024-11-27 | created_at |
| Moe's Home Collection | **4,383** | Email Draft | 2012-11-02 | 2024-11-02 | created_at |
| Savoy House Lighting | **4,501** | Email Draft | 2012-07-10 | 2024-11-05 | created_at |
| Philip Whitney | **4,513** | Email Draft | 2012-12-05 | 2025-04-14 | created_at |
| Decca Home / Bolier & Co, | **4,525** | Presentation (Stack) | 2013-08-17 | 2026-01-06 | created_at |
| Palecek | **4,546** | Email Draft | 2012-05-22 | 2024-11-01 | created_at |
| Home Essentials & Beyond | **4,612** | Email Draft | 2012-03-23 | 2024-11-07 | created_at |
| Alden Home | **4,663** | Email Draft | 2012-01-26 | 2024-11-01 | created_at |
| Ricci Argentieri Company | **4,725** | Email Draft | 2011-11-25 | 2024-11-01 | created_at |
| Abaline Supply Inc. | **4,730** | Email Draft | 2011-12-13 | 2024-11-24 | created_at |
| Studio Silversmiths, Inc. | **4,750** | Email Draft | 2011-11-25 | 2024-11-26 | created_at |
| Godinger Silver Art Co. | **4,865** | Email Draft | 2011-07-08 | 2024-11-01 | created_at |
| Bassett Mirror | **4,886** | Email Draft | 2011-06-17 | 2024-11-01 | created_at |
| Century Furniture | **4,918** | Email Draft | 2011-05-20 | 2024-11-05 | created_at |
| Wildwood/Chelsea House | **4,918** | Email Draft | 2011-05-16 | 2024-11-01 | created_at |
| Somerset Bay and Modern History | **4,991** | Email Draft | 2011-03-04 | 2024-11-01 | created_at |
| Sarreid, Ltd. | **5,165** | Email Draft | 2010-09-11 | 2024-11-01 | created_at |
| Butler Specialty Company | **5,199** | Presentation (Stack) | 2011-08-02 | 2025-10-26 | created_at |
| Bethel International | - | - | - | - | No Valid TTFV |
| Bliss Studio | - | - | - | - | No Valid TTFV |
| BT Shalom | - | - | - | - | No Valid TTFV |
| Elan, a Kichler Company | - | - | - | - | No TTFV Events |
| French Heritage | - | - | - | - | No Valid TTFV |
| Jonathan Charles Fine Furniture Ltd. | - | - | - | - | No Valid TTFV |
| Kaleen Rugs & Broadloom | - | - | - | - | No Valid TTFV |
| Opame Collective | - | - | - | - | No TTFV Events |
| Sonneman - A Way of Light | - | - | - | - | No TTFV Events |
| Sixtrees Limited | - | - | - | - | No Valid TTFV |
| Wesley Allen | - | - | - | - | No TTFV Events |

---

## TTFV Analysis by Baseline Source

### HubSpot Close Date (Most Accurate - Recent Deals)

| Organization | Close Date | First Value Date | TTFV (Days) | Action Type |
|--------------|------------|------------------|-------------|-------------|
| Kuzco Lighting Inc. | 2025-10-03 | 2024-11-01 | **-336** | Email Draft |
| Universal Furniture | 2025-06-26 | 2024-11-01 | **-237** | Email Draft |
| Jonathan Charles Designs Inc. | 2025-06-13 | 2024-11-08 | **-217** | Email Draft |
| DEBRAH FURNITURE USA | 2025-02-28 | 2024-12-09 | **-81** | Email Draft |
| Golden Lighting | 2024-09-27 | 2024-11-01 | **35** | Email Draft |
| Wendover Art Group | 2025-02-07 | 2025-03-14 | **35** | Email Draft |
| Oly Studio | 2025-03-19 | 2025-04-28 | **40** | Email Draft |
| RENWIL | 2024-11-07 | 2025-01-07 | **61** | Email Draft |
| Buster & Punch | 2024-12-20 | 2025-02-28 | **70** | Presentation (Stack) |
| Arabela Lighting | 2025-03-13 | 2025-05-24 | **72** | Presentation (Stack) |
| Hooker Furnishings | 2024-08-20 | 2024-11-01 | **73** | Email Draft |
| Ratana International Ltd. | 2024-08-20 | 2024-11-11 | **83** | Email Draft |
| International Home Miami | 2024-11-18 | 2025-02-15 | **89** | Email Draft |
| Fine Art Handcrafted Lighting | 2024-08-01 | 2024-11-01 | **92** | Email Draft |
| Minka Lighting Group | 2025-01-20 | 2025-04-24 | **94** | Presentation (Stack) |
| Elk Home | 2024-07-13 | 2024-11-01 | **111** | Email Draft |
| Lucas McKearn | 2025-02-28 | 2025-06-27 | **119** | Email Draft |
| Sanders Collection Inc | 2024-06-20 | 2024-11-01 | **134** | Presentation (Stack) |
| Access Lighting | 2024-06-13 | 2024-11-04 | **144** | Email Draft |
| Donald Choi Canada | 2024-06-04 | 2024-11-04 | **153** | Email Draft |
| Groupe Courchesne | 2024-05-29 | 2024-11-01 | **156** | Email Draft |
| Designer's Fountain | 2024-06-03 | 2024-11-13 | **163** | Email Draft |
| Alfonso Marina | 2024-10-21 | 2025-04-11 | **172** | Email Draft |
| Yutzy Woodworking | 2024-05-10 | 2024-12-06 | **210** | Email Draft |
| America's Backyards and Outdoor Living | 2024-03-29 | 2025-02-04 | **312** | Email Draft |
| Ideal Living | 2024-03-11 | 2025-02-04 | **330** | Email Draft |
| Capital Lighting Fixture Co. | 2023-09-22 | 2024-11-01 | **406** | Email Draft |

#### HubSpot TTFV Statistics
- **Best TTFV:** -336 days (Kuzco Lighting Inc.)
- **Average TTFV:** 84.6 days
- **Median TTFV:** 92 days

---

### Created_At as Start Date (Legacy Clients)

For legacy clients, TTFV from `created_at` reflects time since initial platform setup. These numbers are large because many clients were set up years ago but the Mixpanel tracking of value events started more recently (around Nov 2024).

#### Recent Implementations (created_at 2023+)

| Organization | Created | First Value | TTFV (Days) |
|--------------|---------|-------------|-------------|
| Theodore Alexander Manhasset | 2025-05-05 | 2025-08-05 | **92** |
| BOBO Intriguing Objects | 2024-03-27 | 2024-11-14 | **232** |
| Geo Contemporary | 2024-03-01 | 2024-11-08 | **252** |
| Silver One | 2024-02-20 | 2024-11-01 | **255** |
| EGLO Canada | 2024-03-13 | 2024-12-03 | **265** |
| Four Seasons Furniture | 2023-11-07 | 2024-11-01 | **360** |
| Accord Lighting | 2023-09-19 | 2024-11-01 | **409** |
| Karat Home Inc. | 2024-01-03 | 2025-03-13 | **435** |
| Bulbrite | 2023-08-23 | 2024-11-04 | **439** |
| Matteo Lighting | 2023-08-23 | 2024-11-11 | **446** |
| DALS Lighting | 2023-08-17 | 2024-11-06 | **447** |
| Lifestyle Solutions | 2023-09-25 | 2025-01-17 | **480** |
| AFX, Inc. | 2023-03-22 | 2024-11-07 | **596** |
| Magnussen Home | 2023-02-22 | 2024-11-02 | **619** |
| Schonbek Lighting | 2023-02-09 | 2024-11-01 | **631** |
| WAC/Modern Forms Lighting | 2023-02-09 | 2024-11-04 | **634** |

#### Recent Implementation Statistics (created_at 2023+)
- **Best TTFV:** 92 days (Theodore Alexander Manhasset)
- **Average TTFV:** 412.0 days
- **Median TTFV:** 439 days

---

## Orgs Without Valid TTFV

| Organization Name | Reason |
|-------------------|--------|
| Bethel International | Admin-only TTFV activity |
| Bliss Studio | Admin-only TTFV activity |
| BT Shalom | Admin-only TTFV activity |
| French Heritage | Admin-only TTFV activity |
| Jonathan Charles Fine Furniture Ltd. | Admin-only TTFV activity |
| Kaleen Rugs & Broadloom | Admin-only TTFV activity |
| Sixtrees Limited | Admin-only TTFV activity |
| Elan, a Kichler Company | No TTFV events recorded |
| Opame Collective | No TTFV events recorded |
| Sonneman - A Way of Light | No TTFV events recorded |
| Wesley Allen | No TTFV events recorded |

---

## Key Insights

### 1. HubSpot-Tracked Deals (Most Reliable)
For the 27 recent deals with HubSpot close dates:
- **Average TTFV: 84.6 days**
- **Best performers:** Kuzco Lighting Inc. (-336 days), Universal Furniture (-237 days), Jonathan Charles Designs Inc. (-217 days)
- **Slowest:** Capital Lighting Fixture Co. (406 days)

### 2. Recent Implementations (2023+ created_at)
For clients created in 2023+ (using created_at as baseline):
- **Average TTFV: 412.0 days**
- **Best performers:** Theodore Alexander Manhasset (92 days), BOBO Intriguing Objects (232 days), Geo Contemporary (252 days)

### 3. Anomalies
- **4 orgs have negative TTFV** (sales activity before deal officially closed in HubSpot):
  - Kuzco Lighting Inc.: -336 days
  - Universal Furniture: -237 days
  - Jonathan Charles Designs Inc.: -217 days
  - DEBRAH FURNITURE USA: -81 days

### 4. Clients Needing Attention
11 orgs have no valid non-admin TTFV:
- 7 have admin-only activity (sales reps not yet engaged)
- 4 have no TTFV events at all (may need enablement focus)

---

## Methodology Notes

1. **Start Date Priority:**
   - Primary: HubSpot deal close date (stage `53599608` = Closed-Won)
   - Fallback: Postgres `organizations.created_at`

2. **Admin Exclusion:** Users with `is_admin = TRUE` in Postgres `org_users` table are excluded from TTFV calculations.

3. **User Validation:** Each TTFV user was validated against Postgres `org_users` to confirm `is_admin = FALSE` and that an org_users record exists.

4. **Value Actions Tracked:**
   - `item_added_via_magic_button` (Presentation/Stack)
   - `document_email_drafted` (Email Draft)
   - `item_email_drafted` (Email Draft)

5. **Data Sources:**
   - Deal close dates: BigQuery `hubspot__deal` table
   - TTFV events: BigQuery `mixpanel__events` table
   - Admin status: Postgres `org_users` table
   - Org created dates: Postgres `organizations` table

---

*Report generated using SuperCat TTFV Analysis methodology (Hybrid Approach).*