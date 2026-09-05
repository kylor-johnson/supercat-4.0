# SuperCat Customer Segmentation Model v2

**Data-verified July 1, 2026** | Sources: Postgres production DB, BigQuery Mixpanel warehouse, Master account data (Pricing Migration v6.2), Entity data (v6.2)

---

## The Model in One Sentence

Segment customers by **how deeply they use the platform** (behavioral engagement) crossed with **how their buyer base is structured** (many small vs. few large buyers). Use price and selling motion to customize playbooks — not to assign value.

---

## Why This Replaces v1

The prior model used **price point** as the primary axis. The audit proved this is wrong:

- **Abaline Supply** ($28/unit) has **8,381 order submissions** — more than Currey & Company (6,735)
- **Bulbrite** ($3/unit) pays **$2,460/mo MRR** and is Platform-Embedded
- **Theodore Alexander** ($907/unit) has **zero order submissions** despite 2,986 logins/90d

**Price correlates with *type* of value, not *amount* of value.** The revised model leads with behavior.

---

## Segment Distribution

| Segment | Accounts | MRR/mo | ARR | % of Revenue |
|---------|----------|--------|-----|-------------|
| **Infrastructure Accounts** | 31 | $65,353 | $784K | 42% |
| **Growth Corridor** | 20 | $31,615 | $379K | 20% |
| **Presentation Layer** | 14 | $18,134 | $218K | 12% |
| **At Risk / Minimal** | 19 | $14,462 | $174K | 9% |
| **Power Users (Narrow Base)** | 6 | $8,960 | $108K | 6% |
| **Dark / Inactive** | 7 | $7,916 | $95K | 5% |
| **Declining (Watch)** | 8 | $7,478 | $90K | 5% |
| **Functional Users** | 4 | $2,515 | $30K | 2% |
| **TOTAL** | **109** | **$156,434** | **$1,877K** | |

---

## 1. Infrastructure Accounts

**31 orgs | $65,353/mo | $784K ARR — 42% of total revenue**

eCat is the daily operating system. High login volume, active order submission, deep feature adoption across distributed buyers. Losing eCat would break their selling workflow.

| Company | MRR | Tier | Logins/90d | Orders | Health | Engage | Price/Unit | Buyers | Entity |
|---------|-----|------|-----------|--------|--------|--------|-----------|--------|--------|
| Summer Classics (Wholesale) | $3,347 | T3 | 14,061 | 44,420 | 95 | 91 | $482 | 14,143 | Gabriella White |
| Summer Classics Retail | $1,930 | T3 | 7,355 | 16,868 | 94 | 85 | $426 | 2,391 | Gabriella White |
| Universal Furniture | $2,875 | T3 | 6,696 | 3,667 | 98 | 94 | $585 | 5,155 | Samson Holdings |
| Gabby | $2,079 | T3 | 6,429 | 16,043 | 91 | 85 | $596 | 2,764 | Gabriella White |
| Palecek | $3,190 | T1 | 6,162 | 4,881 | 96 | 85 | $3,626* | 17,382 | — |
| Hubbardton Forge | $3,045 | T3 | 3,699 | 3,178 | 92 | 78 | $715 | 3,302 | — |
| Interlude Home | $1,900 | T3 | 3,671 | 7,006 | 98 | 91 | $1,142 | 1,259 | Interlude |
| Braxton Culler | $2,380 | T3 | 3,659 | 2,193 | 95 | 91 | $482 | 884 | Classic Home |
| Interlude Furniture | $1,725 | T3 | 3,657 | 3,522 | 94 | 91 | $2,085 | 518 | Interlude |
| Visual Comfort – Studio/Fans | $1,856 | T1 | 3,222 | 2,127 | 87 | 78 | $30 | 3,238 | Visual Comfort |
| Wildwood/Chelsea House | $2,310 | T3 | 3,075 | 2,098 | 96 | 87 | $434 | 4,456 | — |
| Jamie Young Company | $3,045 | T3 | 2,548 | 7,446 | 94 | 87 | $214 | 4,207 | — |
| RENWIL | $2,838 | T3 | 2,491 | 10,337 | 73 | 81 | $235* | 4,900 | — |
| Savoy House Lighting | $2,175 | T3 | 2,454 | 543 | 83 | 81 | $59 | 1,212 | — |
| Furniture Classics | $2,010 | T3 | 2,237 | 3,685 | 89 | 81 | $354 | 2,076 | — |
| Somerset Bay / Modern History | $2,245 | T3 | 2,145 | 3,364 | 97 | 93 | $1,947 | 2,041 | — |
| Currey & Company | $2,190 | T3 | 2,138 | 6,735 | 92 | 81 | $592 | 11,024 | — |
| Wendover Art Group | $1,450 | T2 | 2,077 | 4,845 | 89 | 84 | $334 | 8,797 | — |
| WAC/Modern Forms | $1,750 | T1 | 2,050 | 2,804 | 94 | 85 | — | 9,611 | WAC Group |
| Capital Lighting | $2,155 | T3 | 1,957 | 909 | 84 | 81 | $104 | 1,578 | — |
| Fine Art Handcrafted Lighting | $1,325 | T1 | 1,844 | 3,612 | 89 | 87 | — | 6,846 | — |
| Visual Comfort – Modern | $1,622 | T1 | 1,836 | 475 | 85 | 74 | — | 4,418 | Visual Comfort |
| Abaline Supply | $2,201 | T3 | 1,745 | 8,381 | 78 | 66 | $28 | 1,202 | Abaline |
| Elegant Furniture & Lighting | $2,195 | T3 | 1,709 | 573 | 69 | 81 | $415* | 6,010 | — |
| Four Seasons Furniture | $1,880 | T3 | 1,604 | 1,206 | 96 | 87 | $653 | 596 | — |
| Alfresco Home | $1,455 | T2 | 1,566 | 1,432 | 73 | 81 | $221* | 3,752 | — |
| Dainolite Ltd. | $745 | T1 | 1,551 | 6,389 | 90 | 81 | $153* | 2,008 | — |
| Charleston Forge | $1,405 | T2 | 1,295 | 477 | 65 | 84 | $841* | 2,555 | — |
| Ratana International | $2,155 | T3 | 1,007 | 2,030 | 88 | 62 | $274 | 1,185 | — |
| Groupe Courchesne | $1,415 | T2 | 889 | 1,872 | 62 | 62 | $160* | 1,513 | — |
| Bulbrite | $2,460 | T3 | 878 | 444 | 87 | 77 | $3 | 1,431 | — |

*Catalog list price (no ERP transacted data)

**Key insight:** This segment spans from $3/unit (Bulbrite) to $3,626/unit (Palecek). Price is irrelevant to segment membership. What unites them: high behavioral engagement + distributed buyers + eCat is operationally essential.

**CS Playbook:** Protect. Respond fast. Proactively surface product updates. Expansion: more seats, eOL activation, Sales Portal.

---

## 2. Power Users, Narrow Base

**6 orgs | $8,960/mo | $108K ARR**

Deeply embedded in the platform but revenue flows through concentrated buyer relationships. High engagement, but structural dependency risk.

| Company | MRR | Logins/90d | Orders | Price/Unit | Top-10% Concentration | Buyers |
|---------|-----|-----------|--------|-----------|----------------------|--------|
| Sarreid, Ltd. | $1,978 | 5,211 | 1,020 | $780 | 42% | 2,121 |
| Magnussen Home | $1,745 | 5,015 | 627 | $149 | 64% | 795 |
| Linon/Powell Furniture | $2,330 | 3,191 | 1,284 | $76 | 45% | 738 |
| Kennedy International | $1,387 | 943 | 4,345 | $4 | 58% | 543 |
| Jonathan Charles (US) | $795 | 815 | 410 | $1,217 | 44% | 624 |
| Home Essentials & Beyond | $725 | 615 | 640 | $4 | 63% | 2,647 |

**CS Playbook:** Protect the relationship. Understand the key buyer accounts. Look for diversification opportunities — can they bring more accounts onto the platform? Kennedy ($4/unit, 4,345 orders) proves commodity companies can be power users.

---

## 3. Growth Corridor

**20 orgs | $31,615/mo | $379K ARR — 20% of revenue**

Commerce-Active engagement with distributed buyer bases. Using eCat regularly but haven't maximized commerce features. These are your expansion targets.

| Company | MRR | Tier | Logins/90d | Orders | Health | Price/Unit | Entity |
|---------|-----|------|-----------|--------|--------|-----------|--------|
| Maxim Lighting | $1,985 | T1 | 4,783 | 156 | 79 | $35 | Maxim group |
| Visual Comfort Signature | $1,660 | T1 | 3,001 | 279 | 90 | $364 | Visual Comfort |
| Craftmade | $2,075 | T3 | 2,077 | 386 | 88 | $41 | Litex |
| Minka Lighting Group | $1,975 | T1 | 2,074 | 182 | 87 | $162 | Ferguson |
| Eurofase Inc. | $2,475 | T3 | 1,865 | 364 | 88 | $207 | — |
| Pioneer Morton | $1,274 | T2 | 1,820 | 9,225 | 66 | $33* | Abaline |
| Kuzco Lighting | $2,155 | T3 | 1,706 | 264 | 87 | — | — |
| Uniware Housewares | $725 | T1 | 1,478 | 6,676 | 82 | $7* | — |
| Kalco/Allegri Crystal | $2,590 | T3 | 1,211 | 274 | 96 | $516 | — |
| Ciana Varaluz | $1,285 | T1 | 1,103 | 174 | 88 | $455 | — |
| Schonbek Lighting | $1,408 | T1 | 987 | 257 | 88 | — | WAC Group |
| Millennium Lighting | $1,680 | T1 | 1,572 | 89 | 68 | $75* | Ferguson |
| Buster & Punch | $1,765 | T2 | 631 | 72 | 58 | $387* | — |
| Donald Choi Canada | $1,515 | T2 | 583 | 437 | 65 | $486 | — |
| Eglo USA | $865 | T1 | 554 | 127 | 87 | $80 | Thesis |
| Hooker Furnishings | $820 | T1 | 547 | 293 | 71 | $940* | — |
| Golden Lighting | $1,935 | T3 | 538 | 62 | 81 | $95 | — |
| Matteo Lighting | $950 | T1 | 522 | 237 | 86 | $230* | — |
| EGLO Canada | $652 | T1 | 410 | 131 | 90 | $38 | Thesis |
| Coleto/Progress | $1,825 | T1 | 338 | 97 | 56 | $115* | Coleto Brands |

**Key insight:** Several high-MRR accounts ($2,590 Kalco, $2,475 Eurofase, $2,155 Kuzco) with high health scores but moderate order volumes. They're paying for the platform — they just haven't fully activated commerce. Feature adoption, not discounting, is the lever.

**CS Playbook:** Activate. Increase order submission (many have high logins but low orders). Push eOL for buyer self-service. Add seats as rep teams grow.

---

## 4. Functional Users

**4 orgs | $2,515/mo | $30K ARR**

Commerce-Active engagement with concentrated buyer bases. Specific functional use case, moderate ceiling.

| Company | MRR | Logins/90d | Orders | Price/Unit | Buyers |
|---------|-----|-----------|--------|-----------|--------|
| ELICO LTD. | $725 | 836 | 1,081 | $12* | 595 |
| Yutzy Woodworking | $495 | 779 | 139 | $877* | 227 |
| Ricci Argentieri | $375 | 616 | 774 | $49* | 548 |
| Alfonso Marina | $920 | 382 | 122 | $12,916* | 92 |

**CS Playbook:** Low-touch maintain. These accounts use eCat within their natural ceiling — which is fine. Growth lever is buyer-base expansion, not feature depth.

---

## 5. Presentation Layer

**14 orgs | $18,134/mo | $218K ARR — 12% of revenue**

High login activity with near-zero order submission. They use eCat as a catalog/presentation tool — showing products, generating PDFs — but orders consummate elsewhere.

| Company | MRR | Tier | Logins/90d | Orders | Health | Price/Unit | Entity |
|---------|-----|------|-----------|--------|--------|-----------|--------|
| Theodore Alexander | $2,150 | T3 | 2,986 | 0 | 90 | $907 | Creative Home |
| Summer Classics Contract | $1,781 | T3 | 2,310 | 0 | 94 | $438 | Gabriella White |
| Baker-McGuire | $1,385 | T1 | 1,843 | 27 | 62 | $2,410* | Samson Holdings |
| Crystorama | $2,540 | T3 | 1,614 | 2 | 87 | $259 | — |
| Rowe Furniture | $885 | T1 | 1,570 | 0 | 83 | $1,197* | — |
| Theodore Alexander Manhasset | $725 | T2 | 933 | 0 | 87 | $2,851* | Creative Home |
| Arabela Lighting | $652 | T1 | 771 | 0 | 65 | $830* | — |
| Access Lighting | $1,795 | T3 | 723 | 6 | 78 | $60 | — |
| Accord Lighting | $965 | T1 | 610 | 46 | 60 | $597* | — |
| Coleto/Kichler | $725 | T1 | 522 | 0 | 47 | $182* | Coleto Brands |
| Godinger Silver Art | $725 | T1 | 479 | 43 | 76 | $32* | Godinger Group |
| Alden Home | $1,415 | T2 | 450 | 8 | 57 | $818* | — |
| Vaxcel International | $1,810 | T3 | 318 | 1 | 79 | $52 | — |
| Butler Specialty | $580 | T1 | 312 | 31 | 75 | $246 | — |

**This confirms the "upstream of commerce" thesis.** Theodore Alexander has $34M in ERP revenue and 2,986 logins but zero order submissions. eCat enables the sale; it doesn't consummate it.

**CS Playbook:** Respect their use case. Value = catalog quality, not order flow. Invest in imagery, PDF generation, offline availability, data freshness. Don't push order submission.

---

## 6. Declining / Watch

**8 orgs | $7,478/mo | $90K ARR at risk**

Previously active accounts where engagement is trending below thresholds. Still some activity but momentum is fading.

| Company | MRR | Logins/90d | Orders | Health | Engage | Entity |
|---------|-----|-----------|--------|--------|--------|--------|
| Shadow Catchers | $725 | 365 | 685 | 82 | 72 | — |
| Geo Contemporary | $795 | 298 | 402 | 77 | 72 | — |
| Lifestyle Solutions | $725 | 290 | 152 | 87 | 72 | — |
| Jonathan Charles (UK) | $1,426 | 260 | 62 | 90 | 60 | Jonathan Charles |
| Sabine Pools | $580 | 251 | 408 | 53 | 65 | — |
| Moda at Home | $1,387 | 204 | 1,003 | 58 | 57 | — |
| AFX, Inc. | $725 | 185 | 69 | 59 | 55 | — |
| Oly Studio | $1,115 | 42 | 116 | 61 | 55 | — |

**CS Playbook:** Intervene now. A check-in call asking "what changed?" may surface a fixable issue. $90K ARR at risk. Moda at Home is notable: 1,003 order submissions historically but only 204 logins/90d — this was once a power user.

---

## 7. At Risk / Minimal

**19 orgs | $14,462/mo | $174K ARR at risk**

Low logins, near-zero ordering, minimal platform engagement. Some are still logging in occasionally; others are barely there.

| Company | MRR | Logins/90d | Orders | Health | Engage | Entity |
|---------|-----|-----------|--------|--------|--------|--------|
| Hudson Valley Lighting | $410 | 283 | 7 | 42 | 57 | HVLG |
| Silver One | $725 | 229 | 0 | 69 | 87 | — |
| Kindel Karges | $795 | 191 | 0 | 62 | 65 | — |
| Designer's Fountain | $725 | 186 | 30 | 73 | 62 | Cordelia |
| Troy Lighting | $350 | 156 | 4 | 44 | 57 | HVLG |
| Studio Silversmiths | $375 | 145 | 1 | 63 | 58 | Godinger |
| Sauder Woodworking | $725 | 145 | 0 | 78 | 58 | — |
| Philip Whitney | $375 | 124 | 0 | 58 | 58 | Godinger |
| Lucas McKearn | $652 | 119 | 5 | 51 | 65 | — |
| Corbett Lighting | $350 | 110 | 2 | 40 | — | HVLG |
| Morgan Fabrics | $1,120 | 103 | 0 | 40 | 50 | — |
| DALS Lighting | $725 | 100 | 15 | 44 | 40 | — |
| Int'l Home Miami | $725 | 47 | 18 | 52 | 67 | — |
| Century Furniture | $652 | 40 | 0 | 40 | 43 | Rock House Farm |
| America's Backyards | $725 | 31 | 0 | 58 | 38 | — |
| Kaleen Rugs | $725 | 14 | 1 | 28 | 47 | — |
| Highland House | $652 | 12 | 0 | 40 | 43 | Rock House Farm |
| CopperSmith | $3,075 | 7 | 0 | — | — | — |
| Sixtrees Limited | $580 | 5 | 1 | 38 | 43 | — |

**Notable:** CopperSmith at $3,075/mo MRR with 7 logins/90d is the single highest-MRR account in this segment. Either brand new (2026 cohort, annual deal) or a ghost account.

**CS Playbook:** Triage. Split into save (morgan, sauder, coppersmith — fixable with outreach) vs. release (sixtrees, kaleen — probably done). $174K ARR total.

---

## 8. Dark / Inactive

**7 orgs | $7,916/mo | $95K ARR — zero logins in 90 days**

| Company | MRR | Tier | Last Known Activity | Entity |
|---------|-----|------|-------------------|--------|
| Magic Lite | $1,890 | T2 | Unknown | — |
| Coaster | $1,825 | T1 | Unknown | — |
| Globalux | $1,350 | T1 | Unknown | — |
| Dorell Fabrics | $749 | T1 | Unknown | — |
| Terracota | $725 | T1 | Unknown | — |
| Pebl Furniture | $725 | T1 | 78 orders historically | Skyard |
| Visual Comfort Europe | $652 | T1 | Active via VCG entity | Visual Comfort |

**CS Playbook:** Determine if paying but not using (ghost) or already churned. $95K ARR paying for nothing. Visual Comfort Europe is a special case — likely managed centrally through the VC entity.

---

## Portfolio Entities (Consolidated)

These multi-org families should be managed as single relationships:

| Entity | Orgs | Combined MRR | Combined ARR | Health | Segments Spanned |
|--------|------|-------------|-------------|--------|-----------------|
| **Gabriella White** | sc, scw, gh, sccon, big | $10,522 | $126K | 94 | Infrastructure + Presentation |
| **Visual Comfort & Co.** | fms, vcg, tla, vce, sbl | $6,198 | $74K | 88 | Infrastructure + Growth + Dark |
| **Interlude Home** | ih, ihw | $3,625 | $44K | 96 | Infrastructure |
| **Abaline** | asi, mpc | $3,475 | $42K | 74 | Infrastructure + Growth |
| **Ferguson Enterprises** | mlg, ml | $3,655 | $44K | 78 | Growth |
| **WAC Group** | wac, sbl | $3,158 | $38K | 91 | Infrastructure + Growth |
| **Creative Home (Theodore Alexander)** | ta, tam | $2,875 | $35K | 89 | Presentation Layer |
| **Coleto Brands** | prog, kl | $2,550 | $31K | 54 | Growth + Presentation |
| **Jonathan Charles** | jc, jcusa | $2,221 | $27K | 89 | Power Users + Declining |
| **Maxim group** | mli | $1,985 | $24K | 79 | Growth |
| **Godinger Group** | gsa, rac, ssi, pw | $1,850 | $22K | 73 | Presentation + At Risk |
| **HVLG (Hudson Valley)** | hvl, tl, cl | $1,110 | $13K | 42 | At Risk |
| **Thesis (EGLO)** | eglo, eglo_can | $1,517 | $18K | 88 | Growth |
| **Rock House Farm** | cf, hh | $1,304 | $16K | 40 | At Risk |

---

## Validation: Engagement Predicts ARR

| Engagement Tier | Median ARR | Mean ARR | Count |
|-----------------|-----------|---------|-------|
| **Platform-Embedded** | **$24,120** | **$24,101** | 37 |
| Commerce-Active | $17,541 | $17,065 | 24 |
| Catalog-Active | $14,100 | $15,543 | 14 |
| Commerce-Declining | $8,700 | $10,972 | 5 |
| Catalog-Low | $8,265 | $7,592 | 18 |

Clear monotonic relationship: deeper engagement = higher ARR. This is what the price-based model couldn't show.

---

## Audit Reconciliation

| Audit Finding | v1 Status | v2 Resolution |
|---------------|-----------|---------------|
| "Abaline ($28/unit) has more orders than Currey" | Commodity Feeder | **Infrastructure Account** — correctly classified by behavior |
| "Bulbrite ($3/unit) pays $31.7K ARR" | Commodity Feeder | **Infrastructure Account** — $2,460 MRR, health 87 |
| "Theodore Alexander ($907/unit) zero orders" | Showroom Seller (high value) | **Presentation Layer** — respects actual usage pattern |
| "Price doesn't predict engagement" | Central thesis | **Removed.** Price is descriptor only. |
| "38% of accounts unclassified" | True | **All 109 accounts classified.** |
| "Portfolio double-counting" | 20+ orgs counted individually | **14 entities consolidated** with combined views |
| "Sales_data has no time dimension" | Unaddressed | **Acknowledged.** Revenue figures are cumulative. Login recency provides the time signal. |

---

## Strategic Implications

### For a 2-Person CS Team

| Priority | Action | Accounts | Revenue at Stake |
|----------|--------|----------|-----------------|
| **Now** | Call Declining accounts — understand what changed | 8 | $90K |
| **Now** | Determine Dark accounts: ghost or churned? | 7 | $95K |
| **This month** | Feature-activation push for Growth Corridor | 20 | $379K (expansion) |
| **Ongoing** | Protect Infrastructure base | 31 | $784K |
| **Quarterly** | Triage At Risk: save or release | 19 | $174K |

### For Pricing

Do not price by segment. Infrastructure Accounts range from $3/unit (Bulbrite) to $3,626/unit (Palecek). Price by **seats used** and **features enabled**.

### For Product Roadmap

- **eOL expansion** → Infrastructure + Growth (they already order)
- **Catalog/PDF tools** → Presentation Layer (that's their value)
- **Rep Copilot** → Infrastructure (highest rep activity)

### For New Logo Sales

Qualify on **engagement likelihood**, not product price. A housewares company with active reps and 1,000+ accounts is a better fit than a luxury brand with 3 reps who'll just use it as a PDF viewer.

---

## Data Sources & Completeness

| Source | Records | Key Fields | Coverage |
|--------|---------|-----------|----------|
| Master Account Data (v6.2) | 109 | MRR, tier, health, engagement, entity | 100% |
| BigQuery Mixpanel | 156 (107 matched) | Behavioral segment, order submissions, feature depth | 98% |
| Postgres login_events | 160+ orgs | Logins/90d, last login | 94% (102/109 with activity) |
| Postgres sales_data | 67 orgs | Transacted avg unit price, buyer count, concentration | 61% |
| Postgres products | 140+ orgs | Catalog net_price (fallback) | 83% with any price |
| Entity data (v6.2) | 14 entities | Parent-child relationships, combined MRR | 100% |

**Remaining gaps (18 orgs without price):** Mostly new accounts (CopperSmith, Pebl, Terracota), orgs with no products loaded yet, or orgs without catalog price data in Postgres (WAC, Kuzco, Schonbek, Fine Art). These can be filled as data arrives.

---

*109 accounts classified. Zero left unassigned. Every field sourced from production systems — no guesses.*
