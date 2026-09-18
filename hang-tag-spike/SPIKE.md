# Hang tag spike

> **Last updated**: 2026-09-18

Standalone Next.js prototype for web-to-print showroom hang tags.
Not iPad reports. Not EBR-794. Not a new catalog API.

Tracked in **`kylor-johnson/supercat-4.0`** as `hang-tag-spike/`.
Not a nested git repo. `node_modules` / `.next` stay gitignored.

## Status (2026-09-18)

Brent asked for designer + a shareable web app first. That is live. Browser CSV
is now the catalog. Live `GET /api/v1/kll/products` and physical Avery stay later.

| Surface | State |
|---|---|
| Public app | https://kuzco-hang-tags.vercel.app — 10 Kuzco (`kll`) SKUs on disk until a CSV is loaded in that browser |
| 5371 sheet | `/` — `TemplateTag` from JSON · official Avery letter 2×5 |
| 5392 sheet | `/5392` — same · official Avery letter 2×3 (not iOS 3-col 3×4) |
| Hang tag | `/hangtag` — 2×3.5 in portrait, one-up. Screen is photo+hole sizzle; print is the tag |
| Designer | `/design`, `/design?stock=5392`, `/design?stock=hangtag` — canvas left, inspector card (Catalog · Selection · Type · Align · Sheet) right |
| Catalog CSV | Designer upload. Parse + map in the browser. Shared across 5371 / 5392 / hangtag. Clear CSV restores the 10-SKU fixture; column map stays. Sample: `/samples/kuzco-hang-tags.csv` |
| Formats | Registry in `src/data/sheets.ts`. Adding a format is data + a default template |
| Git | `hang-tag-spike/` on `main`. GitHub is how this moves between Macs. |
| Vercel | CLI project `kuzco-hang-tags`. **Not GitHub-linked.** Push does not deploy. |
| Fonts | Template default + per-object face, size (pt), weight, tracking. |
| Align | Text left/center/right. Elements vs tag / selection; distribute at 3+. Snap + arrow nudge. |
| History | ⌘Z / Undo · Redo. 20 JSON states. |
| Fields | Per-object Field (binding or static text) + Show when (always / flag true / flag false) |
| Booleans | `c.MarketSpecial`, `c.QuickShip`, `c.ContainerDiscount`. Additive `showIf` |
| Sheet products | Template `itemNumbers` over the current catalog (CSV or fixture). Avery: short list repeats to fill slots. Hang tag: one per SKU |
| Barcodes | UPC-A / Code 128 / QR generated in-app from the SKU’s UPC digits. No pre-rendered SVG required. |
| Photo preview | Designer toggle. Default on for hang tag. Hole is preview-only — not punched through Avery print |
| Live IMAP / catalog API | Parked. No live prices on the public URL. CSV is not that API. |
| EBR-794 | Parked. Do not comment in Jira. |
| Physical Avery | A check, not the gate. |

`TEMPLATE_VERSION` stays **1**. New fields are additive; missing keys on old
localStorage JSON fall back (SKU → Geist Mono, barcode → UPC-A, text → left,
missing `showIf` → always visible).

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

- Local: http://localhost:3000/ · `/5392` · `/hangtag` · `/design` · `/design?stock=5392` · `/design?stock=hangtag`
- Live: https://kuzco-hang-tags.vercel.app (same paths)
- Static PDF snapshots (stale vs live JSON sheets): `public/reviews/kuzco-5371-sheet.pdf`, `kuzco-5392-sheet.pdf`. Print from the browser, not these files.

Redeploy after a hang-tag change:

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npx vercel deploy --prod --yes
```

## What this is

Brent’s Confluence spec: [Web-to-Print Hang Tag Spike Spec](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1842937857/Web-to-Print+Hang+Tag+Spike+Spec).

The product is a **browser designer** that prints hang tags. iPad hang tags stay as they are (`IpadReport` shapes + NIBs). This spike must speak SuperCat’s **field names**, not copy the iPad layout engine.

## What exists now

- Avery **5371** letter: 3.5×2 in, 2×5, 0.5" top, 0.75" sides, no gap
- Avery **5392** letter: 4×3 in, 2×3, 0.25" sides, 1" top/bottom (official Avery, not iOS 3-col 3×4)
- Portrait **hang tag** 2×3.5 in, one-up (not a letter label grid)
- Designer templates for all stocks (`src/data/template.ts`); print surfaces render `TemplateTag` from that JSON
- Font, size, weight, tracking, text align, element align/distribute, snap, nudge, barcode type, `itemNumbers`, Field, and `showIf` persist on that JSON
- Designer shows a live mini sheet (Avery) or one-up tag beside Fabric; optional photo+hole sizzle; ⌘Z undoes JSON states
- Sheet product picker: unique ordered SKUs, reorder, add/remove. Missing `itemNumbers` uses the full current catalog. Avery: a short list repeats to fill slots. Hang tag: one printed tag per selected SKU
- Default templates include a `QUICK SHIP` text object with `showIf` on `c.QuickShip`. Existing 5371/5392 localStorage will not grow that object until Reset layout — hang tag is a new storage key so it shows immediately
- 10 live Kuzco (`kll`) SKUs on disk in `src/data/kuzco-fixture.json`, with mixed boolean flags. Designer CSV import replaces that list in **this browser** (`hang-tag-catalog-v1`, localStorage or IndexedDB if the file is large). Clear CSV restores the fixture. Column map is `hang-tag-catalog-map-v1`
- Guess `collection_name` from collection headers first; LongDesc / name only if collection isn’t mapped. Booleans: Y / true / 1 / yes. Unmapped flag = false. This is not the eCat iPad `products.csv` importer. Kuzco’s live export has `CollectionCodes` / `price_us_imap` / `upcvalue` / `ImageFileName`, not `c.QuickShip`
- UPC-A, Code 128, and QR generated in-app from the SKU UPC digits (`jsbarcode` / `qrcode`). `scripts/render-upcs.mjs` can still write on-disk SVGs; print does not require them
- Photos: HTTPS URL, `/fixtures/...`, or an eCat `ImageFileName` (first of a comma list). Filenames load from `https://supercatcdn.global.ssl.fastly.net/kll/product_image/full/{file}` — public Fastly, no API key, no Next proxy, no ZIP/FTP. Rows with no image still print (empty photo box)
- If every saved sheet SKU is missing from the imported catalog, the sheet falls back to the first 10 of the new list (so hang tag does not print thousands of pages)
- Print CSS hides chrome; Chrome File → Print. Avery print is a flat letter sheet of labels (no hole). Hang-tag print is the 2×3.5 tag on letter, not the photo sizzle
- Unused leftover: `src/components/hang-tag.tsx` (old hardcoded renderer; sheets no longer import it)

Bindings match Kuzco live formats 3198 / 3204:

`collection_name`, `c.FinishOptions`, `c.LampType`, `c.Voltage`, `c.ColorTemperature`, `c.Wattage`, `c.Lumens`, `product_dimensions_in`, `pl.us_imap` (CAD IMAP included even though those live formats omit it), `upc_value`.

Boolean fixture fields (visibility, not a field-type CMS): `c.MarketSpecial`, `c.QuickShip`, `c.ContainerDiscount`.

## What this is not

| Thing | Why |
|---|---|
| iPad `IpadReport` line slots | Spec: new template model, not renderer rows |
| iPad 5392 3-col 3×4 | Web 5392 is official Avery letter |
| EBR-794 | Rails hang-tag-shapes / server PDF of the **old** shape model. Park it. Do not comment in Jira. |
| New catalog API | Use existing `GET /api/v1/:org_shortname/products` + `X-CLIENT-ID` / `X-API-KEY` when we get there |
| CSV lead magnet | Different product (prospects without SuperCat) |
| SSO | Person login. Catalog key is a dedicated OrgUser. Need SSO only when the app is public with live prices |

## Template JSON (the durable artifact)

Drag/drop must serialize. If layout only lives in React/Fabric state, the spike is throwaway.

Schema: `src/data/template.ts`. Positions in **inches**. Objects: `text` / `image` / `barcode`. Bindings are IpadReport vocabulary (`item_number`, `c.FinishOptions`, `upc_value`, …), not `populate_hash` keys. Template-level `fontFamily` / `barcodeFormat` / `itemNumbers`; per-object `fontFamily`, `textAlign`, `barcodeFormat`, optional `showIf: { binding, equals }`.

Defaults live in git (`KUZCO_5371_TEMPLATE`, `KUZCO_5392_TEMPLATE`, `KUZCO_HANGTAG_TEMPLATE`). Designer edits persist in **that browser only**:

| Key | Stock |
|---|---|
| `hang-tag-template-v1-5371` | 5371 (falls back to legacy `hang-tag-template-v1`) |
| `hang-tag-template-v1-5392` | 5392 |
| `hang-tag-template-v1-hangtag` | 2×3.5 hang tag |

Brent on the public URL sees the git default **templates**, not anyone else’s localStorage. Download JSON from the designer to share a layout. Catalog CSV is also this-browser-only (`hang-tag-catalog-v1`). Do not build a new API for this.

## Catalog

Browser CSV is the catalog until a live key exists. Parser + mapper live in `src/lib/csv.ts` and `src/lib/catalog.ts`. Upload is in the designer; print pages read the same stored list. eCat `ImageFileName` values are not URLs — hang-tag prefixes the first filename with Kuzco’s public Fastly product-image CDN.

`GET /api/v1/kll/products` — NDJSON, `Products::RenderForApi` in `supercat_server`. Console-issued key, one dedicated OrgUser, `org_shortname` must match. Next route handler proxies (no CORS). Do not invent an API. Do not query Postgres from this app.

Live IMAP on a public URL needs auth first.

## Codebase map

| Surface | Where |
|---|---|
| This spike | `hang-tag-spike/` in this repo |
| Format registry | `src/data/sheets.ts` |
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

## Next

1. Decide how templates are shared beyond localStorage (commit JSON into the repo vs download-only).
2. Physical Avery when a sheet is worth hanging.
3. Catalog proxy only after Brent’s console key + a dedicated OrgUser. CSV is the stand-in until then.

## Design system

Copied SuperCat tokens/primitives into `src/design-system/ds`. Do not import `tokens/index.css` or `type.css` (PostCSS `@import` order). Chrome is SuperCat **app**: format switcher, Catalog, designer, Print. Kuzco is catalog data. Type scale tokens needed by `.ktab` / `.kf-check` are copied into `globals.css` `:root` (no Google Fonts `@import`).

### Sensibility critique (2026-09-18)

- **Hierarchy.** Format switcher + Print sit in the topbar; canvas/preview left, one inspector card right. Catalog · Selection · Type · Align · Sheet are labeled groups, not twelve equal tools.
- **One accent.** Crimson is Print (and the Catalog confirm while a CSV map is pending). Weight/align toggles use `.is-pressed` on secondary, not `.kb-primary`. Gold stays on the SVG mark.
- **Anti-slop.** No marketing hero, no hover-lift cards, no typed “SuperCat”, no indigo mesh. Geist via `next/font`, not Inter. Hex stays in token files and in Avery/sizzle/Fabric print internals.
- **Empty is composed.** No selection names Field and Show when. Add-from-catalog is a search box, not 6k chips. Fixture vs “N products from CSV” is the Catalog line.
- **Print.** 5371/5392 remain 8.5×11 letter labels. Hole preview is the checkbox on the canvas, default-on for hang tag only, and it does not punch Avery.

