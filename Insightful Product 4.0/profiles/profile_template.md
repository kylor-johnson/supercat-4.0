# Client Profile — {Client Name} (`{shortname}`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of this client's **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule and the derive→ratify→cache workflow.
>
> **Status:** DRAFT (derived, not yet ratified) | RATIFIED {date} — _set one_. A run may proceed only against a
> RATIFIED profile.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | {legal/display name} | ratified |
| `organization_id` (Postgres) | {id} | `Q-ECON-00` preflight |
| Shortname | `{shortname}` | ratified |
| Same-name disambiguation | {e.g. "`fal` is a different company — not this org"} | ratified |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` (clamps fantasy dates) | gate-computed |

## 2. Business model / segment

- **Model:** {manufacturer | distributor | marketplace seller | hybrid — one line, factual}
- **Client segment (SuperCat v4.0, stamped):** {exact v4_segment label WITHOUT the leading "N. ", e.g. Luxury Specification | Premium Trade Brand | Mid-Market Multi-Channel | Volume Distribution — or `unassigned` if the org is not on the stamped 109-org roster; do not infer}
- **How they sell (axis):** {MASTER how_they_sell}
- **What they sell (axis):** {MASTER what_they_sell}
- **Who they sell to (axis):** {MASTER who_they_sell_to}
- **Price (continuous, not a boundary):** best available unit price ≈ ${best_price} (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org={shortname} · org_id={id} (verified)
- _Forbidden here: any judgment about whether the model is healthy._

> **Client segment vs in-client customer segmentation — do not conflate.**
> - **Client segment** (this field) = SuperCat's stamped **selling-motion** classification of this client org (Workstream A, Client Segmentation v4.0). It is a fact about how *this manufacturer* goes to market and belongs on the profile.
> - **In-client customer segmentation** = behavior-derived clusters of the *buyers inside this client's book* (Workstream B, `foundation/segmentation_derivation.md` / Q-SEG-DERIVE). That method is 🧊 FROZEN (Spine §8) and is **NOT** a profile field — never stamp a buyer-cluster label here.

## 3. Channel model (how they sell)

- {e.g. "sells through independent dealers + one drop-ship marketplace; eCat is a minority channel under 20%"}
- This overrides the industry-default channel mix in `../knowledge/industry_context.md` when they differ.
- _State the structure, not a finding about it._

## 4. House / sample / marketplace accounts to screen

The bill-to codes/names excluded from leakage and from leadership-facing dispersion (drives the leakage headline):

- House: {patterns/codes, e.g. `ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`}
- Named exclusions: {specific bill-to numbers/names confirmed at ratification}
- Marketplace account(s) handled separately: {name + why screened from per-dealer dispersion}
- _This is a scope decision, not a finding — it sets which rows the math runs on._

## 5. Buyer-type context

- {e.g. "a meaningful share of one-time buyers are designer/project purchases — a conversion test, not assumed churn"}
- Used so the report frames a pattern correctly **without** pre-judging it.

## 6. Structural concentration (context, NOT a finding)

- {e.g. "one marketplace account is a structurally large share and runs through one rep — known and structural"}
- Stated so the report doesn't "discover" known structure as a surprise. The *dollar* of it still comes from live data.
- _No number is asserted here; the run computes it._

## 7. Report mode default + scope exclusions

- **Default mode:** {1 Standard | 2 Activation | 3 Reactivation} — _the gate (`Q-ECON-00`/§3) still resolves mode live;_
  _this is only the expected default and is overridden by the gate if data says otherwise._
- **Confirmed hard-gap suppressions for this org** (no faking — surface as upsell only): {margin/COGS, AR/DSO,
  returns/credit-memos, stock-outs, carrier/damage, segmentation — list what is genuinely absent for this org}.

## 8. Sensitive callouts — per-client scrubbing policy *(gold-stamp 2026-06-30)*

The render-time policy for marketplace / strategic / sensitive accounts the client wants treated differently
than a normal dealer in the rendered output. Drives whether an account gets its own standalone section, gets
folded into body prose, or is screened from leadership-facing dispersion entirely.

**The automatic top-1-share rule (default — used unless the human ratifier overrides per account below):**

| Account's top-1 share of LTM invoiced revenue | Render policy | What renders |
|---|---|---|
| **≥ 20%** | `full_section` | Standalone section with the account named, its $-share, its YoY, and a "Decide this quarter — the {account} question" decision block in §3 |
| **5%–20%** | `body` | Named in body prose (Account intelligence, Growth Engine subsections, Channels) but no standalone decision block |
| **< 5%** | `exclude_only` | Screened from per-dealer dispersion / concentration calcs (per §4 above) but not surfaced in client-facing copy |

The rule is computed once at preflight (Step 1) from the deterministic `Q-ECON-CONC` output for this org
and the resulting policy is logged in the Appendix Traceability block. The human ratifier may override per
account in the table below — overrides win, and the override reason is logged on ship.

**Per-account overrides (rare — use only when the auto rule produces the wrong client read):**

| Account (bill-to or name) | Auto rule says | Override to | Reason |
|---|---|---|---|
| {e.g. "WAYFAIR (28239)"} | {full_section at 29.8%} | {body} | {e.g. "client deliberately under-narrates marketplace channel; surfaces only as a body mention"} |

**Cascade rule (the orphaned-hero-hedge fix from qa-lessons Finding 7):** when a callout is toggled out
of `full_section` to `body` or `exclude_only`, **every reference to it downstream** (hero lead-in, §5
Growth Engine sub-headers, §10 Channels prose, §11 methodology bullets) must drop or auto-substitute in
the same render pass. Leaving a hero hint promising a reveal that no longer exists is a §N-class defect
caught at Step 10.

_Forbidden here: any judgment about whether the account is good or bad for the client. The policy is a
scope decision (which surface renders this account), not a finding (whether this concentration is risk)._

---

### Ratification log
- {date} — {what was ratified / what changed} — {who}
