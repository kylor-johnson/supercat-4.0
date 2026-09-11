# Open items — flagged but not yet acted on

Everything surfaced during the onboarding-agent programme that needs a human decision or
action and hasn't had one. Started 2026-09-04. **Append as new items appear; strike
through rather than delete when closed, so the record of what was found stays intact.**

Each item says what was measured and what is inferred. Where a consequence hasn't been
proved, it says so — that distinction is why `SCORECARD.md § 12 R1` exists.

---

## A. Client-facing, live right now

### A1 — `ufi` Universal Furniture: 37,816 orders, no delivery mechanism visible
`order_email_recipient` empty, backup empty, `export_type` unset, no export URL,
**zero orders ever marked exported**, 8 sitting queued. 436 orders in the last 90 days.
**Measured.** *Not proved:* that nothing reaches them — a retrieval path outside these
fields may exist. Needs a direct question to whoever owns the account.

### A2 — `fms` Visual Comfort: 17,087 orders, empty recipient
`order_email_recipient` and `company_email` both empty. 27 report formats, so the org is
otherwise well configured. Same question as A1.

### A3 — Fleet: ~20% of orgs email orders nowhere
25 of the 121 orgs with `send_order_email_on_submit = true` have an empty recipient.
Bigger than any single-client finding. Wants a fleet sweep, not a per-org check.

### ~~A4 — `leg` Legrand: 13 registered filter fields, all empty~~ — CLOSED, was never a defect

**Closed 2026-09-04.** The 13 fields were POC/demo residue from the sales process, not part
of the real Legrand build. Kylor deleted the registrations on 2026-09-03.

The full picture, measured:

| where | state |
|---|---|
| `products.csv` (current build file) | all 13 columns **present, 0 populated across 1,020 rows** |
| `custom_fields` as of 2026-08-27 | all 13 registered, `send_to_ipad=true`, 9 as filters, 0 values |
| `custom_fields` as of 2026-09-04 | **deleted.** leg now has 5 fields, all well populated (Finish 1001, CountryOfOrigin 897, drop_ship 1020, shipped_via 1020, order_uom 851) |

They were empty in the file, empty in the registry, and are now gone from the registry.
**No data was ever dropped and nothing rep-facing was ever degraded.** My original framing —
"announced to the client as enabled and delivering nothing" — overstated it.

**Residual, minor:** `build_ecat_files.py` still emits the 13 empty columns, so every import
warns 13 times. Cosmetic; remove them from the generator when convenient.

**What this taught the harness — see G3.**

### A5 — `libco` Lib and Co: 3 filter chips that cannot match
`Dimmable` (880 values), `SlopeCeilingCompatible` (786), `MotionSensor` (162) are
registered `binary` but carry `Yes`/`No`; eCat filters match `Y`/`T`/digits.
**1,828 values across three dead chips.** Also `Rating`: registered `binary` with 907
non-Yes/No values — same family, different problem. Fix is `Yes`/`No` → `Y`/blank in
source plus a re-import.

### A6 — `leg`: Deco Combo, 50 SKUs never imported
Absent from the catalogue in any state — not hidden, not deleted. Sellable radiant
decorator-combo devices with descriptions. **The sheet carries no prices**, so this is not
a re-import fix; the price data has to come from somewhere. Client question.
Note: `Legrand/Notes/2026-09-04_deco_combo_gap.md`.

### A7 — `leg`: 12 discontinued SKUs are rep-visible
8 adorne + 4 radiant marked Discontinued in the client's own June price lists, live with
`hideable = false`, while 23 sheet-mates are already hidden — an incomplete pass.
**Visibility confirmed:** leg has no group restriction (26 of 26 groups `collections_auth='a'`
and `trade_names_auth='a'`) and 0 visible products lack an image, so the photo gate never
fires. `hideable=false` means rep-visible for this org.

### A8 — `leg`: two inventory files overwrite each other daily
Each import hard-deletes and reloads, so only one brand's stock exists at a time.
**The winner has flipped** — 439 rows / adorne on 2026-08-27, 755 rows / radiant as of
2026-09-04 06:01.

### ~~A17 — `leg`: no inventory display alias, "unlike 165 other orgs"~~ — DOWNGRADED, wrong denominator

**Corrected 2026-09-04 by the end-to-end review.** The registration counts are exact —
`i.qty_available` 165 orgs, `i.qty_on_hand` 44, plus six other quantity aliases, and the
`ic.` prefix for division orgs. **The denominator was wrong.**

Of the **187 orgs that actually carry inventory rows, 30 (16%) register no qty alias at
all** — `uhc` among them, and uhc has processed 20,034 orders.

**One in six is a pattern, not an outlier.** My "strong enough anomaly to put to the product
team" does not survive that denominator and is withdrawn. leg and mer having no alias is
unremarkable.

What survives, and is still worth knowing: `custom_fields.alias` is where the display field
is configured, which is the answer BUILD_SPEC B5 was missing. That part stands.

**Related and still open — see F4 in the review:** `mali` registers ten `ic.` aliases, and
the five `NSL_*` keys are absent from all 703 inventory rows while every row is
`LocationCode = 'ML'`. Five `send_to_ipad` display fields carrying the unqualified labels a
rep reads as defaults, with no data behind them. *Not proved:* what the iPad renders for an
absent JSONB key.

### ~~A9 — `drf`: every customer priced at a $1.00 placeholder~~ — CLOSED, by design

**Closed 2026-09-04 on client evidence.** drf is not an ICP client and does not use eCat the
way lighting/furniture clients do. From the 2026-04-29 onboarding call, Suzanne Fukunaga,
verbatim:

> *"There's not going to be any pricing on anything at this point. We don't charge for our
> half-yard cuts, and we don't charge for our waterfalls."* … *"maybe prices going forward
> just to give a, but Brian right now doesn't want prices."*

> *"This is purely to show customer samples and to show them a new product, to order
> waterfalls and samples."*

> *"95% of our business is from POs"* — 70% FOB China, EDI for the rest.

So eCat at drf is a **presentation tool for Showtime**, not an ordering system. No pricing
by design, no inventory (*"Nope"* when asked), and orders are sample requests at $0.00.

The `$1.00` net is a placeholder in a catalogue deliberately built without prices, and
**pricing does live in the stories file**, so a rep can check a price when needed. That is
the intended arrangement, not a workaround that failed.

**My framing was wrong twice over** — I called it a defect, then proposed switching
`DefaultPriceCode` to `list`, which would surface prices the client explicitly does not want
shown.

**Also declared, same source:** *"Our salesmen don't have territories, and we let all our
salespeople look at all our customers."* So drf needs no territory filtering either — B3
passing on drf is incidental, not a requirement.

→ belongs in `config_intent.toml` as `drf: presentation_only`, so no future check reports it.

### A10 — `drf`: order email still a placeholder
Flagged 2026-07-17 as temporary; unchanged. Stated intent on the 2026-05-18 call was
customer service, not the client contact.

### A11 — `pebl`: rep↔customer filtering broken, and it was explicitly designed — CONFIRMED

**Upgraded 2026-09-04. I doubted this one and was wrong.** Territory filtering at pebl was
designed, built, and confirmed to the client in writing. Kylor to Mandy, **2026-07-01**:

> *"I created the 'Pebl Managers' group and moved Priscilla, Mandy, Tom, and Vincent into it.
> You four see all 171 customers — no territory filtering. The nine reps (Annie, Daria, Dawn,
> Gavin, Joe, Marly, Rita, Theresa, Wisteria) stay in 'Peblers' and see only their assigned
> accounts. **Territory codes set** — each rep's territory code is set in their user account
> to match what's in the customer file."*

**Twenty-nine days later, on 2026-07-30**, Mandy re-imported all 171 customers with empty
territory codes (`'[]'`), destroying the customer half of that mapping.

The current state is worse than "empty," because the user half survived:

| user | group | user territory | matching customers |
|---|---|---|---|
| `sales13@peblfurniture.com` | Pebl sales oversea | `["daria"]` | **0** |
| `sales15@peblfurniture.com` | Pebl sales oversea | `["rita"]` | **0** |

Two reps carry a filter pointing at a value no customer holds. Depending on how sync
resolves an unmatched territory they see everything or nothing — neither is the design.

**And the structure has moved further:** the `Peblers` group named in that email no longer
exists, and seven of the nine named reps (Annie, Dawn, Gavin, Joe, Marly, Theresa, Wisteria)
are not in the current user list at all.

**Not proved:** what a rep actually sees on device with an unmatched territory code. That
needs the sync payload or a device. The measurement — designed, confirmed in writing,
subsequently broken — stands on its own.

### A12 — `pebl`: 12 orders reference a deleted price level
$264,130 against price level `project`, which no longer exists in the org.

### A13 — `mali`: empty order recipient, 4 dangling references
`order_email_recipient` and backup both empty. Dangling: an eOL site pointing at price
level 5722 (exists in no org — **since fixed**, both sites now resolve), a deleted
MobileSite link in an admin-training email, a bulk-invite link pointing **into org `tcd`**,
and a "we set up two Distribution Centers" email against `distribution_centers = 0`.

### A14 — `mer` 111Mercer: 0 images on all 102 products
Catalogue is correct and priced; nothing to show on the iPad yet.

### A15 — `uhc`: org's own record disagrees with where mail goes
`company_email = sales@uniwarehouseware.com`, order mail → `uniwarehs@gmail.com`.
20,032 orders have gone through it, so it works — but it is an accepted mismatch, not a
correct configuration. Re-examine first if delivery is ever reported flaky.

### A16 — `drf`: the support handoff didn't hold
Kyla declared handoff 2026-07-20 and last appeared 2026-07-29. Suzanne's 2026-08-11
message addressed to "Kyla or support person" was answered by Kylor. Four action items
Kyla promised "this week" have no answer anywhere in the corpus.

---

### ~~A18 — `libco`: every barcode ships with a float tail~~ — DOWNGRADED, live is clean

Found 2026-09-05 by the Phase 2 blind run, **before any build**, in the source file.
`UPCValue` is a text field carrying a float representation on **100% of rows**. A barcode
with a decimal tail is not the barcode. Distinct from a formatting nit because the value is
what a scanner matches against.

**Measured:** the source column, 897/897. **Not established:** what the live org currently
holds, or whether the existing build already strips it — the blind rule forbade reading the
build. **Confirm against live `products` before this reaches the client.**

Same run found `ShipWeight` float-tailed on 822 rows, missed initially by the validator's
own >50% prevalence threshold (41%). Threshold removed.

**CONFIRMED AGAINST LIVE 2026-09-05 — and it does not hold.** Org 288, 915 live products,
912 with a populated `upc_value`: **0 carry a float tail.** Specimen of a live value:
`810117540005` — clean. The existing build already strips it.

So the measurement was right about the SOURCE and wrong about the consequence. Nothing on
any iPad has a bad barcode, and nothing needs telling to the client. This is a **source
hygiene note and a code hazard for the next regeneration**, not a live defect — the §12 R1
distinction, and the fourth time on this programme that a true measurement pointed at a
false consequence.

What survives: any mapping reading that xlsx must strip the tail explicitly, because
`openpyxl` returns every numeric cell as a float and `UPCValue` is a TEXT field. That is
now `ecatlib.values.strip_float_tail`, and it is in the libco mapping.

### A19 — `libco`: Yes/No on binary filters — CONFIRMED live, narrower than filed, and it is A5

Registered as booleans, populated with `Yes`/`No`. eCat's boolean tokens are `Y`/`N`.

**CONFIRMED AGAINST LIVE 2026-09-05, org 288, with the scope corrected.** I filed this as
*five* fields. Only **three** of the five are registered with `use_as_filter = 'binary'`:

| field | live values | registered |
|---|---|---|
| `Dimmable` (`ecat_custom_field_27`) | Yes 871 / No 9 = **880** | binary filter |
| `SlopeCeilingCompatible` (`_37`) | Yes 733 / No 53 = **786** | binary filter |
| `MotionSensor` (`_40`) | No 160 / Yes 2 = **162** | binary filter |
| **total** | **1,828** | **3 chips** |
| `BulbIncluded` (`_36`) | Yes 493 / No 74 = 567 | `send_to_ipad`, **not a filter** |
| `ADA` (`_32`) | Yes only | `send_to_ipad`, **not a filter** |

`BulbIncluded` and `ADA` are detail-view fields, where `Yes`/`No` is the correct and
readable value. **Filing them as defects would have been wrong.**

`Rating` (`_31`) is separately registered `binary` and carries **Damp 628 / Dry 279 = 907** —
neither `Yes/No` nor `Y/N`, and unambiguous whatever eCat's matcher does.

**This is A5, re-derived independently from the source by an agent that had never read A5.**
Same three fields, same 1,828, same `Rating` footnote. Not a new finding — it is
corroboration of an existing one by a different route, which is worth more than a fifth
instance would have been. **Merge A19 into A5.**

Standing caveat unchanged: whether eCat's boolean matcher is first-character or exact has
**not** been settled from the product side. `Rating` is unambiguous; the `Yes`/`No` three
are conditional on that answer.

### ~~A20 — `libco`: 15 `FinishCode` case-duplicates~~ — DOWNGRADED, live is clean

`Aged Brass` and `Aged brass` are two filter facets for one finish, in the SOURCE file.

**CONFIRMED AGAINST LIVE 2026-09-05 — and it does not hold.** Org 288, `FinishCode` is
`ecat_custom_field_14`, registered `use_as_filter = 'multi'`. Live: **43 distinct finishes,
907 values, and ZERO pairs differing only by case.** The existing build already normalises
them.

Same shape as A18: true of the source, false of the live org. A source-hygiene finding for
any future regeneration, not something a rep is seeing and not something to raise with the
client.

### A21 — `libco`: image references with no file — CONFIRMED live, 199 of 1,992

Found blind in the source: 191 of 1,812 references with no file in either image folder.

**CONFIRMED AGAINST LIVE 2026-09-05.** Org 288, references read from `products.images_json`
(**not** `products.images`, which is empty on all 915 — the sibling-column trap again) and
checked against the org's `product_images` library of 2,796 files:

```
1,992 distinct image references
  199 resolve to no file in the org library   (10.0%)
  190 products affected
```

**The consequence splits, and the split is the whole point:**

- **190 are SECONDARY images** (position > 1, every one ending `-1.jpg`). Those products
  show their primary image; a secondary slot resolves to nothing.
- **9 are PRIMARY images** (position 1). Those 9 products have **no image at all** —
  corroborated independently by `image_exists = false` on exactly 9 of 915 products, a
  different column reaching the same number. Specimens: `12069-01`, `12069-02`, `12070-01`,
  `12298`, `12299`.

Those 9 are the SKUs added by `rebuild_lib_co_files.py`'s hand-written `FORCE_ADD_PRODUCTS`
manifest — rows cloned from a template, which is why no image was ever uploaded for them.

So: **"191 products have no image" would have been false.** 9 do. 190 are missing one
secondary view. Both are worth fixing and they are not the same conversation.

An image import runs clean with all 199 missing — D10 again.

### A22 — the blind-mapping run works, and its most useful output was a failure

`libco` was mapped blind — source files only, forbidden from opening
`rebuild_lib_co_files.py` or the existing `products.csv` until the mapping was written and
committed. Four calls were wrong, and **three were the same mistake**: renaming a header,
dropping `ShipLBS`, dropping `Video` — all reasonable improvements to a file where a human
had already decided.

**Class 2 is `validate, do not transform`, and the agent was wrong 3 for 3 in exactly the
way the rule predicts.** That is the empirical justification for the rule, and it argues
the rule should be a **hard guard in `mapper.py`** — a class-2 file's headers are immutable
and column drops require an explicit per-field override — not prose in a kickoff.

**IMPLEMENTED 2026-09-05.** `Engine.class2_guard()` in `mapping/mapper.py`. On any mapping
declaring `input_class = 2` or `mode = "validate"` the engine REFUSES to run when a field's
output name differs from its source column without a `rename_reason`, or when a source
column is neither emitted nor declared in `[[drop]]` with a `reason`. Pointed at the libco
mapping as written blind, it refuses with exactly the three violations:

```
CLASS-2 GUARD (OPEN_ITEMS A22) — 3 violation(s):
   - header renamed 'netprice' -> 'NetPrice' with no `rename_reason`
   - source column 'ShipLBS' is not emitted and not declared in [[drop]]
   - source column 'Video' is not emitted and not declared in [[drop]]
```

The libco mapping has been corrected the way the rule prescribes rather than annotated
around it: the rename is reverted (the lowercase header is now a validation FINDING), and
both columns ship. Byte-exact columns went 27 -> 29 of 63 as a result.

### A23 — filing A18–A21 into §A was 50% wrong, and the caveat did not save it

I filed four libco findings into **§A — the client-issue section** — from source-file
evidence, each carrying *"confirm against live before this reaches the client."* Two were
then refuted outright (A18, A20) and a third had the wrong consequence (A21: "191 products
have no image" would have been false; it is 9).

The caveat was correct and insufficient. **§A is the section someone reads to decide what
to tell a client**, so a finding's presence here is itself a claim. The rule that cost us
F1 is not *attach a caveat* — it is **confirm first, then file.**

**Changed:** source-only findings stay in the session report until confirmed against live.
§A means confirmed. See also §F.

### A24 — `cl`: 212 users, no import in 134 days, no order since 2025-02-28

Surfaced 2026-09-05 by F6's org-state header, **on an org that had been returning clean.**

```
users        212 provisioned · 184 ever logged in · 11 active in 30d
last import  2026-04-24   (134 days)
last order   2025-02-28
```

Not a defect — a **business signal**, and the first one this programme has produced. It is
also precisely what the cold read said a green report must not be able to hide. Whether
`cl` is dormant, seasonal or churning is a question for the account owner, not the harness.

Same run, from `login_events`: **`ufi` 15, `clli` 13, `pebl` 10 users who appear in
`login_events` with no `org_users` row today** — accounts destroyed rather than
deactivated. `pebl`'s ten are Mandy's, and they are why 27 of 93 `pebl` orders carry
`org_user_id` NULL. D13/D16's *"three sources nothing reads"* is now partly read.

### A25 — `drf`: 62 products carry `-` as their image filename, and all 62 render as missing

Found by the Phase 2 blind run in the built file; **confirmed against live 2026-09-05**,
org 290, BEFORE filing here — per A23, §A means confirmed.

**Measured:**

```
1,627 live products
1,564 image_exists = true
   63 image_exists = FALSE
   62 of those carry the literal string "-" in images_json
    0 of the 62 resolve                       (dash_but_resolves = 0)
    0 files named "-" or "-.jpg" exist in the org's 1,564-file image library
    1 further product is imageless for a different reason
```

**Consequence, and it is now established rather than assumed:** `-` is **not** a known
placeholder that the app renders as anything. It is an ordinary filename that matches no
file, so those 62 products show no image. The question this item was raised to settle —
*missing, or a deliberate placeholder?* — has an answer: **missing.**

**Not a single category.** 26 of the 62 are `*-WF-ASSORTED`, but 96 `-WF-ASSORTED` SKUs
exist in total so the suffix does not predict it. The other 36 are a mix — `CARMINE
SB-ASSORTED`, `CELARA SB-ASSORTED`, and ordinary colourways like `ECHELON-GINGER`,
`ECHELON-SAFARI`, `ECHELON-STEEL`. So this is not "assortment cards have no photo"; it is
62 individually unresolved rows.

Same family as `pebl`'s doubled `.jpg.jpg` and `mali`'s ~200 wrong photos: **an image
import runs clean with all 62 in place.** A literal `-` is a valid string; nothing rejects
it.

### A26 — **DO NOT REGENERATE `mali` CUSTOMERS FROM THE AVAILABLE EXPORT** — data-loss hazard

Found 2026-09-05 by the Phase 2b run. Filed at this weight because the operation looks
routine and destroys production data.

`customers.csv` **HARD-DELETES ALL customers and ship-tos, then reloads.** Measured against
`mali`'s live org, the export the repo holds is not a faithful representation of live:

| | |
|---|---|
| addresses **blank in the export, filled live** | **2,701** |
| postcodes where both are filled and they **disagree** | 1,428 |
| `BillToAddress1` content | holds **contact names**, not addresses |

So a regeneration from that export, imported normally, **blanks 2,701 live addresses.**
Nothing about the run would look wrong: the file parses, the import reads clean, and the
deletes fire precisely *because* it is clean (deletes only run on a warnings-only import).

**Same shape as the 111Mercer incident** — Legrand's 1,020-row `products.csv` imported into
`mer` on 2026-08-18, soft-deleting all 102 of their products, second occurrence of that
failure mode. This one would be worse: customers hard-delete, so there is no `deleted=true`
to reverse.

**Rules until an enriched export exists:**

1. `mali` customer regeneration is **blocked**. Not "careful" — blocked.
2. The mapping carries the live addresses forward and **declares them as carried**, which
   the Phase 2b run already does. That declaration must survive any future edit.
3. The outstanding ask is an export that includes address fields. Until it lands, live
   Postgres is the only complete record of mali's customer addresses.
4. `a1_fingerprint.py` does not protect against this. It confirms the file's item codes
   overlap the target org — it says nothing about whether the file's *contents* are poorer
   than live. **That is a gap in the pre-upload gate**, and it generalises past mali: any
   regeneration from a lossy export passes A1 and destroys data.

#### A26a — the worse hazard is not the blank addresses, it is a silent repricing of every customer

Found 2026-09-09 by B7's spot-check, which is the check that was almost not built.

A26 documents mali's export as blanking ~2,700 addresses and disagreeing on 1,428
postcodes. Both are true and both are the smaller problem.

```
FILE   nsllist 3,096  +  mllist 421  =  3,517     every row a *list* level
LIVE   nsldn   3,003  +  mldn   415  =  3,418     every row a *dn* (discount net) level
                                                   ZERO overlap
```

**`DefaultPriceCode` disagrees on 49 of 49 sampled rows.** Importing that file moves **all
3,418 mali customers off discount pricing and onto list pricing.** That does not change
what an address field says — it changes **what every rep quotes**, on every customer, from
the next sync.

**It is invisible to every other gate:**

| gate | why it misses |
|---|---|
| B7 density | 100% filled in the file, 100% filled live — no drop to detect |
| A1 fingerprint | every key is present and matches the org |
| B6 carry-forward | no previous generated file to diff against |
| the importer | valid codes, clean parse, clean import |

Only a **value-level spot-check on matched keys** sees it. The 50-row sample caught it at
100% disagreement, which is the argument for pairing the spot-check with the density check
rather than shipping density alone.

The same sample also found disagreements A26 never recorded: `BillToCity` 45%,
`BillToState` 26%, `BillToAddress1` 70% — the last being A26's *"BillToAddress1 holds
contact names"* caught in the act, specimen `16304: file='BILL HALEY' live='15 COMMERCE
DRIVE'`.

**A26's block on mali customer regeneration stands and is now underwritten by a second,
larger reason.** Nothing is at immediate risk. But if the block is ever lifted on the
grounds that "the addresses were fixed," the repricing is still there and still silent.

### ~~A27 — user counts include SuperCat staff~~ — RESOLVED 2026-09-05

Found 2026-09-05 by the session-prep run. `kylor22johnson@gmail.com` is the admin account on
both `leg` and `mer`, so filtering on `@supercatsolutions.com` misses it. `mer`'s "2 users
logged in" is really **1**.

**This reaches back into a tool marked done.** F6's org-state header counts users, and the
at-risk rule reasons about provisioning. Both are soft by however many staff accounts sit
in an org — including **A24's headline**, `cl`'s *"212 users, 184 ever logged in, 11 active"*,
which is the finding that justified building the header at all.

**RESOLVED.** The rule, derived and tested rather than assumed:

```sql
staff = users.billable IS FALSE  OR  email ILIKE '%@supercatsolutions.com'
```

Both halves earn their place. `billable` catches the **24** on personal or contractor
domains a filter misses — including `kylor22johnson@gmail.com`, `is_admin = true`, member
of 110 orgs. The domain half catches the **39** staff seats marked billable: test and demo
accounts provisioned inside client orgs (`chuck+911@`, `steve+53@`, `kyla+rep@`,
`brent+demo2@`, `sarah+test@`).

Fleet: **96 staff** (33 both signals · 24 billable-only · 39 domain-only = 96) against
70,008 client-side, total 70,104. `login_events.is_super_user` corroborates independently —
10 accounts, none missed. **Residual named, not zero:** a staff member on a personal domain
holding a billable seat is invisible to both signals.

**A24 recounted, and it survives:** 204 client-side provisioned · 182 ever logged in · **11
active in 30d, unchanged — none of cl's active users are staff.** 283 orders, 0
staff-placed, last order 2025-02-28. Fit to send. (Worth noting alongside it: cl's
Inventory was last imported **2023-02-08** and Customers 2024-10-11 — older signals than
the 134-day figure that raised the flag.)

Proportional damage was worst on small onboarding orgs: `sp` −41% of provisioned, `leg`
−29%, `mer` −25%. The header now states staff-exclusion, names the rule, and lists the
excluded addresses, so the definition travels with the number.

### A28 — a user in many orgs is normally a REP, not staff — and it breaks sender→org attribution

Found 2026-09-05 while deriving the staff rule, by testing a hypothesis rather than
adopting it. **This is a domain fact about eCat's market, and it invalidates an inference
that holds in most SaaS.**

eCat's client-side population includes **multi-line rep agencies and multi-brand dealers
who legitimately hold accounts at many manufacturers**:

```
riccisales.com             5 accounts, up to 11 orgs   jeff@ jessica@ maureen@ rob@ steve@
decorlightingsales.com     5 accounts, up to 15 orgs   allison@ nick@ tami@
pacificliteforcesales.com  8 accounts, up to 13 orgs
lightingvision@comcast.net                   16 orgs
christieslightinggallery@gmail.com          10+ orgs
```

**2,982 accounts sit in 5+ orgs and none of them are staff.** Using org-count as a staff
signal would have misclassified thousands of real client users. By contrast, the 57
non-billable accounts average **32.4** orgs (max 167) against 70,047 billable averaging
**1.6** (max 17) — `billable` separates where org-count does not.

**Two consequences beyond the staff question:**

1. **An email domain does not identify a client org.** A message from `riccisales.com`
   could concern any of eleven manufacturers. Any tool that routes correspondence,
   attributes a ticket, or scopes a corpus by sender domain **must disambiguate** —
   probably by the org named in the thread, or by asking. This directly constrains the
   **correspondence agent**.
2. **Personal and free-mail domains are load-bearing client identities**, not noise.
   `lightingvision@comcast.net` holds accounts at 16 orgs. A rule that drops free-mail
   domains as "staff and personal logins" loses real users — the session-prep skill
   currently does this at SKILL.md:149 and should be narrowed to the staff rule above.

## B. Decisions needed, not defects

### B1 — `leg` MATRIX sheet: products or matrix options?
22 SKUs, header on row 4. 16 already in the catalogue as ordinary products (8 hidden,
3 live), so the current build already decided. **Recommendation: leave as products.**
`matrix_options.csv` hard-deletes and reloads on import, so building one speculatively is
the expensive mistake. Does Legrand price these as combinations? One line in the next email.

### B2 — `leg`: `Catalyst` and `Futura` user groups deviate
`Catalyst` is `shared_resources_auth='a'` with 0 scoped resources; its 23 peer agency
groups are `'c'` with 96. `Futura` has 95. Intended, or missed?

### B3 — Legrand image batches were never reconciled
~2,000 files diverging in both directions between the archived 4.0 tree and canonical.
`images_batch_02_NEW` is 500/0, `images_missing_batch` is 0/613. Needs someone who knows
which batches actually reached FTP.

### B4 — `00_KICKOFF_PROMPT.md` points at an archived folder
Still says copy `_Template/` → `<Client>/`; `_Template` moved to
`_ARCHIVE_superseded_2026-09-03/`. Repoint at `02_Implementation/_Template` or archive
the prompt.

---

### B5 — `pebl` has a fourth distributor group nobody has documented

Found 2026-09-04 while verifying a rep count. `whiteline`, holding
`hadi@whitelinemod.com`, sits alongside the three already known: `ICA`
(`ckirbeyi@ica.com.tr`, Turkey), `Albania-Sezon Dekor` (`info@sezondekor.com`) and `ETC`
(`eltecul@hotmail.com`).

Not a defect — a gap in our understanding. pebl's group structure has been described in
`SCORECARD` §9 and in `config_intent.toml` as six user types, and the distributor layer was
characterised from the three we happened to notice. There is a fourth.

**Why it matters:** anything that reasons about pebl's structure — the config checker's
conformance rule especially — is working from an incomplete picture, and an undocumented
group is exactly the shape that later gets flagged as an anomaly and wastes a cycle.

**Action:** confirm whiteline is a real distributor (whitelinemod.com is a furniture
brand), then record all four in `config_intent.toml` with the same treatment ICA and
Albania-Sezon Dekor already have. While there, re-derive the group list from the database
rather than from notes — if one was missed, others may be.

**Related:** `ica.com.tr` and `sezondekor.com` were originally mischaracterised as Turkish
suppliers and corrected to distributors on 2026-08-25 (`corpus.py` note). `whitelinemod.com`
should be checked for HelpScout tickets on the same basis — the three known distributors
have zero, which is why they stayed invisible to the corpus builder.

## C. Unexplained counts — chase when convenient

| # | item | detail |
|---|---|---|
| C1 | `mali` customers | source COMBINED 2.0 has 3,517 rows, live has 3,418 — 99 unaccounted |
| C2 | `leg` customer source | 1,133 live customers, no customer file anywhere in `Source Data/` |
| C3 | `drf` inventory | 0 rows live; verified count, not an assumption. By design? |
| C4 | `mer` customers | 0 live, no customer source in the folder |

---

### C5 — `pebl`'s group set changed under us; `ICA` is gone

**Measured 2026-08-25:** pebl had a user group named `ICA` holding `ckirbeyi@ica.com.tr`,
with 2 submitted orders. Recorded in `SCORECARD` §9 and in `corpus.py`'s pebl note as one of
two named distributors.

**Measured 2026-09-04:** six groups — `Pebl sales oversea` (9), `Pebl Managers` (3),
`Pebl sales domestic` (2), `Albania-Sezon Dekor` (1), `whiteline` (1), `ETC` (1). **No `ICA`,
and `ckirbeyi@ica.com.tr` has no `org_users` row at all** — not disabled, absent.

So between those dates the group and its user were removed, and `whiteline` appeared (B5).

**Two consequences, and the second is the important one:**

1. `SCORECARD` §9 and the `corpus.py` pebl note now describe a group that does not exist.
   Record ICA as *removed on or before 2026-09-04* with its prior state, so the next reader
   does not go looking for it.
2. **The group set is not stable, so no conformance rule may cache it.** B5 concluded
   "distributor-to-group mapping is not 1:1" — correct, and the reason is not that it never
   was, but that pebl's structure moved. Any config check must re-derive the group list
   every run.

**This is the third client whose structure changed mid-programme** — leg's 13 custom fields
deleted 2026-09-03, mali's price-level 5722 dangler resolved, pebl's groups here. It is the
strongest practical argument for the dated-measurement convention: two accurate readings
taken weeks apart will disagree, and without dates one of them just looks wrong.

---

## D. Programme work not done

- **Fine Art (`fal`) as a transacting control.** 6,734 products, 6,872 customers, 3,902 orders — the only genuinely transacting org in the set. Targeted queries, not a corpus. Would let "here's what healthy looks like" rest on observation instead of inference.
- **`SCORECARD.md` § 13 — the verdict.** repair / replace / reframe. Evidence points at *reframe*. Never written.
- **A second blind read of one client**, to test reproducibility. All five are single runs; two independent runs agreeing would be much stronger evidence than one run agreeing with the framework.
- **Session-prep skill** — agent #2, kickoff never written. Mostly assembly of `corpus.py` + `rawstate.py`.
- **Snapshot bridge**, then eve. Blocked on nothing but sequence.

### D6 — Use the whole fleet as corpus, not just the 6 source-file clients

Raised 2026-09-04. The idea is right but splits in two, and the halves have different
answers.

**Mapping (source → eCat): no, and it cannot be fixed retroactively.** Learning a mapping
needs input/output *pairs*. The database holds outputs for 200+ orgs, but the source files
are gone for nearly all of them — 3 of the 6 clients surveyed had no `Source Data/` folder
at all. The mapping corpus is those ~6 clients and more orgs do not enlarge it. Treat that
as a ceiling, and start archiving source files for every new client so the ceiling rises
over time.

**Validation, config profiling and error taxonomy: yes, and it is the most valuable
corpus available.** Proof of concept, one query: the inventory-display config turned out to
be `custom_fields.alias` with a 165 / 44 fleet split — a question five clients could not
have answered and that I would otherwise have guessed at.

Three things only the fleet provides:
1. **What "correct" looks like empirically** — not "leg has 26 user groups" but "orgs of this shape have N, configured this way." This is the config agent's missing expected-profile.
2. **The complete import error taxonomy** — every warning and error ever produced, ranked by frequency, instead of the handful of incident types five clients surfaced.
3. **Archetype config profiles** — lighting vs furniture vs fabric, what each actually enables.

**Timing — this is the part that matters.** Do NOT expand scope before Phase 0/1 land. But
the `import_events` YAML parser being written for A4 and B4 has a second job: written once
for one org, running it fleet-wide is nearly free, and it converts the entire import
history into the error taxonomy. Build that parser knowing it will be pointed at
everything.

**Caveat when it runs:** `import_events` is large enough that a naive `sum(length(data))`
across the whole table times out at 30s. Batch by org.

---

### D17 — `drf`: the source folder is one season's supplement, and nothing says so

**This is the drf failure reproduced exactly, and it is a finding about the SOURCE FOLDER,
not about any mapping.**

`Source Data/` contains three files. The only product file is `Characteristics Interwoven
spring 2026_eCat MAPPED (1).csv` — 11.7 KB, **72 patterns**, no images, no prices, no
colourways. Reconciled against the built catalogue (pinned before scoring):

```
built SKUs                                      1,627
  attributable to one of the source's 72 patterns   743   (45.7%)
  belonging to a family ABSENT from the source      884   (54.3%)

built pattern families                            115
source patterns                                    72
  appearing in the build                           55
  appearing NOWHERE in the build                   17
colourways per pattern                     min 4, max 28, mean 13.5
```

**More than half the live catalogue is outside the only product file in the folder.** The
filename says "Interwoven spring 2026" and the catalogue spans many lines; nothing else in
`Source Data/` records that, and a build started from that folder is building 46% of a
catalogue while believing it has all of it.

The blind read of this client concluded *"the data question was never actually settled
before the build started"* — two weeks lost, Showtime missed. **The folder is still in that
state today.** Nothing has been added that would stop the next person making the same
assumption.

What would close it: a one-line manifest in `Source Data/` naming what each file covers and
what it does not. The profiler's folder mode produces exactly that and nobody has run it
here.

*(Related but separate: `NetPrice` is the constant `1` on all 1,627 rows with real money in
`Price_List` / `Price_Retail` and eight more columns. Already recorded as by-design — A9.
Not re-raised.)*

## E. Framework defects recorded but deliberately not fixed

| id | defect | why unfixed |
|---|---|---|
| D2 | Phases are a checklist, not a sequence — Phase 7 needs any two of four clauses, so Phase 6 is skippable by construction | needs a design decision, not a patch |
| D3 | No adoption state. Five clients, five distinct failure modes | same |
| D10 | Import tier is silent on catalogue correctness. Confirmed on drf, mali, leg | **not fixable from Postgres.** Bounds what any log-reading automation can know |
| D19 | The D1 at-risk fix false-positives on pre-sales orgs | `overrides.toml § project_start_date` now populated for `leg`; the *rule* still needs the guard before at-risk ships |

---

## F. My own errors, for the record

Kept visible because the pattern recurs and naming it is the only thing that stops it.

| # | error | cost |
|---|---|---|
| F1 | Claimed `qty_available` is "the field the iPad displays." NULLs were real; the consequence was invented | **Reached the client.** Legrand was told inventory couldn't be displayed. False. |
| F2 | Read leg's 26 user groups as scaffolding. They are deliberate per-agency Library scoping | wrong rule built into the config checker; corrected |
| F3 | Called Legrand's price-list files an encoding problem. They are XLSX with a `.csv` extension (`504b0304`) | would have shipped an encoding ladder that decodes ZIP as mac_roman and returns confident garbage |
| F4 | Said the CopperSmith Parts header is row 3. It is row 2 | minor; caught by the session |
| F5 | `rawstate.py` had `libco: 279`. libco is **288**; 279 has zero products | any libco check through that constant returns silent zeros |

| F6 | Prescribed a fix for G1 that would not have worked — "flatten to block level." The loop was *already* block-level; 09:56 seq 1 (Options) precedes 09:56 seq 2 (Option Groups), so the window still closes unremedied at block granularity | none — the session tested the prescription before applying it, by replaying the exact pebl sequence |

| F7 | Published a breakdown that did not sum to its own total. Reported leg inventory as "755 non-null, 704 greater than zero, 28 exactly zero" — 704 + 28 = 732, not 755. **23 values are negative**, one at −12,643 | caught by the session on recount. Committed in the same message where I endorsed the specimen rule; a sum check is the cheapest specimen there is |

**F7 adds a third shape:** not an unverified consequence (F1/F3/F5) nor an untested prescription (F6), but arithmetic that contradicted itself in plain sight. **Partitions must sum to the total** belongs beside the specimen requirement — same defence, cheaper.\n\n**F6 is a different shape and worth separating:** not an unverified consequence but a confidently-prescribed remedy that was never tested against the failing case. Diagnosing correctly and prescribing wrongly is its own error.\n\n**The shared shape of F1, F3 and F5:** a measurement was correct and the *consequence
asserted from it* was never checked. That is the rule in `SCORECARD § 12 R1`, and it has
now cost something three times.

---

### F8 — I predicted G6's blast radius from a premise I never checked

Stated before the G6 re-run, as a falsifiable prediction and with a stated falsifier:

> Fatals are already outside `n_pair` and outside the alternation window — `0/0` is never a
> pair member — so dropping them raises coverage and **can only add pairs**. If B4 falls, or
> any alternation rate moves, the edit is wrong.

The premise is false. `0/0` is the signature of a **pure** fatal block. Across thirteen orgs
there are 1,594 fatal blocks and **1,292 of them (81%) also carry warnings or errors**, so
their signature is `237/0`-shaped, not `0/0` — and several are live pair members (`cl`
Inventory `1/0`, `sp` Products `1001/0` and `1002/0`, `ufi` and `uhc` Inventory `1001/0`).
Dropping fatals therefore removes pair members too: `n_pair` can fall below the floor and
`alts` can change.

`cl`'s coverage-passing pairs went 246 → 245 — exactly the movement I said could not happen.
It reached no finding only because `cl` was already at zero.

**The cost, had it landed differently: my stated falsifier would have condemned a correct
edit.** A prediction is only worth making if its premise is checked as hard as its
conclusion, and I checked neither — I reasoned from the *name* of the sentinel (`sig <>
'0/0'` in the candidate filter) to a claim about the *severity* of the block, which are
different things that happen to coincide in 19% of cases.

Same family as §F1: a measurement (`sig = '0/0'`) and its consequence (`this block is
fatal-only`) are two claims. I verified neither and asserted the link.

## G. Harness defects found in testing

Defects in the tooling being built, as distinct from defects in client orgs (§A) or in the
framework (§E). Kept separate because these are ours to fix, and because the pattern
matters more than the instances.

### G1 — A4 (import-order check) false-positives when blocks share an event

Found 2026-09-04, on the newest case the check reported, on a live client.

A4's rule is *"is every Options import followed by an Option Groups import before the next
Options import"* — correct, because importing options nulls group membership and the log
reads clean either way. The implementation evaluates at **event** level. Blocks share
events, so it breaks:

```
pebl, 2026-09-04
  09:28   Options -> Option Groups     paired, correct
  09:32   Options                      <- FLAGGED as never followed
  09:46   Products
  09:54   Products
  09:56   Options -> Option Groups     <- the actual remedy, 24 min later
  10:25   Options -> Option Groups
```

09:32 **was** remedied at 09:56. The scan for "the next Options import" lands on 09:56's
Options block and closes the window unremedied, never seeing the Option Groups block
sitting beside it in the same event.

**Live state confirms no defect:** pebl has 423 option groups, **423 with membership**,
last updated 2026-09-04 10:25.

**Reported counts are therefore wrong and pending re-run** — leg 4/1, tcs 45/7, pebl 54/10.
Expect all three to drop; some of tcs's 7 and pebl's 10 are likely the same artifact. The
corrected numbers replace SCORECARD's *"groups imported before options at tcs and pebl"*,
which stays directionally right but gains a real figure.

**Fix:** evaluate at block level within the ordered event stream — flatten to
`(timestamp, sequence_within_event, block_type)` — not at event level. `rawstate.py`
already splits blocks with `regexp_split_to_table` preserving within-event order.

**Why it was findable:** the session implemented the rule twice, in Python and in SQL,
noted the two disagreed on "OG separated from Options by an unrelated file," and recorded
it as not arising in this data. It arose. **Writing it twice is what made this catchable
before it shipped** — worth keeping as a practice for any rule with sequence semantics.

**RESOLVED 2026-09-04, and the fix was not the one prescribed.** Granularity was never the
problem — the question was. The importer runs an event's blocks in order, so an event's net
effect is decided by its *last* Options/Option Groups block. Membership is a **running state
over the event stream**, not a lookahead:

- **FATAL** — standing state is nulled and nothing restored it
- **WARN** — nulled for a period, later restored

Corrected figures, both implementations agreeing on every one:

| org | nulled windows | avg | longest | never restored | standing violation |
|---|---|---|---|---|---|
| leg | 1 | 2.6 h | 2.6 h | **0** | **0** |
| tcs | 42 | 69 min | 25.8 h | **0** | **0** |
| pebl | 25 | 11.4 h | 276.5 h | **0** | **0** |

The old rule reported 18 defects; **live defects are 0**, corroborated in state — leg 11/11,
pebl 423/423, tcs 343/343 option groups carry membership, no empty group anywhere.

Note the transient counts went *up* (tcs 7→42, pebl 10→25): the old rule counted only a
subset of the windows it was misclassifying. **The severity collapsed, not the volume** —
this is a recurring-transient problem, not a live defect, and BUILD_SPEC §3.1 A4 now says so
with these numbers.

**One finding survives** — pebl was nulled 2026-04-10 → 2026-04-22, 11.5 days. `login_events`
shows activity inside it: 8 logins on 04-10, 2 on 04-14 (squarely mid-window), 7 on 04-22.
All `DefaultUserGroup`, so admin/testing rather than field selling, and a login is not proof
of sync nor of opening a product with options. **Client-safe phrasing:** *at least one user
was active during an 11.5-day window when option group membership was nulled.* Not *reps saw
broken options.*

### G2 — The standing rule this produced

**A harness finding must be confirmed against live state before it reaches a client.**

A4 would have told a client their option groups were nulled today. The database says 423
of 423 have membership. That is the same failure class as `SCORECARD §12 R1` — the
`qty_available` claim — pointing the other way: there, the data was right and the
consequence invented; here, the log was wrong and the data exonerated it.

Three times now a claim has survived only because someone checked live state rather than
trusting the derived signal. The harness reports *evidence*, never *verdicts a client
hears*, until live state agrees.

---

### G4 — "age" is not one dimension: `submit_date` vs `created_at`

Found 2026-09-04, while reading `clli` cold. A3 reported nine dangling
`orders.price_level` values; one of them, price level `3`, looked like a live case:

```
order_number  63390-022021-7   THE LIGHTING BOUTIQUE   $20,252.25
submit_date   2021-02-21       <- the business event
created_at    2026-08-05       <- the database row
updated_at    2026-08-05
```

Reading `created_at`, it is one month old and urgent. Reading `submit_date` — and the
order number, which encodes `022021` — it is five and a half years old and archaeology.
**Neither column alone says what happened:** a 2021 order was backfilled or re-synced on
2026-08-05.

Measured spread, submitted orders where the row was created >30 days after the event:

| org | orders | diverging | max lag |
|---|---|---|---|
| `fal` | 3,909 | 80 (2.0%) | 641 days |
| `clli` | 1,362 | 5 (0.4%) | 2,002 days |
| `uhc` | 20,034 | 32 (0.2%) | 1,805 days |
| `ufi` | 37,817 | 22 (0.1%) | **4,751 days** |
| `pebl` / `cl` / `sp` | — | 0 | ≤ 7 days |

Rare, but with enormous lags — which is the dangerous shape. A recency filter on
`created_at` surfaces a thirteen-year-old order as new; one on `submit_date` misses that
the row changed last month.

**Constraint on F6 (severity), recorded not solved.** Any recency-based severity must say
**which clock it means**, and the honest input is probably both — when the business event
happened, and when the row last changed — reported separately. Do not fold them into a
single "age".

**This is the third pair of this shape** — see `SESSION_HANDOFF` § Things that will bite
you. `qty_available`/`qty_on_hand`, the two login columns plus `login_events`, and now
these. Before using any column as *the* answer, look for its sibling.

---

### G3 — B1b must separate "unregistered and populated" from "unregistered and empty"

Found 2026-09-04 via A4's closure. B1b flags source columns that carry no Admin
registration — correct, because the importer silently drops them. But the two cases have
opposite severity:

| case | consequence | severity |
|---|---|---|
| column **populated**, not registered | **data is silently discarded on every import** | BLOCKING |
| column **empty**, not registered | 13 warnings per import and nothing else | INFO / clutter |

leg is the second case: all 13 columns present in `products.csv`, **0 populated across
1,020 rows**, POC residue from the sales process. As written, B1b returns `exit 1` on every
future Legrand build — a false alarm on a file that is fine, which is how a gate gets
switched off.

**Fix:** B1b measures fill rate per unregistered column. Populated → BLOCKING. Empty →
INFO, with the advice to drop the column from the generator rather than register the field.

Same failure family as G1: the check was directionally right and its severity was wrong,
and the cost of that is an operator who stops reading it.

### G5 — B4's substrate cannot see a competing feed that imports cleanly

Found 2026-09-04, reading the F3 fix rather than running it. **Not a defect in the fix — a
limit of what B4 can know, which has to be declared before a green B4 is trusted.**

`import_log.sql_feed_pairs` builds every signature as `n_warning || '/' || n_error`, then
filters candidates with `WHERE events >= 3 AND sig <> '0/0' AND fs::date <> ls::date`. That
`sig <> '0/0'` is load-bearing and correct — a clean block carries nothing to compare — but
it has a consequence nobody wrote down:

> **Two files overwriting each other daily are invisible to B4 if either of them imports
> cleanly.**

`leg` was caught only because its two inventory files happen to produce *different nonzero*
warning counts (237/0 and 10/0). Had both been well-formed, A8 would be live and B4 silent.
Same shape as the cold-read finding — output that reads as "no competing feeds" and means
"no competing feeds *that produce two distinct nonzero warning counts*."

**Action:** B4 emits a `NOT CHECKED` line naming this on every run, the way
`preflight_gate.py` does. An unexplained absence is how a real gap becomes a silent pass.

#### G5a — there IS a filename side channel, and it independently confirms A8

The first pass concluded *"no filename to read, so the blind spot is permanent."* That is
right about `import_events` — verified, it has exactly four columns (`id`, `created_at`,
`organization_id`, `data`), and the 6,397 fleet-wide `.csv` mentions are message text naming
the canonical import name, identical for both competing files. It is **wrong about the
database.** A wider sweep of `information_schema` for filename-shaped columns found:

```
active_storage_blobs.filename          97 rows, 88 matching .csv/.xls[x]/.txt/.zip
  joined via active_storage_attachments -> record_type = 'InboundEmail'
```

Files arrive as **email attachments**. For `leg` they are named, dated, and unambiguous:

| day | Legrand-named .xlsx | leg Inventory import events |
|---|---|---|
| 2026-09-04 | `LegrandAdorneInventory.xlsx` (51,805 B) + `LegrandRadiantInventory.xlsx` (66,461 B) | 1 |
| 2026-09-03 | both | 4 |
| 2026-09-02 … 08-25 | both, every day including weekends | 1/day |

**Two files in per day, one import slot out.** That is A8, visible without inferring
anything from warning counts — a third independent confirmation, after the corpus and after
B4. It also supplies the mechanism A8 never had: the ingestion channel accepts two daily
emails into a single inventory import, and `inventory.csv` hard-deletes and reloads, so each
day one file wins and erases the other's rows.

State already recorded this and A8 says so — 439 rows / adorne on 2026-08-27, 755 rows /
radiant as of 2026-09-04 06:01 (re-confirmed: 755 rows, 755 distinct `updated_at`, all
inside a 2.2-second window). **The filenames are not new evidence of the flip; they are the
first evidence of its cause.** A8 knew the winner alternates. It did not know why, and
"two files are emailed in every day against one import slot" is the why.

*(A third daily attachment, `inventory-report-<date>.xlsx` ~157 KB, is weekday-only where the
Legrand pair is seven-day — a different source, not attributed. Do not assume it is `leg`.)*

**Four limits, all of which keep G5's NOT CHECKED line necessary:**

1. `record_type = 'InboundEmail'` has **no backing table in this schema** — no
   `inbound_emails`, no `action_mailbox_inbound_emails`. Blobs cannot be attributed to an
   organization in the database. `leg`'s are identifiable only by the string "Legrand" in
   the filename and by date correlation.
2. **97 blobs total.** This covers a handful of orgs and a short window, not the fleet.
3. It records what **arrived**, never what the importer **consumed**. Two files landing is
   not proof both were imported.
4. It is a different ingestion path from FTP, which is how most orgs deliver and which
   leaves no filename anywhere.

**So B4 does not change.** 97 rows cannot carry a check. What changes is the wording: the
`NOT CHECKED` line says *no filename in `import_events`; a partial side channel exists in
`active_storage_blobs` for the email-attachment path, unattributable to an org in-DB* —
and G5 stops being described as permanent.

**Separately, and larger than B4:** inbound client files arrive by email into ActiveStorage
and nothing in the programme documents that channel. It is a live ingestion path for at
least one onboarding client. It belongs in the correspondence agent's scope and in
`BUILD_SPEC`.

### G6 — fatal blocks read as `0/0`, and the two fixes are not the same edit

Found by the F3 session and filed as *"two characters, outside this change."* The characters
are right; **"inert" is not, and neither is "one edit."**

`sql_signatures` and `sql_feed_pairs` both count only `warning` and `error`. `sql_events`
computes tier properly (`CASE WHEN n_fatal>0 THEN 'fatal' ...`), so the conflation is
confined to the two signature modes — but within them a **fatal import, where the entire
file was rejected and nothing changed, is byte-identical to a clean one.** Specimen: `fal`
2025-01-23, `Column shiptoaddress1 is missing`.

**The correction, which the F3 session made and which the first version of this item got
wrong.** These are two different changes:

| target | edit | why |
|---|---|---|
| `sql_signatures`, tier reporting | **add** fatal to the signature | a rejected file reading as identical to a clean one is straightforwardly wrong |
| `sql_feed_pairs` / B4 | **drop fatal blocks from the stream** | a fatal import did not overwrite anything. Making it a distinct signature would let B4 count a no-op as a file switch, manufacturing alternations out of imports that had no effect |

**Predicted direction of the B4 delta, stated in advance so the re-run can falsify it.**
Fatal blocks are already excluded from `n_pair` and from the alternation window (their sig
is `0/0`, never a pair member), but they *are* counted in `n_win`, the coverage denominator.
Dropping them therefore **raises coverage and can only add pairs, never remove them.** So:

> B4's count after G6 is **≥ 2**, it moves only where an org has fatal blocks inside a
> candidate pair's window, and it moves via coverage alone — alternation figures are
> untouched.

If the re-run shows B4 *falling*, or any alternation rate changing, something else moved and
the change is wrong.

### G7 — the 0.30 alternation rate is fitted, and should be labelled as such

The F3 report says the three tests each have *"a meaning rather than a knob."* True of two.
**Coverage ≥ 0.90** is definitional and **n_pair ≥ 10** is a volume floor. **alts/(n_pair−1)
≥ 0.30 is a knob**, sitting between `cl`'s highest false positive at 16.7% and `leg`'s single
true positive at 52.8% — chosen the way a count cutoff would have been, one level up.

Reasonable place for it; the objection is the label, not the number. **One true positive
cannot calibrate a rate.** Two properties worth knowing, both verified:

- The thresholds swap which one binds at **n_pair = 17** (0.30 × 16 = 4.8). Below it the
  count binds — at the volume floor of 10, five alternations is already 55%. Above it the
  rate binds, and a 340-event pair needs 102 alternations.
- So a large, clumpy interleave — two files on a weekly rotation — is silent. Unknown
  whether that case exists in the fleet.

**Action now:** the constant's comment explains the mechanism, not the provenance —

```python
MIN_ALTERNATIONS = 5     # the pattern returns, rather than swapping once
MIN_ALT_RATE = 0.30      # ...and returns at a rate, not 8 times in 340 events
```

— add that it is fitted to n=1, and revisit after the **second** confirmed true positive.

**The principled replacement, when it bites** (F3 session's proposal, recorded so it isn't
re-derived): count maximal same-signature **runs** and test the longest run as a share of
the pair. Two files on a weekly rotation produce many runs at a low switch rate; a drifting
feed produces few long runs. Separates the case the rate cannot, with no fitted constant.
Not worth building until something is actually missed.

### G8 — a percentage was published without its denominator

After F3 the report said A4 membership (73) and B1a (70) were *"94% of what is left."*
Reading that against the 166 sub-top-tier findings gives 86%, and the discrepancy was raised
as an arithmetic error.

**It was not one.** The 94% was over WARN only: B5's 14 findings are 5 WARN + 9 INFO, so the
denominator is 151 and 143/151 = **94.7%**. Both numbers were right.

The defect is that the sentence opened with *"the remaining WARN volume"* and closed with
*"94% of what is left"*, naming no denominator and inviting the wrong one. Corrected and
republished as **143 of the 151 remaining WARN findings (95%); 81% of all 177 remaining
findings at every level.**

**The rule this confirms, which is now the second instance in a week** (the first was mine,
§F7): a partition names its denominator in the same sentence as its percentage. A correct
number with an unlabelled base is indistinguishable from a wrong one, and costs the same to
chase.
