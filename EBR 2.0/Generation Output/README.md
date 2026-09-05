# Generation Output — Working Directory

This is a **temporary working directory** for the Account Brief generation pipeline (Prompt 1).

When you run `Account_Brief_Prompt_v2.md` against a new account or refresh an existing one, the raw outputs land here first:

```
[Account]_Intelligence_Brief_v1.md
[Account]_Snapshot_v1.md
[Account]_Generation_Notes_v1.md
```

## After generation, move files to the correct account folder:

```
EBR 2.0/
└── Accounts/
    └── [Account_Name]/
        ├── Account Overview/     ← Canonical consolidated docs (renamed per convention)
        │   └── Archive/          ← Per-entity v1 files and superseded versions
        └── Decks/                ← Final HTML decks + reference docs
```

## Naming convention

```
[DocumentType]_[AccountName]_[YYYY-MM].[ext]

Examples:
  Brief_Gabby_SC_2026-03.md
  Snapshot_Gabby_SC_2026-03.md
  GenerationNotes_Gabby_SC_2026-03.md
  EBR_Gabby_SC_2026-03.html
```

## Rules

- Do not leave final deliverables in this directory — move them to the account folder after review
- Per-entity intermediate files go to `Account Overview/Archive/`
- Consolidated/canonical files get renamed per the naming convention above
- This directory should be empty between generation runs
