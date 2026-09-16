# User Group Mapping — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Total Postgres users (all, including disabled)**: 197
- **Active (not disabled)**: 197 (0 disabled)
- **Admin users**: 25
- **Matched to Mixpanel (Q-01 Step 1)**: — (see below)
- **Classification confidence**: LOW
- **Split available**: false

## Why Split Is Unavailable

The org_users table has 197 users with no explicit user_type differentiation beyond `is_admin` (25 admins). The remaining 172 non-admin users include:

1. **Field sales reps** (confirmed via orders table match)
2. **Showroom location accounts** (e.g., "PALECEK LOS ANGELES", "PALECEK SAN FRANCISCO" — these appear as org_users with brand-name first/last fields)
3. **Internal staff** (e.g., @palecek.com email addresses that are not admins)
4. **Unknown/ambiguous** users with no ordering history and no clear classification signal

Without an explicit user_group or user_type column, classification relies on heuristic matching (email domain, name patterns, ordering history). The `ambiguous_rate > 0` condition is triggered because a significant portion of non-admin users cannot be reliably classified into field_rep, showroom, or admin_internal buckets.

## Summary Classification (heuristic only — not used for report)

| Bucket | Estimated Count | Method |
|--------|----------------|--------|
| admin_internal | 25 | is_admin = true |
| field_rep (confirmed) | ~48 | Users with ≥1 iPad order LTM matched to orders table |
| showroom_accounts | 6 | Confirmed via showroom scan (PALECEK + city names) |
| other / unclassified | ~118 | Remaining — includes inactive reps, internal non-admin staff, legacy accounts |

## Gate Decision

- `ambiguous_rate` > 0: **true** (118 of 197 users are unclassified)
- `join_rate` to Mixpanel: Not computed (prerequisite failed)
- `showroom_event_share`: Not computed (prerequisite failed)
- **USER_GROUP_SPLIT_AVAILABLE = false**

The §8 section builder will skip the user group split and render platform metrics without field_rep vs. showroom segmentation.
