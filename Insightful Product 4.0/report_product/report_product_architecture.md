# Report Product Architecture — Insightful 4.0

> **Status**: Active (merge build, 2026-06-29)
> **What this is**: The org-level intelligence **report product** — the signal-first delivery shell
> that turns the 4.0 provenance stack into a document a CEO/VP of Sales reads in five minutes and says
> *"holy shit, I didn't know that about my business."*
> **Lineage**: This is the **Insightful Product 3.0 report architecture** (`Insightful Product 3.0/authority/report_architecture.md`)
> **re-anchored onto the 4.0 provenance foundation**. 3.0 gave us the dope *product* (signal-first ordering,
> the 26-signal catalog, narrative-arc editorial voice, account mini-briefs, the HTML shell). 4.0 gives us the
> *truth* (invoiced-net axiom, `COMMERCE_CONFIDENCE`, `FEED_COMPLETENESS`, tier-aware leakage, rep-identity tiers,
> hard-gap suppression). This file fuses them.
> **Companions**: [`signal_catalog_v4.md`](signal_catalog_v4.md) (the re-anchored signals) ·
> [`report_editorial_rules_v4.md`](report_editorial_rules_v4.md) (voice + dollar-tag rules) ·
> [`provenance_spine.md`](../foundation/provenance_spine.md) (Tier-0 truth) · [`query_library_v2.md`](../foundation/query_library_v2.md) (SQL).
> **Governed by**: [`CANON.md`](../CANON.md) — the precedence order and the reading contract (load
> `provenance_spine` + client `profile.md` + [`industry_context.md`](../knowledge/industry_context.md) +
> [`communication_guideline.md`](../knowledge/communication_guideline.md) **before any query runs**) that this
> architecture honors.

---

## 0. The merge in one paragraph

3.0 built a genuinely great report and then printed **booked / eCat GMV** as if it were the client's business —
the exact number 4.0 proved is off **4×–9×** (`portal_orders.total_amount`). 4.0 fixed the truth but never
rebuilt the report; it lives as a query library, operators, and CEO prompts. **This architecture keeps 100% of
3.0's delivery craft and swaps the data underneath onto the provenance layer.** Every signal still fires on
surprise × dollar × actionability — but the dollar is now **invoiced net**, gated by `Q-ECON-00`, capped at
`COMMERCE_CONFIDENCE`, stamped with `FEED_COMPLETENESS`, and **suppressed rather than approximated** when the feed
can't carry it. The result is the report that makes clients say *"I didn't know that"* **and** survives a CFO's
scrutiny.

---

## 1. Core philosophy (kept from 3.0, unchanged)

**The report should make the client say: "Holy shit — I didn't know that about my business. I need to keep paying
for this."**

Intelligence-first, not domain-ordered, not an alarm board:
- Lead with what's **working**, then surface intelligence they can't get elsewhere, then opportunities, then risk.
- Every insight is **item-level specific**: named customer/rep/SKU, a dollar, and a clear action.
- Sections render if they have a fired signal **or** their data gate passes.

**The three tests (3.0, retained):**
1. If a finding could appear on a generic industry dashboard, it doesn't belong here.
2. If the report makes the client feel bad about their business, the framing is wrong.
3. If a reader of only the Signal Summary concludes "we should churn," the tone balance failed — rewrite.

**The 4.0 fourth test (new, non-negotiable):**
4. **If a reader could mistake a capped/partial/booked number for a hard invoiced fact, the labeling failed —
   suppress or re-tag.** Intellectual honesty about confidence is now a first-class design constraint, ranked
   *above* the insight itself (per `CEO_brief_sarreid_PROMPT.md` and the Spine).

---

## 2. What changed vs. 3.0 (the re-anchor, at a glance)

| Dimension | 3.0 (as built) | 4.0 (this product) |
|---|---|---|
| Topline / "total business" | `SUM(portal_orders.total_amount)` (booked) | **`SUM(portal_invoices.net_amount)`** (invoiced), **`Q-ECON-00`-selected**, clamped window |
| Truth labels on dollars | `[HYPOTHETICAL]` / `[ESTIMATED]` / `[eCat ONLY]` | **three tags**: `[source]` · `[confidence tier]` · `[completeness]` (see editorial rules) |
| Highest confidence | `FULL` intelligence tier | **`FULL` retired for economics** — STRONG ceiling on a single invoice feed |
| Data adequacy gate | `DATA_MASS_TIER` (volume only) | `DATA_MASS_TIER` **× `FEED_COMPLETENESS`/`COMMERCE_CONFIDENCE`** — capacity *and* truth (§4) |
| Capture rate | computed freely | **capture ≠ attribution**: a *rate* only when `CORROBORATED` + ≥STRONG, else absolute eCat $ only, labeled LIMITED |
| Price leakage | not present | **new**: tier-aware same-SKU dispersion (`Q-ECON-LEAK`/C2/K7), house-account auto-flag, directional + gut-check |
| Rep naming | named freely | **rep-identity tier gate** (§7.1): Tier 2 named; Tier 1 `rep_number` only; Tier 0 behavior-only |
| Returns / margin / AR | estimated where convenient | **suppressed** (gross-only orgs, no COGS, no dealer AR) — surfaced as "with connected data," never faked |
| Segmentation | segment labels existed internally | **🧊 FROZEN** everywhere (Spine §8) |
| Peer benchmarking | excluded in shared_rules §E | **still excluded** (peer data unreliable) — deferred |

**Net-new dope from 4.0 that 3.0 never had:** price-leakage dollars, rep-attributed revenue-at-risk (S1),
the confidence/completeness stamp that lets you ship a number you can defend, and the "what we deliberately
won't fake" trust-builder.

---

## 3. Report modes (kept from 3.0, gate re-anchored)

| Mode | 3.0 gate | 4.0 gate (re-anchored) |
|---|---|---|
| **1 — Standard** | LTM commerce > 0 (any channel) | `Q-ECON-00` returns a usable feed (invoiced **or** booked fallback) with `COMMERCE_CONFIDENCE ≥ LIMITED` |
| **2 — Activation** | Zero commerce ever | No ERP feed at all → behavior-only (Rep layer, ERP-optional); **no dollar outcomes**, "what becomes possible" |
| **3 — Reactivation** | Had commerce, now lapsed | Feed exists but `FEED_COMPLETENESS = STALE`/lapsed → historical (peak invoiced) + re-engagement, recovery playbook |

Mode 2 changes most: 3.0 ran Activation when eCat orders = 0; **4.0 runs it only when there is no commercial
truth to report at all** (no invoices and no keyed orders). An org with zero eCat but a live invoice feed is a
**Standard** report about total business with eCat capture shown as a channel — not an Activation report.

---

## 4. The adequacy gate — `DATA_MASS_TIER` × truth (the key reconciliation)

3.0 asked *"is there enough data to be surprising?"* (volume). 4.0 asks *"can the data carry a number we'd
defend?"* (truth). **Both must pass. The report's overall intelligence tier is the *lower* of the two** —
"lowest input wins" (Spine §5.3).

### 4a. Capacity axis — `DATA_MASS_TIER` (kept from 3.0)
Points for eCat order volume, active accounts, active reps, `HAS_PORTAL_ORDERS`, Mixpanel present, inventory,
GMV, months of history → `FULL`(14+) / `STRONG`(10–13) / `MODERATE`(6–9) / `EARLY`(3–5) / `MINIMAL`(0–2).
*(Computation table unchanged from `Insightful Product 3.0/authority/report_architecture.md`.)*

### 4b. Truth axis — `COMMERCE_CONFIDENCE` + `FEED_COMPLETENESS` (from 4.0)
Run `Q-ECON-00` first. It emits `COMMERCE_CONFIDENCE` (STRONG/PARTIAL/LIMITED/NONE — **never FULL**) and the
clamped `report_through_date`, and `FEED_COMPLETENESS` (CORROBORATED / UNVERIFIED-SINGLE-FEED /
PROVABLY-INCOMPLETE / STALE / DEAD).

### 4c. The combined tier (new)
```
REPORT_INTELLIGENCE_TIER = LEAST( DATA_MASS_TIER , confidence_to_tier(COMMERCE_CONFIDENCE) )
where FULL is unreachable for any economics-bearing report (collapses to STRONG).
```
- **High mass, low truth** (e.g. tons of eCat orders but `PROVABLY-INCOMPLETE` invoices — the `sc` case where
  eCat $43.1M > 1.05× invoiced $34.2M): the report still renders, but **economics toplines are suppressed**
  and it leans on behavior/eCat-capture (clearly labeled), not "total business."
- **Low mass, high truth** (clean invoice feed, few accounts): a credible but thin **EARLY/MODERATE** report —
  the 3.0 thin-data handling (header disclosure + per-section "with more data") applies verbatim.
- **`NONE`** on the truth axis → **Activation mode** (behavior-only), regardless of volume.

The thin-data header disclosure, the per-section "with more data" sentence, and the "never apologize" rule are
**carried over from 3.0 unchanged** — they're the right pattern; 4.0 just adds the truth dimension to *when* they fire.

---

## 5. Section architecture — fixed positions (kept from 3.0)

Deterministic order; no fluid ordering.

| Position | Section | § | 4.0 binding added |
|---|---|---|---|
| 1 (always) | **Signal Summary** | §1 | built last; top 5–7 by `SIGNAL_RANK`; every dollar three-tagged; min 3 positive; finding #1 positive |
| 2 | **Team Intelligence** | §5 | rep naming gated to **Tier 2**; Tier 1 → `rep_number`; Tier 0 → behavior-only, no rep→revenue |
| 3 | **Account Intelligence** | §2 | per-customer mini-briefs at **billing-entity grain**; toplines invoiced + completeness-stamped |
| 4 | **Commerce Patterns** | §4 | capture shown as **capture, not attribution** (LIMITED unless CORROBORATED); **leakage** lives here, directional |
| 5 | **Product Intelligence** | §3 | ghost-SKU / stockout / velocity unchanged (eCat/inventory-grain, labeled); no margin (no COGS) |
| 6 | **Platform Context** | §6 | operational health / staleness; collapsed unless P0/P1 |
| last | **Appendix** | — | data sources, methodology, **the three-tag legend**, and the **"what we won't fake" list** |

**Render gate (3.0, retained):** a section renders if ≥1 fired P0/P1 signal **or** its alternate gate passes
**or** it has a query-driven subsection passing the specificity test. Suppressed only if all fail.

---

## 5a. Rendered client-facing structure — the gold-standard layout *(pinned 2026-06-30)*

> **What this is.** §5 above defines the **six source-data sections** the operator gathers around (Signal Summary,
> Team, Account, Commerce, Product, Platform). **§5a defines the 13-section CEO-facing render those source sections
> assemble into** — the layout the Sarreid CEO Brief settled in the 2026-06-30 gold-stamp audit and that every
> subsequent client run must reproduce.
>
> **Layout authority:** [`../outputs/Sarreid_CEO_intelligence_report_2026-06-29.html`](../outputs/Sarreid_CEO_intelligence_report_2026-06-29.html)
> is the canonical reference. CSS, fonts, JS (sticky TOC, `<details>` collapsibles, semantic color tokens) are
> settled — port verbatim, do not redesign. See the gold-stamp handoff (`build_notes/sarreid_gold_stamp_handoff_2026-06-30.md`)
> §1 / §4 / §9 for the don't-touch list.

### 5a.1 — Canonical section sequence (13 positions; preserve order)

| Pos | Section | Collapsible | Color bar | Pulls from §5 source sections |
|---|---|---|---|---|
| 0 | Header — client name, "Selling & Commerce Intelligence — CEO Brief," period framing (`Trailing 12 months through {date} · vs the prior matching 12 months`) | n/a | — | preflight outputs |
| 0a | Sticky TOC strip — 10 anchor pills, all resolving to existing section IDs | n/a | — | structural |
| 1 | **§1 The 60-second read** — always expanded | open | — | Signal Summary + Team + Account headlines |
| 2 | **§2 Do this week** — urgent | `<details>` | `danger` | Account (S1) + Team (rung-4 cards) |
| 3 | **§3 Do this month** — plays | `<details>` | `warn` | Commerce + Account (3 plays) |
| 4 | **§5 Growth engine** — three subsections (same-dealer base · breakout product family · field team) | `<details>` | — | Commerce + Product + Team |
| 5 | **§6 The team** — top-10 leaderboard + 5 coaching cards + discount-discipline note | `<details>` | — | Team (RS-01 + rung-4 cards) |
| 6 | **§7 Full risk watchlist** — positions 6–25 (top 5 live in §2) | `<details>` | — | Account (S1 tail) |
| 7 | **§8 Product intelligence** — top-12 items + the named cross-sell | `<details>` | — | Product |
| 8 | **§9 Dealer base** — new / lapsed / returning + buyer-cadence segments + "two stories" callout | `<details>` | — | Account |
| 9 | **§10 Channels** — channel mix + eCat as a channel | `<details>` | — | Commerce |
| 10 | **§11 What this report can't see / how to trust these numbers** — honest disclosure *(may render as one combined section or two sequential sections — see note below)* | `<details>` | `info` | Appendix |
| 11 | Footer | n/a | — | — |

**Render gate inheritance:** §5's section-render gate still governs which of the 13 positions actually appear
(a section suppresses if its source-data section has no fired P0/P1 signal AND no query-driven subsection
passes the specificity test). The 13 above are the **maximum render**, not the minimum.

**Position 10 — single vs split rendering** *(NEW 2026-06-30 — cohort lesson; either form is gold-bar)*.
Position 10 may render as **one combined section** (the Sarreid pattern: §11 "What this report can't see /
how to trust these numbers" as a single block) OR as **two sequential sections** (the cci / hfg / kal
cohort pattern: §11 "What this report can't see — and what to add next" + §12 "How to trust these
numbers"). Choose based on length: if either subsection runs longer than ~200 words on the rendered MD,
**split into two sections**; if both subsections together fit in a single `<details>` collapsible without
visual fatigue, **combine into one**. The position count remains 10 either way (the second section, when
present, becomes position 10b); the footer remains position 11. Both renderings preserve the §5a.5
"6-item honest list, one sentence each" invariant.

### 5a.2 — §1 internal structure (the 60-second read)

The CEO can stop here and still take action. **Fixed shape — do not add a fifth metric card or a fourth callout:**

1. **Hero** — headline $ + YoY % + one sub-prose line (sets the period framing) — **NOT** a verbatim echo of any
   downstream sub-header (§N.9/N.10 catches the echo).
2. **4 metric cards** — exactly four; each one figure + one label + one micro-context line.
3. **3 CEO-callouts** — *"Three things you wouldn't have known without this report"* — exactly three; each one is
   a Tier-A finding with a §Q sensitivity hedge inline.
4. **Priorities by cadence** — three rows: `this-week / this-week / this-month`, each naming a real account +
   rep + dollar stake. Drives §2 and §3 expansion below.

### 5a.3 — §2 internal structure (Do this week)

- **7-row named call list** — not five, not ten. Sized for one rep meeting. Each row: account · rep · action ·
  one-line talking point · timing.
- **"Don't conflate the two conversations" callout** — splits decline calls (investigative) from growth calls
  (confirm/expand). Cadence-cliff rows tagged so the rep doesn't open a decline conversation by accident.
- **"How these were chosen" nested disclosure** — `<details>` inside `<details>`. Hides the selection logic
  from the CEO read; exposes it to the curious. Don't surface inline; don't drop entirely.

### 5a.4 — §6 internal structure (The team)

- **Top-10 RS-01 leaderboard** — the at-a-glance roster. House-rep screened (§N.1).
- **5 coaching cards** — not fewer when 5+ qualify; not more. Each card splits "real decline" from "growing but
  skipped a beat" *explicitly* (the framing failure the report avoids: rep walks into a growing account with a
  "we're worried about you" speech).
- **Discount-discipline note** — one line, named reps if Tier-2.

### 5a.5 — §11 internal structure (What this report can't see)

- **6-item honest list** — exactly six. Each item one sentence. Don't expand. Don't soften. The honesty is the value.
- The canonical six: margin / returns / AR / stock-outs / competitive losses / the "why" behind any decline.
  Add only on explicit per-org confirmation; never auto-extend.
- Single-feed posture named here: *"your invoiced business,"* not *"your total business"*; one-line disclosure of
  the booked-vs-invoiced agreement ratio.

### 5a.6 — The "don't break these" list (gold-state invariants)

These were settled by hand-iteration on Sarreid. The operator's first pass on the next client must NOT touch them:

| Invariant | Locked at | Why |
|---|---|---|
| CSS palette + typography | DM Sans + IBM Plex Mono; orange-warm accent `#C47A4A`; 4 semantic states (`ok` / `warn` / `danger` / `info`) | settled visual identity; re-skinning is a separate, scoped decision |
| Collapsible behavior | `<details>` with `urgent` / `month` / `quarter` color-bar variants; sticky TOC strip with inline `<script>` | JS dependencies on the inline `<script>` at the bottom of the HTML — preserve verbatim |
| 60-second read shape | hero → 4 metric cards → 3 CEO-callouts → priorities-by-cadence | the constraint *is* the gold standard; do not add a fifth card or a fourth callout |
| §2 call list size | 7 rows | sized for one rep meeting; less = thin, more = unfocused |
| §6 coaching cards | 5 (or fewer if <5 qualify; never more) | rendering 7 cards dilutes the action; the cards are the action layer the leaderboard never produced |
| §11 honest list | 6 items, one sentence each | softening or extending dilutes the credibility move |
| "How these were chosen" disclosure | nested `<details>` inside §2 | exposes selection logic to the curious without burdening the CEO read |
| Per-section sensitivity hedges | inline (within ±400 chars of the Tier-A/S claim — §Q) | the load-bearing voice move that makes the report read as consultant briefing, not dashboard |

The HTML/CSS/JS shell to lift verbatim is the Sarreid HTML body, the `<style>` block, and the closing `<script>`.
The Python pipeline (`run.sh` → `pipeline/` → `report_render/`) templates against this shell. Shipped 2026-07-01; golden regression verified (v9).

---

## 6. Generation sequence (3.0 sequence + 4.0 preflight bolted to the front)

0. **Reading-contract load (per [`CANON.md`](../CANON.md), before anything).** Load the four governing
   inputs into context first: `provenance_spine.md` (Tier-0 truth), the client `profile.md` (who this
   client is), `industry_context.md` (what's industry-normal, therefore *not* a finding — seasonality,
   market calendar, concentration, channel mix), and `communication_guideline.md` (how the report may
   talk). A run that skips any of the four is invalid.
1. **Provenance preflight (NEW, first).** Run `Q-ECON-00` (→ `COMMERCE_CONFIDENCE`, clamped `report_through_date`),
   `FEED_COMPLETENESS`, `Q-CHAN-00`, and the rep-identity gate (Spine §7.1). Compute `REPORT_INTELLIGENCE_TIER` (§4c).
   Resolve mode (§3). **Nothing downstream may emit a number that violates these caps.**
2. **Data gather** — execute the query library; materialize results (now invoiced-anchored).
3. **Signal detection** — run each signal's detection logic; **only signals whose feed passes their gate may fire**.
4. **Signal scoring** — `SIGNAL_RANK = surprise × dollar_impact × actionability`, where `dollar_impact` is a
   provenance-stamped number and the signal's confidence is `LEAST(its ceiling, COMMERCE_CONFIDENCE)`.
5. **Context bundles** — per-section, each carrying the provenance stamps + editorial rules.
6. **Section rendering** — build each qualifying section; every dollar three-tagged; rep naming tier-gated.
7. **Signal Summary** — top 5–7 by rank, re-sorted into narrative arc (momentum→intelligence→opportunity→risk),
   diversity constraint (max 4 from one section), finding #1 positive.
8. **HTML assembly** — fixed render order into the 3.0 template shell.
9. **Structural verification** — all mandatory subsections present.
10. **Provenance + static check (NEW + kept).** Re-read every dollar: confirm it has all three tags and traces to
    a query in the appendix; delete any that doesn't; then run the static checker.

---

## 7. Hard gaps — surfaced as opportunity, never faked (4.0 discipline meets 3.0's "If You Gave Us X")

3.0 already had a beautiful pattern for missing data: the **"With Connected Data" callout** and the **SIG-EXT-***
"if you gave us X" layer. 4.0's hard-gap list slots straight into it. These are **suppressed as facts** and
**offered as the upsell**, never estimated:

| Hard gap (4.0 suppress) | 3.0 surface to reuse | What connecting it unlocks |
|---|---|---|
| True/gross margin (no COGS) | "With Connected Data" callout | per-SKU/customer margin, true leakage-after-cost |
| AR / DSO / collections | callout | cash-risk on the concentration story (invoiced ≠ collected) |
| Channel attribution (`order_origin` null) | SIG-EXT-02 | "this customer shifted $X eCat → phone," precise displacement |
| Carrier / damage / claims | SIG-EXT (carrier) | damage-by-carrier, claims cost |
| Parent/family rollup (no native key) | SIG-EXT-03 | combined-relationship view (e.g. Wayfair across codes) |
| Returns on gross-only orgs (0 credit memos) | callout | net-of-returns truth |

**Rule:** the report never prints a faked version of these. It prints the **gap as a growth lever** — which, per
3.0's editorial voice, reads as opportunity, not apology.

---

## 8. Rendered document skeleton (unchanged from 3.0)

```html
<article class="insightful-report" data-mode="[1|2|3]"
         data-intelligence-tier="[STRONG|MODERATE|EARLY|MINIMAL]"
         data-commerce-confidence="[STRONG|PARTIAL|LIMITED|NONE]"
         data-feed-completeness="[CORROBORATED|UNVERIFIED|PARTIAL|STALE|DEAD]"
         data-generated="[ISO_DATE]" data-through="[CLAMPED_DATE]">
  <section id="signal-summary" data-position="1">...</section>
  <section id="team"           data-position="2">...</section>
  <section id="accounts"       data-position="3">...</section>
  <section id="commerce"       data-position="4">...</section>
  <section id="product"        data-position="5">...</section>
  <section id="platform"       data-position="6">...</section>
  <section id="appendix"       data-position="last">...</section>
</article>
```
The four `data-*` provenance attributes on the root are the only structural addition — they let the HTML shell
and the static checker assert that the whole document inherited a single, consistent confidence posture.

---

## 9. Relationship to the rest of 4.0

| File | Role in the report product |
|---|---|
| `signal_catalog_v4.md` | every detectable signal, re-anchored: detection, scoring, **provenance binding**, output format |
| `report_editorial_rules_v4.md` | voice (narrative arc, specificity, competitive-hypothesis, what-this-means) + the **three-tag** dollar rules |
| `provenance_spine.md` | Tier-0 truth: invoiced axiom, confidence tiers, `FEED_COMPLETENESS`, identity gates |
| `industry_context.md` | industry-normal layer — seasonality, market calendar, concentration, channel mix; if a pattern is explained here it's **context, not a finding** (loaded per the CANON reading contract) |
| `communication_guideline.md` | voice layer — the "no shit" test, anti-cute, Failure Modes 1–5, house style, pre-send checklist (loaded per the CANON reading contract) |
| `CANON.md` | the governed index: precedence order + reading contract this sequence honors |
| `query_library_v2.md` | SQL for LIVE gather/preflight/platform queries (see `WHAT_ACTUALLY_RUNS.md` / `config.QUERIES_ALL`) |
| `selling_customer_exception_layer.md` | S1 (account-health $-at-risk) + C2 (leakage-by-rep) — feed Account/Team/Commerce signals |
| `rep_copilot_operator.md` · customer brief operator (v5.1) · `rung4_option_a_operator.md` | the **per-entity** surfaces; this report is the **org-level roll-up** that sits above them |
| `capability/value_moment_catalog.md` | **roadmap** capability catalog — not loaded to run; code signals are authoritative |
| `Insightful Product 3.0/authority/html_report_template.html` | the HTML/CSS shell to port forward (delivery craft, do not rewrite) |

**Foundation-not-rewrite principle (from the roadmap):** keep 3.0's delivery shell, prompts, and section shapes;
swap the data underneath onto the provenance layer; add the levers 3.0 lacked (leakage, gated revenue-at-risk,
identity tiering); demote vanity scores unless fused to a defensible dollar.
