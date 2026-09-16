# Failure Taxonomy — Insightful Product 2.0

Categorized failure modes with severities and detection methods.
Sourced from `HANDOFF.md`, `HARDENING_RESULTS.md`, and production run observations.

Last updated: 2026-06-16

---

## Category 1: Subsection Omission

Rendering agent fails to include a subsection whose gate is met.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| SO-1 | Q-52 penetration not rendered when PORTAL_CUSTOMER_DATA_PRESENT=true | **HIGH** | `check_static.sh` gate-aware check (Session 4) | Agent misreads gate_flags or skips cache file |
| SO-2 | Admin disclosure missing when ADMIN_REPS_IN_LEADERBOARD=true | **HIGH** | `check_static.sh` gate-aware check (Session 4) | Agent skips §2-ADMIN-DISCLOSURE append |
| SO-3 | Q-14b deceleration alert missing when HAS_PORTAL_ORDERS=true | **MEDIUM** | Manual browser review; future static check | Agent omits subsection 6b within subsection 6 |
| SO-4 | Q-63/65 mandatory subsections skipped in §2 | **HIGH** | Conditional Subsection Checklist (section guide) | Agent treats MANDATORY as conditional |
| SO-5 | §6 rendered when HAS_CLICKY=false | **HIGH** | `check_static.sh` (Clicky is hard-forbidden) | Incorrect gate evaluation in section manifest |

---

## Category 2: Duplicate / Stale Data

Agent renders the same data twice or carries forward prior-run data.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| DD-1 | Lynn Ross appears twice in §2 leaderboard | **MEDIUM** | Manual browser review; Conditional Subsection Checklist dedup rule | Q-01 Step 1 + Step 2 contain overlapping rep names |
| DD-2 | Same customer in both Q-13 and Q-52 tables with different GMV | **LOW** | Manual cross-section review | Q-52 joins on different time window than Q-13 |
| DD-3 | Stale metrics from prior run carried into new report | **HIGH** | Cache dir timestamp check | Agent reads wrong cache dir or old fragments |

---

## Category 3: Forbidden Phrase Leak

Prohibited terms appear in client-facing HTML.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| FP-1 | "ERP" in client-facing text | **HIGH** | `check_static.sh` REVIEW tokens + manual confirm | Agent uses technical term instead of "total business" |
| FP-2 | Segment label (Platform-Embedded) in §7 | **HIGH** | `check_static.sh` HARD tokens | Agent renders raw peer_group label |
| FP-3 | "Clicky" in delivered HTML | **HIGH** | `check_static.sh` HARD tokens | Agent references data source by name |
| FP-4 | "health score" in external output | **HIGH** | `check_static.sh` HARD tokens | Agent surfaces internal classification |
| FP-5 | Raw username (e.g., "staciebaker") in §2 table | **MEDIUM** | Manual review; future static check | Agent fails Q-63/64/65 username→display name cross-ref |

---

## Category 4: Template Token Leak

Internal pipeline markers appear as visible text.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| TT-1 | Literal `[HYPOTHETICAL]` in HTML | **HIGH** | `check_static.sh` HARD tokens | Agent renders pipeline tag instead of hedging language |
| TT-2 | Literal `[ESTIMATED]` in HTML | **HIGH** | `check_static.sh` HARD tokens | Agent renders pipeline tag instead of hedging language |
| TT-3 | Unsubstituted `{{VARIABLE}}` in output | **HIGH** | `check_static.sh` `{{` check | Stage 4 assembly fails to resolve template parameter |

---

## Category 5: Connection / Infrastructure Failure

Pipeline fails to complete due to infrastructure issues.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| CF-1 | Postgres connection pool exhaustion mid-batch | **HIGH** | `_run_status.md` shows PARTIAL; failed_queries list | Too many concurrent SSE connections (mitigated: Session 5 semaphore) |
| CF-2 | BigQuery timeout on large Mixpanel query | **MEDIUM** | `_run_status.md` failed_queries | Q-01 Step 1 scan across full events table |
| CF-3 | MCP SSE connection drop (VPN instability) | **MEDIUM** | Query retry logs; `_run_status.md` | Network-level transient failure |
| CF-4 | Service account key expired | **HIGH** | BigQuery auth error in logs | Credential rotation not tracked |

---

## Category 6: Structural HTML Defect

Output HTML is malformed or structurally incorrect.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| SH-1 | Unbalanced `<details>` tags | **MEDIUM** | `check_static.sh` tag balance check | Agent omits closing tag on collapsed subsection |
| SH-2 | Empty `<table><tbody></tbody></table>` for zero-traction items | **LOW** | Manual review; Q-61 rendering rules | Agent renders table instead of `.callout.warn` count |
| SH-3 | Missing `what-this-means` close block on subsection | **MEDIUM** | `check_static.sh` WTM count check (Session 4) | Agent omits required close block |
| SH-4 | `section-contents` middot list includes skipped subsections | **LOW** | Manual review | Agent lists subsections that were not rendered |

---

## Category 7: Semantic Error

Content is factually wrong or makes unsupported claims.

| ID | Example | Severity | Detection | Cause |
|----|---------|----------|-----------|-------|
| SE-1 | "portal_orders" described as "buyer self-service activity" | **HIGH** | Manual review; REVIEW tokens | Agent misinterprets data source semantics |
| SE-2 | Revenue projection without hedging language | **MEDIUM** | Manual review; Hard Rule #8 | Agent presents extrapolation as fact |
| SE-3 | Metric without time qualifier | **MEDIUM** | Manual review; Hard Rule #7 | Agent omits "trailing 12 months" or similar |
| SE-4 | Confidence footer shows wrong tier | **MEDIUM** | Cross-ref gate_flags → section_confidence → rendered footer | Agent reads wrong tier or paraphrases template |

---

## Severity Guide

| Level | Meaning | Action |
|-------|---------|--------|
| **HIGH** | Blocks delivery — report cannot ship | Fix before delivery. Add regression test. |
| **MEDIUM** | Degrades quality — report can ship with manual correction | Fix if time permits. Document in validation log. |
| **LOW** | Cosmetic or minor — no client impact | Fix in next iteration. |

---

## Detection Coverage Summary

| Detection Method | Categories Covered | Automated? |
|------------------|--------------------|-----------|
| `check_static.sh` (existing) | FP, TT, SH (partial) | Yes |
| `check_static.sh` (Session 4 enhancements) | SO (partial), SH (WTM count) | Yes |
| `_run_status.md` inspection | CF | Semi (requires run) |
| Conditional Subsection Checklist (per guide) | SO, DD | Manual (agent self-check) |
| Manual browser review | DD, SE, SH (partial), FP (context) | No |
| Golden-set eval (static mode) | FP, TT, SH | Yes |
| Golden-set eval (full mode) | All categories | Yes (with manual review step) |
