# Data table — `.kdt`

> **Source of truth.** Canonical table primitive for the entire
> SuperCat system. Production apps, prototypes, framework integrations,
> and AI-generated code all use `.kdt`. The master DS showcase in
> `ds/sections/13-tables.jsx` and the App screens at `app/screen-*.jsx`
> consume the same primitive directly.

iPad-grade, framework-agnostic data table. Works with React, Vue, plain
HTML — any DOM the browser renders. Authors compose classes; state is
driven by ARIA attributes (`aria-sort`, `aria-selected`, `aria-busy`)
and `data-*` for visual states.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/table.css">

<div class="kdt-wrap">
  <table class="kdt">
    <thead>
      <tr>
        <th class="kdt-check"><input type="checkbox" aria-label="Select all"/></th>
        <th>Order #</th>
        <th>Customer</th>
        <th class="kdt-num">Total</th>
        <th class="kdt-actions" aria-label="Actions"></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="kdt-check"><input type="checkbox" aria-label="Select row"/></td>
        <td class="kdt-mono">112625-10</td>
        <td>Brent Sanders</td>
        <td class="kdt-num">$12,480.00</td>
        <td class="kdt-actions"><button class="kdt-act" aria-label="Row actions">…</button></td>
      </tr>
    </tbody>
  </table>
</div>
```

No JS required for the visual primitive. Selection state is whatever
your app sets on `<tr aria-selected="true">`. Sortable state is whatever
your app sets on `<th aria-sort="ascending|descending|none">`. The
bulk-actions strip is just a `.kdt-bulk` element with `hidden` toggled
based on selection count.

## API

### Required classes

| Slot         | Class               | Notes                                              |
|--------------|---------------------|----------------------------------------------------|
| Wrapper      | `kdt-wrap`          | Provides horizontal scroll + sticky header frame.  |
| Table        | `kdt`               | Apply to `<table>`.                                |

The wrapper is **not** optional. The table primitive expects to live
inside one — that's where overflow, sticky-head shadow, and stack-mode
re-flow are scoped.

### Density (apply to the table)

| Class            | Row height | Cell padding         | Body size | Use                                       |
|------------------|-----------:|----------------------|-----------|-------------------------------------------|
| `kdt-compact`    | 32px       | 8px × 12px           | 11px      | Power-user dense screens (admin, finance).|
| _(default)_      | 44px       | 12px × 16px          | 13px      | **iPad-grade.** Most app surfaces.        |
| `kdt-cozy`       | 60px       | 16px × 20px          | 15px      | Tablets in landscape; settings-adjacent.  |

### Surface (apply to the table — except `kdt-card` which is on the wrapper)

| Class               | Effect                                                          |
|---------------------|-----------------------------------------------------------------|
| _(default)_         | Hairline row dividers, transparent rows.                        |
| `kdt-zebra`         | Alternating row tint; no row dividers. Good for number scans.   |
| `kdt-card`          | **Wrapper class.** Bordered rounded container; no row dividers. |

### Wrapper modifiers

| Class                  | Effect                                                              |
|------------------------|---------------------------------------------------------------------|
| `kdt-sticky-head`      | `<thead>` sticks to the wrapper top during vertical scroll.         |
| `kdt-sticky-first`     | First column stays anchored during horizontal scroll.               |
| `kdt-stack`            | At ≤640px, re-flow rows to stacked label-value cards.               |

### Cell-type classes (apply to `<th>` and matching `<td>`)

| Class            | Effect                                                                 |
|------------------|------------------------------------------------------------------------|
| `kdt-mono`       | Mono font + tabular numerals. IDs, timestamps, SKUs.                   |
| `kdt-num`        | Right-aligned + tabular numerals. Money, counts, percentages.          |
| `kdt-status`     | Vertical padding collapses; cell hosts a `.kdt-pill` chip.             |
| `kdt-actions`    | Right-aligned, narrow (44px). Hosts a `.kdt-act` kebab button.         |
| `kdt-check`      | First column, 44px wide. Hosts the row checkbox.                       |
| `kdt-soft`       | Cell text reads as `--text-muted`. Use for secondary metadata.         |
| `kdt-faint`      | Cell text reads as `--text-faint`. Even quieter than `kdt-soft`.       |
| `kdt-wrap-cell`  | Opt out of nowrap — let this cell wrap (long descriptions).            |
| `kdt-trunc`      | Truncate to a single line with ellipsis (defaults to 22ch).            |

### Row states

| Attribute / class                       | Effect                                          |
|-----------------------------------------|-------------------------------------------------|
| `<tr aria-selected="true">`             | Solid crimson left-edge bar + paper-lift tint.  |
| `<tr data-row-state="muted">`           | Row text reads as `--text-muted` (archived).    |
| `<tbody aria-busy="true">`              | Used together with `.kdt-skel` rows for loading.|
| `<table data-empty>`                    | Convention for sibling `.kdt-empty-board` slot. |

### Sortable headers

```html
<th aria-sort="ascending">
  <button class="kdt-sort" type="button">
    Customer
    <span class="kdt-sort-ind" aria-hidden="true"></span>
  </button>
</th>
```

`aria-sort` is the source of truth — the indicator and color follow.
Valid values: `none` · `ascending` · `descending` · `other`.

### Status pills (built in)

```html
<span class="kdt-pill kdt-pill-success">
  <span class="kdt-pill-dot" aria-hidden="true"></span> Confirmed
</span>
```

Variants: `kdt-pill-success` · `kdt-pill-warning` · `kdt-pill-danger`
· `kdt-pill-info` · `kdt-pill-neutral`.

**Migration note.** These chips are inlined here so the table primitive
ships zero-dependency. When the standalone Tag primitive `.kt-*` lands,
`.kdt-pill-*` will alias to `.kt-tag-*` (same visual language). No
markup changes required in your pages.

### Bulk-actions strip

```html
<div class="kdt-bulk" hidden>
  <span class="kdt-bulk-count"><strong>3</strong> selected</span>
  <span class="kdt-bulk-spacer"></span>
  <button>Export</button>
  <button>Mark shipped</button>
  <button>Archive</button>
</div>
```

Place the strip immediately before the `.kdt-wrap`. Remove the `hidden`
attribute when selection count > 0. The strip is full-width, ink-dark,
mono-cased — a quiet "active mode" replacement for the otherwise-empty
header rail above the table.

### Empty states

Two flavors:

1. **Inline empty row** — a single `<tr class="kdt-empty-row">` with one
   `colspan` `<td>`. Use when filters return no results.
2. **Empty board** — `.kdt-empty-board` rendered as a sibling of the
   table inside the wrapper. Use for first-run / never-had-any moments.

```html
<div class="kdt-wrap">
  <table class="kdt">…<tbody></tbody></table>
  <div class="kdt-empty-board">
    <div class="kdt-empty-mark" aria-hidden="true">…icon svg…</div>
    <h3>No orders yet</h3>
    <p>When sales reps submit orders, they'll appear here.</p>
    <button class="kb kb-md kb-primary">Import CSV</button>
  </div>
</div>
```

### Loading

```html
<tbody aria-busy="true">
  <tr class="kdt-skel">
    <td><span class="kdt-skel-bar" style="--w: 70%"></span></td>
    <td><span class="kdt-skel-bar" style="--w: 50%"></span></td>
    …
  </tr>
</tbody>
```

`--w` sizes the bar within the cell. Vary it per column so the skeleton
reads as plausible content rather than a uniform stripe.

### Responsive collapse to stacked cards

Add `.kdt-stack` to the wrapper **and** a `data-label="…"` attribute to
every `<td>`. Below 640px:

- Headers hide
- Each row renders as a card with the label-value pairs stacked
- Number cells left-align
- Actions cell hides

```html
<div class="kdt-wrap kdt-stack">
  <table class="kdt">
    <thead><tr><th>Order #</th><th>Customer</th><th class="kdt-num">Total</th></tr></thead>
    <tbody>
      <tr>
        <td data-label="Order #" class="kdt-mono">112625-10</td>
        <td data-label="Customer">Brent Sanders</td>
        <td data-label="Total" class="kdt-num">$12,480.00</td>
      </tr>
    </tbody>
  </table>
</div>
```

## Tokens consumed

Semantic layer only — no `--k-*` legacy tokens, no raw hex.

- **Color**: `--text-{primary,strong,body,muted,faint}`,
  `--surface-{card,page,2,3}`, `--border-{subtle,default,strong}`,
  `--color-{crimson,crimson-l,gold,gold-l}`,
  `--status-{success,warning,danger,info}` (+ `-tint`),
  `--text-on-crimson`, `--action-primary`
- **Type**: `--font-{sans,mono}`, `--text-{2xs,xs,sm,base,lg}`,
  `--tracking-{wider,widest}`, `--leading-{relaxed,normal}`,
  `--weight-{medium,semibold}`
- **Space**: `--space-{1,2,3,4,5,6,10,12}`
- **Radius**: `--radius-{xs,sm,md,lg,pill,full}`
- **Motion**: `--duration-{fast,base}`, `--ease-out`

## Accessibility

| Concern          | How it's handled                                                |
|------------------|-----------------------------------------------------------------|
| Table semantics  | Native `<table>` + `<thead>`/`<tbody>` + `<th scope="col">`.    |
| Sort state       | `aria-sort` on each sortable `<th>`. Indicator follows it.      |
| Selection        | `aria-selected` on the `<tr>`. Checkbox has `aria-label`.       |
| Loading state    | `aria-busy="true"` on the `<tbody>`.                            |
| Keyboard         | Sort buttons, row actions, and checkboxes are all `<button>` /  |
|                  | `<input>` with proper focus rings (`:focus-visible` + crimson). |
| Touch targets    | Default density: 44px row, 44px checkbox column, 44px action.   |
| Reduced motion   | All transitions disabled; skeleton shimmer stops.               |
| Dark theme       | Token-based; no per-rule duplication needed except 4 overrides. |

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Use `.kdt-mono` for IDs, timestamps, SKUs. | Render IDs in plain prose — they don't line up. |
| Render empty cells with `<span class="kdt-empty">—</span>`. | Render empty city/state as raw `", "` — broken. |
| Reserve crimson for active sort + selection edge + status-danger pill. | Make every order-number cell crimson. Loses meaning. |
| Use status pills for any categorical column (status, tier, source). | Use color *alone* — every pill carries a dot + label. |
| Wrap every table in `.kdt-wrap`. | Place `<table class="kdt">` directly in flow. |
| Set `aria-sort` to drive the indicator. | Toggle a `.is-sorted` class — `aria-sort` is the source of truth. |
| Use density variants to fit the surface. | Override row height in page CSS — drift. |

## Examples

See `table.html` for the full visual suite:

- §1 — Default Orders shape (10 rows, all real states)
- §2 — Density variants (compact / default / cozy, same data)
- §3 — Surface variants (flat / zebra / card)
- §4 — Status pill catalog
- §5 — Sticky head + sticky first column (vertical + horizontal scroll)
- §6 — Sortable columns with `aria-sort`
- §7 — Selection with bulk-actions strip (working JS demo)
- §8 — Empty state (inline + full board)
- §9 — Loading with skeleton rows
- §10 — Responsive collapse to stacked cards (resize ≤640px to see)

## Local preview

```
http://localhost:8000/ds/primitives/table.html
```

## Open work (tracked in `AUDIT-2026-05-15.md`)

- `.kdt-pill-*` will alias to the standalone Tag primitive (`.kt-*`) once that lands. No markup migration in pages.
- A `kdt-virtual` mode (for 10k-row tables with row recycling) is intentionally out-of-scope here — that's an app-layer concern. The primitive supports `aria-rowcount` / `aria-rowindex` if you wire it.
- Multi-row drag-to-select and shift-click range selection are app concerns. The primitive provides the visual contract; behavior lives in your data layer.
