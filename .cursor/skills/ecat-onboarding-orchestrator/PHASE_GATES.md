# eCat Onboarding — Phase Gates

A phase is **done** only when its gate passes. The orchestrator must not advance to the
next phase otherwise. Each gate is a hard checklist plus, where possible, a tool/query
that produces objective evidence. Prefer evidence over judgment.

Evidence sources:
- `scripts/validate_products.py` — data quality + code inventory
- `scripts/audit_images.py` — image integrity
- `ecat-postgres-audit` — live DB counts/state by org shortname
- Admin Console **Tools → Admin Reports → File Import Status** — import result tier

---

## G1 — Discovery / Kickoff

- [ ] Org shortname confirmed; Admin Console reachable at `supercatsolutions.com/<SHORTNAME>`
- [ ] Contacts, ERP/PIM, product lines, go-live/event date captured
- [ ] Pricing model + territories understood (NetPrice only | imported levels | arithmetic | divisions)
- [ ] Taxonomy method decided: **Standard** (pre-create codes) vs **Auto-Create**
- [ ] `CLIENT_PROFILE.md` filled in (no `{placeholders}` left in Identity/Systems/Pricing)

**Evidence:** profile has zero unfilled `{...}` tokens in the required sections.

---

## G2 — Admin Console pre-flight

- [ ] TradeNameCode exists (Standard method)
- [ ] Groups created first, then categories under them (groups never auto-create)
- [ ] Every unique CollectionCode/CategoryCode from the data exists in Admin (Standard method)
- [ ] Custom product/inventory/customer fields registered with "Send to iPad"
- [ ] Price levels created; codes match the `Price_<code>` columns
- [ ] Option types defined (if options)
- [ ] Flags set as needed: Options import, 12-image, country validation
- [ ] FTP credentials confirmed

**Evidence:** run `validate_products.py`; reconcile its printed CollectionCodes/CategoryCodes
list against Admin one-for-one. Any code not in Admin under Standard method = gate fails.

---

## G3 — Build

- [ ] `validate_products.py` exits 0 (no duplicate BaseItemCode, no blank required fields, Hideable ∈ {Y,N}). Long-BaseItemCode warnings are advisory, NOT a blocker — the importer accepts >20-char codes.
- [ ] **Images (conditional):** only when images are staged **locally** (rare — e.g. a scraped client like mali), `audit_images.py` exits 0. Most clients upload images straight to FTP/Admin and never stage them in the repo — for them, skip the local audit and verify coverage in G5 against the live DB instead.
- [ ] stories.csv: one row per product, ≤ 500 chars
- [ ] `validate_customers.py` exits 0 (required bill-to fields present; `DefaultPriceCode` is a real price level, not `0`/status text — the #1 import blocker). Pass `--price-levels <codes from DB>` to confirm membership.
- [ ] Priced products also have `price_net_price` populated (Net Price mode reads this, not custom levels)
- [ ] Hideable strategy applied: one representative per family `N`, everything else `Y`; all accessories/drivers/controllers `Y`

**Evidence:** `validate_products.py` exits 0. If images were staged locally, `audit_images.py`
exits 0 and 5 hero images spot-check as product cutouts; otherwise image coverage is a G5
check (live DB), not a local-disk check.

---

## G4 — Import

- [ ] Images uploaded BEFORE product import (products.csv references filenames)
- [ ] Import order honored: options → option_groups → products → stories → inventory → customers
- [ ] option_groups.csv re-sent after options.csv
- [ ] Full files sent for customers/inventory/options (omission HARD-deletes)
- [ ] **File Import Status is error-free** — only `Warning`-tier rows, no `Error`/`Fatal`

**Evidence:** File Import Status timestamp is NOT a blue link, or the linked detail shows
zero `Error`/`Fatal` rows. Remember: expected deletes only happen on a clean import — if
deletes didn't run, look for an `Error` row.

---

## G5 — iPad review

- [ ] **Image coverage (authoritative check):** `ecat-postgres-audit` shows `image_exists`
  near the active-product count by shortname — this is the real gate, since most clients'
  images live in FTP/Admin, not on local disk (mali had 691/694 live with only 17 staged locally).
- [ ] Hero image is a product cutout for every visible product (no lifestyle/application as image 1)
- [ ] Visible-product count matches the Hideable plan (not the whole catalog)
- [ ] Prices show correctly per customer type (no $0.00 / blank on priced items)
- [ ] RelatedItems, options, and smartlists resolve on detail pages
- [ ] At least one full review cycle completed; issues logged with screenshots

**Evidence:** `ecat-postgres-audit` confirms visible vs hideable counts and image-match
rate by shortname; reviewer screenshots attached. Budget 2–3 fix/re-import cycles.

---

## G6 — Go-live

- [ ] User groups configured; price-level visibility correct (hide list/net where required)
- [ ] Reps invited; territory codes aligned to customers
- [ ] Order email recipient set
- [ ] ≥ 3 PDF report formats configured
- [ ] Subscription provisioned; training scheduled

**Evidence:** `ecat-go-live` checklist complete; `ecat-postgres-audit` confirms user-group
and distribution-center config.

---

## G7 — Maintenance (recurring)

- [ ] Image two-step run as new photos arrive (upload, then assign)
- [ ] Recurring feeds (inventory/pricing) healthy if applicable
- [ ] Org state tracked (health scorecard / Postgres) at the agreed cadence
- [ ] `HANDOFF.md` updated each session

**Evidence:** latest `ecat-postgres-audit` snapshot stored; HANDOFF reflects current state.
