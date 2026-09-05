# Stage 3.2 — Authoring Prompt for `format-b-notices/_brief-template.md` + `_delivery-email-template.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by planning agent (drafted in parallel with Stage 3.1; **delta-pass applied 2026-05-26 after Stage 3.1 was operator-approved**: pattern-inheritance cross-references added to Stage 3.1's output; strict-placeholder precedent added to Step 5 per operator stamp; "unique to Format B" claim about "Your Pricing at a Glance" corrected — the section appears in both Format A and Format B; CL-022 reference added for the delivery email routing-block subset gap)
> **Output target**: TWO new files under a NEW folder at `Pricing Migration/format-b-notices/`:
>   - `format-b-notices/_brief-template.md` (the structural skeleton for every Format B per-account brief — handles both standard Notice + Meeting Offer and the CEO Pre-Call → Format B variant via routing-block flags)
>   - `format-b-notices/_delivery-email-template.md` (the cover email that wraps every Format B brief at delivery; also carries variants for the CEO Pre-Call follow-up case)
> **Estimated authored length**: brief template 400–550 lines (Format B carries 8 driver blocks vs. Format A's 6, plus a "Your Pricing at a Glance" summary table unique to Format B); delivery email template 90–130 lines (4 sentences default; CEO Pre-Call follow-up variant adds 1–2 sentences).
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all authored and operator-stamped); CL-013 cleanup applied at `_root/05 §2.5.4` source 2026-05-26. Independent of Stage 3.1 / 3.3 / 3.4 / 3.5. **Pattern inheritance from Stage 3.1**: if `format-a-notices/_brief-template.md` exists in your read environment at the time you author, you may consult it for structural-convention reference only (operator-notes header style, dispatch-table format, QA-checklist citation style). Do NOT lift Format A driver content, Format A close text, or Format A routing-block fields — those are Format-A-specific and Format B has different §-references throughout.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `format-b-notices/_brief-template.md` is the structural skeleton every Stage 4 per-account drafting agent fills in to produce a Format B Notice + Meeting Offer brief (or, when the CEO Pre-Call routing pattern fires for Δ ≥ $600 accounts, the CS-sent Format B brief that follows the CEO's pre-engagement call). The companion `_delivery-email-template.md` is the cover email that wraps the completed brief at delivery time.

Your job is to **author two new template files that reference `_root/` rules by §-number and never restate them.** This is the single most important discipline of this entire task. Every voice rule, every forbidden phrase, every driver-prose block, every routing condition, every quality check lives in exactly one `_root/` doc. The templates carry only:

- **Drafter-facing structural scaffolding** — the operator-notes blockquote header, the routing block format, the section headings, the bracketed placeholders the drafter fills in from data, the pricing-table row template structure, the "Your Pricing at a Glance" summary table structure unique to Format B.
- **Lookup instructions** — pointers like `[INSERT _root/05 §2.1.2 — Format B canonical block for user_rate_normalization — verbatim, with [BRACKETED_TOKENS] filled from v6.2 + Postgres data per _root/07 §4]`. The drafter at draft time copies the verbatim block from the owning `_root/` doc into the brief; the template does not carry the prose.
- **Conditional flow logic** — `[IF migration_driver = X: use block A | IF migration_driver = Y: use block B]`. The conditions reference v6.2 columns by name (per `_root/07 §2`); the resulting block is a pointer to `_root/05 §N.M`, not inline prose.

If you find yourself about to paste verbatim prose from `_root/03`, `_root/04`, or `_root/05` into the template, **stop**. That is exactly the drift the path-reference contract (`_root/CONTRACTS.md §5`) was written to prevent. The template carries the lookup; the prose stays in its owning doc.

The cost of a single inlined rule is a template that quietly diverges from the rule layer the next time the rule is edited. The cost of "the template is harder to read because of all the §-pointers" is one extra read step per drafter per brief. The former is unrecoverable drift; the latter is a five-second cost. The discipline is non-negotiable.

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will not extend the template's scope beyond what `_root/06 §1` defines Format B (and CEO Pre-Call → Format B) to be. You will reference what exists in `_root/` and render the template precisely.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date (from each file's header block where present) in the conformance block of your final reply.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` — the operator contract, agent contract, rule-change protocol, anti-archive rule with explicit-extraction exception, path-reference contract.
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. **Particularly important entries for Format B**: Wave 1 (peer-dollars universal-strip + competitor-pricing broadening; both stamped 2026-05-22 and both apply to Format B's "How This Compares" section); Wave 2 (Q4 — "What's Coming in 2026" landed in ALL formats including Format B, which the archived Format B template does NOT yet carry); Wave 3 operator-stamping pass (CL-016 stamped: extend Format B + CEO Letter templates with explicit `[IF secondary driver = included_user_reduction]` sub-block under `multi_org_retirement`); Wave 4 (the `_root/05 §1.1` arithmetic correction; doesn't change Format B scope but informs the driver counts you'll cite); **Stage 3 prep 2026-05-26 (CL-013 applied at `_root/05 §2.5.4` source — for Format B this means §2.5.6's bullet on the platform-base-grown sentence was rewritten to say "all three formats reference `_root/04 §4.6` by pointer," which preserves Format B's existing pattern but updates the cross-reference language)**.

### The rule layer — read in FULL (these are the rules the new template references)

6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` — the strategic register. Few mechanical rules; sets the tone every Format B brief operates inside.
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — segments, ownership boundary, overlays, errata, 109/107/2 reconciliation. **For Format B specifically**: Narrative segment ($201 ≤ Δ ≤ $400) is Format B's primary home; plus Core segment accounts that fail Format A's ≤10% threshold per the operator-stamped Δ_pct vs Δ_mrr precedence (higher-touch wins); plus the bottom of the Strategic segment ($401 ≤ Δ ≤ $600 routes to CEO Letter, NOT Format B); plus the Tailwind segment when Δ > $0 (Tailwind decreases route to Good News, not Format B); plus the CEO Pre-Call → Format B routing pattern that lands accounts with Δ ≥ $600 in this template AFTER the CEO has personally pre-engaged the account.
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — T1/T2/T3 verbatim "What You're Getting at $X" blocks (Section 1 — one verbatim block per tier under "T1 — Catalog Essentials", "T2 — Commerce Professional", "T3 — Commerce Enterprise"), user-rate ladder (Section 2 Block A — 1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18), "What's Coming in 2026" verbatim block (Section 3 — now mandatory in ALL formats including Format B per operator decision Q4 2026-05-22; the archived Format B template does NOT yet carry this section — your new template adds it via Section-3 pointer), implementation-fee table (Section 4 — recommendation only; surfaces in Format B only on tier-transition accounts), INTERNAL peer ranges (Section 5 — never in client copy; Format B's archived template already stripped these correctly per CL-003 universal stamp), INTERNAL unpublished premium SKUs (Section 6 — never in client copy). (`_root/03` uses "Section N" headings rather than `§N`; treat them as equivalent.)
9. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — **the highest-rule-density doc.** Read every subsection. **For Format B specifically**: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase table (every row applies to Format B), §4.1 tenure-aware lede variants (Format B's archived lede integrates tenure into sentence one as a relationship signal), §4.2 lede stat guardrail (no provisioned-vs-active ratio), §4.3 "above the midpoint" user-count clause, §4.4 high-delta annual-dollar sentence (when Δ_pct > 30% — much more common in Format B than Format A given Format B's $81–$399 scope), §4.5 operations-unchanged sentence + IUR fork (Format B uses BOTH variants heavily; archived Format B template surfaces both as `[IF primary or secondary driver IS/IS NOT included_user_reduction]` conditionals), §4.6 platform-base-grown sentence (Format B applies as a follow-on paragraph when `new_tier_base > current_platform_mrr` per `_root/05 §2.5.6` — Format B does NOT inline the §4.6 sentence; it references it), §4.7 early-adopter tenure paragraph (Format B's archived template carries an explicit "ADD FOR EARLY ADOPTER COHORTS" block — the new template references §4.7 instead of inlining), §4.8 value anchor (`cost_per_order < $200` threshold — operator-stamped 2026-05-22; **the archived Format B template uses the OLD $35 threshold per CL-002 — your new template MUST use $200**), §4.9 billing-basis footnote, §4.11 "How This Compares" structure (Format B's archived template already strips peer dollar values per CL-003 universal stamp and explicitly forbids comparative language in its `[GUIDANCE]` block — the new template references §4.11 and preserves the strip), §4.12 Format B close text — `Let's Talk` / meeting offer variant — and the formal-notice line, §4.13 health-band lede overrides (Watch/At Risk/Critical accounts skip the relationship lede and open with standalone dollar sentence — Format B uses this same rule), §4.14 discount-correction lede substitution (Format B accounts with `migration_driver = platform_discount_correction` substitute the §4.14 sentence for the "rate was set in [YEAR]" sentence in the lede).
10. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/05_driver_taxonomy.md` — **the driver-prose library.** Read every subsection. **For Format B specifically — 8 driver blocks are carried verbatim**: §2.1.2 (URN — `user_rate_normalization`), §2.2.2 (`platform_discount_correction`), §2.3.2 (`tier_base_increase` — **note CL-012**: the conditional marker `[IF secondary driver = user_rate_normalization AND included base expands]` in §2.3.2's secondary sub-block is suspected of being incorrectly labeled and should likely read `[IF secondary driver = included_user_reduction]`; the integrated sentence reads as IUR-style; CL-012 in `_meta/stage3_cleanup.md` notes this and asks the Stage 3 builder to confirm against v6.2 — if the 7 URN+IUR combinations route through this block, the IUR marker is correct), §2.4.2 (`included_user_reduction`), §2.5.2 (`at_book_tier_shift` — references `_root/04 §4.6` by pointer per §2.5.6 conditional context paragraphs), §2.6.2 (`multi_org_retirement` — **note CL-016 operator-stamped 2026-05-22**: the new Format B template MUST carry an explicit `[IF secondary driver = included_user_reduction]` sub-block under the MOR primary block, integrating the included-base move alongside the multi-org rate retirement; the sub-block's structure is documented in `_root/05 §2.6.6` and `_root/05 §4`; the 2 multi_org + URN-secondary accounts continue with per-account narrative integration per the same CL-016 stamp), §2.7.2 (`annual_discount_retirement`), §2.8.2 (`special_arrangement`). **For Format B explicitly NOT carried — the decrease-side drivers**: §3.1.2 (`module_compression`), §3.2.2 (`user_count_variance`), §3.3.2 (`rate_architecture`) all route to Good News per `_root/06 §3` row 1. If a Stage 4 drafter routes a Format B brief for an account whose `migration_driver` is a decrease-side value, the routing itself is suspect — Format B's mechanical scope (Δ ≥ $81) does not produce decrease drivers, and the drafter escalates per `_root/CONTRACTS.md §2`.
11. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/06_format_routing.md` — **the format definition and routing.** Read every subsection. **For Format B specifically**: §1 the Format B definition (CS-led, meaningful delta, $81–$399, meeting-offer close) AND the CEO Pre-Call → Format B routing-pattern definition (Δ ≥ $600, CEO pre-engages by phone before CS sends the Format B brief), §2 the 6-step routing-decision flow, §3 the delta-tier dispatch table (Format B is row 3: `$81 ≤ Δ ≤ $399`; CEO Pre-Call → Format B is row 5: `Δ ≥ $600`), §3 the operator-stamped Δ_pct vs Δ_mrr precedence ("higher-touch format wins" — so a $75 / 12% account routes to Format B, not Format A), §4.1 entity overlay (entity-children do NOT receive Format B briefs — they route to entity packets via `_root/02 §3`; this is the same rule that affects Format A), §4.2 health override (At-Risk routes to Strategic where the notice is eventually drafted post-stabilization per Reading A operator-stamped 2026-05-22; Critical routes per `post_hold_action` per-account operator judgment), §4.3 annual overlay (annual Format-B-eligible accounts get a 90-day notice window, not 60), §5 the `comm_action` vocabulary (Format B values: `Format B — Notice + Meeting Offer` for standard; `CEO Pre-Call → Format B` for the routing-pattern variant — count from `migration_comm_tiers_2026-05-19.csv` is 19 standard rows + 9 CEO Pre-Call rows + an unknown number of HOLD rows whose `post_hold_action` resolves to one of those two), §5.5 the additional CSV columns (`hold_condition`, `post_hold_action`, `flags`, `nuances`), §6 the 5 routing-CSV errata.
12. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — **the data-fetching contract.** Read every subsection. **For Format B specifically**: §1 source-of-truth hierarchy, §2 the 53-column v6.2 field guide (every bracketed placeholder in your template references one of these column names), §3 the canonical loader (the drafter uses this — the template does not), §4 the 3 Postgres MCP queries + derived metrics (the template's bracketed placeholders reference outputs of these queries), §5 the 9-row fallback table, §6 file-naming convention (`format-b-notices/[ord_id]__[company-slug]__brief.md` and `__delivery-email.md`; versioned re-runs use `__v2`, `__v3`), §7 the canonical routing-block field-list matrix per format — **THIS IS THE AUTHORITATIVE FORMAT-B ROUTING-BLOCK SPECIFICATION; your template's routing-block block MUST match this matrix exactly**. The §7 per-format matrix specifies that Format B's `CEO awareness required before send` field is `NO` for standard Notice + Meeting and `YES` for CEO Pre-Call → Format B; the routing block carries the field unconditionally but with the appropriate value based on the routing pattern.
13. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/08_quality_bar.md` — **the QA layer.** Read every subsection. **For Format B specifically**: every QB-NNN check whose `Applies to:` field includes "Format B" or "all formats." A new template that fails one of those checks at drafting time is broken. Your template's structure (section presence, placeholder coverage, conditional logic) must enable every Format-B-applicable QB-NNN check to pass when the drafter fills it in. **Particularly important Format-B-applicable blocker checks to verify your template enables**: QB-046 ("What's Coming in 2026" present — the archived Format B template OMITS this; your new template MUST include it), QB-077 ("above the midpoint" user-count clause when applicable), QB-078 (high-delta annual-dollar sentence in lede for Δ_pct > 30%), QB-082 (value-anchor `cost_per_order < $200` threshold — promoted from old $35 per CL-002), QB-085 (no peer dollar values in client copy — strengthened from prior pattern via Wave 1 operator stamp).

### Cleanup-tracker items the new template must address (read all 6)

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file** (the normal AGENTS.md hard rule against browsing `_meta/` is overridden here for Stage 3 template-build sessions). Read in full but apply specifically to Format B:
    - **CL-001** — Remove "no account-specific adjustments" sentence wherever it appears. The archived Format B template does NOT carry this sentence (only CEO Letter and `da` exemplar did); your new Format B template confirms its absence and uses the plain-English "How This Compares" structure from `_root/04 §4.11`.
    - **CL-002** — Change Format B value-anchor threshold from `cost_per_order ≤ $35` to `cost_per_order < $200`. The archived Format B template's "What This Works Out To" section (lines ~211–219 of `_archive/.../format-b-notices/_brief-template.md`) uses the $35 threshold; the new template uses $200 per the operator-stamped 2026-05-22 universal change and via reference to `_root/04 §4.8`.
    - **CL-004** — Cut "equivalent platforms range from $3,000–$3,500/month" sentence for T3 accounts. The archived Format B template's `[GUIDANCE]` block in "How This Compares" already forbids comparative language; your new template references `_root/04 §3` row on competitor-pricing prohibition (broadened to named OR unnamed per Wave 1 operator stamp 2026-05-22).
    - **CL-005** — "What's Coming in 2026" verbatim block applies to ALL 4 formats including Format B. **The archived Format B template OMITS this section entirely** — your new template ADDS it via a Section-3 pointer to `_root/03 Section 3`. This is the most additive change in the Format B rebuild.
    - **CL-012** — Format B `tier_base_increase` block: the conditional marker `[IF secondary driver = user_rate_normalization AND included base expands]` is suspected of being incorrectly labeled (the integrated sentence "the included user base for this tier is expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED]" reads as IUR-style, not URN-style). Confirm against v6.2: the 7 URN+IUR combinations and the 6 multi_org+IUR combinations both route through the IUR-related secondary-driver logic; if the §2.3.2 block's secondary marker is the entry point for URN-primary + IUR-secondary, the marker should read `[IF secondary driver = included_user_reduction]`. Your dispatch table's `tier_base_increase` row should cite `_root/05 §2.3.2` and reflect whichever marker `_root/05 §2.3.2` currently carries. If the marker in `_root/05 §2.3.2` is still ambiguous when you read it, flag in your conformance block — the resolution belongs to `_root/05`, not to this template.
    - **CL-016** (operator-stamped 2026-05-22) — Extend Format B's `multi_org_retirement` primary block with an explicit `[IF secondary driver = included_user_reduction]` sub-block. The 6 multi_org + IUR-secondary accounts get templated coverage; the 2 multi_org + URN-secondary accounts continue with per-account narrative integration per the kii / da exemplar patterns. The sub-block structure is documented in `_root/05 §2.6.6` and `_root/05 §4`. Your dispatch table's `multi_org_retirement` row directs the drafter to consult §2.6.2 (primary block) + §2.6.6 (secondary sub-blocks) + §4 (the secondary-driver weaving matrix) and apply the IUR sub-block when `secondary_drivers` includes `included_user_reduction`.

### Archive references (explicitly authorized per `_root/CONTRACTS.md §4` for Stage 3 template-build extraction)

These are the prior artifacts the new template SUPERSEDES. Read them for structural scaffolding (operator-notes header style, routing-block layout, section ordering, conditional-flow markers, the "Your Pricing at a Glance" summary table structure) and to understand what a completed brief looks like. **Do NOT lift verbatim driver prose from these into the new template** — driver prose is owned by `_root/05` now. The archived inlined prose is the very drift the rebuild exists to eliminate.

15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md` — the prior Format B brief template. **Read in FULL.** Note: this template's body inlines driver prose verbatim for all 8 drivers — that is exactly the drift the new template fixes. Structural elements you may carry forward (with `_root/`-pointer rewrites): operator-notes blockquote header style, internal routing-note block, section ordering (lede → "Why the Number Is Changing" → "What You're Getting at $X" → "What This Works Out To" → "How This Compares" → "Your Pricing at a Glance" summary table → operations-unchanged paragraph + IUR fork → "Let's Talk" close + formal-notice line). The conditional `[USE ONLY THE APPLICABLE BLOCK]` markers can be retained as scaffolding — they map to `_root/05 §2.X.2` pointers in the new template. **The "Your Pricing at a Glance" summary table is unique to Format B** (Format A does not carry it; CEO Letter has its own variant; Good News has its own variant) — preserve the table structure as scaffolding; the data tokens reference v6.2 + Postgres outputs per `_root/07 §2` + §4.
16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_delivery-email-template.md` — the prior Format B delivery email template. **Read in FULL.** Short structure. The new delivery email template largely retains this structure but rewrites the inlined "only thing changing" sentence + IUR fork as a pointer to `_root/04 §4.5` (with both variants available to the drafter at draft time), and rewrites the inlined "rate was set in [YEAR] — this is the first time we've updated it" sentence as a pointer to `_root/04 §4.1` tenure variants. The archived delivery email's "Operator notes" block at the bottom carries 3 important variant notes (CEO Letter sign-off swap; CEO Pre-Call → Format B opening adjustment; never adjust effective date without updating brief) — preserve those notes in the new template's operator-notes section, referenced by `_root/04 §4.12` and `_root/07 §6` rather than restated.
17. **Three Format B exemplar briefs (clean v2 versions only; do NOT read the pre-v2 versions)** — these show what a completed Format B brief looks like AFTER the prior template's S1–S7 fixes were applied. They establish what "drafter fills in placeholders correctly" produces; they are calibration, not templates.
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/ih__interlude-home__brief__v2.md` — TBI + URN exemplar (good calibration for the CL-012 secondary marker question)
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/cci__currey-company__brief__v2.md` — full Format B v2 exemplar
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/gl__golden-lighting__brief__v2.md` — full Format B v2 exemplar
    Flag in your conformance block any place these exemplars contradict the current `_root/04` voice rules, `_root/05` driver blocks, or any of the 6 Format B CL items above — those contradictions are evidence the exemplars need regeneration when Stage 4 production drafting begins (file as new `CL-NNN` items via your gaps list).

### Pattern reference from Stage 3.1 (required — Stage 3.1 was operator-approved 2026-05-26)

18. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_brief-template.md` AND `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_delivery-email-template.md` — **read both in FULL.** Stage 3.1 was operator-approved 2026-05-26 (see `_root/09_changelog.md` "Stage 3.1 review pass" entry); these are the canonical structural-convention references for every Stage 3.X template. **Match the following conventions exactly** (deviating produces inconsistency across format folders that operator review will flag):
    - **Operator-notes blockquote header style** — Stage 3.1 brief template lines 6–23 (the `> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**` block with sub-paragraphs for When to use / Who sends / What this template is NOT for / Cleanup-tracker history / Drafter's responsibility / Conformance block).
    - **Internal routing-note structure** — Stage 3.1 brief template lines 27–50 (the `> **Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for [FORMAT]):` block; field names and order match `_root/07 §7` exactly; conditional rows enumerated separately).
    - **Driver dispatch table format** — Stage 3.1 brief template lines 131–143 (Markdown table with columns "v6.2 `migration_driver`" / "Insert `_root/05` block verbatim from" / "Notes"; out-of-scope drivers appear with "NOT carried in [FORMAT]" + forward-reference; `already_migrated` anomaly appears as final row).
    - **Tier verbatim block pointer** — Stage 3.1 brief template Section 3i (lines 163–170): `[INSERT _root/03 Section 1 — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block ...]`.
    - **QA-checklist `>` blockquote convention** — Stage 3.1 brief template Section 4 (lines 262–326): bucketed by `_root/08` section (drift-control / routing / data-pipeline / voice-content / driver-content / product-pricing-language / math-reconciliation); QB-NNN cited by number with one-line description; closing reminder that the full `_root/08` checklist is canonical.
    - **Cross-references footer** — Stage 3.1 brief template line 330: italicized closing paragraph mapping every `_root/XX §N.M` the template touches.
    - **Section blockquote convention** — Stage 3.1 brief template uses `> **Section [N][letter] — [section title].**` followed by drafter-facing instructions in indented blockquote, then the placeholder / verbatim section content. Match this convention for every section.
    - **Strict-placeholder precedent** (operator-stamped 2026-05-26) — see Step 5 below; Stage 3.1 demonstrates two specific examples (Section 3c effective-date sentence and Section 3l-continued graduated-rate string both rendered as `[INSERT _root/XX §N.M ...]` placeholders rather than inline).
    - **Section presence pattern** — Stage 3.1 brief template carries: Section 0 file header / Section 1 operator notes / Section 2 routing note / Section 3 brief content skeleton (3a subject through 3n close + formal-notice line) / Section 4 pre-send drafter checklist / cross-references footer. Match this structure; Format B inserts the additional driver coverage (3 more drivers) within Section 3f dispatch table and the additional "Your Pricing at a Glance" section already specified in Step 3 below.
    
    **What you may legitimately deviate from Stage 3.1 on** — only the Format-B-specific scope differences specified in Step 2 (driver coverage, close text per `_root/04 §4.12` Format B variant, routing-block fields per `_root/07 §7` Format B row, CEO Pre-Call → Format B variant handling, CL items addressed: CL-002 vs. CL-013, CL-012 vs. CL-011, CL-016 vs. n/a, etc.). The structural conventions above are uniform across all 4 format folders.
    
    **What was wrong in this prompt's initial draft (corrected in this delta-pass)** — the initial draft claimed the "Your Pricing at a Glance" summary table was "unique to Format B." This is incorrect — Stage 3.1's Format A template carries the same section (lines 215–230). The section appears in BOTH Format A and Format B (and likely CEO Letter and Good News too — Stage 3.3 / 3.4 will verify). When you author Format B's version, match Stage 3.1's table structure for consistency.

### Do NOT read

- Any other format folder's brief template, delivery email template, or per-account briefs (CEO Letter, Good News, entity-packets, plus the Format A archive material) — that is Stage 3.1 / 3.3 / 3.4 / 3.5 scope. Reading Format A archive material here pulls Format-A-specific patterns into the Format B template. Reading CEO Letter / Good News / entity-packet material pulls different-scope content into Format B.
- Any pre-v2 exemplar in `_archive/.../format-b-notices/` (e.g. `ih__interlude-home__brief.md` without `__v2`, `cci__currey-company__brief.md` without `__v2`, `gl__golden-lighting__brief.md` without `__v2`). The pre-v2 versions predate the S1–S7 template fixes; the v2 versions in step 17 are the clean ones.
- `_meta/stage2_prompts/**` and other `_meta/stage3_prompts/**` files — operator-process material; not relevant for Format B template building.
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material already abstracted into `_root/01`–`_root/07`. Reading them here is scope creep.
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/` (per AGENTS.md hard rules).

---

## Step 2: Authoritative Format B scope (use as fact — do not re-derive)

The planning agent verified the following against v6.2 + `_root/06` on 2026-05-22 + 2026-05-26 (CL-013 source application). Use as-is; if you believe any of it is wrong, flag in your conformance block and do not proceed.

**Format B's mechanical scope** (per `_root/06 §3`):

- Δ MRR satisfies: `$81 ≤ Δ ≤ $399`, applying the operator-stamped "higher-touch format wins" precedence rule (so a $75 / 12% account routes to Format B, not Format A; a $700 / 8% account routes to CEO Pre-Call → Format B, not standard Format B).
- AND no override fires (no entity overlay per `_root/02 §3`, no health override per `_root/02 §4`, no annual overlay timing impact per `_root/02 §5` — though annual accounts may still route to Format B's format substance with a 90-day window instead of 60).

**CEO Pre-Call → Format B's mechanical scope** (per `_root/06 §1` 5th routing pattern + `_root/06 §3` row 5):

- Δ MRR ≥ $600. CEO personally pre-engages the account by phone BEFORE CS sends the Format B brief.
- Same template as standard Format B (this template). Differs only in: (a) routing-block `CEO awareness required before send: YES`; (b) routing-block `comm_action: CEO Pre-Call → Format B`; (c) delivery email's opening adjusts to "As [CEO NAME] mentioned on [DAY]…" per the archived delivery email's operator note + `_root/04 §4.12`; (d) the brief's lede may reference the CEO conversation that preceded it.

**Format B's routing-CSV counts** (per `migration_comm_tiers_2026-05-19.csv` + `_root/06 §5`): 19 accounts carry `comm_action = Format B — Notice + Meeting Offer`; 9 accounts carry `comm_action = CEO Pre-Call → Format B`; plus an unknown number of HOLD rows whose `post_hold_action` resolves to one of those two values. Total Format-B-template usage: 28+ accounts.

**Format B's driver coverage** (per `_root/05` — 8 increase-side blocks IN scope, 3 decrease-side blocks OUT of scope):

| Driver | In scope for Format B? | Owning `_root/05` block (Format B canonical) |
|---|---|---|
| `user_rate_normalization` | YES | §2.1.2 |
| `platform_discount_correction` | YES | §2.2.2 |
| `tier_base_increase` | YES (CL-012 — secondary marker resolution flagged) | §2.3.2 |
| `included_user_reduction` | YES | §2.4.2 |
| `at_book_tier_shift` | YES (references `_root/04 §4.6` by pointer per §2.5.6 — Format B handles §4.6 as a follow-on paragraph, not inline) | §2.5.2 |
| `multi_org_retirement` | YES (CL-016 — new template carries explicit IUR-secondary templated sub-block; URN-secondary stays narrative) | §2.6.2 + §2.6.6 IUR-secondary sub-block + §4 weaving matrix |
| `annual_discount_retirement` | YES | §2.7.2 |
| `special_arrangement` | YES | §2.8.2 |
| `module_compression` (decrease-side) | NO — routes to Good News per `_root/06 §3` | n/a |
| `user_count_variance` (decrease-side) | NO — Good News only per `_root/05 §3.2` | n/a |
| `rate_architecture` (decrease-side) | NO — Good News only per `_root/05 §3.3` | n/a |

If a Stage 4 drafter encounters a Format B routing for an account whose `migration_driver` is a decrease-side value, the routing is suspect — the drafter escalates per `_root/CONTRACTS.md §2` and does not draft.

**Format B's voice-rule coverage** (per `_root/04` — every applicable subsection):

Apply at every brief: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase prohibitions, §4.2 lede stat guardrail.

Apply conditionally (with the rule's own IF condition stated in §4):

- §4.1 tenure-aware "rate was set in [YEAR]" variant (cohort-year-dependent; integrated into Format B's lede paragraph per the archived template pattern)
- §4.3 "above the midpoint" user-count clause (when applicable per the §4.3 condition; "How This Compares" section)
- §4.4 high-delta annual-dollar sentence (when Δ_pct > 30% per `_root/04 §4.4` — more common in Format B than Format A given Format B's $81–$399 scope; lede must name the annual figure)
- §4.5 operations-unchanged sentence (default OR IUR-fork variant — drafter selects based on `secondary_drivers` value; the archived Format B template surfaces this AS a conditional in the "Your Pricing at a Glance" trailer block and AGAIN in the delivery email)
- §4.6 platform-base-grown sentence (when `new_tier_base > current_platform_mrr` per `_root/04 §4.6` condition — Format B applies as a follow-on paragraph AFTER the pricing table per `_root/05 §2.5.6`; the at_book_tier_shift block invokes this, but the prose lives in §4.6, NOT in the §2.5.2 driver block)
- §4.7 early-adopter tenure paragraph (cohort year ≤ 2015 per §4.7 condition; the archived Format B template carries an explicit "ADD FOR EARLY ADOPTER COHORTS" block — the new template uses a §4.7 pointer)
- §4.8 value anchor section (when `cost_per_order < $200` per the operator-stamped 2026-05-22 threshold — **NOT $35 per CL-002**)
- §4.9 billing-basis footnote (when an excess-users line is in the pricing table — for URN and IUR drivers; per `_root/04 §4.9` does NOT apply to ABTS)
- §4.11 "How This Compares" structure (drafter judgment whether to include; if included, no peer dollar ranges per CL-003 + operator stamp, no equivalent-platforms sentence per CL-004 + operator stamp)
- §4.13 health-band lede override (when `health_band ∈ {Watch, At Risk, Critical}` — Format B uses standalone dollar sentence; though most At-Risk and Critical accounts route to Strategic per `_root/02 §4`, the rare Format-B-eligible health-flagged account uses this override)
- §4.14 discount-correction lede substitution (when `migration_driver = platform_discount_correction` — substitutes the §4.14 sentence for the standard "rate was set in [YEAR]" sentence)

Apply at every brief's close: §4.12 — Format B close text (the `Let's Talk` / meeting offer variant: "I'll reach out in the next few days to walk through this together. If you want to get ahead of that — or if you have questions before then — reply directly and we'll find time.") + the formal-notice line.

---

## Step 3: What you are authoring — file 1 of 2: `format-b-notices/_brief-template.md`

The brief template is the structural skeleton for every Format B per-account brief (standard Notice + Meeting Offer AND CEO Pre-Call → Format B variant). Stage 4 drafters at draft time:

1. Look up the account in v6.2 + run the 3 Postgres queries per `_root/07 §4`.
2. Open this template.
3. Fill in every bracketed placeholder from v6.2 + Postgres data.
4. Where the template says `[INSERT _root/05 §N.M block verbatim]`, the drafter opens `_root/05`, copies the named block character-for-character, and pastes it in place, then fills the block's own bracketed placeholders.
5. Where the template says `[INSERT _root/04 §N.M sentence/paragraph]`, same procedure against `_root/04`.
6. Apply the `_root/08` Quality Bar checklist to the completed draft before posting the conformance block.

Author the brief template as the following sections, in this order. **Every section either contains pure scaffolding (placeholders + headings) OR a §-pointer to an owning `_root/` doc. NO rule prose is inlined.**

### Section 0 — File header

```
# Format B — Notice + Meeting Offer (and CEO Pre-Call → Format B) — Brief Template
*CS-led | Meaningful delta ($81 ≤ Δ ≤ $399 standard; Δ ≥ $600 with CEO Pre-Call) | Meeting-offer close per `_root/04 §4.12`*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote block at the top of the file (removed before send) that:

- Names when to use this template (cite `_root/06 §1` and `§3`; do not restate the conditions — point to the rule). Note the dual-routing nature: standard Format B for $81–$399 deltas; CEO Pre-Call → Format B for Δ ≥ $600 with CEO pre-engagement.
- Names who sends (CS team, Kylor; cite `_root/06 §1`). Note that CEO Pre-Call → Format B variant requires CEO pre-engagement BEFORE CS sends; CEO does not sign the brief itself (that's CEO Letter).
- Names what this template is NOT for (Δ ≤ $80 / ≤10% → Format A per `_root/06 §1`; entity-children → entity packet per `_root/02 §3`; CEO Letter $400–$599 → CEO Letter format per `_root/06 §1`; decrease-side → Good News per `_root/06 §3` — point to the rule, do not restate).
- Names the cleanup-tracker history (CL-001 confirmed absent, CL-002 applied via §4.8 reference, CL-004 confirmed absent via §4.11 reference, CL-005 ADDED via Section-3 pointer, CL-012 dispatch follows §2.3.2 marker, CL-016 dispatch carries explicit IUR-secondary sub-block reference — list IDs only, link to `_meta/stage3_cleanup.md`).
- States the drafter's responsibility: every § reference in this template is to a canonical `_root/` doc. The drafter follows each reference and copies the named content verbatim into the per-account brief at draft time.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote block that mirrors the routing-block field list in `_root/07 §7` for Format B exactly. Field names and order match `_root/07 §7`; do not invent fields, do not omit fields. Bracketed placeholders for each field. Particularly important for Format B vs. Format A:

- `CEO awareness required before send: [YES for CEO Pre-Call → Format B / NO for standard Notice + Meeting Offer]` — conditional value based on `comm_action`.
- `Comm_action: [Format B — Notice + Meeting Offer / CEO Pre-Call → Format B]` from routing CSV.
- Does NOT carry `Expansion eligible` (that's Format A only per `_root/07 §7` matrix).
- Does NOT carry `CEO call commitment date` or `CEO name for sign-off` (those are CEO Letter only per `_root/07 §7` matrix).

### Section 3 — Brief content skeleton (the customer-facing body)

Sub-sections in this order:

#### 3a. Subject / greeting / brief title

Standard format: `# [ACCOUNT_NAME]: Your Pricing Is Changing` followed by `*Prepared for [ACCOUNT_NAME] | [DATE]*` per the archived template. Drafter-fillable bracketed placeholders.

#### 3b. Lede paragraph (always — health-band-conditional structure)

A bracketed instructional comment naming:

- The lede paragraph structure (cite `_root/04 §4.1` + `§4.2` + `§4.7`; do not restate). Format B's lede integrates tenure into sentence one and lands the dollar change in the same paragraph.
- The conditional skip for Watch / At Risk / Critical (cite `_root/04 §4.13`) — for these accounts, open with the standalone dollar sentence and omit the relationship-stats lede.
- The high-delta annual-dollar sentence (cite `_root/04 §4.4`) — when `Δ_pct > 30%`, the lede MUST name the annual figure alongside the monthly change.
- The `_root/01 §1` relationship-before-price principle as the lede's organizing principle.
- A pointer to the v6.2 columns the drafter pulls from: `cohort_year`, `composite_narrative`, Postgres-derived `active_org_users` / `logged_in_90d` / `ltm_orders` (per `_root/07 §2` + `§4.2` + `§4.3`).
- Bracketed placeholders for the actual prose the drafter writes (the lede is drafter-generated per `_root/04 §4.1`, not pulled from a `_root/` block — the drafter writes a 2–3 sentence lede tuned to the specific account).

#### 3c. Consolidated 2026 framing sentence + tenure-aware variant + driver-substitution variant

Standard sentence per `_root/04 §3` row on the consolidated 2026 sentence: "In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you." Drafter pastes verbatim from `_root/04 §3`. Then a conditional `[IF cohort_year ≤ X | IF cohort_year between Y and Z | etc.]` selector pointing to `_root/04 §4.1` for the tenure-aware "rate was set in [YEAR]" variants. Drafter selects the variant based on `cohort_year` from v6.2 and pastes verbatim. The template does NOT inline any of these sentences.

**Conditional substitution for `platform_discount_correction` accounts**: drafter-facing `[IF migration_driver = platform_discount_correction]` selector pointing to `_root/04 §4.14` for the substitute sentence ("Your rate reflects a discount applied at signing that's being retired as part of this change."). Drafter substitutes this sentence FOR the "rate was set in [YEAR]" sentence when applicable. The template references §4.14; does NOT inline.

#### 3d. Early-adopter tenure paragraph (conditional)

Drafter-facing `[IF cohort_year ≤ 2015]` selector pointing to `_root/04 §4.7` for the early-adopter tenure paragraph. Drafter pastes verbatim from §4.7. The template does NOT inline. (The archived Format B template inlines this as an "ADD FOR EARLY ADOPTER COHORTS" block; the new template replaces with a §-pointer.)

#### 3e. "Why the Number Is Changing" section header + driver dispatch

Section heading: `## Why the Number Is Changing`. Then a drafter-facing `[DRIVER DISPATCH]` block:

```
[DRIVER DISPATCH — select ONE based on v6.2 `migration_driver` value; reject if not listed]:

| v6.2 `migration_driver` | Insert _root/05 block verbatim from | Conditional sub-blocks + secondary handling | Notes |
|---|---|---|---|
| `user_rate_normalization` | _root/05 §2.1.2 | §2.1.6 (conditional context paragraphs incl. _root/04 §4.10 platform-base conditional) + §2.1.7 (secondary-driver integration) | Format B canonical block. |
| `platform_discount_correction` | _root/05 §2.2.2 | §2.2.6 + §2.2.7 | Format B canonical. |
| `tier_base_increase` | _root/05 §2.3.2 | §2.3.6 + §2.3.7 | Format B canonical. CL-012: the §2.3.2 secondary-marker `[IF secondary driver = …]` reflects whatever marker `_root/05 §2.3.2` currently carries — drafter follows §2.3.2 verbatim. |
| `included_user_reduction` | _root/05 §2.4.2 | §2.4.6 + §2.4.7 | Format B canonical. |
| `at_book_tier_shift` | _root/05 §2.5.2 | §2.5.6 (incl. `_root/04 §4.6` follow-on paragraph when `new_tier_base > current_platform_mrr`; OMITTED when base moves down per kii special case) + §2.5.7 | Format B canonical. The §4.6 sentence is a separate follow-on paragraph, not inlined in §2.5.2. |
| `multi_org_retirement` | _root/05 §2.6.2 + §2.6.6 (CL-016 IUR-secondary sub-block) + §4 (weaving matrix) | §2.6.7 | Format B canonical. CL-016: when `secondary_drivers` includes `included_user_reduction` (6 v6.2 accounts), the drafter ALSO inserts the §2.6.6 IUR-secondary templated sub-block. When `secondary_drivers` includes `user_rate_normalization` (2 v6.2 accounts), the drafter integrates per-account narrative per the kii / da exemplar patterns documented in §4. |
| `annual_discount_retirement` | _root/05 §2.7.2 | §2.7.6 + §2.7.7 | Format B canonical. |
| `special_arrangement` | _root/05 §2.8.2 | §2.8.6 + §2.8.7 | Format B canonical. Operator note from archived template: for SA accounts with Δ > 30%, confirm account history with Finance before outreach; CEO must be prepared to answer the "what was the arrangement and why is it changing?" question. This is operator-facing, not customer-facing — cite as a drafter note pointing to `_root/05 §2.8` definition. |
| `module_compression` | NOT carried in Format B | n/a | Decrease-side; routes to Good News per `_root/06 §3` row 1. If routing produces this driver in Format B, escalate per `_root/CONTRACTS.md §2`. |
| `user_count_variance` | NOT carried in Format B | n/a | Decrease-side; Good News only. |
| `rate_architecture` | NOT carried in Format B | n/a | Decrease-side; Good News only. |
```

After the dispatch table, an instructional `[INSERT_DRIVER_BLOCK]` placeholder where the drafter pastes the verbatim block(s) from the selected `_root/05 §N.M`. The template does NOT inline any of the 8 driver-prose blocks.

#### 3f. Pricing-table row template (per driver)

A drafter-facing instruction pointing to `_root/05 §N.M`'s pricing-table row template for the selected driver. The template does NOT inline pricing-table row structures (each driver has its own per `_root/05 §2.1.5`, `§2.2.5`, `§2.3.5`, `§2.4.5`, `§2.5.5`, `§2.6.5`, `§2.7.5`, `§2.8.5` — all rendered as fenced code blocks in `_root/05` because the driver-prose blockquotes contain markdown special chars).

#### 3g. "What You're Getting at $[NEW_MRR]/Month" tier block

Section heading: `## What You're Getting at $[NEW_MRR]/Month`. Then `[INSERT _root/03 Section 1 — [T1 | T2 | T3] verbatim block — verbatim, with [NEW_INCLUDED] and any other bracketed tokens filled from v6.2 \`new_included_users\` and \`assigned_tier\`]`. Drafter pastes the canonical block from `_root/03 Section 1` selected by tier; the template does NOT inline the tier blocks.

If the account's `new_user_charge` reflects users above the included base, append the `_root/04 §4.9` billing-basis footnote pointer.

#### 3h. "What This Works Out To" value-anchor section (conditional)

Section heading (conditional): `## What This Works Out To`. Drafter-facing instruction: `[IF derived metric \`cost_per_order < $200\` per _root/04 §4.8 (operator-stamped 2026-05-22; **NOT $35 — CL-002 cleanup**): include the value-anchor section using _root/04 §4.8 structure. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.8` exactly. The template does NOT inline `_root/04 §4.8`'s structure; it points. Drafter computes `cost_per_order` per `_root/07 §4.4`. The §4.8 structure also handles the conditional second sentence (delta-per-order reframe when `delta_per_order < $50`).

#### 3i. "What's Coming in 2026" verbatim block

Section heading: `## What's Coming in 2026`. Then `[INSERT _root/03 Section 3 verbatim block — verbatim, no substitution]`. Drafter pastes the canonical block from `_root/03 Section 3`. **This is CL-005's application in Format B**: the archived Format B template OMITS this section entirely; the new template ADDS it via the Section-3 pointer per operator decision Q4 2026-05-22 (mandatory in all 4 formats).

#### 3j. "How This Compares" section (conditional, drafter-judgment)

Section heading (conditional): `## How This Compares`. Drafter-facing instruction: `[IF drafter judgment + _root/04 §4.11 indicates this section adds clarity for the account: include the section using the structure in _root/04 §4.11. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.11` exactly:

- No peer dollar ranges (per CL-003 + operator stamp 2026-05-22 universal — the archived Format B template already strips these correctly).
- No "equivalent platforms range from $X–$Y" sentence (per CL-004 + operator stamp 2026-05-22 universal).
- No "no account-specific adjustments" sentence (per CL-001 + `_root/04 §3` row).
- Use the plain-English position vocabulary from `_root/04 §4.11`.
- Apply the `_root/04 §4.3` "above the midpoint" clause when applicable.

The template does NOT inline `_root/04 §4.11`'s structure; it points. Use the archived Format B template's `[GUIDANCE]` discipline pattern as the scaffolding model — but the actual guidance text comes from `_root/04 §4.11` and `_root/04 §3`, not from the archived block.

#### 3k. "Your Pricing at a Glance" summary table

Section heading: `## Your Pricing at a Glance`. **This section appears in both Format A and Format B** (and the planning agent expects it in CEO Letter and Good News too — Stage 3.3 / 3.4 will verify; the initial draft of this prompt incorrectly claimed it was "unique to Format B"). Match Stage 3.1's Format A table structure (`format-a-notices/_brief-template.md` Section 3l-continued, lines 215–230) for cross-format consistency. The table structure is:

```
| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | $[LEGACY_RATE]/user | [INSERT `_root/03 §2 Block A` graduated-rate summary string verbatim — e.g. "Graduated ($25/$22/$20/$18)" per current §2 Block A canonical values] |
```

The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Drafter values come from v6.2 + Postgres per `_root/07 §2` + §4 — EXCEPT the "Additional user rate" after-column, which is a placeholder pointing to `_root/03 §2 Block A` per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass). Match Stage 3.1's table form exactly; the only Format-B-specific variation is the row data itself (since Format B handles 8 drivers vs. Format A's 6, some Format B `LEGACY_RATE_DESCRIPTION` strings may differ in structure from typical Format A rate descriptions).

#### 3l. Operations-unchanged paragraph + IUR fork

Drafter-facing instruction: `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless v6.2 \`secondary_drivers\` includes \`included_user_reduction\`; in that case, INSERT _root/04 §4.5 IUR-fork variant.]` The template does NOT inline either variant; both live in `_root/04 §4.5`.

#### 3m. Close paragraph (Format B `Let's Talk`)

Section heading: `## Let's Talk` (per `_root/04 §4.12` Format B variant). Then `[INSERT _root/04 §4.12 Format B close text — verbatim, meeting-offer variant]`. Then the formal-notice line per `_root/04 §4.12` — `[INSERT _root/04 §4.12 formal-notice line verbatim, with [EFFECTIVE_DATE] filled in]`. Drafter pastes both from `_root/04 §4.12`. The template does NOT inline either.

**Conditional adjustment for CEO Pre-Call → Format B variant**: if `comm_action = "CEO Pre-Call → Format B"`, the close may be adjusted to acknowledge the CEO conversation that preceded (per the archived delivery email's operator note + `_root/04 §4.12`). The adjustment is per-account narrative — the §4.12 verbatim close is still the canonical close text.

#### 3n. Signature

Standard signature: `[CSM NAME] | Customer Success | SuperCat` + `[DATE]`. Drafter-fillable.

### Section 4 — Pre-send drafter checklist (drafter-facing, removed before sending OR retained as conformance evidence)

A short `>` blockquote pointing to `_root/08` for the full 126-check QA layer. Name 6–10 of the most Format-B-specific blocker checks by QB-NNN for drafter convenience (e.g. QB-002 conformance block, QB-046 "What's Coming in 2026" present, QB-077 above-the-midpoint clause, QB-078 high-delta annual-dollar, QB-082 value-anchor `cost_per_order < $200` threshold, QB-085 no peer dollars, the QB-NNN for IUR-fork dispatch, the QB-NNN for §4.6 follow-on paragraph application). Do NOT restate any check; cite the QB-NNN and `_root/08`.

---

## Step 4: What you are authoring — file 2 of 2: `format-b-notices/_delivery-email-template.md`

The delivery email template is the cover email that wraps the completed brief at delivery time. Short structure. The drafter sends this email with the brief attached. Variants for: (a) standard Format B Notice + Meeting Offer; (b) CEO Pre-Call → Format B follow-up email (CEO has already called; CS sends the email after the call).

Author the delivery email template as the following sections, in this order:

### Section 0 — File header

```
# Format B — Delivery Email Template
*60-Day Notice | CS-sent | Wraps the Format B brief; includes CEO Pre-Call follow-up variant*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote naming:

- When to use (delta is Format B's scope per `_root/06 §3` standard or CEO Pre-Call variant; the brief does the heavy lifting; this email is the wrapper).
- Who sends (CS, with CEO awareness only for CEO Pre-Call variant, per `_root/06 §1`).
- Length: standard variant 4–5 sentences; CEO Pre-Call follow-up variant 4–6 sentences (opens by referencing the CEO conversation).
- What is NEVER in this email (cite `_root/04 §3` rows — minimizing language, apologies, percentage in the lede, "modest/small/minor", expansion language, upgrade mentions). Do not restate the prohibitions; cite the §3 rows.
- Variant routing instructions: standard Format B uses the default body; CEO Pre-Call → Format B opens with "As [CEO NAME] mentioned on [DAY]…" and drops the "I'll reach out" close (the CEO call already happened). Cite `_root/04 §4.12` Format B close + the archived delivery email's variant notes.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote mirroring the routing-block field list in `_root/07 §7` for Format B's delivery email. **Note: `_root/07 §7` enumerates the canonical brief routing-block matrix, but does NOT yet separately specify the delivery email's slim subset (CL-022 filed 2026-05-26 — Stage 3.1 fresh agent surfaced the gap; rule-layer extension scheduled for Wave 6 batch after all 4 Stage 3 templates land).** Until CL-022 lands, infer the delivery email slim subset from: (a) Stage 3.1's `format-a-notices/_delivery-email-template.md` Section 2 (lines 27–42 in the approved template) — Format A established the precedent slim-subset pattern; (b) the archived Format B delivery email's routing block (`_archive/.../format-b-notices/_delivery-email-template.md` lines 6–12); (c) the brief's full routing block per Step 3 Section 2 above. Cross-reference all three and produce a slim block that includes: Brief type, Account / Tier / Wave, Migration driver / Health, Current MRR / New MRR / Delta, Cohort / Contract / Renewal, Earliest enforceable effective date, Attachment, `CEO awareness confirmed before send: [YES/NO]`, plus Format-B-specific conditional rows. Flag in your conformance block that the slim subset is inferred per CL-022's pending rule-layer extension; the planning agent decides whether to amend `_root/07 §7` now or accept the inference as Wave 6 cleanup material.

### Section 3 — Email body skeleton (standard Format B)

Standard fields:

- `**Subject:** [ACCOUNT NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]`
- `Hi [CONTACT NAME],`
- Sentence 1: drafter writes the dollar-change effective-date sentence per `_root/04 §4.13` (leads with dollars per `_root/04 §3` no-percentage-in-lede rule). For Δ_pct > 30%, the sentence MUST name the annual figure per `_root/04 §4.4`.
- Sentence 2: drafter-facing note + `_root/04 §4.1` tenure-variant pointer (the archived delivery email's "Your rate was set in [YEAR] — this is the first time we've updated it" sentence is a tenure variant per §4.1, not a unique delivery-email sentence). For `platform_discount_correction` accounts, substitute the §4.14 sentence per §4.14 rule. Template references; does NOT inline.
- Sentence 3: `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless secondary_drivers includes included_user_reduction; in that case INSERT IUR-fork variant.]` Same selector as brief Section 3l.
- Sentence 4: drafter writes a brief meeting-offer sentence echoing `_root/04 §4.12` Format B close register (the email's offer is a short echo of the brief's `Let's Talk` close — NOT a new commitment).
- Signature: `[CSM NAME] | Customer Success | SuperCat`

### Section 4 — Email body variant (CEO Pre-Call → Format B)

A conditional `[IF comm_action = "CEO Pre-Call → Format B"]` selector that swaps the body's opening:

- Sentence 1 (variant): drafter writes a sentence referencing the CEO conversation: "As [CEO NAME] mentioned on [DAY], your monthly invoice is moving from $[CURRENT_MRR] to $[NEW_MRR] — effective [EFFECTIVE_DATE]." Drafter-facing template; cites `_root/04 §4.12` for the variant register.
- Sentences 2 and 3 remain as in the standard body.
- Sentence 4 (variant): drops the "I'll reach out" meeting offer (CEO call already happened); instead drafter writes a one-sentence offer to follow up on any unanswered questions from the CEO call. Drafter-facing template.

The template does NOT inline either variant's prose beyond the structural skeleton; rule references point to `_root/04 §4.12` and `_root/04 §4.5`.

### Section 5 — Pre-send checklist (drafter-facing)

Short `>` blockquote pointing to `_root/08` for the relevant QB-NNN checks. Cite QB-NNN; do not restate. Include the archived template's checklist items (attach brief PDF; follow through within 3 business days; never adjust effective date without updating brief) as drafter-process notes, cited to `_root/06 §1` and `_root/07 §6` rather than freshly authored.

### Section 6 — Voice calibration notes (drafter-facing)

A short closing paragraph pointing to `_root/04 §4.12` for the email's voice calibration (zero friction; the brief does the heavy lifting; if you're writing more than 5 sentences, you've crossed into CEO Letter territory). Cite the rule; do not restate.

---

## Step 5: Anti-drift discipline

- **The path-reference contract is absolute — strict-placeholder precedent operator-stamped 2026-05-26.** Every rule the template needs to enforce is referenced by `_root/XX §N.M`, never inlined. The template's content is scaffolding + pointers; the rule prose stays in its owning `_root/` doc. If you find yourself pasting a sentence from `_root/03`, `_root/04`, `_root/05`, `_root/06`, or `_root/07` into the template, stop — you are introducing drift. **This applies even to short sentences with only bracketed-token substitutions**: the Stage 3.1 review pass surfaced two such inlines (the `_root/04 §4.13` effective-date sentence and the `_root/03 §2 Block A` graduated-rate string) and the operator stamped STRICT — both became placeholders. Follow the same precedent here: any prose owned by a `_root/` doc, no matter how short, is a `[INSERT _root/XX §N.M ...]` placeholder, never an inline. The cost is one extra fetch step at draft time; the benefit is the path-reference contract holding end-to-end.
- **The ONLY content the template inlines** is: (a) drafter-facing instructions / blockquote scaffolding; (b) section headings and table column / row layouts; (c) `[ALL_CAPS_TOKEN]` placeholders for v6.2 + Postgres data the drafter substitutes; (d) `[INSERT _root/XX §N.M ...]` placeholders for rule prose the drafter fetches; (e) structural bridge sentences that have NO owning `_root/` rule (e.g. the Stage 3.1 transition sentence "Below is exactly why your number is changing and what you're getting at the new price." — operator-stamped 2026-05-26 as durable template scaffolding rather than promoted to a `_root/` rule). If you encounter a bridge sentence in the archived Format B template that has no owning `_root/` rule, treat it as scaffolding only if it appears verbatim across all Format B v2 exemplars (ih, cci, gl) AND the archived template. Otherwise, flag in your conformance block — the planning agent decides whether to promote to a `_root/` rule or accept as scaffolding.
- **The 8 driver-prose blocks live in `_root/05`.** The template's "Why the Number Is Changing" section is a driver dispatch table that names which `_root/05 §N.M` block applies for each `migration_driver` value. The block prose itself is fetched by the drafter at draft time, not inlined here.
- **CL-002 is the single most important Format-B-specific cleanup.** The archived Format B template's value-anchor threshold is `cost_per_order ≤ $35`. The new template uses `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22 universal). Verify when you read `_root/04 §4.8` that the threshold is $200; if you find $35, STOP — the rule layer was not updated and the cleanup cannot proceed.
- **CL-005 is additive.** The archived Format B template does NOT carry a "What's Coming in 2026" section. The new template ADDS one via a `_root/03 Section 3` pointer per operator decision Q4 2026-05-22 (CL-005). This is the most additive change.
- **CL-016 is operator-stamped.** The new Format B template's `multi_org_retirement` dispatch row directs the drafter to `_root/05 §2.6.2` + `§2.6.6` IUR-secondary sub-block + `§4` weaving matrix. When `secondary_drivers` includes `included_user_reduction`, the drafter inserts the §2.6.6 IUR-secondary templated sub-block (covers 6 v6.2 accounts). When `secondary_drivers` includes `user_rate_normalization`, the drafter applies per-account narrative integration per the kii / da exemplar patterns documented in `_root/05 §4` (covers 2 v6.2 accounts). The template's dispatch row names both paths.
- **CL-012 is a flagged unresolved.** The `_root/05 §2.3.2` secondary-driver marker may be miscoded as URN when it should be IUR. The template references whatever `_root/05 §2.3.2` currently carries; the resolution belongs to `_root/05`, not to this template. Flag in your conformance block what marker §2.3.2 currently has.
- **CL-001, CL-003, CL-004 are universal.** No "no account-specific adjustments" sentence (the archived Format B template already omits it — preserve absence), no peer dollar ranges (archived already strips), no equivalent-platforms sentence (archived already forbids via `[GUIDANCE]`). Reference `_root/04 §3` rows and `_root/04 §4.11`; do not invent new "How This Compares" prose.
- **The drafter is the integration point, not the template.** Drafters at draft time fetch verbatim blocks from `_root/`, fill in placeholders from v6.2 + Postgres, and apply conditional rules. The template's job is to tell the drafter what to fetch and where to put it; it does NOT pre-fill what the drafter fetches.
- **No new operator-policy decisions.** If you discover that a rule in `_root/` is ambiguous for Format B's use case, flag in your conformance block. Do NOT pick an interpretation and bake it into the template.
- **No new Format B scope.** Format B handles 8 increase-side drivers per Step 2 + CEO Pre-Call variant. Do NOT extend coverage to decrease-side drivers even if you think Format B "should" carry them — that is a Stage 3 cleanup item to file via your gaps list, not a template change.
- **Asking is cheap. Inventing is the drift vector.**

---

## Step 6: Voice and format constraints

- Register for operator-notes and drafter-facing instructions: declarative, no marketing language. Same register as `_root/02`, `_root/04`, `_root/06`, `_root/07`. Use `>` blockquote for every drafter-facing block (matching the archived template's convention).
- Use clean Markdown structure: `#` for the file title, `##` for the customer-facing brief sections, `###` for sub-sections inside drafter-facing blocks. Bracketed placeholders use the `[ALL_CAPS_WITH_UNDERSCORES]` convention from the archived template (e.g. `[ACCOUNT_NAME]`, `[NEW_MRR]`, `[EFFECTIVE_DATE]`, `[CSM NAME]`).
- The customer-facing sections of the brief template should READ AS A BRIEF when the drafter fills in placeholders — the template's bracketed instructions are the scaffolding, and the resulting brief (after placeholder fill + `_root/` block insertion) reads as a coherent customer communication.
- No emoji. No "Importantly" / "Critically" — the QB-NNN severity in `_root/08` is the operational signal of importance.
- For dual-routing-pattern fields in the routing block + delivery email body, use a clear `[IF comm_action = "X" / IF comm_action = "Y"]` syntax that mirrors the archived template's conditional convention.

---

## Step 7: Output

Replace nothing — both files are NEW.

Create the new folder + both files:

- `Pricing Migration/format-b-notices/_brief-template.md` (the brief template)
- `Pricing Migration/format-b-notices/_delivery-email-template.md` (the delivery email template)

The folder `Pricing Migration/format-b-notices/` does not exist yet (the prior folder was moved to `_archive/2026-05-22__pre-refactor/format-b-notices/` during the 2026-05-22 refactor); your authoring creates the folder.

Then, in your chat reply (NOT in the files), produce this conformance block per `_root/00_manifest.md §5`:

```
─── Conformance Block ─────────────────────────────────────────
Session task: Stage 3.2 — author format-b-notices/_brief-template.md + _delivery-email-template.md
Output target:
- Pricing Migration/format-b-notices/_brief-template.md (NEW file, NEW folder)
- Pricing Migration/format-b-notices/_delivery-email-template.md (NEW file)

Files read (with last-updated date / mtime):
- <enumerate every file path from Step 1 with last-updated date or mtime>

Explicitly-authorized archive reads (per Stage 3.2 §1 items 15–17):
- <list every archived file you read with mtime>

Pattern-reference read (Step 1 item 18 — optional):
- <"Stage 3.1's format-a-notices/_brief-template.md was [present / absent] at read time. If present, consulted for: [structural conventions]. Did NOT lift content from.">

Files NOT read:
- <enumerate per Step 1 "Do NOT read">

Brief template sections authored: <count + names — should match Step 3's section list>
Delivery email template sections authored: <count + names — should match Step 4's section list>

Drivers covered in brief template (per the dispatch table in 3e):
- In scope (8): <list with §-pointer for each>
- Out of scope (3 decrease-side): <list with §-pointer for each>

CL items addressed (with the specific template element that addresses each):
- CL-001: <where in the template — should be "confirmed absent; _root/04 §4.11 structure prevents reintroduction">
- CL-002: <where — should be "value-anchor section 3h references _root/04 §4.8 ($200 threshold), NOT $35">
- CL-004: <where — should be "How This Compares section 3j references _root/04 §3 row on competitor-pricing prohibition">
- CL-005: <where — should be "Section 3i ADDS What's Coming in 2026 verbatim block via _root/03 Section 3 pointer (new in Format B template)">
- CL-012: <where — should be "tier_base_increase dispatch row in 3e references _root/05 §2.3.2 verbatim marker; current state of marker reported below">
- CL-016: <where — should be "multi_org_retirement dispatch row in 3e references _root/05 §2.6.2 + §2.6.6 IUR-secondary sub-block + §4 weaving matrix">

CL-012 marker state when read (operator-facing observation):
- `_root/05 §2.3.2` secondary-driver marker currently reads: <verbatim quote of the marker text>
- This <does / does not> match the IUR-style integrated sentence in the block, suggesting the marker <is correctly labeled IUR / should be IUR but is mis-labeled URN>.
- Recommended action: <"file as resolved if marker is IUR" or "escalate as `_root/05 §2.3.2` rule-change-protocol fix if marker still says URN">.

Path-reference contract verification:
- Number of verbatim rule blocks INLINED in the template (should be 0 — if non-zero, list each and explain why it could not be referenced): <count + list or "0">
- Number of §-pointers TO _root/ docs in the template: <count by owning doc — e.g. "_root/03: 3, _root/04: ~14, _root/05: 11, _root/06: ~5, _root/07: ~3, _root/08: ~8">
- Number of bracketed placeholders for drafter data fill-in (per v6.2 + Postgres): <count>

Verbatim text the template DOES carry (template scaffolding only — NOT rule prose):
- <list: e.g. "operator-notes blockquote header style (drafter-facing, not a rule)", "internal routing-note block (drafter-facing metadata, per _root/07 §7)", "section heading text like 'Why the Number Is Changing' (drafter-facing structure, not a rule)", "bracketed placeholders like [ACCOUNT_NAME] (drafter-facing fill points)", "Your Pricing at a Glance summary table structure (Format-B-specific brief structure carried from archive, not a _root/ rule)">

Routing-block field list cross-check (per _root/07 §7 Format B matrix):
- <confirm every required field is present in the template's routing block; flag any divergence; particularly confirm CEO awareness conditional handling for standard Notice + Meeting vs. CEO Pre-Call → Format B>

CEO Pre-Call → Format B variant handling:
- <confirm the brief template handles the variant via routing-block flag + drafter-narrative adjustment, not via a separate template>
- <confirm the delivery email template carries explicit variant body per Step 4 Section 4>

Gaps surfaced (a Format B scope element that has no _root/ rule, OR a _root/ rule that the template cannot enforce structurally):
- <list, or "none">

Conflicts between sources (and chosen resolution / flag):
- <list, e.g. "the archived Format B template's value-anchor threshold ($35) vs. _root/04 §4.8 threshold ($200) — resolution: _root/04 §4.8 wins per CONTRACTS §5; CL-002 cleanup applied", or "none">

Open questions for operator:
- <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file (do not edit `_root/`, do not edit other format folders, do not edit `_meta/stage3_cleanup.md`, do not edit the Format A template if it exists). The operator will paste your output back to the planning agent for review before Stage 3.3.

---

## Step 8: If something is missing or contradictory

- A `_root/04` voice rule that Format B should enforce but is not yet authored → flag in your conformance block; the planning agent decides whether to author the rule via the `_root/CONTRACTS.md §3` rule-change protocol before you proceed.
- A `_root/05` driver block that the dispatch table says Format B carries but is not yet authored in `_root/05` → flag; do not invent the block.
- A `_root/07 §7` routing-block field list that does not match what Format B briefs actually need → flag both versions; do not pick one.
- A conflict between the archived Format B template's S1–S7 fixes and the current `_root/04` voice rules → `_root/04` wins per `_root/CONTRACTS.md §5`. The archived template's drift is the reason for the rebuild.
- A conflict between two `_root/` docs (e.g. `_root/04 §4.12` close text vs. `_root/06 §1` Format B close description) → flag the conflict; do not pick one. The planning agent resolves via the rule-change protocol.
- A driver an exemplar brief (ih v2, cci v2, gl v2) renders that the new template's dispatch table does not name → flag; the exemplar may be using forbidden phrasing or improvised integration.
- A field the prior template's routing block carried that `_root/07 §7` does not name → flag; either `_root/07 §7` is missing the field (and needs an update via rule-change protocol) or the prior template carried scope creep.
- CL-012: if `_root/05 §2.3.2` still carries the URN marker but the integrated sentence reads as IUR, flag the discrepancy in your conformance block with the verbatim marker text and a recommended resolution. Do NOT pick a marker yourself — the resolution belongs to `_root/05 §2.3.2`, not to this template.
- Anything in the cleanup tracker that you cannot translate into a template element → flag; the planning agent decides.

**Asking is cheap. Inventing is the drift vector.**
