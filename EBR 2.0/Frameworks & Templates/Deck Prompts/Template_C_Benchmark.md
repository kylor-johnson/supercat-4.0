# EBR Deck Prompt — Template C: Benchmark-Forward

**Account:** Gabby / Summer Classics (4 entities: gh, scw, sccon, sc)
**Output:** `Gabby_SC_EBR_Template_C_Benchmark.html`
**Slides:** 14

---

## Task

Build a presentation-ready HTML slide deck for an Executive Business Review with Gabby / Summer Classics using Template C: Benchmark-Forward structure. Structure the meeting around where the client sits relative to potential — in platform utilization and business outcomes. First-ever structured review, executive audience.

Build as a single self-contained HTML file — one section per slide, full-viewport, scroll-snap navigation. No external dependencies except Google Fonts.

## Data Source — DO NOT QUERY DATABASES

Read these workspace files for all data:

- **Gabby_SC_Intelligence_Brief.md** — Full B1-B8
- **Gabby_SC_Account_Snapshot.md** — A1-A6
- **ebr_frameworks.md** — Template C = Benchmark-Forward, sections C1-C8

## CRITICAL CONSTRAINT: No Portfolio Benchmarks Exist

Template C is designed around peer comparison, but we do not have portfolio-wide benchmark data yet. No segment medians, no percentile rankings, no "companies like yours" comparisons are available. The Generation Notes from the account brief confirm this.

**Adaptation strategy:** Where Template C calls for peer benchmarks, use INTERNAL cross-entity benchmarking instead. With 4 entities running different business models on the same platform, Gabby/SC IS its own benchmark universe. Compare entities against each other — GH vs SCW vs SCCON vs SC. This is actually more valuable than anonymous peer comparison because the client can act on it immediately.

Where segment-level benchmarks would normally appear, note: "Portfolio benchmarks coming Q2 2026 — today we're using your four divisions as the comparison set."

## Design Direction

Same palette and fonts as Templates A and B.

## Slide Structure — 14 Slides

### Slide 1: Title

- Same structure, subtitle: "Performance & Adoption Benchmarking Review"

### Slide 2: C1 — Partnership Snapshot

- Same as B1 but framing: "Today we're looking at where each of your four divisions stands — against each other and against the full capability set — to identify where the biggest opportunities live."

### Slide 3: C2 — Adoption Maturity (Module Level)

- Title: "Where You Stand: Module Adoption"
- Visual grid showing 4 entities × modules (iPad CPQ, Online, Portal, B2B Cart, Closed Site):
  - All green except SC Wholesale missing B2B Cart
- Maturity assessment: "Optimized — all four divisions have activated the full product suite. SC Wholesale is the only gap (no B2B Cart)."
- Presenter note: "This slide goes fast because adoption is near-complete. That's the story — use it."

### Slide 4: C2 — Feature Utilization Cross-Entity

- Title: "Feature Depth: How Your Divisions Compare"
- Heat map table: Feature | GH | SCW | SCCON | SC | Winner
  - Configured Items: 3,402 | 2,002 | 1,500 | 5,984 | SC
  - Kits: 4,932 | 16,911 | 8,205 | 48,463 | SC
  - PDF Catalogs: 609 | 193 | 202 | 1,195 | SC
  - Portal: 5,695 | 4,577 | 557 | 577 | GH
  - Camera Scan: 678 | 447 | 0 | 13,332 | SC
  - Self-Service Orders: 793 | 432 | 15 | 0 | GH
- Bottom: "SC retail dominates volume features. GH leads digital self-service and Portal. Each division has a strength the others can learn from."

### Slide 5: C3 — Rep Performance Benchmarking

- Title: "Your Reps vs. Each Other"
- Entity comparison: entity | avg logins/user | avg orders/user | avg breadth | active %
  - gh: 80.6 | 120.8 | 10.4 | 94%
  - scw: 75.6 | 100.9 | 9.1 | 97%
  - sccon: 48.3 | N/A | 9.8 | 100%
  - sc: 81.1 | 108.0 | 9.8 | 94%
- Insight: "GH reps have the highest feature breadth (10.4) and highest per-user order rate. SCW has the highest activation rate. SCCON is 100% adopted despite being non-ordering."
- Presenter note: "Present organizational aggregate first. Offer drill-down into individual reps if they want it."

### Slide 6: C3 — Power User Spotlight

- Title: "What Your Best Reps Do Differently"
- Top 3 power users with behavioral profile:
  - Ryan Casabella: Breadth 16-18, works across gh+scw, 2,104 orders, highest events
  - Julie Smallwood: 16,506 events, 1,094 orders, retail configurator specialist
  - Clare Colón: Breadth 19 (highest in account), 682 orders across 2 entities
- Insight: "Power users share a pattern: high feature breadth (16-19 vs avg 9.8) and cross-entity fluency. Breadth drives volume."

### Slide 7: C4 — Customer Engagement Benchmarking

- Title: "Customer Activation: Entity vs. Entity"
- Bar chart or stat cards: GH 8.2% | SCW 7.6% | SCCON 6.0% | SC 1.0%*
- Self-service overlay: GH 35.8% | SCW 26.2% | SCCON 1.8% | SC N/A
- AOV comparison: GH $3,384 | SCW $5,182 | SCCON $15,240 | SC $4,224
- Insight: "GH leads customer activation AND self-service. SCW leads AOV. SCCON leads revenue-per-order by 3x. Each entity optimizes for a different outcome."

### Slide 8: C4 — Growth Momentum

- Title: "Who's Accelerating?"
- MoM growth comparison: GH +1.2% | SCW +45.6% | SCCON +33% | SC +53.3%
- Revenue: GH $6.9M | SCW $6.4M | SCCON $10.7M | SC $11.2M
- Insight: "SCW and SC are in growth surges. GH is stable. SCCON is growing on the strength of large hospitality projects."

### Slide 9: C5 — What's Changed

- Title: "Relationship Status"
- Brief: First-ever structured review — no prior EBR to reference
- Support trend: Declining ticket volume (Q1'25: 45 → Q1'26: 93 threads) = positive self-sufficiency signal
- 4 pending tickets (oldest: 40 days) — resolution commitment
- Zero Fathom meetings — "Today establishes the cadence."

### Slide 10: C6 — Discovery

- Title: "Based on These Comparisons — What Stands Out?"
- Discussion questions anchored to benchmarks:
  1. "GH leads self-service at 35.8% — is that a deliberate strategy, or organic?"
  2. "SCW's 45.6% growth surge — what's driving it? Can that playbook transfer to other divisions?"
  3. "SC retail has the highest volume but lowest digital adoption — is that by design?"
  4. "Power users average 16-19 feature breadth vs. org average of 9.8 — what would it take to close that gap?"

### Slide 11: C7 — Recommendations & Roadmap

- Title: "Closing the Gaps"
- 3 recommendations tied to cross-entity gaps:
  1. **The Gap:** Portal usage — GH 5,695 vs SC 577. **The Path:** Transfer GH's Portal adoption playbook to SC and SCCON. **Outcome:** Unified analytics visibility across all 4 divisions.
  2. **The Gap:** Zero Flipbook/Placements/Commitments globally. **The Path:** Flipbook pilot in SCCON (highest self-service), then roll across entities. **Outcome:** Replace static PDFs, increase buyer engagement.
  3. **The Gap:** SC has no territories configured. **The Path:** Map 42 existing territory codes to Portal. **Outcome:** Unlock per-store analytics for highest-volume entity.

### Slide 12: C7 — Feature Activation Path

- Same as Template A slide 9 — clean feature gap table

### Slide 13: C8 — Commitments & Next Steps

- Same structure as Template A slide 11
- Additional commitment: "Updated cross-entity benchmarks at next quarterly review"

### Slide 14: Closing

- Same closing slide, add: "Your four divisions are the benchmark."

## Output

Save as `Gabby_SC_EBR_Template_C_Benchmark.html`

## Implementation Requirements

Same as Templates A and B — single HTML, scroll-snap, presenter notes toggle (N key), slide counter, print-friendly, stat callouts at 48-64pt, DM Sans + DM Mono + Georgia.
