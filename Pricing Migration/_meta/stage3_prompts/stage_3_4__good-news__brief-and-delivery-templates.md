# Stage 3.4 — Authoring Prompt for `good-news-notices/_brief-template.md` + `_delivery-email-template.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-26 by planning agent in parallel with Stage 3.3 review approval. Inherits Stage 3.1 + Stage 3.2 + Stage 3.3 pattern conventions + strict-placeholder precedent + "pricing" subject convention. Stage 3.3 was a clean review (no source fixes, no new CL items), so no delta-pass was needed before drafting Stage 3.4. **Operator stamps applied 2026-05-26 before paste**: brief title "Your Pricing Is Decreasing"; delivery email subject "your SuperCat pricing is decreasing — effective [EFFECTIVE_DATE]"; `_root/04 §4.5` Good News operations-unchanged variant promoted at source; `_root/04 §3.1` Good News consolidated 2026 framing sentence promoted at source; 10-day follow-up sentence accepted as template scaffolding; uniform brief + delivery email pattern (not archived Option A / Option B split).
> **Output target**: TWO new files under a NEW folder at `Pricing Migration/good-news-notices/`:
>   - `good-news-notices/_brief-template.md` (the structural skeleton for every Good News per-account brief — CS-led / CSM-signed; warm low-touch voice; decrease-side only)
>   - `good-news-notices/_delivery-email-template.md` (the cover email that wraps every Good News brief at delivery; CS is the sender)
> **Estimated authored length**: brief template 250–350 lines (Good News carries 3 driver blocks, a 4-row summary table, no "How This Compares" / no value anchor / no tier block / no formal-notice line); delivery email template 90–130 lines (3–4 sentences; CS-sent).
> **Dependency**: Stage 5 complete (`_root/00`–`_root/09` all authored and operator-stamped); `_root/04 §3.1` + `§4.5` Good News variants operator-stamped 2026-05-26 at source (Stage 3.4 prep). Independent of Stage 3.1 / 3.2 / 3.3 / 3.5. **Pattern inheritance from Stage 3.1 + 3.2 + 3.3**: consult all three approved template sets for structural-convention reference only. Do NOT lift increase-side driver content, CEO call-commitment close text, or CEO-specific routing fields.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `good-news-notices/_brief-template.md` is the structural skeleton every Stage 4 per-account drafting agent fills in to produce a Good News brief for accounts whose Δ MRR is negative (`Δ MRR < $0` per `_root/06 §3` row 1). The brief is CS-led — CSM sends and signs; no CEO involvement per `_root/06 §1`. The companion `_delivery-email-template.md` is the cover email CS sends, wrapping the completed brief at delivery time.

Your job is to **author two new template files that reference `_root/` rules by §-number and never restate them.** This is the single most important discipline of this entire task. Every voice rule, every forbidden phrase, every driver-prose block, every routing condition, every quality check lives in exactly one `_root/` doc. The templates carry only:

- **Drafter-facing structural scaffolding** — the operator-notes blockquote header, the routing block format (with Good-News-specific fields per `_root/07 §7`), the section headings, the bracketed placeholders the drafter fills in from data, the pricing-table row template structure, the 4-row "Your Pricing at a Glance" mini-summary table.
- **Lookup instructions** — pointers like `[INSERT _root/05 §3.1.2 — module_compression Good News mechanic block — verbatim, with [BRACKETED_TOKENS] filled from v6.2 + Postgres data per _root/07 §4]`. The drafter at draft time copies the verbatim block from the owning `_root/` doc into the brief; the template does not carry the prose.
- **Conditional flow logic** — `[IF migration_driver = module_compression: use §3.1.2 | IF migration_driver = user_count_variance: use §3.2.2 | IF migration_driver = rate_architecture: use §3.3.2]`. The conditions reference v6.2 columns by name (per `_root/07 §2`); the resulting block is a pointer to `_root/05 §3.X.Y`, not inline prose.

If you find yourself about to paste verbatim prose from `_root/03`, `_root/04`, or `_root/05` into the template, **stop**. That is exactly the drift the path-reference contract (`_root/CONTRACTS.md §5`) was written to prevent.

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will not extend the template's scope beyond what `_root/06 §1` + `§3` row 1 define Good News to be (decrease-side accounts only; Watch / At Risk / Critical preempted out per `_root/06 §4.2`).

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date (from each file's header block where present) in the conformance block of your final reply.

### Folder orientation (mandatory — echo in conformance block per `_root/00_manifest.md §6`)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` — the index. **The §2 manifest table is the authoritative list of every `_root/` doc; you echo it in your first chat response per the manifest-echo contract in §1 step 6.**
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` — read every entry. **Particularly important for Good News**: Wave 2 Q4 (CL-005 — "What's Coming in 2026" in ALL formats including Good News; archived Good News OMITS this section); Wave 1 (peer-dollars universal-strip + competitor-pricing broadening — Good News archived template already strips both); **Stage 3.4 prep 2026-05-26** (`_root/04 §3.1` Good News consolidated 2026 framing sentence + `_root/04 §4.5` Good News operations-unchanged variant promoted at source per operator stamp).

### The rule layer — read in FULL

6. `_root/01_why_we_are_migrating.md` — strategic register. Good News is low-touch; relationship-before-price applies lightly (lead with the mechanical decrease fact, not relationship stats).
7. `_root/02_who_is_being_migrated.md` — **For Good News**: §3 entity overlay (entity-children fold into entity packets — no standalone Good News); §4 health overrides (Watch-band carve-out per `_root/06 §4.2` preempts Good News); §5 annual overlay (timing follows ≥90-day renewal window; substance stays Good News).
8. `_root/03_what_we_sell.md` — **For Good News**: Section 3 "What's Coming in 2026" verbatim block (CL-005 — mandatory additive section; archived Good News OMITS). Good News does NOT carry tier verbatim blocks ("What You're Getting at $X") — decrease notices explain the mechanic, not a tier upsell.
9. `_root/04_communication_posture.md` — **For Good News**: §2 non-negotiables (lead with dollars not percentage in lede); §3 forbidden-phrase rows on gift/reward/apology/expansion/peer dollars/competitor pricing; **§3.1 Good News consolidated 2026 framing sentence** (operator-stamped 2026-05-26 — NOT the universal §3 row sentence); **§4.5 Good News operations-unchanged variant** (operator-stamped 2026-05-26); **§4.12 Good News close** (operator-led, no ask; **NO formal-notice line** per §4.12 "immediately after each close, except Good News").
10. `_root/05_driver_taxonomy.md` — **Good News driver library — Section 3 only**: §3.1.2 (`module_compression` mechanic) + §3.1.4 (pricing table); §3.2.2 (`user_count_variance` mechanic) + §3.2.3 (pricing table); §3.3.2 (`rate_architecture` mechanic) + §3.3.3 (pricing table). **Section 2 increase-side blocks are OUT of scope** — if routing produces an increase driver under Good News `comm_action`, escalate per `_root/CONTRACTS.md §2`.
11. `_root/06_format_routing.md` — §1 Good News definition; §3 row 1 (`Δ < $0`); §4.2 Watch-band carve-out (Good-News-eligible account that is Watch / At Risk / Critical routes to CSM first); §4.3 annual overlay; §5 `comm_action` row 5 (`Good-News Notice`) + HOLD-row `post_hold_action` variants.
12. `_root/07_data_pipeline.md` — §7 per-format routing-block matrix **Good-News row** (authoritative): `CEO awareness: NO (always)`; `Expansion eligible: required`; `Watch health flag: required` (Good News only); substitutes `Current MRR / New MRR / Delta(negative)` for standard `Delta:` row; **omits Postgres live-data line** per §7 footnote; §6 file-naming (`good-news-notices/[ord_id]__[slug]__brief.md`).
13. `_root/08_quality_bar.md` — Good-News-applicable QB-NNN checks only if your task requires QA awareness; cite IDs in Section 4 checklist, do not restate check text.

### Cleanup-tracker items the new template must address

14. `_meta/stage3_cleanup.md` — read in full; apply specifically to Good News:
    - **CL-001** — confirm absent in archived Good News + preserve absence (no "no account-specific adjustments" sentence; Good News has no "How This Compares" section; reference `_root/04 §3` row in operator-notes for cross-format consistency).
    - **CL-003** — confirm absent + preserve absence (no peer dollar ranges; reference `_root/04 §3` row).
    - **CL-004** — confirm absent + preserve absence (no equivalent-platforms sentence; reference `_root/04 §3` row).
    - **CL-005 (ADDITIVE)** — ADD "What's Coming in 2026" via `_root/03 Section 3` pointer (archived OMITS; new template ADDS).
    - **CL-022** — delivery email routing-block subset inferred per Stage 3.1 / 3.2 / 3.3 precedent (see Step 4 Section 2).

### Archive references (explicitly authorized per `_root/CONTRACTS.md §4`)

15. `_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md` — prior Good News brief template (121 lines). Read for structural scaffolding ONLY. **Do NOT lift verbatim driver prose** at lines 44–80 — those blocks now live in `_root/05 §3.1.2 / §3.2.2 / §3.3.2`.
16. `_archive/2026-05-22__pre-refactor/good-news-notices/jyc__jamie-young/option-a__email-with-table.md` — calibration only (prior Option A delivery pattern; superseded by uniform brief + delivery email per operator stamp 2026-05-26).
17. `_archive/2026-05-22__pre-refactor/good-news-notices/pf__palecek/option-b__short-email-plus-doc.md` — calibration only (prior Option B delivery pattern; superseded by uniform brief + delivery email per operator stamp 2026-05-26).

### Pattern reference from Stage 3.1 + 3.2 + 3.3 (required — all operator-approved 2026-05-26)

18. Read all six approved template files in FULL:
    - `format-a-notices/_brief-template.md` + `_delivery-email-template.md`
    - `format-b-notices/_brief-template.md` + `_delivery-email-template.md`
    - `ceo-letter-notices/_brief-template.md` + `_delivery-email-template.md`

    **Match these 12 cross-format conventions exactly** (deviating produces operator review flags):
    1. Operator-notes blockquote header style
    2. Internal routing-note structure per `_root/07 §7`
    3. Driver dispatch table format (3 rows in-scope + out-of-scope increase drivers + `already_migrated` anomaly)
    4. Tier / roadmap pointer convention (Good News: Section 3 roadmap pointer only — no tier block)
    5. QA-checklist `>` blockquote convention citing QB-NNN by number
    6. Cross-references footer
    7. Section blockquote convention (`> **Section N — ...**`)
    8. Strict-placeholder precedent (operator-stamped 2026-05-26)
    9. "Your Pricing at a Glance" table structure (**Good News: 4-row mini form** — Monthly / Annual / Change / Effective date; NOT the 6-row increase-side table)
    10. Section presence pattern (Section 0 header / Section 1 operator notes / Section 2 routing / Section 3 brief skeleton / Section 4 checklist / footer)
    11. Bridge sentence position (Good News: operations-unchanged + consolidated 2026 framing per §3d + §3e below — no increase-side "Below is exactly why..." bridge)
    12. Subject-line "pricing" convention (brief title + delivery email subject per operator stamp below)

    **What you may legitimately deviate on** — only Good-News-specific scope per Step 2: 3 decrease-side drivers; CS/CSM authorship; `_root/04 §4.12` Good News close with **no formal-notice line**; `_root/04 §3.1` + `§4.5` Good News variants; routing-block fields (`Expansion eligible`, `Watch health flag`, no CEO fields, no Postgres line); 4-row summary table; lede is drafter-generated decrease sentence (dollar + effective date in sentence one); operator-notes "Do not send if" + "After sending" blocks from archived template; 10-day follow-up sentence as template scaffolding (operator-stamped 2026-05-26).

### Do NOT read

- Other format archives (Format A / B / CEO Letter / entity-packets) — out of scope.
- Other Good News exemplars beyond items 16–17.
- `_meta/stage2_prompts/**` and other `_meta/stage3_prompts/**` files beyond this prompt.
- `_reference/**` or `~/Downloads/**`.

---

## Step 2: Authoritative Good News scope (use as fact — do not re-derive)

**Mechanical scope** (per `_root/06 §3` row 1 + `_root/06 §1`):

- `Δ MRR < $0` (any decrease) routes to Good News.
- ~11–13 v6.2 template usages: 4 standard `Good-News Notice` + 7–9 HOLD-row `post_hold_action` Good News variants.
- **Watch-band carve-out** (per `_root/06 §4.2`): Good-News-eligible account that is Watch / At Risk / Critical does NOT receive Good News — routes through CSM for health check-in first; per-account operator decision in routing-CSV `post_hold_action`.
- **Annual overlay** shifts timing not substance (per `_root/02 §5` + `_root/06 §4.3`).
- **Entity-children** fold into entity packets (per `_root/02 §3`) — no standalone Good News brief for entity-children even if Δ < $0.

**Driver coverage** (per `_root/05 §3`):

| Driver | In scope? | Owning `_root/05` block |
|---|---|---|
| `module_compression` | YES | §3.1.2 mechanic + §3.1.4 pricing table |
| `user_count_variance` | YES | §3.2.2 mechanic + §3.2.3 pricing table |
| `rate_architecture` | YES | §3.3.2 mechanic + §3.3.3 pricing table |
| All 8 increase-side drivers | NO | n/a — escalate if routing produces one |
| `already_migrated` | n/a | Status-marker leak per `_root/05 §1.4`; no brief drafted |

**Voice posture** (per `_root/04 §3` + `_root/05 §3.1.5 / §3.2.4 / §3.3.4`):

- "Math, not a favor." State the mechanic plainly.
- Lead with dollar amount + effective date in sentence one. No percentage in the lede.
- No apology for prior pricing. No expansion language. All universal §2 + §3 prohibitions apply.

**Good News close** (per `_root/04 §4.12` Good News variant):

- `[INSERT _root/04 §4.12 Good News close — verbatim]`
- **NO formal-notice line** (Good News exception explicitly named in §4.12).

**Routing block** (per `_root/07 §7` Good-News row):

- General fields through `Comm_action` (substitute `Current MRR / New MRR / Delta(negative)` for standard `Delta:` row).
- `CEO awareness required before send: NO (always)`
- `Expansion eligible: required`
- `Watch health flag: required` (Good News only field among the 4 formats)
- **OMIT** Postgres live-data line per §7 footnote.
- Conditional rows per standard `_root/07 §7` convention (support fire; user-billing reconciliation; billing entity; tenure acknowledgment; Postgres-unavailable fallback applies differently — no Postgres line in Good News routing block).

**Authorship**: CS team sends; CSM signature (not CEO). Per archived template line 105 pattern: `*[CSM NAME] | [TITLE] | SuperCat*`.

**Operator-stamped subject conventions (2026-05-26)**:

- Brief title (Section 3a): `# [ACCOUNT_NAME]: Your Pricing Is Decreasing`
- Delivery email subject: `[ACCOUNT_NAME]: your SuperCat pricing is decreasing — effective [EFFECTIVE_DATE]`

---

## Step 3: What you are authoring — file 1 of 2: `good-news-notices/_brief-template.md`

Author the brief template as the following sections, in this order. **Every section either contains pure scaffolding OR a §-pointer. NO rule prose is inlined.**

### Section 0 — File header

```
# Good News Notice — Brief Template
*CS-led | Δ MRR < $0 (decrease-side per `_root/06 §3` row 1) | Good News close per `_root/04 §4.12` (no formal-notice line)*
```

### Section 1 — Operator notes (drafter-facing, removed before sending)

A `>` blockquote block naming:

- When to use (cite `_root/06 §1` + `§3` row 1; Watch-band carve-out cite `_root/06 §4.2`).
- Who sends (CS team; no CEO involvement; cite `_root/06 §1` + `_root/04 §4.12` Good News close register).
- What this template is NOT for (increase-side formats; entity-children; Watch/At-Risk/Critical without CSM clearance; point to rules, do not restate).
- Cleanup-tracker history (CL-001 / CL-003 / CL-004 confirmed absent + referenced; CL-005 ADDED via Section 3f; CL-022 delivery email subset inferred).
- Length target: 200–300 words (cite archived template operator notes).
- **Do not send if** block (preserve from archived template lines 110–115): Watch / At Risk / Critical; Unscored; entity-child packet not assembled; annual without renewal date — each with `_root/` pointer.
- **After sending** block (preserve from archived lines 117–120, with "invoice" normalized to "pricing" per 2026-05-26 universal subject-line stamp): log send date; 60-day notice clock; Format C queue rule; **10-day no-response follow-up** sentence as template scaffolding (operator-stamped 2026-05-26 — NOT promoted to `_root/04`): `"Just checking the above reached you — wanted to make sure the pricing change on [DATE] doesn't catch anyone off guard."`

### Section 2 — Internal routing block (drafter-facing, removed before sending)

A `>` blockquote mirroring `_root/07 §7` Good-News row exactly:

- `Brief type: good_news_notice | Format: Good News (decrease)`
- Standard general fields through `Comm_action`
- **`Current MRR: $[CURRENT_MRR] | New MRR: $[NEW_MRR] | Delta: –$[DELTA]/month`** (substituted for standard `Delta:` row per §7 footnote)
- **`Expansion eligible: [YES/NO]`** — required; queue Format C only after confirmed positive signal
- **`Watch health flag: [YES/NO]`** — required; if YES, DO NOT use this template (escalate per `_root/06 §4.2`)
- **`CEO awareness required before send: NO`** (always)
- **OMIT** Postgres live-data line (per §7 footnote)
- Conditional rows per `_root/07 §7` standard convention

### Section 3 — Brief content skeleton

#### 3a. Subject / brief title

`# [ACCOUNT_NAME]: Your Pricing Is Decreasing` + `*Effective [EFFECTIVE_DATE]*` (operator-stamped 2026-05-26).

#### 3b. Lede paragraph (always — drafter-generated)

Instructional comment: Good News leads with the mechanical decrease fact in sentence one — dollar amount + effective date. No percentage in lede per `_root/04 §2.1` + §3 row. This is drafter-generated prose (no `_root/` block owns the lede sentence shape). Pattern from archived template line 38:

`Your monthly invoice is decreasing from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a reduction of **$[DELTA]/month** — effective **[EFFECTIVE_DATE]**.`

Bracketed placeholders for drafter fill-in.

#### 3c. Driver dispatch (3 drivers only)

Section heading: `## Why the Number Is Changing` (or equivalent). Driver dispatch table:

| v6.2 `migration_driver` | Insert `_root/05` block verbatim from | Pricing table from | Notes |
|---|---|---|---|
| `module_compression` | §3.1.2 | §3.1.4 | Good News canonical |
| `user_count_variance` | §3.2.2 | §3.2.3 | Good News canonical |
| `rate_architecture` | §3.3.2 | §3.3.3 | Good News canonical |
| All 8 increase-side drivers | NOT carried | n/a | Escalate per `_root/CONTRACTS.md §2` |
| `already_migrated` | n/a | n/a | Status-marker leak; no brief |

`[INSERT_DRIVER_BLOCK]` placeholder after table. Template does NOT inline mechanic prose.

#### 3d. Operations-unchanged sentence

`[INSERT _root/04 §4.5 Good News variant — verbatim]`

#### 3e. Consolidated 2026 framing sentence

`[INSERT _root/04 §3.1 Good News consolidated 2026 framing sentence — verbatim]`

(Do NOT use the universal §3 row consolidated sentence — operator-stamped Good News addendum at `_root/04 §3.1`.)

#### 3f. "What's Coming in 2026" verbatim block (CL-005 — additive)

`## What's Coming in 2026` + `[INSERT _root/03 Section 3 verbatim block — verbatim, no substitution]`

#### 3g. "Your Pricing at a Glance" 4-row mini-summary table

| | Before | After |
|---|---|---|
| **Monthly** | $[CURRENT_MRR] | **$[NEW_MRR]** |
| **Annual** | $[CURRENT_ARR] | **$[NEW_ARR]** |
| **Change** | — | –$[DELTA]/month (–[DELTA_PCT]%) |
| **Effective date** | — | [EFFECTIVE_DATE] |

**Do NOT carry** the 6-row increase-side table (no Tier / Included users / Additional user rate rows).

#### 3h. Close section

`[INSERT _root/04 §4.12 Good News close — verbatim]`

**NO formal-notice line** — explicitly note the Good News exception per `_root/04 §4.12`.

#### 3i. Signature

`*[CSM NAME] | [TITLE] | SuperCat*` — CSM, not CEO.

### Section 4 — Pre-send drafter checklist

`>` blockquote pointing to `_root/08`. Cite 8–10 Good-News-applicable QB-NNN checks by number only — e.g. QB-002, QB-046 (roadmap present — CL-005), QB-059 (no "no account-specific adjustments"), QB-085 (no peer dollars), QB-086 (Good News close — no formal-notice line), QB-119 (path-reference contract). Do NOT restate check text.

Cross-references footer mapping every `_root/XX §N.M` the template touches.

---

## Step 4: What you are authoring — file 2 of 2: `good-news-notices/_delivery-email-template.md`

Uniform brief + delivery email pattern (operator-stamped 2026-05-26). CS sends; 3–4 sentences.

### Section 0 — File header

```
# Good News Notice — Delivery Email Template
*CS-sent | Wraps the Good News brief; warm low-touch voice per `_root/04 §4.12`*
```

### Section 1 — Operator notes

When to use; who sends (CS); length (3–4 sentences); what is NEVER in this email (cite `_root/04 §3` rows — gift/reward framing, apology, expansion language, percentage in lede, health-band names, peer dollars, competitor pricing); attach brief PDF per `_root/07 §6`; no CEO involvement; Good News has no formal-notice line in brief OR email.

### Section 2 — Internal routing block

Slim subset inferred per CL-022 (Stage 3.1 / 3.2 / 3.3 precedent + archived Good News patterns + brief Section 2). Include: Brief type, Account / Tier / Wave, Migration driver / Health, Current MRR / New MRR / Delta(negative), Cohort / Contract / Renewal, Earliest effective date, Attachment, CEO awareness: NO, **Expansion eligible**, **Watch health flag**. Flag in conformance block that subset is inferred pending `_root/07 §7` Wave 6 batch.

### Section 3 — Email body skeleton

- **Subject:** `[ACCOUNT_NAME]: your SuperCat pricing is decreasing — effective [EFFECTIVE_DATE]` (operator-stamped 2026-05-26)
- `Hi [CONTACT_NAME],`
- Sentence 1: drafter-generated decrease lede (mirror brief Section 3b — dollars + date; no percentage in lede)
- Sentence 2: `[INSERT _root/04 §4.5 Good News variant — verbatim]`
- Sentence 3: `[INSERT _root/04 §3.1 Good News consolidated 2026 framing sentence — verbatim]`
- Sentence 4 (optional attachment pointer): one-sentence pointer to attached brief (template scaffolding — flag in conformance block)
- Sentence 5: `[INSERT _root/04 §4.12 Good News close — verbatim]` (echo of brief close; no formal-notice line)
- Signature: `[CSM NAME] | Customer Success | SuperCat`

### Section 4 — Pre-send checklist

Cite QB-NNN; include attach-brief + log-send-date process notes cited to `_root/07 §6` + operator-notes "After sending" block.

### Section 5 — Voice calibration notes

Point to `_root/04 §4.12` Good News register: math not favor; no meeting offer; no call commitment; brief does the heavy lifting; email is the wrapper.

---

## Step 5: Anti-drift discipline

- **Path-reference contract is absolute** — strict-placeholder precedent operator-stamped 2026-05-26. Any prose owned by a `_root/` doc is a `[INSERT _root/XX §N.M ...]` placeholder, never inline — including `_root/04 §3.1`, `§4.5` Good News variant, `§4.12` Good News close.
- **ONLY inlined content**: drafter-facing scaffolding; section headings; table layouts; bracketed data placeholders; bridge/scaffolding sentences with no owning rule (10-day follow-up in operator-notes; optional attachment-pointer sentence in delivery email — flag in conformance block).
- **CL-001 / CL-003 / CL-004**: confirm absent; reference `_root/04 §3` rows in operator-notes.
- **CL-005**: ADD roadmap section via `_root/03 Section 3` pointer.
- **CL-022**: infer delivery email routing subset; flag in conformance block.
- **NOT Good-News-applicable**: CL-002, CL-011, CL-012, CL-013, CL-014, CL-015, CL-016, CL-017, CL-018, CL-019, CL-020, CL-021, CL-023 — document as out of scope in conformance block.
- **Do NOT carry** archived Option A / Option B dual delivery patterns — uniform brief + delivery email per operator stamp 2026-05-26.
- **Asking is cheap. Inventing is the drift vector.**

---

## Step 6: Voice and format constraints

- Declarative register; `>` blockquotes for drafter-facing blocks.
- `#` file title; `##` customer-facing sections; `###` inside drafter blocks.
- `[ALL_CAPS_WITH_UNDERSCORES]` placeholder convention.
- No emoji. No "Importantly" / "Critically".

---

## Step 7: Output

Create the new folder + both files:

- `Pricing Migration/good-news-notices/_brief-template.md`
- `Pricing Migration/good-news-notices/_delivery-email-template.md`

Then produce this conformance block in chat (NOT in the files) per `_root/00_manifest.md §5`:

```
─── Conformance Block ─────────────────────────────────────────
Session task: Stage 3.4 — author good-news-notices/_brief-template.md + _delivery-email-template.md
Output target:
- Pricing Migration/good-news-notices/_brief-template.md (NEW file, NEW folder)
- Pricing Migration/good-news-notices/_delivery-email-template.md (NEW file)

Files read (with last-updated date / mtime):
- <enumerate every file path from Step 1>

Explicitly-authorized archive reads (Step 1 items 15–17):
- <list with mtime>

Pattern-reference read (Step 1 item 18):
- <Stage 3.1 / 3.2 / 3.3 templates present/absent + conventions consulted>

Files NOT read:
- <per Step 1>

Brief template sections authored: <count + names 3a–3i>
Delivery email template sections authored: <count + names>

Drivers covered:
- In scope (3): module_compression §3.1.2+§3.1.4 | user_count_variance §3.2.2+§3.2.3 | rate_architecture §3.3.2+§3.3.3
- Out of scope (8 increase-side + already_migrated)

CL items addressed:
- CL-001 / CL-003 / CL-004 / CL-005 / CL-022: <template element for each>

Path-reference contract verification:
- Inlined rule prose count (should be 0): <count>
- §-pointer count by owning doc: <counts>
- Bracketed placeholder count: <count>

Good-News-specific verification:
- `_root/04 §3.1` pointer present (NOT universal §3 sentence): <yes/no>
- `_root/04 §4.5` Good News variant pointer present: <yes/no>
- `_root/04 §4.12` Good News close + NO formal-notice line noted: <yes/no>
- `Expansion eligible` + `Watch health flag` in routing block: <yes/no>
- Postgres line omitted from routing block: <yes/no>
- CEO awareness NO (always): <yes/no>
- 4-row summary table (not 6-row): <yes/no>
- CSM signature (not CEO): <yes/no>
- Brief title "Your Pricing Is Decreasing" + delivery subject "pricing is decreasing": <yes/no>

Routing-block field list cross-check (per _root/07 §7 Good-News row):
- <confirm / flag divergences>

Gaps surfaced: <list or none>
Conflicts resolved: <list or none>
Open questions for operator: <list or none>
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit `_root/`, other format folders, or `_meta/stage3_cleanup.md`.

---

## Step 8: If something is missing or contradictory

- Missing `_root/04 §3.1` or `§4.5` Good News variants at read time → STOP; flag — source fixes were applied 2026-05-26 Stage 3.4 prep; if absent, propagation failure (QB-125).
- Increase-side driver in Good News routing → escalate per `_root/CONTRACTS.md §2`; do not draft.
- Conflict between archived Good News inlined prose and `_root/05 §3` → `_root/05` wins.
- `_root/07 §7` Good-News row mismatch → flag both versions; do not pick one.

**Asking is cheap. Inventing is the drift vector.**
