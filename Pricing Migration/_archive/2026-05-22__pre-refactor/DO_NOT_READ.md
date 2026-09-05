# DO NOT READ — SUPERSEDED ARTIFACTS

**Archived**: 2026-05-22
**Reason**: Full system refactor to eliminate cross-template drift. All operational artifacts in this folder are SUPERSEDED.

---

## STOP

Everything in this folder is **pre-refactor history**. It is preserved only as a historical record of what was tried before the root-doc architecture was put in place.

**If you are an agent or operator drafting, planning, or QA'ing migration communications: do not read any file inside this archive.**

The active system lives one level up:
- `Pricing Migration/_root/` — authoritative rules, voice, drivers, routing, quality bar
- `Pricing Migration/_root/00_manifest.md` — required-reading entry point
- `Pricing Migration/format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/` — active templates + agent prompts
- `Pricing Migration/_reference/` — read-only source data (execution plan v3.3, HTML revenue model)

---

## Why this matters

Every voice rule, driver framing, non-negotiable, and quality check that previously lived in this folder has been moved to the appropriate `_root/` doc. Reading files here will surface stale, contradictory, or superseded rules and silently introduce drift back into the system.

If you believe you need something from this archive, that's a signal that a `_root/` doc has a gap. Per `_root/CONTRACTS.md`:

1. Stop drafting.
2. Identify the missing rule.
3. Ask the operator to add it to the appropriate `_root/` doc.
4. Log the change in `_root/09_changelog.md`.
5. Resume from `_root/00_manifest.md`.

---

## What's in here (for reference only, do not act on)

- All per-account drafts (briefs + delivery emails) generated 2026-05-19 → 2026-05-20 under the pre-refactor system
- The four pre-refactor `_brief-template.md` and `_delivery-email-template.md` files
- The four pre-refactor `_fresh-agent-prompt.md` files
- The pre-refactor `_handoff-prompt.md` (242 lines, was carrying constitutional/voice/data/quality content inline)
- `_current-state.md`, `_roadmap.md`, `_template-test-prompt.md`
- `_master-account-data-v6.1.csv` (older snapshot — v6.2 is authoritative)
- Two stale HTML status artifacts (`migration_comms_progress_*.html`, `migration_plan_alignment_*.html`)
- The pre-refactor `README.md`

---

*This file exists to prevent accidental drift. Do not delete it.*
