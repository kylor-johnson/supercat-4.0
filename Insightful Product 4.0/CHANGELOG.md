# CHANGELOG — Insightful Product 4.0

Dated, human-readable log for canon + structure changes. Newest first.

## 2026-09-16 — Anti-Sarreid send set (Tracks 0–3 / 2.5 wrap)

Owner-accepted send set: sarreid, cci, clc, hfg, ali, da, sca. The factory was a
Sarreid PASS3 clone; everyone else now gets adaptive sections, house/DTC screening
on the decay extract, hero actions from the live list, and honest cross-sell
(including ali `Q-CROSS-SELL` gap 0). **No golden freeze** — `config/golden_set.json`
is not restamped; `./regression.sh` expected-red is accepted.

## 2026-09-15 — Track 2.5 send-blockers (Slot C, identity, same-dealer card, floor copy)

Close the four remaining unsendable defects on hfg/clc/sca/da. No new doctrine.
**No golden freeze. No LIVE SQL edits.**

- **A1 Slot C:** never drop `coaching_narratives` while coaching cards remain. House-card
  screens re-key C by rep identity instead of falling through to the decline-walk
  fallback. Card fallback is slope-aware (`is_real_decline` / grow / cadence-cliff) so a
  grow-row account cannot be told to “walk the top at-risk account.”
- **A2 identity:** one `display_rep_label` for L3, leaderboard, cards, and the call list.
  Agency names on the RS-01 row print even on Tier 1 (BrandJump, not `rep  ` / `rep (1)`).
  Rows with neither name nor number are omitted from named grids.
- **A3 same-dealer card:** hero card is **Same-dealer spend change** (`same_base_lift_pct`).
  §9 uses that label and unit; no “spent −2% more.” NRR `$0.84` sentence is unchanged.
- **A4 floor copy:** quiet+dark sums say **quiet or dark**. “90+ days” only when the count
  is `dark_seats`.

## 2026-09-15 — Track 3 product wrap (Q-CROSS-SELL fill, no new religion)

- **B1:** ali `Q-CROSS-SELL.csv` added to the existing `2026-06-30` cache dir (header-only =
  gap 0). Query executed date-pinned to 2026-06-30 — not live-today — so it matches sibling
  CSVs. Result: every LED FMT 35W anchor dealer already buys ROMA. sarreid/clc already 0;
  cci 184; hfg 1; kal 42. No BACKLOG product queries.
- **B2:** §8 leads with the new-line / YoY finding when that is the story (ali ROMA).
- **B3:** ali Slot D rewritten to the honest depth sentence. Slot A left as the 1-year
  new-line story (no overlap to add at gap 0). Play count unchanged.

## 2026-07-20 — Golden set rebaselined to the 2026-07-16 template voice pass

The `pipeline/templates/*.j2` files were edited 2026-07-16 (voice pass: "doors"→"dealers",
metric-label rewrites). `config/golden_set.json` was still stamped 2026-07-14, so `./regression.sh`
reported 3 deterministic-core FAILs. The diffs are **template copy only — deterministic numbers are
identical**; this was a stale baseline, not a real regression. Rebaselined the golden set to the
2026-07-16 voice pass (`golden_set.json` version 10 → 11, stamped 2026-07-20).

- **cci** (Currey & Company) — core `a28cf92b…` → `cf7fd16c…`, bytes 60694 → 60688
- **clc** (Capital Lighting) — core `dafa48ad…` → `48dda77b…`, bytes 62764 → 62822
- **sarreid** (Sarreid Ltd.) — core `bf31db0d…` → `00e99822…`, bytes 58090 → 58084
- **da** (Dainolite) — unchanged (`c6b7a125…`, 39026); no invoice math, so the copy-only pass
  leaves its deterministic core byte-identical.

`./regression.sh` now reports **GOLDEN SET: PASS (4/4)**. Segment-label leak grep stays 0.
Prior-session baseline backups remain at `/tmp/insightful_golden_baseline/`.

## 2026-07-20 — Client Segmentation v4.0 propagated into profiles (thin consumption layer)

Consume the stamped **Client Segmentation v4.0** (Workstream A — SuperCat's ~109 client orgs
classified by selling motion; `Customer Segmentation/current/`, stamped 2026-07-09) into the
Insightful **interpretation layer only**. This does **not** touch the frozen in-client customer
segmentation (Workstream B / Q-SEG-DERIVE, Spine §8).
**No LIVE SQL edits. No golden re-baseline** (only profile markdown, docs, and the auto-derive
draft doc-string changed; deterministic cores / golden HTML / `config/golden_set.json` checksums
untouched).

### Profiles — §2 stamped (segment + how/what/who axes + continuous price + verified org_id)
- Replaced the incorrect "segmentation is 🧊 FROZEN per Spine §8" **client-segment** wording in
  `sarreid.md`, `cci.md`, `hfg.md`, `kal.md`, `sca.md` — that wording misapplied Spine §8, which
  governs Workstream B (buyer clusters), not the client's stamped selling motion.
- Expanded the one-line "dealer-distribution manufacturer" default in the auto-derived profiles
  `ali.md`, `bri.md`, `da.md`, `bsc.md`, `clc.md` (and drafts `ali.draft.md`, `bri.draft.md`,
  `da.draft.md`) to the full schema.
- Per-org before→after and §3 tensions logged in
  [`handoffs/CLIENT_SEGMENT_V4_PROPAGATION_2026-07-20.md`](handoffs/CLIENT_SEGMENT_V4_PROPAGATION_2026-07-20.md).
- `bmc.md`: org 11 (Bassett Mirror) is **not** on the 109-org roster → §2 marked **unassigned**;
  no segment invented.
- §5 buyer-type framing aligned to the stamped motion on the auto-derived profiles only
  (MMC: don't assume one buyer type / respect channel mix; VD: replenishment + structural
  concentration is not a discovery; PTB: stocking-dealer reorder default). Ratified profiles'
  §5 prose left as-is.

### Template + knowledge + pipeline doc-string
- `profiles/profile_template.md` §2 rewritten to the new schema and explicitly distinguishes
  **Client segment** (Workstream A stamp) from **in-client customer segmentation** (Workstream B,
  frozen, not a profile field).
- `knowledge/industry_context.md`: new section "Selling-motion segments in SuperCat's client book
  (context, not findings)" (after Structural truths, before Vocabulary) — four segments as
  context/not-a-finding; price is a correlate not a classifier; product vertical does not define
  segment; never emit internal segment labels in client-facing copy.
- `pipeline/run_report.py`: the auto-derived profile §2 **draft doc-string** now instructs the
  author to stamp from the v4.0 MASTER (or mark `unassigned`) instead of defaulting every client to
  "dealer-distribution manufacturer." Doc-string only — no query/signal/template/gate changes.

## 2026-07-13 — Client voice pass (templates + prose)

Strip SaaS / machinery language from client-facing report surfaces.
**Golden HTML untouched** — verify against PREVIEW before promoting.

### Templates (`pipeline/templates/`)
- Label dictionary in `_macros.md.j2`; confidence-header copy softened
  (invoice data, not “feed/pipeline”).
- Hero: three operator metric cards; drop lifter/decliner/GMV/contribution proxy.
- Section H2s carry dollars where available (week / team / watchlist).
- Layers / dealers / channels: retention→same-dealer spend; GMV→eCat orders /
  other channels; “lapsed churn”→dealers who lapsed.
- Methodology rewritten: no Preflight posture / Q-ID ledger / surgical footer —
  plain-English appendix only (query IDs stay as Jinja comments for builders).

### Renderer + prose
- `report_render/html_renderer.py`: footer “invoice data” (not ERP feed).
- Sarreid `outputs/sarreid_prose_2026-07-02.json`: removed “Dollar retention”
  phrasing from hero + layer_1 slots.

### Verify
- `outputs/Sarreid_Ltd._CEO_intelligence_report_2026-07-02_PREVIEW.html`
  step10 PASS; visible-text scan clean of GMV / NRR / Q-IDs / surgical /
  dollar retention. Golden `…_2026-07-02.html` checksum unchanged.

## 2026-07-13 — Re-anchor Phases A+B+C+D1

Plan: [`handoffs/REANCHOR_PLAN_2026-07-13.md`](handoffs/REANCHOR_PLAN_2026-07-13.md).
**No LIVE SQL body edits. No intentional golden re-baseline.**

### Phase A — Capability shelf
- Created `foundation/capability/`; moved `value_moment_catalog.md`,
  `vm_runtime_index.md`, `insights_moneymap_SYNTHESIS.md` (+ README).
- Rewrote `CANON.md` governing vs capability tables; reading contract excludes
  `capability/**`.
- Live pointer updates; logged in `_archive/ARCHIVE_LOG.md`.

### Phase B — Spine ↔ runtime reconciliation (doc-only)
- `provenance_spine.md`: **Runtime mapping** callout — factory commerce gate =
  `Q-ECON-00`; `Q-PROV-00` marked doctrinal ancestor / BACKLOG; `FULL` unreachable
  as shipped economics label; §6.1 / §6.8 headers clarified.
- Stale live-path IDs fixed in `report_product/report_product_architecture.md`,
  `signal_catalog_v4.md`, `operators/report_operator.md`,
  `operators/rep_copilot_operator.md` (`Q-PROV-00` / `Q-SELL-QC` / Mixpanel Q-63…
  no longer claimed as factory `QUERIES_ALL`).

### Phase C — Agent path loads the reading contract
- `.cursor/skills/insightful-report-4/SKILL.md`: CANON reading contract 0–4 before
  Step 1; agent must apply industry + voice (API path auto-injects; agent path does not).
- `README.md`: documents v9 Option C Hybrid Prose (deterministic numbers + bounded
  prose slots + deterministic fallback) — replaces “fully templated, no LLM” as
  the only story.

### Phase D1 — Industry downweight honesty
- `WHAT_ACTUALLY_RUNS.md`: table of LIVE vs STUB downweights (`ecat_minority` only LIVE).
- `pipeline/signals.py`: stub branch logs **all** non-`always` conditions (stderr only;
  no ranking change vs prior silent skip for unhandled conditions).

### Known pre-existing (not caused by this re-anchor)
- Owner rejected the 2026-07-13 Sarreid re-run. Restored
  `outputs/Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html` + DRAFT from git
  HEAD; shelved the disliked artifacts under
  `_archive/outputs_noncanonical_2026-07-13/`.
- Working-tree `config/golden_set.json` (v9) still stamps a
  `deterministic_core_sha256` that does **not** match that restored HEAD HTML —
  v9 stamp / `extract_deterministic_core.py` are uncommitted hybrid-prose work.
  Reconcile golden separately; do **not** re-stamp from the rejected run.

---

## 2026-07-13 — Folder cleanup + doc patches (v9 alignment)

**Golden set v9** (Option C Hybrid Prose, split verification: `deterministic_core_sha256`
+ prose conformance + bytes range). 4-org golden roster: `sarreid`, `cci`, `da`, `clc`.

**14th signal detector:** `territory_cluster_decay` (3+ accounts under one rep all in
`real_decline`) added to `pipeline/signals.py` since the v6 golden freeze. All doctrine
docs that said "13 signals" have been patched to say 14.

**Folder cleanup:**

- `build_notes/` (15 files) → `_archive/build_notes_2026-06-29_to_07-09/` (all historical QA)
- `handoffs/` root: 19 closed files → `_archive/handoffs_closed_2026-07-09/`; 5 files with
  open items retained (decision memo, substance review, template reconciliation, MCP cache, README)
- `handoffs/completeness_rollout/`: 8 closed track prompts → `_archive/completeness_rollout_closed/`;
  3 files retained (README, 99_review gate, next_wave_followups)
- `outputs/`: 21 non-golden files → `_archive/outputs_noncanonical_2026-07-09/`; 2 iCloud
  duplicates deleted; golden outputs retained (sarreid/cci @ 07-02, da/clc @ 07-09)
- `report_product/report_product_README.md` → `_archive/report_product_stale/` (still said
  "pipeline not ported")
- `_archive/` root: 8 loose files organized into `_archive/misc_pre-v9/`
- `.DS_Store` files and `.pytest_cache/` deleted

**Doc patches (no runtime changes):**

- `CANON.md`: signal count 13 → 14; removed archived `report_product_README.md` row
- `foundation/WHAT_ACTUALLY_RUNS.md`: signal count 13 → 14; added `territory_cluster_decay`
- `report_product/report_product_architecture.md`: removed "pipeline deferred" (shipped 07-01)
- `report_product/signal_catalog_v4.md`: signal count 13 → 14

---

## 2026-07-09 — 99-review BLOCK close-out: template-honesty fixes + golden re-freeze (sarreid, cci)

The Phase-1 acceptance review (`handoffs/completeness_rollout/99_review_after_E.md`)
returned BLOCK with a specific defect list. Landed exactly those fixes — all
template/label edits that make canned prose match the data; **no §0 guardrail moved,
no new SQL, no new template/mode, no number changed.**

**What was done (5 edits):**

- **`section_06_team.md.j2:105`** — restored the Track-D honesty label the uncommitted
  rep-floor rewrite had reverted: leaderboard YoY `new`→`n/a`, "First-year book — no
  comp yet"→"No prior-year comp available", and restored the RS-01 NOTE comment
  (RS-01 emits no prior-year column, so `yoy_pct` is `none` for every rep — labeling
  that "new" asserts a fact the query never checked).
- **`section_08_products.md.j2`** — added a broad-decline branch before the "steady"
  `{% else %}` so an all-declining family set (e.g. bmc, −35% to −92%) reads as a
  contraction, not "steady — no clear fade."
- **`section_01_hero.md.j2` + `section_03_thismonth.md.j2`** — the hardcoded "roughly
  flat" / "growing modestly" are now contracting-vs-flat aware on the same `−5`
  threshold `section_09_dealers.md.j2` already uses (bmc −62% now reads "contracting").
- **`section_10_channels.md.j2`** — relabeled `Invoiced net (all channels)` →
  `Invoiced business, channel-split basis (all channels)`. That row is Q-CHAN-05's
  `total_business_gmv`, a channel-decomposition total that legitimately differs from
  the canonical §1 invoiced-net topline (cci $70.34M vs $70.02M); the label now names
  the basis so a CEO never sees two "invoiced net" dollars.

**Decision gate (owner-ruled):** the earlier drop of §6 "Customer-level pricing
leakage" (present at `08f5af0`, removed by the rep-floor rewrite) was ruled
**INTENTIONAL** by the owner. Left dropped; recorded here so it is not re-flagged as a
regression in future audits.

**Verify:** all 9 cached orgs (sarreid, cci 07-02 & 07-09, da, bmc, hfg, kal, sca, ali)
SHIP with smoke + step10 [4 8 9 11 12] passing; zero `#}` / `<!--` / `QUERY-NEEDED` in
fresh HTML. Golden re-frozen (v6) for **sarreid + cci** against real disk bytes; the
golden→new delta is label/prose-only with no commercial number moved, and the
`08f5af0`→new sarreid delta contains only intended Track-A/B/C/D additions (the honesty
regression is gone). `./regression.sh`: **sarreid / cci / da GREEN**; hfg/kal/sca/ali
remain collateral-RED (separate Phase-2 re-baseline, out of this scope).

---

## 2026-07-07 — STAMP: Insightful 4.0 factory production-ready

Independent golden-set regression verified (`build_notes/regression_verification_2026-07-07.md`):
`GOLDEN SET: PASS (6/6)` — exit codes, byte counts, and SHA-256 checksums match
`config/golden_set.json` on commit `358396c`. Factory STAMPED.

---

## 2026-07-07 — Ops polish: golden-set regression + output naming + cleanup

Closed the remaining ops items from the 07-02 rails handoff. The factory now has a
checksum-verified golden set and a single canonical output naming contract.

**What was done:**

- **Golden-set regression.** `regression.sh` + `config/golden_set.json` — 6 orgs
  (sarreid/cci/hfg/kal SHIP, sca REDIRECT, ali PREVIEW) pinned to cache dates
  `2026-07-02` / `2026-07-01`. Verifies exit codes, byte counts, and SHA-256.
- **Canonical naming.** `report_render/naming.py` centralizes SHIP/PREVIEW/DRAFT/GATESTOP
  filename rules. `run.sh` and `pipeline/assemble.py` now share the same display-name parser.
- **Output cleanup.** 25 non-canonical or superseded files moved to
  `_archive/outputs_noncanonical_2026-07-07/`. `outputs/` now holds only the Sarreid gold
  pair (06-29), the authoritative 07-02 cohort set, and ali/bri preview artifacts.

**Regression result (local):** `GOLDEN SET: PASS (6/6)`.

**Canon untouched.**

---

## 2026-07-02 — Inference-to-code remediation: pipeline internals hardened

A harness audit (2026-07-01) found that business logic critical to report correctness was implicit
in LLM inference and ad-hoc agent decisions rather than explicit in code. 14 targeted remediation
subagents hardened the `pipeline/` module — extracting configuration, adding schema validation, wiring
typed contexts, adding post-LLM validation, and expanding automated checks. Zero functional changes
to report output; every change moves implicit knowledge into auditable code.

**What was done (7 modules modified, 3 config files created):**

- **Config extraction.** `config.py`: added `QUERY_SCHEMAS` (column-level contracts for 8 gather
  queries, with alias resolution), `load_tier_overrides()` (deadband carry-overs and dormant org
  flags from `config/tier_overrides.json`), `load_house_exclusions()` (machine-readable house-rep
  rules from `config/house_rep_exclusions.json`), and path constants for the three new config files
  (`HOUSE_REP_EXCLUSIONS_JSON`, `TIER_OVERRIDES_JSON`, `PROFILE_SCHEMA_JSON`).

- **Signal weight tables.** `signals.py`: `SIGNAL_WEIGHTS` (editorial surprise × actionability per
  signal kind — 13 entries), `SIGNAL_ARC_ORDER` (narrative arc ordering: momentum → intelligence →
  opportunity → risk), `INDUSTRY_CONTEXT_DOWNWEIGHT` (3 rules: channel concentration, eCat minority,
  cadence cliff — each with a condition and a surprise multiplier grounded in
  `knowledge/industry_context.md`). Nine `TypedDict` context classes (`DeclineContext`,
  `CadenceContext`, `ConcentrationContext`, `RepContext`, `CrossSellContext`, `RetentionContext`,
  `ChannelContext`, `LeakContext`, `EcatContext`) replace untyped dicts in signal `.context` fields.
  New `_apply_industry_downweights()` reduces surprise on signals matching known industry-normal
  patterns rather than suppressing them entirely.

- **Gather-time validation.** `gather.py`: `_validate_columns()` checks that required columns (or
  known aliases from `QUERY_SCHEMAS`) are present in every loaded CSV — logs to stderr, never raises.
  Called by every `load_*` function. `outreach_sort_key()` added per operator §5a.3 (actionability ×
  dollars-at-risk; 30-day-silent decline outranks same-LTM cadence cliff).
  `GatherBundle.outreach_list` is now populated in `gather_all()` — pre-sorted top-7 accounts.

- **Tier-2 deadband override.** `preflight.py` (~line 247): loads `config/tier_overrides.json` and
  applies the Tier-2 deadband hold — if SQL returns Tier 1 but the org is on the declared carry-over
  list (currently: bcf at 81.8%), override to Tier 2. Source: `rep_copilot_operator.md` §1 hysteresis
  band.

- **Post-LLM validation gate.** `narrative.py`: `_validate_hero()` runs three structural checks on
  the LLM output before accepting it: (1) forbidden vocabulary regex (posture, feed, pipeline,
  house-rep, NRR, cohort, playbook), (2) dollar provenance (every $ in the output must appear in the
  prompt facts or signal headlines), (3) structural completeness (multi-paragraph body, summary table,
  priority actions block). If all three structural checks fail, the caller falls back to the template
  placeholder. Warnings are logged but do not block.

- **StrictUndefined wired.** `assemble.py`: the Jinja2 `Environment` now uses `StrictUndefined`
  instead of the default silent-empty behavior. Any typo'd template variable raises at render time
  instead of silently rendering blank.

- **smoke_check expansion.** `smoke_check.py`: expanded from 4 checks to 8. New checks:
  [5] §Q sensitivity-hedge gate (dollar claims in early sections without hedge markers when
  confidence < STRONG), [6] §R concentration-framing mismatch (rejects "broad-based" framing when
  top-1 ≥ 25% or HHI ≥ 1500), [7] §S addressable-base qualifier (growth projections without
  "addressable" / "full base" qualifier), [13] topline parity (cache Q-ECON-00 vs rendered MD
  appendix inv_ltm_net). New CLI args: `--confidence` (commerce confidence level) and `--cache-dir`
  (cache path for parity checks).

**Files created (3):**

| File | Contents |
|---|---|
| `config/house_rep_exclusions.json` | Machine-readable house-rep exclusion rules: `auto_rules` (ILIKE patterns), per-org `exclude` lists keyed by organization_id, `keep_notes` pointer to the .md authority |
| `config/tier_overrides.json` | `tier2_deadband_hold` (bcf 81.8%) and `dormant` org flags (mhc last invoice 2025-12-22) |
| `config/profile_schema.json` | Profile section contract (8 sections: identity through sensitivity, with required fields and required/optional flags) |

**Files modified (7):** `pipeline/config.py`, `pipeline/signals.py`, `pipeline/gather.py`,
`pipeline/preflight.py`, `pipeline/narrative.py`, `pipeline/assemble.py`, `pipeline/smoke_check.py`.

**Canon untouched.** No edits to `CANON.md`, `foundation/`, `knowledge/`, `report_product/`,
`operators/`, or any ratified `profiles/*.md`.

---

## 2026-07-01 — Pipeline completion (Phases 0–6)

The Insightful 4.0 pipeline is now a runnable factory. "Run this for client X" → ship-ready HTML,
deterministic, byte-identical on re-run.

**What shipped:**

- **Phase 0 (Cache):** All 5 cohort orgs (sarreid, cci, hfg, kal, sca) populated with 9 gather
  queries each via MCP. Phase-2 gather queries (Q-PROD-TOP, Q-PROD-FAMILY, Q-DEALER-COHORT) remain
  out of scope (not yet in canon).
- **Phase 1 (Signals):** All 13 `detect_*` rules implemented in `signals.py`. Cohort validation:
  sarreid 11, cci 10, hfg 10, kal 7, sca 0 signals.
- **Phase 2 (Templates):** 11 templates rewritten with editorial voice. `_macros.md.j2` created with
  13 signal-pattern macros, confidence headers, action blocks, §O suppression templates (plain-English,
  §P-compliant).
- **Phase 3 (§1 Hero):** `narrative.py` narrowed to one synthesis sentence, cached at
  `cache/{org}/{date}/hero_synthesis.txt`. Deterministic fallback when no API key.
- **Phase 4 (Run Prompt):** `operators/external/run_prompt.md` and `audit_prompt.md` created.
  End-to-end: pipeline → render → Step-10, validated on cci.
- **Phase 5 (Cohort Validation):** All 5 orgs produce HTML, pass Step-10, and are byte-identical
  on re-run.
- **Phase 6 (Cleanup):** Intermediates archived to `_archive/cohort_2026-06-30/`.
  `html_report_template.html` and `SURGICAL_EDIT_GUIDE.md` archived (surgical edit step eliminated).

**Step-10 results (all PASS):**

| Org | Mode | [4] §P | [8] # recon | [9] phrase | [11] struct | [12] anchors |
|---|---|---|---|---|---|---|
| sarreid | Mode 1 | pass | pass | pass | pass | pass |
| cci | Mode 1 | pass | pass | pass | pass | pass |
| hfg | Mode 1 Tier-1 | pass | pass | pass | pass | pass |
| kal | Mode 1 | pass | pass | pass | pass | pass |
| sca | Mode 2 (Gate-STOP) | n/a | pass | pass | pass | pass |

**Determinism contract satisfied:** same shortname + same cache date + same pipeline commit =
byte-identical output, verified across all 5 orgs.

---

## Older entries (2026-06-29 → 2026-06-30) — archived

The full build-out narrative for the initial 4.0 stand-up (2026-06-29 and
2026-06-30) has been moved to [`CHANGELOG_archive.md`](CHANGELOG_archive.md) to
keep this log lean. See that file for the historical detail.
