# Button — `.kb`

> **Source of truth.** This is the canonical button primitive for the
> entire SuperCat system. Production apps, prototypes, framework
> integrations, and AI-generated code all use `.kb`. The Master DS
> showcase in `ds/sections/06-buttons.jsx` consumes the same primitive
> directly — there is no legacy `.ds-btn` shim anymore.

Framework-agnostic button primitive. Works with React, Vue, Svelte,
plain HTML — any DOM the browser renders. Authors compose classes;
state is driven by `data-*` attributes.

## Quickstart

```html
<link rel="stylesheet" href="/ds/tokens/index.css">
<link rel="stylesheet" href="/ds/primitives/button.css">
<script src="/ds/primitives/button.js" defer></script>

<button class="kb kb-primary">Save changes</button>
<!-- size is optional — defaults to kb-xl (52px). Override with kb-sm / kb-md / kb-lg. -->
```

`button.js` is **optional** — when loaded, it upgrades `[data-loading]`
to a premium orbiting comet ring around the button. Without the script,
buttons fall back to a classic CSS-only spinner inside the button.
Both render the same `data-loading` attribute, so you can ship the
fallback alone if you want zero JS.

## API

### Required classes

Every button needs `kb` + a variant. A size class is **optional** —
omitting it gives you the chunky `kb-xl` default suited to most web
CTAs and form actions.

| Slot    | Classes                                                                  |
|---------|--------------------------------------------------------------------------|
| Base    | `kb`                                                                     |
| Size    | `kb-sm` · `kb-md` · `kb-lg` · `kb-xl` (★ default)                        |
| Variant | `kb-primary` · `kb-accent` · `kb-secondary` · `kb-ghost` · `kb-danger` · `kb-link` · `kb-link-grow` |

**Sizes at a glance**

| Class    | Height | Padding   | Font | Use                                              |
|----------|--------|-----------|------|--------------------------------------------------|
| `kb-sm`  | ~26px  | 5×14px   | 11px | Toolbars, table-row actions, dense inline        |
| `kb-md`  | ~32px  | 7×18px   | 12px | Compact forms, modal footers                     |
| `kb-lg`  | ~36px  | 9×22px   | 13px | Prominent inline CTAs                            |
| `kb-xl` ★ | ~52px | 14×28px  | 13px | **Default.** Marketing hero CTAs, signup, form-row CTAs (matches input height) |

Size classes don't apply to `.kb-link` / `.kb-link-grow` (link variants
size themselves).

### Modifiers

| Class      | Effect                                       |
|------------|----------------------------------------------|
| `kb-icon`  | Square, icon-only. Pair with `aria-label`.   |

### States

| Trigger                              | Behaviour                          |
|--------------------------------------|------------------------------------|
| `:hover`                             | Variant-specific bg / fg shift     |
| `:focus-visible`                     | Crimson 35% glow ring              |
| `:active`                            | `scale(0.97)` press                |
| `disabled` attr (button)             | 40% opacity, not interactive       |
| `class="disabled"` or `aria-disabled="true"` | Same, works on `<a>`       |
| `data-loading` attr                  | Orbiting comet ring around button  |
| `data-success` attr                  | Ring closes, text → animated check |

`data-loading` and `data-success` together animate a graceful close:
remove `data-loading` and add `data-success` in the same tick → the
ring forms into a full ring, then text swaps for a check.

## Examples

### Variants

```html
<button class="kb kb-primary">Save changes</button>            <!-- default xl -->
<button class="kb kb-xl kb-accent">Continue</button>           <!-- explicit xl -->
<button class="kb kb-md kb-secondary">Cancel</button>
<button class="kb kb-sm kb-ghost">Skip</button>
<button class="kb kb-lg kb-danger">Delete</button>
<button class="kb kb-link">Read the docs</button>
<button class="kb kb-link-grow">Browse catalog</button>
```

### Icons

Right-side icons get an animated nudge on hover. Mark them
`class="arr-svg"` so the slide is enabled. Left-side icons get a tiny
scale instead.

```html
<button class="kb kb-md kb-primary">
  Continue
  <svg class="arr-svg" viewBox="0 0 16 16">
    <path d="M3 8h10M9 4l4 4-4 4"/>
  </svg>
</button>

<button class="kb kb-md kb-primary">
  <svg viewBox="0 0 16 16"><path d="M3 8l3.5 3.5L13 5"/></svg>
  Confirm
</button>

<button class="kb kb-md kb-secondary kb-icon" aria-label="Close">
  <svg viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8"/></svg>
</button>
```

### Loading + success flow

```js
async function save(btn) {
  btn.setAttribute('data-loading', '');
  try {
    await api.save();
    btn.removeAttribute('data-loading');
    btn.setAttribute('data-success', '');
    setTimeout(() => btn.removeAttribute('data-success'), 2000);
  } catch (e) {
    btn.removeAttribute('data-loading');
  }
}
```

Pure-CSS rendering of an idle "loading-shaped" button (e.g. SSR before
JS hydrates):

```html
<button class="kb kb-md kb-primary" data-loading>Saving</button>
```

The script promotes it to an animated orbit on mount.

### React

```jsx
<button
  className={`kb kb-md kb-primary`}
  {...(loading && { 'data-loading': '' })}
  {...(success && { 'data-success': '' })}
  onClick={save}
>
  Save changes
</button>
```

### Vue

```vue
<button
  class="kb kb-md kb-primary"
  :data-loading="loading || null"
  :data-success="success || null"
  @click="save"
>Save changes</button>
```

### Anchor as button

```html
<a class="kb kb-md kb-secondary" href="/cancel">Cancel</a>
<a class="kb kb-md kb-secondary disabled" aria-disabled="true">Cancel</a>
```

## Customising

Per-instance overrides — set any of the component-local custom
properties via `style`:

```html
<button class="kb kb-md kb-primary" style="--kb-bg: hotpink; --kb-bg-hover: deeppink">
  One-off
</button>
```

Available custom properties:

| Property            | Purpose                              |
|---------------------|--------------------------------------|
| `--kb-bg`           | Idle background                      |
| `--kb-fg`           | Idle text color                      |
| `--kb-border`       | Idle border color                    |
| `--kb-bg-hover`     | Hover background                     |
| `--kb-fg-hover`     | Hover text color                     |
| `--kb-border-hover` | Hover border color                   |
| `--kb-ring-color`   | Loading orbit + success ring color   |
| `--kb-focus-ring`   | `:focus-visible` glow color          |

Don't write CSS that re-targets `.kb-primary` etc. — just override
properties on a single instance, or define a new variant class that
sets the same custom properties.

## Theme

Buttons respond to `[data-theme="dark"]` on `<html>` automatically.
The danger variant uses a brighter crimson in dark mode for contrast;
all other variants flow through token swaps.

## Accessibility

- Always provide visible text OR `aria-label` (icon-only).
- `[data-loading]` automatically gets `aria-busy="true"` from the script.
- For status announcements after success, pair the button with a
  separate `aria-live="polite"` region — the visual check isn't
  announced by itself.
- Respects `prefers-reduced-motion`: orbit + check + skeleton all
  disable their animations.

## Related

- `.ds-skel` — skeleton placeholder utility (ships in same stylesheet).
- Tokens — `/ds/tokens/index.css` provides every variable consumed here.
