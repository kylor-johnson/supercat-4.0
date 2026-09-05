# Coaster (CST) Feedback Analysis — March 2026

**Sources:** Marlene Vidal feedback doc (3/6/26) + Coaster call transcript (3/5/26)
**Analyst:** Kylor Johnson
**Date:** March 10, 2026

---

## Mission-Critical Items (Block Go-Live)

These must be resolved before rep training / go-live.

---

### MC1. Pricing Missing for M6–M9 Price Levels

**Priority:** Mission Critical
**Source:** Call (3/5)
**Status:** Data fix needed — Brent action required

**Problem:** Products show no pricing under M6 through M9 price levels. Pricing appears on other levels (e.g. DS) but M6 is blank. This customer's reps rely on M6.

**Root Cause:** Marlene updated the customer file to include M6–M9 default price codes, but the products themselves may not have been re-imported with pricing rows for those levels. In eCat, pricing is stored per product per price level in `ProductPrice` records. If there's no record for a given product + M6 code, the price is blank.

**Fix:** Re-import the product pricing file that includes M6–M9 columns. Verify in Admin Console that products have `ProductPrice` entries for M6. Reps will need to re-sync after the fix.

---

### MC2. Pricing Not Carrying Over to Orders

**Priority:** Mission Critical
**Source:** Call (3/5)
**Status:** Likely same root cause as MC1

**Problem:** Even when prices display in the catalog, they don't appear when products are added to an order. The order line items show no price.

**Root Cause:** Order pricing is computed at runtime by looking up `ProductPrice` records using the order's price level code. If there's no `ProductPrice` record for that product + price level combination, the price resolves to `nil`. Additionally, on the call Kyla identified that "Show Prices" was toggled off in the rep's settings, which hides prices in the catalog and order views.

**Fix:**
1. Ensure M6–M9 product pricing is imported (same as MC1)
2. Verify "Show Prices" is toggled ON in Settings (gear icon) for the rep
3. Verify the customer's `defaultPriceCode` matches an imported price level

---

### MC3. Images Disappearing After Sync/Refresh

**Priority:** Mission Critical
**Source:** Call (3/5)
**Status:** Needs investigation — Brent action required

**Problem:** Product images that were present yesterday are missing today. Specific product mentioned: **509340**. Marlene reports this is recurring — images keep dropping.

**Possible Causes (from codebase analysis):**
1. **Failed re-download:** During sync, the app deletes the existing image file before downloading the replacement. If the download fails (network error, 404, server issue), the image is gone with no fallback.
2. **Orphan purge:** Every 20 syncs, images not referenced by current products and older than 90 days are deleted. If the orphan detection misses alternate image references, valid images could be wrongly purged.
3. **Server-side timestamp change:** If `imageLastModifiedAt` changed on the server, the app thinks it needs to re-download, triggering the delete-then-download flow.

**Fix:** Brent needs to investigate. Check server logs for image availability on product 509340. Review whether the image URL is returning a 404. Check if this correlates with sync timing or orphan purge cycles.

---

### MC4. "New" Flag Showing Incorrectly on Items

**Priority:** Mission Critical
**Source:** Call (3/5)
**Status:** Data fix — Coaster action required

**Problem:** Items in the order view show a "NEW" badge next to the item number, but the items are not new in Coaster's eyes.

**Root Cause:** The "New" badge comes directly from the `NewItem` boolean field in the product import CSV. It's not date-based or automatic. If the product file has `NewItem = T` or `NewItem = Y` for those items, eCat will display them as new.

**Fix:** Coaster needs to review their product export/API feed and ensure the `NewItem` field is set correctly (T/Y only for genuinely new items, F/N for everything else). After updating and re-importing, reps re-sync.

---

## Configurable Now (Admin Console / Super Admin)

These can be addressed through existing settings without code changes.

---

### C1. Rename "Main Color" Filter to "Color Family"

**Source:** PDF feedback
**Status:** Configurable now

**Problem:** The filter shows "Main Color" but Coaster wants "Color Family" which maps to fewer, more generic color options available in their API.

**How to fix:** In Admin Console → Organization → Custom Fields, find the "Main Color" custom field and change its `label` to "Color Family". If the underlying data also needs to change (from specific colors to generic families), Coaster would need to update the product data to use the "Color Family" values from their API instead.

---

### C2. Change Product Detail Subtitle (Group #, Catalog Year, Vendor No)

**Source:** PDF feedback
**Status:** Configurable now (super admin)

**Problem:** The text under each product tile in the catalog shows Group #, Catalog Year, and Vendor Number. Marlene wants it to show "Is Discontinued — Yes or No" instead.

**How to fix:** Update the `ipad_custom_views` setting on the Organization (super admin field). The subtitle lines use template placeholders like `{groupName}`, `{catalogYear}`, `{vendorNumber}`. These can be replaced with `{deleted}` or a custom field that maps to a human-readable discontinued status. Brent or a super admin would need to update this.

---

### C3. Rename "Product Types" in Left Sidebar

**Source:** PDF feedback
**Status:** Configurable now (super admin)

**Problem:** The left sidebar shows "Product Types" but Coaster wants it to show their main categories (Bedroom, Living Room, Dining Room, etc.).

**How to fix:** Set the `product_types_alternative_name` property on the Organization (super admin field). The label can be changed to anything (e.g. "Categories" or "Rooms"). The actual items that appear when tapping are driven by the Groups data — if Coaster's groups are configured as Bedroom, Living Room, Dining Room, etc., those will appear in the drill-down. Verify the group data matches their desired structure.

---

### C4. Price Level Indicator on Order PDF/Email

**Source:** Call (3/5)
**Status:** Likely configurable now

**Problem:** When an order is emailed as a PDF, it just says "Price" with no indication of which price level (DS, M6, etc.) is being used. Reps can't tell what pricing they shared with the customer.

**How to fix:** The order email template system already supports these placeholders:
- `%pricelevelcode%` — e.g. "M6"
- `%pricelevelname%` — e.g. "DS FOB"
- `%pricelevelcue%` — display character

Check if Coaster's order template includes these. If not, add them to the order header section of the template. This may require Brent to update the template if it's not editable in the admin UI. **Note:** This works at the order level, not per line item. Per-line price level would be an enhancement.

---

### C5. Price Level Visible Near Warehouse ID on Customer View

**Source:** Call (3/5)
**Status:** Configurable now

**Problem:** Marlene wants the customer's assigned price level to be visible on the customer screen, near where the warehouse ID is displayed, so reps can quickly reference it.

**How to fix:** Add a customer custom field that displays the `defaultPriceCode` value. Marlene indicated on the call she could likely do this herself.

---

### C6. Verify Grid Ordering Mode (Add to Order from Catalog)

**Source:** PDF feedback
**Status:** Check configuration

**Problem:** Reps find it cumbersome to add items to orders — too many steps from catalog to order.

**How to fix:** The app has a grid ordering mode (`CatalogViewSelectionModeNumeric`) that shows +/- buttons directly on catalog tiles for quick ordering. Verify whether this mode is enabled for Coaster. If it's not, enabling it would significantly improve the order workflow. The reps may simply not know about it.

---

## Enhancement Requests (Product Roadmap)

These require code changes and should be logged in the feature backlog.

---

### E1. Refresh Data Resets to Home Screen

**Source:** PDF feedback

**Problem:** Every data refresh or sync resets the app to the home screen, losing the rep's place. Reps want to refresh data without losing context (e.g. the customer they're working with, the product they were viewing).

**Technical context:** The sync process in `Synchronizer.m` rebuilds the entire data flow and resets navigation state. There's no mechanism to preserve the current navigation context across a sync.

---

### E2. Remove "Collections" from Left Sidebar

**Source:** PDF feedback

**Problem:** Coaster doesn't use Collections and wants to remove it from the sidebar to reduce clutter.

**Technical context:** The left sidebar sections are hardcoded as always-visible in `TopLevelLeftNavViewController.m`. There is no per-org or per-user-type flag to hide individual sidebar sections. The label CAN be renamed via `collections_alternative_name`, but it cannot be hidden without a code change.

---

### E3. Search Scoped to Current Category

**Source:** PDF feedback

**Problem:** The search bar searches ALL products globally, even when the rep is browsing within a specific category. Reps expect search to filter within their current category/collection context.

**Technical context:** `SearchProductSetInfo` creates a new `ProductQuery` with only the search string, completely replacing the current product set. There is no configuration to enable scoped search. Would require changes to `ProductQuery`, `SearchProductSetInfo`, and `BuildsDataFlow` to combine search with the current category/collection context.

---

### E4. Discontinued — Hide vs. Show Toggle

**Source:** PDF feedback

**Problem:** The current "Discontinued" boolean filter shows ONLY discontinued items when selected. Reps want the opposite — the ability to HIDE discontinued items while browsing, with an option to show them if needed.

**Technical context:** Boolean custom field filters work by intersection — they show only items where the field is true. There is no "exclude" or "invert" filter mode. On the server side, `active_products` already excludes deleted items, but the iPad includes them by default. Adding an inverted filter mode would require changes to `ProductQuery.buildFilteredItemsForProductFilter`.

---

### E5. SKU Autofill / Auto-Suggest in Order Entry

**Source:** PDF feedback

**Problem:** When manually typing an item number to add to an order, the system requires the exact, complete SKU. No auto-suggest, no partial matching. This was a key feature in AMP.

**Technical context:** `OrderItemScanView` performs an exact `productForItemNumberCaseInsensitive` lookup only when Return is pressed. There is no incremental search, prefix matching, or suggestion dropdown. Would need a new typeahead/autocomplete component in the order entry flow.

---

### E6. Customer Info Autofill on Presentation Emails

**Source:** PDF feedback + Call (3/5) — Marlene's Mission Critical #2

**Problem:** When building and emailing a presentation, the customer's name and email are not carried over. The rep has to manually enter the recipient email and there's no customer identification on the presentation. In AMP, the customer name was always visible in the header and their email auto-populated as the recipient.

**Technical context:** `ReportPreviewViewController.launchEmailComposer` does not call `setToRecipients` or pull any customer data. It only uses rep/org template data. By contrast, order emails DO pre-fill recipients (org order email as To, customer email as CC). This gap between order emails and presentation emails would require code changes to pass customer context into the report/presentation flow.

---

### E7. Inconsistent Presentation Formats (Share vs. Email Report)

**Source:** PDF feedback

**Problem:** Sharing a presentation via the share sheet produces a different format than using "Email Report." The formatting is inconsistent. Additionally, if reps don't use "Email Report," the presentation may not be saved/archived.

**Technical context:** These are two different code paths with different rendering. Would need investigation and alignment of the output format.

---

### E8. Landed Pricing / $/Cube Calculation

**Source:** PDF feedback + Call (3/5)

**Problem:** Reps need a field to enter "shipping per cube" to calculate estimated landed pricing for container orders. Common calculation: DS FOB Price × $/cube = landed price. This was heavily used in AMP.

**Example from Marlene:** DS - 365 × $1.50/cube (68.69 cubes) = $103.035 → Extended price $468.04 (landed price per item) × qty 50 = $23,402

**Technical context:** No equivalent exists in eCat. Would need a new column/field on the order form with a per-cube rate input and calculated landed price column.

---

### E9. Multiple Carts / Toggle Between Presentation, Proposal, Order

**Source:** PDF feedback

**Problem:** In AMP, reps had 4 accessible carts with item counts visible, and could toggle between presentation, proposal, and order views for items in each cart. This workflow doesn't exist in eCat.

**Technical context:** eCat has a different order/presentation model. This would be a significant feature addition.

---

### E10. Clear Cart / Clear Entire Order

**Source:** Call (3/5)

**Problem:** No "Clear All" button on the order page. Reps working with hundreds of items need a quick way to start over.

**Workaround:** Tap the pencil/edit icon → Select All → Delete. This works but isn't discoverable.

**Technical context:** Would need a "Clear Order" action in `OrderItemsViewController`.

---

### E11. Navigation Friction / Losing Place

**Source:** Call (3/5)

**Problem:** Switching between views (e.g. toggling "Show All Variants," going to a different filter, then coming back) forces the rep to navigate back out and re-establish their context. The app doesn't preserve state well when moving between views.

**Technical context:** Related to the data flow rebuild on navigation changes. The `ProductSetHistoryManager` manages some history, but state is often lost when switching between product set types.

---

## Summary by Priority

### Fix Before Training
| # | Item | Owner |
|---|------|-------|
| MC1 | M6–M9 pricing import | Brent |
| MC2 | Pricing on orders (same root cause + Show Prices toggle) | Brent + rep config |
| MC3 | Images disappearing | Brent (investigate) |
| MC4 | "New" flag incorrect | Coaster (product data) |

### Configure This Week
| # | Item | Owner |
|---|------|-------|
| C1 | Rename "Main Color" → "Color Family" | Admin |
| C2 | Update product subtitle fields | Super admin / Brent |
| C3 | Rename "Product Types" sidebar label | Super admin / Brent |
| C4 | Add price level to order template | Super admin / Brent |
| C5 | Price level on customer view | Marlene (customer custom field) |
| C6 | Verify grid ordering mode | Kylor / Kyla |

### Feature Backlog
| # | Item | Complexity |
|---|------|-----------|
| E1 | Refresh preserves position | Medium |
| E2 | Hide sidebar sections per org | Low |
| E3 | Scoped search within category | Medium |
| E4 | Hide discontinued toggle | Medium |
| E5 | SKU autofill in order entry | Medium |
| E6 | Customer info on presentation emails | Medium |
| E7 | Consistent presentation formats | Low–Medium |
| E8 | Landed pricing ($/cube) | High |
| E9 | Multiple carts + view toggle | High |
| E10 | Clear cart button | Low |
| E11 | Navigation state preservation | Medium |
