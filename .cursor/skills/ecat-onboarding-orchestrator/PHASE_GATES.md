# eCat Onboarding — Phase Gates

A phase is **done** only when its gate passes. The orchestrator must not advance to the
next phase otherwise. Each gate is a hard checklist plus, where possible, a tool/query
that produces objective evidence. Prefer evidence over judgment.

Evidence sources:
- `scripts/preflight_gate.py` — **the pre-import gate**: every Phase 1 check over the whole
  upload set, in one read-only command. Exit 1 blocks the upload; exit 2 means a check could
  not run
- `scripts/validate_products.py` — data quality + code inventory (one file)
- `scripts/audit_images.py` — image integrity (one file)
- `scripts/validate_customers.py` — required fields + the `DefaultPriceCode` blocker
- `ecat-postgres-audit` — live DB counts/state by org shortname; also the source of the
  `--live-state` JSON the gate consumes
- Admin Console **Tools → Admin Reports → File Import Status** — import result tier

Two rules that apply to every gate below:

**A check that did not run is not a pass.** The gate reports three outcomes and no fourth:
FAIL, WARNING, or `SKIP (flag: …)` naming the declared flag that switched it off. When live
state is missing, the affected checks warn and say what went unconfirmed. Reading such a
warning as a pass is how a gate becomes theater.

**Counts are query results with a timestamp, or they do not appear.** Do not type a count
into a gate note, a profile, or a handoff. Terracotta's profile said "0 customers imported"
for months while the org held 346.

---

## G1 — Discovery / Kickoff

- [ ] Org shortname confirmed; Admin Console reachable at `supercatsolutions.com/<SHORTNAME>`
- [ ] Contacts, ERP/PIM, product lines, go-live/event date captured
- [ ] Pricing model + territories understood (NetPrice only | imported levels | arithmetic | divisions)
- [ ] Taxonomy method decided: **Standard** (pre-create codes) vs **Auto-Create**
- [ ] `CLIENT_PROFILE.md` filled in (no `{placeholders}` left in Identity/Systems/Pricing)
- [ ] **Archetype & applicability declared:** archetype, product line(s), applicability flags,
  file owner mode, image mode, source cutover date, sub-brands
- [ ] Every applicability flag is **citable** — a call, a client email, or an explicit statement
  in the profile. An undeclared subsystem stays checked, which is the safe default
- [ ] **File owner mode** decided per deliverable: `generator` (the script owns it and every
  correction is codified in its config) or `csv` (the CSV is the deliverable and the generator
  is retired with a tombstone). **Never two owners for one file** — dual ownership is what
  silently reverted hand-applied fixes at The CopperSmith

**Evidence:** profile has zero unfilled `{...}` tokens in the required sections, and
`preflight_gate.py` prints the client line with no `UNDECLARED` fields and no
`unrecognized flag` warnings.

---

## G2 — Admin Console pre-flight

- [ ] TradeNameCode exists (Standard method)
- [ ] Groups created first, then categories under them (groups never auto-create)
- [ ] Every unique CollectionCode/CategoryCode from the data exists in Admin (Standard method)
- [ ] Custom product/inventory/customer fields registered with "Send to iPad"
- [ ] Price levels created; codes match the `Price_<code>` columns
- [ ] Option types defined (if options)
- [ ] Flags set as needed: Options import, 12-image, country validation
- [ ] FTP credentials confirmed

**Evidence:** run the gate with the live taxonomy supplied, so the reconciliation is
mechanical rather than a manual read-through:

```bash
python scripts/preflight_gate.py --client-dir eCat_Onboarding/<Client> \
    --dir <Ready_For_Import> --live-state live_<shortname>.json
```

Any code not in Admin under the Standard method is a FAIL. `--admin-groups ""` asserts that
Admin has **zero** groups, which is itself a FAIL — categories live under groups and groups
never auto-create, so every category in the file would fail. Registering custom fields is
checked the same way, against `custom_fields` in the live-state JSON.

---

## G3 — Build

- [ ] **`preflight_gate.py` exits 0** over the full upload set, with `--live-state` supplied.
  This subsumes the individual validators below; run those when working one file at a time.
- [ ] No duplicate BaseItemCode, no blank required fields, Hideable ∈ {Y,N}. Long-BaseItemCode
  warnings are advisory, NOT a blocker — the importer's real cap is 40 and 21-char codes are
  live at `mali`.
- [ ] No field over a **hard** length limit. Truncation-tier overflow (`LongDesc`, `ShortDesc`,
  `MediumDesc`, `Features`, `Materials`, `Dimensions`) is a WARNING: the row imports with the
  value cut mid-word, which is survivable but should be a decision, not a surprise.
- [ ] **Images — pick the check that matches the delivery path**, since each is blind to the
  others:
  - *FTP/Admin (most clients):* `--live-state` `uploaded_images` populated, and the
    primary-image diff is clean. **`image_exists` tracks only the FIRST filename** — an
    alternate does not satisfy it, and eOL suppresses imageless products from search.
  - *CDN URLs:* `--check-urls` clean. PNG fails both `CdnImageSync` gates, logs at `:error`,
    and that error tier **also suppresses every delete in the same import**.
  - *Local disk (rare):* `audit_images.py` exits 0. A clean local audit proves little on its
    own — `mali` had 691 images live against 17 staged.
  - Where the client's own file is available, pass `--source`: a SKU blank at source must stay
    blank, and no image may be shared unless the source shares it.
- [ ] stories.csv: one row per product. **There is no 500-character story limit** — `products.story`
  is an unbounded `text` column and the importer sets it verbatim. This gate previously asserted
  500; `leg`'s 442 over-500 rows are fine. Run `preflight_gate.py --claims` for the evidence.
- [ ] `DefaultPriceCode` is a real price level, not `0`/status text — the #1 import blocker. Pass
  the org's actual codes; a plausible-looking value proves nothing on its own.
- [ ] Priced products also have `price_net_price` populated (Net Price mode reads this, not custom levels)
- [ ] Hideable strategy applied: one representative per family `N`, everything else `Y`; all accessories/drivers/controllers `Y`

**Evidence:** `preflight_gate.py` exits 0 and its SKIPPED list contains only checks whose flags
are declared and citable in `CLIENT_PROFILE.md`. If images were staged locally, 5 hero images
also spot-check as product cutouts.

---

## G4 — Import

- [ ] **The gate was run against these exact files and exited 0.** Not a similar earlier
  version — the file being uploaded.
- [ ] **Org fingerprint confirmed** for every hard-delete file: the keys overlap this org's live
  keys, the row count is in tolerance, and the file lives under this client's own build folder.
  A perfectly valid file from the wrong tenant is what replaced `mali`'s inventory with `leg`'s
  1,194 rows, and inventory hard-deletes before it reloads, so there was nothing to undo.
- [ ] Images uploaded BEFORE product import (products.csv references filenames)
- [ ] Import order honored: options → option_groups → products → stories → inventory → customers
- [ ] **option_groups.csv re-sent after options.csv** — importing options nulls every group's
  membership and nothing else restores it. Two passes, not one.
- [ ] Full files sent for customers/inventory/options (omission HARD-deletes). The omission
  preview was reviewed and `--ack-deletes` was a deliberate acknowledgement of a specific
  blast radius, not a reflex to clear a red line.
- [ ] **File Import Status is error-free** — only `Warning`-tier rows, no `Error`/`Fatal`

**Evidence:** File Import Status timestamp is NOT a blue link, or the linked detail shows
zero `Error`/`Fatal` rows.

**The inverted trap:** expected deletes only happen on a clean import. An `Error`-tier row makes
the importer skip *every* delete of an omitted record — so "the deletes didn't happen" is a
symptom of an error row, not of a missing file, and re-sending the file will not fix it. This
compounds: a catalog carrying PNG image URLs (which log at `:error`) is probably also failing to
soft-delete its discontinued products, silently.

---

## G5 — iPad review

- [ ] **Image coverage (authoritative check):** `ecat-postgres-audit` shows `image_exists`
  near the active-product count by shortname — this is the real gate, since most clients'
  images live in FTP/Admin, not on local disk (mali had 691/694 live with only 17 staged locally).
- [ ] Hero image is a product cutout for every visible product (no lifestyle/application as image 1)
- [ ] Visible-product count matches the Hideable plan (not the whole catalog)
- [ ] Prices show correctly per customer type (no $0.00 / blank on priced items)
- [ ] RelatedItems, options, and smartlists resolve on detail pages
- [ ] **Reviewed from a rep's profile, not Admin's.** Admin sees things a rep does not; six of
  nine items escalated at `mali` were Admin-view artifacts rather than defects. Where an org runs
  sub-brands, review once per brand.
- [ ] **Orphaned configuration noted** (not necessarily fixed): options and option groups that
  zero products reference. `leg` carries 29 and `tcd` 222, all unreferenced. This is cleanup
  hygiene and it must **not** be read as evidence that the client needs an options architecture.
- [ ] At least one full review cycle completed; issues logged with screenshots

**Evidence:** `ecat-postgres-audit` confirms visible vs hideable counts and image-match
rate by shortname; reviewer screenshots attached. Budget 2–3 fix/re-import cycles.

---

## G6 — Go-live

- [ ] User groups configured; price-level visibility correct (hide list/net where required)
- [ ] Reps invited; territory codes aligned to customers
- [ ] Order email recipient set
- [ ] ≥ 3 PDF report formats configured
- [ ] Subscription provisioned; training scheduled

**Evidence:** `ecat-go-live` checklist complete; `ecat-postgres-audit` confirms user-group
and distribution-center config.

---

## G7 — Maintenance (recurring)

- [ ] Image two-step run as new photos arrive (upload, then assign). **eCat caches image bytes at
  import; it does not live-render.** The download is conditional on the CDN's last-modified beating
  the stored timestamp, so replacing bytes at the same URL changes nothing until a re-import — use
  a versioned filename (`-v2`) when an image is corrected.
- [ ] Recurring feeds (inventory/pricing) healthy if applicable. **A pre-upload gate does nothing
  for a scheduled feed** — it protects manual FTP pushes only. `libco` syncs hourly from Business
  Central, which no amount of pre-upload checking covers; recurring feeds need post-import
  assertions instead.
- [ ] Org state tracked (health scorecard / Postgres) at the agreed cadence
- [ ] The gate re-run whenever a limit could have moved upstream: `tests/test_gen_limits.py`
  fails if `preflight/limits_generated.py` has drifted from `supercat_server`
- [ ] `HANDOFF.md` updated each session

**Evidence:** latest `ecat-postgres-audit` snapshot stored; HANDOFF reflects current state.
