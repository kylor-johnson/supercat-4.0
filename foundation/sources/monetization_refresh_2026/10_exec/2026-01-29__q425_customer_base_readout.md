# Q425 customer base readout (2025-10-01 → 2025-12-31)

Source: `Pricing Refresh Master Data - Master Customer Data - Q425.csv`  
Notes: `ARR` is **implied ARR = MRR * 12** in most cases (monthly-heavy base; seasonality present).

---

## Snapshot (n=110 accounts)

- **Status**: 109 active, 1 inactive
- **MRR distribution (USD)**: p25 **$725**, median **$1,192.50**, p75 **$1,899** (mean **$1,408.69**)
- **Implied ARR distribution (USD)**: p25 **$9,425**, median **$16,122.75**, p75 **$25,084.50** (mean **$17,726.71**)

## Orders (Q425)

- **Order count distribution**: p25 **1**, median **29**, p75 **330**, p90 **~923** (mean **~330**)
- **Total orders**: **36,249**
  - iPad: **27,371** (**~75.5%**)
  - eCat Online (eOL): **8,878** (**~24.5%**)
- Reconciliation: total orders = iPad + eOL (0 mismatches)

## Catalog proxy (“Total products”)

- p25 **~1,108**, median **~2,747**, p75 **~5,538**, p90 **~10,197**, max **48,727**

## Feature enablement (within these 110 accounts)

- eOL Catalog: **53/110 (48.2%)**
- eOL Cart: **32/110 (29.1%)**
- eOL Portal: **35/110 (31.8%)**
- Credit Card: **10/110 (9.1%)**
- Address Validation: **4/110 (3.6%)**
- Enrollment: **55/110 (50.0%)**
- Online Library (mobile site): **45/110 (40.9%)**
- RMA Processing (mobile site): **4/110 (3.6%)**

## eCat Online penetration (dependency-aware)

Per product structure:

- **eOL Catalog** is the base of eCat Online
- **eOL Cart** builds on eOL Catalog (adds B2B commerce/transactions)
- **eOL Portal** builds on eOL Catalog (adds sales portal/visibility)

Data validation (this customer dataset):

- **Cart ⇒ Catalog**: 0 violations
- **Portal ⇒ Catalog**: 0 violations

## Adoption cohorts (based on Catalog/Cart/Portal combinations)

| Cohort | Count | Median MRR | Median orders (Q425) | p75 orders (Q425) |
|---|---:|---:|---:|---:|
| No eOL (Catalog=N, Cart=N, Portal=N) | 57 | $725 | 7 | 54 |
| eOL Catalog only (Catalog=Y, Cart=N, Portal=N) | 7 | $1,120 | 0 | 1 |
| eOL Cart only (Catalog=Y, Cart=Y, Portal=N) | 11 | $1,415 | 118 | 310.5 |
| eOL Portal only (Catalog=Y, Cart=N, Portal=Y) | 14 | $1,937 | 262.5 | 754.25 |
| eOL Cart + Portal (Catalog=Y, Cart=Y, Portal=Y) | 21 | $2,095 | 574 | 1,584 |

**Interpretation**: Tier-fit is cleaner when we treat **eOL Catalog as the base layer**. The base splits into:

- **Tier 1-like**: “No eOL” + “Catalog only” (64 accounts total), lower order volume and lower ARPA.
- **Tier 2-like**: Cart and/or Portal enabled (46 accounts), materially higher order volume and higher ARPA.

