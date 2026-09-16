# Q-17: Dormant eCat Customer Identification (Postgres)
- **Org:** Magnussen Home (mh, org_id=184)
- **Period:** LTM
- **Rows:** 45 (25 recently lapsed + 20 at-risk)
- **Run date:** 2026-04-20

## Recently lapsed (ordered 4-12mo ago, NOT in last 3mo)

Rows: 25

| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
|---|---|---|---|---|---|
| m03_RFI2 | Reeds Furniture Inc. | CA | 2025-07-11 | 3 | $62,233 |
| m02_MEGA2.US | Mega Group Inc. Allied | SK | 2025-11-17 | 4 | $43,897 |
| m03_RMJ | JRJT Trading Inc David Kirsch | NL MX | 2025-10-09 | 6 | $36,329 |
| m02_COL0 | MEGA0 - Colemans Countrywide | NL | 2025-10-08 | 2 | $23,845 |
| m03_JAC4 | Jack's Furniture Center | WV | 2025-11-10 | 3 | $18,231 |
| m03_FMO2 | FMO BG Corp | KY | 2026-01-14 | 15 | $17,997 |
| m02_ALS0 | Mansour and Ali Al Shammasi Trading Co | N/A | 2025-04-28 | 1 | $17,940 |
| m03_WOO7 | Southern Craftsmen, Inc. dba Woodstock Furniture | MS | 2025-10-25 | 2 | $16,960 |
| m03_SCF4 | Southern Charm Furniture & Design LLC | MS | 2025-11-10 | 18 | $15,200 |
| m02_RENA0 | MEGA0 - Renaud's BrandSource Home Furnishings | NB | 2026-01-16 | 3 | $13,370 |
| m03_BRO7 | Furniture World Inc dba Brown Squirrel | TN | 2025-05-21 | 1 | $12,830 |
| m03_HUR1 | Hurwitz Mintz Furniture | LA | 2025-09-04 | 7 | $11,077 |
| m03_FMO1 | Furniture & Merchandise Outlet | TN | 2025-11-17 | 13 | $10,657 |
| m02_SOR0 | MEGA0 - Sorensen's Fine Furniture Ltd | SK | 2025-04-29 | 1 | $10,220 |
| m02_GRE1 | MEGA0 - Green's Countrywide Furniture And Appliances | ON | 2025-10-27 | 2 | $10,009 |
| m03_KNO3 | Knoxville Wholesale Furniture Co, Inc | TN | 2025-07-28 | 7 | $8,150 |
| m02_HAM2 | MEGA0 - Hambly's Home Furnishings | PE | 2025-11-30 | 5 | $7,424 |
| m03_BLI2 | King Krabs LLC /Bliss Home | TN | 2025-10-01 | 4 | $7,404 |
| m03_DON2 | Donna's Interiors Furniture & Design Inc | CA | 2025-08-27 | 2 | $7,340 |
| m03_LFF0 | LF Furniture LLC dba Louisville Furniture | KY | 2026-01-16 | 1 | $6,836 |
| m03_CLA20 | Classic Oak Furniture, dba Classic Home | MS | 2025-07-23 | 2 | $5,920 |
| m03_WOO0 | Woodland Wholesale Retail Furniture | MS | 2025-12-04 | 2 | $4,768 |
| m03_CUM1 | Cumberland Investment Group Cumberland Furniture Outlet | KY | 2025-10-22 | 2 | $4,729 |
| m03_JOH24 | Johnson's Home Furnishings | TN | 2025-09-05 | 2 | $4,127 |
| m02_CHE3 | MEGA0 - Tom Chediac Furniture | NS | 2026-01-13 | 1 | $3,837 |

## At-risk high-value (last order >90 days ago)

Rows: 20 (top by GMV)

| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
|---|---|---|---|---|---|
| m03_RFI2 | Reeds Furniture Inc. | CA | $62,233 | 2025-07-11 | 283 |
| m02_MEGA2.US | Mega Group Inc. Allied | SK | $43,897 | 2025-11-17 | 154 |
| m03_RMJ | JRJT Trading Inc David Kirsch | NL MX | $36,329 | 2025-10-09 | 193 |
| m02_COL0 | MEGA0 - Colemans Countrywide | NL | $23,845 | 2025-10-08 | 193 |
| m03_JAC4 | Jack's Furniture Center | WV | $18,231 | 2025-11-10 | 161 |
| m03_FMO2 | FMO BG Corp | KY | $17,997 | 2026-01-14 | 96 |
| m02_ALS0 | Mansour and Ali Al Shammasi Trading Co | N/A | $17,940 | 2025-04-28 | 357 |
| m03_WOO7 | Southern Craftsmen, Inc. dba Woodstock Furniture | MS | $16,960 | 2025-10-25 | 177 |
| m03_SCF4 | Southern Charm Furniture & Design LLC | MS | $15,200 | 2025-11-10 | 161 |
| m02_RENA0 | MEGA0 - Renaud's BrandSource Home Furnishings | NB | $13,370 | 2026-01-16 | 94 |
| m03_BRO7 | Furniture World Inc dba Brown Squirrel | TN | $12,830 | 2025-05-21 | 334 |
| m03_HUR1 | Hurwitz Mintz Furniture | LA | $11,077 | 2025-09-04 | 228 |
| m03_FMO1 | Furniture & Merchandise Outlet | TN | $10,657 | 2025-11-17 | 154 |
| m02_SOR0 | MEGA0 - Sorensen's Fine Furniture Ltd | SK | $10,220 | 2025-04-29 | 356 |
| m02_GRE1 | MEGA0 - Green's Countrywide Furniture And Appliances | ON | $10,009 | 2025-10-27 | 175 |
| m03_KNO3 | Knoxville Wholesale Furniture Co, Inc | TN | $8,150 | 2025-07-28 | 266 |
| m02_HAM2 | MEGA0 - Hambly's Home Furnishings | PE | $7,424 | 2025-11-30 | 141 |
| m03_BLI2 | King Krabs LLC /Bliss Home | TN | $7,404 | 2025-10-01 | 201 |
| m03_DON2 | Donna's Interiors Furniture & Design Inc | CA | $7,340 | 2025-08-27 | 236 |
| m03_LFF0 | LF Furniture LLC dba Louisville Furniture | KY | $6,836 | 2026-01-16 | 94 |
