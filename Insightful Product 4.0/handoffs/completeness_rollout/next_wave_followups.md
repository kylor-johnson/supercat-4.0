# Next wave — logged follow-ups from Track E (2026-07-09)

Track E (Sarreid re-baseline + cci anointing) is **complete**. These are real findings
from that work that are **out of Track E's scope** to fix, but must not be dropped.
Owner (Kylor) explicitly asked these be logged, not silently forgotten. No priority
order implied by numbering.

---

## 1. ✅ Comment-leak bug — FIXED (2026-07-09)

**What:** Templates used a raw markdown `<!-- QUERY-NEEDED: ... -->` comment as their
"there's no data, don't render anything" placeholder. The markdown→HTML step did
**not** treat this as a real HTML comment — it escaped `<` / `>` and printed it as
**visible client-facing text**. Track E fixed the one instance that was live on the
two golden orgs (`section_05_layers.md.j2`'s "Platform readiness floor"). All
remaining sites are now fixed.

**Fix applied — two-layer approach:**

1. **PRIMARY (durable, class-wide):** `report_render/md_render.py` — added
   `_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)` and `_strip_html_comments()`
   called inside both `md_to_html()` and `md_inline_to_html()` before the markdown-it
   render. This is the renderer-level fix that catches any future `<!-- -->` that ever
   reaches the MD layer, regardless of template origin. No markdown-it option changed.

2. **HYGIENE (trivially safe):** Converted all 10 remaining raw `<!-- ... -->` dev-notes
   in the affected templates to Jinja `{# ... #}` comments (which Jinja strips entirely
   at render time, never reaching `md_render.py`):
   - `section_10_channels.md.j2` lines 69, 113
   - `section_05_layers.md.j2` line 141
   - `section_06_team.md.j2` lines 24, 57
   - `section_08_products.md.j2` lines 20, 42
   - `section_03_thismonth.md.j2` lines 48, 52, 114

**Verified (2026-07-09):** Full pipeline render + smoke_check + step10 on all 8 orgs
(sarreid, cci, da, bmc, hfg, kal, sca, ali) — all PASS. Zero `<!--` and zero
`QUERY-NEEDED` in any fresh HTML output. `da` pre-fix had 6 QUERY-NEEDED leaks;
post-fix has 0. sarreid + cci golden checksums are **byte-identical** to the Track-E
freeze (no re-baseline needed — these orgs have full caches and never hit the
`<!-- -->` branches).

---

## 2. ✅ Rep-behavior floor (VM-R1–R4) — BUILT 2026-07-09

**What was built:** Phase 1 investigation (`handoffs/completeness_rollout/phase1_rep_floor_proposal_2026-07-09.md`) confirmed the gap and proposed three OWNED legs. Phase 2 (approved by owner, 2026-07-09) implemented:

- **`foundation/query_library_v2.md`**: Q-R1 (rep activity & cadence), Q-R2 (coverage penetration), Q-R4 (quote→submit discipline) — all Postgres MCP, owned tables, always-on. Routing table entries added.
- **`pipeline/gather.py`**: `RepActivityRow`, `RepCoverageRow`, `RepQuoteDisciplineRow` dataclasses + `load_rep_activity/coverage/quote_discipline` loaders + `GatherBundle.rep_activity/rep_coverage/rep_quote_discipline` fields + wiring in `gather_all()`.
- **`pipeline/config.py`**: Q-R1/R2/R4 added to `QUERIES_PLATFORM` (always-on) + schemas in `QUERY_SCHEMAS`.
- **`pipeline/templates/section_06_team.md.j2`**: `### Rep activity floor` H3 block added at top of §6, fires for ALL tiers. Each leg independently guarded (omit-not-stub). No "eCat" in client prose — step10 §P passes clean.

**Verification (2026-07-09):** All 8 orgs pass smoke + step10 [4 8 9 11 12]. sarreid + cci golden checksums are **byte-identical** to Track-E freeze (no re-baseline needed — empty cache for Q-R1/R2/R4 produces zero output, template whitespace fixed). Synthetic cache test on `da` confirmed all three legs render correctly and step10 passes with real floor data.

**`da` anointing — COMPLETE (2026-07-09):**
1. ✅ Populated Q-R1/R2/R4 CSVs via Postgres MCP (org_id=62, `orders` table, `created_at` date column). SQL correction applied: canon queries used `portal_orders`/`order_date` — corrected to `orders`/`created_at` in `query_library_v2.md`.
2. ✅ Floor renders substantively: Q-R1 (41 active seats, 26 logins/30d, 8 order authors, 1,225 confirmed orders), Q-R2 (8.4% coverage, 169/2,010 accounts), Q-R4 (100% submission rate). smoke + step10 [4 8 9 11 12] PASS.
3. ✅ `da` anointed as Tier-0/floor gold standard — `golden_set.json` v5 frozen (SHA256 `db91bb0e…`, 46,043 bytes).

**VM-R3 (Mixpanel-gated legs Q-63/64/65):** NOT wired in this pass. Fast-follow item — requires BigQuery cache infrastructure for the rep layer. Does not block `da` anointing (R1/R2/R4 are the always-on floor).

---

## 3. `hfg` / `kal` / `sca` / `ali` golden checksums are now collaterally stale

**What (discovered during Track E, not asked for, flagging anyway):** Track E only
re-baselined Sarreid + cci. But Tracks A/B/C/D's template changes
(`section_01_hero`, `section_02_thisweek`, `section_05_layers`, `section_07_watchlist`,
`section_09_dealers`, `section_10_channels`, `_macros`) are pipeline-wide, not
Sarreid/cci-specific. Live-checked during Track E: `hfg`, `kal`, `sca`, and `ali` all
now render with different bytes/checksums than `config/golden_set.json` v3 recorded,
confirmed via `./regression.sh --verify` (4 FAIL / 2 PASS after the v4 freeze — the 2
passes are Sarreid + cci).

`config/golden_set.json` v4 already carries a `"note"` field on each of these 4 entries
flagging the staleness, so nobody mistakes a regression-suite FAIL on them for a new
bug. Their checksums were **not** touched or re-verified by Track E — that was out of
scope for this task.

**Owner action needed:** a Track-E-style reviewed re-baseline pass for `hfg`/`kal`/
`sca`/`ali` (same rigor: regenerate, diff against last-good, categorize
expected-vs-unexpected, human sign-off) before re-freezing them. Until then,
`./regression.sh` will legitimately show `4 FAIL` and that is expected, not a new
incident.
