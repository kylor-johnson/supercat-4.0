# Wave 1.3 — Authoring Prompt for `_root/04_communication_posture.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/04_communication_posture.md` (replace stub contents)
> **Estimated authored length**: 400–600 lines (this is the rule-density doc of the entire system)
> **Dependency**: Independent. Can be authored in parallel with Wave 1.1 and Wave 1.2.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `_root/04` is the highest-leverage drift-control doc in the entire system — every voice failure, every forbidden phrase that slipped through, every inconsistency between two briefs traces back to a rule that either wasn't here or wasn't here clearly enough. Your job is to **extract, consolidate, and crisply state** every voice and language rule that has accumulated across the pre-refactor system, in one place, with no duplication.

Because the existing system has 8+ templates and 5+ orchestration files that each carry voice rules inline, the operator is using a fresh agent — you — to do the consolidation **independently of the drafting bias** that produced the duplication. Your output will become the single source of truth that future drafters reference, never restate.

You will not improvise. You will not invent rules. You will extract rules that exist, deduplicate them, and render them precisely.

---

## Step 1: Required reading (in this exact order)

This is a large reading list. Read it all before writing. Echo each file path + last-updated date in your first chat response so the operator can verify.

### Folder orientation (mandatory)
1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` (read in full)
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` (the stub you're about to replace — read the "owns / does not own" boundary carefully)

### Primary content sources — the pre-refactor archive (this prompt EXPLICITLY authorizes reading these despite the general anti-archive rule in `_root/CONTRACTS.md` §4)

You are extracting voice rules that today live scattered across these files. You will be the last agent to read these — once you've consolidated, future agents read only `_root/04`.

5. **The handoff prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md`. Read **the full file**. Pay special attention to these sections:
   - §"Non-Negotiables — Every Draft Must Pass All 9" (lines ~137–150) — these are the headline rules
   - §"Language Register" (lines ~151–171) — forbidden phrases, replacements, voice register
   - §"Driver Framing" (lines ~172–191) — voice-shaping rules per driver (driver content itself goes to `_root/05`; the voice posture per driver stays here only as a one-paragraph orientation, see §spec below)
   - §"Quality Bar — Every Draft Before Send" (lines ~227–end) — checks that imply rules

6. **The template-test prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_template-test-prompt.md`. Read **the full file**. Each of the 8 named CHECKs (CHECK 1 through CHECK 8) encodes a voice or content rule that was retroactively bolted onto the templates after a draft violated it. Every one of them must be present in your authored output as a rule (not just as a check — the check goes to `_root/08`; the rule it enforces lives here).

7. **The current-state doc** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_current-state.md`. Read §"Template Fixes Applied (2026-05-19)" and §"Decisions Made". These document the *evolution* of the rules — every "fix" is a rule that was missing and is now present. Cross-reference against the handoff to ensure no fix was lost in translation.

### Primary content sources — the templates themselves (where the voice rules live inline as `> **... rule:**` blockquotes)

These are the templates whose voice rules you are consolidating. Each contains 3–6 inline rule blockquotes that need to be extracted, deduplicated against each other, and reframed as standalone rules.

8. **Format A brief template** (canonical, pre-pre-refactor) — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md`. Read in full. Note especially the inline rules: "Tone rule", "Included user change rule", "Platform base repricing rule", "Above the midpoint rule" (search for it), "Lede stat guardrail" (search), "Only thing changing" line conditional, "What Happens Next" close.

9. **Format A delivery email template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_delivery_email.md`. Read in full. Extract the voice posture for the delivery email envelope (the email that delivers the brief — its voice is distinct from the brief's voice and that distinction is a rule).

10. **Format B brief template (refined)** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md`. Read in full. Note especially the High-Delta Lede Rule (delta >30%), the IUR fork, the platform base repricing rule, the "Let's Talk" close.

11. **Format B brief template (earlier era)** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_b_normalization_significant_delta.md`. Read in full. Where it differs from #10, the *later* (Pricing Migration archive) version wins on conflicts — but read this earlier version to see what original design intent existed that may have been lost.

12. **CEO Letter brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md`. Read in full. The CEO voice has its own rules — peer-to-peer, "I'll call you personally by [DATE]" close, the high-delta annual-dollar acknowledgment, the personal-tenure acknowledgment for early-adopter cohorts.

13. **Good News brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md`. Read in full. Good News has its own voice: warmer, less defensive, no apology, and an explicit "we caught this; you don't have to do anything" posture. Extract these.

14. **Format C — expansion/upgrade template** (earlier era, for future) — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_c_expansion_upgrade.md`. Read in full. Format C is not in active rotation but its voice rules belong in `_root/04` so that when Format C is built out post-migration, the rules already exist.

15. **Good News alternate template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_good_news_notice.md`. Read in full. Cross-check against #13.

16. **Internal CEO/CS prep sheet template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/internal_ceo_cs_prep_sheet.md`. Read in full. This is an INTERNAL-only voice (operator-facing). Its rules belong here only insofar as they establish the "internal voice vs. client voice" boundary — a rule.

### Primary content sources — exemplar briefs (the "voice in practice" reference)

Read these to see the rules instantiated. Where a brief's actual voice contradicts a rule you've extracted from the templates, flag it as a question for the operator — do not invent a reconciliation.

17. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kal__kalco-allegri-crystal__brief__v2.md` (Format A, post-fix exemplar)
18. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/kii__kennedy-international__brief__v2.md` (Format A, IUR exemplar)
19. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/ih__interlude-home__brief__v2.md` (Format B, post-fix exemplar)
20. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/da__dainolite__brief.md` (CEO Letter, high-delta exemplar)
21. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/pf__palecek/option-a__email-with-table.md` (Good News, email-with-table exemplar)

### Do NOT read

- Any other `_root/` doc beyond the ones in items 1–4 — your scope is `_root/04`. Other docs are being authored in parallel.
- Any other archived brief beyond items 17–21 — you have enough exemplars. Reading more risks accreting per-account exceptions into general rules.
- Any file outside the `Pricing Migration/` and `Migration-Health Artifacts/` folders — the rules you need live in these two folders.

---

## Step 2: What you are authoring

`_root/04_communication_posture.md` is the single source of truth for **voice and language rules** in the migration communications system. Every rule in this doc gets referenced (never restated) by templates, agent prompts, the quality bar, and per-account drafts.

Author the doc as the following sections, in this order:

### Section 1 — Audience and posture (the foundation)

One short section (~150 words) defining:
- **Audience**: The reader is the CFO, business owner, or principal of a B2B furniture/lighting/decor wholesaler — not a procurement agent, not an end-user. They read a small number of vendor pricing communications per year. They are sophisticated. They notice tone. They will not respond well to corporate-speak or apology language.
- **Voice posture**: Declarative, professional, empathetic on impact, firm on architecture. Peer-to-peer (CEO Letter) or vendor-to-principal (Format A/B) — never service-rep-to-buyer.
- **Internal vs. client boundary**: Briefs and delivery emails are CLIENT-FACING. Internal prep sheets, routing notes, fresh-agent prompts, and root docs are INTERNAL-ONLY. The "internal routing note" blockquote at the top of every brief is removed before sending. State this boundary explicitly and name it as a non-negotiable.

### Section 2 — The non-negotiables

A numbered list. Extract every "Non-Negotiable" from the archived `_handoff-prompt.md` §"Non-Negotiables — Every Draft Must Pass All 9". You may renumber, deduplicate, and lightly rewrite, but you may not delete or soften any.

Then, scan the 8 CHECKs in the archived `_template-test-prompt.md`. Each CHECK encodes a rule that was added because a draft violated something. Promote each into the non-negotiable list if it is not already covered. Cross-reference with the §"Template Fixes Applied" section of `_current-state.md` to catch any rule that was added after the handoff was written.

Final list should be 9–14 non-negotiables, each one a single declarative sentence with a one-sentence rationale.

### Section 3 — The forbidden phrase / replacement table

A Markdown table with three columns: **Do not write** | **Replacement** | **Why**.

Extract the forbidden-phrase content from the archived `_handoff-prompt.md` §"Language Register". Add any "do not say X / say Y" rules embedded in the template blockquotes (e.g. the "logins as a ratio of provisioned users" prohibition, the "per-order subscription cost in the lede" prohibition, the "leading with the percentage" prohibition).

The table should be comprehensive — 15–30 rows. Each row pairs a specific forbidden phrase with a specific replacement, plus a brief rationale. Do not aggregate (no "various corporate-speak phrases"). Be specific. The whole point is that future drafters can grep this table for the exact phrase they're tempted to use.

### Section 4 — Named voice rules (each as its own short subsection)

Each rule below gets its own `###` subsection with the rule name as the heading. State the rule. Show one example that follows it (extract from an exemplar brief in items 17–21). Show one example that violates it (you may invent a violation if no archived example exists — make it minimal, one sentence).

Required rules (extract precise wording from the indicated sources; do not paraphrase loosely):

- **§4.1 — Opening: relationship-before-price.** Source: Format A template "Tone rule" + Format B template lede block. The lede names the relationship (tenure, platform stats) before the price change, in the same paragraph. Never the reverse. Tenure-band variations: 3+ years, 10+ years.
- **§4.2 — Lede stat guardrail (the provisioned-vs.-active prohibition).** Source: `_template-test-prompt.md` CHECK 7. Use unambiguous platform metrics (users, sessions, surfaces active, tenure). If order count is used, scope it to "orders submitted through SuperCat" — never the account's total order volume. Do not frame logins as a ratio of provisioned users. Do not calculate per-order subscription costs in the lede.
- **§4.3 — Above-the-midpoint user-count clause.** Source: `_template-test-prompt.md` CHECK 5. State the rule precisely.
- **§4.4 — High-delta lede rule (delta >30%).** Source: CEO Letter template + `_template-test-prompt.md` CHECK 8. State the annual-dollar acknowledgment requirement.
- **§4.5 — "Only thing changing" line + IUR fork.** Source: `_template-test-prompt.md` CHECK 4 + the IUR blocks in Format A/B templates. State the conditional precisely.
- **§4.6 — Platform-base-grown sentence.** Source: Format A template "Platform base repricing rule". State the conditional (when `new_tier_base > current_platform_mrr`) and the exact sentence to use. Per the source: this is verbatim — do not paraphrase, do not synthesize, copy the exact sentence.
- **§4.7 — Tenure acknowledgment for early-adopter cohorts (pre-2016).** Source: CEO Letter + Format B templates. State the trigger (cohort year ≤2015) and the required content (named years, "fundamentally different product" framing).
- **§4.8 — Value anchor delta-per-order reframe.** Source: `_template-test-prompt.md` CHECK 6 + Format A "What This Works Out To" sections.
- **§4.9 — Billing basis definition (italicized footnote).** Source: `_template-test-prompt.md` CHECK 2 + CHECK 3 — the italicized footnote that follows IUR and `included_user_reduction` tables.
- **§4.10 — Platform base conditional in `user_rate_normalization` block.** Source: `_template-test-prompt.md` CHECK 1.
- **§4.11 — "How This Compares" structure.** Source: search the archived briefs for "How This Compares" sections (it appears in many) — extract the canonical two-sentence structure: one sentence positioning the new MRR/MRR-delta within a peer range; one sentence on why the peer comparison is fair. This is INTERNAL-language-bordering: be careful. The peer range itself (the dollar values) is INTERNAL-ONLY and gets stripped before send.
- **§4.12 — Close variants by format.** Source: each template's close. Format A → "What Happens Next" (CS-led). Format B → "Let's Talk" (CS-led, with meeting offer). CEO Letter → "I'll call you personally by [DATE]" (CEO-led, with specific date commitment). Good News → "you don't have to do anything" (operator-led, no ask). State each variant verbatim where it exists in the templates; do not invent new close language.
- **§4.13 — Health-band overrides (Watch / At Risk / Critical).** Source: Format A template "[LEDE BLOCK — Thriving and Healthy accounts only…]" + CEO Letter template "[For Watch/At Risk health bands…]". State: for Watch/At Risk/Critical health bands, the relationship-stats lede is suppressed; lead directly with the dollar change. State the precise threshold (Value Delivery <40, Watch/At Risk/Critical health band).
- **§4.14 — Discount-correction posture.** Source: each template's "[ADD FOR PLATFORM_DISCOUNT_CORRECTION ACCOUNTS]" block. State the substitution rule for the standard "rate at signing" sentence.

### Section 5 — Driver-voice orientation (one-paragraph; the driver content itself lives in `_root/05`)

A single paragraph (~150 words): each migration driver shapes the voice of the brief slightly differently. URN leads with the user-rate history. IUR leads with the included-base expansion (often a *win* for the customer). `tier_base_increase` leads with the "platform has grown" framing. `discount_correction` leads with the discount-retiring framing. `special_arrangement` leads with the relationship-historicity framing. **Do not author per-driver narrative content here** — that's `_root/05`'s job. Just state that the *voice* shifts per driver and point forward.

### Section 6 — What this doc does NOT own (closing reminder)

A short closing section that lists what `_root/04` does NOT own and points to the owning doc for each:
- Per-driver narrative content (the actual "Why the Number Is Changing" prose) → `_root/05`
- Tier feature language ("T1 includes…") → `_root/03`
- Segment / format mapping (who gets Format A vs CEO Letter) → `_root/02` + `_root/06`
- Data field meanings (what `migration_driver` IS) → `_root/07`
- The quality checklist (the verification procedure) → `_root/08`

### Header block

Match the pattern in the other root-doc stubs:
- `> **Last updated**: 2026-05-22`
- `> **Owner**: CEO`
- `> **Primary sources**: archived `_handoff-prompt.md` §Non-Negotiables + §Language Register + §Quality Bar; archived `_template-test-prompt.md` (CHECKs 1–8); archived `_current-state.md` §Template Fixes Applied; archived Format A/B/CEO/Good News brief templates; Migration-Health Artifacts seed templates`
- `> **Supersedes**: voice rules previously scattered across the templates and orchestration files listed above`
- `> **What this doc owns** / `> **What this doc DOES NOT own**`: populate with your final section list

---

## Step 3: Anti-drift discipline (this is the doc you are authoring, so model the discipline)

- **Every rule lives in exactly one §-section.** If you write the same rule in two sections, you've already created the drift you're authoring this doc to prevent.
- **No rule is restated in a footnote or appendix.** If a rule needs emphasis, it gets its own subsection. Never a "see also" duplication.
- **Verbatim phrasings stay verbatim.** Some content (e.g. the platform-base-grown sentence, the CEO call-commitment close, the "What's Coming in 2026" block — though that block lives in `_root/03`, not here) is verbatim across all templates because it was iterated to exact wording. Where you encounter verbatim content, copy it character-for-character. Do not "improve" it.
- **Rules borrow each other's authority by reference, not by copy.** If §4.5 needs to acknowledge §4.2, write "(see §4.2)" — do not restate §4.2.

---

## Step 4: Voice and format constraints

- Register: operator-facing, declarative, no marketing language. Same register as `AGENTS.md` and `CONTRACTS.md`.
- This is a *long* doc. Use clean Markdown structure: `##` for the 6 sections, `###` for each named rule inside Section 4, tables where called out, blockquotes only for verbatim copy from templates that you are preserving.
- Each rule's "Example that follows it / Example that violates it" pair should be one or two sentences each, in a fenced block:
  ```
  ✅ Follows: <one-sentence example>
  ❌ Violates: <one-sentence example>
  ```
  (The checkmark/X-mark glyphs are permitted here as visual structural markers — they are NOT emojis in the prohibited sense; they are functional. If preferred, use plain text "Follows:" / "Violates:" labels.)
- No exhortation. No "Importantly," "Critically," "This is the most important rule." Section ordering already implies importance.

---

## Step 5: Output

Replace the entire current contents of `Pricing Migration/_root/04_communication_posture.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/04_communication_posture.md (replaced stub)
Files read (21 total): <enumerate every file path from Step 1 with its last-updated date>
Files NOT read: every other root-doc stub, every other archived brief, anything outside Pricing Migration/ and Migration-Health Artifacts/
Rules extracted — non-negotiables (Section 2): <count, e.g. "11">
Rules extracted — forbidden phrases (Section 3): <count, e.g. "23 table rows">
Rules extracted — named voice rules (Section 4): <count, e.g. "14 subsections (§4.1 through §4.14)">
Source rules I expected but did not find (gap report): <list, or "none">
Conflicts between sources (e.g. template version A says X, template version B says Y): <list with my chosen resolution, or "none">
Verbatim content preserved character-for-character: <list of the specific verbatim blocks, e.g. "the platform-base-grown sentence (§4.6)", "the CEO call-commitment close (§4.12)">
Self-audit — rules I duplicated within this doc: <list, or "none — every rule appears in exactly one §-section">
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. The operator will paste your output back to the planning agent for review before the next wave begins.

---

## Step 6: If something is missing or contradictory

The whole point of this exercise is to surface implicit, accreted, or contradictory rules and make them explicit. If you find:
- A rule embedded in one template but not another → flag it. The operator may want it canonical, or the operator may have intended the difference. Don't infer.
- A `_template-test-prompt.md` CHECK that doesn't map cleanly to template content → flag it.
- A rule in `_handoff-prompt.md` §Non-Negotiables that doesn't appear in any template → flag it. This is either a missing implementation or a stale rule.
- An exemplar brief that violates an extracted rule → flag it. This is either a rule that needs amendment or an exemplar that needs correction.

For each flag: state the conflict in your conformance block under "Open questions for operator." The operator's answer becomes a `_root/09_changelog.md` entry and a clarification you propagate.

**Asking is cheap. Inventing is the drift vector.**
