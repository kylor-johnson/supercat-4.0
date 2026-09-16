# CHANGELOG (archive) — Insightful Product 4.0

> Resolved-incident / build-out narrative from the 2026-06-29 → 2026-06-30 stand-up
> of the 4.0 factory, moved out of `CHANGELOG.md` (Scope B doctrine trim,
> 2026-07-09) to keep the live changelog lean. History only — nothing here is a
> current gate. The lean, maintainer-facing log lives in `CHANGELOG.md`.

---

## 2026-06-30 (night) — Phase 4 complete: Task A (renderer fixes) + Task B (§P source-MD patches) + Task C (ali.draft smoke-test)

Closed all three Phase 4 tasks from the handoff (`Downloads/insightful_4.0_phase4_handoff_2026-06-30.md`).
All 5 cohort outputs now pass the full Step-10 ledger on items [4 8 9 11 12].

**Final Step-10 ledger (all PASS):**

| Output | [4] §P | [8] # recon | [9] phrase echo | [11] struct | [12] anchors |
|---|---|---|---|---|---|
| Sarreid (regenerated) | **pass** (post-patch) | pass | pass | pass | pass |
| cci | pass | pass | pass | pass | pass |
| hfg | pass | pass | pass | pass | pass |
| kal | **pass** (post-patch) | pass | pass | pass | pass |
| sca (Gate-STOP) | n/a (relaxed §5b) | pass | pass | pass | pass |

---

### Task A — Renderer heuristic fixes (5 corrections in `sections.py`)

Closed Task A of the Phase 4 handoff (`Downloads/insightful_4.0_phase4_handoff_2026-06-30.md`).
Ran the structural eye-check of the 5 generated HTMLs against the Sarreid gold
(`outputs/Sarreid_CEO_intelligence_report_2026-06-29.html`). Step-10 ledger results
are unchanged (same PASS/FAIL state as Phase 3). Five renderer heuristic regressions
identified and fixed in `report_render/sections.py`.

**What was fixed (all in `report_render/sections.py`):**

1. **`_enrich_title` applied consistently to all section h2 headings.** All section
   renderers (`render_growth`, `render_team`, `render_risk`, `render_products`,
   `render_base`, `render_channels`) were using `md_inline_to_html(chunk.heading)`
   directly, which left ` — ` (em-dash) separators in the rendered h2 titles. Now
   all call `_enrich_title`, converting ` — ` → ` · ` uniformly (matching the
   Sarreid gold standard).

2. **`_enrich_title` applied to h3 subsection titles.** `_render_subsection_section`
   and `render_team` were using `md_inline_to_html(title)` for the `<h3
   class="subsection-title">` elements. Changed to `_enrich_title(title)`, so all
   H3-derived subsection titles (e.g. Growth engine layer labels) now use ` · ` as
   separator.

3. **`_BOLD_SECTION_LEAD` soft-boundary feature implemented in
   `_render_subsection_section`.** The no-H3 branch previously always fell through to
   flat `_render_freeform_blocks`. Now detects `**Bold text with colon:**` standalone
   paragraphs as soft subsection boundaries, wrapping each in a
   `<div class="subsection">` with an `<h3 class="subsection-title">`. Restores "eCat
   as a channel" h3 in `#channels` for Sarreid and cci.

4. **Bold-colon → h3 in `_render_methodology_body`.** Added `_BOLD_SECTION_LEAD`
   detection before the `upgrade_match` check. Restores "Two specific upgrades worth
   queuing" as an `<h3 class="subsection-title">` in the `#methodology` section for
   all Mode-1 reports (Sarreid, cci, hfg, kal).

5. **`render_methodology` gaps-chunk h3 uses prefix-only title.** Previously passed
   `gaps_chunk.heading` verbatim (e.g. "What this report can't see — and what to add
   next") to the h3, making it longer than the gold's "What this report can't see".
   Now uses `_split_heading_prefix` (new helper) to take only the portion before
   ` — `, matching the gold.

**New helper added:** `_split_heading_prefix(heading)` — returns the portion before
the first ` — ` / ` – ` separator, falling back to the full heading if no separator
is found. Used for methodology h3 context where the suffix belongs in the h2, not
the h3 label.

**Five HTML outputs re-rendered** (determinism: same MD + same profile + updated
renderer commit → consistent output). Byte counts shifted slightly from Phase 3
values due to the heuristic changes; new authoritative sizes:

| Output | Bytes | Mode |
|---|---|---|
| `Sarreid_CEO_intelligence_report_regenerated_2026-06-30.html` | 59,756 | 1 |
| `Currey_and_Company_CEO_intelligence_report_2026-06-30.html` | 85,233 | 1 |
| `Hubbardton_Forge_CEO_intelligence_report_2026-06-30.html` | 91,116 | 1 |
| `Kalco_Lighting_CEO_intelligence_report_2026-06-30.html` | 90,364 | 1 |
| `Shadow_Catchers_CEO_intelligence_report_2026-06-30.html` | 57,220 | 2 (Gate-STOP) |

**Step-10 ledger — unchanged from Phase 3:**

| Output | [4] §P | [8] # recon | [9] phrase echo | [11] struct | [12] anchors |
|---|---|---|---|---|---|
| Sarreid (canary regen) | 2 inherited | pass | pass | pass | pass |
| cci | **pass** | pass | pass | pass | pass |
| hfg | **pass** | pass | pass | pass | pass |
| kal | 1 inherited | pass | pass | pass | pass |
| sca (Gate-STOP) | n/a (relaxed per §5b) | pass | pass | pass | pass |

**Documented acceptable deviations (not renderer defects):**

- Various h2 subtitle wording differs from gold (MD heading wording vs gold's
  hand-crafted subtitles — e.g. "The growth engine · three layers, all real" vs
  gold's "Growth engine · 3 layers, all real").
- "Buyer cadence segments" h3 absent from `#base` — no H3 or bold-colon lead in the
  Sarreid dealer-base MD; title was hand-inserted into the gold.
- "Channel mix (LTM, booked orders)" h3 absent from `#channels` — the gold derived
  this from the table header with an editorial "mix" suffix; not auto-reproducible.
- Row 7 of Sarreid call list: `row-danger` (heuristic: −79%) vs gold `row-warn`
  (editorial: position-based urgency cap). Same heuristic limitation as the
  risk-watchlist tinting (documented in Phase 3 as by-design).
- Risk watchlist tinting: deterministic 40%/20% threshold produces more `row-danger`
  rows than gold's editorial judgment — documented as by-design since Phase 3.

**Canon untouched.** No edits to `CANON.md`, `report_product/*`, `operators/*`,
`foundation/*`, `knowledge/*`, or any ratified `profiles/*.md`.

---

### Task B — §P source-MD patches (3 surgical prose swaps)

User-authorized edits to the two source MDs carrying inherited §P violations.
Two files touched; all changes are minimal, like-for-like §P substitutions per the
spec's own substitute table (§P.1.A and §P.1.C).

| MD | Section | Old text | New text | Rule |
|---|---|---|---|---|
| `outputs/Sarreid_CEO_intelligence_report_2026-06-29.md` | §6 Team | `a discount problem this run` | `a discount problem in this analysis` | §P.1.C process-language ban |
| `outputs/Sarreid_CEO_intelligence_report_2026-06-29.md` | §11 Methodology | `**Single-feed posture.**` | `**One feed of your business.**` | §P.1.C system-phrase ban |
| `outputs/kal_PASS3_intelligence_report_2026-06-30.md` | §9 Dealer base | `first-timer cohort` | `first-timer group` | §P.1.A retention-context ban |

**Ledger lines updated in each patched MD:**

- Sarreid: no existing STEP-10 LEDGER line (predates format) → added post-patch LEDGER
  line `4:pass-on-re-sweep` + `[POST-REVIEW PATCH · sarreid · 2026-06-30 · §P.1.C sweep]`
- kal: LEDGER `4:pass` → `4:pass-on-re-sweep` + `[POST-REVIEW PATCH · kal · 2026-06-30 · §P.1.A sweep]`

Both HTMLs re-rendered and Step-10 re-run. All 5 cohort outputs now pass [4].

**Authoritative byte counts post Task B re-render:**

| Output | Bytes |
|---|---|
| `Sarreid_CEO_intelligence_report_regenerated_2026-06-30.html` | 60,289 |
| `Kalco_Lighting_CEO_intelligence_report_2026-06-30.html` | 90,702 |

---

### Task C — ali.draft smoke-test

Rendered `outputs/Access_Lighting_CEO_intelligence_report_2026-06-17.md` with
`profiles/ali.draft.md` as a stress-test of renderer robustness against a
non-ratified profile that doesn't follow the canonical H1 convention.

**Output:** `outputs/Access_Lighting_CEO_intelligence_report_2026-06-30_regenerated.html`
(46,414 bytes). **Not promoted to the cohort.** Do NOT treat as a deliverable — smoke-test only.

**Robustness findings:**

- Renderer handled the non-standard `ali.draft.md` H1 without error (org name
  extraction succeeded via the robust profile-parsing path in `html_renderer.py`).
- Produced valid HTML: correct `<details>` pairing, no duplicate IDs, no broken
  structure (Step-10 [11] and [12] pass).
- The ali MD (2026-06-17) uses pre-canonical section headings (`§2 — Team Performance`
  instead of the 13-section layout). Sections without a canonical match fall through
  to the `#misc-*` fallback path correctly; no content is lost.
- **Step-10 [4] §P**: FAIL — 19 hits across `eCat`, `Rung-4`, `this run`,
  `customer_bill_to_number`, `house-rep`, `YoY`, `Q-ECON-00`, `Q-ECON-LEAK`,
  `Q-CHAN-00`, `order_origin`. All expected — this MD predates §P by ~6 weeks.
  These are source-MD lints, not renderer defects.

**Do NOT** promote `ali.draft.md` → `ali.md` — that requires a separate Phase-2-style
ratification pass (§8 questions + gutcheck + profile sign-off), which is out of scope.

---

## 2026-06-30 (evening) — Phase 3: HTML render pipeline + Step-10 HTML checker

Closed Phase 3 of the post-cohort plan (handoff
`Downloads/insightful_4.0_phase3_handoff_2026-06-30.md`). Stood up a
deterministic `report_render/` Python module that converts a ratified profile
plus a PASS3 MD into a Sarreid-quality HTML, and built the companion Step-10
checker that closes ledger items **4 / 8 / 9 / 11 / 12** (the HTML-only checks
deferred during the MD-only Phase 1). Five HTMLs generated; cohort outputs run
through the ledger.

**Files added (10):**

1. **`report_render/README.md`** — module overview, CLI, Step-10 closure table.
2. **`report_render/__init__.py`** — package marker.
3. **`report_render/templates/report.html.j2`** — Jinja2 template carrying the
   verbatim Sarreid CSS palette + sticky-TOC JS + collapsible-section JS;
   placeholders for org name, subtitle, period line, TOC links, summary block,
   body block, footer text, and footer-ledger code lines.
4. **`report_render/md_parse.py`** — chunks the MD by `##` H2, classifies each
   chunk into a canonical section id (`summary` / `thisweek` / `thismonth` /
   `growth` / `team` / `risk` / `products` / `base` / `channels` /
   `methodology_*` / `appendix` / Mode-2 ids), detects Mode-1 vs Mode-2
   Gate-STOP, and lifts footer code-line ledgers verbatim.
5. **`report_render/md_render.py`** — `markdown-it-py` wrapper configured for
   GFM tables + soft-breaks-to-space.
6. **`report_render/sections.py`** — chunk-to-HTML transformers for every
   canonical section: hero / metric cards / CEO callouts / priorities / call
   list with row tinting / play cards / coaching cards / subsection-titled
   layouts / channels / methodology / appendix / Gate-STOP preflights +
   concentration + patch register.
7. **`report_render/html_renderer.py`** — CLI entry point; loads profile basics
   (robustly parses the H1 of any `profiles/{org}.md`), derives header
   metadata, assembles either Mode-1 or Gate-STOP body, renders the template.
8. **`report_render/step10_check.py`** — Step-10 ledger checker for items
   4 / 8 / 9 / 11 / 12 (§P forbidden-vocab sweep, HTML↔MD number
   reconciliation, 12-word verbatim phrase echo, structure pairing + id
   uniqueness, anchor resolution).
9. **`.venv-renderer/`** — Python 3.14 virtualenv with `markdown-it-py`,
   `jinja2`, `beautifulsoup4`, `lxml` pinned. (Not committed; recreate via
   `python3.14 -m venv .venv-renderer && .venv-renderer/bin/pip install
   markdown-it-py jinja2 beautifulsoup4 lxml`.)
10. **`CHANGELOG.md`** — this entry.

**Files generated (5):**

| Output | MD source | Profile | Bytes | Mode |
|---|---|---|---|---|
| `outputs/Sarreid_CEO_intelligence_report_regenerated_2026-06-30.html` | `Sarreid_CEO_intelligence_report_2026-06-29.md` | `sarreid.md` | 59,686 | 1 |
| `outputs/Currey_and_Company_CEO_intelligence_report_2026-06-30.html` | `cci_PASS3_intelligence_report_2026-06-30.md` | `cci.md` | 85,156 | 1 |
| `outputs/Hubbardton_Forge_CEO_intelligence_report_2026-06-30.html` | `hfg_PASS3_intelligence_report_2026-06-30.md` | `hfg.md` | 91,024 | 1 |
| `outputs/Kalco_Lighting_CEO_intelligence_report_2026-06-30.html` | `kal_PASS3_intelligence_report_2026-06-30.md` | `kal.md` | 90,265 | 1 |
| `outputs/Shadow_Catchers_CEO_intelligence_report_2026-06-30.html` | `sca_PASS3_intelligence_report_2026-06-30.md` | `sca.md` | 57,220 | 2 (Gate-STOP) |

**Step-10 ledger results (items 4 / 8 / 9 / 11 / 12):**

| Output | [4] §P | [8] # recon | [9] phrase echo | [11] struct | [12] anchors |
|---|---|---|---|---|---|
| Sarreid (canary regen) | 2 inherited | pass | pass | pass | pass |
| cci | **pass** | pass | pass | pass | pass |
| hfg | **pass** | pass | pass | pass | pass |
| kal | 1 inherited | pass | pass | pass | pass |
| sca (Gate-STOP) | n/a (relaxed per §5b) | pass | pass | pass | pass |

**Inherited §P findings (real source-MD lints, NOT renderer defects):**

The MD inputs are immutable per the Phase 3 contract; these are the checker
honestly surfacing leaks that an upstream pass over the source MDs should fix:

- **Sarreid MD (pre-§P canary):**
  - §6 Team — `this run` × 2 (process-language leak; §P.1.C)
  - §11 Methodology — `single-feed posture` × 2 (substitute per §P.1.C:
    *"one feed of your business"*)
- **kal MD (post-§P but mis-graded):**
  - §9 Dealer base — `cohort` × 1 in *"first-timer cohort returned at 25.4%"*.
    §P.1.A bans `cohort` in retention contexts; substitute *"first-timer
    group"* or *"first-timer base"*.

**Determinism contract.** Same MD + same profile + same renderer commit
produces byte-identical HTML. The template is verbatim Sarreid (CSS + JS);
the only sources of variance are the inputs and the section-mapping
heuristics in `sections.py` (pure functions of the MD source — no clock,
no entropy).

**Canon untouched.** No edits to `CANON.md`, `report_product/*`,
`operators/*`, `foundation/*`, `knowledge/*`, or any ratified `profiles/*.md`.

---

## 2026-06-30 (late PM) — Phase 2: cohort profile ratification — 4 of 4 cohort drafts → ratified

Closed Phase 2 of the post-cohort plan (handoff `Downloads/insightful_4.0_handoff_2026-06-30.md` §6). All
four cohort draft profiles (cci / kal / hfg / sca) were walked through their §8 ratifier-questions blocks
and renamed from `{org}.draft.md` → `{org}.md`. Five profiles are now ratified (Sarreid + the four cohort
orgs); only `ali.draft.md` remains (out of cohort scope).

**Ratifier decisions, by org:**

| Org | §8 decision | Resolution |
|---|---|---|
| **cci** | E-commerce / marketplace cluster — `cluster_section` vs `individual`? | **`cluster_section`** with a revisit-after-first-client-run flag. The §6-listed 11-account marketplace book renders as one named channel with its own §3 decision block + §10 channels block. Per-account auto-rule defaults stand (none ≥20% top-1). |
| **kal** | Online-dealer cluster — `cluster_section` vs `individual`? | **`individual`** (auto-rule holds). kal's `Q-CHAN-00 = NONE` means a `cluster_section` override could not produce a real §10 channel block; PASS3's existing **routing-question** framing (the house-routed-book play that asks "who covers these 72 accounts?") is the correct framing, and a dedicated cluster §3 block would duplicate it. Documented as **differs from cci** because cci has a populated origin tag and kal doesn't. |
| **hfg** | 5 open questions | (1) **Illuminating Expressions = Unknown** — PASS3's go-investigate framing holds (the §1/§3/§5 sub-section all stand). (2) **E-commerce cluster = `individual`** — matches kal for the same `Q-CHAN-00 = NONE` reason. (3) **HF DTC + Internal exclusions confirmed** (Handmade In Vermont.com 10505, Shop Hubbardton Forge 35639, six HF Internal codes). (4) **NENOREP = Unknown, exclusion held** (top accounts are the DTC sites + HF Internal regardless). (5) **Rep-bridge gap = investigation item, not a profile decision** (profile stays Tier-1 degraded until backfilled). Tier-2 carry-over decision **deferred** to canon-level `rep_copilot_operator.md` §1 work (handoff §7 Phase 5). |
| **sca** | eCat-only by design vs connector gap? | **Structurally eCat-only by design** — verified via three independent live-data signals: (a) `subscriptions` row for org 90 → `subscription_plans.name = 'eCat iPad'` (active monthly since 2025-08-26); (b) `portal_invoices` / `portal_orders` / `sales_data` = **0 rows ever** for organization_id 90 since creation 2015-05-05 (lifetime, not just LTM); (c) Pricing Migration brief classifies sca as **T1 Catalog Essentials** ("the rep iPad app and your buyer-facing catalog"). Mode-2 lock updated from "until ERP feed arrives" → **permanent on current product configuration**. Re-ratify only if Shadow Catchers upgrades to a tier that ships the ERP integration AND `portal_invoices` begins to populate. |

**Standing leakage gut-check** (per `foundation/provenance_spine.md` §6.10) **held for all four ratifications:**
no leadership-facing dollar in any of the four PASS3 outputs was authored against an account the ratified
policy screens out (vacuously held on sca — no invoice feed exists against which a leakage finding could be
authored).

**Files touched (5):**

1. **[`profiles/cci.md`](profiles/cci.md)** — renamed from `cci.draft.md`; §8 cluster question resolved
   (`cluster_section`, revisit clause); Status header updated to RATIFIED; ratification log entry added.
2. **[`profiles/kal.md`](profiles/kal.md)** — renamed from `kal.draft.md`; §8 cluster question resolved
   (`individual` / auto-rule holds); differs-from-cci rationale documented; ratification log entry added.
3. **[`profiles/hfg.md`](profiles/hfg.md)** — renamed from `hfg.draft.md`; five §8 open questions resolved
   in a "Ratified resolutions" block (1–5 above); Tier-2 carry-over deferral noted; ratification log entry
   added.
4. **[`profiles/sca.md`](profiles/sca.md)** — renamed from `sca.draft.md`; load-bearing structural question
   resolved as eCat-only by design (with three-signal verification trail); §7 Mode-2 lock upgraded from
   "until feed arrives" → permanent on current product configuration; ratification log entry added.
5. **[`CHANGELOG.md`](CHANGELOG.md)** — this entry.

**Net result:** all four cohort PASS3 outputs are now ratification-cleared (subject to any user's own
gut-check on the rendered output). The next concrete moves available per handoff §7 are Phase 3 (HTML shell
port from the Sarreid gold-standard) and Phase 4 (Python render pipeline). Phase 5 (Tier-2 carry-over list
refresh — whether hfg at 79.3% deadband should be added to `rep_copilot_operator.md` §1) remains an open
canon-level decision separate from the four profile ratifications.

---

## 2026-06-30 (PM) — Phase-1.5 cohort-cold-run absorption: 6 canon refinements + hfg post-review patch

Closed the gap between the **morning gold-stamp absorption** (the entry below) and the **afternoon cohort
cold re-run findings** across cci / hfg / kal / sca. The cohort surfaced one new render-time defect class
that the morning Phase-0 absorption did not catch (the **Tier-fallback identifier leak** — DB column names
substituted for unrenderable names when `REP_IDENTITY_TIER < 2`), one canon gap (§O templates dilute the
consultant-voice when expanded as terse render-time fillers), and four smaller refinements that the worked
cohort outputs surfaced as gold-bar nuances. This entry absorbs all six **before** the next cohort run or
the Python pipeline port — so the next worked example ships gold-bar by construction.

**Cohort context (4 PASS3 outputs reviewed):**

| Org | Gate state | Audit verdict |
|---|---|---|
| **cci** | Mode-1 STRONG · Tier-2 | Post-review patched 18:14 (3 §P prose swaps); clean after patch |
| **hfg** | Mode-1 Tier-1 degraded · `Q-CHAN-00=NONE` | 7 `rep_number` Tier-fallback leaks (§P miss class), 1 §N.7 paraphrase (canon gap, not runner defect) — **patched in this entry** |
| **kal** | Mode-1 STRONG · Tier-2 · `Q-CHAN-00=NONE` | Cleanest output of the 4; canary lessons applied verbatim; house book surfaced as a Tier-A finding (gold pattern) |
| **sca** | Mode-2 Gate-STOP · `COMMERCE_CONFIDENCE=NONE` · Tier-0 | Textbook Gate-STOP; §5b.2 + §5b.3 verbatim; §5b.3 user-grain rule fires (user 7435 = 88.5%) |

**Files touched (4 canon + 1 output + this CHANGELOG = 6 total):**

1. **[`report_product/report_editorial_rules_v4.md`](report_product/report_editorial_rules_v4.md)** — 4 surgical refinements:
   - **§P.1.C — Tier-fallback identifier leak ban.** Added `rep_number` / `rep_name` / `rep_label` /
     `bill_to_number` / `ship_to_number` / `item_number` / `customer_num` / `customer_bill_to_number` /
     `org_user_id` / `net_amount` / `order_origin` etc. as explicit banned tokens with `rep code` /
     `customer code` / `item code` / `SKU` as the plain-English substitutes. Also added compound
     `<col> → <col>` arrow phrases (e.g. `rep_number → rep_name`) and `feed posture` / `single-feed
     posture` as bans (cci canary lesson). New load-bearing paragraph names the "Tier-fallback identifier
     leak" pattern hfg surfaced (7 hits across §1/§2/§3/§5/§6/§11) and provides the substitution rule.
     §P.2 allow-list updated so DB column names survive only in the Appendix Traceability footer.
   - **§O.6 — Narrative-form expansion permitted.** Closes the hfg §N.7 paraphrase gap. The §O.1–§O.5
     terse templates may be expanded into a narrative-form consultant-voice block **provided** (a) the
     gate state is named verbatim, (b) the operational fix is given inline, (c) the verbatim canonical
     footer line is present. The hfg PASS3 §6 "Coaching cards — held back in this report" block is the
     worked example. §N.7 enforcement updates: passes when **either** terse template emitted verbatim
     **or** the three §O.6 conditions all met.
   - **§R.6 — Polarity symmetry (loss-direction also covered).** §R.1–§R.5 were authored around the
     Sarreid "broad-based +29% growth" misframing; §R.6 extends the same trigger set and the same
     top-1 / top-10 / HHI thresholds to the loss direction ("broad-based decline" / "broadly spread
     churn" / "the broad middle is fading" / "it's everywhere"). Canonical loss-direction replacement
     template provided. Symmetry rationale: a CEO planning around "everyone is fading a little"
     deploys differently than one planning around "five accounts walked out the door." cci cohort lesson.
   - **§Q.4 — Collective hedging permitted on table-format claim lists.** When Tier-A/S claims are
     rendered as rows in a single table (§2 7-row call list, §6 5-card coaching layer, §3 plays table,
     §7 watchlist tail), a single collective hedge below the table satisfies §Q **provided** (a) the
     hedge addresses the underlying systemic uncertainty class that applies across all rows, (b) it
     sits within ±400 chars of the last row, (c) the table itself carries the "two-conversations"
     split when rows represent two distinct call-shape patterns. Worked examples cited from cci / hfg /
     kal §2 call lists. §Q.3 enforcement updates: passes on per-row OR collective form.

2. **[`report_product/report_product_architecture.md`](report_product/report_product_architecture.md)** —
   **§5a.1 position 10 single-vs-split nuance.** Position 10 may render as one combined section (the
   Sarreid pattern: §11 "What this report can't see / how to trust these numbers" as a single block)
   OR as two sequential sections (the cci / hfg / kal pattern: §11 + §12 split). Threshold rule:
   split if either subsection runs >200 words on rendered MD. Both forms are gold-bar; the position
   count stays at 10 either way (second section becomes position 10b); footer remains position 11.
   §5a.5 "6-item honest list, one sentence each" invariant preserved across both forms.

3. **[`foundation/provenance_spine.md`](foundation/provenance_spine.md)** — **§7.1 Tier-0 enumeration:
   add sca.** The Tier-0 list was `ufi, heb, kll, lpf` (4 orgs with `rep_number ≈ 0%` on populated
   invoice feeds). sca is the **structural feed-absence** variant — 0 `portal_invoices` rows at all,
   so the rule is vacuously satisfied. Tier-0 condition updated to "invoice `rep_number ≈ 0%` (no key
   at all) **OR** zero invoice rows entirely (structural feed absence)." Cohort summary table on
   line 219 also updated to acknowledge the 4 + 1 split. Closes sca PASS2 §C.4 register item.

4. **[`outputs/hfg_PASS3_intelligence_report_2026-06-30.md`](outputs/hfg_PASS3_intelligence_report_2026-06-30.md)** —
   **post-review patch (7 surgical prose swaps).** The cohort cold re-run produced a PASS3 with the
   `[STEP-10 LEDGER]` line claiming all gates `pass`, but the cohort audit found 7 §P misses in
   customer-facing copy (§1 callout #3, §2 intro, §3 Play 3 main body, §3 Play 3 blockquote, §5
   Layer 3 intro, §6 leaderboard table, §11 methodology) — every one a Tier-1 fallback substituting
   `rep_number` for the unrenderable rep name. All seven patched in place: `rep_number` → "rep code" /
   "rep-code-to-rep-name." Appendix Trace lines retain `rep_number` as a real DB column referent per
   §P.2 internal-provenance allow-list. Ledger updated `3:pass → 3:pass-on-re-sweep`; a
   `[POST-REVIEW PATCH · hfg · ...]` annotation added to the footer for auditability. The §11 §P
   sweep-result self-documentation rewritten to acknowledge the new defect class and queue the canon
   refinement that closes it (item 1 above).

5. **`CHANGELOG.md`** — this entry.

**Closes (Phase-1.5 register):**

- **cci canary lesson #1–#3** *(closed at 2026-06-30 18:14 in cci post-review patch — pre-existing)*: the
  `Single-feed posture` / `house-rep screen` / `in this pipeline` prose pattern. Encoded as §P bans
  with plain-English substitutes ("one feed of your business" / "the house-routed accounts" / "in
  this data feed").
- **hfg cohort lesson #1** *(closed in §P.1.C update)*: the `rep_number` Tier-fallback identifier
  leak class — DB column names substituted for unrenderable names. 11 DB column names + the column-arrow
  compound pattern now explicitly banned with plain-English substitutes.
- **hfg cohort lesson #2** *(closed in §O.6 update)*: the §O terse-template-vs-narrative-voice tension.
  Narrative expansion permitted under three named conditions; hfg PASS3 §6 cited as worked example.
- **cci cohort lesson — concentration polarity** *(closed in §R.6 update)*: §R was authored around
  growth-direction misframing; loss-direction now covered symmetrically with the same thresholds.
- **cci cohort lesson — collective hedging on tables** *(closed in §Q.4 update)*: tables of Tier-A/S
  claims may carry one collective hedge below the table rather than per-row.
- **cohort lesson — §5a position 10 nuance** *(closed in §5a.1 update)*: combined or split rendering
  of position 10 is both gold-bar.
- **sca PASS2 §C.4 register item** *(closed in Spine §7.1 update)*: sca added to Tier-0 enumeration
  as the structural feed-absence variant.

**Does NOT close (still open):**

- Phase-2 ratification of the 4 cohort draft profiles (`profiles/cci.draft.md` / `profiles/hfg.draft.md` /
  `profiles/kal.draft.md` / `profiles/sca.draft.md`). All 4 PASS3 outputs ran under `--cohort-validation`
  override; none are client-ready until the human ratifier signs off on the draft profile §8 questions.
- HTML shell port (§5a.1 layout) — ledger items 8 / 9 / 11 / 12 (HTML number reconciliation, HTML
  phrase echo, HTML structure pairing, in-document anchor resolution) stay DEFERRED until the port
  lands. The MD outputs are the worked examples.
- Python pipeline port (the §N / §O / §P / §Q / §R / §S gates currently run by-agent against canon
  text; the deterministic regex pipeline that runs them at Step 10 lives in the deferred
  `report_operator.py`).

**Implementation note (for the pipeline port).** Every gate refinement above is authored as a regex- or
threshold-deterministic check; the morning Phase-0 absorption + this Phase-1.5 absorption together give
the pipeline implementer the full check set. The 4 cohort PASS3 outputs (cci patched, hfg patched, kal
clean, sca Gate-STOP) are the canonical end-to-end test cases for the pipeline: one Mode-1 STRONG with
the cci canary lesson encoded, one Mode-1 Tier-1 degraded with the hfg Tier-fallback leak encoded,
one Mode-1 STRONG with all gates passing on the first try, one Mode-2 Gate-STOP with the §5b.3
user-grain rule firing.

---

## 2026-06-30 — Gold-stamp absorption: §P/§Q/§R/§S editorial gates + 13-check verification ledger + 13-section pinned layout + `sensitive_callouts` profile policy

Closed the gap between the Sarreid CEO Brief gold-stamp standard (set by an independent surgical-audit agent on
2026-06-30) and the canon, **before** the cohort cold re-run. Pre-patch state: the qa-lessons doc
([`build_notes/report_product_qa_lessons_sarreid_2026-06-30.md`](build_notes/report_product_qa_lessons_sarreid_2026-06-30.md))
named the 10 systemic findings but only operational fixes for some had been encoded (`§N.1–§N.7` PASS1 patch,
`§O` suppression templates). The handoff (`build_notes/sarreid_gold_stamp_handoff_2026-06-30.md` — written
externally, kept for reference) spelled the rest out as render-time gates. This entry absorbs the un-encoded
specifics so the next 4 cohort outputs (cci / kal / hfg / sca cold re-run) ship gold-bar **by construction**,
not by per-output surgical pass.

**Files touched (6 — exactly the canon surfaces the absorption requires; zero outputs touched):**

1. **[`report_product/report_editorial_rules_v4.md`](report_product/report_editorial_rules_v4.md)** — appended
   four new render-time gates after `§O`:
   - **`§P` Forbidden-vocabulary regex sweep** *(HALT)* — supersedes the small §A1 "use instead" table with a
     comprehensive hard fail-list (NRR / cohort / playbook / new logos / ICP / TAM / motion / GTM / north-star /
     internal codes `S1`/`C2`/`K7`/`VM-*`/`Q-ECON-*` / `FEED_COMPLETENESS` / `COMMERCE_CONFIDENCE` / `TIER-N`
     raw labels / DB table names `portal_invoices`/`portal_orders` / paths `config/` `operators/` `foundation/` /
     internal product names `Insightful`/`SuperCat` / any `2.0`/`3.0`/`4.0` version number / `preflight` /
     `the operator` etc.). Per-token allow-list per context (e.g. `eCat` in §10 channels only; `AOV` in furniture
     context only). HALT on hit — the operator does NOT silently substitute.
   - **`§Q` Sensitivity-hedge gate** *(HALT)* — every Tier-A/S claim (§1 findings, CEO-callouts, §2 call list,
     §3 plays, §6 coaching cards, Priority Actions) must carry one of N marker-phrase sensitivities within
     ±400 chars (*"what would change this read"*, *"worth pressure-testing"*, *"if X, the addressable Y"*,
     *"loosening/tightening the rule would"*, etc.). The hedge is the load-bearing voice move that makes the
     report read consultant-briefing vs dashboard-explanation; HALT forces it to be authored, not auto-templated.
   - **`§R` Concentration-check gate** *(HALT + REPLACE)* — closes qa-lessons Finding 1. Any "broad-based" /
     "spread" / "diversified" framing fails if top-1 ≥ 25% **OR** top-10 ≥ 40% **OR** HHI ≥ 1500 on the
     underlying $-lift; canonical "concentrated in the top N" replacement template provided verbatim. The
     Sarreid same-dealer +29% misframing (top-10 = 94.9% of lift; WAYFAIR alone 65%) is now impossible to
     ship on any client. The probe is mandatory at preflight.
   - **`§S` Addressable-base rule** *(DELETE via §N.5)* — every "+$X per N-pt move" claim must carry an
     addressable-base footnote OR a full-vs-addressable range; else DELETE under the §N.5 untraceable-arithmetic
     rule. Closes qa-lessons Finding 8.
   - **Render-time enforcement contract** updated at the bottom to enumerate all 11 gates in firing order
     (§N.1–§N.7 + §P/§Q/§R/§S).

2. **[`operators/report_operator.md`](operators/report_operator.md)** — Step 10 rewritten as **the verification
   ledger (13 checks)** (consolidates the PASS1 §N gate set with the gold-stamp §P/§Q/§R/§S adds and adds
   five operationally-new structural / numerical / live-parity checks: number reconciliation across the per-run
   key-numbers list (HTML ↔ MD), verbatim 12-word phrase echo sweep × 2 (HTML + MD), HTML structure pairing
   + unique-`id` check, in-document anchor-link resolution, **topline live-query parity re-pull** (re-run
   `Q-ECON-00` for `{ORG_ID}` and compare LTM invoiced $/YoY/dealer count against gather output — catches
   hand-edited or stale headlines)). Per-run ledger pass/fail summary appended to the Appendix Traceability
   block as a greppable `[STEP-10 LEDGER · ...]` line so cohort cold-run state is auditable across outputs.
   Relationship-to-canon table updated so the editorial-rules pointer names §P/§Q/§R/§S.

3. **[`report_product/report_product_architecture.md`](report_product/report_product_architecture.md)** — new
   **§5a "Rendered client-facing structure — the gold-standard layout"** pins the **13-section CEO-facing
   layout** the Sarreid HTML settled (Header → Sticky TOC → §1 60-second read → §2 Do this week → §3 Do this
   month → §5 Growth engine → §6 The team → §7 Full risk watchlist → §8 Product intelligence → §9 Dealer
   base → §10 Channels → §11 What this report can't see → Footer); cites
   `outputs/Sarreid_CEO_intelligence_report_2026-06-29.html` as the layout authority. Internal-structure
   subsections lock the constraint counts (§1 = 4 metric cards + 3 CEO-callouts + priorities-by-cadence; §2 =
   7-row call list + "How these were chosen" nested disclosure; §6 = 5 coaching cards; §11 = 6-item honest
   list). New **"don't break these"** invariants table lists the CSS palette (DM Sans + IBM Plex Mono,
   `#C47A4A` orange-warm, 4 semantic states), the `<details>` + sticky-TOC JS, and the section-size locks —
   the spec the Python pipeline / HTML shell port must template against.

4. **[`knowledge/communication_guideline.md`](knowledge/communication_guideline.md)** — added **"The bar"**
   as a sister test to "The one test that governs everything": *"A senior furniture-industry consultant
   wrote this for a furniture CEO. If any sentence reads like a SaaS analyst, a CRO, a revenue-ops PM, or
   an internal engineer wrote it — fix it."* The read-through is the consultant-briefing-vs-dashboard
   question; the §N/§P/§Q/§R/§S gates catch the worst leaks, the bar catches the rest.

5. **[`profiles/profile_template.md`](profiles/profile_template.md)** — added **§8 Sensitive callouts —
   per-client scrubbing policy**. Automatic top-1-share rule (≥20% → `full_section`; 5–20% → `body`;
   <5% → `exclude_only`) computed from `Q-ECON-CONC` at preflight; per-account override table for the
   rare human-ratifier exception; cascade rule (when a callout is toggled out, every downstream reference
   drops or auto-substitutes in the same render pass — closes qa-lessons Finding 7 orphaned-hero-hedge).
   Profile policy keeps the Wayfair-style "which surface renders this account" decision at the *facts/scope*
   layer (per the profiles `README.md` allowed/forbidden rule), not in the body of the run.

6. **`CHANGELOG.md`** — this entry.

**Explicit non-touches:** no outputs touched (Sarreid pair stays as shipped; the §R gate prevents recurrence
on the next client — owner decision 2026-06-30 against shipping an addendum). The 4 cohort PASS1/PASS2
outputs (`outputs/{cci,kal,hfg,sca}_PASS{1,2}_intelligence_report_2026-06-30.md`) are unchanged. No SQL
body changed, no per-org quirk touched, no Spine gate logic re-authored. The frozen Insightful Product 2.0 /
3.0 trees are not touched. The legacy `html_report_template.html` at root is not yet retired — the new shell
spec at §5a now points the pipeline port at the Sarreid HTML as the source-of-truth body/CSS/JS to lift
verbatim; the legacy file stays parked until the port begins.

**Next agent: cold cohort re-run.** Run `report_operator.md` against cci / kal / hfg / sca with
`--cohort-validation` (per their current draft-profile state) on the patched operators + the Phase-0 gates
added in this entry. The Step-10 ledger HALT lines are the structural enforcement — outputs that pass all
13 checks are gold-bar by construction. Sarreid Finding-1 hotfix stays not-shipped per the 2026-06-30
owner decision (no addendums); the §R gate is the prevention going forward.

## 2026-06-30 — VM catalog: restored the dual-value spine ("why valuable to client / why valuable to SuperCat")

Addressed value drift introduced during the v4.1/v4.2 compression: the original catalog's **Customer Value /
SuperCat Value** framing had been replaced by `Decision & Dollar` / `Who pays` and dropped from the VM bodies,
even though the "How to Read" schema still promised it. Restored without touching any gate, claim, or provenance.

1. **A one-line `Client value` · `SuperCat value` pair added to every functional VM** (87 VMs across all 13
   domains) — grounded in the original `04_value_moment_catalog` text for the legacy 1–50 VMs and derived from
   the existing Decision/Who-pays content for the 4.0-era C/CHAN/K/R/S families. Inserted under the `Audience`
   line (long-form VMs) or inline before `Decision & Dollar` (compressed economics/customer/rep VMs).
   Intentionally skipped: the frozen **VM-K5**, internal-rule **VM-K-HEALTH** / **VM-R-FUSION**, and the
   **R-PROMPTS** / **S/C-ROADMAP** shells.
2. **`How to Read` schema corrected** — the `Customer Value` / `SuperCat Value` rows now read `Client value` /
   `SuperCat value` and state the line is present on every VM (matching reality, not an unkept promise).
3. **Genre separation** — the two older reconciliation callouts (v4.1 re-gating + v3 provenance) were collapsed
   into a single `<details>` expander so the value content leads; the live v4.2 note still sits at the top, and
   the full governance trail is preserved (collapsed), not deleted. No anchors changed.

## 2026-06-30 — VM menu fully runnable: 8 economics queries + Q-48 authored & live-validated

Closed the last `pending_query` gap so `foundation/vm_runtime_index.md` is runnable end-to-end. All new SQL
inherits the `Q-ECON-00` denominator/clamp and was live-smoke-tested before shipping.

1. **8 economics queries authored** into `foundation/query_library_v2.md` Domain 10, each validated on **cci
   (org 161, RTD 2026-06-26)**: `Q-ECON-CONC` (VM-C3, HHI 54), `Q-ECON-QUALITY` (VM-C7, 94% recurring),
   `Q-ECON-SEASON` (VM-C8, Q4-heavy curve), `Q-ECON-PACE` (VM-C9, pacing-band inputs — never a point),
   `Q-ECON-MOMENTUM` (VM-C10, +5.2% YoY on equal RTD-anchored windows), `Q-ECON-LUMP` (VM-C11, Gini 0.532),
   `Q-ECON-NRR` (VM-C17, 88% dollar NRR), `Q-ECON-CONTRIB` (VM-C20, contribution proxy — **not** margin).
2. **`Q-48` (HubSpot Expansion Signals, internal-only)** authored against BigQuery `hubspot.*` and validated on
   **cfg** (2 open "Exp. Tier 3" deals, stage "Qualifying", 10% win prob). Join key is
   `company.properties_org_id` = SuperCat **shortname** (populated for 177 of 20,070 companies); the company-level
   `hs_last_sales_activity_date` is a corrupted load (epoch→1970) so deal-level recency is used instead.
3. **Reconciliation updated** — `value_moment_catalog.md` Query-ID Reconciliation table flips VM-C3/C7/C8/C9/
   C10/C11/C17/C20 + VM-48 to ✅ live; the only economics rows still gated are cost-gated VM-C19/C21/C25
   (`unit_cost` hard gap). `vm_runtime_index.md` `pending_query` count is now **0** (those 9 rows → `conditional`),
   `active`+`conditional` = **78 runnable**.

## 2026-06-30 — Operator/spine patch: tier-bridge hysteresis, S1 severity cadence-floor, Step-0 profile-gate override

Three targeted fixes in the operators/spine; no reports regenerated, no validation re-run, none of the
2026-06-30 PASS1-patched surfaces (house screen, Step 5a wiring, Mode-2/Gate-STOP, §N/§O editorial) or any
one-off org quirk touched. Cold re-run is the next agent's job.

1. **TIER-BRIDGE HYSTERESIS** — `foundation/provenance_spine.md` §7.1 and `operators/rep_copilot_operator.md`
   §1 (RP-2 SQL + cohort tier map + carry-over list): the rep-identity Tier-2 boundary is now a band — promote
   at `name_bridge_pct ≥ 82%`, demote out of Tier 2 only below 78%, deadband 78–82% defaults to Tier 1 unless
   the org is on the declared Tier-2 carry-over list (today: `bcf` 81.8%). hfg's 79.3% → 81.0% feed wobble now
   returns Tier 1 in both runs (stable); bcf stays Tier 2 via the application-layer hold.

2. **S1 SEVERITY THRESHOLD** — `foundation/selling_customer_exception_layer.md` Exception S1 SQL: CRITICAL
   cadence-side trigger changed from `silent > 2 × mean_gap` to `silent > GREATEST(14, 4 × mean_gap)`, scaled
   to the account's own reorder rhythm with a 14-day absolute floor so a 590-invoice daily-cadence book stops
   tripping CRITICAL on ~1.5 days of silence. The WARNING WHERE clause (2× mean_gap) is unchanged — the account
   still surfaces, only the CRITICAL framing waits for material silence.

3. **STEP-0 PROFILE GATE — explicit `--cohort-validation` override** — `operators/report_operator.md` Step 0:
   missing/DRAFT profile = HARD STOP (default, unchanged); the new `--cohort-validation` flag permits an
   inline-draft profile for PASS1/PASS2/cohort runs, tags the run header verbatim as `INLINE DRAFT
   (cohort-validation override)`, writes the draft to `profiles/{org}.draft.md`, and appends a greppable
   `[STEP-0 OVERRIDE · {org} · {ts} · profile=INLINE-DRAFT · --cohort-validation]` line into the appendix
   Traceability block. The flag only relaxes the missing-profile gate; every other Step 5b.2 hard preflight
   still STOPs as before. Past PASS1/PASS2 outputs were operating inside this newly-explicit exception path.

**Files touched (5 — exactly the operators/spine surfaces of the three fixes, plus two cross-reference
sentences in `query_library_v2.md` that restated the now-banded rule):**
- `foundation/provenance_spine.md` — §7.1 tier table + hysteresis-band paragraph + the §7.1 "Rule" line
  threshold reference (Fix 1)
- `operators/rep_copilot_operator.md` — §1 RP-2 SQL `>=80` → `>=82`, hysteresis preamble, cohort tier map +
  declared carry-over list, bcf hardcoded-flag note (Fix 1)
- `foundation/query_library_v2.md` — two cross-reference sentences in the Q-70 Tier-gate notes (the
  "≥80%" pointer to Spine §7.1) updated to mirror the new band; no SQL body changed (Fix 1)
- `foundation/selling_customer_exception_layer.md` — S1 SQL CRITICAL severity expression + one prose
  paragraph documenting the cadence-floor (Fix 2)
- `operators/report_operator.md` — Step 0 order-of-operations diagram line + the `--cohort-validation`
  exception block, header template, and logging contract (Fix 3)

**Explicit non-touches:** none of the 16 PASS1 patched surfaces, no per-org quirks (hfg 0.7pp Tier-1 miss,
sca self-purchase, kal 254-customer buyer gap, any NRR<100% read), no `query_library_v2.md` SQL bodies, no
report regeneration, no validation rerun, no consolidation/refactor. The cci/kal/hfg/sca PASS1+PASS2 outputs
are unchanged; a cold re-run against the patched operators is the next agent's job.

## 2026-06-30 — PASS1 cohort patch: 5 operator surfaces (cci / kal / hfg / sca defect registers)

Cold validation across 4 orgs (cci, kal, hfg, sca) on 2026-06-30 surfaced 16 systemic defects concentrated
in 5 operator surfaces. This patch fixes those 5 in the operators/config so they propagate to all orgs.
**No reports regenerated; no one-off org-data quirks touched; no canon outside the 5 listed surfaces
modified. The cold re-run is a separate agent.**

**The 5 fixes (one line per fix; defect-register entries closed in parens):**

1. **RS-01 HOUSE SCREEN — wired `config/house_rep_exclusions.md` + AUTO-RULE into every rep-grain query that
   renders `rep_label`.** Added an `AUTO-RULE` section to `config/house_rep_exclusions.md` (`rep_label ILIKE
   'house%' OR ILIKE '% house account%'` fires on every org, regardless of EXCLUDE-table presence) and baked
   the two-layer screen (auto-rule + per-org EXCLUDE list) into `rep_copilot_operator.md` §3 RS-01 SQL and
   `rung4_option_a_operator.md` §2 O1/O2 SQL — house-rep rows are dropped at the `HAVING` clause, not after
   render. Closes cci §C.1, cci §E.1, kal §C.1, kal §C.2, kal §D.3 (HOUSE ACCOUNT at #1 leaderboard /
   $695K-at-risk-on-rep-0999 / cross-org house-handling inconsistency).

2. **STEP 5a PER-ENTITY OPERATORS RUNNABLE — report now CALLS and CONSUMES, with explicit scope guard.**
   Added §5a.0 "Invocation contract" to `report_operator.md` enumerating the 5 sequential operator
   invocations (preflight → RS-01 → rung-4 O1/O2 → v5.1 mini-brief → S1 outreach seed) and a "Scope guard
   — STOP if you are rebuilding" subsection naming the 4 symptoms of a 5a interface failure. **This is an
   INTERFACE fix only — no operator-layer redesign.** Closes cci §C.2, cci §C.7, kal §C.3, kal §C.7
   (rung-4 not actually called / v5.1 reconstructed inline / outreach list built by hand).

3. **MODE-2 / TIER-0 TEMPLATE + GATE-STOP ARTIFACT — authored the missing canon for NONE-feed and gate-failed
   orgs.** New `report_operator.md` §5b: §5b.1 mode resolution table; §5b.2 the Gate-STOP artifact format
   (verbatim shape, used by hfg/sca PASS1); §5b.3 the Mode-2 (Activation / NONE-feed) template with the
   formal redirect text to `rep_copilot_operator.md` and the user-grain concentration rule (>80% single
   `org_user_id` = structural-concentration finding, the sca rule). Closes hfg §C.1, hfg §C.2, sca §C.1,
   sca §C.2, sca §C.3, sca §E.2.

4. **EDITORIAL ENFORCEMENT AT RENDER — added §N to `report_editorial_rules_v4.md` with 7 deterministic
   render-time checks**, wired into `report_operator.md` Step 10. The checks: §N.1 `HOUSE-LEAK` (HALT),
   §N.2 `FM9-CHANNEL-LEAD` (DELETE — banned "What it is" narration phrases), §N.3 `CROSS-ORG-LEAK`
   (DELETE — literal "Sarreid"/"cci"/etc. in customer copy), §N.4 `CUTE-METAPHOR` (DELETE — "engine"
   banned outright + banned-metaphor list), §N.5 `UNTRACEABLE-ARITHMETIC` (DELETE — the "$X per 5pt" /
   "estimated $X" sensitivity arithmetic with no Trace line, which Step 10 was supposed to delete but
   wasn't), §N.6 `VISUAL-CUE` (DELETE emoji/glyphs), §N.7 `CHANNEL-NONE-SUPPRESSION` (REPLACE with §O
   canonical templates). Closes cci §A.4, cci §B.1, cci §B.2, cci §B.4, cci §B.5, cci §E.5, kal §A.4,
   kal §B.1, kal §B.3, kal §B.4, kal §B.5.

5. **Q-CHAN-00 NONE SUPPRESSION TEMPLATE — authored canonical §O suppression templates** in
   `report_editorial_rules_v4.md`: §O.1 Q-CHAN-00 = NONE, §O.2 Q-CHAN-00 = PARTIAL, §O.3
   `COMMERCE_CONFIDENCE = NONE`, §O.4 `REP_IDENTITY_TIER < 2`, §O.5 `FEED_COMPLETENESS = STALE / DEAD`.
   Validators emit these verbatim; §N.7 enforces it at render time. Cross-referenced from
   `report_operator.md` Step 1 (Q-CHAN-00 emit) and Step 6 (section rendering). Closes kal §C.8 and
   hfg §C.2 (no standard suppression text → every validator wrote different wording).

**Hard guards honored:** Fix only the 5 surfaces; no one-off org-data quirks touched (hfg's 0.7pp Tier-1
miss, sca's self-purchase data, kal's NRR<100% finding, any org's data gaps); no reports regenerated; no
validation re-run; no canon outside the 5 surfaces modified; no consolidation/refactor/renumbering;
no invented numbers or findings.

**Files touched (5):**
- `config/house_rep_exclusions.md` — added AUTO-RULE section + canonical SQL fragment (Fix 1)
- `operators/rep_copilot_operator.md` — RS-01 §3 SQL: two-layer house screen + render-rule note (Fix 1)
- `operators/rung4_option_a_operator.md` — O1/O2 §2 SQL: two-layer house screen; §3 G-B + §8 status
  updated to reflect baked-in screen (Fix 1)
- `operators/report_operator.md` — Step 1 / Step 5 / Step 6 / Step 10 cross-references to §N/§O; new
  Step 5a.0 invocation contract + scope guard (Fix 2); new Step 5b mode resolution + gate-STOP
  template + Mode-2 redirect (Fix 3); Step 10 wired to §N.1–§N.7 (Fix 4); relationship table now
  names `config/house_rep_exclusions.md` (Fix 1) and §N/§O of the editorial rules (Fixes 4 & 5)
- `report_product/report_editorial_rules_v4.md` — new §N (7 render-time checks, Fix 4) + new §O (5
  canonical suppression templates, Fix 5)

**Closes 16 of the cohort's 16 systemic defect-register entries.** One-off org-data findings (e.g.
hfg's 0.7pp Tier-1 miss, sca's "Shadow Catchers buying from Shadow Catchers", kal's 254-customer
buyer-frequency gap, any org's NRR<100% read) remain in their respective registers and are explicitly
NOT addressed by this patch — they belong in per-org tuning, not the canon.

**Next agent: cold re-run.** This patch does NOT regenerate any output. The 4 PASS1 reports
(`outputs/{cci,kal,hfg,sca}_PASS1_intelligence_report_2026-06-30.md`) are unchanged. A cold re-run
against the patched operators is the next agent's job.

## 2026-06-30 — VM catalog v4.2: grounded + compressed + uniform ("holy grail" pass)

Took the value-moment catalog from "v4.1 + two grounding probes" to a **fully data-proven, uniformly compressed,
LLM-loadable** state. Scope was locked to **format + accuracy + finish-grounding** — **no net-new VMs** (untapped
Mixpanel-depth / HubSpot / Clicky / freight expansion deferred by owner choice). Live file:
[`foundation/value_moment_catalog.md`](foundation/value_moment_catalog.md) (now **2,019 lines / 183,128 bytes**, down
from the v4.0 195,255 bytes despite adding the master gate table). Header bumped to **v4.2**; v4.2 milestone snapshot at
[`_archive/value_moment_catalog_v4.2_2026-06-30.md`](_archive/value_moment_catalog_v4.2_2026-06-30.md).

**Phase 1 — finished the data-grounding (read-only, live).** Proved all three binding-gate axes against a 6-org
cohort + full population, written up in
[`build_notes/vm_org_coverage_matrix_2026-06-30.md`](build_notes/vm_org_coverage_matrix_2026-06-30.md):
- **Commerce** — `Q-PROV-00` reproduced verbatim across a cohort spanning all five `COMMERCE_CONFIDENCE` states
  (`cci` FULL · `bcf`/`sarreid` STRONG · `mhc` PARTIAL-stale · `sc` PARTIAL-incomplete (126% capture trap) · `da`
  NONE). Headline economics fire **3 / degrade 2 / dark 1**.
- **Rep-identity tier** — name-bridge reproduced; 4 cohort orgs Tier-2 named, `sc` number-only, `da` behavior-only;
  row-weighted attribution ≥98% for every Tier-2 org (the decision-relevant measure).
- **Mixpanel coverage** — rich depth cohort-wide (even `da`, which is commerce-NONE), `mhc` the lone dormant org;
  population census: behavioral **187/252 (74%)**, active **146/252 (58%)**.
- **Sub-feed census** — `smart_stacks` 185/252, `shared_resources` 164/252, HubSpot 157/252, enrollment 68/252,
  Clicky a 48-portal eCat-Online subset.
- **Hard-gap** — `information_schema` scan re-confirmed **no `unit_cost`/COGS/landed/margin column** anywhere; the
  only cost-adjacent column is `portal_invoices.freight_amount`.

**Phase 2 — five claim-accuracy deltas folded in (no tier/gate changed).** (D1) `CORROBORATED` now carries a
**coverage guard** — a *sparse* second feed (e.g. `bcf` `portal_orders` ~11% of invoiced) can't corroborate even
with a clean topline (catalog VM-C1 body + `provenance_spine.md` §6.3). (D2) The **two different "FULL"s** made
explicit at the ceiling: `COMMERCE_CONFIDENCE=FULL` (clean topline, e.g. `cci`) vs `FEED_COMPLETENESS=CORROBORATED`
(needs a 2nd materially-present feed); economics still caps **STRONG** by Option A on purpose. (D3) VM-C5 returns
suppression verified already-correct. (D4) `mhc` now carries both stale-clamp **and** `DOESNT_CORRELATE`. (D5)
Register C `unit_cost` hard-gap footnoted as live-re-confirmed 2026-06-30.

**Phase 3 — compressed Domains 1–8 (49 VMs) to the locked Domain-9–13 format.** `·`-joined identity/ops lines,
one punchy Decision line, merged Allowed/Forbidden, one-line examples (tables kept only where the shape *is* the
point). **Invariants preserved verbatim in meaning:** every Gating rule, Forbidden Claim, Health-V2 reconciliation
note, Query ID, demotion banner, and the redirect stubs (VM-16 → VM-C1, VM-45 → VM-C14/CHAN-1, VM-38b → VM-38a).
Domains 9–13 were already compressed and were left as-is except the Phase 2 edits.

**Phase 4 — machine-readable Master gate table (anti-drift).** One parse-once block under the Unified Stack Rank:
`VM | tier | confidence ceiling | binding gate | Lib | live coverage` for every VM, with coverage stamped from the
Phase 1 probe (coverage keys defined once: COMMERCE / MIXPANEL / IDENTITY / OWNED / CLICKY / STACKS / RESOURCES /
HUBSPOT / ENROLL / HARD-GAP). On any disagreement with a VM body, the rank + gate tables win.

**Phase 5 — close-out.** Header → v4.2 with a top-of-file v4.2 reconciliation callout; v4.2 snapshot archived +
logged in [`_archive/ARCHIVE_LOG.md`](_archive/ARCHIVE_LOG.md) (note: no standalone v4.1 snapshot — v4.1 was a
never-committed in-place milestone; v4.0 remains the pre-rewrite rollback point); v4.1 review doc disposition
updated to "closed in v4.2"; static consistency check (anchors, no orphan `Rank N`/Prioritization-Matrix refs,
gate-table ↔ VM-body agreement).

**What was NOT touched:** no new VMs; no economics mechanism or dollar definition; no Spine gate logic (only the
§6.3 coverage-guard wording); segmentation stays 🧊 frozen; the v4.1 Unified Stack Rank tiers/ceilings/gates are
unchanged (the Master gate table consolidates them, it does not re-rank).

## 2026-06-30 — Per-entity wiring: §2 coaching cards + §3 mini-briefs + Outreach List

Wired the report's §2 (Team) and §3 (Account) onto the already-built per-entity operators — the wiring that
[`report_product/report_product_architecture.md`](report_product/report_product_architecture.md) §9 sketched but
[`operators/report_operator.md`](operators/report_operator.md) never made runnable. **No canon changed; no economics
math touched; no new findings invented.** Pure assembly under the existing contract.

**Why.** A prior review found the 4.0 Sarreid report well-calibrated but ~¼ the actionable density of the 3.0
reports. The diagnosis was already established: the rung-4 Option A operator (C2-by-rep × S1-by-rep × Mixpanel),
the rep copilot's commercial levers, and the customer brief v5.1's §15/§16 mini-brief shape all exist and are
dry-run-validated on Sarreid — nothing in `report_operator.md` was pulling from them.

**What changed (wiring only):**
- **`operators/report_operator.md` — new Step 5a "Per-entity wiring."** Explicit consumption steps for §2 (from
  `rung4_option_a_operator.md`) and §3 (from the customer brief v5.1 operator + `selling_customer_exception_layer.md`
  S1). Adds the Trace contract: every $-figure rendered in a §2 card or §3 mini-brief must trace, in the Appendix
  Traceability block, to the operator row it came from — or Step 10 deletes it. Order-of-operations diagram
  updated; relationship table now points at the three per-entity operators by file.

**What changed in the Sarreid worked example (regenerated against live data, read-only, 2026-06-29 through-date):**
- **§2 Team.** Prose paragraph replaced with **5 coaching cards** rendered from rung-4 O1/O2 — Hoffman $786K
  (7 accounts) / Klein $398K (1) / Davis $344K (2) / Barnard $243K (7) / Anhut $83K (2) = **$1.854M of bookable
  $-at-risk to coach against this week**. Each card carries its $-figure, the matched C2 leak cell, and a one-
  sentence action tied to a specific named account. The top-10 RS-01 leaderboard table is kept as the at-a-glance
  roster (it now sits above the cards, not as the §2 endpoint). C2-by-rep produced no rogue — that's said plainly
  in §2 rather than manufactured into a fake card.
- **§3 Account.** 30-row watchlist table replaced with **5 mini-briefs** (Kathy Kuo $522K, France and Son $398K,
  NetRetailers $318K, Swan's Nest $66K, OP Jenkins $62K). The three accounts that fire editorial §M (>25% decline
  on >$50K) get a Decline Investigation hypothesis block in the disown-the-cause form. The two cadence-cliff
  accounts (Kathy Kuo, NetRetailers — growing but skipped a normal beat against a daily cadence) get a confirm
  call read, **not** a §M block. Positions 6–30 collapse into a short tail watchlist table.
- **§3 Outreach List (new).** 7-row "This Week's Outreach List" — account · rep · action · talking point ·
  timing — covering ~$1.47M LTM across the top 5 mini-briefs + 2 high-decay tail accounts. Cadence-cliff rows
  tagged so the rep doesn't open a decline conversation by accident.
- **§3 watchlist total corrected.** ~$1.35M LTM at risk (old >60d-silent filter) → **~$2.18M LTM at risk** (the
  canonical S1 form: silent > 2× the account's normal gap). Same 30-dealer count; the canonical S1 includes
  cadence-cliff signals the older filter missed.
- **Appendix.** Six new Traceability rows for the cards, mini-briefs, §M blocks, and Outreach List — each tracing
  to a named operator (rung-4 O1/O2; customer brief v5.1 §15/§16; editorial rule §M). The "Queries referenced"
  block now names the per-entity operators explicitly.
- **Minor naming-consistency tweaks in §1** (Finding #6, Priority Actions row 1, "What the data can't tell you"):
  "rep 546" → "Deborah Klein (rep 546)" now that §2/§3 name her. **§1 numbers unchanged.**

**What was NOT touched (explicit guardrails honored):** no canon file (CANON.md, the Spine, query_library_v2,
value_moment_catalog, editorial rules, communication_guideline, industry_context, sarreid profile); no economics
mechanism; no new dollar definition; no segmentation logic; no consolidation/refactor/renumbering (deferred —
this is wiring, not the canon-consolidation pass a prior review separately recommended). The 4.0 wins are
intact: provenance header, "what we don't show, and won't fake," tier-aware leakage with canon-vs-raw contrast,
NRR/new-logo split, partner-frame voice. Every new $-figure carries the same plain-English provenance treatment
as the rest of the report and traces to an operator's actual output.

**Determinism contract honored.** Same data + same profile + same operator reproduces this report. Per-entity
operator outputs were regenerated live via the operator's specified queries (read-only, `user-supercat-postgres-
vpn` `execute_sql`); no figure was authored from memory.

## 2026-06-29 — VM catalog v4.1 Pass B: Domain 9–13 body provenance remediation

Closes the pre-existing body defects the independent review found (the ones outside v4.1's original scope). All
verified against `provenance_spine.md` §6.3 and `query_library_v2.md` before editing.

- **VM-C1 confidence rule corrected.** `UNVERIFIED–SINGLE-FEED` now **caps at STRONG** (was wrongly "cap PARTIAL"),
  matching Spine §6.3 and the catalog's own through-line; PROVABLY-INCOMPLETE/STALE keep PARTIAL, DEAD suppresses.
  Same fix applied to the **Forbidden Claims Register** row that repeated "cap PARTIAL."
- **FULL→STRONG body cleanup (Option A).** VM-CHAN-1 gating + example relabeled from `FULL` to `STRONG (CORROBORATED)`;
  VM-C20 readiness changed from "FULL with cost" to "cost unlocks true margin but the single-feed ceiling stays STRONG."
- **Body query-ID drift fixed.** Verified the library actually contains Q-43 (live), Q-44 (internal), Q-46/47/49/50
  (conditional) — removed the stale "to be added to query library" tags on VM-43/44/46/47/49/50. **Only Q-48 (HubSpot)
  is genuinely unauthored** and is now labeled "pending," not "to be added."
- **Corrected the Pass-A readiness note**, which had over-counted pending VMs (VM-44/47/49/50 are live/conditional, not
  pending; only VM-48 is pending).

After Pass B, the catalog bodies, the Unified Stack Rank, the Spine, and the query library agree on confidence ceilings
and query readiness. No query/pipeline logic changed — catalog + spine prose only.

## 2026-06-29 — sarreid worked-example reconciliation: one canon-compliant, deterministic output

Reconciled the two conflicting Sarreid worked-example outputs (`outputs/Sarreid_CEO_intelligence_report_2026-06-29.md`
and `..._rerun.md`) into a **single regenerated, gate-determined report** produced end-to-end via
[`operators/report_operator.md`](operators/report_operator.md) against live data. **Read-only throughout; no Spine,
gate, query, or operator was re-authored** — only consumed. The single live file is now
[`outputs/Sarreid_CEO_intelligence_report_2026-06-29.md`](outputs/Sarreid_CEO_intelligence_report_2026-06-29.md);
both prior versions are archived under `_archive/` with top-of-file SUPERSEDED markers and an entry in
[`_archive/ARCHIVE_LOG.md`](_archive/ARCHIVE_LOG.md).

**Defects resolved (the canon-correct way, every time):**
- **A — Tier-aware leakage.** Recomputed live via `Q-ECON-LEAK` with the true-median + tier guard + volume guard +
  profile §4 house/sample/Wayfair screen. Result: **~$150,159 = 1.61% leak rate**, broadly distributed (top rep 2.3%,
  bottom 0.7% — no rogue). Ships **DIRECTIONAL** with the mandatory human gut-check completed in-session (passed; see
  the report's §4 commerce-patterns block). The earlier file's raw ~$250K–$400K is exactly the pre-guard overclaim
  the product exists to prevent (the asi "$1.35M / 42% rogue" lesson).
- **B — `FEED_COMPLETENESS` is gate-determined, not chosen.** `Q-ECON-00` for sarreid emits `commerce_confidence =
  STRONG` and `salesdata_over_invoiced = 1.74`. Per Spine §6.8, `> 1.3` is the soft signal "invoice feed is likely a
  channel subset → reinforces UNVERIFIED-SINGLE-FEED." The booked-vs-invoiced agreement (1.005) is one corroborating
  signal, but by Spine §5.3 "lowest input wins" the gate emits **`FEED_COMPLETENESS = UNVERIFIED-SINGLE-FEED`**.
  Every dollar's third tag in the new report matches; the header language is no longer "the numbers are solid /
  CORROBORATED."
- **C — Deterministic signal ranking.** Signal Summary is now built last from `SIGNAL_RANK = surprise × dollar ×
  actionability` with pinned tie-breaks (`dollar_impact DESC, signal_id ASC`), then re-sorted into the narrative arc.
  Documented in the appendix's "Signal ranking (determinism contract)" block.
- **D — Tone balance enforced.** Signal Summary: Finding #1 positive (NRR-driven topline + non-Wayfair +22.5%
  growth), ≥3 positive (#1/#2/#3/#4), risk in slots #6/#7, max 4 from one section.
- **E — §1 contradiction removed.** New-logo retention (cohort) and existing-base NRR (dollar) are now separate
  findings with their own numbers (#1 and #5), and the body §4 narrates them as two distinct stories.
- **F — Retention cohort pinned.** Cohort = `MIN(invoice_date) per customer_bill_to_number` falls in the prior-LTM
  window (= the 451). Reorder = current-LTM activity for those customers (= 111). 24.6%. The pin is in the appendix
  Traceability and the same numbers run in §1, §4, and the appendix.
- **G — Rep table determinism.** Top 10 reps by current-LTM invoiced (deterministic sort), names bridged via
  `portal_orders.rep_name` (97.9% — Tier 2), with footnote "Eight reps carry material revenue (>$50K) with no
  prior-year history; five clear $100K." Both the row count and the "new rep" count fall out of fixed thresholds, not
  ad-hoc.
- **H — eCat shown as absolute dollars.** Recomputed live: **$2.05M, 558 orders, 230 customers, 36 reps (= 13.1% of
  invoiced)**. Never as a "share" or "capture rate" at this penetration (profile §3 + signal-catalog SIG-COMMERCE-01).
  Reconciled the prior $2.5M vs $2.05M discrepancy to the live number.
- **I — Every dollar three-tagged.** Step-10 re-read pass: every dollar in the body carries
  `[source · confidence · completeness]` inline and traces to a query named in the appendix (`Q-ECON-00`,
  `Q-ECON-LEAK`, `S1`, `C2`, `Q-CHAN-00`, plus the explicit per-metric SQL lines in the Traceability block).

**Determinism contract honored.** Profile context, mode, and confidence caps come from `profiles/sarreid.md` and the
gates — not the model. A second identical run (same data + same profile) reproduces this report (operator §"determinism
contract").

**Open question — resolved (does not require user input).** `Q-ECON-00` for sarreid emits `FEED_COMPLETENESS =
UNVERIFIED-SINGLE-FEED`, which **agrees with the rerun and contradicts only the earlier original** — so the
"differs from *both* prior reports" stop condition didn't trigger. The new report uses UNVERIFIED-SINGLE-FEED
language end-to-end.

**Repointed canon (these previously cited the overclaiming original):**
- `profiles/sarreid.md` status note: re-ratified against the regenerated report.
- `operators/report_operator.md` "Worked example" pointer: now points at the regenerated report.
- `report_product/report_product_README.md` "Suggested next step" / sarreid pointer: updated.

**Archived (reversible — top-of-file SUPERSEDED marker, full content kept):**
- `_archive/Sarreid_CEO_intelligence_report_2026-06-29_original_SUPERSEDED.md`
- `_archive/Sarreid_CEO_intelligence_report_2026-06-29_rerun_SUPERSEDED.md`

## 2026-06-29 — VM catalog v4.1 Pass A cleanup (post-independent-review)

A fresh-agent stress review (`build_notes/vm_catalog_v4.1_review_2026-06-29.md`, verdict: ship-with-fixes) was
itself reviewed and triaged. **Pass A** applies the small set of defects that v4.1 *introduced*; the larger set of
**pre-existing Domain 9–13 body** provenance issues is deferred to **Pass B** (logged below as a follow-up, not done).

- **Confidence-ceiling correction (owner decision: Option A — conservative).** Removed the false claim that "a single
  invoice feed never reaches `FEED_COMPLETENESS=CORROBORATED`" (≈14/21 cohort orgs *are* CORROBORATED). Reworded to:
  economics VMs **deliberately cap at STRONG even when CORROBORATED** (one ERP's booked-vs-invoiced agreement is internal
  corroboration, not an independent feed) — a *presentation* cap one notch below Spine §6.3's "eligible for FULL," with
  the operating principle "never show a client a number we can't stand behind — caveat or suppress." Mirrored as a new
  **presentation-cap note in `provenance_spine.md` §6.3** so the canon no longer self-contradicts.
- **Query-readiness vs priority decoupled.** Added a `Lib` column (✅ live / 🟡 pending / ⏳ gated) to the Unified Stack
  Rank S/A/B tables + a long-tail note, instead of downgrading strategically-important pending-SQL VMs (C11/C3/C10/C7/
  C9/C17/C20). Priority is the *value* claim; `Lib` is whether audited SQL exists today.
- **Register A two-lane rule.** Replaced "cousins lead only for no-ERP/catalog-only orgs" (which contradicted the
  VM-18/19/20/21 banners) with: invoiced twin leads the **commercial-outcome** story; cousin leads the **eCat
  workflow/adoption** story (or when no invoice feed exists). Synced the header callout.
- **Count fix.** "Six" → "Seven" demoted cousins (callout + this changelog).
- **Link fix.** Domain-13 hard-gap pointer now targets **Register C** directly, not the consolidated-appendix redirect.
- **Pass B follow-up (NOT done — pre-existing, out of v4.1's scope):** Domain 9–13 VM *bodies* still carry provenance
  drift the rewrite didn't touch — VM-C1 caps UNVERIFIED at PARTIAL (Spine §6.3 says STRONG); VM-CHAN-1 / VM-C20 bodies
  use old FULL language; several body-level `Query IDs` say "to be added" while the library has them (Q-43/Q-46) and
  vice-versa (VM-44/47/48/49/50). Remediate against the Spine + `query_library_v2.md` in a dedicated pass.

## 2026-06-29 — `value_moment_catalog.md` v4.0 → v4.1: unified stack rank, Domains 1–8 re-gated, eCat cousins demoted

Capability-catalog rewrite. The stress test found the catalog was half-reconciled: Domains 9–13 were born
provenance-hardened, but the **original Domains 1–8** were never re-gated against the Spine, and the bottom-of-file
**Prioritization Matrix still ranked the superseded VM-16 and VM-45 as "Tier 1 — Implement Now."** v4.1 closes that
seam. **Scope = the catalog only** (no query, pipeline, or report-build logic changed). v4.0 snapshot preserved at
`_archive/value_moment_catalog_v4.0_2026-06-29.md` (logged in `_archive/ARCHIVE_LOG.md`).

- **One ranking system.** Removed the legacy Tier-1/2/2.5/Conditional/Deferred **Prioritization Matrix** (now a
  redirect stub) and demoted the money-map's inline `Rank N` tokens to labeled legacy provenance. Added a single
  **Unified Stack Rank** (Tier S/A/B/C/D) near the top — the authoritative carrier of every VM's `Stack` tier +
  `Confidence Ceiling` + binding `Gate`, on one 5-factor rubric (confidence-survivability weighted ×1.2).
- **Anchor flipped to VM-C1 True Topline** (the invoiced-net denominator). VM-01 stays a Tier-A differentiator; its
  `r > 0.96` claim was softened to "BCF-only, cohort-broadening pending."
- **Domains 1–8 re-gated** to the Spine: added the three v4.1 fields to the schema, with inline gate stamps where
  legacy text was stale (VM-05 active-seat roster, VM-12 FEED+billing-entity, VM-43 territory-format preflight,
  VM-37 point-in-time/`sales_data` caveat).
- **Seven eCat VMs demoted to "intent/activity cousins"** with banners (VM-13→C3/K2, VM-14→K-cadence, VM-17→K8/S1,
  VM-18/19/20/21→Domain-9 economics), into a new **Register A**. VM-16/VM-45 confirmed as pure redirect stubs.
- **Frozen + hard-gap items moved off the stack** into **Register B** (VM-K5 segmentation 🧊) and **Register C**
  (VM-C19/C21/C25 + margin/AR/claims/lead-time/market-ROI ⏳); the duplicate "Demand-Side Honest-Gaps" appendix was
  consolidated into Register C so hard gaps are catalogued once.
- **Summary Statistics rewritten** off the v4.1 tier/register counts (dropped the "49/51 original" framing).
- **Follow-ups (not done here):** re-sync the `copilot_simulation` prototype to invoiced truth + Tier-1 rep-identity
  labeling; downstream `operators/` and `report_product/` docs that cite the catalog still resolve (links unchanged)
  but their prose may reference the old matrix.

## 2026-06-29 — Wire company foundation as purpose layer; fix drift in foundation docs

Connected the report canon to SuperCat's company-level foundation (`../../foundation/`, the 00–06
strategic docs). No structural changes to the precedence chain or reading contract.

- **Restored company foundation** to `SuperCat 4.0/foundation/` (7 files: `00_README` through
  `06_how_we_operate`, dated 2026-05-12). Previously stranded in `~/Downloads/foundation 3/` (iCloud
  sync artifact). This is the company's strategic context — identity, ICP, economics, market,
  direction, operations — not the Insightful Product's data-provenance `foundation/` folder (which is
  a separate, correctly-scoped corpus inside this project).
- **Added purpose-layer section** to `CANON.md` (above the precedence chain): the report's voice and
  posture derive from SuperCat's Core Values (Customer-Obsessed, Own the Outcome, Learn Loudly). The
  foundation is the *purpose* layer — it does not participate in the data-authority precedence chain.
- **Added voice-origin citation** to `knowledge/communication_guideline.md`: one paragraph connecting
  the "no shit" test / lead-with-value / refuse-to-fake discipline to the Core Values.
- **Fixed "benchmarking" overclaim** in foundation docs (`00_README`, `04_market_and_competitors`,
  `05_strategic_direction`): "cross-customer benchmarking" → "cross-customer intelligence" where the
  term described SuperCat's moat. The report product explicitly excludes peer benchmarking
  (`report_editorial_rules_v4.md` §E.5); the foundation was overclaiming a capability the product
  refuses to ship. (Domain 6 name "Cross-Instance Benchmarking" in `01_what_we_do.md` left as-is — that
  is the catalog's proper noun, not the strategic claim.)
- **Updated VM count** in foundation docs: "42 value moments across 8 domains" → "50+ value moments
  across 13 domains" (reflecting the v4 catalog's Domains 9–13 Intelligence Stack expansion). Pinned
  counts replaced with "canonical count in the catalog" pointers where appropriate.
- **Known debt (unchanged):** the foundation docs' relative links (`../skills/…`, `../AGENTS.md`) assume
  sibling folders that do not currently exist at `SuperCat 4.0/`. These were already broken before this
  change; the content is correct, only the source-citation links are stale.

## 2026-06-29 — Operationalize the report: `report_operator.md` + `profiles/` (Route A)

Additive build that makes the org-level report repeatable. No file moves, no link rewrites to existing docs,
`CANON.md` precedence/reading-contract logic unchanged (only the profile's path made explicit).

- **New `profiles/` folder** (reading-contract input #2): `profile_template.md` (strict facts-only schema with an
  allowed-vs-forbidden table), `README.md` (the anti-drift / anti-generic-bias rationale + the derive→ratify→cache
  workflow), and `sarreid.md` (first ratified instance, reverse-engineered from the existing Sarreid report
  appendix — identity, channel model, house/sample + Wayfair screen, designer-project buyer note, structural
  concentration, Standard mode, hard-gap suppressions; **no dollar findings carried in**).
- **New `operators/report_operator.md`** (Route A, agent-operated): Step-0 four-input reading contract + Steps 1–10
  bound one-to-one to `report_product/report_product_architecture.md` §6, plus a 7-point determinism contract so a
  re-run with the same profile + data reproduces the report. Dry-run-validated on `sarreid` (the existing output is
  the worked example).
- **Additive wiring:** `CANON.md` canon-docs table + reading-contract step 2 now name `profiles/{org}.md`;
  `report_product/report_product_README.md` status table flips the report-operator + profile rows to done.
- **Out of scope (deferred):** the Python pipeline + HTML shell port (Route B) — requires the frozen
  `Insightful Product 3.0/`; untouched. Live second-client validation is a separate (MCP-executing) session.

## 2026-06-29 — Doc reconciliation: corrected `_archive/ARCHIVE_LOG.md` after the phase-2 audit

Docs-only fix. An independent audit (given the phase-1 spec) flagged that phase 2 had updated `CANON.md` and this
CHANGELOG but **not** `_archive/ARCHIVE_LOG.md`, leaving that log with false on-disk claims and a "Pass" numbering
that collided with this file's "Phase" numbering. No files moved, no links rewritten, `CANON.md` untouched.

- **Corrected stale location claims** in `ARCHIVE_LOG.md` Pass-2 section: the 6 canon files it said were "kept live
  at root" (`communication_guideline.md`, `report_editorial_rules_v4.md`, `report_product_README.md`,
  `report_product_architecture.md`, `signal_catalog_v4.md`, `segmentation_derivation.md`) were relocated by the
  phase-2 foldering into `knowledge/`, `report_product/`, and `foundation/`.
- **Corrected the `external_vm_index.md` link note:** its outbound links read `../foundation/…` after phase 2,
  not the bare `../` the Pass-2 note recorded.
- **Added a terminology bridge** to `ARCHIVE_LOG.md`: its "Pass 2" == this file's "Root scaffold" entry; this
  file's "Phase 2" (canon foldering) left `_archive/` untouched but supersedes the Pass-2 location claims.

## 2026-06-29 — Phase 2: canon foldered into foundation/ + knowledge/ + report_product/

Deeper organization pass (after the phase-1 scaffold passed an independent audit). The governed canon, which
phase 1 deliberately kept flat at root, is now grouped into three folders. `CANON.md` and `CHANGELOG.md` remain
at root as the index and the log.

- **`foundation/`** ← `provenance_spine.md`, `query_library_v2.md`, `value_moment_catalog.md`,
  `insights_moneymap_SYNTHESIS.md`, `selling_customer_exception_layer.md`, `provenance_map_rep.md`,
  `provenance_map_customer.md`, `segmentation_derivation.md`
- **`knowledge/`** ← `industry_context.md`, `communication_guideline.md`
- **`report_product/`** ← `report_product_README.md`, `report_product_architecture.md`, `signal_catalog_v4.md`,
  `report_editorial_rules_v4.md`
- **Link sweep:** the move broke 33 in-scope markdown links (intra-canon cross-refs + the phase-1 `../X.md`
  pointers from `operators/`, `build_notes/`, and the `_archive/external_vm_index.md` curated links). All were
  rewritten to correct relative paths and re-verified with the resolver. One cross-product link in
  `foundation/selling_customer_exception_layer.md` to the sibling `Customer Intelligence/` folder was repointed
  `../` → `../../` (move-induced).
- **`CANON.md` updated:** the precedence bullets, reading contract, canon-docs table, and status note now show
  the `foundation/`, `knowledge/`, `report_product/` paths.
- **Accepted debt unchanged:** the 5 stale links inside frozen `_archive/phaseA_census/` remain (archive content
  not edited). Bare-name prose mentions left as-is per policy.

## 2026-06-29 — Root scaffold: working folders + `external_vm_index` retired + cross-folder link sweep

Basic, link-safe first-pass reorganization for the agent-operated (route A) workflow. Governed canon stays
flat at root by design (`CANON.md` says canon lives at the folder root); only working/process/output docs moved.

- **Created 5 folders** and moved 14 live files:
  - `operators/` ← `rep_copilot_operator.md`, `rung4_option_a_operator.md`
  - `config/` ← `house_rep_exclusions.md`
  - `build_notes/` ← `rep_intelligence_layer2_build.md`, `rep_intelligence_label_signoff.md`,
    `selling_customer_label_signoff.md`, `selling_customer_confidence_audit.md`,
    `selling_customer_pilot_test_worksheet.md`
  - `handoffs/` ← `intelligence_stack_roadmap.md`, `intelligence_stack_handoff_2026-06-29.md`,
    `rung4_fusion_decision_brief.md`, `report_substance_review_2026-06-29.md`,
    `selling_customer_NORTHSTAR_MVP_reconciliation_handoff.md`
  - `outputs/` ← `Sarreid_CEO_intelligence_report_2026-06-29.md`
- **Retired `external_vm_index.md` → `_archive/`** per `provenance_spine.md` (stale, superseded by
  `value_moment_catalog.md` v4). Its 6 outbound links repointed to `../`; the one live inbound pointer in
  `value_moment_catalog.md` repointed to `_archive/external_vm_index.md`. (See `_archive/ARCHIVE_LOG.md` Pass 2.)
- **Cross-folder markdown links rewritten** so nothing breaks. Files repointed: `value_moment_catalog.md`,
  `_archive/external_vm_index.md`, `operators/rep_copilot_operator.md`, `operators/rung4_option_a_operator.md`,
  `handoffs/intelligence_stack_roadmap.md`, `handoffs/intelligence_stack_handoff_2026-06-29.md`,
  `handoffs/selling_customer_NORTHSTAR_MVP_reconciliation_handoff.md`, `build_notes/rep_intelligence_layer2_build.md`,
  `build_notes/rep_intelligence_label_signoff.md`, `build_notes/selling_customer_confidence_audit.md`,
  `build_notes/selling_customer_pilot_test_worksheet.md`. Same-directory links and bare-name prose mentions left
  as-is (still accurate). A few pre-existing dangling links to already-archived files (`commerce_*`, phase-A census)
  were repointed into `_archive/` while in those files.
- **Verified programmatically:** all 118 relative markdown links across the tree were resolved against the
  filesystem. The only 5 unresolved are inside frozen `_archive/phaseA_census/` drafts (pre-existing Pass-1 debt,
  archive content intentionally not edited).
- **No code changed.** No `scripts/`/`pipeline/` folder created — route A now; the deterministic data layer is
  extracted only when the hybrid step begins. Deeper foldering of the governed canon (`foundation/`/`knowledge/`/
  `report_product/`) is deferred to a phase-2 pass with its own link sweep.

## 2026-06-29 — Wired `industry_context.md` into the report spec; repointed stale comms refs

- **Repointed `report_substance_review_2026-06-29.md`** (the follow-up flagged below — now resolved).
  The "FM9 / channel-first" references were split: the channel-is-a-minority framing now points at
  `industry_context.md` ("How they sell"), and the don't-narrate-your-machinery voice rule points at
  **Failure Mode 3** in `communication_guideline.md`. The dead "FM9" label (the new guideline only has
  Failure Modes 1–5) was removed.
- **Enforced the reading contract in `report_product_architecture.md`.** Added a generation-sequence
  **step 0** that loads the four governing inputs (`provenance_spine` + client `profile.md` +
  `industry_context.md` + `communication_guideline.md`) before any query runs, added both knowledge-layer
  docs + `CANON.md` to the §9 "Relationship to the rest of 4.0" table, and added a "Governed by" pointer
  to `CANON.md` in the header. Previously the build spec never named `industry_context.md`, so a run
  could skip it despite CANON requiring it.
- **Cross-linked `report_editorial_rules_v4.md`** to `industry_context.md` and `communication_guideline.md`,
  stating the boundary: editorial rules = report-structure voice; comms guideline = cross-cutting voice
  test (wins on tone overlap); industry_context = "is this even a finding."
- **Added a GOVERNANCE layer** to the `report_product_README.md` stack diagram so the index shows the
  reading contract above the report product.
- **Scope note:** documentation/reference fixes only — no pipeline, query, or report-build logic changed.

## 2026-06-29 — Communication guideline split into voice-only + industry_context; CANON seeded

- **Split the communication guideline.** The previous `communication_guideline.md` tried to hold
  **both** writing style **and** domain facts. It is now **voice-only** (how the report talks):
  the "no shit" test, the state-what-the-data-shows / never-invent-why rule, Failure Modes 1–5,
  house style, the provenance voice, and the pre-send checklist. Replaced in place with the
  finalized voice-only version (from a prior working session).
- **Added `industry_context.md`** as a new governed root canon file. It holds the
  furniture/lighting/décor domain knowledge that used to be tangled into the guideline — who the
  clients and their buyers are, the wholesale market calendar (the seasonality fix), structural
  truths that are never findings on their own (big-account concentration, lumpy project revenue,
  long lead times, configure-to-order price dispersion), and native vocabulary. **The two were not
  merged back together** — voice and domain facts are deliberately separate files now.
- **Seeded `CANON.md`** — the governed index. Establishes the precedence
  `provenance_spine > client profile > industry_context > communication_guideline > source-data
  labels` and the **reading contract**: every report run loads provenance_spine + client profile +
  industry_context + communication_guideline before any queries run.
- **Scope note:** no pipeline, query, or report-build files were changed in this step. Canon
  currently lives flat at the folder root; both new files are governed root files.
- **Cleanup left for a follow-up:** `report_substance_review_2026-06-29.md` still points at
  `communication_guideline.md` for the "FM9 + channel-first" framing (lines ~20, ~88, ~134) — that
  content now lives in `industry_context.md` ("How they sell"), so those references should be
  repointed. **→ RESOLVED 2026-06-29** (see the entry above).
