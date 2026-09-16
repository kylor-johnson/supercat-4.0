# Re-anchor Plan — Insightful Product 4.0 (2026-07-13)

> **Owner decision pending.** This plan re-centers the product on the true runtime
> anchors without changing report dollars, golden checksums, or LIVE SQL bodies.
> Derived from the 4.0↔3.0 quality review + core-file weave audit.

---

## 0. Non-negotiables (freeze rules)

Do **not** do any of the following in this re-anchor:

1. **No commercial number changes** — no SQL body edits to LIVE queries; no gather/signal formula changes that alter `$` outputs.
2. **No golden-set re-baseline unless forced** — `config/golden_set.json` v9 `deterministic_core_sha256` for sarreid/cci/clc/da must still pass after every phase. If a phase would force a re-baseline, **stop and ask the owner**.
3. **No deletion** — archive via `mv` only; log every move in `_archive/ARCHIVE_LOG.md` (existing pattern).
4. **No “make FULL work”** — `FULL` remaining unreachable on a single invoice feed is intentional; document it, don’t invent corroboration.
5. **No resurrecting BACKLOG queries** into `QUERIES_ALL` as part of this pass.
6. **No rewrite of `value_moment_catalog.md` content** — move/label only.

**Allowed to change:** governance docs, reading contracts, stale ID references in *report_product / operators / skill / README*, folder placement of aspirational docs, agent skill load list, honesty banners, industry-downweight stub documentation (and optionally wiring stubs → real, only if profile fields already exist and regression stays green).

---

## 1. Target end-state (what “re-anchored” means)

### Live governing set (must load to run / reason about a report)

| # | Doc | Role |
|---|-----|------|
| 0 | `foundation/WHAT_ACTUALLY_RUNS.md` | Runtime map (24Q / 14 signals / 2 axes) |
| 1 | `foundation/provenance_spine.md` | Truth axioms — **reconciled to Q-ECON-00 as the live commerce gate** |
| 2 | `profiles/{org}.md` | Client truth |
| 3 | `knowledge/industry_context.md` | Context ≠ finding |
| 4 | `knowledge/communication_guideline.md` | Voice |
| 5 | LIVE SQL sources | `query_library_v2.md` LIVE 20 + `rep_copilot_operator.md` (RP-2, RS-01) + `selling_customer_exception_layer.md` (S1, C2) |

### Capability / roadmap (do **not** load to run)

| Doc | Disposition |
|-----|-------------|
| `value_moment_catalog.md` | Move to `foundation/capability/` (or `_archive/capability/` if owner prefers harder split) |
| `vm_runtime_index.md` | Same |
| `insights_moneymap_SYNTHESIS.md` | Same |
| BACKLOG SQL inside `query_library_v2.md` | Keep in file for now; strengthen LIVE banner; **do not split file in Phase 1** |

### Explicitly demoted from “must read”

- `report_product/*` — still report **spec**, not reading-contract #1–4
- `operators/*` — consume canon; do not redefine gates
- Open handoffs — historical; not runtime

---

## 2. Phased work

### Phase A — Governance shelf (safest, highest clarity)

**Goal:** Make the folder structure match the mental model so agents stop loading the museum.

1. Create `foundation/capability/` (preferred over `_archive` so capability remains findable, not “dead”).
2. Move (not edit bodies):
   - `value_moment_catalog.md`
   - `vm_runtime_index.md`
   - `insights_moneymap_SYNTHESIS.md`
3. Update all in-repo links that pointed at the old paths (CANON, WHAT_ACTUALLY_RUNS, query_library header, report_product pointers, operators “inherits” blocks).
4. Rewrite `CANON.md` canon table:
   - Split into **Governing (runtime)** vs **Capability (roadmap)** sections
   - Reading contract stays 0–4; add explicit “do not load capability/ to run”
5. Add a 10-line banner at top of each moved file: *Capability / not what `./run.sh` executes. See WHAT_ACTUALLY_RUNS.md.*
6. Log moves in `_archive/ARCHIVE_LOG.md` (even if destination is `capability/`, not `_archive/`).
7. `CHANGELOG.md` entry.

**Exit gate:** `rg` for old paths returns only intentional archive notes; `./regression.sh --verify` still green (no code touch → should be identical).

---

### Phase B — Spine ↔ runtime reconciliation (doc-only, precision required)

**Goal:** End the `Q-PROV-00` vs `Q-ECON-00` cognitive fork without deleting BACKLOG SQL.

1. In `provenance_spine.md`:
   - Add a **Runtime mapping** callout near §6: *Factory commerce gate = `Q-ECON-00` (`QUERIES_PREFLIGHT`). `Q-PROV-00` remains the doctrinal ancestor / BACKLOG SQL in the library; live posture is derived from Q-ECON-00 outputs.*
   - Clarify §5: `FULL` is doctrinal; factory ceiling = `STRONG` (already noted in CANON — promote into Spine header so it can’t be missed).
   - Do **not** delete §6.1 `Q-PROV-00`; mark it `BACKLOG / doctrinal preflight` and point to §6.8 `Q-ECON-00` as **LIVE**.
2. In `report_product/report_product_architecture.md` + `signal_catalog_v4.md` + `operators/report_operator.md`:
   - Replace live-path claims of `Q-PROV-00` / `Q-SELL-QC` / `Q-63/64/65/69/70` with the LIVE 24 set (or “BACKLOG — not in QUERIES_ALL”).
3. Keep `query_library_v2.md` BACKLOG bodies intact; only fix **headers / indexes / “what runs” claims** that imply those IDs ship.

**Exit gate:** Zero places in `report_product/` or `operators/report_operator.md` claim a non-LIVE query is what the factory runs. Golden verify unchanged.

---

### Phase C — Voice/industry actually load on the agent path

**Goal:** Close the gap where API path loads knowledge files but the Cursor skill / prose-file path does not.

1. Update `.cursor/skills/insightful-report-4/SKILL.md`:
   - Step 0 reading contract: WHAT_ACTUALLY_RUNS → spine → profile → industry → communication_guideline
   - Require agent to apply guideline failure modes + industry “context not finding” before writing slots
   - Keep absolute constraints / forbidden vocab (already present)
2. Update `README.md` hybrid-prose paragraph so it matches v9 (LLM expresses, never computes) — kill “fully templated, no LLM required” as the only story (deterministic fallback remains true; hybrid is the product).
3. Optional small code: if easy and safe, have `run_report.py` print a one-liner when prose file is used: *voice/industry not auto-injected — agent/skill must have loaded them* (honesty, not behavior change).

**Exit gate:** Skill text matches CANON reading contract. No golden impact.

---

### Phase D — Industry downweight honesty (choose one path)

**Path D1 (recommended for this re-anchor):** Document stubs as stubs in `WHAT_ACTUALLY_RUNS.md` + `signals.py` comment block. List which conditions actually fire (`ecat_minority` only) vs stubbed.

**Path D2 (only if owner wants code in this pass):** Wire profile-backed conditions that already have reliable fields; leave seasonal stub until profile schema supports it. Requires regression full run + possible golden re-baseline → **owner gate**.

Default = **D1**.

---

### Phase E — Explicitly DEFERRED (do not start without a new brief)

| Item | Why deferred |
|------|----------------|
| Split `query_library_v2.md` into `query_library_LIVE.md` + backlog | High breakage risk (`cache._CANON_DOCS`); weeks of SQL provenance in one file |
| Implement RS-01 prior-year column | Track D already flagged; changes §6 YoY semantics → golden |
| Enable industry seasonal/buyer-type downweights for real | Needs profile schema + golden re-check |
| Merge Q-PROV-00 SQL into Q-ECON-00 or delete Q-PROV-00 | Doctrine archaeology; not needed for operator clarity |
| Port 3.0 deploy clients wholesale | Out of scope |

---

## 3. Verification protocol (every phase)

```bash
cd "Insightful Product 4.0"
./regression.sh --verify          # after doc-only phases
# After ANY python/template/skill-adjacent change that could touch render:
./regression.sh                   # full re-run vs v9 cores
```

Also:

- `rg` stale-ID checklist post Phase B
- Spot-read one SHIP HTML (sarreid) for voice regressions only if prose path touched
- Confirm `pipeline/cache.py` `_CANON_DOCS` paths still resolve after any moves (exception layer must stay put)

---

## 4. Execution model — decision

### Recommendation: **This agent owns Phases A–C (+ D1); fresh agent only for mechanical inventory if needed**

| Work | Who | Why |
|------|-----|-----|
| Phase A (capability shelf + CANON) | **This agent** | Needs the weave judgment already loaded; low mechanical risk, high nuance |
| Phase B (spine / stale IDs) | **This agent** | Easy for a fresh agent to “fix” BACKLOG SQL that must stay; nuance is the whole point |
| Phase C (skill + README) | **This agent** | Small surface; already audited |
| Phase D1 (honesty) | **This agent** | Trivial |
| Phase D2 / E | Fresh agent **only after** a new micro-brief | Separate risk class |
| Final review | **This agent** (or second pass by fresh reviewer with this plan as rubric) | Weeks of investment → review against §0 freeze + exit gates |

### Why not “fresh agent does everything, then review”

1. Fresh context will re-ingest ~520KB of VM catalog + library and recreate the same overload.
2. Highest risk is **well-intentioned “cleanup”** of Q-PROV-00 / FULL / BACKLOG that looks like contradiction but is intentional dual-layer history.
3. This session already holds the distinction between *doctrine ancestor* and *LIVE gate* — that distinction is the product of the audit.

### Why not “this agent does a single mega-PR”

Context overload is real. Execute **one phase → verify → stop for owner skim** rather than A–E in one blast. Perfect beats fast.

### Overload self-check (honest)

- **Enough skill/context for A–C + D1:** yes.
- **Enough for splitting the query library or RS-01 SQL:** no — needs a fresh micro-brief and golden re-baseline authority.
- **Fresh agent value:** optional Phase B *inventory* (“list every non-LIVE Q-ID claimed as runtime in report_product”) then this agent applies edits.

---

## 5. Suggested owner approval checklist

Reply with which to run:

- [x] **Go A** — capability shelf + CANON (recommended first)
- [x] **Go A+B+C+D1** — full re-anchor as scoped (recommended package) — **DONE 2026-07-13**
- [ ] **Include D2** — wire real industry downweights (accept possible golden re-baseline)
- [ ] **Include E (LIVE SQL split)** — separate project; not in this package
- [ ] **Fresh agent inventory only** — then this agent edits

**Executed:** A+B+C+D1. See `CHANGELOG.md` 2026-07-13 re-anchor entry.

**Pre-existing note:** sarreid golden HTML (07-02) was overwritten earlier on 2026-07-13
before this package; cci/da/clc verify green. Owner decision needed to re-freeze sarreid.
