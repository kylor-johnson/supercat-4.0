# SuperCat Design System v3 — Complete LLM Instruction File

> Upload this as project context in Lovable, Cursor, Claude Projects, or v0. Contains ALL tokens, primitive CSS, logo SVGs, page patterns, and design rules needed for 100% on-brand web pages.

**v0.4 · May 2026**

---

## 0. How to Use This File

### Setup
Upload this file as an **attachment** in Lovable chat, or paste into **Project Knowledge** / **System Prompt** in Cursor or Claude Projects.

### Prompt template
After upload, just describe what you want. Header (logo pill + theme toggle) and footer (logo pill) are included on every page — you only need to describe the body:

```
[Attached: SuperCat Design System v3]

Build [DESCRIBE YOUR PAGE]. Apply the SuperCat Design System for all styling.

[YOUR CONTENT — paste text, describe sections, or attach a content file]
```

**Examples:**
```
Build a landing page for SuperCat Solutions.
Hero: "Sell Smarter. Grow Faster." — B2B commerce for furniture manufacturers.
Features: 3 cards — Digital Catalog, Dealer Portal, Analytics.
CTA: "Start Free Trial" form with name, email, company.
```

```
Restyle this existing page using the SuperCat Design System. Keep all content and logic.
```

### What's automatic (built into every page by default)

**Every page MUST be fully responsive** — desktop (1440px), laptop (1200px), tablet (768px), mobile (375px). Single-column on mobile. Text scales. Padding reduces. Non-negotiable.

**Default page structure (always included, don't ask for these):**
- **Header** — Logo pill (SuperCat SVG from §3, `border-radius:999px`, `height:40px`) + theme toggle (40px circle) + optional CTA. Transparent with progressive blur backdrop. `position:fixed; top:0; width:100%`, overlays hero. No nav links unless specified.
- **Footer** — Same logo pill as header. Copyright text. Responsive columns if links provided, otherwise simple centered layout.
- **Theme toggle** — light/dark switching with moon/sun icon. Light is default. Set `data-theme="light|dark"` on `<html>`.
- **Fonts** — Geist + Geist Mono loaded from Google Fonts.
- **Logo SVGs** — Inline from §3. Auto-recolor for light/dark via `fill` rules.
- **Colors, spacing, dark mode** — all handled by CSS tokens in §4.
- **Buttons** — `.kb` primitive in §6a, drop-in classes with hover/loading/success.
- **Forms** — `.kf-input` `.kf-check` `.kf-switch` `.kf-field` primitives in §6b–e.

### For The Line Card brand
Mention "The Line Card" or "TLC" in your prompt — uses crimson + clay accent (**never gold**).

### Three-tier architecture

```
Tokens (§4)        →   Primitive components (§6)   →   Page patterns (§7)
--color-crimson        .kb, .kf-input, .kf-check        Hero, Section, Card, CTA
--space-6              .kf-switch, .kf-field, .kf-date
--text-primary
```

Don't author new tokens or new component classes. Use what's here. To re-skin one instance, override component-local custom properties via inline `style` (see component sections).

---

## 1. Brand

**SuperCat Solutions** — B2B commerce platform for furniture, lighting, and home décor manufacturers. Audience: senior decision-makers (owners, VPs of Sales, COOs) at small-to-mid manufacturers.

| Sub-brand | Purpose | Accent |
|-----------|---------|--------|
| **SuperCat** | Primary platform | Crimson + Gold |
| **eCat** | iPad sales app | Crimson + Gold (same as SuperCat) |
| **The Line Card** | Industry directory product | Crimson + Clay (**NEVER gold**) |

**Voice:** confident, restrained, editorial. No exclamation points. Short headlines (4–7 words). High-school reading level for body. Numbers always in mono font.

---

## 2. Fonts

```html
<!-- In <head> of every page -->
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- **Geist Sans** — headings, body, buttons, nav links
- **Geist Mono** — labels, eyebrows, badges, metrics, table headers, code, data values, numbers
- Eyebrows / micro-labels: **always uppercase**, `letter-spacing: 0.12em` (`var(--tracking-wider)`)

---

## 3. Logos (Full SVG Embeds)

**Which logo where:**

| Context | Logo | Width | Text fill | Icon fill |
|---------|------|-------|-----------|-----------|
| Header pill (light) | SuperCat full | 140–180 | `#7A1218` | `#B97727` |
| Header pill (dark) | SuperCat full | 140–180 | `#EBE6D7` | `#B97727` |
| Footer (light) | SuperCat full | 120–160 | `#7A1218` | `#B97727` |
| Footer (dark) | SuperCat full | 120–160 | `#EBE6D7` | `#B97727` |
| Hero on crimson | SuperCat full | 200+ | `#F0EFEC` | `#F0EFEC` |
| Dark hero CTA | Cat mark only | 32–48 | — | `#B97727` |
| Favicon | Cat mark only | 24–32 | — | `#B97727` |
| The Line Card page (light) | TLC logo | 160–200 | `#731819` | — |
| The Line Card page (dark) | TLC logo | 160–200 | `#EBE6D7` | — |

**How to recolor for any LLM:** find-replace `fill="#7A1218"` → new text color; `fill="#B97727"` → new icon color. The `viewBox` preserves proportions — just change `width` / `height` to resize.

### 3a. Cat Mark (41×28)

Use for favicons, hero accents, dark CTA marks. Both paths share the same fill.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="41" height="28" viewBox="0 0 41 28" fill="none">
  <path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="#B97727"/>
  <path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="#B97727"/>
</svg>
```

### 3b. SuperCat Full Logo (237×28)

Use for header pill, footer, hero. Text paths use `#7A1218`, mark paths (last 2) use `#B97727`. Recolor accordingly.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="237" height="28" viewBox="0 0 237 28" fill="none">
  <path d="M49.001 18.931V15.1316C49.0258 14.9292 48.9804 14.7268 48.8646 14.5575C48.6952 14.4543 48.4968 14.4088 48.3025 14.4336H46.7732C45.5911 14.4336 45 13.8431 45 12.6619V8.77581C45 7.59469 45.5911 7 46.7732 7H48.753C49.9351 7 50.5262 7.59469 50.5262 8.77581V10.9316H48.9762V9.01947C49.0796 8.73864 48.9349 8.42891 48.6538 8.32566C48.5298 8.28024 48.3976 8.28024 48.2777 8.32566H47.2444C46.9633 8.22242 46.6533 8.36696 46.55 8.64779C46.5045 8.76755 46.5045 8.89971 46.55 9.01947V12.41C46.5252 12.6041 46.5706 12.8024 46.674 12.9717C46.8434 13.0832 47.046 13.1327 47.2444 13.1038H48.7737C49.9558 13.1038 50.551 13.6985 50.551 14.8796V19.1953C50.551 20.3764 49.9558 20.967 48.7737 20.967H46.8186C45.6365 20.967 45.0455 20.3764 45.0455 19.1953V17.0395H46.5955V18.931C46.4921 19.2118 46.6368 19.5215 46.9178 19.6248C47.0377 19.6702 47.17 19.6702 47.2898 19.6248H48.3025C48.4968 19.6496 48.6952 19.6041 48.8646 19.5009C48.9804 19.3357 49.03 19.1333 49.001 18.931Z" fill="#7A1218"/>
  <path d="M60.5261 7H62.0513V19.1953C62.0513 20.3764 61.4602 20.967 60.2781 20.967H57.9841C56.802 20.967 56.2109 20.3764 56.2109 19.1953V7H57.7361V18.931C57.7072 19.1333 57.7568 19.3357 57.8725 19.5009C58.042 19.6041 58.2404 19.6496 58.4346 19.6248H59.8482C60.0425 19.6496 60.2409 19.6041 60.4104 19.5009C60.5261 19.3357 60.5757 19.1333 60.5468 18.931L60.5261 7Z" fill="#7A1218"/>
  <path d="M68.0586 7H72.1258C73.3079 7 73.9031 7.59469 73.9031 8.77581V13.5622C73.9031 14.7475 73.3079 15.3381 72.1258 15.3381H69.5879V20.9504H68.0586V7ZM72.3737 13.3351V9.01947C72.4812 8.73864 72.3407 8.42891 72.0596 8.32153C71.9356 8.27611 71.7992 8.27611 71.6752 8.32153H69.6086V14.0289H71.6752C71.9563 14.1322 72.2663 13.9917 72.3737 13.7109C72.4192 13.5912 72.4192 13.4549 72.3737 13.3351Z" fill="#7A1218"/>
  <path d="M80.9553 19.6413H84.7952V20.967H79.4219V7H84.6505V8.32566H80.9677V13.0419H83.9768V14.3882H80.9677L80.9553 19.6413Z" fill="#7A1218"/>
  <path d="M91.6074 15.1316V20.967H90.0781V7H94.1577C95.3398 7 95.935 7.59469 95.935 8.77581V13.3558C95.935 14.4171 95.4679 15.0077 94.5421 15.1068L96.6377 20.967H94.9843L92.9177 15.1316H91.6074ZM91.6074 8.32566V13.8059H93.6741C93.9552 13.9133 94.2652 13.7729 94.3726 13.492C94.4181 13.3681 94.4181 13.2319 94.3726 13.108V9.01947C94.4801 8.73864 94.3395 8.42891 94.0585 8.32153C93.9345 8.27611 93.7981 8.27611 93.6741 8.32153H91.6074V8.32566Z" fill="#7A1218"/>
  <path d="M107.467 11.1339H105.917V9.01947C105.942 8.81711 105.896 8.61475 105.78 8.44543C105.615 8.34218 105.417 8.29676 105.222 8.32153H103.982C103.701 8.21829 103.391 8.36283 103.288 8.64366C103.243 8.76755 103.243 8.89971 103.288 9.01947V18.9681C103.263 19.1622 103.309 19.3605 103.412 19.5298C103.581 19.6454 103.784 19.6909 103.987 19.6661H105.227C105.421 19.6867 105.619 19.6413 105.785 19.5298C105.896 19.3646 105.946 19.1664 105.921 18.9681V16.8661H107.471V19.2242C107.471 20.4053 106.88 21 105.698 21H103.515C102.333 21 101.742 20.4053 101.742 19.2242V8.77581C101.742 7.59469 102.333 7 103.515 7H105.698C106.88 7 107.471 7.59469 107.471 8.77581V11.1339H107.467Z" fill="#7A1218"/>
  <path d="M117.786 20.967L117.199 17.4195H114.367L113.851 20.967H112.301L114.479 7H116.93L119.336 20.967H117.786ZM114.549 16.0938H116.996L115.694 8.07788L114.549 16.0938Z" fill="#7A1218"/>
  <path d="M129.405 7V8.32566H127.157V20.967H125.627V8.32566H123.379V7H129.405Z" fill="#7A1218"/>
  <path d="M144.532 18.931V15.1316C144.557 14.9292 144.512 14.7268 144.396 14.5575C144.226 14.4543 144.028 14.4088 143.834 14.4336H142.304C141.122 14.4336 140.531 13.8431 140.531 12.6619V8.77581C140.531 7.59469 141.122 7 142.304 7H144.284C145.466 7 146.057 7.59469 146.057 8.77581V10.9316H144.507V9.01947C144.611 8.73864 144.47 8.42891 144.189 8.32153C144.069 8.27611 143.933 8.27611 143.813 8.32153H142.776C142.495 8.21829 142.185 8.36283 142.081 8.63953C142.036 8.76342 142.036 8.89558 142.081 9.01947V12.41C142.056 12.6041 142.102 12.8024 142.205 12.9717C142.375 13.0832 142.577 13.1327 142.776 13.1038H144.305C145.487 13.1038 146.082 13.6985 146.082 14.8796V19.1953C146.082 20.3764 145.487 20.967 144.305 20.967H142.35C141.168 20.967 140.577 20.3764 140.577 19.1953V17.0395H142.127V18.931C142.023 19.2118 142.168 19.5215 142.449 19.6248C142.569 19.6702 142.701 19.6702 142.821 19.6248H143.834C144.028 19.6496 144.226 19.6041 144.396 19.5009C144.512 19.3357 144.561 19.1333 144.532 18.931Z" fill="#7A1218"/>
  <path d="M153.468 7H155.762C156.945 7 157.536 7.59469 157.536 8.77581V19.1953C157.536 20.3764 156.945 20.967 155.762 20.967H153.468C152.286 20.967 151.695 20.3764 151.695 19.1953V8.77581C151.695 7.59469 152.286 7 153.468 7ZM156.01 18.931V9.01947C156.035 8.81711 155.99 8.61475 155.874 8.44543C155.705 8.34218 155.506 8.29676 155.312 8.32153H153.919C153.725 8.29676 153.526 8.34218 153.357 8.44543C153.266 8.52802 153.225 8.71799 153.225 9.01947V18.931C153.225 19.2283 153.266 19.4224 153.357 19.5009C153.526 19.6041 153.725 19.6496 153.919 19.6248H155.328C155.523 19.6496 155.721 19.6041 155.891 19.5009C156.002 19.3316 156.044 19.1292 156.01 18.931Z" fill="#7A1218"/>
  <path d="M165.025 19.6413H168.237V20.967H163.496V7H165.025V19.6413Z" fill="#7A1218"/>
  <path d="M177.428 7H178.958V19.1953C178.958 20.3764 178.367 20.967 177.18 20.967H174.891C173.704 20.967 173.109 20.3764 173.113 19.1953V7H174.643V18.931C174.614 19.1292 174.663 19.3316 174.775 19.5009C174.944 19.6041 175.143 19.6496 175.337 19.6248H176.734C176.928 19.6496 177.127 19.6041 177.292 19.5009C177.408 19.3357 177.457 19.1333 177.428 18.931V7Z" fill="#7A1218"/>
  <path d="M189.857 7V8.32566H187.609V20.967H186.079V8.32566H183.852V7H189.857Z" fill="#7A1218"/>
  <path d="M195.008 7H196.537V20.967H195.008V7Z" fill="#7A1218"/>
  <path d="M204.516 7H206.81C207.992 7 208.587 7.59469 208.587 8.77581V19.1953C208.587 20.3764 207.992 20.967 206.81 20.967H204.516C203.333 20.967 202.742 20.3764 202.742 19.1953V8.77581C202.73 7.59469 203.321 7 204.516 7ZM207.045 18.931V9.01947C207.07 8.81711 207.024 8.61475 206.909 8.44543C206.739 8.34218 206.541 8.29676 206.347 8.32153H204.954C204.759 8.29676 204.561 8.34218 204.392 8.44543C204.28 8.61475 204.23 8.81711 204.259 9.01947V18.931C204.23 19.1292 204.28 19.3316 204.392 19.5009C204.561 19.6041 204.759 19.6496 204.954 19.6248H206.347C206.541 19.6496 206.739 19.6041 206.909 19.5009C207.024 19.3357 207.074 19.1333 207.045 18.931Z" fill="#7A1218"/>
  <path d="M219.111 7H220.529V20.967H218.842L215.949 10.1469V20.967H214.531V7H216.329L219.115 17.4442V7H219.111Z" fill="#7A1218"/>
  <path d="M230.255 18.931V15.1316C230.284 14.9292 230.234 14.7268 230.123 14.5575C229.953 14.4543 229.755 14.413 229.561 14.4336H228.031C226.849 14.4336 226.254 13.8431 226.254 12.6619V8.77581C226.254 7.59469 226.849 7 228.031 7H230.007C231.193 7 231.784 7.59469 231.784 8.77581V10.9316H230.234V9.01947C230.342 8.73864 230.201 8.42891 229.92 8.32153C229.796 8.27611 229.66 8.27611 229.536 8.32153H228.486C228.201 8.22655 227.895 8.37935 227.8 8.66018C227.758 8.77581 227.763 8.90384 227.804 9.01947V12.41C227.779 12.6041 227.825 12.8024 227.928 12.9717C228.097 13.0832 228.3 13.1327 228.502 13.1038H230.032C231.214 13.1038 231.805 13.6985 231.805 14.8796V19.1953C231.805 20.3764 231.214 20.967 230.032 20.967H228.073C226.886 20.967 226.291 20.3764 226.295 19.1953V17.0395H227.845V18.931C227.82 19.1292 227.862 19.3316 227.969 19.5009C228.139 19.6083 228.345 19.6496 228.544 19.6248H229.556C229.751 19.6454 229.949 19.6041 230.119 19.5009C230.23 19.3357 230.28 19.1292 230.255 18.931Z" fill="#7A1218"/>
  <path d="M20.4773 17.6424C16.8375 10.6856 13.5207 10.6117 10.2067 10.5378C8.69685 10.5042 7.18762 10.4706 5.64872 9.78608L0 0H2.43148C5.09633 3.25885 7.65432 3.51236 10.2129 3.76594C13.5561 4.09728 16.9003 4.42872 20.4853 11.4648C24.0761 4.39466 27.4109 4.0844 30.7463 3.77408C33.2971 3.53675 35.8483 3.29939 38.5148 0.0385625H41L35.3692 9.78883C33.8047 10.503 32.2722 10.5331 30.7392 10.5634C27.4294 10.6286 24.1175 10.6937 20.4773 17.6424Z" fill="#B97727"/>
  <path d="M20.4773 27.9975L20.4771 27.9972L20.4756 28L20.4756 27.9944C17.538 22.3699 14.7931 21.2243 12.1087 20.9635L7.9752 13.8017C8.72235 13.9462 9.4664 14.0158 10.2103 14.0855C13.5487 14.398 16.8835 14.7102 20.4773 21.7843C24.0589 14.7274 27.3849 14.4269 30.7115 14.1261C31.4831 14.0563 32.2548 13.9866 33.0298 13.8324L28.8886 20.9942C26.1863 21.25 23.4405 22.3367 20.4773 27.9969V27.9975Z" fill="#B97727"/>
  <path d="M234.88 7V7.1941H234.306V8.69735H234.078V7.1941H233.504V7H234.88ZM236.72 8.69735L236.641 7.54513C236.641 7.44602 236.641 7.31799 236.62 7.18171C236.583 7.28083 236.525 7.45841 236.484 7.59469L236.091 8.68083H235.835L235.422 7.56578C235.389 7.45841 235.335 7.29735 235.298 7.18997V7.55339L235.215 8.70561H234.992L235.128 7.00826H235.459L235.872 8.0944C235.922 8.21829 235.951 8.33805 235.988 8.44956C236.025 8.33392 236.071 8.19351 236.104 8.10678L236.517 7.00826H236.848L237.001 8.70561L236.72 8.69735Z" fill="#7A1218"/>
</svg>
```

### 3c. eCat Full Logo (455×82)

iPad app branding. Mark paths use `#B97727`, text paths use `#7C282C`.

```svg
<svg width="455" height="82" viewBox="0 0 455 82" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M60.1289 51.6671C49.4411 31.2936 39.7016 31.0771 29.9705 30.8608C25.5371 30.7623 21.1055 30.6638 16.5867 28.6592L0 0H7.13973C14.9647 9.54376 22.4759 10.2862 29.9889 11.0288C39.8056 11.9992 49.6255 12.9698 60.1525 33.5755C70.6963 12.8701 80.4883 11.9615 90.2824 11.0527C97.7725 10.3576 105.264 9.66251 113.093 0.112933H120.391L103.857 28.6673C99.263 30.7587 94.7629 30.8471 90.2616 30.9355C80.5429 31.1265 70.8179 31.3172 60.1289 51.6671Z" fill="#B97727"/>
  <path d="M60.1288 81.9926L60.1283 81.9917L60.124 82L60.124 81.9835C51.498 65.5119 43.438 62.1569 35.5557 61.393L23.4181 40.4192C25.612 40.8424 27.7968 41.0463 29.9811 41.2503C39.784 42.1656 49.576 43.0798 60.1288 63.797C70.6459 43.1303 80.4121 42.2502 90.1802 41.3693C92.4461 41.165 94.7121 40.9606 96.9875 40.5093L84.8275 61.4831C76.8925 62.232 68.8299 65.4145 60.1288 81.9909V81.9926Z" fill="#B97727"/>
  <path d="M154.208 69.5968C149.895 69.5968 146.197 69.2891 143.178 68.7045C140.158 68.1199 137.693 67.0738 135.814 65.6276C133.934 64.1814 132.548 62.2122 131.685 59.7507C130.822 57.2891 130.391 54.2122 130.391 50.4891C130.391 46.243 130.822 42.7353 131.685 39.9353C132.548 37.1661 133.904 34.9507 135.814 33.3199C137.693 31.6891 140.158 30.5199 143.178 29.8737C146.197 29.2276 149.864 28.8891 154.208 28.8891C157.29 28.8891 159.97 29.1045 162.22 29.5661C164.5 30.0276 166.41 30.6737 168.043 31.5353C169.645 32.3968 170.97 33.4122 171.956 34.643C172.973 35.843 173.743 37.1353 174.329 38.4891C174.914 39.8122 175.284 41.3814 175.499 43.1968C175.715 44.9814 175.807 46.8891 175.807 48.8891L175.284 51.043H136.923C136.923 53.9353 137.231 56.3045 137.817 58.1814C138.402 60.0276 139.388 61.3814 140.713 62.243C142.069 63.1045 143.856 63.6584 146.043 63.8738C148.262 64.0891 150.973 64.2122 154.208 64.2122C157.197 64.2122 159.662 64.1199 161.603 63.9661C163.544 63.8122 165.116 63.5045 166.256 63.043C167.396 62.5814 168.197 61.9661 168.659 61.1661C169.121 60.3661 169.368 59.3199 169.368 58.0584H175.869C175.869 60.1507 175.499 61.9353 174.76 63.4122C174.02 64.8891 172.819 66.0891 171.124 66.9814C169.429 67.9045 167.211 68.5507 164.438 68.9814C161.665 69.4122 158.276 69.5968 154.208 69.5968ZM154.208 34.3045C152.052 34.3045 150.11 34.3353 148.416 34.4276C146.721 34.5199 145.211 34.7045 143.948 35.0122C142.685 35.3199 141.576 35.7507 140.682 36.3353C139.789 36.9199 139.049 37.5661 138.494 38.3661C137.94 39.1353 137.539 40.243 137.262 41.6276C137.016 43.043 136.861 44.7353 136.861 46.7045H169.306C169.306 44.0584 169.029 41.9968 168.474 40.5199C167.92 39.0122 167.026 37.7814 165.794 36.8276C164.592 35.8738 163.021 35.1968 161.11 34.8276C159.2 34.4584 156.889 34.2737 154.178 34.2737" fill="#7C282C"/>
  <path d="M268.397 33.2283C268.397 30.5206 268.089 28.3975 267.534 26.8283C266.949 25.259 265.963 24.059 264.638 23.259C263.282 22.459 261.526 21.936 259.307 21.7206C257.12 21.5052 254.378 21.3821 251.142 21.3821H235.952C233.056 21.3821 230.653 21.4744 228.681 21.6283C226.709 21.7821 225.076 22.1513 223.812 22.6436C222.518 23.1667 221.532 23.9052 220.824 24.859C220.115 25.8129 219.622 27.1052 219.314 28.7052C219.006 30.3052 218.821 32.2744 218.759 34.5821C218.698 36.9206 218.698 39.6898 218.698 42.9206C218.698 46.1513 218.698 48.9513 218.79 51.2898C218.852 53.6283 219.037 55.5667 219.345 57.1667C219.653 58.7667 220.146 60.059 220.854 61.0129C221.532 61.9975 222.518 62.7359 223.812 63.2283C225.106 63.7513 226.739 64.0898 228.681 64.2436C230.653 64.4283 233.087 64.4898 235.952 64.4898H251.142C253.669 64.4898 255.826 64.4283 257.674 64.2744C259.492 64.1513 261.064 63.9052 262.327 63.536C263.621 63.1667 264.638 62.6744 265.439 62.059C266.24 61.4436 266.825 60.6436 267.288 59.6898C267.719 58.736 268.027 57.5975 268.181 56.2436C268.335 54.8898 268.428 53.3513 268.428 51.5359H274.929C274.929 53.6898 274.806 55.659 274.528 57.3821C274.251 59.136 273.789 60.6744 273.08 62.0283C272.402 63.3821 271.478 64.5513 270.338 65.5667C269.198 66.5821 267.75 67.3821 265.994 68.0283C264.237 68.6744 262.142 69.1359 259.708 69.4436C257.274 69.7513 254.439 69.9052 251.204 69.9052H236.014C232.039 69.9052 228.711 69.659 226 69.1667C223.289 68.6744 221.039 67.9667 219.283 66.9821C217.527 65.9975 216.171 64.7667 215.216 63.2898C214.261 61.8129 213.552 60.059 213.121 58.059C212.689 56.059 212.443 53.7821 212.35 51.2898C212.289 48.7667 212.258 45.9667 212.258 42.9206C212.258 39.8744 212.289 37.0744 212.35 34.5513C212.412 32.0283 212.658 29.7821 213.121 27.7513C213.552 25.7513 214.261 23.9975 215.216 22.5206C216.171 21.0436 217.527 19.8129 219.283 18.8283C221.039 17.8437 223.289 17.1052 226 16.6436C228.711 16.1513 232.07 15.9052 236.014 15.9052H251.204C254.439 15.9052 257.274 16.059 259.708 16.3667C262.142 16.6744 264.237 17.136 265.994 17.7513C267.75 18.3667 269.198 19.1667 270.338 20.0898C271.478 21.0437 272.402 22.1513 273.08 23.4129C273.758 24.7052 274.251 26.1513 274.528 27.7821C274.806 29.4129 274.929 31.1975 274.929 33.1667H268.428L268.397 33.2283Z" fill="#7C282C"/>
  <path d="M363.978 56.9822H323.368L316.589 68.8591H309.071L338.681 17.0129H347.987L377.504 68.8591H370.695L363.947 56.9822H363.978ZM360.897 51.5975L343.704 21.3206L326.449 51.5975H360.927H360.897Z" fill="#7C282C"/>
  <path d="M454.253 17.0129V22.4283H428.309V68.8591H421.808V22.4283H395.864V17.0129H454.253Z" fill="#7C282C"/>
</svg>
```

### 3d. The Line Card Logo (192×16)

TLC pages only. Single fill color: `#731819` (light) → `#EBE6D7` (dark).

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="192" height="16" viewBox="0 0 192 16" fill="none">
  <path d="M0 2.92468V0.301025H12.3656V2.92468H7.74194V15.6774H4.62366V2.92468H0Z" fill="#731819"/>
  <path d="M13.9414 15.6774V0.301025H17.0597V6.32253H23.1027V0.301025H26.221V15.6774H23.1027V8.90318H17.0597V15.6774H13.9414Z" fill="#731819"/>
  <path d="M28.582 15.6774V0.301025H39.8939V2.92468H31.7003V6.36554H38.8831V8.92468H31.7003V13.0752H39.9584V15.6774H28.582Z" fill="#731819"/>
  <rect x="47.6055" y="6.80786" width="31.8451" height="2.27465" fill="#731819"/>
  <path d="M87.3945 15.6776V0.30127H90.5128V13.0755H97.7386V15.6776H87.3945Z" fill="#731819"/>
  <path d="M99.4297 15.6776V0.30127H102.548V15.6776H99.4297Z" fill="#731819"/>
  <path d="M104.93 15.6776V0.30127H108.091L113.209 8.88192C113.704 9.72063 114.285 11.0325 114.285 11.0325H114.328C114.328 11.0325 114.242 9.44105 114.242 8.36579V0.30127H117.317V15.6776H114.306L109.059 7.18299C108.564 6.36579 107.962 5.05396 107.962 5.05396H107.919C107.919 5.05396 108.005 6.66686 108.005 7.74213V15.6776H104.93Z" fill="#731819"/>
  <path d="M119.676 15.6776V0.30127H130.988V2.92492H122.794V6.36579H129.977V8.92493H122.794V13.0755H131.052V15.6776H119.676Z" fill="#731819"/>
  <path d="M143.331 16.0002C139.009 16.0002 135.934 12.6669 135.934 8.04325C135.934 3.48411 138.772 0.000244141 143.31 0.000244141C147.095 0.000244141 149.331 2.25831 149.654 5.18304H146.557C146.278 3.63465 145.116 2.6239 143.31 2.6239C140.471 2.6239 139.116 4.98949 139.116 8.04325C139.116 11.183 140.751 13.4411 143.331 13.4411C145.159 13.4411 146.45 12.3443 146.643 10.7314H149.697C149.611 12.0863 149.03 13.3981 147.998 14.3658C146.944 15.3551 145.46 16.0002 143.331 16.0002Z" fill="#731819"/>
  <path d="M149.762 15.6776L155.117 0.30127H158.342L163.762 15.6776H160.514L159.482 12.4088H153.934L152.923 15.6776H149.762ZM156.041 5.59159L154.665 10.0217H158.729L157.353 5.59159C157.095 4.77439 156.729 3.226 156.729 3.226H156.686C156.686 3.226 156.299 4.77439 156.041 5.59159Z" fill="#731819"/>
  <path d="M165.059 15.6776V0.30127H172.112C175.08 0.30127 177.059 2.0217 177.059 4.58084C177.059 6.38729 176.22 7.76363 174.241 8.30127V8.36579C175.661 8.77439 176.392 9.59159 176.585 11.4626C176.801 13.6346 176.715 15.2905 177.252 15.5271V15.6776H174.263C173.876 15.5056 173.833 13.7851 173.704 12.1292C173.575 10.4518 172.628 9.50557 170.693 9.50557H168.177V15.6776H165.059ZM168.177 2.8174V7.09697H171.489C173.188 7.09697 174.026 6.21525 174.026 4.98944C174.026 3.74213 173.231 2.8174 171.575 2.8174H168.177Z" fill="#731819"/>
  <path d="M179.066 15.6776V0.30127H185.066C189.174 0.30127 191.819 3.6131 191.819 8.15073C191.819 10.6454 190.98 12.8389 189.367 14.1937C188.228 15.14 186.744 15.6776 184.808 15.6776H179.066ZM182.185 12.9894H184.593C187.518 12.9894 188.658 11.2045 188.658 8.15073C188.658 5.09697 187.324 2.96794 184.679 2.96794H182.185V12.9894Z" fill="#731819"/>
</svg>
```

### React component pattern

```tsx
// src/components/SuperCatLogo.tsx
interface LogoProps {
  variant?: 'color' | 'cream' | 'mono';
  width?: number;
}

export const SuperCatLogo = ({ variant = 'color', width = 160 }: LogoProps) => {
  const textFill = variant === 'color' ? '#7A1218' : variant === 'cream' ? '#EBE6D7' : 'currentColor';
  const iconFill = variant === 'color' ? '#B97727' : variant === 'cream' ? '#B97727' : 'currentColor';
  const height = Math.round(width * (28 / 237));
  return (
    <svg width={width} height={height} viewBox="0 0 237 28" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Paste all paths from §3b — replace fill="#7A1218" with fill={textFill}, fill="#B97727" with fill={iconFill} */}
    </svg>
  );
};
```

---

## 4. Tokens — Complete CSS Block

Copy this entire block into `src/styles/supercat-tokens.css` (or paste into your `:root` block). It contains every primitive scale, every semantic mapping, and dark theme overrides. Components in §6 reference these — never override at the component level, change the token here.

### Three-tier model

```
Primitive   →   Semantic            →   Component-local
--color-*       --text-primary          --kb-bg
--space-*       --surface-card          --kf-border-focus
--text-*        --action-primary        --kfc-bg-checked
--radius-*      --status-danger         --kfs-bg-on
                --border-default
```

| Layer | Example | Use when |
|---|---|---|
| Primitive | `--color-ink-3` | No semantic name fits yet (rare) |
| **Semantic** | `--text-primary` | **Default — always reach here first** |
| Component-local | `--kb-bg-hover` | Per-instance override via `style="--kb-bg: hotpink"` |

### Full tokens block

```css
/* ════════════════════════════════════════════════════════════════
   SuperCat DS — Token Bundle
   Order: primitives (color/type/space/radius/shadow/motion) → semantic
   ════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600;700&display=swap');

:root {
  /* ── COLOR PRIMITIVES ───────────────────────────────────────────
     Paper (warm cream surfaces), Ink (text + dark UI), Line (hairlines),
     Crimson (brand primary), Gold (support), Clay (editorial). */
  --color-paper-1:  #F5F2EC;   /* canvas */
  --color-paper-2:  #EDE9E1;   /* hero panel */
  --color-paper-3:  #E5E0D6;   /* sunken */

  --color-ink-1:    #1A1614;
  --color-ink-2:    #3D3532;
  --color-ink-3:    #5C5450;
  --color-ink-4:    #8A857D;
  --color-ink-5:    #B5B0A9;

  --color-line:       rgba(26, 22, 20, 0.10);
  --color-line-soft:  rgba(26, 22, 20, 0.06);

  --color-crimson:    #7A1218;
  --color-crimson-d:  #5C1215;
  --color-crimson-l:  #F2E2E2;

  --color-gold:       #B97727;
  --color-gold-l:     #F5EDD8;

  --color-clay:       #9B7C60;

  --color-white:      #FFFFFF;
  --color-black:      #000000;

  /* ── TYPE ─────────────────────────────────────────────────────── */
  --font-sans:  'Geist', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-mono:  'Geist Mono', 'SF Mono', 'JetBrains Mono', 'Courier New', monospace;
  --font-serif: 'Source Serif Pro', Georgia, serif;

  --text-2xs:  10px;
  --text-xs:   11px;
  --text-sm:   13px;
  --text-base: 15px;       /* default body */
  --text-md:   16px;
  --text-lg:   18px;
  --text-xl:   22px;
  --text-2xl:  28px;
  --text-3xl:  36px;
  --text-4xl:  48px;
  --text-5xl:  64px;
  --text-6xl:  84px;

  --leading-tight:   1.05;
  --leading-snug:    1.15;
  --leading-normal:  1.45;
  --leading-relaxed: 1.55;
  --leading-loose:   1.7;

  --weight-light:    300;
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;
  --weight-black:    800;

  --tracking-tightest: -0.04em;   /* display */
  --tracking-tighter:  -0.035em;  /* h1/h2 */
  --tracking-tight:    -0.025em;  /* h3/h4 */
  --tracking-snug:     -0.015em;
  --tracking-normal:    0;
  --tracking-wide:      0.05em;
  --tracking-wider:     0.12em;   /* eyebrow */
  --tracking-widest:    0.16em;   /* mono caps */

  /* ── SPACE (4-px scale) ───────────────────────────────────────── */
  --space-0:   0;
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-7:   28px;
  --space-8:   32px;
  --space-9:   36px;
  --space-10:  40px;
  --space-12:  48px;
  --space-14:  56px;
  --space-16:  64px;
  --space-20:  80px;
  --space-24:  96px;
  --space-28:  112px;
  --space-32:  128px;
  --space-40:  160px;
  --space-48:  192px;

  --container-max:    1240px;
  --container-narrow: 880px;
  --container-wide:   1480px;

  --gutter: clamp(20px, 4vw, 56px);
  --section-y: clamp(48px, 6vw, 80px);
  --chapter-y: clamp(72px, 9vw, 128px);

  /* ── RADIUS ───────────────────────────────────────────────────── */
  --radius-none:  0;
  --radius-xs:    2px;
  --radius-sm:    4px;
  --radius-md:    6px;
  --radius-lg:    10px;
  --radius-xl:    14px;
  --radius-2xl:   20px;
  --radius-3xl:   28px;
  --radius-pill:  999px;
  --radius-full:  9999px;

  /* ── SHADOW ───────────────────────────────────────────────────── */
  --shadow-none: none;
  --shadow-1: 0 1px 2px rgba(26, 22, 20, 0.04), 0 1px 1px rgba(26, 22, 20, 0.03);
  --shadow-2: 0 2px 8px rgba(26, 22, 20, 0.06), 0 1px 2px rgba(26, 22, 20, 0.04);
  --shadow-3: 0 8px 24px rgba(26, 22, 20, 0.08), 0 2px 6px rgba(26, 22, 20, 0.05);
  --shadow-4: 0 20px 50px rgba(26, 22, 20, 0.12), 0 6px 16px rgba(26, 22, 20, 0.06);
  --shadow-5: 0 32px 80px rgba(26, 22, 20, 0.18), 0 12px 24px rgba(26, 22, 20, 0.08);
  --shadow-inset: inset 0 1px 2px rgba(26, 22, 20, 0.06);
  --shadow-focus: 0 0 0 3px rgba(122, 18, 24, 0.18);
  --shadow-focus-soft: 0 0 0 3px rgba(122, 18, 24, 0.10);

  /* ── MOTION ───────────────────────────────────────────────────── */
  --duration-instant: 0ms;
  --duration-fast:    120ms;
  --duration-base:    200ms;
  --duration-medium:  320ms;
  --duration-slow:    520ms;
  --duration-slower:  800ms;

  --ease-linear:  linear;
  --ease-out:     cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in:      cubic-bezier(0.42, 0, 0.84, 0);
  --ease-in-out:  cubic-bezier(0.65, 0, 0.35, 1);
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-emph:    cubic-bezier(0.2, 0.8, 0.2, 1.0);

  /* ════════════════════════════════════════════════════════════════
     SEMANTIC TOKENS — map primitives to meaning.
     Components reference these, NOT raw --color-* / --space-*.
     ════════════════════════════════════════════════════════════════ */

  --surface-page:     var(--color-paper-1);
  --surface-1:        var(--color-paper-1);
  --surface-2:        var(--color-paper-2);
  --surface-3:        var(--color-paper-3);
  --surface-card:     var(--color-white);
  --surface-overlay:  rgba(26, 22, 20, 0.45);

  --text-primary:     var(--color-ink-1);
  --text-strong:      var(--color-ink-2);
  --text-body:        var(--color-ink-3);
  --text-muted:       var(--color-ink-4);
  --text-faint:       var(--color-ink-5);
  --text-on-crimson:  #F0EFEC;
  --text-link:        var(--color-ink-1);
  --text-link-hover:  var(--color-crimson);
  --text-crimson:     var(--color-crimson);

  --border-subtle:    var(--color-line-soft);
  --border-default:   var(--color-line);
  --border-strong:    var(--color-ink-2);

  --action-primary:        var(--color-crimson);
  --action-primary-hover:  var(--color-crimson-d);
  --action-primary-tint:   var(--color-crimson-l);

  /* Status colors.
     IMPORTANT: --status-danger uses crimson per design call (consistent
     "something wrong" signal). DO NOT introduce a separate red. */
  --status-success: #2D6A4F;
  --status-warning: var(--color-gold);
  --status-danger:      var(--color-crimson);
  --status-danger-tint: var(--color-crimson-l);
  --status-info:    #2B5F87;
}

/* ════════════════════════════════════════════════════════════════
   DARK THEME — opt-in via <html data-theme="dark">
   Only color + shadow tokens override. Everything else stays.
   ════════════════════════════════════════════════════════════════ */

[data-theme="dark"] {
  /* Surfaces — neutral with faint warmth (R is 1–2 points above G/B). */
  --color-paper-1:  #131211;   /* page */
  --color-paper-2:  #1F1E1C;   /* card / hero panel */
  --color-paper-3:  #2B2A27;   /* sunken */

  --color-ink-1:    #EBE6D7;   /* warm off-white (cream on dark paper) */
  --color-ink-2:    #CFCABC;
  --color-ink-3:    #A8A398;
  --color-ink-4:    #74706A;
  --color-ink-5:    #454340;

  --color-line:       rgba(235, 230, 215, 0.12);
  --color-line-soft:  rgba(235, 230, 215, 0.06);

  /* Crimson lifts in dark mode for chip-scale legibility on near-black. */
  --color-crimson:    #8C2A2F;
  --color-crimson-d:  #6E1F23;
  --color-crimson-l:  rgba(140, 42, 47, 0.20);

  /* Re-map semantic surfaces under dark */
  --surface-card:    var(--color-paper-2);
  --surface-overlay: rgba(0, 0, 0, 0.65);

  /* Text-on-crimson warmer to harmonize with cream-ink palette */
  --text-on-crimson: #F5F2EC;

  /* Crimson tuned for use as text/border on dark (passes WCAG AA on #0F0D0C) */
  --text-crimson:    #B83A3F;
  --text-link-hover: #C25560;

  --status-danger:      #B83A3F;
  --status-danger-tint: rgba(184, 58, 63, 0.18);

  --shadow-1: 0 1px 2px rgba(0, 0, 0, 0.30), 0 1px 1px rgba(0, 0, 0, 0.20);
  --shadow-2: 0 2px 8px rgba(0, 0, 0, 0.35), 0 1px 2px rgba(0, 0, 0, 0.25);
  --shadow-3: 0 8px 24px rgba(0, 0, 0, 0.45), 0 2px 6px rgba(0, 0, 0, 0.30);
  --shadow-4: 0 20px 50px rgba(0, 0, 0, 0.55), 0 6px 16px rgba(0, 0, 0, 0.35);
  --shadow-5: 0 32px 80px rgba(0, 0, 0, 0.65), 0 12px 24px rgba(0, 0, 0, 0.45);
  --shadow-inset: inset 0 1px 2px rgba(0, 0, 0, 0.40);
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast:    0ms;
    --duration-base:    0ms;
    --duration-medium:  0ms;
    --duration-slow:    0ms;
    --duration-slower:  0ms;
  }
}

/* ── Base page styles ── */
html, body { margin: 0; padding: 0; }
html { background: var(--surface-page); color: var(--text-primary); }
body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  background: var(--surface-page);
  color: var(--text-primary);
}
```

---

## 5. Dark Theme — How to Apply

### Toggling

```html
<html lang="en" data-theme="light">   <!-- default -->
<html lang="en" data-theme="dark">    <!-- dark mode -->
```

### What auto-adapts (no extra code)
- All `var(--text-*)`, `var(--surface-*)`, `var(--border-*)`, `var(--action-*)`, `var(--status-*)` consumers
- All `var(--color-*)` consumers (crimson lifts, ink inverts, paper darkens)
- All shadows
- Every component primitive in §6 (they all use semantic tokens)

### What does NOT auto-adapt
- **Inline `style="background:#7A1218"`** — bypasses tokens. Always use CSS vars or className.
- **Hardcoded hex in component JSX** — replace with `var(--text-primary)` etc.
- **SVG logos** — the SVG `fill="#7A1218"` is baked in. Use the React component pattern in §3 with conditional fills.
- **Images / photos** — won't auto-invert. Provide light/dark sources if needed.

### React toggle pattern

```tsx
const [isDark, setIsDark] = useState(false);
useEffect(() => {
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
}, [isDark]);

return (
  <button
    onClick={() => setIsDark(!isDark)}
    aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
    style={{
      width: 40, height: 40, borderRadius: '50%',
      background: 'transparent',
      border: '1px solid var(--border-default)',
      color: 'var(--text-primary)',
      cursor: 'pointer',
    }}
  >
    {isDark ? '☀' : '☾'}
  </button>
);
```

---

## 6. Primitive Components

Six primitives. Each is framework-agnostic CSS that decorates standard HTML elements. The browser's native form/button semantics are preserved — labels click-toggle, autofill works, password managers work, screen readers work.

**Required classes (use these — don't author new ones):**

```
.kb         button (any variant)
.kf-input   text inputs, selects, textarea
.kf-check   checkbox + radio (same primitive, input[type] picks shape)
.kf-switch  toggle switch
.kf-field   label + control + hint + validation wrapper
.kf-date    date picker (uses .kf-input + popover)
```

To re-skin a single instance, override component-local custom properties (`--kb-bg`, `--kf-border-focus`, etc.) via `style="..."` — never re-target the class.

### 6a. Button — `.kb`

```css
:where(.kb) {
  --kb-bg:           transparent;
  --kb-fg:           var(--text-primary);
  --kb-border:       transparent;
  --kb-bg-hover:     transparent;
  --kb-fg-hover:     var(--text-primary);
  --kb-border-hover: transparent;
  --kb-ring-color:   var(--text-primary);
  --kb-focus-ring:   color-mix(in oklch, var(--color-crimson) 55%, transparent);
}

.kb {
  font-family: var(--font-mono);
  font-weight: 500;
  letter-spacing: 0.10em;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid var(--kb-border);
  background: var(--kb-bg);
  color: var(--kb-fg);
  white-space: nowrap;
  position: relative;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  text-decoration: none;
  transition:
    background-color .2s cubic-bezier(0.25,0.1,0.25,1),
    color           .2s cubic-bezier(0.25,0.1,0.25,1),
    border-color    .2s cubic-bezier(0.25,0.1,0.25,1),
    box-shadow      .2s cubic-bezier(0.25,0.1,0.25,1),
    transform       .15s cubic-bezier(0.25,0.1,0.25,1);
}
.kb:hover:not(:disabled):not(.disabled):not([data-loading]):not([data-success]) {
  background: var(--kb-bg-hover);
  color: var(--kb-fg-hover);
  border-color: var(--kb-border-hover);
}
.kb:active:not(:disabled):not(.disabled):not([data-loading]):not([data-success]) {
  transform: scale(0.97);
}
.kb:focus-visible {
  outline: none;
  box-shadow: 0 0 0 4px var(--kb-focus-ring);
}

.kb-sm { padding: 5px 14px; font-size: 11px; }
.kb-md { padding: 7px 18px; font-size: 12px; }
.kb-lg { padding: 9px 22px; font-size: 13px; }

.kb-icon.kb-sm { padding: 5px;  width: 26px; height: 26px; }
.kb-icon.kb-md { padding: 7px;  width: 30px; height: 30px; }
.kb-icon.kb-lg { padding: 9px;  width: 36px; height: 36px; }
.kb-icon { gap: 0; }

/* Variants — hover principle: same hue, brighter (lift toward white), never darker. */
.kb.kb-primary {
  --kb-bg:           var(--color-crimson);
  --kb-fg:           var(--text-on-crimson);
  --kb-border:       var(--color-crimson);
  --kb-bg-hover:     color-mix(in oklch, var(--color-crimson) 90%, #fff);
  --kb-fg-hover:     var(--text-on-crimson);
  --kb-border-hover: color-mix(in oklch, var(--color-crimson) 90%, #fff);
  --kb-ring-color:   var(--color-crimson);
}
.kb.kb-accent {
  /* Ink-on-paper, both surfaces inverted (flips with dark theme). */
  --kb-bg:           var(--color-ink-1);
  --kb-fg:           var(--color-paper-1);
  --kb-border:       var(--color-ink-1);
  --kb-bg-hover:     color-mix(in oklch, var(--color-ink-1) 92%, #fff);
  --kb-fg-hover:     var(--color-paper-1);
  --kb-border-hover: color-mix(in oklch, var(--color-ink-1) 92%, #fff);
  --kb-ring-color:   var(--color-ink-1);
}
.kb.kb-secondary {
  --kb-bg:           var(--surface-card);
  --kb-fg:           var(--text-primary);
  --kb-border:       var(--border-default);
  --kb-bg-hover:     var(--surface-card);
  --kb-fg-hover:     var(--text-primary);
  --kb-border-hover: color-mix(in oklch, var(--text-primary) 28%, transparent);
  --kb-ring-color:   var(--text-primary);
}
.kb.kb-ghost {
  --kb-bg:           transparent;
  --kb-fg:           var(--text-primary);
  --kb-border:       transparent;
  --kb-bg-hover:     color-mix(in oklch, var(--text-primary) 5%, transparent);
  --kb-fg-hover:     var(--text-primary);
  --kb-border-hover: transparent;
  --kb-ring-color:   var(--text-primary);
}
.kb.kb-danger {
  --kb-bg:           transparent;
  --kb-fg:           var(--text-crimson);
  --kb-border:       var(--text-crimson);
  --kb-bg-hover:     color-mix(in oklch, var(--text-crimson) 10%, transparent);
  --kb-fg-hover:     var(--text-crimson);
  --kb-border-hover: var(--text-crimson);
  --kb-ring-color:   var(--text-crimson);
}

/* Link variants */
.kb.kb-link,
.kb.kb-link-grow {
  background: transparent;
  color: var(--text-primary);
  border: none;
  padding: 6px 2px;
  font-weight: 500;
  font-size: 12px;
  gap: 6px;
  border-radius: 0;
  text-transform: uppercase;
  letter-spacing: 0.10em;
  text-decoration: none;
  position: relative;
  --kb-ring-color: var(--text-primary);
  --kb-bg-hover: transparent;
  --kb-fg-hover: var(--text-link-hover);
  --kb-border-hover: transparent;
  transition: color .2s cubic-bezier(0.25,0.1,0.25,1);
}
.kb.kb-link::before,
.kb.kb-link::after,
.kb.kb-link-grow::before {
  content: "";
  position: absolute;
  left: 0; right: 0;
  bottom: 0;
  height: 1px;
  pointer-events: none;
  transition: transform .4s cubic-bezier(0.65, 0, 0.35, 1);
}
.kb.kb-link::before,
.kb.kb-link-grow::before {
  background: var(--text-link-hover);
  transform: scaleX(0);
  transform-origin: left center;
}
.kb.kb-link:hover::before,
.kb.kb-link-grow:hover::before { transform: scaleX(1); }
.kb.kb-link::after {
  background: currentColor;
  transform: scaleX(1);
  transform-origin: right center;
}
.kb.kb-link:hover::after { transform: scaleX(0); }
.kb.kb-link:hover,
.kb.kb-link-grow:hover { color: var(--text-link-hover); }
.kb.kb-link:visited,
.kb.kb-link-grow:visited { color: var(--text-primary); }

/* Disabled */
.kb:disabled,
.kb.disabled,
.kb[aria-disabled="true"] {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

/* Loading + success — CSS-only fallback (script in §6g upgrades to orbit ring) */
.kb[data-loading],
.kb[data-success] { pointer-events: none; position: relative; }

.kb[data-loading] {
  color: transparent !important;
  text-shadow: none !important;
}
.kb[data-loading] > * { visibility: hidden; }
.kb[data-loading]::before {
  content: "";
  position: absolute;
  left: 50%; top: 50%;
  width: 14px; height: 14px;
  margin: -7px 0 0 -7px;
  background: transparent;
  border-radius: 50%;
  border: 1.5px solid currentColor;
  border-top-color: transparent;
  color: var(--kb-ring-color);
  animation: kb-spin .8s linear infinite;
}
.kb-sm[data-loading]::before { width: 12px; height: 12px; margin: -6px 0 0 -6px; }
.kb-lg[data-loading]::before { width: 16px; height: 16px; margin: -8px 0 0 -8px; border-width: 2px; }

.kb.kb-orbit[data-loading] { color: var(--kb-fg) !important; }
.kb.kb-orbit[data-loading] > * { visibility: visible; }
.kb.kb-orbit[data-loading]::before { display: none; }

@keyframes kb-spin { to { transform: rotate(360deg); } }

.kb[data-success]:not(.kb-ring-forming) {
  color: transparent !important;
  text-shadow: none !important;
}
.kb[data-success]:not(.kb-ring-forming) > *:not(.kb-loader):not(.kb-check) {
  opacity: 0;
  transition: opacity .22s ease;
}
.kb[data-success]::before { display: none; }

.kb-loader {
  position: absolute;
  top: -6px; bottom: -6px;
  left: -8px; right: -8px;
  width: calc(100% + 16px) !important;
  height: calc(100% + 12px) !important;
  pointer-events: none;
  overflow: visible;
  color: var(--kb-ring-color);
  transform: none !important;
  stroke: none;
}
.kb-loader rect {
  fill: none;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
}

.kb-check {
  position: absolute;
  left: 50%; top: 50%;
  width: 18px; height: 18px;
  margin: -9px 0 0 -9px;
  pointer-events: none;
  opacity: 0;
  transition: opacity .2s ease .08s;
  transform: none !important;
}
.kb-sm .kb-check { width: 14px; height: 14px; margin: -7px 0 0 -7px; }
.kb-lg .kb-check { width: 20px; height: 20px; margin: -10px 0 0 -10px; }
.kb-check path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 24;
  stroke-dashoffset: 24;
  transition: stroke-dashoffset .55s cubic-bezier(0.65, 0, 0.35, 1) .18s;
}
.kb[data-success]:not(.kb-ring-forming) .kb-check { opacity: 1; }
.kb[data-success]:not(.kb-ring-forming) .kb-check path { stroke-dashoffset: 0; }

.kb.kb-primary   .kb-check { color: var(--text-on-crimson); }
.kb.kb-accent    .kb-check { color: var(--color-paper-1); }
.kb.kb-secondary .kb-check,
.kb.kb-ghost     .kb-check,
.kb.kb-link      .kb-check,
.kb.kb-link-grow .kb-check { color: var(--text-primary); }
.kb.kb-danger    .kb-check { color: var(--text-crimson); }

@media (prefers-reduced-motion: reduce) {
  .kb-loader rect { display: none; }
  .kb-check path { transition: none; stroke-dashoffset: 0; }
  .kb { transition: none; }
  .kb[data-loading]::before { animation: none; border-top-color: currentColor; opacity: 0.4; }
}

/* Icons inside .kb — right-side .arr-svg translates on hover */
.kb svg,
.kb .arr-svg {
  width: 14px; height: 14px;
  flex-shrink: 0;
  display: block;
  stroke: currentColor;
  stroke-width: 1.5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
  transition: transform .25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.kb-sm svg, .kb-sm .arr-svg { width: 12px; height: 12px; }
.kb-lg svg, .kb-lg .arr-svg { width: 15px; height: 15px; }
.kb-icon.kb-sm svg { width: 14px; height: 14px; }
.kb-icon.kb-md svg { width: 16px; height: 16px; }
.kb-icon.kb-lg svg { width: 18px; height: 18px; }

.kb:hover > .arr-svg:last-child,
.kb:hover > svg.arr-svg:last-child { transform: translateX(3px); }
.kb:hover > svg:first-child:not(.arr-svg),
.kb:hover > .arr-svg:first-child:not(:last-child) { transform: scale(1.08); }
.kb:hover > .kb-loader,
.kb:hover > .kb-check { transform: none !important; }
```

**API**

| Slot | Classes |
|------|---------|
| Base | `kb` (required) |
| Size | `kb-sm` · `kb-md` · `kb-lg` |
| Variant | `kb-primary` · `kb-accent` · `kb-secondary` · `kb-ghost` · `kb-danger` · `kb-link` · `kb-link-grow` |
| Modifier | `kb-icon` (square, icon-only — pair with `aria-label`) |

| State | Trigger |
|-------|---------|
| Hover | `:hover` |
| Focus | `:focus-visible` — crimson glow ring |
| Press | `:active` — `scale(0.97)` |
| Disabled | `disabled` attr or `class="disabled"` |
| Loading | `data-loading` attr |
| Success | `data-success` attr |

**Examples**

```jsx
<button className="kb kb-md kb-primary">Save</button>
<button className="kb kb-md kb-accent">Continue</button>
<button className="kb kb-md kb-secondary">Cancel</button>
<button className="kb kb-md kb-ghost">Skip</button>
<button className="kb kb-md kb-danger">Delete</button>
<a className="kb kb-md kb-link" href="/docs">Read the docs</a>
<a className="kb kb-md kb-link-grow" href="/catalog">Browse catalog</a>

{/* Icon-only */}
<button className="kb kb-md kb-secondary kb-icon" aria-label="Close">
  <svg viewBox="0 0 16 16"><path d="M4 4l8 8M12 4l-8 8"/></svg>
</button>

{/* With trailing arrow that animates on hover — mark icon class="arr-svg" */}
<button className="kb kb-md kb-primary">
  Continue
  <svg className="arr-svg" viewBox="0 0 16 16">
    <path d="M3 8h10M9 4l4 4-4 4"/>
  </svg>
</button>

{/* Loading + success flow (works without JS — orbit ring loads via §6g) */}
<button className="kb kb-md kb-primary" data-loading="">Saving</button>
<button className="kb kb-md kb-primary" data-success="">Saved</button>

{/* React with state */}
<button
  className="kb kb-md kb-primary"
  {...(loading && { 'data-loading': '' })}
  {...(success && { 'data-success': '' })}
  onClick={save}
>
  Save changes
</button>
```

### 6b. Input — `.kf-input`

Decorates native `<input>` (every text type), `<select>`, `<textarea>`. Browser semantics preserved.

```css
.kf-input,
:where(.kf-input) {
  --kf-bg:            var(--surface-card);
  --kf-bg-hover:      var(--surface-card);
  --kf-bg-disabled:   var(--surface-3);
  --kf-fg:            var(--text-primary);
  --kf-fg-placeholder:var(--text-faint);
  --kf-border:        var(--border-default);
  --kf-border-hover:  var(--border-strong);
  --kf-border-focus:  var(--text-primary);
  --kf-ring-color:    var(--text-primary);
  --kf-ring-alpha:    0.10;
  --kf-radius:        var(--radius-sm);
  --kf-h:             40px;
  --kf-pad-x:         var(--space-3);
  --kf-font-size:     var(--text-sm);

  box-sizing: border-box;
  width: 100%;
  height: var(--kf-h);
  padding: 0 var(--kf-pad-x);
  margin: 0;
  background: var(--kf-bg);
  color: var(--kf-fg);
  border: 1px solid var(--kf-border);
  border-radius: var(--kf-radius);
  font-family: var(--font-sans);
  font-size: var(--kf-font-size);
  line-height: 1.4;
  font-weight: var(--weight-regular);
  appearance: none;
  -webkit-appearance: none;
  outline: none;
  transition:
    border-color  var(--duration-base) var(--ease-out),
    background    var(--duration-base) var(--ease-out),
    box-shadow    var(--duration-base) var(--ease-out),
    color         var(--duration-base) var(--ease-out);
}
.kf-input::placeholder { color: var(--kf-fg-placeholder); opacity: 1; }

.kf-input.kf-sm { --kf-h: 32px; --kf-pad-x: var(--space-3); --kf-font-size: var(--text-xs);  }
.kf-input.kf-md { --kf-h: 40px; --kf-pad-x: var(--space-3); --kf-font-size: var(--text-sm);  }
.kf-input.kf-lg { --kf-h: 48px; --kf-pad-x: var(--space-4); --kf-font-size: var(--text-base);}

.kf-input:hover:not(:disabled):not([data-state]) { border-color: var(--kf-border-hover); }
.kf-input:focus {
  border-color: var(--kf-border-focus);
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--kf-ring-color) 12%, transparent);
}
.kf-input:disabled,
.kf-input[disabled] {
  background: var(--kf-bg-disabled);
  color: var(--text-faint);
  cursor: not-allowed;
  border-color: var(--border-subtle);
}
.kf-input:disabled::placeholder,
.kf-input[disabled]::placeholder { color: var(--text-faint); }

/* Validation states */
.kf-input[data-state="error"]   { --kf-border-state: var(--status-danger);  border-color: var(--kf-border-state); --kf-ring-color: var(--status-danger); }
.kf-input[data-state="warn"]    { --kf-border-state: var(--color-gold);     border-color: var(--kf-border-state); --kf-ring-color: var(--color-gold); }
.kf-input[data-state="success"] { --kf-border-state: var(--status-success); border-color: var(--kf-border-state); --kf-ring-color: var(--status-success); }
.kf-input[data-state]:hover:not(:disabled) { border-color: var(--kf-border-state); }
.kf-input[data-state]:focus {
  border-color: var(--kf-border-state);
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--kf-ring-color) 16%, transparent);
}

.kf-input[readonly] { background: var(--surface-3); cursor: default; }
.kf-input[readonly]:focus { box-shadow: none; }

/* Search — hide native cancel button */
.kf-input[type="search"]::-webkit-search-decoration,
.kf-input[type="search"]::-webkit-search-cancel-button,
.kf-input[type="search"]::-webkit-search-results-button,
.kf-input[type="search"]::-webkit-search-results-decoration { -webkit-appearance: none; }

/* Number — hide native steppers (we ship our own .kf-input-stepper) */
.kf-input[type="number"]::-webkit-inner-spin-button,
.kf-input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
.kf-input[type="number"] { -moz-appearance: textfield; }

.kf-input[type="date"]::-webkit-calendar-picker-indicator,
.kf-input[type="time"]::-webkit-calendar-picker-indicator,
.kf-input[type="datetime-local"]::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.55;
  filter: var(--kf-picker-filter, none);
}
.kf-input[type="date"]:hover::-webkit-calendar-picker-indicator,
.kf-input[type="time"]:hover::-webkit-calendar-picker-indicator,
.kf-input[type="datetime-local"]:hover::-webkit-calendar-picker-indicator { opacity: 1; }

textarea.kf-input {
  height: auto;
  min-height: calc(var(--kf-h) * 2);
  padding-top: var(--space-2);
  padding-bottom: var(--space-2);
  resize: vertical;
  line-height: var(--leading-normal);
}

select.kf-input {
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none' stroke='%238A857D' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round'><polyline points='3,4.5 6,7.5 9,4.5'/></svg>");
  background-position: right var(--space-3) center;
  background-size: 12px 12px;
  background-repeat: no-repeat;
  padding-right: calc(var(--space-3) * 2 + 12px);
  cursor: pointer;
}
[data-theme="dark"] select.kf-input {
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none' stroke='%237A7368' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round'><polyline points='3,4.5 6,7.5 9,4.5'/></svg>");
}

/* Wrap for slots (lead icon, trail button, stepper) */
.kf-input-wrap { position: relative; width: 100%; display: block; }
.kf-input-wrap.has-lead  .kf-input { padding-left:  calc(var(--space-4) + 24px); }
.kf-input-wrap.has-trail .kf-input { padding-right: calc(var(--space-4) + 28px); }
.kf-input-wrap.has-trail select.kf-input { background-image: none; padding-right: calc(var(--space-3) + 28px); }

.kf-input-lead {
  position: absolute;
  left: var(--space-3); top: 50%;
  transform: translateY(-50%);
  display: flex; align-items: center;
  color: var(--text-muted);
  pointer-events: none;
  line-height: 0;
}
.kf-input-lead svg { display: block; }

.kf-input-trail {
  position: absolute;
  right: var(--space-2); top: 50%;
  transform: translateY(-50%);
  height: calc(var(--kf-h, 40px) - 14px);
  padding: 0 var(--space-3);
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xs);
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: var(--text-2xs);
  font-weight: var(--weight-semibold);
  letter-spacing: var(--tracking-widest);
  text-transform: uppercase;
  cursor: pointer;
  transition: color var(--duration-fast), border-color var(--duration-fast);
}
.kf-input-trail:hover { color: var(--text-primary); border-color: var(--text-primary); }
.kf-input-trail:disabled { opacity: 0.4; cursor: not-allowed; }

.kf-input-trail-icon {
  position: absolute;
  right: var(--space-3); top: 50%;
  transform: translateY(-50%);
  display: flex; align-items: center; justify-content: center;
  width: 20px; height: 20px;
  color: var(--text-muted);
  pointer-events: none;
  line-height: 0;
}
.kf-input-trail-icon svg { display: block; }
button.kf-input-trail-icon {
  background: transparent;
  border: none;
  border-radius: var(--radius-xs);
  width: 24px; height: 24px;
  cursor: pointer;
  pointer-events: auto;
  transition: color var(--duration-fast), background var(--duration-fast);
}
button.kf-input-trail-icon:hover {
  color: var(--text-primary);
  background: color-mix(in oklch, var(--text-primary) 6%, transparent);
}

.kf-input-stepper {
  position: absolute;
  right: 4px; top: 50%;
  transform: translateY(-50%);
  display: flex; flex-direction: column; gap: 1px;
}
.kf-input-stepper button {
  width: 22px; height: 16px;
  padding: 0;
  display: flex; align-items: center; justify-content: center;
  background: var(--surface-card);
  border: 1px solid var(--border-default);
  color: var(--text-muted);
  font-family: var(--font-mono); font-size: 11px; font-weight: 600;
  cursor: pointer; line-height: 1;
  transition: color var(--duration-fast), border-color var(--duration-fast);
}
.kf-input-stepper button:hover { color: var(--text-primary); border-color: var(--text-primary); }
.kf-input-stepper button:first-child { border-radius: var(--radius-xs) var(--radius-xs) 0 0; }
.kf-input-stepper button:last-child  { border-radius: 0 0 var(--radius-xs) var(--radius-xs); }
.kf-input-stepper button:disabled { opacity: 0.4; cursor: not-allowed; }
.kf-input-wrap:has(.kf-input-stepper) > .kf-input { padding-right: 32px; }

.kf-input-wrap.kf-sm .kf-input-trail { height: 22px; padding: 0 var(--space-2); }
.kf-input-wrap.kf-lg .kf-input-trail { height: 32px; padding: 0 var(--space-3); }

[data-theme="dark"] .kf-input {
  --kf-bg:            color-mix(in oklch, var(--text-primary) 4%, transparent);
  --kf-bg-hover:      color-mix(in oklch, var(--text-primary) 6%, transparent);
  --kf-bg-disabled:   color-mix(in oklch, var(--text-primary) 2%, transparent);
  --kf-border:        color-mix(in oklch, var(--text-primary) 22%, transparent);
  --kf-border-hover:  color-mix(in oklch, var(--text-primary) 40%, transparent);
  --kf-picker-filter: invert(1) brightness(1.4);
}

@media (prefers-reduced-motion: reduce) {
  .kf-input, .kf-input-trail, .kf-input-stepper button { transition: none; }
}
```

**Examples**

```jsx
{/* Bare */}
<input className="kf-input kf-md" type="email" placeholder="you@company.com" />
<textarea className="kf-input kf-md" rows={3} />
<select className="kf-input kf-md">
  <option>Tier 1 · MAP</option>
  <option>Tier 2 · MSRP</option>
</select>

{/* Sizes — kf-sm | kf-md | kf-lg */}
<input className="kf-input kf-sm" />  {/* 32px */}
<input className="kf-input kf-md" />  {/* 40px (default) */}
<input className="kf-input kf-lg" />  {/* 48px touch */}

{/* Validation states */}
<input className="kf-input kf-md" data-state="error" />
<input className="kf-input kf-md" data-state="warn" />
<input className="kf-input kf-md" data-state="success" />

{/* With lead icon (search) */}
<div className="kf-input-wrap kf-md has-lead">
  <span className="kf-input-lead">
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
      <circle cx="7" cy="7" r="5"/><path d="m11 11 3 3"/>
    </svg>
  </span>
  <input className="kf-input kf-md" type="search" placeholder="Search products" />
</div>

{/* With trailing text button (e.g. password Show) */}
<div className="kf-input-wrap kf-md has-trail">
  <input className="kf-input kf-md" type="password" />
  <button type="button" className="kf-input-trail">Show</button>
</div>

{/* Number stepper */}
<div className="kf-input-wrap kf-md">
  <input className="kf-input kf-md" type="number" defaultValue={3} />
  <span className="kf-input-stepper">
    <button type="button">+</button>
    <button type="button">−</button>
  </span>
</div>
```

### 6c. Check — `.kf-check` (checkbox + radio)

One class for both. `<input type>` decides shape — square (checkbox) or circle (radio).

```css
.kf-check,
:where(.kf-check) {
  --kfc-size:           18px;
  --kfc-bg:             var(--surface-card);
  --kfc-bg-checked:     var(--text-crimson);
  --kfc-border:         var(--border-default);
  --kfc-border-hover:   var(--text-muted);
  --kfc-border-checked: var(--text-crimson);
  --kfc-fg:             var(--text-on-crimson);
  --kfc-ring-color:     var(--text-crimson);

  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  user-select: none;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  line-height: var(--leading-snug);
  color: var(--text-body);
}
.kf-check:has(.kf-check-hint) { align-items: flex-start; }

.kf-check > input[type="checkbox"],
.kf-check > input[type="radio"] {
  position: absolute;
  width: var(--kfc-size); height: var(--kfc-size);
  margin: 0;
  opacity: 0;
  cursor: inherit;
  top: 1px; left: 0;
  z-index: 1;
}

.kf-check-box {
  flex: 0 0 auto;
  width: var(--kfc-size); height: var(--kfc-size);
  background: var(--kfc-bg);
  border: 1.5px solid var(--kfc-border);
  border-radius: var(--radius-xs);
  position: relative;
  transition:
    background var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
  color: var(--kfc-fg);
}
.kf-check:has(.kf-check-hint) > .kf-check-box { margin-top: 2px; }
.kf-check > input[type="radio"] ~ .kf-check-box { border-radius: 50%; }

.kf-check-box::after {
  content: "";
  position: absolute;
  opacity: 0;
  transform: scale(0.6);
  transition:
    opacity var(--duration-fast) var(--ease-out),
    transform var(--duration-base) var(--ease-spring);
}

.kf-check > input[type="checkbox"] ~ .kf-check-box::after {
  width: calc(var(--kfc-size) * 0.7);
  height: calc(var(--kfc-size) * 0.7);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0.6);
  background: currentColor;
  -webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='3.5,8.5 6.5,11.5 12.5,5'/></svg>");
          mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='none' stroke='black' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><polyline points='3.5,8.5 6.5,11.5 12.5,5'/></svg>");
  -webkit-mask-size: contain; mask-size: contain;
  -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
  -webkit-mask-position: center; mask-position: center;
}
.kf-check > input[type="radio"] ~ .kf-check-box::after {
  width: calc(var(--kfc-size) * 0.4);
  height: calc(var(--kfc-size) * 0.4);
  border-radius: 50%;
  background: currentColor;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0.6);
}

.kf-check-label { flex: 1 1 auto; padding-top: 0; }
.kf-check-hint {
  display: block;
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-top: var(--space-1);
  line-height: var(--leading-snug);
}

.kf-check.kf-sm { --kfc-size: 14px; font-size: var(--text-xs); }
.kf-check.kf-md { --kfc-size: 18px; font-size: var(--text-sm); }
.kf-check.kf-lg { --kfc-size: 22px; font-size: var(--text-base); }

.kf-check:hover > .kf-check-box { border-color: var(--kfc-border-hover); }
.kf-check > input:focus-visible ~ .kf-check-box {
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--kfc-ring-color) 22%, transparent);
}
.kf-check > input:checked ~ .kf-check-box {
  background: var(--kfc-bg-checked);
  border-color: var(--kfc-border-checked);
}
.kf-check > input:checked ~ .kf-check-box::after { opacity: 1; }
.kf-check > input[type="checkbox"]:checked ~ .kf-check-box::after,
.kf-check > input[type="radio"]:checked ~ .kf-check-box::after {
  transform: translate(-50%, -50%) scale(1);
}

/* Indeterminate (checkbox only) — solid bar */
.kf-check > input[type="checkbox"]:indeterminate ~ .kf-check-box {
  background: var(--kfc-bg-checked);
  border-color: var(--kfc-border-checked);
}
.kf-check > input[type="checkbox"]:indeterminate ~ .kf-check-box::after {
  width: calc(var(--kfc-size) * 0.5);
  height: 2px;
  border: none;
  background: currentColor;
  border-radius: 1px;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  opacity: 1;
  margin: 0;
  -webkit-mask-image: none; mask-image: none;
}

.kf-check:has(> input:disabled),
.kf-check.disabled { cursor: not-allowed; color: var(--text-faint); }
.kf-check:has(> input:disabled) > .kf-check-box,
.kf-check.disabled > .kf-check-box {
  background: var(--surface-3);
  border-color: var(--border-subtle);
}
.kf-check:has(> input:disabled:checked) > .kf-check-box {
  background: var(--text-faint);
  border-color: var(--text-faint);
}

.kf-check[data-state="error"] {
  --kfc-border:         var(--status-danger);
  --kfc-border-hover:   var(--status-danger);
  --kfc-ring-color:     var(--status-danger);
}

/* Group layouts */
.kf-check-stack { display: flex; flex-direction: column; gap: var(--space-3); }
.kf-check-row { display: flex; flex-wrap: wrap; gap: var(--space-5); }

@media (prefers-reduced-motion: reduce) {
  .kf-check-box, .kf-check-box::after { transition: none; }
}

[data-theme="dark"] .kf-check {
  --kfc-bg: transparent;
  --kfc-bg-checked:     var(--color-crimson);
  --kfc-border-checked: var(--color-crimson);
  --kfc-fg:             var(--text-on-crimson);
  --kfc-ring-color:     var(--color-crimson);
}
```

**Required structure: `input` + `.kf-check-box` + `.kf-check-label` (in that order, all 3 inside `<label class="kf-check">`).**

```jsx
{/* Checkbox */}
<label className="kf-check">
  <input type="checkbox" />
  <span className="kf-check-box"></span>
  <span className="kf-check-label">Email me product updates</span>
</label>

{/* Radio */}
<label className="kf-check">
  <input type="radio" name="tier" value="1" />
  <span className="kf-check-box"></span>
  <span className="kf-check-label">Tier 1 · MAP</span>
</label>

{/* With hint */}
<label className="kf-check">
  <input type="checkbox" />
  <span className="kf-check-box"></span>
  <span>
    <span className="kf-check-label">Auto-sync to Highpoint</span>
    <span className="kf-check-hint">Sends order data within 5 minutes.</span>
  </span>
</label>

{/* Groups */}
<div className="kf-check-stack">  {/* vertical, gap-3 */}
  <label className="kf-check">...</label>
  <label className="kf-check">...</label>
</div>
<div className="kf-check-row">    {/* horizontal, gap-5, wraps */}
  <label className="kf-check">...</label>
  <label className="kf-check">...</label>
</div>

{/* Indeterminate — set via ref/JS */}
useEffect(() => { ref.current.indeterminate = true; }, []);
```

### 6d. Switch — `.kf-switch`

```css
.kf-switch,
:where(.kf-switch) {
  --kfs-w:           36px;
  --kfs-h:           20px;
  --kfs-thumb:       14px;
  --kfs-pad:         3px;
  --kfs-bg-off:      var(--border-strong);
  --kfs-bg-on:       var(--text-crimson);
  --kfs-thumb-bg:    var(--surface-card);
  --kfs-ring-color:  var(--text-crimson);

  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  cursor: pointer;
  user-select: none;
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  color: var(--text-body);
  line-height: var(--leading-snug);
}

.kf-switch > input[type="checkbox"] {
  position: absolute;
  width: var(--kfs-w); height: var(--kfs-h);
  margin: 0;
  opacity: 0;
  cursor: inherit;
  z-index: 1;
}

.kf-switch-track {
  flex: 0 0 auto;
  width: var(--kfs-w); height: var(--kfs-h);
  background: var(--kfs-bg-off);
  border-radius: 999px;
  position: relative;
  transition:
    background var(--duration-base) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
}

.kf-switch-thumb {
  position: absolute;
  top: var(--kfs-pad);
  left: var(--kfs-pad);
  width: var(--kfs-thumb); height: var(--kfs-thumb);
  background: var(--kfs-thumb-bg);
  border-radius: 50%;
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.15),
    0 0 0 0.5px rgba(0, 0, 0, 0.06);
  transition: transform var(--duration-base) var(--ease-spring);
  display: flex; align-items: center; justify-content: center;
}

.kf-switch-state {
  font-family: var(--font-mono);
  font-size: 0.55em;
  letter-spacing: var(--tracking-wider);
  color: var(--text-primary);
  font-weight: var(--weight-semibold);
  opacity: 0;
  transition: opacity var(--duration-fast);
}

.kf-switch-label { flex: 1 1 auto; }
.kf-switch-hint {
  display: block;
  font-size: var(--text-xs);
  color: var(--text-muted);
  margin-top: var(--space-1);
}

.kf-switch.kf-sm {
  --kfs-w: 28px;  --kfs-h: 16px;  --kfs-thumb: 12px;  --kfs-pad: 2px;
  font-size: var(--text-xs);
}
.kf-switch.kf-lg {
  --kfs-w: 44px;  --kfs-h: 26px;  --kfs-thumb: 20px;  --kfs-pad: 3px;
  font-size: var(--text-base);
}

.kf-switch > input:focus-visible ~ .kf-switch-track {
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--kfs-ring-color) 22%, transparent);
}
.kf-switch > input:checked ~ .kf-switch-track { background: var(--kfs-bg-on); }
.kf-switch > input:checked ~ .kf-switch-track .kf-switch-thumb {
  transform: translateX(calc(var(--kfs-w) - var(--kfs-thumb) - var(--kfs-pad) * 2));
}
.kf-switch > input:checked ~ .kf-switch-track .kf-switch-state { opacity: 1; }

.kf-switch:has(> input:disabled),
.kf-switch.disabled { cursor: not-allowed; color: var(--text-faint); }
.kf-switch:has(> input:disabled) .kf-switch-track,
.kf-switch.disabled .kf-switch-track { opacity: 0.5; }

.kf-switch[data-state="error"] {
  --kfs-bg-off:     var(--status-danger);
  --kfs-ring-color: var(--status-danger);
}

@media (prefers-reduced-motion: reduce) {
  .kf-switch-track, .kf-switch-thumb { transition: none; }
}

[data-theme="dark"] .kf-switch {
  --kfs-bg-off:     var(--color-ink-3);
  --kfs-bg-on:      var(--color-crimson);
  --kfs-thumb-bg:   var(--color-paper-1);
  --kfs-ring-color: var(--color-crimson);
}
```

```jsx
<label className="kf-switch">
  <input type="checkbox" />
  <span className="kf-switch-track">
    <span className="kf-switch-thumb"></span>
  </span>
  <span className="kf-switch-label">Auto-sync orders</span>
</label>

{/* Sizes — kf-sm | kf-md (default) | kf-lg */}
<label className="kf-switch kf-sm">...</label>
<label className="kf-switch kf-lg">...</label>
```

### 6e. Field — `.kf-field`

Wrapper for label + control + hint + validation. Optional but recommended — gives consistent rhythm and one hook for `data-state`.

```css
.kf-field,
:where(.kf-field) {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-family: var(--font-sans);
}
.kf-field > .kf-field-hint,
.kf-field > .kf-field-message,
.kf-field > .kf-field-meta { margin-top: 2px; }
.kf-field.kf-field-tight { gap: var(--space-1); }

.kf-field-label {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: var(--weight-semibold);
  cursor: pointer;
}

.kf-field-required {
  color: var(--text-crimson);
  font-family: var(--font-sans);
  font-weight: var(--weight-bold);
  letter-spacing: 0;
  font-size: 1.1em;
  line-height: 0;
  margin-left: -2px;
}

.kf-field-optional {
  font-style: normal;
  color: var(--text-faint);
  font-size: var(--text-2xs);
  letter-spacing: var(--tracking-wider);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
}

.kf-field-hint {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-muted);
  line-height: var(--leading-snug);
}

.kf-field-message {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-muted);
  line-height: var(--leading-snug);
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
}

.kf-field[data-state="error"]   .kf-field-message,
.kf-field-message[data-state="error"]   { color: var(--status-danger); }
.kf-field[data-state="warn"]    .kf-field-message,
.kf-field-message[data-state="warn"]    { color: var(--color-gold); }
.kf-field[data-state="success"] .kf-field-message,
.kf-field-message[data-state="success"] { color: var(--status-success); }

.kf-field[data-state="error"] > .kf-field-label { color: var(--status-danger); }

/* Error shake — add .kf-shake to error-state element to play one-shot horizontal shake */
@keyframes kf-shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-4px); }
  40%      { transform: translateX(4px); }
  60%      { transform: translateX(-3px); }
  80%      { transform: translateX(2px); }
}
.kf-shake { animation: kf-shake 320ms var(--ease-out) both; }
@media (prefers-reduced-motion: reduce) { .kf-shake { animation: none; } }

.kf-field-meta {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
}

.kf-field-counter {
  flex: 0 0 auto;
  font-family: var(--font-mono);
  font-size: var(--text-2xs);
  letter-spacing: var(--tracking-wider);
  color: var(--text-faint);
  font-feature-settings: "tnum";
}
.kf-field-counter[data-state="warn"]  { color: var(--color-gold); }
.kf-field-counter[data-state="error"] { color: var(--status-danger); }

.kf-field.kf-field-inline {
  flex-direction: row;
  align-items: center;
  gap: var(--space-5);
}
.kf-field.kf-field-inline > .kf-field-label {
  flex: 0 0 auto;
  min-width: 120px;
  margin-bottom: 0;
}
.kf-field.kf-field-inline > .kf-input,
.kf-field.kf-field-inline > .kf-input-wrap { flex: 1 1 auto; }

.kf-fieldset {
  border: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.kf-fieldset > legend {
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: var(--weight-semibold);
  padding: 0;
  margin-bottom: var(--space-2);
}
```

```jsx
{/* Basic */}
<div className="kf-field">
  <label className="kf-field-label" htmlFor="po">PO number</label>
  <input className="kf-input kf-md" id="po" type="text" />
  <p className="kf-field-hint">Auto-generated if blank.</p>
</div>

{/* Required */}
<label className="kf-field-label" htmlFor="email">
  Buyer email <span className="kf-field-required" aria-hidden="true">*</span>
</label>

{/* Optional flag */}
<label className="kf-field-label" htmlFor="po">
  PO number <span className="kf-field-optional">Optional</span>
</label>

{/* Validation — set data-state on field; tone propagates to label + message */}
<div className="kf-field" data-state="error">
  <label className="kf-field-label" htmlFor="qty">Quantity</label>
  <input className="kf-input kf-md" id="qty" data-state="error" />
  <p className="kf-field-message">Maximum order qty is 250.</p>
</div>

{/* Counter row */}
<div className="kf-field-meta">
  <p className="kf-field-hint">Visible to dealer + warehouse.</p>
  <span className="kf-field-counter" data-state="warn">485 / 500</span>
</div>

{/* Inline (label-left) */}
<div className="kf-field kf-field-inline">
  <label className="kf-field-label">Region</label>
  <select className="kf-input kf-md">...</select>
</div>

{/* Fieldset for radio/checkbox groups */}
<fieldset className="kf-fieldset">
  <legend>Pricing tier</legend>
  <div className="kf-check-stack">
    <label className="kf-check">...</label>
    <label className="kf-check">...</label>
  </div>
</fieldset>
```

### 6f. Date — `.kf-date`

Wraps a real `<input type="date">` + a branded popover. The CSS styles the trigger, popover, day grid, month/year views. The popover open/close + day selection requires a small JS controller — for Lovable, **start with the native picker** (it inherits `.kf-input` styling) and add the popover JS later if needed.

```css
.kf-date,
:where(.kf-date) {
  --kfd-cell:        36px;
  --kfd-bg-pop:      var(--surface-card);
  --kfd-border:      var(--border-default);
  --kfd-fg:          var(--text-primary);
  --kfd-fg-muted:    var(--text-faint);
  --kfd-active-bg:   var(--text-crimson);
  --kfd-active-fg:   var(--text-on-crimson);
  --kfd-hover-bg:    color-mix(in oklch, var(--text-crimson) 10%, transparent);
  --kfd-today-ring:  var(--text-crimson);

  position: relative;
  display: inline-block;
  width: 100%;
}

.kf-date .kf-input[type="date"]::-webkit-calendar-picker-indicator {
  display: none;
  -webkit-appearance: none;
}
.kf-date .kf-input[type="date"] { padding-right: calc(var(--space-3) + 28px); }

.kf-date-trigger {
  position: absolute;
  right: var(--space-2); top: 50%;
  transform: translateY(-50%);
  width: 28px; height: 28px;
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: var(--radius-xs);
  padding: 0;
  transition: color var(--duration-fast), background var(--duration-fast);
}
.kf-date-trigger:hover {
  color: var(--text-primary);
  background: color-mix(in oklch, var(--text-primary) 6%, transparent);
}
.kf-date-trigger:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px color-mix(in oklch, var(--text-crimson) 22%, transparent);
}

.kf-date-pop {
  position: absolute;
  top: calc(100% + var(--space-2));
  left: 0;
  z-index: 50;
  min-width: 280px;
  padding: var(--space-4);
  background: var(--kfd-bg-pop);
  border: 1px solid var(--kfd-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-4);
  font-family: var(--font-sans);
  color: var(--kfd-fg);
  animation: kfd-pop var(--duration-base) var(--ease-out);
}
.kf-date-pop[hidden] { display: none; }

@keyframes kfd-pop {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.kf-date-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
}
.kf-date-title {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  letter-spacing: var(--tracking-tight);
  color: var(--kfd-fg);
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  margin: 0 calc(var(--space-2) * -1);
  border-radius: var(--radius-xs);
  background: transparent;
  border: none;
  font-family: inherit;
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  transition: background var(--duration-fast);
}
.kf-date-title:hover { background: color-mix(in oklch, var(--text-primary) 6%, transparent); }

.kf-date-nav { display: inline-flex; gap: 2px; }
.kf-date-nav-btn {
  width: 28px; height: 28px;
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: var(--radius-xs);
  padding: 0;
  transition: color var(--duration-fast), background var(--duration-fast);
}
.kf-date-nav-btn:hover {
  color: var(--text-primary);
  background: color-mix(in oklch, var(--text-primary) 6%, transparent);
}
.kf-date-nav-btn svg { width: 12px; height: 12px; }

.kf-date-grid {
  display: grid;
  grid-template-columns: repeat(7, var(--kfd-cell));
  gap: 2px;
}
.kf-date-dow {
  height: 24px;
  display: inline-flex; align-items: center; justify-content: center;
  font-family: var(--font-mono);
  font-size: var(--text-2xs);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--text-faint);
  font-weight: var(--weight-semibold);
}
.kf-date-day {
  width: var(--kfd-cell); height: var(--kfd-cell);
  display: inline-flex; align-items: center; justify-content: center;
  font-size: var(--text-sm);
  font-feature-settings: "tnum";
  background: transparent;
  border: none;
  border-radius: var(--radius-xs);
  color: var(--kfd-fg);
  cursor: pointer;
  padding: 0;
  position: relative;
  transition: background var(--duration-fast), color var(--duration-fast);
  font-family: inherit;
}
.kf-date-day:hover:not(:disabled):not([data-selected]) { background: var(--kfd-hover-bg); }
.kf-date-day:focus-visible { outline: none; box-shadow: 0 0 0 2px var(--kfd-active-bg); }
.kf-date-day[data-out] { color: var(--kfd-fg-muted); }

.kf-date-day[data-today]:not([data-selected])::after {
  content: "";
  position: absolute;
  bottom: 5px;
  left: 50%;
  width: 12px; height: 2px;
  background: var(--kfd-today-ring);
  border-radius: 1px;
  transform: translateX(-50%);
}

.kf-date-day[data-selected] {
  background: var(--kfd-active-bg);
  color: var(--kfd-active-fg);
  font-weight: var(--weight-semibold);
}
.kf-date-day:disabled { color: var(--kfd-fg-muted); cursor: not-allowed; opacity: 0.4; }

.kf-date-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-3);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-subtle);
}
.kf-date-shortcut {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--text-muted);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-xs);
  transition: color var(--duration-fast), background var(--duration-fast);
}
.kf-date-shortcut:hover { color: var(--text-crimson); background: var(--kfd-hover-bg); }

@media (prefers-reduced-motion: reduce) {
  .kf-date-pop { animation: none; }
  .kf-date-day, .kf-date-trigger, .kf-date-nav-btn { transition: none; }
}

[data-theme="dark"] .kf-date {
  --kfd-active-bg:   var(--color-crimson);
  --kfd-today-ring:  var(--color-crimson);
  --kfd-hover-bg: color-mix(in oklch, var(--color-crimson) 18%, transparent);
}
```

**For Lovable: simplest pattern — use native date input with `.kf-input` styling:**

```jsx
<div className="kf-field">
  <label className="kf-field-label" htmlFor="due">Due date</label>
  <input className="kf-input kf-md" id="due" type="date" />
</div>
```

The native browser picker is good enough for most pages. The branded popover requires JS — bring in a library like `react-day-picker` and skin its day cells with `.kf-date-day`, `.kf-date-day[data-selected]`, etc.

### 6g. Button JS — orbit ring + success check

Optional polish layer for `.kb`. Without this script, `[data-loading]` shows an inline CSS spinner — perfectly fine. With it, you get an orbiting comet ring around the button on `data-loading`, which closes into a full ring and morphs into an animated check on `data-success`.

**Drop in `<head>` after the CSS:**

```html
<script src="/scripts/supercat-button.js" defer></script>
```

Or paste this whole block into a `useEffect` once at app mount, or as a `public/scripts/supercat-button.js` file referenced from `index.html`:

```javascript
/* SuperCat DS — Button orbit loader + success check.
   Framework-agnostic. Idempotent. No globals leaked.
   Toggle attributes on any .kb button:
     btn.setAttribute('data-loading', '')
     btn.removeAttribute('data-loading'); btn.setAttribute('data-success', '')
     btn.removeAttribute('data-success') */
(() => {
  if (window.__kbButtonInit) return;
  window.__kbButtonInit = true;
  const NS = "http://www.w3.org/2000/svg";
  const HALO_OUTSET_X = 8, HALO_OUTSET_Y = 6, BTN_RADIUS = 8;
  const HALO_RADIUS_X = BTN_RADIUS + HALO_OUTSET_X;
  const HALO_RADIUS_Y = BTN_RADIUS + HALO_OUTSET_Y;
  const STROKE = 1.5, COMET_LEN = 22, LAP_MS = 2400;
  const orbits = new WeakMap();

  function ensureLoader(btn) {
    let svg = btn.querySelector(":scope > .kb-loader");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "kb-loader");
      svg.setAttribute("aria-hidden", "true");
      const rect = document.createElementNS(NS, "rect");
      rect.setAttribute("pathLength", "100");
      rect.setAttribute("stroke-dasharray", `${COMET_LEN} ${100 - COMET_LEN}`);
      rect.setAttribute("stroke-dashoffset", "0");
      svg.appendChild(rect);
      btn.appendChild(svg);
    }
    return svg;
  }
  function ensureCheck(btn) {
    let svg = btn.querySelector(":scope > .kb-check");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "kb-check");
      svg.setAttribute("viewBox", "0 0 24 24");
      svg.setAttribute("aria-hidden", "true");
      const path = document.createElementNS(NS, "path");
      path.setAttribute("d", "M5 12 L10 17 L19 8");
      svg.appendChild(path);
      btn.appendChild(svg);
    }
    return svg;
  }
  function sizeLoader(btn) {
    const svg = ensureLoader(btn);
    const r = btn.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return null;
    const w = r.width + HALO_OUTSET_X * 2;
    const h = r.height + HALO_OUTSET_Y * 2;
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    svg.setAttribute("width", w);
    svg.setAttribute("height", h);
    const rect = svg.querySelector("rect");
    const inset = STROKE / 2;
    rect.setAttribute("x", inset);
    rect.setAttribute("y", inset);
    rect.setAttribute("width", Math.max(0, w - STROKE));
    rect.setAttribute("height", Math.max(0, h - STROKE));
    rect.setAttribute("rx", HALO_RADIUS_X);
    rect.setAttribute("ry", HALO_RADIUS_Y);
    return rect;
  }
  function bezY(t) { return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2; }
  function bezDerivative(t) { return t < 0.5 ? 12*t*t : 3*Math.pow(-2*t+2, 2); }

  function startOrbit(btn) {
    if (orbits.get(btn)?.alive) return;
    const rect = sizeLoader(btn);
    if (!rect) return;
    rect.style.opacity = "1";
    rect.setAttribute("stroke-dasharray", `0 100`);
    rect.setAttribute("stroke-dashoffset", "0");
    btn.setAttribute("aria-busy", "true");
    btn.classList.add("kb-orbit");
    const state = {
      rect, raf: null, alive: true, offset: 0, currentDash: 0,
      lapStart: performance.now(), lapDuration: LAP_MS, lapBase: 0, lap: 0,
      introT0: performance.now(), introMs: 540,
    };
    orbits.set(btn, state);
    const tick = (now) => {
      if (!state.alive) return;
      let lapT = (now - state.lapStart) / state.lapDuration;
      if (lapT >= 1) {
        state.lapBase -= 100; state.lap += 1;
        state.lapStart += state.lapDuration;
        state.lapDuration = LAP_MS * (0.85 + Math.random() * 0.30);
        lapT = (now - state.lapStart) / state.lapDuration;
        if (lapT > 1) lapT = 1; if (lapT < 0) lapT = 0;
      }
      const eased = bezY(lapT);
      state.offset = state.lapBase - 100 * eased;
      const introT = Math.min(1, (now - state.introT0) / state.introMs);
      const introEase = 1 - Math.pow(1 - introT, 3);
      let targetDash;
      if (introT < 1) targetDash = COMET_LEN * introEase;
      else {
        const vel = bezDerivative(lapT);
        const velNorm = Math.min(1, vel / 3);
        const phaseSeed = (state.lap * 0.61803) % 1;
        const wobble = Math.sin((lapT + phaseSeed) * Math.PI * 2) * 4 * velNorm;
        targetDash = COMET_LEN + wobble;
      }
      state.currentDash += (targetDash - state.currentDash) * 0.18;
      const d = Math.max(0.5, state.currentDash);
      const offRounded = Math.round(state.offset * 100) / 100;
      const dRounded = Math.round(d * 100) / 100;
      if (offRounded !== state.lastOff) {
        rect.style.strokeDashoffset = offRounded;
        state.lastOff = offRounded;
      }
      if (dRounded !== state.lastDash) {
        rect.style.strokeDasharray = `${dRounded} ${(100 - dRounded).toFixed(2)}`;
        state.lastDash = dRounded;
      }
      state.raf = requestAnimationFrame(tick);
    };
    state.raf = requestAnimationFrame(tick);
  }

  function stopOrbit(btn, opts = {}) {
    const state = orbits.get(btn);
    if (!state) return;
    state.alive = false;
    if (state.raf) cancelAnimationFrame(state.raf);
    orbits.delete(btn);
    btn.removeAttribute("aria-busy");
    btn.classList.remove("kb-orbit");
    const svg = btn.querySelector(":scope > .kb-loader");
    const rect = svg?.querySelector("rect");
    if (opts.success && rect) {
      const currentDash = state.currentDash || COMET_LEN;
      const currentOffset = state.offset ?? 0;
      const closeOffset = currentOffset - 50;
      btn.classList.add("kb-ring-forming");
      const grow = rect.animate([
        { strokeDasharray: `${currentDash} ${100 - currentDash}`, strokeDashoffset: currentOffset },
        { strokeDasharray: "100 0", strokeDashoffset: closeOffset }
      ], { duration: 560, fill: "forwards", easing: "cubic-bezier(0.4, 0, 0.2, 1)" });
      grow.onfinish = () => {
        btn.classList.remove("kb-ring-forming");
        const collapse = rect.animate([{ opacity: 1 }, { opacity: 0 }],
          { duration: 420, fill: "forwards", easing: "cubic-bezier(0.4, 0, 0.2, 1)" });
        collapse.onfinish = () => svg?.remove();
      };
    } else { svg?.remove(); }
  }

  function syncBtn(btn) {
    const wasLoading = orbits.has(btn);
    const isLoading = btn.hasAttribute("data-loading");
    const isSuccess = btn.hasAttribute("data-success");
    if (isSuccess) ensureCheck(btn);
    if (!isSuccess) {
      btn.querySelector(":scope > .kb-check")?.remove();
      btn.classList.remove("kb-ring-forming");
    }
    if (isLoading) startOrbit(btn);
    else if (wasLoading) stopOrbit(btn, { success: isSuccess });
    else if (!isSuccess) btn.querySelector(":scope > .kb-loader")?.remove();
  }
  function syncAll(root = document) { root.querySelectorAll?.(".kb").forEach(syncBtn); }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => syncAll());
  } else syncAll();

  new MutationObserver((muts) => {
    for (const m of muts) {
      if (m.type === "attributes" && (m.attributeName === "data-loading" || m.attributeName === "data-success")) {
        syncBtn(m.target);
      } else if (m.type === "childList") {
        m.addedNodes.forEach((n) => {
          if (n.nodeType !== 1) return;
          if (n.matches?.(".kb")) syncBtn(n);
          n.querySelectorAll?.(".kb").forEach(syncBtn);
        });
        m.removedNodes.forEach((n) => {
          if (n.nodeType !== 1) return;
          if (orbits.has(n)) {
            const state = orbits.get(n);
            state.alive = false;
            if (state.raf) cancelAnimationFrame(state.raf);
            orbits.delete(n);
          }
        });
      }
    }
  }).observe(document.documentElement, {
    childList: true, subtree: true, attributes: true,
    attributeFilter: ["data-loading", "data-success"],
  });

  const ro = new ResizeObserver((entries) => {
    for (const e of entries) if (e.target.hasAttribute("data-loading")) sizeLoader(e.target);
  });
  document.querySelectorAll(".kb").forEach((b) => ro.observe(b));
  new MutationObserver((muts) => {
    for (const m of muts) m.addedNodes.forEach((n) => {
      if (n.nodeType !== 1) return;
      if (n.matches?.(".kb")) ro.observe(n);
      n.querySelectorAll?.(".kb").forEach((b) => ro.observe(b));
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
```

**Usage in React:** the script binds via mutation observer, so toggling `data-loading` / `data-success` via state just works:

```jsx
async function handleSave() {
  setLoading(true);
  await api.save();
  setLoading(false);
  setSuccess(true);
  setTimeout(() => setSuccess(false), 2000);
}

<button
  className="kb kb-md kb-primary"
  {...(loading && { 'data-loading': '' })}
  {...(success && { 'data-success': '' })}
  onClick={handleSave}
>
  Save changes
</button>
```

---

## 7. Layout Patterns

Reusable page-level patterns. Use these instead of inventing new structures.

### 7a. Page shell

Every page is built on the same shell. Three layers, no exceptions.

```jsx
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="stylesheet" href="/styles/supercat-tokens.css" />
  <script src="/scripts/supercat-button.js" defer></script>
</head>
<body>
  <Header />            {/* §7b */}
  <main>
    <Hero />            {/* §7d */}
    <Section />         {/* §7e */}
    <Section />
    <CtaBlock />        {/* §7f */}
  </main>
  <Footer />            {/* §7c */}
</body>
</html>
```

### 7b. Header — logo pill + theme toggle

Fixed-top, transparent with backdrop blur. Logo pill + theme toggle + optional CTA. Same height across all items (40px).

```jsx
<header
  style={{
    position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
    padding: 'var(--space-4) var(--gutter)',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    backdropFilter: 'blur(12px) saturate(140%)',
    WebkitBackdropFilter: 'blur(12px) saturate(140%)',
    background: 'color-mix(in oklch, var(--surface-page) 70%, transparent)',
    borderBottom: '1px solid var(--border-subtle)',
  }}
>
  {/* Logo pill — 40px tall */}
  <a href="/" style={{
    display: 'inline-flex', alignItems: 'center', gap: 'var(--space-2)',
    height: 40, padding: '0 var(--space-4)',
    borderRadius: 999,
    background: 'var(--surface-card)',
    border: '1px solid var(--border-default)',
    textDecoration: 'none',
  }}>
    <SuperCatLogo width={140} />
  </a>

  <nav style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
    {/* Theme toggle — 40px circle */}
    <button
      aria-label="Toggle theme"
      onClick={toggleTheme}
      style={{
        width: 40, height: 40, borderRadius: '50%',
        background: 'transparent',
        border: '1px solid var(--border-default)',
        color: 'var(--text-primary)',
        cursor: 'pointer',
        display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
      }}
    >
      {isDark ? '☀' : '☾'}
    </button>

    {/* Optional CTA — only when explicitly requested */}
    <a className="kb kb-md kb-primary" href="/start">Get Started</a>
  </nav>
</header>
```

### 7c. Footer — logo + copyright

Simple by default. Same logo pill as header. Add link columns only if explicitly requested.

```jsx
<footer style={{
  padding: 'var(--section-y) var(--gutter)',
  borderTop: '1px solid var(--border-default)',
  background: 'var(--surface-page)',
}}>
  <div style={{
    maxWidth: 'var(--container-max)', margin: '0 auto',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    gap: 'var(--space-6)', flexWrap: 'wrap',
  }}>
    <a href="/" style={{ /* same logo pill as header */ }}>
      <SuperCatLogo width={120} />
    </a>
    <span style={{
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      color: 'var(--text-faint)',
      letterSpacing: 'var(--tracking-wider)',
      textTransform: 'uppercase',
    }}>
      © 2026 SuperCat Solutions
    </span>
  </div>
</footer>
```

### 7d. Hero — three flavors

**Editorial hero (most common — restrained, mono eyebrow + large headline + lede + CTA pair):**

```jsx
<section style={{
  padding: 'calc(var(--chapter-y) + 64px) var(--gutter) var(--chapter-y)',
  /* +64px top offset accounts for the fixed header */
  background: 'var(--surface-page)',
}}>
  <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto' }}>
    <span style={{
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      letterSpacing: 'var(--tracking-wider)',
      textTransform: 'uppercase',
      color: 'var(--text-crimson)',
      fontWeight: 'var(--weight-semibold)',
    }}>
      B2B Commerce · For Manufacturers
    </span>
    <h1 style={{
      fontFamily: 'var(--font-sans)',
      fontSize: 'clamp(44px, 7vw, 92px)',
      lineHeight: 0.96,
      letterSpacing: 'var(--tracking-tighter)',
      fontWeight: 'var(--weight-medium)',
      color: 'var(--text-primary)',
      maxWidth: '14ch',
      margin: 'var(--space-6) 0 var(--space-4)',
    }}>
      Sell smarter. <em style={{ fontStyle: 'normal', color: 'var(--text-muted)' }}>Grow faster.</em>
    </h1>
    <p style={{
      fontSize: 'clamp(16px, 1.4vw, 19px)',
      lineHeight: 'var(--leading-relaxed)',
      color: 'var(--text-body)',
      maxWidth: '58ch',
      margin: '0 0 var(--space-8)',
    }}>
      The B2B commerce platform built for furniture, lighting, and home décor manufacturers — wholesale done right.
    </p>
    <div style={{ display: 'flex', gap: 'var(--space-3)', flexWrap: 'wrap' }}>
      <a className="kb kb-lg kb-primary" href="/start">Start Free Trial</a>
      <a className="kb kb-lg kb-secondary" href="/demo">Book a Demo</a>
    </div>
  </div>
</section>
```

**Crimson hero (high-stakes / brand moment — use sparingly, ONE per page max):**

```jsx
<section style={{
  padding: 'calc(var(--chapter-y) + 64px) var(--gutter) var(--chapter-y)',
  background: 'var(--color-crimson)',
  color: 'var(--text-on-crimson)',
  position: 'relative',
  overflow: 'hidden',
}}>
  {/* Optional grid texture overlay */}
  <div style={{
    position: 'absolute', inset: 0,
    backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 47px,rgba(255,255,255,0.04) 47px,rgba(255,255,255,0.04) 48px),repeating-linear-gradient(90deg,transparent,transparent 47px,rgba(255,255,255,0.04) 47px,rgba(255,255,255,0.04) 48px)',
    pointerEvents: 'none',
  }} />
  <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto', position: 'relative' }}>
    <h1 style={{ /* same as editorial — color inherits from parent */ }}>
      Built for manufacturers.
    </h1>
    {/* CTAs: PRIMARY button on crimson uses an INK fill (kb-accent), not crimson */}
    <a className="kb kb-lg kb-accent" href="/start">Get Started</a>
  </div>
</section>
```

**Image hero (with overlay):**

```jsx
<section style={{
  position: 'relative',
  minHeight: 600,
  display: 'flex', alignItems: 'center',
  padding: 'calc(var(--chapter-y) + 64px) var(--gutter) var(--chapter-y)',
  overflow: 'hidden',
}}>
  <img src="/warehouse.jpg" alt="" style={{
    position: 'absolute', inset: 0, width: '100%', height: '100%',
    objectFit: 'cover', zIndex: 0,
  }} />
  {/* Gradient overlay — match alignment direction */}
  <div style={{
    position: 'absolute', inset: 0,
    background: 'linear-gradient(90deg, rgba(19,17,16,0.95) 0%, rgba(19,17,16,0.8) 35%, rgba(19,17,16,0.3) 65%, transparent 100%)',
    zIndex: 1,
  }} />
  <div style={{ position: 'relative', zIndex: 2, maxWidth: 560, color: '#EBE6D7' }}>
    <span style={{ /* eyebrow — use gold #B97727 on dark images */ }}>B2B Commerce</span>
    <h1 style={{ color: '#EBE6D7' }}>Sell smarter. Grow faster.</h1>
    <p style={{ color: '#A8A398' }}>...</p>
    {/* On dark image, primary CTA can use kb-accent (cream) or stay kb-primary (crimson) */}
    <a className="kb kb-lg kb-accent" href="/start">Get Started</a>
  </div>
</section>
```

### 7e. Section — features / content

Default section structure: eyebrow → headline → lede → content (grid or split). Alternate background between `--surface-page` (canvas cream) and `--surface-2` (raised cream) for visual rhythm.

```jsx
<section style={{
  padding: 'var(--section-y) var(--gutter)',
  background: 'var(--surface-2)',  /* or --surface-page for canvas */
}}>
  <div style={{ maxWidth: 'var(--container-max)', margin: '0 auto' }}>
    {/* Section head — eyebrow + h2 */}
    <div style={{ marginBottom: 'var(--space-12)', maxWidth: '70ch' }}>
      <span style={{
        fontFamily: 'var(--font-mono)',
        fontSize: 'var(--text-2xs)',
        letterSpacing: 'var(--tracking-wider)',
        textTransform: 'uppercase',
        color: 'var(--text-crimson)',
        fontWeight: 'var(--weight-semibold)',
      }}>
        What's included
      </span>
      <h2 style={{
        fontSize: 'clamp(30px, 3.8vw, 48px)',
        lineHeight: 1.05,
        letterSpacing: 'var(--tracking-tighter)',
        fontWeight: 'var(--weight-medium)',
        margin: 'var(--space-3) 0 var(--space-4)',
        color: 'var(--text-primary)',
      }}>
        Everything you need to sell wholesale.
      </h2>
      <p style={{
        fontSize: 'var(--text-lg)',
        color: 'var(--text-body)',
        lineHeight: 'var(--leading-relaxed)',
        margin: 0,
      }}>
        Three products built for the way manufacturers actually work.
      </p>
    </div>

    {/* Feature grid — 3 columns desktop, 1 column mobile */}
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)',
      gap: 'var(--space-6)',
    }}>
      <FeatureCard />
      <FeatureCard />
      <FeatureCard />
    </div>
  </div>
</section>
```

### 7f. Card — tile / feature

Cream surface, hairline border, no shadow at rest (shadow only on hover for interactive cards). One accent per card.

```jsx
<article style={{
  background: 'var(--surface-card)',
  border: '1px solid var(--border-default)',
  borderRadius: 'var(--radius-lg)',
  padding: 'var(--space-8)',
  display: 'flex', flexDirection: 'column', gap: 'var(--space-4)',
  transition: 'box-shadow var(--duration-base) var(--ease-out), transform var(--duration-base) var(--ease-out)',
}}
on:hover={{ boxShadow: 'var(--shadow-3)', transform: 'translateY(-2px)' }}>
  <span style={{
    fontFamily: 'var(--font-mono)',
    fontSize: 'var(--text-2xs)',
    letterSpacing: 'var(--tracking-wider)',
    textTransform: 'uppercase',
    color: 'var(--text-crimson)',
    fontWeight: 'var(--weight-semibold)',
  }}>
    01 · Digital Catalog
  </span>
  <h3 style={{
    fontSize: 'var(--text-xl)',
    lineHeight: 1.2,
    letterSpacing: 'var(--tracking-tight)',
    fontWeight: 'var(--weight-medium)',
    margin: 0,
    color: 'var(--text-primary)',
  }}>
    Beautiful catalogs that replace PDFs.
  </h3>
  <p style={{
    color: 'var(--text-body)',
    lineHeight: 'var(--leading-relaxed)',
    margin: 0,
  }}>
    Shoppable line cards with real-time pricing and inventory.
  </p>
  <a className="kb kb-link" href="/catalog" style={{ marginTop: 'auto', alignSelf: 'flex-start' }}>
    Learn more
    <svg className="arr-svg" viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></svg>
  </a>
</article>
```

### 7g. CTA block — closing section

Final-section call-to-action. Centered or split. Often on contrasting bg (raised cream OR crimson).

```jsx
<section style={{
  padding: 'var(--chapter-y) var(--gutter)',
  background: 'var(--surface-2)',
  textAlign: 'center',
}}>
  <div style={{ maxWidth: 720, margin: '0 auto' }}>
    <span style={{ /* eyebrow */ }}>Ready when you are</span>
    <h2 style={{ fontSize: 'clamp(36px, 4.5vw, 64px)', /* ... */ }}>
      Modernize your wholesale business today.
    </h2>
    <p style={{ margin: 'var(--space-4) 0 var(--space-8)' }}>
      Join 200+ manufacturers already selling smarter.
    </p>
    <div style={{ display: 'flex', gap: 'var(--space-3)', justifyContent: 'center', flexWrap: 'wrap' }}>
      <a className="kb kb-lg kb-primary" href="/start">Start Free Trial</a>
      <a className="kb kb-lg kb-secondary" href="/contact">Talk to Sales</a>
    </div>
  </div>
</section>
```

### 7h. Form block — signup / contact

Single-column form, max-width 480px, label-on-top by default.

```jsx
<form onSubmit={handleSubmit} style={{
  display: 'flex', flexDirection: 'column', gap: 'var(--space-5)',
  maxWidth: 480, margin: '0 auto',
}}>
  <div className="kf-field">
    <label className="kf-field-label" htmlFor="name">
      Full name <span className="kf-field-required" aria-hidden="true">*</span>
    </label>
    <input className="kf-input kf-md" id="name" type="text" required />
  </div>

  <div className="kf-field">
    <label className="kf-field-label" htmlFor="email">
      Work email <span className="kf-field-required" aria-hidden="true">*</span>
    </label>
    <input className="kf-input kf-md" id="email" type="email" required />
    <p className="kf-field-hint">We'll never share your email.</p>
  </div>

  <div className="kf-field">
    <label className="kf-field-label" htmlFor="company">Company</label>
    <input className="kf-input kf-md" id="company" type="text" />
  </div>

  <label className="kf-check">
    <input type="checkbox" />
    <span className="kf-check-box"></span>
    <span className="kf-check-label">Email me product updates</span>
  </label>

  <button className="kb kb-lg kb-primary" type="submit" style={{ width: '100%' }}>
    Start Free Trial
  </button>
</form>
```

### 7i. Responsive — breakpoints

| Width | Layout |
|-------|--------|
| 1480px+ | container-wide max content |
| 1200–1479px | container-max (1240px) |
| 768–1199px | container-max with reduced gutter |
| <768px (mobile) | **All grids collapse to 1 column. All flex rows wrap. Text scales via clamp(). Hero h1 drops to 44px. Section padding halves.** |

Standard responsive checklist for every page (non-negotiable):

```css
@media (max-width: 768px) {
  /* Grids → single column */
  .grid-3, .grid-2 { grid-template-columns: 1fr; }

  /* Hero text scales (clamp() handles this automatically if you used the values above) */

  /* Section padding reduces */
  section { padding: var(--space-12) var(--gutter); }

  /* Sticky CTAs/footer items stack vertically */
  .cta-row { flex-direction: column; }
  .cta-row .kb { width: 100%; }
}
```

---

## 8. Rules — Non-Negotiable

**Color**
- **One accent per page.** Crimson OR Gold (SuperCat/eCat). The Line Card is always crimson + clay, **never gold**.
- **Never `#FFFFFF` for surfaces.** Use `--surface-page` (`#F5F2EC`) or `--surface-2` (`#EDE9E1`). Pure white feels sterile against the warm palette.
- Crimson is brand-primary AND error-danger — same hue, no separate red.
- Hero is the one exception: ONE hero section per page can use crimson/dark gradient as a contrast entry; everything after returns to the page tone.
- Headlines: `--text-primary` (near-black). Body: `--text-body` (ink-3). Muted: `--text-muted`. Labels: `--text-muted` in `var(--font-mono)`.

**Type**
- Eyebrows / labels / metrics / numbers / table headers: **Geist Mono**, uppercase, `var(--tracking-wider)` (0.12em).
- Body / headings / buttons / nav: **Geist Sans**.
- Headlines max 14ch line length. Body max 58ch.
- Headlines use `var(--weight-medium)` (500), not bold. Restraint > weight.
- Numbers always mono (table cells, metrics, prices).

**Buttons**
- Primary CTA: `kb kb-primary` (crimson). One per section.
- Secondary CTA: `kb kb-secondary` (outlined). Always pairs with primary.
- On crimson surfaces, use `kb-accent` (ink) for primary CTAs — crimson on crimson is invisible.
- Never style a button via CSS that re-targets `.kb-primary` etc. — override component-local custom properties via `style="--kb-bg: ..."` instead.

**Spacing**
- All padding/margin via `var(--space-*)`. No magic numbers.
- Section padding: `var(--section-y)` (regular) or `var(--chapter-y)` (hero / closing).
- Gutter: `var(--gutter)` (clamp 20px–56px).
- Card padding: `var(--space-6)` to `var(--space-8)`.
- Grid gaps: `var(--space-6)` for cards, `var(--space-4)` for tight grids.

**Radii**
- Cards / panels: `var(--radius-lg)` (10px) or `var(--radius-xl)` (14px).
- Inputs / small buttons (`.kb`, `.kf-input`): set in component (4–8px).
- Pills: `999px`.
- **Never `border-radius: 0`** on cards or panels — sharp corners read as unfinished.

**Borders**
- Hairline rules: `1px solid var(--border-default)` (light) or `--border-subtle` (decorative grid).
- Dashed gridlines: 1px dashed `var(--border-default)` — for index/numbered structures.
- Strong borders: `var(--border-strong)` — for fieldset boundaries, table dividers.

**Imagery**
- Photos: always `object-fit: cover` to fill frame.
- Overlay gradient: 60% dark from bottom-left for text-over-image patterns.
- Don't use stock illustrations or 3D renders — editorial photo or no photo.
- Logo on photo: use cat mark only, `fill="#EBE6D7"` (cream) or `#B97727` (gold).

**Motion**
- Hover transitions: `var(--duration-base)` (200ms) with `var(--ease-out)`.
- Page reveals: `var(--duration-slower)` (800ms) with `var(--ease-emph)`.
- Always respect `prefers-reduced-motion: reduce` (tokens auto-zero durations).

**Dark mode**
- Set `<html data-theme="dark">`. Everything in tokens flips.
- Never hardcode dark hex values in component CSS — use semantic tokens.
- Test the dark toggle on every page.

**Accessibility**
- All form controls have `<label for>` paired to input `id`.
- All buttons have visible text OR `aria-label` (for icon-only).
- All images have `alt=""` (decorative) or descriptive `alt`.
- Focus visible: every interactive element gets the 3–4px crimson ring (built into primitives).
- Don't disable focus rings.

---

## 9. React / Lovable Quick Reference

**JSX gotchas:**
- `class` → `className`
- `for` → `htmlFor` (on labels)
- Inline styles use objects: `style={{ marginTop: '16px' }}`
- `onclick` → `onClick` (camelCase)
- SVG: `stroke-width` → `strokeWidth`, `fill-rule` → `fillRule`, `viewBox` stays `viewBox`
- `data-*` attributes: write as-is — `data-state="error"`, `data-loading=""`
- Conditional `data-*`: `{...(loading && { 'data-loading': '' })}`

**Theme toggle:**

```tsx
const [isDark, setIsDark] = useState(false);
useEffect(() => {
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
}, [isDark]);
```

**File structure for Lovable:**

```
src/
├── styles/
│   └── supercat-tokens.css   ← paste §4 block here, import in App.tsx
├── scripts/
│   └── (optional) supercat-button.js   ← §6g, reference in index.html
├── components/
│   ├── SuperCatLogo.tsx      ← §3 component pattern
│   ├── Header.tsx            ← §7b
│   ├── Footer.tsx            ← §7c
│   └── ThemeToggle.tsx       ← §5
└── App.tsx
```

In `src/App.tsx` (or `src/main.tsx`):
```tsx
import './styles/supercat-tokens.css';
```

**Don't use Tailwind utility classes for design-system colors/spacing.** Tailwind is fine for layout (`flex`, `grid`, `gap-*`) but use CSS vars for any color, type, or radius value — that's how the design system stays consistent across light/dark.

---

## 10. What's NOT in this kit (yet)

- **Combobox / autocomplete** — needs popover primitive first. Use a library (`react-select`, Radix Combobox) and skin its parts with `.kf-input` + `.kf-date-day` (for the dropdown options).
- **File upload** — needs drag-and-drop affordance. Use a library, wrap its trigger in `.kb kb-secondary`.
- **Slider / range** — design pending. Use native `<input type="range">` with `.kf-field` for label + hint.
- **Toast / notification** — not in this kit. Roll your own with the surface + shadow tokens.
- **Modal / dialog** — not in this kit. Use Radix Dialog or shadcn/ui, skin with tokens.
- **Tabs** — not a primitive. Build inline with the same mono-eyebrow + active-state crimson underline.
- **Tables** — not a primitive. Use mono font for headers and numbers, `var(--border-default)` for row separators, `var(--surface-2)` for striping.

---

## 11. Versioning

`v3 · May 2026` · Built on SuperCat Design System v0.4 (internal architecture).

This file consolidates: `ds/tokens/*.css`, `ds/primitives/*.css`, `ds/primitives/button.js`, and `assets/*.svg` into a single Lovable-ready instruction set. The internal project keeps its modular structure; this file is the shipped contract.

