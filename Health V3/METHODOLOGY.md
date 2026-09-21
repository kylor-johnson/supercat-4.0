# Client Health Score — Methodology Overview

**Version:** 3.4.1 | **Last Updated:** 2026-09-21

> This document is the executive-facing explainer. It describes *what* the score measures and *why* it is built this way. The operational spec — exact thresholds, SQL, field names, score formulas — lives in `README.md`. Anywhere this document would otherwise pin a specific number, it points at the README. That keeps a single source of truth for current operating values and prevents the two docs from drifting.

---

## Executive Summary

### The Problem We Were Solving

SuperCat's previous client health model (V2) had grown difficult to trust and difficult to explain. It incorporated risk modifiers, growth signals, and weighted inputs that were not grounded in data — they were gut-feel coefficients that accumulated over time. The result was a score that was hard to interpret ("why did this client drop 12 points?"), hard to defend in a client conversation, and structurally conflated two separate questions: *is this client healthy today?* and *is this client growing?*

CS was left either ignoring the score or reverse-engineering it. Neither is what a health score is for.

### What We Set Out to Build

The goal of V3 was to start over with a simpler, more honest model built around one question: **is this client actually using and benefiting from SuperCat right now?**

Four things had to be true about the new model:
1. **Explainable in one sentence per dimension.** A CS rep reading the output should know exactly why a score is what it is and what to do about it — without a decoder ring.
2. **No growth signals.** Expansion and upsell are a separate conversation. Health is about the current state of the relationship, not the opportunity.
3. **No invented weights.** Weighting dimensions against each other implies we know which dimensions best predict churn. We don't — not yet. Equal weights are honest; gut-feel weights create false precision.
4. **Grounded in real data before shipping.** Before finalizing thresholds, we ran empirical research across the full 104-org portfolio to see what the actual distributions looked like. Every key threshold in the model was validated against or derived from that research.

### What We Built

V3 is a composite score (0–100) built from four equal dimensions — Engagement, Adoption, Value Delivery, and Operational Health — each contributing 25%. The score runs monthly, covers every active paying client, and produces a health band (Thriving / Healthy / Watch / At Risk / Critical) alongside a plain-English narrative for each dimension.

Two safety overrides cap the composite downward when behavior tells a story the averages alone would miss: a Ghost Account override (high-ARR clients with zero logins) and a Behavioral Floor (clients who are barely showing up and generating no observable outcomes).

Thresholds for each signal were set by looking at the actual portfolio distribution — not by estimating what "should" be normal. Key design choices like equal dimension weights and unweighted point systems for Adoption and Value Delivery were made deliberately, with a documented plan to revisit them once real churn outcome data is available.

### Where We Are Now

V3.2 has completed its first full run across all 104 active clients (May 2026). The run reflects every calibration change since the V3.0 ship:

- Velocity-based engagement replaced a recency signal that had zero discriminating power across this portfolio.
- The freshness sub-signal is frequency-weighted, so a daily inventory feed drives more weight than a quarterly product reload.
- Engagement-denominator handling was corrected for large-bundle orgs whose user counts are inflated by B2B portal accounts.
- Three import types with systematic parser errors are excluded from the import-health ratio (but remain in freshness).
- A Behavioral Floor override now caps the composite at Watch for accounts whose users are not meaningfully showing up *and* whose platform activity is not producing observable outcomes.
- The operator is deterministic in cache mode — the same cache and the same score date always produce byte-identical output, regardless of when the run executes. A client's score reflects their state on the score date, not the moment the operator happened to run.

The output is a monthly CSV that CS can use immediately to prioritize outreach. Beyond the dimension scores, each row now carries an executive-summary `composite_narrative` that explains the score in 2–4 sentences for non-technical readers. The roadmap from here — trigger alerts for score drops, churn-pattern recognition, and save-play playbooks — is staged in the spec and depends on accumulating monthly history and labeled outcomes before each next step can run responsibly.

---

## 1. What This Is

The Client Health Score is a monthly signal that tells us how each client is actually using and benefiting from SuperCat — expressed as a single number between 0 and 100. It exists because we need a consistent, objective way to know which accounts need attention before they churn, which ones are thriving, and how to prioritize CS time across a large portfolio. The score runs once per month, covers every active client, and produces both a summary number and a plain-English explanation of what's driving it. New accounts in their first 90 days are excluded — during onboarding, a different metric (Time to First Value) is more appropriate than a health score.

---

## 2. How the Score Is Built

The composite score is a simple average of four equal dimensions: **Engagement**, **Adoption**, **Value Delivery**, and **Operational Health**. Each dimension scores 0–100 and contributes exactly 25% to the composite. No dimension outweighs another at this stage — that weighting decision is intentionally deferred until we have enough outcome data (retention, ARR change) to know which dimensions actually predict churn for each product tier.

A score of 80 or above means things look good across the board. A score below 40 is a signal to act. Each account also carries two possible safety overrides — Ghost Account and Behavioral Floor — that can cap the composite downward when behavior tells a story the averages alone might miss.

---

## 3. How Each Dimension Is Scored

### Engagement — Are users actually showing up?

Engagement measures login activity across three lenses, then averages them equally:

- **Login volume** — raw logins across the trailing quarter, banded against the actual portfolio distribution.
- **Active user ratio** — what share of enabled users logged in at least once in the trailing quarter. For large-bundle orgs whose enabled-user counts are inflated by B2B portal accounts, the denominator switches to the count of users who actually logged in across the trailing year.
- **Login velocity** — whether the pace of logins is holding steady, accelerating, or fading compared to the prior six months. A client can log in frequently and still score poorly on velocity if usage was high early on and has dropped off. This is intentional — it catches the "great launch, slow fade" pattern that raw login counts miss.

Exact band scores and thresholds: see `README.md` §1.

---

### Adoption — Are they using what they have?

Adoption measures feature breadth. Each feature the client is configured to use counts as one point. Using it = 1 point; not using it = 0. The score is the share of applicable features actually being used. No feature is worth more than another — Adoption is intentionally an unweighted point system.

A feature only counts if it is actively turned on in the client's configuration. No client is penalized for not using something that was never set up for them. The features evaluated span the iPad app itself, smart stacks, sharing / quoting, the eCat online catalog, online ordering, the Sales Portal, inventory management, and sales-data feeds. Every client has at least three applicable features (iPad, Smart Stacks, Sharing); most have more depending on their subscription tier.

Exact applicability gates and usage signals: see `README.md` §2.

---

### Value Delivery — Are they getting real outcomes?

Value Delivery applies the same point-per-channel logic as Adoption, but focuses on whether the platform is producing observable business results — not just whether features are turned on and touched. Channels evaluated include iPad order volume, sharing / quoting activity, online catalog engagement, portal ordering, Sales Portal engagement, and inventory data flow.

Thresholds are intentionally low for V1. The question being answered is "is this channel producing anything?" — not "is it producing enough?" Volume calibration is deferred to a later iteration so that orgs with real but modest activity are not flagged falsely in the first run.

A deliberate design choice: Adoption and Value Delivery are unweighted point systems. An org doing 200 presentations and an org submitting 2,000 portal orders are both delivering value through their primary channel. Neither is privileged over the other in V1, because weighting channels against each other would require evidence we don't yet have.

Exact qualifying signals and per-channel thresholds: see `README.md` §3.

---

### Operational Health — Is the data infrastructure in good shape?

Operational Health has three sub-signals, averaged equally.

**1. Catalog Completeness** — what share of active products have a name, an image, and a price (or the equivalent under contract or price-level pricing). A well-maintained catalog is the foundation of every other outcome. Completeness is mapped to a band score, not used raw, so a 75%-complete catalog and a 60%-complete catalog land in the same band — both are "usable in the field with coaching room."

**2. Import Health** — for every data feed the client actively runs, did the most recent run succeed? The score is the share of active feed types with a clean last run. Imports with only warnings (not errors) count as successful for V1.

**3. Data Freshness** — is each data feed running on its own normal cadence? Freshness is measured relative to each client's historical rhythm, not a universal clock. A daily inventory feed that hasn't run in three days is in worse shape than a quarterly product re-load that's two weeks behind. The per-feed staleness scores are averaged with each feed weighted by its run frequency, so a stalled daily feed dominates a quiet quarterly one.

Exact band scores, freshness math, and the excluded-import-types list: see `README.md` §4.

---

## 4. Health Bands

| Band | Score Range | What It Means for CS |
|------|-------------|----------------------|
| Thriving | 80–100 | Account is in good shape. No action required; periodic check-in sufficient. |
| Healthy | 60–79 | Strong across most dimensions with identifiable room to grow. Coaching opportunity, not a rescue. |
| Watch | 40–59 | Meaningful gaps in engagement or outcomes. Proactive outreach warranted within the current month. |
| At Risk | 20–39 | Significant problems across multiple dimensions. Prioritize for active save play. |
| Critical | 0–19 | Severe disengagement or zero usage. Urgent intervention; escalate to executive if high ARR. |

---

## 5. Override Rules

Two overrides can cap the composite score downward. They exist because averages can sometimes produce misleading results when behavior tells a more urgent story.

### Ghost Account Override

**What it catches:** A client paying meaningful ARR who has had zero logins in the trailing quarter. A high-ARR account with nobody opening the app is broken regardless of catalog completeness or import health. Operational signals can light up green on infrastructure that nobody is actively using — the override prevents that from producing a misleading composite.

**What it does:** Caps the composite score in the Critical band. All four dimension scores still compute and are shown — CSMs need to see why the account isn't using each surface.

Lower-ARR dormant accounts are not overridden; they may genuinely be on pause or in a different lifecycle stage where this urgency does not apply.

### Behavioral Floor Override

**What it catches:** An account whose users are not meaningfully showing up *and* whose platform activity is producing no observable business outcomes. These are the near-ghost accounts that don't quite trip the ghost threshold (some logins do exist) but are functionally dormant.

**What it does:** Caps the composite score at the top of the Watch band. All four dimension scores are still shown in full so CSMs can see why the floor fired.

The principle: Operational Health and Adoption can score well on a catalog and configuration that nobody is actively using. Allowing those scores to carry the composite to Healthy or Thriving would produce a misleading picture.

When either override applies, the output labels it explicitly and the composite narrative explains why the composite differs from the average of the dimensions.

Exact ARR and dimension-score thresholds for both overrides: see `README.md` §5.1 and §5.2.

---

## 6. Key Design Decisions

- **Equal weights, on purpose.** All four dimensions contribute 25% each. We do not have enough outcome data yet (churned accounts, ARR changes) to know empirically which dimensions best predict retention for each product tier. Weighting by gut feel would be worse than not weighting at all. The plan is to run a formal correlation analysis once we have 3+ months of scores and 30+ labeled outcomes — and only introduce weights if the data clearly supports it.

- **No trajectory scoring.** Month-over-month trend is not a scored dimension. Trend direction is much more useful as context — surfaced in narrative, visible to the CSM — than as a mathematical input to the score. Scoring trend would require a longer baseline than we currently have, and would add complexity without clear explanatory value.

- **Seasonality is flagged, not suppressed.** If a measurement window falls during a known slow cycle for an industry (furniture, lighting, etc.), that context is noted alongside the score. The score itself is not adjusted. We don't yet have 12-month per-account baselines to normalize against, and adjusting scores algorithmically without that baseline would introduce noise, not signal.

- **Adoption and Value Delivery are unweighted point systems.** Every applicable feature or channel counts equally. An org with 200 presentations and an org with 2,000 portal orders are both delivering value through their primary channel. Neither outcome is privileged over the other in V1.

---

## 7. How the Key Thresholds Were Set

Thresholds in V3 were not pulled from benchmarks or estimated in advance. They were anchored to the actual SuperCat portfolio distribution at the time of the May 2026 calibration. The exact numbers used by the operator today are documented in `README.md` §1–4; the principles below explain *how* those numbers were chosen.

### Login Volume

The login-count bands were placed at natural breaks in the trailing-90-day login distribution across all 104 active clients. Lower-band boundaries sit near the bottom quartile of the portfolio so that quietly-active accounts land in the developing tier rather than at zero. The ceiling sits near the top decile so that the most active orgs are not artificially compressed against the rest of the distribution. The intent is that the bands describe where this client base actually clusters and where behavior meaningfully changes between groups, not where a textbook says "high engagement" lives.

### iPad Order Volume

The threshold separates accounts where one rep tested the feature from accounts where the iPad is part of a recurring workflow. A natural shoulder in the order-count histogram falls in the low double-digits, which became the operating boundary. An earlier draft used a much higher cutoff carried over from V2; that was rejected after the empirical pass because it would have penalized roughly a fifth of the portfolio with real but modest order activity.

### Sharing / Quoting Activity

The current threshold is intentionally conservative — set low enough to avoid false negatives in the first run, knowing that the real "workflow-level" pattern sits substantially higher. Tightening this is a planned V3.2 refinement once we have enough run history to do it safely.

### Health Bands

The band boundaries (Thriving / Healthy / Watch / At Risk / Critical) are judgment calls anchored to CS workflow actions, not derived from a statistical model. The boundaries are round numbers — the underlying scoring mechanics (step-ladders, point ratios) do not produce enough precision to justify non-round boundaries, and a threshold of 63 vs. 60 would imply a level of measurement precision the signals don't actually have.

The 40-point boundary is the most operationally grounded: the Behavioral Floor override exists specifically to prevent a client from landing above Watch when engagement and value delivery are both below their respective thresholds. That override was calibrated by manually reviewing client profiles during the first run.

### Validation Plan

The plan is to validate these thresholds retrospectively against churn outcomes once 3+ months of score history and 30+ labeled outcomes are available. If clients who churned were consistently in the Watch band 60+ days before leaving, the thresholds are well-placed; if they were landing in the Healthy band, the boundaries need to shift down. That analysis cannot run until sufficient outcome data accumulates — the subscription history table in the database was bulk-backfilled in mid-2025 and is not reliable as a churn source. Labeled outcomes are tracked in `outcomes.csv`, which is empty at V3.2 launch and must be populated as accounts churn, renew, or are saved.

---

## 8. What This Is Not

**Seasonality is acknowledged, not modeled.** The system flags when a score might reflect a known industry slow period, but it does not adjust scores accordingly. Without a full year of per-account history, any seasonal adjustment would be a guess. This is a known limitation until 12-month baselines are available.

**Dimension weights are not correlated to business outcomes yet.** The 25/25/25/25 weighting is an intentional starting point, not a validated model. A formal correlation study against retention and ARR outcomes will determine whether weighting is warranted — and if so, which dimensions carry the most predictive weight for which product tiers. That study cannot run until sufficient outcome data accumulates.

**Growth scoring is out of scope.** Expansion, upsell, and growth signals are a separate concern and are not included in the health score. The health score measures the health of what a client currently has — not the opportunity or likelihood of them buying more.

**Narrative action recommendations are heuristic.** Each composite narrative carries an action sentence calibrated to the org's health band. These are starting suggestions for CS, not policy. The full save-play runbook is a V3.3 deliverable; until then, treat the narrative as context for a CS judgment call rather than a directive.

### Known Model Behavior Limitations

The following limitations were identified during the May 2026 manual spot check and are targeted for V3.2+. They do not represent bugs in the current scoring math — all scores are arithmetically correct per the spec. They represent cases where a correct score can still produce a misleading CS picture, and are documented so the next iteration can address them deliberately.

- **Thriving accounts with majority import feeds broken.** Operational health contributes only 25% of the composite, so an account that is strong on engagement, adoption, and value delivery can land in Thriving even when most of its import feeds are erroring. A CSM seeing a Thriving label may reasonably deprioritize what is actually an infrastructure fire. Until V3.2 introduces a composite-level guard, the composite narrative is responsible for surfacing this.
- **Import health passes despite universal staleness.** The import-health sub-signal checks whether the last run errored, not whether it ran recently. A feed that simply stopped running (without erroring) still scores healthy. Feeds with very low recent run counts are also excluded from freshness scoring entirely, making them invisible to the model.
- **Denominator inflation for some bundle tiers.** The active-user denominator switch (replacing the raw enabled-user count with annual active users) currently covers Full and iPad+Catalog+Cart bundles. iPad+Catalog+Portal orgs with large B2B buyer bases are not covered, and their active-user ratios may be artificially low.
- **Burst-weighted freshness lag after a feed is retired.** If an org ran a large one-time migration through a particular import type and then permanently retired that type, the burst run-count anchors the freshness weighted average for the full 180-day window even when all other active feeds are healthy.
- **Sharing-activity threshold is conservative.** The current threshold catches "any meaningful activity" rather than "established workflow-level use." A planned refinement raises it once portfolio history justifies the move.

Specific example accounts and proposed fixes for each item were captured during the May 2026 calibration audit and are the next iteration's backlog. They are not promises.
