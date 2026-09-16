# Historical Health Score Backfill — What It Actually Tells Us

**For:** Pricing migration planning  
**What this is:** We re-ran Health V3 for six month-end snapshots (Nov 2025 through Apr 2026) and stacked them against the May 2026 production scorecard. The goal wasn’t perfection — historical adoption and catalog optics are fuzzy — but to see whether the **shape of the portfolio** and **who slips** stays consistent enough to inform how you tier customers during a migration.

---

## The headline he can carry into pricing conversations

**Most of your book looks fine.** Roughly five in six accounts sit in the stronger half of the model (Thriving or Healthy). The stress is concentrated: a **tiny tail** shows real distress patterns, while a **somewhat larger middle** spends time in Watch without fully breaking. That’s useful for migration: **you’re not managing a uniformly fragile base** — you’re managing a **skewed portfolio** where revenue-weighted outliers matter disproportionately.

Second headline: **when accounts go sideways, orders usually blink out first.** Usage and engagement often follow weeks or a month later. For pricing moves, read that as — **commercial tension shows up before “they stopped logging in.”** Listening on order cadence / rep workflow beats waiting for churn signals that arrive late.

---

## How bands work in practice (why this matters when you tie price to tier)

Production behavior is **five** ordered buckets, not the four-band shorthand some docs still imply. Roughly speaking you have a strong upper tier (**Thriving**), then **Healthy**, then **Watch**, then **At Risk**, then **Critical**. There’s also a **behavioral floor**: several accounts hug **exactly score 40** and sit in **Watch** artificially. So from a migration lens:

- Band labels are **reasonable for routing** (“who gets a proactive call”), but  
- Treat **score 40 Watch** clusters as **“needs second look,”** not as “lightly fine.”  

If pricing tiers ever map to headline health bands, disclose the floor internally so sales and CS aren’t debating ghosts.

---

## What six months + May showed portfolio-wide

- **Roughly 102–104 orgs scored per month** once the stable panel settles; two joins mid-window.  
- **January** was the best month overall — strongest average score and biggest Thriving cohort. Useful as **“normal good” baseline** when you compare quarters.  
- **April** stood out softer: slightly more orgs slid into Watch+. Not a catastrophe, but **the clearest month-level wobble** in the series — worth remembering if Q2 pricing outreach coincides with natural seasonal softness.  
- **Value Delivery** (orders) **trended down a couple of points**, while Adoption and Ops were comparatively flat and Engagement floated a bit. Translation: macro drag in the panels **shows up in commerce throughput**, not in “whether they flipped feature flags six months ago” (those adoption numbers are noisy historically anyway).

Bottom line for pricing: **the composite already leans optimistic at the median** — migration risk hides in **thin tails and in Watch-band revenue**, not in the headline “average client is healthy.”

---

## WHO actually looks sick (and WHO is just weird)

Across all seven snapshots, **only two accounts** were trapped in **At Risk or Critical essentially the entire time**:

- **`tel` — collapsing story.** Orders go to effectively zero early; engagement then craters. Ops looks frozen (single import posture with no freshness). Escalations never lit on fire in the extracts we had. For migration: assume **commercial rescue + technical unblock** simultaneously — price alone won't fix inertia that deep.  
- **`krb` — chronic catalog-without-commerce.** Engagement wobbles; orders stay at zero seven months straight. Imports still happen. For migration this behaves like someone paying for tooling they use as browse-only — economics of an uplift may hinge on enablement narrative, not on “their score says they hate us.”

**Rapid plunges** (big one-month composite drops) hit **several brands** but **often mean-reverted** within a quarter. The ones **that stayed wrong** overwhelmingly shared **`Value Delivery pinned at zero`** — stalled orders rather than flaky login counts.

Recoveries happened too (**`ol`** is the textbook bounce — orders came back fast once activity resumed). So the model distinguishes **panic vs. ditch** moderately well once you stare at pillars, not ONLY at composite deltas.

---

## Connecting this to YOUR pricing migration (plain English)

Here’s where health scores genuinely help—and where they shouldn’t dictate price by themselves.

### Where health helps

**1. Routing and sequencing.** You can align migration waves roughly as:

| Signal | Practical migration angle |
|--------|---------------------------|
| Thriving / stable Healthy | Default path; standard enablement collateral |
| Watch with healthy pillars except orders | Probe **commercial motion** — maybe pricing isn’t objection; maybe pipeline went quiet |
| Watch parked at behavioral floor (~40 composite) | **Human review**, not autopilot tiers — composite understates softness |
| At Risk/Critical tight cluster | Dedicated plays; assumption that **commercial + adoption rescue** precedes uplift success |

**2. Narrative cohesion.** Chronic zero-order footprints line up tightly with misery. Messaging that reinforces **measurable throughput** lands better before you talk **price.**

**3. Revenue concentration vigilance.** A small-dollar Critical tail is tolerable optics; a mid-five-figures **Watch concentration** (**`prog`-style**) is strategically loud even if headline percentage “Watch+Below” looks modest (**~8½% portfolio ARR** in the summarized analysis).

### Where health does NOT suffice alone

Contract value, SKU mix, margin, contractual windows, competitor timing, seasonal buying — none of those live purely inside composite score. Treat health as:

- **A tripwire**, not  
- **A rate card.**

Especially because historical adoption fidelity is imperfect; don’t retrofit perfect fairness stories from Adoption pillar drift.

---

## Triggers headed into V3.3 (human workflow, informs support during pricing)

Soon you’ll automate month-over-month alerts. Skeleton intent your CEO cares about commercially:

| Trigger | Loose threshold | Plain purpose |
|---------|-----------------|---------------|
| Composite cliff | Meaningful single-month drop (analysis suggested ≥10 pts) | Early escalation before churn narrative hardens |
| Band downgrade across five tiers | Any step down | Policy-level escalation — band already encodes executive intent |
| Long open support escalation | Tentative ≥14-day open backlog | High-score whales can bleed quietly otherwise |
| “Stuck Watch” streak | Recommended add-on pending approval | Finds floor-muted chronic weakness |
| ARR tiers on top | e.g., ≥20K Watch+ ⇒ leadership eyeball FAST | Migrates scarce CS attention deliberately |

Operational honesty: retrospective support-fire history is thin before May — thresholds will tighten after live months breathe.

---

## Data humility (still say it once, clearly)

Historical runs anchor **logged behavior and timestamps** honestly; several dimensions **don’t rewind time cleanly** — feature configs, catalog completeness optics, escalation status, roster membership edges. Directions are dependable; microscopic historic precision is not.

Pricing decisions should cite health as **“confirmatory sequencing,”** corroborating account strategy — not courtroom evidence on willingness-to-pay.

---

## Immediate human actions surfaced by the narrative (pricing-adjacent)

**No product launch required.**

1. **`tel`** — don’t await automation; intervene now commercially and technically.  
2. **`prog`** — largest Watch-dollar concentration; reconcile why roster visibility flickered (**MAL gap story**) before layering price change — data truth vs contractual truth.  
3. **Floor policy** — decide whether pinning weak accounts near 40 is strategic kindness or a migration blind spot. If it’s blinding you to risk, annotate internally or rethink how bands are presented.

---

## Suggested sequencing through migration

**Now:** classify commercial waves using **pillars + floors + ARR** more than naive composite thresholds.

**Soon (pre-scale automation):** validate trigger volume so CS isn’t drowned or asleep at the wheel.

**After 2–3 live prospective months:** recalibrate fire-duration thresholds & weight hypothesis tests if you pursue alternate composite emphasis (**do not silently ship weight changes** absent side-by-side live comparison).

---

**Bottom line sentence you can reuse:**  

*The historical panels say our install base skews healthier than scary headlines imply—yet material revenue risk nests in thin tails and artificially muted Watch cohorts—and order drought remains the earliest honest commercial stress signal.*

---

*Compiled from historical backfill + May 2026 production panel narratives; directional, not audited for regulatory pricing fairness.*
