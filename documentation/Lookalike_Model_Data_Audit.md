# Lookalike Model — Data Audit & Feature Landscape

**Date:** March 24, 2026
**Purpose:** Validate data availability and quality for the benchmark peer model before engineering begins.

---

## 1. Universe Size

The `org_feature_usage_report` table in BigQuery has **81 orgs** with `hubspot_company_id` mapped. Of those, **~66 have active_users > 0** (the realistic candidate pool for benchmarking).

However, many Postgres orgs (~210 total) do NOT appear in the org_feature_usage_report. The orgs that DO appear are the ones with Mixpanel instrumentation and HubSpot mapping — which skews toward active, paying clients. This is actually fine for the lookalike model since we only care about active clients.

**Key numbers from the queries:**
- Orgs with TTM order revenue > $0: ~100
- Orgs with TTM order revenue > $10K: ~85
- Orgs with active_users > 0 in Mixpanel: ~66
- Orgs with active subscriptions: varies by plan, but 93 have eCat iPad subscriptions

---

## 2. HubSpot Segment Data: USABLE

### `properties_industry` — NOT usable (auto-enriched Clearbit, wrong categories)

The `properties_industry` field uses generic SIC/NAICS-style categories (LUXURY_GOODS_JEWELRY, RENEWABLES_ENVIRONMENT, COMPUTER_SOFTWARE, etc.) that are meaningless for Supercat's purposes. Ignore this field.

### `properties_segment` — USABLE as the hard filter for the lookalike model

HubSpot has a custom `Segment` property with Supercat-specific vertical categories. Coverage is excellent (~96% of active clients have a value) and the values are correct:

| Segment Value | Active Client Examples |
|---|---|
| **Furniture** | Gabriella White, Palecek, Universal Furniture, Summer Classics, Gabby, Braxton Culler, Theodore Alexander, Charleston Forge |
| **Lighting** | Visual Comfort, Hubbardton Forge, Corbett Lighting, Maxim Lighting, Craftmade, Capital Lighting, Savoy House, Currey & Company |
| **Home & Decor / Housewares / Art Manufacturers** | RENWIL, Wendover Art Group, Ricci Argentieri, Godinger Silver Art, Uniware Housewares, Moda at Home, Philip Whitney |
| **Generic B2B Wholesale** | Pioneer Morton |
| **Other - Unrelated Industry** | Lifestyle Solutions |

### Segment distribution across active clients (active_users > 0):

| Segment | Count |
|---|---|
| Furniture | ~25 |
| Lighting | ~28 |
| Home & Decor / Housewares / Art Manufacturers | ~10 |
| Generic B2B Wholesale | ~1 |
| Other / null | ~4 |

This gives workable pool sizes for both Furniture and Lighting. Home & Decor is smaller but viable. A few orgs may need manual review (Godinger Group and Stoneline Designs have null segment; BOBO Intriguing Objects is classified as Lighting but arguably Home & Decor).

### `properties_subsegment` — sparse, mostly empty. Only 1 real value found: "L2 - Decorative & Builder". Not usable yet but could be enriched over time.

### `properties_pain_based_segment_summary` — interesting for sales, not for lookalike model. Contains scored pain-based segments (e.g., "Complex Product Manufacturers with Captive Reps - Score: 0.95"). Only ~45 companies have values. Could be a v2 enrichment signal.

---

## 3. HubSpot Employee Count & Revenue: UNRELIABLE

| Org | Supercat TTM Revenue | HubSpot `annualrevenue` | HubSpot `employees` |
|---|---|---|---|
| Gabriella White (sc) | $142M | $1.27M | 220 |
| Summer Classics (scw) | $75M | $99.8M | 157 |
| Rowe Furniture (rf) | $368K | $50K | 40 |
| Pioneer Morton (mpc) | $15.5M | $50K | 59 |
| ELICO LTD (etl) | $1.9M | $105.2M | 6 |

The `annualrevenue` and `numberofemployees` fields are Clearbit-enriched estimates of the client company's own revenue — NOT their contract value with Supercat. Some are wildly wrong (ELICO showing $105M revenue with 6 employees). These fields are not useful for the similarity model.

**What to use instead:** Supercat's own data — TTM order revenue, subscription price, user count — are all more reliable proxies for client scale.

---

## 4. Feature Distributions (What IS Reliable)

### Product Catalog Size — Excellent Variance

| Bucket | Count | Range |
|---|---|---|
| < 500 SKUs | ~30 orgs | 1-499 |
| 500 - 2,000 SKUs | ~40 orgs | 500-1,999 |
| 2,000 - 5,000 SKUs | ~35 orgs | 2,000-4,999 |
| 5,000 - 10,000 SKUs | ~25 orgs | 5,000-9,999 |
| 10,000 - 20,000 SKUs | ~15 orgs | 10,000-19,999 |
| 20,000+ SKUs | ~8 orgs | 20,000-47,661 |

Strong variance, log-normal distribution. **Log-transform recommended.**

### TTM Order Revenue — Extreme Variance

| Bucket | Count |
|---|---|
| $0 (non-ordering) | ~115 orgs |
| $1 - $100K | ~15 orgs |
| $100K - $1M | ~20 orgs |
| $1M - $10M | ~25 orgs |
| $10M - $50M | ~15 orgs |
| $50M+ | ~5 orgs (sc, sccon, scw, shl, gh) |

Confirms the use-case profile split is essential: non-ordering clients are a huge portion. **Log-transform required; zero-handling needed.**

### User Count (enabled org_users) — Extreme Variance

Top orgs have 1,000-20,000 users (these are B2B rep networks). Most have 20-200. Some have < 10.

Note: `org_users` includes customer/buyer users in many orgs, not just sales reps. The `user_type_id` filter from the Metrics Framework is critical for getting meaningful "billable user" counts.

### Configuration Complexity — Good Signal

| Dimension | Orgs with > 0 | Max Value |
|---|---|---|
| Territories | ~25 orgs | 292 (sc_test) |
| Price Levels | ~170 orgs | 213 (vcgcon) |
| Option Groups | ~60 orgs | 1,093 (jc) |
| Matrix Options | ~35 orgs | 770K+ (ati) |
| Customers | ~155 orgs | 91K+ (sc) |

Configuration complexity has excellent discriminating power. Companies using matrix options and large option group counts are fundamentally different from those with simple catalogs.

### Subscription Plans — Clean Data

| Plan | Active Count | Base Price |
|---|---|---|
| eCat iPad | 93 | $725/mo |
| eCat Online Service | 52 | $295/mo |
| eCat Online - Closed Site | 47 | $100/mo |
| eCat Online - Portal | 36 | $395/mo |
| eCat Online - B2B Cart | 31 | $295/mo |
| eCat iPad + CPQ | 16 | $795/mo |
| Library FlipBook | 5 | $195/mo |
| Secure Credit Card | 5 | $195/mo |

**Product bundle (which plans an org subscribes to) is an excellent similarity signal.**

---

## 5. Data Source Reliability Summary

| Feature | Source | Reliability | Notes |
|---|---|---|---|
| Industry vertical (Segment) | HubSpot `properties_segment` | EXCELLENT | Custom Supercat-specific categories, ~96% coverage |
| Industry vertical (Industry) | HubSpot `properties_industry` | BAD — ignore | Auto-enriched Clearbit values are wrong |
| Employee count | HubSpot | BAD | Clearbit estimates, often wrong |
| Annual revenue | HubSpot | BAD | Client's own revenue, not contract value |
| Product count | Postgres `products` | EXCELLENT | Direct, accurate |
| Customer count | Postgres `customers` | EXCELLENT | Direct, accurate |
| Order volume/revenue | Postgres `orders` | EXCELLENT | TTM windowed |
| User count | Postgres `org_users` | GOOD | Needs user_type filter for billable |
| Active users | Mixpanel (via BQ) | GOOD | 66 orgs mapped |
| Territories | Postgres | EXCELLENT | Direct count |
| Price levels | Postgres | EXCELLENT | Direct count |
| Option groups | Postgres | EXCELLENT | Direct count |
| Matrix options | Postgres | EXCELLENT | Direct count |
| Subscription plans | Postgres | EXCELLENT | Active subs, plan names |
| Tenure | Postgres `organizations.created_at` | EXCELLENT | Direct |
| Import cadence | Postgres `import_events` | GOOD | Needs aggregation |
| Support tickets | BQ HelpScout | MODERATE | Needs org name fuzzy matching |
| Portal traffic | BQ Clicky | MODERATE | Needs prefix mapping |

---

## 6. Immediate Next Steps

1. **Spot-check segment values** — Review the ~4 active orgs with null/questionable `properties_segment` assignments (Godinger Group, Stoneline Designs, BOBO Intriguing Objects, Lifestyle Solutions). ~15 minutes.
2. **Use-case profile classification** — Run the 3-profile detection (Ordering / Non-Ordering / Non-Ordering+Pushed) across all active orgs. ~1 hour query work.
3. **Build org feature matrix** — Single table combining Postgres structural features + HubSpot `properties_segment` (via `hubspot_company_id` join from `org_feature_usage_report`) + Mixpanel active user counts. ~3-4 hours.
4. **Implement similarity engine** — Hard filters (segment must-match + use-case profile must-match) → weighted Euclidean distance on standardized features → top 5 peers. ~3-4 hours.
5. **HubSpot write-back** — Custom properties on company records via API. ~2-3 hours.
