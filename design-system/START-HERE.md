# SuperCat Design System — Start here

## 1. Preview it (30 seconds)

**Easiest — local server (recommended):**

- **Mac:** double-click `preview-mac.command`. A terminal opens, the browser opens to the portal. Done.
- **Windows:** double-click `preview-windows.bat`. Same idea.

(If macOS warns "can't be opened because it is from an unidentified developer," right-click → Open → Open.)

**Alternative — no terminal at all:**

Double-click `index.html`. It opens in your browser via `file://`. Everything works including the nav, mega-menus, sign-in, dashboards, and the ROI page.

The portal lists every page. Click any card to jump in. Toggle dark mode with the moon/sun in the top-right.

---

## 2. What you're looking at

| Page | Where | What it shows |
|---|---|---|
| Portal | `index.html` | Index of everything below |
| Reference | `ds/reference.html` | Every primitive on one page — tokens, buttons, forms, cards, tables, tabs, nav, modal |
| MaxROI · 90-Day payback | `marketing/maxroi.html` | Live calculator + lead-magnet landing — editorial hero, real customer math, intent-aware modal |
| Dashboard | `app/dashboard.html` | Workspace home — metric tiles, charts (bar + line + donut, all interactive), tables |
| Orders | `app/orders.html` | Data-table screen — tabs, filters, sorting, pagination |
| Products | `app/products.html` | Card-grid product catalog |
| Settings | `app/settings.html` | Form-heavy admin — horizontal tabs + sticky save bar |
| Sign in | `app/signin.html` | Two-panel auth flow — editorial brand left, form right |

---

## 3. Use it in your own project

Two paths.

### Option A — Real app (React / Vue / Next / etc.)

1. Copy these folders into your project: `ds/tokens/`, `ds/primitives/`, `assets/`, `nav/`.
2. Import tokens once at app root: `import './ds/tokens/index.css';`
3. Import primitives à la carte: `import './ds/primitives/button.css';` etc.
4. Use real HTML with class names: `<button className="kb kb-md kb-primary">Save</button>`.
5. Logo is a vector — never type "SuperCat" as text. Use `assets/supercat-mark.svg`.
6. Dark mode: `<html data-theme="dark">`.

Full guide: `docs/FRAMEWORK-GUIDE.md`.

#### Lovable / React + Tailwind specifically

If you're using Lovable (or any Vite + React + Tailwind project):

**1. Put the design system in `src/design-system/`** — drop the entire `ds/`, `nav/`, `assets/` folders there.

**2. Wire tokens into `src/index.css`:**
```css
@import './design-system/ds/tokens/index.css';
@import './design-system/ds/primitives/button.css';
@import './design-system/ds/primitives/card.css';
@import './design-system/ds/primitives/input.css';
@import './design-system/ds/primitives/field.css';
@import './design-system/ds/primitives/check.css';
@import './design-system/ds/primitives/tabs.css';
@import './design-system/ds/primitives/modal.css';
@import './design-system/ds/primitives/footer.css';
@import './design-system/nav/marketing-nav.css';
/* …whichever primitives your page uses… */
```

**3. Extend `tailwind.config.ts` to expose tokens as Tailwind utilities** (so `bg-crimson`, `text-primary`, `p-space-4` work):
```ts
export default {
  theme: {
    extend: {
      colors: {
        crimson:  'var(--color-crimson)',
        gold:     'var(--color-gold)',
        clay:     'var(--color-clay)',
        cream:    'var(--color-cream)',
        moss:     'var(--color-moss)',
        ink:      'var(--text-primary)',
        body:     'var(--text-body)',
        muted:    'var(--text-muted)',
        surface:  'var(--surface-page)',
        card:     'var(--surface-card)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        mono: 'var(--font-mono)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
      },
    },
  },
}
```

**4. Load the nav + primitive JS controllers via `useEffect` once at app mount** (or import the script tags in `index.html`):
```tsx
useEffect(() => {
  // marketing-nav.js + tabs.js + input.js + modal.js
  // are vanilla — just include them in index.html with `defer`
}, []);
```
Easier: just add to `index.html`:
```html
<script type="module" src="/src/design-system/nav/marketing-nav.js" defer></script>
<script type="module" src="/src/design-system/ds/primitives/tabs.js" defer></script>
<script type="module" src="/src/design-system/ds/primitives/input.js" defer></script>
<script type="module" src="/src/design-system/ds/primitives/modal.js" defer></script>
```

**5. Use primitives + Tailwind together freely.** Class names from the DS work alongside Tailwind utilities:
```tsx
<button className="kb kb-md kb-primary">Save</button>
<article className="kc">
  <header className="kc-head">
    <h3 className="kc-title">Title</h3>
  </header>
  <div className="kc-body">Body</div>
</article>
```

**6. The nav as a React component** — `<sc-marketing-nav>` is a Web Component (custom element). React handles it natively. Just use it in JSX:
```tsx
<sc-marketing-nav
  current="roi"
  cta-href="#calculator"
  cta-label="Run mine"
  sections={JSON.stringify([
    {label: 'Calculator',  href: '#calculator'},
    {label: 'The math',    href: '#math'},
    {label: 'Take it with me', href: '#share'},
  ])}
/>
```
(React JSX needs the `sections` JSON as a string. Type with `declare namespace JSX { interface IntrinsicElements { 'sc-marketing-nav': any } }` if TypeScript complains.)

### Option B — Landing pages (Lovable, v0, plain HTML)

1. Link `ds/tokens/index.css` + `nav/marketing-nav.css` + the primitives you need.
2. Drop `<sc-marketing-nav></sc-marketing-nav>` at the top of `<body>` — it self-registers.
3. Copy the structure of `marketing/maxroi.html`.

---

## 4. The 30-second contract

- **One brand. Two products. One foundation.** Marketing (editorial) and App (utilitarian) share the same tokens + primitives.
- **Classes:** `.kb` = button · `.kf-*` = form · `.kc` = card · `.kdt` = data table · `.knav` = app sidebar · `.ktab` = tabs · `.kmd` = modal · `.kfoot` = footer · `.vn` = marketing nav.
- **Color roles (do not swap):** crimson = primary action. Gold = brand mark. Cream = paper. Clay = neutral. Moss = success.
- **Logo = SVG always.** Never `<h1>SuperCat</h1>`. The vector lives at `assets/supercat-mark.svg`.
- **Tokens are CSS custom properties** (`--color-crimson`, `--space-4`, `--radius-md` …) — override anywhere.
- **Dark mode:** `<html data-theme="dark">`.

---

## ★ Demo content vs. real implementation — READ BEFORE BUILDING

**Everything you see in this folder is DEMO content + the editorial visual system.** The dashboards, the  MaxROI · 90-Day payback copy, the orders, the marketing nav items — all of it is **placeholder content showing the style, layout patterns, and primitive vocabulary**. It is **NOT** the canonical content for any real product page.

When you (or any tool — Lovable, v0, Cursor) build a real page using this system:

**Keep:**
- The editorial energy — paper-warm cream, ink type, generous whitespace, hairline borders, mono numbers, crimson-for-primary-action.
- The primitive vocabulary — `.kb`, `.kc`, `.kf-*`, `.kfoot-*`, the eyebrow strip pattern, the hero composition, the stat strip rhythm.
- The hard rules — logo as SVG, no custom colors, no primitive base-style overrides, color roles intact.

**Adapt:**
- Section count + order — based on what the real page actually needs to communicate.
- Nav items in `<sc-marketing-nav>` — **do not import our portal/dashboard/orders/settings links into a real product page.** Override with the consumer's own nav data, or hide and use plain links.
- Content + copy — write for the real audience, real offer, real conversion goal. Don't reuse our placeholder copy verbatim ("Pay back your SuperCat investment in under 90 days" is OUR demo line; your page needs its own).
- Layout structures — a real product page may need 5 sections or 12; copy the editorial vocabulary, not the section count from `maxroi.html`.

**The mental model:** this system is to a real page what a typeface family is to a book. The typeface defines how it feels; the manuscript defines what it says. Don't ship the manuscript with the typeface.

**For LLM-assisted builds:** when prompting an AI tool to apply this system to your page, always include the instruction *"this is a foundation + guide, not a content template — adapt structure and copy to my real audience and conversion goal; keep only the visual vocabulary."* Without that line, tools tend to copy demo content one-to-one.

---

## ★ Marketing page recipe — build any landing page on-brand

Every marketing page in this system is a remix of the same ingredients. Internalize this and you can build any landing/lead-magnet/product page without confusion or off-brand results.

### The look — what "premium editorial" means here

| | |
|---|---|
| **Background** | Paper-warm cream (`var(--surface-page)`). Never pure white. |
| **Type** | Geist Sans for everything visible; Geist Mono for numbers, eyebrows, captions, table cells. Tabular nums on any numeric column. |
| **Headlines** | Big editorial. `clamp(40px, 6vw, 84px)` · `font-weight: 500` · `letter-spacing: -0.02em` · `line-height: ~1.04`. Wrap the accent phrase in `<em>` styled `color: var(--color-crimson)` (no italic). |
| **Spacing** | Generous. Section padding `clamp(48px, 6vw, 96px)` top/bottom. Dashed `border-bottom` between sections. Body content max-width 1480px, padding `clamp(20px, 4vw, 56px)` sides. |
| **Hairlines** | 1px solid `var(--border-default)` for structural lines · 1px dashed `var(--border-subtle)` for editorial dividers. |
| **Color roles** | Crimson = ONE primary CTA per section + danger. Gold = brand mark + occasional editorial accents. Cream = paper. Clay = neutral data viz. Moss = success. **Don't swap.** |
| **Radii** | `--radius-sm/md/lg/xl` — cards, buttons, modals all share the family. |
| **Motion** | Pulsing eyebrow dot for "live" indicators. Hover-lift on `.kc.kc-interactive` cards. WAAPI slide on `.ktab-seg`. Always honor `prefers-reduced-motion: reduce`. |

### The section vocabulary

A marketing page is built from these blocks. Pick what your page needs — not every page uses all of them.

| Block | When to use | Anatomy |
|---|---|---|
| **Nav** (always) | `<sc-marketing-nav>` for site-wide; `<sc-marketing-nav sections=[...]>` for one-page anchors. | Dark glass pill. Logo left · links center · theme toggle + primary CTA right. |
| **Hero** (always) | First impression. | 2-col grid: editorial copy (eyebrow + headline + lede + CTA pair + trust line) left, viz/screenshot right. Trust line under CTAs: mono uppercase "No credit card · 25-sec setup". |
| **Stat strip** | When you have hard numbers worth flashing. | 3–4 mono tabular nums + small uppercase captions. Dashed borders top + bottom. |
| **Section** | Every content beat. | 2-col head (h2 + lede), dashed `border-bottom`. h2 size `clamp(36px, 4.4vw, 60px)`. |
| **Card grid** | "Here's what's inside / how it works" — 3–5 features. | `.kc` cards with `.kc-head` + `.kc-body`. Hover-lift if interactive. Driver-pattern: eyebrow → title → tag → copy → big number. |
| **Radio-card picker** | Plan / tier / preset selectors. | `.kc.kc-pick` in 3-up grid with `role="radiogroup"`. Cards show title + description + meta. Crimson border + "SELECTED" tag on active. |
| **Segmented control** | Compact toggles (scenario, view mode). | `.ktab.ktab-seg` (single line) or `.ktab.ktab-seg.ktab-rich` (2-line with name + spec). Sliding bar driven by `tabs.js`. |
| **Math table / breakdown** | Transparency moment. | Surface-card box. Each row: name (sans) · formula (mono, crimson highlights on key constants) · value (sans, tabular nums). |
| **Cost-of-waiting** | Emotional appeal. ONE big stat. | Dark inverted section (`background: var(--text-primary); color: var(--surface-card)`). ONE giant mono number. Gold eyebrow + gold accent in headline. |
| **Final CTA + lead form** | Conversion moment. | 2-col: copy + summary strip left, form card right. Form is name + company + email + 2 CTAs (Email it to me · Book a session). |
| **Footer** | Always. | `.kfoot` with brand mark + universal motto + 2–3 link columns + "Bring it live" CTA card. Bottom rule with copyright. |
| **Lead modal** | Triggered by passive cues (dwell, scroll) + share CTAs. | `<dialog class="kmd kmd-md">` with intent attribute. Same 3 fields (name + company + email). |

### ★ Nav + Footer — style is fixed, content is per-page

Every marketing page in this system uses the **same dark glass pill nav** and the **same `.kfoot` brand footer**. The chrome is shared, the content adapts.

**Nav — `<sc-marketing-nav>` (custom element, lives in `nav/marketing-nav.js`)**

The pill itself never changes — translucent ink-2 background, cream type, gold mark, theme toggle, primary crimson CTA. Only the **content shape** changes:

| Mode | When to use | Markup |
|---|---|---|
| **Mega menus** (default) | Site-wide nav with cross-site routes | `<sc-marketing-nav current="…"></sc-marketing-nav>` |
| **Sections** (on-page anchors) | Product / lead-magnet pages with their own section nav | `<sc-marketing-nav current="…" cta-href="#…" cta-label="…" sections='[{"label":"…","href":"#…"}, …]'></sc-marketing-nav>` |

The `sections` attribute is JSON — Lovable / any tool can override it with the host page's own section list. **Don't import the demo mega-menu items** (Foundation / Web Marketing / etc) into a real product page; either use sections mode or override the data via `marketing-nav.js` config before that script loads.

**Footer — `.kfoot` (primitive in `ds/primitives/footer.css`)**

The footer **structure is fixed** — gold brand mark + tag + meta-dot + 2–3 link columns + "Bring it live" CTA card + bottom rule. The **content swaps** per page:

| Block | Style locked | Content per page |
|---|---|---|
| `.kfoot-brand` | Gold SVG mark via `<use href="#i-mark"/>` | URL it links to |
| `.kfoot-tag` | Sans, text-lg, tracking-tighter, kfoot-fg-strong | Universal brand motto (NOT page-specific) |
| `.kfoot-meta` | Mono uppercase, kfoot-fg-muted, with status dot | Brand domain or status line |
| `.kfoot-col` | Mono eyebrow + sans link list | Column title + link names + hrefs |
| `.kfoot-cta` | Card with title + copy + crimson kb-primary | Title + copy + action (e.g. "Book a session") |
| `.kfoot-rule-copy` | Mono small caps | Copyright line |
| `.kfoot-rule-links` | Right-aligned small links | 1–2 secondary nav items |

**Universal rule**: footer copy should read on ANY page — describe the brand, not the current page. The maxroi tag *"The sales engine for product brands…"* works on every SuperCat surface.

### The hard rules — non-negotiable

1. **Logo = vector SVG always.** Never typed text. Asset at `assets/supercat-mark.svg`. Inline via `<use href="#i-mark"/>` with `viewBox="0 0 41 28"` and `fill="currentColor"`. Default color `var(--color-gold)`.
2. **No custom colors.** Tokens only — `--color-*`, `--text-*`, `--surface-*`, `--border-*`, `--status-*`. If you need a color that doesn't exist, ask before adding.
3. **No overriding primitive base styles.** Scope tweaks via descendant selectors only. `.toolbar .kb { height: 40px }` ✓ · `.kb { padding: 12px }` ✗.
4. **Crimson is for PRIMARY action + danger + ONE accent phrase per headline.** Never body, eyebrow, or chrome.
5. **Gold is for the brand mark + rare editorial accents.** Never for actions.
6. **Eyebrows** have a pulsing crimson dot (animated halo), mono uppercase text, muted color. Don't substitute with chunky badges or block-color blobs.
7. **Numbers** always use the mono font + `font-variant-numeric: tabular-nums lining-nums`. Currency rounds: `$273K`, `$1.37M`, `Day 76`.
8. **One primary CTA per section.** Multiple CTAs are fine; multiple PRIMARY visual weights are not.
9. **Real content only.** No lorem ipsum, no fabricated testimonials, no invented stats. If proof is missing, ask.
10. **Dark mode honored.** `<html data-theme="dark">` switches every primitive. Don't add inline colors that won't flip.

### The 5-step recipe for any new marketing page

1. **Outline first, then design.** What does the page need to communicate? In what order? What's the ONE next action? Write a 4–6 bullet structural plan before touching code. (For LLM tools: ask the agent to audit + propose structure before implementing.)
2. **Pick blocks from the section vocabulary above.** Hero is required. Footer is required. Everything in between is need-driven.
3. **Use the page shell pattern from `marketing/maxroi.html`:**
   ```html
   <link rel="stylesheet" href="../ds/tokens/index.css"/>
   <link rel="stylesheet" href="../nav/marketing-nav.css"/>
   <!-- primitives you use -->
   <script src="../nav/marketing-nav.js" defer></script>
   <!-- primitive JS controllers you use -->
   <body>
     <svg width="0" height="0" style="position:absolute"><defs>
       <symbol id="i-mark" viewBox="0 0 41 28">…</symbol>
     </defs></svg>
     <sc-marketing-nav …></sc-marketing-nav>
     <main class="page-shell" style="max-width:1480px;margin:0 auto;padding:clamp(48px,8vw,96px) clamp(20px,4vw,56px) 0;">
       <!-- sections here -->
     </main>
     <footer class="kfoot">…</footer>
   </body>
   ```
4. **Compose using token + primitive vocabulary only.** Every spacing decision: a `--space-N`. Every color: a `--color-*` or semantic alias. Every font size: a `--text-*`. Every radius: a `--radius-*`.
5. **Verify in light + dark + mobile (375px).** If anything reads wrong in any of the three, the issue is composition (your code), not the design system.

### Anti-patterns — what an off-brand page looks like

| ✗ Off-brand | ✓ On-brand |
|---|---|
| Pure white background `#fff` | Cream paper `var(--surface-page)` |
| `<h1>SuperCat</h1>` text logo | SVG mark via `<use href="#i-mark"/>` |
| Heading 1 in crimson | Heading 1 in ink; ONE accent phrase in `<em>` crimson |
| Solid blocks of gradient as accent | Hairline borders, dashed dividers |
| Sans-serif numbers | Mono numbers with tabular-nums |
| Multiple competing primary CTAs | One crimson CTA per section, others secondary |
| Generic "Get Started" button | Specific action verb: "Run mine", "See my projection", "Book a session" |
| Static eyebrow dot | Pulsing animated dot (radar ping) |
| Crammed cards, tight padding | `clamp()` padding, generous breathing room |
| Custom color hex values | Tokens (`var(--color-*)`) |
| Sans labels everywhere | Mono uppercase for eyebrows + captions + numbers |

---

## 5. Folders at a glance

```
ds/tokens/        → color, type, space, radius, motion, shadow, semantic
ds/primitives/    → button, input, check, switch, field, date, card, table,
                    tabs, nav, modal, skeleton, icon, footer
nav/              → <sc-marketing-nav> + <sc-app-sidebar> shared components
assets/           → brand mark SVG + logos
app/              → 5 reference app screens
marketing/        → MaxROI lead-magnet landing page (canonical marketing example)
docs/             → SURFACES.md (architecture) + FRAMEWORK-GUIDE.md (integration)
```

Open `index.html` and start clicking. Read **`marketing/maxroi.html` end-to-end** before building anything new — it's the canonical reference for every block above.
