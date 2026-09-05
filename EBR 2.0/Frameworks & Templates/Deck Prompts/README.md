# EBR Deck Prompts — How This Works

This folder contains all Cursor prompts used to generate and maintain Executive Business Review decks. Read this before touching anything.

---

## Generation Flow

```
Step 1 → Step 2 → Step 3 → Step 4
Account Brief    Data Layer    Deck Build    Refinement
```

### Step 1 — Generate Account Intelligence
**Prompt:** Not stored here — lives in `Frameworks & Templates/Account_Brief_Prompt_v2.md`
**Inputs:** Raw eCat data export + HubSpot account record
**Outputs saved to:** `Accounts/[AccountName]/Account Overview/`
- `Brief_[AccountName]_[YYYY-MM].md` — Full B1-B8 intelligence brief
- `Snapshot_[AccountName]_[YYYY-MM].md` — A1-A6 one-page summary
- `GenerationNotes_[AccountName]_[YYYY-MM].md` — What was and wasn't available

### Step 2 — Review Data Layer Rules
**Prompt:** `EBR_Data_Cursor_Prompt.md`
**Purpose:** Governs how data is interpreted, displayed, and suppressed in the deck.
Read this before running Step 3. It defines:
- TTM vs. MoM rules (always TTM — never raw MoM without market calendar context)
- Market calendar seasonality flags (Priority 1 events must be called out inline)
- Feature suppression rules (never show zeros for features that aren't activated)
- Calculation definitions: Breadth, Top Concentration, Adoption Rate, AOV
- Rep concentration thresholds and risk levels
- Deferred data dependencies (what requires a separate pipeline)

### Step 3 — Generate the Deck
**Prompt:** `EBR_Generation_Prompt_v2.md`
**Inputs:** Brief + Snapshot + Generation Notes from Step 1 + rules from Step 2
**Output saved to:** `Accounts/[AccountName]/Decks/EBR_[AccountName]_[YYYY-MM].html`
This prompt builds the full 17-slide HTML deck. It references the design system,
slide structure, component patterns, and all strict content rules.

**Do not run this without completing Steps 1 and 2 first.**

### Step 4 — Refinement (if needed)
Any post-generation edits follow the rules in `EBR_Data_Cursor_Prompt.md`.
Always update in place — do not rebuild from scratch.
Save refined output back to the same path: `Accounts/[AccountName]/Decks/EBR_[AccountName]_[YYYY-MM].html`

---

## Prompt Files — What Each One Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `EBR_Generation_Prompt_v2.md` | Master deck generation spec — design system, 17-slide structure, CSS components, strict rules | Step 3 — every deck build |
| `EBR_Data_Cursor_Prompt.md` | Data layer rules — TTM logic, market calendar, suppression rules, calculation definitions | Step 2 — review before every build; Step 4 — refinement reference |
| `Template_A_Discovery.md` | Original 12-slide discovery-led template (Gabby/SC v1) | Archive / reference only |
| `Template_B_Intelligence.md` | Original 14-slide intelligence-led template (Gabby/SC v1) | Archive / reference only |
| `Template_C_Benchmark.md` | Original 14-slide benchmark-forward template (Gabby/SC v1) | Archive / reference only |
| `Template_HYBRID.md` | Original 15-slide hybrid synthesis (Gabby/SC v1 — recommended) | Archive / reference only |

**Note:** Templates A, B, C, and HYBRID were the v1 generation prompts for Gabby/SC.
`EBR_Generation_Prompt_v2.md` supersedes all four — it incorporates the best of each
template plus all formatting and data refinements made in the March 2026 update session.

---

## Naming Convention

All files follow: `[DocumentType]_[AccountName]_[YYYY-MM].[ext]`

| Document type | Example |
|--------------|---------|
| Deck | `EBR_Gabby_SC_2026-03.html` |
| Intelligence Brief | `Brief_Gabby_SC_2026-03.md` |
| Account Snapshot | `Snapshot_Gabby_SC_2026-03.md` |
| Generation Notes | `GenerationNotes_Gabby_SC_2026-03.md` |
| Reference doc | `EBR_Gabby_SC_2026-03_reference.md` |

---

## For a New Account

1. Run `Account_Brief_Prompt_v2.md` with the new account's data → save outputs to `Accounts/[NewAccount]/Account Overview/`
2. Read `EBR_Data_Cursor_Prompt.md` — no changes needed, it's account-agnostic
3. Run `EBR_Generation_Prompt_v2.md` with the new account's Brief + Snapshot + GenerationNotes
4. Save deck to `Accounts/[NewAccount]/Decks/EBR_[NewAccount]_[YYYY-MM].html`

---

## What Requires a Separate Data Pipeline

These items are stubbed in the current deck and cannot be generated from prompt alone:

- Rep performance through 6 activities (needs eCat activity schema)
- Low/mid/high performer cohort analysis (needs rep segmentation model)
- Account scores — B2 scoring model (adoption depth, business impact, growth signals)
- HubSpot SuperCat Fit score (needs HubSpot integration)
- Recent engagement narrative (needs HubSpot + HelpScout API)
- TTM trend chart — monthly revenue over 12 months (needs time-series data)
- B2B commerce funnel breakdowns (needs funnel data)
- Instance health detail (needs eCat admin API)

---

*Last updated: March 2026 — EBR 2.0 refinement session*
