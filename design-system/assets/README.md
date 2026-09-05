# Brand assets

Two files, very different roles. **Don't trust filenames — read this before using.**

## `supercat-mark.svg` — icon only, single color

The cat-whisker icon, 41×28 viewBox, two paths, hardcoded gold (`#B97727`). One file, one color, no variants.

Use when you need the icon-only mark and don't need theme-awareness or color variants.

```html
<svg viewBox="0 0 41 28"><use href="#i-mark"/></svg>
```

## `logos.jsx` — canonical source for the full wordmark + every brand lockup

Despite the React filename, this file is **the only source** for the path data behind the full SuperCat wordmark and supporting brand lockups. Port it into your framework — don't try to extract a wordmark from screenshots or type the brand name as text.

Exports:

| Component | What it is | Size | Variants |
|---|---|---|---|
| `SuperCatMark` | Cat-whisker icon (theme-aware) | 41×28 | `color` / `white` / `cream` / `auto` |
| `SuperCatLogo` | **Full "SuperCat Solutions" wordmark + mark lockup** | 237×28 | `color` / `white` / `cream` / `auto` |
| `LineCardLogo` | "THE LINE CARD" wordmark (separate active brand — TLC) | 192×16 | `color` / `white` / `cream` / `auto` |
| `SuperCatLogoPill` | Full wordmark inside a rounded pill (40px tall, 999px radius) for header/footer | composed | `dark` / `light` |

### Color variants

| Variant | Text fill | Mark fill | When to use |
|---|---|---|---|
| `color` (default) | `#7A1218` crimson | `#B97727` gold | Light surfaces (cream, white) |
| `white` | `#FFFFFF` | `#FFFFFF` | Photo / image overlays, monochrome contexts |
| `cream` | `#EDE4D6` | `#D4A85A` | Dark / ink surfaces |
| `auto` | `var(--sc-logo-ink, #7A1218)` | `var(--sc-logo-mark, #B97727)` | Theme-aware — recolors with `[data-theme]` |

### Porting notes

- **Drop** the `Object.assign(window, ...)` block at the bottom — that's legacy React-Babel runtime mount code. Use ES module exports / your framework's component pattern instead.
- **Skip** `ECatLogo` if you find it — the eCat brand was retired 2026-05-15.
- All four active components are SVG path data + variant logic. They port cleanly to React, Vue, Svelte, or vanilla web components.

## The rule

**Never render the brand name as styled text.** Always use a vector — the SVG for icon-only contexts, or the components from `logos.jsx` for any context that needs the wordmark.
