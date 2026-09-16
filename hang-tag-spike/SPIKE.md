# Hang tag spike

> **Last updated**: 2026-09-16

Standalone Next.js prototype for web-to-print showroom hang tags.
Not iPad reports. Not EBR-794. Not a new catalog API.

Tracked in **`kylor-johnson/supercat-4.0`** (remote `personal`) as `hang-tag-spike/`.
Not a nested git repo. `node_modules` / `.next` stay gitignored (and `.nosync` on this Mac).

| Mac | Path |
|---|---|
| This Mac (iCloud ops tree) | `SuperCat 4.0/hang-tag-spike` |
| Other Mac | `~/repos/supercat-4.0/hang-tag-spike` |

## Run

This Mac:

```bash
cd "~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/hang-tag-spike"
npm install
npm run dev
```

Other Mac (after `git pull` in `~/repos/supercat-4.0`):

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npm install
npm run dev
```

- Print sheets: http://localhost:3000/ (Avery 5371) and http://localhost:3000/5392
- Designer: http://localhost:3000/design
- PDFs: `public/reviews/kuzco-5371-sheet.pdf`, `kuzco-5392-sheet.pdf`

## What this is

Brent’s Confluence spec: [Web-to-Print Hang Tag Spike Spec](https://supercatsolutions.atlassian.net/wiki/spaces/EOL/pages/1842937857/Web-to-Print+Hang+Tag+Spike+Spec).

The product is a **browser designer** that prints Avery tags. iPad hang tags stay as they are (`IpadReport` shapes + NIBs). This spike must speak SuperCat’s **field names**, not copy the iPad layout engine.

## What exists now

- Avery **5371** letter: 3.5×2 in, 2×5, 0.5" top, 0.75" sides, no gap
- Avery **5392** letter: 4×3 in, 2×3, 0.25" sides, 1" top/bottom (official Avery, not iOS 3-col 3×4)
- 10 live Kuzco (`kll`) SKUs on disk in `src/data/kuzco-fixture.json`
- Real UPC-A (`scripts/render-upcs.mjs` → `public/fixtures/barcodes/`)
- Logo + product photos on disk
- Print CSS hides chrome; Chrome File → Print or Download PDF

Bindings match Kuzco live formats 3198 / 3204:

`collection_name`, `c.FinishOptions`, `c.LampType`, `c.Voltage`, `c.ColorTemperature`, `c.Wattage`, `c.Lumens`, `product_dimensions_in`, `pl.us_imap` (CAD IMAP included even though those live formats omit it), `upc_value`.

## Shift 2026-09-16 (Brent)

Designer + a shareable web app first. Live catalog API key later. Physical Avery print is a check, not the gate.

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

Schema: `src/data/template.ts`. Positions in **inches**. Objects: `text` / `image` / `barcode`. Bindings are IpadReport vocabulary (`item_number`, `c.FinishOptions`, `upc_value`, …), not `populate_hash` keys.

localStorage key: `hang-tag-template-v1`. Download JSON from the designer to share a layout.

## Catalog later

`GET /api/v1/kll/products` — NDJSON, `Products::RenderForApi` in `supercat_server`. Console-issued key, one dedicated OrgUser, `org_shortname` must match. Next route handler proxies (no CORS). Do not invent an API. Do not query Postgres from this app.

## Vercel later

Fixture-only is fine for Brent to click. Live IMAP on a public URL needs auth first.

## Codebase map

| Surface | Where |
|---|---|
| This spike | this repo |
| Catalog API, API keys, `IpadReport` | `~/supercat-code/supercat_server` (read `origin/master`) |
| iPad Avery NIBs | `~/supercat-code/sarreid_ios` |
| Ops notes | SuperCat 4.0 (`WORKSPACE.md`) |

iPad 5392 portrait is 3 columns of 3×4 in — that does **not** fit Avery letter 5392. Web uses official letter stock.

Rails `render_upca` on master still emits Code128B. This spike generates real UPC-A. Do not file that as a Kuzco bug.

## iCloud / machines

**GitHub is how this moves between Macs**, not iCloud. iCloud earlier duplicated
`repos` vs `repos 2` and choked on `node_modules`. This folder used to live under
`repos/hang-tag-spike` (gitignored). It is now a tracked directory of
`kylor-johnson/supercat-4.0`.

On this Mac, `node_modules.nosync` / `.next.nosync` keep install artifacts out of
iCloud. Other Mac: `git pull` then `npm install` — never Download Now on
`node_modules`.

Leave `SuperCat 4.0/repos/` and `repos 2/` alone until the other Mac is cloned
from GitHub; then delete `repos 2` from iCloud. Nested clones inside `repos/`
are not this spike.

## Design system

Copied SuperCat tokens/primitives into `src/design-system/ds`. Do not import `tokens/index.css` or `type.css` (PostCSS `@import` order).
