# ufi eval inputs — Universal Forest Industries

## Stage 1 params
- CLIENT_NAME: `Universal Forest Industries`
- SHORTNAME: `ufi`
- ORG_ID: `241`
- YYYY-MM-DD: use today's date (so the eval run dir does not collide)

## Stage 2–4 params
- REPORT_DATE_DISPLAY: today's date, long form (e.g. `June 16, 2026`)
- PERIOD_END: the month before the run date
- PERIOD_START: 12 months before PERIOD_END
- BUNDLE_LABEL: `iPad + eCat Online + Sales Portal`

## Coverage Profile
- HAS_PORTAL_ORDERS=true (full ERP enrichment path)
- HAS_SALES_SECTION=true (many qualifying reps)
- HAS_PEER_DATA=true (benchmark eligible)
- HAS_CLICKY=false (§6 excluded)
- HAS_CART=false
- Full ERP enrichment: Q-51, Q-52, Q-53, Q-54, Q-55, Q-56, Q-57 all active
- Elite insights: Q-14b, Q-59, Q-60, Q-61, Q-62, Q-63, Q-64, Q-65 active

Why included: Exercises the full ERP enrichment path with the most conditional
queries active. The org with the richest data surface.
