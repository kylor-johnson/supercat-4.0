# SuperCat Design System — v3.0

**One brand. Two products. One foundation.**

```
                ┌─────────────────────────────────────────────┐
                │            SHARED FOUNDATION                │
                │           one brand · one voice             │
                │                                             │
                │   Tokens (color · type · space · radius ·   │
                │           motion · semantic · component)    │
                │   Primitives (.kb · .kf-* · .kc · .kdt ·    │
                │               .ktab · .ki · .kskel · .knav) │
                │   Brand assets                              │
                └────────────────────┬────────────────────────┘
                                     │
              ┌──────────────────────┴──────────────────────┐
              ▼                                             ▼
   ┌──────────────────────────┐              ┌──────────────────────────┐
   │  PRODUCT 1               │              │  PRODUCT 2               │
   │  Web Marketing           │              │  Web / iPad App          │
   │                          │              │                          │
   │  editorial · premium ·   │              │  utilitarian · dense ·   │
   │  restrained · paper      │              │  fast · floating shell   │
   │                          │              │                          │
   │  Portal · Reference      │              │  Dashboard · Orders ·    │
   │                          │              │  Products · Settings     │
   └──────────────────────────┘              └──────────────────────────┘
```

The two products **share every fundamental** — color, type, space, radius, motion, voice. They look and behave differently because they serve different audiences.

→ See [`docs/SURFACES.md`](docs/SURFACES.md) for the full architecture + file-by-file map.
→ See [`docs/FRAMEWORK-GUIDE.md`](docs/FRAMEWORK-GUIDE.md) for React / Vue / Angular / Svelte / Tailwind / LLM integration.

---

## Open this first

`index.html` is the portal. It's grouped exactly the way this README is — **Web Marketing** on top, **Web / iPad App** below, **Documentation** at the bottom.

---

## The contract — fast reference

| | Web Marketing | Web / iPad App |
|---|---|---|
| Audience | buyers, partners, public | sales reps, admins, ops |
| Tone | editorial — confident, premium, restrained | utilitarian — data-dense, fast |
| Layout | 12-col, dashed gridlines, paper background | floating `.kshell` + sticky `.knav` sidebar |
| Class roots | `.ds-*` · `.vn-*` (nav) · `.mn-*` (manual chrome) | `.k*` kit family — see below |
| Nav | `.vn` two-pill marketing nav (`nav/marketing-nav.css`) | `.knav` vertical sidebar (`ds/primitives/nav.css`) |
| Hover-lift on cards | yes | no |
| Theme toggle | rare | always available top-right |
| Files | `index.html` · `ds/reference.html` · `ds/sections/*` · `nav/*` | `app/*.html` |

**Shared foundation** (consumed by both products): all `ds/tokens/`, all `ds/primitives/`, all `assets/`.

### Class-prefix legend (instant LLM contract)

| Prefix | Where | Means |
|---|---|---|
| `--color-*`, `--text-*`, `--surface-*`, `--space-*`, `--radius-*`, `--shadow-*`, `--duration-*`, `--ease-*` | foundation | Tokens. Components consume these. |
| `.kb` | foundation | Kit Button. `.kb.kb-md.kb-primary` etc. |
| `.kf-*` | foundation | Kit Form: `.kf-input`, `.kf-check`, `.kf-switch`, `.kf-field`, `.kf-date`. |
| `.ki` | foundation | Kit Icon wrapper. |
| `.kc` | foundation | Kit Card (cross-product — App suppresses hover-lift). |
| `.kdt` | foundation, App-leaning | Kit Data Table. Used primarily in App. |
| `.ktab` | foundation | Kit Tabs (underline · pill · segmented · vertical). |
| `.knav` | foundation, App-only | Kit Nav — vertical App sidebar. Distinct from `nav/marketing-nav.css`. |
| `.kshell` | App | Floating App shell layout (sidebar + topbar + content). |
| `.kskel` | App | Kit Skeleton loader. Content-shape placeholder. |
| `.vn-*` | Web Marketing | Marketing Nav — the universal two-pill nav with mega menus. |
| `.ds-*` | Web Marketing | Section showcase chrome (chapter heads, dashed gridlines, anatomy stages). |
| `.mn-*` | Web Marketing | Manual chrome (hero, app preview cards, section heads inside `reference.html`). |

---

## Source tree (post-v3 cleanup)

```
design-system/
├── README.md                    ·  This file — start here
├── index.html                   ·  Portal · groups by surface family
│
├── ds/                          ·  CANONICAL DESIGN SYSTEM SOURCE
│   ├── reference.html              ·    Reference — the complete system on one page (Marketing)
│   ├── reference.css               ·    Manual chrome
│   ├── tokens.css               ·    Legacy entrypoint — back-compat shim
│   │
│   ├── tokens/                  ·  ★ SHARED FOUNDATION — TOKENS
│   │   ├── index.css                primitives → semantic → aliases
│   │   ├── color.css                8 color families · light + dark
│   │   ├── type.css                 family · scale · weight · tracking
│   │   ├── space.css                4-px scale · containers · gutter
│   │   ├── radius.css               corner radii
│   │   ├── shadow.css               elevation + focus + dark overrides
│   │   ├── motion.css               duration + easing + reduced-motion
│   │   ├── semantic.css             --text-* · --surface-* · --action-* · --status-*
│   │   └── design-tokens.json       W3C Design Tokens mirror
│   │
│   ├── primitives/              ·  ★ SHARED FOUNDATION — PRIMITIVES
│   │   ├── button.{css,js,md}       .kb
│   │   ├── input.{css,js}           .kf-input
│   │   ├── check.css                .kf-check
│   │   ├── switch.css               .kf-switch
│   │   ├── field.css                .kf-field
│   │   ├── date.{css,js}            .kf-date
│   │   ├── icon.{css,md}            .ki
│   │   ├── card.{css,md}            .kc
│   │   ├── table.{css,md}           .kdt
│   │   ├── tabs.{css,js,md}         .ktab
│   │   ├── nav.{css,md}             .knav (App sidebar)
│   │   └── skeleton.{css,js}        .kskel (loader)
│   │
│
├── app/                         ·  PRODUCT 2 · WEB / iPad APP
│   ├── README.md                ·    Per-folder guide
│   ├── dashboard.html           ·    Workspace home (skeleton-loaded)
│   ├── orders.html              ·    Orders data table (skeleton-loaded)
│   ├── products.html            ·    Products card grid (skeleton-loaded)
│   └── settings.html            ·    Company Settings (horizontal tabs + save bar)
│
├── nav/                         ·  PRODUCT 1 · MARKETING NAV
│   ├── marketing-nav.css            .vn two-pill nav (universal across marketing pages)
│   └── marketing-nav.js             hover mega menus + theme toggle
│
├── docs/                        ·  REFERENCE DOCS
│   ├── SURFACES.md                  Architecture + file-by-file map
│   └── FRAMEWORK-GUIDE.md           React/Vue/Angular/Svelte/Tailwind + LLM contract
│
└── assets/                      ·  SHARED FOUNDATION — BRAND ASSETS
```

Archived in `_legacy/_backup/2026-05-15-cleanup/`: old React-based marketing nav (`nav-old/`), legacy iPad React app (`app/`), TLC editorial kit (`content-dir/`), old `app/index.html` ipad-frame demo.

---

## Token contract

Three tiers, in increasing specificity:

1. **Primitive** — raw scales. `--color-ink-3`, `--color-cream`, `--color-moss`, `--space-8`, `--text-lg`.
2. **Semantic** — meaning. `--text-primary`, `--surface-card`, `--action-primary`, `--status-success`, `--border-default`. **Components consume these.**
3. **Component-local** — per-instance knobs. `--kb-bg`, `--knav-w`, `--ktab-h`, `--vn-radius`. Override on a single element to re-skin.

Legacy `--k-*` aliases remain for back-compat in section CSS. Use the primitive names directly in new code.

---

## Conventions

- **Color.** Paper-warm cream surfaces, ink text, crimson sparingly for primary action + danger, gold + clay as brand-flippable support, moss for editorial OK-tags. Light + dark mode.
- **Type.** Geist Sans + Geist Mono. Numbers always mono with tabular numerals.
- **Edges.** 1px hairline `--border-default`. Dashed gridlines for indices and metadata strips.
- **Radius.** 8/14 are the benchmarks. Cards, buttons, inputs share the family.
- **Dark theme.** Opt-in via `<html data-theme="dark">`. Color, shadow, and a few crimson tokens override; everything else stays.
- **Two-product split.** Always. Web Marketing pages live at the root + `ds/` + `nav/`. App pages live at `app/`. Foundation lives at `ds/tokens/` + `ds/primitives/` + `assets/`. The split is the system.

---

## ★ Logo — never type "SuperCat" as text

The brand is a **vector**. Never render the logo as styled HTML text (`<h1>SuperCat</h1>`, `<span class="logo">SuperCat</span>`, etc.). Always use the SVG mark.

**Where the vector lives:**
- Standalone asset: [`assets/supercat-mark.svg`](assets/supercat-mark.svg) — 41×28 viewBox, double-wave glyph, paths fill via `currentColor`
- Inline symbol on every page: `<symbol id="i-mark" viewBox="0 0 41 28">…</symbol>` — referenced via `<svg viewBox="0 0 41 28"><use href="#i-mark"/></svg>`

**Canonical inline usage** (copy-paste anywhere):

```html
<!-- Defs (once per page, inside an invisible <svg>) -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="i-mark" viewBox="0 0 41 28">
      <path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="currentColor"/>
      <path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="currentColor"/>
    </symbol>
  </defs>
</svg>

<!-- Usage — anywhere, any size, recolor via the `color` CSS property -->
<a href="/" class="brand-mark" style="color: var(--color-gold)">
  <svg viewBox="0 0 41 28" width="41" height="28" aria-label="SuperCat"><use href="#i-mark"/></svg>
</a>
```

**Coloring rules:**
- Mark fills via `currentColor`, so just set `color` on the parent.
- Default brand: `color: var(--color-gold)`.
- On dark glass / inverted contexts: `color: var(--color-cream)`.
- Never crimson (that's the primary-action accent, not the brand mark).

**LLM/agent rule:** If you are generating HTML/JSX/Vue for a SuperCat surface and need a logo, always emit the SVG block above — never substitute a text node, even temporarily. The asset path `assets/supercat-mark.svg` is the source of truth.

---

## ★ Demo content vs. real implementation — READ THIS FIRST

**Everything shipped in this folder is DEMO content + the editorial visual system.** The dashboard data, the  MaxROI · 90-Day payback copy, the orders rows, the mega-menu items in `<sc-marketing-nav>` — **all of it is placeholder content showing the style, layout patterns, and primitive vocabulary**. It is **NOT** the canonical content for any real page you build.

**Keep when shipping real pages:**
- Editorial energy — paper-warm cream, ink type, generous whitespace, hairline borders, mono numbers, crimson-for-primary-action.
- The primitive vocabulary — `.kb`, `.kc`, `.kf-*`, `.kfoot-*`, eyebrow strip pattern, hero composition, stat strip rhythm.
- Hard rules — logo as SVG, no custom colors, no primitive base-style overrides, color roles intact.

**Adapt to your real use:**
- **Section count + order** — based on what your page actually needs to communicate.
- **Nav contents in `<sc-marketing-nav>`** — DO NOT import our portal/dashboard/orders/settings demo links into a real product surface. Override the mega-panel data, point to your own routes, or hide the nav and use plain links.
- **Copy + content** — write for the real audience, real offer, real conversion goal. Don't reuse our placeholder copy verbatim ("Pay back your SuperCat investment in under 90 days" is OUR demo line; your page needs its own).
- **Layout structures** — a real page may need 5 sections or 12; copy the editorial vocabulary, not the section count from `maxroi.html`.

**Mental model:** this system is to your page what a typeface family is to a book. The typeface defines how it feels; the manuscript defines what it says. Ship your manuscript with our typeface — don't ship our manuscript.

**LLM-prompt instruction (mandatory line for any AI build):**
> *"This design system is a foundation + guide, not a content template. Adapt structure and copy to my real audience and conversion goal; keep only the visual vocabulary (tokens, primitives, editorial patterns). Do not reuse demo nav items, demo data, or demo section copy."*

Without that line, AI tools tend to copy our demo content one-to-one, which is what just happened to the previous build.

---

## How to use this system in your project

Two paths, depending on environment complexity.

### Path A — Inside the SuperCat app (or any complex framework environment)

For a real product app — React/Vue/Next/Svelte/etc with a build step, multiple routes, state management:

1. **Drop the foundation into your project.** Copy `ds/tokens/`, `ds/primitives/`, and `assets/` into your project (or alias them via a path import).
2. **Load tokens once at app root.** `import 'supercat-ds/ds/tokens/index.css'` in your entry file. Tokens are CSS custom properties — they cascade.
3. **Load primitives à la carte.** Only import the primitives you use (`button.css`, `card.css`, `table.css`, …). Each is independent.
4. **Use real HTML elements + class names.** `<button class="kb kb-md kb-primary">` works in any framework. No wrapper components required.
5. **Wire the few JS primitives.** `input.js`, `tabs.js`, `skeleton.js`, `date.js`, `modal.js` are vanilla controllers — load with `defer` or call once at mount.
6. **Theme via `<html data-theme="dark">`.** Toggle by writing the attribute; every primitive responds via the semantic-token bridge.

See [`docs/FRAMEWORK-GUIDE.md`](docs/FRAMEWORK-GUIDE.md) for React, Vue, Angular, Svelte, and Tailwind snippets.

### Path B — Landing pages (Lovable, v0, plain HTML, etc.)

For a marketing page, demo, or rapid-prototype tool that generates static HTML:

1. **Link the bundle from the root of the design system.**
   ```html
   <link rel="stylesheet" href="ds/tokens/index.css"/>
   <link rel="stylesheet" href="nav/marketing-nav.css"/>
   <link rel="stylesheet" href="ds/primitives/button.css"/>
   <link rel="stylesheet" href="ds/primitives/card.css"/>
   <link rel="stylesheet" href="ds/primitives/footer.css"/>
   <script src="nav/marketing-nav.js" defer></script>
   ```
2. **Use the universal marketing nav — two modes, same dark glass pill.**
   - Mega menus (cross-site): `<sc-marketing-nav current="portal"></sc-marketing-nav>`
   - On-page section anchors (product/lead-magnet pages): `<sc-marketing-nav sections='[{"label":"Calculator","href":"#calculator"},…]' cta-href="#calculator" cta-label="Run mine"></sc-marketing-nav>`
3. **Inline the logo symbol once** (see the logo block above) — every `<sc-marketing-nav>` and `<kfoot>` will pick it up.
4. **Model new sections on [`marketing/maxroi.html`](marketing/maxroi.html).** Editorial hero with payback viz, calculator with `.kc-pick` radio cards + `.ktab-seg` scenario toggle, driver-card grid, math transparency, cost-of-waiting moment, intent-aware lead modal (`.kmd` primitive), `.kfoot` brand footer.
5. **No build step needed.** Open the file directly in a browser. Tokens + primitives work via CDN-style direct links.

When generating with Lovable / v0 / similar: paste the canonical class-prefix legend (below) into the prompt context, plus the logo block, and the tool will produce on-brand markup without inventing new class names.

---

## Versioning

`v3.0` · 2026-05-15. Third major iteration. The system is now **one foundation, two products**.

For session-by-session decisions: see `../PROGRESS.md` (workspace root).
