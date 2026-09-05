# EBR Deck Prompt — Template B: Intelligence-Led

**Account:** Gabby / Summer Classics (4 entities: gh, scw, sccon, sc)
**Output:** `Gabby_SC_EBR_Template_B_Intelligence.html`
**Slides:** 14

---

## Task

Build a presentation-ready HTML slide deck for an Executive Business Review with Gabby / Summer Classics using Template B: Intelligence-Led structure. Lead with rep behavioral data and customer intelligence — earn the right to have the strategic conversation. First-ever structured review, executive audience.

Build as a single self-contained HTML file — one section per slide, full-viewport, scroll-snap navigation. No external dependencies except Google Fonts.

## Data Source — DO NOT QUERY DATABASES

Read these workspace files for all data:

- **Gabby_SC_Intelligence_Brief.md** — Full B1-B8
- **Gabby_SC_Account_Snapshot.md** — A1-A6
- **ebr_frameworks.md** — Template B = Intelligence-Led, sections B1-B7

Do not dump the entire brief onto slides. Pick the sharpest data points per section. This audience wants to see numbers, but curated ones.

## Design Direction

Same palette and fonts as Template A (dark forest, warm sand, gold accent, Georgia/DM Sans). Maintain visual consistency across all four decks.

## Slide Structure — 14 Slides

### Slide 1: Title

- Same as Template A title slide
- Subtitle addition: "Sales Intelligence & Customer Insights Review"

### Slide 2: B1 — Partnership Context

- 60-second orientation: 4 entities, 13 years, $8,975/mo MRR, 5 products active
- One-line framing: "Today we're sharing intelligence about your sales team and customer base across all four divisions, and we want your guidance on what matters most."
- Presenter note: "60-90 seconds. This audience wants data — move quickly."

### Slide 3: B2 — Sales Team Intelligence (Overview)

- Title: "Your 250 Reps Across Four Divisions"
- Large stat callouts: 250 active users · 95.4% adoption · 7,436 orders · $35.2M revenue
- 4-entity summary table: entity | reps | active % | orders | revenue | AOV
  - gh: 54 | 94% | 2,215 | $6.9M | $3,384
  - scw: 58 | 97% | 1,646 | $6.4M | $5,182
  - sccon: 29 | 100% | 849 | $10.7M | $15,240
  - sc: 121 | 94% | 2,726 | $11.2M | $4,224
- Presenter note: "Lead with the headline — $35.2M through the platform. Then let them absorb the per-entity breakdown."

### Slide 4: B2 — Power Users & Cross-Entity Activity

- Title: "Your Top Performers Work Across Divisions"
- Cross-entity rep table (top 4):
  - Ryan Casabella: 992 gh + 1,112 scw = 2,104 orders
  - Wynne White (Owner): 289 gh + 492 scw + active sccon = 781+ orders
  - Clare Colón: 408 gh + 274 scw = 682 orders
  - Tanya Houge: 162 gh + 351 scw = 513 orders
- Right side callout: "Combined 250 'active users' includes individuals working across entities. True unique count is lower — your team is more concentrated than the headline suggests."
- Presenter note: "Name names. This audience wants specifics. Wynne White ordering daily across 3 entities is a story worth telling."

### Slide 5: B2 — Feature Adoption Patterns

- Title: "What Your Team Uses — and What They Don't"
- Split layout:
  - Left (green accent): Heavy adoption — Kits: 78,511 events (SC retail dominant), Configured Items: 12,888, Portal: 11,406 (GH+SCW), Camera Scan: 14,457 (SC retail)
  - Right (gold accent): Zero adoption — Flipbook: 0, Placements: 0, Commitments: 0, SmartPicks: 138, Maybe Lists: 12
- Presenter note: "Kit workflows in SC retail (48K events) tell a story — the retail configurator is mission-critical. Camera scanning is retail-unique. The zeros on the right are the expansion conversation."

### Slide 6: B2 — Concentration Risk

- Title: "Rep Concentration by Entity"
- 4 mini cards:
  - GH: Ryan Casabella 16.1% — Low
  - SCW: Ryan Casabella 19.7% — Moderate (approaching 20% threshold)
  - SCCON: N/A (non-ordering)
  - SC: Julie Smallwood 8.9% — Low
- Bottom insight: "SCW is the only entity approaching single-rep dependency. Otherwise distribution is healthy across all divisions."
- Presenter note: "Only surface this if relevant to the conversation. Don't lead with risk — lead with the positive story."

### Slide 7: B3 — Customer Base Intelligence

- Title: "What the Platform Reveals About Your Customers"
- 4-entity comparison: entity | customers | ordering | activation | AOV | top concentration
  - gh: 11,812 | 967 | 8.2% | $3,384 | 1.8%
  - scw: 8,281 | 628 | 7.6% | $5,182 | 3.4%
  - sccon: 5,228 | 316 | 6.0% | $15,240 | 8.3% (OMNI Hotels)
  - sc: 91,090 | 944 | 1.0%* | $4,224 | 1.5%
- Footnote about SC denominator
- Callout: "SCCON has the highest customer concentration: OMNI Hotels at 8.3% ($883K, $126K AOV) + Direct Supply 7.3%"

### Slide 8: B3 — Self-Service & Growth

- Title: "Digital Self-Service Adoption"
- Bar chart or stat callouts: GH 35.8% | SCW 26.2% | SCCON 1.8% | SC 0% (retail)
- Insight: "GH leads digital adoption. SCW is growing. SCCON's 52.9% quote rate reflects project-based hospitality workflows. SC is physical retail — self-service doesn't apply."
- Growth callout: "SCW +45.6% MoM order growth. SC +53.3%. Revenue is accelerating in both wholesale divisions."

### Slide 9: B4 — Platform & Data Health

- Title: "Platform Health Check"
- Clean status dashboard:
  - Data freshness: Current (all 4 entities)
  - Import error rate: 0.2%
  - Payment status: Current — $0 outstanding
  - MRR trend: Flat ($8,975/mo, stable 12 months)
  - Last invoices: March 1, 2026
- Flag: "SC Wholesale has 0 territories configured despite 42 territory codes in order data. Quick fix that unlocks Portal analytics."
- Presenter note: "2-3 minutes max. If everything is healthy, say so and move on. The territory gap is worth flagging."

### Slide 10: B5 — Business Context & Discovery

- Title: "Now That You've Seen the Data — What Resonates?"
- Discussion starters anchored to the intelligence:
  1. "Ryan Casabella works across two divisions with 2,100+ orders — is that by design, or something to watch?"
  2. "SC Contract's $15,240 AOV is 3-4x other entities — are those large hospitality projects growing?"
  3. "Your team uses Kit workflows 78,000+ times but Flipbook is at zero — is there a reason, or just awareness?"
  4. "SC retail is growing 53% MoM — what's driving that? New stores? Seasonal?"
- Presenter note: "The intelligence sections earned you this conversation. Reference specific data points — don't re-present. Listen for which patterns they care about."

### Slide 11: B6 — Growth Opportunities

- Title: "Expansion Roadmap"
- 3 prioritized cards (same as Template A slide 8):
  1. Flipbook → SCCON pilot
  2. SmartPicks → SCW
  3. Territory config → SC
- Plus: B2B Cart module for SC (only entity without it — incremental MRR)
- Presenter note: "Connect every recommendation to something surfaced earlier. If they didn't react to it in B5, don't push it here."

### Slide 12: B6 — Cross-Entity Best Practice Transfer

- Title: "What One Division Does Well, Others Can Learn"
- 3 transfer opportunities:
  1. Portal: GH uses it 5,695 times vs SC at 577. Transfer adoption playbook.
  2. Self-Service: GH at 35.8% → help SCW (26.2%) close the gap
  3. Camera Scan: SC retail at 13,332 → could GH reps at trade shows benefit?
- Presenter note: "This is the unique value of the multi-entity view. No one else can show them this."

### Slide 13: B7 — Action Plan

- Same structure as Template A slide 11 — open layout for live capture
- Pre-filled item: "Full rep activity CSV export — Owner: SuperCat — By: end of week"
- Presenter note: "For this audience, be crisp. Ops-minded stakeholders want clarity, not open-ended commitments."

### Slide 14: Closing

- Same as Template A closing slide

## Output

Save as `Gabby_SC_EBR_Template_B_Intelligence.html`

## Implementation Requirements

Same as Template A — single HTML, scroll-snap, presenter notes toggle (N key), slide counter, print-friendly, stat callouts at 48-64pt, DM Sans + DM Mono + Georgia.
