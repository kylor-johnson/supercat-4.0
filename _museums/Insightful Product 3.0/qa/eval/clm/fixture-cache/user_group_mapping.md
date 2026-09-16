# User-Group Mapping — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-12
- **Purpose**: Classify Mixpanel-active users into rep / admin_internal / showroom / other buckets to derive `USER_GROUP_SPLIT_AVAILABLE`.
- **Source join**: Q-01 Step 1 (100 Mixpanel usernames, BigQuery `mixpanel.user_feature_usage_report`, org='clm') ⋈ Postgres `org_users`→`user_types` (organization_id=64), case-insensitive username match.

## Match summary

| Postgres user group | Bucket | Matched Mixpanel users |
|---|---|---|
| Sales Reps | field_rep | 80 |
| z-SuperCat | admin_internal | 6 |
| Internal Employees | admin_internal | 4 |
| (no org-64 match) | unmatched | 10 |
| **Total** | | **100** |

- **Matched**: 90 / 100 → **join_rate = 0.90** (meets ≥0.90).
- **Ambiguous (`other` bucket)**: 0 matched users → **ambiguous_rate = 0.00** (meets threshold).
- **Unmatched (10)**: calebr, chermclelland, danapoe, jlindquist, khale1, mayerbrian, pmorris, rhiggins, robertgarcia, vwalker1 — no `org_users` row in org 64 (belong to other orgs / global SuperCat accounts).
- **Showroom note**: operational/showroom-style usernames (dunnlighting, hpshow, dalshow, sourceltg, lightingvision) are all members of **Sales Reps** in org 64, so they map to field_rep — there is **no distinct showroom user group** to split on.

## Event share

| Bucket | Users | total_events |
|---|---|---|
| field_rep (Sales Reps) | 80 | 74,468 |
| admin_internal (z-SuperCat + Internal Employees) | 10 | 5,206 |
| **Matched total** | 90 | **79,674** |
| unmatched (excluded) | 10 | 1,139 |
| org-wide (Q-01 Step 1) | 100 | 80,813 |

- **showroom_event_share** = admin_internal events / matched events = 5,206 / 79,674 = **0.065 (6.5%)** — below the 0.10 threshold.

## Gate derivation

`USER_GROUP_SPLIT_AVAILABLE = false`
- join_rate 0.90 ✓, ambiguous_rate 0.00 ✓ — but admin_internal/showroom event share 6.5% < 10% ⇒ internal/showroom activity is negligible, so a rep-vs-internal activity split is not meaningful.
- §8 (Strategic Recommendations / engagement narrative) renders **without** a user-group split.
