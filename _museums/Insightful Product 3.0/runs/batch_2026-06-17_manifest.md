# Batch Manifest — 2026-06-17
- **Clients processed**: 1
- **Ready for section agents**: 1
- **Failed**: 0
- **Total elapsed**: 86.4s

## Ready for LLM Section Agents

| Shortname | Elapsed | Bundles Dir |
| --- | --- | --- |
| shl | 86.4s | `runs/shl_2026-06-17/cache/` |

## Next Steps

For each ready client, spawn a fresh agent with the orchestrator prompt.
The agent only needs to:
1. Spawn 5 section agents (parallel) using section_build_prompt.md
2. Build Signal Summary (§1) from highlights + signal_rank
3. Run: `python scripts/assemble_report.py --shortname X --run-date Y`
4. Run: `python scripts/audit_report.py --shortname X --run-date Y`