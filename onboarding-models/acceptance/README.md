# The acceptance harness — BUILD_SPEC §3

Post-import (and pre-upload) state checks. **Read-only**: emits SQL for the
supercat-postgres-vpn MCP, never connects and never writes.

| # | criterion | status |
|---|---|---|
| A1 | org fingerprint | **SHIPPED** — `a1_fingerprint.py` |
| A2 | placeholder pricing | **SHIPPED** — `state_checks.py` |
| A3 | references resolve | **SHIPPED** — `state_checks.py` |
| A4 | option-group membership | **SHIPPED** — `import_log.py` + `a4_b4.py` (canonical-order rule deleted 2026-09-04) |
| B1 | registered fields populated | **SHIPPED** — `b1_fields.py` |
| B2 | image filenames match FTP | **UNIMPLEMENTED — blocked, see below** |
| B3 | territory codes | **SHIPPED** — `state_checks.py` |
| B4 | feeds overwriting | **SHIPPED** — `import_log.py --mode feed_pairs` + `a4_b4.py` (alternation test added 2026-09-04) |
| B5 | inventory config vs data | **SHIPPED** — `state_checks.py` |
| B6 | carry-forward diff | **done** — `ecatlib.carryforward.diff_against_previous` |

---

## What §3 does NOT close

**§3 narrows D10. It does not close it.** Nine of the ten criteria are
Postgres-answerable, so the harness genuinely closes most of the distance between
"the import ran clean" and "the catalogue is right".

It does not close the case that produced D10. On `drf`, every product parsed,
every reference resolved, and the colours were still wrong — the file was a
correct-looking wrong catalogue, and two weeks and a Showtime deadline were lost
before anyone noticed. **No §3 criterion detects that, and none can**, because
correctness there is a claim about the client's intent, and intent lives only in
the conversation record.

So: a green harness means "no criterion in §3 is violated". It does not mean the
catalogue is right. Anyone extending this file should keep that sentence in it.

## B2 is unimplemented, deliberately

**B2 requires listing the FTP `/images` root and comparing `ImageFileName`
byte-for-byte.** This environment has no FTP credentials, so it cannot be built
here.

**Do not substitute `products.image_exists`.** It is the importer's own opinion,
and `pebl` ran 18 days of images at clean tier with doubled `.jpg.jpg` extensions
that could never match — a partial check against `image_exists` would have passed
all 18 days. Shipping that as B2 would be the clean-import fallacy inside the
tool built to detect the clean-import fallacy.

**What would unblock it:** FTP credentials for the client's `/images` and
`/option_images` roots, reachable from wherever the harness runs.

---

## A1 — org fingerprint

    2026-08-18: Legrand's 1,020-row products.csv was imported into 111Mercer,
    soft-deleting all 102 of their products. Second occurrence (leg -> mali
    previously).

Both times the file was valid and the import was clean. The org was wrong, and
nothing in the file says which org it belongs to.

```bash
# 1. emit
python3 a1_fingerprint.py <file.csv> --org <shortname> --emit-sql
# 2. run the emitted SQL through supercat-postgres-vpn (read-only)
# 3. verdict
python3 a1_fingerprint.py <file.csv> --org <shortname> --from-results results.json
```

Exit 1 = do not upload.

### Why overlap alone is not the check

Three separate questions, and the verdict needs all three:

1. how much of the file already exists in the target org
2. **how many live records the import would DELETE**
3. whether some *other* org matches the file better than the target does

(2) is the number that matters — on 2026-08-18 it was 102 of 102 — and (3) is
what actually names the incident, since Legrand's codes match `leg` and no one
else. Omitted-record behaviour is per file type and is printed in the verdict:
`products.csv` **soft**-deletes; `customers.csv`, `inventory.csv`, `options.csv`
and `option_groups.csv` **hard**-delete.

### Verified against live data, four branches

| case | file → org | result |
|---|---|---|
| correct org | mer's products.csv → `mer` | 102/102 matched, 0 deleted → **PASS** |
| wrong org | mer's products.csv → `leg` | 0/102 matched, **1,020 of 1,020 would be soft-deleted** → **FATAL** ×2 (zero overlap; and the keys match `mer` at 100%) |
| empty org | drf's customers.csv → `mer` (0 live customers) | **WARN, not PASS** |
| right org, wrong file | mali's `REVISED` (421 keys) → `mali` (3,418 live) | ~96% of the file matched, **2,997 of 3,418 would be hard-deleted** → **FATAL** |

The last two are the ones that justify the design:

- **The empty org does not PASS.** With nothing to fingerprint against, A1 can
  confirm the org is empty and nothing more. Reporting that as PASS would be a
  verdict the evidence does not support.
- **The subset file matches ~96% and is still FATAL.** A naive "does the file
  overlap the org" check waves it through. It is caught only because A1 measures
  the deletion forecast rather than the overlap — and this is a real Magic Lite
  situation, where three customer files sit in one folder and only one is
  authoritative.

**The overlap figure does not have to be perfect for the check to work.** A
30-key sample of the `REVISED` file against `mali` found 29 present, not 30: the
miss is `ALCUR`, a customer that exists in **no** org — present in the source
file, never imported anywhere. So case 4 runs at ~96% overlap rather than 100%,
and the verdict is identical, because it is driven by the 2,997 forecast
deletions and not by the overlap percentage. A check that fired only at 100%
would be brittle against exactly this kind of ordinary source-file debris.

Cases 1–3 were measured live, and case 4's overlap was sampled live. Case 4's
verdict was produced by feeding the logic row counts verified during Phase 0
(421 distinct keys in the file; 3,418 live customers in `mali`) rather than by a
fresh full-key query.

### Limits

- **Rival-org scan is products-only.** `products_item_number_idx` makes it
  indexed and fast. `customers` has no standalone index on `code` (only
  `(organization_id, code)`), so the scan is skipped rather than run slowly — a
  customers file gets questions 1 and 2 but not 3.
- `stories.csv`, `options.csv` and `option_groups.csv` have no directly
  comparable live table, so A1 declines rather than guessing. Fingerprint the
  `products.csv` built in the same run; it shares the key space.
- Matching is case-insensitive (`upper()`), which is deliberate — a case-only
  difference is a near-certain match, not a new product.
- **Comparing distinct file keys to distinct live codes is sound for customers.**
  A customers file is bill-to rows plus ship-to continuation rows (mali's is 842
  rows over 421 codes), but that shape does not reach the `customers` table:
  mali has 3,418 customers with 3,418 distinct codes. The repetition is a
  file-shape property, not a data property, so de-duplicating file keys before
  the comparison is correct rather than lossy.
- A1 says the file belongs to the org. It says nothing about whether the file is
  *correct*. See "What §3 does NOT close".

---

## The `import_events` parser

`import_events.data` is a Ruby-YAML blob and PyYAML is not installed here.
Pulling the blobs out to parse in Python would move megabytes for nothing — leg
has 160 events and one inventory event carries 237 warnings — so **the parse
happens in SQL and only structured summaries come back**. That is what makes the
eventual fleet run affordable rather than a rewrite.

Org-scoped and parameterised by shortname; `--org-ids` switches to fleet batches.
Batched by `organization_id` because naive full-table aggregates time out at 30s
here. **Not run fleet-wide.**

```bash
python3 import_log.py --org leg --mode events|taxonomy|signatures --emit-sql
python3 import_log.py --org leg --mode events --from-results rows.json --out recs.json
python3 a4_b4.py --events recs.json --signatures sigs.json
```

### Two failure modes worth keeping written down

**`E''` strings silently break every regex.** Postgres consumes the backslash
inside `E'...'`, so `\s` reaches the regex engine as a literal `s` and the
pattern matches nothing — **returning zero rows rather than raising**. The first
taxonomy run reported no messages at all against an org with 6,115 of them. All
regexes here are plain single-quoted strings for that reason.

**Postgres regex `.` matches a newline.** `- (.*)` swallowed every following
message into the first one. Bodies are captured with `[^\n]*`.

Both fail *quietly*, which is the worst property a parser can have — hence the
comment block in the source and this note.

### The second job

The taxonomy mode aggregates message templates server-side, so it returns N rows
however many million messages sit behind it. Run across every org it becomes an
empirical error taxonomy — the corpus a config agent needs and that five clients
could never supply. leg alone yields:

| n | file | template |
|---|---|---|
| 6,115 | Inventory | `Line N: Product not found, record ignored., BaseItemCode=X` |
| 2,164 | Products | `Line N: Illegal quoting, probably in the following text: ...` |
| 362 | Products | `Line N: UPC value matches product on line N: BaseItemCode=X` |
| 171 | Customers | `Line N: error=Validation failed: Default price code must be valid` |

---

## A4 — option-group membership

**The canonical-order rule was DELETED 2026-09-04.** A4 used to assert
`options -> option_groups -> products -> stories -> inventory -> customers`
within a single import event and emit **FATAL** on any deviation. Nothing
motivated it: no incident, no line in BUILD_SPEC §3.1 A4, no line in this file.
It fired on ordinary working feeds —

| org | A4.order FATALs | that org's actual routine |
|---|---|---|
| `ufi` | **4,602** | `Products -> Inventory -> Product Stories -> Customers`, unchanged since 2013 |
| `ih` | 2,383 | (since 2025-01-01 only) |
| `pf` | 633 | " |
| `swc` | 607 of 609 multiblock events | " |
| `ta` | 291 | " |

— because Inventory (rank 4) legitimately precedes Product Stories (rank 3) in
those clients' routines. Ordering across unrelated importers is a preference,
not a correctness property.

What replaces it is the single adjacency with a **mechanism**: an `Option
Groups` block processed *before* an `Options` block inside one event has its
membership nulled again by that Options block. Reported at **INFO**, because
rule 2 below already scores the net standing effect and is where a defect would
actually show.

**Corrected 2026-09-04, after a false positive.** The first rule was "every
Options block must be followed by an Option Groups block before the next Options
block". It flagged pebl's most recent import:

```
09:28  Options -> Option Groups     paired
09:32  Options                      flagged
09:46  Products
09:54  Products
09:56  Options -> Option Groups     the remedy, 24 minutes later
```

09:32 *was* remedied at 09:56 — but the scan for "the next Options block" lands
on 09:56 seq 1, which precedes the remedying Option Groups block at 09:56 seq 2,
and closes the window unremedied.

**Iterating blocks rather than events does not fix this**; that loop was already
block-level. What was wrong was the question, not the granularity. The importer
runs an event's blocks in order, so an event's net effect is decided by its LAST
Options/Option Groups block, and membership is a running state over the event
stream:

- **FATAL** — the standing state is nulled, nothing has restored it
- **WARN** — membership was nulled for a period and later restored

Only the standing state is a defect. A transient window is real — reps syncing
inside it see no option groups — but it is a different claim, and conflating the
two turned **0 live defects into 17 reported ones**.

### Corrected numbers

| org | nulled windows | avg | longest | never restored | standing violation |
|---|---|---|---|---|---|
| leg | 1 | 2.6h | 2.6h | 0 | **0** |
| tcs | 42 | 69min | 25.8h | 0 | **0** |
| pebl | 25 | 11.4h | **276.5h** (11.5 days) | 0 | **0** |

Corroborated in live state: option groups carrying membership are `leg` 11/11,
`pebl` 423/423, `tcs` 343/343 — no empty group anywhere.

The one worth a client conversation is pebl's **2026-04-10 → 2026-04-22** window,
11.5 days with membership nulled. That is a measurement about the import log;
whether any rep synced inside it and saw nothing is a separate claim this check
does not make.

**The code now says that too (fixed 2026-09-04).** Every `A4.membership_window`
finding used to end with the sentence *"Reps who synced inside that window saw
no option groups."* — a consequence, asserted unconditionally, with no reference
to `login_events`. OPEN_ITEMS G1 had already settled the wording after doing the
work: a login is not proof of a sync, and a sync is not proof anyone opened a
product with options. Findings now carry `measured` / `not_established` fields
in the same shape B4 uses, and name `login_events` as what would settle it.

Window counts are per **window**, not per event: pebl has 25 events ending on an
Options block but **20 nulled windows**, because consecutive Options-ending
events collapse into one. Earlier notes quoting 25 were counting events.

Two independent implementations (Python over records, SQL over the event stream)
agree on every figure above — the same discipline that made the original bug
findable.

## B4 — two files feeding one importer

**Rewritten 2026-09-04. Range overlap was never the test.**

The first version asked only "do the two signatures' `[first_seen, last_seen]`
ranges overlap". For any long-running feed they always do, so it fired on
drift — a feed whose error count moves — as loudly as on two real files:

| org | B4 before | of which FATAL | after |
|---|---|---|---|
| `cl` | 1,048 | 1,033 | **0** |
| `sp` | 247 | 0 | 1 |
| `uhc` | 201 | 167 | **0** |
| `ufi` | 151 | 49 | **0** |
| `pebl` | 23 | 1 | **0** |
| `clli` | 20 | 3 | **0** |
| `fal` | 16 | 7 | **0** |
| `mali` | 3 | 1 | **0** |
| `leg` | 1 | 1 | **1** ✅ |
| `libco` | 1 | 0 | **0** |
| **13 orgs** | **1,711** | **1,262** | **2** |

`cl`'s 1,033 FATALs were an Inventory feed that ran **clean 5,641 times out of
5,865**, whose three "competing files" were one feed drifting 1 → 14 → 17
warnings over six months.

**`fal` is the case that shows what a signature actually is.** Its seven
Customers FATALs came from a ten-day window in January 2025 in which the same
file was re-uploaded after each fix. `0/1001` is "still lots of billing errors";
`0/8` is "down to the last eight" — and those eight are byte-identical across
2025-01-20, 01-24, 01-28 and 01-29 ×3:

```
Line 1927: error=Validation failed: Shipping post code can't be blank: Customer # = 851825
```

One file being iterated is indistinguishable from two files alternating *if all
you compare is a count*.

### The three tests

Two files feeding one importer implies all three. None is a knob.

| test | rule | meaning |
|---|---|---|
| **coverage** | `n_pair / n_win ≥ 0.90` | if two files alternate into an importer, nearly every run of it is one of them. `leg`: 37 of 37 |
| **alternation** | `alts ≥ 5` **and** `alts / (n_pair−1) ≥ 0.30` | `A…A B…B` is one file *replaced* by another and scores near zero at any volume |
| **volume** | `n_pair ≥ 10` | enough runs to see a pattern at all |

The rate is needed as well as the count. `sp`'s Kit Items pair is **340 events
at 96.6% coverage with 8 alternations** — 2.4%, drift wearing coverage's
clothing. A bare `alts ≥ 5` would have passed it.

### Validated against four cases whose answer is known independently

```
leg   Inventory 237/0 vs 10/0    100% coverage, 19 alts, 52.8%   -> FIRES  (correct)
cl    Inventory, 246 pairs       max alternation rate 16.7%      -> silent (correct)
fal   Customers, 7 pairs         max 2 alts at >=90% coverage    -> silent (correct)
pebl  Option Groups              0 alts; 423/423 groups OK       -> silent (correct)
```

The one survivor besides `leg` is `sp` **Products**, 2021-09-16..09-26: 11 runs,
100% coverage, 5 alternations. Genuinely alternating; `Products` soft-deletes
rather than hard-deletes, so WARN. A five-year-old window, reported as what it
is.

### Input, and the declined path

B4 now consumes `import_log --mode feed_pairs`, which computes coverage and
alternation **server-side** — `cl` has 39k blocks and `clli` 64k, so streaming
them to Python was never affordable. That mode is deliberately two-stage
(`HAVING` on coverage, then the window function only for survivors); the
one-stage form times out at 30s on `cl`.

A `--mode signatures` file is **declined**, not silently downgraded:

```
INFO    B4.not_evaluated
        NOT EVALUATED - B4 needs `import_log --mode feed_pairs`. The rows supplied
        are `--mode signatures`, which carry only per-signature date ranges; whether
        two signatures ALTERNATE cannot be decided from those, and testing range
        overlap instead is what produced 1,262 FATALs of which two were defensible.
```

### What it still does not establish

The signature is a **count** of warnings and errors. Two different files produce
different message *content*, and comparing content is what would settle this
definitively. `--mode taxonomy` is the substrate for that and is not wired in.
Every finding says so.

**Known gap, not fixed:** the signature is `n_warning/n_error` and ignores
`fatal`, so a fatal-tier block reads as `0/0` and is dropped as clean. `fal`'s
2025-01-23 `Column shiptoaddress1 is missing` block is one. Two characters to
fix; out of scope for this change.

---

### The original note, kept

Detector is the message-count signature: one file produces one recurring
signature, two alternating files produce two, interleaved over the same window.

leg Inventory, confirmed:

```
237/0   23 events   2026-08-05 .. 2026-09-04
 10/0   17 events   2026-08-05 .. 2026-09-03
```

Forty events, two signatures, one window. `Inventory` hard-deletes and reloads,
so only one file's rows survive at a time — which matches folder mode's finding
that leg's two inventory files share **zero** item numbers.

**A feed must recur over time.** The first version flagged leg's Images on
2025-06-13, where signatures `10/0` and `12/0` were one demo-day batch uploaded
in pieces. Requiring each signature to span more than a single day removes it.

**What B4 measures and what it does not.** It measures the *log*. Two signatures
is strong evidence of two files; it does **not** establish which file's rows are
live right now. Every finding says so and names what would settle it — comparing
the live key set against each candidate source file.

---

## B1 — registered custom fields

**The leg incident is the inverse of the criterion as written.** B1 says
"registered, but no product carries a value". leg's 13 fields were the other
direction: `rohscompliant`, `Color`, `voltage`, `wattage`, `switchtype`,
`workswith`, `wiresize`, `mountingtype`, `prop65`, `warranty`,
`numberofswitches`, `bulbcompatibility`, `numberofgangs` were **in
`products.csv` and never registered in Admin**, so the importer warned
`Custom field 'X' is missing` and dropped them.

Verified: leg has **5** registered custom fields — `Finish`, `CountryOfOrigin`,
`drop_ship`, `shipped_via`, `order_uom` — and **all five are well populated**
(1001, 897, 1020, 1020, 851 of 1020). `numberofgangs` is not among them, so it
was never "registered as a filter with `send_to_ipad = true`". **leg has zero
violations of B1 as written.**

Same client-visible outcome, opposite mechanism, opposite fix. So the check has
two halves:

    B1a  registered, but no product carries a value       post-import
    B1b  in the file, but not registered - dropped        pre-upload

B1b reproduces the leg incident from **the file plus the registry alone**, with
no reference to the import log — which is what makes it a pre-upload gate rather
than an autopsy.

### The two storage shapes

    db_column_name   'ecat_custom_field_N' - a real column (180 of them exist)
    alias            a POINTER, with no storage of its own:
                     'i.qty_on_hand'    -> inventories.qty_on_hand
                     'ic.ML_QtyOnHand'  -> inventories.custom_fields JSONB key
                     'pl.murray'        -> a price level
                     'upc_value'        -> products.upc_value

An alias field cannot be "empty because nothing populated it" the way a column
field can — it inherits whatever its target holds. So the two are reported
separately rather than summed; counting them together manufactures zeros.

`cl` uses both in one org: 16 column fields and 5 aliases, including
`i.qty_available` — the same field B5 reads for inventory display.

### Findings at `cl`

Nine registered fields are populated on under 5% of 724 live products. Two are
registered **multi-select filters**:

| filter chip | populated |
|---|---|
| Shade | 20 / 724 (2.8%) |
| LampType | 22 / 724 (3.0%) |

Not empty, so not BLOCKING — but a filter that matches 20 of 724 products reads
as broken to a rep. Reported as WARN with the percentage rather than a verdict,
because whether that is deliberate is a client question.

Findings show the **label** a rep actually sees, with the internal field name in
parentheses — `Shade (xxShade)`. The chip text is the client-visible artifact and
is what the conversation will be about.

---

## A2, A3, B3, B5 — `state_checks.py`

```bash
python3 state_checks.py --org drf --check all --emit-sql
python3 state_checks.py --org drf --from-results rows.json --measured-at 2026-09-04
```

### F6 — one ladder, `stage`, demotion, repair channels, org-state header

Implemented 2026-09-05 from `ground-truth/SPEC_F6_severity.md`. `severity.py` is
the shared module; no check decides its own vocabulary any more.

| | |
|---|---|
| **severities** | `BLOCKING` · `WARN` · `INFO` — all three in all five modules |
| **`FATAL`** | **retired.** `fatal` is the *importer's* word (`import_log.py` computes it for import tiers); two live meanings for one word made "was that finding fatal?" ambiguous |
| **not severities** | `NOT CHECKED` (method) and `DECLARED` (intent) — no ladder position, never demote, counted separately |
| **`stage`** | `pre_upload` (A1, B1b) · `post_import` (everything else). A `BLOCKING` at `pre_upload` means *stop*; at `post_import` it means *remediate what is live* |
| **demotion** | one level, **closed evidence only**, against the declared channel |
| **`repair_channel`** | `file:<type>` · `admin:<table>` · `none` |

**The closed-evidence clause is the regression test.** `leg`'s B4 finding (A8)
has an alternation *window* of 2026-08-05..09-03 and the last Inventory import
is 09-04 — a naive "evidence older than the last relevant import" rule demotes
it. For a **standing** condition the most recent import is part of the evidence,
not a chance to have fixed it. B4 therefore reports `pair_last_seen`
(`greatest(a.ls, b.ls)`, = 09-04) rather than the window end, and `leg` stays
`BLOCKING`. If A8 ever demotes, the clause was dropped.

**`admin:custom_fields` was verified before being declared**, per the spec:
`custom_fields.updated_at` is non-null on 13 of 13 cohort orgs and diverges from
`created_at` on 11 of 13, so it is maintained rather than a create-time
backfill. `orders.price_level` gets `none` — a historical order's price-level
string is immutable, so the finding says *demotion does not apply* instead of
appearing to have been evaluated.

**A bug worth keeping written down.** The first run demoted **nothing**: the
declared channel `file:option_groups` never matched the `import_events` key
`Option Groups`, because the lookup normalised case but not separators. A silent
miss there is indistinguishable from "no repair opportunity", so all 73 A4
windows sat at WARN looking evaluated. `_key()` now folds case *and*
spaces/hyphens to underscores.

### The org-state header

Printed on **every** report, clean or not — that is the structural answer to the
cold read, because a green report becomes impossible once the org's state is on
it.

```
ecat-acceptance — leg (Legrand US, org 273)     status: onboarding
  users            14 provisioned · 11 ever logged in · 8 active in 30d
                   (org_users rows; "rep" per collector/queries.py::REPS is a
                    narrower count and is not this number)
  login history    13 distinct users seen in login_events; 2 of them NO LONGER
                   PROVISIONED · last 2026-09-04
  last login       iPad 2026-09-04 · eOL never
  last import      any 2026-09-04 · Customers 2026-08-28 · Inventory 2026-09-04 ...
  orders           1 submitted · last submitted 2026-09-03 · last row written 2026-09-03
```

Three requirements, each from something that already cost us:

- **never vs dropped** — "0 users" reads identically for a pre-launch org and one
  that lost forty last month. `login_events` survives user deletion, so it can
  say which. This makes the header the **first consumer of `login_events`**,
  closing part of D13/D16. It immediately finds `pebl` 10, `ufi` 15, `clli` 13
  users who used the app and have no `org_users` row today.
- **name the clock** — both order clocks, always (G4). They differ on `libco`
  (submitted 2026-08-11, row written 2026-08-24) and the header says so.
  Likewise iPad and eOL logins are two surfaces (D14).
- **state the definition** — provisioned / ever-logged-in / active-in-30d are
  three numbers, and the header says it is *not* the framework's `REPS` count.

### Severity discipline, and why it is the hard part

Three findings in a row were right about the fact and wrong about the severity:
A4 (18 defects → 0), B1b (13 blocking → 13 informational), and cl's sparse chips
(correctly WARN first time). **The failure mode is not missing things — it is
over-alarming, and the cost is that an operator stops reading the output.**

All four of these are threshold checks, which is exactly where that lives. So:

    BLOCKING  a client-visible defect, evidenced
    WARN      real, but severity depends on intent only the client knows
    INFO      measured, notable, not a defect

B3 is the clearest case. Empty territory codes on an org with **reps
provisioned** is BLOCKING — filtering is off and every rep sees every customer.
The identical measurement on an org with **no non-admin users** is INFO: nothing
is being mis-filtered today, and it becomes blocking the moment reps arrive. Same
number, different consequence.

### Dated measurements

Every finding carries `measured_at`, and the footer says state moves. leg's
custom-field registry changed between 2026-08-27 and 2026-09-04 and both readings
were accurate for their moment; without a date, one of them just looks wrong.

### Verified against live orgs, 2026-09-04

| check | org | result |
|---|---|---|
| A2 | drf | **BLOCKING** — `net` carries 389/389 customers and resolves to ONE value ($1.00) across 1,627 products |
| A3 | drf | pass — all six reference classes resolve |
| B3 | pebl | **BLOCKING** — 171/171 empty, 10 reps provisioned |
| B3 | drf / leg / mali | pass — 389, 1,133, 3,418 all carry territories |
| B5 | cl | INFO — alias `i.qty_available` agrees with the populated column |
| B5 | leg | WARN — 755 rows, on-hand 727, **no alias registered** |

### Count discipline — three requirements

**Every count ships with an example.** A3's 29,161 was plausible; the specimen
`'"ADELINA-UV-ASH"'` (quotes attached) is what exposed it. Volume makes a wrong
count more convincing, not less. If a specimen cannot be produced, the count is
not ready to report.

**Name each state separately.** B5 reported leg's on-hand as "727 populated".
Measured: 755 rows, 755 non-null, **704 > 0, 28 exactly 0, 23 negative** — 727
was the non-zero count, which described none of those states and silently folded
in the negatives. "No stock value" and "a stock value of zero" read differently
to a rep, so both are now reported.

**Use the system's own definition of a shared word.** B3 reported pebl as "10
reps"; the framework counts **9**, excluding `chuck+u@supercatsolutions.com` as
SuperCat staff. B3 now uses `collector/queries.py::REPS` verbatim — not
`is_admin` alone — and names who it excluded. Neither correction changed a
verdict; both would have eroded trust on a recount.

### One false positive caught before it shipped

A3's related-items branch first reported **29,161 dangling references at drf**.
`related_items` is stored as a **JSON array string** (`["A","B"]`), not the comma
list the CSV carries, so splitting on `,` left brackets and quotes attached and
every element failed to resolve. The example value gave it away — it came back as
`'"ADELINA-UV-ASH"'`, with the quotes. Parsing the array properly takes it to
**0**.

Worth noting how it was caught: not by review, but by the check printing an
example alongside its count. A bare "29,161 dangling" would have looked
plausible.

### Limits

- **A2 evaluates `ad-hoc` price levels ONLY, and now declares the rest.**
  `net` is read from `products.net_price`; every other ad-hoc level from the
  `prices_json` blob (TEXT, so it needs a `::jsonb` cast). `arithmetic` and
  `quantity` levels store NO key there - their value is computed from
  `net_price` x `factor` - so a level carrying more than half the org's
  customers that is not ad-hoc is reported as `A2.not_evaluated` (INFO) rather
  than measured against the wrong column.

  **Corrected 2026-09-04.** The previous wording said A2 "does not evaluate the
  arithmetic", which describes silence. The code did not stay silent: it read
  `prices_json ->> code`, got NULL on every row, and emitted a defect finding
  from what `count(DISTINCT ...)` returned after discarding those NULLs. On
  `uhc` that was a **BLOCKING** finding - 'wholesale' is arithmetic factor=1.0,
  exactly ONE of 4,433 products carried a stray `wholesale` key at 307.89, and
  A2 reported "resolves to ONE distinct value across all 4433 live products".
  The catalogue carries 396 distinct net prices, $0.00-$450.00. Fleet-wide,
  **46 of A2's 47 findings were this artifact**; the 47th was `drf`, closed as
  by design in OPEN_ITEMS A9.

  Resolving arithmetic properly means following `factor` and
  `target_price_level_id` chains. That is a separate job and is not needed to
  stop the check lying.

- **A2's denominator is the products that carry a price for the level**, not the
  catalogue. `products_carrying_value` is selected for exactly this. The old
  text said "across all N live products" with N = the whole catalogue even when
  the distinct count came from one row - OPEN_ITEMS F7's shape, a partition that
  does not describe what it claims.

- **Residual, not fixed:** an ad-hoc level with >50% of customers, one distinct
  value, and only a handful of products carrying it would still be BLOCKING. No
  live org is in that state today (the only ad-hoc hit fleet-wide is drf at
  1,627 of 1,627), and the denominator now makes the situation visible in the
  message rather than hidden. Add a carrying-share threshold if a case appears.
- A3 does **not** cover image filenames. That is B2, still unimplemented and
  still blocked on FTP access.
- B5 reports what is registered and what is populated. **What the iPad renders
  when no alias is registered is not established** — leg's WARN says so
  explicitly rather than concluding reps see nothing. That inference is what
  produced SCORECARD §12 R1.
