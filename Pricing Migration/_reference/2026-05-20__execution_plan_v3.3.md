# SuperCat Pricing Migration — Execution Plan v3.3 (OUTLINE)

> **Status**: Revised outline — segment framework refined, schedule anchored to billing cycles; pending stamp to produce full plan
>
> **Supersedes**: `2026-05-19__migration_execution_plan__v3_OUTLINE.md` (v3.2)
>
> **Date**: May 20, 2026
>
> **Revision rationale**: v3.0 (May 18) established the four-segment framework, 60-day notice architecture, entity overlay, and Council governance. v3.1 absorbs: (1) Kylor's audit; (2) CEO capacity constraint (2 humans); (3) completed driver taxonomy; (4) health-tiered parallel-track model. v3.2 (May 19) calibrates sequencing: Core/Narrative split at $200 absolute delta (percentage dropped), entity packet as notice vehicle, and health clarified as content+tone layer distinct from segment routing. **v3.3 (May 20)** refines segment framework (Narrative decomposed into Narrative/Executive/Pre-Engagement at $400 ownership boundary), replaces 8-week tide rhythm with billing-cycle-anchored monthly cohort model (June/July), removes formal pilot in favor of entity conversations as high-fidelity validation.

---

## What's Been Accomplished Since v2

| Work Product | Impact |
|---|---|
| Migration Model v6 (account-level) | 109 accounts mapped with corrected economics; +$32,653/mo delta (+20.9%); 2D risk classification |
| Client Health v3.3.2 | Rebalanced composite (25E/20A/35V/20O); 104 scored accounts; 4-dimension breakdown + narratives |
| Driver Taxonomy | `discount_drivers` (current-state legacy discount diagnosis) + `classify_migration_drivers` (forward-looking structural explanation); 11 driver types with primary/secondary decomposition |
| Two-Dimensional Risk Framework | 7 `migration_confidence` levels; health × delta segmentation |
| Entity Migration Table v2 | 13 parent entities (33 accounts) with consolidation economics; max leakage: $2,278/mo |
| Account-Level Audit (2 rounds) | 18 account corrections applied; current install-base MRR now $156,433 (credible baseline) |
| Deep Research (v1 + v2) | Best practices, pitfall inventory, sequencing frameworks, governance model, metrics; v2 integrates 60-day notice |
| Value Justification Prototypes | 3 account-specific HTML artifacts demonstrating segment-adapted communication |
| Interactive HTML Artifact | Live at ceosystem.io/ceo-system/migration-revenue-model-2026-05-19 — source of truth |
| Kylor's Audit (v3) | 8 structural challenges, 6 health-data enhancements, 4 strategic decisions — absorbed into this revision |
| Health-Tiered Execution Plan | Parallel-track model, honest-framing principles, segment-level objection scripts |

**Decisions stamped**: 16 (unchanged). **Decisions reversed**: 0.

---

## I. Strategic Frame

### The Migration in One Sentence

Migrate 107 pending accounts from legacy negotiated pricing to standardized tier architecture, realizing +$32,653/mo in MRR uplift while retaining >95% of accounts, within a defined execution window governed by the 60-day contractual notice period.

### Four Operating Principles

1. **Empathetic in communication, fast on notice, firm on architecture.** Flexible on timing, billing mechanics, user cleanup, and multi-brand consolidation. Not flexible on recreating bespoke legacy pricing.

2. **Migration starts when compliant written notice is received.** The 60-day window is simultaneously legal requirement, customer adjustment period, and commercial transition. Every day without notice is a day of delayed revenue.

3. **Architecture-forward. Don't hide behind "standardization."** Standardization is true — but it's not why a customer accepts a price increase. They accept it because SuperCat is embedded in their workflow and replacement costs more than normalization. Lead with what the customer gets. Never lead with the percentage.

4. **Artifacts over meetings.** With a 2-person CS team (CEO + Kylor), bespoke communication artifacts are the primary vehicle for substance delivery. Meetings are reserved for entity parents and Strategic accounts. A data-rich value justification delivered alongside notice communicates more substance than a 20-minute call — and scales.

### What Changed from v2 → v3.1 → v3.2 → v3.3

| v2 / v3.0 Assumption | v3.1 Operating Reality |
|---|---|
| 4 risk cohorts by price-delta % | 5 segments by operational motion: Core / Narrative / Strategic / Tailwind / Annual |
| Core/Narrative split at >$400 or >20% | **>$200/mo absolute delta → Narrative.** Percentage dropped (every account >100%). |
| CSM meeting before notice | Artifact IS the communication; entity packet IS the notice. |
| Account-level notices for entities | **Entity packet IS the notice** — entity-level framing, all children covered in one document. |
| 6-person Council | CEO + Kylor with explicit concession budget gating |
| 15–20 conversations/week capacity | 2 humans; Strategic deferred post-migration |
| 3 template variants (Opportunity/Reassurance/Correction) | Two-axis dynamic composition: migration_driver + health profile compose per-account |
| Segment = routing only | **Segment = operational motion (what). Health = content + tone (how).** Distinct layers. |
| `discount_drivers` generic | Granular taxonomy: 11 driver types informing messaging posture per account |
| Health v3.2.11 (equal-weight) | Health v3.3.2 (rebalanced 25/20/35/20); support_fire_days_open; updated narratives |

| v3.2 Assumption | v3.3 Operating Reality |
|---|---|
| 5 segments (Core / Narrative / Strategic / Tailwind / Annual) | **8 segments**: Core / Narrative / Executive / Pre-Engagement / Entity / Strategic / Tailwind / Annual. $400 delta is an **ownership boundary**, not a tone adjustment. |
| Narrative covers $201–$∞ delta (single bucket) | Narrative ($201–$400, Kylor-owned) / Executive ($401–$600, CEO co-authored) / Pre-Engagement (>$600, CEO-initiated). Entity children always route to Entity segment. |
| 8-week tide rhythm (send/react alternating) | **Billing-cycle-anchored monthly cohorts** (June → P&L Oct 1; July → P&L Nov 1). Schedule governed by arrears billing + 60-day notice = 90-day P&L gap. |
| Formal pilot cohort (6-8 Core, Week 1) | **Entity conversations ARE the pilot.** No separate pilot cohort. Entity packets go first; feedback refines artifacts for subsequent cohorts. |
| Entity packets delivered Week 7 after conversations | Entity packets sent first in June cohort (packet first, meeting proposed after). Core + Narrative digital sends follow in parallel. |
| Sequential: Pilot → Narrative → Entity → Tailwind | June cohort (Entity + Core + Narrative = 55 accts, +$16,928). July cohort (Executive + Pre-Engagement = 16 accts, +$9,417). Deferred (Tailwind + Strategic + Annual). |
| ~61 sends across 8-week window | Revenue trajectory: Oct P&L +$16,928/mo; Nov P&L cumulative +$26,345/mo. |

---

## II. Migration Segment Framework

### Why 7 Confidence Levels → 8 Migration Segments

The 7 `migration_confidence` levels are analytically precise but operationally redundant. The plan consolidates them into **8 segments** defined by distinct **operational motions** and **ownership boundaries**:

| Segment | Routing Logic | Accounts | Delta MRR | Owner |
|---|---|---|---|---|
| **Tailwind** | Delta ≤ 0 | 6 | −$813 | Kylor |
| **Core** | ≤$200 delta, healthy, standalone | 13 | +$1,361 | Kylor |
| **Narrative** | $201–$400, healthy, standalone | 15 | +$4,664 | Kylor |
| **Executive** | $401–$600, healthy, standalone | 8 | +$3,879 | Kylor + CEO (co-authored) |
| **Pre-Engagement** | >$600, healthy, standalone | 8 | +$5,538 | CEO leads; Kylor executes |
| **Entity** | Multi-brand child account | 27 | +$10,903 | CEO (complex) + Kylor |
| **Strategic** | Watch/At Risk/VD<40/HVLG | 19 | +$4,800 | CEO |
| **Annual** | Annual deal type | 11 | +$2,321 | Kylor + CEO |

**Total monthly migration-pending: 107 accounts.** June cohort (55 accts, +$16,928/mo) + July cohort (16 accts, +$9,417/mo) + Deferred (36 accts).

### The $400 Ownership Boundary

The $400 delta threshold is an **ownership boundary**, not a tone adjustment:

- **Below $400** (Core + Narrative): Kylor fully owns communication. Digital-first, simplified value summaries.
- **$400–$600** (Executive): CEO co-authors — exec letter, proactive call commitment. Kylor still executes delivery.
- **>$600** (Pre-Engagement): CEO initiates before any notice is sent. Full bespoke artifact + CEO-initiated call.
- **Entity children** always route to Entity segment regardless of delta (overlay rule).

### Segment Label = Operational Motion; Health = Content + Tone

The segment label determines **what** kind of communication the account receives and **who** owns it. Customer health determines **how** that communication reads. These are distinct layers:

**Segment → operational motion + owner:**
- Core → simplified value summary + Standard Migration Notice (Kylor)
- Narrative → simplified value summary + Value Migration Notice (Kylor)
- Executive → full bespoke artifact + CEO exec letter + Value Migration Notice (Kylor + CEO co-authored)
- Pre-Engagement → full bespoke artifact + CEO-initiated call + Value Migration Notice (CEO leads)
- Entity → entity packet (packet first, meeting proposed after) (CEO complex + Kylor)
- Strategic → CEO conversation + Strategic Migration Notice (CEO)

**Health → content and tone within that motion:**

This is the two-axis artifact composition (Section VI). Every artifact is composed from the intersection of `migration_driver` (x-axis) and `health_profile` (y-axis). Two accounts at the same delta get meaningfully different artifacts:

- Sarreid ($655 delta, Thriving 96) → confident value-forward artifact, platform investment framing
- Accord Lighting ($564 delta, Healthy 60) → more careful artifact, heavier on concrete value evidence, softer on "investment" language

**Health drives four additional operational decisions:**

1. **Routing overrides** — Watch/At Risk/VD<40 escalate to Strategic regardless of delta (unchanged)
2. **Within-cohort sequencing** — Thriving accounts go first within each cohort, fastest MRR realization at lowest risk
3. **Escalation sensitivity** — Healthy accounts get faster follow-up on non-response (Day 7 vs. Day 10)
4. **Concession posture** — lower health = more latitude for pre-authorized concessions

### Health-Based Routing Overrides

These override delta-based routing:

| Override | Affected Accounts | Routing |
|---|---|---|
| **value_delivery < 40** | Studio Silversmiths (Healthy 62.6, VD 33.3), Baker-McGuire (Healthy 62.5, VD 33.3) | → Strategic |
| **Watch-band composite** | All Watch-band accounts | → Strategic |
| **Watch-band decreases** | Morgan Fabrics (Watch 40.0, −33.1%), Alden Home (Watch 59.4, −8.5%) | → Strategic (pulled from Tailwind) |
| **Coleto Brands entity** | Kichler (Watch 47.1, +77.2%) + Progress Lighting (Watch 57.5, +19.9%) | Both → Strategic; entity consistency |

### Entity Overlay: Packet First, Meeting Proposed After

The 13 parent entities (~27 child accounts, ~17 packets) receive an **entity-level packet** that serves as the notice vehicle for all child brands. Individual account-level notices are not sent separately — the entity packet conveys entity-level impact underpinned by account-level detail.

**Updated entity posture (v3.3):** Packet sent first, meeting proposed after — not CEO conversation first. Entity conversations serve as the high-fidelity pilot for the entire migration; feedback refines artifacts for subsequent cohorts.

| Entity Rule | Detail |
|---|---|
| Entity packet IS the notice | One packet per entity covering all child brands; satisfies 60-day notice for all children simultaneously |
| Packet first, meeting proposed after | Packet delivery precedes conversation; meeting proposed alongside or after packet receipt |
| Packet structure | Entity-level impact summary → per-brand pricing detail → consolidated multi-brand option → entity health profile → talk track |
| Lead with multi-brand consolidation lever | 90%-of-natural-tier brand fee positioned as partnership benefit |
| All entities get entity-level framing | Even single-child entities (2 accounts involved — entity impact must be resolved) |
| Entity-level concessions only | No brand-by-brand improvisation without CEO approval |
| Mixed-segment entities | Packet covers ALL children including Strategic-routed ones (maintains entity consistency) |
| Entity conversations = pilot | Feedback from entity conversations refines Core/Narrative/Executive/Pre-Engagement artifacts |

**Entity posture summary** (updated with health v3.3.2):

| Entity | Accts | Segment | Health | Cohort | Posture |
|---|---|---|---|---|---|
| Gabriella White | 4 | Entity | 93.5 Thriving | June | Ideal early entity proof point; consolidation as partnership |
| Visual Comfort & Co. | 4 | Entity | 88.0 Thriving | June | Multi_org_retirement driver; exec letter warranted |
| WAC Group | 2 | Entity | 91.3 Thriving | June | Both value_led; strong health; consolidation-led |
| Godinger Group | 4 | Entity (mixed health) | 73.1 Healthy | June | Studio Silversmiths VD<40; entity packet covers all 4 children including Strategic |
| Interlude Home | 2 | Entity | 95.9 Thriving | June | Confident/value_led; straightforward consolidation |
| Jonathan Charles | 2 | Entity / Annual | 88.6 Thriving | June | Both value_led; 1 annual — renewal date is urgent unknown |
| Thesis | 2 | Entity | 88.3 Thriving | June | Both value_led; straightforward |
| Creative Home Furniture | 2 | Entity | 89.2 Thriving | June | Confident/value_led; straightforward |
| Ferguson Enterprises | 2 | Tailwind | 78.0 Healthy | Deferred | Net-negative entity; goodwill — do NOT upsell during decrease notice |
| Abaline | 2 | Entity | 73.8 Healthy | June | Both standard; routine; small delta |
| Rock House Farm | 2 | Strategic | 40.0 Watch | Deferred | Both Watch-band; entity-pair vulnerability; health check first |
| Coleto Brands | 2 | Strategic / Annual | 56.5 Watch | Deferred | Both → Strategic; entity consistency; deal-type asymmetry |
| HVLG | 3 | Strategic | 42.1 Watch | Deferred | CEO-owned; +210-229%; VD=0; walk-away pre-authorized |
| Samson Holdings | 2 | Entity (mixed health) | Varies | June | Entity packet covers both; Strategic child addressed in entity context |

---

## III. The 60-Day Notice Architecture

### Why Notice Is the Centerpiece

- **The 60-day window is the default transition period.** Transition credits and grandfathering are generally unnecessary.
- **Revenue realization is gated by notice date.** Every day without notice is deferred MRR.
- **The governing mechanic**: Arrears billing + 60-day notice = 90-day gap between notice and P&L realization. Each month's 1st is a binary gate.
- **For annual contracts**: 90 days before renewal is the notice window (60-day minimum + 30-day buffer).

```
Notice before July 1  →  new pricing Sept 1  →  first new-rate invoice Oct 1
Notice before Aug 1   →  new pricing Oct 1   →  first new-rate invoice Nov 1
```

### Notice vs. Artifact vs. Meeting: The Capacity-Realistic Resolution

| Segment | Communication Architecture |
|---|---|
| **Tailwind** | Good News Notice IS the communication. No meeting, no artifact, no call. Deferred — each month of delay preserves higher legacy revenue. |
| **Core** | Standard Notice + simplified value summary. Kylor-owned, digital-first. Follow-up at Day 7 (Healthy) or Day 10 (Thriving) if non-response. June cohort. |
| **Narrative** | Simplified value summary + Value Notice. Kylor-owned, digital-first. June cohort. |
| **Executive** | Full bespoke artifact + CEO co-authored exec letter + Value Notice. No default meeting. July cohort. |
| **Pre-Engagement** | Full bespoke artifact + CEO-initiated call before notice. CEO leads. July cohort. |
| **Entity** (all children) | Entity packet IS the notice. Packet sent first, meeting proposed after. June cohort — serves as high-fidelity pilot. |
| **Strategic** | CEO-led conversation precedes notice. Addressed post-migration. |
| **Annual** | Same architecture as natural segment. Renewal-date driven. Addressed post-migration. |

**The key reframe**: For Core + Narrative standalone accounts (28 accts), the digital artifact IS the personal outreach. For Entity accounts (~27 children, ~17 packets), the entity packet IS the notice — packet first, meeting proposed after. For Executive + Pre-Engagement (16 accts), the CEO is directly involved in the communication. Meetings are proactively scheduled for:
- Entity parents (meeting proposed after packet delivery, June)
- Pre-Engagement accounts (CEO-initiated call, July)
- Inbound requests from any account

### Notice Template Family

The **notice** is the formal written document satisfying the 60-day contractual requirement. It is distinct from — and delivered alongside — the value artifact, exec letter, or entity packet. The notice triggers the legal clock; the supporting materials carry the substance.

| Template | Segment | What It Contains | What It Does NOT Contain |
|---|---|---|---|
| **Good News Notice** | Tailwind (6 accts) | "Your price is decreasing from $X to $Y, effective [DATE]." One sentence of mechanic. What doesn't change. Done. | No upsell. No expansion ask. No relationship preamble. |
| **Standard Migration Notice** | Core (13 accts, ≤$200 delta) | New tier name + pricing. What's included (features, users). User model. Effective date. Simplified value summary attached. Kylor's contact for questions. | No full bespoke artifact. No percentage framing. No apology. |
| **Value Migration Notice** | Narrative (15 accts, $201–$400) + Executive (8 accts, $401–$600) + Pre-Engagement (8 accts, >$600) | New tier + pricing. References the value artifact (linked). Install-base normalization framing. Effective date. | The artifact carries the substance — the notice is the formal/legal vehicle. |
| **Entity Migration Packet** | All entities (~17 packets → 27 child accts) | Entity-level impact summary. Per-brand pricing detail. Consolidated multi-brand option. Entity health profile. Satisfies 60-day notice for all child brands simultaneously. | Not an account-by-account notice. Entity-level framing throughout. |
| **Strategic Migration Notice** | Strategic (19 accts) | Sent AFTER CEO conversation. References the discussion. Confirms agreed terms or standard pricing. Effective date. | Not a first-touch document. Addressed post-migration. |
| **Annual Renewal Notice** | Annual (11 accts) | New tier + pricing effective at next renewal date. Renewal-specific framing. Sent ≥90 days before renewal. Matches natural segment substance. | Not tied to monthly migration timing. |

**Companion materials (separate from the notice):**

| Material | Applies To | Relationship to Notice |
|---|---|---|
| **Full value artifact** (bespoke HTML) | Executive ($401–$600 delta) + Pre-Engagement (>$600 delta) | Delivered with or ahead of notice. The substance layer. |
| **Simplified value summary** (parameterized 1-page) | Core (≤$200) + Narrative ($201–$400) | Attached to notice. Key data points from v6 table + health. |
| **CEO exec letter** | Executive ($401–$600 delta) | Delivered alongside notice. CEO co-authored — signals executive awareness and ownership. |
| **CEO-initiated call** | Pre-Engagement (>$600 delta) | CEO initiates before any notice is sent. Full conversation before formal notice. |

### Annual Contract Handling — Addressed Post-Migration

11 accounts on annual terms. Annual migration is **not a critical priority** and is **not a roadblock** to the broader pricing migration on monthly accounts. Annual accounts are addressed once the monthly migration is well underway.

1. **Renewal date audit** — conducted during readiness sprint for awareness (24-hour ask for Jonathan Charles specifically)
2. **90-day notice window** — notice sent no later than renewal − 90 days
3. **If a renewal is imminent (<90 days from today)** — fast-track notice for that specific account; does not change the broader sequencing posture
4. **Effective date = next renewal date** for all annual accounts
5. **Notice substance** — each annual account uses the notice variant (Standard, Value, Strategic) that matches its natural segment characteristics

---

## IV. Execution Architecture: Billing-Cycle-Anchored Monthly Cohorts

### Operating Model: Monthly Cohort Sequencing

The migration operates on **monthly cohorts anchored to billing deadlines**, not abstract week counts. The governing mechanic: arrears billing + 60-day notice = 90-day gap between notice and P&L realization. Each month's 1st is a binary gate.

```
Notice before July 1  →  new pricing Sept 1  →  first new-rate invoice Oct 1
Notice before Aug 1   →  new pricing Oct 1   →  first new-rate invoice Nov 1
```

### Cohort Summary

| Cohort | Accounts | Delta MRR | P&L Realization | Segments Included |
|---|---|---|---|---|
| **June** (→ P&L Oct 1) | 55 | +$16,928/mo | Oct 1 | Entity (27), Core (13), Narrative (15) |
| **July** (→ P&L Nov 1) | 16 | +$9,417/mo | Nov 1 | Executive (8), Pre-Engagement (8) |
| **Deferred / Post-Migration** | 36 | +$6,308/mo | Varies | Tailwind (6), Strategic (19), Annual (11) |
| **Total** | **107** | **+$32,653/mo** | | |

### June Cohort — 55 Accounts, +$16,928/mo (→ P&L Oct 1)

The June cohort is the volume cohort: Entity packets, Core, and Narrative — all Kylor-owned or CEO-complex for entities. Entity conversations serve as the high-fidelity pilot; no separate formal pilot needed. Feedback from entity conversations refines artifacts for the July cohort.

| Segment | Accounts | Delta MRR | Communication | Owner |
|---|---|---|---|---|
| Entity | 27 (across ~17 packets) | +$10,903 | Entity packet sent first, meeting proposed after | CEO (complex) + Kylor |
| Core | 13 | +$1,361 | Standard Notice + simplified value summary, digital-first | Kylor |
| Narrative | 15 | +$4,664 | Value Notice + simplified value summary, digital-first | Kylor |

**June operating cadence:**

| Timing | Activity | Owner |
|---|---|---|
| Weeks 1–2 | Entity packets go out; first entity meetings scheduled | CEO + Kylor |
| Weeks 2–4 | Core + Narrative digital sends in parallel (~2-3/day) | Kylor |
| Late June | Internal HubSpot dry-run for July templates; begin Executive/Pre-Engagement artifact production | Kylor + CEO |
| Ongoing | Handle inbound responses from June sends | Kylor (primary) + CEO (escalations) |

**Why entity conversations ARE the pilot:**

Entity conversations are the highest-fidelity validation of the migration's operational mechanics and customer reception. They test:
- Packet delivery + receipt confirmation mechanics
- Multi-brand consolidation framing
- Customer reaction to pricing changes at meaningful delta
- CEO + Kylor handoff dynamics
- Objection script coverage against real customer responses

Feedback from these conversations directly refines the Executive and Pre-Engagement artifacts produced for the July cohort.

### July Cohort — 16 Accounts, +$9,417/mo (→ P&L Nov 1)

The July cohort is the high-touch cohort: accounts where the CEO is directly involved in the communication. Benefits from 4+ weeks of entity conversation feedback from the June cohort.

| Segment | Accounts | Delta MRR | Communication | Owner |
|---|---|---|---|---|
| Executive | 8 | +$3,879 | Full bespoke artifact + CEO co-authored exec letter | Kylor + CEO (co-authored) |
| Pre-Engagement | 8 | +$5,538 | Full bespoke artifact + CEO-initiated call before notice | CEO leads; Kylor executes |

**July operating cadence:**

| Timing | Activity | Owner |
|---|---|---|
| Week 1 | Executive + Pre-Engagement notices sent | CEO + Kylor |
| Weeks 1–4 | Handle reactions from June + July cohorts | Kylor (primary) + CEO |
| Ongoing | CEO manages Pre-Engagement accounts directly | CEO |

### Deferred / Post-Migration

| Segment | Accounts | Delta MRR | Timing | Owner |
|---|---|---|---|---|
| **Tailwind** | 6 | −$813 | Deliberately last — each month of delay preserves higher legacy revenue | Kylor |
| **Strategic** | 19 | +$4,800 | CEO conversations post-migration; no time pressure; no overlap with main cohorts | CEO |
| **Annual** | 11 | +$2,321 | Renewal-date-driven; fast-track only if imminent | Kylor + CEO |

### Revenue Trajectory

```
Oct P&L:  +$16,928/mo  (June cohort realized)
Nov P&L:  +$9,417/mo   (July cohort realized)  →  cumulative $26,345/mo
Deferred: +$6,308/mo   (Strategic + Tailwind + Annual — realized on individual timelines)
Full run-rate: +$32,653/mo
```

---

## V. Communication Playbooks

Each segment gets a playbook. The outline defines structure; the full plan will contain production-ready content for each deliverable.

### Playbook Anatomy (shared structure)

Every playbook contains:

1. **Segment definition** — which accounts, routing logic, what they have in common
2. **Owner** — CEO or Kylor, with escalation path
3. **Communication sequence** — timeline from pre-notice through post-migration
4. **Notice template** — segment-specific variant (required deliverable: readiness sprint)
5. **Value artifact** — if applicable (required deliverable: readiness sprint)
6. **Objection scripts** — 5-7 most common objections with scripted responses (required deliverable: readiness sprint exercise)
7. **Concession menu** — what's pre-authorized vs. what requires CEO approval
8. **Escalation triggers** — conditions that escalate
9. **CRM stage checklist** — stages with owner and expected duration
10. **Exit criteria** — what "done" looks like

### Tailwind Playbook — Key Distinctions

- **Deferred** — deliberately last; each month of delay preserves higher legacy revenue
- **No conversation required** — Good News Notice is the communication
- **No artifact** — notice only
- **CRM stages**: Notice sent → Receipt confirmed → Billing migrated → Complete
- **Honest framing**: Lead with "decrease" in sentence one. Don't bury it, don't frame as a gift, don't attach an expansion ask.
- **Owner**: Kylor
- **Duration**: 60 days, near-zero effort per account

### Core Playbook — Key Distinctions

- **June cohort** — digital-first, Kylor-owned, sends in June Weeks 2–4 in parallel with Narrative
- **Standard Migration Notice + simplified value summary** — no full bespoke artifact
- **Kylor available for inbound** — no proactive call scheduling
- **Non-response follow-up**: Day 7 (Healthy accounts) or Day 10 (Thriving accounts) — health-driven escalation sensitivity
- **Honest framing**: Lead with dollar amount and effective date, then mechanic. Not percentage. Not relationship preamble.
- **Pre-authorized concessions**: User cleanup, billing date adjustment, annual prepay
- **Owner**: Kylor
- **Duration**: 60–75 days

### Narrative Playbook — Key Distinctions

- **June cohort** — digital-first, Kylor-owned, sends in June Weeks 2–4 in parallel with Core
- **Simplified value summary + Value Migration Notice** — not a full bespoke artifact (delta $201–$400)
- **No default meeting scheduled** — Kylor available for inbound
- **Two-axis artifact composition**: content driven by `migration_driver` × `health_profile` (see Section VI)
- **Honest framing for discount_correction** (>$300/mo delta): direct acknowledgment — *"You negotiated a discount at signing. We're retiring all legacy arrangements simultaneously. You are not being singled out."*
- **Pre-authorized concessions**: User cleanup, 30-day transition credit, annual prepay
- **Concessions requiring CEO approval**: Permanent discount, >30-day transition credit, any discount >10% of target
- **Owner**: Kylor
- **Duration**: 60–90 days

### Executive Playbook — Key Distinctions

- **July cohort** — $401–$600 delta; CEO co-authors the communication
- **Full bespoke value artifact + CEO exec letter + Value Migration Notice**
- **No default meeting scheduled** — but CEO exec letter signals direct ownership and availability
- **Two-axis artifact composition**: content driven by `migration_driver` × `health_profile` (see Section VI)
- **Benefits from entity conversation feedback** — artifacts refined based on 4+ weeks of June cohort learnings
- **Pre-authorized concessions**: User cleanup, 30-day transition credit, annual prepay
- **Concessions requiring CEO approval**: Permanent discount, >30-day transition credit, any discount >10% of target
- **Owner**: Kylor + CEO (co-authored)
- **Duration**: 60–90 days

### Pre-Engagement Playbook — Key Distinctions

- **July cohort** — >$600 delta; CEO initiates before any notice is sent
- **Full bespoke value artifact + CEO-initiated call** — CEO leads the conversation before notice delivery
- **Opening move**: CEO-initiated proactive call to frame the transition; notice sent after conversation
- **Two-axis artifact composition**: content driven by `migration_driver` × `health_profile` (see Section VI)
- **Benefits from entity conversation feedback** — artifacts refined based on 4+ weeks of June cohort learnings
- **Pre-authorized concessions**: Everything in Executive menu + bounded transition pricing (up to 90 days at intermediate rate)
- **Owner**: CEO leads; Kylor executes
- **Duration**: 60–90 days

### Entity Playbook — Key Distinctions

- **June cohort** — entity packets sent first (Weeks 1–2), meeting proposed after packet delivery
- **Entity packet IS the notice** — entity-level impact framing, underpinned by per-brand account detail
- **Entity conversations ARE the pilot** — feedback refines artifacts for July cohort (Executive + Pre-Engagement)
- **Mixed-segment entities** (Godinger, Samson): packet covers ALL children including Strategic-routed ones, maintaining entity consistency
- **CEO delivers complex entities** (Gabriella White, Visual Comfort, Godinger, etc.); **Kylor delivers simpler entities** (Abaline, Hearthstone, etc.)
- **Lead with multi-brand consolidation lever** — 90%-of-natural-tier brand fee positioned as partnership benefit
- **Pre-authorized concessions**: Multi-brand consolidation, user cleanup, 30-day transition credit
- **Entity-level concessions only** — no brand-by-brand improvisation without CEO approval
- **Owner**: CEO (complex entities) + Kylor (simpler entities)

### Strategic Playbook — Key Distinctions

- **Deferred / post-migration** — addressed after main cohorts are well complete. No overlap with June/July cohort execution.
- **CEO-led from the start** — conversation precedes notice
- **Opening move does not mention pricing** — product health call first: *"We've been reviewing how your team uses SuperCat and I wanted to connect to make sure you're getting full value."*
- **HVLG, Coleto Brands, Rock House Farm, Watch-band, VD<40 accounts** — all addressed here
- **Walk-away threshold pre-authorized** before first call
- **Pre-authorized concessions**: Everything in Executive menu + bounded transition pricing (up to 90 days at intermediate rate)
- **Owner**: CEO
- **Duration**: 60–120 days (longer runway acceptable)

### Annual Playbook — Key Distinctions

- **Deferred / post-migration** — addressed after monthly migration underway; not a critical priority, not a roadblock
- **Segment label, not a separate operational motion** — each annual account uses the playbook (Core, Narrative, Executive, or Strategic) that matches its natural segment characteristics
- **Timing is renewal-driven** — notice references renewal date, not migration effective date
- **Notice sent ≥90 days before renewal** — only fast-tracked if a specific renewal is imminent
- **Entity annuals** (e.g., Coleto Progress, Jonathan Charles annual brand) — coordinated with entity packet and parent conversation
- **Owner**: Kylor (notice execution) + CEO (entity annuals)

### Required Deliverables — Exercises During Readiness Sprint

| Deliverable | Exercise | Owner | Output |
|---|---|---|---|
| Notice templates (6 variants) | Draft → CEO review → Legal review → stamp | Kylor + CEO | 6 production-ready notice documents (Good News, Standard, Value, Entity Packet, Strategic, Annual Renewal) |
| Objection scripts (per playbook) | Brainstorm top 7 objections per playbook → draft scripted responses → internal red-team → refine | CEO + Kylor | 8 playbook-specific objection scripts (~56 total responses) |
| Entity packets | Per entity: entity-level impact summary + per-brand pricing + consolidated option + health profile + talk track | CEO + Kylor | ~17 entity packets (serving as notice for ~27 child accounts) |
| Entity talk tracks | Per entity: draft parent-level talk track for meeting proposed after packet delivery | CEO | ~17 entity-specific talk tracks |
| Value artifacts (full, bespoke HTML) | Produce for Executive ($401–$600) + Pre-Engagement (>$600) accounts → internal red-team 3 exemplars → refine → batch produce | Kylor + CEO review | ~16 bespoke HTML artifacts (July cohort) |
| Value summaries (simplified, parameterized) | Build template → batch populate from v6 table + health CSV | Kylor | ~28 simplified summaries (Core + Narrative accounts) |
| Segment assignment validation | CEO + Kylor review all 107 accounts against $200/$400/$600 delta thresholds + health overrides + entity overlay → confirm or override | CEO + Kylor | Stamped account-by-account segment assignment |
| Cohort assignment plan | Assign accounts to June / July / Deferred cohorts; validate entity overlay routing | Kylor + CEO | Stamped cohort rosters |
| Annual account audit | Pull all 11 renewal dates → identify any within 90 days → flag for fast-track | Kylor | Renewal date table |
| Strategic account plans | Per Strategic account: health posture, success criteria, conversation timeline, walk-away threshold | CEO + Kylor | ~19 Strategic account plans (for post-migration phase) |
| HubSpot configuration | Configure notice templates, personalization tokens, tracking, CRM stage automation | Kylor | HubSpot ready for June cohort execution |
| Contract audit | Per account: legal name, entities, renewal date, notice clause, price-change language | Kylor + Legal | Complete contract audit table |

---

## VI. Value Justification Artifact System

### Two-Axis Dynamic Composition

The artifact architecture composes dynamically along TWO co-equal axes. This replaces the v3.0 three-template-variant model (Opportunity / Reassurance / Correction), which was over-fitted to the 3 prototypes.

#### Axis 1 — Migration Driver (the "why your price is changing" spine)

The `migration_driver` + `discount_drivers` fields determine the pricing explanation content:

| Primary Driver | Messaging Posture | Key Framing |
|---|---|---|
| `user_rate_normalization` (37 accts) | "User pricing standardized" | Graduated rate vs. legacy flat; volume benefit |
| `platform_discount_correction` (17 accts) | "Legacy discount retired" | Acknowledge discount existed (per `discount_drivers`); install-base normalization |
| `included_user_reduction` (11 accts) | "Included users now tier-based" | What's included in tier; excess priced transparently |
| `tier_base_increase` (12 accts) | "New architecture delivers more" | Feature inventory of tier vs. legacy modules |
| `multi_org_retirement` (6 primary) | "Multi-brand consolidation replaces discount" | Lead with consolidation option; partnership framing |
| `annual_discount_retirement` (2 accts) | "Annual commitment discount retired" | Standard rate; annual prepay still available |
| `module_compression` (8 accts) | "Good news — price flat or decreasing" | Minimal artifact needed |

Secondary drivers compose as supporting context in the artifact.

#### Axis 2 — Health Profile (the "here's the value you're receiving" substance)

The full health data composes the value demonstration — this is not supplementary, it is half the artifact:

- **Composite score + band** → headline positioning ("you're a Thriving partner at 94/100")
- **4 dimension scores** → targeted value proof:
  - High engagement → cite login volume, rep penetration, pace trend
  - High adoption → cite feature breadth, capabilities actively used
  - High value delivery → hero as ROI proof ("all configured channels producing outcomes")
  - High ops health → cite catalog completeness, feed reliability
  - Low dimension → acknowledge honestly; frame as joint opportunity
- **Composite narrative** → direct quote from health system as personalized evidence
- **Dimension narratives** → specific, actionable language about what's working
- **Support fire** → if active, acknowledge and resolve BEFORE pairing with pricing notice

#### How the Two Axes Compose (examples)

- **Crystorama** (included_user_reduction + Thriving 94.4 + high adoption): "Your expanded user allotment is being normalized to tier-standard; here's what 94/100 health looks like — you're extracting exceptional value across all channels..."
- **Hudson Valley** (platform_discount_correction + Watch 42.5 + VD=0): Fundamentally different — leads with discount acknowledgment, does NOT lead with value proof. Frames as opportunity to address product-fit gap.
- **WAC/Modern Forms** (user_rate_normalization + Thriving 93.7 + high engagement): "Your user rate is being standardized; with 97 active users generating orders, you're operating at scale..."

**The artifact is NOT a template selection — it is a composition.** Every artifact is unique because the two axes produce different content for every account.

### Two-Tier Production (Capacity-Aligned)

| Tier | Criteria | Output | Production Effort |
|---|---|---|---|
| **Full artifact** (bespoke HTML) | Executive ($401–$600 delta) + Pre-Engagement (>$600 delta) | ~16 accounts (July cohort) | Rich composition of both axes; personalized narrative |
| **Simplified value summary** (parameterized 1-page) | Core (≤$200) + Narrative ($201–$400) | ~28 accounts (June cohort) | Template-driven; key data points populated from v6 table + health CSV |
| **Entity packet** | All entity children (~27 accounts across ~17 packets) | ~17 packets (June cohort) | Entity-level impact + per-brand detail; serves as notice vehicle |
| **No artifact** | Tailwind | 6 accounts (Deferred) | Good News Notice only |

Production timeline: Entity packets and simplified summaries complete during readiness sprint before June cohort launch. Full bespoke artifacts for July cohort produced during late June, refined by entity conversation feedback.

---

## VII. Governance: CEO + Kylor Migration Authority

### Why Not a 6-Person Council

The original v3.0 prescribed a 6-person Pricing Migration Council. CS reality: the team is CEO + Kylor. The governance model simplifies to executive decision authority with explicit guardrails.

### Decision Structure

| Decision Type | Authority | Mechanism |
|---|---|---|
| Standard migration (notice + no concession) | Kylor | Execute per playbook |
| Pre-authorized concession (user cleanup, billing adj, 30-day credit, annual prepay, consolidation) | Kylor | Offer per menu; log to tracker |
| Concession beyond pre-authorized menu | CEO | Kylor requests; CEO approves same-day |
| Permanent discount or strategic exception | CEO | Documented decision with business case |
| Walk-away / intentional churn (≥$500/mo new MRR) | CEO | Pre-authorized threshold or deliberate decision |
| Walk-away / intentional churn (<$500/mo new MRR) | Kylor + CEO confirmation | Brief async approval |

### Concession Budget Gating

- **Aggregate cap**: <10% of modeled uplift (~$3,265/mo or ~$39,180/yr)
- **Per-account L1 ceiling**: Pre-authorized concessions capped at 25% of individual account's annual uplift
- **Tracking**: Kylor maintains running concession-cost total. No concession offered that would breach remaining budget without CEO approval.
- **Tightened menu** (per audit): 30-day max transition credit without CEO sign-off (not 90 days)

### Cadence

| Phase | CEO + Kylor Sync |
|---|---|
| Readiness sprint | Daily (15 min) |
| June cohort active | Daily (15 min) — covers entity packet delivery, Core/Narrative sends, responses, escalations |
| Late June (July prep) | Daily (15 min) — covers July artifact production, HubSpot dry-run, entity conversation feedback synthesis |
| July cohort active | Daily (15 min) — covers Executive/Pre-Engagement sends, CEO co-authored artifacts, reaction handling |
| Post-cohort (Strategic phase) | Twice weekly |
| Post-migration watch | Weekly |
| Churn threat (any time) | Same-day async |

---

## VIII. Operational Readiness (Pre-Launch Sprint)

### Duration: 2.5–3 Weeks

Extended from v3.0's "1-2 weeks" based on artifact production load and the dry-run requirement.

### Sprint Structure

| Week | Focus | Key Outputs |
|---|---|---|
| Week 1 | Data closure + contract audit + HubSpot setup | Renewal dates pulled; segment assignment validated ($200/$400/$600 thresholds + health overrides + entity overlay); HubSpot templates configured; cohort rosters stamped |
| Week 2 | June cohort artifact production + templates | Simplified summaries (~28 for Core + Narrative); entity packets (~17); notice templates (6); entity talk tracks (~17) |
| Week 3 (half) | Dry-run + objection scripting + stamp | Internal HubSpot dry-run; objection scripts finalized; cohort assignment plan stamped; CEO stamps all June deliverables |

### Dry-Run (Pre-Launch Validation)

Before June cohort launch: send a test entity packet and a test Core notice to an internal account via HubSpot to validate the end-to-end delivery pipeline. Also: produce simplified summaries for 3 representative Core/Narrative accounts and run internal red-team — CEO plays the customer, Kylor presents. Validates the production pipeline under simulated pressure.

Full bespoke artifacts for July cohort (Executive + Pre-Engagement) are produced during late June, informed by entity conversation feedback from the June cohort.

### Gate Criteria for June Cohort Launch

- [ ] Segment assignment validated (all 107 accounts reviewed against $200/$400/$600 thresholds + health overrides + entity overlay)
- [ ] Annual renewal table published with notice deadlines
- [ ] All 6 notice templates produced and CEO-approved
- [ ] Entity packets (~17) assembled and CEO-reviewed
- [ ] Entity talk tracks finalized
- [ ] Simplified value summaries produced for Core + Narrative accounts (~28)
- [ ] CRM stages configured and tested
- [ ] HubSpot templates configured with personalization tokens
- [ ] Cohort rosters stamped (June / July / Deferred)
- [ ] Concession tracker operational
- [ ] Objection scripts finalized per playbook
- [ ] Internal HubSpot dry-run complete

### Gate Criteria for July Cohort Launch

- [ ] Entity conversations from June cohort debriefed; feedback synthesized
- [ ] Full bespoke artifacts produced for Executive (8) + Pre-Engagement (8) accounts — refined by entity feedback
- [ ] CEO exec letters drafted for Executive accounts
- [ ] Pre-Engagement CEO call schedule confirmed
- [ ] June cohort response patterns reviewed; no systemic issues blocking July launch

---

## IX. Metrics & Success Criteria

### Migration-Specific KPIs (the MRR Pipeline)

| Metric | Definition | Target |
|---|---|---|
| **Noticed MRR** | MRR for accounts with compliant notice sent and receipt confirmed | ≥95% of June cohort before July 1; ≥95% of July cohort before Aug 1 |
| **Billable MRR** | MRR where 60-day clock elapsed and new pricing effective | Tracks Noticed MRR with 60-day lag |
| **Realized MRR** | MRR actually collected at new pricing | ≥90% of modeled uplift |
| **Concession cost** | Total MRR reduction from all concessions | <10% of modeled uplift ($3,265/mo cap) |
| **Permanent exceptions** | Accounts with non-standard pricing (CEO approval) | <5% of accounts |
| **Uplift capture rate** | Realized MRR uplift ÷ Modeled uplift | ≥90% |

### Post-Migration Health Tracking

| Checkpoint | What to Track | Action Trigger |
|---|---|---|
| Notice date (baseline) | Health score per account | Flag any account <60 for CSM monitoring |
| +30 days post-notice | Login activity, order volume vs. pre-notice | Proactive outreach if engagement drops >20% |
| +60 days (effective date) | Health score delta; payment confirmed | Same-day CEO notification if >15pt decline + non-payment |
| +90 days post-effective | Full health rescore; concession expiration review | Flag delayed churn signals |

### Success Thresholds

| Criterion | Threshold |
|---|---|
| June cohort noticed (55 accounts) | ≥95% with compliant notice before July 1 |
| July cohort noticed (16 accounts) | ≥95% with compliant notice before August 1 |
| Modeled uplift realized or firmly scheduled | ≥90% within migration window |
| Billing applied without notice compliance | Zero |
| Permanent exceptions | <5% of accounts; CEO approval each |
| Entity packets delivered (June) | All ~17 packets; all 27 child brands covered |
| Parent-entity consistency | No inconsistent sibling-brand treatment without CEO approval |
| Logo churn (migration-induced) | ≤6 accounts |
| MRR churn (migration-induced) | ≤$3,000/mo |
| Entity conversations yield actionable feedback | Feedback synthesized before July cohort launch |
| Strategic accounts resolved (post-migration) | Each: migrated / approved transition / intentional churn documented |
| Annual accounts noticed ≥90 days before renewal | 100% (for renewals falling within plan horizon) |

---

## X. Timeline

### Assumptions

- Readiness sprint begins upon plan approval
- CS capacity: CEO + Kylor — 2 humans
- June cohort throughput: ~17 entity packets (Weeks 1–2) + ~28 Core/Narrative digital sends (Weeks 2–4) at ~2-3/day
- July cohort throughput: 16 Executive + Pre-Engagement sends (Week 1 of July)
- Billing-cycle-anchored: notice before month's 1st → new pricing 60 days later → first invoice 90 days later

### Phased Timeline

| Phase | Timing | Key Activities |
|---|---|---|
| **Readiness Sprint** | Late May – mid June (~3 weeks) | Contract audit, simplified summaries (~28), entity packets (~17), templates, objection scripts, HubSpot setup, dry-run, segment + cohort validation |
| **June Cohort: Entity Packets** | June Weeks 1–2 | ~17 entity packets sent (→ 27 child accounts); first entity meetings scheduled |
| **June Cohort: Core + Narrative** | June Weeks 2–4 | 13 Core + 15 Narrative digital sends (~2-3/day); Kylor-owned |
| **June: July Prep** | Late June | Internal HubSpot dry-run for July templates; begin Executive/Pre-Engagement bespoke artifact production; entity conversation feedback synthesis |
| **July Cohort: Executive + Pre-Engagement** | July Week 1 | 8 Executive + 8 Pre-Engagement notices sent; CEO co-authored/initiated |
| **July: Reaction Handling** | July Weeks 1–4 | Handle reactions from both June + July cohorts; CEO manages Pre-Engagement accounts directly |
| **Deferred: Tailwind** | Post-July | 6 Tailwind accounts; deliberately last — each month of delay preserves higher legacy revenue |
| **Deferred: Strategic** | Post-July | 19 CEO-led conversations; no time pressure; no overlap with main cohorts |
| **Deferred: Annual** | Renewal-driven | 11 accounts on renewal schedule; not a roadblock |
| **Oct P&L** | Oct 1 | June cohort realized: +$16,928/mo |
| **Nov P&L** | Nov 1 | July cohort realized: +$9,417/mo → cumulative +$26,345/mo |
| **Post-Migration Watch** | Through Q1 2027 | 90-day monitoring; health tracking; concession expiration |

---

## XI. Resolved Decisions + Remaining Open Items

### Resolved Decisions

| # | Decision | Resolution |
|---|---|---|
| 1 | **HVLG approach** | HVLG routes into **Strategic segment** via standard health-based routing (Watch-band, VD=0). Addressed after pricing migration is well underway on healthier accounts. CEO-led when the time comes. No separate negotiation program. |
| 2 | **Discount-correction language posture** | **Deferred to readiness sprint.** Will be resolved when crafting notice templates and value artifacts — needs to be expressed via real-life account examples before stamping. |
| 3 | **Off-table at-risk accounts** | **Resolved / moot.** Tomlinson, Hancock & Moore, and other previously at-risk accounts have since churned and are not in the canonical account table. Going forward, accounts exhibiting similar risk profiles would be labeled Strategic and addressed accordingly. |
| 4 | **Decrease account treatment** | **Pass through reductions confirmed.** Tailwind accounts (decreases) are migrated **last** — after Core + Narrative migration is well underway. Sequencing to be calibrated in the next exercise. |
| 5 | **Exec letter threshold** | **Deferred to readiness sprint.** Will be resolved when crafting notice templates and artifacts — the scope and content of an exec letter needs to be defined first. |
| 6 | **Notice-start date** | **Pending.** June cohort entity packets target early June (exact date gated by readiness sprint completion and July 1 billing-cycle deadline). |
| 7 | **Walk-away MRR threshold** | **Confirmed: $500/mo new MRR.** Below this: Kylor + CEO async approval. Above: deliberate CEO decision. |

### Operational Parameters (stamped into body of plan)

| Parameter | Stamped Value |
|---|---|
| Segment thresholds | ≤$200 → Core; $201–$400 → Narrative; $401–$600 → Executive; >$600 → Pre-Engagement. $400 is the **ownership boundary**. |
| Entity overlay | Multi-brand child accounts → Entity segment regardless of delta |
| VD override | value_delivery < 40 → Strategic |
| Watch-band override | Watch composite → Strategic |
| Entity notice vehicle | Entity packet IS the notice; packet sent first, meeting proposed after |
| Mixed-entity treatment | Entity packet covers ALL children including Strategic-routed ones |
| Transition credit (pre-authorized) | 30-day max without CEO sign-off |
| Concession budget cap | <10% of modeled uplift aggregate |
| Per-account L1 ceiling | 25% of individual account annual uplift |
| Tailwind sequencing | Deferred — deliberately last; each month of delay preserves higher legacy revenue |
| Strategic sequencing | Deferred / post-migration — no overlap with main cohorts |
| Coleto Brands | Both Strategic; entity consistency |
| Decrease pass-through | Confirmed — reductions passed through to customer |
| Walk-away threshold | $500/mo new MRR |
| Schedule model | Billing-cycle-anchored monthly cohorts: June (Entity + Core + Narrative), July (Executive + Pre-Engagement), Deferred (Tailwind + Strategic + Annual) |

### Items Deferred to Readiness Sprint (Template & Artifact Crafting)

These decisions will be resolved when producing the actual deliverables, grounded in real account examples:

1. Discount-correction language posture (direct acknowledgment vs. normalization framing, by delta size)
2. Exec letter scope, content, and threshold
3. Notice template final language (all 6 variants: Good News, Standard, Value, Entity Packet, Strategic, Annual Renewal)

---

## XII. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Migration-induced churn exceeds expected (>6 accounts) | Medium | High | Health-as-content-layer; Strategic deferred post-migration; entity conversations validate ops before July cohort |
| Death by concessions | Medium | High | CEO approval for non-standard; budget gating; 30-day credit max without approval |
| HVLG churn (3 accounts, +210–229%, VD=0) | High | Medium | Strategic segment; addressed post-migration; CEO-led; walk-away pre-authorized |
| Entity conversations reveal systemic ops issue | Low | High | June entity feedback synthesized before July cohort launch; process refinement before Executive/Pre-Engagement sends |
| Entity packet complexity (~17 packets, ~27 accounts) | Medium | Medium | Entity packets sent first in June cohort; meeting proposed after packet delivery; feedback refines July artifacts |
| Annual contract notice windows missed | Low | High | Renewal date audit in readiness sprint; 24-hour Jonathan Charles ask; fast-track if imminent |
| Entity contradictions (sibling brands inconsistent) | Low | Medium | Entity packet IS the notice — all children covered in one document; entity-level concessions only |
| Capacity bottleneck (Kylor artifact throughput) | Medium | Medium | ~3 week sprint; two-tier production; June cohort is digital-first/simplified (lower per-account effort); bespoke artifacts deferred to late June for July cohort |
| Response overload (June + July cohort reactions overlap) | Medium | Medium | Non-response follow-up cadence (Day 7/10) staggers inbound; June Core/Narrative are digital-first low-touch; Kylor + CEO daily sync |
| Post-migration delayed churn | Medium | Medium | 90-day health tracking; +30/+60/+90 checkpoints with action triggers |
| Competitive displacement during window | Medium | Medium | Support fire tracking; 72-hour response for competitive signals |

---

## XIII. Driver Taxonomy Reference

The completed `discount_drivers` and `classify_migration_drivers` taxonomy is the data backbone for artifact composition and messaging.

### `discount_drivers` — Current-State Legacy Discount Diagnosis

Answers: "Why is this account currently below our legacy book pricing?"

| Driver | Accounts | Messaging Use |
|---|---|---|
| User rate below $25/user | 75 | Informs user_rate_normalization framing |
| Platform below legacy module-based book | 25 | Informs platform_discount_correction framing |
| None (at or above book) | 19 | No legacy discount to acknowledge |
| Multi-org discount (10%) | 16 | Informs multi_org_retirement framing; lead with consolidation |
| Expanded user allotment (>25 provided) | 6 | Informs included_user_reduction framing |
| Annual commitment discount | 5 | Informs annual_discount_retirement framing |
| Special cases | 2 | CEO-negotiated; account-specific language |

### `classify_migration_drivers` — Forward-Looking Structural Explanation

Answers: "What structural change is causing the delta?"

| Primary Driver | Accounts | Delta | Communication Posture |
|---|---|---|---|
| `user_rate_normalization` | 37 | +$14,383 | "User pricing standardized at $25 with volume discounts" |
| `platform_discount_correction` | 17 | +$8,817 | "Legacy platform discount retired across install base" |
| `tier_base_increase` | 12 | +$4,039 | "New tier delivers expanded capabilities" |
| `included_user_reduction` | 11 | +$3,840 | "Included users now tier-based; excess priced transparently" |
| `multi_org_retirement` | 6 | +$1,490 | "Multi-org discount replaced by consolidation option" |
| `annual_discount_retirement` | 2 | +$965 | "Annual discount retired; prepay still available" |
| `at_book_tier_shift` | 10 | +$213 | Near-zero change — standard notice |
| `module_compression` | 8 | −$1,290 | "Good news — price flat or decreasing" |

### How Drivers Inform Artifacts

- The **primary driver** determines the pricing explanation spine of the artifact
- **Secondary drivers** compose as supporting context ("additionally...")
- **discount_drivers** informs how to acknowledge the legacy discount in Narrative-Correction accounts
- The combination of driver + health profile produces the unique two-axis artifact per account

**Live data source**: ceosystem.io/ceo-system/migration-revenue-model-2026-05-19

---

## XIV. Artifact Index

| Artifact | Location / Status |
|---|---|
| Pricing Constitution (authoritative) | `11_synthesis/PRICING_CONSTITUTION.md` |
| Project Plan v2 (superseded) | `11_synthesis/2026-03-11__pricing_refresh_project_plan__v2.md` |
| Project Plan v3.0 (superseded) | `11_synthesis/2026-05-18__migration_execution_plan__v3_OUTLINE.md` |
| Project Plan v3.2 (superseded) | `11_synthesis/2026-05-19__migration_execution_plan__v3_OUTLINE.md` (prior revision) |
| **Project Plan v3.3 (this document)** | `11_synthesis/2026-05-19__migration_execution_plan__v3_OUTLINE.md` |
| Migration Revenue Model v6 | `03_data/extracts/2026-05-19__migration_table__v6.csv` |
| Entity Migration Table v2 | `03_data/extracts/2026-05-19__entity_migration_table__v2.csv` |
| Migration Revenue Model HTML (live) | ceosystem.io/ceo-system/migration-revenue-model-2026-05-19 |
| Health v3.3.2 Run | `~/Downloads/client_health_scores_2026-05-13_formatted (1).csv` |
| Health Diff (v3.2.11 → v3.3.2) | `~/Downloads/health-run-diff-2026-05-13-v3.2.11-vs-v3.3.2.md` |
| Kylor's Audit (v3) | `~/Downloads/migration_plan_synthesis_and_final_2026-05-19_v3.html` |
| Health-Tiered Execution Plan | `~/Downloads/2026-05-19__pricing_migration_plan__health-tiered_v2.html` |
| Deep Research v1 + v2 | `~/Downloads/v1 Deep Research...`, `~/Downloads/v2 Deep Research...` |
| Value Justification Prototypes | `~/Downloads/mh_magnussen-home_*.html`, `bcf_braxton-culler_*.html`, `sarreid_*.html` |

---

## Immediate Next Steps

1. **Set June cohort start date** — target first entity packet send date, working backward from readiness sprint completion and July 1 billing-cycle gate
2. **Launch readiness sprint** — ~3 weeks:
   - Week 1: Contract audit, renewal dates, segment validation ($200/$400/$600 thresholds + health overrides + entity overlay), HubSpot setup, cohort roster stamping
   - Week 2: Simplified summaries (~28 for Core + Narrative), entity packets (~17), notice templates (6), entity talk tracks (~17)
   - Week 3 (half): Internal HubSpot dry-run, objection scripts, cohort assignment plan stamped, CEO stamps all June deliverables
3. **June Cohort** — Entity packets (Weeks 1–2), then Core + Narrative digital sends (Weeks 2–4, ~2-3/day)
4. **Late June** — Synthesize entity conversation feedback; produce Executive + Pre-Engagement bespoke artifacts for July cohort; HubSpot dry-run for July templates
5. **July Cohort** — Executive (8) + Pre-Engagement (8) notices sent in July Week 1; CEO co-authored/initiated
6. **Deferred: Tailwind** (6 accounts) — deliberately last; preserves higher legacy revenue
7. **Deferred: Strategic** (19 accounts) — CEO-led conversations, post-migration, no time pressure
8. **Deferred: Annual** (11 accounts) — renewal-date driven; not a roadblock
