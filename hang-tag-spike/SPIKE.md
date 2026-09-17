# Hang tag spike

> **Last updated**: 2026-09-17

Standalone Next.js prototype for web-to-print showroom hang tags.
Not iPad reports. Not EBR-794. Not a new catalog API.

Tracked in **`kylor-johnson/supercat-4.0`** as `hang-tag-spike/`.
Not a nested git repo. `node_modules` / `.next` stay gitignored.

## Status (2026-09-17)

Brent asked for designer + a shareable web app first. That is live. Catalog key
and physical Avery are later.

| Surface | State |
|---|---|
| Public app | https://kuzco-hang-tags.vercel.app — fixture-only, 10 Kuzco (`kll`) SKUs on disk |
| 5371 sheet | `/` — `TemplateTag` from JSON |
| 5392 sheet | `/5392` — same |
| Designer | `/design` (5371) and `/design?stock=5392` — Edit canvas + mini Avery sheet |
| Git | `hang-tag-spike/` on `main`. GitHub is how this moves between Macs. |
| Vercel | CLI project `kuzco-hang-tags`. **Not GitHub-linked.** Push does not deploy. |
| Fonts | Template default + per-object face, size (pt), weight, tracking. |
| Align | Text left/center/right. Elements vs tag / selection; distribute at 3+. Snap + arrow nudge. |
| History | ⌘Z / Undo · Redo. 20 JSON states. |
| Sheet products | Template `itemNumbers`. Ordered unique SKUs; a short list repeats to fill 10 / 6 slots. |
| Barcodes | UPC-A default. Code 128 and QR in-app from the SKU’s UPC digits. |
| Catalog / live IMAP | Parked. No live prices on the public URL. |
| EBR-794 | Parked. Do not comment in Jira. |
| Physical Avery | A check, not the gate. |

`TEMPLATE_VERSION` stays **1**. New fields are additive; missing keys on old
localStorage JSON fall back (SKU → Geist Mono, barcode → UPC-A, text → left).

## Run

Both Macs — same clone:

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npm install
npm run dev
```

| Workspace | File |
|---|---|
| Mac mini | `SuperCat.code-workspace` |
| MacBook | `SuperCat.macbook.code-workspace` |

- Local: http://localhost:3000/ · `/5392` · `/design` · `/design?stock=5392`
- Live: https://kuzco-hang-tags.vercel.app (same paths)
- Static PDF snapshots (stale vs live JSON sheets): `public/reviews/kuzco-5371-sheet.pdf`, `kuzco-5392-sheet.pdf`. Print from the browser, not these files.

Redeploy after a hang-tag change:

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npx vercel deploy --prod
```

## What this is

Brent’s Confluence spec: [Web-to-Print Hang Tag Spike Spec](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1842937857/Web-to-Print+Hang+Tag+Spike+Spec).

The product is a **browser designer** that prints Avery tags. iPad hang tags stay as they are (`IpadReport` shapes + NIBs). This spike must speak SuperCat’s **field names**, not copy the iPad layout engine.

## What exists now

- Avery **5371** letter: 3.5×2 in, 2×5, 0.5" top, 0.75" sides, no gap
- Avery **5392** letter: 4×3 in, 2×3, 0.25" sides, 1" top/bottom (official Avery, not iOS 3-col 3×4)
- Designer templates for **both** stocks (`src/data/template.ts`); print sheets render `TemplateTag` from that JSON
- Font, size, weight, tracking, text align, element align/distribute, snap, nudge, barcode type, and `itemNumbers` persist on that JSON
- Designer shows a live mini Avery sheet beside Fabric (same SKUs and layout as `/` or `/5392` in this browser); ⌘Z undoes JSON states
- Sheet product picker: unique ordered SKUs, reorder, add/remove. Missing `itemNumbers` uses the full fixture list. A short list repeats to fill the Avery slots.
- 10 live Kuzco (`kll`) SKUs on disk in `src/data/kuzco-fixture.json`
- Real UPC-A (`scripts/render-upcs.mjs` → `public/fixtures/barcodes/`); Code 128 and QR generated in-app from the SKU UPC digits
- Logo + product photos on disk
- Print CSS hides chrome; Chrome File → Print
- Unused leftover: `src/components/hang-tag.tsx` (old hardcoded renderer; sheets no longer import it)

Bindings match Kuzco live formats 3198 / 3204:

`collection_name`, `c.FinishOptions`, `c.LampType`, `c.Voltage`, `c.ColorTemperature`, `c.Wattage`, `c.Lumens`, `product_dimensions_in`, `pl.us_imap` (CAD IMAP included even though those live formats omit it), `upc_value`.

## What this is not

| Thing | Why |
|---|---|
| iPad `IpadReport` line slots | Spec: new template model, not renderer rows |
| EBR-794 | Rails hang-tag-shapes / server PDF of the **old** shape model. Park it. Do not comment in Jira. |
| New catalog API | Use existing `GET /api/v1/:org_shortname/products` + `X-CLIENT-ID` / `X-API-KEY` when we get there |
| CSV lead magnet | Different product (prospects without SuperCat) |
| SSO | Person login. Catalog key is a dedicated OrgUser. Need SSO only when the app is public with live prices |

## Template JSON (the durable artifact)

Drag/drop must serialize. If layout only lives in React/Fabric state, the spike is throwaway.

Schema: `src/data/template.ts`. Positions in **inches**. Objects: `text` / `image` / `barcode`. Bindings are IpadReport vocabulary (`item_number`, `c.FinishOptions`, `upc_value`, …), not `populate_hash` keys. Template-level `fontFamily` / `barcodeFormat` / `itemNumbers`; per-object `fontFamily`, `textAlign`, `barcodeFormat`.

Defaults live in git (`KUZCO_5371_TEMPLATE`, `KUZCO_5392_TEMPLATE`). Designer edits persist in **that browser only**:

| Key | Stock |
|---|---|
| `hang-tag-template-v1-5371` | 5371 (falls back to legacy `hang-tag-template-v1`) |
| `hang-tag-template-v1-5392` | 5392 |

Brent on the public URL sees the git defaults, not anyone else’s localStorage. Download JSON from the designer to share a layout. Do not build a new API for this.

## Catalog later

`GET /api/v1/kll/products` — NDJSON, `Products::RenderForApi` in `supercat_server`. Console-issued key, one dedicated OrgUser, `org_shortname` must match. Next route handler proxies (no CORS). Do not invent an API. Do not query Postgres from this app.

Live IMAP on a public URL needs auth first.

## Codebase map

| Surface | Where |
|---|---|
| This spike | `hang-tag-spike/` in this repo |
| Catalog API, API keys, `IpadReport` | `~/supercat-code/supercat_server` (read `origin/master`) |
| iPad Avery NIBs | `~/supercat-code/sarreid_ios` |
| Ops notes | `WORKSPACE.md` |

iPad 5392 portrait is 3 columns of 3×4 in — that does **not** fit Avery letter 5392. Web uses official letter stock.

Rails `render_upca` on master still emits Code128B. This spike generates real UPC-A. Do not file that as a Kuzco bug.

## Machines

**GitHub is how this moves between Macs**, not iCloud.

Both Macs edit `~/repos/supercat-4.0`. Pull, work, commit, push, other Mac pulls.

**iCloud `SuperCat 4.0` is an unread trap.** It still contains a stale git clone and a copy of `hang-tag-spike/` (including `node_modules`). Do not open it, do not commit from it, do not `npm install` there.

Do not push this repo to `agentic_operations`. Do not commit `node_modules`.

## Next (do not start catalog)

1. Decide how templates are shared beyond localStorage (commit JSON into the repo vs download-only).
2. Physical Avery when a sheet is worth hanging.
3. Catalog proxy only after Brent’s console key + a dedicated OrgUser.

## Design system

Copied SuperCat tokens/primitives into `src/design-system/ds`. Do not import `tokens/index.css` or `type.css` (PostCSS `@import` order).
