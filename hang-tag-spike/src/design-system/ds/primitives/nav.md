# Side nav — `.knav`

> **Source of truth.** Canonical sidebar primitive for the SuperCat App
> shell. NOT to be confused with `nav/nav.css` (the marketing-site
> mega-menu, which is a horizontal top nav). This is the vertical left
> sidebar for app surfaces — Dashboard, Orders, Settings, etc.

Framework-agnostic. Pure CSS for visuals; consumers set the active state
via `aria-current="page"` on the chosen item.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/nav.css">

<aside class="knav" aria-label="Primary navigation">
  <header class="knav-brand">
    <a class="knav-brand-link" href="/">
      <span class="knav-brand-mark"><svg>…</svg></span>
      <span class="knav-brand-name">Supercat</span>
    </a>
  </header>

  <div class="knav-body">
    <nav class="knav-list" aria-label="Main">
      <a class="knav-item" href="/home"><span class="knav-icon"><svg>…</svg></span><span class="knav-text">Home</span></a>
      <a class="knav-item" aria-current="page" href="/dashboard"><span class="knav-icon"><svg>…</svg></span><span class="knav-text">Dashboard</span></a>
      <a class="knav-item" href="/orders"><span class="knav-icon"><svg>…</svg></span><span class="knav-text">Orders</span><span class="knav-trail"><span class="knav-count">1,287</span></span></a>
    </nav>

    <div class="knav-section">
      <h3 class="knav-eyebrow">Settings &amp; Tools</h3>
      <nav class="knav-list">…</nav>
    </div>

    <div class="knav-spacer"></div>
  </div>

  <footer class="knav-account">
    <div class="knav-org">
      <span class="knav-org-badge">OP</span>
      <span class="knav-org-name">Opame Collective</span>
    </div>
    <button class="knav-user">
      <span class="knav-user-avatar">AM</span>
      <span class="knav-user-info">
        <span class="knav-user-name">Alex Malyshev</span>
        <span class="knav-user-role">Account</span>
      </span>
    </button>
  </footer>
</aside>
```

No JS required for the visual primitive. Selection is whatever your
app sets via `aria-current="page"`. Expandable groups toggle
`aria-expanded` — wire your own state.

## API

### Required structure

| Slot              | Class                  | Purpose                              |
|-------------------|------------------------|--------------------------------------|
| Wrapper           | `knav`                 | The `<aside>` container.             |
| Brand header      | `knav-brand`           | Top block — logo + name.             |
| Body              | `knav-body`            | Scrollable middle area.              |
| Item              | `knav-item`            | One nav row.                         |
| List              | `knav-list`            | Group of items (any `<nav>`/`<ul>`). |
| Section group     | `knav-section`         | Subsection with eyebrow heading.     |
| Eyebrow           | `knav-eyebrow`         | Mono-caps section label.             |
| Spacer            | `knav-spacer`          | `flex: 1` pusher (push footer down). |
| Account footer    | `knav-account`         | Bottom block — org + user.           |

### Sizes (apply to `.knav`)

| Class       | Width  | Item height | Icon | Use                                  |
|-------------|-------:|------------:|-----:|--------------------------------------|
| `knav-sm`   | 200 px | 36 px       | 16   | Tight surfaces, secondary apps.      |
| _(default)_ | 240 px | 40 px       | 18   | **App default.** Matches screenshot. |
| `knav-lg`   | 280 px | 44 px       | 20   | Roomy / iPad landscape primary nav.  |

### Variants (apply to `.knav`)

| Class          | Effect                                                              |
|----------------|---------------------------------------------------------------------|
| _(default)_    | Always-visible sidebar, full width.                                 |
| `knav-rail`    | Collapsed to 64 px — icons only, no labels/trail/count/eyebrow.     |
| `knav-drawer`  | Off-canvas drawer for iPad portrait + mobile. Toggle with `aria-expanded` on the `.knav-drawer` element. Pair with `<div class="knav-backdrop"></div>` sibling. |
| `knav-embedded`| Inside a layout container — drops the `min-height: 100dvh`.         |

### Item slots (children of `.knav-item`)

| Class                 | Effect                                                          |
|-----------------------|-----------------------------------------------------------------|
| `knav-icon`           | Leading 18-px icon slot. SVG stroke-only.                       |
| `knav-text`           | The label. Ellipsizes on overflow.                              |
| `knav-trail`          | Trailing slot — chevron, count, status dot.                     |
| `knav-count`          | Count badge inside trail. Mono caps, tabular numerals.          |

### States

| Attribute / class               | Effect                                          |
|---------------------------------|-------------------------------------------------|
| `aria-current="page"`           | Active state. Paper-2 fill + bold + crimson count badge. |
| `aria-disabled="true"`          | Faint text, not-allowed cursor.                 |
| `aria-expanded="true"`          | Expandable group is open. Chevron rotates to point down. Sub-list visible. |
| `aria-expanded="false"`         | Sub-list hidden.                                |
| `:hover`                        | Paper-page fill + text-primary lift.            |
| `:focus-visible`                | Crimson 35 % glow ring.                         |

### Expandable groups

```html
<button class="knav-item" aria-expanded="true" aria-controls="orders-sub">
  <span class="knav-icon"><svg>…</svg></span>
  <span class="knav-text">Orders</span>
  <span class="knav-trail"><svg><!-- chevron --></svg></span>
</button>
<ul class="knav-sublist" id="orders-sub">
  <li><a class="knav-item" href="/orders/all">All orders</a></li>
  <li><a class="knav-item" href="/orders/pending">Pending</a></li>
</ul>
```

Use a `<button>` for the parent (not an `<a>`) since clicking toggles
the sub-list, not navigates. The chevron rotates 90 ° when expanded.
The sub-list lives in `.knav-sublist` directly after the parent;
it auto-hides when `aria-expanded="false"`.

### Account footer

```html
<footer class="knav-account">
  <div class="knav-org">
    <span class="knav-org-badge">OP</span>
    <span class="knav-org-name">Opame Collective</span>
  </div>
  <button class="knav-user">
    <span class="knav-user-avatar">AM</span>
    <span class="knav-user-info">
      <span class="knav-user-name">Alex Malyshev</span>
      <span class="knav-user-role">Account</span>
    </span>
    <span class="knav-user-trail"><svg><!-- chevron --></svg></span>
  </button>
</footer>
```

- **`knav-org-badge`** — 28 × 28 gold square with two-letter mono caps initials.
- **`knav-user-avatar`** — 32 × 32 crimson circle with cream initials.
- **`knav-user`** is a real `<button>` — opens a user menu when clicked.

### Theming knobs (component-local CSS custom properties)

Override per-instance with `style="--knav-w: 260px"` etc.

| Property             | Default                    | Notes                                    |
|----------------------|----------------------------|------------------------------------------|
| `--knav-w`           | 240 px                     | Sidebar width.                           |
| `--knav-bg`          | `var(--surface-card)`      | Sidebar background.                      |
| `--knav-border`      | `var(--border-default)`    | Hairline on the right edge.              |
| `--knav-item-h`      | 40 px                      | Item row height.                         |
| `--knav-bg-active`   | `var(--surface-2)`         | Active item fill. Swap to a brand color for stronger wayfinding. |
| `--knav-bg-hover`    | `var(--surface-page)`      | Hover row fill.                          |
| `--knav-icon-size`   | 18 px                      | Leading icon dimension.                  |

## Tokens consumed

Semantic layer only — no `--k-*` legacy tokens, no raw hex.

- **Color**: `--text-{primary,strong,body,muted,faint,on-crimson}`,
  `--surface-{card,page,2,3,overlay}`,
  `--border-{subtle,default,strong}`,
  `--color-{crimson,gold,ink-1}`
- **Type**: `--font-{sans,mono}`, `--text-{2xs,sm,base}`,
  `--tracking-{wider,widest}`, `--weight-{medium,semibold}`
- **Space**: `--space-{1,2,3,4,5,6}`
- **Radius**: `--radius-{sm,md,pill,full}`
- **Shadow**: `--shadow-{1,4}`
- **Motion**: `--duration-{base,medium}`, `--ease-{out,emph}`

## Accessibility

| Concern         | How it's handled                                                  |
|-----------------|-------------------------------------------------------------------|
| Semantics       | `<aside>` for the wrapper; `<nav>` for each list with a unique    |
|                 | `aria-label`. Sub-lists are `<ul>` of `<li>`s.                    |
| Active item     | `aria-current="page"` drives the visual state. Screen readers     |
|                 | announce "current page".                                          |
| Disabled item   | `aria-disabled="true"` — keep the link in the DOM for context,    |
|                 | strip its href if it shouldn't navigate.                          |
| Expandable      | `aria-expanded` + `aria-controls`. Parent must be a `<button>`    |
|                 | so it's announced as a toggle.                                    |
| Keyboard        | Native `<a>` / `<button>` — Tab to focus, Enter / Space to        |
|                 | activate. Arrow-key navigation is an app-layer concern.           |
| Touch targets   | Default 40 px items (iPad-grade). `knav-lg` is 44 px for primary  |
|                 | tablet contexts. Tap zones extend to the full row width.          |
| Focus rings     | Crimson 35 % glow, inset to avoid clipping in the scroll body.    |
| Reduced motion  | All `transition` rules disable cleanly.                           |
| Dark theme      | All tokens flip via the semantic layer.                           |

## Composition patterns

### App shell — sidebar + topbar + main

```html
<div class="kshell">
  <aside class="knav">…</aside>
  <div class="kshell-main">
    <header class="kshell-top">…breadcrumb + actions…</header>
    <main class="kshell-content">
      …page content…
    </main>
  </div>
</div>
```

`.kshell` is a thin CSS Grid layout — see `app/orders.html` for the
canonical composition with sidebar + topbar + main + nested
`.ktab` + `.kc` + `.kdt`.

### Rail with hover-expand

To make `.knav-rail` expand on hover (common iPad portrait pattern),
add a transition + media query in your app layer:

```css
.knav-rail:hover {
  --knav-w: 240px;
}
.knav-rail .knav-text,
.knav-rail .knav-trail { display: revert; }
```

Out of scope for the primitive itself — the rail variant is "icons
only" by default; consumers compose hover-expand if they want it.

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Set `aria-current="page"` on the active item — let CSS style it. | Toggle a custom `.is-active` class. ARIA IS the state. |
| Give each `<nav>` a unique `aria-label` (Primary, Settings, etc.). | Leave `<nav>` unlabeled — screen readers can't differentiate. |
| Use `<button>` for expandable groups (they toggle, not navigate). | Wrap a toggle in `<a href="#">` — kills screen-reader semantics. |
| Match `.knav-rail` width to your icon-set's optical size. | Custom-width rails — 64 px is the canonical iPad-friendly target. |
| Reserve `aria-current="page"` for the ACTUAL current page. | Mark multiple items active — only one page is current at a time. |

## Examples

See `nav.html` for the full visual suite:

- §1 — Default sidebar (the App pattern)
- §2 — Sizes (sm 200 / default 240 / lg 280)
- §3 — Rail (collapsed to 64 px, icons only)
- §4 — Expandable groups (sub-lists, aria-expanded)
- §5 — Dark theme (zero per-rule overrides)

For the App composition (sidebar + topbar + tabs + table), see
`app/orders.html` — the Orders screen redesigned.

## Local preview

```
http://localhost:8000/ds/primitives/nav.html
http://localhost:8000/app/orders.html         (App composition demo)
```

## Relation to `nav/nav.css`

`nav/nav.css` is the **marketing-site mega-menu** — a horizontal top
nav for the SuperCat home page and content kit. `.knav` (this file)
is the **App sidebar** — a vertical left rail. Different surface
context, different visual vocabulary, different namespace. Don't mix.

## Open work

- Mobile drawer wire-up (`.knav-drawer` works but consumers must
  manage `aria-expanded` themselves; a small `nav.js` helper for
  toggle + outside-click + focus trap is nice-to-have).
- Tooltip layer for `.knav-rail` labels (out of scope — apps should
  use their own tooltip primitive when this ships).
- Pinned / favorites section above the main list (consumer pattern,
  not primitive concern).
