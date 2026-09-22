# Insightful Product 4.0 — SUPERSEDED

**Do not work in this directory.** On 2026-09-22 this tree was split in two and
everything here became the pre-extraction record.

| Where | What |
|---|---|
| `kylor-johnson/insightful` | the product. All development happens here. |
| `kylor-johnson/insightful-client-data` | caches, profiles, authored prose, rendered briefs and the programme's handoffs, read through `INSIGHTFUL_DATA_ROOT` |

```bash
git clone git@github.com:kylor-johnson/insightful.git
git clone git@github.com:kylor-johnson/insightful-client-data.git
cd insightful && make venv
export INSIGHTFUL_DATA_ROOT=../insightful-client-data
./run.sh <org> --date <YYYY-MM-DD>
```

## Nothing was lost

Every one of the 155 files that used to sit here is in one of those two repos.
Verified file by file, including the ones that moved rather than copied:

| Was here | Is now |
|---|---|
| `handoffs/exec/TRAPS.md` | `insightful/TRAPS.md` |
| `AUDIT_FINDINGS.md`, `CHANGELOG_archive.md` | `insightful-client-data/handoffs/` |
| `foundation/provenance_map_rep.md`, `operators/rung4_option_a_operator.md`, `foundation/capability/insights_moneymap_SYNTHESIS.md` | `insightful-client-data/doctrine/` |
| the four client-calibrated test suites | `insightful-client-data/tests_client/` |
| everything else | `insightful/` |

The caches and rendered reports came across too — 23 org/date cache
directories and 47 output files, all present in the client-data repo.

## Why the folder is still here

The files are untracked from `HEAD`, not deleted. They remain on disk and in
**this repo's history**, which is the only reason to keep the folder: the
Phase 11 golden re-stamp was justified by diffing against the artifacts in
this tree, and that provenance should stay checkable.

It also cannot be cleaned by deleting files. This repo's history holds 6,008
lines matching client names across several unrelated projects, which is
precisely why the product needed a repo that never contained any.

## If you change something here

It goes nowhere. The new repos do not read from this tree, it has no CI, and
the product repo fails its build if a client name reaches it — a change made
here and copied across would bypass that check, which is the one thing the
split exists to prevent.
