# Magic Lite - Product & Customer File Update Email

---

**Subject:** Product & Customer File Update — A Few Items + Weekly Standup

---

Hi All,

Quick follow-up on both the product and customer files.

**Product File**
We ran into a few things with the file you sent back — some columns were in the wrong order, a chunk of products were missing, and the price level columns got dropped. No worries, we sorted it out on our end. We rebuilt from the last clean import, fixed the structure, and merged duplicates where needed. The cleaned file (906 products) is imported and live.

There are 4 products that had conflicting info across duplicate rows (different prices, descriptions, etc.) — we went with the most recent values but it'd be good for someone on your side to give those a quick look. Happy to send that list over.

**Customer File**
We combined the ML (421 customers) and NSL (3,096 customers) lists into one file — 3,517 rows total, no overlapping account numbers.

One thing we noticed: a lot of the NSL records (~2,200) had email addresses sitting in the street address field. We moved those over to the BuyerEmail column so they're preserved, but those rows will still need real street addresses added when you get a chance.

There are also some other gaps in the NSL data — missing street addresses, city/state/zip, and country codes on a good number of rows. Nothing unusual for a first pass with a list this size.

We went ahead and uploaded everything as-is. The records with complete data will come through fine, and the ones with gaps will just flag in the import error report so they can be cleaned up in a future update. No rush on any of it.

**Weekly Standup**
We'd love to get the remaining data items buttoned up by end of month. Would it help to set up a quick weekly check-in (15–20 min) to knock out the open items together? Thinking the product conflicts, the NSL address stuff, and whatever else comes up. Happy to send a recurring invite if that works.

Let me know if you have any questions or want to dig into any of this.

Thanks,
Kylor

---

## Internal Notes
- ML customer data: 421 rows, clean, all Canadian (CA), ready to import
- NSL customer data: 3,095 rows, severe data quality issues from source
- 2,215 emails moved from BillToAddress1 → BuyerEmail column (fixed in file)
- Only ~352 NSL rows have complete address data
- Combined file: `ML + NSL CUSTOMERS COMBINED 2.0.csv` (16 columns, includes BuyerEmail)
- Product file: 906 unique products after dedup, 4 conflict BaseItemCodes to review
- BillToCountry blank on 94% of NSL rows — need US/CA codes from client
- Target: all data items resolved by EOM (March 31)
