# Design Tokens

Single source of truth for every visual constant. Components consume these — no hardcoded hex/px in component CSS.

## Quickstart

```html
<!-- Load all tokens at once -->
<link rel="stylesheet" href="/ds/tokens/index.css">

<!-- Or pick one slice -->
<link rel="stylesheet" href="/ds/tokens/color.css">
```

Tokens then drop onto `:root`. Use them anywhere with `var(--token-name)`.

## Files

| File | Purpose |
|---|---|
| `index.css` | Imports everything in the correct order. Start here. |
| `color.css` | Paper, ink, line, crimson, accent ramps + dark-theme overrides |
| `type.css` | Font stacks, size scale, line heights, weights, tracking |
| `space.css` | 4-px scale, container widths, gutter, section rhythm |
| `radius.css` | Corner radii (none → pill) |
| `shadow.css` | Elevation shadows + focus ring + dark-theme overrides |
| `motion.css` | Durations, easings, prefers-reduced-motion overrides |
| `semantic.css` | Maps primitives → meaning (`--text-primary`, `--surface-card`). **Also** aliases legacy `--k-*` names. |
| `design-tokens.json` | Machine-readable mirror (W3C Design Tokens draft format). For Style Dictionary, Tokens Studio, Tailwind config generators, etc. |

## Three tiers

**Primitive tokens** are raw scales: `--color-ink-3`, `--space-4`, `--text-lg`. They have no meaning — they are just the palette and ramps.

**Semantic tokens** ARE the meaning: `--text-primary`, `--surface-card`, `--border-default`, `--action-primary`. They reference primitives. **Components consume semantic tokens.** Only fall back to primitives when there genuinely isn't a semantic name yet.

**Component-local tokens** are per-instance knobs: `--kb-bg`, `--kfc-bg-checked`. Override these on a single element to restyle one instance without specificity wars.

## Naming rules

- Primitives: `--<category>-<scale>` — e.g. `--color-ink-3`, `--space-8`, `--radius-md`.
- Semantic: `--<meaning>-<role>` — e.g. `--text-primary`, `--surface-card`, `--border-subtle`.
- Components: `--<component>-<part>-<state>` — e.g. `--kb-bg-hover`, `--kfc-border-checked`.
- Legacy `--k-*` names are aliases only. **Do not add new ones.** Every primitive component now consumes the new namespace.

## Dark theme

Toggled with `<html data-theme="dark">`. Color and shadow tokens override under that selector; all other tokens stay the same. Brand crimson lifts slightly in dark mode (`#7A1218` → `#8C2A2F`) so chip-scale fills stay legible on near-black surfaces.

## Editing

When you change a primitive (e.g. `--color-paper-1`), every component picks it up. That's the point. **Do not override a token at component level — fix it here.**

After editing a `*.css` file, regenerate `design-tokens.json` to keep the machine-readable mirror in sync.
