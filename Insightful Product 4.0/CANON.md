# CANON — Insightful Product 4.0 (governed index + reading contract)

> **What this is.** The index of governing docs for the 4.0 report product, the **precedence**
> when two of them conflict, and the **reading contract** every report run must honor before it
> touches data. This file is governance, not pipeline — operators and the render pipeline
> *consume* it; they do not re-author the rules it points to.
>
> **Status:** seeded 2026-06-29; foldered 2026-06-29; **re-anchored 2026-07-13** — capability
> roadmap docs live under `foundation/capability/` and are **not** part of the reading contract.
> `CANON.md` and `CHANGELOG.md` stay at the folder root. Plan:
> [`handoffs/REANCHOR_PLAN_2026-07-13.md`](handoffs/REANCHOR_PLAN_2026-07-13.md).

---

## Purpose layer (above the precedence chain)

The report's voice and posture derive from SuperCat's **Core Values** — Customer-Obsessed, Own the
Outcome, Learn Loudly — declared in the [company foundation](../../foundation/00_README.md). This
is the *purpose* layer: it explains *why* the report leads with value, refuses to fake a number, and
never narrates the client's business back to them. It does not participate in the data-authority
precedence chain below — it is the ground those rules stand on.

---

## Precedence (highest authority wins on conflict)

```
running code  >  WHAT_ACTUALLY_RUNS.md  >  provenance_spine  >  client profile  >  industry_context  >  communication_guideline  >  source-data labels
```

- **running code** (`pipeline/**`, `report_render/**`, `pipeline/templates/*.j2`,
  and the SQL fences extracted by `pipeline/cache.py`) — the product *is* the
  code. Doctrine describes it; it never overrides it.
- **`foundation/WHAT_ACTUALLY_RUNS.md`** — the runtime ground-truth map (the 24
  live queries, the 14 signals, the two gating axes, the template set), derived
  from the code. **If any doctrine file below disagrees with it, this doc wins.**
- **`foundation/provenance_spine.md`** — Tier-0 truth: invoiced axiom, confidence tiers, FEED_COMPLETENESS,
  identity gates, the gate catalog. The single definition of the invoiced-net +
  confidence-gate spine; nothing in the doctrine layer overrides it.
  *(Runtime commerce gate = `Q-ECON-00`; see Spine runtime mapping.)*
- **client profile** (`profile.md`, per-client, per-run input) — the authoritative statement of
  *this* client's segment, channels, top accounts, buyer types. Overrides industry defaults and a
  possibly-wrong source-data segment label.
- **`knowledge/industry_context.md`** — what is *normal* for furniture/lighting/décor (seasonality, market
  calendar, concentration, channel mix). If a pattern is explained here, it is **context, not a
  finding**. Overrides the voice layer on "is this even worth saying."
- **`knowledge/communication_guideline.md`** — voice only: how the report talks (the "no shit" test, anti-cute,
  failure modes, house style, pre-send checklist). Governs phrasing, not facts.
- **source-data labels** — raw segment/category/territory strings from the warehouse are the
  *lowest* authority; the profile or the Spine overrides them when they conflict.

---

## Vocabulary — the two axes (glossary)

**"Tier" is overloaded across the doctrine — collapse it to exactly two named
axes in prose.** Both are resolved in `pipeline/preflight.py` (`RunPosture`).

- **`COMMERCE_CONFIDENCE`** — *"can I show dollars?"* Values
  `STRONG / PARTIAL / LIMITED / NONE`. Set by `Q-ECON-00`. This is what the
  Spine's "confidence tiers" (§5) mean at runtime. (`FULL` is documented in the
  Spine but unreachable in the pipeline — the economics ceiling is `STRONG`.)
- **`REP_IDENTITY_TIER`** — *"can I name reps?"* Values `0 / 1 / 2`. Set by
  `RP-2` (Spine §7.1). This axis legitimately keeps the word "tier."

**"Behavior-only report"** (owner's term) = the `COMMERCE_CONFIDENCE = NONE`
output. No invoice feed, so the report analyzes in-app **rep behavior** and never
invents dollars. In `_base.md.j2` this is an ordering branch, not a separate
template family. Use this phrase — not "Tier 0 / Mode-2 / Activation" — in prose.

Everywhere else the word "tier" appears (VM stack rank, signal priority, data-mass
prose), it means something specific — name that thing, don't call it "tier."
**Do not rename the Python fields** `report_intelligence_tier`, `data_mass_tier`,
`rep_identity_tier` when quoting the gate table / appendix — those are literal
`RunPosture` field names.

---

## Reading contract (load before ANY queries run)

Before you run or reason about a report, read exactly these — nothing else is required:

0. **`foundation/WHAT_ACTUALLY_RUNS.md`** — what the factory actually executes
   (the 24 live queries, 14 signals, two axes, template set). Read this first; it
   tops precedence and settles any doctrine-vs-runtime conflict.
1. **`foundation/provenance_spine.md`** — the truth/confidence foundation (invoiced-net axiom + confidence gates).
2. **client profile** (`profiles/{org}.md` for the org being run; ratified, facts-only) — who this client is.
3. **`knowledge/industry_context.md`** — what's normal, therefore not a finding.
4. **`knowledge/communication_guideline.md`** — how the report is allowed to talk.

**Do not load** `foundation/capability/**` (VM catalog, VM runtime index, Money Map)
to run a report. Those are roadmap only.

LIVE SQL for the run is pulled by code from `foundation/query_library_v2.md` (20 of
24) + `operators/rep_copilot_operator.md` (`RP-2`, `RS-01`) +
`foundation/selling_customer_exception_layer.md` (`S1`, `C2`). You do not need to
read the full query library to run — only the reading contract above — then the
preflight (`Q-ECON-00` / gates) proceeds. A run that skips any of 0–4 is invalid.

---

## Governing docs (runtime — load / inherit)

| Doc | Role |
|---|---|
| `foundation/WHAT_ACTUALLY_RUNS.md` | **runtime ground truth — precedence-topping** (24 queries, 14 signals, 2 axes, templates) |
| `foundation/provenance_spine.md` | Tier-0 truth, gates, identity tiers |
| `foundation/query_library_v2.md` | SQL bodies — **LIVE 20** of 24 plus BACKLOG reference SQL (see its LIVE/BACKLOG index) |
| `foundation/selling_customer_exception_layer.md` | S1 + C2 — holds live SQL |
| `operators/rep_copilot_operator.md` | RP-2 + RS-01 — holds live SQL |
| `knowledge/industry_context.md` | industry-normal layer (context, not findings) |
| `knowledge/communication_guideline.md` | voice layer |
| `profiles/{org}.md` | per-client truth (ratified input) |
| `report_product/report_product_architecture.md` | report structure + generation sequence |
| `report_product/signal_catalog_v4.md` | the 14 detectable signals (spec; code in `signals.py` wins) |
| `report_product/report_editorial_rules_v4.md` | narrative arc + three-tag dollar rules |

## Capability / roadmap (do **not** load to run)

| Doc | Role |
|---|---|
| `foundation/capability/value_moment_catalog.md` (v4.2) | ~87 VM capability catalog |
| `foundation/capability/vm_runtime_index.md` | aspirational VM menu (not the factory manifest) |
| `foundation/capability/insights_moneymap_SYNTHESIS.md` | commerce synthesis / design bible |
| `foundation/provenance_map_rep.md`, `foundation/provenance_map_customer.md` | Tier-1 domain maps (reference) |
| `foundation/segmentation_derivation.md` | derived-segment method (🧊 FROZEN) |

Lower-tier docs in `operators/`, `handoffs/`, `config/`, `outputs/` consume the governing
set and do not redefine any rule they state. **Single definition, everywhere-reference.**
