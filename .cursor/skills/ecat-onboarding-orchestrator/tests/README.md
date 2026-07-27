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

| File | Locks in |
|---|---|
| `test_validate_products.py` | duplicate BaseItemCode, blank required fields, invalid Hideable, missing columns, case-insensitive headers, code inventory printed, long-BaseItemCode advisory warning (not a fail — importer accepts >20 chars) |
| `test_audit_images.py` | missing files, sub-500-byte error pages, the 6/12 image limit, oversized-hero warning (warns, doesn't fail) |
| `test_validate_customers.py` | the tcd `DefaultPriceCode=0`/status blocker, price-level membership (`--price-levels`), missing columns, field-length overflow, bill-to vs ship-to row counting |

Static inputs live in `fixtures/`; image tests build temp dirs/files at runtime.

## The snowflake → fixture loop (read this)

Every client has a one-off quirk. The way nuance gets hardened permanently:

1. A quirk bites a real client.
2. Fix it for the client and record it in their `CLIENT_PROFILE.md` "Snowflake quirks".
3. If it's **generalizable**, promote it to `_Template/LESSONS_LEARNED.md`.
4. Add a row to a fixture (or a new fixture) + an assertion here that proves the scripts
   catch it. Now it can never silently regress.

Each assertion in `test_validate_products.py` already maps 1:1 to a documented entry in
`LESSONS_LEARNED.md`. Keep that mapping intact as the corpus grows.

## Seeding fixtures from a real client

`fixtures/products_clean.csv` and `products_dirty.csv` mirror the real Magic Lite column
set. To add a real-derived fixture, copy a small slice of a client's
`Ready_For_Import/products.csv`, **strip pricing and any PII**, keep ~3–10 rows that
exercise the case you care about, and reference it from a new test.
