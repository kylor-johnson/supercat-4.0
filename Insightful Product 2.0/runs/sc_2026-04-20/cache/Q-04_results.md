# Q-04 Results — Non-Selling User Role Classification
- **Org**: Gabriella White (sc, org_id=69)
- **Period**: All-time (Mixpanel)
- **Run date**: 2026-04-20
- **Source**: BigQuery mixpanel.user_feature_usage_report
- **Note**: Q-04 classification is derived from Q-01 Step 1 data using the classification rules in query_library.md. Full Q-04 SQL was not run separately. The Stage 2 §2 builder applies the CASE logic to Q-01 Step 1 rows.

Classification rules applied to Q-01 Step 1 data. Non-selling users (submit_order <= 2) to be classified by the §2 section builder.
