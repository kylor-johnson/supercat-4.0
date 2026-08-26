---
id: WORKING
title: Working set — what is reproducible and what is not
version: 0.1
status: reference
date: 2026-08-25
owner: Kylor Johnson
---

# Working set

The data and scripts behind Phases 1 and 4. Preserved so nobody re-derives them by hand.
**580 KB. No client data** — public HPMKT directory listings, public website observations, and
roster-derived marker flags.

## data/

| File | What it is | Reproducible? |
|---|---|---|
| `frame.csv` | 836 rows / 693 unique HPMKT exhibitors — name, building, space, floor, neighborhood. Upholstered Furniture + Lamp & Lighting | Yes, ~15 min (`harvest.py`) |
| `companies_dd.csv` | The frame with building-rows removed and dedupe verdicts against Postgres `organizations` | Yes, but the **hand-adjudication of 21 brand families is not scripted** — see below |
| `attrs.json` | Directory-declared attributes: Designer Friendly, PricePoint High/Medium-High/Medium, Contract/Hospitality | Yes, ~20 min (`harvest2.py`) |
| `cands_m.csv` / `ranked.csv` | 246 candidates with observed channel markers and lane scores | **Snapshot-dependent** — sites change |
| `features.csv` | The 109-org roster with Layer B markers. **The Phase 1 back-test input** | **Snapshot-dependent** |
| `backtest_rows.csv` | Per-org archetype + stamped segment. Produces the 33.3% figure | Deterministic from `features.csv` |
| `orgs.csv` | Roster joined to normalised domains, with the 3 malformed `company_website` values fixed | Yes |
| `all_reach.txt` | HTTP reachability of the 95 distinct roster domains, 2026-08-25 | Snapshot |

## scripts/

`harvest.py` / `harvest2.py` — HPMKT directory harvest (server-side filters, `?pageindex=N&filters={...}`).
`build_set.py` — roster + domain working set.
`markers.py` / `cmark.py` — channel-marker extraction from fetched HTML.
`seg_rule.py` — Layer A precedence rule and its 38.5% reproduction figure.
`backtest.py` — Layer B back-test, produces the 33.3% figure and the correspondence matrix.
`rank.py` — lane scoring.

## NOT preserved

**437 fetched homepages (99 MB).** Too large, and a snapshot that will not reproduce identically as
sites change. Re-fetching is ~45 minutes with `harvest.py`'s fetch loop. **Re-running the marker
scripts against fresh pages will produce different numbers** — the Phase 1 back-test figures
(33.3% / 65% / 34.5% baseline) are stamped 2026-08-25 and should be cited with that date, not
recomputed and silently updated.

## Two things a re-run must not skip

1. **Hand-adjudication of brand-family dupes.** Automated name matching missed Sauder (6-char key),
   Oly (3-char), Allegri→Kalco (token order), Wildwood/Chelsea House and Mitzi→Hudson Valley
   (compound/sub-brand). The list is in `../prospects/disqualified.md` §1. Automation alone puts
   existing customers on a prospect list.
2. **Hostname matching, never token matching, for competitor detection.** Loose tokens produced
   7 fictional NuOrder installs from `"menuOrder":3` in Wix JSON. See
   `../prospects/competitor-platform-signal.md` §2.
