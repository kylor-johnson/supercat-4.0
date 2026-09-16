# Health V3 — Cold Read Audit

**Auditor:** External cold read (no prior context on this project)
**Date:** 2026-05-11
**Files read:** README.md, health_operator_v3.py, HANDOFF_TO_RUN_AGENT.md, runs/2026-05-11/run_metadata.md, runs/2026-05-11/spot_check_10_clients.md, runs/test_2026-05-11/scoring_test_results.md

---

### 1. What this system actually is

Health V3 is a monthly report card for every paying SuperCat client. Once a month it pulls usage data — how often their reps log in, how many features they actually use, whether they're submitting orders and sharing content, whether their data feeds are running on schedule — and turns all of that into a single score from 0 to 100, plus a plain-English label (Thriving, Healthy, Watch, At Risk, Critical). Each of the four underlying components gets its own score and a one-sentence explanation, so a customer success manager can see not just the grade but the specific reason for it.

The practical purpose is a ranked list of clients who need attention. Any account sitting in Watch, At Risk, or Critical — or flagged as a "ghost account" (a client paying meaningful ARR but not logging in at all) — shows up on the radar for proactive outreach or a save campaign. The system doesn't make decisions; it surfaces signals. A CS rep reading the output is expected to look at the score, read the dimension narratives, and decide what conversation to have. The whole thing runs monthly, writes a CSV, and is meant to be the factual foundation for that conversation — not a replacement for it.

---

### 2. Honest complexity assessment

**Is the system appropriately complex?**

Yes, with one exception. The scoring logic itself — four dimensions, band lookup tables, straight averages — is clean and appropriately simple for a V1. The spec is well-written and the code faithfully implements it. The exception is the operational running process: to actually run this monthly you have to manually extract 10 SQL queries from Python function bodies and execute them through two separate database tools before the scoring operator can touch anything. That step is documented but barely. "Copy each query verbatim from the corresponding loader function" is technically accurate, but a cold runner staring at 909 lines of Python will spend more time finding the right lines than running them. The separation between "where queries live" (Python functions) and "how to run them" (handoff doc) creates unnecessary friction every month.

**Most complex part — is it justified?**

The data freshness scoring in Operational Health. It measures how late each data feed is relative to *that org's own historical cadence* rather than against a universal clock, handles minimum-history requirements, includes an initial-load carve-out, and applies a floor to prevent degenerate ratios. The complexity is justified in concept — a daily feed that's 3 days late is more alarming than a weekly feed that's 3 days late, and a naive universal-clock approach would produce misleading scores. But the initial-load carve-out has a known floating-point bug that means it almost never fires. The complexity was added to solve a real problem and then partially failed at it.

**Simplest part — could it be simplified further?**

The composite math (straight average of four dimensions) is the simplest part and should stay that way. Do not add complexity to the averaging step without correlation data.

**Tribal knowledge required to run monthly**

High. A cold runner needs to know: (1) the MAL file lives in `Health V2/inputs/` and must be manually kept current — the operator doesn't fetch it; (2) the Python environment is in a *different* project folder (`Health V2/.venv`); (3) the `--pg-cache-dir` flag controls both Postgres and BigQuery caches despite the name; (4) the 10 SQL queries for cache population must be extracted from the Python loader functions by hand, not from any standalone query file; (5) what a "correct" cache CSV looks like so you know if the MCP returned garbage. None of these are in one place.

**Is the handoff doc sufficient for a cold runner?**

Close but not sufficient. It is well-intentioned and covers the broad steps clearly. Where it falls short: it tells you *what* to do in Step 4a (populate the cache) but not *how* precisely enough. A cold runner who has never touched an MCP tool will not know how to "run a query and write results to CSV" without several rounds of trial and error. The doc also doesn't specify what column names the cache files must have, leaving the runner to infer from the Python loader code. The single-org debug command is a good safety valve; the expected output listed for `tam` is the best piece of operational documentation in the file.

---

### 3. The weighting question

**Does 25/25/25/25 make sense for identifying at-risk accounts?**

No. The spot check makes this concrete. The four accounts Kylor identified as Red — mfc, st, hmjc, hh — all land in Watch (49.6–53.3), not At Risk. They share a pattern: Engagement and Value Delivery are correctly cold (0–55), but Adoption (60–80) and Operational Health (47–92) are warm enough to pull the average above 40. The reason is structural: a dormant account with a clean catalog and configured features scores reasonably on Adoption and Operational Health even when nobody is using the product. st has a 91.7 on Operational Health while running zero orders and seven logins from one person. That 91.7 is technically correct — the data infrastructure *is* clean — but averaging it equally with a 0 on Value Delivery produces a Watch score for what is functionally an abandoned account.

For a save-campaign use case, the central question is "is this account at risk of churning?" Engagement (are they logging in?) and Value Delivery (are they getting business outcomes from the platform?) are behavioral signals directly tied to that question. Adoption (are they using all their features?) is a secondary signal — an account that uses more features has more reason to stay, but an account that uses zero features while scoring high on Adoption because features are "configured" is not healthy. Operational Health (are the data feeds clean?) is a hygiene indicator — it predicts whether the account will have problems eventually, not whether they're leaving now.

**Proposed weights from scratch for the save-campaign use case:**

- Engagement: 35%
- Value Delivery: 30%
- Adoption: 20%
- Operational Health: 15%

Rationale: Engagement is the most direct leading indicator of churn. If reps aren't logging in, no other dimension can compensate. Value Delivery is the next most predictive — it measures whether the platform is generating observable business outcomes, which is what keeps clients renewing. Adoption matters because breadth of use increases switching cost, but it deserves less weight because the point system gives partial credit for configured-but-unused features. Operational Health deserves the least weight for churn prediction — a broken data feed is a problem, but it is a lagging indicator and can be fixed quickly; a rep base that stopped logging in 90 days ago is harder to recover.

**Risk of changing weights before correlation data exists:**

Real, but asymmetric. If you reweight incorrectly and generate false alarms, CS reps spend time on accounts that are actually fine. If you keep the current weights and keep missing Reds, save campaigns launch late and ARR is lost. The current error mode (missing at-risk accounts) is more expensive than the proposed error mode (chasing borderline-healthy accounts). That said, arbitrary reweighting without any evidence is worse than both — but the spot check *is* evidence, just qualitative. It consistently shows Operational Health inflating scores for dormant accounts. That's sufficient reason to act.

**The middle path:**

Add a behavioral floor override before touching weights at all. If Engagement < 40 AND Value Delivery < 40, cap the composite at 40 (the top of the Watch range, so the account cannot be classified as Healthy or Thriving). This is additive — it doesn't change any dimension score, doesn't require reweighting, and can be removed or adjusted later. The four Reds from the spot check (mfc, st, hmjc, hh) all have Engagement ≤ 53 and Value Delivery ≤ 33. A floor at 40 on the composite for accounts that are cold on *both* behavioral dimensions would move them into At Risk or Watch-bottom, which matches Kylor's intuition, without waiting for 6 months of correlation data and without committing to a permanent weight change. It is also explainable to a CS rep in one sentence: "If an account's users aren't showing up and the platform isn't producing outcomes, it can't be classified as Healthy regardless of how clean the catalog is."

---

### 4. The three things I would do next

---

**1. Add the behavioral floor override**

*What it is:* A composite cap that triggers when both Engagement < 40 AND Value Delivery < 40. When it fires, the composite score is capped at 40 and the health band cannot exceed Watch. The four dimension scores are still shown unchanged so CSMs can see why. The cap is surfaced in the output with a plain-English note ("behavioral floor applied — engagement and value delivery both below threshold").

*Why highest leverage:* It directly fixes the primary problem the system has right now: accounts that are functionally dormant are landing one band too high and missing the save-campaign trigger. This is not a design change; it is the same pattern as the existing ghost-account override (§5.1 in the spec), which already caps dormant high-ARR accounts at Critical. The behavioral floor is that override generalized to catch the accounts that are nearly-ghost but not quite: logging in rarely, producing nothing, but maintaining clean infrastructure. mfc, st, hmjc, and hh would all be caught by this. The fix is reversible, explainable, and consistent with the spec's existing design patterns.

*What done looks like:* The README has a §5.2 defining the override with the same structure as §5.1. The operator implements it in ~5 lines after the composite calculation. A rerun confirms the four Reds land at or below 40. The run_metadata.md reports a `behavioral_floor_applied` count alongside `ghost_account`.

*Rough effort:* 2–3 hours.

---

**2. Fix the eCat Online Catalog gate in Adoption to require actual usage, not just configuration**

*What it is:* Right now, a client scores an Adoption point for eCat Online Catalog if `enable_online_catalog = true` on their mobile site — regardless of whether anyone has ever visited the catalog. This is the only Adoption feature with a flag-only gate; every other gated feature (Online Ordering, Sales Portal) requires `portal_orders_90d > 0`. Changing eCat Online Catalog to require `portal_orders_90d > 0` makes the dimension internally consistent and removes the free credit currently given to dormant accounts with catalog enabled.

*Why highest leverage:* This is the single easiest spec fix with a direct and measurable impact on the Reds. mfc (zero portal traffic, 0 iPad orders) is currently scoring 80 on Adoption partly because of this free point. st and hmjc both score 60 on Adoption for the same reason. Without the flag-only credit, mfc drops from 80 to 75 (still overestimates, but closer), and st drops from 60 to 40 — which, combined with a 0 on Value Delivery, starts looking like an At Risk reading. The fix is one line in the spec and one line in the operator. It also eliminates a logical inconsistency that will confuse any CS rep who notices that "using" eCat means something different from "using" Online Ordering when they're both the same underlying portal.

*What done looks like:* README §2 updates the Adoption feature matrix's eCat row: gate remains `enable_online_catalog = true`, but usage signal becomes `portal_orders_90d > 0` (same signal as Online Ordering and Sales Portal). One line of code changes in `score_adoption`. Rerun confirms mfc Adoption drops from 80. Narrative examples in §2 are updated to remove the "(flag-only gate)" notation.

*Rough effort:* 2 hours.

---

**3. Start tracking labeled outcomes now, before the next run**

*What it is:* The §9 validation plan — the formal test of whether weights should ever change — requires labeled outcomes: which accounts churned, which renewed, which expanded, which were saved. Without labels, that test can never run. There is no database for this, no pipeline, and as far as the project files show, no one owns the task of recording them. The fix is not technical: it is a maintained spreadsheet (or equivalent) with columns for org, outcome date, and outcome type (churned / renewed / expanded / saved), updated after each renewal cycle or churn event.

*Why highest leverage:* The system is now on its first monthly snapshot. If labeled outcomes start accumulating now, the §9 correlation test becomes runnable in 3–4 months. If this doesn't start now, the weights conversation gets deferred indefinitely and the system runs on 25/25/25/25 forever — or weights get changed without any evidence. The labeled-outcome tracker is also the mechanism by which the save campaigns the system is designed to support get measured: did the outreach work? Without labels, Health V3 is a dashboard with no feedback loop. Everything downstream — V3.1 triggers, V3.2 churn patterns, V3.3 save plays — requires this data.

*What done looks like:* A simple file (CSV or spreadsheet) exists at a known location in the project folder. It has a defined schema. Someone owns the responsibility of updating it when a client churns, renews, or is formally saved. The §9 validation plan in the README is updated with a pointer to where this file lives.

*Rough effort:* 2 hours to create the file and document the process. Ongoing: 15 minutes per churn/renewal event.

---

### One more thing

The `denominator_quality` flag currently only detects the case where more users are logging in than there are enabled accounts (ratio > 100%). The spot check surfaced the opposite problem: the `enabled_users` count for Full-bundle orgs (gh with 7,911, kll with 933, fsf with 718) is inflated by customer-portal accounts provisioned in `org_users`. This produces artificially low Engagement scores for active accounts — gh, which has 6,246 logins and 814 sharing events, is scored at 66.7 on Engagement because its ratio is 0.71% against a denominator that includes thousands of B2B customer accounts. The model isn't identifying these accounts as at-risk; it is misrepresenting their engagement to CSMs. This belongs on the V3.1 list as a flag improvement — specifically, detecting when `enabled_users` far exceeds what's plausible for an account's size and surfacing a `denominator_quality = inflated` note in the output.
