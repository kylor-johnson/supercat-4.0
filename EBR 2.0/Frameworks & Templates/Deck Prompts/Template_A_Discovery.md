# EBR Deck Prompt — Template A: Discovery-Led

**Account:** Gabby / Summer Classics (4 entities: gh, scw, sccon, sc)
**Output:** `Gabby_SC_EBR_Template_A_Discovery.html`
**Slides:** 12

---

## Task

Build a presentation-ready HTML slide deck for an Executive Business Review with Gabby / Summer Classics using Template A: Discovery-Led structure. This is the first-ever structured review — no prior meeting history exists. Build for an executive audience (we don't know exactly who's in the room yet).

Build this as a single self-contained HTML file with embedded CSS. The deck should function as a slide-based presentation using CSS scroll-snap or section-based layout — one section per slide, full-viewport height, keyboard/scroll navigation. No external dependencies except Google Fonts.

## Data Source — DO NOT QUERY DATABASES

All data has already been validated. Your ONLY data inputs are these files in the workspace:

- **Gabby_SC_Intelligence_Brief.md** — Full B1-B8 intelligence brief with all scoring, rep data, customer intelligence, expansion opportunities, and risks
- **Gabby_SC_Account_Snapshot.md** — One-page A1-A6 snapshot with identity, scoring, signals, usage, activity, financials
- **ebr_frameworks.md** — The EBR template framework definitions (Template A = Discovery-Led, sections A1-A7)

Read all three files before building anything. Extract only the data points specified per slide below. Do not dump every number from the brief onto slides. Executive decks are sparse — one insight per slide, supporting data beneath it.

## Design Direction

- **Color palette:** Dark forest green (#1E3A2F) as primary, warm sand (#F5F0E8) as surface, white (#FFFFFF) for cards, muted gold (#B8960C) as accent. This is a premium furniture brand — the deck should feel elevated, not SaaS-generic.
- **Fonts:** @import DM Sans (body) and DM Mono (labels/captions) from Google Fonts. Use Georgia as fallback for titles if DM Sans doesn't feel weighty enough at 36-40px. Body at 15-16px. Captions/labels at 11-12px in DM Mono.
- **Layout:** Each slide is a full-viewport `<section>` (100vw × 100vh, scroll-snap-align: start). Max content width 960px, centered. Dark background on title + closing slides. Light/warm on content slides.
- **Motif:** Left-edge accent bar (4px, gold) on content cards. Consistent across all slides. Cards use subtle box-shadow, 1px border in #e2e0da.
- **Transitions:** Scroll-snap with `scroll-snap-type: y mandatory` on the container. Optional: fade-in animation on section entry using IntersectionObserver.

## Slide Structure — 12 Slides

### Slide 1: Title

- Dark background (1E3A2F)
- "Executive Business Review" in large white Georgia
- "Gabby / Summer Classics" subtitle
- "March 2026 · SuperCat Solutions" in small muted text
- No logos, no decorative elements — clean and confident

### Slide 2: A1 — Partnership Snapshot

- Light background
- Key facts in a clean 2-column layout:
  - Left column: Partner since April 2013 (nearly 13 years) · 4 operating divisions · Products: iPad CPQ, eCat Online, Sales Portal, B2B Cart, Closed Site
  - Right column: Combined MRR $8,975/mo · 250 active users · 95.4% adoption rate
- Bottom: "This is your review — our goal today is to understand where your business is heading and how we can support that."
- Presenter note: "Spend 90 seconds max. Orient the room."

### Slide 3: A1 continued — Entity Overview

- 4-column card layout (one per entity):
  - Gabby (gh): Ordering · 51 users · $6.9M orders (2mo) · Residential wholesale
  - Summer Classics (scw): Ordering · 56 users · $6.4M orders · Outdoor/casual wholesale
  - SC Contract (sccon): Non-Ordering + Pushed · 29 users · $10.7M orders · Contract/hospitality
  - SC Wholesale (sc): Ordering (Retail) · 114 users · $11.2M orders · 15 physical stores
- Presenter note: "Four divisions, four distinct business models, one platform. This is what makes your account unique."

### Slide 4: A2 — Your Business & Market (Discovery)

- Warm background — this is a LISTENING slide, not a data slide
- Title: "What's Changing in Your World?"
- 5 pre-seeded questions in clean spaced layout (NOT bullets — use numbered rows with generous whitespace):
  1. "You were likely at High Point Market recently — how did spring ordering shape up?"
  2. "SC Contract is growing fast (+33% MoM) — is hospitality/contract demand accelerating broadly?"
  3. "With 15 retail stores under Gabriella White, are new locations on the horizon?"
  4. "How is the relationship between your four divisions evolving — more shared, more independent?"
  5. "What's keeping leadership up at night right now?"
- Presenter note: "This is the most important slide in the deck. Resist filling silence. Capture responses — they inform everything that follows."

### Slide 5: A3 — Platform Utilization Overview

- Title: "How Your Team Uses the Platform Today"
- Large stat callouts across top (3 big numbers):
  - 250 active users (95.4% of licensed)
  - 7,436 orders in 2 months
  - $35.2M in platform-facilitated revenue
- Below: Simple 4-column table — entity | active users | MAU trend | activity ladder
  - gh: 51/54 (94%) · ↑ · 6/6
  - scw: 56/58 (97%) · → · 6/6
  - sccon: 29/29 (100%) · ↑ · 6/6
  - sc: 114/121 (94%) · → · 6/6
- Presenter note: "Translate to business language: 'Your team has adopted virtually every capability we offer — 95% of your licensed users are active, all four divisions hit all six levels of our activity ladder.' Pause for reaction."

### Slide 6: A4 — Your Sales Team in Action

- Title: "What Your Reps Are Doing Inside the Platform"
- Two-section layout:
  - Left: Power Users — Top 3 cross-entity (Ryan Casabella: 2,104 orders across gh+scw, Julie Smallwood: 1,094 orders in sc retail, Wynne White: 781+ orders across 3 entities)
  - Right: Feature Adoption — Heat map summary showing universal adoption (Configured Items, Kits, Portal) vs. zero adoption (Flipbook, Placements, Commitments)
- Small note: "Full rep-level data available as CSV companion — ask if you'd like it."
- Presenter note: "Frame as 'here's what your team is doing' not 'here's how they score.' Ryan Casabella works across two divisions — 2,100+ orders. Wynne White is active daily across three entities."

### Slide 7: A5 — Your Customer Signals

- Title: "What the Platform Sees Across Your Customer Base"
- 4 entity cards, each showing:
  - Customers in DB → ordering customers → activation rate
  - gh: 11,812 → 967 → 8.2%
  - scw: 8,281 → 628 → 7.6%
  - sccon: 5,228 → 316 → 6.0% (OMNI Hotels 8.3% concentration)
  - sc: 91,090 → 944 → 1.0%*
- Footnote: "*SC Wholesale: 91K records are 12 years of consumer imports. Not comparable to B2B activation."
- Large callout: "Reactivating 100 dormant SCW accounts at $5,182 AOV = ~$518K incremental opportunity"
- Presenter note: "The reactivation number is the actionable takeaway. The customer lists behind this exist — offer to share them."

### Slide 8: A6 — Opportunities on the Horizon

- Title: "Where We See Growth Potential"
- 3 opportunity cards (NOT more than 3):
  1. **Flipbook for SC Contract** — "52.9% of your contract buyers already self-serve. Replace static PDF catalogs with interactive digital versions. SCCON is the ideal pilot." Priority: HIGH
  2. **SmartPicks for Summer Classics** — "Highest AOV ($5,182) + strongest growth (+45.6%). Algorithmic recommendations during this momentum phase." Priority: HIGH
  3. **Territory Configuration for SC Wholesale** — "42 territory codes in your order data, zero configured in the system. Unlocks Portal analytics for your highest-volume entity." Priority: MEDIUM
- Presenter note: "Only present opportunities that connect to something the client said in the discovery section or confirmed matters. If they didn't validate it, skip it."

### Slide 9: A6 continued — Feature Adoption Gap

- Title: "Capabilities Available but Not Yet Activated"
- Clean table: Feature | Combined Events | Best Pilot Entity | Business Case (one line each)
  - Flipbook: 0 | SCCON | Interactive catalogs for self-service buyers
  - Placements: 0 | GH | Visual merchandising for residential showrooms
  - Commitments: 0 | GH+SCW | Pre-season order tracking for trade shows
  - SmartPicks: 138 | SCW | AI-powered product recommendations
  - Maybe Lists: 12 | SCCON | Project bid consideration tracking
- Also note: SC Wholesale missing B2B Cart module (only entity without it)

### Slide 10: Support & Relationship Status

- Title: "Current Support Status"
- Left: HelpScout summary — 6 tickets (90d), 4 pending (oldest: 40 days), declining trend Q1'25→Q1'26 (positive = self-sufficient)
- Right: Relationship signals — 27 days since last touchpoint, 100% inbound communication, zero proactive meetings on record
- Bottom callout: "This is a ~$108K ARR account generating $35M+ in orders with zero structured engagement history. Today changes that."
- Presenter note: "Acknowledge the 4 pending tickets. Commit to resolution sweep."

### Slide 11: A7 — Shared Priorities & Next Steps

- Title: "What We'll Commit to Together"
- Clean open layout with 5 numbered rows — mostly blank for live capture:
  1. [Priority from discussion] — Owner: ___ — By: ___
  2. [Priority from discussion] — Owner: ___ — By: ___
  3. [Priority from discussion] — Owner: ___ — By: ___
  4. Quarterly EBR cadence — Owner: Both — Starting: ___
  5. Pending ticket resolution — Owner: SuperCat — By: [1 week]
- Bottom: "We'll send a formalized version within 48 hours."
- Presenter note: "Write this collaboratively in real time. The client should see their input reflected."

### Slide 12: Closing

- Dark background (1E3A2F)
- "Thank You" in large white Georgia
- "13 years. 4 divisions. 250 users. $35M in orders." in muted gold accent text
- "SuperCat Solutions · March 2026" small bottom text

## Output

Save as `Gabby_SC_EBR_Template_A_Discovery.html`

Presenter notes should be embedded as hidden elements (e.g., `<div class="presenter-notes">`) within each slide section, toggled visible with a keyboard shortcut (press N to show/hide notes). Not visible by default.

## Implementation Requirements

- Single self-contained HTML file. All CSS embedded. Only external dependency: Google Fonts (DM Sans + DM Mono).
- Scroll-snap layout: each slide is a `<section>` at 100vh. Scroll or arrow keys to navigate. Subtle slide counter ("3 / 12") bottom-right.
- Print-friendly: `@media print` should render one slide per page.
- Tables: DM Mono headers, muted borders, compact padding.
- Stat callouts: large numbers (48-64pt equivalent) with small labels beneath.
- The deck should look like a real presentation, not a web page with sections. Full-bleed backgrounds, centered content blocks, generous whitespace.
