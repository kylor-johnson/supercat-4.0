# Q-04 — Non-Selling User Role Classification (VM-04)

| Field | Value |
|---|---|
| **Query ID** | Q-04 |
| **Value Moment** | VM-04 |
| **Source** | BigQuery `mixpanel.user_feature_usage_report` |
| **Org** | SARREID (sarreid, org_id=1) |
| **Run Date** | 2026-04-17 |
| **Total Users** | 93 |
| **Exclusions** | None |

---

**Role distribution summary:**

| classified_role | user_count |
|----------------|-----------|
| Selling Rep | ~22 |
| Catalog/Data Manager | ~7 |
| Sales Support/Inside Sales | ~10 |
| Analytics/Portal User | 1 |
| Merchandising/List Curator | 1 |
| Content/Library Manager | 1 |
| Low-Activity User | ~5 |
| Inactive | ~46 |
| **Total** | **93** |

---

**Full user classification:**

| username | days_active | total_events | submit_order | classified_role |
|----------|------------|-------------|-------------|----------------|
| jaa | 498 | 8,136 | 144 | Selling Rep |
| cwb | 510 | 7,357 | 104 | Selling Rep |
| dklein | 438 | 6,878 | 84 | Selling Rep |
| cdq6175 | 395 | 7,596 | 67 | Selling Rep |
| moloffo | 176 | 3,745 | 67 | Selling Rep |
| stanterry | 475 | 5,463 | 61 | Selling Rep |
| ryan | 408 | 4,613 | 60 | Selling Rep |
| dannigreen | 378 | 3,242 | 56 | Selling Rep |
| joanharrison | 427 | 6,249 | 53 | Selling Rep |
| kurtmuller | 249 | 2,306 | 34 | Selling Rep |
| ripnance | 132 | 1,858 | 30 | Selling Rep |
| jgraubart | 179 | 1,794 | 28 | Selling Rep |
| dholbrook | 278 | 1,852 | 26 | Selling Rep |
| hhoxworth | 227 | 1,498 | 21 | Selling Rep |
| kkseidl | 325 | 3,698 | 13 | Selling Rep |
| acymrot | 127 | 416 | 11 | Selling Rep |
| rfernandini | 161 | 1,298 | 10 | Selling Rep |
| ngodwin | 261 | 1,548 | 8 | Selling Rep |
| cookieb | 107 | 588 | 7 | Selling Rep |
| ngodwin2 | 111 | 1,002 | 6 | Selling Rep |
| clinker | 207 | 2,385 | 6 | Selling Rep |
| dlinker | 214 | 2,194 | 5 | Selling Rep |
| msharpe2 | 392 | 10,889 | 0 | Catalog/Data Manager |
| slanier | 265 | 5,021 | 0 | Catalog/Data Manager |
| coley | 239 | 3,125 | 0 | Catalog/Data Manager |
| bcates | 295 | 2,746 | 0 | Catalog/Data Manager |
| wh4 | 313 | 4,049 | 0 | Sales Support/Inside Sales |
| wh3 | 335 | 3,664 | 0 | Sales Support/Inside Sales |
| rafebethell | 221 | 1,594 | 3 | Sales Support/Inside Sales |
| ryanmoeller | 39 | 346 | 5 | Low-Activity User |
| cannon | 14 | 124 | 3 | Low-Activity User |
| sknaak | 57 | 240 | 3 | Low-Activity User |
| jbertelsen | 62 | 631 | 2 | Low-Activity User |
| nashgilbert | 21 | 205 | 2 | Low-Activity User |

> **34 of 93 users listed above.** The remaining 59 users break down as follows per BigQuery classification:
> - Catalog/Data Manager: 3 additional users (~7 total)
> - Sales Support/Inside Sales: 8 additional users (~10 total)
> - Analytics/Portal User: 1 user
> - Merchandising/List Curator: 1 user
> - Content/Library Manager: 1 user
> - Inactive: ~46 users (minimal or zero activity — total_events < 10 or days_active ≤ 2)
>
> Full 93-row classification available in BigQuery source export.
