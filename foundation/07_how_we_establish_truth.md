# SuperCat — How We Establish Truth (Epistemic Foundation)

> **What this is**: The second pillar of `foundation/`. The first seven docs
> (`00`–`06`) are **strategic** ground truth — *who we are, who we serve, how we
> make money, where we're going.* This doc is **epistemic** ground truth — *how
> we decide what is true, and how confident we are allowed to be, before we emit
> a single number.* It is domain-agnostic on purpose: it governs any report,
> agent, or analysis that makes a claim from data.
>
> **Last updated**: 2026-07-02 · **Owner**: CEO + Head of CS · **Review cadence**: when the Spine changes materially
>
> **Canonical source (Tier 0)**: This doc is a distilled, socializable summary of
> [`skills/insightful_product/00_provenance_spine.md`](../skills/insightful_product/00_provenance_spine.md).
> The Spine is the authority — validated against a live Postgres cohort and carrying
> the full gate/SQL/identity detail. **Where this summary and the Spine ever
> disagree, the Spine wins.** This is an inheriting summary, not a fork: keep it
> principles-only (no SQL, no per-org numbers, no gate bodies), and re-distill it
> when the Spine changes in a way that changes a principle.

---

## Why this is foundation

A number stated without knowing whether it is *true* and *how complete* is worse
than no number — it manufactures false confidence and, in a client-facing
product, reputational risk. Strategy tells us *what matters*; this pillar tells
us *what we're allowed to say we know*. Both are first-order: an agent should
carry this discipline before it reasons, exactly as it carries the ICP or the
pricing model.

The rules below were forged building SuperCat's insight product (Commerce truth,
Rep Copilot, Customer Profiles) on real customer data, but the **discipline is
universal** — it improves any SuperCat report that cites a figure.

---

## The principles

**1. Name the source of truth before trusting a number.**
For commercial outcomes, the ERP is the only source of truth: a sale is real when
it is **invoiced** (shipped + billed), or, failing an invoice feed, when it is a
consummated order in the ERP. Everything upstream — an app order, a cart, a quote,
a pipeline stage — is **intent**, not a transaction. Generalize the habit: for any
claim, know which system is authoritative and stamp it on the output.

**1a. Selling instrument ≠ order consummation (narrative binds with the number).**
eCat iPad is a **rep selling tool** (browse → configure → present → write). Consummation
often stays in ERP or other channels even when the rep sold well on iPad. Do not narrate
low SuperCat-submitted volume as failed “eCat adoption” or as proof the account’s
workflow is broken. Channel-provenance numbers and this product narrative are one
discipline — see [`02_who_we_serve.md`](02_who_we_serve.md) § Selling instrument vs order
consummation and [`01_what_we_do.md`](01_what_we_do.md) Surface 1.

**2. Capture is a fact; attribution is a gated estimate. Never blur them.**
What flows verifiably through our own rails is *capture* (numerator and
denominator both ours). A claim about our *share of, or influence on,* a larger
whole is *attribution* — its denominator belongs to someone else and is only as
complete as we can prove. Never present an attribution estimate as a captured
fact, or a captured fact as the whole.

**3. Every total carries confidence and completeness. No bare numbers.**
Two labels ride on every meaningful figure: a **confidence tier** and, for any
total/denominator, a **completeness state**.

| Tier | Meaning | Behavior |
|---|---|---|
| **FULL** | Internally consistent *and* independently corroborated complete | Headline truth |
| **STRONG** | Authoritative feed present, fresh, consistent; completeness not independently corroborated | Report with a one-line completeness caveat |
| **PARTIAL** | Feed present but stale, provably incomplete, or lower-grain than the claim | Report ranges/directional only; label loudly |
| **LIMITED** | Only coarse data (no dates/detail) | Magnitude only; most detail suppressed |
| **NONE** | No usable feed | **Suppress**; offer only what a different, available source can honestly support |

**4. The binding rule: a composite inherits the *lowest* confidence of its inputs — or it is suppressed.** Confidence never increases by combining inputs. When the honest answer is "we can't stand behind this," **suppress rather than guess.**

**5. Billed is not collected.** An invoiced/billed figure is not cash received.
Never imply collection, AR health, DSO, or "money in the bank" from billing data
alone. (The general form: don't let a number imply a stronger claim than its
source supports.)

**6. Identities are not clean keys — gaps are real, and silence is not zero.**
The joins we most want (person ↔ outcome, entity ↔ parent, record ↔ record) often
aren't stored as reliable keys. When a mapping is incomplete, **degrade the grain
(or suppress), and never silently drop the unmapped rows** — dropping unmatched
reps from a revenue ranking fabricates a leaderboard. Report the match rate as
part of the claim.

**7. First-party behavior over imposed labels.** Segments, types, and scores are
**derived from what customers actually do**, never imposed from an external label
or an LLM-enrichment guess. Enrichment is validated *against*, never seeded
*from*; known-biasing enrichment is excluded as an input.

**8. Label live vs. illustrative, and lead with the decision.** Mark figures as
real (`[from-live]`) vs. designed/example (`[ILLUSTRATIVE]`) so no one mistakes a
placeholder for a measurement. Lead with the decision/"so what"; method and
caveats are drill-down, never buried and never omitted.

---

## How this applies to the CEO System

This is a **house-wide reasoning standard**, applied in proportion to how much a
report leans on figures:

- **Binds hardest** where we consume customer commercial data directly — the
  `insightful_product` skill's per-customer reports must obey the Spine in full.
- **Applies as discipline** to any CEO System artifact that cites commercial or
  customer reality (e.g. `growth_reality`, `voice_of_market`, `weekly_CEO_digest`):
  label confidence/completeness, keep capture vs. attribution straight, don't
  imply collection from billing, prefer first-party signal over enrichment.
- **Applies lightly everywhere else** as the generic "be honest with numbers"
  posture — cheap to inherit, harmless where there are no figures.

The runtime-facing condensation of these principles lives in
[`CEO_SYSTEM_CONTEXT.md`](CEO_SYSTEM_CONTEXT.md) ("Data & number discipline"),
which is read at run start by the artifacts above.

---

## What this set is not

- **Not the implementation.** The gates, SQL, per-org coverage, identity tiers,
  and validation cohorts live in the Spine and the query library, not here.
- **Not optional for client-facing numbers.** For anything a customer could see,
  the Spine is binding, not advisory.
- **Not static.** When the Spine adds or changes a principle, re-distill this doc
  and bump both dates.
