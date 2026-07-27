# Onboarding script tests

Regression harness for the deterministic core of the onboarding agent — the validation
and image-audit scripts the phase gates rely on. The judgment/routing layer is tested
separately (scenario evals); this folder covers the parts that have a single correct
answer.

## Run

```bash
cd ".cursor/skills/ecat-onboarding-orchestrator"
python3 -m pytest tests -q
```

(If `pytest` isn't installed: `python3 -m pip install pytest`.)

## What's covered

The three validator files test through the **CLI**, which is the contract an operator
uses. The `preflight` files test by **import**, so a failure message stays specific
enough to act on. Both matter.

| File | Locks in |
|---|---|
| `test_validate_products.py` | duplicate BaseItemCode, blank required fields, invalid Hideable, missing columns, case-insensitive headers, code inventory printed, long-BaseItemCode advisory warning (not a fail — importer accepts >20 chars), BOM, two-tier lengths, duplicate UPC, unregistered columns, taxonomy pre-registration, dangling `RelatedItems` |
| `test_audit_images.py` | missing files, sub-500-byte error pages, the 6/12 image limit, oversized-hero warning (warns, doesn't fail), URLs not treated as local files, PNG/share-link URLs, primary-image set diff against the org, blank-stays-blank |
| `test_validate_customers.py` | the tcd `DefaultPriceCode=0`/status blocker, price-level membership (`--price-levels`), missing columns, field-length overflow, bill-to vs ship-to row counting, BOM, the 15-vs-20 `BillToCode` advisory tier, Pebl's 55-char `Terms`, duplicate `BillToCode` |
| `test_preflight_gate.py` | the gate CLI: exit codes, `SKIP (flag: …)`, live-state wiring, `--ack-deletes`, the org-fingerprint and import-order blocks, `--claims` |
| `test_preflight_core.py` | severity tiers and exit codes, case-insensitive headers, BOM detection vs. BOM-tolerant parsing |
| `test_preflight_limits.py` | the truncate-vs-error split, provenance in every message, the advisory tier, retired claims |
| `test_preflight_flags.py` | archetype/flag parsing, "undeclared means checked", template placeholders disabling nothing, **and every real client profile** |
| `test_preflight_files.py` | delete semantics per file, canonical order, filename classification |
| `test_checks_data.py` | bom, dupes, cross-file refs, custom-field diff, taxonomy, enums |
| `test_checks_org.py` | org fingerprint, omission preview, import-order manifest |
| `test_checks_images.py` | URL census (network stubbed), primary-image diff, blank-stays-blank |
| `test_gen_limits.py` | the committed limit table is not stale vs. supercat_server |

Static inputs live in `fixtures/`; image tests build temp dirs/files at runtime. The
network is never touched: the URL census's HEAD path is exercised with a stubbed request.

## Two invariants worth stating outright

**Every check has exactly three outcomes, and "absent" is not one of them.** It FAILs,
it WARNs, or it SKIPs with the flag that caused the skip. A check that cannot confirm
something warns and names what went unconfirmed. Several tests here exist only to prove
a check did not quietly disappear — `test_without_a_profile_nothing_is_skipped` and
`test_template_placeholders_never_disable_a_check` are the load-bearing ones.

**Tier assertions beat value assertions.** Tests assert *what the importer does* with a
bad row (rejects it vs. truncates it), not the specific limit. The numbers come from
`tools/gen_limits.py`; hard-coding one in a test would recreate the transcription bug the
generator exists to prevent. `test_gen_limits.py` catches drift instead.

## The snowflake → fixture loop (read this)

Every client has a one-off quirk. The way nuance gets hardened permanently:

1. A quirk bites a real client.
2. Fix it for the client and record it in their `CLIENT_PROFILE.md` "Snowflake quirks".
3. If it's **generalizable**, promote it to `_Template/LESSONS_LEARNED.md`.
4. Add a row to a fixture (or a new fixture) + an assertion here that proves the scripts
   catch it. Now it can never silently regress.

Each assertion in `test_validate_products.py` already maps 1:1 to a documented entry in
`LESSONS_LEARNED.md`. Keep that mapping intact as the corpus grows.

For the Phase 1 checks the same loop applies, with one addition: **name the incident in
the test.** Every check in `preflight/checks/` exists because something specific went
wrong, and a test that says *why* survives a refactor that a test named
`test_check_returns_findings` does not. The incidents currently pinned:

| Incident | Test |
|---|---|
| `tcd` — 100% customer rejection on `DefaultPriceCode = 0` | `test_placeholder_price_codes_are_caught_offline` |
| `mali` — inventory wiped by importing `leg`'s file | `test_foreign_file_blocks_on_a_hard_delete_file` |
| `libco` — 9 products off the eOL portal, iPad fine | `test_missing_primary_blocks_and_explains_the_portal_symptom` |
| `pebl` — 16 of 24 option groups rejected at 15 chars | `test_erroring_field_blocks` |
| `pebl` — all 171 customer rows rejected on lengths | `test_terms_is_covered_now`, `test_long_address_blocks` |
| `tcs`/`pebl` — groups imported before options | `test_groups_scheduled_before_options_blocks` |
| `tcs` — 23 PNG URLs live for eight weeks | `test_png_url_is_reported_with_both_gates_it_fails` |
| `libco` — a BOM reported as a missing column | `test_bom_is_reported_with_the_fatal_it_will_produce` |
| `leg` — 24 KB of orphan inventory warnings | `test_orphan_inventory_row_blocks` |
| `leg` — unregistered custom fields, three months running | `test_unknown_column_blocks_and_says_the_data_is_dropped` |

## Seeding fixtures from a real client

`fixtures/products_clean.csv` and `products_dirty.csv` mirror the real Magic Lite column
set. To add a real-derived fixture, copy a small slice of a client's
`Ready_For_Import/products.csv`, **strip pricing and any PII**, keep ~3–10 rows that
exercise the case you care about, and reference it from a new test.
