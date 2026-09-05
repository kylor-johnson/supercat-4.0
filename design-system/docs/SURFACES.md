# Architecture — one brand, two products

The SuperCat Design System is **one brand expressed through two products**. They share every fundamental — color, type, space, radius, motion, voice — but they look and behave differently because they serve different audiences.

```
                ┌─────────────────────────────────────────────┐
                │            SHARED FOUNDATION                │
                │           one brand · one voice             │
                │                                             │
                │   Tokens     primitive · semantic · local   │
                │   Color      paper · ink · crimson · gold   │
                │              clay · cream · moss            │
                │   Type       Geist Sans + Geist Mono        │
                │   Space      4-px ladder · 18 steps         │
                │   Radius     8/14 benchmarks                │
                │   Motion     6 durations · 6 easings        │
                │   Brand      SUPERCAT SOLUTIONS wordmark    │
                │                                             │
                │   ds/tokens/  ·  ds/primitives/  ·  assets/ │
                └────────────────────┬────────────────────────┘
                                     │
              ┌──────────────────────┴──────────────────────┐
              ▼                                             ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │   PRODUCT 1              │              │   PRODUCT 2              │
   │   Web Marketing          │              │   Web / iPad App         │
   │   ─────────────────      │              │   ─────────────────      │
   │   Audience  buyers       │              │   Audience  reps · admin │
   │   Tone      editorial    │              │   Tone      utilitarian  │
   │   Vibe      premium      │              │   Vibe      data-dense   │
   │             restrained   │              │             fast         │
   │             paper        │              │   Layout    floating     │
   │   Layout    12-col       │              │             shell        │
   │             dashed grid  │              │                          │
   │                          │              │                          │
   │   Surfaces:              │              │   Surfaces:              │
   │   • Portal               │              │   • Dashboard            │
   │   • Reference            │              │   • Orders               │
   │                          │              │   • Products             │
   │                          │              │   • Company Settings     │
   │                          │              │                          │
   │   Class prefixes:        │              │   Class prefixes:        │
   │   .ds-* · .vn-* · .mn-*  │              │   .kb · .kf-* · .kc      │
   │                          │              │   .kdt · .knav · .ktab   │
   │                          │              │   .kshell · .kskel · .ki │
   │                          │              │                          │
   │   Lives in:              │              │   Lives in:              │
   │   index.html             │              │   app/dashboard.html     │
   │   ds/reference.html         │              │   app/orders.html        │
   │   nav/                   │              │   app/products.html      │
   │                          │              │   app/settings.html      │
   │                          │              │                          │
   └──────────────────────────┘              └──────────────────────────┘
```

**Both products consume the foundation. Neither product touches the other.**

---

## The contract — fast reference

| | Web Marketing | Web / iPad App |
|---|---|---|
| **Who** | buyers, partners, public | sales reps, admins, ops |
| **Goal** | sell the product · publish editorial · evangelize the brand | run the business · move data quickly |
| **Tone** | confident, premium, restrained | utilitarian, dense, fast |
| **Vibe cues** | wide editorial columns · dashed gridlines · 12-col rhythm · paper background · `.kc:hover` lifts | floating `.kshell` · sticky sidebar · transparent topbar · cards do NOT lift · skeleton-load on data fetches |
| **Class roots** | `.ds-*` (chapter chrome) · `.vn-*` (universal pill nav) · `.mn-*` (manual chrome) | `.k*` kit family — `.kb` button · `.kf-*` forms · `.kc` card · `.kdt` table · `.knav` sidebar · `.ktab` tabs · `.kshell` shell · `.kskel` skeleton · `.ki` icon |
| **Nav** | `.vn` two-pill marketing nav (`nav/marketing-nav.css`) | `.knav` vertical sidebar (`ds/primitives/nav.css`) |
| **Chart palette** | crimson + gold + moss + taupe (editorial) | neutral ink scale + gold for emphasis |
| **Theme toggle** | rare (portal/manual) | always available top-right |

---

## File-by-file map

### Shared foundation

| Path | Belongs to | Role |
|---|---|---|
| `ds/tokens/index.css` | foundation | The canonical entrypoint. Load this first. |
| `ds/tokens/color.css` | foundation | 8 color families · light + dark. |
| `ds/tokens/type.css` | foundation | Family, scale, weight, tracking. |
| `ds/tokens/space.css` | foundation | 4-px ladder · containers · gutters. |
| `ds/tokens/radius.css` | foundation | 8 radii. |
| `ds/tokens/shadow.css` | foundation | 5 elevations + focus + dark overrides. |
| `ds/tokens/motion.css` | foundation | Durations · easings · reduced-motion. |
| `ds/tokens/semantic.css` | foundation | `--text-*`, `--surface-*`, `--action-*`, `--status-*`, `--border-*`. |
| `ds/tokens/design-tokens.json` | foundation | W3C Design Tokens mirror. |
| `ds/primitives/button.css` + `.js` + `.md` | foundation | `.kb` button family. |
| `ds/primitives/input.css` + `.js` | foundation | `.kf-input`. |
| `ds/primitives/check.css` | foundation | `.kf-check` checkbox + radio. |
| `ds/primitives/switch.css` | foundation | `.kf-switch` toggle. |
| `ds/primitives/field.css` | foundation | `.kf-field` label + control + hint wrapper. |
| `ds/primitives/date.css` + `.js` | foundation | `.kf-date` calendar. |
| `ds/primitives/icon.css` | foundation | `.ki` icon wrapper. |
| `ds/primitives/card.css` | foundation | `.kc` card surface (cross-surface). |
| `ds/primitives/table.css` | foundation | `.kdt` data table. |
| `ds/primitives/tabs.css` + `.js` | foundation | `.ktab` tabs. |
| `ds/primitives/nav.css` | foundation | `.knav` App sidebar primitive — only used in App, but its CSS lives in foundation. |
| `ds/primitives/skeleton.css` + `.js` | foundation | `.kskel` content-shape loader. |
| `assets/supercat-mark.svg` | foundation | Brand mark vector. |

### Product 1 — Web Marketing

| Path | Role |
|---|---|
| `index.html` | Portal. Top-level page index. Editorial page-rows with crimson hover arrows. |
| `ds/reference.html` | **Reference** — the complete system on one page. Tokens, primitives, patterns, themes, framework integration. THE single source of truth for the marketing surface. |
| `ds/reference.css` | Manual chrome — hero, app preview cards, foundations, primitives showcase. |
| `nav/marketing-nav.css` + `.js` | Universal `.vn` two-pill marketing nav with hover mega-menus. |

### Product 2 — Web / iPad App

| Path | Role |
|---|---|
| `app/dashboard.html` | Workspace home — metric tiles + chart + best-sellers + activity. Skeleton-loaded. |
| `app/orders.html` | Orders data table — status tabs · filters · sortable headers · pagination. Skeleton-loaded. |
| `app/products.html` | Products card-view grid — 4-up with cover tones + status flags. Skeleton-loaded. |
| `app/settings.html` | Company Settings — horizontal section tabs · panel swap · sticky save bar. |

### Documentation

| Path | Role |
|---|---|
| `docs/SURFACES.md` | This file. Architecture + file map. |
| `docs/FRAMEWORK-GUIDE.md` | React / Vue / Angular / Svelte / Tailwind / LLM integration. |
| `README.md` | Top-level entry point. |
| `../PROGRESS.md` | Session-by-session log of decisions. |

---

## The two-nav distinction (most-asked clarification)

There are **two unrelated nav components** in the system. They live in different folders and serve different products:

| | Web-Marketing universal nav | App sidebar |
|---|---|---|
| File | `nav/marketing-nav.css` + `.js` | `ds/primitives/nav.css` |
| Class root | `.vn-*` | `.knav-*` |
| Direction | horizontal top, two-pill | vertical left rail |
| Used in | `index.html`, `ds/reference.html` | `app/*.html` |
| Behavior | hover mega-menus, dark glass pills | static rail · drawer on mobile · rail-collapsed variant |

If a file links `nav/marketing-nav.css` and renders `<header class="vn">`, it is a Web-Marketing page. If a file links `ds/primitives/nav.css` and renders `<aside class="knav">`, it is an App page.

---

## What was archived in v3.0

Preserved at `_legacy/_backup/2026-05-15-cleanup/`:

- `app/index.html` — old ipad-frame demo. Superseded by the four production-fidelity HTML screens.
- `app/{shell,tokens,ipad-frame,screen-browser,screen-product-review}.jsx` — legacy React-based iPad app. Maintained a parallel JS-object token system; never migrated.
- `content/` — entire TLC editorial validation kit.
- `nav-old/{nav.css,nav.jsx,menus.jsx,site-nav.jsx}` — old React mega-menu marketing nav. Replaced by the universal `.vn` pill nav in v3.0.

The "eCat" brand naming was retired in v3.0. The App is just "the App" or "SuperCat App". Two products: Web Marketing and Web / iPad App.

---

## When in doubt

- Building a customer-facing page (landing, blog, lead magnet)? → **Product 1 · Web Marketing.** Use `ds/reference.html` as a reference. Use `.vn` nav, `.kc` cards (with hover-lift).
- Building an admin / sales / data workspace? → **Product 2 · Web / iPad App.** Use `app/dashboard.html` or `app/orders.html` as a reference. Always inside `<div class="kshell">`. Use `.knav` sidebar, `.kdt` tables, `.kskel` loaders.
- Building a shared component (button, form input, card)? → **Foundation.** Use `.kb` / `.kf-*` / `.kc` primitives directly. They work in both products with no flip.
