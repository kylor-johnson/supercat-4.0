---
name: ecat-source-profile
description: Profile a client's source folder or file BEFORE any eCat build - which files are catalog source vs Library content vs noise, which are duplicates and which is authoritative, which eCat file each is trying to be, what is missing, and what does not add up. Read-only. Use whenever client source data arrives, before writing any mapping or transform.
---

# ecat-source-profile

Profile before you transform. The expensive question is never "how do I parse this
column" — it is **"which of these files is the one, and is this even catalog source?"**

Five client audits say the same thing: the losses were **specification failures**, not
transform bugs. Nobody established what the source contained before building on it.
drf lost two weeks and Showtime that way.

**Read-only.** Opens files, writes nothing but its report. No Postgres writes, no Admin
Console, no imports.

## Two modes, folder first

```bash
python3 folder_mode.py "<client>/Source Data" [more folders...] [--json out.json]
python3 file_mode.py   "<path to one file>" [more files...]
```

Run **folder mode first, always.** File mode on the wrong file is wasted work.

### Folder mode answers

1. catalog source vs Library content vs noise vs tabular-but-unreadable
2. how files relate to each other — see the taxonomy below
3. which eCat file each candidate is trying to be
4. what is missing entirely

### File mode answers

1. what is this — rows, cols, encoding, delimiter, **where the header actually is**
2. what's populated — fill rate per column; a 3%-populated column is not a field
3. what looks like a key
4. what maps to eCat — proposal **with confidence**, never a bare assertion
5. what's missing — required fields with no source, each with a reason
6. what doesn't add up

## The relation taxonomy — four different actions, do not conflate them

Getting this wrong destroys data. Each verdict implies a different action:

| relation | evidence | action |
|---|---|---|
| **rival-version** | same shape, same keys, different row counts | choose one |
| **superseded** | every key of the smaller is inside the larger | drop the smaller |
| **complementary-partition** | same shape, keys barely intersect | **UNION — choosing drops a slice** |
| **division-variant** | same shape, filenames differ by one token | **MERGE into one file with per-division columns** |
| **mapping-pair** | high key overlap, low header overlap, one raw + one mapped | keep both |
| **key-linked** | different eCat targets sharing a key | expected join, not a duplicate |
| **format twins** | same content, different declared format | drop one only if byte-identical |

## Rules learned the hard way

**Route on magic bytes, never on the extension.** Legrand ships XLSX workbooks named
`.csv` (`50 4B 03 04`, `xl/workbook.xml` inside). An encoding ladder will "successfully"
decode those ZIP bytes as mac_roman and return 700KB of confident garbage — **worse than
crashing**, because it looks like an answer. Sniff the content; if it contradicts the
extension, say so and parse it as what it is.

**A measurement and its consequence are two claims.** SCORECARD §12 R1. The original
instance: `qty_available` was NULL on 439 rows (measurement) → "the iPad shows nothing"
(consequence, invented, told to a client, false — display is configurable).
The second instance, same shape: `tr` throws "illegal byte sequence" (symptom) →
"this is an encoding problem" (cause, asserted, wrong — it is a ZIP). **Verify the
consequence separately, or state the measurement alone.**

**Uniqueness is the wrong key test once the target is known.** `customers.csv` is bill-to
rows plus ship-to continuation rows, so BillToCode legitimately repeats: 842 rows over 421
distinct codes is the *expected* shape, not a broken key. Ask "does this match the key
semantics of the eCat file it claims to be", not "is this column unique".

**Per-division files are not rival versions.** Two files of the same shape whose names
differ by exactly one token (ML vs NSL, adorne vs radiant) are one dataset split by
brand or warehouse. eCat merges them into ONE file with per-division columns
(`Price_ml_list`, `NSL_QtyOnHand`). Calling them rivals tells someone to delete a
division.

**Use containment, not Jaccard, to compare key sets.** A 421-row file whose keys all
appear in a 3,517-row file is *superseded* by it. Jaccard reads 12% and says
"complementary — union them", which is the opposite of the right answer.

**mtime is worthless in this tree.** A bulk merge on 2026-09-03 stamped nearly every
file with that date. Never infer recency, and never infer which file came first, from a
timestamp. For derived-copy direction prefer content hash and row-count containment;
where those cannot decide, print **undetermined** rather than guessing from a directory
name — `_converted/` is a filename, not evidence.

**Take the most populated worksheet, not sheet 1.** A cover or notes sheet in position 1
hides the data. Legrand's radiant-CA workbook has four sheets; three had never been
profiled by anything.

**A false certain is worse than an honest moderate.** A reader checks a "moderate";
they act on a "certain". Confidence must fall as evidence weakens, and a match that
required an assumption is never "certain".

**EVERY COUNT SHIPS WITH AN EXAMPLE. This is a requirement, not a habit.**
A count without a specimen cannot be sanity-checked, and **volume makes a wrong
count more convincing, not less**. The reference integrity check reported *29,161
dangling related-item references* at drf — entirely plausible, and entirely an
artifact of splitting a JSON array string on commas. The only thing that killed
it before it reached a client report was the specimen printed beside it:
`'"ADELINA-UV-ASH"'`, with the quotes still attached. Nothing else in the output
was wrong-looking.

So: any finding that states N of something must show at least one of them. If a
specimen cannot be produced, the count is not ready to report.

**When two columns look like they answer the same question, they usually
answer adjacent ones. Name which you used.** This family has bitten this project
four times now:

| pair | trap |
|---|---|
| `qty_available` / `qty_on_hand` | both run live; which one displays is CONFIGURED (§12 R1) |
| `custom_fields.db_column_name` / `.alias` | two storage shapes; checking one reports false zeros for the other |
| `last_ipad_login_at` / `last_ecat_online_login_at` | two surfaces; measuring one under-reports any eOL org (D14) |
| `users.last_login_at` / `login_events` | **different events entirely** |

The last one, measured 2026-09-04 across 139 users in 8 cohort orgs:

    139 have last_login_at
    100 have any login_events
     39 have last_login_at and ZERO login_events   (28%)
    125 have last_login_at LATER than their newest login_event   (90%)

`ckirbeyi@ica.com.tr` shows the shape: `last_login_at` 2026-07-28 01:26, newest
`login_events` row 2026-07-24 12:32. There is a login on 07-28 that produced no
event row. **Neither source is wrong; they count different things**, and
`login_events` systematically under-reports recent activity — read alone, it
would call 39 of those users never-logged-in.

What the difference IS has not been proved and the harness must not assert it.
Plausibly `login_events` records device/sync sessions while `last_login_at` also
catches web or Admin access — plausible is not measured. **State which source a
figure came from, and never substitute one for the other.**

**Deleted parents NULLIFY their children's references — count the NULLs
explicitly.** `GROUP BY creator` returns the creators that still exist and
silently drops everything whose creator was deleted; the result looks complete
because every group in it is real. pebl: 93 submitted orders, 8 distinct
creators, and **27 orders (29%) with a NULL creator** because those users were
deleted. Every read of "who is ordering here" was made on 66 of 93 rows.

Nothing dangles, so a referential-integrity check finds nothing wrong. The only
trace is `audit_log_entries` and `login_events`. This is silence-is-not-zero with
a named mechanism: **always report the unattributable count beside the grouped
one.**

**PARTITIONS MUST SUM TO THE TOTAL, and each part must be measured, not
derived.** It is the cheapest specimen there is. A published breakdown of leg's
inventory read "755 non-null, 704 greater than zero, 28 exactly zero" — and
704 + 28 = 732, not 755. The missing 23 were negative values, one at -12,643.

Two traps, and the second is subtler:

1. Check the sum before publishing any part of a breakdown. If it does not add
   up, none of the numbers are reportable yet.
2. **Derive nothing.** If "zero" is computed as `non_null - gt_zero - negative`,
   the sum can never fail and the check is vacuous — the same flaw as a test
   that cannot go red. Every part needs its own COUNT.

**Name each state separately; never merge them into one word.** "Populated" hid
three different things in one inventory column: leg has 755 rows where 704 are
above zero, 28 are exactly zero, and 23 are negative. A single figure of 727
described none of them, and "no stock value" versus "a stock value of zero" is a
difference a rep experiences.

**Use the system's own definition of a shared word.** Counting "not is_admin"
gave 9 reps as 10 at pebl, because the framework's rep definition also excludes
SuperCat staff, disabled accounts and the default user group. Two parts of one
system disagreeing about what "rep" means is worse than either being wrong alone.

**A parser that quietly reports nothing is worse than one that breaks.** Two
silent failures cost real time here: Postgres `E''` strings consume the backslash,
so `\s` reaches the regex engine as a literal `s` and the pattern matches nothing
— returning zero rows rather than raising, against an org with 6,115 messages.
And Postgres regex `.` matches a newline, so `- (.*)` swallowed every following
message into the first. Prefer the form that fails loudly, and when a parse
returns nothing, verify that against a known-non-empty case before believing it.

**Never print an unverified zero.** Undetermined prints as "undetermined" with the reason
and what would settle it.

**Scope an exact eCat-name match to the detected target.** `Name` is a real field in
`options.csv`, but in a NetSuite products export the `Name` column holds the item code.
A target-blind "certain" is a false certain, and a false certain is worse than an honest
"moderate".

## Reusable value checks — the ones that ship silently

**Identical values under two names.** Legrand's `MSRP CDN` and `IMAP CDN` hold the same
448 values over the same 235 distinct amounts. That is one price level wearing two
names, not two levels — and building two is a config error nobody notices until a rep
sees the wrong number. Compare value multisets across columns, not just headers.

**Binary-float tails.** `5.8740000000000006` is a spreadsheet rounding artifact, not a
price. 143 of them in one Legrand column. Any value with 5+ decimal places heading for a
money field must be rounded first; the importer will happily take the tail.

## Input classes — detect which, they need different handling

| class | what to do |
|---|---|
| **Raw ERP export** | map it |
| **Pre-mapped by a human** | **validate, do not transform** — the mapping is done; the job is checking it |
| **Hybrid** | eCat headers *and* client-domain columns side by side; map only the client half |
| **Industry template** | map, but the template is the contract |

## What it does not do

It proposes a mapping and flags what it cannot map. **It does not write transform code**
— that division is the whole point. It also cannot decide authority between rival files
on its own: that needs reconciliation against the live org (`ecat-postgres-audit`), and
the report says so rather than guessing.

A clean import proves the file parsed and nothing else. Never treat import success as
done.

## Files

- `folder_mode.py` — folder mode
- `file_mode.py` — file mode
- `ecat_vocab.py` — eCat field vocabulary + key semantics; header names sourced from
  `preflight/limits_generated.py` (generated from `supercat_server`), never transcribed
- `ecat_aliases.py` — source-column → eCat-field aliases, each with a confidence
