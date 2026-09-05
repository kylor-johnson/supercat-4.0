# eCat_Onboarding — pointers only, not the implementation tree

**Canonical implementation, source data, and build work lives at:**

```
~/repos/ecat-onboarding-workspace/02_Implementation/<Client Name>/
```

iCloud mirror (do not treat as the edit surface):

```
SuperCat_Simple_Final/02_Implementation/<Client Name>/
```

Use full client names there (`Dorell`, `Legrand`, `Lib & Co Onboarding`,
`Magic Lite`, `Pebl`, `Teracotta`, `The CopperSmith`, `Fine Art`, `111Mercer`,
`jcusa`), not shortnames.

**Never recreate a live client folder in this directory.** This folder is
kickoff + registry + pointers. Client CSVs belong in the private
`kylor-johnson/ecat-onboarding-workspace` repo.

## What happened on 2026-09-03

This folder had drifted into a second, partial copy of the implementation tree —
including **41 Python build scripts that duplicated canonical paths**, several of
them stale. Legrand's `build_ecat_files.py` here was 143 lines behind the live one.
A stale runnable build script is how the wrong file gets imported into the wrong org.

So:

1. Every file here that was **newer than, or absent from,** canonical was copied
   across. 24 new files, 8 updates (each with a `.bak_20260903_pre-merge` beside it).
   Manifest: `02_Implementation/_MERGE_FROM_SUPERCAT4_2026-09-03.md`
2. Files where canonical was already newer were **left alone**.
3. The client folders were moved to `_ARCHIVE_superseded_2026-09-03/`.
   Nothing was deleted — images in particular were never merged and still live there.

## Still only in the archive

**Images.** They diverge in both directions and were deliberately not merged —
reconciling them needs knowing which batches actually reached FTP:

| batch | archive | canonical |
|---|---|---|
| `images_batch_02_NEW` | 500 | 0 |
| `images_batch_03_NEW` | 500 | 5 |
| `images_batch_01_NEW` | 500 | 121 |
| `images_missing_batch` | 0 | 613 |

## What legitimately still lives in SuperCat 4.0

The onboarding **assessment** work — not implementation:

- `onboarding-models/` — the Phase Progression framework (v3.6)
- `onboarding-models/collector/` — corpus, rawstate and collector tooling
- `onboarding-models/ground-truth/` — SCORECARD, BUILD_SPEC, SESSION_HANDOFF, blind-read handoffs
- `onboarding-models/ground-truth/clients/<sn>/` — the per-client blind reads
  (CORPUS / JOURNEY / GAPS / RAWSTATE), moved here 2026-09-03
- `eCat_Onboarding/REGISTRY.yaml` — machine-readable client registry
- `eCat_Onboarding/00_KICKOFF_PROMPT.md` — session starter
- `eCat_Onboarding/jcusa.md` — pointer to Implementation `jcusa`
