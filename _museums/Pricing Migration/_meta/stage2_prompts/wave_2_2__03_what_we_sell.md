# Wave 2.2 — Authoring Prompt for `_root/03_what_we_sell.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/03_what_we_sell.md` (replace stub contents)
> **Estimated authored length**: 250–400 lines
> **Dependency**: Independent. Can be authored after Wave 1 produces `_root/01` + `_root/CONTRACTS.md`. Parallelizable with Wave 2.1 and Wave 2.3.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. Your job is to author **one file** — `Pricing Migration/_root/03_what_we_sell.md` — using only the materials this prompt directs you to.

**Critical distinction for this prompt:** there are TWO product-language registers in SuperCat documentation:
- **Strategic / internal register** (in `foundation 2/`) — names tiers, gives reasoning, includes peer ranges, discusses competitive positioning. This is for SuperCat operators, board, and prospect-facing strategy work.
- **Comms-ready / customer register** (in the migration templates) — describes what the customer GETS at each tier in plain English, without strategic framing or competitive context. This is for customer-facing briefs and delivery emails.

Your job: **author the comms-ready register** as the canonical source. The strategic-register content (peer ranges, tier ratios) is captured here only as INTERNAL-only reference, clearly tagged.

You will not improvise. If anything is unclear, stop and ask the operator.

---

## Step 1: Required reading (in this exact order)

Read each file completely. Echo each file path + last-updated date in your first chat response.

### Folder orientation (mandatory)
1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` (the stub — read the "owns / does not own" boundary)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` (read to understand the migration context that "what we sell" is being repriced into)

### Primary content sources — comms-ready language (explicitly authorized archive reads)

You ARE permitted to read these specific archive files for verbatim language extraction. This is an explicit per-prompt override of the anti-archive rule per `_root/CONTRACTS.md` §4.

6. **Format A brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md`. Read the sections titled "What You're Getting at $[NEW_MRR]/month" and "What's Coming in 2026". These contain the **canonical comms-ready language** for tier features and roadmap.

7. **Format B brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_brief-template.md`. Read the same two sections.

8. **CEO Letter brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_brief-template.md`. Read the same two sections.

9. **Good News brief template** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/good-news-notices/_brief-template.md`. Good News won't have the same tier-language structure (no price increase to justify), but it will have *some* tier-feature language — extract it.

10. **The user-rate ladder and peer ranges** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md` §"Key Reference Tables" (search for this exact section heading). This section contains the user-rate ladder ($25 / $22 / $20 / $18) and the per-tier peer-range mappings used internally. **The peer ranges are INTERNAL-ONLY** — they appear in your authored doc only inside a clearly-tagged INTERNAL section, never in comms-ready language.

### Primary content sources — strategic register (inlined here in the prompt)

The next two blocks are extracted from `~/Downloads/foundation 2/03_how_we_make_money.md`. **Do NOT go to the source file** — the relevant content is inlined here. Integrate these into the doc's INTERNAL section only.

> **— BEGIN FOUNDATION EXCERPT (foundation 2 / 03_how_we_make_money.md §"Stamped price points" + §"User expansion") —**
>
> **Stamped price points (D-004a — stamped 2026-02-25)**
>
> | Tier | Platform fee | Included users | Included brands |
> |---|---:|---:|---:|
> | **T1 Catalog Essentials** | **$749/mo** | 10 | 1 |
> | **T2 Commerce Professional** | **$1,295/mo** | 15 | 3 |
> | **T3 Commerce Enterprise** | **$2,295/mo** | 40 | 5 |
>
> Tier ratios: T2/T1 = 1.7×; T3/T2 = 1.8×; T3/T1 = 3.1× — squarely within the 1.5–2.5× best-practice band for G/B/B packaging.
>
> **User expansion (D-004b — stamped 2026-02-25)**
>
> Step-declining per-user curve beyond the included base:
>
> | Additional users beyond included | Per-user / mo |
> |---|---:|
> | 1–25 | $25 |
> | 26–50 | $22 |
> | 51–100 | $20 |
> | 101+ | $18 |
>
> **— END FOUNDATION EXCERPT —**

> **— BEGIN FOUNDATION EXCERPT (foundation 2 / 03_how_we_make_money.md §"Where T2 sits competitively") —**
>
> | Tier | SuperCat | AmpTab equivalent | Pepperi equivalent | Notes |
> |---|---:|---:|---:|---|
> | T1 ($749) | $749/mo | AmpTab Starter $500/mo (sticker) / $917/mo (Y1 effective with $5K setup amortized) | Pepperi Pro $1,220/mo at 15 users | SuperCat sits in the competitive sweet spot |
> | T2 ($1,295) | $1,295/mo | AmpTab Advanced $1,000/mo / $1,833/mo Y1 effective | Pepperi Corporate $3,450/mo at 25 users | SuperCat is the clear value play |
> | T3 ($2,295) | $2,295/mo | AmpTab Pro $3,000/mo / $5,500/mo Y1 effective | Pepperi Ultimate $6,400+/mo | SuperCat is 23% below AmpTab Pro sticker, ~58% below Y1 effective |
>
> Stripping out raw rate-card differences, **SuperCat's full-stack Y1 effective price is within 15% of AmpTab at every tier**.
>
> **— END FOUNDATION EXCERPT —**

> **— BEGIN FOUNDATION EXCERPT (foundation 2 / 03_how_we_make_money.md §"Implementation") —**
>
> Tiered by customer **data readiness**, not module count:
>
> | Implementation tier | When it applies | Fee |
> |---|---|---:|
> | **Essentials** | Standard data, ready to import | **Included** in subscription |
> | **Guided** | Moderate data prep / mapping required | **$2,500** |
> | **Comprehensive** | Heavy data work, multiple sources, custom mapping | **$5,000** |
>
> **— END FOUNDATION EXCERPT —**

### Do NOT read

- `~/Downloads/foundation 2/**` — the relevant excerpts are inlined above. Reading the full foundation risks scope-creep into strategic-register prose that doesn't belong in this doc.
- Any other root-doc stub beyond items 1–5.
- Any other archived brief beyond items 6–10.

---

## Step 2: What you are authoring

`_root/03_what_we_sell.md` is the **product-language source of truth** for migration communications. Every "What You're Getting at $X" block in every brief draws from this doc. The doc has two layers — a customer-facing layer and an internal-only layer — clearly tagged so a drafter never mixes them.

Author the doc as the following sections in this order:

### Section 1 — The three tiers, in comms-ready plain English

A subsection per tier (`### T1 — Catalog Essentials`, etc.). For each tier:
- **Headline price**: from the stamped foundation excerpt above (T1 $749/mo / T2 $1,295/mo / T3 $2,295/mo).
- **Included users**: 10 / 15 / 40.
- **Included brands**: 1 / 3 / 5.
- **"What You're Getting at $X" block**: VERBATIM from the Format A / Format B / CEO Letter brief templates. These templates have iterated language that the operator considers final. Where the three templates phrase the SAME tier slightly differently, use the most recent (Pricing Migration archive) version and flag the discrepancy in your conformance block.
- **Plain-English feature list**: 4–8 bullets per tier. Customer language — "rep app for iPad," "buyer-facing online catalog," "self-serve cart and order tracking," "analytics dashboards" — never "iPad-native CPQ-enabled sales-rep mobile capability." Source these from the brief templates, NOT from foundation 2's strategic-register descriptions.

The whole point of this section is: a drafter copying a "What You're Getting at $X" block into a customer brief reads THIS section, finds the exact verbatim block, and pastes it. No rewording. No translation from strategic-register to comms-ready.

### Section 2 — The user-rate ladder (comms-ready)

Two blocks:

**Block A — the customer-facing ladder** (a Markdown table — this is the ladder customers see in briefs):

| Additional users above included base | Rate |
|---|---|
| 1–10 excess users | $25/user |
| 11–25 excess users | $22/user |
| 26–50 excess users | $20/user |
| 51+ excess users | $18/user |

**IMPORTANT:** Note the discrepancy with the foundation excerpt above. The foundation excerpt is keyed to *additional users beyond the included base* in bands of 1–25 / 26–50 / 51–100 / 101+. The templates use bands of 1–10 / 11–25 / 26–50 / 51+. These appear to differ. **Use the templates' band structure as canonical for customer-facing comms** (this is what's been iterated against real briefs) and **flag the foundation discrepancy in your conformance block** so the operator can reconcile in foundation 2 if needed.

**Block B — internal note** (clearly tagged `> **INTERNAL**`): the strategic intent behind the ladder (step-declining curve to create volume incentive; fixes Problem 1 of the foundation's "Five problems"). One paragraph.

### Section 3 — "What's Coming in 2026" verbatim block

The "What's Coming in 2026" block appears in every brief template. It is the customer-facing roadmap statement. It is iterated to exact wording.

Extract this block VERBATIM from the Format A brief template (item 6 above). Render it in your doc as a fenced quote. Future drafters will copy this exact block into briefs. Do not rewrite. Do not "improve."

If the Format B, CEO Letter, and Good News templates have DIFFERENT versions of "What's Coming in 2026," cross-compare and:
- If they're equivalent in substance but differ in phrasing: use the most recent (Pricing Migration archive) version as canonical.
- If they're substantively different (different features promised, different timelines): flag in conformance block. Do not silently reconcile.

### Section 4 — Implementation tiers

A short subsection. The Essentials / Guided / Comprehensive table from the foundation excerpt above. Include the **comms framing** the templates use (if any — search the brief templates for "implementation" or "Essentials"; if no template references implementation in customer-facing language, note that and recommend to the operator that this section may not actually be needed for migration comms, since implementation is rarely surfaced in re-pricing notices).

### Section 5 — Peer ranges (INTERNAL-only)

A clearly-tagged INTERNAL section. The peer ranges from the archived `_handoff-prompt.md` §"Key Reference Tables" + the competitive table from the foundation excerpt above (item 2 inline).

Heading: `## Section 5 — Peer ranges and competitive positioning (INTERNAL — strip before send)`.

Add a blockquote at the top of this section: `> **INTERNAL ONLY.** The peer ranges and competitive comparisons in this section are reference for the drafter to confirm a new MRR sits "within range." They are never quoted to the customer. They never appear in customer-facing artifacts. The "How This Compares" section of a brief uses peer ranges as a CHECK — the brief itself states "this falls within the typical range for accounts of your size and usage" without naming dollar values. See `_root/04` §4.11 for the comms-ready treatment.`

Then render the peer ranges as a table.

### Section 6 — Add-ons and unpublished premiums

A short subsection. Reference the foundation excerpt above for the unpublished-premium SKUs (Commerce $795/mo, Sales Intelligence $995/mo, Premium Support $495/mo). Tag as INTERNAL — these are response-only and never appear in proactive comms.

### Section 7 — What this doc does NOT own

- The "why we're moving to tiers at all" reasoning → `_root/01`
- Voice/tone rules for how to *introduce* tier language in a brief → `_root/04`
- Per-driver narrative content (which tier a customer is moving to, framed for that account's driver) → `_root/05`
- The data field that carries a customer's `new_tier` value in the v6.2 CSV → `_root/07`

### Header block

Match the pattern:
- `> **Last updated**: 2026-05-22`
- `> **Owner**: CEO`
- `> **Primary sources**: foundation `03_how_we_make_money.md` (inlined excerpts in this prompt — §"Stamped price points," §"User expansion," §"Where T2 sits competitively," §"Implementation"); archived Format A/B/CEO Letter/Good News brief templates (the "What You're Getting" and "What's Coming in 2026" verbatim blocks); archived `_handoff-prompt.md` §Key Reference Tables (peer ranges, INTERNAL only)`
- `> **What this doc owns** / `> **What this doc DOES NOT own**` — populate

---

## Step 3: Anti-drift discipline

- **Verbatim is verbatim.** The "What You're Getting at $X" blocks and "What's Coming in 2026" block are character-for-character copies from the templates. Any rewording risks the customer seeing two slightly-different versions across different briefs.
- **INTERNAL stays INTERNAL.** Sections 5 and 6 (peer ranges, add-ons) are tagged `INTERNAL` and a drafter copying from this doc into a customer brief should immediately see the tag and stop. Do not let INTERNAL content leak into Sections 1–4.
- **The foundation excerpts ARE this doc's data backbone.** Don't paraphrase the stamped foundation tables; render them as given.

---

## Step 4: Voice and format constraints

- Register: customer-facing in Sections 1–4 (because the content is what customers will read); operator-facing in Sections 5–7 (because the content is for the drafter, never the customer).
- Tables for the price/user/implementation matrices.
- Fenced blockquotes for the verbatim "What You're Getting" and "What's Coming" blocks.
- INTERNAL sections get a prominent `> **INTERNAL ONLY**` blockquote at top.

---

## Step 5: Output

Replace the entire current contents of `Pricing Migration/_root/03_what_we_sell.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/03_what_we_sell.md (replaced stub)
Files read: <enumerate items 1–10 from Step 1 with last-updated dates>
Explicitly-authorized archive reads: Migration-Health Artifacts format_a template; Pricing Migration/_archive/.../format-b/CEO/Good News brief templates; Pricing Migration/_archive/.../_handoff-prompt.md §Key Reference Tables (per Step 1 items 6–10 and Section 5 of the spec)
Files NOT read: ~/Downloads/foundation 2/** (excerpts inlined in prompt); other root-doc stubs; other archived briefs
Tiers authored: <count, should be 3>
Verbatim "What You're Getting at $X" blocks extracted: <count, should be 3 (one per tier)>
Verbatim "What's Coming in 2026" block extracted: yes/no + source template
User-rate ladder bands authored: <bands used + source>
Discrepancies between foundation excerpt and template language (and my resolution): <list, or "none">
Discrepancies between Format A / B / CEO Letter / Good News templates on the same content: <list with my chosen canonical source, or "none">
INTERNAL-tagged sections: <list>
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. The operator will paste your output back for review.

---

## Step 6: If something is missing

If a tier's "What You're Getting" block isn't found in the expected templates, or the foundation excerpts and template language disagree in substance (not just phrasing), stop and ask the operator. Do not synthesize a "best-of-both" version. The operator's reconciliation is a `_root/09_changelog.md` entry that propagates correctly.
