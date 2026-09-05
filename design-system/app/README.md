# Web / iPad App — Product 2 of 2

This folder holds **Product 2** of the SuperCat Design System: the **Web / iPad App** surface.

→ See [`../docs/SURFACES.md`](../docs/SURFACES.md) for the full architecture (one foundation, two products).
→ See [`../docs/FRAMEWORK-GUIDE.md`](../docs/FRAMEWORK-GUIDE.md) for React/Vue/Angular/Svelte/Tailwind integration.
→ See [`../README.md`](../README.md) for the top-level entry point.

---

## What lives here

| File | Role |
|---|---|
| `sales-portal-skin-mockup.html` | Before/after mockup of eCat Sales Portal with DS tokens on existing chrome (Phase 1). Toggle Legacy ↔ Proposed. |
| `dashboard.html` | Workspace home — metric tiles + chart + best-sellers + activity. Skeleton-loaded with a Refresh control. |
| `orders.html` | Orders data table — status tabs · search · filters · sortable headers · status pills · pagination. Skeleton-loaded. |
| `products.html` | Products card-view grid — 4-up with rotating cover tones, vendor + SKU eyebrow, status pill + tabular-num price, New/Low corner flags. Skeleton-loaded. |
| `settings.html` | Company Settings — horizontal `.ktab` section nav with panel swap. Profile, branding, address, defaults, notifications, API tokens, danger zone. Sticky save bar. |

---

## The App contract

| Aspect | Rule |
|---|---|
| **Layout root** | `<div class="kshell">` — floating shell with sticky `.knav-floating` sidebar + transparent `.kshell-top` topbar + `.kshell-content` main. |
| **Sidebar** | `<aside class="knav knav-floating">` — vertical nav, full SUPERCAT SOLUTIONS wordmark at top, nav items grouped by section + a sticky account footer. Distinct from `nav/marketing-nav.css` — that's the Web Marketing nav. |
| **Cards** | `.kc` cards do **not** hover-lift inside `.kshell`. Workspace surfaces stay quiet. |
| **Tables** | `.kdt` — sortable, status-pilled, responsive. First and last cells (`.kdt-check` / `.kdt-actions`) get safe shoulder padding on tight screens. |
| **Loading** | Use `.kskel` skeleton primitive with `[data-loadable] [aria-busy]` swap. Wire `aria-busy` to React loading state / Vue refs / Angular signals / Svelte stores. |
| **Theme** | Always-available toggle in the topbar. `<html data-theme="dark">` flips color, shadow, and a few crimson tokens. |
| **Chart palette** | Use neutral ink scale for default bars. Gold for emphasis (peak day, current period). **Never crimson in charts.** Crimson is reserved for primary action + danger pills. |

---

## Build a new App page in 5 steps

1. Copy `orders.html` as a starting template.
2. Replace the `<title>` and breadcrumb.
3. Update the sidebar `aria-current="page"` to point at the right item.
4. Replace the page-head + main content with your own.
5. Wrap data regions with `<div data-loadable aria-busy="true" data-load="1000">…</div>` so they show the skeleton primitive during fetch.

---

## What was archived

The legacy iPad React app (`shell.jsx`, `tokens.jsx`, `ipad-frame.jsx`, `screen-browser.jsx`, `screen-product-review.jsx`) and the old `index.html` ipad-frame demo were retired in v3.0. They maintained a parallel JS-object token system that never reached the cascade. Preserved at `../../_legacy/_backup/2026-05-15-cleanup/app/` if needed.
