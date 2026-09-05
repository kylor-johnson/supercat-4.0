# Nav

This folder holds **marketing-site navigation** as native web components. The app-surface side nav lives separately in `ds/primitives/nav.*` (the `.knav` primitive).

## `marketing-nav.{css,js}` — the canonical marketing nav

A native custom element (`<sc-marketing-nav>`) that renders the dark glass pill header: logo, section links or mega menus, theme toggle, primary CTA. Use on any web marketing page.

Two modes:

- **Cross-site mode** (default) — renders the mega-menu structure for portal / app / docs / marketing links.
- **Sections mode** — pass `sections='[{label, href, current}]'` to render in-page section anchors instead. Used by `marketing/maxroi.html`.

Includes a **self-locating path resolver**: each script detects its own URL via `document.currentScript`, computes `DS_ROOT`, and rewrites absolute hrefs at render time. Works under `file://`, any localhost subpath, or a production root with zero per-page config.

```html
<link rel="stylesheet" href="/nav/marketing-nav.css">
<script src="/nav/marketing-nav.js" defer></script>

<sc-marketing-nav
  sections='[
    {"label":"Calculator","href":"#calc"},
    {"label":"Why it works","href":"#drivers","current":true}
  ]'
></sc-marketing-nav>
```

## `app-sidebar.{css,js}` — APP SURFACE ONLY

The `<sc-app-sidebar>` custom element wraps the `.knav` primitive (`ds/primitives/nav.*`) for app surfaces — Dashboard, Orders, Settings, etc. **Skip in web-only workspaces.**

## Rule

Every public web page mounts `<sc-marketing-nav>`. Never type a custom marketing nav from scratch — extend via the `sections` prop.
