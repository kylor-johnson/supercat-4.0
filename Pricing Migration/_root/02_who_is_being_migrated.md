# 02 — Who Is Being Migrated

> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: `_reference/2026-05-20__execution_plan_v3.3.md` §II + §IV + §VI; `_master-account-data-v6.2.csv`; `migration_comm_tiers_2026-05-19.csv`; archived `_handoff-prompt.md` §Data Corrections (explicitly-directed extraction per `_root/CONTRACTS.md` §4)
>
> **What this doc owns**: The 8 migration segments (names, definitions, account counts, deltas, owners). The $200 / $400 / $600 ownership boundary that triages who owns the comm. The entity overlay rule. The health-override triggers (VD<40, Watch, At Risk, Critical). The annual overlay and its consequence for cohort timing. The June / July / Deferred cohort assignment. The five known routing-CSV errata. The roster pointer (the 109-account roster lives in v6.2 CSV) and the 109 / 107 / locked-pricing reconciliation.
>
> **What this doc DOES NOT own**: Segment → format mapping (Format A / B / CEO Letter / Good News) — that is `_root/06`. Per-segment driver framing — `_root/05`. Voice / tone differences by health band — `_root/04`. Data-loading mechanics — `_root/07`. The verbatim text of the WHY thesis — `_root/01`.

---

## 1. The 8 migration segments

The 8-segment vocabulary is set by `_reference/2026-05-20__execution_plan_v3.3.md` §II. Names are stamped — they are not renamed, reordered, or "improved" anywhere in the system. The vocabulary replaces the v3.0 4-cohort risk framework and the v3.2 5-segment framework (the §"What Changed v2 → v3.3" table in the exec plan documents that transition); the 8 here are the current operating vocabulary.

The numbers below come from `_master-account-data-v6.2.csv`, filtered to `migration_status = 'migration_pending'` (107 accounts; see §8 for the reconciliation between this 107 and the v6.2 total of 109). All segment counts and Δ MRR totals reconcile cleanly with exec plan v3.3 §II.

| Segment | Definition (routing logic) | Accts | Avg Δ MRR | Median Δ MRR | Owner | Notes |
|---|---|---:|---:|---:|---|---|
| **Tailwind** | Δ ≤ $0 (price flat or decreasing) | 6 | −$136/mo | −$96/mo | Kylor (CS) | Deferred — each month of delay preserves higher legacy revenue; Good News Notice is the entire comm. |
| **Core** | $0 < Δ ≤ $200, healthy, standalone | 13 | +$105/mo | +$134/mo | Kylor (CS) | June cohort; digital-first; Standard Migration Notice + simplified value summary. |
| **Narrative** | $201 ≤ Δ ≤ $400, healthy, standalone | 15 | +$311/mo | +$305/mo | Kylor (CS) | June cohort; digital-first; Value Migration Notice + simplified value summary. |
| **Executive** | $401 ≤ Δ ≤ $600, healthy, standalone | 8 | +$485/mo | +$492/mo | Kylor + CEO (co-authored) | July cohort; full bespoke artifact + CEO exec letter. $400 is the **ownership boundary** (§2). |
| **Pre-Engagement** | Δ > $600, healthy, standalone | 8 | +$692/mo | +$676/mo | CEO (CEO + CS) | July cohort; full bespoke artifact + CEO-initiated call before notice. |
| **Entity** | Multi-brand child account (overlay rule, §3) | 27 | +$404/mo | +$388/mo | CEO + Kylor | June cohort; entity packet IS the notice; serves as high-fidelity pilot for July cohort. |
| **Strategic** | Watch / At Risk / VD<40 / HVLG (override rule, §4) | 19 | +$253/mo | +$169/mo | CEO | Deferred / post-migration; CEO-led conversation precedes notice; walk-away thresholds pre-authorized. |
| **Annual** | `deal_type = 'Annual'` (overlay rule, §5) | 11 | +$211/mo | +$24/mo | Kylor + CEO | Renewal-driven timing; substance matches natural segment; ≥90-day notice. |
| **Total** | | **107** | | | | **Aggregate Δ = +$32,653/mo** |

The 8-segment vocabulary is the authoritative way to talk about *what kind of customer is being migrated*. The 4-format vocabulary (Format A / Format B / CEO Letter / Good News) — which is *how a customer gets communicated to* — is the routing layer and lives in `_root/06`.

---

## 2. The ownership boundary — $200 / $400 / $600

The dollar-delta thresholds triage who owns the comm. They exist because the binding constraint on this migration is CEO bandwidth (2-person CS team), not customer sophistication. The threshold is the mechanical way to keep CEO time on the largest deltas without informally drifting through the list.

- **Δ ≤ $200/mo** → CS-owned. Kylor delivers the artifact and notice. (Core segment.)
- **$201 ≤ Δ ≤ $400/mo** → CS-owned, value-led. Kylor delivers; no CEO authorship required. (Narrative segment.)
- **$401 ≤ Δ ≤ $600/mo** → CEO co-authored. Kylor still executes delivery; CEO signs and is visible. (Executive segment.)
- **Δ > $600/mo** → CEO-owned. CEO initiates a call before notice is sent. Kylor executes. (Pre-Engagement segment.)

$400 is the **ownership boundary** — it is the point at which CEO authorship becomes structurally required, regardless of customer health or tenure. $600 is the **engagement boundary** — it is the point at which a CEO-initiated conversation precedes the notice rather than accompanying it.

Two exceptions to the pure-Δ triage are detailed below: the **entity overlay** (§3) and **health overrides** (§4). The corresponding `comm_action` values in `migration_comm_tiers_2026-05-19.csv` (e.g. *CEO Pre-Call → Format B*, *CEO Letter + Call Commitment*) are owned by `_root/06_format_routing.md`; this doc owns only the dollar thresholds that drive the ownership decision.

---

## 3. The entity overlay rule

An **entity** in this system is an organizational parent that owns two or more child SuperCat accounts. v6.2 carries the entity relationship in the `parent_entity` column — there is no dedicated boolean flag. The operational rule is: **a row is an entity child iff `parent_entity` is non-empty and `parent_entity != company`.** When that condition holds, the entity overlay applies.

The entity overlay says: **any child account of a multi-brand parent routes to the Entity segment regardless of its individual Δ**, and the entity receives a single coordinated treatment via one entity packet covering all child brands. The overlay's rationale is consistency of relationship. Entity parents (e.g. Gabriella White, Visual Comfort & Co., Godinger Group) deal with SuperCat at the parent level; sibling-brand asymmetry — one child treated as Core, another as Pre-Engagement — would produce internal contradiction that the parent would surface back to SuperCat. The entity packet preempts that by framing the migration at the entity level, with per-brand pricing detail underneath.

**v6.2 figures (migration_pending only):**

- Distinct `parent_entity` values among `migration_segment = 'Entity'` rows: **16** (Gabriella White, Visual Comfort & Co., WAC Group, Godinger Group, Creative Home Furniture, Thesis, Abaline, Interlude Home, Jonathan Charles, Litex Industries, Maxim Group Lighting, Cordelia Lighting, Samson Holdings Ltd, Hearthstone Enterprises, Classic Home Inc, Holladay Design Group).
- Total Entity-segment child accounts: **27**. Matches exec plan v3.3 §II exactly.
- Several multi-brand entities have children that route OUT of the Entity segment via the overrides in §4: HVLG (3 children → Strategic, VD=0), Coleto Brands (2 children → Strategic + Annual, Watch-band), Rock House Farm (2 children → Strategic, Watch-band), Ferguson Enterprises (2 children → Tailwind, net-negative). They do not appear in the Entity-segment count of 27. The entity packet still covers them (per exec plan v3.3 §II, "Mixed-segment entities: packet covers ALL children including Strategic-routed ones, maintaining entity consistency"). Counting these entities as well, the operational scope is **~17 packets covering ~33 child accounts**, matching exec plan v3.3 §II.

The CEO is involved in every entity-parent conversation. **Entity-level concessions only** — no brand-by-brand improvisation without CEO approval. (The detailed entity playbook lives in exec plan v3.3 §II + §V; this doc owns only the overlay *trigger*.)

---

## 4. Health overrides — VD<40, Watch, At Risk, Critical

Health is computed as a composite of the four sub-scores carried in v6.2 CSV: `engagement_score`, `adoption_score`, `value_delivery_score`, `operational_health_score`. The composite is weighted 25 / 20 / 35 / 20 per the v3.3.2 rebalance, producing the `health_score` (0–100) and the `health_band` label (Thriving / Healthy / Watch / At Risk / Critical / Unscored). The weighting and band thresholds are inputs to this doc — they are owned by the health scoring system, not by this folder.

Per exec plan v3.3 §VI, two override rules apply to *segment routing*. **This doc owns only the trigger** (the bands and thresholds that fire the override); the override's downstream effects are owned elsewhere:

1. **`value_delivery_score` < 40 (the VD<40 rule).** Forces the account into a Watch-or-worse operating posture regardless of the composite score. The justification is mechanical: an account whose value-delivery sub-score has cratered is by definition not realizing the platform's value, and the migration cannot be framed as a value-led transaction with that account. v6.2 reports **14 VD<40 accounts** among pending; 13 are already routed to Strategic in v6.2, and 1 (Lucas McKearn) sits in Annual because the annual overlay (§5) supersedes the health override on timing.
2. **`health_band` ∈ {Watch, At Risk, Critical} (the Watch-band rule).** Routes the account to Strategic regardless of Δ. v6.2 reports **20 Watch-or-worse accounts** among pending; 17 are in Strategic, 2 are in Annual (annual overlay supersedes timing), and 1 sits inside an Entity packet (the entity overlay supersedes — the parent's treatment governs).

The two rules overlap heavily in v6.2 — most VD<40 accounts are also Watch-band — but both triggers fire independently. An account satisfying either condition routes to Strategic.

The health override has two downstream consequences, both owned elsewhere:

- **Voice** — the lede block of the artifact changes. A Watch-band lede is structured around the gap, not around the value proof. Owned by `_root/04` §health-band-overrides.
- **Routing** — the format selection may be downgraded so that CEO involvement is preserved (e.g. a Watch-band account that would otherwise route as Narrative or Executive becomes Strategic with a CEO-led conversation). Owned by `_root/06`.

This doc owns only the **trigger** — the bands and the VD<40 threshold that fire the override. It does not own the voice consequence (`_root/04`) and does not own the routing consequence (`_root/06`).

**Critical-band per-account exception (operator-stamped 2026-05-22).** While Watch and At-Risk accounts route deterministically to Strategic with deferred-then-drafted handling, Critical-band accounts (`health_band = 'Critical'`) have **no band-level rule**. The routing CSV's `post_hold_action` column carries the per-account decision — observed values include both `"NOT migration — separate health intervention program"` (account exits the migration motion entirely into a separate health workflow; no migration notice ever drafted) and standard format values that follow the defer-and-draft pattern. The operator decides per-account at routing-CSV maintenance time. `_root/06 §4.2` is the canonical owner of the Critical-band handling rule; this cross-reference exists so the segment-roster math above (20 Watch-or-worse → 17 Strategic / 2 Annual / 1 Entity) does not silently assume Critical-band accounts will always be drafted post-stabilization. Drafters reading a Critical-band row consult `post_hold_action` directly rather than defaulting to the Strategic / draft-eventually pattern.

---

## 5. Annual overlay

The annual overlay is the third routing-overriding rule (after entity and health). Accounts with `deal_type = 'Annual'` in v6.2 carry a contractual ≥90-day notice requirement before renewal (60-day minimum + 30-day buffer per exec plan v3.3 §III). The consequence is that timing — not segment — drives execution: annual accounts are noticed off the **renewal calendar**, not the **billing cohort calendar**.

The overlay's consequences:

- An annual account whose renewal falls inside the standard cohort window may be routed to a **deferred** cohort (`notice_cohort = 'Renewal-Based'` in v6.2) so the standard cohort timing does not violate the 90-day notice clock.
- The notice **substance** still uses the variant that matches the account's natural segment characteristics (Core / Narrative / Executive / Pre-Engagement / Strategic) — the annual overlay changes timing only, not content. Notice template selection is owned by `_root/06`.
- An annual account with an imminent renewal (<90 days from today) is fast-tracked. This is a per-account operator judgment; the renewal-date audit conducted during the readiness sprint surfaces which accounts qualify.
- Annual entity-children (e.g. Coleto Brands | Progress Lighting, Jonathan Charles | annual brand) are coordinated with the entity packet and parent conversation — the entity overlay still supersedes on segment label and ownership; the annual overlay supersedes on timing.

v6.2 reports **11 annual accounts** among pending (`deal_type = 'Annual'`), all carrying `migration_segment = 'Annual'` and `notice_cohort = 'Renewal-Based'`. The annual cohort total Δ is +$2,321/mo, matching exec plan v3.3 §IV. (Note: v6.2 also carries 1 already-migrated annual account — CopperSmith — which counts toward the 109 total but not toward the 107 pending; see §8.)

---

## 6. Cohort assignment — June / July / Deferred

The cohort assignment IS rule-bound. It flows from the 60-day notice window (structural / contractual) + the annual overlay + the strategic ordering of which segments go first. It is not an operator preference. Per exec plan v3.3 §IV:

```
Notice before July 1  →  new pricing Sept 1  →  first new-rate invoice Oct 1
Notice before Aug 1   →  new pricing Oct 1   →  first new-rate invoice Nov 1
```

| Cohort | Send window | Earliest enforceable effective date | Accounts | Δ MRR | Segments included |
|---|---|---:|---:|---:|---|
| **June** | June Weeks 1–4 (target: notice before July 1) | Sept 1 (P&L Oct 1) | 55 | +$16,928/mo | Entity (27) + Core (13) + Narrative (15) |
| **July** | July Week 1 (target: notice before Aug 1) | Oct 1 (P&L Nov 1) | 16 | +$9,417/mo | Executive (8) + Pre-Engagement (8) |
| **Deferred** | Post-July, calendar varies | Per-account | 36 | +$6,308/mo | Tailwind (6) + Strategic (19) + Annual (11) |
| **Total** | | | **107** | **+$32,653/mo** | |

In v6.2 the Deferred bucket is split across three `notice_cohort` values that preserve the per-segment timing logic:

| `notice_cohort` value | Segment | Accounts | Δ MRR | Timing rationale |
|---|---|---:|---:|---|
| `Deferred` | Tailwind | 6 | −$813/mo | Deliberately last — each month of delay preserves higher legacy revenue. |
| `Post-Migration` | Strategic | 19 | +$4,800/mo | CEO-led conversations, no time pressure, no overlap with main cohorts. |
| `Renewal-Based` | Annual | 11 | +$2,321/mo | Renewal-date driven (≥90-day notice window per §5). |

The three roll up to the 36-account Deferred cohort the exec plan describes (6 + 19 + 11 = 36, Δ = +$6,308/mo). The split inside v6.2 is a routing convenience; the strategic intent is the single Deferred cohort.

The 60-day notice window is **structural** (regulatory / contractual); the cohort timing flows from the notice window + the annual overlay + the strategic ordering of which segments go first. The cohort assignment IS rule-bound. It is not an operator preference. Cohort counts cross-check cleanly between exec plan v3.3 §IV and v6.2 CSV — no discrepancies to resolve.

---

## 7. The five known routing-CSV errata

`migration_comm_tiers_2026-05-19.csv` contains five known errors caught during the pre-refactor drafting. They are not yet baked into the CSV itself. Until they are, every routing decision must cross-check against this list. The corrections are recorded both here (because the segment roster is canonical) and in `_root/06_format_routing.md` (where the routing decision is owned).

Extracted per the explicit per-prompt authorization in §7 of this prompt (per `_root/CONTRACTS.md` §4, "explicitly-directed extraction" exception) from `_archive/2026-05-22__pre-refactor/_handoff-prompt.md` §Data Corrections:

| `ord_id` (account) | Routing-CSV value | Corrected value | Reason |
|---|---|---|---|
| `rac` (Godinger) | CEO Letter | CEO Pre-Call → Format B | Δ +$734/mo ≥ $600 ownership boundary |
| `wac` (WAC Group) | CEO Letter | CEO Pre-Call → Format B | Δ +$744/mo ≥ $600 ownership boundary |
| `sbl` (WAC Group) | CEO Letter | CEO Pre-Call → Format B | Δ +$672/mo ≥ $600 ownership boundary |
| `big` (Baker-McGuire) | Listed in CSV as `ufi` | HOLD — VD Override | `big` = Baker-McGuire; `value_delivery_score` = 33.3 triggers Strategic override; entity disambiguation with Samson Holdings / `ufi` required before send |
| `kl` (Coleto Brands \| Kichler) | Annual | Monthly | CSV `deal_type` error — only `prog` (Coleto Brands \| Progress Lighting) is Annual in v6.2 |

These corrections are not yet baked into the routing CSV. Until they are, every routing decision must cross-check against this list. The corrections also live in `_root/06_format_routing.md` (the routing doc owns the routing decision; this doc owns the errata so the segment roster is canonical).

---

## 8. The per-account roster — and the 109 / 107 / locked-pricing reconciliation

The per-account roster is `_master-account-data-v6.2.csv` at the root of `Pricing Migration/`. It is the authoritative source for every per-account field this system depends on. How to load and use it is owned by `_root/07_data_pipeline.md`; the field meanings are owned there as well. The key columns the roster carries (verified to exist in v6.2 — names match the CSV header exactly):

`company`, `parent_entity`, `billing_entity`, `paying_entity`, `ord_id`, `cohort_year`, `deal_type`, `current_mrr`, `delta_mrr`, `delta_pct`, `assigned_tier`, `migration_driver`, `secondary_drivers`, `migration_status`, `migration_confidence`, `health_score`, `health_band`, `engagement_score`, `adoption_score`, `value_delivery_score`, `operational_health_score`, `composite_narrative`, `support_fire`, `support_fire_days_open`, `migration_segment`, `notice_cohort`, `notice_deadline`, `messaging_headline`, `artifact_type`, `delivery_owner`.

### The 109 / 107 / locked-pricing reconciliation

The exec plan v3.3 §I states **109 accounts mapped** with corrected economics, but **107 migration-pending** in the cohort total (June 55 + July 16 + Deferred 36 = 107). Foundation/03 (§"How the migration works") separately referenced a **5-account locked-pricing / in-implementation cohort** as "exceptions in the migration plan, not part of the default motion." The v6.2 CSV is the source of truth for the count; the resolution is:

- **Total unique accounts in v6.2 CSV (by `ord_id`): 109.** (Matches v3.3 §I's "109 mapped" figure.)
- **`migration_status = 'migration_pending'`: 107.** (Matches v3.3 §IV's 55 + 16 + 36 cohort total exactly.)
- **`migration_status = 'already_migrated'`: 2.** (109 − 107 = 2.) The two accounts are **CopperSmith** (`tcs`, segment `Annual`, "Already on T3 pricing. No migration needed.") and **Dorell Fabrics** (`drf`, segment `Tailwind`, "Already on T1 pricing. No migration needed.").
- **The 5-account locked-pricing claim in foundation/03 appears stale relative to v6.2.** v6.2 reports only 2 such accounts. Either (a) three additional accounts were locked in foundation/03's era but have since moved to migration-pending status, or (b) the foundation count was always approximate. The v6.2 figure of **2 already-migrated accounts (CopperSmith, Dorell Fabrics)** is the authoritative count for this system; the foundation/03 figure should be updated when foundation/03 is next revised.

This reconciliation is the authoritative count for the entire migration system. `_root/01_why_we_are_migrating.md` §4 ("Definition of done") references the 107-pending count and points here for the full reconciliation. Downstream docs (the format-routing doc, the data-pipeline doc, the quality-bar doc) trust the 107 / 109 / 2 numbers stated here.

### Data-integrity notes on v6.2

Two observations on v6.2 surfaced during this doc's authoring; both have been operator-resolved as of 2026-05-22:

1. **Duplicate-row cleanup — RESOLVED 2026-05-22.** v6.2 previously contained 168 raw data rows for 109 unique `ord_id` values (59 accounts appeared twice — older pre-v3.3 vocabulary rows alongside current v3.3-aligned rows with a slight column-shift in the last six fields). Per operator decision (see `_root/09_changelog.md` Wave 2 cleanup entry), the obsolete rows were deleted; v6.2 is now **one-row-per-account (109 rows)**. The pre-cleanup snapshot is preserved at `_archive/2026-05-22__pre-refactor/_master-account-data-v6.2__pre-dedupe-snapshot.csv` for traceability. Post-cleanup verification: 107 `migration_pending` + 2 `already_migrated`, all 8 segment counts match exec plan v3.3 §II exactly, total pending Δ MRR = $32,652.60/mo (= exec plan v3.3's $32,653/mo within rounding). Loader in `_root/07` §3 retains defensive keep-last-wins dedupe by `ord_id` as belt-and-suspenders against future re-introduction.

2. **`locked_pricing` / `in_implementation` status — operator decision 2026-05-22: not added.** v6.2's `migration_status` column carries only `'migration_pending'` (107) and `'already_migrated'` (2). The foundation/03 "5-account locked-pricing" reference appears stale relative to v6.2 (only 2 non-pending accounts exist today: CopperSmith on T3 Annual, Dorell Fabrics on T1). Per operator decision, no new column is added; the 109 / 107 / 2 reconciliation stands. If future exceptions surface (an account moved to locked-legacy or in-implementation), the operator revisits and may add a `pricing_exception_type` column at that time.

---

*Cross-references: exec plan v3.3 §II (segment definitions), §IV (cohort timing), §VI (health-routing overrides); `_root/01` §4 (definition of done); `_root/04` (voice consequence of health overrides); `_root/05` (driver framing per segment); `_root/06` (format routing, including the comm_action mapping and the same 5 errata recorded there); `_root/07` (v6.2 load mechanics and dedupe rule); `_root/CONTRACTS.md` §4 (anti-archive rule and the explicit-extraction exception that authorized the §7 errata read).*
