# Competitive Packaging Audit — M3 Input

> **Purpose**: Structured analysis of how direct competitors and adjacent platforms package their products. Focus is on *structure* (not just price points) to inform SuperCat's packaging architecture decisions (D-003a through D-003d).
>
> **Sources**: Competitor websites (scraped Jan 2026), exploratory-phase analysis (`2026-01-30__modular_alternative__option_b.md`), web search.
>
> **Date**: January 28, 2026

---

## Competitor Universe

| Tier | Vendor | Relevance | Pricing Transparency |
|------|--------|-----------|---------------------|
| **Direct** | AmpTab (AMP) | Home furnishings focus; same trade shows; same ICP | Full (public pricing page) |
| **Direct** | Pepperi | B2B commerce + field sales; broader vertical | Full (public pricing page) |
| **Direct** | WizCommerce | AI-first B2B sales + ecommerce; fast-growing | Quote-only (no public pricing) |
| **Direct** | MarketTime | Network/marketplace model; largest in space | Quote-only |
| **Direct** | RepZio / ShopZio | Sales rep software + B2B marketplace; owned by ANDMORE | Partial ($25/user/mo visible) |
| **Adjacent** | Candid Wholesale | Digital catalog / B2B ordering | Public |
| **Adjacent** | B2B Wave | B2B ecommerce platform | Public |
| **Adjacent** | Onsight / App4Sales | iPad-first sales apps (horizontal) | Public |
| **Adjacent** | Geckoboard / Equals | Sales analytics / dashboards | Public |

---

## Direct Competitor Deep Dives

### 1. AmpTab (AMP)

**Source**: [amptab.com](https://amptab.com/)
**Industry**: Home furnishings / homegoods (same ICP as SuperCat)
**Scale**: Mid-market; client list includes Coaster, Progressive, Hillsdale, Riverside, Jofran

#### Packaging Model: Good/Better/Best Tiers

| Dimension | Starter | Advanced | Pro |
|-----------|---------|----------|-----|
| **Monthly** | $500 | $1,000 | $3,000 |
| **Setup fee** | $5,000 | $10,000 | $30,000 |
| **Users** | Unlimited | Unlimited | Unlimited |
| **SKUs** | Unlimited | Unlimited | Unlimited |
| **iOS App** | Yes | Yes | Yes |
| **B2B Buyers Portal** | Yes | Yes | Custom |
| **Hosted Website** | No | Yes | Custom (professionally designed) |
| **Catalog** | Build & publish | + Automated imports | + Custom |
| **Orders** | Create & process (emailed) | + Order workflow | + Order integration to other systems |
| **Reporting** | General | Advanced | Custom / scheduled |
| **ERP Integration** | No | CRM / ERP automation | + Automated data exports |
| **Territory Mgmt** | No | Yes (tracking) | + Territory performance map + route planning |
| **Credit Card** | No | Yes | Yes |
| **Configurator/CPQ** | No | **Yes** ("Configurator for Made to Order Products") | + Automated kits |
| **Kiosks** | No | No | Yes (live in-store catalog) |
| **Data feeds** | No | No | Yes (retailer data feeds) |
| **AI/Smart merch** | No | No | Yes |
| **Support** | Starter | Advanced | Pro |

**Key structural observations:**
- **Unlimited users at every tier** — users are NOT a value metric
- **Tier fences are capability-driven**: Starter = catalog + ordering; Advanced = +integrations, +CPQ, +territory; Pro = +analytics, +AI, +multi-channel
- **CPQ/Configurator is a tier fence** — gated at Advanced ($1,000/mo), not an add-on
- **Significant setup fees** scale with tier ($5K→$30K)
- **No per-order or per-transaction pricing** — pure platform fee
- **Expansion mechanism**: Tier upgrade only

**AmpTab vs. SuperCat positioning:**
- AmpTab's Starter ($500/mo) is cheaper than SuperCat's iPad base ($725/mo) but includes less
- AmpTab's Advanced ($1,000/mo) bundles what SuperCat sells as 3-4 separate subscriptions (iPad + catalog + CPQ + territory)
- AmpTab Pro ($3,000/mo) is the only tier with analytics, which SuperCat sells separately as Sales Portal ($395/mo)
- AmpTab includes unlimited users; SuperCat charges $20-25/user beyond 25

---

### 2. Pepperi

**Source**: [pepperi.com/pricing](https://www.pepperi.com/pricing/)
**Industry**: Broader B2B (CPG, fashion, food, home); enterprise-leaning
**Scale**: Enterprise; larger organizations

#### Packaging Model: Good/Better/Best Tiers × Module Matrix

| Dimension | Pro | Corporate | Ultimate |
|-----------|-----|-----------|----------|
| **Monthly** | Starting at $500 | Starting at $1,500 | Custom (contact sales) |
| **Users** | Unlimited | Unlimited | Unlimited |
| **SKUs** | Unlimited | Unlimited | Unlimited |
| **Transaction fees** | None (generous annual pool) | None (generous annual pool) | None |

**Module availability by tier (B2B eCommerce):**

| Capability | Pro | Corporate | Ultimate |
|-----------|-----|-----------|----------|
| Web & native mobile apps (online/offline) | Yes | Yes | Yes |
| Barcode scanning | Yes | Yes | Yes |
| Smart search & dynamic filters | Yes | Yes | Yes |
| Multiple price lists | Yes | Yes | Yes |
| Multiple catalog views | Yes | Yes | Yes |
| Custom domain & branded login | Yes | Yes | Yes |
| Custom homepage | Yes | Yes | Yes |
| Approval workflows | Yes | Yes | Yes |
| Related items / substitutions | Yes | Yes | Yes |
| Multiple storefronts | No | Yes | Yes |
| Headless storefront | No | Yes | Yes |
| Multi-language | No | Yes | Yes |
| Multi-currency | No | Yes | Yes |
| Trade promotions | No | Yes | Yes |
| Real-time shipping rates | No | No | Yes |
| Automatic tax-rate | No | No | Yes |

**Module availability by tier (Field Sales Reps):**

| Capability | Pro | Corporate | Ultimate |
|-----------|-----|-----------|----------|
| Web & native mobile apps (online/offline) | Yes | Yes | Yes |
| Multiple price lists | Yes | Yes | Yes |
| Discount permission | Yes | Yes | Yes |
| Account dashboards | Yes | Yes | Yes |
| Curated catalogs | Yes | Yes | Yes |
| Map view + GPS navigation | Yes | Yes | Yes |
| Multiple order types | Yes | Yes | Yes |
| BOGO & order-level promotions | Yes | Yes | Yes |
| Trade promotions | No | Yes | Yes |
| Multiple warehouses | No | Yes | Yes |
| Sales rep schedules / activity on map | No | No | Yes |
| Rep activity report (table + map) | No | No | Yes |
| Calendar planning view | No | No | Yes |

**Additional modules (Ultimate only):**
- **Route Accounting / DSD**: Van ordering, inventory tracking, load/unload van, warehouse ordering, cross-warehouse visibility, quotations, payment collection
- **Merchandising**: Geo-tagged photos, account visits, task management, custom audit forms, planogram, stocktaking, replenishment recommendations

**Key structural observations:**
- **Two-dimensional packaging**: Tiers (Pro/Corporate/Ultimate) × Modules (eCommerce, Field Sales, DSD, Merchandising)
- **Customers can buy individual modules** — don't need the full suite
- **Unlimited users at all tiers** — users are NOT a value metric
- **Transaction pool model** — "generous pool of annual transactions" included; overages purchased separately; no per-order fees
- **Tier fences**: Pro = single-market basics; Corporate = multi-market/multi-store; Ultimate = enterprise operations
- **CPQ not mentioned** — configurable products don't appear to be a distinct capability
- **Expansion**: Module addition (add DSD, add Merchandising) + tier upgrade + transaction pool overages

**Pepperi vs. SuperCat positioning:**
- Pepperi is more enterprise-focused (multi-language, multi-currency, headless, DSD)
- Pepperi's Pro ($500/mo) includes both eCommerce and field sales with unlimited users — significantly more than SuperCat's $725 iPad-only
- Pepperi's transaction pool model aligns with the "generous allowance + overage" pattern
- Pepperi packages field sales and ecommerce as a unified platform; SuperCat sells them separately

---

### 3. WizCommerce

**Source**: [wizcommerce.com](https://wizcommerce.com/), product pages for [WizOrder](https://wizcommerce.com/wizorder) and [WizShop](https://wizcommerce.com/wizshop)
**Industry**: Wholesale/distribution broadly, including home furnishings (Howard Elliott is a client)
**Scale**: 500+ customers; recently raised $8M; AI-first positioning

#### Packaging Model: Modular Product Lines (Quote-Only Pricing)

| Product | What It Does | Positioning |
|---------|-------------|-------------|
| **WizOrder** | B2B order-taking app (iPad/mobile); offline support; AI search & recommendations; barcode scanning; showroom mode; presentations; quote-to-order conversion | Field sales |
| **WizShop** | AI-powered B2B ecommerce portal; custom pricing per buyer; AI search; inventory intelligence; easy reordering; unified order management | Buyer self-service |
| **Kai** | AI sales assistant; lead scoring; call prep; natural language product search; automated follow-ups; quote/email generation | Sales intelligence |
| **WizStudio** | AI product imagery; lifestyle images without photoshoots | Marketing |
| **Ella** | AI order & quote automation | Operations |
| **WizPay** | B2B payment solution; card-on-file, payment links, terminal; refunds | Payments |

**Estimated pricing**: $500-1,000/mo (from industry benchmarks and exploratory analysis)

**Key structural observations:**
- **Modular product portfolio** — distinct named products, not tiers
- **Quote-only** — no public pricing (common for AI-first vendors)
- **AI is the differentiator**, not features — WizCommerce positions AI capabilities (recommendations, search, lead scoring) as the core value proposition
- **Sub-30-day implementation** — emphasizes speed to value
- **No CPQ/configurator** mentioned — product configuration doesn't appear to be a capability
- **Expansion**: Add modules (WizOrder → + WizShop → + Kai)
- **ERP integration is native** — emphasized as a key selling point
- **Free trial available** for WizShop (unusual in B2B)

**WizCommerce vs. SuperCat positioning:**
- WizCommerce is the most disruptive competitor — AI-first, fast implementation, aggressive pricing
- Directly targets the same "wholesalers writing orders on iPads" use case
- Key gap: No CPQ/configurator capability (SuperCat advantage)
- Key advantage: AI recommendations, AI search, AI sales assistant (SuperCat gap)
- Marketing is significantly more polished and modern
- Howard Elliott is a shared prospect/customer in the home furnishings space

---

### 4. MarketTime

**Source**: [markettime.com](https://www.markettime.com/)
**Industry**: Wholesale broadly (fashion, gift, furniture, floral, lighting, etc.)
**Scale**: 6,500 brands, 300K buyers, 350 sales agencies, 7,000 salespeople, 2.7M orders/year

#### Packaging Model: Quote-Only / Network Model

| Solution | What It Does | Notes |
|----------|-------------|-------|
| **Sales Order Writing** | iPad/iPhone/Android order writing; digital catalogs; barcode scanning; back-office tools; commission tracking | Core sales tool |
| **B2B eCommerce Website** | Branded buyer portal; shoppable images; promotions; product showcases | Self-service commerce |
| **Reporting & Analytics** (mtView) | Tableau-powered BI; drill-through dashboards; 10K-to-10ft view | Analytics |
| **Data Management** | Centralized data; API integrations; QuickBooks/NetSuite/SAP/Sage connectors | Platform |

**Key structural observations:**
- **Quote-only pricing** — zero transparency (competitive disadvantage per industry research: 78% of B2B buyers demand upfront pricing)
- **Network effects are the moat** — MarketTime's value proposition is access to 300K retail buyers, not the software itself
- **Agency model**: Serves sales agencies (multi-brand) as a primary customer, not just manufacturers
- **Commission tracking** is a core feature (reflects the agency model)
- **Tableau-powered analytics** — likely higher-end than SuperCat's Sales Portal but also quote-only
- **No CPQ/configurator** mentioned
- **Expansion**: Unknown (quote-only)

**MarketTime vs. SuperCat positioning:**
- MarketTime is the incumbent leader by volume (2.7M orders/year)
- Value proposition is network access, not software quality
- Quote-only pricing is a competitive weakness SuperCat can exploit
- Agency-first model (commission tracking, multi-brand) is different from SuperCat's manufacturer-first model
- MarketTime's scale means switching costs are high for existing customers

---

### 5. RepZio / ShopZio (ANDMORE)

**Source**: [repzio.com](https://repzio.com/)
**Industry**: Wholesale broadly; owned by ANDMORE (trade show operator)
**Scale**: Unknown; positioned as part of ANDMORE ecosystem

#### Packaging Model: Per-User Pricing (Simple)

| Dimension | RepZio App | ShopZio Marketplace |
|-----------|-----------|-------------------|
| **Price** | $25/user/month | Separate product |
| **Platform** | iOS app + web app | B2B ecommerce marketplace |
| **Offline** | Yes | N/A |
| **Users** | Per-user | N/A |

**Key features:**
- Online/offline operation
- Barcode scanning (generate + scan)
- Credit card capture (PCI compliant)
- Live inventory
- Container configuration ("configure and sell containers of goods on the fly")
- Order status checking
- Field inventories
- Territory management with integrated reports
- Presentations and bestseller lists

**Key structural observations:**
- **Pure per-user pricing** ($25/user/month) — simplest model in the competitive set
- **No tiers, no feature gating** — every user gets everything
- **ShopZio is a separate marketplace** — not an integrated ecommerce storefront
- **ANDMORE ownership** means bundled with trade show access (unique advantage)
- **Minimal configurator** — "containers of goods" suggests basic kit/assortment building, not full CPQ
- **Expansion**: Add users only
- **No analytics/portal capability** mentioned

**RepZio vs. SuperCat positioning:**
- RepZio's $25/user/mo is dramatically simpler but lower-functionality than SuperCat
- A 25-user SuperCat deployment at $725/mo = $29/user effective; RepZio at $25/user = $625/mo
- SuperCat offers significantly more depth (CPQ, portal, online catalog, cart) but at higher complexity
- RepZio's per-user model means large teams get expensive ($25 × 100 = $2,500/mo for just the app)

---

## Adjacent Platform Benchmarks

From exploratory-phase research (no structural changes since):

| Category | Vendor | Price | Value Metric | Notes |
|----------|--------|-------|-------------|-------|
| Digital Catalog | Candid Wholesale | $179-719/mo | Order volume ($1.5M-$5M caps) | GMV-based |
| Digital Catalog | B2B Wave | $295/mo | 20K products, 10 users | Product + user limits |
| Digital Catalog | Endless Commerce | $499-1,499/mo | 5K-10K SKUs | SKU-based |
| iPad Sales App | Onsight | $49.50-65/user/mo | Per-user | User-based with product/order caps |
| iPad Sales App | App4Sales | ~$97/mo | Flat | ERP integration at premium |
| Sales Analytics | Geckoboard | $175-319/mo | Dashboards + viewers | Dashboard/viewer limits |
| Sales Analytics | Equals | $699-1,899/mo | Capability tiers | Feature-gated |
| BI Platform | Amazon QuickSight | $40/user/mo + infra | Per-user + usage | Infrastructure-based |

---

## Structural Pattern Analysis

### Pattern 1: Packaging Model Convergence

| Model | Vendors Using It | Trend |
|-------|-----------------|-------|
| **Good/Better/Best tiers** | AmpTab, Pepperi | **Dominant** — used by 2 of 3 vendors with transparent pricing |
| **Modular products** | WizCommerce | Emerging — AI-first vendor using product-line modularity |
| **Per-user flat** | RepZio | Legacy — simplest but least sophisticated |
| **Quote-only** | MarketTime, WizCommerce | Common but competitively disadvantaged (78% of buyers demand upfront pricing) |

**Conclusion**: Good/Better/Best is the market-converging model. Modular is viable for AI-first positioning but harder to compare. Per-user flat is a niche/legacy approach.

### Pattern 2: Value Metric Consensus

| Value Metric | Vendors Using It | Notes |
|-------------|-----------------|-------|
| **Platform fee (flat monthly)** | AmpTab, Pepperi, WizCommerce (est.) | **Dominant** — most direct competitors use flat platform fees |
| **Per-user** | RepZio, Onsight | **Secondary** — used as expansion lever, rarely primary |
| **Transaction pools** | Pepperi, Candid Wholesale | **Emerging** — generous included pools with optional overages |
| **SKU-based** | Endless Commerce, B2B Wave | **Adjacent only** — not used by direct competitors |
| **GMV-based** | Candid Wholesale | **Adjacent only** — "success tax" concern |

**Conclusion**: Direct competitors do NOT lead with per-user pricing. Platform fee is the primary value capture; users are secondary (if used at all). Transaction pools are emerging as a supplementary metric.

### Pattern 3: Tier Fence Architecture

What differentiates tiers across competitors:

| Tier Fence | AmpTab | Pepperi |
|-----------|--------|---------|
| **Base → Mid** | +ERP integration, +credit card, +CPQ/configurator, +territory management | +Multi-storefront, +headless, +multi-language/currency, +trade promotions |
| **Mid → Top** | +Custom website, +analytics/AI, +kiosks, +data feeds, +route planning | +Route accounting/DSD, +advanced merchandising, +rep activity tracking, +replenishment |

**Common fence themes:**
- **Base**: Catalog + ordering + basic reporting (table stakes)
- **Mid**: Integrations + advanced commerce + CPQ/configuration + territory management
- **Top**: Analytics/BI + AI/intelligence + multi-channel + enterprise operations

### Pattern 4: CPQ/Configurator Treatment

| Vendor | CPQ Treatment | Price Impact |
|--------|-------------|-------------|
| **AmpTab** | **Tier-gated** (Advanced, $1,000/mo) | Included in $500→$1,000 tier step |
| **Pepperi** | Not mentioned | N/A |
| **WizCommerce** | Not available | N/A |
| **MarketTime** | Not mentioned | N/A |
| **RepZio** | Basic ("containers") | Included |
| **SuperCat (current)** | **Add-on** ($195/mo or $795 bundle) | Separate billing SKU |

**Conclusion**: Among competitors that offer CPQ, it's tier-gated (AmpTab), not a standalone add-on. SuperCat is the only vendor charging for CPQ as a separate line item. This supports either folding CPQ into a tier (simplification) or maintaining it as a premium differentiator (SuperCat has the deepest CPQ: option sets, mappings, riser prices, kits).

### Pattern 5: eOL/Storefront Treatment

| Vendor | Storefront Model | Bundled with Core? |
|--------|-----------------|-------------------|
| **AmpTab** | B2B Buyers Portal included at all tiers; hosted website at Advanced+ | **Yes** (portal), **No** (website) |
| **Pepperi** | Web + native apps at all tiers; headless at Corporate+ | **Yes** |
| **WizCommerce** | WizShop is separate product from WizOrder | **No** (modular) |
| **MarketTime** | B2B ecommerce website as solution | Unknown (quote-only) |
| **RepZio** | ShopZio is separate marketplace | **No** (separate product) |
| **SuperCat (current)** | Catalog ($295), Cart ($295), Closed Site ($100) are separate subscriptions | **No** (à la carte) |

**Conclusion**: The market is split. Tier-based vendors (AmpTab, Pepperi) include basic buyer-facing portals in all tiers. Modular vendors (WizCommerce, RepZio, SuperCat current) sell storefronts separately. If SuperCat moves to tiers, including a base buyer portal creates parity with AmpTab/Pepperi.

### Pattern 6: User Pricing

| Vendor | User Model | Included Users |
|--------|-----------|---------------|
| **AmpTab** | **Unlimited** at all tiers | All |
| **Pepperi** | **Unlimited** at all tiers | All |
| **WizCommerce** | Unknown (quote-only) | Unknown |
| **MarketTime** | Unknown (quote-only) | Unknown |
| **RepZio** | **Per-user** ($25/user/mo) | None (all paid) |
| **SuperCat (current)** | **25 included**, $20-25/user beyond | 25 |

**Conclusion**: The two most transparent, tier-based competitors (AmpTab and Pepperi) both include unlimited users. RepZio is the outlier with pure per-user pricing. SuperCat's M2 decision to keep billable users as the value metric is **counter to the competitive pattern** among direct competitors. This is a tension worth acknowledging — SuperCat's user-based expansion works because of deep feature engagement, but it may face resistance from prospects comparing to AmpTab/Pepperi's unlimited-user models.

---

## Competitive Pricing Map

| Monthly Price | AmpTab | Pepperi | RepZio (25 users) | SuperCat Current (iPad+Catalog+Cart+Portal) |
|--------------|--------|---------|-------------------|--------------------------------------------|
| **$500** | Starter | Pro | $625 | — |
| **$1,000** | Advanced | — | — | — |
| **$1,500** | — | Corporate | — | — |
| **$1,810** | — | — | — | **$1,810** ($725+$295+$295+$395+$100 closed) |
| **$3,000** | Pro | — | — | — |

SuperCat's current full-stack price (~$1,810/mo) places it between AmpTab Advanced ($1,000) and Pro ($3,000), and roughly at Pepperi Corporate ($1,500). But SuperCat's offering at this price point doesn't include unlimited users, analytics, or AI — which AmpTab Pro and Pepperi Corporate do include.

---

## Key Implications for M3 Decisions

### D-003a: Packaging Model

**Market signal**: Good/Better/Best tiers are the converging model. Both transparent-pricing direct competitors (AmpTab, Pepperi) use it. Modular is viable but harder to communicate.

**Implication**: Tiered packaging aligns with market expectations and competitive positioning.

### D-003b: Tier Fences

**Market signal**: Tier fences in this space are capability-driven (what you can do), not usage-driven (how much you use). Common fence points:
- Base → Mid: +integrations, +CPQ/configurator, +territory management
- Mid → Top: +analytics/BI, +AI, +multi-channel

**Implication**: SuperCat's natural tier fences align with the market — iPad base → +eOL/Cart/CPQ → +Portal/Analytics. The question is whether CPQ is a tier fence (AmpTab model) or an add-on (current SuperCat model).

### D-003c: Expansion Mechanism

**Market signal**: Direct competitors avoid per-user and per-order expansion. The dominant pattern is tier upgrade + module addition. Pepperi's transaction pool is the only usage-based expansion observed.

**Implication**: SuperCat's billable-user expansion mechanism is unique in this competitive set. This is either a differentiation advantage (predictable, usage-aligned) or a competitive vulnerability (prospects comparing to unlimited-user competitors). The M2 decision to keep users as the value metric should be paired with a clear narrative for why SuperCat charges per-user when AmpTab and Pepperi don't.

### D-003d: Implementation/Onboarding

**Market signal**:
- AmpTab: Significant setup fees ($5K-$30K) — implementation is monetized
- WizCommerce: "<30 days, low-cost" — implementation is a competitive weapon
- Pepperi: Not specified
- MarketTime/RepZio: Not specified

**Implication**: The market is split on implementation monetization. AmpTab successfully charges for it; WizCommerce uses speed/cost as a differentiator. SuperCat should decide whether implementation is a revenue source or a competitive lever.

---

## Competitive Threat Assessment

| Vendor | Threat Level | Why | SuperCat Advantage | SuperCat Vulnerability |
|--------|------------|-----|-------------------|-----------------------|
| **WizCommerce** | **High** | AI-first; fast implementation; same ICP; aggressive pricing; $8M fundraise | Deeper product (CPQ, Portal); established install base; industry depth | No AI capabilities; slower implementation; higher price; less modern marketing |
| **AmpTab** | **Medium** | Same industry; transparent pricing; home furnishings focus; unlimited users | Deeper CPQ; Sales Portal analytics; stronger data integration | AmpTab bundles more at lower price; unlimited users; lower entry point |
| **Pepperi** | **Medium** | Enterprise-grade; unlimited users; transaction pools; broader capability | Industry-specific depth; CPQ; simpler for mid-market | Pepperi more feature-rich at similar price; unlimited users |
| **MarketTime** | **Low-Med** | Largest network; incumbent; trade show integration | Transparent pricing; modern product; CPQ | MarketTime's network effects create switching costs |
| **RepZio** | **Low** | Simple per-user model; ANDMORE backing | Deeper product across every dimension | RepZio's simplicity and low per-user price attractive to basic users |
