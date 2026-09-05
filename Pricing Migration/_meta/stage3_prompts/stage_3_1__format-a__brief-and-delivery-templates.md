# Stage 3.1 — Authoring Prompt for `format-a-notices/_brief-template.md` + `_delivery-email-template.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by planning agent
> **Output target**: TWO new files under a NEW folder at `Pricing Migration/format-a-notices/`:
>   - `format-a-notices/_brief-template.md` (the structural skeleton for every Format A per-account brief)
>   - `format-a-notices/_delivery-email-template.md` (the cover email that wraps every Format A brief at delivery)
> **Estimated authored length**: brief template 300–450 lines; delivery email template 80–120 lines.
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all authored and operator-stamped as of 2026-05-22). Independent of Stage 3.2 / 3.3 / 3.4 / 3.5 — can run in parallel with those, though Stage 3.5 (entity packets) is best done last (it inherits patterns from the other four format templates).

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `format-a-notices/_brief-template.md` is the structural skeleton every Stage 4 per-account drafting agent fills in to produce a Format A 60-Day Notice brief. The companion `_delivery-email-template.md` is the cover email that wraps the completed brief at delivery time.

Your job is to **author two new template files that reference `_root/` rules by §-number and never restate them.** This is the single most important discipline of this entire task. Every voice rule, every forbidden phrase, every driver-prose block, every routing condition, every quality check lives in exactly one `_root/` doc. The templates carry only:

- **Drafter-facing structural scaffolding** — the operator-notes blockquote header, the routing block format, the section headings, the bracketed placeholders the drafter fills in from data, the pricing-table row template structure.
- **Lookup instructions** — pointers like `[INSERT _root/05 §2.1.5 — Format A canonical block for user_rate_normalization — verbatim, with [BRACKETED_TOKENS] filled from v6.2 + Postgres data per _root/07 §4]`. The drafter at draft time copies the verbatim block from the owning `_root/` doc into the brief; the template does not carry the prose.
- **Conditional flow logic** — `[IF migration_driver = X: use block A | IF migration_driver = Y: use block B]`. The conditions reference v6.2 columns by name (per `_root/07 §2`); the resulting block is a pointer to `_root/05 §N.M`, not inline prose.

If you find yourself about to paste verbatim prose from `_root/03`, `_root/04`, or `_root/05` into the template, **stop**. That is exactly the drift the path-reference contract (`_root/CONTRACTS.md §5`) was written to prevent. The template carries the lookup; the prose stays in its owning doc.

The cost of a single inlined rule is a template that quietly diverges from the rule layer the next time the rule is edited. The cost of "the template is harder to read because of all the §-pointers" is one extra read step per drafter per brief. The former is unrecoverable drift; the latter is a five-second cost. The discipline is non-negotiable.

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will not extend the template's scope beyond what `_root/06 §1` defines Format A to be. You will reference what exists in `_root/` and render the template precisely.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date (from each file's header block where present) in the conformance block of your final reply.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` — the operator contract, agent contract, rule-change protocol, anti-archive rule with explicit-extraction exception, path-reference contract.
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. The changelog tells you which rules have been operator-stamped, which were superseded, and which decisions inform what the new template must encode. **Particularly important entries**: Wave 1 (the 2 operator policy decisions on peer dollars + competitor pricing that affect Format A's "How This Compares" section); Wave 2 (the Q4 decision that "What's Coming in 2026" lands in ALL formats including Format A); Wave 3 operator-stamping pass (the higher-touch-wins precedence rule that affects boundary routing into / out of Format A); Wave 4 (the `_root/05 §1.1` arithmetic correction that affects `module_compression` Format A coverage).

### The rule layer — read in FULL (these are the rules the new template references)

6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` — the strategic register. Few mechanical rules; sets the tone every Format A brief operates inside.
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — segments, ownership boundary, overlays, errata, 109/107/2 reconciliation. **For Format A specifically**: Core segment ($0 < Δ ≤ $200) and a subset of Narrative ($201 ≤ Δ ≤ $400 that satisfy the ≤10% / ≤$80 condition per the operator-stamped precedence rule); plus Annual segment accounts whose natural Δ tier lands in Format A; plus Tailwind accounts (Δ ≤ $0) that have small absolute decreases per `_root/05 §3.1.3` (the Format A `module_compression` block).
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — T1/T2/T3 verbatim "What You're Getting at $X" blocks (Section 1 — one verbatim block per tier under "T1 — Catalog Essentials", "T2 — Commerce Professional", "T3 — Commerce Enterprise"), user-rate ladder (Section 2 Block A — 1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18), "What's Coming in 2026" verbatim block (Section 3 — now mandatory in ALL formats including Format A per operator decision Q4 2026-05-22), implementation-fee table (Section 4 — recommendation only; surfaces in Format A only on tier-transition accounts), INTERNAL peer ranges (Section 5 — never in client copy) and INTERNAL unpublished premium SKUs (Section 6 — never in client copy). (`_root/03` uses "Section N" headings rather than `§N`; treat them as equivalent.)
9. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — **the highest-rule-density doc.** Read every subsection. **For Format A specifically**: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase table (every row applies to Format A), §4.1 tenure-aware lede variants, §4.2 lede stat guardrail (no provisioned-vs-active ratio), §4.3 "above the midpoint" user-count clause, §4.5 operations-unchanged sentence + IUR fork, §4.6 platform-base-grown sentence (referenced from `_root/05 §2.5.4` Format A `at_book_tier_shift` block per CL-013 — the new template MUST cite §4.6 by reference, not inline the prose), §4.7 early-adopter tenure paragraph, §4.8 value anchor (`cost_per_order < $200` threshold — operator-stamped 2026-05-22; Format A applies the same threshold), §4.9 billing-basis footnote, §4.11 "How This Compares" structure (no peer dollar ranges per CL-003, no equivalent-platforms sentence per CL-004 — both operator-stamped 2026-05-22 universal), §4.12 Format A close text (the passive variant), §4.13 health-band lede overrides (Watch/At Risk/Critical → suppress lede block + open with standalone dollar sentence), §4.14 discount-correction lede substitution (Format A accounts with `migration_driver = platform_discount_correction`).
10. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/05_driver_taxonomy.md` — **the driver-prose library.** Read every subsection. **For Format A specifically — 6 driver blocks are carried verbatim**: §2.1.4 (URN — `user_rate_normalization`), §2.2.4 (renamed driver — `platform_discount_correction` per CL-011; the prior archive used `discount_correction`), §2.5.4 (`at_book_tier_shift` — note: CL-013 was applied at this source on 2026-05-26 per operator stamp; §2.5.4 now carries a `[INSERT _root/04 §4.6 verbatim sentence]` placeholder in place of the formerly-inlined platform-base-grown sentence; the new Format A template references §2.5.4 cleanly), §2.6.4 (`multi_org_retirement` — Format A carries the additional "every entity is making the same move" paragraph that Format B / CEO Letter omit), §2.8.4 (`special_arrangement`), §3.1.3 (`module_compression` Format A near-flat variant for decrease-side accounts that don't route to Good News). **For Format A explicitly NOT carried — 3 driver blocks forward-reference to Format B**: §2.3.4 (`tier_base_increase`), §2.4.4 (`included_user_reduction`), §2.7.4 (`annual_discount_retirement`). If a Stage 4 drafter routes a Format A brief for an account whose `migration_driver` is one of those three, the routing itself is suspect — Format A's mechanical scope (Δ ≤ $80 / ≤10%) does not typically produce those drivers, and the drafter escalates per `_root/CONTRACTS.md §2`.
11. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/06_format_routing.md` — **the format definition and routing.** Read every subsection. **For Format A specifically**: §1 the Format A definition (CS-led, near-flat, ≤$80 / ≤10%, passive close), §2 the 6-step routing-decision flow (the order matters), §3 the delta-tier dispatch table (Format A is row 2: `0 < Δ ≤ $80 OR Δ_pct ≤ 10%`), §3 the operator-stamped Δ_pct vs Δ_mrr precedence ("higher-touch format wins"), §4.1 entity overlay (entity-children do NOT receive Format A briefs — they route to entity packets via `_root/02 §3`), §4.2 health override + Format-A-vs-Good-News interaction (a Good-News-eligible account that is Watch/At Risk/Critical does NOT receive Format A's `module_compression` near-flat variant either — same CSM-check-in carve-out), §4.3 annual overlay (annual Format-A-eligible accounts get a 90-day notice window, not 60), §5 the `comm_action` vocabulary (Format A's value: `Format A — 60-Day Notice`; 15 rows in the routing CSV per `_root/06 §5`), §6 the 5 routing-CSV errata mirror.
12. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — **the data-fetching contract.** Read every subsection. **For Format A specifically**: §1 source-of-truth hierarchy, §2 the 53-column v6.2 field guide (every bracketed placeholder in your template references one of these column names), §3 the canonical loader (the drafter uses this — the template does not), §4 the 3 Postgres MCP queries + derived metrics (the template's bracketed placeholders reference outputs of these queries), §5 the 9-row fallback table (the template may need to direct the drafter to a fallback when Postgres data is missing), §6 file-naming convention (`format-a-notices/[ord_id]__[company-slug]__brief.md` and `__delivery-email.md`; versioned re-runs use `__v2`, `__v3`), §7 the canonical routing-block field-list matrix per format — **THIS IS THE AUTHORITATIVE FORMAT-A ROUTING-BLOCK SPECIFICATION; your template's routing-block block MUST match this matrix exactly**.
13. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/08_quality_bar.md` — **the QA layer.** Read every subsection. **For Format A specifically**: every QB-NNN check whose `Applies to:` field includes "Format A" or "all formats." A new template that fails one of those checks at drafting time is broken. Your template's structure (section presence, placeholder coverage, conditional logic) must enable every Format-A-applicable QB-NNN check to pass when the drafter fills it in.

### Cleanup-tracker items the new template must address (read all 6)

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file** (the normal AGENTS.md hard rule against browsing `_meta/` is overridden here for Stage 3 template-build sessions, since the cleanup tracker is exactly the input list of corrections the templates need to encode). Read in full but apply specifically to Format A:
    - **CL-001** — Remove "no account-specific adjustments" sentence wherever it appears. Format A's archived `_brief-template.md` may or may not contain it; the new template must NOT.
    - **CL-003** — Strip peer dollar ranges from Format A client copy (operator-stamped 2026-05-22 universal). The prior Format A template included peer dollars in "How This Compares" client-facing copy; the new template uses the plain-English position vocabulary from `_root/04 §4.11` and keeps peer dollars INTERNAL-ONLY (and not in the brief at all per the universal stamp).
    - **CL-004** — Cut "equivalent platforms range from $3,000–$3,500/month" sentence for T3 accounts (operator-stamped 2026-05-22 universal). The new Format A template does NOT carry this sentence anywhere.
    - **CL-005** — "What's Coming in 2026" verbatim block applies to all 4 formats including Format A (Format A already carried it in the archived template; the new template confirms the §-pointer is to `_root/03 §3`, not an inlined block).
    - **CL-011** — Driver-name rename: the prior Format A template's `**IF \`discount_correction\`:**` conditional becomes `**IF \`platform_discount_correction\`:**` to align with v6.2 + `_root/05` canonical naming.
    - **CL-013** — RESOLVED 2026-05-26 at the `_root/05 §2.5.4` source (NOT at the new Format A template). The new Format A template's driver dispatch for `at_book_tier_shift` references `_root/05 §2.5.4` cleanly; the source-level cleanup is upstream of the template build, so no per-template carve-out is needed. Verify §2.5.4 carries the `[INSERT _root/04 §4.6 verbatim sentence]` placeholder when you read it — if the inline somehow remains, STOP and flag in your conformance block.

### Archive references (explicitly authorized per `_root/CONTRACTS.md §4` for Stage 3 template-build extraction)

These are the prior artifacts the new template SUPERSEDES. Read them for structural scaffolding (operator-notes header style, routing-block layout, section ordering, conditional-flow markers) and to understand what a completed brief looks like. **Do NOT lift verbatim driver prose from these into the new template** — driver prose is owned by `_root/05` now. The archived inlined prose is the very drift the rebuild exists to eliminate.

15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` — the prior Format A brief template (15.7 KB). **Read in FULL.** Note: this file is not in `_archive/`; it's in the older `Migration-Health Artifacts/` folder structure. The template's body inlines driver prose verbatim — that is exactly the drift the new template fixes. Structural elements you may carry forward (with `_root/`-pointer rewrites): operator-notes blockquote header style, internal routing-note block, section ordering (lede → "What You've Built" → "Why the Number Is Changing" → "What You're Getting" → "What's Coming in 2026" → "How This Compares" → "What This Works Out To" → operations-unchanged paragraph → close). The conditional `[IF driver = X]` markers can be retained as scaffolding — they map to `_root/05 §N.M` pointers in the new template.

16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/_delivery-email-template.md` — the prior Format A delivery email template (3.4 KB). **Read in FULL.** Short, 4-sentence structure. The new delivery email template largely retains this structure but rewrites the inlined "only thing changing" sentence as a pointer to `_root/04 §4.5` (with the default + IUR-fork variants both available to the drafter at draft time).

17. **Three Format A exemplar briefs (clean v2 versions only; do NOT read the pre-v2 versions)** — these show what a completed Format A brief looks like AFTER the prior template's S1–S7 fixes were applied. They establish what "drafter fills in placeholders correctly" produces; they are calibration, not templates.
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kal__kalco-allegri-crystal__brief__v2.md` — URN exemplar
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kii__kennedy-international__brief__v2.md` — ABTS + URN-secondary exemplar
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/lss__lifestyle-solutions__brief__v2.md` — `at_book_tier_shift` exemplar
    Flag in your conformance block any place these exemplars contradict the current `_root/04` voice rules or `_root/05` driver blocks — those contradictions are evidence that the exemplars need regeneration when Stage 4 production drafting begins (file as new `CL-NNN` items via your gaps list; the planning agent will add them to `_meta/stage3_cleanup.md`).

### Do NOT read

- Any other format folder's brief template, delivery email template, or per-account briefs — that is Stage 3.2 / 3.3 / 3.4 / 3.5 scope. Reading them here is scope creep and may pull non-Format-A patterns into the Format A template.
- Any pre-v2 exemplar in `_archive/.../format-a-notices/` (e.g. `kal__kalco-allegri-crystal__brief.md` without the `__v2` suffix) — the pre-v2 versions predate the S1–S7 template fixes and contain forbidden language per the archived `_handoff-prompt.md`. The v2 versions in step 17 are the clean ones.
- `_meta/stage2_prompts/**` — operator-process material for the Wave 1–4.1 fresh-agent sessions that authored `_root/`; not relevant for template building.
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material already abstracted into `_root/01`–`_root/07`. Reading them here is scope creep; the abstracted version in `_root/` is canonical.
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/` (per AGENTS.md hard rules).
- Any other `_meta/stage3_prompts/**` file (the other Stage 3 prompts) — independent waves.

---

## Step 2: Authoritative Format A scope (use as fact — do not re-derive)

The planning agent verified the following against v6.2 + `_root/06` on 2026-05-22. Use as-is; if you believe any of it is wrong, flag in your conformance block and do not proceed.

**Format A's mechanical scope** (per `_root/06 §3`):

- Δ MRR satisfies: `0 < Δ ≤ $80 OR Δ_pct ≤ 10%`, applying the operator-stamped "higher-touch format wins" precedence rule (so a $75 / 12% account routes to Format B, not Format A).
- AND no override fires (no entity overlay per `_root/02 §3`, no health override per `_root/02 §4`, no annual overlay timing impact per `_root/02 §5` — though annual accounts may still route to Format A's format substance with a 90-day window instead of 60).
- AND `delta_mrr ≥ 0` (decrease-side accounts route to Good News per `_root/06 §3` row 1, EXCEPT `module_compression` near-flat decreases that route to Format A per `_root/05 §3.1.3`).

**Format A's routing-CSV count**: 15 accounts as of 2026-05-22 carry `comm_action = "Format A — 60-Day Notice"` in `migration_comm_tiers_2026-05-19.csv`. Plus an unknown number of HOLD rows whose `post_hold_action` resolves to Format A. Your template is sized for 15+N accounts.

**Format A's driver coverage** (per `_root/05` — 6 blocks IN scope, 3 OUT of scope):

| Driver | In scope for Format A? | Owning `_root/05` block (Format A canonical) |
|---|---|---|
| `user_rate_normalization` | YES | §2.1.4 |
| `platform_discount_correction` | YES (renamed from `discount_correction` per CL-011) | §2.2.4 |
| `tier_base_increase` | NO — forward-reference to Format B | §2.3.4 (forward-ref only) |
| `included_user_reduction` | NO — forward-reference to Format B | §2.4.4 (forward-ref only) |
| `at_book_tier_shift` | YES (CL-013 resolved at source 2026-05-26 — §2.5.4 now uses a `[INSERT _root/04 §4.6 sentence]` placeholder; new template references §2.5.4 cleanly) | §2.5.4 |
| `multi_org_retirement` | YES (Format A carries 2nd "every entity is making the same move" paragraph that Format B / CEO Letter omit) | §2.6.4 |
| `annual_discount_retirement` | NO — forward-reference to Format B | §2.7.4 (forward-ref only) |
| `special_arrangement` | YES | §2.8.4 |
| `module_compression` (decrease-side) | YES — for near-flat decrease accounts that don't route to Good News | §3.1.3 |
| `user_count_variance` (decrease-side) | NO — Good News only per `_root/05 §3.2` | n/a |
| `rate_architecture` (decrease-side) | NO — Good News only per `_root/05 §3.3` | n/a |

If a Stage 4 drafter encounters a Format A routing for an account whose `migration_driver` is one of the 5 NOT-in-scope values, the routing is suspect — the drafter escalates per `_root/CONTRACTS.md §2` and does not draft.

**Format A's voice-rule coverage** (per `_root/04` — every applicable subsection):

Apply at every brief: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase prohibitions, §4.2 lede stat guardrail.

Apply conditionally (with the rule's own IF condition stated in §4):
- §4.1 tenure-aware "rate was set in [YEAR]" variant (cohort-year-dependent)
- §4.3 "above the midpoint" user-count clause (when applicable per the §4.3 condition)
- §4.4 high-delta annual-dollar sentence (when Δ_pct > 30% per `_root/04 §4.4` — rare in Format A given the ≤10% scope, but possible for accounts in the Δ ≤ $80 half of the OR with high Δ_pct)
- §4.5 operations-unchanged sentence (default OR IUR-fork variant — drafter selects based on `secondary_drivers` value)
- §4.6 platform-base-grown sentence (when `new_tier_base > current_platform_mrr` per `_root/04 §4.6` condition — the at_book_tier_shift block invokes this, but the prose lives in §4.6, NOT in the §2.5.4 driver block)
- §4.7 early-adopter tenure paragraph (cohort year ≤ 2016)
- §4.8 value anchor section (when `cost_per_order < $200` per the operator-stamped 2026-05-22 threshold)
- §4.9 billing-basis footnote (when an excess-users line is in the pricing table)
- §4.11 "How This Compares" structure (drafter judgment whether to include; if included, no peer dollar ranges per CL-003 + operator stamp, no equivalent-platforms sentence per CL-004 + operator stamp)
- §4.13 health-band lede override (when `health_band ∈ {Watch, At Risk, Critical}` — though for Format A this typically routes the account to Strategic per `_root/02 §4`; rare edge case)
- §4.14 discount-correction lede substitution (when `migration_driver = platform_discount_correction`)

Apply at every brief's close: §4.12 — Format A close text (the passive "If you'd like to talk through the rate or anything about this before then — that conversation is welcome" variant).

---

## Step 3: What you are authoring — file 1 of 2: `format-a-notices/_brief-template.md`

The brief template is the structural skeleton for every Format A per-account brief. Stage 4 drafters at draft time:
1. Look up the account in v6.2 + run the 3 Postgres queries per `_root/07 §4`.
2. Open this template.
3. Fill in every bracketed placeholder from v6.2 + Postgres data.
4. Where the template says `[INSERT _root/05 §N.M block verbatim]`, the drafter opens `_root/05`, copies the named block character-for-character, and pastes it in place, then fills the block's own bracketed placeholders.
5. Where the template says `[INSERT _root/04 §N.M sentence/paragraph]`, same procedure against `_root/04`.
6. Apply the `_root/08` Quality Bar checklist to the completed draft before posting the conformance block.

Author the brief template as the following sections, in this order. **Every section either contains pure scaffolding (placeholders + headings) OR a §-pointer to an owning `_root/` doc. NO rule prose is inlined.**

### Section 0 — File header

Standard markdown title + one-line subtitle naming the format. Match the prior template's tone but update for the new architecture:

```
# Format A — 60-Day Notice — Brief Template
*CS-led | Near-flat delta (≤$80/mo or ≤10%, higher-touch-wins precedence per `_root/06 §3`) | Passive close per `_root/04 §4.12`*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote block at the top of the file (removed before send) that:
- Names when to use this template (cite `_root/06 §1` and `§3`; do not restate the conditions — point to the rule).
- Names who sends (CS team, Kylor; cite `_root/06 §1`).
- Names what this template is NOT for (entity-children → entity packet per `_root/02 §3`; CEO-involvement Δ ≥ $400 → CEO Letter per `_root/06 §1`; Δ ≥ $600 → CEO Pre-Call → Format B per `_root/06 §1`; etc. — point to the rule, do not restate).
- Names the cleanup-tracker history (CL-001, CL-003, CL-004, CL-005, CL-011, CL-013 — list IDs only, link to `_meta/stage3_cleanup.md`).
- States the drafter's responsibility: every § reference in this template is to a canonical `_root/` doc. The drafter follows each reference and copies the named content verbatim into the per-account brief at draft time.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote block that mirrors the routing-block field list in `_root/07 §7` for Format A exactly. Field names and order match `_root/07 §7`; do not invent fields, do not omit fields. Bracketed placeholders for each field.

### Section 3 — Brief content skeleton (the customer-facing body)

Sub-sections in this order:

#### 3a. Subject / greeting / brief title

Standard format: `# [ACCOUNT_NAME]: Your Pricing Is Changing` followed by `*Prepared for [ACCOUNT_NAME] | [DATE]*` per the prior template. Drafter-fillable bracketed placeholders.

#### 3b. Lede block (Thriving / Healthy accounts only)

A bracketed instructional comment naming:
- The lede paragraph structure (cite `_root/04 §4.1` + `§4.2` + `§4.7`; do not restate).
- The conditional skip for Watch / At Risk / Critical (cite `_root/04 §4.13`).
- The "What You've Built" sub-section that follows for in-scope health bands (cite `_root/04 §4.2` for the lede stat guardrail; cite `_root/01 §1` for the relationship-before-price principle).
- A pointer to the v6.2 columns the drafter pulls from: `cohort_year`, `composite_narrative`, Postgres-derived `active_org_users` / `logged_in_90d` / `ltm_orders` (per `_root/07 §2` + `§4.2` + `§4.3`).
- Bracketed placeholders for the actual prose the drafter writes (this is the ONE section where the prose is drafter-generated per `_root/04 §4.1`, not pulled from a `_root/` block — the drafter writes a 2–3 sentence lede tuned to the specific account).

#### 3c. Effective-date sentence (always, for all health bands)

The standalone "Effective **[EFFECTIVE_DATE]**, your monthly invoice moves from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a change of **$[DELTA]/month ([DELTA_PCT])**." sentence per `_root/04 §4.13` (this is the lede for Watch/At-Risk/Critical AND is the second sentence for Thriving/Healthy after the lede paragraph). Drafter-fillable bracketed placeholders.

#### 3d. Consolidated 2026 framing sentence

Cite `_root/04 §3` row on the consolidated 2026 sentence (operator-stamped). The sentence is "In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you." Drafter pastes verbatim from `_root/04 §3`. Do not inline the sentence in this template.

#### 3e. Tenure-aware variant sentence

Conditional `[IF cohort_year ≤ X | IF cohort_year between Y and Z | etc.]` selector pointing to `_root/04 §4.1` for the tenure-aware "rate was set in [YEAR]" variants. Drafter selects the variant based on `cohort_year` from v6.2 and pastes verbatim. Do not inline the variants in this template.

#### 3f. "Why the Number Is Changing" section header + driver dispatch

Section heading: `## Why the Number Is Changing`. Then a drafter-facing `[DRIVER DISPATCH]` block:

```
[DRIVER DISPATCH — select ONE based on v6.2 `migration_driver` value; reject if not listed]:

| v6.2 `migration_driver` | Insert _root/05 block verbatim from | Notes |
|---|---|---|
| `user_rate_normalization` | _root/05 §2.1.4 | Format A canonical block. |
| `platform_discount_correction` | _root/05 §2.2.4 | Format A canonical (driver renamed from `discount_correction` per CL-011 + Wave 3.1 review). |
| `at_book_tier_shift` | _root/05 §2.5.4 | Format A canonical. The §2.5.4 block carries an `[INSERT _root/04 §4.6 verbatim sentence]` placeholder (per CL-013 cleanup applied 2026-05-26 at source); drafter pastes §2.5.4, then fetches the §4.6 sentence and substitutes it into the placeholder. The §4.6 sentence is OMITTED when `new_tier_base < current_platform_mrr` (kii exemplar pattern, per §2.5.6 special case). |
| `multi_org_retirement` | _root/05 §2.6.4 | Format A canonical (carries the additional "every entity is making the same move" paragraph that Format B / CEO Letter omit). |
| `special_arrangement` | _root/05 §2.8.4 | Format A canonical. |
| `module_compression` (decrease-side near-flat only) | _root/05 §3.1.3 | Format A near-flat variant for decrease accounts that don't route to Good News. |
| `tier_base_increase` | NOT carried in Format A | Forward-reference to _root/05 §2.3.4; if routing produces this driver in Format A, escalate per _root/CONTRACTS.md §2. |
| `included_user_reduction` | NOT carried in Format A | Forward-reference to _root/05 §2.4.4; if routing produces this driver in Format A, escalate per _root/CONTRACTS.md §2. |
| `annual_discount_retirement` | NOT carried in Format A | Forward-reference to _root/05 §2.7.4; if routing produces this driver in Format A, escalate per _root/CONTRACTS.md §2. |
```

After the dispatch table, an instructional `[INSERT_DRIVER_BLOCK]` placeholder where the drafter pastes the verbatim block from the selected `_root/05 §N.M`. The template does NOT inline any of the 6 driver-prose blocks.

#### 3g. Secondary-driver weaving (conditional)

A drafter-facing instruction: `[IF v6.2 \`secondary_drivers\` is non-empty: consult _root/05 §4 (secondary-driver weaving matrix) and apply the named integration pattern within the driver block above. If no entry in §4 covers the combination, escalate per _root/CONTRACTS.md §2.]`

#### 3h. Pricing-table row template (per driver)

A drafter-facing instruction pointing to `_root/05 §N.M`'s pricing-table row template for the selected driver. The template does NOT inline pricing-table row structures (each driver has its own per `_root/05 §2.1.5`, `§2.2.5`, `§2.5.5`, `§2.6.5`, `§2.8.5`, `§3.1.4` — all rendered as fenced code blocks in `_root/05` because the driver-prose blockquotes contain markdown special chars).

#### 3i. "What You're Getting at $[NEW_MRR]" tier block

Section heading: `## What You're Getting at $[NEW_MRR]/month`. Then `[INSERT _root/03 Section 1 — [T1 | T2 | T3] verbatim block — verbatim, with [NEW_INCLUDED] and any other bracketed tokens filled from v6.2 \`new_included_users\` and \`assigned_tier\`]`. Drafter pastes the canonical block from `_root/03 Section 1` selected by tier (T1 / T2 / T3); the template does NOT inline the tier blocks (there are 3 of them and inlining produces drift on every `_root/03` edit).

If the account's `new_user_charge` reflects users above the included base, append the `_root/04 §4.9` billing-basis footnote pointer.

#### 3j. "What's Coming in 2026" verbatim block

Section heading: `## What's Coming in 2026`. Then `[INSERT _root/03 Section 3 verbatim block — verbatim, no substitution]`. Drafter pastes the canonical block from `_root/03 Section 3`. Per operator decision Q4 2026-05-22 (CL-005), this section is mandatory in Format A (it was mandatory in the archived template too; the new template preserves the mandate via §-pointer).

#### 3k. "How This Compares" section (conditional, drafter-judgment)

Section heading (conditional): `## How This Compares`. Drafter-facing instruction: `[IF drafter judgment + _root/04 §4.11 indicates this section adds clarity for the account: include the section using the structure in _root/04 §4.11. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.11` exactly:
- No peer dollar ranges (per CL-003 + operator stamp 2026-05-22 universal).
- No "equivalent platforms range from $X–$Y" sentence (per CL-004 + operator stamp 2026-05-22 universal).
- No "no account-specific adjustments" sentence (per CL-001 + `_root/04 §3` row).
- Use the plain-English position vocabulary from `_root/04 §4.11`.
- Apply the `_root/04 §4.3` "above the midpoint" clause when applicable.

The template does NOT inline `_root/04 §4.11`'s structure; it points.

#### 3l. "What This Works Out To" value-anchor section (conditional)

Section heading (conditional): `## What This Works Out To`. Drafter-facing instruction: `[IF derived metric \`cost_per_order < $200\` per _root/04 §4.8 (operator-stamped 2026-05-22): include the value-anchor section using _root/04 §4.8 structure. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.8` exactly. The template does NOT inline `_root/04 §4.8`'s structure; it points. Drafter computes `cost_per_order` per `_root/07 §4.4`.

#### 3m. Operations-unchanged paragraph

Drafter-facing instruction: `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless v6.2 \`secondary_drivers\` includes \`included_user_reduction\`; in that case, INSERT _root/04 §4.5 IUR-fork variant.]` The template does NOT inline either variant; both live in `_root/04 §4.5`.

#### 3n. Close paragraph

Section heading: `## What Happens Next` (or whatever heading `_root/04 §4.12` specifies for Format A — confirm against `_root/04 §4.12` when authoring). Then `[INSERT _root/04 §4.12 Format A close text — verbatim, passive variant]`. Drafter pastes the canonical close from `_root/04 §4.12`. The template does NOT inline the close text.

### Section 4 — Pre-send drafter checklist (drafter-facing, removed before sending OR retained as conformance evidence)

A short `>` blockquote pointing to `_root/08` for the full 126-check QA layer. Name 5–8 of the most Format-A-specific blocker checks by QB-NNN for drafter convenience (e.g. QB-002 conformance block present, QB-040 lede leads with dollar+date not percentage, QB-046 "What's Coming in 2026" present, QB-059 no "no account-specific adjustments" sentence, QB-071 no peer dollars, QB-054 no equivalent-platforms sentence, QB-082 value-anchor threshold respected, QB-085 etc.) — but do NOT restate any check; cite the QB-NNN and `_root/08`.

---

## Step 4: What you are authoring — file 2 of 2: `format-a-notices/_delivery-email-template.md`

The delivery email template is the cover email that wraps the completed brief at delivery time. Short (4 sentences per `_root/04 §4.5` IUR fork conditions). The drafter sends this email with the brief attached.

Author the delivery email template as the following sections, in this order:

### Section 0 — File header

```
# Format A — Delivery Email Template
*60-Day Notice | CS-sent | Wraps the Format A brief; nothing more*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote naming:
- When to use (delta is Format A's scope per `_root/06 §3`; the brief does the heavy lifting; this email is the wrapper).
- Who sends (CS, no CEO co-signature, per `_root/06 §1`).
- Length: 4 sentences. Do not exceed.
- What is NEVER in this email (cite `_root/04 §3` rows — minimizing language, apologies, percentage in the lede, "modest/small/minor", pre-committed call). Do not restate the prohibitions; cite the §3 rows.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote mirroring the routing-block field list in `_root/07 §7` for Format A's delivery email (which may or may not differ from the brief's routing block — confirm against `_root/07 §7` and match exactly).

### Section 3 — Email body skeleton

Standard fields:
- `**Subject:** [ACCOUNT NAME]: your SuperCat invoice is changing — effective [EFFECTIVE_DATE]`
- `Hi [CONTACT NAME],`
- Sentence 1: drafter writes the dollar-change effective-date sentence per `_root/04 §4.13` (this is the standalone dollar sentence; the email leads with dollars per `_root/04 §3` no-percentage-in-lede rule).
- Sentence 2: `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless secondary_drivers includes included_user_reduction; in that case INSERT IUR-fork variant.]` Same selector as brief Section 3m. Template does NOT inline either variant.
- Sentence 3: drafter writes a passive offer matching `_root/04 §4.12` Format A close register (the email's offer is a one-sentence echo of the brief's close — NOT a pre-committed call).
- Signature: `[CSM NAME] | Customer Success | SuperCat`

### Section 4 — Pre-send checklist (drafter-facing)

Short `>` blockquote pointing to `_root/08` for the relevant QB-NNN checks. Cite QB-NNN; do not restate.

### Section 5 — Day-10 follow-up (drafter-facing template)

A short follow-up sentence template for if the customer hasn't acknowledged within 10 days. Standard skeleton; no rule restated.

### Section 6 — Voice calibration notes (drafter-facing)

A short closing paragraph pointing to `_root/04 §4.12` for the email's voice calibration (zero friction, no over-explanation; if you find yourself writing a third paragraph, you've crossed into Format B territory). Cite the rule; do not restate.

---

## Step 5: Anti-drift discipline

- **The path-reference contract is absolute.** Every rule the template needs to enforce is referenced by `_root/XX §N.M`, never inlined. The template's content is scaffolding + pointers; the rule prose stays in its owning `_root/` doc. If you find yourself pasting a sentence from `_root/03`, `_root/04`, `_root/05`, `_root/06`, or `_root/07` into the template, stop — you are introducing drift.
- **The 6 driver-prose blocks live in `_root/05`.** The template's "Why the Number Is Changing" section is a driver dispatch table that names which `_root/05 §N.M` block applies for each `migration_driver` value. The block prose itself is fetched by the drafter at draft time, not inlined here.
- **CL-013 was resolved at source on 2026-05-26.** `_root/05 §2.5.4` no longer inlines the `_root/04 §4.6` platform-base-grown sentence — it carries an `[INSERT _root/04 §4.6 verbatim sentence]` placeholder instead, restoring the path-reference contract upstream of this template build. Your job is straightforward: the new Format A template's driver dispatch (§3f) references `_root/05 §2.5.4` cleanly with no per-template carve-out. Verify when you read `_root/05 §2.5.4` that the placeholder is present (not the inlined sentence); if the inline somehow remains, STOP and flag in your conformance block — the source-level cleanup did not propagate and the template build cannot proceed.
- **CL-001, CL-003, CL-004 are universal.** No "no account-specific adjustments" sentence, no peer dollar ranges, no equivalent-platforms sentence — anywhere in the template, ever. The drafter who follows the template's `_root/04 §4.11` pointer gets the clean structure automatically; the template just needs to not invent its own "How This Compares" prose that resurrects the forbidden phrases.
- **CL-011 is a one-line fix.** The prior template's `**IF \`discount_correction\`:**` conditional becomes the dispatch-table entry for `platform_discount_correction` pointing to `_root/05 §2.2.4`.
- **CL-005 is a confirmation, not a change.** Format A's archived template already carried "What's Coming in 2026"; the new template confirms the §-pointer to `_root/03 §3` and that the section is structurally mandatory.
- **The drafter is the integration point, not the template.** Drafters at draft time fetch verbatim blocks from `_root/`, fill in placeholders from v6.2 + Postgres, and apply conditional rules. The template's job is to tell the drafter what to fetch and where to put it; it does NOT pre-fill what the drafter fetches.
- **No new operator-policy decisions.** If you discover that a rule in `_root/` is ambiguous for Format A's use case, flag in your conformance block. Do NOT pick an interpretation and bake it into the template.
- **No new Format A scope.** Format A handles 6 of 11 drivers per Step 2. Do NOT extend coverage to the 3 forward-referenced drivers (TBI / IUR / ADR) even if you think Format A "should" carry them — that is a Stage 3 cleanup item to file via your gaps list, not a template change.
- **Asking is cheap. Inventing is the drift vector.**

---

## Step 6: Voice and format constraints

- Register for operator-notes and drafter-facing instructions: declarative, no marketing language. Same register as `_root/02`, `_root/04`, `_root/06`, `_root/07`. Use `>` blockquote for every drafter-facing block (the brief-template scaffolding uses Markdown blockquotes for routing notes, conditional flow markers, and operator notes — matching the archived template's convention).
- Use clean Markdown structure: `#` for the file title, `##` for the customer-facing brief sections, `###` for sub-sections inside drafter-facing blocks. Bracketed placeholders use the `[ALL_CAPS_WITH_UNDERSCORES]` convention from the archived template (e.g. `[ACCOUNT_NAME]`, `[NEW_MRR]`, `[EFFECTIVE_DATE]`, `[CSM NAME]`).
- The customer-facing sections of the brief template should READ AS A BRIEF when the drafter fills in placeholders — the template's bracketed instructions are the scaffolding, and the resulting brief (after placeholder fill + `_root/` block insertion) reads as a coherent customer communication.
- No emoji. No "Importantly" / "Critically" — the QB-NNN severity in `_root/08` is the operational signal of importance.

---

## Step 7: Output

Replace nothing — both files are NEW.

Create the new folder + both files:
- `Pricing Migration/format-a-notices/_brief-template.md` (the brief template)
- `Pricing Migration/format-a-notices/_delivery-email-template.md` (the delivery email template)

The folder `Pricing Migration/format-a-notices/` does not exist yet (the prior folder was moved to `_archive/2026-05-22__pre-refactor/format-a-notices/` during the 2026-05-22 refactor); your authoring creates the folder.

Then, in your chat reply (NOT in the files), produce this conformance block per `_root/00_manifest.md §5`:

```
─── Conformance Block ─────────────────────────────────────────
Session task: Stage 3.1 — author format-a-notices/_brief-template.md + _delivery-email-template.md
Output target: 
- Pricing Migration/format-a-notices/_brief-template.md (NEW file, NEW folder)
- Pricing Migration/format-a-notices/_delivery-email-template.md (NEW file)

Files read (with last-updated date / mtime):
- <enumerate every file path from Step 1 with last-updated date or mtime>

Explicitly-authorized archive reads (per Wave 3.1 §1 items 15–17):
- <list every archived file you read with mtime>

Files NOT read:
- <enumerate per Step 1 "Do NOT read">

Brief template sections authored: <count + names — should match Step 3's section list>
Delivery email template sections authored: <count + names — should match Step 4's section list>

Drivers covered in brief template (per the dispatch table in 3f):
- In scope (6): <list with §-pointer for each>
- Out of scope (3 forward-references): <list with §-pointer for each>

CL items addressed (with the specific template element that addresses each):
- CL-001: <where in the template>
- CL-003: <where>
- CL-004: <where>
- CL-005: <where>
- CL-011: <where>
- CL-013: RESOLVED 2026-05-26 at `_root/05 §2.5.4` source — no per-template work needed. Confirm §2.5.4 carries the `[INSERT _root/04 §4.6 verbatim sentence]` placeholder as of your read; if it does not, STOP.

Path-reference contract verification:
- Number of verbatim rule blocks INLINED in the template (should be 0 — if non-zero, list each and explain why it could not be referenced): <count + list or "0">
- Number of §-pointers TO _root/ docs in the template: <count by owning doc — e.g. "_root/03: 3, _root/04: ~12, _root/05: 9, _root/06: ~5, _root/07: ~3, _root/08: ~6">
- Number of bracketed placeholders for drafter data fill-in (per v6.2 + Postgres): <count>

Verbatim text the template DOES carry (template scaffolding only — NOT rule prose):
- <list: e.g. "operator-notes blockquote header style (drafter-facing, not a rule)", "internal routing-note block (drafter-facing metadata, per _root/07 §7)", "section heading text like 'Why the Number Is Changing' (drafter-facing structure, not a rule)", "bracketed placeholders like [ACCOUNT_NAME] (drafter-facing fill points)">

Routing-block field list cross-check (per _root/07 §7 Format A matrix):
- <confirm every required field is present in the template's routing block; flag any divergence>

Gaps surfaced (a Format A scope element that has no _root/ rule, OR a _root/ rule that the template cannot enforce structurally):
- <list, or "none">

Conflicts between sources (and chosen resolution / flag):
- <list, e.g. "the archived Format A template's S1–S7 fixes vs. _root/04 voice rules — resolution: _root/04 wins per CONTRACTS §5", or "none">

Open questions for operator:
- <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file (do not edit `_root/`, do not edit other format folders, do not edit `_meta/stage3_cleanup.md`). The operator will paste your output back to the planning agent for review before Stage 3.2.

---

## Step 8: If something is missing or contradictory

- A `_root/04` voice rule that Format A should enforce but is not yet authored → flag in your conformance block; the planning agent decides whether to author the rule via the `_root/CONTRACTS.md §3` rule-change protocol before you proceed.
- A `_root/05` driver block that the dispatch table says Format A carries but is not yet authored in `_root/05` → flag; do not invent the block.
- A `_root/07 §7` routing-block field list that does not match what Format A briefs actually need → flag both versions; do not pick one.
- A conflict between the archived Format A template's S1–S7 fixes and the current `_root/04` voice rules → `_root/04` wins per `_root/CONTRACTS.md §5`. The archived template's drift is the reason for the rebuild.
- A conflict between two `_root/` docs (e.g. `_root/04 §4.12` close text vs. `_root/06 §1` Format A close description) → flag the conflict; do not pick one. The planning agent resolves via the rule-change protocol.
- A driver an exemplar brief (kal v2, kii v2, lss v2) renders that the new template's dispatch table does not name → flag; the exemplar may be using forbidden phrasing or improvised integration.
- A field the prior template's routing block carried that `_root/07 §7` does not name → flag; either `_root/07 §7` is missing the field (and needs an update via rule-change protocol) or the prior template carried scope creep.
- Anything in the cleanup tracker that you cannot translate into a template element → flag; the planning agent decides.

**Asking is cheap. Inventing is the drift vector.**
