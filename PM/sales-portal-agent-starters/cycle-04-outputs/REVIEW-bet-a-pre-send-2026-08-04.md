DO NOT SEND.

# Bet A pre-send verification

**Reviewed:** 2026-08-04  
**Evidence:** live Jira and Confluence, read-only production Postgres, and the local Rails checkout at `/Users/kylorjohnson/supercat-code/supercat_server`.

## Product-decision error found

The unlabeled tenth Customers CSV field is **not customer class**. The export builds it from `PriceLevel.cue_character`, selected through each customer's `default_price_code` (`app/services/controllers/ecat_customer.rb:49-63,129-134`). Values such as `DN` and `WS` are therefore **price-level cue characters**.

This changes an already-published product instruction. Confluence comment `1820655618` currently tells engineering to “label the tenth column as the customer class it carries.” That instruction would make the CSV structurally valid but semantically mislabeled. Use the exact correction in item 4 below before Brent acts on it.

There is a second stop condition: the Tier 1 account premise moved while this review was running. `brentsanders` is no longer on type 1378; he is now on type 2864 `z'-Bet A Verify`, with six `105:x` territories. `Kylor_Johnson` is no longer on 2864; he is back on type 92 `z-SuperCat`.

A new non-admin member, `betaverify`, was created on type 2864 during the review. Its flags, blank customer number, and admin state are correct, but its territory assignment is malformed: Postgres contains an array with **one concatenated string**, not six territory values:

> `["105:1 Gigi Lane 105:2 Katherine McMullan 105:3 Weezie Ward 105:4 Susan Rutherford 105:5 Grace Ingram 105:6 Krissa DeGennaro Newell"]`

Do not run the wwjc warehouse build until that array is corrected.

## Claim-by-claim result

Numeric database results below were derived on **2026-08-04** unless another date is stated.

| Claim | Result | Evidence / correction |
|---|---|---|
| D1 — SERV-2449 has a duplicated tail | **REFUTED (already fixed)** | The live description has one `Diagnosis pointers` block and one `Out of scope` block. Do not delete anything from the tail now. |
| D2 — SERV-2449 captions are backticked | **CONFIRMED** | Both live captions remain wrapped in backticks. |
| D3 — SERV-2449 remains in June 2026 while comment 38300 says all three were cleared | **CONFIRMED** | `customfield_10020` is sprint 651, `June 2026`, state `active`, board 3. SERV-2447 and SERV-2448 have no sprint. |
| D4 — EBR-40 has a contradictory duplicate bullet and malformed heading | **CONFIRMED** | Live text has `**Done** when` and both the qualified and unqualified no-territory bullets. |
| T1.1 — Brent is on type 1378 with totals/dashboard off and NULL territories | **REFUTED** | Live now: `brentsanders` is on type **2864**, admin on both columns, totals/dashboard flags true, all-customer totals false, and six `105:1`–`105:6` territories. |
| T1.1 — Kylor is on type 2864, org-user non-admin but global user admin | **REFUTED in part** | Admin columns remain `false/true`, but Kylor is now on type **92 `z-SuperCat`**, not 2864; all-customer totals is true. |
| T1.2 — one outer flag encloses all four stat cards | **CONFIRMED as code; no longer describes Brent's current screen** | `index.html.erb:36-101` directly gates LY, CY, selected-range, and Backlog. Brent's current type has the flag true. |
| T1.3 — admin does not override this direct flag | **CONFIRMED** | The view reads `user_type.display_sales_portal_totals` directly. The admin short-circuit is in `UserTypePermissions.may?` at lines 117-125 and is not used on this path. `UserType#get_flag` is at 529-536; the totals flag defaults true, and old type 1378 explicitly stores false. |
| T1.4 — the per-row selected-range column sits outside the stat-card gate | **CONFIRMED** | `render 'list'` is at `index.html.erb:103`; `_list.html.erb:13-15,37-40` gates only on `@custom_totals_by_bill_to.present?`. Controller lines 15-25 compute it independently of the user-type totals flag. |
| T1.5 — header is `Previous YTD Sales`, between CY Sales and Backlog | **CONFIRMED** | Controller line 386 builds `"#{label} Sales"`; `Eol::DateRanges` maps `previous_ytd` to `Previous YTD`; `_list.html.erb:11-16` fixes the ordering. |
| T1.6 — moving Brent to 2864 is side-effect free | **REFUTED** | The move has already happened. It enables the needed cards, but changes trade-name auth custom→all, price-level auth custom→all, product-image download true→false, and `view_products` false→true. Customer syncing and distribution-center auth remain All. Treat 2864 as a temporary walkthrough group, not a permanent equivalent to 1378. |
| T1.6 — type 1378 is a live shared type | **CONFIRMED, count changed** | Seven active users remain after Brent's move: angie, atlantashowroom, brucew, kjael, marco, ognezdyonova, wale. Do not flip its totals flag. |
| New fixture — type 2864 now has a non-admin member | **CONFIRMED, but malformed** | Active members are `brentsanders` (admin/admin) and `betaverify` (non-admin/non-admin). `betaverify` has a blank customer number and the correct type flags, but one concatenated territory value instead of six array elements. |
| T2.1 — type 2864 and the org dashboard gate are configured as stated | **CONFIRMED** | Dashboard true, portal totals true, all-customer totals false, customer syncing All; org-level dashboard flag true. |
| T2.2 — portal dashboard uses `enable_portal_dashboard`, not `view_dashboard` | **CONFIRMED, with omitted gates** | `ecat_permissions_helper.rb:54-59`. The full gate also requires `@show_customers`, org dashboard enablement (or feature flag), and `display_sales_portal_totals`. Thus Brent's old type 1378 would have failed both user-type flags, not only the totals-card gate. The superseded `view_dashboard` claim remains in Confluence pages `1819836417` and `1819901953`; it is not in comments 38276 or 38288 as the handoff suspected. |
| T2.3 — invoice `territory_key` comes from `portal_invoice.rep_number` | **CONFIRMED** | `sales_portal_invoice_dimension.rb:25-35`. |
| T2.4 — direct rep-number matching adds 29 invoices / $43,093.69 and does nothing for Gigi | **CONFIRMED** | YTD window `2026-01-01` through `2026-08-04`: 29 distinct invoices, $43,093.69; Gigi direct-only result 0 / $0.00. There are 72 distinct rep-number strings, 51 comma composites. |
| T2.5 — ship-to casing code defect exists | **CONFIRMED** | Territory sources are downcased in `extracts_and_transforms.rb:18-42`; `territory_to_ship_to_bridge.rb:25-39` looks up raw keys. |
| T2.5 — roughly 150k records across 15+ orgs; listed counts exact | **CONFIRMED concept, REFUTED exact counts** | Current impact is **152,294 ship-tos across 23 orgs**. Current leading counts: cci 75,127; ta 39,632; clli 11,545; kii 10,123; el 3,956; gl 2,349. The 75,114 and 39,610 figures in comment 38300 were a dated snapshot, not current counts. |
| T2.6 — wwjc and kal are unaffected by casing | **CONFIRMED conclusion, REFUTED exact counts** | wwjc: **0 of 14,019** ship-tos have territory data. kal: **3,707**, with zero uppercase-bearing territory values. The previously stated 14,020 and 3,709 have drifted. |
| T2.7 — Gigi and cmallon YTD baselines | **CONFIRMED** | Gigi: 762 invoices, 251 accounts, $830,845.72. Six-territory union: 1,508 invoices, 437 accounts, $1,555,691.19. |
| T2.7 — June closed baseline | **CONFIRMED** | 110 invoices, 75 accounts, $123,585.35 for `2026-06-01` through `2026-06-30`. The five-date stability claim is supportable from the 7/28 export/SQL record, dated 7/29 and 7/30 artifacts, the 8/3 derivation record, and this 8/4 derivation. |
| T2.8 — June 2026 remains the active open sprint on board 3 | **CONFIRMED** | Jira's open-sprint JQL returns sprint 651 as `active`, board 3, ending 2026-06-26. No other active sprint name appeared in those results. |
| T3.1 — cmallon fixture | **CONFIRMED** | Non-admin on both columns; six territories `105:1`–`105:6`; all-customer totals false. Note: cmallon's type has `display_sales_portal_totals=true`, not false. |
| T3.2 — `OrgUser#is_admin?` is either-column | **CONFIRMED** | `org_user.rb:383-386`. |
| T3.3 — substring gate affects six of eight ranges | **CONFIRMED** | Only `previous_ytd` and `custom` contain one of the tested substrings; all_available, current_ytd, previous_year, current_mtd, previous_month, and yesterday fail. |
| T3.4 — CY/LY ignore selected range | **CONFIRMED** | `app/services/controllers/ecat_customer.rb:113-126` uses fixed current/previous calendar-year helpers. |
| T3.5 — 9 headers versus 10 fields | **CONFIRMED** | Export lines 15-31 emit 9 headers and 10 values when custom totals are present; the no-custom branch is 8 versus 9. |
| T3.5 — tenth field is customer class | **REFUTED — product-decision change** | It is a **price-level cue character** from `PriceLevel.cue_character`, keyed by `customer.default_price_code`. |
| T3.6 — feature is on for el and not wwjc | **CONFIRMED in local checkout only** | `config/initializers/enabled_features.rb:75-76` lists only `el`. This does not independently prove which commit/config production is running. |
| T3.7 — screenshots match their captions | **UNVERIFIABLE** | Jira returned blob references and dimensions, not accessible image pixels. The captions' visual truth still needs a human check in Jira. |
| Confluence comment 1820655618 proposed correction | **NECESSARY, but currently malformed** | It was edited at 2026-08-04 17:01Z. Item 6 now contains quoted replacement text, but the old false “On sequencing” paragraph remains beneath it. Item 5 also carries the newly found customer-class error. Repair this comment; do not add a second correction comment. |
| Message A | **REFUTED by current state** | It says Brent is on 1378, Kylor is on 2864, and Brent still needs moving. All three statements are now false. |
| Message B | **DO NOT SEND as drafted** | It repeats “customer class,” says type 2864's sole member is Kylor, says Kylor is creating the needed account, and says all three sprints are cleared. |

## Required corrections — exact actions and text

1. **EBR-40 description**

   Change `**Done** when` to `**Done when**`.

   Delete this bullet only:

   > A user with no territories sees no customer data, never company-wide data.

2. **SERV-2449**

   Remove the backticks from both screenshot captions:

   > Previous Month — the selected-range sales column is missing  
   > Previous YTD — the selected-range sales column is present

   Visually inspect the two images in Jira and confirm each caption is immediately above the matching image. Then clear Sprint `June 2026`. Do **not** delete the description tail; D1 is already fixed.

3. **SERV-2447 comment 38300**

   Clear SERV-2449's Sprint field. That makes the comment's final sentence true without rewriting history. Do not update the dated ship-to counts merely because live imports have changed them.

4. **Confluence page 1820262402, footer comment 1820655618**

   Replace everything from item 5 through the end with:

   > 5. Malformed CSV — IN SCOPE for Phase 4. Nine header fields against ten data fields breaks positional parsing outright. The unlabeled tenth field is the customer's price-level cue character, produced from `PriceLevel.cue_character` through the customer's `default_price_code`; it is not customer class. Label it `Price Level Cue`.
   >
   > 6. Territory baselines moving upward after the ship-to fix — WITHDRAWN. wwjc is unaffected because none of its ship-tos carries a territory code, so no wwjc baseline moves. kal's ship-to territory values contain no uppercase letters, so this defect also cannot explain the original kal / 0016 false negative. The casing defect is real and deserves its own ticket, but it does not touch this bet's verification numbers.
   >
   > On sequencing: the wwjc warehouse build does not depend on the ship-to casing fix. The casing defect is a valuable separate discovery, not the explanation for the original false negative.

5. **Live fixture `betaverify`**

   In the wwjc Admin Console, assign these as **six separate territory selections**, not one pasted string:

   > `105:1 Gigi Lane`  
   > `105:2 Katherine McMullan`  
   > `105:3 Weezie Ward`  
   > `105:4 Susan Rutherford`  
   > `105:5 Grace Ingram`  
   > `105:6 Krissa DeGennaro Newell`

   Verify that `territory_codes` contains six array elements. Only then request the wwjc warehouse build.

6. **SERV-2448 description**

   Replace the paragraph beginning “The only gap is a non-admin member” with this, after correction 5:

   > The non-admin verification member now exists: `betaverify` is non-admin on both admin columns, has a blank customer number, belongs to `z'-Bet A Verify`, and carries `cmallon`'s six territories as six separate assignments. The remaining setup step is the wwjc portal warehouse build, because portal territory access resolves from `rep_to_territory_bridge` rather than the live `org_users.territory_codes` value. Brent's account is also on this type temporarily for the walkthrough, but it is admin and therefore is not the rep-shaped acceptance fixture.

7. **Confluence pages 1819836417 and 1819901953**

   Replace the statements that all 22 wwjc user types have `view_dashboard:false` and therefore no non-admin can open the portal Dashboard with:

   > The Admin Console `view_dashboard` permission does not gate the Sales Portal Dashboard. The portal gate is `should_display_portal_dashboard?`, which reads the user type's `enable_portal_dashboard` and `display_sales_portal_totals` flags plus the org-level dashboard gate. Type 2864 `z'-Bet A Verify` satisfies those gates. Its non-admin fixture is `betaverify`; after its six territory assignments are corrected and the wwjc portal warehouse build runs, it is the rep-shaped production fixture. `brentsanders` is also a temporary member of the type but remains admin on both admin columns, so his walkthrough does not prove rep permission behavior.

   On page `1819901953`, also delete the statement that type 2864 has no further use and can safely be deleted.

8. **Kylor admin-state references**

   In SERV-2447 comment `38290`, Confluence comment `1820655618` item 1, and Confluence pages `1819836417` / `1819901953`, replace “Kylor_Johnson is admin on both columns” with:

   > `Kylor_Johnson` has `org_users.is_admin = false` and `users.is_admin = true`; `OrgUser#is_admin?` therefore still returns true and the admin short-circuit still applies.

9. **SERV-2449 comment 38278 and Confluence pages 1819836417 / 1819901953**

   Replace every description of the unlabeled `DN` / `WS` field as “customer class” with:

   > The unlabeled field is the customer's price-level cue character, produced from `PriceLevel.cue_character` through `customer.default_price_code`.

10. **Message A — replace the full draft**

   Send only after corrections 1-9 and the Sprint clear are complete:

   > Nothing got deleted — all three tickets are live: SERV-2447, SERV-2448, and SERV-2449. I had cleared the Sprint on 2447 and 2448, which dropped them off the June board, while 2449 was still assigned to June. I've now cleared 2449 too, so all three are together in the backlog.
   >
   > You were also right that the two Customers links did not match what I showed. Your wwjc account was on ATL Sales Reps, whose `display_sales_portal_totals` flag is off, so the entire four-card sales band was hidden even though you're an admin; that page reads the flag directly rather than through `may?`.
   >
   > I've moved your wwjc account to `z'-Bet A Verify`, which has the portal totals and Dashboard flags on, so refresh and the links should now match the captures. That is a temporary walkthrough group: it also has broader trade-name and price-level authorization than ATL Sales Reps, so I'll return you to your original group after the review.
   >
   > The per-row comparison is independent of those cards: Previous YTD shows a `Previous YTD Sales` column between CY Sales and Backlog, while Previous Month hides that selected-range column. That's the SERV-2449 before/after.
   >
   > The non-admin `betaverify` fixture now exists with the six territories entered separately. It still needs the wwjc warehouse build before it can produce valid production evidence for SERV-2447 and SERV-2448. Let's step through all three with that distinction explicit.

11. **Message B — replace the full draft**

   > Brent — the six Bet A descriptions are now short enough to work from. Here is the factual handoff, including where we have code evidence versus a live reproduction.
   >
   > **SERV-2449 has the live before/after.** Previous Month hides the selected-range sales column; Previous YTD shows it. The value is already computed correctly and exported, so this is a display gate, not a revenue-math rewrite. `ecat_customers_controller.rb:294` is a Ruby `String#[]` substring test, which is why only `previous_ytd` and `custom` pass out of the eight dropdown ranges. The CSV is also malformed: 9 headers against 10 values. The unlabeled tenth value is a price-level cue character from `PriceLevel.cue_character`, not customer class; the agreed header is `Price Level Cue`.
   >
   > **SERV-2447 is intentionally candid:** there is no valid user-visible reproduction yet. The earlier captures were on admin accounts, which bypass territory permissions. The ticket is justified by the two territory-resolution paths, the missing non-stubbed test, and the fail-closed requirement. Its implementation must keep territory as customer/ship-to assignment. Do not add unconditional invoice `territory_key` matching: that key comes from `portal_invoices.rep_number`, which is EBR-180 / SERV-2178 scope. On wwjc that alternative adds 29 invoices / $43,093.69 YTD outside the bill-to book and adds zero for `105:1 Gigi Lane`.
   >
   > **SERV-2448 uses the same foundation.** I had confused the Admin Console `view_dashboard` permission with the Sales Portal gate. Type `z'-Bet A Verify` already has the portal Dashboard and totals flags on, all-customer totals off, and the org gate is on. I moved your account onto it for this walkthrough, so you can now see the same Customers cards. Your account is still admin and does not prove rep permission behavior. The non-admin `betaverify` fixture now exists with six separate territory assignments; the remaining production-verification setup is the wwjc warehouse build.
   >
   > **The ship-to casing defect is separate.** Current production data shows 152,294 affected ship-tos across 23 orgs, led by cci 75,127 and ta 39,632. It does not affect wwjc, where 0 of 14,019 ship-tos carries a territory code, or kal, whose 3,707 ship-to territory values contain no uppercase letters. It does not gate the wwjc build and does not explain the old kal / 0016 report.
   >
   > **Acceptance:** use the closed June 2026 window for `105:1 Gigi Lane`: 110 invoices, 75 accounts, $123,585.35. Current YTD is 762 invoices / $830,845.72 and continues to drift. I'm the PO acceptance owner; SERV-2447 and SERV-2448 still need a genuine non-admin production walkthrough before final acceptance, but that walkthrough is not a prerequisite for engineering to start from the code evidence and acceptance tests.
   >
   > All three SERV tickets are in To Do and have been removed from the stale June sprint. No local markdown files are needed; the six Jira tickets and the linked Confluence pages are the shared record.

## New problems not listed in the handoff

1. The tenth CSV value is a price-level cue character, not customer class. This changes the required header and an already-published product decision.
2. Brent's user was moved during the verification window. Tier 1 and both draft messages became stale: Brent is now on 2864; Kylor is on 92.
3. The move to type 2864 has non-portal side effects: broader trade-name and price-level authorization, disabled product-image download, and a different `view_products` permission.
4. The newly created `betaverify` user has all six territory labels stored as one concatenated array element. A warehouse build now would create an invalid fixture.
5. Several published records say Kylor is admin on both columns; current production is `org_users.is_admin=false`, `users.is_admin=true`. The conclusion is unchanged, but the stated facts are wrong.
6. Confluence comment `1820655618` is currently internally contradictory after a partial edit.
7. The obsolete `view_dashboard` blocker remains in the bodies of both the AC and evidence pages even though Jira comment 38300 corrected it.

## Sequencing and engineering readiness

SERV-2447 and SERV-2448 descriptions themselves are sufficiently shaped for engineering. No additional ticket rewrite blocks implementation. What blocks the messages is record cleanup and current-state accuracy, not unfinished engineering scope.

Read-only Postgres plus the Rails code is sufficient for engineering to begin and for tests to be written. A corrected non-admin production fixture is **not required before coding**, but it **is required before PO acceptance** of SERV-2447 and SERV-2448. SERV-2449 already has a real before/after route, subject to the remaining human image-caption check.

Do not send Message A or Message B until:

1. EBR-40 is corrected.
2. SERV-2449 captions are fixed, pixels checked, and Sprint cleared.
3. Confluence comment `1820655618` is repaired.
4. The customer-class mislabel is corrected in Jira/Confluence.
5. `betaverify` has six separate territory array elements.
6. SERV-2448 and the Confluence fixture text reflect the new account accurately.
7. The stale Dashboard-gate and Kylor admin-column text are corrected.

After those five actions, send Message A first. Message B can follow immediately; SERV-2447 and SERV-2448 do not need any further description work.
