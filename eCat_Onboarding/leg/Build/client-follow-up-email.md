# Client follow-up — copy/send

**To:** Trey Wilson, Alexandra Briggs, Kyle Smith  
**Subject:** eCat follow-up — confirmations from today’s session + open data items

---

Hi Trey, Alex, Kyle,

Thank you for the time today. The initial catalog is in good shape — collections, categories, related items, and romance copy are tracking correctly. Below is what we locked in on the call, what I’m implementing next, and the open items I need confirmed so we can keep moving between Fridays.

**Agreed today**
1. Trade name = Legrand; collections = adorne / radiant. Keep SKUs individual for now; other finishes/sizes via Related. We can revisit collapsing colors after rep feedback.
2. Prefer collection-first browse so adorne and radiant don’t mix. I’ll enable **Finish** and **product type / category** as filters inside a collection. Spec filters (mounting, gangs, voltage, etc.) only make sense if you can provide that data — see §3 below.
3. Related item mappings looked correct on the spot checks.
4. Romance copy is fine; I’m removing the junk character before adorne® / radiant® (keeping the ®).
5. Sell sheets, literature, and videos belong in **Library**, not on every product page. I’ll continue loading those.
6. Primary use for now = presentations / lists, not order entry. Presentation logo is correct.
7. Daily inventory at ~1:00 a.m. Central is sufficient. I need the feed details in §6 before we schedule Brent, so that conversation is concrete.
8. Recurring Fridays at **12:00 p.m. Eastern / 11:00 a.m. Central / 10:00 a.m. Mountain** on **Teams** — please send the invite when you can.
9. No August hard go-live; Lightovation Dallas / January market as the next milestone.

**I’m implementing now**
- Romance-copy character cleanup  
- Finish + category filters  
- Short description under the product tile (grid always shows the part number on the primary line — that’s fixed in the app; the readable name sits under it)  
- Library uploads from the Drive folder  
- Homepage branding swap once you send the correct asset (§1)

---

**Please confirm / reply on the following**

**1. Homepage branding**  
Please send the image (or asset-portal link) you want on the Legrand homepage in place of the current Europe creative.

**2. Drive / Library**  
- Reply with the obsolete or replaced PDF filenames you mentioned and I’ll remove or swap them.  
- Library for org collateral (vs attaching PDFs on every product) — confirmed today; OK to proceed loading the remaining sell sheets, LED pack, training, CEU, competitor conversion, etc.?  
- Full Library load (~65–70 files + ~9 video/CEU links), or a smaller curated subset first?  
- Competitor Conversion and price-bearing planograms — which user groups should see those?  
- Per-SKU cut sheets / install guides on the product page later only if you can provide a SKU → URL map; otherwise Library stays the home for documents.

**3. Taxonomy**  
- OK keeping the seven best-guess category placements?  
  - Connectivity, Night Lights, Antimicrobial Devices, EV Charging, Locator Light → Switches & Outlets  
  - Fan Control → Dimmers  
  - Smart Dimmer → Smart Technology  
  - Or should we add an Accessories group for the odd ones?  
- Keep **Light Switch** and **Switches** as separate categories (adorne vs radiant wording), or merge?

**4. Pricing & US / Canada**  
Levels live today: US Net, US Retail (MSRP), US iMAP, Canada Net, Canada iMAP, Canada MSRP.

- Are those the right labels, and should reps see all of them?  
- Any promotional prices to load, or none for now?  
- How should US vs Canada be separated — Divisions, User Groups, or both? Canadian customers must default to a CAD level, not US Net.  
- Coverage gaps (all traced to your price files, not our converter):  
  - **Drop from catalog?** No US price + only on CA Discontinued: `1597TRUSBAA`, `1597TRUSBCCI`, `1597TRUSBCCLA`, `1597TRWRUSBCCW`  
  - **Canada-only?** `AWP6GBL1` (Pale Blue 6-gang) — priced in CA, $0 US  
  - **Need updated US price list?** `R26USBPD65WCC6` — new, CA-priced only so far  
  - **OK blank in Canada?** ~20 SKUs never appear in any CA sheet (AFCI/GFCI combo devices + Microban / screwless-plate lines), plus 6 discontinued-in-Canada-only  
  - **CA radiant iMAP:** every radiant row in the CA file is `"N/A"` (adorne CA iMAP is complete). Hide Canada iMAP for radiant, or is a real number coming?

**5. Product content**  
- Spec fields in your source (voltage, wattage, switch type, mounting, gangs, wire size, bulb compatibility, warranty, Prop 65, ROHS, etc.) are empty. Do you have that data to send, or launch without those filters/fields?  
- 908 / 1,020 products have romance copy — OK to leave the other ~112 blank for now?  
- Finish filter near-duplicates — merge any of these, or keep distinct?  
  - Mirror / Mirror White / Mirror Black  
  - Gloss White / Gloss White on White / Powder White / Matte White  
  - Brushed Stainless / Brushed Stainless Steel / Stainless Steel / Spiraled Stainless  
- Source typo we corrected in Related Items: `ASPD1531W277` Product Name said “227V” instead of “277V” — please confirm.  
- ~73 SKUs where Finish column disagrees with the color word in Product Name — happy to send the list if your data team wants to clean the source.  
- 20 SKUs have no matching image file in the download set — do images exist for those, or leave blank?

**6. Inventory (static file + daily feed)**  
Current static load:

- 247 inventory SKUs are not in the product file (e.g. `1597`, `1597BKCCD12`) — discontinued/components to omit, or missing sellable items to add?  
- 73 products have no inventory row — OK that those show no stock until the feed includes them?  
- We set QtyAvailable = QtyOnHand (no separate reserved/backorder columns in the source). Correct?  
- NewItem is “N” on all 1,020 — should any be flagged new?  
- drop_ship = Y on every item; shipped_via = “Fedex or Truck” on every item — real, or placeholder?  
- order_uom: UNIT (843), blank (169), MASTER (8) — intentional?  
- UPCs present on all 1,020 — accurate?

For the **daily 1:00 a.m. Central CSV**, please have whoever owns that feed send:

1. A recent sample (headers + several rows) or a full daily file  
2. Delivery method — email, SFTP, SharePoint, other — and who we should add as a recipient  
3. Column definitions (SKU, qty available / on hand, next receipt, etc.)  
4. Confirmation the SKU matches eCat part numbers (e.g. `AAFN4S16AG4`)  
5. Full file replace each day, or deltas only  
6. One inventory pool vs multiple warehouses / DCs  
7. Technical contact for feed breaks or format changes  

**7. Videos / CEU (Library links)**  
We cannot upload raw MP4. Please send public URLs (YouTube / Vimeo / SharePoint) for:

1. How to - Adjusting Settings of Dimmer Through Control App.mp4  
2. How to - Create a Custom Alexa Voice Activation.mp4  
3. How to - Create a Custom Google Home Voice Activation.mp4  
4. How to - Creating Schedules in Home + Control App.mp4  
5. How to - Install adorne Surface Mount Smart Gateway.mp4  
6. How to - Install radiant Surface Mount Smart Gateway.mp4  
7. How to - Providing Additional User Access to Smart Home.mp4  
8. How to - Setup Smart Gateway with Netatmo.mp4  

Also: a hosted link for **The Art of Resi Lighting 11-6-25.pptx** (~56 MB; over our 30 MB upload cap), or confirm we should use the smaller Art of Residential Lighting PDF instead. The training `.pptm` needs to be re-saved as `.pptx` before upload if you want that in Library.

**8. Customers (next file)**  
We’ll need a real customer file when you’re ready: bill-to / ship-to, **DefaultPriceCode** in the correct currency (US vs CAD), and territory / rep assignment. Only a test customer is in the org today.

**9. Between calls**  
Please use the app and email screenshots anytime something looks off — no need to wait for Friday.

Reply inline on the numbered items above as you’re able; partial answers are fine and keep us from blocking on any one thread.

Best,  
Kylor
