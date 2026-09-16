# Stage 3.3 — Authoring Prompt for `ceo-letter-notices/_brief-template.md` + `_delivery-email-template.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by planning agent (drafted in parallel with Stage 3.1 + Stage 3.2). **Delta-pass applied 2026-05-26** after Stage 3.2 operator approval: (a) pattern-inheritance references in Step 1 item 18 now span both Stage 3.1 (`format-a-notices/`) and Stage 3.2 (`format-b-notices/`); (b) CL-012 + CL-016 carry-through language updated to reflect RESOLVED status (source fixes applied at `_root/05 §2.3.2 + §2.3.3` and `_root/05 §2.6.2 + §2.6.3` during Stage 3.2 review pass — the fresh agent now pastes `_root/05 §2.3.3` and `_root/05 §2.6.3` as-written without second-guessing markers); (c) subject-line convention normalized to "your SuperCat **pricing** is changing" across all 4 formats per operator stamp 2026-05-26 (Stage 3.1 Format A delivery email subject was edited from "invoice" to "pricing" in lockstep — this prompt's Section 3 subject line is already correct).
> **Output target**: TWO new files under a NEW folder at `Pricing Migration/ceo-letter-notices/`:
>   - `ceo-letter-notices/_brief-template.md` (the structural skeleton for every CEO Letter per-account brief — CEO-authored / CEO-signed; CS executes delivery; specific call-commitment date within 5 business days of send)
>   - `ceo-letter-notices/_delivery-email-template.md` (the cover email that wraps every CEO Letter brief at delivery; CEO is the sender; CS prepares but CEO reviews and personalizes before send)
> **Estimated authored length**: brief template 450–600 lines (CEO Letter carries 8 driver blocks like Format B, plus a more elaborate lede structure with integrated tenure + call commitment per `_root/04 §4.1` + `§4.4` + `§4.7` + `§4.12`, plus the "Your Pricing at a Glance" summary table, plus the CEO-specific "I'll Call You" close section); delivery email template 100–140 lines (4–6 sentences; CEO is named as the sender; CEO awareness flag is `YES (always)`).
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all authored and operator-stamped); CL-013 cleanup applied at `_root/05 §2.5.4` source 2026-05-26 (the source-level fix; CEO Letter ABTS at `_root/05 §2.5.3` already used the §4.6-as-follow-on pattern, so the source fix preserves CEO Letter's existing pattern and updates the cross-reference paragraph in §2.5.6). Independent of Stage 3.1 / 3.2 / 3.4 / 3.5. **Pattern inheritance from Stage 3.1**: if `format-a-notices/_brief-template.md` exists in your read environment at the time you author, you may consult it for structural-convention reference only (operator-notes header style, dispatch-table format, QA-checklist citation style, strict-placeholder precedent rendering). Do NOT lift Format A driver content, Format A close text (passive offer — wrong format for CEO Letter), Format A routing-block fields (no `Expansion eligible`; no `CEO call commitment date`), or Format A signature block (CSM, not CEO).

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `ceo-letter-notices/_brief-template.md` is the structural skeleton every Stage 4 per-account drafting agent fills in to produce a CEO Letter brief for accounts whose Δ MRR satisfies `$400 ≤ Δ ≤ $599` (per `_root/06 §3` row 4 + `_root/02 §2` $400 ownership boundary). The brief is CEO-authored — Mike signs it personally and personalizes the lede; CS prepares the draft and executes delivery once CEO approves. The companion `_delivery-email-template.md` is the cover email that the CEO sends from his own email, wrapping the completed brief at delivery time.

Your job is to **author two new template files that reference `_root/` rules by §-number and never restate them.** This is the single most important discipline of this entire task. Every voice rule, every forbidden phrase, every driver-prose block, every routing condition, every quality check lives in exactly one `_root/` doc. The templates carry only:

- **Drafter-facing structural scaffolding** — the operator-notes blockquote header, the routing block format (with CEO-specific fields per `_root/07 §7`), the section headings (including the CEO Letter-specific "I'll Call You" close section per `_root/04 §4.12`), the bracketed placeholders the drafter fills in from data, the pricing-table row template structure, the "Your Pricing at a Glance" summary table structure carried from the archived CEO Letter template.
- **Lookup instructions** — pointers like `[INSERT _root/05 §2.1.3 — CEO Letter canonical block for user_rate_normalization — verbatim, with [BRACKETED_TOKENS] filled from v6.2 + Postgres data per _root/07 §4]`. The drafter at draft time copies the verbatim block from the owning `_root/` doc into the brief; the template does not carry the prose.
- **Conditional flow logic** — `[IF migration_driver = X: use block A | IF migration_driver = Y: use block B]`, plus the CEO-Letter-specific `[IF health_band ∈ {Watch, At Risk}: call commitment moves to second sentence per _root/04 §4.13]` selector. The conditions reference v6.2 columns by name (per `_root/07 §2`); the resulting block is a pointer to `_root/05 §N.M` or `_root/04 §N.M`, not inline prose.

If you find yourself about to paste verbatim prose from `_root/03`, `_root/04`, or `_root/05` into the template, **stop**. That is exactly the drift the path-reference contract (`_root/CONTRACTS.md §5`) was written to prevent. The template carries the lookup; the prose stays in its owning doc.

The cost of a single inlined rule is a template that quietly diverges from the rule layer the next time the rule is edited. The cost of "the template is harder to read because of all the §-pointers" is one extra read step per drafter per brief. The former is unrecoverable drift; the latter is a five-second cost. The discipline is non-negotiable.

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will not extend the template's scope beyond what `_root/06 §1` defines CEO Letter to be (the CEO-authored variant for the $400–$599 Executive segment; the $400 ownership boundary is owned by `_root/02 §2`). You will reference what exists in `_root/` and render the template precisely.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date (from each file's header block where present) in the conformance block of your final reply.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` — the operator contract, agent contract, rule-change protocol, anti-archive rule with explicit-extraction exception, path-reference contract.
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. **Particularly important entries for CEO Letter**: Wave 1 (peer-dollars universal-strip + competitor-pricing broadening; both stamped 2026-05-22 and both apply to CEO Letter's "How This Compares" section — the archived CEO Letter brief template `_archive/.../ceo-letter-notices/_brief-template.md` line 232 carries the operator-stamped CL-001 forbidden sentence "there are no account-specific adjustments in how your number was calculated" inside the "How This Compares" section; the new template MUST NOT carry it); Wave 2 (Q4 — "What's Coming in 2026" landed in ALL formats including CEO Letter, which the archived CEO Letter template does NOT yet carry); Wave 3 operator-stamping pass (CL-016 stamped: extend Format B + **CEO Letter** templates with explicit `[IF secondary driver = included_user_reduction]` sub-block under `multi_org_retirement`); Wave 4 (the `_root/05 §1.1` arithmetic correction); **Stage 3 prep 2026-05-26 (CL-013 applied at `_root/05 §2.5.4` source — for CEO Letter this means §2.5.6 was rewritten to say "all three formats reference `_root/04 §4.6` by pointer," which preserves CEO Letter's existing follow-on-paragraph pattern but updates the cross-reference language)**; **Stage 3.1 review pass 2026-05-26 (Format A templates approved; CL-018–CL-022 filed; strict-placeholder precedent operator-stamped for ALL Stage 3 templates — applies uniformly to CEO Letter)**; **Stage 3.2 review pass 2026-05-26 (Format B templates approved; CL-012 source fix at `_root/05 §2.3.2 + §2.3.3` — secondary-driver marker amended from URN to IUR; CL-016 source fix at `_root/05 §2.6.2 + §2.6.3` — `[IF secondary driver = included_user_reduction]` templated sub-block added to MOR primary block; subject-line normalized to "pricing" across all 4 formats; CL-023 filed for v6.2 re-evaluation of TBI+URN rows under the amended marker — applies directly to CEO Letter's §2.3.3 and §2.6.3 which carry the source fixes in lockstep)**.

### The rule layer — read in FULL (these are the rules the new template references)

6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` — the strategic register. Few mechanical rules; sets the tone every CEO Letter brief operates inside. **For CEO Letter specifically**: §1's relationship-before-price principle is the lede's organizing principle, and the CEO Letter's lede integrates it more explicitly than Format A/B (CEO is writing peer-to-peer to a buyer the company has had a multi-year relationship with).
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — segments, ownership boundary, overlays, errata, 109/107/2 reconciliation. **For CEO Letter specifically**: §1 Executive segment (`$401 ≤ Δ ≤ $600`, healthy, standalone; 8 accounts) is CEO Letter's primary home; §2 the $400 ownership boundary that triggers CEO involvement; §3 entity overlay (entity-children do NOT receive standalone CEO Letter briefs — they route to entity packets per `_root/02 §3`; the parent-entity conversation is CEO-led but follows the CEO-Led Entity Pre-Engagement → Coordinated Notices pattern in `_root/06 §1`, not the standalone CEO Letter pattern); §4 health overrides (CEO Letter is rare for Watch/At-Risk because the Strategic override fires for most health-flagged accounts; the rare Watch-band CEO Letter applies the §4.13 lede override differently — call commitment moves to the second sentence per `_root/04 §4.13`); §5 annual overlay (annual CEO-Letter-eligible accounts get a 90-day notice window, not 60). Note: Δ ≥ $600 routes to CEO Pre-Call → Format B (Stage 3.2's territory), NOT to CEO Letter — CEO Letter is bounded above at $599.
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — T1/T2/T3 verbatim "What You're Getting at $X" blocks (Section 1 — one verbatim block per tier under "T1 — Catalog Essentials", "T2 — Commerce Professional", "T3 — Commerce Enterprise"; CEO Letter accounts in v6.2 trend toward T3 given the $400+ delta scope, but T1 and T2 CEO Letters also exist), user-rate ladder (Section 2 Block A — 1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18), "What's Coming in 2026" verbatim block (Section 3 — now mandatory in ALL formats including CEO Letter per operator decision Q4 2026-05-22; **the archived CEO Letter template does NOT yet carry this section** — your new template adds it via Section-3 pointer), implementation-fee table (Section 4 — recommendation only; surfaces in CEO Letter on tier-transition accounts), INTERNAL peer ranges (Section 5 — never in client copy; the archived CEO Letter template line 232 should be read carefully — it carries the CL-001 forbidden sentence next to a structural-fairness sentence; the new template uses only the structural-fairness register from `_root/04 §4.11`), INTERNAL unpublished premium SKUs (Section 6 — never in client copy). (`_root/03` uses "Section N" headings rather than `§N`; treat them as equivalent.)
9. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — **the highest-rule-density doc.** Read every subsection. **For CEO Letter specifically**: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase table (every row applies to CEO Letter; the "no account-specific adjustments" row is the CL-001 cleanup item that the archived CEO Letter template violates), §4.1 tenure-aware lede variants (CEO Letter integrates tenure into a first-person peer-to-peer paragraph per the §4.1 CEO Letter variant — longer than Format A/B's tenure-in-sentence-one pattern), §4.2 lede stat guardrail (no provisioned-vs-active ratio in any format including CEO Letter), §4.3 "above the midpoint" user-count clause, **§4.4 high-delta annual-dollar sentence (when Δ_pct > 30%) — `_root/04 §4.4` carries an explicit CEO Letter variant** ("That's $[DELTA × 12]/year — a real budget line, and you deserve a straight explanation of exactly what changed and why."); for CEO Letter the §4.4 sentence lands BETWEEN the monthly delta and the call commitment in the lede paragraph, §4.5 operations-unchanged sentence + IUR fork (CEO Letter uses BOTH variants; archived CEO Letter template surfaces them as `[IF primary or secondary driver IS/IS NOT included_user_reduction]` conditionals near the "Your Pricing at a Glance" trailer block), §4.6 platform-base-grown sentence (CEO Letter applies as a follow-on paragraph when `new_tier_base > current_platform_mrr` per `_root/05 §2.5.6` — CEO Letter does NOT inline the §4.6 sentence; it references it; this pattern was preserved by the 2026-05-26 source fix at `_root/05 §2.5.4`), **§4.7 early-adopter tenure paragraph — `_root/04 §4.7` carries an explicit CEO Letter variant** that is longer, first-person, and ends with the call commitment ("You've been with us since [YEAR] — [N] years. A change of this size from us warrants a real conversation, not a form letter. The platform you're running today is a fundamentally different product than it was in [YEAR]: your reps, your buyers, and your analytics team are all working from the same catalog, the same customer file, and the same order infrastructure. The pricing should reflect that. I'll call you personally by [SPECIFIC DATE] so we can talk through this directly."), §4.8 value anchor (`cost_per_order < $200` threshold — operator-stamped 2026-05-22; **the archived CEO Letter template already uses the $200 threshold per line 226** — verify when you read §4.8 that the threshold is $200), §4.9 billing-basis footnote (CEO Letter applies after URN and IUR pricing tables — per §4.9 does NOT apply to ABTS), §4.11 "How This Compares" structure (CEO Letter's archived template strips peer dollar values correctly but DOES carry the CL-001 forbidden sentence at line 232 — the new template references §4.11 and uses ONLY the plain-English position vocabulary), **§4.12 — CEO Letter close text — `I'll Call You` variant — and the formal-notice line**: the canonical close text is "I'll call you personally by **[SPECIFIC DATE]** — this isn't something I want to leave to email. If that timing doesn't work or you'd rather get ahead of it, reply to this email directly." The CEO call-commitment date is specific (an actual calendar date within 5 business days of send), not "soon" or "in the coming days" — this is the §4.12 anti-pattern explicitly named, §4.13 health-band lede overrides (Watch/At Risk accounts skip the relationship lede; for CEO Letter specifically, the call commitment ALSO moves to the second sentence — "Effective [EFFECTIVE_DATE], your monthly invoice moves from $[CURRENT_MRR] to $[NEW_MRR] — a change of $[DELTA]/month. I'll call you personally by [SPECIFIC DATE] to walk through this directly." — per `_root/04 §4.13` CEO Letter sub-paragraph), §4.14 discount-correction lede substitution (when `migration_driver = platform_discount_correction` — substitutes the §4.14 sentence for the "rate was set in [YEAR]" sentence; uniform across Format A / Format B / CEO Letter per §4.14).
10. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/05_driver_taxonomy.md` — **the driver-prose library.** Read every subsection. **For CEO Letter specifically — 8 driver blocks are carried verbatim**: §2.1.3 (URN — `user_rate_normalization`), §2.2.3 (`platform_discount_correction`), §2.3.3 (`tier_base_increase` — **CL-012 RESOLVED 2026-05-26**: the secondary-driver marker at §2.3.2 + §2.3.3 was amended from `[IF secondary driver = user_rate_normalization AND included base expands]` to `[IF secondary driver = included_user_reduction]` at the `_root/05` source during Stage 3.2 review pass. The new CEO Letter template's `tier_base_increase` dispatch row directs the drafter to paste §2.3.3 verbatim — no marker second-guessing needed; the marker is now correct. CL-023 was filed in lockstep for v6.2 `secondary_drivers` re-evaluation on TBI rows historically coded with URN secondary — that is a v6.2 maintenance question, not a CEO Letter template concern), §2.4.3 (`included_user_reduction`), §2.5.3 (`at_book_tier_shift` — references `_root/04 §4.6` by pointer per §2.5.6 conditional context paragraphs; this is CEO Letter's existing pattern, preserved by the 2026-05-26 CL-013 source fix), §2.6.3 (`multi_org_retirement` — **CL-016 RESOLVED 2026-05-26**: the `[IF secondary driver = included_user_reduction]` templated sub-block was added directly to §2.6.2 + §2.6.3 at the `_root/05` source during Stage 3.2 review pass per the 2026-05-22 operator stamp. The new CEO Letter template's `multi_org_retirement` dispatch row directs the drafter to paste §2.6.3 verbatim — the IUR-secondary sub-block now lives inside the canonical block and fires automatically when `secondary_drivers` includes `included_user_reduction`. The 2 multi_org + URN-secondary accounts continue with per-account narrative integration per §2.6.7 — that distinction was preserved at source), §2.7.3 (`annual_discount_retirement`), §2.8.3 (`special_arrangement` — **note**: per `_root/05 §2.8.3` doc-level commentary, the CEO Letter SA block is materially longer and more direct than Format B's, adding the explicit "this is not a judgment about your account" reframe and the "one rate card, applied consistently" closing line; the divergence is intentional because SA in a CEO-to-peer context warrants the longer framing). **For CEO Letter explicitly NOT carried — the decrease-side drivers**: §3.1.2 (`module_compression`), §3.2.2 (`user_count_variance`), §3.3.2 (`rate_architecture`) all route to Good News per `_root/06 §3` row 1. CEO Letter's mechanical scope (Δ ≥ $400) does not produce decrease drivers; if routing produces one, the routing is suspect — escalate per `_root/CONTRACTS.md §2`.
11. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/06_format_routing.md` — **the format definition and routing.** Read every subsection. **For CEO Letter specifically**: §1 the CEO Letter + Call Commitment definition (CEO-authored letter; CS executes delivery; the $400 ownership boundary in `_root/02 §2`; the close commits to a specific calendar date within 5 business days of send; closing language owned by `_root/04 §4.12`; the verbatim §4.13 Watch-band lede override applies when health override is in play but does not preempt the format); §2 the 6-step routing-decision flow; §3 the delta-tier dispatch table (CEO Letter is row 4: `$400 ≤ Δ ≤ $599`); §4.1 entity overlay (CEO Letter does NOT cover entity-children — those route to entity packets; the parent-entity case uses the CEO-Led Entity Pre-Engagement → Coordinated Notices pattern per `_root/06 §1`, which is a separate routing pattern from standalone CEO Letter); §4.2 health override (Watch / At-Risk routes to Strategic; the rare Watch-band CEO Letter applies the §4.13 lede override with the call-commitment-moves-to-sentence-two variant — see §4.13 + the §4.2 Watch-band-handling cross-reference); §4.3 annual overlay (annual CEO-Letter-eligible accounts get a 90-day notice window, not 60); §5 the `comm_action` vocabulary (CEO Letter values: `CEO Letter + Call Commitment` for standard; HOLD-row `post_hold_action` may resolve to `CEO Letter + Call Commitment (+$XXX)` with parenthetical Δ detail — both route through this template; count from `migration_comm_tiers_2026-05-19.csv` is 9 standard CEO Letter rows + 11 `post_hold_action` CEO Letter variants per `_root/06 §5` = 20 CEO Letter template usages); §5.5 the additional CSV columns (`hold_condition`, `post_hold_action`, `flags`, `nuances`); §6 the 5 routing-CSV errata. **NOT a CEO Pre-Call → Format B template** — that variant (Δ ≥ $600) is Stage 3.2's territory; CEO Letter is bounded above at $599.
12. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — **the data-fetching contract.** Read every subsection. **For CEO Letter specifically**: §1 source-of-truth hierarchy, §2 the 53-column v6.2 field guide (every bracketed placeholder in your template references one of these column names; note that CEO Letter uses `health_band` rather than `risk_label` per §2's field-guide note on line 68), §3 the canonical loader (the drafter uses this — the template does not), §4 the 3 Postgres MCP queries + derived metrics (the template's bracketed placeholders reference outputs of these queries), §5 the 9-row fallback table, §6 file-naming convention (`ceo-letter-notices/[ord_id]__[company-slug]__brief.md` and `__delivery-email.md`; versioned re-runs use `__v2`, `__v3`), §7 the canonical routing-block field-list matrix per format — **THIS IS THE AUTHORITATIVE CEO-LETTER ROUTING-BLOCK SPECIFICATION; your template's routing-block block MUST match this matrix exactly**. CEO Letter's §7 row specifies: `CEO awareness required before send: YES (always)`; `CEO call commitment date: required` (specific date within 5 business days of send); `CEO name for sign-off: required` (CEO FIRST + LAST NAME). CEO Letter does NOT carry the Format A `Expansion eligible` field. CEO Letter does NOT carry the Format B `comm_action` variants for CEO Pre-Call → Format B (that's Format B's domain). Note that `_root/07 §7` does not separately enumerate the delivery email routing-block subset per format — CL-022 filed 2026-05-26 — see Step 4 Section 2 below for the inference procedure.
13. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/08_quality_bar.md` — **the QA layer.** Read every subsection. **For CEO Letter specifically**: every QB-NNN check whose `Applies to:` field includes "CEO Letter" or "all formats." A new template that fails one of those checks at drafting time is broken. Your template's structure (section presence, placeholder coverage, conditional logic) must enable every CEO-Letter-applicable QB-NNN check to pass when the drafter fills it in. **Particularly important CEO-Letter-applicable blocker checks to verify your template enables**: QB-046 ("What's Coming in 2026" present — the archived CEO Letter template OMITS this; your new template MUST include it), QB-059 (no "no account-specific adjustments" sentence — the archived CEO Letter template VIOLATES this at line 232; your new template MUST NOT carry it), QB-077 ("above the midpoint" user-count clause when applicable), QB-078 (high-delta annual-dollar sentence in lede for Δ_pct > 30% — CEO Letter variant per §4.4), QB-082 (value-anchor `cost_per_order < $200` threshold — CEO Letter archive already uses $200), QB-085 (no peer dollar values in client copy), QB-086 (CEO Letter close verbatim per `_root/04 §4.12`; formal-notice line present; specific call-commitment date — never "soon" or "in the coming days"), QB-087 (Watch/At-Risk lede override with call-commitment-moves-to-sentence-two variant for CEO Letter), QB-088 (`_root/04 §4.14` discount-correction substitution when `migration_driver = platform_discount_correction`).

### Cleanup-tracker items the new template must address (read all 6)

14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_meta/stage3_cleanup.md` — **explicit per-prompt authorization to read this file** (the normal AGENTS.md hard rule against browsing `_meta/` is overridden here for Stage 3 template-build sessions). Read in full but apply specifically to CEO Letter:
    - **CL-001 (CRITICAL for CEO Letter)** — REMOVE the "no account-specific adjustments" sentence wherever it appears. **The archived CEO Letter brief template `_archive/.../ceo-letter-notices/_brief-template.md` line 232 carries this sentence verbatim inside the "How This Compares" section**: "The same pricing structure is going to every account we work with — there are no account-specific adjustments in how your number was calculated." The new CEO Letter template MUST NOT carry this sentence. The structural-fairness register from `_root/04 §4.11` handles the same intent without the defensive sentence. This is the single most consequential cleanup for CEO Letter — the sentence appears in BOTH the archived CEO Letter template AND the `da__dainolite__brief.md` archived exemplar (per CL-001 source notes); both predate the operator-stamped CL-001 cleanup.
    - **CL-003** — Strip peer dollar ranges from CEO Letter client copy. The archived CEO Letter template already strips these correctly per CL-003 + Wave 1 operator stamp 2026-05-22 (universal). Your new CEO Letter template confirms the absence and references `_root/04 §4.11` for the plain-English position vocabulary; do NOT reintroduce peer dollar values.
    - **CL-004** — Cut "equivalent platforms range from $3,000–$3,500/month" sentence for T3 accounts. The archived CEO Letter template (as of read time) does not appear to carry this sentence in the "How This Compares" section, but your read of the archived template at item 15 below will confirm. The new template MUST NOT carry the sentence in any case — the Wave 1 operator stamp 2026-05-22 is universal, covering CEO Letter for any T3 account.
    - **CL-005** — "What's Coming in 2026" verbatim block applies to ALL 4 formats including CEO Letter. **The archived CEO Letter template OMITS this section entirely** (confirm at item 15 read) — your new template ADDS it via a Section-3 pointer to `_root/03 Section 3`. This is the second most consequential cleanup for CEO Letter (after CL-001).
    - **CL-012 RESOLVED 2026-05-26** — The §2.3.2 / §2.3.3 secondary-driver marker was amended from `[IF secondary driver = user_rate_normalization AND included base expands]` to `[IF secondary driver = included_user_reduction]` at the `_root/05` source during Stage 3.2 review pass per operator stamp. Your CEO Letter template's `tier_base_increase` dispatch row simply directs the drafter to paste §2.3.3 verbatim — the marker is now correct; no second-guessing needed. CL-023 was filed in lockstep for v6.2 maintenance (re-evaluation of TBI rows historically coded with URN secondary, e.g. the `ih` exemplar) — that lives in `_meta/stage3_cleanup.md` and is dispatched to the v6.2 maintainer; it is NOT a CEO Letter template concern. Verify when reading `_root/05 §2.3.3` directly that the marker text now reads `[IF secondary driver = included_user_reduction]`; if it still reads URN, STOP — the source fix did not propagate and your template build cannot proceed cleanly.
    - **CL-016 RESOLVED 2026-05-26** — The `[IF secondary driver = included_user_reduction — add this paragraph:] Your included base also moves from [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED].` templated sub-block was added directly to §2.6.2 + §2.6.3 at the `_root/05` source during Stage 3.2 review pass per the 2026-05-22 operator stamp. Your CEO Letter template's `multi_org_retirement` dispatch row simply directs the drafter to paste §2.6.3 verbatim — the IUR-secondary sub-block now lives inside the canonical block and fires automatically when `secondary_drivers` includes `included_user_reduction`. The 6 multi_org + IUR-secondary accounts now get templated coverage automatically; the 2 multi_org + URN-secondary accounts continue with per-account narrative integration per §2.6.7 (preserved at source per the same operator stamp). §2.6.6 was updated in lockstep to reflect that the billing-basis footnote is REQUIRED for MOR + IUR-secondary (the IUR sub-block can produce excess users in the new pricing table) but NOT for MOR-primary standalone or MOR + URN-secondary. Verify when reading `_root/05 §2.6.3` directly that the IUR-secondary sub-block is present; if it is not, STOP — the source fix did not propagate.
    - **CL-022 (CEO Letter delivery email impact)** — `_root/07 §7` does not separately enumerate the delivery email routing-block field subset per format. Stage 3.1 inferred Format A's subset; Stage 3.2 inferred Format B's subset. CEO Letter follows the same inference procedure (see Step 4 Section 2 below). Rule-layer extension to `_root/07 §7` is scheduled for Wave 6 batch after all 4 Stage 3 templates land — CEO Letter is the third of the four; your delivery email template uses the inferred subset; flag in your conformance block that the CEO-Letter-specific slim subset is inferred per CL-022's pending rule-layer extension.

### Archive references (explicitly authorized per `_root/CONTRACTS.md §4` for Stage 3 template-build extraction)

These are the prior artifacts the new template SUPERSEDES. Read them for structural scaffolding (operator-notes header style, routing-block layout, section ordering including the CEO-specific "I'll Call You" section, conditional-flow markers, the "Your Pricing at a Glance" summary table structure, the CEO-specific signature block) and to understand what a completed CEO Letter brief looks like. **Do NOT lift verbatim driver prose from these into the new template** — driver prose is owned by `_root/05` now. The archived inlined prose is the very drift the rebuild exists to eliminate. **Also: do NOT preserve the CL-001 forbidden sentence at line 232 of the archived brief template** — that is the cleanup CL-001 is filed to remove.

15. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md` — the prior CEO Letter brief template. **Read in FULL.** Note: this template's body inlines driver prose verbatim for all 8 drivers — that is exactly the drift the new template fixes. Structural elements you may carry forward (with `_root/`-pointer rewrites): operator-notes blockquote header style (lines 6–19; note the CEO-specific fields `CEO awareness required before send: YES — CEO must review and personalize before this goes out`, `CEO call commitment date: [DATE — specific, within 5 business days of send]`, `CEO name for sign-off: [CEO FIRST + LAST NAME]`), internal routing-note block, section ordering (lede → CEO-Letter-specific early-adopter expanded paragraph → "Why the Number Is Changing" → "What You're Getting at $X" → "What This Works Out To" → "How This Compares" → "Your Pricing at a Glance" summary table → operations-unchanged paragraph + IUR fork → "**I'll Call You**" close section + formal-notice line → CEO signature). The `[USE ONLY THE APPLICABLE BLOCK]` markers can be retained as scaffolding — they map to `_root/05 §2.X.3` pointers in the new template. **DO NOT carry forward line 232's CL-001 forbidden sentence** — that's the cleanup. **DO NOT inline the §4.7 early-adopter paragraph from lines 35–36 — the new template references `_root/04 §4.7` (CEO Letter variant)**. **DO NOT inline the §4.12 close text from lines 256–259 — the new template references `_root/04 §4.12` (CEO Letter variant) for both the close and the formal-notice line**. **DO NOT inline the §4.13 health-band override sentences from lines 29's last bracketed instruction — the new template references `_root/04 §4.13` (CEO Letter variant) for the call-commitment-moves-to-sentence-two pattern**.
16. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_delivery-email-template.md` — the prior CEO Letter delivery email template. **Read in FULL.** Short structure (42 lines). The new delivery email template largely retains this structure but rewrites the inlined effective-date sentence as a pointer to `_root/04 §4.13`, the inlined "this brings it in line with what every account at your tier and usage profile pays" framing as a pointer to `_root/04 §4.1` + `§3` consolidated 2026 sentence, the inlined "Everything stays the same except the invoice" sentence + IUR fork as a pointer to `_root/04 §4.5` (with both variants available to the drafter at draft time), and the inlined "I'll call you personally by [SPECIFIC DATE]" sentence as a pointer to `_root/04 §4.12` (CEO Letter close). The archived delivery email's "Operator notes" block at the bottom (lines 33–41) carries 6 important variant notes — preserve those notes in the new template's operator-notes section, referenced by `_root/04 §4.12` and `_root/04 §4.7` and `_root/07 §6` rather than restated.
17. **Three CEO Letter exemplar briefs from the archive (read in FULL — these show what a completed CEO Letter brief looks like under the prior template; they predate CL-001 / CL-005 / CL-016 cleanups, so they are calibration only)**:
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/da__dainolite__brief.md` — the CL-001 violation exemplar (carries the forbidden "no account-specific adjustments" sentence; flagged in CL-001 source notes)
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/shl__savoy-house-lighting__brief.md` — a representative CEO Letter exemplar
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/hfg__hubbardton-forge__brief.md` — a representative CEO Letter exemplar
    Flag in your conformance block any place these exemplars contradict the current `_root/04` voice rules, `_root/05` driver blocks, or any of the CEO-Letter-applicable CL items above — those contradictions are evidence the exemplars need regeneration when Stage 4 production drafting begins (file as new `CL-NNN` items via your gaps list).

### Pattern reference from Stage 3.1 + Stage 3.2 (required — both operator-approved 2026-05-26)

18. **Stage 3.1 (Format A) and Stage 3.2 (Format B) reference templates — read all four in FULL**:
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_brief-template.md`
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_delivery-email-template.md`
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_brief-template.md`
    - `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_delivery-email-template.md`
    
    Both Stage 3.1 (operator-approved 2026-05-26 — see `_root/09_changelog.md` "Stage 3.1 review pass" entry) and Stage 3.2 (operator-approved 2026-05-26 — see "Stage 3.2 review pass" entry) are canonical structural-convention references for CEO Letter. **Stage 3.1 anchors the slim-format conventions** (Format A is the shortest, simplest brief — 4 sections, passive offer close, no meeting offer); **Stage 3.2 anchors the long-format conventions** (Format B is the closest sibling to CEO Letter — both carry 8 driver blocks, both apply Section 3 "What's Coming in 2026" via CL-005 pointer, both apply §4.4 high-delta annual-dollar sentence frequently, both have integrated tenure-aware ledes, both carry the "Your Pricing at a Glance" summary table). CEO Letter inherits Stage 3.2's structural patterns most directly; consult Stage 3.1 for the cross-format invariants. **Match the following conventions exactly** (deviating produces inconsistency across format folders that operator review will flag):
    - **Operator-notes blockquote header style** — Stage 3.1 brief template lines 6–23 (the `> **Operator notes — drafter-facing scaffolding; remove this entire blockquote before sending.**` block with sub-paragraphs for When to use / Who sends / What this template is NOT for / Cleanup-tracker history / Drafter's responsibility / Conformance block).
    - **Internal routing-note structure** — Stage 3.1 brief template lines 27–50 (the `> **Internal routing note** (drafter-facing; remove before sending — matches the canonical field list per `_root/07 §7` for [FORMAT]):` block; field names and order match `_root/07 §7` exactly; conditional rows enumerated separately).
    - **Driver dispatch table format** — Stage 3.1 brief template lines 131–143 (Markdown table with columns "v6.2 `migration_driver`" / "Insert `_root/05` block verbatim from" / "Notes"; out-of-scope drivers appear with "NOT carried in [FORMAT]" + forward-reference; `already_migrated` anomaly appears as final row).
    - **Tier verbatim block pointer** — Stage 3.1 brief template Section 3i (lines 163–170): `[INSERT _root/03 Section 1 — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block ...]`.
    - **QA-checklist `>` blockquote convention** — Stage 3.1 brief template Section 4 (lines 262–326): bucketed by `_root/08` section (drift-control / routing / data-pipeline / voice-content / driver-content / product-pricing-language / math-reconciliation); QB-NNN cited by number with one-line description; closing reminder that the full `_root/08` checklist is canonical.
    - **Cross-references footer** — Stage 3.1 brief template line 330: italicized closing paragraph mapping every `_root/XX §N.M` the template touches.
    - **Section blockquote convention** — Stage 3.1 brief template uses `> **Section [N][letter] — [section title].**` followed by drafter-facing instructions in indented blockquote, then the placeholder / verbatim section content. Match this convention for every section.
    - **Strict-placeholder precedent** (operator-stamped 2026-05-26) — see Step 5 below; Stage 3.1 demonstrates two specific examples (Section 3c effective-date sentence and Section 3l-continued graduated-rate string both rendered as `[INSERT _root/XX §N.M ...]` placeholders rather than inline).
    - **"Your Pricing at a Glance" table structure** — Stage 3.1 brief template Section 3l-continued (lines 215–230) carries the canonical 6-row summary table that the CEO Letter archive also surfaces in the same form (with minor tier-label variations); match Stage 3.1's table structure exactly. The "Additional user rate" after-column cell uses the strict-placeholder pattern `[INSERT _root/03 §2 Block A graduated-rate summary string verbatim ...]`.
    - **Section presence pattern** — Stage 3.1 brief template carries: Section 0 file header / Section 1 operator notes / Section 2 routing note / Section 3 brief content skeleton (3a subject through 3n close + formal-notice line) / Section 4 pre-send drafter checklist / cross-references footer. Match this structure; CEO Letter inserts the "I'll Call You" close section + the additional CEO-specific lede structure (integrated tenure + call commitment + §4.4 high-delta sentence as a single longer paragraph) and CEO-specific signature block.
    
    **What you may legitimately deviate from Stage 3.1 on** — only the CEO-Letter-specific scope differences specified in Step 2 (driver coverage `_root/05 §2.X.3` instead of `§2.X.4`, close text per `_root/04 §4.12` CEO Letter variant — "I'll Call You" with specific date — instead of Format A's passive offer, routing-block fields per `_root/07 §7` CEO Letter row including `CEO awareness required before send: YES (always)` + `CEO call commitment date: required` + `CEO name for sign-off: required`, lede structure per `_root/04 §4.1` + `§4.4` + `§4.7` + `§4.12` CEO Letter peer-to-peer pattern with integrated call commitment, signature block carrying CEO not CSM, CL items addressed: CL-001 + CL-005 + CL-012 + CL-016 + CL-022 instead of Format A's CL-001 + CL-003 + CL-004 + CL-005 + CL-011 + CL-013, etc.). The structural conventions above are uniform across all 4 format folders.

### Do NOT read

- Any other format folder's brief template, delivery email template, or per-account briefs (Format B archive, Good News archive, entity-packets — and the rest of the CEO Letter exemplars beyond the three named in item 17) — that is Stage 3.2 / 3.4 / 3.5 scope. Reading Format B archive material here pulls Format-B-specific patterns (meeting-offer close; no CEO call commitment) into the CEO Letter template. Reading Good News material pulls decrease-side content into CEO Letter (which is increase-side).
- Any of the other 6 CEO Letter exemplars not named in item 17 (`ali`, `all`, `am`, `fsf`, `mlc`, `vic`). Reading more exemplars beyond the 3 named adds calibration noise without proportionate signal; the 3 chosen (`da` for CL-001 violation calibration, `shl` + `hfg` for representative voice) are sufficient.
- `_meta/stage2_prompts/**` and other `_meta/stage3_prompts/**` files (including the Stage 3.1 and Stage 3.2 prompts themselves) — operator-process material; not relevant for CEO Letter template building. (Note: the Stage 3.1 and Stage 3.2 *output* templates under `format-a-notices/` and `format-b-notices/` ARE referenced — see item 18 above; only the `_meta/stage3_prompts/` operator prompts are out of scope here.)
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material already abstracted into `_root/01`–`_root/07`. Reading them here is scope creep.
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/` (per AGENTS.md hard rules).

---

## Step 2: Authoritative CEO Letter scope (use as fact — do not re-derive)

The planning agent verified the following against v6.2 + `_root/06` on 2026-05-22 + 2026-05-26 (CL-013 source application). Use as-is; if you believe any of it is wrong, flag in your conformance block and do not proceed.

**CEO Letter's mechanical scope** (per `_root/06 §3` row 4):

- Δ MRR satisfies: `$400 ≤ Δ ≤ $599`, applying the operator-stamped "higher-touch format wins" precedence rule.
- AND no override fires (no entity overlay per `_root/02 §3`, no health override per `_root/02 §4` — though the rare Watch-band CEO Letter applies the §4.13 lede override with the call-commitment-moves-to-sentence-two pattern; no annual overlay timing impact per `_root/02 §5` — though annual accounts may still route to CEO Letter's format substance with a 90-day window instead of 60).
- CEO Letter is the format for the **Executive segment** ($401 ≤ Δ ≤ $600 healthy standalone accounts; per `_root/02 §1` table) — the segment count is 8 standalone accounts. Plus HOLD-row `post_hold_action` resolutions where the row resolves to `CEO Letter + Call Commitment (+$XXX)`.

**NOT in CEO Letter's scope**:

- Δ ≥ $600: routes to CEO Pre-Call → Format B (Stage 3.2 territory). CEO Letter is bounded above at $599.
- Entity-children: route to entity packets per `_root/02 §3` (Stage 3.5 territory). The CEO-Led Entity Pre-Engagement → Coordinated Notices pattern in `_root/06 §1` is a separate routing pattern from standalone CEO Letter — it uses entity packets, NOT this template.
- Decrease-side accounts: route to Good News (Stage 3.4 territory). CEO Letter is increase-side only.

**CEO Letter's routing-CSV counts** (per `migration_comm_tiers_2026-05-19.csv` + `_root/06 §5`): 9 accounts carry `comm_action = CEO Letter + Call Commitment`; an additional 11 HOLD rows have `post_hold_action` resolving to `CEO Letter + Call Commitment` variants (per `_root/06 §5` line 191). Total CEO Letter template usage: 20 accounts.

**CEO Letter's driver coverage** (per `_root/05` — 8 increase-side blocks IN scope, 3 decrease-side blocks OUT of scope):

| Driver | In scope for CEO Letter? | Owning `_root/05` block (CEO Letter canonical) |
|---|---|---|
| `user_rate_normalization` | YES | §2.1.3 |
| `platform_discount_correction` | YES | §2.2.3 |
| `tier_base_increase` | YES (CL-012 RESOLVED 2026-05-26 — secondary marker amended URN→IUR at source; paste §2.3.3 verbatim) | §2.3.3 |
| `included_user_reduction` | YES | §2.4.3 |
| `at_book_tier_shift` | YES (references `_root/04 §4.6` by pointer per §2.5.6 — CEO Letter handles §4.6 as a follow-on paragraph, not inline; preserved by 2026-05-26 source fix) | §2.5.3 |
| `multi_org_retirement` | YES (CL-016 RESOLVED 2026-05-26 — IUR-secondary templated sub-block added at source to §2.6.2 + §2.6.3; URN-secondary stays narrative per the operator stamp's IUR-only scope) | §2.6.3 (carries IUR-secondary sub-block) + §2.6.6 (conditional context paragraphs) + §2.6.7 (per-secondary guidance) + §4 (weaving matrix for URN-secondary narrative) |
| `annual_discount_retirement` | YES | §2.7.3 |
| `special_arrangement` | YES (longer + more direct than Format B per §2.8.3 doc note — adds explicit "this is not a judgment about your account" reframe and "one rate card, applied consistently" closing line) | §2.8.3 |
| `module_compression` (decrease-side) | NO — routes to Good News per `_root/06 §3` | n/a |
| `user_count_variance` (decrease-side) | NO — Good News only per `_root/05 §3.2` | n/a |
| `rate_architecture` (decrease-side) | NO — Good News only per `_root/05 §3.3` | n/a |

If a Stage 4 drafter encounters a CEO Letter routing for an account whose `migration_driver` is a decrease-side value, the routing is suspect — the drafter escalates per `_root/CONTRACTS.md §2` and does not draft.

**CEO Letter's voice-rule coverage** (per `_root/04` — every applicable subsection):

Apply at every brief: §2 the 14 non-negotiables, §3 the 27-row forbidden-phrase prohibitions, §4.2 lede stat guardrail.

Apply conditionally (with the rule's own IF condition stated in §4):

- §4.1 tenure-aware "rate was set in [YEAR]" variant (cohort-year-dependent; CEO Letter integrates tenure into a peer-to-peer first-person paragraph longer than Format A/B's pattern; the §4.1 CEO Letter variant is the canonical source)
- §4.3 "above the midpoint" user-count clause (when applicable per the §4.3 condition; "How This Compares" section)
- §4.4 high-delta annual-dollar sentence (when Δ_pct > 30% per `_root/04 §4.4` — the CEO Letter variant lands BETWEEN the monthly delta and the call commitment in the lede paragraph; verbatim sentence in §4.4 CEO Letter sub-paragraph)
- §4.5 operations-unchanged sentence (default OR IUR-fork variant — drafter selects based on `secondary_drivers` value; the archived CEO Letter template surfaces this as a conditional in the "Your Pricing at a Glance" trailer block and AGAIN in the delivery email)
- §4.6 platform-base-grown sentence (when `new_tier_base > current_platform_mrr` per `_root/04 §4.6` condition — CEO Letter applies as a follow-on paragraph AFTER the pricing table per `_root/05 §2.5.6`; the at_book_tier_shift block invokes this, but the prose lives in §4.6, NOT in the §2.5.3 driver block)
- §4.7 early-adopter tenure paragraph (cohort year ≤ 2015 per §4.7 condition; the CEO Letter variant is longer, first-person, and ends with the call commitment — the §4.7 CEO Letter variant is the canonical source; the archived CEO Letter template inlines this at lines 35–36 — the new template references §4.7 instead)
- §4.8 value anchor section (when `cost_per_order < $200` per the operator-stamped 2026-05-22 threshold — the archived CEO Letter template already uses $200; verify when reading §4.8)
- §4.9 billing-basis footnote (when an excess-users line is in the pricing table — for URN and IUR drivers; per `_root/04 §4.9` does NOT apply to ABTS)
- §4.11 "How This Compares" structure (drafter judgment whether to include; if included, no peer dollar ranges per CL-003 + operator stamp, no equivalent-platforms sentence per CL-004 + operator stamp, **NO "no account-specific adjustments" sentence per CL-001 + operator stamp — this is the CL-001 CEO Letter cleanup**)
- §4.13 health-band lede override (when `health_band ∈ {Watch, At Risk, Critical}` — CEO Letter applies the call-commitment-moves-to-sentence-two variant per the §4.13 CEO Letter sub-paragraph; though most At-Risk and Critical accounts route to Strategic per `_root/02 §4`, the rare CEO-Letter-eligible health-flagged account uses this override)
- §4.14 discount-correction lede substitution (when `migration_driver = platform_discount_correction` — substitutes the §4.14 sentence for the standard "rate was set in [YEAR]" sentence; uniform across Format A / Format B / CEO Letter per §4.14)

Apply at every brief's close: §4.12 — CEO Letter close text (the `I'll Call You` / specific-date-commitment variant: "I'll call you personally by **[SPECIFIC DATE]** — this isn't something I want to leave to email. If that timing doesn't work or you'd rather get ahead of it, reply to this email directly.") + the formal-notice line. The specific date is a calendar date within 5 business days of send; **NEVER "soon" or "in the coming days"** — this is the §4.12 anti-pattern explicitly named.

**CEO Letter's authorship pattern** (per `_root/06 §1` + `_root/02 §2`):

- CEO (Mike) writes / signs / personalizes; CS prepares the draft and executes delivery once CEO approves.
- CEO is the sender of the delivery email (the email goes from CEO's email address, not from CS).
- The brief's signature block is CEO, not CSM.
- Routing-block `CEO awareness required before send: YES (always)` per `_root/07 §7`.

---

## Step 3: What you are authoring — file 1 of 2: `ceo-letter-notices/_brief-template.md`

The brief template is the structural skeleton for every CEO Letter per-account brief. Stage 4 drafters at draft time:

1. Look up the account in v6.2 + run the 3 Postgres queries per `_root/07 §4`.
2. Open this template.
3. Fill in every bracketed placeholder from v6.2 + Postgres data, plus the CEO-specific placeholders (`[CEO FIRST + LAST NAME]`, `[SPECIFIC DATE]` within 5 business days of send).
4. Where the template says `[INSERT _root/05 §N.M block verbatim]`, the drafter opens `_root/05`, copies the named block character-for-character, and pastes it in place, then fills the block's own bracketed placeholders.
5. Where the template says `[INSERT _root/04 §N.M sentence/paragraph]`, same procedure against `_root/04` (selecting the CEO Letter variant of the named subsection where the subsection has multiple variants — e.g. §4.7 CEO Letter variant vs Format A/B variants).
6. Apply the `_root/08` Quality Bar checklist to the completed draft before posting the conformance block.
7. CEO reviews the draft and personalizes the lede + close + sign-off before delivery; CS does not send until CEO has signed off.

Author the brief template as the following sections, in this order. **Every section either contains pure scaffolding (placeholders + headings) OR a §-pointer to an owning `_root/` doc. NO rule prose is inlined.**

### Section 0 — File header

```
# CEO Letter + Call Commitment — Brief Template
*CEO-authored | $400 ≤ Δ ≤ $599 (Executive segment per `_root/02 §1`) | "I'll Call You" close with specific date per `_root/04 §4.12`*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote block at the top of the file (removed before send) that:

- Names when to use this template (cite `_root/06 §1` and `§3` row 4; do not restate the conditions — point to the rule). Note: CEO Letter is for $400–$599 only; Δ ≥ $600 routes to CEO Pre-Call → Format B (Stage 3.2 territory).
- Names who sends (CEO is the email sender from his own email account; CS prepares the draft; CEO reviews and personalizes the lede + close before send; cite `_root/06 §1` + `_root/02 §2`). Note that CEO awareness is `YES (always)` per `_root/07 §7`.
- Names what this template is NOT for (Δ ≤ $399 → Format B per `_root/06 §1`; Δ ≥ $600 → CEO Pre-Call → Format B per `_root/06 §1`; entity-children → entity packet per `_root/02 §3`; decrease-side → Good News per `_root/06 §3`; CEO-Led Entity Pre-Engagement → Coordinated Notices is a separate routing pattern per `_root/06 §1` that uses entity packets, not this template — point to the rules, do not restate).
- Names the cleanup-tracker history (CL-001 REMOVED — the archived "no account-specific adjustments" sentence is gone; CL-003 confirmed absent — peer dollar ranges stripped; CL-004 confirmed absent via §4.11 reference; CL-005 ADDED via Section-3 pointer — the "What's Coming in 2026" block; CL-012 carry-through — `_root/05 §2.3.3` marker state reported in the conformance block; CL-016 — `multi_org_retirement` dispatch row carries the IUR-secondary sub-block reference; CL-022 — delivery email routing-block subset inferred per Stage 3.1 / Stage 3.2 precedent — list IDs only, link to `_meta/stage3_cleanup.md`).
- States the drafter's responsibility: every § reference in this template is to a canonical `_root/` doc. The drafter follows each reference and copies the named content verbatim into the per-account brief at draft time. CEO reviews and personalizes the lede + close + sign-off before delivery — that personalization is the only client-facing prose authored at draft time.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote block that mirrors the routing-block field list in `_root/07 §7` for CEO Letter exactly. Field names and order match `_root/07 §7`; do not invent fields, do not omit fields. Bracketed placeholders for each field. Particularly important for CEO Letter vs. Format A/B:

- `CEO awareness required before send: YES — CEO must review and personalize before this goes out` (always; per `_root/07 §7` CEO Letter row).
- `CEO call commitment date: [DATE — specific calendar date within 5 business days of send per _root/04 §4.12]` (required; per `_root/07 §7` CEO Letter row).
- `CEO name for sign-off: [CEO FIRST + LAST NAME]` (required; per `_root/07 §7` CEO Letter row).
- `Comm_action: [CEO Letter + Call Commitment | CEO Letter + Call Commitment (+$XXX) per post_hold_action variant]` from routing CSV.
- Does NOT carry `Expansion eligible` (that's Format A only per `_root/07 §7` matrix).
- Does NOT carry CEO Pre-Call → Format B variant fields (that's Format B only per `_root/07 §7` matrix).
- Include the conditional rows from `_root/07 §7` (support fire warning; tenure acknowledgment when cohort_year ≤ 2016; user-billing reconciliation when `_root/07 §4.5` discrepancy threshold tripped; billing entity when non-blank; Postgres-unavailable fallback per `_root/07 §5`) — same conditional-row pattern as Stage 3.1's Format A template, with CEO-Letter-specific values where they differ.

### Section 3 — Brief content skeleton (the customer-facing body)

Sub-sections in this order:

#### 3a. Subject / greeting / brief title

Standard format: `# [ACCOUNT_NAME]: Your Pricing Is Changing` followed by `*Prepared for [ACCOUNT_NAME] | [DATE]*` per the archived template. Drafter-fillable bracketed placeholders.

#### 3b. Lede paragraph (CEO Letter integrated structure — always)

A drafter-facing instructional comment naming:

- The CEO Letter lede structure (cite `_root/04 §4.1` + `§4.2` + `§4.4` + `§4.7` + `§4.12` — CEO is writing peer-to-peer; opens by acknowledging the relationship or the significance of the news; lands the price change in dollars not percentage in the same paragraph; commits to the call in the same paragraph). This is the ONE section of the brief where the prose is drafter-generated rather than pasted from a `_root/` block — CEO personalizes the lede.
- The high-delta annual-dollar sentence (cite `_root/04 §4.4` CEO Letter variant) — when `Δ_pct > 30%`, the lede MUST land the annual figure between the monthly delta and the call commitment. The verbatim §4.4 CEO Letter sentence is fetched from §4.4, not inlined here per strict-placeholder precedent.
- The conditional `[IF cohort_year ≤ 2015]` selector pointing to `_root/04 §4.7` (CEO Letter variant) for the early-adopter expanded tenure paragraph — when fired, the CEO Letter lede integrates the §4.7 peer-to-peer paragraph (which ends with the call commitment).
- The `_root/01 §1` relationship-before-price principle as the lede's organizing principle.
- A pointer to the v6.2 columns the drafter pulls from: `cohort_year`, `composite_narrative`, Postgres-derived `active_org_users` / `logged_in_90d` / `ltm_orders` (per `_root/07 §2` + `§4.2` + `§4.3`).
- Bracketed placeholders for the actual prose the drafter writes (the lede is CEO-personalized per `_root/04 §4.1`, not pulled from a `_root/` block — CEO writes a 3–4 sentence lede tuned to the specific account, fetching §4.4 + §4.7 verbatim sentences as referenced and weaving them into the personalized paragraph).

#### 3c. Watch / At-Risk lede override (conditional; CEO-Letter-specific)

A drafter-facing instructional comment with conditional `[IF health_band ∈ {Watch, At Risk, Critical} OR value_delivery_score < 40]` selector pointing to `_root/04 §4.13` for the **CEO Letter variant** of the health-band lede override: the lede skips relationship stats entirely and opens with the standalone dollar-change sentence; the call commitment moves to the SECOND sentence (per the §4.13 CEO Letter sub-paragraph). Drafter fetches the §4.13 CEO Letter variant verbatim and substitutes it for Section 3b. The template does NOT inline §4.13 prose; it references.

Note per `_root/02 §4` + `_root/06 §4.2`: a Watch / At-Risk / Critical CEO Letter is rare because the Strategic override typically routes the account away from CEO Letter. The lede-suppression rule is preserved here for the rare edge case where CEO Letter still applies.

#### 3d. Consolidated 2026 framing sentence + tenure-aware variant + driver-substitution variant

Standard sentence per `_root/04 §3` row on the consolidated 2026 sentence. Drafter pastes verbatim from `_root/04 §3`. Then a conditional `[IF cohort_year ≤ X | IF cohort_year between Y and Z | etc.]` selector pointing to `_root/04 §4.1` for the tenure-aware "rate was set in [YEAR]" variants (CEO Letter selects the variant based on `cohort_year` from v6.2 and pastes verbatim). The template does NOT inline any of these sentences.

**Conditional substitution for `platform_discount_correction` accounts**: drafter-facing `[IF migration_driver = platform_discount_correction]` selector pointing to `_root/04 §4.14` for the substitute sentence. Drafter substitutes this sentence FOR the "rate was set in [YEAR]" sentence when applicable. The template references §4.14; does NOT inline.

#### 3e. Early-adopter expanded tenure paragraph (conditional; CEO-Letter-specific variant)

Drafter-facing `[IF cohort_year ≤ 2015]` selector pointing to `_root/04 §4.7` for the **CEO Letter variant** of the early-adopter tenure paragraph (longer, first-person, ends with the call commitment). The §4.7 CEO Letter paragraph may be integrated into the Section 3b lede (CEO judgment) OR rendered as a standalone Section 3e paragraph after the consolidated 2026 sentence. Drafter pastes verbatim from §4.7. The template does NOT inline. (The archived CEO Letter template inlines this at lines 35–36; the new template replaces with a §-pointer to the §4.7 CEO Letter variant.)

#### 3f. "Why the Number Is Changing" section header + driver dispatch

Section heading: `## Why the Number Is Changing`. Then a drafter-facing `[DRIVER DISPATCH]` block:

```
[DRIVER DISPATCH — select ONE based on v6.2 `migration_driver` value; reject if not listed]:

| v6.2 `migration_driver` | Insert _root/05 block verbatim from | Conditional sub-blocks + secondary handling | Notes |
|---|---|---|---|
| `user_rate_normalization` | _root/05 §2.1.3 | §2.1.6 (conditional context paragraphs incl. _root/04 §4.10 platform-base conditional) + §2.1.7 (secondary-driver integration) | CEO Letter canonical block. |
| `platform_discount_correction` | _root/05 §2.2.3 | §2.2.6 + §2.2.7 | CEO Letter canonical. Note: CEO Letter PDC block uses "as part of this **refresh**" (vs Format B's "as part of this **change**") per §2.2.3 doc-level note. |
| `tier_base_increase` | _root/05 §2.3.3 | §2.3.6 + §2.3.7 | CEO Letter canonical. CL-012 RESOLVED 2026-05-26 — the §2.3.3 secondary marker now reads `[IF secondary driver = included_user_reduction]` post-source-fix; drafter pastes §2.3.3 verbatim. Per `_root/05 §2.3` doc note, §2.3.3 is identical character-for-character to §2.3.2 (Format B's block); both received the source fix in lockstep. |
| `included_user_reduction` | _root/05 §2.4.3 | §2.4.6 + §2.4.7 | CEO Letter canonical. Note: CEO Letter IUR block uses "as part of this **refresh**" per §2.4.3 doc-level note. |
| `at_book_tier_shift` | _root/05 §2.5.3 | §2.5.6 (incl. `_root/04 §4.6` follow-on paragraph when `new_tier_base > current_platform_mrr`; OMITTED when base moves down per kii special case) + §2.5.7 | CEO Letter canonical. The §4.6 sentence is a separate follow-on paragraph, not inlined in §2.5.3. Preserved by 2026-05-26 source fix at §2.5.4 — §2.5.6 now documents all three formats reference §4.6 by pointer. |
| `multi_org_retirement` | _root/05 §2.6.3 (now carries the IUR-secondary templated sub-block at source per CL-016 fix 2026-05-26) | §2.6.6 (conditional context paragraphs — note the billing-basis footnote bullet was updated 2026-05-26 to reflect it is REQUIRED for MOR + IUR-secondary but NOT for MOR-primary standalone or MOR + URN-secondary) + §2.6.7 (per-secondary-driver guidance) + §4 (weaving matrix for MOR + URN-secondary narrative integration) | CEO Letter canonical. Note: CEO Letter MOR block uses "as part of this **refresh**" per §2.6.3 doc-level note. CL-016 RESOLVED 2026-05-26: drafter pastes §2.6.3 verbatim — the `[IF secondary driver = included_user_reduction]` templated sub-block fires automatically for the 6 v6.2 multi_org + IUR-secondary accounts. For the 2 v6.2 multi_org + URN-secondary accounts the sub-block does NOT fire; drafter integrates per-account narrative per the kii / da exemplar patterns documented in §4. |
| `annual_discount_retirement` | _root/05 §2.7.3 | §2.7.6 + §2.7.7 | CEO Letter canonical. Note: CEO Letter ADR block uses "as part of this **refresh**" per §2.7.3 doc-level note. |
| `special_arrangement` | _root/05 §2.8.3 | §2.8.6 + §2.8.7 | CEO Letter canonical. Per §2.8.3 doc note: CEO Letter SA block is materially longer and more direct than Format B's, adding "this is not a judgment about your account" reframe + "one rate card, applied consistently" closing line — the longer framing is intentional for the peer-to-peer context. Operator note: for SA accounts with Δ > 30%, confirm account history with Finance before outreach; CEO must be prepared to answer "what was the arrangement and why is it changing?" — drafter-facing note pointing to `_root/05 §2.8.6` operator-note paragraph. |
| `module_compression` | NOT carried in CEO Letter | n/a | Decrease-side; routes to Good News per `_root/06 §3` row 1. If routing produces this driver in CEO Letter, escalate per `_root/CONTRACTS.md §2`. |
| `user_count_variance` | NOT carried in CEO Letter | n/a | Decrease-side; Good News only. |
| `rate_architecture` | NOT carried in CEO Letter | n/a | Decrease-side; Good News only. |
| `already_migrated` | n/a | n/a | Status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. |
```

After the dispatch table, an instructional `[INSERT_DRIVER_BLOCK]` placeholder where the drafter pastes the verbatim block(s) from the selected `_root/05 §N.M`. The template does NOT inline any of the 8 driver-prose blocks.

#### 3g. Pricing-table row template (per driver)

A drafter-facing instruction pointing to `_root/05 §N.M`'s pricing-table row template for the selected driver (URN: `§2.1.5`; PDC: `§2.2.5`; TBI: `§2.3.5`; IUR: `§2.4.5`; ABTS: `§2.5.5`; MOR: `§2.6.5`; ADR: `§2.7.5`; SA: `§2.8.5`). The template does NOT inline pricing-table row structures.

**Billing-basis footnote** — required for URN and IUR per `_root/04 §4.9`. Drafter pastes the `_root/04 §4.9` verbatim italicized sentence immediately after the URN or IUR pricing table (NOT after ABTS — per §4.9). Cite `_root/04 §4.9`; do not inline.

#### 3h. "What You're Getting at $[NEW_MRR]/Month" tier block

Section heading: `## What You're Getting at $[NEW_MRR]/Month`. Then `[INSERT _root/03 Section 1 — [T1 — Catalog Essentials | T2 — Commerce Professional | T3 — Commerce Enterprise] verbatim block — verbatim, with [NEW_INCLUDED] and any other bracketed tokens filled from v6.2 \`new_included_users\` and \`assigned_tier\` per the §1 drafter notes (T3 hard-codes "Up to 40 users" — no substitution)]`. Drafter pastes the canonical block from `_root/03 Section 1` selected by tier; the template does NOT inline the tier blocks.

#### 3i. "What This Works Out To" value-anchor section (conditional)

Section heading (conditional): `## What This Works Out To`. Drafter-facing instruction: `[IF derived metric \`cost_per_order < $200\` per _root/04 §4.8 (operator-stamped 2026-05-22): include the value-anchor section using _root/04 §4.8 structure. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.8` exactly. The template does NOT inline `_root/04 §4.8`'s structure; it points. Drafter computes `cost_per_order` per `_root/07 §4.4`. The §4.8 structure also handles the conditional second sentence (delta-per-order reframe when `delta_per_order < $50`).

Note: the archived CEO Letter template already uses the $200 threshold per line 226 — CEO Letter does NOT need the CL-002 cleanup that applies to Format B. Verify when reading §4.8 that the threshold is $200; if you find $35, STOP — the rule layer was not updated and the cleanup cannot proceed.

#### 3j. "What's Coming in 2026" verbatim block (CL-005 — additive)

Section heading: `## What's Coming in 2026`. Then `[INSERT _root/03 Section 3 verbatim block — verbatim, no substitution]`. Drafter pastes the canonical block from `_root/03 Section 3`. **This is CL-005's application in CEO Letter**: the archived CEO Letter template OMITS this section entirely; the new template ADDS it via the Section-3 pointer per operator decision Q4 2026-05-22 (mandatory in all 4 formats). This is the second most additive change in the CEO Letter rebuild after CL-001's sentence removal.

#### 3k. "How This Compares" section (conditional, drafter-judgment) — CL-001 CRITICAL

Section heading (conditional): `## How This Compares`. Drafter-facing instruction: `[IF drafter judgment + _root/04 §4.11 indicates this section adds clarity for the account: include the section using the structure in _root/04 §4.11. Otherwise: omit the section entirely.]`

If included, drafter follows `_root/04 §4.11` exactly:

- **No "no account-specific adjustments" sentence** (per CL-001 + `_root/04 §3` row). **This is the CL-001 CEO Letter cleanup — the archived CEO Letter template at line 232 carries this forbidden sentence; the new template MUST NOT carry it.** Delete entirely; never write it. The structural-fairness register from `_root/04 §4.11` handles the same intent without the defensive sentence.
- No peer dollar ranges (per CL-003 + operator stamp 2026-05-22 universal — the archived CEO Letter template already strips these correctly).
- No "equivalent platforms range from $X–$Y" sentence (per CL-004 + operator stamp 2026-05-22 universal — confirm the archived CEO Letter template does not carry it; in any case, the new template MUST NOT).
- Use the plain-English position vocabulary from `_root/04 §4.11`.
- Apply the `_root/04 §4.3` "above the midpoint" clause when applicable.

The template does NOT inline `_root/04 §4.11`'s structure; it points. Drafter follows §4.11 exactly, NOT the archived CEO Letter template's line 232 inlined sentence (which is the CL-001 violation).

#### 3l. "Your Pricing at a Glance" summary table

Section heading: `## Your Pricing at a Glance`. **This section appears in CEO Letter per the archived template lines 238–253** and is also carried by Format A (Stage 3.1 lines 215–230) and Format B (per Stage 3.2 prompt Section 3k). Match Stage 3.1's table structure exactly for cross-format consistency. The table structure is:

```
| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | +$[DELTA]/month ([DELTA_PCT]) |
| **Tier** | [LEGACY_TIER_LABEL] | [NEW_TIER_LABEL] |
| **Included users** | [LEGACY_INCLUDED] | **[NEW_INCLUDED]** |
| **Additional user rate** | [LEGACY_RATE_DESCRIPTION] | [INSERT `_root/03 §2 Block A` graduated-rate summary string verbatim — e.g. "Graduated ($25/$22/$20/$18)" per current §2 Block A canonical values] |
```

The table's column / row layout is template scaffolding (drafter-facing structure), not rule prose. Drafter values come from v6.2 + Postgres per `_root/07 §2` + §4 — EXCEPT the "Additional user rate" after-column, which is a placeholder pointing to `_root/03 §2 Block A` per the strict-placeholder precedent operator-stamped 2026-05-26 (Stage 3.1 review pass). Match Stage 3.1's table form exactly.

#### 3m. Operations-unchanged paragraph + IUR fork

Drafter-facing instruction: `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless v6.2 \`secondary_drivers\` includes \`included_user_reduction\`; in that case, INSERT _root/04 §4.5 IUR-fork variant.]` The template does NOT inline either variant; both live in `_root/04 §4.5`.

#### 3n. Close section (CEO Letter "I'll Call You" — CEO-Letter-specific)

Section heading: `## I'll Call You` (per the archived CEO Letter template + `_root/04 §4.12` CEO Letter variant). Then `[INSERT _root/04 §4.12 CEO Letter close text — verbatim, "I'll Call You" variant with specific calendar date within 5 business days of send. Substitute [SPECIFIC DATE].]`. Then the formal-notice line per `_root/04 §4.12` — `[INSERT _root/04 §4.12 formal-notice line verbatim, with [EFFECTIVE_DATE] filled in]`. Drafter pastes both from `_root/04 §4.12`. The template does NOT inline either.

**CEO-specific constraint per `_root/04 §4.12`**: the call-commitment date is a specific calendar date within 5 business days of send. **NEVER "soon" or "in the coming days"** — the §4.12 anti-pattern is explicitly named. The date appears in the close section AND is logged in the internal routing block per Section 2.

#### 3o. Signature

Standard CEO signature: `*[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat*` + `*[DATE]*`. Drafter-fillable. NOT a CSM signature — CEO Letter is CEO-signed per `_root/06 §1` + `_root/02 §2`.

### Section 4 — Pre-send drafter checklist (drafter-facing, removed before sending OR retained as conformance evidence)

A short `>` blockquote pointing to `_root/08` for the full 126-check QA layer. Name 8–12 of the most CEO-Letter-specific blocker checks by QB-NNN for drafter convenience — particularly QB-002 (conformance block), QB-046 ("What's Coming in 2026" present), QB-059 (no "no account-specific adjustments" sentence — CL-001 CEO Letter critical), QB-077 (above-the-midpoint clause), QB-078 (high-delta annual-dollar — CEO Letter §4.4 variant), QB-082 (value-anchor $200 threshold), QB-085 (no peer dollars), QB-086 (CEO Letter close verbatim per §4.12 — specific date, NEVER "soon"; formal-notice line present), QB-087 (Watch/At-Risk lede override with CEO-Letter call-commitment-moves-to-sentence-two variant), QB-088 (§4.14 discount-correction substitution), the QB-NNN for CEO awareness flag, the QB-NNN for §4.6 follow-on paragraph application. Do NOT restate any check; cite the QB-NNN and `_root/08`.

---

## Step 4: What you are authoring — file 2 of 2: `ceo-letter-notices/_delivery-email-template.md`

The delivery email template is the cover email that the CEO sends from his own email account, wrapping the completed brief at delivery time. Short structure (4–6 sentences). CS prepares the draft; CEO reviews + personalizes + sends from his email address.

Author the delivery email template as the following sections, in this order:

### Section 0 — File header

```
# CEO Letter — Delivery Email Template
*60-Day Notice | CEO-sent (from CEO's email address) | Wraps the CEO Letter brief; CEO reviews and personalizes before send*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote naming:

- When to use (delta is CEO Letter's scope per `_root/06 §3` row 4; the brief does the heavy lifting; this email is the CEO-sent wrapper).
- Who sends (CEO, from CEO's email address; CS prepares the draft; CEO reviews + personalizes + sends; per `_root/06 §1` + `_root/02 §2`).
- Length: 4–6 sentences. Longer than Format A/B's 3–4 because the CEO is opening peer-to-peer and committing to the specific-date call.
- What is NEVER in this email (cite `_root/04 §3` rows — minimizing language, apologies, percentage in the lede, "modest/small/minor", expansion language, upgrade mentions, "soon" or "in the coming days" instead of a specific date). Do not restate the prohibitions; cite the §3 rows.
- The CEO call-commitment date in the email body MUST match the date logged in the brief's internal routing block (per Section 2 of the brief) and MUST match the date logged in this delivery email's routing block (per Section 2 below). Per `_root/04 §4.12` + `_root/06 §1` — the three locations consistency-check is operator-judgment but the date is the same calendar date in all three.
- Operator-process notes (from the archived delivery email lines 33–41, but rewritten as references):
  - Attach the CEO Letter brief PDF before sending (cite `_root/07 §6` file-naming convention).
  - CEO call-commitment date logging — put on CEO calendar before email goes out (cite `_root/04 §4.12`).
  - For `included_user_reduction` accounts (primary or secondary driver): swap the §4.5 default sentence for the §4.5 IUR-fork variant per `_root/04 §4.5` (do NOT inline either variant).
  - Never adjust the effective date in the email without updating the brief to match (cite `_root/06 §1` consistency rule).
  - Do not add expansion language or upgrade mentions (cite `_root/04 §3` forbidden-phrase rows).
  - For early-adopter accounts (cohort_year ≤ 2015), add one sentence after the consolidated 2026 sentence acknowledging tenure per `_root/04 §4.7` (CEO Letter variant — first-person, peer-to-peer); do not inline the §4.7 paragraph in the delivery email — the email is short; pull only the tenure-acknowledgment sentence from §4.7 and reference §4.7 for the full paragraph in the brief.

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote mirroring the routing-block field list in `_root/07 §7` for CEO Letter's delivery email. **Note: `_root/07 §7` enumerates the canonical brief routing-block matrix, but does NOT yet separately specify the delivery email's slim subset (CL-022 filed 2026-05-26; rule-layer extension scheduled for Wave 6 batch after all 4 Stage 3 templates land).** Until CL-022 lands, infer the delivery email slim subset from: (a) Stage 3.1's `format-a-notices/_delivery-email-template.md` Section 2 — Format A established the precedent slim-subset pattern; (b) the archived CEO Letter delivery email's routing block (`_archive/.../ceo-letter-notices/_delivery-email-template.md` lines 6–13); (c) the brief's full routing block per Step 3 Section 2 above. Cross-reference all three and produce a slim block that includes: Brief type, Account / ord_id / Tier, Delta + percentage, Health, Comm_action, Effective date, **CEO call commitment date**, **CEO awareness confirmed before send: YES**, Support fire cleared, Attachment. **CEO-specific fields that MUST appear in the delivery email routing block** (per the archived delivery email + the CEO-Letter brief routing block): `CEO call commitment date: [DATE — specific, within 5 business days of send]`, `CEO awareness confirmed before send: YES` (vs Format A/B/Good News slim blocks where this field is omitted or NO). Flag in your conformance block that the slim subset is inferred per CL-022's pending rule-layer extension; the planning agent decides whether to amend `_root/07 §7` now or accept the inference as Wave 6 cleanup material.

### Section 3 — Email body skeleton

Standard fields:

- `**Subject:** [ACCOUNT NAME]: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]` (per the archived delivery email; the subject mirrors Format A/B's pattern).
- `Hi [CONTACT NAME],`
- Sentence 1: drafter-facing pointer to `_root/04 §4.13` for the effective-date sentence written in CEO's voice ("I'm writing to you directly. Effective **[EFFECTIVE_DATE]**, your monthly invoice is moving from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a change of **+$[DELTA]/month**."). For Δ_pct > 30%, the sentence MUST name the annual figure per `_root/04 §4.4` CEO Letter variant. Template references; does NOT inline.
- Sentence 2 (attached brief acknowledgment): drafter writes a one-sentence pointer to the attached brief ("I've attached a full explanation of why that number is what it is and what you're getting at the new rate."). This sentence is template scaffolding (drafter-facing structure carried from archived template line 21), NOT a `_root/` rule — flag in conformance block if the planning agent should promote it to a `_root/04` rule or accept as scaffolding.
- Sentence 3 (short-version framing): drafter-facing pointer to `_root/04 §3` consolidated 2026 sentence + `_root/04 §4.1` tenure-aware variant pointer. For `platform_discount_correction` accounts, substitute the §4.14 sentence per §4.14 rule. Template references; does NOT inline.
- Sentence 4 (operations-unchanged + IUR fork): `[INSERT _root/04 §4.5 sentence — DEFAULT variant unless secondary_drivers includes included_user_reduction; in that case INSERT IUR-fork variant.]` Same selector as brief Section 3m.
- Sentence 5 (call commitment): drafter-facing pointer to `_root/04 §4.12` for the CEO Letter close text echo — the email's call-commitment sentence is a one-sentence echo of the brief's §4.12 close, with the SAME specific calendar date as the brief routing block + delivery email routing block. Template references; does NOT inline. Per `_root/04 §4.12`: the date is a specific calendar date, NEVER "soon" or "in the coming days".
- Sentence 6 (optional, for early-adopter accounts): conditional `[IF cohort_year ≤ 2015]` selector pointing to a tenure-acknowledgment sentence pulled from `_root/04 §4.7` CEO Letter variant — one sentence only in the delivery email (the full §4.7 paragraph lives in the brief). Template references; does NOT inline.
- Signature: `[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat`

### Section 4 — Pre-send checklist (drafter-facing)

Short `>` blockquote pointing to `_root/08` for the relevant QB-NNN checks. Cite QB-NNN; do not restate. Include the archived template's checklist items (attach brief PDF; CEO call-commitment date on CEO calendar before send; CEO must review and approve before send — do not send from CS queue; the specific date constraint per §4.12) as drafter-process notes, cited to `_root/06 §1` and `_root/04 §4.12` and `_root/07 §6` rather than freshly authored.

### Section 5 — Voice calibration notes (drafter-facing)

A short closing paragraph pointing to `_root/04 §4.12` + `_root/04 §4.1` for the email's voice calibration (peer-to-peer; CEO is writing directly; the brief does the heavy lifting; the email is the wrapper with a personal commitment; if you're writing more than 6 sentences, you've crossed into brief territory). Cite the rules; do not restate.

---

## Step 5: Anti-drift discipline

- **The path-reference contract is absolute — strict-placeholder precedent operator-stamped 2026-05-26.** Every rule the template needs to enforce is referenced by `_root/XX §N.M`, never inlined. The template's content is scaffolding + pointers; the rule prose stays in its owning `_root/` doc. If you find yourself pasting a sentence from `_root/03`, `_root/04`, `_root/05`, `_root/06`, or `_root/07` into the template, stop — you are introducing drift. **This applies even to short sentences with only bracketed-token substitutions**: the Stage 3.1 review pass surfaced two such inlines (the `_root/04 §4.13` effective-date sentence and the `_root/03 §2 Block A` graduated-rate string) and the operator stamped STRICT — both became placeholders. Follow the same precedent here: any prose owned by a `_root/` doc, no matter how short, is a `[INSERT _root/XX §N.M ...]` placeholder, never an inline. The cost is one extra fetch step at draft time; the benefit is the path-reference contract holding end-to-end. **Particularly important for CEO Letter** because CEO Letter has more §-pointers than Format A/B (8 driver blocks vs Format A's 6; CEO-specific §4.1 + §4.4 + §4.7 + §4.12 + §4.13 variants beyond the standard §-pointers).
- **The ONLY content the template inlines** is: (a) drafter-facing instructions / blockquote scaffolding; (b) section headings and table column / row layouts; (c) `[ALL_CAPS_TOKEN]` placeholders for v6.2 + Postgres data the drafter substitutes (including CEO-specific tokens `[CEO FIRST NAME]`, `[CEO LAST NAME]`, `[SPECIFIC DATE]`); (d) `[INSERT _root/XX §N.M ...]` placeholders for rule prose the drafter fetches; (e) structural bridge sentences that have NO owning `_root/` rule (e.g. the Stage 3.1 transition sentence "Below is exactly why your number is changing and what you're getting at the new price." — operator-stamped 2026-05-26 as durable template scaffolding rather than promoted to a `_root/` rule; the delivery email "I've attached a full explanation..." sentence may be a similar candidate — flag in conformance block). If you encounter a bridge sentence in the archived CEO Letter template that has no owning `_root/` rule, treat it as scaffolding only if it appears verbatim across all 3 CEO Letter exemplars you read (da, shl, hfg) AND the archived template. Otherwise, flag in your conformance block — the planning agent decides whether to promote to a `_root/` rule or accept as scaffolding.
- **The 8 driver-prose blocks live in `_root/05`.** The template's "Why the Number Is Changing" section is a driver dispatch table that names which `_root/05 §N.M` block applies for each `migration_driver` value. The block prose itself is fetched by the drafter at draft time, not inlined here.
- **CL-001 is the single most important CEO-Letter-specific cleanup.** The archived CEO Letter template line 232 carries the forbidden "no account-specific adjustments" sentence. The new template MUST NOT carry this sentence in any form. The structural-fairness register from `_root/04 §4.11` handles the same intent without the defensive sentence.
- **CL-005 is additive.** The archived CEO Letter template does NOT carry a "What's Coming in 2026" section. The new template ADDS one via a `_root/03 Section 3` pointer per operator decision Q4 2026-05-22 (CL-005).
- **CL-016 is RESOLVED 2026-05-26 at source.** `_root/05 §2.6.2` (Format B) and `_root/05 §2.6.3` (CEO Letter) now carry the `[IF secondary driver = included_user_reduction]` templated sub-block directly in the canonical block per operator stamp 2026-05-26 (matches the 2026-05-22 operator stamp directing templated coverage for MOR + IUR-secondary). The new CEO Letter template's `multi_org_retirement` dispatch row simply directs the drafter to paste §2.6.3 verbatim — the sub-block fires automatically for the 6 v6.2 multi_org + IUR-secondary accounts. The §2.6.6 conditional context paragraphs bullet on the billing-basis footnote was updated in lockstep (REQUIRED for MOR + IUR-secondary; NOT for MOR-primary standalone or MOR + URN-secondary). For the 2 v6.2 multi_org + URN-secondary accounts, the sub-block does NOT fire; drafter integrates per-account narrative per `_root/05 §4` + §2.6.7. **Verify when reading `_root/05 §2.6.3` directly that the IUR-secondary sub-block is present; if absent, STOP — source fix did not propagate.**
- **CL-012 is RESOLVED 2026-05-26 at source.** `_root/05 §2.3.2 + §2.3.3` secondary-driver marker was amended from `[IF secondary driver = user_rate_normalization AND included base expands]` to `[IF secondary driver = included_user_reduction]` per operator stamp 2026-05-26 (the marker now matches the integrated paragraph's IUR-style included-base-move behavior). The new CEO Letter template's `tier_base_increase` dispatch row simply directs the drafter to paste §2.3.3 verbatim — no marker second-guessing needed. CL-023 was filed in lockstep for v6.2 maintenance (downstream re-evaluation of TBI rows historically coded with URN secondary, e.g. `ih__interlude-home`) — that is a v6.2 maintainer concern, not a CEO Letter template concern. **Verify when reading `_root/05 §2.3.3` directly that the marker text now reads `[IF secondary driver = included_user_reduction]`; if it still reads URN, STOP — source fix did not propagate.**
- **CL-003, CL-004 are universal.** No peer dollar ranges (archived CEO Letter already strips), no equivalent-platforms sentence (confirm absent in archived; new template MUST NOT carry). Reference `_root/04 §3` rows and `_root/04 §4.11`; do not invent new "How This Compares" prose.
- **CL-022 is the delivery email-specific gap.** `_root/07 §7` does not enumerate the delivery email routing-block subset; the new CEO Letter delivery email template infers the subset per Step 4 Section 2 above. Flag in conformance block.
- **CL-002, CL-011, CL-013, CL-014, CL-015, CL-017, CL-018, CL-019, CL-020, CL-021 are NOT CEO-Letter applicable.** CL-002 ($35→$200 threshold) is Format-B-specific (CEO Letter archive already uses $200). CL-011 (`discount_correction` rename) is Format-A-specific (CEO Letter archive already uses `platform_discount_correction`). CL-013 was resolved at source 2026-05-26 — no template work needed. CL-014 (entity-packet) is Stage 3.5. CL-015 (Annual voice rules) is a `_root/04` cleanup not a template change. CL-017 (Critical-band) is RESOLVED. CL-018–CL-021 are Format A exemplar regeneration items (apply to Format A exemplars only; CEO Letter exemplars have their own regeneration items implicitly via CL-001 / CL-005 / CL-016 — flag any CEO Letter exemplar contradictions surfaced during item 17 read as new CL-NNN items in your conformance gaps list).
- **The drafter (and CEO) are the integration point, not the template.** Drafters at draft time fetch verbatim blocks from `_root/`, fill in placeholders from v6.2 + Postgres, and apply conditional rules; CEO personalizes the lede + close + sign-off before delivery. The template's job is to tell the drafter what to fetch and where to put it; it does NOT pre-fill what the drafter fetches.
- **No new operator-policy decisions.** If you discover that a rule in `_root/` is ambiguous for CEO Letter's use case, flag in your conformance block. Do NOT pick an interpretation and bake it into the template.
- **No new CEO Letter scope.** CEO Letter handles 8 increase-side drivers for the $400–$599 Executive segment per Step 2. Do NOT extend coverage to decrease-side drivers or to Δ ≥ $600 (that's CEO Pre-Call → Format B, Stage 3.2 territory) even if you think CEO Letter "should" carry them — that is a Stage 3 cleanup item to file via your gaps list, not a template change.
- **Asking is cheap. Inventing is the drift vector.**

---

## Step 6: Voice and format constraints

- Register for operator-notes and drafter-facing instructions: declarative, no marketing language. Same register as `_root/02`, `_root/04`, `_root/06`, `_root/07`. Use `>` blockquote for every drafter-facing block (matching the archived template's convention).
- Use clean Markdown structure: `#` for the file title, `##` for the customer-facing brief sections (including the CEO-Letter-specific `## I'll Call You` close section), `###` for sub-sections inside drafter-facing blocks. Bracketed placeholders use the `[ALL_CAPS_WITH_UNDERSCORES]` convention from the archived template (e.g. `[ACCOUNT_NAME]`, `[NEW_MRR]`, `[EFFECTIVE_DATE]`, `[CEO FIRST NAME]`, `[CEO LAST NAME]`, `[SPECIFIC DATE]`).
- The customer-facing sections of the brief template should READ AS A CEO LETTER when the drafter fills in placeholders + CEO personalizes the lede / close — peer-to-peer voice; first-person ("I'll call you personally"); the dollar change is the primary fact; the call commitment is the primary structural feature.
- No emoji. No "Importantly" / "Critically" — the QB-NNN severity in `_root/08` is the operational signal of importance.
- For dual-routing-pattern fields in the routing block + delivery email body (e.g. `comm_action` with parenthetical Δ detail for `post_hold_action` resolutions), use a clear `[IF post_hold_action variant: append parenthetical (+$XXX)]` syntax that mirrors the archived template's conditional convention.

---

## Step 7: Output

Replace nothing — both files are NEW.

Create the new folder + both files:

- `Pricing Migration/ceo-letter-notices/_brief-template.md` (the brief template)
- `Pricing Migration/ceo-letter-notices/_delivery-email-template.md` (the delivery email template)

The folder `Pricing Migration/ceo-letter-notices/` does not exist yet (the prior folder was moved to `_archive/2026-05-22__pre-refactor/ceo-letter-notices/` during the 2026-05-22 refactor); your authoring creates the folder.

Then, in your chat reply (NOT in the files), produce this conformance block per `_root/00_manifest.md §5`:

```
─── Conformance Block ─────────────────────────────────────────
Session task: Stage 3.3 — author ceo-letter-notices/_brief-template.md + _delivery-email-template.md
Output target:
- Pricing Migration/ceo-letter-notices/_brief-template.md (NEW file, NEW folder)
- Pricing Migration/ceo-letter-notices/_delivery-email-template.md (NEW file)

Files read (with last-updated date / mtime):
- <enumerate every file path from Step 1 with last-updated date or mtime>

Explicitly-authorized archive reads (per Stage 3.3 §1 items 15–17):
- <list every archived file you read with mtime>

Pattern-reference read (Step 1 item 18 — required):
- <"Stage 3.1's format-a-notices/_brief-template.md and _delivery-email-template.md were [present / absent] at read time. If present, consulted for: [structural conventions]. Did NOT lift content from.">

Files NOT read:
- <enumerate per Step 1 "Do NOT read">

Brief template sections authored: <count + names — should match Step 3's section list (3a through 3o)>
Delivery email template sections authored: <count + names — should match Step 4's section list>

Drivers covered in brief template (per the dispatch table in 3f):
- In scope (8): <list with §-pointer for each — should be §2.1.3 / §2.2.3 / §2.3.3 / §2.4.3 / §2.5.3 / §2.6.3 / §2.7.3 / §2.8.3>
- Out of scope (3 decrease-side): <list with §-pointer for each>

CL items addressed (with the specific template element that addresses each):
- CL-001 (CRITICAL): <where in the template — should be "How This Compares section 3k REMOVES the archived line 232 forbidden sentence; references _root/04 §4.11 structure that prevents reintroduction">
- CL-003: <where — should be "How This Compares section 3k references _root/04 §3 row on peer-dollar prohibition; archived already strips, new template preserves absence">
- CL-004: <where — should be "How This Compares section 3k references _root/04 §3 row on competitor-pricing prohibition">
- CL-005: <where — should be "Section 3j ADDS What's Coming in 2026 verbatim block via _root/03 Section 3 pointer (new in CEO Letter template)">
- CL-012 (RESOLVED 2026-05-26 — verify-at-source): <where — should be "tier_base_increase dispatch row in 3f references _root/05 §2.3.3 verbatim; verified marker reads `[IF secondary driver = included_user_reduction]` per source fix; STOP if marker still reads URN">
- CL-016 (RESOLVED 2026-05-26 — verify-at-source): <where — should be "multi_org_retirement dispatch row in 3f references _root/05 §2.6.3 verbatim (now carries IUR-secondary templated sub-block at source) + §2.6.6 conditional context + §2.6.7 + §4 weaving matrix; verified §2.6.3 contains the IUR-secondary sub-block per source fix; STOP if absent">
- CL-022: <where — should be "Delivery email Section 2 routing block inferred per CL-022 pending rule-layer extension; flagged for Wave 6 cleanup">

CL-012 + CL-016 source-fix verification (operator-facing — both should be VERIFIED post-2026-05-26 source fix):
- `_root/05 §2.3.3` secondary-driver marker reads: <verbatim quote of marker text — expected `[IF secondary driver = included_user_reduction — add this paragraph:]`>
- `_root/05 §2.6.3` `[IF secondary driver = included_user_reduction]` templated sub-block: <"PRESENT — verbatim sub-block text quoted here" or "ABSENT — STOP and escalate per CONTRACTS §2">
- Both verifications must pass; if either fails, the source fix did not propagate to the file you read, and template building cannot proceed cleanly.

Path-reference contract verification:
- Number of verbatim rule blocks INLINED in the template (should be 0 — if non-zero, list each and explain why it could not be referenced): <count + list or "0">
- Number of §-pointers TO _root/ docs in the template: <count by owning doc — e.g. "_root/03: ~3, _root/04: ~16 (CEO Letter has more §-pointers than Format A/B due to §4.1 / §4.4 / §4.7 / §4.12 / §4.13 CEO Letter variants), _root/05: 11, _root/06: ~5, _root/07: ~3, _root/08: ~10">
- Number of bracketed placeholders for drafter data fill-in (per v6.2 + Postgres + CEO-specific): <count>

CEO-specific structural elements verification:
- `CEO awareness required before send: YES (always)` field in routing block: <present / absent>
- `CEO call commitment date: required` field in routing block: <present / absent>
- `CEO name for sign-off: required` field in routing block: <present / absent>
- `## I'll Call You` section heading (vs Format A's `## What Happens Next` or Format B's `## Let's Talk`): <present / absent>
- CEO signature block (vs CSM signature): <present / absent>
- Specific-calendar-date constraint per `_root/04 §4.12` (NEVER "soon" or "in the coming days") surfaced in operator notes + close section + checklist: <present / absent>
- Delivery email sender = CEO (not CS) noted in operator notes + Section 1: <present / absent>

Verbatim text the template DOES carry (template scaffolding only — NOT rule prose):
- <list: e.g. "operator-notes blockquote header style (drafter-facing, not a rule)", "internal routing-note block (drafter-facing metadata, per _root/07 §7)", "section heading text like 'I'll Call You' (drafter-facing structure, not a rule — note this heading is CEO-Letter-specific)", "bracketed placeholders like [CEO FIRST NAME] (drafter-facing fill points)", "Your Pricing at a Glance summary table structure (CEO-Letter-format-shared brief structure carried from archive, not a _root/ rule)", "delivery email 'I've attached a full explanation...' sentence (flagged for planning agent decision: promote to _root/04 rule or accept as scaffolding)">

Routing-block field list cross-check (per _root/07 §7 CEO Letter matrix):
- <confirm every required field is present in the template's routing block; flag any divergence; particularly confirm CEO awareness YES (always), CEO call commitment date required, CEO name for sign-off required>

Watch / At-Risk / Critical lede override handling (CEO-Letter-specific):
- <confirm Section 3c references _root/04 §4.13 CEO Letter sub-paragraph for the call-commitment-moves-to-sentence-two pattern, not a separate inlined sentence>

§4.7 early-adopter handling (CEO-Letter-specific variant):
- <confirm Section 3e (or Section 3b lede integration) references _root/04 §4.7 CEO Letter variant — first-person, peer-to-peer, ends with call commitment — not the Format A/B shorter variant>

§4.4 high-delta annual-dollar sentence handling (CEO-Letter-specific variant):
- <confirm Section 3b lede references _root/04 §4.4 CEO Letter variant ("That's $[DELTA × 12]/year — a real budget line, and you deserve a straight explanation of exactly what changed and why.") — not the Format A/B variant>

Gaps surfaced (a CEO Letter scope element that has no _root/ rule, OR a _root/ rule that the template cannot enforce structurally):
- <list, or "none">

Conflicts between sources (and chosen resolution / flag):
- <list, e.g. "the archived CEO Letter template's line 232 CL-001 forbidden sentence vs. _root/04 §3 + _root/04 §4.11 — resolution: _root/04 wins per CONTRACTS §5; CL-001 cleanup applied; new template omits the sentence entirely", or "none">

Open questions for operator:
- <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file (do not edit `_root/`, do not edit other format folders, do not edit `_meta/stage3_cleanup.md`, do not edit the Format A template if it exists, do not edit the Format B template if it exists). The operator will paste your output back to the planning agent for review before Stage 3.4.

---

## Step 8: If something is missing or contradictory

- A `_root/04` voice rule that CEO Letter should enforce but is not yet authored → flag in your conformance block; the planning agent decides whether to author the rule via the `_root/CONTRACTS.md §3` rule-change protocol before you proceed.
- A `_root/05` driver block that the dispatch table says CEO Letter carries but is not yet authored in `_root/05` → flag; do not invent the block.
- A `_root/07 §7` routing-block field list that does not match what CEO Letter briefs actually need → flag both versions; do not pick one.
- A conflict between the archived CEO Letter template's inlined prose and the current `_root/04` voice rules → `_root/04` wins per `_root/CONTRACTS.md §5`. The archived template's drift (including the CL-001 line-232 forbidden sentence) is the reason for the rebuild.
- A conflict between two `_root/` docs (e.g. `_root/04 §4.12` close text vs. `_root/06 §1` CEO Letter close description) → flag the conflict; do not pick one. The planning agent resolves via the rule-change protocol.
- A driver an exemplar brief (da, shl, hfg) renders that the new template's dispatch table does not name → flag; the exemplar may be using forbidden phrasing or improvised integration.
- A field the prior template's routing block carried that `_root/07 §7` does not name → flag; either `_root/07 §7` is missing the field (and needs an update via rule-change protocol) or the prior template carried scope creep.
- CL-012 + CL-016 verify-at-source: both were RESOLVED 2026-05-26 via source fixes at `_root/05 §2.3.2 + §2.3.3` (URN→IUR marker amendment) and `_root/05 §2.6.2 + §2.6.3` (templated IUR-secondary sub-block addition). If your read of `_root/05 §2.3.3` finds the marker still reads URN, OR your read of `_root/05 §2.6.3` finds the IUR-secondary sub-block absent, STOP — the source fix did not propagate to the file you read (likely iCloud sync issue or stale cache). Flag both verifications in your conformance block; do NOT pick a marker yourself, do NOT improvise the sub-block. The resolutions belong at source per `_root/CONTRACTS.md §5`.
- CL-001 in the archived exemplars: the `da` exemplar carries the forbidden sentence per CL-001 source notes; if `shl` or `hfg` also carry it (or any variation of it), flag in your conformance block — those exemplars need regeneration when Stage 4 production drafting begins (file as new `CL-NNN` items via your gaps list).
- Anything in the cleanup tracker that you cannot translate into a template element → flag; the planning agent decides.

**Asking is cheap. Inventing is the drift vector.**
