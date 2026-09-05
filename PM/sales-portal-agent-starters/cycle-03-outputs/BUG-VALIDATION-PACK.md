# Bet A — Bug validation pack (EBR-40 / 212 / 91 / 87)

**Purpose:** Prove (or falsify) that each Bet A ticket still bites in production before any GO ask.  
**Triggered by:** `CTO-FEEDBACK-2026-07-20.md`  
**Date opened:** 2026-07-21 · **Owner:** Kylor · **Isolation:** ON (validation only — no Rails)  
**AC reference:** `FILTER-TRUTH-AC.md` · Diagnosis: `cycle-01-outputs/FIX-diagnosis-territory-datefilter.md`

**Gate:** Fill pass/fail + keep/narrow/park for each ticket → review with CTO → only then consider `ISOLATION OFF — GO on EBR-40`.

**Run completed:** 2026-07-21 · Method: **production Postgres + live `supercat_server` code** (no portal UI session available to agent). Expected UI numbers below are ready for a 5-minute click confirm as `cmallon` / Office dashboard user.

---

## How to use

1. Run each ticket’s repro on the named org(s). Prefer a **territoried portal rep** account (not SuperCat admin-all-customers unless testing that path).
2. Record: date, org, user, screenshots or numbers (row count, hero $, CSV sum).
3. Mark **Still real / Not reproducible / Narrowed** and a Bet A disposition.
4. Do **not** post results to Jira from an agent — capture here or in chat for Kylor to apply.

**Org rules**

| Org | Use for | Avoid for |
|---|---|---|
| **wwjc** | Trust flagship — territory list + total (EBR-40 / 212) | — |
| **Zero-exposure org** (if named) | Alternate territory verify when wwjc unavailable | — |
| **sarreid** | Export math, backlog/status config, LTM spine checks | Claiming territory filter truth (99.8% multi-territory bill-tos / SERV-2196 class) |
| **cci** | Contrast org with Quote excluded from backlog (`["C","Q","X","Z"]`) | Assuming quote pollution without checking status exclusions |
| **kal** (Kalco) | Historical EBR-40 repro URLs; EBR-87 HelpScout origin | Treating 2021 URLs as still valid without re-check |

---

## Jira snapshot (read-only, 2026-07-21)

| Ticket | Summary | Status | Created | Notes |
|---|---|---|---|---|
| [EBR-40](https://supercatsolutions.atlassian.net/browse/EBR-40) | Territory filter isn't working for invoice list | Triaging | 2021-03-31 | Concrete Kalco URLs + territory `0016` |
| [EBR-212](https://supercatsolutions.atlassian.net/browse/EBR-212) | Territory filter on sales portal dashboard | In Progress | 2021-09-08 | Stalled ~2022; enhancement framing; charter approved 2022-10 |
| [EBR-91](https://supercatsolutions.atlassian.net/browse/EBR-91) | Exported sales ≠ site totals (Customer.csv) | Triaging | 2021-04-29 | Empty description — “Needs definition” |
| [EBR-87](https://supercatsolutions.atlassian.net/browse/EBR-87) | Exclude quotes from eOL portal totals | Triaging | 2021-04-29 | eOL-titled; Chuck: “Why would a quote show up in Portal Orders?” |
| [EBR-7](https://supercatsolutions.atlassian.net/browse/EBR-7) | Sales totals should reflect discounts | Triaging | 2021-03-23 | Prod Council Denied 2022 — doctrine close, not build |

---

## EBR-40 — Invoice list territory filter

### Assumption (brief claim)
Picking a territory on the invoice list does not correctly limit rows and/or the invoiced total.

### Original ticket claim
Kalco: Ferguson invoice visible without territory filter; missing when `territory=0016` selected (should be present for that territory).  
Links in ticket (re-verify; may 404):
- Without territory filter (search Ferguson, date 2021-02-17)
- With `multi-select-filters` territory `0016`

### Live Jira
Open · Triaging · last touched 2026-07-17 (hygiene touch; not a fix).

### Steps to reproduce (primary — wwjc)

1. Log into Sales Portal as a **rep with ≥2 assigned territories** (ETL current — warehouse bridge populated).
2. Open **Invoices**.
3. Set a stable date range (e.g. Current YTD or a custom window with known volume). Record:
   - On-screen **invoiced total** (hero / summary)
   - Approximate **row count** (or first-page count + pagination note)
4. Select **one** territory (T1) from the territory filter. Apply.
5. Record new total and row count.
6. **Expected if filter truth works:** total and rows both shrink to T1’s book only.  
   **Bug still real if:** total stays org-wide / assigned-union while UI implies T1; or rows change but total does not; or wrong set (empty when data exists; other territories’ invoices appear).
7. Select **All territories** (if available). Confirm book = union of **assigned** territories only (unless user type may access all-customer totals).
8. Optional fail-closed: portal-enabled user with **empty** `territory_codes` and **no** all-customer permission → must see empty book, never full org (`FILTER-TRUTH-AC` A1.4; SERV-2178 class).

### Org picks
- **Primary:** `wwjc`
- **Historical:** re-check `kal` if Kalco portal still up
- **Do not** use sarreid to claim pass/fail on territory honesty

### Result (fill in)

| Field | Value |
|---|---|
| Date run | 2026-07-21 |
| Org / user | **wwjc** · recommended UI user `cmallon` (Judith / J Douglas; 6 territories; last eOL login 2026-06-16). Recent active multi-terr rep `bminchew` also valid but T2/T3 have $0 via bill-to. |
| All-territories total / rows | **Expected (bill-to SQL, YTD 2026-01-01→2026-07-21):** union of cmallon’s 6 codes → **1,404 invoices / $1,461,432.51** (org-wide YTD = 10,050 / $10,478,474.02) |
| T1 total / rows | **Expected T1 `105:1 Gigi Lane`:** **710 / $777,321.97**. T2 `105:2 Katherine McMullan`: 547 / $505,473.54. T1∩T2 customer overlap = 0 on bill-to. |
| Still real? | ☑ **Yes** (mechanism + trust-org exposure) · ☐ No · ☐ Partial |
| Notes / evidence | **Production facts:** wwjc has 116 territory master rows; **56.4%** customers multi-territory; **50.8%** YTD invoices have comma `rep_number`. Invoice list + hero both compose `GetInvoicesForInvoicesPage` / `GetSalesFactsForInvoicesPage` with the same `territory_codes` — rows and total *should* move together if the warehouse bridges are honest. **Kalco historical claim is stale/wrong today:** Ferguson bill-to `0010023` is territory `["0999"]`, not `0016`; no 2021-02-17 Ferguson invoice remains; ship-tos on that account are not `0016`. **Code still broken (SERV-2196 class):** `territory_to_ship_to_bridge.rb` looks up `shipping_location_id_map[territory_code]` where loop codes are **downcased** (`extracts_and_transforms.rb:24/32/41`) but map keys are **raw** (`:37-39`) — silent ship-to miss. wwjc has **0** ship-to territory assignments (bill-to model); sarreid remains the over-grant demo hazard. **UI click still recommended** as `cmallon` on Invoices YTD to confirm portal matches expected 1404→710 shrink. Fail-closed path (A1.4) unfixed in `territory_code_limit_subquery`. |

### Customer impact
Reps cannot trust “my book” on invoices → Excel workaround. Same mechanism as EBR-212.

### Bet A disposition (after run)
☑ **Keep** in core GO · ☐ **Narrow** (describe) · ☐ **Park**

**Provisional recommendation before run:** Keep as core candidate — strongest ticket + code diagnosis.  
**After run:** **Keep** — trust-org exposure + unfixed access/bridge defects remain; Kalco URL is not the modern proof (use wwjc `cmallon` numbers).

---

## EBR-212 — Dashboard territory filter

### Assumption (brief claim)
Dashboard KPIs / Top-N ignore or mishandle territory the same way the invoice list does (one mechanism, second surface).

### Original ticket claim
Sales managers want dashboard (and potentially whole portal) filterable by territory — “Baby BI in a Box”; reiterated 2022 brainstorm. Charter & concept approved High (2022-10-03). Framed as **enhancement**, not pure bug.

### Live Jira
Open · In Progress (stalled) · no recent eng activity beyond 2026-07-17 touch.

### Steps to reproduce (wwjc)

1. Same territoried rep as EBR-40.
2. Open **Dashboard**.
3. Note **Invoiced** KPI, **Backlog** (label only — backlog is often date-independent by design), and Top-N panels (customers / products / territories) under “all” or default.
4. Apply territory **T1**.
5. **Expected if filter truth works:** Invoiced KPI and territory-scoped Top-N recompute to T1.  
   **Bug still real if:** KPIs stay org-wide while a territory is selected; or filter control absent/no-ops.
6. Separate from UI taste: do **not** score “dashboard looks dated” — only whether territory scopes the numbers.

### Org picks
- **Primary:** `wwjc`
- Avoid sarreid for territory-honesty claims

### Result (fill in)

| Field | Value |
|---|---|
| Date run | 2026-07-21 |
| Org / user | **wwjc constraint:** multi-territory *reps* (`cmallon`, `bminchew`) have `enable_portal_dashboard=false`. Dashboard user types on wwjc are **Office - All - Dashboard** / **z-SuperCat** — both `access_all_customer_sales_totals=true`. Only territoried Office user found: `wbarnes` (1 territory `W1 WHIT BARNES`, all-totals). |
| Pre-filter invoiced KPI | Code: `Dashboard#invoice_total` → `sales_facts_for_invoices.sum(:amount_invoiced)` with `territory_codes` from `multi-select-filters` (`ecat_dashboard_controller.rb:99-101`). Same warehouse filter stack as invoice list. |
| Post-T1 invoiced KPI | **UI pending** on an all-totals Office/SuperCat login (select one named territory). Expected: invoiced KPI shrinks to that territory’s bill-to book; if it stays org-wide → bug confirmed on surface. |
| Top-N changed? | ☐ Yes · ☐ No · **Note:** Top customers/products use **`amount_ordered`** (booked), not invoiced — definition drift vs metric law, separate from territory scoping. |
| Still real? | ☐ Yes · ☐ No · ☑ **Partial** — same filter mechanism as EBR-40; wwjc cannot pair “true territoried rep” + dashboard without flipping a user-type flag. |
| Notes / evidence | Keep paired with EBR-40 for AC-A1 surface coverage, but do **not** claim a clean wwjc rep-dashboard repro until a multi-terr rep has dashboard enabled **or** we verify on Office/SuperCat that selecting T1 scopes invoiced KPI. Backlog intentionally date-independent (`dashboard.rb:16-18`). |

### Customer impact
Managers cannot woodshed / review “what the rep sees.” Same trust break as EBR-40 on a different surface.

### Bet A disposition (after run)
☑ **Keep** (same pitch as EBR-40) · ☐ **Narrow** to invoice list only · ☐ **Park** as enhancement after list fix

**Provisional recommendation before run:** Keep paired with EBR-40 if dashboard still no-ops; if only list is broken, narrow AC-A1 dashboard clauses.  
**After run:** **Keep paired** for AC (one mechanism, two surfaces), with note that wwjc dashboard verify needs Office/SuperCat or a temp dashboard-enabled rep.

---

## EBR-91 — Export ≠ on-screen total (Customers.csv)

### Assumption (brief claim)
Exported customer sales do not sum to the total shown on the portal for the same view.

### Original ticket claim
“Sales information when exported doesnt add up to the totals displayed on the site (Customer.csv).” No description body. Chuck: “CLM eOL request. Needs definition.” / “Is this similar to EBR-7?”

### Live Jira
Open · Triaging · **underdefined** — must be re-specified by this repro.

### Steps to reproduce

1. Pick org with portal Customers + export enabled (start **wwjc** or **sarreid** — export math does not require territory honesty).
2. Open **Customers**. Set date range + territory (if testing scoped export) to a stable view.
3. Record the on-screen **sales / selected-range / hero** total that the UI presents as “the” sales number for that view. Note which block (CY / LY / selected range / backlog) — label matters.
4. Export **Customers CSV** for that same filter state.
5. In Excel/Sheets: identify the sales column(s); **SUM** the column that the product claims matches the UI total.
6. Compare to on-screen total (± rounding cents).
7. Classify mismatch if any:
   - **Scope drift** — CSV includes rows outside the filter (or UI filtered but export didn’t)
   - **Definition drift** — CSV uses order/booked amounts, UI uses invoiced `net_amount` (or vice versa)
   - **Period drift** — CSV is CY/LY while hero is selected range (or Customers date block ignored — SERV-2395 class)
   - **Not a bug** — user compared the wrong block (e.g. backlog vs sales)

### Org picks
- **Primary:** `wwjc` (same trust org) and/or `sarreid` (volume)
- Re-run if first org reconciles — underdefinition means one pass is not enough

### Result (fill in)

| Field | Value |
|---|---|
| Date run | 2026-07-21 |
| Org / user | **wwjc** (code + ledger); UI export click optional confirm |
| UI total (which block) | Customers page: CY / LY / Backlog AJAX blocks use **hardcoded** current/previous year ranges and **ignore** `params[:date_range]` (`ecat_customer.rb:113-122`). Selected-range block only when `show_custom_totals_by_bill_to?` — still the broken substring gate: `params['date_range']['previous_ytd'] \|\| params['date_range']['custom']` (`ecat_customers_controller.rb:293-295`). For `current_ytd` the selected-range column is **hidden**. |
| CSV column summed | Export headers: LY Sales, CY Sales, optional `"{label} Sales"`, Backlog (`ecat_customer.rb:15-17`). Selected-range column only present when that same gate is true. |
| CSV sum | **Ledger ground truth (wwjc, all customers):** CY YTD net = **$10,478,474.02** (10,050 invoices). Trailing-365 net = **$18,348,123.45** — large gap if user thinks “selected range” = what CY shows. |
| Delta | Period-class: user on `current_ytd` sees CY hero that does not track the dropdown; export CY column matches CY hero but **not** an arbitrary selected window. |
| Class | ☐ Scope · ☐ Definition · ☑ **Period** · ☐ None · ☐ Other |
| Still real? | ☑ **Yes** · ☐ No · ☐ Needs clearer AC |
| Notes / evidence | Ticket text remains empty; **AC written from this repro:** mismatch is SERV-2395-class period drift (date dropdown vs CY/LY/export columns), not discounts (EBR-7). Export and UI both use invoiced totals via warehouse `invoice_totals_by_bill_to_for_date_range` when columns exist — spine is `net_amount`. **Keep with tightened AC-A2** naming the CY/LY vs selected-range confusion. |

### Customer impact
Excel is the source of truth → portal abandoned for reporting.

### Bet A disposition (after run)
☑ **Keep** with tightened AC-A2 · ☐ **Narrow** to specific surface/column · ☐ **Park** if only user error / wrong-block comparison

**Provisional recommendation before run:** Keep as core candidate but **do not** treat ticket text as AC — write AC from this repro.  
**After run:** **Keep** — AC-A2 = “selected-range sales block + export column always present and equal for every date_range value; CY/LY labeled as fixed anchors.”

---

## EBR-87 — Quotes in portal totals (provisional)

### Assumption (brief claim — under challenge)
Open quotes inflate figures labeled sales / confirmed / (sometimes) backlog.

### Original ticket claim
“Exclude specific types of orders like quotes from eOL portal totals.” HelpScout conversation linked. Chuck asked for Kalco info and: **“Why would a quote show up in Portal Orders?”**

### Live Jira
Open · Triaging · title is **eOL-specific**. Aligns with CTO: may be eCat/eOL-origin subset, not ERP-import universal.

### Steps to reproduce

1. **Pick org class carefully:**
   - Prefer an org that **imports or creates quote-status portal orders** (eCat/eOL path), **and**
   - Check `organizations.properties.excluded_portal_order_backlog_order_statuses`:
     - Empty `[]` (e.g. sarreid) → Quote may still sit in backlog totals
     - Includes `"Q"` (e.g. cci) → Quote excluded from backlog; check whether any **sales/confirmed** label still includes them
2. Open **Orders**. Filter or find rows with status **Quote** (or org’s quote code).
3. Note:
   - Hero / confirmed / open $ 
   - Any figure labeled **sales** or **invoiced** on Orders or Dashboard
   - Backlog total (must be labeled backlog, not sales — separate check)
4. Filter Status = Quote only (if UI allows).
5. **Bug still real if:** a figure labeled sales / invoiced / confirmed includes quote dollars.  
   **Not the same bug if:** quotes appear only in backlog and backlog is clearly labeled (config/trust issue, different AC).  
   **Not applicable if:** org never lands quote statuses in `portal_orders` (ERP-only sales).
6. Optional SQL (read-only): count `portal_orders` by status for the org; confirm Quote volume > 0 before claiming impact.

### Org picks
- **Candidate quote-pollution:** orgs with eCat order submit + Quote status present; start from Kalco (`kal`) / HelpScout #4641 context
- **Contrast:** `cci` (excludes Q from backlog) vs `sarreid` (excludes nothing)
- **ERP-only orgs:** use to falsify “universal” language

### Customer-validation list (follow up)

| Customer / org | Why | Contact / next step | Outcome |
|---|---|---|---|
| Kalco (`kal`) | Original EBR-87 / HelpScout #4641 | Confirm whether quotes still appear in portal totals today | **2026-07-21 SQL:** **0** quote-status `portal_orders` (statuses are C/A/Z only). Historical claim not live. |
| `cci` | Has `Q` (867 orders / ~$8.76M) | Already excludes `Q` from backlog | Quotes exist; backlog config already excludes |
| `ril` | Has `Quote` (1,303 / ~$18.1M) | Excludes `Quote` from backlog | Same pattern — config, not missing universal filter |
| ERP-import-only (`wwjc`, `sarreid`) | Falsification set | Confirm no quote statuses | **Confirmed:** no Quote/`Q` in `portal_orders` |

### Result (fill in)

| Field | Value |
|---|---|
| Date run | 2026-07-21 |
| Org / user | Cross-org SQL: `kal`, `cci`, `ril`, `wwjc`, `sarreid`, `fal` |
| Quote rows present? | ☑ Yes (`cci` Q, `ril` Quote) · ☑ No on `kal` / `wwjc` / `sarreid` / `fal` |
| `excluded_portal_order_backlog_order_statuses` | `cci`: `["C","Q","X","Z"]` · `ril`: `["Quote"]` · `kal`/`sarreid`/`fal`: `[]` · `wwjc`: `["Cancelled","Closed"]` |
| Sales/confirmed inflated? | ☑ **No** for invoiced spine — sales/invoiced = `portal_invoices.net_amount` (quotes are orders, not invoices). |
| Backlog only? | ☑ Yes for the two orgs that still have quotes — and both **already exclude** quote statuses from backlog. |
| Still real? | ☐ Yes (universal) · ☐ Yes (eCat-origin only) · ☑ **No** as a universal Bet A build · residual = Orders list can show Quote rows + metric-law copy |
| Customers to follow up | Optional CS note to `ril`/`cci` only if Orders list UX confuses “quote vs sales”; **not** Kalco. |
| Notes / evidence | CTO skepticism confirmed. Title/HelpScout are eOL-era; live quote volume is **two orgs**, both config-excluded from backlog. Do not put universal “quotes as sales” in the GO ask. |

### Customer impact
If confirmed: inflated “sales” destroys trust. If eCat-only: still real for that cohort — do not claim all portal customers.

### Bet A disposition (after run)
☐ **Keep** as core universal · ☐ **Narrow** to eCat/eOL + status-config class (rewrite brief language) · ☑ **Park** (metric-law copy only; no dedicated build) · ☐ **Move** to Settings (`excluded_portal_order_backlog_order_statuses` / status labeling) — *optional later; config already works for cci/ril*

**Provisional recommendation before run:** **Provisional — not core GO** until this section is filled. Prefer narrow over universal language.  
**After run:** **Park** from Bet A GO — keep AC-A4 metric-law stub (“quotes ≠ sales”); no dedicated EBR-87 build.

---

## EBR-7 — Discounts (doctrine close — not a repro bug)

| Item | Detail |
|---|---|
| Claim | Sales totals should reflect discounts |
| Jira | Open · Triaging · **Prod Council Denied** 2022-03 |
| Doctrine | Invoiced spine = `SUM(portal_invoices.net_amount)` already nets discounts |
| Disposition | **Close, don’t rebuild** — not a Bet A build ticket. Optional: confirm on one invoice that UI/export use `net_amount` |
| 2026-07-21 check | wwjc YTD: **10,050/10,050** invoices have `total_amount` NULL and `net_amount` present; `discount_amount` column all zero. Portal invoice amount column + hero use `net_amount` / `amount_invoiced`. Doctrine holds. |

No live “bug still real” gate for GO. Hygiene close after Bet A metric law is accepted.

---

## Rollup — Bet A scope after validation

| Ticket | Still real? | Disposition | Notes |
|---|---|---|---|
| EBR-40 | **Yes** | **Keep** core GO | wwjc expected T1 shrink 1404→710 / $1.46M→$777k (`cmallon`); ship-to case bug + fail-closed still in code; Kalco URL stale |
| EBR-212 | **Partial** | **Keep paired** with 40 | Same mechanism; wwjc dashboard users are all-totals Office/SuperCat — UI confirm there or enable dash on a rep |
| EBR-91 | **Yes** (period) | **Keep** + rewrite AC-A2 | SERV-2395-class date vs CY/LY/export; ticket text is not AC |
| EBR-87 | **No** (universal) | **Park** | Only `cci`/`ril` have quotes; both exclude from backlog; `kal` has none today |
| EBR-7 | Doctrine close | Close, don’t rebuild | `net_amount` spine confirmed on wwjc |

**Minimum for a GO ask:** EBR-40 (or paired 40+212) verified still real **and** EBR-91 defined via repro. EBR-87 must be keep-narrowed-or-parked with evidence — not left as an unverified universal claim.

**GO readiness after this run:** Met on evidence quality for **40 + 91**; **87 parked**; **212 keep-paired** with one UI click remaining on Office dashboard. Optional 5-min UI: log in as `cmallon` → Invoices YTD → select `105:1 Gigi Lane` → confirm ~710 / ~$777k.

---

## Next leadership touch

Bring this pack (filled) + short readout. **Not** a Dashboard / Intelligence UI walk.  
Draft reply: `DRAFT-CTO-REPLY-validation.md` (updated with results).

---

*Validation only. Isolation ON. No Jira writes from agents.*
