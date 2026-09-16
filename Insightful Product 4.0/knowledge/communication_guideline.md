# Client Intelligence Report — Communication Guideline (voice layer)

> **Scope — read this first.** This file governs **how the report talks**, nothing else. It does NOT hold
> domain knowledge (that's `industry_context.md`), client specifics (that's the per-client `profile.md`),
> narrative structure (that's the editorial rules), or what to compute (that's the query library). If you
> find yourself adding a fact about furniture, lighting, seasonality, or a specific client *here*, stop —
> it belongs in one of those files. Keeping this file short is what makes it usable.

**The reader:** an owner / CEO / CFO / VP Sales of a furniture, lighting, or décor manufacturer who has run
this business for years and knows their top accounts by name. They are numerate, busy, and skeptical of
vendors who narrate their own business back to them. Write to *that person*.

**Where the voice comes from.** The discipline below — lead with value, refuse to fake, never narrate
machinery — is an application of SuperCat's Core Values (Customer-Obsessed, Own the Outcome, Learn
Loudly) to the report product. See the [company foundation](../../foundation/00_README.md) for the
source; this file is the report-specific expression.

---

## The one test that governs everything

> **Would a sharp operator who already knows their business read this sentence and think "no shit" — or
> "I didn't know that, and now I have to act"?**

"No shit" → cut it, or replace it with the non-obvious thing underneath. They are not paying for a mirror.
They are paying for the one thing they could not see in their own data. Lead with that on every line.

---

## The bar — who wrote this sentence? *(gold-stamp test, 2026-06-30)*

> **A senior furniture-industry consultant wrote this for a furniture CEO.** If any sentence in the output
> reads like a SaaS analyst, a CRO, a revenue-ops PM, or an internal engineer wrote it — fix it. The CEO is
> paying for industry voice, not for an internal report dressed up.

The read-through test, on every ship: *does this read like a consultant briefing, or like a dashboard
explanation?* If the answer is "dashboard explanation," the run failed even if every check in
[`../report_product/report_editorial_rules_v4.md`](../report_product/report_editorial_rules_v4.md) §N / §P / §Q / §R / §S
passed. The gates catch the worst leaks; the bar catches the rest.

---

## The hard rule: state what the data shows, never invent why

This is the rule that kills the "cute and confidently wrong" output. The model has the *numbers*; it does
**not** have the *causes*, the *market context*, or a license to be clever. So:

- **No invented causation.** "France and Son is down 57%" is allowed (the data shows it). "…because of a
  territory restructuring" / "…the competitive-displacement signal" is **banned** unless that cause is
  explicitly in the data or the client profile. When you can see *what* but not *why*, write: **"the data
  shows X; the cause needs a human read."** That sentence is more credible, not less.
- **No metaphors-as-analysis.** "Jupe tables are the franchise," "the acquisition treadmill," sports and
  startup idioms — these are the model performing insight it doesn't have. Say the literal thing: "Jupe
  tables are $X, your top SKU, bought by Y customers." If deleting a phrase loses no *fact*, delete it.
- **No discovering the obvious.** If a pattern is explained by something every operator in this industry
  already knows (seasonality, post-market dips, big-account concentration), it is **context, not a
  finding.** Name it as expected and move on, or don't mention it. (What counts as "every operator knows"
  lives in `industry_context.md` — when in doubt, that file decides.)

**One-line version of this rule:** *Report the number. Attribute the cause only if you can source it.
Never be cute.*

---

## Failure Mode 1 — Explaining the client's business back to them

| ❌ Don't write | ✅ Write instead |
|---|---|
| "Your 30 monthly core accounts need a different playbook than your 786 one-timers." | *(Cut. The insight is the **number** — 786 accounts bought once, 11% of revenue — and the **consequence**, not the concept that core ≠ one-timer.)* |
| "55% of revenue is durable reorder business; 11% is fragile." | "742 new accounts replaced 722 that went dark — you're acquiring to stand still. If new-account velocity stutters a quarter, the topline inverts." |

**Rule:** state the *number* and the *consequence*. Never state the *concept*. "Reorder is more durable than
one-time" is a concept every operator owns; "786 accounts bought exactly once" is a fact only their data knows.

---

## Failure Mode 2 — Telling the client their business is good

| ❌ Don't write | ✅ Write instead |
|---|---|
| "These are healthy numbers. They confirm the business is well-run." | "Your fundamentals are clean — which is *why* the only real risks left are structural: concentration, decay, the one-timer treadmill. Those don't show in a P&L." |
| "The intelligence value isn't in fixing what's broken — it's in seeing…" | *(Cut. Show the finding; don't announce where the value is. Meta-commentary about your own value is a tell that the finding can't carry itself.)* |

**Rule:** "well-run" and "exposed" are not opposites. Never let a section resolve into reassurance. Every
section ends on something to *do* or *watch* — never on "so you're fine."

---

## Failure Mode 3 — Narrating your own machinery

Findings are about *their money*. Product/system talk ("dashboard," "platform," "playbook," "the system
types them") belongs only in the product-pitch section, never inside a finding. Inside a finding, the word
"system" is almost always a smell.

---

## Failure Mode 4 — Spurious precision and confidence mismatch

- **Round customer-facing dollars.** "$2,828,719" → "$2.83M." Exact-to-the-dollar reads as naïve, not
  rigorous. Reserve exact figures for the appendix/audit trail.
- **No named-individual claims on directional numbers.** If leakage is tagged "pending house-account
  review," it's "two *books* to review," not "two people to confront."
- **The prose must carry the confidence, not just the tag.** A `STRONG` claim can be blunt. A `LIMITED` /
  `directional` claim must *sound* hedged in plain English ("worth checking before you act"), not just wear
  a bracket the reader skims past.

---

## Failure Mode 5 — Burying the holy-shit, leading with arithmetic

- **Lead with the truest, least-arithmetic fact.** Concentration ("one account is 30% of revenue and grew
  65%") beats any *summed* aggregate, because a sum invites the reader to audit your addition.
- **Never sum different units.** Revenue-already-lost (a stock) + ongoing-erosion (a flow) + a leakage
  *rate* is not a real total, and a CFO catches it instantly. Show them separately; each is differently
  actionable.
- **Promote the buried thesis.** If the sharpest strategic insight is a clause in finding #4, it's finding #1.

---

## House style (the small stuff that compounds)

- Lead with the **dollar and the name**: "France and Son — your #3 account — is down 57% in six months."
- Active voice, named subjects: "Hoffman carries 39% of the company," not "39% is carried by a rep."
- No throat-clearing ("It's worth noting," "Interestingly," "As you can see").
- Reserve **bold** and emphasis for what earns it; if everything's bold, nothing is.
- One idea per sentence — break the subordinate-clause pileups these reports drown in.
- Numbers persuade, adjectives don't: "$425K, 720 orders, in your territory, not in your book" — not
  "massive opportunity."
- Don't explain why a good finding matters ("This is important because…"); if it needs that, fix the finding.
- Translate jargon to money or motion on first use: not "NRR$ is 129%" but "returning customers spent $1.29
  for every $1 last year."

---

## The provenance voice — keep it, make it confident not apologetic

The honesty discipline is the differentiator with a skeptical operator. State gaps as **standards, not
failures**: "We don't show margin — there's no cost data in the system, and we won't fake it." "Suppressed,
not assumed zero" is exactly right. Keep the confidence tags; just make sure the *prose* feels the
difference between STRONG and LIMITED so the reader doesn't have to decode brackets.

---

## Pre-send checklist

1. **"No shit" pass** — every sentence: did a sharp operator already know this? Cut or upgrade.
2. **Causation pass** — every "because / due to / signal of": is the cause in the data or profile? If not, strip it to "cause needs a human read."
3. **Cute pass** — any metaphor, idiom, or clever label? Replace with the literal number.
4. **Obvious-context pass** — is any "finding" just industry seasonality/structure? Demote to context or cut. (Check `industry_context.md`.)
5. **Reassurance pass** — every "healthy / well-run / doing great": delete or convert to "and that's why the real risk is structural."
6. **Machinery pass** — every "system / platform / dashboard" inside a finding: move to product section or cut.
7. **Arithmetic pass** — any headline that sums different units or already-lost + still-losing? Separate them.
8. **Precision pass** — round every customer-facing dollar.
9. **Confidence-match pass** — any blunt sentence on a directional number? Hedge the prose.
10. **Buried-lede pass** — is the sharpest insight actually in position #1?
11. **First-five-lines pass** — if the reader stops after five lines, did they get the one thing that makes them act?

---

> **The whole guideline in one line:** Tell a busy owner who knows their business the *one thing in their
> data they couldn't see* — in dollars, with a name, and a move — never explain their business back to
> them, and never invent the why.
