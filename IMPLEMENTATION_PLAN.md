# SuperCat Onboarding Automation — v1 Implementation Plan

**Date:** 2026-07-27
**Author:** planning pass over the Loop Engineering POV, the canonical Track A / Track B docs,
the merged agent transcript corpus, and seven live client folders — with every load-bearing
claim re-verified against the live `supercat_server` Postgres.

---

## 0. TL;DR — what this plan concludes

1. **The knowledge and the tooling already exist. The missing piece is *enforcement at the
   moment of action*.** Every catastrophic failure in the corpus was already documented in a
   skill, and in two cases a validator existed that would have caught it. Nothing forced the
   check to run. v1 should be a **gate**, not a brain.

2. **Do not build a regenerator.** The POV's "intake pipeline" and my own first read
   ("generalize Legrand's `build_ecat_files.py`") are both partly wrong. A generator that owns
   `products.csv` destroyed weeks of work at The CopperSmith and was formally retired. The
   rule is **one owner per artifact** (§5.2).

3. **Branch by archetype, not by cohort size.** My earlier "the cohort is two clients" was an
   artifact of querying Postgres for orgs in `onboarding` state. The HelpScout onboarding inbox
   shows **8–10 clients active in the last 90 days** across three different products. The right
   scoping axis is not headcount but **archetype**: a default automated path, a snowflake flag that
   attaches nuance notes without blocking, and a `manual_review` flag that skips inapplicable
   automation (§2.4). Worktrees and parallel factories are still deferrable; the multi-product FRD
   is *not* hypothetical (§8).

4. **Phase 0 is not code.** The entire onboarding IP is untracked by git, which hard-blocks
   Cursor Automations. Three canonical docs contain queries that error out or claims that are
   false. Fix those first (§6).

5. **Highest-ROI build is a pre-import gate.** Its strongest case is Magic Lite's inventory wipe
   plus Terracotta's 100% customer rejection. It is *not* Legrand — that story was wrong, and
   correcting it sharpens the plan rather than weakening it (§2.1).

6. **Stop transcribing field limits — generate them from code.** The documented `LongDesc` 50 /
   `ShortDesc` 15 / `MediumDesc` 25 / `TradeNameCode` 5 / `BaseItemCode` 20 are all wrong. The real
   values live in `Product::ATTR_LENGTHS`. Two invented constants mangled 355 product names and 379
   descriptions at one client, and a validator written by the same agent certified the damage as
   passing. **A validator must assert against source, code, or the live DB — never against the
   transform's own rules** (§4.1).

7. **An entire image delivery path is undocumented.** `ImageFileName` accepts a full HTTPS URL that
   eCat fetches itself, which makes FTP optional — but `CdnImageSync` silently rejects PNG and
   caches at import rather than live-rendering. A one-hour HEAD-request census at intake collapses
   the corpus's most reputation-damaging failure from eight weeks to day one (§4.7).

8. **Freeze the architecture after client sign-off.** Six option rebuilds in eight weeks, and the
   one that cost SuperCat control of an engagement was driven by an internal review, shipped over an
   approved layout, and depended on a feature never enabled for the org. Ranked above every data
   check in the post-mortem (§5.5).

---

## 1. Evidence base

This plan is grounded in three sources, cross-checked against each other.

| Source | What it gave |
|---|---|
| Canonical docs (POV, Track A orchestrator + gates, Track B framework, 10 `ecat-*` skills, 3 validators, FRD v3.0) | The intended system |
| Merged transcript corpus (`ecat-onboarding-transcripts-MERGED-2026-07-27`) | What actually happened, in Kylor's and clients' own words |
| Seven client folders + live Postgres | What is true right now |

### 1.1 Live state, measured 2026-07-27

All numbers below are query results, not document claims.

| org | state | active products | hidden | customers | price levels | options | groups | orders | inventory rows / matching |
|---|---|---|---|---|---|---|---|---|---|
| `drf` | active | 1,627 | 0 | 389 | 11 | 0 | 0 | 7 | 0 / 0 |
| `leg` | onboarding | 1,020 | 0 | **1** | 5 | 29 | 11 | 0 | 1,194 / 947 |
| `libco` | onboarding | 832 | 0 | 231 | 4 | 0 | 0 | 4 | 912 / 829 |
| `mali` | active | 683 | 529 | 3,418 | 4 | 2 | 2 | 1 | 694 / 683 |
| `pebl` | active | 713 | 0 | 171 | 8 | 151 | 382 | 91 | 0 / 0 |
| `tcd` | active | 396 | 0 | **346** | 4 | 222 | 98 | 7 | 425 / 395 |
| `tcs` | fully suspended | 395 | 266 | 720 | 2 | 364 | 343 | 0 | 0 / 0 |

**One caveat on reading this table.** Row counts include POC/demo residue. For `leg`, everything
before the **2025-07-08** cutover is demo data and excluded from ground truth: its 29 options, 11
option groups, and 518 soft-deleted products all predate it. Any archetype or requirement inferred
from pre-cutover rows is invalid — in particular, **`leg` must not be used to infer options or
option-mapping requirements** (§2.4, Axis 3). Every org needs a declared source-data cutover date
before its numbers mean anything.

Image coverage, from the server-computed `products.image_exists` boolean:

| org | active | has image | missing | missing **and visible** |
|---|---|---|---|---|
| `drf` | 1,627 | 1,564 | 63 | 63 |
| `leg` | 1,020 | 1,000 | 20 | 20 |
| `libco` | 832 | 823 | 9 | 9 |
| `mali` | 683 | 671 | 12 | 2 |
| `pebl` | 713 | 690 | 16 | 16 |
| `tcd` | 396 | 395 | 1 | 0 |
| `tcs` | 395 | 393 | 1 | 1 |

### 1.2 Drift: documents vs. reality

| org | document claim | live | verdict |
|---|---|---|---|
| `tcd` | "go-live blocked, 0 customers imported" | 346 customers | **false** |
| `pebl` | "0 price levels, 0 customers" | 8 levels, 171 customers, 91 orders | **false** |
| `pebl` | 687 products / 135 options / 356 groups | 713 / 151 / 382 | live **exceeds** local |
| `libco` | `output/products.csv` = 915 rows | 832 active | 83 never landed |
| `leg` | "no options by design" | 29 options / 11 groups exist, but **0 of 1,020 products reference any** | **substantively true** — the rows are POC residue from a single 2025-06-16 import, all written within 0.15 s |
| `drf` | (pre-reconciliation) "~87 images" | 1,564 | **false** |
| `drf` | (post-reconciliation) 63 missing | 63 | **exact** |
| `leg` | 1,020 products, 20 image gaps | 1,020, 20 | **exact** |
| `mali` | 683 products, 529 hidden | 683, 529 | **exact** |

**The pattern is precise and it matters for design.** Numbers *generated by a query at the
time of writing* are reliable. Hand-maintained status and narrative fields rot. Dorell's
profile was wrong until someone reconciled it on 2026-07-21; after reconciliation it is exact.

**Design consequence:** build a reconciler that *regenerates* factual fields. Do not build a
rule that tells agents to distrust documents wholesale — that throws away the accurate half
and adds a full re-audit to every session.

---

## 2. The core diagnosis

### 2.1 Correction: there is no Legrand customer stall

My earlier draft led with "Legrand: a 13-month stall with a validator already written for it."
**That was wrong, and the correction matters because it changes what the gate is for.**

Legrand has exactly five customer import events, ever:

| Date | Result |
|---|---|
| 2025-06-19 ×4 | `Default price code must be a valid price level code` on nearly every row, plus seven `BillTo_*` unregistered-field warnings |
| 2026-06-18 ×1 | **Clean — zero errors, zero warnings** |

The June 2025 failures were against **POC/demo data**, not the client's real source, and everything
before the 2025-07-08 cutover is excluded from ground truth. The most recent import was clean; it
simply carried one row. So `leg`'s single customer (`code 4444`, `"eCat Test"`) is not the residue
of an unfixed validation failure — it is an org **waiting on the client's real customer file**. The
HelpScout thread confirms it: *"Legrand x SuperCat — Progress Update + What We Need From You"*,
2026-07-23.

A pre-import gate would not have changed this outcome. Nothing was being blocked.

**What Legrand actually needs the gate for** is visible in its live imports, and it is real:

- 2026-07-23 products: `Custom field 'rohscompliant' is missing`, `'Color'`, `'voltage'` — the
  header ↔ custom-field diff catches this before upload.
- 2026-07-14 products: `Field name carton1_h / carton1_l / carton1_w is unknown`.
- 2026-07-14 inventory: **24 KB of `Product not found, record ignored`** warnings — the cross-file
  referential check catches this.

The load-bearing argument for the gate is therefore Terracotta and Magic Lite, not Legrand:

- `tcd`: 100% customer rejection on `DefaultPriceCode=0` — the exact case named in
  `validate_customers.py`'s own docstring, which accepts `--price-levels` to cross-check the live
  org, and which passes cleanly on Pebl's real 171-row file (`pebl`: 171 customers, 91 orders).
- `mali`: inventory wiped by importing another org's file.

**The gap is still not knowledge, tooling, or model capability. It is that nothing invoked the
check.** That conclusion survives; only the headline example changes.

### 2.2 The same shape, five more times

| Incident | Already known? | Would a gate have caught it? |
|---|---|---|
| `tcd` 100% customer rejection on `DefaultPriceCode=0` | Yes — the validator's own docstring | Yes |
| `mali` inventory wiped by importing `leg`'s 1,194-row file | Delete semantics documented in `ecat-ground-truth` | Yes — org fingerprint check |
| `libco` products absent from portal | `image_exists` mechanism knowable | Yes — primary-image set diff |
| `pebl` 16 of 24 option groups rejected at 15 chars | Limit documented in `ecat-ground-truth` | Yes — length linter |
| `pebl` customer file rejected on `Terms` > 30 chars | Limit in `validate_customers.MAX_LEN`… **but `Terms` is absent from it** | Almost |
| `tcs`/`pebl` option groups imported before options, nulling membership | Import order in three separate docs | Yes — order enforcer |

### 2.3 Corollary: the assessment framework broke its own rule

The 2026-07-16 Track B report states LIBCO has "1,620 active products." That table has 915 rows
total, ever. The percentage in the same sentence was computed correctly off the real 832/823, so
the number was *narrated*, not queried — violating `Flags_and_Signals.md`'s own "no metric
without a tool call."

**Design consequence:** counts must never be typed into prose. They are query results with a
timestamp, or they do not appear. This applies to agent output *and* to handoff documents.

### 2.4 Client archetypes — the branching model that replaces "the cohort"

Scoping by org state was the wrong axis. Three axes actually determine what automation applies, and
they are independent — a client has one value on each.

**Axis 1 — Handling archetype.** This is the one that governs the default path.

| Archetype | Orgs | Effect on the pipeline |
|---|---|---|
| **Standard** | `pebl`, `leg`, `libco`, `drf`†, `mali`*, `tcd` | Default automated path; all gates apply |
| **Snowflake** | `mali`*, `tcs` | Same path, plus a documented exception note and a human checkpoint. **Never a blocker.** |
| **Churned, pattern-relevant** | `tcs` | Excluded from go-live success metrics; **retained** for options/mapping learnings |

\* `mali` is listed in Standard pending Open Decision 3 (§11). If OD3 resolves as Snowflake, move it to that row only.
† `drf`'s deviations (no pricing, sample-catalog model) are **Axis 3 applicability flags** — they produce `SKIP`, not a different gate path. `drf` is Standard; its flags are declared in Axis 3 below. *(Previously mis-listed in the Snowflake row under a "dorell" alias — corrected 2026-07-27.)*

The critical design rule: a snowflake flag **annotates**, it does not gate. Nothing in the corpus
supports treating an unusual client as un-automatable — the CopperSmith failures were ordinary bugs
(invented field limits, wrong import order, PNG URLs) wearing an unusual costume.

Verified snowflake nuances, each a note rather than a stop:

- **`mali`** — two brands (Magic Lite / NSL) in one org, separated by user group, described on the
  2026-05-13 call as *"a workaround for the platform's current lack of native sub-brand support."*
  Collections, price level, email templates, and branding all diverge per group. Any check that
  assumes one brand per org must read the user-group layer here.
- **`tcs`** — buildable SKUs, nested options, a PIM as upstream source, and a live builder script in
  org properties. Retain for the options/mapping and configured-SKU learnings (§5.5).

**Axis 2 — Product line.** Not every "onboarding" is an eCat iPad import, and this plan is scoped to
the eCat file family. Fine Art and Kuzco are currently onboarding the **Sales Portal**, whose file
family (`order_data.csv`, `invoice_data.csv`) has its own deterministic rules (§6.5). Lib & Co adds
eOL. This axis decides *which* gate set runs, and it is why the multi-product FRD is not
hypothetical.

**Axis 3 — Applicability flags.** Some clients legitimately do not use a subsystem. These are
`manual_review` flags that **skip** automation, never fail it:

| Flag | Client | Meaning |
|---|---|---|
| `pricing: n/a` | `drf` | Confirmed on the 2026-04-29 call: *"The app will not include pricing or inventory data."* Skip pricing and inventory gates entirely. A missing `Price_*` column is correct here, not a defect. |
| `options: none` | `leg` | Zero of 1,020 active products reference any option. Skip the options/group/mapping gates. |
| `sample-catalog model` | `drf` | Free half-yard cuts and "waterfall" collection samples rather than priced SKUs — a different commerce model, not a broken catalog. |

**Consequence for the gate runner:** every check declares its applicability preconditions and
reports `SKIP (flag: pricing n/a)` rather than `FAIL` or silence. A skipped check must be visible in
the output, because an unexplained absence is how "we don't do X for this client" gets forgotten and
re-litigated next quarter.

---

## 3. What already works — do not rebuild

| Asset | State | Verdict |
|---|---|---|
| `validate_customers.py` | Required fields, `MAX_LEN`, `BAD_PRICE_CODES` enum, optional live price-level cross-check, honest "local file only" docstring | **Production-grade. This is the template for everything else.** |
| `validate_products.py` | Required columns, blank/dupe `BaseItemCode`, `Hideable` enum, taxonomy extraction, method inference | Solid; **no field-length checks** (§4.1) |
| `audit_images.py` | Referenced images exist on disk, non-trivial size, count limit, heuristic hero-size warnings | Solid for local disk; **blind to the live org** (§4.3) |
| Test suite | 24 tests, all passing | Keep; extend with each new check |
| `ecat-*` skills (10) | Accurate domain knowledge, KB-vs-reality corrections | Keep; they are the spec for the checks |
| `PHASE_GATES.md` G1–G7 | Correct checklists | Keep; make items **executable** |
| Legrand `build_ecat_files.py` | 1,394 lines, produces a clean 1,020-row import, fixes codified as named tables | Keep as the **reference generator pattern** (§5.2) |

---

## 4. Confirmed gaps in the existing validators

### 4.1 Field lengths: every document has them wrong, and so does one validator

`validate_products.py` has no length checks at all beyond a `BaseItemCode` advisory. But the
deeper problem is that **the documented limits are wrong**, and transcribing them has already
caused the single worst data bug in the corpus.

Ground truth, read from `supercat_server/app/models/product.rb` `ATTR_LENGTHS` and confirmed by
a passing assertion in `test/services/importer/product_importer_test.rb`:

| eCat field | Model attribute | Real limit | Docs say | Behavior over limit |
|---|---|---|---|---|
| `LongDesc` | `long_description` | **255** | 50 | warn + truncate |
| `ShortDesc` | `short_description` | **255** | 15 | warn + truncate |
| `MediumDesc` | `plist_description` | **255** | 25 | warn + truncate |
| `Materials` | `materials_description` | 50 | 50 ✓ | warn + truncate |
| `Features` | `features` | 50 | 50 ✓ | warn + truncate |
| `Dimensions` | `product_dimensions_in` | 50 | 50 ✓ | warn + truncate |
| `BaseItemCode` | `item_number` | **40** | 20 | **validation error** |
| `TradeNameCode` | `trade_name_code` | **255** | 5 | **validation error** |
| `ShipWeight` | `shipping_weight` | 8 | 8 ✓ | **validation error** |
| option / group `Code` | `code` | 15 | 8 | **validation error** |
| option / group `Name` | `name` | 50 | 25 | **validation error** |

The critical structural distinction is `ATTRS_TO_TRUNCATE` — `features`, `long_description`,
`materials_description`, `plist_description`, `product_dimensions_in`, `short_description`.
Those six warn and truncate. **Everything else raises a validation error.** So `LongDesc` at 300
chars is survivable; a 16-char option code is not, which is exactly why 16 of Pebl's 24 option
groups were rejected in one shot.

This corrects three of my own earlier notes and one live-DB inference: `BaseItemCode`'s real
limit is 40 and it *is* enforced, so `mali`'s 21-char codes pass because 21 < 40 — not because
the limit is advisory. `TradeNameCode` is 255, so Legrand's pending `adorne`/`radiant` will
import fine.

**Why this matters more than the numbers.** At The CopperSmith an agent wrote
`[:15]` and `[:50]` into a sync script from the documented limits, producing 355 products whose
`ShortDesc` was the literal string `Handcrafted sol` and 379 whose `LongDesc` was severed
mid-word. `validate_source_truth.py` asserted `ShortDesc == source[:15]` — **the validator was
written by the same agent that wrote the bug, so it certified it as "VALIDATION PASSED."** The
client eventually diagnosed and fixed it themselves.

Two rules follow, and they are non-negotiable:

> **Generate the limit table from `ATTR_LENGTHS` at build time. A truncation constant that
> isn't traceable to a code-derived limit is a build error, not a style choice.**
>
> **A validator must assert against an external authority — source data, code-derived limits, or
> the live DB. Never against the transform's own rules.**

Also correct `validate_customers.py`: it caps `BillToCode` at 15 where `Customer::ATTR_LENGTHS`
says **20** (a false positive), and it omits `Terms` (30 — the real Pebl rejection),
`buyer_email` (100), `buyer_phone`/`buyer_fax`/`buyer_first_name`/`buyer_last_name` (25),
`billing_address2`/`3` and `billing_country` (60).

Still genuinely missing everywhere: `RelatedItems` 255 (a real cap that makes "related = whole
collection" impossible for a 207-SKU collection) and any check on `stories.csv`. Note that the
"`ProductStory` ≤ 500" rule in G3 appears to be **fabricated** — `story` is a `text` column set
verbatim by the importer. Confirm before enforcing it; Legrand's 442 over-500 rows may be a
non-issue.

### 4.2 No cross-file referential integrity
`inventory.BaseItemCode ⊆ products`, `stories.BaseItemCode ⊆ products`, `RelatedItems` targets
exist and are not soft-deleted, every `OptionSet*` code exists in `option_groups.csv`, every
group member exists in `options.csv`.

Live orphan inventory rows right now: `leg` 247, `libco` 83, `tcd` 30, `mali` 11.

### 4.3 No live-org image check
`audit_images.py` reads local disk. The failure that took Lib & Co's catalog off the portal is
only visible against the org's uploaded image inventory.

**Verified mechanism, zero exceptions across 832 products:**

| `image_exists` | primary file present in `product_images` | products |
|---|---|---|
| false | no | 9 |
| true | yes | 823 |

`image_exists` tracks **only the first filename** in the reference list. Alternates (`-1.jpg`)
do not satisfy it. eOL suppresses imageless products from search, so "products aren't showing
up" was literally true on the portal while the same products browsed fine on the iPad.
`product_images` is a flat, filename-keyed table with no product reference.

### 4.4 No orphaned-configuration check — a failure mode no doc covers
`leg` carries 29 options and 11 finish-combination groups, every one written inside a single
0.15-second import on 2025-06-16 — i.e. **POC residue from before the 2025-07-08 cutover**, not an
abandoned real attempt. All 1,020 active products carry `---\n:custom: false\n`, so there are **zero
references**. `tcd` is the same shape at larger scale: 222 options, 98 groups, zero of 396 products
referencing any.

This is cleanup hygiene, not a blocker, and it must not be read as evidence that either client needs
an options architecture.

This is permanent by design. Option cleanup only happens when you *send* `options.csv` (which
hard-deletes and reloads). Both clients' current builds emit no options file, so the dead
config never clears — it sits in the Admin Console waiting to be picked up by mistake.

### 4.5 No omission / delete-blast preview
Kylor's own invariant, from a handoff: *"Always include ALL products in products.csv on upload —
missing products get deleted."* Nothing enforces it.

### 4.6 No import-order enforcement, no placeholder register
Order is documented in three places (and the `_Template` contradicts itself — §6.3).
Placeholders are a deliberate unblocking technique that directly caused both image-visibility
incidents, and nothing tracks which values are synthetic or gates go-live on their removal.

### 4.7 An entire image delivery path is undocumented — and it silently rejects PNG

`ImageFileName` accepts a **full HTTPS URL**, not just a filename; eCat fetches the bytes itself,
so FTP is unnecessary. Nobody at SuperCat knew this five weeks into the CopperSmith engagement —
the CTO mentioned it mid-call: *"if you've been scraping the images, downloading them and then
uploading them, you can just pass the full URL and then have the system do the grabbing for
you... the FTP is sort of the legacy method."* Weeks of manual scraping preceded that sentence.

Verified in `product_importer_lib/cdn_image_sync.rb`, the fetch runs **two** gates and needs both:

```ruby
unless valid_image_content_type?(image_url) && valid_image_filename?(image_filename)
  log(:error, "Skipping invalid #{image_url}")
```

`valid_image_content_type?` accepts only `image/jpeg` or `image/jpg`. `valid_image_filename?`
requires an `.jpg`/`.jpeg` extension **and** a match on `Product::VALID_IMAGE_REGEX`. So a `.png`
URL fails both, the product keeps pointing at a file that never downloads, and it renders stale or
blank. This was the root cause of the client complaint *"I see VERY old image file names, so I am
wondering if we are pulling images from the live Catsy links at all?"* — 23 PNG URLs affecting 54
option rows, live for weeks.

Two consequences worth more than the bug itself:

- **The failure logs at `:error` tier.** Per the delete semantics, an `Error` row makes the
  importer skip *all* deletes of omitted records. So a catalog with PNG URLs probably also fails
  to soft-delete discontinued products, silently. Worth confirming, then encoding as a gate.
- **eCat caches at import; it does not live-render.** The download is conditional on the CDN's
  last-modified beating the stored timestamp. Replacing bytes at the same URL therefore changes
  nothing until a re-import, which is precisely the client's unanswered question *"we are seeing
  images go stale after they render once."* The workaround is a versioned filename (`-v2`).

Non-fetchable URL schemes are a separate silent class: `drive.google.com` and `dropbox.com/s/`
share links can never resolve, and two CopperSmith SKUs sat broken for a month on them.

**Check:** at intake, extract every URL from every image column, HEAD each one, and bucket into
`jpg-ok / png / dead / non-http / share-link` with counts. This is a one-hour pass that would have
collapsed the largest reputational failure in the corpus from eight weeks to day one. It belongs
in Phase 1, not later.

### 4.8 A UTF-8 BOM is fatal and reads as a missing column

Three leading bytes (`EF BB BF`) attach to the first header name, so `BaseItemCode` becomes
`\ufeffBaseItemCode` and the importer rejects the whole file with `Column baseitemcode is
missing` — an error message that points at the one thing that is plainly present. Excel for
Windows produces it by default via *Save As → CSV UTF-8*, so it recurs whenever a client
hand-edits a file. It cost a full round trip on Lib & Co's `stories.csv`.

A three-byte check on every deliverable is the cheapest gate in this entire plan.

---

## 5. Architecture

### 5.1 Principle: gates over brains

v1 is a set of **read-only, deterministic, independently-runnable checks** wired to the moments
where damage occurs: before an FTP upload, before an outbound client email, and at each phase
gate. Agents orchestrate and explain. Scripts decide.

### 5.2 The single-owner rule for generated files

**The corpus's most important lesson, and it contradicts the POV.**

At The CopperSmith a 38KB `generate.py` became the de facto source of truth. It silently
reverted hand-applied fixes — the `ShortDesc` fix was re-lost this way — and was renamed
`generate.py.RETIRED` with a do-not-run banner. Kylor's diagnosis, twice, on two clients:
*"why cant you just edit them directly instead of a py rebuild?"*

But Legrand's `build_ecat_files.py` is healthy and produced a clean 1,020-row import. The
difference is not script-vs-no-script. It is **dual ownership of one artifact**. Legrand's
corrections live *inside* the generator as named tables — `CATEGORY_FIXES`, `FINISH_FIXES`,
`PRODUCT_NAME_FIXES` — so regeneration is reproducible and loses nothing.

**The rule:**

> Each client declares exactly one owner per deliverable.
> **Mode A (generator-owned):** the script owns the file; every correction is codified in its
> config; hand-editing the output is forbidden. Legrand.
> **Mode B (CSV-owned):** the CSV is the deliverable; transforms are one-shot and in-place; the
> generator is retired with a tombstone. CopperSmith, Lib & Co.
> Never both. Declare it in `CLIENT_PROFILE.md`. A validator may never write.

### 5.3 Three-way split for images

The Magic Lite saga is fully explained by having no vocabulary for the third category.

| Class | Detection | Owner |
|---|---|---|
| File missing / never uploaded | `image_exists`, primary-token set diff | **Script** — deterministic |
| Filename wrong, shared hero, orphaned-hidden | set arithmetic on the CSV | **Script** — deterministic |
| Unfetchable URL (PNG, dead, share-link) | HEAD check for `200` + `image/jpeg` (§4.7) | **Script** — deterministic |
| **Right filename, wrong bytes** | none | **Human**, on a suspicion-ranked contact sheet |

Note that the first three classes now cover both delivery modes — FTP-uploaded files *and* CDN
URLs — so a client's image mode must be declared in `CLIENT_PROFILE.md` alongside the file-owner
mode. A blank source image cell is also a **decision, not a defect**: the standing client rule is
*"If an image isn't linked for that specific SKU, please don't make assumptions that a similar SKU
image link will suffice... Just leave it blank."* Inheriting a sibling's image violates it, and
that is mechanically checkable — assert that no two SKUs share an image filename unless the
*source* shares it.

Agents must not adjudicate class 3. On 2026-07-24 one agent read the live catalog and declared
`GDL-6`, `DL-FR`, and `RGL-FR` broken, wrote that into a handoff as verified fact; hours later a
second agent with per-SKU screenshots found all three already correct and reverted seven
repoints that would have overwritten good images with catalogue crops. The catalog was untouched
in between. Nothing was lost only because the guardrail said *stage, don't import*.

The agent's job is to **assemble and rank** the sheet, which cut the human pass to "only 22 of
218 heroes worth looking at."

### 5.4 Components

```
preflight/            read-only validators (extends the 3 existing scripts)
  lengths.py          two-tier: fatal vs advisory
  refs.py             cross-file referential integrity
  images_live.py      primary-token vs product_images for the org
  orphans.py          options/groups with zero product references
  omission.py         outgoing file vs live DB → delete-blast preview
  order.py            import sequence manifest + option_groups re-send
  placeholders.py     synthetic-value register + go-live gate
reconcile/
  queries.py          named query library (kills schema archaeology)
  profile.py          regenerate CLIENT_PROFILE factual fields + diff
verify/
  before_send.py      the pre-send checker contract (§7 Phase 3)
handoff/
  serialize.py        context serializer (§7 Phase 4)
```

### 5.5 Freeze the architecture after client sign-off

This is the one control the CopperSmith post-mortem ranks above every data check, and no existing
doc contains it. That client's option architecture was rebuilt **six times in eight weeks**. Each
rebuild forced a full `options → option_groups → products` re-import plus manual Admin relabeling,
because `option_type_labels` is not file-driven.

The rebuild that ended the engagement shipped on 2026-06-18: a flat 8-section layout was
re-architected into a two-step mount-type cascade, motivated by an *internal* maintainability
review, over a layout the client had already approved, and dependent on a beta-gated Admin feature
that was never enabled for the org. The client's reply — *"we had a workable and approved structure
in place... it feels like we've taken one step forward and three steps back"* — came with the SKU
Builder locked and the CSV build reassigned to their own vendor. SuperCat spent the next week
auditing someone else's imports of its own product.

Three rules, all mechanically enforceable:

> **Once a layout is client-approved, changing it requires a differential proof plus explicit
> client approval.** Enumerate every valid selection path across all products, run the old and new
> layouts through the live builder, and assert byte-identical configured SKUs. This check is proven
> to work: built after the fact, it returned 1222/1222 and caught a prior agent's false claim in
> the process. Run before the change, and it either blocks it or surfaces the defect first.
>
> **Never design around a capability that isn't enabled for the org.** Verify the feature flag, the
> beta gate, and the merge status before the design, not after. The mount cascade needed a
> beta-gated feature, an unmerged branch, and an unpushable importer — it was unshippable on day one.
>
> **Publish the capability inventory at kickoff**, not week eight: CDN URL support, 6-vs-12 images,
> drill-down nav flags, view layouts, per-user-group overrides, whether matrix pricing even applies.
> Every item on that list was discovered reactively by a frustrated client.

A useful precedent-lookup habit falls out of this: when a config is needed, query whether another
org already has it working and copy that shape. Pebl's populated `option_mappings` answered a
CopperSmith question directly.

---

## 6. Phase 0 — prerequisites (blocking, not optional)

### 6.1 Put the IP under git
`.cursor/skills/` and `eCat_Onboarding/` are untracked — not ignored, never added.
`SuperCat_Simple_Final` is not a repo at all. Last commit: 2026-06-12.

**Cursor Automations can only reference committed files in the automation's own repo, so all
scheduling is blocked until this is fixed.** It is also the only reason a 1,394-line generator
and 24 passing tests are one bad `mv` from gone.

### 6.2 Fix the broken canonical queries
`RUN_PROMPT.md` v3.5's "primary documented approach" selects `ie.file_type`,
`num_warnings`, `num_errors`, `warning_message`, `error_message` from `import_events`. **None of
those columns exist.** The table has exactly four: `id`, `created_at`, `organization_id`,
`data` (text). The query errors out. The v3.5 note presents this as the fix for two *previously*
broken forms; the CTE+CROSS JOIN form does still fail MCP validation.

Working form: plain `JOIN` + `data ILIKE '%- - Products%'`, parsing `data` for `:fatal`,
`:error`, `:warning` — which is what `Phase_Anchors.md` already implies.

### 6.3 Retract one unsupported claim, and finish one unfinished migration

`RUN_PROMPT.md` calls the orchestrator skill *"misguided per the audit; do not invoke."* The audit
never mentions the orchestrator, and the orchestrator predates it by two days. Retract it.

The path conflict is a different thing, and I had it backwards. The orchestrator claims client
state lives in `SuperCat 4.0/eCat_Onboarding/<Client>/` while all seven `CLIENT_PROFILE.md` and
four `HANDOFF.md` files actually sit in `SuperCat_Simple_Final/02_Implementation/`. That is not the
orchestrator being wrong — it encodes a **decision Kylor made and then only half-executed**. He
asked to consolidate, approved it, and the template plus the orchestrator's paths were rewritten;
the client folders were never moved.

The reason for the decision is technical and still binding: **rules and skills only auto-load
inside their own workspace root.** Client work living in a second root gets none of the eCat
ground-truth rules, which is a direct cause of the "markdown lies" problem this plan exists to
fix. So finish the migration — move the seven client folders under
`SuperCat 4.0/eCat_Onboarding/` — rather than editing the orchestrator to point at the split
layout. Everything in Phase 5 depends on a single root anyway.

Also fix `_Template`, which contradicts itself: `LIFECYCLE_CHECKLIST.md` includes options in the
import order, `00_Import_Files/README.md` omits them and adds pricing; image limits read 5 in
one file and 6 in another. **The template cannot be the contract until it agrees with itself.**

### 6.4 Correct `validate_customers.MAX_LEN` against the model

Add `Terms: 30` — a real Pebl rejection, where the client's true trade terms *"30% T/T Advance,
Balance Against Copy of Bill of Lading"* is 62 characters against a 30-char field, i.e. a
structural mismatch needing a client decision rather than a truncation. In the same pass, raise
`BillToCode` from 15 to its real limit of 20 and add the six omitted buyer/address fields (§4.1).
Generate the whole table from `Customer::ATTR_LENGTHS` instead of transcribing it.

### 6.5 Complete the file inventory

The canonical spec covers six files. At least five more are live in client work and unmentioned:
`riser_prices.csv` and `contract_prices.csv` (both hard-delete-and-reload), the
`products_N.csv` + `sentinel.csv` multi-file merge, and `order_data.csv` / `invoice_data.csv` for
Portal reporting. Add `matrix_options.csv` to the tail of the documented import order, which
currently stops at six files. A gate that doesn't know a file exists cannot protect it.

The **Sales Portal** family is the live gap. Fine Art is mid-launch on it right now, and the
2026-07-23 calls produced four rules that are all mechanically checkable and none of them documented:

1. **Date fields must be date-only.** `4-16-2026 12:00:00 AM` is rejected; applies to `Order Date`,
   `Ship Date`, `Invoice Date`.
2. **No extra columns** — a stray `fiscal month` column fails the file.
3. **Order line items must be contiguous by order number.** The importer reads top-to-bottom and
   treats a change in order number as end-of-order, so an order number reappearing later in the file
   is an error. This one is structural and worth stating plainly: ERPs that log order changes as new
   transactions scatter line items by default, so **the client's natural export is wrong until
   sorted**.
4. **Exact filenames** — a `TBL_` prefix (`TBL_Order_Data`) fails; it must be `Order_Data.csv`.

Rule 3 in particular is a sort-and-verify check worth writing before the next Portal onboarding,
because it is invisible to the client and expensive to diagnose from the error alone.

---

## 7. Phased build

### Phase 1 — the pre-import gate (highest ROI)

One command, run before every FTP upload. Read-only. Exit non-zero blocks.

| Check | Prevents |
|---|---|
| **BOM check** — assert no `EF BB BF` on any deliverable | A fatal "column missing" on a column that is present (§4.8) |
| **Org fingerprint** — sample `BaseItemCode`s, assert ≥95% match `products.item_number` for *this* org; row count within tolerance; path under the client's own build folder | The `mali`/`leg` inventory wipe. Hard-block for inventory, customers, options, groups — all hard-delete. |
| **Image URL census** — HEAD every URL for `200` + `image/jpeg`; reject `.png`, dead links, and Drive/Dropbox share links | The CopperSmith PNG crisis: 23 URLs, 54 rows, eight weeks (§4.7) |
| **Blank-stays-blank** — every SKU blank at source is blank in output; no shared filename unless the source shares it | Sibling-image inheritance against an explicit client rule |
| **Enum + required fields** — `DefaultPriceCode` ∈ live `price_levels.code`; non-blank bill-to and ship-to fields | `tcd`'s 100% customer rejection |
| **Two-tier lengths** | Pebl's 16 rejected groups; CopperSmith `ShortDesc`; Libco `Name` |
| **Cross-file refs** | 247 orphan `leg` inventory rows; dangling `RelatedItems` |
| **Header ↔ custom-field diff** (case-insensitive, live) | `ML_qtybackordered` vs `ML_QtyOnBackorder`; Legrand's 7 `BillTo_*` warnings; Pebl's 3-month chronic warning set |
| **Taxonomy pre-registration** — groups never auto-create | Real fatal errors in Magic Lite's import log |
| **Omission preview** — "N products soft-delete / ALL customers hard-delete and reload", require ack | Silent catalog loss |
| **Import-order manifest** — refuse groups-before-options; auto-append the second `option_groups.csv` pass | Nulled group membership at `tcs` and `pebl` |
| **Primary-image set diff** | Lib & Co's portal outage |
| **Duplicate scan** — `BaseItemCode`, option/group `Code`, UPC | CopperSmith duplicates; Pebl's `MT_FAROEXT_GR` |

Ship as an extension of the three existing validators, same CLI shape, same two-tier
FAIL/WARNING output, same test discipline.

Two companion checks belong here even though they are not blocking gates:

- **Source-coverage reconciliation.** Every row of every source tab must be explicitly classified
  as `→ product`, `→ option`, `→ related item`, or `EXCLUDED (reason)`. Unclassified is a build
  failure. At CopperSmith an agent silently dropped 12 kits and **234 parts**; the client found
  them, not us. Silent omission should be impossible, not merely discouraged.
- **Two kickoff documents, generated rather than written.** The corpus contains an unusually good
  artifact — a code-verified, client-shippable `llms.txt` stating exactly what eCat needs — meant to
  be re-cut per client and largely wasn't. Alongside it, the single best client-facing explainer in
  the corpus mapped CSV column → iPad element → who controls it → where, and separated Admin custom
  fields from view layouts. It was sent in **week eight**, and every layer of it was something a
  confused client had already asked about. Generate both from the actual delivered files plus live
  Admin config, and re-issue with every delivery.

### Phase 2 — reconciler + named query library

- **Query library** for the audit battery: org by shortname, product/image/customer counts,
  `import_events` recency and tier, price levels, user-group → authorized levels, orphan
  inventory, dangling refs, orphaned options, placeholder-price detection, `image_exists` split.
  Roughly a third of every diagnostic session in the corpus is schema archaeology
  (`stories` → `product_stories`, `users` → `org_users`, lifecycle state → `properties->>'status'`
  not `o.state` which is the physical US state, `product_images` has no `product_id`). This is
  pure cost removal.
- **`reconcile profile`** regenerates `CLIENT_PROFILE.md` factual fields from live SQL and diffs.
  Any field older than N days renders as `STALE — re-query`. Directly kills the Terracotta,
  Pebl, and Dorell drift.
- **Rule:** handoffs cite a query name, never a typed count.

### Phase 3 — the pre-send checker

Lift the contract verbatim from the corpus, where Kylor already runs it by hand on every
outbound artifact and it caught three wrong agent answers:

1. Declare stakes. 2. Void prior analysis. 3. Require three independent evidence tiers —
source files / importer code + tests / live org state. 4. Name the exact prior error the client
already pushed back on. 5. Enumerate every file by absolute path. 6. Enumerate live-state
questions entity by entity, with disambiguation ("as active product, deleted product, option, or
group member" — four states, not "does it exist"). 7. Review the actual draft, not a summary.
8. Failure criterion: factually airtight, no over-claimed ownership, no blame, no
asserted-but-unconfirmed mapping. 9. Verdict: safe-to-send or not, plus rewrite.

Classify every claim **verified / unverifiable / contradicted**. Two governing lines from the
corpus: *"a flagged gap beats a wrong-but-confident map"* and *"if you can't prove it, flag it —
do not invent."*

### Phase 4 — handoff serializer

Twelve sections appear in essentially every good specimen across two clients, which makes this a
contract rather than a style. Emit all twelve:

1. **Identity** — client, org shortname **and id**, product scope (iPad vs eOL vs Portal), phase.
2. **Client emotional/political state.** Load-bearing, not colour: *"the client is frustrated about
   wrong images, so correctness matters more than speed"* sets the speed/accuracy tradeoff.
3. **Sources of truth, ranked, with parse quirks** — absolute paths, which file wins a conflict,
   row-offset and junk-line notes, and explicit **anti-sources** ("the generator is not truth").
4. **Locked decisions** that must not be re-litigated (base-item definition, OptionSet↔category map,
   taxonomy method, file-owner mode, image mode).
5. **Field mapping table** — source column → eCat field → transform → *code-derived* limit.
6. **Current state with exact counts**, live-vs-local diff, and explicitly **what has not happened**.
7. **eCat gotcha block** — import order, the options→groups nulling trap, per-file delete semantics,
   error-tier-blocks-deletes, image rules.
8. **Validation checklist as runnable commands with expected numeric outputs** — not prose.
9. **Open items split "we can fix" vs "need the client."**
10. **Do-NOT / out-of-scope**, including "do not FTP or import without explicit approval."
11. **Deliverable format** — GO/NO-GO, or a mismatch table with a **fix-owner column**.
12. **Anti-hallucination preamble** (below).

Later specimens add four more worth keeping: **chain of custody** (who changed what, when — this is
what turned a blame argument into a query), **email tone rules**, **skills to load**, and **schema
notes** (`import_events.data` is YAML; `option_groups.options` is a YAML id array; org config lives
in `properties->>'key'`).

The preamble is the highest-value line in the corpus and should be emitted verbatim on every
handoff: **"You are a fresh agent with no prior context. Do NOT trust this document's claims —
re-derive them from the data and code. Find anything wrong and fix it."** Used twice, it caught a
prior agent's false claim both times. Pair it with falsify-the-premise instructions that verify the
*reason* rather than the result — *"open `cdn_image_sync.rb` and confirm it rejects PNG; if the code
says otherwise the whole premise is wrong, flag it"* — and with explicit stop-don't-guess
authorization, which worked the one time it was used.

Two structural weaknesses to fix versus the hand-written era. First, **every fact needs a provenance
pointer** (source file + line, DB query, or code path) and must be re-derived on read: hand-written
handoffs described a lantern company as a "range hood manufacturer," listed SuperCat's own CTO as a
client contact, and carried the fabricated field limits into fresh agents as ground truth. The
client eventually noticed — *"the handoff files do not fully match the admin environment."* Second,
**include the client's own words by default**: emails and call transcripts had to be requested
repeatedly, and the serializer should never need to be asked.

Trigger on context pressure, on new client input, and before any pre-send review. Kylor
commissioned at least six of these in 36 hours during the Magic Lite crisis — the
handoff-writing is itself a meaningful share of the labour.

### Phase 5 — scheduling (only after Phase 0)

Weekly Track B assessment as a Cursor Automation, once the repo exists and the queries work.
Add a **cross-tenant fingerprint scan**: after any root cause, sweep all orgs for the same
signature. This found a second broken tenant for free in the corpus (Savoy House, from Golden
Lighting's Cloudflare misconfiguration).

---

## 8. Explicit non-goals for v1

| Deferred | Why |
|---|---|
| Worktrees / parallel client factory | 8–10 active clients, but one reviewer. Review bandwidth is the ceiling, not agent throughput. |
| 12-stage multi-product FRD v3.0 | Track B's 7 phases are live and used; the FRD is not. Don't run two frameworks — but note the FRD's multi-product premise is **correct** and now needs an owner (§11). |
| Vision-based image adjudication | Demonstrably non-reproducible between agents; nearly caused a live regression. |
| A generator that owns deliverables | §5.2. |
| Option Mapping automation | Admin-Console-only, not CSV-configurable. Generate the worksheet and the click-path; the human clicks. |
| Anything that writes to Jira | Read-only, per workspace rule. Draft text for Kylor to post. |

---

## 9. Human-judgment items — surface, never decide

| Item | Why it can't be scripted | Automate instead |
|---|---|---|
| Right filename, wrong bytes | §5.3 | Ranked contact sheet |
| Authoritative source when master and accessory index disagree (`WY` vs `WY36`) | Determines what prints on a PO | Detect conflict, show order-SKU impact, ask |
| `RelatedItems` rule: same collection vs. same variant root | 255-char cap makes one impossible — a 207-SKU collection needs ~2,690 chars | Compute both, show the cost, force a choice |
| `Hideable` policy for pack/variant SKUs | Contradicted client intent at Magic Lite | Echo the hide decision back for sign-off |
| Option Mapping cascades | Needs the client's real build matrix | Worksheet + completeness/contradiction validation |
| Demo vs. final scope | Premature go-live on scraped data triggered the Magic Lite escalation | Readiness gate with named criteria + a required label on every catalog state |
| Missing price: lost vs. not yet costed | Only the client knows | Gap workbook with input cells, track return |
| Config vs. code change | Required reading `supercat_server` and the iOS app | Maintained capability matrix |
| Environment problems (China/VPN reach to FTP, corporate networks, iPad Mail unconfigured) | Not in any file | Capability probe + an explicit "not a data problem" triage branch |
| Admin-view vs. rep-view | Six of nine escalated Magic Lite items were not defects | **Make "client has a non-Admin rep profile per brand" a hard go-live gate** |

Two of these deserve emphasis because they were the most expensive items in the corpus:

- **A 30-second capability probe** before committing to a client-system transfer. One attempt at
  an authenticated call; on 403 or hang, stop and send the access request. This turns 3.5 hours
  of failed SharePoint scraping into 30 seconds.
- **The rep-profile gate.** It was called "the single highest-leverage open item" and
  "MUST-PASS," and was still open four months later. It alone would have retired a large
  fraction of every client complaint list in this corpus.

---

## 10. Success criteria for v1

1. No import proceeds without a passing pre-import gate. Zero repeats of a wrong-org import or a
   100%-rejected customer file.
2. `CLIENT_PROFILE.md` factual fields are regenerated, never typed. Drift measured at zero for the
   active eCat clients, each with a declared source-data cutover date.
3. Every outbound client artifact passes the pre-send checker, with each claim labelled.
4. `leg` clears its three live warning classes — unregistered custom fields (`rohscompliant`,
   `Color`, `voltage`, `carton1_*`) and 24 KB of orphaned inventory rows. Its customer file is
   tracked as **awaiting client input**, not as a validation failure. The 29 POC options and 11 POC
   groups are consciously cleaned or accepted.
5. Every client carries an archetype, a product line, and its applicability flags. A skipped check
   prints `SKIP` with the reason — `drf` shows `SKIP (pricing n/a)`, never a silent pass.
6. The G3 500-char story rule is either traced to code or deleted. Legrand's 442 over-length rows
   are then knowingly fine or knowingly fixed — not silently pending.
7. Every field limit in every validator is generated from `ATTR_LENGTHS`. No transcribed constants
   remain anywhere in the toolchain.
8. Every new check ships with tests, extending the existing 24.

---

## 11. Open decisions

Five things the validation pass surfaced that I cannot settle from evidence. Each needs a call
before the corresponding work starts; none blocks Phase 0 or Phase 1.

1. **Who owns the Sales Portal file family?** Fine Art launches in early August on
   `order_data.csv` / `invoice_data.csv`, with four undocumented rules (§6.5) and Kuzco already live
   on the same product. This plan is scoped to eCat imports. Either widen Phase 1 to cover the
   Portal family — the contiguous-order-number rule is worth a script on its own — or scope it out
   explicitly and let it stay manual. Right now it is neither, which is how it stays undocumented.

2. **Does the gate attach to files or to feeds?** Legrand is moving to a daily 1 AM API inventory
   feed, Lib & Co to hourly Business Central sync, and Lib & Co's inventory feed already generates a
   daily HelpScout thread. A pre-**upload** gate protects manual FTP pushes and does nothing for a
   scheduled feed. Recurring feeds need post-import assertions instead. Confirm whether v1 covers
   feeds or explicitly defers them.

3. **Is `mali` standard or snowflake?** It appears in both rows of the archetype table, which is a
   real ambiguity rather than a typo: its data path is ordinary, but its user-group/sub-brand layer
   breaks the one-brand-per-org assumption that several checks would otherwise make. My inclination
   is standard-with-a-flag (`sub_brands: ML,NSL`), but it is your call.

4. **What is the cutover date for every org other than `leg`?** `leg`'s is 2025-07-08 and `tcs`'s is
   effectively the Catsy migration, since its Google Drive data was explicitly demo-only. Without a
   declared date per org, POC residue keeps re-entering analysis as if it were real — it already did
   twice in this plan.

5. **Should the archetype live in `CLIENT_PROFILE.md` or in a single registry?** Per-profile matches
   the existing layout; a registry is what a scheduled automation actually needs to enumerate the
   cohort, and would have prevented the "cohort is two clients" error. I lean registry, with the
   profile referencing it.

---

## Appendix A — verified corrections to the canonical docs

| Doc | Claim | Reality |
|---|---|---|
| `RUN_PROMPT.md` v3.5 | `import_events` has `file_type`, `num_warnings`, `num_errors`, `warning_message`, `error_message` | Only `id`, `created_at`, `organization_id`, `data`. Query errors out. |
| `RUN_PROMPT.md` | Orchestrator is "misguided per the audit" | Audit never mentions it; orchestrator predates it |
| Orchestrator `SKILL.md` | Client state in `eCat_Onboarding/`, "this path wins" | Real state is in `02_Implementation/` — but the orchestrator encodes an approved, half-executed consolidation. Finish the move; don't retarget the skill (§6.3). |
| `ecat-core-files` | `LongDesc` 50 / `ShortDesc` 15 / `MediumDesc` 25 | All three are **255** — `Product::ATTR_LENGTHS`, asserted in `product_importer_test.rb`. Warn-and-truncate, never fatal. |
| `ecat-core-files` | `TradeNameCode` 5 | **255**, and it is a hard validation error, not a truncate |
| `ecat-ground-truth` | `BaseItemCode` 20, "advisory not fatal" | Real limit **40**, and it *is* enforced. `mali`'s 21-char codes pass because 21 < 40, not because the limit is advisory. |
| `ecat-images-ftp` | FTP is the delivery path | `ImageFileName` also accepts a full HTTPS URL that eCat fetches itself. **PNG is silently rejected** by `CdnImageSync` (needs `.jpg`/`.jpeg` *and* `Content-Type: image/jpeg`), and it caches at import rather than live-rendering (§4.7). |
| `PHASE_GATES.md` G3 | `ProductStory` ≤ 500 chars | Appears fabricated — `story` is a `text` column set verbatim. Confirm before enforcing. |
| `validate_customers.py` | `BillToCode` ≤ 15 | `Customer::ATTR_LENGTHS` says **20**; `Terms` (30) and six buyer/address fields are missing entirely |
| Import order (all docs) | Six files, ending at `customers.csv` | `matrix_options.csv` follows; `riser_prices.csv`, `contract_prices.csv`, `products_N.csv` + `sentinel.csv`, `order_data.csv`, `invoice_data.csv` are undocumented (§6.5) |
| `_Template` (both copies) | Import order; image limit | Self-contradictory: options included in one file, omitted in another; 5 vs 6 images |
| Track B 2026-07-16 output | LIBCO 1,620 active products | 832 active; table has 915 rows total |
| `organizations` | `status` column for lifecycle | No top-level `status` column. `state` is the physical US/Canada state (`CA`, `TX`, `Ontario`). Lifecycle state (`onboarding`, `active`, `fully_suspended`) is in `properties->>'status'`. Writing `WHERE o.state = 'onboarding'` silently returns 0 rows. |
| `customers` | `customer_number` | It is `code` |
| `price_levels` | `description` | Does not exist |
| `products` | `image_file_name`, `OptionSet1..5` columns | Images in `images_json`; options in a single serialized `options` column |

## Appendix B — the two catastrophes, for the record

**Magic Lite inventory wipe (2026-07-23).** `leg`'s 1,194-row inventory file was imported into
`mali`. Because inventory hard-deletes then reloads, `mali`'s real inventory was replaced with
1,194 rows matching zero `mali` products. **Resolved same day** — `mali` now holds 694 rows with
all 683 active products matched, reloaded 2026-07-23. The orphan counts corroborate the
diagnosis exactly: `leg`'s own inventory is 1,194 rows, precisely the foreign row count.

**Terracotta customer rejection (`tcd`).** `DefaultPriceCode = 0` — an ERP placeholder, not a price
level — rejected every row of the customer file at the time, which is why the docs still say "0
customers." It was later fixed and `tcd` now holds 346 customers, so this is a **resolved** incident
whose value is diagnostic: it is the canonical case named in `validate_customers.py`'s own docstring,
the validator would have caught it before upload, and it is reproducible today. It replaces the
retracted Legrand story as the plan's load-bearing example (§2.1).

---

## Appendix C — validation pass: Fathom + HelpScout

Scope: BigQuery `Fathom.call-transcripts` / `ai-summaries` (613 / 877 rows) and `helpscout`
(`conversations` 5,307; `conversation_threads` 41,060; two inboxes). Targeted queries only.

**What changed in the plan**

| Finding | Source | Plan change |
|---|---|---|
| Onboarding spans **45+ client domains since 2023**, 8–10 active in the last 90 days | HelpScout inbox 312855 "SuperCat Onboarding" | Retracted "the cohort is two clients"; replaced with the archetype model (§0.3, §2.4) |
| Legrand is **waiting on client data**, not blocked by validation — *"Progress Update + What We Need From You"*, 2026-07-23 | HelpScout + `import_events` | Rewrote §2.1; corrected §0.5, §7 Phase 1, §10.4, Appendix B |
| `drf`: *"The app will not include pricing or inventory data"* | Fathom 2026-04-29 | Confirms `pricing: n/a` / `sample-catalog` flags (§2.4 Axis 3) |
| `mali`: sub-brand split is *"a workaround for the platform's current lack of native sub-brand support"* | Fathom 2026-05-13 | Snowflake nuance note; flagged as Open Decision 3 |
| `tcs`: PNG assets and a JPEG-only requirement were **both raised at kickoff** and never checked | Fathom 2026-04-21 | Strengthens the day-one image census (§4.7) |
| `tcs`: *"The previous Google Drive data was for demo purposes only"* | Fathom 2026-04-21 | Generalized the POC-cutover rule beyond `leg` (§1.1, Open Decision 4) |
| Sales Portal has four undocumented import rules, incl. contiguous order numbers | Fathom 2026-07-23 ×2 | Added to §6.5; raised as Open Decision 1 |
| Recurring/API feeds are displacing manual CSV at `leg`, `libco`, `mali`, `tcs` | Fathom, multiple | Raised as Open Decision 2 |
| `dorell`: *"The system lacks an admin-to-file sync"* — all edits go through the CSV | Fathom 2026-05-18 | Independent confirmation of the single-owner rule (§5.2) |
| Support tags: `data-sync imports and exports` **349**, `image asset` 54, `config issue` 81, `manual work` 38 | HelpScout inbox 65829 | Import/export is the largest non-generic support category — supports gate-first sequencing |

**What did not change.** The gate-over-brains principle, the single-owner rule, the three-way image
split, the architecture freeze, and all Phase 0 prerequisites are unaffected. No source contradicted
them; two independently confirmed them.

**One methodological finding.** The onboarding inbox is **entirely untagged** — every sampled
conversation returned `[]`, while the support inbox carries a 40-tag taxonomy across ~4,000
conversations. So archetype classification cannot be derived from HelpScout onboarding metadata
today; it has to be declared per client (Open Decision 5). If onboarding threads were tagged with
the existing vocabulary, `type: manual work` and `status: waiting on client` would map almost
directly onto the `manual_review` and awaiting-input states this plan needs.
