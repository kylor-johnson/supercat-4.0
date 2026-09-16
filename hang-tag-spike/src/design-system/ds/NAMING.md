# Class & Token Naming — quick reference

One page. Open this first when you don't recognize a class or token.

## Class prefixes

### Active — use in new web code

| Prefix | Meaning | Files |
|---|---|---|
| **`.kb`** + `.kb-{primary\|secondary}` + `.kb-{sm\|md\|lg}` | Button | `ds/primitives/button.css` |
| **`.kc`** + `.kc-pick` | Card / radio-card picker | `ds/primitives/card.css` |
| **`.kf-field`** + `.kf-field-label` + `.kf-field-hint` + `.kf-field-message` | Field wrapper (label + control + hint + error message) | `ds/primitives/field.css` |
| **`.kf-input`** + `.kf-{sm\|md\|lg}` | Text input | `ds/primitives/input.css` |
| **`.kf-check`** | Checkbox / radio (same primitive) | `ds/primitives/check.css` |
| **`.kf-switch`** | Toggle switch | `ds/primitives/switch.css` |
| **`.kf-date`** | Date input | `ds/primitives/date.css` |
| **`.ki`** + size + shape + tone variants | Icon container | `ds/primitives/icon.css` |
| **`.kdt`** | Data table | `ds/primitives/table.css` |
| **`.ktab`** + `.ktab-seg` | Tabs (incl. segmented control) | `ds/primitives/tabs.css` |
| **`.kmd`** | Modal (extends native `<dialog>`) | `ds/primitives/modal.css` |
| **`.vn`** | Marketing nav | `nav/marketing-nav.css` |
| **`.kfoot`** + `.kfoot-shell` | Marketing footer | `ds/primitives/footer.css` |

### Active — app surface only (skip in web-only workspaces)

| Prefix | Meaning | Files |
|---|---|---|
| **`.knav`** | App side nav (vertical left sidebar) | `ds/primitives/nav.{css,js,md,html}` |
| **`.kshell`** | App layout shell | composed in `app/*.html` pages |
| **`.kskel`** | Skeleton-load placeholder | `ds/primitives/skeleton.{css,js}` |

### Legacy — showcase-only, never propagate

| Prefix | Meaning | Where it lives |
|---|---|---|
| `.kit-*` | Master DS legacy chrome | `ds/tokens.css` (back-compat shim) |
| `.ds-*` | Master DS section chrome | `ds/master.css`, `ds/sections/*.css` |
| `.kbg` | Legacy badge | `ds/tokens.css` demo |
| `.kt-*` | Legacy tabs (predecessor of `.ktab`) | `ds/tokens.css` demo |

**Use in new code:** anything from the "Active" tables above. Never invent parallel Tailwind utilities (`text-white`, `bg-gray-900`, etc.) for the same purpose. Never rename these classes.

## Primitive components — the framework-agnostic API

```html
<!-- Button -->
<button class="kb kb-md kb-primary">Save changes</button>

<!-- Text input -->
<input class="kf-input kf-md" type="text" />

<!-- Checkbox + radio (same primitive) -->
<label class="kf-check">
  <input type="checkbox" />
  <span class="kf-check-box"></span>
  <span class="kf-check-label">Email me product updates</span>
</label>

<!-- Toggle switch -->
<label class="kf-switch">
  <input type="checkbox" />
  <span class="kf-switch-track"><span class="kf-switch-thumb"></span></span>
  <span class="kf-switch-label">Auto-sync orders</span>
</label>

<!-- Field wrapper with inline error -->
<div class="kf-field" data-state="error">
  <label class="kf-field-label">Work email</label>
  <input class="kf-input kf-md" data-state="error" />
  <p class="kf-field-message">Please use your work email.</p>
</div>

<!-- Card -->
<article class="kc">
  <h3 class="kc-title">Title</h3>
  <p class="kc-copy">Body…</p>
</article>

<!-- Radio-card picker -->
<label class="kc kc-pick">
  <input type="radio" name="profile" value="..." />
  <h3 class="kc-pick-title">Option title</h3>
  <p class="kc-pick-copy">Short description.</p>
</label>

<!-- Tabs (segmented control variant) -->
<div class="ktab ktab-seg" role="tablist">
  <button class="ktab-item" role="tab" aria-selected="true">Base</button>
  <button class="ktab-item" role="tab" aria-selected="false">Upside</button>
</div>

<!-- Modal (native dialog) -->
<dialog class="kmd" data-context="calc">
  <div class="kmd-head">…</div>
  <div class="kmd-body">…</div>
</dialog>

<!-- Marketing nav (web component, sections mode) -->
<sc-marketing-nav sections='[{"label":"Calculator","href":"#calc"}]'></sc-marketing-nav>
```

Full reference: each primitive has a sibling `.md` doc — `ds/primitives/button.md`, `card.md`, `forms.md`, `modal.md`, `tabs.md`, `table.md`.

## Tokens — three tiers

```
Primitive   →   Semantic            →   Component-local
--color-*       --text-primary          --kb-bg
--space-*       --surface-card          --kf-border-focus
--text-*        --action-primary        --kfc-bg-checked
--radius-*      --status-danger         --kfs-bg-on
                --border-default
```

| Layer          | Example                | Use when                                            |
|----------------|------------------------|-----------------------------------------------------|
| Primitive      | `--color-crimson`      | No semantic name fits yet (rare)                    |
| **Semantic**   | `--text-primary`       | **Default — always reach here first**               |
| Component-local| `--kb-bg-hover`        | Per-instance override on a single element via `style="--kb-bg: hotpink"` |

**Color model:** brand colors are hex (`--color-crimson: #7A1218`, `--color-gold: #B97727`, etc.). Opacity blends and tints use `color-mix(in oklch, ...)` for perceptual uniformity. Dark theme toggles via `[data-theme="dark"]` on `<html>` — NOT a `.dark` class.

Legacy `--k-*` names (`--k-ink`, `--k-paper`, `--k-crimson`) still resolve as back-compat aliases. **Do not author new code with them.**

## Files at a glance

```
ds/
├── NAMING.md         ← you are here
├── tokens.css        ← LEGACY back-compat shim — DO NOT IMPORT in new code
├── tokens/           ← ★ canonical token source
│   ├── index.css     ← load this in new pages
│   ├── color.css     ← brand colors (hex) + ink/cream/border ramps
│   ├── type.css      ← Geist + Geist Mono @import + scale
│   ├── space.css
│   ├── radius.css
│   ├── shadow.css
│   ├── motion.css
│   ├── semantic.css  ← --text-*, --surface-*, --action-*, --status-*
│   ├── design-tokens.json   ← machine-readable mirror
│   └── README.md     ← token contract in detail
└── primitives/       ← ★ canonical component source
    ├── button.{css,js,md,html}     ← .kb
    ├── card.{css,md,html}          ← .kc, .kc-pick
    ├── field.css                   ← .kf-field
    ├── input.{css,js}              ← .kf-input
    ├── check.css                   ← .kf-check
    ├── switch.css                  ← .kf-switch
    ├── date.{css,js}               ← .kf-date
    ├── forms.{md,html}             ← forms reference
    ├── icon.{css,md,html}          ← .ki
    ├── table.{css,md,html}         ← .kdt
    ├── tabs.{css,js,md,html}       ← .ktab, .ktab-seg
    ├── modal.{css,js,html}         ← .kmd
    ├── footer.css                  ← .kfoot
    ├── nav.{css,js,md,html}        ← .knav (APP sidebar — skip in web-only)
    └── skeleton.{css,js}           ← .kskel (APP — skip in web-only)
```

## In a hurry? Decision tree

```
Need a button?            →  <button class="kb kb-md kb-primary">
Need a card?              →  <article class="kc">…</article>
Need a radio-card picker? →  <label class="kc kc-pick"><input type="radio">…</label>
Need a text input?        →  <input class="kf-input kf-md">
Need a field+label+error? →  <div class="kf-field" data-state="error">…</div>
Need a checkbox/radio?    →  <label class="kf-check">…</label>
Need a toggle?            →  <label class="kf-switch">…</label>
Need a date picker?       →  <input class="kf-input kf-md kf-date">
Need an icon?             →  <span class="ki ki-md"><svg>…</svg></span>
Need a table?             →  <table class="kdt">…</table>
Need tabs?                →  <div class="ktab" role="tablist">…</div>
Need a segmented control? →  <div class="ktab ktab-seg" role="tablist">…</div>
Need a modal?             →  <dialog class="kmd">…</dialog>
Need a marketing nav?     →  <sc-marketing-nav> (web component)
Need a marketing footer?  →  <footer class="kfoot">…</footer>
Need a color?             →  var(--text-primary), var(--surface-card),
                             var(--action-primary), var(--border-default)
Need a space?             →  var(--space-3), var(--space-6), etc.
```

That's the system. Web marketing first; app primitives (`.knav`, `.kshell`, `.kskel`) live in this same folder but are out of scope for web-only workspaces.
