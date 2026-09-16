"""Insightful Pipeline — agent-orchestrated Python factory.

Produces PASS3-quality Markdown drafts on demand for any org. The pipeline
covers ~80% of report assembly; the remaining 20% is surgical hand-polish
(see SURGICAL_EDIT_GUIDE.md).

Architecture follows the Health V3 pattern: cache layer (immutable CSVs per
org per date) → preflight → gather → signals → assemble. Output MD feeds
into the existing report_render/ HTML pipeline unchanged.

Module surface ownership (the bug is cross-talk):
  config      paths, query-id manifest, constants
  cache       MCP/PG → CSVs; never reads results
  preflight   cache CSVs → RunPosture; never runs SQL
  gather      cache CSVs → typed dataclasses; never runs SQL
  signals     gather output → fired Signals with SIGNAL_RANK; never writes prose
  assemble    signals + gather + posture → Jinja2 → MD; never runs SQL or detects signals
  narrative   §1 hero framing LLM call; never reads cache directly
  smoke_check minimal validation (file exists, sections non-empty); not a gate library

CLI entries:
  populate_cache.py   one-off per org per date; writes cache/{org}/{date}/*.csv
  run_report.py       reads cache, writes outputs/{org}_DRAFT_{date}.md
"""
__version__ = "0.1.0"
