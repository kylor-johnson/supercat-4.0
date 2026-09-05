# Wave 1.2 — Authoring Prompt for `_root/01_why_we_are_migrating.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/01_why_we_are_migrating.md` (replace stub contents)
> **Estimated authored length**: 200–300 lines
> **Dependency**: This prompt is **independent** of any other root doc. Author whenever the operator paste this prompt.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is intentional and protective. Your independence is what makes your output trustworthy. Your job is to author **one file** — `Pricing Migration/_root/01_why_we_are_migrating.md` — using only the materials this prompt directs you to.

You will not improvise. If anything is unclear, stop and ask the operator. Do not invent rules. Do not add scope.

---

## Step 1: Required reading (in this exact order)

Read each file completely. Echo every file path + last-updated date (and section IDs where called out below) in your first chat response so the operator can verify you've read them.

### Folder orientation (mandatory)
1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` (read in full — it tells you what you can and cannot do)
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` (the stub you're about to replace — read so you understand the "owns / does not own" boundary)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` (a stub; read to understand how this doc fits the index)

### Primary content sources (mandatory)
6. **The execution plan, v3.3** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_reference/2026-05-20__execution_plan_v3.3.md`. **Read these sections in full**: §I (Strategic Frame — contains the v3 thesis, "The Migration in One Sentence" with the 107-account migration-pending count and +$32,653/mo uplift, AND the Four Operating Principles at sub-section "Four Operating Principles" — these are what you quote verbatim in Section 3), §IV (Execution Architecture: Billing-Cycle-Anchored Monthly Cohorts — the June/July/Deferred cohort framing for the "done" definition; per-cohort details live in `_root/02`), §IX (Metrics & Success Criteria — for the metric thresholds), and §"What Changed from v2 → v3.1 → v3.2 → v3.3" (to understand the evolution of the plan).

### Inlined foundation excerpt (read here, in this prompt — do not seek out the source file)

The next section is verbatim from `~/Downloads/foundation 2/03_how_we_make_money.md` §"Five problems the legacy economics create" (the stamped reference, decision D-000a, stamped 2026-01-28). This is the foundation excerpt you will integrate into the authored doc. **You may quote, paraphrase for the migration-comms register, or condense — but you may not invent additional problems or omit any of the five.**

> **— BEGIN FOUNDATION EXCERPT (foundation 2 / 03_how_we_make_money.md §Five problems the legacy economics create) —**
>
> 1. **Per-user value metric is poorly executed.** The metric is right (value scales with selling teams), but the 25-user included base doesn't map to actual usage patterns, there's no volume incentive (the 26th user costs the same as the 200th), and arrears billing creates unpredictable customer bills.
> 2. **Per-module pricing has no expansion gravity.** Every module is $295–$395 with no tier logic, no bundle pricing, no aspirational upgrade path. Expansion is event-driven (customer needs a feature) rather than aspiration-driven (customer wants the next tier).
> 3. **Legacy pricing creates structural inequity.** Years of grandfathered rates and one-off discounts have spread the book from **56% below book to 42% above book** for equivalent value. This is not a handful of exceptions — it's the structural norm. Custom iPad bases as low as $350 (vs. $725 book), discounted user rates ($15–$22 vs. $25 book), bundled/free modules, and up to 100 provided users (vs. 25 standard).
> 4. **Implementation fees are front-loaded and disconnected from data readiness.** Fixed upfront fees regardless of whether the customer's data is pristine or requires extensive cleaning. Simple implementations subsidize complex ones; SuperCat likely undercharges data-heavy implementations.
> 5. **Support is unmonetized and uniform.** No tiered SLAs, no premium pathway. High-touch accounts consume disproportionate CS resources with no revenue offset.
>
> **— END FOUNDATION EXCERPT —**

### Inlined foundation excerpt (migration philosophy)

> **— BEGIN FOUNDATION EXCERPT (foundation 2 / 03_how_we_make_money.md §How the migration works) —**
>
> The 2026 refresh is not a flag-day repricing. The migration is **per-account, value-anchored, and timeline-bounded**, with the explicit goal of correcting legacy inequity without triggering involuntary churn.
>
> There is a **5-account locked-pricing / in-implementation cohort** with contracted "true ARR" not reflected in the Q425 baseline. These are exceptions in the migration plan, not part of the default motion.
>
> **ACV (Average Contract Value)** is the primary success metric for the refresh (D-000b — stamped 2026-01-28). Two lightweight guardrails are watched but not formally instrumented:
> - **Gross retention**: If accounts churn citing pricing, pause and reassess migration pacing.
> - **Win rate**: If new-business close rates deteriorate, the issue is messaging or price calibration — not architecture.
>
> These are check-engine lights, not KPIs.
>
> **— END FOUNDATION EXCERPT —**

### Do NOT read
- `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/**` — per `_root/CONTRACTS.md` §4. The archive is OFF-LIMITS for this task.
- `~/Downloads/foundation 2/**` — the operative excerpts are inlined above. You do not need the rest of foundation 2 for this doc.
- Any other root-doc stub beyond the ones listed above — your scope is `_root/01`. Other stubs are being authored by other agents in parallel and reading them risks scope-creep.

---

## Step 2: What you are authoring

`_root/01_why_we_are_migrating.md` is the **migration thesis**. It is the doc an operator hands to a new salesperson, a board member, or a fresh CS hire who asks "why are we doing this?" It is also the doc a draft-authoring agent reads to understand WHY a customer is getting a notice — so that voice, framing, and choice of driver all flow from a shared thesis.

The doc owns exactly five things. Author each as its own top-level section in this order:

### Section 1 — The thesis (one paragraph, ~120 words)

Open with: why we're migrating at all. Synthesize from exec plan §I + foundation/03 excerpts. Lead with the structural reality (years of custom deals → 56% below to 42% above book for equivalent value), name the asymmetry (this is the structural norm, not the exception), and state the migration's purpose: **establish a defensible price book; correct legacy inequity systematically; preserve the relationships that justify the embedded position.** Do not hedge. Do not promise pricing won't change in the future. This doc is internal — agents and operators read it. Customers never see this doc.

### Section 2 — The five structural problems being solved

Render the inlined foundation excerpt above as a numbered list — preserve all five, in order, with the stamped substance (56–42% spread; bare numbers like 25-user base, $295–$395 module pricing). You may tighten language. You may not add a sixth problem. You may not soften the structural-inequity framing.

End the section with a one-sentence bridge: "The migration is the operational response to these five problems. The remaining sections of this doc describe what 'response' means."

### Section 3 — The four operating principles (verbatim from exec plan §I, sub-section "Four Operating Principles")

Render the four operating principles **verbatim** from the execution plan v3.3 §I sub-section "Four Operating Principles" (around line 39 of the plan). These are the principles the entire communication system is built on; every voice rule in `_root/04` and every driver framing in `_root/05` traces back to one of these four. Inlining them here makes that traceability legible.

The four principles are titled:
  1. Empathetic in communication, fast on notice, firm on architecture.
  2. Migration starts when compliant written notice is received.
  3. Architecture-forward. Don't hide behind "standardization."
  4. Artifacts over meetings.

After the list, add a one-paragraph "How these show up in communications" note that maps each principle to one concrete communications consequence (e.g. "Empathetic in communication → the per-customer brief is the artifact, not a generic email blast. See `_root/04`."). One sentence per principle. **No other content** — the rules themselves live in `_root/04`/`_root/05`/`_root/06`.

### Section 4 — Success metrics and the definition of "done"

Pull the success-metric thresholds from exec plan §IX. State explicitly:
- **Primary metric**: ACV uplift (per the stamped foundation decision D-000b — cite as "stamped in foundation/03").
- **Migration-induced logo churn cap**: ≤6 accounts.
- **Migration-induced MRR churn cap**: ≤$3,000/mo.
- **Entity-conversation feedback**: synthesized before July cohort launch.
- **Strategic account resolution**: each Strategic account is either migrated, on an approved transition path, or has its churn documented as intentional.
- **Annual-account notice timing**: 100% noticed ≥90 days before renewal (for renewals inside the plan horizon).

Then define "done" in one paragraph: the migration is complete when the 107-account migration-pending book is on the new price card (or has been intentionally churned per the caps), the per-account corrections to the v6.2 dataset have been incorporated, and the June/July/Deferred cohorts have all executed their last comm action per `migration_comm_tiers_2026-05-19.csv`. (Note for the agent: the exec plan v3.3 §I distinguishes 109 mapped accounts from 107 migration-pending; the 2 non-pending accounts plus the foundation's 5-account locked-pricing cohort are reconciled in `_root/02`, not here.)

### Section 5 — What "communication" means inside this migration (the principle that gates all other root docs)

One short section (~150 words) that establishes the philosophical position the rest of the `_root/` stack operationalizes. Make these points:

- Every comm artifact is a **per-account** artifact. There is no "blast." The artifact is engineered to that customer's pricing, drivers, health, and tenure.
- Voice is **always** opening-relationship-before-price, never the inverse. Tone is professional, declarative, empathetic on impact, firm on architecture — not friendly-personal, not legalistic-cold.
- The migration is a moment where SuperCat earns the right to its embedded position by communicating with intent and craft, not where it merely informs. The artifact is the case.
- The 60-day notice window is non-negotiable architecture; the framing inside the window is fully flexible per-customer.

End by pointing forward: "How that philosophy becomes operational rules lives in `_root/04` (voice), `_root/05` (drivers), `_root/06` (format routing), and `_root/08` (quality bar)."

### Header block

Match the pattern in the other root-doc stubs:
- `> **Last updated**: 2026-05-22`
- `> **Owner**: CEO`
- `> **Primary sources**: `_reference/2026-05-20__execution_plan_v3.3.md` §I, §IV, §IX; foundation `03_how_we_make_money.md` (inlined excerpts in this doc; see §2 and §4)`
- `> **What this doc owns**: <fill in based on above>`
- `> **What this doc DOES NOT own**: voice/tone (`_root/04`); driver framing (`_root/05`); segment/format mapping (`_root/02` + `_root/06`); data fields (`_root/07`); quality checks (`_root/08`).`

---

## Step 3: What this doc must NOT contain

The most common drift failure is a doc that wanders into ownership owned by another doc. Be vigilant.

- **No voice rules.** No "say X instead of Y." No forbidden-phrase list. Those belong to `_root/04`.
- **No driver framing.** No "for URN customers, lead with…". That belongs to `_root/05`.
- **No segment definitions.** "What is a Watch account?" belongs to `_root/02`.
- **No format mapping.** "Which segment gets Format A vs. CEO Letter?" belongs to `_root/06`.
- **No tier-feature descriptions.** "T1 = Catalog Essentials includes…" belongs to `_root/03`.
- **No data-pipeline mechanics.** "Load v6.2 CSV first, then…" belongs to `_root/07`.
- **No quality checklist.** "Verify the lede stat is ARR not MRR" belongs to `_root/08`.

If you find yourself writing toward any of those topics, stop and remove. Reference the owning doc with a pointer ("see `_root/04`") and move on.

---

## Step 4: Voice and format constraints

- Register: operator-facing, declarative, no marketing language, no hedging. Same register as `AGENTS.md` and `00_README.md`.
- Sentences should be short and structural. Avoid "Importantly," "Critically," "It is worth noting that…"
- Use **bold** sparingly — only for the named principles, the metric labels, and the structural-inequity numbers.
- Use Markdown headers (## for sections 1–5, ### for sub-elements where useful).
- Inline references to other root docs use the pattern: `` `_root/04` `` or `` `_root/04_communication_posture.md` §<section-name> `` (the latter when pointing to a specific rule).
- No emojis.

---

## Step 5: Output

Replace the entire current contents of `Pricing Migration/_root/01_why_we_are_migrating.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/01_why_we_are_migrating.md (replaced stub)
Files read:
  - Pricing Migration/AGENTS.md (last-updated: <date>)
  - Pricing Migration/00_README.md (last-updated: <date>)
  - Pricing Migration/_root/CONTRACTS.md (last-updated: <date>)
  - Pricing Migration/_root/01_why_we_are_migrating.md [stub] (last-updated: <date>)
  - Pricing Migration/_root/00_manifest.md [stub] (last-updated: <date>)
  - Pricing Migration/_reference/2026-05-20__execution_plan_v3.3.md (last-updated per its header: <date>) — sections read: I, III, IV, IX, "What Changed v2 → v3.3"
  - Inlined foundation excerpts: foundation 2/03_how_we_make_money.md §"Five problems" + §"How the migration works" (delivered in this prompt; original last-updated 2026-05-12 per excerpt provenance)
Files NOT read: Pricing Migration/_archive/**, ~/Downloads/foundation 2/** (per CONTRACTS §4 and this prompt's scope)
Self-audit — sections this doc touched on that are NOT in its ownership:
  - <list with location + suggested move, or "none">
Self-audit — rules from other root docs that I restated rather than referenced:
  - <list with location, or "none">
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. The operator will paste your output back to the planning agent for review before the next wave begins.

---

## Step 6: If something is missing

If a section the prompt asks you to author cannot be supported by the materials in Step 1, stop and tell the operator exactly what is missing and which source you expected to find it in. Do not synthesize. Do not approximate. The cost of asking is one round-trip; the cost of inventing a metric or principle is a downstream draft that's structurally wrong.
