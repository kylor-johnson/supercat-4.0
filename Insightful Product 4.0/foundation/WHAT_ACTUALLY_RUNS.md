# WHAT ACTUALLY RUNS — the runtime ground-truth map

> **Precedence-topping.** This doc describes what the shipped report factory
> (`./run.sh {org} --date {date}`) actually executes, transcribed by reading the
> code — `pipeline/config.py`, `pipeline/signals.py`, `pipeline/preflight.py`,
> `pipeline/cache.py`, and `pipeline/templates/*.j2`. **If any other doctrine
> file disagrees with this one, this one wins** — because this one is derived
> from the running code, and the code is the product. Everything else in
> `foundation/capability/` (the VM catalog, VM runtime index, Money Map synthesis)
> and the BACKLOG portion of the query library is capability/roadmap documentation,
> not a description of the running pipeline.
>
> Nothing in this file changes what the pipeline emits. When the code changes,
> re-derive this file from the code — never the reverse.

---

## The two axes that gate everything

Both are resolved in `pipeline/preflight.py` (`RunPosture`) and drive every
downstream decision.

- **`COMMERCE_CONFIDENCE`** — *"can I show dollars?"* Values
  `STRONG / PARTIAL / LIMITED / NONE` (`preflight.Confidence`). Set from
  `Q-ECON-00`. `NONE` = no usable invoice feed → the **behavior-only report**
  (owner's term: analyze in-app rep behavior; never invent dollars).
  Note: the code's ceiling is `STRONG` — `FULL` is documented in the Spine but is
  unreachable in the pipeline (`preflight._derive_data_mass_tier` /
  `_intelligence_tier` top out at `STRONG`).
- **`REP_IDENTITY_TIER`** — *"can I name reps?"* Values `0 / 1 / 2`
  (`RunPosture.rep_identity_tier`). Set from `RP-2`.
  `0` = no ERP rep key → behavior-only rep insights; `1` = `rep_number` grain,
  no names; `2` = named rep→revenue allowed.

`REPORT_INTELLIGENCE_TIER = LEAST(DATA_MASS_TIER, COMMERCE_CONFIDENCE)`
(`preflight._intelligence_tier`). `data_mass_tier`, `report_intelligence_tier`,
and `rep_identity_tier` are literal `RunPosture` field names — do not rename them
in prose that quotes the gate table.

`resolve_mode()` maps the two axes to one of:
`Mode 1 - Standard`, `Mode 1 - Tier-1 degraded`, `Mode 2 - Activation`,
`Gate-STOP`.

---

## The live queries — 24 (`config.QUERIES_ALL`)

Derived from `pipeline/config.py`. `QUERIES_ALL = QUERIES_PREFLIGHT +
QUERIES_GATHER + QUERIES_PLATFORM`. SQL bodies are extracted at cache time by
`pipeline/cache.extract_sql()` from the docs in `cache._CANON_DOCS`
(query_library_v2.md → rep_copilot_operator.md → selling_customer_exception_layer.md
→ rung4_option_a_operator.md, first match wins).

**PREFLIGHT (4)** — posture resolution, read by `preflight.py`:
`Q-ECON-00`, `Q-CHAN-00`, `Q-CHAN-06`, `RP-2`.

**GATHER (13)** — the report body:
`Q-ECON-LEAK`, `Q-ECON-CONC`, `Q-ECON-NRR`, `Q-ECON-CONTRIB`, `RS-01`, `S1`,
`C2`, `Q-CHAN-10`, `Q-CHAN-05`, `Q-PROD-TOP`, `Q-PROD-FAMILY`, `Q-CROSS-SELL`,
`Q-DEALER-COHORT`.

**PLATFORM / rep-behavior floor (7)**:
`Q-08`, `Q-09`, `Q-10`, `Q-11`, `Q-R1`, `Q-R2`, `Q-R4`.

Where the SQL actually lives (verified via `cache._find_block_in_doc`):
- **`query_library_v2.md`** holds 20: all of the above **except** the four below.
- **`operators/rep_copilot_operator.md`** holds `RP-2`, `RS-01`.
- **`foundation/selling_customer_exception_layer.md`** holds `S1`, `C2`.

Doctrine claims "~120 queries" in the library; only these 24 IDs run, and only
20 of them are sourced from the library file. The rest of the library is BACKLOG.

---

## The signals — 14 (`pipeline/signals.py` `SignalKind`)

Every detector that can fire, from `signals.SignalKind` + `detect_all()`:

`real_decline`, `cadence_cliff`, `growth_pocket`, `new_line_takeoff`,
`lift_concentration`, `rep_overperform`, `rep_underperform`, `rep_atrisk_book`,
`cross_sell_pocket`, `second_year_gap`, `channel_concentration`, `ecat_minority`,
`leakage_discipline`, `territory_cluster_decay`.

- `SIGNAL_RANK = surprise × dollar_impact × actionability` (`Signal.rank`).
- Each signal's confidence ceiling is capped at `COMMERCE_CONFIDENCE`
  (`detect_all()` tail).
- `signal_summary_set()` selects top-7 into a momentum→intelligence→opportunity→risk
  arc; industry-normal patterns are down-weighted, not suppressed
  (`_apply_industry_downweights`).

### Industry downweights — what actually fires (honesty, 2026-07-13)

`INDUSTRY_CONTEXT_DOWNWEIGHT` in `signals.py` is grounded in
`knowledge/industry_context.md`, but **most conditions are stubs**:

| Signal kind | Condition | Runtime |
|---|---|---|
| `ecat_minority` | `always` | **LIVE** — surprise × 0.5 |
| `channel_concentration` | `single_channel_is_marketplace_or_dtc` | **STUB** — needs profile; logs + skips |
| `cadence_cliff` | `buyer_type_is_project_or_designer` | **STUB** — needs profile; logs + skips |
| `second_year_gap` | `buyer_type_is_project_or_designer` | **STUB** — needs profile; logs + skips |
| `lift_concentration` | `no_second_qualifying_fact` | **STUB** — not evaluated yet; logs + skips |
| `real_decline` | `seasonal_q1_to_q2_dip_under_25pct` | **STUB** — not evaluated yet; logs + skips |

Do not claim the factory fully enforces industry-context demotion beyond
`ecat_minority`. Wiring the stubs is Phase D2 (deferred; may affect golden).

Doctrine claims "~87 value moments across 13 domains"; only these 14 detectors
fire. The VM catalog is capability documentation, not the runtime signal set.

---

## The template set (`pipeline/templates/*.j2`)

One template family. `_base.md.j2` includes `header.md.j2` + the section files;
`_macros.md.j2` holds shared macros. There is no `section_04`.

`_base.md.j2` has exactly **two ordering branches**, keyed on
`posture.commerce_confidence`:

- **STANDARD** (`!= NONE`): hero → thisweek → thismonth → layers → team →
  watchlist → products → dealers → channels → methodology.
- **behavior-only** (`== NONE`): hero → team → channels → `erp_unlock_block` →
  methodology. This is an ordering branch, **not** a second template family — it
  drops the ERP-dependent sections and closes with a single "what an ERP feed
  unlocks" block.

---

## The doctrine-vs-runtime gaps this doc closes

| Doctrine claims | Runtime reality (this doc) |
|---|---|
| ~87 value moments across 13 domains | 14 signal detectors fire (`signals.py`) |
| ~120 queries in `query_library_v2.md` | 24 IDs run (`config.QUERIES_ALL`); 20 sourced from the library |
| "tier" means ~5 things | Two axes: `COMMERCE_CONFIDENCE`, `REP_IDENTITY_TIER` |
| Same truth restated in ~5 docs | One spine: `provenance_spine.md` (invoiced-net + confidence gates) |
