---
name: truth-discipline
description: "SuperCat's epistemic standard — how to decide whether a number can be stated at all, and how confident you're allowed to sound. Covers source-of-truth naming (invoiced/ERP vs. intent), capture vs. attribution, the five confidence tiers and the binding rule, billed ≠ collected, identity-gap handling, first-party signal over enrichment, and suppress-rather-than-guess. Use this skill whenever a response, report, chart, deck, or query result will state a figure about customers, revenue, GMV, orders, reps, adoption, health scores, or market size — including internal analysis, QBR prep, a Slack answer, or a single number dropped mid-sentence. Trigger it during data work even when nobody asked about confidence: the standard binds on the output, not on the question. Anything a customer could see is governed by the Spine, not by judgment."
---

# Truth discipline (epistemic standard)

A number stated without knowing whether it is true and how complete it is is
worse than no number — it manufactures false confidence, and in client-facing
work, reputational risk. Carry this before you reason, not after you draft.

**Authority chain**: `Insightful Product 4.0/foundation/provenance_spine.md` (Tier 0,
canonical) → `foundation/07_how_we_establish_truth.md` (socializable summary) →
`foundation/CEO_SYSTEM_CONTEXT.md` (runtime condensation). **On any conflict,
the Spine wins.** For client-facing numbers the Spine is binding, not advisory —
read it rather than relying on this summary.

**If the Spine isn't reachable** (you're outside the repo), the nine principles
below still bind — they are complete as stated. What you lose is the gate catalog
and the identity-resolution tiers. So when a claim needs a named gate, degrade to
suppression and say which gate you couldn't check, rather than improvising one
that sounds plausible.

## The nine principles

**1. Name the source of truth before trusting a number.** For commercial
outcomes the ERP is the only source of truth: a sale is real when **invoiced**
(shipped + billed), or failing an invoice feed, when it is a consummated order in
the ERP. An app order, cart, quote, or pipeline stage is **intent**, not a
transaction. Stamp the authoritative system on the output.

**2. Selling instrument ≠ order consummation.** eCat iPad is a rep selling tool.
Consummation often stays in ERP, email, phone, EDI, or at market even when the
rep sold well on iPad. Never narrate low SuperCat-submitted volume as failed
"eCat adoption" or as proof the account's workflow is broken. The
channel-provenance number and this narrative are one discipline, not two.

**3. Capture is a fact; attribution is a gated estimate. Never blur them.** What
flows verifiably through our own rails is *capture* — numerator and denominator
both ours. A claim about our *share of, or influence on,* a larger whole is
*attribution*; its denominator belongs to someone else and is only as complete as
we can prove. Never present attribution as captured fact, or capture as the whole.

**4. Every total carries confidence and completeness. No bare numbers.**

| Tier | Meaning | Behavior |
|---|---|---|
| **FULL** | Internally consistent *and* independently corroborated complete | Headline truth |
| **STRONG** | Authoritative feed present, fresh, consistent; completeness not independently corroborated | Report with a one-line completeness caveat |
| **PARTIAL** | Feed present but stale, provably incomplete, or lower-grain than the claim | Ranges/directional only; label loudly |
| **LIMITED** | Only coarse data (no dates/detail) | Magnitude only; suppress most detail |
| **NONE** | No usable feed | **Suppress**; offer only what a different available source honestly supports |

**5. The binding rule: a composite inherits the *lowest* confidence of its
inputs — or it is suppressed.** Confidence never increases by combining inputs.
When the honest answer is "we can't stand behind this," **suppress rather than
guess.** Suppression is a valid deliverable; a hedged guess is not.

**6. Billed is not collected.** An invoiced figure is not cash received. Never
imply collection, AR health, DSO, or "money in the bank" from billing data alone.
General form: don't let a number imply a stronger claim than its source supports.

**7. Identities are not clean keys — gaps are real, and silence is not zero.**
The joins we most want (rep ↔ outcome, entity ↔ parent, record ↔ record) often
aren't stored as reliable keys. When a mapping is incomplete, **degrade the grain
or suppress, and never silently drop the unmapped rows** — dropping unmatched
reps from a revenue ranking fabricates a leaderboard. **Report the match rate as
part of the claim.**

**8. First-party behavior over imposed labels.** Segments, types, and scores
derive from what customers actually do — never from an external label or an
LLM-enrichment guess. Enrichment is validated *against*, never seeded *from*;
known-biasing enrichment is excluded as an input.

**9. Label live vs. illustrative, and lead with the decision.** Mark figures
`[from-live]` vs. `[ILLUSTRATIVE]` so nobody mistakes a placeholder for a
measurement. Lead with the decision and the "so what"; method and caveats are
drill-down — never buried, never omitted.

## When to go to the Spine instead of stopping here

This file is principles-only by design — no SQL, no gate bodies, no per-org
coverage. Go read `Insightful Product 4.0/foundation/provenance_spine.md` when
you need:

| You need | Spine section |
|---|---|
| The re-keying distortion as a structural fact | § 2 |
| Commerce Origin Taxonomy (how to classify a channel) | § 3 |
| What sets a tier, and the binding rule in one line | § 5.2–5.3 |
| A named gate — provenance/channel preflight, feed completeness, date clamps, eCat-SALE filter, row caps, economics preflight | § 6 |
| Whether an economics gap is suppressible or approximable | § 6.9 |
| Price realization / leakage methodology | § 6.10 |
| Identity resolution — rep, customer/parent, territory, product, customer "type" | § 7 |
| This Spine's empirical validation basis | § 9 |

## Known data traps (check before querying)

**`quickbooks__invoice` in BigQuery must be deduplicated. Always.** The WELD_RAW
table has two defects that silently produce wrong numbers:

- **Duplicate historical rows** — Weld appends a new row version when an invoice
  changes in QBO, but stale rows remain. A bare `WHERE balance > 0` picks up old
  snapshots of invoices that have since been paid, inflating AR and overdue.
- **Missing updates** — some invoices voided, deleted, or paid in QBO never had
  the update synced. The only row carries the full original balance.

Before running any balance, AR, overdue, or payment query, read
`QBO_Invoice_BigQuery_Dedup_Guide_README.md` (workspace root) and use its
`ROW_NUMBER() OVER (PARTITION BY doc_number ORDER BY
meta_data_last_updated_time DESC)` pattern. Note that dedup fixes defect one but
**not** defect two — a deduplicated balance is still `PARTIAL` at best, because
the missing-update population is unmeasured from inside this feed. Never present
a QBO-derived AR or overdue figure as `STRONG` on the strength of dedup alone,
and never let it imply cash position (principle 6).

**Source-specific junk traps live in `supercat-data-routing`, not here.** That
skill carries the per-source artifacts that silently corrupt a result before any
confidence tier is applied — Facebook Ads tables mixed into the `helpscout`
dataset, `test20260311*` leftover tables, and zero-row tables (`helpscout.teams`,
`team_members`, `inbox_custom_fields`) whose emptiness is an artifact, not a
finding of "no data." **Consult it before tiering any query result**: a tier
assigned to a junk-polluted or artifact-empty result is confidence theater, and
reading emptiness as zero is principle 7's silence-is-not-zero failure wearing a
different hat.

## How hard this binds

- **Hardest** where we consume customer commercial data directly — per-customer
  reports from `Insightful Product 4.0/` must obey the Spine in full.
- **As discipline** on any artifact citing commercial or customer reality
  (`growth_reality`, `voice_of_market`, `weekly_CEO_digest`): label
  confidence/completeness, keep capture vs. attribution straight, don't imply
  collection from billing, prefer first-party signal.
- **Lightly everywhere else** as the generic "be honest with numbers" posture.

## One related trap worth carrying

There is **no canonical install-base count.** 104 / 109 / 110 / 118 / 132 are all
internally valid under different inclusion rules and dates. Name the one you used
and its window; never average them or present one as "our customer count." See
the `supercat-foundation` skill.

## The standard binds on capability claims too, not just figures

Everything above is written about numbers. The same bar applies to **statements about what
the product does** the moment they enter customer-facing text — an email, a scoping doc, a
proposal, a commitment on a call.

A capability claim in client copy is a stated fact. Before it ships, it needs the same
grounding a dollar figure would need: live code, live config, the live KB, or a live page.
Failures observed 2026-08-25, all three drafted into a client email before being checked:

- "extra columns are picked up as custom fields" — actually requires a `header_` / `footer_`
  / `item_` prefix; an arbitrarily named column is silently ignored.
- "smart list visibility is set per user" — it is set per **user group**.
- "the demo login didn't have ordering enabled" — an inference; the site had ordering on and
  the actual cause was never established.

Two rules that would have caught all three:

1. **A skill is evidence, not proof.** Skills go stale. On 2026-08-25 two skills documented
   an HTTP API that returns 404 in production, two KB slugs that 404, and three DB columns
   that do not exist. When a claim is load-bearing for a client, verify against the live
   artifact and update the skill when it is wrong.
2. **Name the inference.** "Most likely X" and "X" read identically once pasted into an
   email. If you have not verified the cause, write the symptom and say you'll confirm.

Cheapest guard: before sending, reread the draft and ask of each factual sentence, *what did
I actually check?* Anything answered "the skill said so" or "it follows" gets verified or
softened.
