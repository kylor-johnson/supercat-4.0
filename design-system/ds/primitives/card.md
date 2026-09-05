# Card — `.kc`

> **Source of truth.** Canonical card primitive for the entire SuperCat
> system. The Master DS showcase, the App's dashboard tiles, summary
> panels, and activity feeds all compose from this primitive.

A surface for grouping content. Slots own their own padding so cards
embed edge-to-edge tables and lists cleanly. Framework-agnostic — works
in React, Vue, plain HTML, anywhere.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/card.css">

<article class="kc">
  <header class="kc-head">
    <div class="kc-head-lead">
      <span class="kc-eyebrow">Past 30 days</span>
      <h3 class="kc-title">Best selling products</h3>
    </div>
    <div class="kc-head-actions">
      <a class="kb kb-link" href="#">Full report</a>
    </div>
  </header>
  <div class="kc-body">…</div>
  <footer class="kc-foot">
    <span class="kc-foot-meta">5 of 47 SKUs</span>
    <span class="kc-foot-spacer"></span>
    <button class="kb kb-sm kb-secondary">Export</button>
  </footer>
</article>
```

No JS required. Cards rendered as `<a>` or `<button>` automatically get
cursor: pointer; interactive hover/focus styling requires
`.kc-interactive` (so non-link cards can opt in).

## API

### Required classes

| Slot   | Class | Notes                                                      |
|--------|-------|------------------------------------------------------------|
| Block  | `kc`  | Apply to `<article>`, `<section>`, `<a>`, or `<button>`.   |

### Sizes (apply to `.kc`)

| Class       | Padding (x · y) | Radius           | Use                                |
|-------------|-----------------|------------------|------------------------------------|
| `kc-sm`     | 16 · 16 px      | `--radius-md`    | Toolbars, sidebar groups, dense.   |
| _(default)_ | 24 · 20 px      | `--radius-lg`    | **Everyday card.**                 |
| `kc-lg`     | 32 · 28 px      | `--radius-xl`    | Feature panels, hero sections.     |

### Surfaces (apply to `.kc`)

| Class             | Effect                                                                |
|-------------------|-----------------------------------------------------------------------|
| _(default)_       | Surface-card fill, hairline `--border-default`. Everyday.             |
| `kc-feature`      | Paper-2 fill, no border. Heavier emphasis — tint IS the chrome.       |
| `kc-inverse`      | `--color-ink-1` fill, cream text. Theme-agnostic.                     |
| `kc-dashed`       | Transparent fill, dashed hairline. Empty-state / "drop here".         |
| `kc-interactive`  | Hover lifts + crimson left edge fades in. Use on `<a>` / `<button>`.  |

### Slots (children of `.kc`)

| Class            | Effect                                                                   |
|------------------|--------------------------------------------------------------------------|
| `kc-head`        | Title row. Auto hairline-bottom when followed by another slot.           |
| `kc-body`        | Main content. Padded by default.                                         |
| `kc-foot`        | Footer row. Auto hairline-top when preceded by another slot.             |
| `kc-eyebrow`     | Mono caps label. Place inside `.kc-head-lead` above the title.           |
| `kc-body-flush`  | Modifier on `.kc-body`. Removes padding (for edge-to-edge tables).       |
| `kc-rule`        | Solid hairline divider inside body. Bleeds to card edges.                |
| `kc-rule-dash`   | Dashed variant of `kc-rule`.                                             |

### Head sub-slots

```html
<header class="kc-head">
  <div class="kc-head-lead">
    <span class="kc-eyebrow">Past 30 days</span>
    <h3 class="kc-title">Title goes here</h3>
  </div>
  <div class="kc-head-actions">
    <button class="kb kb-sm kb-ghost">Edit</button>
    <button class="kb kb-sm kb-secondary">Save</button>
  </div>
</header>
```

`.kc-head-lead` stacks eyebrow above title. `.kc-head-actions` is
pushed to the right by flex. Both are optional — a head can hold raw
content directly.

### Foot sub-slots

```html
<footer class="kc-foot">
  <span class="kc-foot-meta">Updated 14:39</span>
  <span class="kc-foot-spacer"></span>
  <button class="kb kb-sm kb-secondary">Export</button>
</footer>
```

`.kc-foot-meta` is mono caps muted text on the left. `.kc-foot-spacer`
pushes everything after it to the right.

### Metric compound (the dashboard stat tile)

```html
<article class="kc kc-metric">
  <span class="kc-eyebrow">Total products</span>
  <div class="kc-metric-row">
    <span class="kc-metric-val">50</span>
    <span class="kc-metric-icon"><svg>…</svg></span>
  </div>
  <span class="kc-metric-trend kc-trend-up">+ 4 this month</span>
</article>
```

`.kc-metric` overrides the slot model with its own vertical flex layout.
Eyebrow at top · big tabular numeral · optional trend below.

| Class           | Effect                                                              |
|-----------------|---------------------------------------------------------------------|
| `kc-metric`     | Stat-tile shape. Min-height 132 px. Use on `<article>`.            |
| `kc-metric-row` | Flex row holding the value and optional icon.                       |
| `kc-metric-val` | Big number — clamp(36, 4vw, 48px), sans-medium, tabular numerals.   |
| `kc-metric-icon`| 32 px slot for a stroked 22 px SVG icon (right-aligned).            |
| `kc-metric-trend` | Mono caps trend row. Combine with one of:                          |
| `kc-trend-up`   | Green up-triangle, `--status-success` text.                         |
| `kc-trend-down` | Red down-triangle, `--status-danger` text.                          |
| `kc-trend-flat` | Muted dash, `--text-muted` text.                                    |

### List compound (activity feeds, stat lines)

```html
<ul class="kc-list">
  <li class="kc-list-item">
    <span class="kc-list-avatar">BS</span>
    <div class="kc-list-main">
      <div class="kc-list-name">Brent Sanders</div>
      <div class="kc-list-meta">42 logins · 18 orders</div>
    </div>
    <span class="kc-list-trail">$84,320.00</span>
  </li>
  …
</ul>
```

| Class            | Effect                                                              |
|------------------|---------------------------------------------------------------------|
| `kc-list`        | Unstyled `<ul>` flex column. Place inside `.kc-body`.               |
| `kc-list-item`   | Row: 48 px min-height, hairline-divided.                            |
| `kc-list-avatar` | 32 px round chip. Initials or icon.                                 |
| `kc-list-main`   | Name + meta column. Ellipsises overflow.                            |
| `kc-list-name`   | Primary line. Sans medium.                                          |
| `kc-list-meta`   | Secondary line. Mono caps, muted.                                   |
| `kc-list-trail`  | Right-aligned trail value. Mono, tabular numerals.                  |

### Grid helper (for laying out cards)

```html
<div class="kc-grid kc-grid-4">
  <article class="kc kc-metric">…</article>
  <article class="kc kc-metric">…</article>
  <article class="kc kc-metric">…</article>
  <article class="kc kc-metric">…</article>
</div>
```

| Class           | Effect                                                              |
|-----------------|---------------------------------------------------------------------|
| `kc-grid`       | Auto-fit grid, min column 260 px. Responsive without help.          |
| `kc-grid-4`     | 4 columns above 880 px · 2 columns above 540 px · 1 below.          |
| `kc-grid-3`     | Same step-down pattern from 3.                                      |
| `kc-grid-2`     | Same step-down pattern from 2.                                      |

## Composition patterns

### Card + table (the "Best Selling Products" panel)

```html
<article class="kc">
  <header class="kc-head">
    <div class="kc-head-lead">
      <span class="kc-eyebrow">Past 30 days</span>
      <h3 class="kc-title">Best selling products</h3>
    </div>
    <div class="kc-head-actions">
      <a class="kb kb-link" href="#">Full report</a>
    </div>
  </header>
  <div class="kc-body kc-body-flush">
    <div class="kdt-wrap">
      <table class="kdt">…</table>
    </div>
  </div>
  <footer class="kc-foot">
    <span class="kc-foot-meta">5 of 47 SKUs</span>
    <span class="kc-foot-spacer"></span>
    <button class="kb kb-sm kb-secondary">Export</button>
  </footer>
</article>
```

`kc-body-flush` is the key — it kills body padding so the table runs
edge to edge inside the card frame. The table's own hairlines align
with the card's hairlines.

### Card + list (the "Most Active Users" panel)

See the list compound above — wrap the `<ul class="kc-list">` directly
inside `.kc-body` (no flush needed; the list spaces itself).

### Card + metric grid (the four dashboard tiles)

Use `.kc-grid.kc-grid-4` containing four `<article class="kc kc-metric">`.
Stack to 2 columns below 880 px, to 1 column below 540 px.

## Tokens consumed

Semantic layer only — no `--k-*` legacy tokens, no raw hex.

- **Color**: `--surface-{card,page,2,3}`, `--color-{ink-1,paper-1,crimson}`,
  `--text-{primary,strong,body,muted,faint,on-crimson}`,
  `--border-{subtle,default,strong}`,
  `--status-{success,danger}`
- **Type**: `--font-{sans,mono}`, `--text-{2xs,xs,sm,base,lg,2xl}`,
  `--tracking-{wider,widest,tighter,tightest}`,
  `--leading-{snug,relaxed,tight}`, `--weight-{medium,semibold}`
- **Space**: `--space-{1,2,3,4,5,6,7,8,10,12}`
- **Radius**: `--radius-{md,lg,xl,pill,full}`
- **Shadow**: `--shadow-{1,2}`
- **Motion**: `--duration-{fast,base}`, `--ease-out`

## Accessibility

| Concern          | How it's handled                                                  |
|------------------|-------------------------------------------------------------------|
| Semantics        | Use `<article>` or `<section>` for content; `<a>` or `<button>`   |
|                  | for interactive cards.                                            |
| Keyboard         | `.kc-interactive:focus-visible` shows a crimson 35% ring.         |
| Touch targets    | Default 24 px padding → ≥56 px head/foot rows. Interactive cards  |
|                  | inherit any `<a>` / `<button>` accessibility for free.            |
| Reduced motion   | `:hover` lift and crimson edge disable. Card stays static.        |
| Dark theme       | All tokens flip via the semantic layer. Inverse cards stay        |
|                  | ink-dark in both themes by design.                                |
| Color contrast   | Inverse cards use `--text-on-crimson` (cream) on `--color-ink-1`  |
|                  | (deep ink) — explicitly engineered for WCAG AA.                   |

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Use `.kc-body-flush` when embedding a table/list edge-to-edge. | Wrap a `.kdt-card` inside a `.kc` — double frames. |
| Reach for `.kc-feature` sparingly — it's emphasis, not decoration. | Use `.kc-feature` for everyday content cards. |
| Render interactive cards as `<a>` or `<button>`. | Add `onClick` to a `<div class="kc">` — no keyboard, no a11y. |
| Use `.kc-inverse` for stamped/feature tiles in any context. | Use `.kc-inverse` inside an already-dark surface — read fails. |
| Use the metric compound for dashboard stats. | Build stat tiles by hand inside `.kc-head` — drift from canon. |
| Combine `.kc-grid.kc-grid-4` with four metric cards. | Hand-roll a grid with media queries — the helper covers it. |

## Examples

See `card.html` for the full visual suite:

- §1 — Anatomy (head · body · foot · body-only)
- §2 — Sizes (sm 16 · md 24 default · lg 32 padding)
- §3 — Surfaces (flat default · feature · inverse · dashed)
- §4 — Metric tiles (the four-stat dashboard pattern)
- §5 — Panels with tables (the "Best Selling Products" composition)
- §6 — Activity lists (the "Most Active Users" composition)
- §7 — Interactive cards (hover lift + crimson edge)
- §8 — Empty / dashed cards

## Local preview

```
http://localhost:8000/ds/primitives/card.html
```

## Open work

- Card-level loading state (skeleton). The table primitive ships its own
  skeleton; cards inherit it when used as a panel. A standalone
  `.kc[aria-busy="true"]` skeleton could ship later if a content card
  outside the panel pattern needs it.
- Splittable cards (two cells side by side with a vertical hairline) —
  intentionally out of scope. The `.kc-grid` helper covers the
  common "row of cards" case; for split layouts use two adjacent cards.
