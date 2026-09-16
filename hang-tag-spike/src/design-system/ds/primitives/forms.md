# SuperCat DS — Forms

Form primitives. Pure CSS, framework-agnostic, no required JS.

```html
<link rel="stylesheet" href="/ds/tokens/index.css" />
<link rel="stylesheet" href="/ds/primitives/input.css" />
<link rel="stylesheet" href="/ds/primitives/check.css" />
<link rel="stylesheet" href="/ds/primitives/switch.css" />
<link rel="stylesheet" href="/ds/primitives/field.css" />
```

Each primitive is a class layer that decorates **standard HTML form elements** (`<input>`, `<select>`, `<textarea>`). The browser's native form behavior is preserved. There is no React/Vue/Svelte coupling; each primitive works identically in any framework.

---

## Why this shape

- **Real `<input>` always present.** Form data, label-click semantics, screen readers, password managers, autofill — all work without glue code.
- **Class layer, not component layer.** Apply `.kf-input` to an `<input>`, get the look. Wrap in `.kf-input-wrap` only when you need slot affordances (lead icon, trailing button).
- **Attribute-driven states.** `data-state="error|warn|success"`, `disabled`, `readonly`, `:checked`, `:indeterminate`. No JS state machines required.
- **Component-local custom properties.** Override per-instance (`style="--kfc-bg-checked: var(--color-gold);"`) without escalating specificity.
- **Tokens, not hex.** Every color/space/motion value resolves through semantic tokens, so dark theme + brand re-skin require no component changes.

---

## `.kf-input` — text-style fields

Single class. Works on `<input>` (every text-style type), `<select>`, `<textarea>`.

### Sizes

```html
<input class="kf-input kf-sm" type="text" />  <!-- 32px -->
<input class="kf-input kf-md" type="text" />  <!-- 40px (default) -->
<input class="kf-input kf-lg" type="text" />  <!-- 48px touch-friendly -->
```

### States

| State        | How                                              |
|--------------|--------------------------------------------------|
| Default      | (none)                                           |
| Hover        | `:hover` — automatic                             |
| Focus        | `:focus` — automatic with ring                   |
| Disabled     | `disabled` attribute                             |
| Read-only    | `readonly` attribute                             |
| Error        | `data-state="error"`                             |
| Warning      | `data-state="warn"`                              |
| Success      | `data-state="success"`                           |
| Force-state (showcase only) | `data-force="hover"` / `data-force="focus"` |

### Slots — `.kf-input-wrap`

Wrap an input in `.kf-input-wrap` to enable lead/trail slots:

```html
<!-- Lead icon (e.g. search) -->
<div class="kf-input-wrap kf-md has-lead">
  <span class="kf-input-lead"><svg>…</svg></span>
  <input class="kf-input kf-md" type="search" />
</div>

<!-- Trailing text button (e.g. password Show) -->
<div class="kf-input-wrap kf-md has-trail">
  <input class="kf-input kf-md" type="password" />
  <button type="button" class="kf-input-trail">Show</button>
</div>

<!-- Trailing icon button (e.g. clear) -->
<div class="kf-input-wrap kf-md has-trail">
  <input class="kf-input kf-md" type="text" />
  <button type="button" class="kf-input-trail-icon" aria-label="Clear"><svg>×</svg></button>
</div>

<!-- Number stepper -->
<div class="kf-input-wrap kf-md has-trail">
  <input class="kf-input kf-md" type="number" />
  <span class="kf-input-stepper">
    <button type="button">+</button>
    <button type="button">−</button>
  </span>
</div>
```

The `.has-lead` / `.has-trail` classes adjust the input padding to clear the slots.

### Custom properties

Override per-instance to re-skin a single field:

```css
--kf-bg            background
--kf-fg            text color
--kf-border        idle border
--kf-border-hover  hover border
--kf-border-focus  focus border
--kf-ring-color    focus ring tint
--kf-h             height (overrides size class)
--kf-pad-x         horizontal padding
--kf-font-size     text size
```

---

## `.kf-check` — Checkbox + radio

**Same class for both.** The underlying `<input type>` decides shape (square vs circle).

```html
<!-- Checkbox -->
<label class="kf-check">
  <input type="checkbox" />
  <span class="kf-check-box"></span>
  <span class="kf-check-label">Email me product updates</span>
</label>

<!-- Radio -->
<label class="kf-check">
  <input type="radio" name="tier" value="1" />
  <span class="kf-check-box"></span>
  <span class="kf-check-label">Tier 1 · MAP</span>
</label>
```

The structural triple — `input` + `.kf-check-box` + `.kf-check-label` — is required. The real `<input>` is visually hidden but present for forms and a11y; `.kf-check-box` is the rendered chip; CSS sibling selectors drive its appearance from `:checked`/`:indeterminate`.

### Sizes

```html
<label class="kf-check kf-sm">…</label>  <!-- 14px -->
<label class="kf-check kf-md">…</label>  <!-- 18px (default) -->
<label class="kf-check kf-lg">…</label>  <!-- 22px -->
```

### Indeterminate

The `:indeterminate` pseudo-class is set via JS — it has no HTML attribute equivalent. One line:

```js
checkbox.indeterminate = true;
```

### Hint text — second-line context

```html
<label class="kf-check">
  <input type="checkbox" />
  <span class="kf-check-box"></span>
  <span>
    <span class="kf-check-label">Auto-sync to Highpoint</span>
    <span class="kf-check-hint">Sends order data to the rep's calendar within 5 minutes.</span>
  </span>
</label>
```

### Group layouts

```html
<div class="kf-check-stack">…</div>  <!-- vertical, gap-3 -->
<div class="kf-check-row">…</div>    <!-- horizontal, gap-5, wraps -->
```

### Custom properties

```css
--kfc-size           chip size
--kfc-bg             chip bg (unchecked)
--kfc-bg-checked     chip bg (checked)
--kfc-border         chip border
--kfc-border-checked checked border
--kfc-fg             check/dot color
--kfc-ring-color     focus ring tint
```

---

## `.kf-switch` — toggle switch

Wraps a `<input type="checkbox">`. Same form semantics; different look.

```html
<label class="kf-switch">
  <input type="checkbox" />
  <span class="kf-switch-track">
    <span class="kf-switch-thumb"></span>
  </span>
  <span class="kf-switch-label">Auto-sync orders</span>
</label>
```

The triple — `input` + `.kf-switch-track > .kf-switch-thumb` + `.kf-switch-label` — is required.

### Sizes

```html
<label class="kf-switch kf-sm">…</label>  <!-- 28×16, thumb 12 -->
<label class="kf-switch kf-md">…</label>  <!-- 36×20, thumb 14 (default) -->
<label class="kf-switch kf-lg">…</label>  <!-- 44×26, thumb 20 -->
```

### Custom properties

```css
--kfs-w            track width
--kfs-h            track height
--kfs-thumb        thumb size
--kfs-pad          track inset
--kfs-bg-off       track bg — off
--kfs-bg-on        track bg — on
--kfs-thumb-bg     thumb bg
--kfs-ring-color   focus ring
```

---

## `.kf-field` — Field wrapper

Pairs label + control + hint + validation message. **Optional but recommended** — gives consistent vertical rhythm and a single hook for `data-state`.

```html
<div class="kf-field">
  <label class="kf-field-label" for="po">
    PO number <span class="kf-field-optional">Optional</span>
  </label>
  <input class="kf-input kf-md" id="po" type="text" />
  <p class="kf-field-hint">Auto-generated if blank.</p>
</div>
```

### Required indicator

```html
<label class="kf-field-label" for="x">
  Buyer email <span class="kf-field-required" aria-hidden="true">*</span>
</label>
```

### Validation

Set `data-state` on the field; tone propagates to label + message:

```html
<div class="kf-field" data-state="error">
  <label class="kf-field-label" for="qty">Quantity</label>
  <input class="kf-input kf-md" id="qty" data-state="error" />
  <p class="kf-field-message">Maximum order qty is 250.</p>
</div>
```

`data-state` values: `error` (crimson) · `warn` (gold) · `success` (green).

### Hint + counter row

```html
<div class="kf-field-meta">
  <p class="kf-field-hint">Visible to dealer + warehouse.</p>
  <span class="kf-field-counter">142 / 500</span>
</div>
```

The counter accepts its own `data-state` for at-limit warnings:

```html
<span class="kf-field-counter" data-state="warn">485 / 500</span>
```

### Inline layout

```html
<div class="kf-field kf-field-inline">
  <label class="kf-field-label">Region</label>
  <select class="kf-input kf-md">…</select>
</div>
```

### Fieldset

For radio/checkbox groups, use semantic `<fieldset>` + `<legend>` styled to match labels:

```html
<fieldset class="kf-fieldset">
  <legend>Pricing tier</legend>
  <div class="kf-check-stack">
    <label class="kf-check">…</label>
    <label class="kf-check">…</label>
  </div>
</fieldset>
```

---

## Framework cookbook

The class API is identical in every framework. JSX uses `className`; everything else is the same HTML.

### React

```jsx
function PoField({ value, onChange, error }) {
  return (
    <div className="kf-field" data-state={error ? "error" : undefined}>
      <label className="kf-field-label" htmlFor="po">PO number</label>
      <input
        id="po"
        className="kf-input kf-md"
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        data-state={error ? "error" : undefined}
      />
      {error && <p className="kf-field-message">{error}</p>}
    </div>
  );
}
```

### Vue

```vue
<template>
  <div class="kf-field" :data-state="error ? 'error' : undefined">
    <label class="kf-field-label" for="po">PO number</label>
    <input
      id="po"
      class="kf-input kf-md"
      type="text"
      v-model="value"
      :data-state="error ? 'error' : undefined"
    />
    <p v-if="error" class="kf-field-message">{{ error }}</p>
  </div>
</template>
```

### Svelte

```svelte
<div class="kf-field" data-state={error ? 'error' : undefined}>
  <label class="kf-field-label" for="po">PO number</label>
  <input
    id="po"
    class="kf-input kf-md"
    type="text"
    bind:value
    data-state={error ? 'error' : undefined}
  />
  {#if error}<p class="kf-field-message">{error}</p>{/if}
</div>
```

### Vanilla

Identical to the HTML examples above. Add an event listener if you need behavior:

```html
<form id="order-form">
  <div class="kf-field">
    <label class="kf-field-label" for="po">PO number</label>
    <input class="kf-input kf-md" id="po" name="po" type="text" />
    <p class="kf-field-message" hidden></p>
  </div>
</form>
<script>
  const form = document.getElementById('order-form');
  form.addEventListener('submit', e => {
    /* validate however you like, set data-state on the field + message */
  });
</script>
```

---

## Accessibility

- **Always pair `<label for>` with input `id`.** Every example does this. Click-on-label-to-toggle is browser-native; do not reinvent.
- **`aria-hidden="true"` on `*`** — the asterisk is decorative; the *required* attribute (or `aria-required="true"`) is the source of truth for screen readers.
- **`<button>` inside `.kf-input-wrap`** — always include `type="button"` to prevent accidental form submission.
- **Focus rings** — every focusable primitive ships a 3px focus-visible ring tinted to its state. Do not disable.
- **Reduced motion** — switch thumb, check glyph, and input transitions all respect `prefers-reduced-motion: reduce`.

---

## Tokens consumed

Every primitive resolves through semantic tokens defined in `/ds/tokens/`. To re-skin globally, change the tokens. To re-skin one instance, override component-local custom properties:

```html
<input class="kf-input kf-md" style="--kf-border-focus: var(--color-gold); --kf-ring-color: var(--color-gold);" />
```

| Used by | Tokens |
|---|---|
| `.kf-input` | `--surface-card`, `--text-primary`, `--border-default`, `--text-muted`, `--text-faint`, `--text-crimson`, `--color-gold`, `--status-success`, `--surface-3`, `--space-*`, `--text-*`, `--radius-sm`, `--duration-*`, `--ease-*` |
| `.kf-check` | `--surface-card`, `--text-primary`, `--text-body`, `--text-muted`, `--text-faint`, `--text-crimson`, `--border-default`, `--surface-3`, `--space-*`, `--text-*`, `--radius-xs`, `--font-mono`, `--font-sans` |
| `.kf-switch` | `--surface-card`, `--text-primary`, `--text-body`, `--text-faint`, `--text-crimson`, `--border-strong`, `--space-*`, `--text-*`, `--font-mono`, `--font-sans` |
| `.kf-field` | `--text-muted`, `--text-faint`, `--text-crimson`, `--color-gold`, `--status-success`, `--space-*`, `--text-*`, `--font-mono`, `--font-sans` |

---

## What's not here yet

- **`.kf-radio-group`** — a card-style radio group (radio rendered as a selectable card, not a chip). Coming alongside the patterns layer.
- **Combobox / autocomplete** — needs a popover primitive first.
- **File upload** — needs drag-and-drop affordance + file-list display. Component, not primitive.
- **Slider / range** — design pending.

For now, native `<input type="range">` works styled with system defaults; pair with `.kf-field` for label + hint.
