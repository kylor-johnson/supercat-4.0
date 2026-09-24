# Phase 2b — findings for `ground-truth/`, reported rather than filed

`ground-truth/` was read and **not modified**, per the run instruction. These are
the entries to file there, with the evidence each one rests on.

Two are SOURCE-ONLY and are marked so. A23 is the rule: a source-only finding
stays out of OPEN_ITEMS §A until it is confirmed against live Postgres. Both
were true of libco's source and false of its org, which is how that rule got
written.

---

## For OPEN_ITEMS §A — confirmed against a trusted build, not against live

These are confirmed against the client's own shipped build files (pinned by
hash in `mapping/baselines.toml`). They are **not** live-Postgres confirmed, and
under A23 that means they belong in the pending bucket until someone runs the
`tcs` and `mali` org queries.

**P1 — `tcs` option codes: five carry two different names, one across two
option types.**
`LR` is `Ladder Rests` on some products and `Post Ladder Rest` on others — a
MOUNT on one and a POST accessory on the other. `options.csv` is keyed on Code
globally, so one code is one option with one name; the second name is discarded.
Also `HSCM` (Heavy Chain Mount / Heavy Slope Ceiling Mount), `PFPAU`, `BMDSM2`,
`BS4`. 37 occurrences. No import objects.
*Evidence:* `Master Sheet E+G-Table 1.csv` + `Weiyan LED-Table 1.csv`, counted by
`mapper.py` as `option.code_collision`.
*To confirm live:* whether the org's `options` table shows one row or two per
code, and which name the iPad shows.

**P2 — `tcs` ships 13 option codes that exist in no file in its folder.**
`BRASS`, `COPPER`, `COY4`, `COY5`, `COY8`, `CY06`, `CY07`, `CY18`, `CY20`,
`GNP7`, `PFA`, `COY12`, `COY13`. Added by hand from a source outside the
implementation tree. A regeneration from the folder drops all 13, and
`options.csv` HARD-deletes.
*Evidence:* `CS_eCat_Rebuild/options.csv` (pinned) minus the union of
`Accessories-Table 1.csv` and the transposed block.

**P3 — `tcs` option swatch filenames are not derivable and only 31 of 341 use
the default.** The rest are a hand-built map (`ContempoFlush_ADS.jpg`,
`BFH.jpg` shared across BFH1..BFH10) that exists nowhere in the source folder.
Regenerating `options.csv` with the importer's `{code}.jpg` default would be
wrong on 310 of 341 and would take every swatch off the iPad. **This is Legrand's
19 destroyed images (A-series) in a different file.**
*Evidence:* `CS_eCat_Rebuild/options.csv` ImageName column vs `Code + '.jpg'`.

**P4 — `mali`'s live customer addresses are not reproducible from its folder.**
Over 3,412 shared codes, `ML + NSL CUSTOMERS COMBINED 2.0.csv` is blank where the
live file is filled on **2,701** `BillToAddress1` and **2,996** `BillToCountry`;
where both are filled they disagree on 371 addresses, 1,428 postcodes, 1,054
cities and 589 states. The export's `BillToAddress1` holds CONTACT NAMES on many
rows (`SALES MANAGER`, `JULIANNA`, `TOM/JAN/BERNIE`). This is not formatting:
`EASTON MD 21601` against `PHILADELPHIA PA 19101` is a different address.
`customers.csv` HARD-deletes all customers and ship-tos before reloading, so a
regeneration from this export destroys the address book.
*Evidence:* pinned `Ready_For_Import/customers.csv` vs the export.
*Action:* an address-enriched customer export is an outstanding client ask.

**P5 — `mali` drops 105 of 3,517 source customers by a rule that is not in the
source.** Not blank-address (67 of 105, against 2,768 of 3,517 overall), not
duplicates (0 duplicate codes), not one division. Four of the first five are
Torbram Electric branches. A hand-curated exclusion whose reason is not
recorded anywhere.

**P6 — `pebl`'s option stack has no source in the repository.**
`IMPORT_README.md` names `ecat-options mapping.xlsx` as "the client's source
mapping document". It is not in the folder. `options.csv` (57 options) and
`option_groups.csv` (62 groups, including hand-applied `PriceAddend` values of
-70, -16, -32, -50, +10) cannot be regenerated, and both files HARD-delete on
import. `option_mappings_spec.json` documents the Admin cascade and not the
options.
*This is the same shape as drf's "the data question was never settled", one step
later: the question was settled and the answer was not kept.*

**P7 — `tcs` files `LR` (Ladder Rests) under POST & PIER MOUNT in its own
accessory catalogue, and it is a ceiling mount.** The live build corrects it to
Ceiling Mount by hand. The miscategorisation is in the client's data, and
because option groups are per-product it propagates to **171 of 379 products**:
reproducing the client's own category cost 68 of 100 member sets and 22 points
of group-membership recall.
*Evidence:* `Accessories-Table 1.csv` row `LR | Ladder Rests | POST & PIER
MOUNT` against `CS_eCat_Rebuild/options.csv` `LR -> Ceiling Mount`.
*Client action:* fix the category in the source, or the correction has to be
re-applied by hand on every rebuild. It is currently declared in
`mappings/tcs/options_v2.toml § option_type_overrides`.

**P8 — `tcs`'s `Post Ladder Rest` column carries `LR` on 3 rows where the other
156 are `PLR`.** A source typo that puts a ladder rest on three products that
should have a post ladder rest. **Not corrected in the mapping** — reproducing
it is right; telling the client is a separate action.

**P9 — `tcs` option availability: the build offers a NARROWER set than its own
matrix states, on 1,540 product-option pairs.** Resolving both sides' OptionSet
columns through their own option_groups, **0 of 379 products have identical
option availability**: 7,749 offers agree, 1,312 are missing from mine, and
**1,561 are extra** — a rep can pick an option the build does not offer for that
product. Concentrated: `ADS` 94, `TLA` 85, `WY` 53, `PFPA`/`PMG`/`GH2` 50 each.
**Not a parent-SKU rollup** — tested and refuted, the build varies within a
parent on 99 of 120 parents, exactly as much as the matrix does.
*Consistent with* the build's own `option_groups_audit_fix.csv` and
`apply_tuesday_fixes.py`, i.e. corrections applied outside the folder.
*The question for the client:* is the Master-sheet option matrix stale, or are
the audit fixes the truth? The folder cannot say, and `options.csv` and
`option_groups.csv` both HARD-delete.
**This is the finding that blocks options for tcs.**

---

## For OPEN_ITEMS §F — my own errors, so the next run does not repeat them

**F-a — classification is per (source file -> target file type), not per source
file, and I treated it as the latter.** `Accessories-Table 1.csv` was classified on the products run as a source
of products. Correct — 46 of its 419 rows ship as products. It is ALSO the option
catalogue: 338 of the build's 341 options are its rows, and its
`Accessory Category` column is the eight-way option-type partition I derived by
hand from column names in the blind mapping.

The generalisation, which matters more than the instance: a class-3 folder with
S sheets and 6 target file types poses **6S** classification questions, and both
the profiler and I answer S of them. Phase 0's target coverage asks "which sheet
feeds products.csv" and stops. **This will recur on the next multi-sheet
client.** Filed as gap 10 in PHASE2_COMPLETE.md; the cheap fix is to fold the
grid into folder mode's coverage line so an unanswered cell is visible rather
than assumed.

Cost here: ~30 points of option accuracy and a paragraph of invented reasoning.

**F-b — I applied a class-3 principle to a field the importer validates.** Blind,
`BillToState` shipped `Florida` rather than `FL`, on the grounds that editing a
client's text is a transform nobody asked for. That is right in general and cost
1,440 cells — 62% of every difference in the file. **A rule about not editing the
client's text does not survive contact with a validated field.**

**F-c — I emitted a value I could not derive.** `ImageName = {code}.jpg` on 328
option rows, wrong on 322. The rule already existed, in this programme, in
writing, from Legrand's 19 images: *a value the generator cannot derive must come
from the last known-good file or a regeneration destroys it.* I broke it while
the rule was two directories away.

**F-c2 — I gated on the wrong metric, and it read green.** `group_membership`
counts DISTINCT member sets. With per-product groups that is a poor proxy for
what a rep sees: the Finish family is 2 of 311 sets and applies to 375 of 379
products. It reported 91.0% while per-product option availability was exact on
ZERO products, and a 91% row on a HARD-DELETING file type sat in a summary
implying options could ship. The end-to-end check now exists and
`acceptance_2b.py` states that PASS means no regression, not readiness.

**F-d — my own test could not go red twice.** In `acceptance_2b.py`, mutating an
axis's option type from GAS to BULBS moved membership by 1.9 points (7 options in
a 341-option file) and `null_tokens = []` changed nothing at all — the catalogue
lookup filters `----` before the null check runs. Both were passing mutations
that tested nothing. Same family as the six §3.4 instances.

---

## For BUILD_SPEC

**§2 — the tcs escape-hatch row needs no change** (options/option_groups/
customers/stories used 0 hatches across every client). But §2's "genuinely
client-specific" list should record that `stage2_lantern_rebuild` and
`sku_ignition` are the option stack, and that the option stack is now a declared
mapping shape rather than client code.

**§3.4 coverage — applied, and it caught its own tool.** `score_blind.py` had no
coverage statement and its case-sensitive column match was the fifth of the six
instances. It now states coverage on the column partition, on the cell count, on
the membership score, and on the "cannot score" path. `folder_mode.py`,
`required_check.py`, `mapper.py` and `acceptance_2b.py` likewise.

A seventh instance was found while applying it: **a cell metric cannot see
over-production.** Changing tcs's option `emit` rule from `referenced` to `all`
adds 86 unorderable options and the cell number does not move, because it only
compares shared keys. Precision is now gated separately.

**Field limits — the KB is wrong and the code is right.** Option and option-group
`Code` is 15, `Name` is 50; the KB says 8 and 25. Enforced at build time, because
an over-length code fails the import outright.

**The option-stack intermediate is not an import file, and §3 should say so.**
The importer reads `options.csv` and `option_groups.csv`; a product references a
group through `OptionSet1..20` INSIDE `products.csv`. There is no slot for a
product-to-group table. The engine now refuses to name that intermediate after
any importer target and warns unless it is prefixed `_INTERMEDIATE`.

**`OptionSet1..20`, not 1..5.** CLAUDE.md was corrected 2026-09-05 (fleet max
20; 30 orgs above 5; 37,803 references above `OptionSet5`). The engine never
capped — slots 13–20 verified — and now refuses out-of-range, because
`OptionSet21` imports as an ignored column and takes a whole axis with it
silently.

**Import semantics belong in §3.** Three of the six file types hard-delete, the
deletes only run on a WARNING-ONLY import, and a single Error row suppresses
them. `mapper.py` prints the mandatory order on every option-stack run.
