# Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Query**: Q-37 | **Org**: Crystorama (clm, org_id=64) | **Source**: Postgres `sales_data` × `inventories` × `products` | **Run date**: 2026-06-12
- **ERP join guard applied**: amount_invoiced > 0 (confirmed ERP sales history) AND qty_available <= 0. Top 20 by ERP invoiced.
- **Caveat**: Point-in-time inventory snapshot (imported 2026-06-12). Cannot determine how long items have been OOS.

| item_code | category | collection | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
|---|---|---|---|---|---|---|---|---|---|
| HAY-1417-AG | CAT1 | HAYES | Hayes 50'' Aged Brass Linear Chandelier | $491,811.89 | 352 | 0 | 0 | 0 | 2026-07-14 |
| ADD-317-AG-CL | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $296,812.82 | 258 | 0 | 0 | 0 | 2026-06-30 |
| ARA-10269-MK-ST | CAT1 | COL127 | Aragon 58.75'' LED Matte Black Chandelier | $265,753.16 | 102 | 0 | 0 | 0 | 2026-08-18 |
| 505-MT | CAT2 | COL100 | Broche 16'' Matte White Semi Flush Mount | $230,738.05 | 972 | 0 | 0 | 0 | 2026-06-26 |
| ADD-317-AG-WH | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $210,975.15 | 189 | 0 | 0 | 0 | 2026-06-22 |
| ADD-317-AG-AU | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $207,762.55 | 183 | 0 | 0 | 0 | 2026-06-29 |
| ADD-317-AG-AM | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $188,094.15 | 162 | 0 | 0 | 0 | 2026-08-05 |
| ARC-1919-GA-CL-MWP | CAT1 | COL70 | Arcadia 46.25'' Antique Gold Chandelier | $178,661.39 | 109 | 0 | 0 | 0 | 2026-07-27 |
| HAY-1409-PN | CAT1 | HAYES | Hayes 40.5'' Polished Nickel Chandelier | $177,252.20 | 87 | 0 | 0 | 0 | 2026-07-14 |
| ADD-308-AG-WH | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $133,039.23 | 228 | 0 | 0 | 0 | 2026-06-30 |
| ADD-308-AG-AM | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $119,539.65 | 210 | 0 | 0 | 0 | 2026-06-22 |
| 2242-VG | CAT6 | COL9 | Libby Langdon Sylvan 15.5'' Vibrant Gold Sconce | $112,508.83 | 1,117 | 0 | 0 | 0 | 2026-06-26 |
| ADD-308-AG-CL | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $99,584.59 | 171 | 0 | 0 | 0 | 2026-06-22 |
| ADD-308-AG-AU | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $98,822.62 | 176 | 0 | 0 | 0 | 2026-06-22 |
| ARC-1909-GA-CL-MWP | CAT1 | COL70 | Arcadia 32.5'' Antique Gold Chandelier | $98,352.24 | 116 | 0 | 0 | 0 | 2026-06-29 |
| 4456-GA-CL-MWP | CAT1 | COL113 | Filmore 29'' Hand Cut Crystal Antique Gold Chandelier | $94,840.71 | 185 | 0 | 0 | 0 | 2026-07-14 |
| 573-OP-GA | CAT5 | COL100 | Broche 25'' Antique Gold Bathroom Vanity | $89,658.35 | 483 | 0 | 0 | 0 | 2026-06-26 |
| ADD-321-AG-WH | CAT2 | ADDIS | Addis 22.25'' Aged Brass Flush Mount | $80,523.03 | 110 | 0 | 0 | 0 | 2026-05-25 |
| 4457-GA-CL-MWP | CAT2 | COL113 | Filmore 19'' Hand Cut Crystal Antique Gold Semi Flush Mount | $72,027.61 | 252 | 0 | 0 | 0 | 2026-07-14 |
| BAI-A2109-AG | CAT1 | COL68 | Bailey 48'' Aged Brass Chandelier | $69,271.16 | 115 | 0 | 0 | 0 | 2026-07-03 |

**Note**: High-velocity ADDIS/HAYES chandelier finishes and Broche flush mounts show zero available inventory but have scheduled receipts (mostly Jun–Aug 2026) — restock pipeline is active. Present with the snapshot caveat; never claim "revenue at risk" without it.
