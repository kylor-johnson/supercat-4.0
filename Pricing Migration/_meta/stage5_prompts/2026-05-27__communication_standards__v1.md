# Migration Communication Standards & Variant Architecture

**Version:** 1.0 · May 27, 2026
**Status:** Canonical reference — all migration communication reviewed against this document
**Audience:** CEO + Kylor (Head of CS)

> **Workspace-internal copy of the operator-attached north-star intake delivered to Stage 5 Phase 1 chat B at 2026-05-27 ~12:45 UTC-6.** The original was attached from `~/Downloads/2026-05-27__communication_standards__v1.md`; per `AGENTS.md` rule "All inputs the system needs live inside `Pricing Migration/`," chat B copied it here verbatim so Stage 5 Phase 1 chat C (incoming) reads it via workspace path instead of `~/Downloads/`. This intake is **Source-fix Session F** (next session marker after E) and is the authoritative substance source for `_root/03.6_platform_narrative.md` (step 3) + `_root/04.5_concessions.md` (step 4). Phase 1 sibling docs already landed (`_root/01.5` + `_root/03.5`) are NOT retroactively amended by this intake without `_root/CONTRACTS.md §3` rule-change protocol stamp.

---

## I. Platform Architecture Narrative

This is the foundational story. Every notice, artifact, entity packet, and conversation must be grounded in this explanation. Kylor and CEO should be able to deliver it from memory.

### What Changed Structurally

SuperCat has operated with module-based, individually negotiated pricing since 2014. Each account's commercial terms were set at signing — a base fee for the iPad app, add-on charges for catalog, portal, CPQ, credit card processing, and per-user rates that varied from $16 to $29 depending on when and how the deal was structured. Over 12 years, this produced a pricing landscape where two accounts running the same platform capabilities at similar scale could be paying meaningfully different amounts.

SuperCat has consolidated this into three platform tiers:

| Tier | What It Covers | Base | Included Users |
|------|----------------|------|----------------|
| **Catalog Essentials** (T1) | iPad field selling | $749/mo | 10 |
| **Commerce Professional** (T2) | iPad + B2B Cart + CPQ + Portal | $1,295/mo | 15 |
| **Commerce Enterprise** (T3) | Full platform — all capabilities | $2,295/mo | 40 |

Each tier bundles the capabilities the account already uses. Users beyond the included base are priced on a transparent graduated schedule ($25 / $22 / $20 / $18 per user based on volume). Multi-brand accounts can consolidate under a single platform tier at 90% of the natural per-brand rate.

### Why

Three reasons, in the order they should be communicated:

1. **What the customer gets is clearer.** Tier-based pricing means a single plan that includes everything — no ambiguity about which modules are on, which are add-ons, or what the user rate is. The customer knows exactly what they're paying for.
2. **Consistency across the platform.** Every customer on the same tier pays the same base rate and the same user schedule. No one is disadvantaged by when they signed or who negotiated their deal.
3. **Continued platform investment.** Standardized economics let SuperCat continue investing in the infrastructure these businesses depend on daily — catalog management, order workflows, commerce capabilities, retailer-facing experiences, security, and payments. The platform is actively evolving: a rebuilt admin console, rapid-fire scanning, multi-order support, rep activity tracking, and direct catalog editing are all shipping in the near term. A consistent pricing architecture is what makes that sustained investment possible.

### What Doesn't Change

The platform itself. The customer's catalog data, integrations, import feeds, workflows, rep access, retailer relationships, order history — none of it is affected. The support relationship doesn't change. The roadmap doesn't change. This is a commercial migration, not a product migration.

### The Canonical Paragraph

This is the reusable block that appears (adapted for tone by health band) across all communications:

> SuperCat is moving all accounts to a standardized pricing architecture — three platform tiers based on the capabilities you use, with transparent, graduated user pricing. Your current terms reflect a legacy arrangement from [YEAR] that predates this structure. Every SuperCat account is migrating to the same architecture — consistent tiers, consistent user economics, consistent investment in the platform you depend on. What you get on the platform doesn't change — your catalog, your integrations, your rep access, your order workflows all stay exactly as they are.

**Thriving variant** (90+ health): Add after the canonical paragraph: *"Your team is extracting exceptional value from the platform — [HEALTH_SCORE]/100 across team activity, feature usage, and business results. That investment is reflected in the tier you're on."*

**Healthy variant** (60–89 health): Add: *"Your team has built a solid operation on SuperCat, and the platform is producing results across your business. The tier you're mapping to reflects the capabilities you're actively using."*

**Watch / At Risk variant** (<60 health): Do NOT append a value claim. Instead: *"We also want to make sure you're getting full value from the platform — [NAME] will follow up separately to review how your team is using SuperCat and whether there are opportunities we should address together."*

---

## II. Communication Principles

Five rules that govern every piece of migration communication.

### 1. Architecture-forward, never percentage-forward

Lead with what the account maps to and what it costs. Never lead with the percentage increase.

- **Say:** "Your account maps to Commerce Professional at $1,295/month."
- **Never say:** "Your price is increasing 43%."

The percentage is an internal metric. Externally, the customer should understand the new commercial structure and the value they receive. If the customer calculates the percentage themselves, acknowledge it — don't hide from it — but never introduce it.

### 2. Lead with what the customer gets, not what SuperCat needs

The message is about the customer's tier, their included capabilities, and their usage — not about SuperCat's economics, cost structure, or revenue goals. The customer doesn't care that SuperCat needs to standardize for operational reasons. They care about what they're paying for and what they get.

- **Say:** "Commerce Enterprise includes your full platform — iPad, catalog, portal, CPQ, credit card processing — with 40 included users."
- **Never say:** "We need to standardize pricing across the platform to support growth."

### 3. Acknowledge legacy terms directly — never imply the customer was "getting away with something"

Many accounts have been below book pricing for years. That's commercially true but emotionally sensitive. The customer negotiated in good faith; they shouldn't feel penalized for it.

- **Say:** "Your current rate reflects legacy terms from 2014 that we no longer offer. We're moving all customers to a consistent architecture."
- **Never say:** "You've been underpriced." / "You've been getting a deal." / "Your discount is being removed."
- **For accounts with explicit legacy discounts:** "Your account includes a [multi-org / platform / user rate] arrangement from your original contract. We're retiring all legacy arrangements simultaneously — you are not being singled out."

### 4. Empathetic in tone, firm in architecture, flexible on mechanics

SuperCat can accommodate timing, billing date adjustments, user cleanup windows, annual prepay options, and multi-brand consolidation. SuperCat cannot recreate bespoke legacy pricing.

- **Flexible:** "We can adjust the effective date to align with your budget cycle." / "If you clean up inactive users before the effective date, your user charges will reflect that."
- **Firm:** "We're not able to extend the legacy rate structure beyond the transition period."

### 5. Artifacts over meetings — the document carries the substance

With a 2-person CS team, bespoke communication artifacts are the primary vehicle for substance delivery. A data-rich value summary delivered alongside the notice communicates more substance than a 20-minute call — and scales.

Meetings are reserved for:
- Entity parents (meeting proposed after packet delivery)
- Pre-Engagement accounts (CEO-initiated call before notice)
- Inbound requests from any account

For Core + Narrative (28 standalone accounts), the digital artifact IS the personal outreach. No default meeting.

---

## III. Never-Say / Always-Say Reference

| Context | Never Say | Always Say |
|---------|-----------|------------|
| **Framing the change** | "Price increase" / "rate hike" | "Pricing update" / "migration to standardized architecture" |
| **Explaining the delta** | "Your price goes up 43%" | "Your new monthly rate is $X, mapped to [Tier]" |
| **Legacy pricing** | "You've been underpriced" / "You got a deal" | "Your current rate reflects legacy terms from [YEAR]" |
| **Discount retirement** | "Your discount is being removed" | "We're retiring all legacy arrangements simultaneously" |
| **Justification** | "We need to raise prices" / "costs have increased" | "We're moving to a consistent architecture across the platform" |
| **Alternatives** | "You have limited alternatives" / "You can't easily switch" | "SuperCat is the platform your catalog, orders, and retailer workflows run on — this architecture lets us keep investing in it" |
| **Timeline** | "This is effective immediately" | "This change takes effect on [DATE], giving you 60 days to review" |
| **Multi-org** | "Your multi-org discount is being taken away" | "Multi-brand consolidation replaces the legacy multi-org arrangement — at 90% of the natural per-brand rate" |
| **Users** | "You'll be paying more for users" | "User pricing is now on a graduated schedule — higher volume means lower per-user cost" |
| **Apology** | "We're sorry for the increase" | "We want to explain this clearly and make sure you have everything you need" |
| **Coercion** | "If you don't accept..." | "Your options include [tier fit review / user cleanup / annual prepay / consolidation]" |
| **Internal terminology** | "install base" / "customer base" | "on the platform" / "every SuperCat account" |

---

## IV. Health-Driven Tone Modulation

The segment label determines WHAT communication the account receives. Health determines HOW that communication reads. These are distinct layers.

### Thriving (90–100)

- **Voice:** Confident, investment-forward
- **Evidence emphasis:** Lead with team activity and feature usage stats as proof of platform centrality. Use phrases like "exceptional value," "platform investment," "core commerce infrastructure."
- **Health badge:** Prominent, green-highlighted
- **Delta framing:** Present as investment alignment — the customer is already getting outsized value, the pricing reflects that
- **Follow-up timing:** Day 10 non-response (lower urgency — Thriving accounts are least likely to churn)
- **Concession posture:** Firm — healthy accounts have the least justification for concessions

### Healthy (60–89)

- **Voice:** Balanced, concrete, evidence-forward
- **Evidence emphasis:** Lead with specific operational data (orders processed, catalog completeness, feed health). Avoid "exceptional" language — stick to "solid," "producing results," "actively using."
- **Health badge:** Prominent, standard
- **Delta framing:** Present as standardization — focus on what the tier includes and what the customer is using. Heavier on concrete evidence, lighter on "investment" framing.
- **Follow-up timing:** Day 7 non-response
- **Concession posture:** Standard — user cleanup and billing adjustment available

### Watch / At Risk / Critical (<60)

- **Voice:** Careful, acknowledgment-forward
- **Evidence emphasis:** Do NOT lead with value proof. If business_results < 40 or composite < 60, the customer may perceive a value claim as tone-deaf. Acknowledge the relationship, explain the architecture, and offer to address product fit separately.
- **Health badge:** Present but not hero'd
- **Delta framing:** Frame as part of the broader platform-wide migration. Do not imply the customer should be grateful for what they're getting.
- **Follow-up timing:** CEO-led (these accounts route to Strategic)
- **Concession posture:** More latitude — transition credits, extended timelines, bounded transition pricing pre-authorized

---

## V. Canonical Tier Feature Reference

Source of truth: [PRICING_CONSTITUTION.md](PRICING_CONSTITUTION.md), D-003b (Tier Fences). All templates, artifacts, and examples must use these exact capability names — no legacy SKU names (e.g., "Sales Portal" is decomposed into Order & Invoice Tracking at T2 and Sales Intelligence at T3).

### T1: Catalog Essentials — $749/mo, 10 included users

| Category | Capabilities |
|----------|-------------|
| **Core Platform** | Admin Console, Automated Data Import, ERP Integration, Multi-Price List Support, Real-Time Inventory, 6 Product Images |
| **eCat iPad App** | eCat iPad App, Barcode Scanning, Curated Product Lists, Document Library, Product Sheets & Reports, Customer History & Favorites |
| **Digital Commerce** | Online Product Catalog |
| **Configurable Products & Payments** | CPQ — à la carte ($195/mo); Credit Card + PCI — à la carte ($195/mo) |
| **Support** | Standard Support |

**Customer-facing headline:** *Your full product catalog in every rep's hands — and an online catalog your buyers can browse on their own.*

**Value pillars:** Field selling tools, online product browsing, one update reaches everyone.

### T2: Commerce Professional — $1,295/mo, 15 included users

Everything in T1, plus:

| Category | Additional Capabilities |
|----------|------------------------|
| **Digital Commerce** | Online Ordering, Private Storefront, Buyer Registration, Customer-Specific Pricing, Quick-Order Grid, Address Validation, Order & Invoice Tracking |
| **Configurable Products & Payments** | CPQ (included), Credit Card Capture + PCI (included) |

**Customer-facing headline:** *Your buyers order online, track shipments, and manage their own accounts — 24/7, no rep required.*

**Value pillars:** Buyers order 24/7, "where's my order?" calls disappear, complex orders handled cleanly.

### T3: Commerce Enterprise — $2,295/mo, 40 included users

Everything in T2, plus:

| Category | Additional Capabilities |
|----------|------------------------|
| **Sales Intelligence** | Sales Intelligence Dashboard, Territory & Performance Views, Sales Reports & Summaries, Data Export (CSV / XLSX) |
| **Product Images** | 12 product images (upgraded from 6) |
| **Support** | Executive Business Reviews |

**Customer-facing headline:** *See what's selling, who's growing, and where to focus — across every channel.*

**Value pillars:** See the full picture, know where to focus, turn activity into answers.

### Graduated User Pricing (all tiers)

| Excess Users | Rate |
|-------------|------|
| 1–10 | $25/user |
| 11–25 | $22/user |
| 26–50 | $20/user |
| 51+ | $18/user |

### Multi-Brand Consolidation (all tiers)

| Tier | Standard Rate | Consolidated Rate (90%) |
|------|-------------|------------------------|
| T1 | $749 | $674 |
| T2 | $1,295 | $1,166 |
| T3 | $2,295 | $2,066 |

One brand included per tier. Additional brands at 90% of natural-tier rate. Per-brand user management (no pooling).

---

## VI. Migration Driver Messaging Spines

Each account has a `migration_driver` that determines the "why your price is changing" explanation. These are the canonical one-sentence explanations and supporting evidence for each driver.

### `user_rate_normalization` (37 accounts, +$14,383 delta)

**One-sentence:** "User pricing is being standardized on a graduated schedule — $25 per user for the first 10 excess users, stepping down to $18 at higher volumes."

**Supporting evidence to include:**
- Current user rate vs. new graduated schedule
- Number of trailing average users and active users
- How many users are absorbed by the new included-user base (10/15/40)
- Net user charge change (often offset by more included users)

**Tone:** Normalization framing. Emphasize that the graduated schedule rewards higher volume.

### `platform_discount_correction` (17 accounts, +$8,817 delta)

**One-sentence:** "Your platform base fee reflects a legacy arrangement from [YEAR]. All accounts are moving to the standard tier rate for the capabilities they use."

**Supporting evidence to include:**
- Legacy platform fee vs. standard tier base
- What the tier includes (feature inventory)
- Tenure on platform
- Discount driver detail from `discount_drivers` field

**Tone:** Direct acknowledgment — "your current rate reflects legacy terms" — not evasion. For >$300/mo delta: "You negotiated a discount at signing. We're retiring all legacy arrangements simultaneously. You are not being singled out."

### `tier_base_increase` (12 accounts, +$4,039 delta)

**One-sentence:** "Your account maps to [Tier], which includes expanded platform capabilities beyond your legacy module configuration."

**Supporting evidence to include:**
- Legacy stack (e.g., "iPad + CPQ") vs. tier-bundled capabilities
- Features the customer gains access to under the new tier
- Current vs. new base comparison

**Tone:** Capability-forward. Lead with what the tier delivers.

### `included_user_reduction` (11 accounts, +$3,840 delta)

**One-sentence:** "Included users are now set by tier — [10/15/40] users included, with excess users priced on the graduated schedule."

**Supporting evidence to include:**
- Previous included users (often 25 as legacy default) vs. new tier inclusion
- How many users become excess and at what rate
- Offset from any base fee change

**Tone:** Transparency framing. "Your legacy plan included 25 users at a flat rate. Your new tier includes [X] users, with a graduated schedule for additional users that rewards volume."

### `multi_org_retirement` (6 primary accounts, +$1,490 delta)

**One-sentence:** "The legacy multi-organization discount is being replaced by multi-brand consolidation — a 90%-of-natural-tier rate for each additional brand under a single platform subscription."

**Supporting evidence to include:**
- Current multi-org discount percentage (typically 10%)
- New consolidation rate and savings vs. standalone pricing
- Entity-level total (from entity table)

**Tone:** Lead with the consolidation option as a partnership benefit. Position the retirement as modernization, not takeaway.

### `annual_discount_retirement` (2 accounts, +$965 delta)

**One-sentence:** "The annual commitment discount from your original agreement is being retired. Annual prepayment remains available as a billing option."

**Supporting evidence to include:**
- Current annual discount value
- Standard tier pricing without discount
- Annual prepay option (billing convenience, not pricing discount)

**Tone:** Brief, factual. Annual prepay is still available — just not at a discount.

### `module_compression` (8 accounts, −$1,290 delta)

**One-sentence:** "Good news — your account maps to a tier where the bundled capabilities cost less than your current module-based configuration."

**Supporting evidence to include:**
- Current itemized module fees vs. new tier base
- Feature parity confirmation

**Tone:** Simple and positive. No upsell, no expansion ask, no relationship preamble.

---

## VII. Concession Language Guardrails

### Kylor-Authorized (can offer in writing)

| Concession | Exact Phrasing |
|------------|---------------|
| **User cleanup window** | "If you'd like to review your active user list before the effective date, we can provide a current user report. Any users deactivated before [EFFECTIVE_DATE] won't be included in the first invoice at the new rate." |
| **Billing date adjustment** | "We can align the effective date with your budget cycle — let us know if a specific month-end works better." |
| **Annual billing option** | "Annual billing is available if that simplifies your budgeting or procurement process — same rate, one invoice." Positioned as a light mention in the notice options or closing — not a concession, not a discount. |
| **30-day transition credit** | "We can apply a one-time 30-day transition credit to smooth the first invoice. The standard rate takes effect the following month." |

### CEO Approval Required

| Concession | When to Escalate |
|------------|-----------------|
| **Permanent discount** | Never offer without CEO approval. No exceptions. |
| **Transition credit > 30 days** | If the account requests more than one month of transition credit. |
| **Discount > 10% of target** | If any concession exceeds 10% of the new annualized rate. |
| **Bounded transition pricing** | Up to 90 days at an intermediate rate (Pre-Engagement + Strategic only). |
| **Custom user arrangement** | Any deviation from the graduated user schedule. |

### Exception ROI Test (from deep research)

Before approving any exception: **allowed concession value ≤ 25% of first-year uplift.** If uplift is $400/month ($4,800/year), total concession should not exceed $1,200 in value. All concessions must have an expiration date — no permanent exceptions.

---

## VIII. Communication Variant Architecture

### Overview: Notices vs. Artifacts

The **notice** is the formal written document satisfying the 60-day contractual requirement. It triggers the legal clock. The **artifact** (value summary, bespoke artifact, entity packet) carries the substance — the value evidence, the pricing explanation, the health data. These are distinct documents with distinct purposes, delivered together.

```
Notice (legal vehicle)  ──────────────  starts the 60-day clock
     │
     ├── Good News Notice              Tailwind — notice IS the communication
     ├── Standard Migration Notice     Core — notice + simplified value summary
     ├── Value Migration Notice        Narrative / Executive / Pre-Engagement — notice + artifact
     ├── Entity Migration Packet       Entity — packet IS the notice for all children
     ├── Strategic Migration Notice    Strategic — sent AFTER CEO conversation
     └── Annual Renewal Notice         Annual — renewal-date framing
```

### Variant 1: Good News Notice

**Segment:** Tailwind (6 accounts)
**Owner:** Kylor
**Companion:** None — the notice IS the entire communication

**Required contents:**
- One-sentence decrease: "Your monthly rate is decreasing from $X to $Y"
- New tier name and base price
- Effective date
- What doesn't change (platform, data, support)
- Kylor's contact for questions

**Excluded:**
- No upsell or expansion ask
- No relationship preamble
- No value artifact
- No percentage framing
- No meeting scheduling

**Length:** 4–6 sentences. This should be the shortest, simplest communication in the portfolio.

### Variant 2: Standard Migration Notice

**Segment:** Core (13 accounts, ≤$200 delta)
**Owner:** Kylor
**Companion:** Simplified Value Summary (attached or linked)

**Required contents:**
- Platform Architecture Narrative (canonical paragraph, health-adapted)
- New tier name + base price
- Included users and graduated user schedule
- Effective date (with 60-day notice language)
- "An account summary is attached with your usage data and tier detail"
- Kylor's contact for questions
- Contractual notice clause: "This notice is provided under your SaaS Licensing Agreement"

**Excluded:**
- No full bespoke artifact
- No percentage framing
- No apology or hedging
- No legacy correction narrative in the notice body (that's in the value summary)
- No meeting scheduling (Kylor available for inbound)

### Variant 3: Value Migration Notice

**Segment:** Narrative (15 accounts, $201–$400) + Executive (8, $401–$600) + Pre-Engagement (8, >$600)
**Owner:** Kylor (Narrative), Kylor + CEO (Executive), CEO leads (Pre-Engagement)
**Companion:** Simplified Value Summary (Narrative) or Full Bespoke Artifact (Executive / Pre-Engagement) + CEO Exec Letter (Executive)

**Required contents:**
- Platform Architecture Narrative (canonical paragraph, health-adapted)
- New tier + pricing
- Reference to the attached/linked artifact: "The attached account review explains the specifics of your pricing and what your platform investment delivers"
- Effective date (with 60-day notice language)
- Contact (Kylor for Narrative; CEO + Kylor for Executive/Pre-Engagement)
- Contractual notice clause

**Excluded:**
- Detailed pricing math (that's in the artifact)
- Percentage framing
- Apology

**Executive variant adds:** CEO exec letter delivered alongside — 3–4 paragraphs acknowledging the change, signaling executive awareness, and offering direct availability. This is a relationship document, not a pricing document.

**Pre-Engagement variant adds:** CEO initiates a call BEFORE the notice is sent. The conversation frames the transition; the notice arrives after.

### Variant 4: Entity Migration Packet

**Segment:** Entity (27 child accounts across ~14 packets)
**Owner:** CEO (complex entities) + Kylor (simpler entities)
**Companion:** Proposed meeting (after packet delivery)

**Required contents:**
- Entity-level cover: aggregate current MRR, aggregate new MRR, total delta
- Per-brand pricing detail table (each child account)
- Consolidated multi-brand option with savings comparison
- Entity health profile (weighted composite)
- 60-day formal notice language covering ALL child brands simultaneously
- Platform Architecture Narrative (entity-adapted)
- "What's Coming" platform investment section
- Proposed meeting: "We'd like to walk through this together — [scheduling link]"

**Excluded:**
- Account-by-account separate notices (the packet IS the notice for all children)
- Brand-by-brand tone variation (entity-level framing throughout)
- Percentage per brand

**Mixed-segment entities** (e.g., Godinger has Entity + Strategic children): The packet covers ALL children including Strategic-routed ones. Maintains entity consistency.

### Variant 5: Strategic Migration Notice

**Segment:** Strategic (19 accounts)
**Owner:** CEO

Sent AFTER CEO conversation. References the discussion. Confirms agreed terms or standard pricing. This is NOT a first-touch document.

### Variant 6: Annual Renewal Notice

**Segment:** Annual (11 accounts)
**Owner:** Kylor + CEO (entity annuals)

Renewal-date framing. Sent ≥90 days before renewal. Uses the substance of the natural segment playbook (Core, Narrative, Executive, etc.) but with renewal-specific timing.

---

## IX. Companion Materials

### Simplified Value Summary

**Used by:** Core (13 accounts) + Narrative (15 accounts) = 28 accounts
**Format:** Single-page HTML, dark SuperCat design language
**Production:** Template-driven, populated from v6 account table + health CSV

**Sections (in order):**

1. **Top bar** — SuperCat · Account Review | [Company] | [Date] · Pricing update effective [DATE]
2. **Health badge** — composite score, top right
3. **Lede** — 2–3 sentences: tenure, key stats, delta spoiled upfront, "this document explains why"
4. **What you've built on SuperCat** — 4+3 stat grid (logins, active reps/users, tenure, feature usage, business results, system health highlights)
5. **Platform health breakdown** — Team Activity / Feature Usage / Business Results / System Health with qualitative status (Exceptional / Strong / Healthy / Developing) and plain-language evidence
6. **What [Tier] includes** — two-column feature inventory for the assigned tier
7. **Why your invoice is changing** — migration driver explanation (from Section V spines) + current-to-new pricing table + graduated user rate table
8. **Tier percentile context** — where this account's new price sits within the tier range (floor / account / ceiling)
9. **What's coming** — June 1 + July 1 platform releases (positioned as evidence of continued investment, not justification)
10. **What happens next** — callout with CS contact and next steps
11. **Footer** — data sourcing and date

**Evidence writing rules for the platform health breakdown (section 5):**

The column header is **"Details"** (not "What this means"). Every evidence sentence must contain at least one concrete number or named feature the client recognizes. Never use a term the client would need defined.

| Area | Formula | Good Example | Bad Example |
|------|---------|-------------|-------------|
| **Team Activity** | [X] reps active out of [Y] provisioned, [Z] logins | "9 of your 20 reps logged in regularly over the last 90 days" | "Broad rep engagement across the organization" |
| **Feature Usage** | Name specific features + % of tier | "Your team uses iPad, catalog, and barcode scanning — every capability in Catalog Essentials" | "Every configured feature in active use" |
| **Business Results** | What's producing output; if gap, name the opportunity | "Your catalog is actively used by reps in the field — adding B2B cart ordering would let buyers order on their own" | "Activity not yet fully converting to tracked outcomes" |
| **System Health** | Catalog completeness %, feed sync status, specific facts | "Your product catalog is 99%+ complete and your import feeds are syncing on schedule" | "Catalog and operations running at strong levels" |

Avoid: "configured channels," "tracked outcomes," "value capture," "commerce outcomes," "operational," "adoption." Use the client's language: reps, buyers, catalog, orders, iPad, cart.

### Full Bespoke Artifact

**Used by:** Executive (8 accounts) + Pre-Engagement (8 accounts) = 16 accounts
**Format:** Rich HTML, dark SuperCat design language
**Production:** Two-axis composition (migration_driver × health_profile). Each artifact is unique.

Same structure as Simplified Value Summary but with:
- Richer driver narrative (dual-correction decomposition if applicable)
- Deeper health dimension analysis with dimension-specific narratives from health CSV
- Net decomposition bar (for multi-driver accounts)
- More detailed current-to-new economics
- CEO exec letter reference (Executive segment)
- Produced during late June, refined by entity conversation feedback

### CEO Exec Letter

**Used by:** Executive (8 accounts)
**Format:** Text (email body or attached letter)
**Production:** CEO co-authored

3–4 paragraphs:
1. Acknowledge the customer relationship and tenure
2. Frame the platform architecture transition at a high level (canonical paragraph, condensed)
3. Signal CEO awareness and ownership: "I've reviewed your account personally"
4. Offer direct availability: "I'm available to discuss directly — [contact]"

Not a pricing document. Not a value justification. A relationship document that signals the change has executive attention.

### Entity Packet

**Used by:** All entity children (~27 accounts across ~14 packets)
**Format:** Multi-section HTML, dark SuperCat design language
**Production:** Requires both account and entity table data

**Sections:**
1. **Entity cover** — entity name, total brands, aggregate current → new MRR, total delta, consolidation option summary
2. **Per-brand detail cards** — for each child: brand name, current stack, current MRR, new tier, new MRR, delta, migration driver headline
3. **Consolidation comparison** — default (independent pricing) vs. consolidated (90% of natural tier per brand), savings amount and percentage
4. **Entity health profile** — weighted composite score, per-brand health scores
5. **What's coming** — June 1 + July 1 platform releases
6. **Formal notice** — 60-day notice language covering all child brands
7. **Proposed meeting** — scheduling link and framing: "We'd like to walk through this together"

---

## X. "What's Coming" — Platform Investment Section

This section appears in value artifacts and entity packets — never in the formal notice. It is evidence of continued platform investment, not justification for the price change. The price change stands on its own.

**Framing line:** *"At your current tier, you have access to every release as it ships — including two already in progress."*

### June 1

- **Rebuilt admin console** — The admin console is getting its first major redesign in years. Faster to navigate, easier to update, cleaner day-to-day management from top to bottom.
- **Rapid fire scanning** — Optimized for high-volume market environments. Your reps write more orders, move between meetings faster, without losing momentum mid-floor.
- **Multiple active orders** — Open more than one order at a time. Start a cart for one account, shift to another buyer, come back without starting over.

### July 1

- **Rep activity log** — Your reps log calls, visits, and follow-up notes inside SuperCat. You see it in one place. One source of truth for what's happening in the field — no separate system needed for the conversations that happen before an order.
- **Direct catalog editing** — Edit product data, configurations, and mappings in a live web view. The export-edit-reimport cycle for small catalog changes goes away.

---

## XI. Anti-Patterns (from Deep Research)

Failure modes identified in the v1 and v2 deep research memos, adapted for SuperCat's context.

| Anti-Pattern | Why It Fails | SuperCat Guardrail |
|-------------|-------------|-------------------|
| **Surprise** | Customers accept price changes; they reject surprises. Unity's Runtime Fee backlash was about unpredictability, not price level. | 60-day written notice + artifact delivered alongside = no surprise |
| **Percentage shock** | +210% sounds punitive even if the absolute dollar change is modest. Percentage amplifies perceived unfairness. | Never introduce percentage. Lead with dollars and tier. |
| **Inconsistent entity messaging** | One brand hears "discount correction," another hears "new tier." Parent entity discovers conflicting messages. | Entity packet covers ALL children with consistent entity-level framing. |
| **Discount drift** | Without guardrails, CS will overuse discounts, extended timelines, waived overages, or special terms to avoid difficult conversations. | Concession menu with explicit Kylor-authorized vs. CEO-required split. Exception ROI test (≤25% of first-year uplift). |
| **Discovery through billing** | Customer's first awareness of the price change is the new invoice amount. | Notice starts the clock. Invoice arrives 60+ days later. |
| **Apology posture** | "We're sorry for the increase" signals that the change is wrong. Undermines the architecture rationale. | Empathetic but not apologetic. Explain clearly; don't hedge. |
| **Feature justification** | "We built these features, so the price is going up" invites "I didn't ask for those features." | Features appear as evidence of investment (after pricing), never as justification (before or alongside pricing). |
| **Loyalty punishment** | Long-tenured customers feel punished for staying. "You've been underpriced" confirms this. | "Your rate reflects legacy terms from [YEAR]" + tenure acknowledgment in lede. |
| **Waiting for meetings to send notice** | Delays the 60-day clock. Meeting manages acceptance; notice starts the clock. | Notice-first. Meeting proposed for entities and Pre-Engagement; available for inbound on all others. |

---

*Prepared May 27, 2026 · Canonical reference for SuperCat pricing migration communication*
