# UX / Lane 1 — Design Overlay Brief + Wireframe (Bet B)

**Date:** 2026-07-16
**Lane:** 1 (Legible / UX)
**Bet:** B — Design overlay wireframes
**Isolation:** ON — prototype only. No Rails/`supercat_server` edits.
**Visual language:** SuperCat App kit (`.kshell` / `.kc` / `.kdt` / `.kb`), utilitarian + data-dense — not marketing editorial.

## Artifact
- **Wireframe (mockup-only):** [`design-system/app/sales-portal-cycle01-mockup.html`](../../design-system/app/sales-portal-cycle01-mockup.html)
  - Links the real App kit token + primitive CSS (`ds/tokens/index.css`, `card.css`, `button.css`, `table.css`, `tabs.css`) — same stylesheets as `app/dashboard.html`, so it inherits the production kit look, light/dark tokens included.
  - **Answer-first composition:** one hero question per panel, restrained (paper canvas, single crimson accent reserved for the risk moment, gold for the "peak/moment"). Follows the handoff north star: 5-9 elements per view, one accent, one hero metric.

## Grounding (live, masked)
All figures are real aggregates from Postgres, rounded, customer names masked.

- **Sarreid (org 1):** trailing-12mo invoiced topline **$16.03M**, 43,687 invoices, 1,414 active customers. Monthly bars are the true 2025-07 → 2026-06 series. Concentration: top-1 **30.0%** ($4.80M), top-10 **46.3%**; steep cliff to #2 at 3.4%.
- **CCI (org 161):** topline **$71.14M**, 7,790 active customers, top-1 **6.1%**, top-10 **16.8%** (diversified).
- Cross-org strip is included specifically to prove the two heroes read the org's *real shape* (concentrated vs diversified) rather than a template.

## What the wireframe deliberately demonstrates
1. **True Topline** as the invoiced ledger number, with a green provenance chip ("Invoiced net_amount · reconciles to ledger") — makes the metric law visible in the UI (DDD/ACL).
2. **Concentration / single-account risk** as a donut + cumulative table + a crimson risk callout. The crimson is used *only* for the risk moment, consistent with the kit's "no crimson in everyday data viz" rule.
3. **One range drives both heroes** — the context bar shows org + range at the top; this is the SERV-2395 lesson made visible (change the range, every number moves). It is a UX statement, not a code claim.

## Feedback questions to ask customers (rep + owner)
1. When you open the portal, is "invoiced trailing-12-months" the number you actually trust, or do you mentally convert to booked/backlog? Which should be the default hero?
2. Does the single-account-risk framing ("losing Account 01 erases ~$4.8M") match how you think about your book, or do you want it per-rep / per-territory instead of org-wide?
3. Masked accounts vs real names: in your own portal you'd see real names — is the top-N concentration list something you'd screenshot for a QBR, or too sensitive to surface by default?
4. Is a 4-segment donut the right read for concentration, or would a simple "top-1 / top-10 / rest" three-number strip be faster?
5. What's the one follow-up you'd want after seeing these two answers (e.g. "which products drive Account 01", "is Account 01 growing or declining")? That defines Hero follow-ups.
6. Does the App kit look (calm paper + one accent) feel like an upgrade over the classic portal, or too far from what your reps recognize today?

## Draft acceptance criteria — overlay / first Rails slice (flagged, portal-only)
> These are for the eventual Rails slice; nothing is built while isolated. Ship only under `ISOLATION OFF`.
- Given a portal user on the Intelligence surface, the True Topline hero shows `SUM(portal_invoices.net_amount)` for the selected org + range, matching the INSIGHT spec's reconciliation query.
- Given a range change in the context bar, both heroes recompute to that range (no stale/fixed period on the primary answers).
- Concentration hero shows top-1 and top-10 share plus a masked/real cumulative top-5 list; the risk callout appears only when top-1 share exceeds a threshold (proposed: >= 20%).
- Rendered inside a **feature-flagged, portal-only** layout/CSS; catalog stays on classic `layouts/ecat` when the flag is on (respects the layout-coupling constraint from FIX + handoff).
- Uses App kit tokens (no bespoke colors); passes light/dark; no `extra_javascript` CSS hacks.
- Numbers respect territory scoping once SERV-2178/2196 land (do not ship the surface assuming filters are already correct — see cross-lane note).

## Explicit no-gos
- No talk-to-data / NL query / anomaly agent (EBR-772 / Lane 3 — parked).
- No implementation of `enable_phase3_sales_portal` or any Rails view/CSS/flag without an explicit GO.
- No catalog/PDP/checkout/iPad/Admin/global-eOL paint.
- No fake `$4.82M`-style placeholders — every number here traces to a query.
- Not a "Sales Portal 2.0" grab-bag: scope is exactly the two heroes (Topline + Concentration).

## Cross-lane dependency (call out to Orchestrator)
This surface is only trustworthy if territory + date filters are correct. It shares the two heroes with INSIGHT (Lane 2) and depends on FIX (Lane 0) for SERV-2178/2196 (territory truth) and SERV-2395 (range drives totals). Parallel work is fine, but freeze the overlay AC until PROGRAM/Orchestrator confirms the heroes.

## Handoff
Paste to `05-ORCHESTRATOR` for the Review Card (done in `ORCHESTRATOR-review-cards.md`). Treat as internal wireframe until a feedback session runs.
