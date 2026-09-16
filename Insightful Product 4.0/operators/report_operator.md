# Insightful Report — Applied Operator (org-level roll-up, Route A)

> **What this is.** The **runnable** org-level intelligence-report operator: it executes the report product by
> hand (agent-operated, MCP queries → assembled document) so a single run is **repeatable and low-drift**. It is
> the *application* of the spec in [`../report_product/report_product_architecture.md`](../report_product/report_product_architecture.md)
> (modes, adequacy gate, fixed section order, generation sequence) on top of
> [`../foundation/query_library_v2.md`](../foundation/query_library_v2.md) (the SQL). The per-entity operators
> ([`rep_copilot_operator.md`](rep_copilot_operator.md), the customer brief, [`rung4_option_a_operator.md`](rung4_option_a_operator.md))
> are surfaces *below* this; this report is the **roll-up that sits above them** and re-authors none of their provenance.
>
> **Consume, do not re-author.** Every number comes from a gated, already-validated source. This operator is
> **assembly under a contract** — it adds no new economics mechanism, no new dollar definition, no segment logic.
>
> **Trigger.** "run the insightful report for {org}", "org intelligence report / CEO report for {org}".
>
> **Inputs.** `{org_shortname}` (required). A **RATIFIED** profile at `../profiles/{org}.md` (required — see Step 0).
> The operator resolves `{ORG_ID}` and `{report_through_date}` itself in the preflight.
>
> **MCP.** `user-supercat-postgres-vpn` (`execute_sql`, read-only) required; `user-bigquery-admin` (`query`,
> read-only) optional (Mixpanel behavior context). **Read-only throughout.** Live figures `[from-live]`; nothing ships
> a number the gates didn't sanction.
>
> **Status: SPEC-COMPLETE OPERATOR — end-to-end-validated on `sarreid` (org 1).** Worked example
> (regenerated, gate-determined, single live Sarreid run):
> [`../outputs/Sarreid_CEO_intelligence_report_2026-06-29.md`](../outputs/Sarreid_CEO_intelligence_report_2026-06-29.md).
> *(Two earlier same-day dry-runs were superseded into `_archive/` during the 2026-06-29 reconciliation —
> see `../CHANGELOG.md` 2026-06-29 entry and `../_archive/ARCHIVE_LOG.md`.)*
> The leakage dollar requires a **per-report human gut-check** and per-org house-account confirmation at every run
> (the profile sets the screen; the human still confirms before any leakage dollar ships).

---

## 0. Order of operations (do not reorder)

```
STEP 0  Reading-contract load (CANON)  ──► load 4 inputs BEFORE any query; no profile ⇒ STOP
        │   provenance_spine · profiles/{org}.md · industry_context · communication_guideline
        │   exception: --cohort-validation flag permits an inline-draft profile (logged, header-flagged)
        ▼
STEP 1  Provenance preflight (FIRST)   ──► Q-ECON-00, FEED_COMPLETENESS, Q-CHAN-00, rep-identity gate
        │   emits COMMERCE_CONFIDENCE (never FULL), clamped report_through_date, REPORT_INTELLIGENCE_TIER, mode
        ▼
STEP 2  Data gather                    ──► run the query library; materialize invoiced-anchored results
        ▼
STEP 3  Signal detection               ──► only signals whose feed passes their gate may fire
        ▼
STEP 4  Signal scoring                 ──► SIGNAL_RANK = surprise × dollar × actionability; conf = LEAST(ceiling, COMMERCE_CONFIDENCE)
        ▼
STEP 5  Context bundles                ──► per-section, carrying provenance stamps + editorial rules
        │                                  §2/§3 bundles are PULLED from the per-entity operators (Step 5a),
        │                                  not re-derived here
        ▼
STEP 5a Per-entity wiring (§2 + §3)    ──► consume rung4_option_a_operator (coaching cards),
        │                                  customer brief v5.1 (account mini-briefs + outreach list),
        │                                  rep_copilot_operator (Tier-2 bridge, identity, RS-01)
        ▼
STEP 6  Section rendering              ──► fixed positions; every dollar three-tagged; rep naming tier-gated
        ▼
STEP 7  Signal Summary (built last)    ──► top 5–7 by rank, narrative arc, ≥3 positive, finding #1 positive, max 4 from one section
        ▼
STEP 8  Assembly                       ──► fixed render order; write to outputs/{Org}_..._report_{date}.md
        ▼
STEP 9  Structural verification        ──► all mandatory subsections present
        ▼
STEP 10 Provenance + static check      ──► re-read every dollar: 3 tags + traces to an appendix query, else DELETE
```

**One line:** *make the CEO say "I didn't know that," and make every number in it survive a CFO — by running the
spec's gates in order and letting the profile, not the model's mood, settle the judgment calls.*

This sequence is the executable form of `report_product_architecture.md` §6. If this operator and the architecture
ever disagree, **the architecture (and the Spine above it) win** — fix the operator.

---

## Step 0 — Reading-contract load (per [`../CANON.md`](../CANON.md); before anything)

Load these **four** into context first, in this order. A run that skips any of the four is **invalid**:

1. **[`../foundation/provenance_spine.md`](../foundation/provenance_spine.md)** — Tier-0 truth (invoiced axiom,
   confidence tiers, `FEED_COMPLETENESS`, identity gates, gate catalog). Nothing downstream overrides it.
2. **`../profiles/{org}.md`** — the client profile (input #2; overrides industry defaults + bad source labels).
3. **[`../knowledge/industry_context.md`](../knowledge/industry_context.md)** — what's industry-normal (seasonality,
   market calendar, concentration, channel mix). **If a pattern is explained here, it is context, not a finding.**
4. **[`../knowledge/communication_guideline.md`](../knowledge/communication_guideline.md)** — voice only (the "no shit"
   test, anti-cute, Failure Modes 1–5, house style, pre-send checklist).

**No ratified profile ⇒ STOP.** Do **not** free-guess the client's context. Derive a draft per
[`../profiles/README.md`](../profiles/README.md) (run the Step-1 preflight + identity/channel/concentration queries),
present it for human ratification, save `../profiles/{org}.md`, then resume. Guessing context is the primary drift/bias
source this operator exists to eliminate.

**The `--cohort-validation` exception flag (2026-06-30).** Cohort validation passes (PASS1 / PASS2 / any
multi-org dry-run intended to stress the operators against unprofiled orgs) need to walk into orgs without a
ratified profile on purpose — that's the point of the exercise. To preserve the gate's force, the override is
**explicit and logged**, not a silent posture:

| Run flag | Profile state | Behavior |
|---|---|---|
| *(no flag)* | `profiles/{org}.md` exists and is RATIFIED | proceed normally |
| *(no flag)* | missing or DRAFT | **HARD STOP** — emit the §5b.2 Gate-STOP artifact with `Step 0 — ratified profile` = FAIL; do not generate a draft inline; do not proceed |
| `--cohort-validation` | `profiles/{org}.md` exists and is RATIFIED | proceed normally (flag is a no-op) |
| `--cohort-validation` | missing or DRAFT | proceed with an **inline draft profile** derived from the Step-1 preflight + identity/channel/concentration queries; the run is tagged `VALIDATION ARTIFACT — INLINE DRAFT PROFILE`; the draft profile is written to `profiles/{org}.draft.md` for human review; **the run header must say so verbatim** (template below) |

**Required header line when `--cohort-validation` fires the inline-draft path (verbatim, never paraphrase):**

```
> **Profile state: INLINE DRAFT (cohort-validation override).** No ratified profile present at run time;
> `--cohort-validation` was passed, so this run derived a draft profile inline from the Step-1 preflight.
> Draft saved to `profiles/{org}.draft.md` — human ratification required before this output is treated as
> a client-facing report.
```

**Logging contract:** every `--cohort-validation` run that fires the inline-draft path **must** emit a
`CHANGELOG.md`-style append-only line into the run's appendix `Traceability` block of the form:

```
[STEP-0 OVERRIDE · {org} · {YYYY-MM-DD HH:MM} · profile=INLINE-DRAFT · --cohort-validation]
```

so the override is greppable across all outputs. **A run that uses the inline-draft path without emitting both
the header line and the appendix log line is non-compliant.** The flag does not relax Step 5b.2 Gate-STOP for
any *other* preflight failure (`COMMERCE_CONFIDENCE = NONE` with no eCat, hard gate fail, etc.) — those still
hard-STOP per the §5b.2 template; the override only relaxes the missing-profile gate.

**Default posture is unchanged: without `--cohort-validation`, missing profile = STOP.** PASS1 / PASS2 outputs
that previously used an implicit inline-draft profile (cci / kal / hfg / sca PASS1 / PASS2) were operating
inside this newly-explicit exception path; future cohort runs must pass the flag.

---

## Step 1 — Provenance preflight (NEW, run FIRST; sets the whole run's posture)

Run before any finding is computed; the outputs cap everything downstream:

| Emits | From | Forces |
|---|---|---|
| `COMMERCE_CONFIDENCE` ∈ {STRONG, PARTIAL, LIMITED, NONE} (**never FULL**) | `Q-ECON-00` (Spine §6.1) | the ceiling every dollar inherits |
| clamped `report_through_date` | `LEAST(MAX(invoice_date), CURRENT_DATE)` | clamps fantasy-date orgs; defines every window |
| `FEED_COMPLETENESS` ∈ {CORROBORATED, UNVERIFIED-SINGLE-FEED, PROVABLY-INCOMPLETE, STALE, DEAD} | Spine | suppress-on-incomplete |
| `DATA_MASS_TIER` (capacity) | §4a table | volume adequacy |
| `REPORT_INTELLIGENCE_TIER` = `LEAST(DATA_MASS_TIER, confidence_to_tier(COMMERCE_CONFIDENCE))` | §4c | overall posture; FULL collapses to STRONG |
| `REP_IDENTITY_TIER` ∈ {0,1,2} | Spine §7.1 / `rep_copilot_operator.md` §1 | rep naming (T2 named / T1 number / T0 behavior-only) |
| channel posture | `Q-CHAN-00` | capture-not-attribution; eCat shown as channel, not "share". **NONE / PARTIAL render uses the canonical suppression templates in [`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md) §O.1 / §O.2 — verbatim, no paraphrase.** Validators MUST NOT hand-write a suppression note (cci PASS1 set the §O.1 template; kal / hfg had to invent one). |
| report **mode** (1/2/3) | §3 | Standard / Activation / Reactivation |

**Mode resolution is by gate, not vibe (§3):** an org with zero eCat but a live invoice feed is **Standard**, not
Activation. `COMMERCE_CONFIDENCE = NONE` on the truth axis → **Activation** (behavior-only), regardless of volume.
`FEED_COMPLETENESS = STALE`/lapsed → **Reactivation**. Carry the profile's default mode only as the expectation; the
gate overrides it.

---

## Steps 2–6 — gather, detect, score, bundle, render

- **Step 2 — Data gather.** Execute the LIVE query set in [`../foundation/WHAT_ACTUALLY_RUNS.md`](../foundation/WHAT_ACTUALLY_RUNS.md)
  (`Q-ECON-00` first, then the gather/platform IDs in `config.QUERIES_ALL`). SQL bodies come from
  [`../foundation/query_library_v2.md`](../foundation/query_library_v2.md) (20), this operator's sibling
  [`rep_copilot_operator.md`](rep_copilot_operator.md) (`RP-2`, `RS-01`), and
  [`../foundation/selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md)
  (`S1`, `C2`). Apply the profile's house/sample/marketplace screen (§4) to every dispersion/leakage query.
- **Step 3 — Signal detection.** Per [`../report_product/signal_catalog_v4.md`](../report_product/signal_catalog_v4.md)
  / `pipeline/signals.py` (**14** detectors). The capability VM catalog (roadmap only) is
  [`../foundation/capability/value_moment_catalog.md`](../foundation/capability/value_moment_catalog.md) —
  do not load it to run.
- **Step 4 — Signal scoring.** `SIGNAL_RANK = surprise × dollar_impact × actionability`; a signal's confidence is
  `LEAST(its ceiling, COMMERCE_CONFIDENCE)`. A pattern explained by `industry_context.md` is **down-weighted as
  context, not scored as a finding.**
- **Step 5 — Context bundles.** One per section, each carrying its provenance stamps + the editorial rules from
  [`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md). **For §2 (Team)
  and §3 (Account) the bundles are *pulled from the per-entity operators*, not re-derived here — see Step 5a below.**
- **Step 6 — Section rendering.** Fixed positions (§5): Signal Summary · Team · Account · Commerce (leakage lives
  here, directional) · Product · Platform · Appendix. A section renders if ≥1 fired P0/P1 signal **or** its alternate
  gate passes **or** it has a query-driven subsection passing the specificity test. **When a section or subsection
  is suppressed by a gate (`Q-CHAN-00 = NONE / PARTIAL`, `COMMERCE_CONFIDENCE = NONE`, `REP_IDENTITY_TIER < 2`,
  `FEED_COMPLETENESS = STALE / DEAD`), the operator emits the canonical templates from
  [`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md) §O.1–§O.5
  verbatim** — do not paraphrase the suppression note. Step 10's §N.7 check enforces this.

---

## Step 5a — Per-entity wiring (§2 and §3 *consume* the per-entity operators)

This is the architecture §9 contract made runnable. The per-entity operators (rep copilot, rung-4 Option A, customer
brief v5.1) sit *below* this report — they already carry every gate, cap, and screen the Spine demands. **The report
does not re-derive their math; it renders the bundles they hand up.** Skipping this step is the defect that ships a
calibrated-but-low-density §2 / §3.

### 5a.0 — Invocation contract (CALL + CONSUME, do not re-author)

**This step is an INTERFACE fix, not an operator-layer redesign.** The report's job in 5a is to *invoke* the
per-entity operators (or their named sub-queries / cached outputs), parse the rows they return, and render them
into the §2/§3 templates below. The report MUST NOT contain a reimplementation of S1, C2, the v5.1 mini-brief
shape, or the RS-01 leaderboard logic.

| Sub-step | Invokes | Reads from | Emits into the report |
|---|---|---|---|
| 5a.0.1 | `rep_copilot_operator.md` §1 RP-1..RP-5 (preflight) | live PG via `Q-ECON-00` + RP-2 | `COMMERCE_CONFIDENCE`, `REP_IDENTITY_TIER`, `house_suspect` set, dormancy flag, `report_through_date`. **All of §5a.1/5a.2/5a.3 read these — do not re-run the preflights inside the §2/§3 builders.** |
| 5a.0.2 | `rep_copilot_operator.md` §3 RS-01 | the RS-01 SQL (verbatim, with `{{ORG_ID}}` + per-org house-rep EXCLUDE rows templated in from [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md)) | the §2 leaderboard table rows |
| 5a.0.3 | `rung4_option_a_operator.md` §2 (O1 + O2) | the O1/O2 SQL (verbatim, with `{{ORG_ID}}` + the same house-rep EXCLUDE template) | the §2 coaching-card rows ($-at-risk by rep + leak by rep) |
| 5a.0.4 | `../Customer Intelligence/operators/customer_brief_run_prompt.md` v5.1 §3/§15/§16 | the v5.1 per-account decay + §M block + §16 competitive-loss banner | the §3 mini-briefs + tail watchlist + §M Decline Investigation blocks |
| 5a.0.5 | `selling_customer_exception_layer.md` S1 (ordered by `dollars_at_risk DESC`, top 5) | S1 customer-grain | the seed list for §3 mini-briefs and the §3 outreach list |

**The invocation is sequential** (preflight → leaderboard → cards → mini-briefs → outreach), because every
later step is capped or gated by an earlier step's emit.

### Scope guard — STOP if you are rebuilding (the Sarreid lesson)

**If at any point inside §2 or §3 you find yourself writing a `WITH … MATERIALIZED` CTE for leakage, a custom
6-month-window CTE for $-at-risk, or a new `customer_bill_to_*` exclusion list, you are doing it wrong.** That
SQL already exists in the per-entity operators; the report's job is to call them and render the rows. Stop and
re-check that you are invoking the operator, not reimplementing it.

Symptoms of a 5a interface failure (each closes a PASS1 defect register entry — cci §C.2, kal §C.3):
- The §2 leaderboard renders a `HOUSE ACCOUNT` row at #1 → RS-01 was reimplemented without the rep-label screen.
- The §2 coaching cards have $-at-risk numbers but no "trace line" in the Appendix → O2 was reimplemented inline.
- The §3 mini-briefs print a v5.1-style 6mo/prior-6mo split but the Appendix has no v5.1 trace row → the brief
  was hand-authored, not consumed from `customer_brief_run_prompt.md`.
- The §3 outreach list was "built by hand from the §3 mini-briefs" with no `Q-OUTREACH` step in the Trace
  contract → the outreach list is being authored, not assembled.

Any of these → revert and call the operator. **If the per-entity operator does not exist (e.g. Tier-1/Tier-0
modes have no rung-4 card emit), the section degrades per 5a.1/5a.2 — never reauthors the missing operator.**

### 5a.1 — §2 Team bundle (3–5 coaching cards from `rung4_option_a_operator.md`)

**Run the rung-4 Option A operator** for `{org_shortname}` (Tier-2 admission gate per its §1; refuse below Tier 2 —
this report's §2 then stays prose-only, not card-rendered). The operator emits:

- **AXIS O — Outcome ($, ERP):** O1 = C2 leakage-by-rep (`Q-ECON-LEAK` rolled to `rep_number`, named via the Tier-2
  bridge, house-rep screened per [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md)); O2 = S1
  $-at-risk-by-rep (the §4 of `rep_copilot_operator.md` rolls S1 to the owning rep).
- **AXIS B — Behavior (Mixpanel, context):** C4 feature depth + C6 cadence/conversion. **Never a dollar.**

**Render in §2 — top 3–5 reps by AXIS-O dollars, as cards (NOT a prose paragraph):**

```
Card — <rep name (Tier-2 named)>
  $ at risk (S1):  $<X>K across <N> accounts  ·  Leak (C2):  $<Y>K / <Z>% (or — if no row)
  Behavior:        <one phrase from AXIS B, or "—" if unmatched / no Mixpanel coverage>
  Action:          <one concrete sentence — the named account, the cadence cue, this week / next quarter>
```

**Hard rules — non-negotiable, mirror rung-4 §3/§5:**
1. **Sort by AXIS-O dollars only** — S1 $-at-risk primary; C2 leakage secondary. Behavior never moves a rank.
2. **Every dollar carries its source label and traces to the operator's row.** No invented figures. If S1 returned
   `$0` for a rep, the card stays unrendered. If C2 returned no row for a rep ("no rogue"), that **cell is `—`**, not
   a fabricated leak figure. **Say plainly** in §2 prose when the whole org returned no coachable C2 — "Rung-4 found
   no rep above the discount-discipline threshold this run" — instead of manufacturing a card.
3. **No fused number.** Do not multiply S1 × C2, do not blend behavior into a single "coached-dollar." Two columns,
   two confidence labels, one human-written `Action` sentence.
4. **PARTIAL feed → floor.** Per `COMMERCE_CONFIDENCE`: `STRONG` ships the figure; `PARTIAL` renders "≥ $X (floor)";
   `NONE` suppresses the card entirely (Tier-2 alone doesn't unlock the dollar — the gate must too).
5. **Tier 1 / Tier 0 orgs:** §2 falls back to the rep copilot's RS-01 leaderboard (`rep_number`-grain or behavior-only
   per the identity tier). No cards rendered in this mode — say so plainly in one sentence.
6. **The top-10 RS-01 leaderboard table is still rendered** (it remains the org's at-a-glance roster). The cards sit
   *above* the table, not in place of it — they are the **action layer** the leaderboard alone never produced.

### 5a.2 — §3 Account bundle (5 mini-briefs + tail watchlist, from the customer brief v5.1 operator)

**Pull the top 5 accounts by `dollars_at_risk` from S1** (per-account decay, equal 6-month windows anchored on
`report_through_date`, billing-entity grain — verbatim from `selling_customer_exception_layer.md`). For each, render
a **mini-brief in the v5.1 shape** (`Customer Intelligence/operators/customer_brief_run_prompt.md` §3 / §15 / §16
contract — consume, do not re-derive):

```
### <Account name>  (<rep label> · rep <rep_number>)
  Invoiced LTM:   $<X>K           Recent 6mo:  $<a>K     Prior 6mo:  $<b>K     Recent vs prior:  <±n>%
  Last invoice:   <YYYY-MM-DD>    Days silent: <n>       Lifetime invoices: <n>
  The read:       <one sentence — what the slope is, what the cadence says, whether it's decline or cadence-cliff>

  [IF (recent_vs_prior_pct < -25% AND ltm_rev > $50K) — editorial §M fires:]
  > Decline Investigation — <Account> (per editorial rule §M):
  > Possible reads: competitive displacement; territory/buyer change; deliberate channel shift; product/pricing
  > change on specific SKUs. None of these is in the data — they are the investigative paths for <rep> this week.
```

**Hard rules:**
1. **Pull the §16 competitive-loss banner where the v5.1 gate fires** (`total_business_source = INVOICES` AND
   `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}`) — the customer brief operator emits the directional/relabeled
   form on PARTIAL/STALE. The banner rides above the mini-brief, never inside it.
2. **The §M Decline Investigation block fires only on >25% decline on >$50K accounts.** Cadence-cliff accounts
   (decay-by-silent-gap but revenue flat or growing) get **no §M block** — they get a one-line cadence read instead.
   Never invent a hypothesis on a non-declining account.
3. **Tail watchlist stays as a short table for the rest** (`Plus N more dealers, $XK total LTM at risk`). The top 5
   are mini-briefs; positions 6+ are rows.
4. **K7 leakage at customer grain is directional** (per v5.1 Step F) — surface only as a separate directional line
   beneath the mini-brief when present and `house_suspect = false`; **never bake a hard K7 dollar into a client face.**

### 5a.3 — "This Week's Outreach List" (5–7 named accounts; appears at end of §3)

The single most operability-restoring element the 3.0 reports carried that 4.0 dropped. Built **from the same S1
mini-brief substance** assembled in §3 — no new economics layer, just a tighter render:

```
| # | Account | Rep | Action | Talking point (one line) | Timing |
|---|---------|-----|--------|--------------------------|--------|
| 1 | <name>  | <rep> | <verb> | "<one-sentence cue tied to the slope or cadence>" | this week / next quarter |
```

**Selection:** top 5–7 named accounts from the §3 mini-briefs, ordered by *actionability × dollars-at-risk* — a
30-days-silent decline outranks a 5-days-silent cadence-cliff at the same LTM. **Tier-2 only for rep names.** No
account appears here without an LTM `$-at-risk` traced to S1 (or, on cadence-cliff cases, an LTM figure traced to
CQ-01); no card lists a coaching action without a customer brief / rep copilot row behind it.

---

### Trace contract (Step 10 still applies)

Every dollar a §2 card or §3 mini-brief renders **must** trace, in the Appendix `Traceability` block, to the operator
row it came from:

| Render site | Trace line |
|---|---|
| §2 coaching card `$-at-risk` cell | `rung4_option_a_operator.md` AXIS O, O2 / S1 by-rep (rep `{rep_number}`) |
| §2 coaching card `Leak` cell | `rung4_option_a_operator.md` AXIS O, O1 / Q-ECON-LEAK by-rep (rep `{rep_number}`) |
| §3 mini-brief LTM / 6mo split | `selling_customer_exception_layer.md` S1, customer `{customer_bill_to_number}` |
| §3 §M Decline Investigation block | editorial rule §M (decline >25% on >$50K) — hypothesis, not finding |
| §3 outreach list rows | §3 mini-brief LTM + S1 by-account; rep label per `rep_copilot_operator.md` Tier-2 bridge |

If a render site **does not have a trace line in this table**, delete the figure in Step 10 — do not patch it in.

---

## Step 5b — Mode-2 (Activation / NONE-feed) and gate-STOP templates

Mode-1 (the Sarreid worked example) assumes the org clears every gate Sarreid cleared. Many orgs do not.
This step defines what the operator emits when a gate fails — **so the output is deterministic and validators
do not invent the wording on the fly** (PASS1 hfg / sca register entries §C).

### 5b.1 — Mode resolution (which template fires)

| Gate state | Template | Sections that render |
|---|---|---|
| Mode 1 — Standard (Sarreid baseline) | the §0-§10 flow above | §1–§6, full |
| Mode 1 — Tier-1 degraded (`REP_IDENTITY_TIER = 1`, `COMMERCE_CONFIDENCE ≥ PARTIAL`) | the §0-§10 flow with §2/§3 §5a.1 fallback | §1, §2 (RS-01 at `rep <n>` grain; **no coaching cards**), §3 (mini-briefs with `rep <n>` cells), §4 (leakage runs; subsections suppressed for cause), §5, §6 — render a one-sentence note in §2 prose: *"§2 coaching cards do not render below Tier 2 — see Appendix"* |
| **Mode 2 — Activation / Tier-0 / NONE-feed** (`COMMERCE_CONFIDENCE = NONE` OR `REP_IDENTITY_TIER = 0`) | **the Mode-2 template in §5b.3 below** + **formal redirect to `rep_copilot_operator.md`** | §1 (non-dollar findings only), §6 (eCat behavior) — everything else suppressed for cause |
| **Gate-STOP** (`COMMERCE_CONFIDENCE = NONE` *and* eCat capture missing or below materiality, OR Step 0 has no ratified profile, OR a hard preflight fails) | **the Gate-STOP template in §5b.2** | header + gate table + recommended next action only; **no report body, no per-rep / per-customer rendering** |

**Mode resolution is by gate, not vibe (§3).** The profile's default mode is the *expectation*; the gate
overrides it. PASS1 lesson: hfg / sca both required validators to invent the STOP artifact shape — that is now
deterministic via §5b.2 / §5b.3 below.

### 5b.2 — Gate-STOP artifact format (used by hfg, sca, any org that fails Step 0 or Step 1 hard)

When an org does not clear the gates Sarreid cleared, emit this exact shape — **no report body**:

```
# {Org name} — Selling & Commerce Intelligence  *({PASS|run} — VALIDATION ARTIFACT, GATE-FAILED)*
### Insightful Report · Did not clear the gates Sarreid cleared — STOP, do not ship.

> **This is a {pass1|run} output.** Generated by running the Layer-1 preflights from
> `operators/report_operator.md` against `{org}` (org {ORG_ID}). The operator's spec says: *"If an org does NOT
> clear the gates Sarreid cleared, STOP on that org and report why — do not force a report through a failed
> gate."* {org} does not clear {n} of them. This file documents which gates failed; no full report is generated.

## Bottom line

| Gate | Sarreid (worked example) | {org} | Verdict |
|---|---|---|---|
| Step 0 — ratified profile (`profiles/{org}.md`) | RATIFIED `sarreid.md` | {state} | {PASS|FAIL} |
| Step 1 — `COMMERCE_CONFIDENCE` | STRONG | {value} | {PASS|FAIL} |
| Step 1 — `REPORT_INTELLIGENCE_TIER` | STRONG | {value} | {PASS|FAIL} |
| Step 1 — `REP_IDENTITY_TIER` | Tier 2 (100% bridge) | {value} | {PASS|FAIL — by N pp if Tier-1 boundary} |
| Step 1 — `Q-CHAN-00` channel availability | {sarreid_value} | {value} | {PASS|FAIL} |
| Step 1 — `FEED_COMPLETENESS` | UNVERIFIED-SINGLE-FEED | {value} | {PASS|FAIL} |
| Step 1 — eCat capture present | YES ($2.05M) | {value} | {PASS|FAIL} |

**Conclusion.** {one paragraph: name the failed gates verbatim, cite the operator section that says STOP,
state the structural consequence (e.g. "§2 coaching cards do not render below Tier 2"). For NONE-feed orgs,
**name the formal redirect to `rep_copilot_operator.md`** (see §5b.3 below).}

## What the preflights returned

### Q-ECON-00 (economics preflight)
| Output | Value |
|---|---|
| `TOTAL_BUSINESS_SOURCE` | {INVOICES|ORDERS|NONE} |
| `n_inv` (LTM) | {n} |
| `inv_ltm_net` | ${X} |
| `report_through_date` | {YYYY-MM-DD or NULL} |
| `commerce_confidence` | {STRONG|PARTIAL|LIMITED|NONE} |
| `salesdata_over_invoiced` | {ratio or undefined} |
| {add side-channel availability flags as they fire — freight_pct, terms_pct, carrier_pct, credit_memos, etc.}

### RP-2 (rep identity tier)
| Output | Value |
|---|---|
| `distinct_repnum` (invoice reps, LTM) | {n} |
| `resolves_to_name` | {n} |
| `name_bridge_pct` | {%} |
| `rep_identity_tier` | {0|1|2} |

### Q-CHAN-00 (channel availability)
| Output | Value |
|---|---|
| `booked_rows` (LTM) | {n} |
| `distinct_origins` | {n} |
| `ecat_tag_status` | {RELIABLE|PARTIAL|NONE} |
| `channel_confidence_gate` | {STRONG-CANDIDATE|PARTIAL|NONE — SUPPRESS channel section} |

## Recommended next action (recommendation only — no canon change made)

{ordered list — name the smallest unlock that would re-qualify the org (backfill N rep_names, populate
order_origin, ratify a profile, etc.). Do NOT recommend pushing the report through anyway.}

`[{org} {run-label} · {YYYY-MM-DD} · STOP at {gate names}]`
```

**This format is binding.** Validators who add or omit fields are off-canon; deviations must round-trip
through this operator, not the output. The hfg and sca PASS1 outputs are the worked examples.

### 5b.3 — Mode-2 (Activation / NONE-feed) template + the formal Rep Copilot redirect

When `COMMERCE_CONFIDENCE = NONE` on the truth axis (no `portal_invoices` rows, or invoiced feed is DEAD),
the report operator **does not run its body** — it emits the §5b.2 gate-STOP artifact AND **formally redirects
to `rep_copilot_operator.md`** with the exact text below. This is the "report operator does not run on
behavior-only orgs" handoff that PASS1 sca had to invent.

**Formal redirect text (verbatim — paste into the gate-STOP "Conclusion" paragraph):**

```
The report operator's correct exit on {org} is to redirect to the **Rep Copilot operator**
(`operators/rep_copilot_operator.md`), which is ERP-optional by design and runs in its Tier-0
behavior-only branch (§2). Run:

   "run the rep copilot for {org}"

That operator will emit the R1–R4 behavior layer (logins, order authorship, feature depth where
Mixpanel coverage allows). It will NOT emit any rep → revenue claim, because `COMMERCE_CONFIDENCE
= NONE` forbids it. The two-section behavior-only render (§1 non-dollar findings + §6 eCat behavior)
is the correct ceiling for {org} until an invoice feed arrives.
```

**If the operator is asked to push through anyway (Mode-2 degraded run):** render only §1 (with non-dollar
findings — e.g. user-grain concentration via the rule below) and §6 (eCat behavior). Suppress §2, §3, §4, §5
in full with the canonical suppression text from `report_editorial_rules_v4.md` §N.5. Do **not** render
RS-01 (no `rep_number`), do **not** render S1 mini-briefs (no `portal_invoices`), do **not** render the
leakage subsection (no priced lines). The result is structurally a 2-of-6-section report and **the header
must say so** ("Mode 2 — behavior-only; 4 of 6 sections suppressed for cause").

**User-grain concentration rule (Mode-2 only, fires when truth axis is NONE):** if a single `org_user_id`
accounts for `> 80%` of LTM eCat GMV, surface as a **structural-concentration finding**, not a coachable
performance finding. This is the sca-pattern rule — the operator's concentration logic is otherwise
account-grain; in Mode-2 with no account-grain data, user-grain concentration is the only legible signal.

---

## Steps 7–10 — summarize, assemble, verify

- **Step 7 — Signal Summary (built last).** Top 5–7 by `SIGNAL_RANK`, re-sorted into the narrative arc
  (momentum → intelligence → opportunity → risk); diversity max 4 from one section; **≥3 positive findings and
  finding #1 positive** (the tone-balance test).
- **Step 8 — Assembly.** Fixed render order. Write to `../outputs/{Org}_CEO_intelligence_report_{report_through_date}.md`.
  (Route B will later emit the 3.0 HTML shell with the four provenance `data-*` root attributes from §8 — not built here.)
- **Step 9 — Structural verification.** All mandatory subsections present; the four `data-*` posture values consistent.
- **Step 10 — The verification ledger (13 checks, the gold-bar render gate).** Re-read every dollar against
  the three-tag rule, then run the full editorial-gate set, then run the structural / numerical / live-parity
  checks. **No output ships unless every check below passes.** This ledger consolidates the PASS1 patch (§N.1–§N.7)
  with the 2026-06-30 gold-stamp absorption (§P/§Q/§R/§S editorial gates + ledger checks 8–13). See
  [`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md) §N + §P–§S for
  the gate bodies.

  ```
  [1]  Three-tag dollar pass (HTML + MD)         →  every dollar has [source · confidence · completeness]
                                                    AND traces to a query in the Appendix; DELETE any that
                                                    doesn't (§D + §N.5 + §S).
  [2]  §N.1–§N.7 PASS1 gate set                  →  HOUSE-LEAK (HALT) · FM9-CHANNEL-LEAD (DELETE) ·
                                                    CROSS-ORG-LEAK (DELETE) · CUTE-METAPHOR (DELETE) ·
                                                    UNTRACEABLE-ARITHMETIC (DELETE) · VISUAL-CUE (DELETE) ·
                                                    CHANNEL-NONE-SUPPRESSION (REPLACE with §O template).
  [3]  §P forbidden-vocabulary regex sweep (HTML)→  0 hits in customer-facing copy; HALT on any hit not in
                                                    the §P.2 allow-list.
  [4]  §P forbidden-vocabulary regex sweep (MD)  →  0 hits; same rule. The MD must pass independently — the
                                                    Sarreid lesson: a QA pass that treats only the HTML as
                                                    canonical leaks NRR / cohort / playbook into the MD.
  [5]  §Q sensitivity-hedge gate                 →  every Tier-A/S claim (§1 / §2 / §3 cards + plays /
                                                    Priority Actions) has one of N marker-phrase
                                                    sensitivities within ±400 chars; HALT on miss.
  [6]  §R concentration-check gate               →  any "broad-based" / "spread" / "diversified" framing
                                                    fails if top-1 ≥ 25% OR top-10 ≥ 40% OR HHI ≥ 1500 on
                                                    the underlying $-lift; HALT and REPLACE with §R.5
                                                    canonical template.
  [7]  §S addressable-base check                 →  every "+$X per N-pt" claim carries an addressable-base
                                                    footnote OR a full-vs-addressable range; DELETE per
                                                    §N.5 if neither.
  [8]  Number reconciliation (HTML ↔ MD)         →  every figure that appears in 2+ sections (the per-run
                                                    "key numbers list" — Sarreid had 25) matches to the
                                                    dollar across HTML and MD; 0 mismatches. The list is
                                                    generated from the gather output, not hand-curated.
  [9]  Verbatim 12-word phrase echo (HTML)       →  0 repeated 12+ word phrases across §1 / §2 / §3 / §5
                                                    headers, sub-headers, and callouts; the post-render
                                                    dedup pass removes any echo found (Sarreid had one
                                                    between hero and §5 sub).
  [10] Verbatim 12-word phrase echo (MD)         →  0; same rule, run independently against the MD.
  [11] HTML structure pairing                    →  every `<details>` / `<section>` / `<table>` opens and
                                                    closes; every `id` attribute is unique; every nested
                                                    disclosure (§2 "How these were chosen") is well-formed.
  [12] In-document anchor link resolution        →  every `<a href="#anchor">` resolves to an `id` that
                                                    exists in the same document; 0 broken anchors. The sticky
                                                    TOC strip must resolve cleanly.
  [13] Topline live-query parity (re-pull)       →  re-run `Q-ECON-00` for `{ORG_ID}` and compare the LTM
                                                    invoiced $, YoY %, dealer count, and `report_through_date`
                                                    on the headline against the gather output written to the
                                                    Appendix Traceability block; 0 mismatches. Catches the
                                                    case where the headline number was hand-edited or stale.
  ```

  **The ledger is binding.** A run that ships without every check passing is non-compliant, regardless of
  how good the prose reads. Each HALT requires a real upstream fix and a re-render — the operator does
  not patch around a HALT, and the operator does not silently strip / substitute tokens on a DELETE.

  **Per-run logging.** Append the ledger pass/fail summary to the Appendix Traceability block of every
  shipped output so the gate state is greppable across the cohort:

  ```
  [STEP-10 LEDGER · {org} · {YYYY-MM-DD HH:MM} · 1:pass 2:pass 3:pass 4:pass 5:pass 6:pass
                                                  7:pass 8:pass 9:pass 10:pass 11:pass 12:pass 13:pass]
  ```

  Then run the static checker.

---

## The determinism contract (why a re-run reproduces the report)

The data layer is already deterministic; this contract pins the interpretation layer so the same operator + same
profile + same data produce the same report:

1. **Context comes from the profile, not the model.** Business model, channel model, house/sample screen, buyer-type,
   structural concentration, identity disambiguation — all read from `../profiles/{org}.md`. No ad-hoc inference.
2. **Mode and caps come from the gates, not judgment.** `Q-ECON-00`/`FEED_COMPLETENESS`/`REPORT_INTELLIGENCE_TIER`
   decide mode and the confidence ceiling; the model cannot raise them.
3. **Every dollar is provenance-stamped and query-traceable**, or it is deleted in Step 10.
4. **Rep naming is tier-gated** — never name a rep below Tier 2.
5. **Hard gaps are suppressed, never approximated** (margin/COGS, AR/DSO, returns, stock-outs, carrier/damage,
   segmentation) — surfaced as the "with connected data" upsell, per the profile's confirmed suppressions.
6. **Leakage stays directional** client-facing, with a **mandatory human gut-check** before any leakage dollar ships
   (the asi "$1.35M / 42%" false-positive lesson — normal 2.1% once tiers/volume/house were excluded).
7. **Industry-normal ≠ finding.** Anything `industry_context.md` explains is context; the report spends its surprise
   budget on what's specific to this client.

---

## Relationship to canon

| Doc | Role for this operator |
|---|---|
| [`../CANON.md`](../CANON.md) | precedence + the four-input reading contract this operator enforces in Step 0 |
| [`../report_product/report_product_architecture.md`](../report_product/report_product_architecture.md) | the spec; Steps 1–10 are its §6 sequence made runnable |
| [`../report_product/signal_catalog_v4.md`](../report_product/signal_catalog_v4.md) | signal detection/scoring/output format (Step 3–4) |
| [`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md) | voice + three-tag dollar rules (Step 5–10) + **§N render-time editorial enforcement** (Step 10) + **§O canonical suppression templates** (Step 6) + **§P forbidden-vocab regex sweep** / **§Q sensitivity-hedge gate** / **§R concentration-check gate** / **§S addressable-base rule** (Step 10 ledger, gold-stamp 2026-06-30) |
| [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md) | **rep-label house screen** — AUTO-RULE + per-org EXCLUDE list, consumed by RS-01 / rung-4 O1/O2 (Step 5a) |
| [`../foundation/provenance_spine.md`](../foundation/provenance_spine.md) | Tier-0 truth; caps everything; wins all conflicts |
| [`../foundation/query_library_v2.md`](../foundation/query_library_v2.md) | the SQL bodies (Step 1–2) |
| [`../foundation/selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md) | S1 + C2 feeding Account/Team/Commerce |
| [`rung4_option_a_operator.md`](rung4_option_a_operator.md) | **§2 Team coaching cards** (Step 5a.1) — Tier-2 only; consume O1 (C2 by-rep) + O2 (S1 by-rep); never blend a fused number |
| [`rep_copilot_operator.md`](rep_copilot_operator.md) | **§2 Team leaderboard + identity** (Step 5a.1) — RS-01 invoiced + house flag + Tier-2 name bridge |
| `../Customer Intelligence/operators/customer_brief_run_prompt.md` (v5.1) | **§3 Account mini-briefs + outreach list** (Step 5a.2/5a.3) — consume S1 + K7 + competitive-loss banner; never re-derive |
| `../profiles/{org}.md` | reading-contract input #2 — the cached, ratified context (Step 0) |
