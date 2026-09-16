# cci eval inputs — Currey & Company

## Stage 1 params
- CLIENT_NAME: `Currey & Company`
- SHORTNAME: `cci`
- ORG_ID: `51`
- YYYY-MM-DD: use today's date (so the eval run dir does not collide)

## Stage 2–4 params
- REPORT_DATE_DISPLAY: today's date, long form (e.g. `June 16, 2026`)
- PERIOD_END: the month before the run date
- PERIOD_START: 12 months before PERIOD_END
- BUNDLE_LABEL: `iPad + eCat Online + Sales Portal`

## Coverage Profile
- HAS_PORTAL_ORDERS=true (full ERP enrichment)
- HAS_CLICKY=true (§6 included — Clicky analytics active)
- HAS_CART=true (B2B Cart with confirmed server orders)
- HAS_SALES_SECTION=true (many qualifying reps)
- Full-bundle path — tests all sections including §6 Portal
- Channel mix analysis active (iPad vs eCat Online split)

Why included: Exercises the full-bundle path with ALL sections active including
§6 Portal Engagement (Clicky) and §5 channel mix (HAS_CART=true). The only org
in the golden set that tests Clicky alongside ERP enrichment and B2B Cart.
