# Wave 3.2 — Authoring Prompt for `_root/06_format_routing.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/06_format_routing.md` (replace stub contents)
> **Estimated authored length**: 250–400 lines (focused routing-logic doc)
> **Dependency**: Wave 2.1 complete (`_root/02` authored). Independent of Wave 3.1 — can run in parallel.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `_root/06_format_routing.md` is the canonical routing-logic doc — it answers the question "given a v6.2 row, which brief format does this account get?" It is what every Stage 4 drafter consults first, and what the comm_action audit script checks against.

Your job is to **extract, consolidate, and crisply state** every routing rule that today lives across three sources (archived `_handoff-prompt.md`, the routing CSV, and exec plan v3.3) — in one place, with no duplication and no invention. The 5 known routing-CSV errata are owned by `_root/02 §7`; you reference them by pointer here and state how they affect format selection.

You will not invent new routing rules. You will not collapse a rule (e.g. an At-Risk override) into something simpler. You will extract what exists and render it precisely.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date in your first chat response.

### Folder orientation (mandatory — echo in conformance block)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/06_format_routing.md` (the stub you're replacing)

### Already-authored root docs (your dependencies — read in full)

5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — the segment + ownership-boundary + overlay logic that gates format selection. Read §1 (segments), §2 (the $200/$400/$600 ownership boundary), §3 (entity overlay), §4 (health overrides), §5 (annual overlay), §6 (cohort assignment), §7 (the 5 routing-CSV errata), §8 (109/107/2 reconciliation).
6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — read §4.12 (close variants by format) and §4.13 (health-band lede overrides). These define how each format closes and how health overrides change the lede; they are voice rules, but they are also the operational fingerprint of "what is a CEO Letter" vs. "what is a Format B."
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — read §1 (source hierarchy), §2 (column field guide for `comm_action`, `migration_segment`, `delta_mrr`, `health_band`, `deal_type`, `parent_entity`, `notice_cohort` and the other routing-relevant fields), §6 (file naming + output folder per format), §7 (the per-format routing-block matrix).
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — read §1 (tier definitions). Tier-to-format correspondence is informational only (tier and format are independent dimensions), but you'll want it to recognize that "T1 with delta +$50" routes the same as "T3 with delta +$50" — the format dispatches on delta, not on tier.

### Reference documents (read targeted sections only)

9. **Exec plan v3.3** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_reference/2026-05-20__execution_plan_v3.3.md`. Read **only** §IV (notice cohorts), §V (segment-by-segment playbooks — only the per-segment "comm_action" calls), §VI (health overrides as they affect format), §IX (timeline / dependencies). Do not read the rest — out of scope.

10. **Routing CSV** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/migration_comm_tiers_2026-05-19.csv`. Open it; document the columns (header row); document the distinct `comm_action` values that appear. **Do not paste row-level data into the authored doc** — the CSV is the data, this doc is the rules.

### Primary content sources — the pre-refactor archive (this prompt EXPLICITLY AUTHORIZES reading these despite the general anti-archive rule in `_root/CONTRACTS.md` §4)

11. **Handoff §Format Routing Rules + §Driver Framing health/annual modifiers** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md`. Read **only**:
    - §"Format Routing Rules" (lines ~192–203) — the delta-threshold routing table
    - §"Driver Framing" (lines ~172–188) — only the health/annual modifier paragraphs at the bottom of that section (these are routing modifiers, not driver content)
    - §"Data Corrections" (lines ~95–135) — the 5 routing-CSV errata (these are also in `_root/02 §7`; you cross-reference)
    Do not read the rest of the handoff — voice rules belong to `_root/04`, driver content belongs to `_root/05`.

12. **Format brief templates — only the operator-notes / when-to-use headers, NOT the body prose** — read just the front-matter of each, to confirm what each format IS in plain English:
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md` (first 25 lines)
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md` (first 30 lines)
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md` (first 30 lines — note: explicit `Watch health flag` rule for Good News)
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` (first 30 lines)

### Do NOT read

- The bodies of the brief templates (the per-driver `**DRIVER:` blocks) — those belong to `_root/05`; reading them here is scope creep.
- Any per-account exemplar brief — out of scope; routing is a CSV-level / segment-level / Δ-level decision, not a per-account voice decision.
- `~/Downloads/**` or anything outside the `Pricing Migration/` and `Migration-Health Artifacts/` folders.
- Other `_root/` stubs (00, 05, 08, 09) — those are stubs or under another wave.

---

## Step 2: Authoritative routing inventory (use these — do not re-derive)

The planning agent ran a definitive count against the deduped `_master-account-data-v6.2.csv` on 2026-05-22. The pipeline operates on **107 migration-pending accounts** (plus 2 already-migrated that are excluded by the loader per `_root/07 §3`). Segment + cohort + delta distribution:

| Segment | Accounts | Avg Δ MRR | Default format per segment | Notes |
|---|---:|---:|---|---|
| Tailwind | 6 | −$136 | Good-News Notice | All decreases. |
| Core | 13 | +$105 | Format A | $0 < Δ ≤ $200, healthy, standalone. |
| Narrative | 15 | +$311 | Format B | $201 ≤ Δ ≤ $400, healthy, standalone. |
| Executive | 8 | +$485 | CEO Letter + Call Commitment | $401 ≤ Δ ≤ $600, healthy, standalone. CEO co-author. |
| Pre-Engagement | 8 | +$692 | CEO Pre-Call → Format B (Δ ≥ $600) | CEO-initiated call BEFORE notice. |
| Entity | 27 | +$404 | Entity packet (combines per-child briefs) | Routes via parent treatment regardless of child Δ. |
| Strategic | 19 | +$253 | Deferred / post-migration; CEO-led | Health or VD override; format selection depends on post-stabilization assessment. |
| Annual | 11 | +$211 | Variant matches natural segment | Timing changes, not format substance. |

**Routing decision flow** (the order of evaluation is itself a rule):

1. **Status filter**: skip rows where `migration_status = 'already_migrated'` (already-migrated → no notice) or `ghost_account = TRUE` (placeholder → no notice). Filter happens at the loader (`_root/07 §3`).
2. **Decrease check**: if `delta_mrr < 0` → Good-News Notice. Health-band override applies (see §3 of your authored doc).
3. **Entity overlay**: if `parent_entity` is non-empty AND `parent_entity != company` → Entity packet (routes through parent's coordinated treatment regardless of child Δ).
4. **Annual overlay**: if `deal_type = 'Annual'` → timing changes (90-day notice clock per §5 of `_root/02`); format substance matches the natural segment.
5. **Health override**: if `value_delivery_score < 40` OR `health_band ∈ {Watch, At Risk, Critical}` → Strategic segment, CEO-led conversation precedes any notice. Watch-band lede override applies (`_root/04 §4.13`).
6. **Delta tier dispatch** (only if no override has fired): the dollar-threshold table that maps Δ to format.

The order matters: the entity overlay supersedes Δ-tier dispatch; the health override supersedes both; the annual overlay supersedes timing but not substance.

**Use this inventory as-is.** Do not silently revise. If you believe it's wrong, flag in your conformance block.

---

## Step 3: What you are authoring

`_root/06_format_routing.md` is the single source of truth for **format selection** in the migration communications system. Author the doc as the following sections, in this order:

### Section 1 — The 4 brief formats + 1 routing pattern

Open with a `##` section that names and one-paragraph-defines each of:

- **Format A — 60-Day Notice** (CS-led, near-flat delta, ≤10% or ≤$80, low touch)
- **Format B — Notice + Meeting** (CS-led, meaningful delta, $81–$399, CSM offers a meeting in the close)
- **CEO Letter + Call Commitment** ($400–$599, CEO sign-off, specific date commitment per `_root/04 §4.12`)
- **Good News Notice** (price decrease — 200–300 words, CS team sends, no CEO involvement)
- **CEO Pre-Call → Format B** (the ≥$600 routing pattern — CEO calls FIRST, then a Format B notice goes out)

For each, name: what it is in 1–2 sentences, who sends, what's distinctive about the close, what the output-folder name is (per `_root/07 §6`), and one cross-reference to `_root/04 §4.12` for the verbatim close language. **Do not restate the close text** — `_root/04` owns it.

### Section 2 — The routing-decision flow (the order of evaluation)

State the 6-step decision flow from Step 2 above. Numbered list. Each step is a rule with a one-sentence rationale and a pointer to the canonical owning doc:

1. Status filter (already_migrated / ghost_account) → `_root/07 §3`
2. Decrease check (delta_mrr < 0 → Good News) → here
3. Entity overlay → `_root/02 §3`
4. Annual overlay → `_root/02 §5`
5. Health override (VD<40 or Watch-or-worse → Strategic) → `_root/02 §4`
6. Delta-tier dispatch → §3 of this doc

The order matters; render it as a numbered list, not a table, so it reads as a flow.

### Section 3 — Delta-tier dispatch table (the headline routing rule)

The dollar-threshold table that maps a healthy, standalone, monthly account's Δ MRR to a format. Source = `_handoff-prompt.md` §Format Routing Rules + exec plan v3.3 §IV/§VI.

| Condition (on Δ MRR per month) | Format | Owner | Notes |
|---|---|---|---|
| Δ < $0 (any decrease) | Good-News Notice | CS team | See §health override — Watch/At Risk Good News holds for health check-in. |
| 0 < Δ ≤ $80 OR Δ_pct ≤ 10% | Format A — 60-Day Notice | CS (Kylor) | Near-flat. Pre-engagement bypass on Δ_pct: an account with Δ_pct ≤ 10% but Δ ≥ $600 still routes to CEO Pre-Call → Format B per the ≥$600 rule (delta_mrr threshold supersedes delta_pct). |
| $81 ≤ Δ ≤ $399 | Format B — Notice + Meeting | CS (Kylor) | Includes CSM meeting offer in close. |
| $400 ≤ Δ ≤ $599 | CEO Letter + Call Commitment | CEO + CS | CEO authors / signs; CS executes delivery. Specific call date within 5 business days of send (`_root/04 §4.12`). |
| Δ ≥ $600 | CEO Pre-Call → Format B | CEO + CS | CEO calls FIRST. Format B notice follows the call. |

Add a one-paragraph note immediately after the table covering the **delta_pct vs delta_mrr precedence** rule (whichever produces the more rigorous format wins — i.e. an account at Δ = $75 / Δ_pct = 12% routes as Format B because 12% > 10%, even though $75 < $80). Source = `_handoff-prompt.md` §Format Routing Rules. If the handoff is ambiguous on the rule, surface as flag.

### Section 4 — Override rules (the things that SUPERSEDE delta-tier dispatch)

Three subsections, one per override. For each:

- **Trigger** (the v6.2 column condition that fires)
- **What it does to format selection** (specific format substitution or routing change)
- **What it does to timing** (cohort window, send order)
- **Voice consequence** (one sentence — points to `_root/04` for detail)
- **Owning doc for the rule itself** (cite `_root/02` §-number)

The three overrides:

#### §4.1 — Entity overlay

A row is an Entity child iff `parent_entity` is non-empty AND `parent_entity != company`. When fired: the child does NOT receive a standalone brief; it is folded into the entity packet (one coordinated artifact covering all child brands under the parent). Format substance: the packet uses the entity-packet template (Stage 3 output — does not yet exist in the archive; flag as future work in `_meta/stage3_cleanup.md`). Format selection per-child is suppressed; the entity packet is the format. Cross-reference: `_root/02 §3`.

#### §4.2 — Health override (VD<40 OR Watch-or-worse)

When fired: account routes to Strategic segment regardless of Δ. The notice itself is deferred until a CEO-led conversation has stabilized the relationship. Format selection at notice time depends on the post-stabilization Δ tier and the operator's assessment of the relationship state. The Watch-band lede override (`_root/04 §4.13`) replaces the relationship-stats lede with a standalone dollar-change sentence. Cross-reference: `_root/02 §4`.

**Format-A-vs-Good-News interaction**: per the archived Good News template's front-matter, an account that would otherwise route to Good News but has `health_band ∈ {Watch, At Risk, Critical}` **does NOT send Good News** — it routes through the CSM for a health check-in first. State this as a rule; cite the Good News template's `Watch health flag` operator note.

**At-Risk handling flag**: the archived `_handoff-prompt.md` §Format Routing Rules says "At Risk → do not draft migration notice." But `_root/02 §4` says At-Risk routes to Strategic where the notice is eventually drafted post-relationship-stabilization. Surface this as a conflict — possibly the handoff means "do not draft a notice in the standard cohort" (i.e. defer until post-stabilization), in which case it agrees with `_root/02`; possibly it means "never draft a notice at all," which conflicts with `_root/02`. Operator resolution needed.

#### §4.3 — Annual overlay

Trigger: `deal_type = 'Annual'`. When fired: a contractual ≥90-day notice window applies (60-day legal minimum + 30-day buffer per exec plan v3.3 §III). The format substance still matches the account's natural Δ-tier; the overlay changes **timing** only. Annual accounts are batched into the `notice_cohort = 'Renewal-Based'` cohort (v6.2 column) and fast-tracked individually if renewal is <90 days from today. Cross-reference: `_root/02 §5`.

### Section 5 — comm_action vocabulary (the routing CSV's column)

The `migration_comm_tiers_2026-05-19.csv` carries a `comm_action` column whose values are the authoritative format-selection per account. Author a table listing every distinct `comm_action` value that appears in the CSV, with its corresponding format. (Read the CSV and enumerate the values; do not invent.)

Expected `comm_action` values per archived `_handoff-prompt.md` (verify against CSV):

- `60-Day Notice` → Format A
- `Notice + Meeting` → Format B
- `CEO Letter + Call Commitment` → CEO Letter
- `Good-News Notice` → Good News
- `CEO Pre-Call → Format B` → CEO Pre-Call → Format B
- (Possibly others — enumerate what you find; the routing CSV is authoritative.)

If a `comm_action` value appears in the CSV that doesn't appear in the handoff or exec plan v3.3, flag it.

### Section 6 — The 5 known routing-CSV errata (cross-reference, do NOT restate)

A short section that cross-references `_root/02 §7` (which owns the errata list) and explains how the errata interact with the routing CSV:

- The errata are NOT yet baked into `migration_comm_tiers_2026-05-19.csv`.
- Until they are (cleanup item `CL-000` per `_meta/stage3_cleanup.md`), every routing decision cross-checks against the errata list in `_root/02 §7`.
- The corrected `comm_action` value (per the errata) wins over the CSV value.
- Restate the 5 ord_ids (rac, wac, sbl, big, kl) and the corrected actions in a small table so this doc is self-sufficient for the operator at brief-drafting time, BUT include an explicit pointer that `_root/02 §7` is the canonical source and any future edits go there.

### Section 7 — Output folder mapping (cross-reference, do NOT restate)

A short section that points to `_root/07 §6` for the per-format output-folder table. Restate the 4 main folder paths (`format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`) for self-sufficiency; note that the CEO Pre-Call → Format B output writes to `format-b-notices/` with a CEO-awareness flag in the routing block (per `_root/07 §7`).

### Section 8 — What this doc does NOT own (closing reminder)

A short closing section listing what `_root/06` does NOT own:

- Segment definitions, account counts, ownership boundaries, the 5 errata list itself → `_root/02`
- Voice / tone rules for each format's lede and close → `_root/04` (especially §4.12, §4.13)
- The "Why the Number Is Changing" per-driver prose that goes into the brief body → `_root/05`
- The verbatim "What You're Getting at $X" tier blocks → `_root/03`
- v6.2 column meanings, the loader, the routing-block field list, the file-naming convention → `_root/07`
- The pre-send quality checklist → `_root/08` (Wave 4)

### Header block (match the pattern in other root docs)

```
# 06 — Format Routing

> **What this doc owns**: <populate from your final section list>
>
> **What this doc DOES NOT own**: <populate>
>
> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: `_root/02` (segments + overlays + errata); `_root/07` (comm_action column + output folders + routing-block matrix); archived `_handoff-prompt.md` §Format Routing Rules + §Data Corrections; `migration_comm_tiers_2026-05-19.csv` (header + distinct comm_action values); exec plan v3.3 §IV / §V / §VI
> **Supersedes**: format-routing rules previously scattered across the handoff + the routing CSV's implicit logic. After this doc lands, every Stage 4 drafter consults _root/06 to determine format, then references _root/02 for overlay confirmation, then opens _root/05 for body content.
```

---

## Step 4: Anti-drift discipline

- **Every routing rule lives in exactly one §-section.** §3 (delta-tier dispatch) does not restate §4 (overrides). §4 references §3 by "the override supersedes the §3 table."
- **The 5 errata are cross-referenced, never restated as new rules.** `_root/02 §7` owns the list; if you restate them here for self-sufficiency, mark the restatement as a mirror with a single-source-of-truth pointer.
- **Voice rules are referenced, not restated.** `_root/04 §4.12` owns close text; `_root/04 §4.13` owns health-band lede overrides; you reference, you do not paste.
- **Pipeline mechanics are referenced, not restated.** `_root/07 §3` owns the loader filter; `_root/07 §6` owns output folders; `_root/07 §7` owns routing-block content. You reference, you do not paste.
- **Asking is cheap. Inventing is the drift vector.** If the handoff's §Format Routing Rules and the exec plan v3.3 §IV disagree (e.g. on the delta_mrr boundaries — handoff says ≤$80, exec plan may say ≤$100), flag the conflict — do not pick one.

---

## Step 5: Voice and format constraints

- Register: operator-facing, declarative, no marketing language. Same register as `_root/02`, `_root/04`, and `_root/07`.
- Use clean Markdown structure: `##` for the 8 sections, `###` for subsections inside §4 (the three overrides), tables where appropriate.
- Numbered lists for the routing-decision flow (§2) and the override list.
- No emoji. No "Importantly" / "Critically" — section ordering signals importance.

---

## Step 6: Output

Replace the entire current contents of `Pricing Migration/_root/06_format_routing.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/06_format_routing.md (replaced stub)
Files read: <enumerate every file path from Step 1 with last-updated date or mtime>
Explicitly-authorized archive reads: <list the archived sections + template front-matter you read>
Files NOT read: <enumerate per Step 1 "Do NOT read" + any others>

Formats authored (Section 1): <count + names — should be 4 brief formats + 1 routing pattern>
Routing rules authored (Section 3): <count — should match the delta-tier table rows>
Overrides authored (Section 4): 3 (entity, health, annual)
comm_action values enumerated from CSV (Section 5): <count + list>
Errata cross-referenced from _root/02 §7 (Section 6): 5 (rac, wac, sbl, big, kl)

Conflicts between sources (handoff vs. exec plan v3.3 vs. routing CSV vs. _root/02) — and my chosen resolution / flag:
- <list, or "none">

Gaps surfaced (a routing condition that has no rule, or a rule that has no v6.2 backing):
- <list, or "none">

Open questions for operator:
- <list, or "none — including the At-Risk handling flag from §4.2 if you resolved it>
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. The operator will paste your output back to the planning agent for review before Wave 4.

---

## Step 7: If something is missing or contradictory

- A routing rule in `_handoff-prompt.md` that's not in exec plan v3.3 (or vice versa) → flag both versions.
- A `comm_action` value in the routing CSV that's not in the handoff or v3.3 → flag.
- The At-Risk handling rule from §4.2 — the conflict between handoff "do not draft migration notice" and `_root/02 §4` "routes to Strategic where notice eventually drafted post-stabilization" — flag with both readings; do not pick one.
- The delta_mrr vs delta_pct precedence rule — if the handoff doesn't state it explicitly, flag and propose the rule "whichever produces the higher-touch format wins" but mark as operator-decision-needed.
- Entity-packet template doesn't exist in the archive — flag as a Stage 3 cleanup item to be added (the planning agent will absorb into `_meta/stage3_cleanup.md`).

**Asking is cheap. Inventing is the drift vector.**
