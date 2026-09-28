---
name: ecat-onboarding-orchestrator
description: Drive an eCat iPad client onboarding end to end — read the client's state, figure out the current lifecycle phase, route to the correct ecat-* skill, enforce the phase gate, and persist state. Use to start or resume any client onboarding, when asked "what's next" for a client, or when you have a client source file but aren't sure which skill applies.
---

# eCat Onboarding Orchestrator

This is the **controller** for an eCat iPad onboarding. It does not do the build work
itself — it loads client state, determines the phase, hands off to the right `ecat-*`
skill, and refuses to advance a phase until that phase's gate passes.

Always-on rules still apply (`ecat-ground-truth`, `ecat-import-ops`, `ecat-data-model`).
This skill orchestrates; those rules constrain.

## The loop (run this every session)

```
0. SURFACE      → this orchestrator owns the **iPad build** only. Browser catalog / Cart /
                  enrollment / My Account pricing → `ecat-online`. ERP order/invoice
                  reporting → `ecat-sales-portal-onboarding`. iPad runtime behavior →
                  `ecat-ipad-app`. Otherwise continue.
1. LOAD STATE   → read eCat_Onboarding/<Client>/CLIENT_PROFILE.md + HANDOFF.md
2. RECONCILE    → for any client past kickoff, ground the profile against the LIVE DB
                  via ecat-postgres-audit (counts + most-recent import_events). Trust the
                  DB over the markdown; flag and correct any mismatch before proceeding.
3. LOCATE PHASE → match RECONCILED state against the 7 phases below
4. CONFIRM      → state the client, phase, source-of-truth file, and today's task
5. ROUTE        → invoke the skill(s) for this phase (table below)
6. GATE         → run the phase gate (see PHASE_GATES.md). Do NOT advance until it passes.
7. PERSIST      → update CLIENT_PROFILE.md (with reconciled state) + write HANDOFF.md via
                  ecat-session-handoff
```

All client state lives under `eCat_Onboarding/<Client>/` in the **SuperCat 4.0** root
(one repo, one roof). When you invoke `ecat-session-handoff`, point it at this path —
its own doc text may still say `02_Implementation/`; this orchestrator's path wins.

Never skip step 6. The whole point of the orchestrator is that a phase is "done" only
when its gate passes — not when the CSV "looks right."

## Reconcile before you act (the profile lies)

`CLIENT_PROFILE.md` is backfilled by hand and **drifts**. Verified case: Terracotta's
profile said "go-live blocked, 0 customers imported," but the live DB had 346 customers —
the blocker was fixed in a later session that never updated the markdown.

So for any non-new client, before locating the phase:
- Resolve the org and pull live counts + the **most-recent `import_events`** with
  `ecat-postgres-audit`. There is no stored "status" field — derive stage from reality.
- **The live system is the source of truth, not local files.** A client may have run a
  NEWER FTP/Admin import than the last CSV we sent (or after we sent one back), so a local
  `Ready_For_Import/` file can be stale. Check `import_events` (= Admin "File Import
  Status") for what actually loaded and when, then reconcile the profile.
- If the DB and profile disagree, correct the profile as part of PERSIST.

## Source of truth (non-negotiable)

Two different "sources of truth" — don't conflate them:
- **For what we BUILD:** the **latest file the client sent** (older files are reference).
  Working outputs live in `eCat_Onboarding/<Client>/00_Import_Files/Ready_For_Import/`.
- **For what is actually LIVE:** the **database + most-recent `import_events`** (Admin
  "File Import Status"). The client may have imported something newer than our last file,
  so never assume a local CSV reflects the live catalog — verify via `ecat-postgres-audit`.
- Don't invent backup files; keep one `CLIENT_PROFILE.md` and one `HANDOFF.md`.

## New client?

Bootstrap before routing:
1. Copy `eCat_Onboarding/_Template/` → `eCat_Onboarding/<Client>/`.
2. Fill `CLIENT_PROFILE.md` (identity, systems, taxonomy method, pricing, images) — including
   the **Archetype & applicability** section, which the pre-import gate reads. Leaving it as
   template text means every check applies, which is the safe default but hides intentional
   exclusions.
3. Read `<Client>/LESSONS_LEARNED.md` before building — it prevents repeat mistakes.
4. Declare the **source-data cutover date**. Everything before it is POC/demo data and is
   excluded from ground truth. Without one, POC residue keeps re-entering analysis as if it
   were real — `leg`'s 29 pre-cutover options were twice mistaken for a live requirement.
5. Start at Phase 1.

## Phase → skill routing

| Phase | What it covers | Route to | Gate (see PHASE_GATES.md) |
|---|---|---|---|
| 1. Discovery / Kickoff | shortname, contacts, ERP/PIM, pricing model, go-live date | `ecat-client-email` (intake) | G1 |
| 2. Admin pre-flight | tradenames/collections, groups→categories, custom fields, price levels, option types, FTP, flags | `ecat-pricing-levels`, `ecat-options-and-mapping` | G2 |
| 3. Build | products → stories → inventory → customers; options; pricing columns; image naming | `ecat-core-files`, `ecat-customers-build`, `ecat-pricing-levels`, `ecat-options-and-mapping`, `ecat-images-ftp` | G3 |
| 4. Import | correct order, via Tools/Upload or FTP `/data`, File Import Status error-free | `ecat-import-ops` (rule), `ecat-images-ftp` | G4 |
| 5. iPad review | hero images, visible counts, pricing per customer type, related/options/smartlists | `ecat-images-ftp`, `ecat-smartlists`, `ecat-postgres-audit` | G5 |
| 6. Go-live | user groups, price-level visibility, reps + territories, order email, PDF formats | `ecat-go-live` | G6 |
| 7. Maintenance | recurring feeds, image two-step, health/state audits | `ecat-images-ftp`, `ecat-postgres-audit`, `ecat-session-handoff` | G7 |

Sub-task overrides (use even mid-phase when the user asks for one thing):

| Ask | Skill |
|---|---|
| products / stories / inventory build | `ecat-core-files` |
| customers | `ecat-customers-build` |
| pricing / price levels / divisions | `ecat-pricing-levels` |
| options + Option Mapping | `ecat-options-and-mapping` |
| images / FTP / missing images | `ecat-images-ftp` |
| smartlists | `ecat-smartlists` |
| users / reps / territories / go-live | `ecat-go-live` |
| client email / reply | `ecat-client-email` |
| live DB audit | `ecat-postgres-audit` |
| browser catalog / Cart / buyer enrollment / My Account pricing | `ecat-online` |
| Sales Portal build (ERP order/invoice history, portal access) | `ecat-sales-portal-onboarding` |
| iPad runtime behavior / rep-facing diagnosis | `ecat-ipad-app` |
| end of session | `ecat-session-handoff` |

## Import order (Phase 4 — enforce, don't reorder)

`options.csv → option_groups.csv → products.csv → stories.csv → inventory.csv → customers.csv`

Re-send `option_groups.csv` after `options.csv` (importing options nulls group membership).
Only products skip deletes when the file has an `Error` row; every other file deletes omitted records on any non-fatal import. Send
full files — customers/inventory/options HARD-delete omitted records.

## The pre-import gate (run before every upload)

One read-only command over the whole upload set. Nothing in `scripts/` ever writes to a
deliverable or touches the DB.

```bash
python scripts/preflight_gate.py \
    --client-dir eCat_Onboarding/<Client> \
    --dir eCat_Onboarding/<Client>/00_Import_Files/Ready_For_Import \
    --live-state live_<shortname>.json \
    --check-urls --ack-deletes
```

| Exit | Meaning |
|---|---|
| 0 | pass (WARNINGs are advisory) |
| 1 | **blocked** — do not upload |
| 2 | a check could not run (unreadable file, missing input) |

**Live state is passed in, never queried by the script.** A validator is only worth
running if it asserts against an external authority — the client's source file,
code-derived limits, or the live DB — so keeping the DB out makes the gate runnable
anywhere and honest about what it could not confirm. Build the JSON from
`ecat-postgres-audit`:

```json
{
  "shortname": "mali",
  "queried_at": "2026-07-27T20:00:00Z",
  "price_levels": ["dn", "imap"],
  "custom_fields": {"products": ["Color"], "customers": ["BillTo_Region"]},
  "taxonomy": {"codes": ["ML", "LIGHT"], "groups": ["MAIN"]},
  "keys": {"products.csv": ["ML-001"], "customers.csv": ["0099"]},
  "counts": {"products.csv": 683, "customers.csv": 3418},
  "uploaded_images": ["ML-001.jpg"]
}
```

Anything absent degrades to a WARNING naming what went unconfirmed — never to a silent
pass. Without `--live-state` the org-fingerprint, omission, taxonomy, custom-field, and
primary-image checks can only warn, so **supply it before any hard-delete upload**
(`customers.csv`, `inventory.csv`, `options.csv`, `option_groups.csv`, and the pricing
files replace everything and reload).

### What it checks, and why each one is there

| Check | The incident behind it |
|---|---|
| BOM | a fatal "column missing" on a column that is plainly present |
| Org fingerprint | `leg`'s inventory file imported into `mali`, wiping that org's inventory |
| Import-order manifest | groups imported before options at `tcs` and `pebl`, nulling membership |
| Omission preview | "always include ALL products" — an invariant nothing enforced |
| Two-tier lengths | 16 of `pebl`'s 24 option groups rejected at 15 chars |
| Enum + required fields | `tcd`'s 100% customer rejection on `DefaultPriceCode = 0` |
| Cross-file refs | 247 orphan `leg` inventory rows; dangling `RelatedItems` |
| Header ↔ custom-field diff | `leg`'s unregistered fields, live for three months |
| Taxonomy pre-registration | groups never auto-create — real fatals in `mali`'s log |
| Duplicate scan | `pebl`'s `MT_FAROEXT_GR` shipped twice |
| Image URL census | 23 PNG URLs at `tcs`, live for eight weeks |
| Primary-image set diff | `libco`'s catalog off the eOL portal while the iPad looked fine |
| Blank-stays-blank | sibling images invented against an explicit client rule |

### Applicability — a skipped check always says why

Checks are switched off only by a **declared flag** in the client's
`CLIENT_PROFILE.md` "Archetype & applicability" section, and a skipped check prints
`SKIP (flag: options none)`. An **undeclared subsystem stays checked** — that is the safe
default, and it means a half-filled profile can never turn into a silent pass. Only
declare a flag you can cite from a call, an email, or the profile itself.

`snowflake` **annotates; it never blocks.** Nothing in the corpus supports treating an
unusual client as un-automatable.

### Field limits are generated, never typed

Every limit comes from `preflight/limits_generated.py`, derived from `ATTR_LENGTHS` in
`supercat_server` by `scripts/tools/gen_limits.py`. Two tiers, because the importer has
two: `ATTRS_TO_TRUNCATE` fields warn and silently truncate (WARNING), everything else
rejects the row (FAIL).

Do not transcribe a limit from a KB article or from these skills — several documented
numbers are wrong (`LongDesc` is 255 and truncates, not 50; `BaseItemCode` is 40 and is
enforced). `python scripts/preflight_gate.py --claims` prints the documented limits that
are deliberately **not** enforced, with the evidence for each.

## Single-file validators (same checks, one file at a time)

```bash
# Data quality + code inventory (Phase 3 → G3)
python scripts/validate_products.py <Ready_For_Import/products.csv> \
    --custom-fields <registered-fields> --admin-taxonomy <codes> --admin-groups <groups>

# Image integrity (Phase 3/5 → G3/G5)
python scripts/audit_images.py <Ready_For_Import/products.csv> <image_dir> \
    [--max 12] [--live-images uploaded.txt] [--check-urls] [--source client_export.csv]

# Customer file: required fields + the DefaultPriceCode blocker (Phase 3 → G3)
python scripts/validate_customers.py <Ready_For_Import/customers.csv> --price-levels <codes-from-DB>
```

All exit non-zero when there are hard issues, so a gate can branch on the result. The
product validator also prints every unique `CollectionCodes`/`CategoryCodes` value — under
the Standard taxonomy method, create each one in Admin before import (Auto-Create orgs
skip this).

`audit_images.py` reads local disk, which is the **narrowest** of the three image delivery
paths: most clients upload straight to FTP/Admin and never stage images in the repo
(`mali` had 691 live against 17 staged), so a clean local audit proves very little on its
own. Pass `--live-images` for the authoritative check.

## End every session

Update `CLIENT_PROFILE.md` (import history row, open items, current source-of-truth) and
regenerate `HANDOFF.md` via `ecat-session-handoff` so the next session resumes cold.

## Additional resources

- Phase gates / definition-of-done per phase: [PHASE_GATES.md](PHASE_GATES.md)
