# Q-37: Inventory × Sales Intelligence (OOS Top Sellers) — Crystorama (clm, org_id=64)
- **Query**: Q-37 (Postgres — sales_data + inventories, qty_available ≤ 0)
- **Period**: All-time ERP sales, current inventory snapshot
- **Row count**: 20
- **Run date**: 2026-04-20
- **Caveat**: Based on today's inventory import. Inventory data reflects current state only — we cannot determine how long items have been out of stock.

| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
|-----------|--------------|----------------|-----------------|-------------------|---------------|--------------|------------|-----------------|--------------------------|
| HAY-1417-AG | CAT1 | HAYES | Hayes 50'' Aged Brass Linear Chandelier | $471,888.67 | 330 | 0 | 0 | 0 | 2026-06-01 |
| ARA-10269-MK-ST | CAT1 | COL127 | Aragon 58.75'' LED Matte Black Chandelier | $248,691.11 | 96 | 0 | 0 | 0 | 2026-08-18 |
| ARC-1929-GA-CL-MWP | CAT1 | COL70 | Arcadia 61'' Antique Gold Chandelier | $178,098.84 | 59 | 0 | 0 | 0 | 2026-05-27 |
| HAY-1409-PN | CAT1 | HAYES | Hayes 40.5'' Polished Nickel Chandelier | $162,504.95 | 81 | 0 | 0 | 0 | 2026-06-01 |
| ARC-1919-GA-CL-MWP | CAT1 | COL70 | Arcadia 46.25'' Antique Gold Chandelier | $158,805.52 | 99 | 0 | 0 | 0 | 2026-05-25 |
| RIV-382-AG | CAT6 | COL15 | Riverdale 6'' Aged Brass Sconce | $122,663.57 | 1,743 | 0 | 0 | 0 | 2026-05-15 |
| ARC-1909-GA-CL-MWP | CAT1 | COL70 | Arcadia 32.5'' Antique Gold Chandelier | $107,656.77 | 127 | 0 | 0 | 0 | 2026-06-10 |
| FUL-905-BK | CAT2 | COL43 | Fulton 18'' Black Semi Flush Mount | $106,963.06 | 503 | 0 | 0 | 0 | 2026-06-05 |
| NIL-70016-BF-MG | CAT1 | NILES | Niles 54'' Black Forged + Modern Gold Chandelier | $102,294.14 | 211 | 0 | 0 | 0 | 2026-05-25 |
| TRA-A3302-VG | CAT2 | COL8 | Travis 12.5'' Vibrant Gold Semi Flush Mount | $95,760.79 | 945 | 0 | 0 | 0 | 2026-05-14 |
| 517-MT | CAT1 | COL100 | Broche 24.5'' Matte White Chandelier | $94,041.87 | 220 | 0 | 0 | 0 | 2026-05-08 |
| 4456-GA-CL-MWP | CAT1 | COL113 | Filmore 29'' Hand Cut Crystal Antique Gold Chandelier | $90,087.84 | 176 | 0 | 0 | 0 | 2026-06-01 |
| DUM-9802-GE | CAT4 | COL48 | Dumont 9.25'' Graphite Outdoor Sconce | $81,563.67 | 231 | 0 | 0 | 0 | 2026-05-18 |
| BAI-A2109-AG | CAT1 | COL68 | Bailey 48'' Aged Brass Chandelier | $80,402.52 | 136 | 0 | 0 | 0 | 2026-06-15 |
| KEE-A3004-VG | CAT1 | COL32 | Keenan 48'' Vibrant Gold Linear Chandelier | $73,259.14 | 366 | 0 | 0 | 0 | 2026-05-14 |
| 136-CH | CAT1 | COL122 | Calypso 20'' Crystal Teardrop Polished Chrome Chandelier | $73,233.47 | 151 | 0 | 0 | 0 | 2026-05-15 |
| ARC-1905-GA-CL-MWP | CAT1 | COL70 | Arcadia 23.5'' Antique Gold Chandelier | $71,819.10 | 210 | 0 | 0 | 0 | 2026-05-25 |
| JES-B7105-BS | CAT1 | JESSA | Jessa 24'' Burnished Silver Chandelier | $68,945.06 | 185 | 0 | 0 | 0 | 2026-06-10 |
| MSL-306-SA | CAT1 | COL137 | Marselle 24'' Antique Silver Chandelier | $68,549.48 | 177 | 0 | 0 | 0 | 2026-05-08 |
| ADD-321-AG-WH | CAT2 | ADDIS | Addis 22.25'' Aged Brass Flush Mount | $64,393.19 | 86 | 0 | 0 | 0 | 2026-05-25 |
