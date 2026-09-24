# Onboarding agents

This folder holds the four onboarding agents Kylor built between 2026-08-18
and 2026-09-15. Each file here is the source. There is no second copy
anywhere else in git.

The five skills below are symlinked from `.cursor/skills/<name>`, so Cursor
still loads them from their usual path. Edit the file in this folder, or
through the symlink. Either way it is the same file.

`ground-truth/SESSION_HANDOFF.md` swaps agents 3 and 4. The numbers in this
README are the correct ones.

| # | Agent | Folder | Runs as | Reads |
|---|---|---|---|---|
| 1 | Data ingestion | `1-ingestion/` | Python pipeline | Local files. Postgres over the VPN for two checks |
| 2 | Settings configuration | `2-config-check/ecat-config-check/` | Skill, read-only | Postgres over the VPN, plus `1-ingestion/config_intent.toml` |
| 3 | HelpScout triage and reply | `3-helpscout/` | Three skills, drafts only | BigQuery (Airbyte mirror, about 6 hours behind) |
| 4 | Meeting prep | `4-session-prep/ecat-session-prep/` | Skill | Postgres over the VPN, among other sources |

## 1. Data ingestion: `1-ingestion/`

This is the former `onboarding-models/`, moved whole so relative paths still
resolve.

```
cd onboarding-agents/1-ingestion
/opt/homebrew/bin/python3 runner/run_ingestion.py --client <shortname>
```

The interpreter must have both `tomllib` and `openpyxl`. See
`runner/README.md`.

- `runner/` is the entry point. It contains `preflight.py`, `sandbox.py`,
  `clients.toml` (six clients: leg, mer, libco, drf, tcs, mali), and
  `FINDINGS_runner.md`. None of the six clients exits 0 yet, and
  `FINDINGS_runner.md` explains why.
- `profiler/` is Phase 0, `ecatlib/` is Phase 1, and `mapping/` plus
  `mappings/<client>/*.toml` are Phase 2.
- `acceptance/` holds the post-import checks, including `dbexec.py`.
- `config_intent.toml` and `overrides.toml` are declared intent. Agent 2 reads
  `config_intent.toml` too.

`clients.toml` points by absolute path into iCloud `SuperCat_Simple_Final`.
Client CSVs stay there. Never copy one into this repo.

**Assessment, not an agent.** `ground-truth/` and the weekly phase assessment
(`Phase_Anchors.md`, `Flags_and_Signals.md`, `Output_Contract.md`,
`RUN_PROMPT.md`, `collector/`, `render_phase_assessment.py`) are evidence and
a standup. They are not agent 1, and they are not a fifth agent. They live
here so the docs sit next to the code they describe.

## 2. Settings configuration: `2-config-check/`

`ecat-config-check` answers one question: what about this org's Admin
configuration is wrong, missing, or contradictory. It reads
`1-ingestion/config_intent.toml` before it reports anything. The kickoff and
spec are `1-ingestion/ground-truth/KICKOFF_config_check.md` and `BUILD_SPEC.md`
§4. This agent never writes to Admin. Applying a change is the job of
`ecat-admin-write`, which stays in `.cursor/skills/`.

## 3. HelpScout triage and reply: `3-helpscout/`

| Skill | Job |
|---|---|
| `ecat-correspondence` | Decides which tickets need a reply and whether a draft is safe to send |
| `ecat-support-triage` | Diagnoses one ticket against live org state |
| `ecat-client-email` | Writes the reply in Kylor's voice |

The inbox loop does not diagnose and does not write the prose. Nothing here
sends mail. There is no HelpScout write credential, so the output is drafts
only. `FINDINGS_agent4.md` (2026-09-05) records what this agent shipped and
what it found. Its filename uses the old numbering. The relative paths inside
it (`acceptance/`, `mapping/`, `ground-truth/`) now point under `1-ingestion/`.

## 4. Meeting prep: `4-session-prep/`

`ecat-session-prep` builds the brief for the next client conversation. The
brief is what changed since the last conversation, not a status dump.

## Hosting

All four run locally from Cursor or Claude Code. A hosted copy is not newer
than the files here. Agents 1, 2 and 4 need Postgres on the VPN. Agent 3
reads only BigQuery, so it is the only one that could run elsewhere. That
decision has not been made.
