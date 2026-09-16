# House-Rep Exclusions — per-org allow/deny (Rung-4 / S1+C2 by rep / RS-01 leaderboard)

> **What this is.** The **rep-label screen** for any rep-grain query that renders a `rep_label` (RS-01
> leaderboard in `rep_copilot_operator.md` §3, O1/O2 in `rung4_option_a_operator.md` §2, the §2 coaching
> cards and §3 mini-briefs in `report_operator.md` Step 5a). House/brand/distributor entities ride in on
> the `rep_name` side and must be screened out of every rep-named surface before any digest, leaderboard,
> or report ships.
>
> **This file changes NO economics logic.** It is a screen applied *after* the locked SQL queries.
> Built read-only 2026-06-29; auto-rule added 2026-06-30 (PASS1 validation findings on cci/kal).
>
> **Two states:** `EXCLUDE` = confirmed (org-self / literal house bucket / dead code) — drop on every run.
> `CONFIRM` = candidate (brand/distributor/e-comm-channel styled) — **owner must vet before it becomes EXCLUDE**;
> until vetted, surface it but flag it, never silently drop (the §7.1 red line).

## AUTO-RULE — fires on EVERY org, regardless of config presence

**Any rep whose `rep_label` matches `ILIKE 'house%'` (case-insensitive) is treated as a house bucket
and screened from every rep-grain render** (RS-01 leaderboard headline, rung-4 O1/O2 coaching cards,
report §2 cards, §3 mini-brief rep cells, "This Week's Outreach List"). This is non-negotiable and
fires whether or not the org appears in the EXCLUDE table below.

**Why an auto-rule and not just a longer table.** Validation (2026-06-30) found cci's `HOUSE ACCOUNT`
rendering at **#1 on the §2 leaderboard ($9.96M, +51%)** and kal's `House Account` (rep 0999) holding
**$1.60M LTM / 71 accounts** and tagged as the **top S1 $-at-risk rep ($695K)** — kal was not in this
file. A CEO opening the §2 leaderboard to "HOUSE ACCOUNT, $9.96M, +51% YoY" is the single most
reputation-damaging defect the report can produce. The auto-rule catches this class even when a new
org hasn't been onboarded into the EXCLUDE table.

**Pattern (canonical SQL fragment, applied identically in every rep-grain query):**

```sql
-- House-rep AUTO-RULE — applied to every rep-grain query that renders rep_label.
-- Catches: HOUSE ACCOUNT (cci), House Account (kal rep 0999), HOUSE-* / House Account - X variants.
AND COALESCE(rep_label, '') NOT ILIKE 'house%'
AND COALESCE(rep_label, '') NOT ILIKE '% house account%'   -- e.g. wwjc "12 House Account", "30440 Interim Rep House Account"
```

The second clause catches the `<prefix> House Account` forms (wwjc's `12 House Account` /
`30440 Interim Rep House Account`); the first clause catches the bare `House Account` /
`HOUSE ACCOUNT` / `Housekeeping ...` / `House Brand` forms. The per-org `EXCLUDE` table below
remains the source of truth for **non-`house*`-named** house entities (org-self brand names like
`Capital Lighting Fixture` at clc, `Ratana` at ril, `Ecom-Sidney` at mhc, `PALECEK - LAGUNA SHOWROOM`
at pf) — the auto-rule would not catch these by name.

**Determinism guarantee:** any rep-grain query that renders a `rep_label` MUST apply BOTH the
auto-rule fragment above AND the per-org `EXCLUDE` rows from the table below. A query that applies
only one is non-compliant; Step 10 of `report_operator.md` flags this in the render-time check
(`HOUSE-LEAK` check, see report_editorial_rules_v4.md §N).

## Confirmed EXCLUDE (drop on every rerun) — owner-confirmed 2026-06-29

| Org | id | rep_label (exact) | Reason |
|---|---|---|---|
| clc | 40 | `Capital Lighting Fixture` | Is the org itself (Capital Lighting Fixture Co.) — house book |
| cci | 161 | `HOUSE ACCOUNT` | Literal house account |
| wwjc | 8 | `12 House Account` | Literal house account |
| wwjc | 8 | `30440 Interim Rep House Account` | Interim/house bucket |
| pf | 32 | `PALECEK - LAGUNA SHOWROOM` | Org's own showroom (Palecek) — house |
| pf | 32 | `GMASOUTH - SO/SO CAL TERRITORY` | Territory rollup bucket, not a person |
| pf | 32 | `DC BRANDS INC` | Distributor/brand-styled entity |
| pf | 32 | `LUXECO / ELITE LIGHTING` | Brand/distributor; outlier 29.7% leak rate |
| mhc | 46 | `Ecom-Sidney` | E-commerce house channel, not a person |
| mhc | 46 | `Multimeuble - Caribbean` | Distributor entity |
| ril | 245 | `Ratana` | Is the org/brand itself (Ratana International Ltd.) — house |
| ril | 245 | `Thomas York*DoNoUse` | Code explicitly tagged "DoNoUse" |
| bcf | 171 | `Morgan Horwitz: E-Comm` | E-commerce house channel |

> All 13 rows **owner-confirmed 2026-06-29** (the 6 former CONFIRM candidates promoted to EXCLUDE this session).
> Re-confirm an org only if its account-code/rep-code scheme changes (D4).

## Explicit KEEP (legitimate outside rep agencies / individuals — do NOT exclude)

These rank high but are the **real reps** (at clc/pf/bcf/wwjc the reps *are* agencies). Listed so a future
pass doesn't over-screen by pattern (`Inc`/`LLC`/`Associates`/code-prefix ≠ house):

- **clc:** KTR Associates, Vince Hall and Associates, California Lighting Concepts, Integrity Lighting Sales,
  York Sales, Texas Lighting Agency, Envision Lighting Sales, Lighting Resource Group, Glassman Brands,
  Starry Lights & Associates, Philip Winston Inc, Winston & Associates, Prairie Lakes, Dean Coxworth
- **pf:** JAY HOME FURNISHINGS LLC/PRINE, BOROWY STEVEN - MDA LITES, JEROME GROUP, LJR HOSPITALITY INC-LEX ROY
- **wwjc:** 107 Nixon and Associates, 111 TC North Design Lines, 114 Beyond The Sale LLC, the `105:x JDouglas` sub-reps
- **bcf:** Todd Teague (Twinco Inc.), SVB Enterprises Inc/Steve Bill, Jerry Montini (Beachside Furn),
  Closter Sales Inc, Home Decor/Jack Johnson, Moody Sales LLC, Tracey Thomas Furn Inc/Tracey
- **sarreid:** all top reps are individuals — no exclusions

## Notes (do not act on these as exclusions)

- **Soft dupes (G-A), flag-only, never auto-merge:** sarreid `Deborah Klein` vs `Deborah Klien` (two rep#s, typo);
  mhc `Jamie Kennedy` vs `Jamie Kennedy-US`. `DISTINCT ON (rep_number)` already collapses same-rep# multi-spellings.
- **Unmapped rep numbers are never dropped** (§7.1): bcf `rep 3`, `rep 28` stay in as `rep <n>`.
- **mhc is DORMANT** (Tier-2, stale feed) — its $ are historical; exclusions still apply when its digest runs.

## Provenance

- Read-only via `user-supercat-postgres-vpn`, 2026-06-29. Source queries: `rung4_option_a_operator.md` §2 (O1/O2),
  verbatim, top-12 per axis. Org names resolved from `organizations`.
- All 13 exclusions owner-confirmed 2026-06-29 (no rows left pending); re-confirm an org only if its
  account-code/rep-code scheme changes (D4).
