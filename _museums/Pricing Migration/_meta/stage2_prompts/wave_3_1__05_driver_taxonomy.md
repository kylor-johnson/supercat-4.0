# Wave 3.1 — Authoring Prompt for `_root/05_driver_taxonomy.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/05_driver_taxonomy.md` (replace stub contents)
> **Estimated authored length**: 500–700 lines (this is the high-density narrative-content doc — 11 drivers × 3 format flavors × conditional blocks)
> **Dependency**: Wave 1 complete (`_root/04` authored). Independent of Wave 3.2 — can run in parallel.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `_root/05_driver_taxonomy.md` is the canonical "Why the Number Is Changing" content layer of the system — every per-account brief's body prose draws from here. Your job is to **extract, consolidate, and crisply state** every per-driver narrative block (and its conditional logic) that has accumulated across the pre-refactor templates, in one place, with no duplication and zero invention.

You will not invent driver framings. You will not fill perceived gaps with new prose. You will extract the prose that exists in the archived templates, deduplicate it across formats, render the canonical version, and flag every conflict or missing piece for the operator.

The voice rules that govern HOW these blocks read are owned by `_root/04`. This doc owns WHAT each block says. References to `_root/04 §X.Y` are how you point at voice rules; you do not restate them here.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date in your first chat response so the operator can verify.

### Folder orientation (mandatory — echo in conformance block)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/05_driver_taxonomy.md` (the stub you're replacing — read the "owns / does not own" boundary)

### Already-authored root docs (your dependencies — read in full)

5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — every voice rule. Especially §4.1 (relationship-before-price), §4.5 (only-thing-changing line + IUR fork), §4.6 (platform-base-grown sentence — verbatim), §4.7 (early-adopter tenure paragraph — verbatim), §4.9 (billing-basis footnote — verbatim), §4.10 (platform-base conditional inside URN block), §4.14 (discount-correction posture). Note that §5 (driver-voice orientation) is the one-paragraph forward pointer to THIS doc — your job is to make that pointer land cleanly.
6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — tier definitions and verbatim "What You're Getting at $X" blocks. Your driver blocks lead into the tier block; the seam between them needs to be clean.
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — segment definitions; relevant only because some segments tend to cluster around certain drivers (e.g. Pre-Engagement skews to `user_rate_normalization` + high delta). Read §1 only.
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — read §2 (column field guide) for the data fields each driver block consumes (`migration_driver`, `secondary_drivers`, `current_user_rate`, `current_platform_mrr`, `tier_base`, `current_provided_users`, `included_users`, `trailing_avg_users`, etc.). Driver blocks dispatch on these fields — get the names right.

### Primary content sources — the pre-refactor archive (THIS PROMPT EXPLICITLY AUTHORIZES reading these despite the general anti-archive rule in `_root/CONTRACTS.md` §4)

The driver-narrative content you are consolidating lives **inside** the archived brief templates as `**DRIVER: \`<driver_name>\`**` blocks. You will be the last agent to read them — once you've extracted and consolidated, future agents read only `_root/05`.

9. **Handoff §Driver Framing** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md`. Read **only** §"Driver Framing" (lines 172–188) for the operator's one-sentence-per-driver framing intent, AND §"Format Routing Rules" (lines 192–203) for the routing modifiers that gate certain drivers. Do not read the rest of the handoff — the rest belongs to `_root/04` (voice, already consolidated) or `_root/06` (format routing, not your scope).

10. **Format B brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md`. Read **the full file**. This template carries the most complete set of per-driver blocks (lines 44–195: all 8 increase-side drivers). For Wave 3.1 this is your **primary canonical source** for the increase-side driver prose.

11. **CEO Letter brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md`. Read **the full file**. This template carries the CEO-voice variant of all 8 increase-side driver blocks. The CEO voice is peer-to-peer and longer; the Format B voice is structural and tighter. Both variants must be preserved in `_root/05`.

12. **Good News brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md`. Read **the full file**. The Good News template carries the 3 decrease-side mechanic blocks (`module_compression`, `user_count_variance`, `rate_architecture`) — see lines 44–80. These are the Tailwind-segment driver narratives.

13. **Format A brief template (Migration-Health Artifacts era)** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md`. Read **the full file**. Note especially: Format A handles the near-flat / low-delta accounts and its driver blocks are subtly different from Format B's (shorter, less explanation since the delta is small). Where Format A and Format B differ on the SAME driver, both versions must appear in `_root/05` because they're used in different contexts.

### Primary content sources — exemplar briefs (the "voice in practice" reference)

Read these to see the driver blocks instantiated. Where an exemplar's actual prose differs from the canonical template, flag it as a question for the operator — do not invent a reconciliation.

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kal__kalco-allegri-crystal__brief__v2.md` — Format A, `user_rate_normalization`, post-S1–S7 cleanup exemplar.
15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kii__kennedy-international__brief__v2.md` — Format A, `included_user_reduction` exemplar.
16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/ih__interlude-home__brief__v2.md` — Format B, `tier_base_increase` (with secondary IUR) exemplar.
17. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/da__dainolite__brief.md` — CEO Letter, high-delta `user_rate_normalization` + `included_user_reduction` exemplar.
18. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/pf__palecek/option-a__email-with-table.md` — Good News, `module_compression` exemplar.

### Do NOT read

- The rest of `_handoff-prompt.md` outside §Driver Framing + §Format Routing Rules — already consolidated to `_root/04` and `_root/06` (next wave).
- Any other archived brief beyond items 14–18 — you have enough exemplars; reading more risks accreting per-account exceptions into general driver rules.
- `~/Downloads/**` or anything outside the `Pricing Migration/` and `Migration-Health Artifacts/` folders.
- Any other `_root/` stub (00, 06, 08, 09) — those are stubs or under another wave.

---

## Step 2: Authoritative driver inventory (DO NOT re-derive — use this list)

The planning agent ran a definitive count against the deduped `_master-account-data-v6.2.csv` on 2026-05-22. The system carries **11 distinct `migration_driver` values across 109 accounts**:

### Increase-side drivers (101 accounts across 107 pending; the other 6 pending are Tailwind / decrease)

| `migration_driver` | Pending accounts | Notes |
|---|---:|---|
| `user_rate_normalization` | 37 | Most common driver. Per-user rate was locked at signing; moving to the graduated standard ladder. |
| `platform_discount_correction` | 17 | Signing-time discount being retired across all accounts. Triggers the §4.14 lede substitution. |
| `tier_base_increase` | 12 | Platform base moved from old book rate to current tier standard. Tier unchanged, only the rate. |
| `included_user_reduction` | 11 | Legacy expanded user allotment normalizing to current tier standard. Triggers IUR fork in `_root/04 §4.5`, billing-basis footnote `_root/04 §4.9`. |
| `at_book_tier_shift` | 10 | Account already at book rate; minor adjustment. Near-zero delta typical. |
| `multi_org_retirement` | 6 | Multi-organization pricing program being retired; each entity moves to individual standard. |
| `annual_discount_retirement` | 2 | Annual commitment discount being retired; standard monthly rate going forward. |
| `special_arrangement` | 1 | Custom arrangement to standard. Delta-dependent CEO involvement. |

### Decrease-side drivers (6 Tailwind accounts + 1 Annual-segment account with negative delta = 7 decrease accounts)

| `migration_driver` | Pending accounts | Notes |
|---|---:|---|
| `module_compression` | 4 (ml, gc, dccl, pf) | Separate module charges consolidating to a single tier subscription — lower combined rate. Mentioned in `_root/04 §5` driver-voice paragraph. |
| `user_count_variance` | 2 (rw, jyc) | Current billed users above 6-month trailing average; user count being aligned to trailing actuals. **NOT** in `_handoff-prompt.md` §Driver Framing — surface as flag. |
| `rate_architecture` | 1 (mlg — Minka Lighting Group) | Per-user rate was set at legacy structure; recalculated rate produces a lower invoice. **NOT** in `_handoff-prompt.md` §Driver Framing — surface as flag. Account is in Annual segment but has negative delta (−$38/mo). |

### Status-marker driver (anomaly — flag)

| `migration_driver` | Accounts | Notes |
|---|---:|---|
| `already_migrated` | 2 (tcs, drf) | `tcs` CopperSmith (T3 Annual), `drf` Dorell Fabrics (T1). This is a `migration_status` value leaking into the `migration_driver` field. Both rows also carry `migration_status = 'already_migrated'`. Per `_root/07` §3 the loader skips these rows; per `_root/02` §8 they are excluded from the 107 pending count. Surface as flag — `_root/05` should document the anomaly but does not need to author a "driver block" for it. |

### Secondary-driver values seen in v6.2 (pipe-separated in CSV)

The `secondary_drivers` field carries 1–2 pipe-separated driver names. Distinct combinations seen in v6.2:

- `included_user_reduction` alone (21 occurrences)
- `user_rate_normalization` alone (17)
- `user_rate_normalization | included_user_reduction` (7)
- `multi_org_retirement | included_user_reduction` (6)
- `multi_org_retirement | user_rate_normalization` (2)
- `annual_discount_retirement` alone (1)
- `multi_org_retirement` alone (1)

Per `_root/04 §5` and the handoff's §Driver Framing note: "secondary_drivers: add as supporting context within the primary driver block — never a separate section." Your §4 of this doc owns how that integration happens.

**Use this inventory as-is.** Do not re-derive from v6.2; do not extend it; do not collapse `rate_architecture` into `module_compression` or similar. If you believe the inventory is wrong, flag it in your conformance block — do not silently revise.

---

## Step 3: What you are authoring

`_root/05_driver_taxonomy.md` is the canonical source of "Why the Number Is Changing" content. Every per-account brief in Stage 4 will pull its primary driver block (and its secondary-driver weaving) from this doc, verbatim where the template prose is verbatim. Author the doc as the following sections, in this order:

### Section 1 — Driver inventory + the "primary vs. secondary" rule

A short opening section (~150–200 words):

- The 11 driver values that appear in v6.2's `migration_driver` field, grouped as: 8 increase-side + 3 decrease-side. Use the table format from Step 2 above (you may render the table; do not reword the driver names).
- The handoff's "primary is authoritative" rule: per archived `_handoff-prompt.md` §Driver Framing, **always use v6.2 CSV's `migration_driver`; if v6.2 and HTML model disagree, v6.2 wins**. Restate it.
- The `secondary_drivers` rule: secondaries are woven into the primary driver block as supporting context, never as a separate section. Forward-reference §4 for the integration patterns.
- The `already_migrated` anomaly: flag it; explain it's a status-marker leak into the driver field; explain that those rows are filtered upstream (per `_root/07 §3`) so no driver block needs to be authored for them.

### Section 2 — Increase-side drivers (eight subsections)

This is the bulk of the doc. Each driver gets its own `###` subsection. Order: by v6.2 account count, descending — `user_rate_normalization` first (37), `platform_discount_correction` (17), `tier_base_increase` (12), `included_user_reduction` (11), `at_book_tier_shift` (10), `multi_org_retirement` (6), `annual_discount_retirement` (2), `special_arrangement` (1).

For each driver, author the following subsections:

#### §2.X.1 — Definition

One paragraph: what triggers this driver. Use the handoff's "What it means" column language as a baseline; add the v6.2 field signature (which `current_*` and `new_*` fields differ in a way that defines this driver). Cite count.

#### §2.X.2 — Format B canonical block (the structural variant)

The "Why the Number Is Changing" prose for this driver, verbatim from the Format B template (archived `_brief-template.md` §44–195). Include all conditional sub-blocks (`[IF Before platform base ≠ After…]`, `[IF trailing avg users ≤ new included base…]`, etc.) exactly as the template renders them. **Verbatim. Character-for-character. Do not paraphrase.**

#### §2.X.3 — CEO Letter canonical block (the peer-to-peer variant)

The "Why the Number Is Changing" prose for this driver, verbatim from the CEO Letter template (archived `_brief-template.md` §48–214). Where the CEO Letter block diverges from the Format B block (longer, first-person, includes call-commitment language), preserve the divergence. **Verbatim.**

If the CEO Letter template does not carry a block for this driver (e.g. some drivers may only appear in lower-delta formats), say so explicitly and forward-reference Format B.

#### §2.X.4 — Format A canonical block (the near-flat variant)

The "Why the Number Is Changing" prose for this driver as it appears in the Migration-Health Artifacts Format A template, verbatim. Format A blocks are typically shorter (Format A handles delta ≤10% and ≤$80, so the explanation is briefer). Where Format A diverges from Format B, preserve the divergence.

If Format A does not carry a block for this driver, say so — Format A's mechanical scope (low delta, near-flat) means some drivers will never route there (e.g. `multi_org_retirement` produces large deltas).

#### §2.X.5 — Pricing-table row template (the table the brief renders directly below the prose)

The `| | Before | After |` table verbatim from the templates. This is mechanical content (mostly identical across formats with the per-driver row varying), but include it because the brief reads as one connected mechanic — driver prose + table — and Stage 4 drafters will copy both.

#### §2.X.6 — Conditional context paragraphs that follow the block

Some drivers trigger additional paragraphs after the table:

- The billing-basis footnote (§4.9 of `_root/04` — italicized, verbatim) — required after `user_rate_normalization` and `included_user_reduction` tables.
- The platform-base-grown sentence (§4.6 of `_root/04` — verbatim) — required when `new_tier_base > current_platform_mrr` regardless of primary driver.
- The platform-base conditional sentence (§4.10 of `_root/04` — Format B variant + CEO Letter variant) — required when primary driver is `user_rate_normalization` AND Before/After platform bases differ.
- Early-adopter tenure paragraph (§4.7 of `_root/04` — verbatim Format B + verbatim CEO Letter variants) — required when `cohort_year ≤ 2015` regardless of driver.

For each driver subsection, state which of these paragraphs apply and reference `_root/04` for the verbatim text — **do not restate them here**.

#### §2.X.7 — Secondary-driver integration

When this driver appears as primary AND a specific secondary is present, what changes about the block?

The v6.2 secondary combinations seen for each primary driver determine what you author. For example, `user_rate_normalization` primary + `included_user_reduction` secondary triggers the "additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" sub-paragraph that appears in the Format B template under §`tier_base_increase` and which propagates to other drivers when IUR is secondary.

Extract these integration patterns from the templates (search for `[IF secondary driver = …]` markers). If the template does not show an integration pattern for a combination that v6.2 actually exhibits, flag it for the operator — do not invent.

### Section 3 — Decrease-side drivers (three subsections)

Each of the three decrease-side drivers (`module_compression`, `user_count_variance`, `rate_architecture`) gets a `###` subsection. Source = the Good News template (lines 44–80 of archived `_brief-template.md`).

Per decrease-side driver:

- **Definition** (what triggers it; cite count + the specific accounts: ml/gc/dccl/pf for module_compression; rw/jyc for user_count_variance; mlg for rate_architecture).
- **Mechanic block** (the verbatim prose from the Good News template).
- **Pricing-table template** (the `| | Before | After |` table the brief renders directly under the prose).
- **Voice posture note** (cross-reference `_root/04 §3` row on "gift / reward for loyalty" prohibition — Good News is math, not a favor).

**Flag**: the handoff's §Driver Framing only names `module_compression` on the decrease side. The Good News template implies `user_count_variance` and `rate_architecture` exist as v6.2 driver values, and v6.2 confirms — but neither has a stamped framing in the handoff. The Good News template prose stands as canonical; flag the gap so `_handoff-prompt.md` (or a future stamped decision) can ratify.

### Section 4 — Secondary-driver weaving patterns

A short section (~250–400 words) that consolidates the integration patterns from §2.X.7 into a single matrix. For each combination v6.2 actually exhibits:

| Primary | Secondary(ies) | What changes about the primary block |
|---|---|---|
| `user_rate_normalization` | `included_user_reduction` | Add sub-paragraph: "Additionally, the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]." Apply IUR-variant of `_root/04 §4.5` close. Apply billing-basis footnote per §4.9. |
| ... | ... | ... |

The matrix is the operational artifact — Stage 4 drafters consult it after picking the primary driver block.

Constraint: **only enumerate combinations that v6.2 actually exhibits** (the 7 combinations listed in Step 2). Do not enumerate hypothetical combinations.

### Section 5 — Driver-segment correlation (informational)

A short table (~10 rows) noting which drivers cluster in which segments. This is *informational only* (segment-to-driver routing is not a rule; per the handoff and `_root/02`, the segment is determined by Δ + entity + health, and the driver is independent). But it's useful context for the drafter — knowing that 7 of the 8 Pre-Engagement accounts also have `user_rate_normalization` as primary helps the drafter calibrate the voice.

Author this section as: small table, no rules, explicit "informational; do not route on this."

### Section 6 — What this doc does NOT own (closing reminder)

A short closing section that lists what `_root/05` does NOT own and points to the owning doc for each:

- Voice rules governing HOW the driver block reads → `_root/04` (especially §4.5, §4.6, §4.7, §4.9, §4.10, §4.14)
- The tier-feature paragraph that follows the driver block ("What You're Getting at $X") → `_root/03 §1`
- Segment definitions and ownership boundaries → `_root/02`
- Which format a driver routes to (delta thresholds, CEO involvement gates) → `_root/06` (next wave)
- The v6.2 data fields each driver dispatches on → `_root/07 §2`
- The quality-bar check that confirms the right block was selected → `_root/08` (Wave 4)

### Header block (match the pattern in other root docs)

```
# 05 — Driver Taxonomy

> **What this doc owns**: <populate from your final section list>
>
> **What this doc DOES NOT own**: <populate>
>
> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: archived `_handoff-prompt.md` §Driver Framing; archived Format A / Format B / CEO Letter / Good News brief templates (per-driver `**DRIVER:` blocks); archived per-account exemplars (kal, kii, ih, da, pf); `_master-account-data-v6.2.csv` (driver counts inlined in Wave 3.1 prompt §2)
> **Supersedes**: per-driver narrative content previously scattered across the four archived brief templates. After this doc lands, Stage 3 templates reference _root/05 by section number, not by inline restatement.
```

---

## Step 4: Anti-drift discipline

- **Every driver block lives in exactly one §-section.** If you write the same driver block twice (e.g. once in §2 and once in §4), you've created drift. §4 is the integration matrix; it references §2 blocks by section number, never restates them.
- **Verbatim is verbatim.** The driver-prose blocks in the templates have been iterated to exact wording. Copy them character-for-character. Do not "improve" them, do not modernize them, do not collapse two sentences into one. If a template uses `[BRACKETED_TOKEN]` for a substitution, preserve the exact token name.
- **Conditional logic stays as-is.** When a template says `[IF trailing avg users ≤ new included base — user charge goes to $0:]`, preserve the bracket-comment exactly. These are operator/drafter-facing markers, not customer copy.
- **Voice rules are referenced, not restated.** Where a paragraph after a driver block is governed by a voice rule in `_root/04` (billing-basis footnote, platform-base-grown sentence, early-adopter tenure paragraph, IUR variant close), reference `_root/04 §X.Y` — do not paste the rule text here. The whole point of `_root/04`'s existence is that `_root/05` doesn't restate it.
- **Where Format A, Format B, and CEO Letter differ on the same driver, preserve all three variants.** They are not duplicates; they are voice-tuned variants for different deltas and audiences. The differences are deliberate.
- **Asking is cheap. Inventing is the drift vector.** If a v6.2 driver value has no archived template block (e.g. `user_count_variance`, `rate_architecture`), flag the gap. If a template block has no v6.2 driver value backing it (none observed but possible), flag the gap. Do not paper over either.

---

## Step 5: Voice and format constraints

- Register: operator-facing for the surrounding documentation (definitions, integration patterns, gap flags). The driver-block bodies themselves are client-facing — they ARE the prose that ends up in the brief. Preserve the client-facing register inside the verbatim blocks; use operator-facing register outside them.
- Use clean Markdown structure: `##` for the 6 sections, `###` for each driver subsection inside §2 and §3, `####` for the sub-subsections within each driver (definition, Format B block, CEO Letter block, etc.).
- Render verbatim driver-prose blocks inside Markdown blockquotes (`> Your additional-user rate has been **$[LEGACY_USER_RATE]/user**…`) or fenced code blocks where the prose contains markdown special characters that would otherwise render. Pick one convention and use it consistently.
- Render conditional markers (`[IF ...:]`, `[REQUIRED when ...]`) in their original form — they are part of the template's drafter-facing scaffolding.
- No emoji. No "Importantly," "Critically," "This is the most important driver." Section ordering and account counts already signal importance.

---

## Step 6: Output

Replace the entire current contents of `Pricing Migration/_root/05_driver_taxonomy.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/05_driver_taxonomy.md (replaced stub)
Files read: <enumerate every file path from Step 1 with last-updated date or mtime>
Explicitly-authorized archive reads: <list the archived templates + exemplars + handoff section>
Files NOT read: <enumerate per Step 1 "Do NOT read" + any others>

Drivers authored — increase-side (Section 2): 8 subsections (user_rate_normalization, platform_discount_correction, tier_base_increase, included_user_reduction, at_book_tier_shift, multi_org_retirement, annual_discount_retirement, special_arrangement)
Drivers authored — decrease-side (Section 3): 3 subsections (module_compression, user_count_variance, rate_architecture)
Drivers documented as anomaly (Section 1): 1 (already_migrated, status-marker leak)
Format variants captured per increase-side driver: <e.g. "all 8 have Format B blocks; 7 have CEO Letter blocks (missing: <list>); 5 have Format A blocks (missing: <list>)">
Secondary-driver combinations enumerated (Section 4): <count — should be 7 per Step 2>

Verbatim content preserved character-for-character: <list the specific verbatim blocks captured, by source template + driver>

Gaps surfaced (template prose missing for a v6.2 driver, or v6.2 backing missing for a template block):
- <list, or "none">

Conflicts between Format A / Format B / CEO Letter on the same driver (where the divergence is more than voice-tuning):
- <list with the divergence noted, or "none">

Self-audit — rules from _root/04 that I restated here rather than referenced:
- <list — should be "none" for voice rules; only verbatim driver prose belongs here>

Self-audit — duplications within this doc (same driver block authored in two sections):
- <list — should be "none">

Open questions for operator:
- <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. The operator will paste your output back to the planning agent for review before Wave 3.2 / Wave 4 review or before any Stage 3 template work begins.

---

## Step 7: If something is missing or contradictory

- A v6.2 driver value with no archived template block → flag. Do not invent prose. (`user_count_variance` and `rate_architecture` are likely candidates — they're in Good News but not in `_handoff-prompt.md` §Driver Framing.)
- An archived template block whose prose contradicts the handoff's "Key framing" sentence for that driver → flag with both versions; do not pick one without operator guidance.
- A conditional sub-block that appears in Format B but not in CEO Letter (or vice versa) on the same driver → flag and preserve both; the divergence may be deliberate (CEO Letter has different conditional triggers because of the longer-form structure).
- An exemplar brief that uses prose differing from the canonical template block → flag. The canonical template wins by default; the exemplar may have been edited per-account or may predate a template fix.
- The `already_migrated` driver-field leak → flag; you do not author a block for it; you note the anomaly in §1 and reference `_root/07 §3` (the loader filters these accounts upstream).

**Asking is cheap. Inventing is the drift vector.**
