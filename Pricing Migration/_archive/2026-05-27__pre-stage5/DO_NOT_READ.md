# DO NOT READ — SUPERSEDED ARTIFACTS (Pre-Stage-5 snapshot)

**Archived**: 2026-05-27 (Phase 0 of Stage 5 — Playbook Architecture Refactor)
**Reason**: The 4-format prose-and-mapping layer (`_root/03`, `_root/04`, `_root/05`, `_root/06`, `format-*-notices/` templates, `_meta/stage4_prompts/`) is being rebuilt to the 8-playbook architecture already stamped in `_root/02 §1`. Everything in this folder is the **pre-rebuild snapshot**, preserved only as the rollback/audit baseline.

---

## STOP

Everything in this folder is **pre-Stage-5 history**. It is preserved only as a deterministic rollback point + audit trail of what existed at 2026-05-27 before the Stage 5 refactor began.

**If you are an agent or operator drafting, planning, or QA'ing migration communications: do not read any file inside this archive.**

Per `_root/CONTRACTS.md §4`, the only legitimate readers of this archive are:

- The operator, for historical reference / rollback.
- An explicitly-instructed extraction task ("pull the verbatim X block from `_archive/2026-05-27__pre-stage5/_root/05_driver_taxonomy.md §2.1.5` and inline it into `_root/05 §<new>`"), directed by file path.

Browsing this folder to "see how the old templates worked" is forbidden under all conditions. The 4-format prose was the drift attractor that the Stage 5 refactor is correcting; inheriting any pattern from it without operator-stamped extraction reintroduces the drift.

The active system continues to live one level up:

- `Pricing Migration/_root/` — rule docs (under Stage 5 rebuild)
- `Pricing Migration/_meta/stage5_prompts/` — Stage 5 planning + per-phase prompts
- `Pricing Migration/_meta/v6_2_reconciliation_log.md` — unchanged; per-account ops cleanup tracker
- `Pricing Migration/_master-account-data-v6.2.csv` — unchanged; canonical
- `Pricing Migration/migration_comm_tiers_2026-05-19.csv` — unchanged; routing CSV

---

## Why this snapshot exists

The operator (CEO) reviewed the 2026-05-26 Stage 4.2 production output (`format-b-notices/cci__currey-and-company__brief.md`) against the 2026-05-19 archived pre-refactor brief (`_archive/2026-05-22__pre-refactor/format-b-notices/cci__currey-company__brief.md`) and observed that **the two artifacts are structurally identical** — same lede shape, same driver explanation prose, same pricing table, same tier description, same close, same formal-notice line. The only material differences: effective date update, lede paraphrase, and one added "What's Coming in 2026" section.

Root-cause analysis: `_root/04 §3` and `_root/05 §2.X` (driver blocks) explicitly cite the archived templates as **primary source** in their header front matter. The rebuild extracted the archive's prose into rule docs, then enforced verbatim paste of that prose via the path-reference contract. The output was structurally guaranteed to look like the archive — because the archive's prose IS the rule layer.

What's actually intended (per `_root/02 §1` 8-segment table, operator-stamped 2026-05-22, and the playbook table the operator shared 2026-05-27):

- 8 playbooks (Core / Narrative / Executive / Pre-Engagement / Entity / Strategic / Tailwind / Annual), not 4 formats
- 5 distinct artifact types (Standard Migration Notice / Simplified Value Summary / Value Migration Notice / Executive Letter / Entity Packet), not 1 long-brief shape with 4 close variants
- Substance distributed across **notice** vs **attached artifact** per playbook — not crammed into one 130-line brief
- Platform-vs-product-menu positioning ("SuperCat is a platform now; platforms have one price book"), not procedural "we're standardizing pricing"
- Pre-authorized + CEO-required concessions framework per playbook — currently absent entirely
- Per-playbook follow-up cadence + duration + mixed-segment handling + pilot/feedback loop

The Stage 5 rebuild authors the missing taxonomy docs, rewrites the source prose at the right granularity, rebuilds templates per playbook, and refreshes the Stage 4 drafter prompts. See `_meta/stage5_prompts/STAGE_5_PLANNING_AGENT_HANDOFF.md` for the full plan.

---

## What's in here (snapshot manifest — for rollback reference, do not act on)

| Path in snapshot | Pre-Stage-5 role | Stage 5 disposition |
|---|---|---|
| `03_what_we_sell.md` | Tier blocks + roadmap (feature-list framing) | Rewritten in Phase 3a for platform-vs-product-menu framing |
| `04_communication_posture.md` | 14 non-negotiables, 32-row forbidden-phrase table, named voice rules including 4 close variants in §4.12 | Rewritten in Phase 3a/3b — 8 playbook-specific closes; refreshed positioning sentence; expanded forbidden-phrase table |
| `05_driver_taxonomy.md` | 11 drivers × per-format prose blocks (§N.2 Format B, §N.3 CEO Letter, §N.4 Format A) | Recut in Phase 3c — per-driver prose at 3 form-cuts (short / mid / long) instead of 3 format-cuts |
| `06_format_routing.md` | 4-format dispatch table | Replaced in Phase 2 — 8-playbook dispatch keyed off `_root/02 §1` segments |
| `08_quality_bar.md` | 138 QB checks, ~12 format-keyed | Format-keyed checks rekeyed to playbook-keyed in Phase 6 |
| `format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/` | 4 format-keyed template folders | Replaced in Phase 4 by playbook-keyed folders (`core/`, `narrative/`, `executive/`, `pre-engagement/`, `tailwind/`, etc.); `entity-packets/` refined in place |
| `entity-packets/` | Stage 3.5 parent-letter templates (operator-approved 2026-05-26) | Refined (not rebuilt) in Phase 4 — closest alignment to Entity playbook |
| `_meta/stage3_prompts/` | Stage 3 template-build prompts (historical) | Not used post-Stage-5; preserved for pattern reference |
| `_meta/stage4_prompts/` | Stage 4 per-account drafter prompts (Format A + Format B drafted; CEO Letter / Good News / Entity Packet pending) | Replaced in Phase 5 by `_meta/stage5_prompts/stage_5_X__[playbook]__per-account-drafter.md` family |
| `_meta/stage3_cleanup.md` | CL-NNN tracker through CL-031 | Continues evolving at canonical location; this is a snapshot of its 2026-05-27 state |
| `_meta/stage4_account_ledger.md` | Per-account ledger (lpf + cci + sca rows) | Continues evolving at canonical location; this is a snapshot of its 2026-05-27 state |

**What is NOT snapshotted** (because it stays unchanged through Stage 5):

- `AGENTS.md` — folder entry / hard rules — unchanged
- `_root/00_manifest.md` — index — updated in lockstep with edits per `_root/CONTRACTS.md §3`
- `_root/CONTRACTS.md` — invariants — unchanged
- `_root/01_why_we_are_migrating.md` — thesis — unchanged
- `_root/02_who_is_being_migrated.md` — 8 segments already correct — unchanged
- `_root/07_data_pipeline.md` — data plumbing + reconciliation discipline — unchanged
- `_root/09_changelog.md` — audit trail continues
- `_master-account-data-v6.2.csv` — canonical data — unchanged
- `migration_comm_tiers_2026-05-19.csv` — routing CSV — unchanged
- `_reference/**` — strategic source — unchanged
- `_meta/v6_2_reconciliation_log.md` — 37-row ops cleanup tracker — unchanged
- `_meta/stage2_prompts/` — pre-refactor build prompts — already historical
- The prior `_archive/2026-05-22__pre-refactor/` and `_archive/2026-05-26__pre-cl-026/` snapshots — preserved untouched

---

*This file exists to prevent accidental drift. Do not delete it.*
