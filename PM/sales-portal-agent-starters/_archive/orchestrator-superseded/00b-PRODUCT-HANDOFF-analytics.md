# Handoff prompt — Sales Portal → 2030 analytics (paste into a fresh agent chat)

Copy everything below the line into a new Cursor chat. Attach any live client exports / screenshots the user provides.

---

# Sales Portal → analytics platform — session handoff

## Who you are continuing for
Kylor (product). Little appetite for “pretty empty shells.” He has strong taste (“a ton of dopeness”) and will supply live client material. He wants mockups / product direction that feel **real and dense**, grounded in what Sales Portal actually has in production — not another Phase 3 card grid with fake `$4.82M` labels.

**Do not implement `supercat_server` code unless he explicitly says GO.** This thread is product/design + data understanding. A prior CTO brief exists for a Phase 3 chrome-only rebuild; the conversation has **moved past** “just reskin portal” toward whether / how to become a modern analytics surface.

## Why the last mockups felt elementary
Two reasons — fix both:

1. **No live data density.** Comps used placeholder metrics and 5 fake rows. Real portal orgs have tens/hundreds of thousands of orders/invoices, real territories, real concentration, real date grains. Without querying that, everything looks like a template.
2. **Wrong fidelity target.** v1 accidentally reused Phase 3 (paper/crimson/Geist floating shell). v2 differentiated product *languages* (Mercury / Omni grid / Hex / Linear / Evidence) but stayed skeletal. Next pass must be **data-faithful + high-craft**, not another style sampler.

If something looks elementary, assume you need more live query + tighter visual craft — not another abstract destination essay.

## What already exists (read these first)

| Artifact | Path |
|---|---|
| Phase 3 CTO brief (chrome-only program; flag + layout isolation) | `~/Downloads/sales-portal-phase3-cto-brief-2026-07-15.md` |
| CTO pack zip | `~/Downloads/sales-portal-phase3-cto-pack-2026-07-15.zip` |
| Destination mockups v2 (A/B/C × 3 examples; visually distinct) | `~/Downloads/sales-portal-destination-mockups-2026-07-16.html` |
| Same mockup in design-system | `SuperCat 4.0/design-system/app/sales-portal-destination-mockups.html` |
| Original Phase 3 comparison mockup | `SuperCat 4.0/design-system/app/sales-portal-phases-mockup.html` |
| Design tokens / shell reference | `SuperCat 4.0/design-system/ds/tokens/`, `.../app/dashboard.html` |
| Code lives here (do not change yet) | `supercat-code/supercat_server` |

## Destination options (still open — user has not locked A/B/C)

- **A — Inside eCat Online:** calmer / Omni-ish / answer-first portal, still under Sales Portal routes; catalog/checkout stay classic.
- **B — Separate analytics app:** different URL/product (Linear/Hex/Omni-class); eOL is a link out.
- **C — Phased:** ship Phase 3 chrome now → answer-first bridge → platform later only if signals prove value.

Through-line from prior strategy chat (keep this):

> Best 2026 analytics UIs = warehouse-native / semantic metrics underneath + answer-first on top + restrained UI (5–9 elements per view, one accent, one hero metric). Visual polish is downstream of metric discipline. Phase 3 chrome ≠ Omni-class product.

Reference set worth studying (products + componentry): Omni, Hex, Evidence, ThoughtSpot; Mercury/Ramp/Brex + Stripe for calm density; Tremor / shadcn / Recharts/visx/Nivo for agent-implementable UI — not Tableau aesthetics.

## Live data access (required — use it)

### Postgres MCP
- Server: `user-supercat-postgres-vpn` (read-only `execute_sql`)
- Skill templates: `SuperCat 4.0/.cursor/skills/ecat-postgres-audit/SKILL.md`
- Always resolve org by shortname first.

### Confirmed live Sales Portal orgs (already peeked 2026-07-16)

| shortname | name | org id | portal enabled | portal_orders | portal_invoices |
|---|---|---|---|---|---|
| `sarreid` | Sarreid, Ltd. | 1 | yes | ~45k | ~44k |
| `cci` | Currey & Company | 161 | yes | ~157k | ~171k |

User may name more shortnames. Query them the same way.

### What to learn from Postgres (do this before redesigning)
Scope tightly — **understand shape**, don’t dump PII into mockups.

1. Org + mobile site portal flags (`enable_sales_portal`, any Phase-3-like flags if present).
2. Portal table inventory relevant to dashboard/reporting (`portal_orders`, `portal_invoices`, related item tables, territories, etc. — confirm names via `list_objects` / `get_object_details`).
3. Date range coverage (min/max order/invoice dates).
4. Grain & dimensions actually available (territory, customer/bill-to, rep, tradename/collection if present, status).
5. Approximate dashboard math the product already exposes (backlog vs invoiced concepts — match Rails portal dataflows if needed under `supercat_server`).
6. Concentration / top-N reality (e.g. top customers share of backlog) — use **rounded/aggregated** figures in mockups; mask customer names unless user says real names are OK for internal comps.
7. What the current portal UI can vs can’t answer (list/show/filter vs semantic explore vs answer-first).

### User-supplied live client data
User will attach exports, screenshots, or notes. Treat those as ground truth for **what reps see** alongside Postgres for **what’s in the warehouse/DB**. Prefer Postgres for counts/coverage; prefer attachments for UX truth.

## Sales Portal product reality (code map — don’t rediscover from zero)

Sales Portal ≠ catalog. Same eOL URL space (`/:org/e/:site`), shared `layouts/ecat` today.

**In scope surfaces:** Dashboard (`ecat_dashboard` / `/portal`), Orders, Invoices, Customers, Reports, portal nav; RMA adjacent.

**Out of scope for this product bet:** catalog/PDP, checkout/payments, enrollment restyle, Admin Console, iPad theme, global eOL theme paint.

**Access gates (existing):** `mobile_site.enable_sales_portal`, user-type flags, `allow_view_sales_portal?`, dataflow `should_show_portal`.

**Architecture constraint if anyone later builds:** feature-flagged portal-only layout/CSS; catalog must stay classic when flag on. Prefer MobileSite JSON FLAGS (no migration) unless asked. No `extra_javascript` CSS hacks. Ask before DB migrations.

Prior Phase 3 implementation plan (only if they return to chrome-only ship): flag `enable_phase3_sales_portal` → `layouts/ecat_portal` → `application-ecat-portal` → Dashboard first → PO review → Orders → Invoices → Customers → Reports.

## Your job in the new session

1. **Ingest** whatever live client data the user pastes/attaches.
2. **Query Postgres** for `sarreid`, `cci`, and any other shortnames they name — map what Sales Portal data actually supports.
3. **Tell them plainly** what the current portal is good/bad at (in their language).
4. **Produce next-fidelity mockups** (HTML fine) that:
   - Use realistic structure from live aggregates (masked as needed)
   - Feel expensive and calm OR deliberately Omni/Hex/Linear — not generic AI dashboard
   - Make A vs B vs C *obviously* different in information architecture, not just CSS theme
   - Avoid another pass that “looks like Phase 3 with new labels”
5. **Recommend a destination** (A/B/C or hybrid) with a crisp “why,” grounded in data + use cases — not vibes alone.
6. Optionally refresh the CTO brief if direction locks.

## Working rules
- Frozen Insightful Product folders: do not touch unless explicitly asked.
- No canvases unless asked (`no-canvas` rule).
- No push/deploy. No secrets in artifacts (.env, creds, raw PII dumps).
- When showing customer-level examples in mockups: prefer pseudonyms unless user OKs real names for internal-only comps.
- Prefer small, reviewable HTML mockups in `~/Downloads` and/or `design-system/app/`.
- After queries: summarize in plain language before dumping SQL.

## Opening move (do this first in the new chat)
1. Confirm shortnames to use (default `sarreid` + `cci` + anything user attaches).
2. Run a short Postgres “shape” pass (org resolve, portal counts, date span, dimension columns) — no full Insightful-style analysis.
3. Ask what artifact they want next: denser mockups, destination recommendation, or CTO brief v2.
4. Only then design.

## One-line north star for the next agent
Make the next artifact feel like it was designed **on top of Sarreid/CCI reality**, with SuperCat-level craft — not like a Tremor demo theme pack.

---

*Handoff written 2026-07-16. Prior chat: Phase 3 CTO pack → destination strategy → mockup v1 (too same) → mockup v2 (distinct languages, still elementary) → Postgres connectivity confirmed for sarreid/cci.*
