# Framework integration guide

## Architecture in one line

**One brand, two products, one foundation.** The SuperCat Design System ships shared tokens + primitives in `ds/tokens/` and `ds/primitives/`, and they power **two distinct surface families**: a **Web Marketing** website (editorial, premium, restrained) at `index.html` + `ds/reference.html`, and a **Web / iPad App** (utilitarian, data-dense, fast) at `app/*.html`. Both products consume the foundation; neither product depends on the other. Read [`SURFACES.md`](SURFACES.md) for the architecture diagram + file-by-file map.

The SuperCat DS is **framework-agnostic by design**. Primitives ship as CSS classes that decorate native HTML elements — no React, Vue, or build tool is required to use them. This guide shows how to wire the system into common stacks.

---

## What you load

Three options for getting tokens + primitives into a project. Pick one.

### A — Direct file links (simplest)
```html
<link rel="stylesheet" href="/ds/tokens/index.css" />
<link rel="stylesheet" href="/ds/primitives/button.css" />
<link rel="stylesheet" href="/ds/primitives/input.css" />
<!-- …each primitive you need… -->
<script src="/ds/primitives/tabs.js" defer></script>
<script src="/ds/primitives/skeleton.js" defer></script>
```

### B — Concatenated single bundle (recommended for prod)
The `scripts/build.sh` (when re-enabled) concatenates everything into `ds/dist/ds.css` + `ds/dist/ds.js`. Link one stylesheet + one script.

### C — Import via npm / Vite / Webpack
Treat the `design-system/` directory as a local package. From a React/Vue/Svelte/Next/etc. project:
```js
// In your entry file
import 'supercat-ds/ds/tokens/index.css';
import 'supercat-ds/ds/primitives/button.css';
import 'supercat-ds/ds/primitives/input.css';
// …
```
Resolve the path however your bundler likes — alias it in `tsconfig.json` / `vite.config.js` / `webpack.config.js`.

---

## ★ Logo — vector only, never typed text

The SuperCat brand is the **double-wave mark**. Never render it as styled HTML text (`<h1>SuperCat</h1>`, etc.).

**Source of truth:** [`assets/supercat-mark.svg`](../assets/supercat-mark.svg) — `viewBox="0 0 41 28"`, paths fill via `currentColor`.

### As a React component

```jsx
export function SuperCatMark({ size = 28, color = 'var(--color-gold)', label = 'SuperCat' }) {
  return (
    <svg width={size * 41 / 28} height={size} viewBox="0 0 41 28" aria-label={label} role="img" style={{ color }}>
      <path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="currentColor"/>
      <path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="currentColor"/>
    </svg>
  );
}
```

### As an SVG sprite (any framework)

Inline the symbol once near the top of the document body, then reference it anywhere:

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <symbol id="i-mark" viewBox="0 0 41 28">
      <path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="currentColor"/>
      <path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="currentColor"/>
    </symbol>
  </defs>
</svg>

<a href="/" style="color: var(--color-gold)">
  <svg viewBox="0 0 41 28" width="41" height="28" aria-label="SuperCat"><use href="#i-mark"/></svg>
</a>
```

### Asset variants

| Use case | Reference |
|---|---|
| Default brand (gold mark on cream) | `color: var(--color-gold)` |
| Inverted (cream mark on dark glass) | `color: var(--color-cream)` |
| Knock-out on solid color | `color: currentColor` of parent |
| External asset (img tag, fav, social) | `assets/supercat-mark.svg` |

**Do not:**
- Render the brand as text (`<h1>SuperCat</h1>`).
- Apply crimson to the mark (crimson is for primary actions).
- Distort the aspect ratio — keep `width / height = 41 / 28`.
- Embed PNG fallbacks; SVG with `currentColor` covers every contrast case.

---

## React

Classes are plain strings. Tokens are CSS custom properties — you can override them inline if you need a one-off skin.

```jsx
// Button
<button className="kb kb-md kb-primary" onClick={onClick}>
  Save changes
</button>

// Input
<label className="kf-field">
  <span className="kf-field-label">Display name</span>
  <input className="kf-input kf-md" type="text" value={value} onChange={onChange} />
</label>

// Toggle — real <input type="checkbox"> works with controlled state
<label className="kf-switch">
  <input type="checkbox" checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />
  <span className="kf-switch-track">
    <span className="kf-switch-thumb"></span>
  </span>
</label>

// Skeleton-loaded card
<article
  className="kc"
  data-loadable
  aria-busy={isLoading}
>
  <div data-skel>
    <span className="kskel kskel-line" style={{ '--w': '60%' }}></span>
    <span className="kskel kskel-line" style={{ '--w': '80%' }}></span>
  </div>
  <div data-real>{data && <ProductCard data={data} />}</div>
</article>
```

Works seamlessly with **React Hook Form**, **Formik**, **TanStack Query** — primitives don't intercept events or wrap inputs.

For Tailwind users: the DS tokens are CSS custom properties. Drop them into `tailwind.config.js`:
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        crimson: 'var(--color-crimson)',
        cream: 'var(--color-cream)',
        moss: 'var(--color-moss)',
        // …
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        mono: 'var(--font-mono)',
      },
    },
  },
};
```

---

## Vue (3.x)

Use `class` attribute. Inputs work with `v-model`.

```vue
<template>
  <label class="kf-field">
    <span class="kf-field-label">Display name</span>
    <input class="kf-input kf-md" type="text" v-model="name" />
  </label>

  <button class="kb kb-md kb-primary" @click="save">Save</button>
</template>
```

Skeleton loading via `:aria-busy` binding:
```vue
<article class="kc" data-loadable :aria-busy="isLoading">
  <div data-skel>
    <span class="kskel kskel-line" :style="{ '--w': '60%' }"></span>
  </div>
  <div data-real>{{ data.title }}</div>
</article>
```

---

## Angular

```html
<label class="kf-field">
  <span class="kf-field-label">Display name</span>
  <input class="kf-input kf-md" type="text" [(ngModel)]="name" />
</label>

<button class="kb kb-md kb-primary" (click)="save()">Save</button>

<article class="kc" data-loadable [attr.aria-busy]="isLoading">
  <div data-skel>
    <span class="kskel kskel-line" style="--w: 60%"></span>
  </div>
  <div data-real>{{ data.title }}</div>
</article>
```

---

## Svelte

```svelte
<label class="kf-field">
  <span class="kf-field-label">Display name</span>
  <input class="kf-input kf-md" type="text" bind:value={name} />
</label>

<button class="kb kb-md kb-primary" on:click={save}>Save</button>

<article class="kc" data-loadable aria-busy={isLoading}>
  <div data-skel>
    <span class="kskel kskel-line" style="--w: 60%"></span>
  </div>
  <div data-real>{data.title}</div>
</article>
```

---

## What this system promises

- **No JS framework lock-in.** Primitives are pure CSS — the few that ship JS (`button.js`, `input.js`, `tabs.js`, `skeleton.js`) are vanilla controllers attached via class hooks (`data-reload`, `data-loadable`, `aria-selected`) and can be replaced or removed without affecting the visual layer.
- **Real form elements.** `<button>`, `<input>`, `<select>`, `<textarea>` — not custom elements. Works with every form library out there.
- **Tokens as CSS custom properties.** Override at any DOM scope: `<html data-theme="dark">`, `<div style="--kb-bg: tomato">`, etc.
- **Light + dark mode.** Set `<html data-theme="dark">`. Every primitive flips through the same semantic-token bridge.
- **Reduced motion respected.** Every animation (tabs slide, skeleton shimmer, button hover) honors `prefers-reduced-motion: reduce`.

---

## LLM-friendliness

The system was designed to be parseable by LLMs without prior context. **First fact an agent should know:** _one brand, two products, one foundation_. The shared foundation lives at `ds/tokens/` + `ds/primitives/`. The two products live at `index.html` + `ds/reference.html` + `ds/sections/` + `nav/` (Web Marketing) and `app/*.html` (Web / iPad App). Class prefixes signal which product owns the rule: `.ds-*` · `.vn-*` · `.mn-*` = Marketing; `.k*` family (`.kb`, `.kf-*`, `.kc`, `.kdt`, `.knav`, `.ktab`, `.kshell`, `.kskel`, `.ki`) = foundation, with `.knav`, `.kshell`, `.kskel` only appearing inside App pages.

Beyond that:

- **Predictable class naming.** `.k{namespace}-{element}`. `kb` = kit button, `kf-` = kit form, `kc-` = kit card, `kdt-` = kit data table, `knav-` = kit nav, `ktab-` = kit tab, `kshell-` = kit shell, `kskel-` = kit skeleton, `ki` = kit icon. The first character (`k`) marks the App-kit family; `.ds-*` marks marketing-section chrome. See `SURFACES.md`.
- **Semantic tokens with meaning embedded.** `--text-primary`, `--text-on-crimson`, `--surface-card`, `--action-primary`, `--status-success`, `--border-default`. An LLM can infer usage from the name.
- **Co-located docs.** Each primitive ships a `.md` file alongside its `.css`. `button.md`, `forms.md`, `card.md`, etc. — point an LLM at the primitive folder and it can answer "how do I make a destructive button?"
- **JSON token mirror.** `ds/tokens/design-tokens.json` exposes the primitive + semantic layers in W3C Design Tokens draft format. Works with Style Dictionary, Figma Tokens, and any tool that consumes that schema.
- **No build step required.** An LLM can read the source CSS, see what tokens a class consumes, and predict the rendered output from the token values in `ds/tokens/color.css`.

---

## Quick contract summary for an agent or LLM

1. Want to render a primary CTA button: `<button class="kb kb-md kb-primary">…</button>`
2. Want a destructive button: `<button class="kb kb-md kb-secondary" style="color: var(--text-crimson); border-color: color-mix(in oklch, var(--color-crimson) 35%, var(--border-default))">…</button>` — or extend with a `.kb-danger` variant if your project standardizes one.
3. Want a card: `<article class="kc"><header class="kc-head"><h3 class="kc-title">…</h3></header><div class="kc-body">…</div></article>`
4. Want a data table: `<table class="kdt">…</table>` — sortable headers with `aria-sort`.
5. Want a skeleton load state: wrap with `<div data-loadable aria-busy="true"><div data-skel>…</div><div data-real>…</div></div>` — flip `aria-busy` to `"false"` when fetch resolves.
6. Want dark mode: `<html data-theme="dark">`.
7. Want an App shell page: copy the structure of `app/orders.html` — `<div class="kshell"><aside class="knav knav-floating">…</aside><div class="kshell-main"><header class="kshell-top">…</header><main class="kshell-content">…</main></div></div>`.
8. Want a marketing landing page: model on `index.html` — page-rows, dashed gridlines, ribbon, editorial chapter layout. Use `nav/nav.css` for the top mega-menu.
