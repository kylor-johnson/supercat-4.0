# 03 — What We Sell (Comms-Ready Language)

> **What this doc owns**: T1/T2/T3 tier definitions in **comms-ready plain English** — the canonical "What You're Getting at $X" verbatim blocks every brief copies from. The customer-facing user-rate ladder ($25 / $22 / $20 / $18, banded 1–10 / 11–25 / 26–50 / 51+). The "What's Coming in 2026" verbatim roadmap block. The implementation-fee tier table. Internal-only peer ranges, competitive-positioning excerpts, and unpublished-premium SKU prices — all clearly tagged `INTERNAL`.
>
> **What this doc DOES NOT own**: The strategic case for moving to tiers at all (`_root/01` §1–2; foundation/03). Voice and tone rules for *how* a brief introduces tier language (`_root/04`). Per-driver narrative content — which tier a customer is moving to, framed for that account's driver (`_root/05`). The data-pipeline fields that carry a customer's `new_tier` value (`_root/07`). The full product surface inventory (foundation/01 — strategic register, not needed in customer-facing comms).
>
> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: foundation `03_how_we_make_money.md` (inlined excerpts in `_meta/stage2_prompts/wave_2_2__03_what_we_sell.md` — §"Stamped price points," §"User expansion," §"Where T2 sits competitively," §"Implementation"); archived brief templates for the "What You're Getting" and "What's Coming in 2026" verbatim blocks (`_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md`, `_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md`, `_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md`, and `Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md`); archived `_handoff-prompt.md` §"Key Reference Tables" (peer ranges, INTERNAL only)

---

## How to use this doc

If you are drafting a per-account brief and you need the "What You're Getting at $X" language for the customer's new tier, you go to **Section 1**, find the matching tier subsection, and copy the fenced verbatim block. No translation. No rewording. The whole point of this doc existing is that the customer sees the same tier description in every brief, regardless of who drafted it.

The user-rate ladder customers see lives in **Section 2 / Block A**. The "What's Coming in 2026" roadmap block every brief should end with lives in **Section 3**.

Sections 5 and 6 are tagged `INTERNAL` and never leave the operator's desk. They exist so the drafter can confirm a new MRR sits "within range" and know which unpublished add-ons to mention only if a customer asks. Per `_root/04` (voice), the brief itself never quotes peer ranges or names unpublished SKUs.

---

## Section 1 — The three tiers, in comms-ready plain English

The three tiers are the only customer-facing product packaging. Pricing, included users, and included brands are stamped per foundation/03 D-004a (2026-02-25).

### T1 — Catalog Essentials

- **Headline price**: **$749/month**
- **Included users**: 10
- **Included brands**: 1

**"What You're Getting at $749/month" — verbatim block for customer briefs:**

> **Catalog Essentials (T1):** At this rate, your team keeps what they're already running — the rep iPad app and your buyer-facing catalog. Your reps carry the full catalog offline, write orders in the field, and sync back. [NEW_INCLUDED] users included and standard support.

*Drafter note: `[NEW_INCLUDED]` is a template variable. For standard T1 accounts on the new architecture, substitute `10`. For legacy accounts whose included base was set higher at signing, substitute that account's `new_included_users` from the v6.2 CSV per `_root/07`.*

**Plain-English feature surface (drafter reference — for tailoring if a brief needs an expanded feature list beyond the verbatim block):**

- Rep app for iPad (offline-capable; field reps carry the full catalog)
- Buyer-facing product catalog
- Standard support
- Up to 10 users included; additional users billed at the graduated ladder in §2

---

### T2 — Commerce Professional

- **Headline price**: **$1,295/month**
- **Included users**: 15
- **Included brands**: 3

**"What You're Getting at $1,295/month" — verbatim block for customer briefs:**

> **Commerce Professional (T2):** At this rate, your team keeps everything they're already running — the rep app, your buyer-facing catalog, online ordering for your accounts, and order and invoice tracking. Your reps and your buyers are both working from the same catalog and customer file. [NEW_INCLUDED] users included, plus a dedicated CSM.

*Drafter note: `[NEW_INCLUDED]` is a template variable. For standard T2 accounts, substitute `15`. For legacy accounts with a non-standard included base, substitute the account's `new_included_users`.*

**Plain-English feature surface (drafter reference):**

- Everything in T1
- Buyer-facing online ordering (self-serve cart for the customer's accounts)
- Order and invoice tracking for buyers
- Dedicated CSM
- Up to 15 users included; up to 3 brands; additional users billed at the graduated ladder in §2

---

### T3 — Commerce Enterprise

- **Headline price**: **$2,295/month**
- **Included users**: 40
- **Included brands**: 5

**"What You're Getting at $2,295/month" — verbatim block for customer briefs:**

> **Commerce Enterprise (T3):** At this rate, your team keeps everything they're already running — the rep app your field team sells from, your buyer-facing catalog, online ordering for your accounts, order and invoice tracking, and your sales intelligence dashboard. Up to 40 users are included, along with a dedicated CSM, priority support, and CPQ and credit card processing. No separate line items for any of it.

*Drafter note: T3's verbatim block hard-codes "Up to 40 users" rather than using a template variable. All three archived templates (Format A, Format B, CEO Letter) phrase T3 identically — no discrepancy.*

**Plain-English feature surface (drafter reference):**

- Everything in T2
- Sales intelligence dashboard
- CPQ (configure-price-quote) capability
- Credit card processing
- Priority support (vs. standard)
- Dedicated CSM (carried from T2)
- Up to 40 users included; up to 5 brands; additional users billed at the graduated ladder in §2

---

## Section 2 — The user-rate ladder

### Block A — Customer-facing ladder (the table customers see in briefs)

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

This table is reproduced verbatim from the Format A, Format B, and CEO Letter brief templates. It is the canonical customer-facing rendering of the graduated user-rate ladder. Briefs render it inside the "Why the Number Is Changing" section whenever the `user_rate_normalization`, `tier_base_increase`, `included_user_reduction`, or `at_book_tier_shift` driver applies (per the driver blocks in those templates).

The bands the customer sees are **1–10 / 11–25 / 26–50 / 51+**. Use these bands. Do not use the foundation excerpt's bands (1–25 / 26–50 / 51–100 / 101+) — see "Flagged discrepancy" below.

### Block B — INTERNAL note on strategic intent

> **INTERNAL.** The ladder's step-declining curve ($25 → $22 → $20 → $18) is the operational fix for Problem 1 in `_root/01` §2 — "the 26th user costs the same as the 200th." The graduated structure creates a volume incentive for accounts that grow their team within SuperCat, without giving up rate on the first incremental users. The ladder is not a discount; it is a rate-card design that aligns price to elasticity. This intent is internal-only because per `_root/04` (voice), customer briefs lead with what the customer gets, not with the strategic rationale.

### Flagged discrepancy — foundation vs. templates (for operator reconciliation)

The foundation excerpt (foundation/03 D-004b, stamped 2026-02-25) lists the ladder bands as:

| Additional users beyond included | Per-user / mo |
|---|---|
| 1–25 | $25 |
| 26–50 | $22 |
| 51–100 | $20 |
| 101+ | $18 |

All four brief templates and `_archive/.../_handoff-prompt.md` §"Key Reference Tables" use the bands above (**1–10 / 11–25 / 26–50 / 51+**). The templates are the iterated artifact and have been used in live brief drafting; per the Wave 2.2 authoring direction, the templates' bands are canonical for customer-facing comms. Foundation/03 likely needs a corresponding update to D-004b so the two registers stop disagreeing. This discrepancy is logged here and in the conformance block; it is not for this doc to resolve unilaterally — `_root/09_changelog.md` should carry the operator's reconciliation when it happens.

---

## Section 3 — "What's Coming in 2026" verbatim block

Every Format A brief closes with a "What's Coming in 2026" section that lists the two in-progress release waves. This is the customer-facing roadmap statement and it is iterated to exact wording. Drafters copy it verbatim from the block below into the customer brief.

**Source:** `Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` §"What's Coming in 2026" (the only archived template that carries this block — see Flagged discrepancy below).

> ## What's Coming in 2026
>
> At this rate, you have access to two releases already in progress:
>
> **June 1**
> - **Rebuilt admin console** — The admin console is getting its first major redesign in years. Faster to navigate, easier to update, cleaner day-to-day management from top to bottom.
> - **Rapid fire scanning** — Optimized for high-volume market environments. Your reps write more orders, move between meetings faster, without losing momentum mid-floor.
> - **Multiple active orders** — Open more than one order at a time. Start a cart for one account, shift to another buyer, come back without starting over.
>
> **July 1**
> - **Rep activity log** — Your reps log calls, visits, and follow-up notes inside SuperCat. You see it in one place. One source of truth for what's happening in the field — no separate system needed for the conversations that happen before an order.
> - **Direct catalog editing** — Edit product data, configurations, and mappings in a live web view. The export-edit-reimport cycle for small catalog changes goes away.
>
> *[Operator note — remove before sending: For T1 accounts, lead with the June 1 field-selling improvements. For T2/T3 accounts with larger rep teams, give equal weight to all five. All five features apply to all accounts.]*

### Coverage rule — "What's Coming in 2026" appears in every brief format

**Operator decision 2026-05-22**: every Stage 3 brief template carries the verbatim "What's Coming in 2026" block above — Format A, Format B, CEO Letter, AND Good News. No exceptions.

Rationale: the asset-side of the migration trade is non-optional. A brief that asks for a rate change (Format A / B / CEO Letter) is one-sided without the roadmap; a price-decrease notice (Good News) reinforces the relationship by showing what's shipping even when the customer is not being asked for more. Drafters of Good News trim other sections to fit the 200–300-word length target; the roadmap is not the section that gets cut.

Historically, only the archived Format A template (`Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md`) rendered the block — the three Pricing Migration archive templates (Format B, CEO Letter, Good News) omitted it. This was a drift; the archived `_handoff-prompt.md` §"Quality Bar" listed "'What's Coming in 2026' section present and verbatim" as a per-draft check. Stage 3 template builds correct the omission; the cleanup item is `CL-005` in `_meta/stage3_cleanup.md`.

---

## Section 4 — Implementation tiers

Tiered by customer **data readiness**, not module count (foundation/03 §"Implementation"):

| Implementation tier | When it applies | Fee |
|---|---|---:|
| **Essentials** | Standard data, ready to import | **Included** in subscription |
| **Guided** | Moderate data prep / mapping required | **$2,500** |
| **Comprehensive** | Heavy data work, multiple sources, custom mapping | **$5,000** |

### Comms framing — recommendation to operator

A search across all four archived brief templates (Format A, Format B, CEO Letter, Good News) finds **no customer-facing language for the implementation-fee tiers**. The word "Essentials" appears only as part of the **Catalog Essentials (T1)** tier name; no template discusses Essentials / Guided / Comprehensive as implementation buckets. The brief artifacts are re-pricing notices for accounts already in production, so implementation fees — which apply at the start of a new account — are out of scope for the active migration comms.

**Recommendation:** unless the operator intends to explicitly reference implementation fees in some future brief variant (for example, a re-implementation conversation tied to a tier upgrade), this section may be reference-only and the implementation-fee table need not appear in customer-facing migration artifacts at all. Pending operator direction, the table above stands as the canonical source if a future brief format does need it.

---

## Section 5 — Peer ranges and competitive positioning (INTERNAL — strip before send)

> **INTERNAL ONLY.** The peer ranges and competitive comparisons in this section are reference for the drafter to confirm a new MRR sits "within range." They are never quoted to the customer. They never appear in customer-facing artifacts. The "How This Compares" section of a brief uses peer ranges as a CHECK — the brief itself states "this falls within the typical range for accounts of your size and usage" without naming dollar values. The customer never sees the floor, midpoint, or ceiling. The customer never sees the competitive table. See `_root/04` for the comms-ready treatment of "How This Compares."

### Peer ranges per tier — drafter check only

Source: `_archive/2026-05-22__pre-refactor/_handoff-prompt.md` §"Key Reference Tables."

| Tier | Floor | ~Midpoint | Ceiling |
|---|---:|---:|---:|
| T1 | $774 | ~$1,200 | $1,629 |
| T2 | $1,295 | ~$1,440 | $1,589 |
| T3 | $2,295 | ~$2,585 | $2,875 |

**Positioning convention used in the archived Format A template "How This Compares" block** (verbatim from the archive — for drafter reference only, do not lift dollar values into customer copy):

- `NEW_MRR < midpoint` → "below the midpoint"
- Within ±$75 of midpoint → "near the midpoint"
- `NEW_MRR > midpoint + $75` → "above the midpoint" — REQUIRED to include a user-count clause explaining the position, e.g., "…driven by your team size at [N] users — the platform base itself is at the [TIER] standard."

A brief never states "this account is above/below the midpoint of $X–$Y." It uses qualitative range language only. The dollar table above is the drafter's verification tool.

### Competitive positioning — strategic reference

Source: foundation `03_how_we_make_money.md` §"Where T2 sits competitively" (inlined here from the Wave 2.2 prompt — do not navigate to the foundation source).

| Tier | SuperCat | AmpTab equivalent | Pepperi equivalent | Notes |
|---|---:|---:|---:|---|
| T1 ($749) | $749/mo | AmpTab Starter $500/mo (sticker) / $917/mo (Y1 effective with $5K setup amortized) | Pepperi Pro $1,220/mo at 15 users | SuperCat sits in the competitive sweet spot |
| T2 ($1,295) | $1,295/mo | AmpTab Advanced $1,000/mo / $1,833/mo Y1 effective | Pepperi Corporate $3,450/mo at 25 users | SuperCat is the clear value play |
| T3 ($2,295) | $2,295/mo | AmpTab Pro $3,000/mo / $5,500/mo Y1 effective | Pepperi Ultimate $6,400+/mo | SuperCat is 23% below AmpTab Pro sticker, ~58% below Y1 effective |

Stripping out raw rate-card differences, **SuperCat's full-stack Y1 effective price is within 15% of AmpTab at every tier**.

These competitive numbers never appear in a customer brief. They live here so the operator can answer a competitive-displacement question in a follow-up call without leaving the migration directory.

### Tier-ratio sanity check (INTERNAL)

From foundation/03 D-004a: T2/T1 = 1.7×; T3/T2 = 1.8×; T3/T1 = 3.1× — squarely within the 1.5–2.5× best-practice band for Good/Better/Best packaging. This is a structural check that the tier card is internally consistent. Never customer-facing.

---

## Section 6 — Add-ons and unpublished premiums (INTERNAL — never in proactive comms)

> **INTERNAL ONLY.** The SKUs below are unpublished add-ons. They do not appear in the rate card. They are NEVER named in a proactive migration communication. They surface only when a customer asks a specific question that one of them answers (e.g., "do you have premium support?"). Pricing the customer hears in a brief is `current_mrr → new_mrr` per the brief table. Add-ons are a separate, response-only conversation.

| Unpublished SKU | Monthly price | When it surfaces |
|---|---:|---|
| Commerce (add-on) | $795/mo | Response-only: customer asks about extending commerce features beyond their tier |
| Sales Intelligence (add-on) | $995/mo | Response-only: customer at T1/T2 asks about adding analytics surfaces beyond their tier |
| Premium Support (add-on) | $495/mo | Response-only: customer asks about elevated support, faster SLAs, or named contacts beyond what their tier includes |

**Drafter rule.** Do not mention these SKUs in any "What You're Getting at $X" block, in any "What's Coming in 2026" block, in any roadmap reference, or in any "How This Compares" framing. They exist for the CSM/CEO to deploy in a 1:1 conversation when the customer specifically asks. The migration brief itself is silent on them.

**Source**: foundation `03_how_we_make_money.md` §"Unpublished à la carte premiums" — **stamped decision D-004d, 2026-02-25**. The full SKU descriptions per the stamped decision: **Commerce** = "CPQ + advanced configuration"; **Sales Intelligence** = "T2 customers wanting the analytics layer without full T3"; **Premium Support** = standalone premium-tier support without a full T-tier upgrade. Prices above are the stamped values; if foundation/03 publishes a superseding decision, this section gets updated and logged in `_root/09_changelog.md`.

---

## Section 7 — What this doc does NOT own

- **The "why we're moving to tiers at all" reasoning** → `_root/01` §1–2 (the thesis and the five structural problems being solved).
- **Voice and tone rules for *how* to introduce tier language in a brief** → `_root/04` (the rule that the lede names the relationship before the price, the prohibition on percentage-first framing, the "above the midpoint" comparative-language constraints).
- **Per-driver narrative content** — which tier a customer is moving to, framed for that account's driver (`user_rate_normalization`, `tier_base_increase`, `included_user_reduction`, `platform_discount_correction`, `at_book_tier_shift`, `multi_org_retirement`, `annual_discount_retirement`, `special_arrangement`) → `_root/05`.
- **Format selection** — which brief format (A / B / CEO Letter / Good News) carries which combination of tier + driver + delta + health → `_root/06`.
- **The data field that carries a customer's `new_tier` value** in the v6.2 CSV, along with `new_tier_base`, `new_included_users`, `current_mrr`, `new_mrr`, and the user-count fields that feed the brief tables → `_root/07`.
- **Quality-bar checks** — the per-draft confirmation that the right verbatim block was used, the right ladder bands appear, and the "What's Coming in 2026" block is present and unmodified → `_root/08`.

This doc is the **product-language source of truth**. Every brief draws its tier descriptions, user-rate ladder, and roadmap copy from here. Everything else — when to talk, how to talk, which driver, which format — lives in the docs above.
