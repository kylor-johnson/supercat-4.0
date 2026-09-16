# Q-04 — Non-Selling User Role Classification — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Source**: BigQuery mixpanel.user_feature_usage_report (same data as Q-01 Step 1)
- **Note**: Classification applied to Q-01 Step 1 data using query library rules

Derived from Q-01 Step 1 data. The classified_role CASE logic identifies:
- Users with submit_order <= 2 classified by dominant activity pattern
- Users with submit_order > 2 classified as "Selling Rep"

Full classification will be applied by the §2 section builder during Stage 2.
See Q-01_step1_results.md for the underlying behavioral data.
