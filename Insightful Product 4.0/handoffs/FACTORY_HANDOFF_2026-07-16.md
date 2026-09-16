# Insightful Product 4.0 — Agent Factory Handoff

**Status:** Re-homing map (framing handoff). **Date:** 2026-07-16
**Companion to:** `Touchstone: Agent Factory Overview (v1)`, 2026-07-09 — specifically
§3 (layer × lane × topology), §6 (the shared quality bar), and §7 (the CEO System
poured into the factory). This doc does the same §7 exercise for **Insightful
Product 4.0**.
**Audience:** whoever stands up the `f/` tree (eng/CTO) and anyone deciding what
Insightful reuses vs. owns.

---

## 1. What this is

This is **not a code change**. It is a map that re-homes the pieces of Insightful
Product 4.0 into the factory's L0–L4 harness stack, so the report product can move
onto GitHub → Windmill → Kubernetes → Langfuse the same disciplined way every other
agent does.

Nothing here overrides the folder's own governance. Precedence is still
`running code > [WHAT_ACTUALLY_RUNS.md](../foundation/WHAT_ACTUALLY_RUNS.md) >
provenance_spine > client profile > industry_context > communication_guideline`,
as declared in [`CANON.md`](../CANON.md). When the code changes, re-derive
`WHAT_ACTUALLY_RUNS.md` from the code — and re-derive this map from that.

The one-line pitch: **Insightful 4.0 is the factory's topology #2 (operator skill)
made real, and it already ships the L2 eval harness the CEO System is still
missing.**

---

## 2. Lane + topology header

```
lane:     customer_product
topology: operator_skill          # Touchstone §3.3 topology #2 — "the Insightful Product / copilot pattern"
owner:    Kylor Johnson
```

- **Lane = `customer_product`.** The output is a client-facing CEO Intelligence
  Report sold to SuperCat's wholesale clients. This puts the whole L4 layer behind
  the **outbound firewall**: named accounts, invoiced dollars, rep names, and call
  content are internal-only inputs that must never surface in the wrong tenant's
  report. The pipeline's provenance spine and identity tiers (`REP_IDENTITY_TIER
  0/1/2`) are exactly this firewall expressed in code.
- **Topology = `operator_skill`.** The Touchstone doc names "the Insightful
  Product / copilot pattern" as topology #2, and the fit is exact: provenance
  gates (`Q-ECON-00` → `COMMERCE_CONFIDENCE`), a surface-detection + fallback
  matrix (the two ordering branches in `_base.md.j2`, the four outcomes
  SHIP/ACTIVATION/PREVIEW/REDIRECT, and the deterministic template fallback for
  every prose slot), and a provenance appendix (§methodology).
- **Hybrid note for the CTO — do not over-fit the label.** The *runtime shape*
  today is a deterministic CLI/cohort batch (`./run.sh {org}`,
  `pipeline/run_cohort.sh`), which reads like topology #1 (scheduled report). The
  honest read: Insightful is an **operator-skill agent driven by a scheduled/batch
  harness**. It inherits topology #2's guides+sensors bundle; if it later runs on a
  Windmill schedule per-cohort, it additionally borrows topology #1's freshness
  gate. Pick the bundle, not the noun.

---

## 3. The L0–L4 crosswalk (real components, re-homed)

Same exercise as Touchstone §7. These are real files in this folder, each mapped to
the layer it belongs in. The test that decides placement: **if a second agent would
reuse it, it belongs in L0–L2; if it only makes sense for the report, it belongs in
its L3.**

### L0 — `f/platform/` (Substrate — Shared by all)

- **Data plane / access:** Postgres via `pg_dsn()` / `DATABASE_URL` in
  [`pipeline/config.py`](../pipeline/config.py) and the `user-supercat-postgres-vpn`
  MCP (same backing DB); BigQuery via the `bigquery-admin` MCP.
- **`bigquery_query`-equivalent tooling / cache layer:** the SQL
  extract → execute → CSV-write path in [`pipeline/cache.py`](../pipeline/cache.py),
  [`pipeline/populate_cache.py`](../pipeline/populate_cache.py), and the MCP-fed
  variant [`pipeline/mcp_cache_tool.py`](../pipeline/mcp_cache_tool.py)
  (`cache.import_from_dicts`).
- **Canonical query library:** [`foundation/query_library_v2.md`](../foundation/query_library_v2.md)
  (LIVE 20 of 24) + the SQL held in
  [`foundation/selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md)
  (`S1`, `C2`) and `operators/rep_copilot_operator.md` (`RP-2`, `RS-01`). This is a
  shared spine — a rep copilot would query the same library.
- **Consolidated secrets:** `DATABASE_URL` / `PG*` + `ANTHROPIC_API_KEY`
  (+ optional `INSIGHTFUL_NARRATIVE_MODEL`). Today env-driven and `.gitignore`'d;
  in the factory these move to the **Windmill / K8s secret store** — never GitHub.
- **Freshness / provenance gate:** the "is the data fresh enough to run?" analog is
  the **dated-cache immutability contract** (`cache/{org}/{date}/` is written once,
  never mutated) plus the checksum verification in `regression.sh`. Gap vs. the CEO
  System: there is no standalone `artifact_freshness.py`-style age gate — freshness
  is a human choice of `--date` today.

### L1 — `f/context/` (Context — Shared, firewalled)

- **Foundation context read at runtime:**
  [`knowledge/industry_context.md`](../knowledge/industry_context.md) — the
  furniture/lighting "what's normal" layer (seasonality, market calendar,
  concentration) that turns a raw pattern into context-not-a-finding. This is the
  `CEO_SYSTEM_CONTEXT.md` analog.
- **Purpose layer:** SuperCat Core Values via
  [`foundation/00_README.md`](../../foundation/00_README.md) (referenced by
  `CANON.md`'s purpose layer).
- **Org registry:** [`config/org_ids.json`](../config/org_ids.json) (shortname →
  org id / display name) — the `customer_org_shortnames.csv` analog.
- **Per-client ratified context:** `profiles/{org}.md` (ratified) and
  `profiles/{org}.draft.md` (unratified). These are `customer_product`-lane context
  and stay firewalled per client. A same-client rep copilot would legitimately reuse
  the ratified profile — which is why it sits in L1, not buried in the report's L3.

### L2 — `f/standards/` (Standards — the shared quality bar)

- **Epistemic constitution / guardrails:** [`CANON.md`](../CANON.md) (precedence +
  reading contract) + [`foundation/provenance_spine.md`](../foundation/provenance_spine.md)
  (invoiced-net axiom, confidence tiers, `FEED_COMPLETENESS`, identity gates, gate
  catalog) + [`knowledge/communication_guideline.md`](../knowledge/communication_guideline.md)
  (voice / the "no shit" test / anti-cute / pre-send checklist).
- **Output-contract sensors (computational, run every time):**
  [`pipeline/smoke_check.py`](../pipeline/smoke_check.py) (structural),
  [`pipeline/slot_validator.py`](../pipeline/slot_validator.py) (prose-slot
  number-parity + voice lint), [`pipeline/prose_conformance_check.py`](../pipeline/prose_conformance_check.py),
  and the HTML-boundary gate [`report_render/step10_check.py`](../report_render/step10_check.py)
  (§P forbidden vocab, §Q sensitivity hedges, §R concentration, §S addressable
  base) + `report_render/tests/`.
- **Eval harness — already built (the CEO System's missing row):**
  [`regression.sh`](../regression.sh) + [`config/golden_set.json`](../config/golden_set.json)
  — a checksum-verified golden set over 6 orgs (cache date `2026-07-02`, ali
  `2026-07-01`) that prints `GOLDEN SET: PASS (6/6)`. This is exactly the L2 eval
  runner Touchstone §6 marks **Missing** for the CEO System. Insightful should
  *donate* this pattern up to shared L2, not keep it private.
- **Gap:** automated **drift detection**. The "Growth Loop maintenance" retro
  (`pipeline/README.md` §Growth Loop) is real but **manual** — it's the
  `editorial_memory.py` steering-loop analog, not yet a measured sensor. This is the
  row Langfuse closes (§5).

### L3 — `f/agents/insightful_report/` (Agent-specific)

- **Orchestrator:** [`run.sh`](../run.sh) (top CLI: outcome routing + exit codes),
  [`pipeline/run_report.py`](../pipeline/run_report.py) (single-org),
  [`pipeline/run_cohort.py`](../pipeline/run_cohort.py) +
  `pipeline/run_cohort.sh` (fan-out + 4-bucket segmentation), and the query
  manifest / DAG in [`pipeline/config.py`](../pipeline/config.py)
  (`QUERIES_PREFLIGHT / GATHER / PLATFORM`).
- **Stages (the agent loop):** `preflight.py` (`RunPosture`, the two axes) →
  `gather.py` (typed bundles) → `signals.py` (14 detectors, `SIGNAL_RANK`,
  top-7 arc) → `assemble.py` (Jinja2 → MD) → `narrative.py` (bounded prose),
  supported by `fact_bundles.py` and `extract_deterministic_core.py`.
- **Prompts / prose:** the six bounded prose slots (hero, talking points, coaching,
  plays, growth connective, outreach — every slot has a fact bundle + parity gate +
  voice lint + deterministic fallback) and the operator specs
  (`operators/report_operator.md`, `operators/rep_copilot_operator.md`,
  `operators/rung4_option_a_operator.md`, `operators/external/run_prompt.md`) plus
  the report spec docs (`report_product/report_product_architecture.md`,
  `signal_catalog_v4.md`, `report_editorial_rules_v4.md`).
- **Renderers:** `report_render/` (`html_renderer.py`, `md_parse.py`, `md_render.py`,
  `naming.py`, `sections.py`) + the one template family in
  `pipeline/templates/*.j2` (`_base` + `header` + `section_01..11` + `_macros`).
- **Header:** `lane: customer_product`, `topology: operator_skill`, `owner: Kylor`.

### L4 — outputs (Agent-specific, `customer_product` lane)

- `outputs/{Org}_CEO_intelligence_report_{date}.html` — **SHIP** (client-facing)
- `outputs/{Org}_Activation_intelligence_report_{date}.html` — **ACTIVATION**
  (eCat-only, no invoice feed)
- `outputs/{org}_PREVIEW_{date}.html` — **PREVIEW** (draft profile; internal)
- `outputs/{org}_DRAFT_{date}.md` — pipeline draft (internal)
- `outputs/{org}_GATESTOP_{date}.md` — **REDIRECT** (zero-signal; internal only)

Four-outcome contract with exit codes `0` (SHIP/ACTIVATION/PREVIEW), `1`
(quality-gate failure), `2` (REDIRECT), `3` (hard failure). These are
`customer_product`-lane artifacts and stay **physically separate** from any
`internal_ops` output (e.g. the CEO System's `reports/ceo_system/`).

---

## 4. Reuse vs. own — the "second agent" test

Everything that passes "a second agent would reuse it" is pulled out of the report's
private ownership and into shared L0–L2:

- **Passes → shared (L0–L2):** the Postgres/BigQuery data plane and MCP access; the
  canonical SQL library; the provenance spine (invoiced-net axiom + confidence
  gates + identity tiers); the industry-context and voice layers; the output-contract
  sensors and the golden-set eval harness.
- **Report-only → stays L3:** the signal detectors and their ranking arc, the
  section templates and renderers, the six prose slots, the outcome-routing
  orchestrator, and the operator/spec docs that define what *this* report says.

When the **rep copilot** gets built for the same clients, it reuses L0–L2 unchanged
(same DB, same SQL library, same spine, same profiles, same quality bar) and only
writes its own L3. That is the whole point of the layering.

---

## 5. What the factory adds (gaps to close)

- **Langfuse tracing — not wired.** Add the three trace levels (whole run / artifact
  / AI call) from Touchstone §8. Metadata should carry `run_date`, `org`,
  `git_commit_sha`, `windmill_run_id`, `commerce_confidence`, `rep_identity_tier`,
  outcome, and per-slot prose provenance (LLM vs. fallback). This also gives the
  drift-detection sensor a home.
- **Secrets move.** `DATABASE_URL`/`PG*` and `ANTHROPIC_API_KEY` leave local env and
  go to the Windmill/K8s secret store; the pipeline already reads them from the
  environment, so this is an injection change, not a code change.
- **Runtime move.** Retire the local iCloud/Mac runtime. The hard part is already
  done: paths are repo-root-relative via `WORKSPACE_ROOT` in
  [`pipeline/config.py`](../pipeline/config.py), and the folder was re-anchored on
  2026-07-13 ([`handoffs/REANCHOR_PLAN_2026-07-13.md`](REANCHOR_PLAN_2026-07-13.md)).
  Remaining: containerize, let Windmill schedule the cohort run on Kubernetes.
- **Make the sensors blocking.** The smoke/slot/step10 checks exist; confirm each is
  a hard gate in the Windmill flow (fail the run, don't warn).
- **Freshness gate.** Optionally add an explicit cache-age gate so a scheduled run
  refuses stale data rather than relying on a human-chosen `--date`.

---

## 6. Reproduce a run from this handoff

The zip carries **no client data** (firewall). The recipient reproduces from source:

1. Set up the venv: `python3 -m venv .venv-renderer && .venv-renderer/bin/pip install -r requirements-pipeline.txt`.
2. Provide access: `DATABASE_URL`/`PG*` (VPN active) or use the
   `user-supercat-postgres-vpn` MCP; set `ANTHROPIC_API_KEY` (optional — the
   pipeline ships with deterministic fallback via `--no-narrative`).
3. Populate cache + run one org: `./run.sh sarreid --populate-cache`.
4. Verify the port is faithful: `./regression.sh` should print
   `GOLDEN SET: PASS (6/6)` once the golden cache dates are populated. A byte-identical
   golden run is the acceptance test that the environment move preserved behavior.

---

*Framing handoff v1. Refine as the `f/` tree is stood up. When the code changes,
re-derive `WHAT_ACTUALLY_RUNS.md`, then this map.*
