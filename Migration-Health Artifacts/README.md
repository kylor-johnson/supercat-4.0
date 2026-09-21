# Migration-Health Artifacts

**Purpose:** Client-facing pricing migration briefs and supporting routing infrastructure for the 2026 SuperCat pricing refresh.

**What this folder is:**
- The production workspace for generating per-account migration briefs (Format A, B, C)
- The routing logic that maps each account to a migration wave, brief format, and sequencing gate
- The operator prompt and templates for generating briefs
- A time-bounded commercial initiative folder (scope: 2026 pricing migration)

**What this folder is not:**
- It does not own or modify Health V3 scoring data (read-only input, see `04_reference/`)
- It does not own or modify Insightful Product query infrastructure (referenced, not duplicated)
- It is not a general-purpose analytics or reporting folder

---

## Folder Structure

```
Migration-Health Artifacts/
├── README.md                              ← this file
├── 01_routing/
│   ├── migration_wave_routing.csv         ← master routing table (org → wave → brief format → expansion gate)
│   └── routing_notes.md                  ← wave logic, sequencing rules, flagged accounts
├── 02_briefs/
│   ├── templates/
│   │   ├── README.md                      ← format selection guide (start here)
│   │   ├── format_a_normalization_near_flat.md      ← delta ≤10%
│   │   ├── format_b_normalization_significant_delta.md  ← delta >10% (CEO letter + appendix)
│   │   ├── format_c_expansion_upgrade.md  ← T1→T2 and T2→T3 (send after migration accepted)
│   │   └── internal_ceo_cs_prep_sheet.md  ← internal only; never share with client
│   └── generated/
│       └── [org_shortname]_[brief-type]_[date].md
├── 03_operator/
│   └── generate_upgrade_brief.md         ← operator prompt for agent-assisted brief generation
└── 04_reference/
    ├── health_data_pointer.md             ← where health scores live (do not copy)
    └── insightful_product_pointer.md      ← where query library lives (do not copy)
```

---

## Brief Format System

| Account Profile | Format | Template |
|---|---|---|
| Price normalization, delta ≤10% | **A** | `format_a_normalization_near_flat.md` |
| Price normalization, delta >10% | **B** | `format_b_normalization_significant_delta.md` |
| Expansion: T1→T2 opportunity | **C** | `format_c_expansion_upgrade.md` (subtype A) |
| Expansion: T2→T3 opportunity | **C** | `format_c_expansion_upgrade.md` (subtype B) |
| Internal CEO/CS prep | — | `internal_ceo_cs_prep_sheet.md` |

See `02_briefs/templates/README.md` for delta thresholds and sequencing rules.

---

## Wave Definitions

| Wave | Criteria | Count |
|---|---|---|
| Wave 0 | Already migrated (no action) | 2 |
| Wave 1 | Thriving or Healthy + delta ≤20% | 39 |
| Wave 2 | Thriving/Healthy + delta >20% OR Watch band OR Unscored | 67 |
| Wave 3 | At Risk, Critical, or Unscored with >30% delta | 1 |

---

## Flagged Accounts Requiring Human Review

See `01_routing/routing_notes.md` for full detail.

- **`sccon`** Summer Classics Contract — +2,450% delta (multi-org rollup; extreme legacy pricing)
- **`kl`** Coleto/Kichler — Watch health + 77.2% delta (double flag: health AND price risk)
- **`hvl`/`tl`/`cl`** Hudson Valley/Troy/Corbett Lighting — Watch health + >200% delta each
- **`krb`** — At Risk; expansion hold; migration brief requires careful tone
- **`wac`/`mf`** WAC Lighting/Modern Forms — large catalog, high delta, sophisticated operator

---

## Upstream Dependencies (read-only)

| Source | Path | What We Use |
|---|---|---|
| Health V3 (current) | `SuperCat 4.0/Health V3/runs/2026-05-13/` | `client_health_scores_2026-05-13.csv` |
| Health V3 backfill | `SuperCat 4.0/Health V3/runs/historical/` | 6-month band history per org |
| Migration table | `Downloads/2026-05-13__migration_table__v6.csv` | MRR delta, drivers, risk labels |
| Pricing authority | `Downloads/PRICING_CONSTITUTION (1).md` | Tier definitions, rate cards |

---

*Last updated: May 18, 2026*
*Health data scored: May 13, 2026 (V3.4.0, equal weights, 104 orgs, SHA `6a2f1d9f…`)*
