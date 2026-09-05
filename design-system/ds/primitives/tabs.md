# Tabs — `.ktab`

> **Source of truth.** Canonical tabs primitive for the entire SuperCat
> system. One primitive, four visual variants — production apps and
> showcase pages both consume this directly.

A framework-agnostic tabs primitive. Works in React, Vue, plain HTML —
the visual is pure CSS; consumers wire the active state via
`aria-selected="true"` on the chosen item.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/tabs.css">
<script src="/ds/primitives/tabs.js" defer></script>

<nav class="ktab" role="tablist" aria-label="Order filter">
  <button class="ktab-item" role="tab" aria-selected="true" aria-controls="p1">
    Orders <span class="ktab-count">1,287</span>
  </button>
  <button class="ktab-item" role="tab" aria-controls="p2">Customers</button>
  <button class="ktab-item" role="tab" aria-controls="p3">Products</button>
</nav>

<div id="p1" role="tabpanel">…orders…</div>
<div id="p2" role="tabpanel" hidden>…customers…</div>
<div id="p3" role="tabpanel" hidden>…products…</div>
```

`tabs.js` auto-wires every `.ktab` on the page:
1. Clicks swap `aria-selected` between items.
2. The underline / vertical indicator **slides** smoothly to the new
   active item (no fade — actual position animation).
3. If items have `aria-controls`, the referenced panels toggle
   `hidden` automatically.

No framework required. For React / Vue / Svelte, you can either keep
the script and let it run on rendered DOM, or replicate the behavior
in your state layer (see "Without JS" below).

### Without JS

You can ship `.ktab` markup without `tabs.js` — the visuals work via
`aria-selected` and the CSS still renders correct colors / sizes /
chrome. What you LOSE without the script:

- The sliding indicator stays at `width: 0` (invisible). You'd need
  to set `--ktab-active-x` / `--ktab-active-w` (underline) or
  `--ktab-active-y` / `--ktab-active-h` (vertical) yourself.
- No click handling. Wire your own.
- No `aria-controls` → panel toggle.

For most apps, just include the script.

### SPA / dynamically mounted tabs

Call `window.__supercatTabsInit()` after mounting new `.ktab` markup
on a client-side route. The function is idempotent — already-wired
wrappers are skipped, only new ones are initialized.

## API

### Required classes

| Slot         | Class               | Notes                                              |
|--------------|---------------------|----------------------------------------------------|
| Wrapper      | `ktab`              | Apply to `<nav>` or `<div>` with `role="tablist"`. |
| Item         | `ktab-item`         | Apply to `<button>` or `<a>` with `role="tab"`.    |

### Variants (apply to `.ktab`)

| Class            | Effect                                                                |
|------------------|-----------------------------------------------------------------------|
| _(default)_      | Underline tabs. Hairline baseline + 2 px ink indicator on active.     |
| `ktab-pills`     | Pill tabs. Wraps onto multiple rows. Neutral filled active by default.|
| `ktab-seg`       | Segmented control. Compact iOS-style toggle group.                    |
| `ktab-vertical`  | Sidebar nav. Items stack; indicator on the left edge.                 |

### Sizes (apply to `.ktab`)

| Class       | Item height | Body size       | Use                                  |
|-------------|------------:|-----------------|--------------------------------------|
| `ktab-sm`   | 32 px       | `--text-xs` (11)| Dense toolbars, filter rows.         |
| _(default)_ | 44 px       | `--text-sm` (13)| **iPad-grade.** Most surfaces.       |
| `ktab-lg`   | 52 px       | `--text-base` (15) | Hero / marketing tab rows.        |

Sizes also propagate to pill + segmented variants:
- `ktab-pills.ktab-sm` → 28 px pills; `ktab-pills.ktab-lg` → 44 px
- `ktab-seg.ktab-sm` → 26 px segments; `ktab-seg.ktab-lg` → 36 px

### Item slots (children of `.ktab-item`)

| Class         | Effect                                                                  |
|---------------|-------------------------------------------------------------------------|
| `ktab-icon`   | Left icon slot (14×14). SVG renders stroke-only via parent currentColor.|
| `ktab-count`  | Right count badge. Mono caps, tabular numerals, paper-2 chip.           |

### Item states

| Attribute / class               | Effect                                          |
|---------------------------------|-------------------------------------------------|
| `aria-selected="true"`          | Active state. Bold weight + variant-specific.   |
| `aria-disabled="true"`          | Non-interactive. Faint text, not-allowed cursor.|
| `disabled` (on `<button>`)      | Same as `aria-disabled="true"`.                 |
| `:hover`                        | Quiet color lift (muted → primary).             |
| `:focus-visible`                | Crimson 35% glow ring (inset to avoid clipping).|

### Variant-specific active treatment

| Variant         | Active visual                                                          |
|-----------------|------------------------------------------------------------------------|
| Underline       | Bold weight + crimson text + **3 px crimson bar that slides** between items (straight bar, overlays the 1 px baseline). |
| Pills           | Filled `--color-crimson` + `--text-on-crimson`. Count badge inverts to read on crimson. Border drops to transparent. |
| Segmented       | Card-on-paper lift (`--surface-card` + `--shadow-1`).                  |
| Vertical        | Crimson text + **3 px crimson left-edge bar that slides** vertically (straight bar) + faint `--surface-2` row fill. |

The sliding bar uses `var(--duration-medium)` (320 ms) with
`var(--ease-emph)` — premium pace, confident but not lingering.
Animation disables under `prefers-reduced-motion`.

### Theming knobs (component-local custom properties)

Override per-instance with `style="--ktab-…: …"` to re-skin a single
tab strip without specificity wars.

| Property                  | Default                  | Notes                                   |
|---------------------------|--------------------------|-----------------------------------------|
| `--ktab-h`                | 44 px                    | Item height (default size).             |
| `--ktab-pad-x`            | `var(--space-4)` 16 px   | Item horizontal padding.                |
| `--ktab-fg`               | `var(--text-muted)`      | Unselected item color.                  |
| `--ktab-fg-active`        | `var(--text-primary)`    | Active item color.                      |
| `--ktab-indicator`        | `var(--text-primary)`    | Underline / left-edge bar color.        |
| `--ktab-indicator-h`      | 2 px                     | Indicator thickness.                    |
| `--ktab-pill-active-bg`   | `var(--surface-3)`       | Pill active fill. Brand override = `--color-crimson`. |
| `--ktab-pill-active-fg`   | `var(--text-primary)`    | Pill active text.                       |

## Composition patterns

### Tabs + card + table (order filter view)

```html
<nav class="ktab" role="tablist" aria-label="Order filter">
  <button class="ktab-item" role="tab" aria-selected="true">
    All <span class="ktab-count">1,287</span>
  </button>
  <button class="ktab-item" role="tab">
    Confirmed <span class="ktab-count">1,082</span>
  </button>
  <button class="ktab-item" role="tab">
    Pending <span class="ktab-count">86</span>
  </button>
</nav>

<article class="kc">
  <div class="kc-body kc-body-flush">
    <div class="kdt-wrap">
      <table class="kdt">…</table>
    </div>
  </div>
</article>
```

The pattern: tabs sit above the card (margin-bottom). Card embeds the
table edge-to-edge via `.kc-body-flush`. One coherent surface.

### Settings — pill tabs + vertical fallback

```html
<!-- Desktop / iPad landscape: pill row that wraps -->
<nav class="ktab ktab-pills" role="tablist" aria-label="Settings">
  <button class="ktab-item" role="tab" aria-selected="true">Company Information</button>
  <button class="ktab-item" role="tab">Data Import</button>
  …
</nav>

<!-- iPad portrait / narrow: vertical sidebar -->
<nav class="ktab ktab-vertical" role="tablist" aria-label="Settings">
  <button class="ktab-item" role="tab" aria-selected="true">Company Information</button>
  <button class="ktab-item" role="tab">Data Import</button>
  …
</nav>
```

For responsive apps, render both and toggle via container queries or
media queries — same markup, same active state, different chrome.

### Segmented control — inline view-mode switch

```html
<div style="display: flex; gap: var(--space-3); align-items: center;">
  <span class="kc-eyebrow">View</span>
  <nav class="ktab ktab-seg" role="tablist">
    <button class="ktab-item" role="tab" aria-selected="true">List</button>
    <button class="ktab-item" role="tab">Grid</button>
    <button class="ktab-item" role="tab">Cards</button>
  </nav>
</div>
```

## Tokens consumed

Semantic layer only — no `--k-*` legacy tokens, no raw hex.

- **Color**: `--text-{primary,strong,body,muted,faint,on-crimson}`,
  `--surface-{card,page,2,3}`, `--border-{subtle,default,strong}`,
  `--color-crimson`
- **Type**: `--font-{sans,mono}`, `--text-{2xs,xs,sm,base}`,
  `--weight-{medium,semibold}`
- **Space**: `--space-{1,2,3,4,5}`
- **Radius**: `--radius-{md,pill}`
- **Shadow**: `--shadow-1`
- **Motion**: `--duration-{fast,base}`, `--ease-out`

## Accessibility

| Concern         | How it's handled                                                  |
|-----------------|-------------------------------------------------------------------|
| Semantics       | `role="tablist"` on `.ktab`, `role="tab"` on `.ktab-item`,        |
|                 | `role="tabpanel"` on the matching content panes.                  |
| Selection       | `aria-selected="true"` drives the visual active state.            |
| Disabled        | `aria-disabled="true"` or native `disabled` on `<button>`.        |
| Keyboard        | Use native `<button>` elements — Tab to focus, Enter/Space to     |
|                 | activate. For arrow-key navigation, wire it in your app layer     |
|                 | (the primitive is markup-only).                                   |
| Focus           | `:focus-visible` crimson glow ring (inset to avoid clipping       |
|                 | inside `.ktab` overflow scroll).                                  |
| Touch targets   | Default 44 px height meets iPad guidelines. `ktab-sm` (32 px)     |
|                 | is for power-user / desktop-only surfaces.                        |
| Reduced motion  | All `transition` rules disable under `prefers-reduced-motion`.    |
| Dark theme      | All tokens flip via the semantic layer; no per-rule duplication.  |

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Wrap tabs in `<nav>` with an `aria-label` describing what they filter. | Use a plain `<div>` with no role — kills screen-reader semantics. |
| Use real `<button>` elements for tab items. | Add `onClick` to a `<div class="ktab-item">` — no keyboard support. |
| Set `aria-selected="true"` on the active item; update via your state. | Toggle a custom `.is-active` class — `aria-selected` IS the source of truth. |
| Use `.ktab-count` for badges; mono numerals already configured. | Hand-roll a circle in a span — drift from the system. |
| Pick a variant per surface: underline for primary nav, pills for many-option, segmented for toggles. | Mix three variants on one page — pick one per surface. |
| Use pills for many-option strips (Settings nav, filters). Use underline for primary view switching. | Mix three tab variants on one page — pick one per surface. |

## Examples

See `tabs.html` for the full visual suite:

- §1 — Underline (default, with count badges, with icons)
- §2 — Pills (default neutral + brand crimson)
- §3 — Segmented control (compact toggles)
- §4 — Vertical (Settings sidebar pattern)
- §5 — Sizes (sm · default · lg)
- §6 — Composition (tabs + card + table)
- §7 — Functional demo (click to switch panels, 12-line vanilla JS)

## Local preview

```
http://localhost:8000/ds/primitives/tabs.html
```

## Relation to `ds/sections/11-tabs.css`

The section file is the master-page showcase. It uses the verbose
`.ds-tabs-*` / `.ds-vtabs-*` namespace and consumes legacy `--k-*`
tokens. This primitive (`.ktab`) is the canonical production reference.
Production consumers (App screens, marketing) use `.ktab`. The section
file's inventory will be migrated to consume `.ktab` in a future pass —
when that lands, `ds/sections/11-tabs.css` will collapse to a thin
shim that just provides the showcase layout chrome.

## Open work

- Programmatic keyboard navigation (Arrow keys, Home/End) is an
  app-layer concern. The primitive provides the visual contract;
  behavior lives in your framework.
- Closable tabs (`<button class="ktab-close">`) for tab-as-document
  patterns — intentionally out of scope for now. Apps that need this
  pattern can extend with a `.ktab-close` button inside each item.
