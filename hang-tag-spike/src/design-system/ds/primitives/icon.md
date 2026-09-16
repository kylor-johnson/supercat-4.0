# Icon wrapper — `.ki`

> **Decorative icon container.** For marketing pages, feature lists,
> empty-state visuals, branded glyphs. **Never for actions** —
> interactive icons live in `.kb kb-icon` (the button primitive).

Pure CSS, framework-agnostic, no JS.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/icon.css">

<span class="ki ki-lg ki-circle ki-primary">
  <svg viewBox="0 0 24 24">
    <path d="M12 2v20M2 12h20"/>
  </svg>
</span>
```

## API

| Slot   | Classes |
|--------|---------|
| Base   | `ki` |
| Size   | `ki-xs` · `ki-sm` · `ki-md` (default) · `ki-lg` · `ki-xl` · `ki-2xl` · `ki-3xl` |
| Shape  | `ki-square` · `ki-rounded` (default) · `ki-pill` · `ki-circle` |
| Tone   | `ki-neutral` (default) · `ki-primary` · `ki-accent` · `ki-gold` · `ki-ghost` |

### Sizes

| Class    | Wrapper | SVG  | Use                                         |
|----------|---------|------|---------------------------------------------|
| `ki-xs`  | 24 px   | 14   | Inline run with text                        |
| `ki-sm`  | 32 px   | 18   | List items, table-row decoration            |
| `ki-md` ⭐ | 40 px   | 24   | **Default.** Feature lists, sidebar items   |
| `ki-lg`  | 56 px   | 28   | Cards, marketing tiles                      |
| `ki-xl`  | 72 px   | 36   | Section heroes, empty states                |
| `ki-2xl` | 96 px   | 48   | Landing-page features, big tiles            |
| `ki-3xl` | 128 px  | 64   | Hero art, page-scale decoration             |

### Shapes

| Class         | Radius                  | Reads as              |
|---------------|-------------------------|-----------------------|
| `ki-square`   | `--radius-sm` (4 px)    | Tile, app icon        |
| `ki-rounded` ⭐ | `--radius-md` (8 px)    | **Default.** Card     |
| `ki-pill`     | `--radius-lg` (12 px)   | Soft chip             |
| `ki-circle`   | `--radius-pill`         | Avatar / badge        |

### Tones

| Class         | Background                   | Foreground            |
|---------------|------------------------------|-----------------------|
| `ki-neutral` ⭐ | `--surface-2` (paper)        | `--text-primary`      |
| `ki-primary`  | `--action-primary-tint`      | `--color-crimson`     |
| `ki-accent`   | `--color-ink-1`              | `--color-paper-1`     |
| `ki-gold`     | `--color-gold-l`             | `--color-gold`        |
| `ki-ghost`    | transparent                  | `--text-primary` + border |

## Examples

### Marketing feature list

```html
<div class="features">
  <article>
    <span class="ki ki-lg ki-circle ki-primary">
      <svg viewBox="0 0 24 24">
        <path d="M12 2v20M2 12h20"/>
      </svg>
    </span>
    <h3>Plus one</h3>
    <p>Decorative wrapper, brand crimson tint, lifted on dark.</p>
  </article>
</div>
```

### Empty-state hero

```html
<div class="empty-state">
  <span class="ki ki-2xl ki-rounded ki-neutral">
    <svg viewBox="0 0 24 24">
      <rect x="3" y="6" width="18" height="14" rx="2"/>
      <path d="M3 10h18M8 6V3M16 6V3"/>
    </svg>
  </span>
  <h2>Nothing here yet</h2>
</div>
```

### Inline with text

```html
<p>
  This step earns
  <span class="ki ki-xs ki-circle ki-gold" style="vertical-align: -4px;">
    <svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/></svg>
  </span>
  bonus points.
</p>
```

## Why a separate primitive?

`.kb-icon` is for **clickable** icon buttons — they ship with hover,
focus rings, press animations, and interactive ARIA semantics. `.ki` is
purely visual chrome. Mixing the two leads to non-button-looking buttons
and clickable-looking decorations — both confusing.

If your "icon" is keyboard-focusable, it's a button. Otherwise, it's a
`.ki`.

## Customising

Per-instance overrides via component-local custom properties:

```html
<span class="ki ki-lg ki-circle"
      style="--ki-bg: #FFE8E0; --ki-fg: #B23A00;">
  <svg>…</svg>
</span>
```

| Property      | Purpose                  |
|---------------|--------------------------|
| `--ki-bg`     | Wrapper background       |
| `--ki-fg`     | SVG stroke color         |
| `--ki-border` | Wrapper border           |
| `--ki-size`   | Wrapper dimensions       |
| `--ki-pad`    | Inner padding            |
| `--ki-icon`   | SVG size                 |
| `--ki-radius` | Wrapper corner radius    |

## Accessibility

- Decorative only. Always add `aria-hidden="true"` to the wrapper OR to
  the inner `<svg>` so screen readers skip it.
- If the icon conveys meaning, pair it with adjacent visible text or a
  visually-hidden label.
