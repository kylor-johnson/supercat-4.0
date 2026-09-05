# Build spec — what an eCat ingestion agent must actually do

Derived from the five-client blind audit (`SCORECARD.md`), a live survey of 127
active/onboarding orgs, and a structural read of the ~60 build scripts written to date.
Written 2026-09-03.

**Purpose.** Not "how to write a transformer." This says what the transformer must
*get right*, drawn from things that have actually gone wrong on real clients — so
whoever builds it has a target and an acceptance test instead of a folder of one-offs.

---

## 1. The problem, measured

`~60 scripts. ~15,000 lines. Zero shared modules.`

Every client got a transformer written from scratch. The file names tell the story:

```
fix_import_warnings.py   apply_tuesday_fixes.py   exact_fixes.py
repair_longdesc.py       fix_case_and_categories.py
fix_image_references.py  mer_fixups.py   patch_inventory_qtyavailable.py
```

Repair scripts outnumber builders. The CopperSmith has 14 scripts, Legrand 16.
This is not a pipeline; it is sixty one-offs and a long tail of corrections.

---

## 2. The shared transformer, discovered not invented

The three largest independent builds — `build_ecat_files.py` (Legrand, 1,537 lines),
`rebuild_lib_co_files.py` (libco, 1,277), `rebuild_perfection.py` (tcs, 656) — were
written separately by different passes and **all three reimplement the same twelve
primitives.** That convergence is the evidence for where the shared boundary sits.

| Primitive | Legrand | libco | tcs |
|---|---|---|---|
| Money parsing | `strip_currency` | `strip_money` | `clean_price` |
| Weight parsing | `parse_ship_weight_lb` | `strip_weight` | — |
| Dimension assembly | `build_dimensions` | — | `fmt_dims` |
| Y/N booleans | `to_boolean_y` | `normalize_bool_y_n` | — |
| Date normalisation | `normalize_receipt_date` | `parse_next_receipt_date`, `normalize_intro_date` | — |
| LongDesc truncation | `build_long_desc`, `_truncate_word_boundary` | `truncate_longdesc` | — |
| Text hygiene | `clean_na`, `clean_country`, `clean_category` | `clean_text` | — |
| RelatedItems | `build_related_items` | `_parse_related_items`, `_join_related_items`, `backfill_variant_sibling_related_items` | `merge_related` |
| Variant grouping | `_normalize_variant_key` | `_variant_root` | `size_sort_key` |
| Taxonomy mapping | `write_taxonomy_files` | — | `brand_to_trade_name`, `fixture_to_category` |
| CSV IO | — | `read_csv`, `write_csv` | `load_rows`, `write_rows` |
| Carry-forward | `load_carryforward` | — | — |

**Genuinely client-specific** (and correctly so): `load_us_radiant_prices` /
`load_ca_adorne_prices` (Legrand's four price files), `load_spec_master` (libco's spec
sheet), `stage2_lantern_rebuild` / `stage4_parts_and_kits` / `sku_ignition` (tcs
buildable SKUs), `apply_discontinued_promo` (libco).

### The primitives are shared; the DIALECT is per-client config

**Added 2026-09-04, after the extraction was actually done.** The table above
reads as though extraction were mechanical — same twelve operations, merge them.
**It is not.** The three builds disagree on *output*, not merely on style:

| primitive | Legrand | libco | tcs |
|---|---|---|---|
| money | `4058.00` — always 2dp | `4058` — integer dollars drop the `.00` | passthrough after stripping `$` and `,` |
| boolean | `Y` / `""` | `Yes` / `No` | — |
| weight | unit-aware; `500 g` → `1.102311` | first number found; `500 g` → `500` | — |
| dimensions | `3.5 in H x 2 in W x 1 in L`; `N/A` when empty | — | `18.75"H x 10.5"W`; `""` when empty |

A naive merge therefore **silently rewrites three clients' files**. The correct
design is one shared implementation per primitive with an explicit, named
`dialect` selected per client in config and **never inferred**. That is also what
made the acceptance test possible: `values.LEGRAND` is byte-exact with
`build_ecat_files.py`, so the rebuild can be diffed at all.

The same holds at finer grain — Legrand's `clean_category` does *not* null-map (a
literal `"0"` category stays `"0"`) while `normalize_finish` does. Same
primitive, different null policy, so the policy is a parameter.

**Divergence is evidence, not noise.** Comparing the dialects surfaced a live
defect: libco normalises booleans to `Yes`/`No`, but eCat boolean filters match
only `Y`/`y`/`T`/`t`/digits 1–9. Confirmed live — `Dimmable` (880),
`SlopeCeilingCompatible` (786) and `MotionSensor` (162): **1,828 values across
three registered filter chips that cannot match**, the same shape as leg's 13
empty filter fields in §3.2 B1. A fourth, `Rating`, is registered binary with 907
values that are neither `Yes` nor `No` — a different problem in the same family.

*(libco's weight primitive ignores units, which would be 453× wrong on a gram
value. It does **not** reproduce in libco's data: 915 products, min 1.32, max
392, mean 46.16 lb, zero ≥ 400. Record it as a **code hazard, not a live
defect** — the distinction is the §12 R1 discipline.)*

**The boundary is therefore:** a shared library of the twelve primitives above plus the
field-length and enum rules already generated in `preflight/limits_generated.py`, and a
per-client *source mapping* that says which source column feeds which eCat field. The
mapping is config; everything else is library.

`load_carryforward` deserves special note — it exists in exactly one script but encodes
a rule the `supercat-mcp-access` skill documents as load-bearing: *when regenerating a
file, values the generator cannot derive (`Hideable`, `ImageFileName` for images
uploaded after the last build) must be carried forward by key, or regeneration silently
destroys them.* This belongs in the shared library, not in one client's script.

---

## 3. Acceptance criteria — from real incidents

Every item is a defect that actually happened. Output that cannot pass these is not
finished, regardless of what the import log says.

### 3.1 Fatal — the file must not be produced

| # | Check | Incident |
|---|---|---|
| A1 | **Org fingerprint.** Confirm the file's item codes overlap the target org's existing catalogue before upload. | 2026-08-18: Legrand's 1,020-row `products.csv` imported into `111Mercer`, soft-deleting all 102 of their products. Second occurrence of this failure mode (`leg` → `mali` previously). |
| A2 | **No placeholder pricing reaching production.** Flag when a price level referenced by >50% of customers resolves to a single constant across the catalogue. | `drf`: all 1,627 products at `net_price = 1.00`, all 389 customers pointed at it, for 42+ days. |
| A3 | **Every stored reference resolves.** Price levels, taxonomy codes, related-item targets, image filenames. | `pebl`: 12 orders ($264,130) point at a deleted price level. `mali`: a site pointing at price level 5722, which exists in no organisation; an invite link pointing into org `tcd`. |
| A4 | **Import order enforced**, and `option_groups.csv` re-sent after `options.csv`. | Groups imported before options at `tcs` and `pebl`, nulling membership. **Quantified 2026-09-04** from `import_events`: membership is nulled by an Options import and restored by the next Option Groups import, and the standing state is what counts. Windows where membership was nulled and later restored: `leg` 1 (max 2.6h), `tcs` 42 (avg 69min, max 25.8h), `pebl` 25 (avg 11.4h, max **276.5h** = 11.5 days, 2026-04-10 → 04-22). **Standing violations: 0 in all three**, corroborated in live state — `leg` 11/11, `pebl` 423/423, `tcs` 343/343 option groups carry membership. So this is a recurring-transient problem, not a live defect. |

### 3.2 Blocking — fix before sending to the client

| # | Check | Incident |
|---|---|---|
| B1 | **Registered custom fields must be populated.** A field registered with `send_to_ipad` and used as a filter, carrying zero values, is worse than absent — it ships an empty filter chip. | `leg`: 13 fields warned missing on 2026-07-23, went clean 61 minutes later, and remain empty across all 1,020 products. `# of Gangs` was announced to the client as enabled. |
| B2 | **Image filenames must match.** Compare `ImageFileName` against what is actually on FTP, byte-for-byte. | `pebl`: 18 days of images importing at clean tier with doubled `.jpg.jpg` extensions that could never match. |
| B3 | **Territory codes present** where rep↔customer filtering is expected. Note the empty value is the literal string `[]`, not `''`. | `pebl`: 171/171 emptied on 2026-07-30, filtering off org-wide. |
| B4 | **Recurring feeds must not overwrite each other.** Two files into the same importer hard-delete and reload. | `leg`: adorne and radiant inventory alternating daily; only one brand's stock in the app at a time, on 17 of 23 days. |
| B5 | **The inventory field the org is configured to display must be the one populated** — and *which* field that is must be read from config, never assumed. Both `qty_available` and `qty_on_hand` are used live: `ta`/`tam`/`etl`/`ol` run on-hand only, `cl`/`cf` run available only. | `leg`: reported as a defect on the assumption the iPad reads `qty_available`. **That assumption was false** — SCORECARD § 12 R1. The real rule is config-vs-data agreement, not a fixed field. |
| B6 | **Carry-forward on regeneration.** Diff generated output against the file that produced current live state; the only differences should be intended. | Legrand: a regenerated `products.csv` silently blanked `ImageFileName` on 19 products with live images. **Root cause found 2026-09-04:** `HIDEABLE_CARRYFORWARD_FILE` is a bare relative path, so it resolves against the *current working directory* rather than the script's. Run the build from any other directory and `load_carryforward` returns `{}` and the build continues — carrying nothing forward, reporting nothing wrong. Pass an absolute path, and **return an explicit warning rather than a silent `{}`** (`ecatlib.carryforward.load_carryforward`). |

### 3.3 The rule underneath all of them

**A clean import proves the file parsed. It proves nothing about whether it was right.**

Confirmed independently on three clients: `drf` (18 days of unmatchable images, clean),
`mali` (86 consecutive clean image imports, ~200 wrong photos), `leg` (nine clean
imports, 13 empty announced filters).

**Therefore: the ingestion agent may never treat import success as done.** Acceptance is
a post-import state check against the criteria above, not a log tier.

---

## 4. The configuration profile

`organizations` carries **92 settings columns**, before taxonomies, price levels, user
types, custom fields and report formats. Prevalence across 127 active/onboarding orgs
tells you which are defaults and which are deliberate:

| Setting | On | Reading |
|---|---|---|
| `send_order_email_on_submit` | 121 / 127 (95%) | **Default on.** The six without it are the anomaly — check each. |
| `enable_sales_data` | 97 (76%) | Common default |
| `mobile_enabled` | 67 (53%) | Genuinely per-client |
| `enrollment_enabled` | 57 (45%) | Genuinely per-client |
| `contract_pricing_enabled` | 42 (33%) | Per-client |
| `imports_options` | 34 (27%) | Per-client, follows the options build |
| `product_synch_requires_photo` | 6 (5%) | Rare, deliberate — and it changes what "visible" means |
| `enable_rep_activity` | 4 (3%) | Rare |
| `hide_order_totals` | 2 (1.6%) | Rare |
| `use_modern_ui` | 1 (0.8%) | Effectively unused |
| `enable_data_import3` | **0** | **Dead flag** |
| `enable_image_import2` | **0** | **Dead flag** |

Two more dead fields already found: `import_active` (true for 0 of 257 orgs) and
`enable_data_import3` / `enable_image_import2` above. A config agent should not report
dead flags at all.

**Cross-field contradictions are the real prize.** These are cheap to detect and nothing
checks them today:

- `send_order_email_on_submit = true` **with** `order_email_recipient` empty → `leg` today, `mali` for months
- `product_synch_requires_photo = true` **with** products lacking images → those products silently never reach the iPad
- custom field registered as filter **with** zero populated values → `leg`, 13 of them
- a user group that **deviates from the pattern its peers follow** → `leg`'s `Catalyst` is `shared_resources_auth='a'` with 0 scoped resources while 23 peer agency groups are `'c'` with 96. **Empty groups are NOT a signal** — leg's 24 agency groups are deliberate per-agency Library scoping (SCORECARD § 12 R2). Check conformance to the org's own pattern, never fleet prevalence.
- `ipad_reports` < 3 at go-live → the go-live checklist requires ≥3; `tcd` shipped with 1

---

## 5. What nobody has automated

Ranked by pain relief per unit of effort.

1. **Admin Console configuration.** 92 settings, no checklist, no diff, no record of intent. Manual and forgotten. → the config-check agent.
2. **Post-import state verification.** `preflight_gate.py` validates *before* upload; nothing validates *after*. Every §3 criterion is a post-import check.
3. **Reference integrity.** No check anywhere that a stored id still resolves.
4. **Recurring-feed health.** `leg`'s feed has run 31+ times, every one warning-tier, and nobody reads them.
5. **The three unread sources** — `audit_log_entries` (destructive client actions), `organization_invitations` (self-enrolment), `login_events` (deleted users' history). All three carry events invisible to HelpScout and Fathom.

---

## 6. Build order

| | Agent | State | Why |
|---|---|---|---|
| 1 | **Config check** | ~80% built | Fully specified by §4. Read-only. Smallest. Proves the stack. |
| 2 | **Session prep** | ~80% built | `corpus.py` + `rawstate.py` + the journey format already do it. |
| 3 | **Ingestion** | ~15% built | §2 is the library, §3 is the acceptance test. Biggest, highest value. |
| 4 | **Correspondence** | 0% | Depends on 1–3 being trustworthy. Client-facing, highest risk. Drafts only. |

Build 1 and 2 as `ecat-*` skills in Claude Code, not in eve. eve cannot reach Postgres
(split-horizon DNS), so anything deployed there needs the snapshot bridge built first —
and eve consumes markdown skills natively, so a skill written now ports rather than
being thrown away.
