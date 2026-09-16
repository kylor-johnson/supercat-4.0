# Insightful Product 2.0 — Artifact Catalog

**Purpose:** Single inventory of files, roles, inputs, and outputs.
**Authority for contracts:** [`GUARDRAILS.md`](GUARDRAILS.md) (hard rules, boundaries, ownership).
**Last updated:** 2026-06-16

---

## Root Documentation

| File | Role |
|------|------|
| `README.md` | Package overview: how to run, authority hierarchy, output paths, locked decisions. |
| `SKILL.md` | Technical context for agents/maintainers: data sources, gating flags, common pitfalls. |
| `RUNBOOK.md` | Report generation runbook — invoke agent with shortname, then browser review. |
| `HANDOFF.md` | HTML output tuning handoff — current known issues and iteration workflow. |
| `GUARDRAILS.md` | **Law layer** — hard rules, boundaries, query ownership, quarterly review. |
| `ARTIFACT_CATALOG.md` | This file — file-to-role inventory. |
| `ELITE_EXECUTION_PLAN.md` | Phase 1 org-report enhancement map (Q-55 through Q-59 + Q-14b). |
| `ELITE_ORDER_OF_OPERATIONS.md` | 5-session implementation sequence for Phase 1 enhancements. |
| `POV_elite_insights.md` | Product strategy — what makes reports worth paying for. |
| `HARDENING_RESULTS.md` | v3 hardening run comparative analysis (UFI, CCI, MLI, WWJC). |

---

## Authority Files (do not modify at runtime)

| File | Role | Consumed By |
|------|------|-------------|
| `authority/value_moment_catalog.md` | **Semantic source of truth** — 51 VMs, allowed/forbidden claims. | All operators, all section guides. |
| `authority/external_vm_index.md` | Runtime VM lookup table — compact derivative of the catalog. | `run_prompt.md`, section guides. |
| `authority/external_report_blueprint.md` | Assembly rules: section order, conditional logic, report modes. | `run_prompt.md`, `stage4_assembly.md`. |
| `authority/query_library.md` | Audited SQL reference (Q-01 through Q-68+), schema-grounded. | `data_gather.py`, `stage1_preflight_and_queries.md`, section guides (for Q-02/Q-03 derivation rules). |
| `authority/peer_benchmark.md` | How to consume peer benchmark CSVs and BigQuery tables. | `section_07_peer.md`. |
| `authority/html_report_template.html` | Parameterized HTML/CSS/JS template (v3.0). | `stage4_assembly.md` (verbatim `<style>` and `<script>` blocks). |

### Gold References (layout/tone oracles — do not override catalog or blueprint)

| File | Role |
|------|------|
| `authority/gold/clm_2026-04-14_deep_intelligence_report.html` | **Primary layout oracle** — cleanest validated rendered output. |
| `authority/gold/clm_2026-04-14_executive_intelligence_report.html` | Historical layout oracle (predates profile retirement). |
| `authority/gold/jyc_2026-04-14_executive_intelligence_report_v2.html` | Historical second-org layout oracle. |

---

## Operator Files — External Report

### Entry Point

| File | Role | Inputs | Outputs |
|------|------|--------|---------|
| `operators/external/run_prompt.md` | **Primary external report entry point.** Orchestrates: data gather → section build → assembly → static check. | Client params, MCP access. | `runs/{shortname}_{date}/output/*_intelligence_report.html` |

### Guides (consumed by the executing agent during Steps 1–4)

| File | Role |
|------|------|
| `operators/external/guides/shared_rules.md` | Runtime semantic guardrails, fragment contract, CSS classes, confidence framework, forbidden phrases, highlight format. |
| `operators/external/guides/stage1_preflight_and_queries.md` | Data-gathering guide: org identity, gates, query execution plan, cache format, derived gates. |
| `operators/external/guides/stage4_assembly.md` | Assembly rules: §1 Executive Summary identity + rendering, Appendix, HTML assembly, QC. |
| `operators/external/guides/section_02_sales_team.md` | §2 Sales Team Performance — rep leaderboard, archetypes, coaching, behavioral queries. |
| `operators/external/guides/section_03_customers.md` | §3 Customer & Buyer Intelligence — activation, penetration, dormancy, velocity, whitespace. |
| `operators/external/guides/section_04_product.md` | §4 Product & Inventory Intelligence — catalog health, inventory, sales lines, fill rate. |
| `operators/external/guides/section_05_commerce.md` | §5 Commerce Analytics — channel mix, trends, capture rate, displacement, price erosion. |
| `operators/external/guides/section_06_portal.md` | §6 Portal Engagement — Clicky traffic, geography, sources (gated on `HAS_CLICKY`). |
| `operators/external/guides/section_07_peer.md` | §7 Peer Benchmarking — cohort comparison, top-performer patterns (gated on `HAS_PEER_DATA`). |
| `operators/external/guides/section_08_platform.md` | §8 Platform & Feature Utilization — feature usage, workflow maturity, seat utilization. |
| `operators/external/guides/orchestrator.md` | Canonical flow documentation (single `run_prompt.md`, optional validator swarm). |
| `operators/external/guides/ARCHITECTURE.md` | Design history doc (LOCKED) — staged pipeline blueprint. |
| `operators/external/guides/stage3_validator.md` | Optional fragment validation swarm (off by default). |

---

## Operator Files — Internal Brief

| File | Role | Inputs | Outputs |
|------|------|--------|---------|
| `operators/internal/generate_internal_brief.md` | **Internal CS brief entry point.** Pulls Health V2 + HelpScout + Jira. | Client shortname. | `runs/{shortname}_{date}/output/*_internal_brief.html` |
| `operators/internal/internal-brief/DESIGN.md` | v1.0 spec — account verdict, health explainer, support themes, meeting playbook. | — | — |
| `operators/internal/internal-brief/QUERIES.md` | Q-IB-HEALTH from Health V2 CSV + HelpScout/Jira queries. | — | — |
| `operators/internal/internal-brief/TEMPLATE.html` | HTML template with blue-steel accent (visually firewalled from external). | — | — |

---

## Scripts

| File | Role |
|------|------|
| `scripts/data_gather.py` | Python Stage 1 data gatherer: parallel SQL execution → cache file writer. Connects to Postgres via MCP SSE, BigQuery via service account. |
| `scripts/requirements.txt` | Python dependencies for `data_gather.py`. |

---

## QA Infrastructure

| File | Role |
|------|------|
| `qa/validation_runbook.md` | Step-by-step QA checklist for a report run. |
| `qa/known_limitations.md` | Stable cross-client limitations and known data-quality patterns. |
| `qa/report_delivery_checklist.md` | Final go/no-go gate before sending a report to a client. |
| `qa/org_validation_log_template.md` | Per-run log template — copy, fill, file in `qa/validation-logs/`. |
| `qa/validation-logs/` | Filed validation logs — one per completed org run. |

### Eval (Golden-Set Regression)

| File | Role |
|------|------|
| `qa/eval/README.md` | Golden-set eval overview: what it proves, two modes (static/full), frozen orgs, acceptance threshold. |
| `qa/eval/run_eval.md` | Operator prompt for running the eval (static or full mode). |
| `qa/eval/check_static.sh` | Post-build forbidden-phrase + structural-integrity checker. |
| `qa/eval/clm/` | Crystorama fixture: `input.md`, `expected/{gate_flags, section_manifest, assertions}.md`, `fixture-cache/`, `results/`. |
| `qa/eval/wwjc/` | Wildwood/Chelsea House fixture: `input.md`, `expected/{gate_flags, section_manifest, assertions}.md`. |

---

## Sibling Products

### Customer Intelligence (per-customer briefs)

| File | Role |
|------|------|
| `Customer Intelligence/00_product_concept.md` | Per-customer brief concept — sibling to org report. |
| `Customer Intelligence/01_data_inventory.md` | Verified data sources (Postgres + BigQuery). |
| `Customer Intelligence/02_brief_sections.md` | Full brief structure: 12+ sections. |
| `Customer Intelligence/03_advanced_insights.md` | Prescriptive layer: Next Best Product, Wallet Share, etc. |
| `Customer Intelligence/04_example_brief.md` | Mock brief with illustrative numbers. |
| `Customer Intelligence/05_gap_analysis.md` | Gap verification against live data. |
| `Customer Intelligence/06_industry_research.md` | Competitive landscape research. |
| `Customer Intelligence/07_prototype_findings.md` | 7 prototype briefs across 3 clients. |
| `Customer Intelligence/08_hardening_findings.md` | 15 hardening briefs across 5 orgs. |
| `Customer Intelligence/authority/customer_query_library.md` | CQ-01–CQ-26 production SQL. |
| `Customer Intelligence/authority/customer_brief_sections.md` | v3 rendering spec (Full vs Orders-Only modes). |
| `Customer Intelligence/authority/health_score_spec.md` | 0–100 composite health score (8 weighted signals). |
| `Customer Intelligence/authority/customer_gate_rules.md` | G-01 through G-09 gate definitions. |
| `Customer Intelligence/operators/customer_brief_run_prompt.md` | Single-customer brief entry point. |
| `Customer Intelligence/operators/org_readiness_profiler.md` | Pre-flight: run 9 gates, compute data richness score. |
| `Customer Intelligence/operators/pilot_batch_prompt.md` | Multi-agent batch prompt for ~40 briefs. |

---

## Output Directories

| Path | Contents |
|------|----------|
| `runs/{shortname}_{YYYY-MM-DD}/cache/` | Query result cache files (`Q-XX_results.md`), gate flags, manifests, confidence tiers. |
| `runs/{shortname}_{YYYY-MM-DD}/fragments/` | Per-section HTML fragments (`section_NN.html`). |
| `runs/{shortname}_{YYYY-MM-DD}/output/` | Final assembled HTML report(s). |
| `hosted/` | Published external reports (copied from run output). |
| `hosted-internal/` | Published internal briefs (copied from run output). |
| `Customer Intelligence/runs/{shortname}/{code}/` | Per-customer brief outputs (`brief.md`). |

---

## Archive

| Path | Contents |
|------|----------|
| `_archive/operators-staged-prompts/` | Legacy staged-pipeline operator files. |
| `_archive/operators-monolithic/` | Legacy monolithic operator files. |
| `_archive/reference-examples/` | Pre-canonical report examples (structural reference only). |
| `_archive/design-docs/` | Legacy design documents. |
| `_archive/reports-legacy/` | Legacy HTML reports from April 2026. |
| `_archive/validation-logs-legacy/` | Legacy validation logs. |
| `_archive/baseline_pre-bq-migration_2026-06-03/` | Pre-BigQuery-migration external report baselines. |
| `_archive/baseline_pre-bq-migration_internal_2026-06-04/` | Pre-BigQuery-migration internal brief baselines. |

---

*Maintainer: keep this catalog aligned when adding files, operators, or output paths.*
