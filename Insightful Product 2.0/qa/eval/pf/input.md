# pf eval inputs — Palecek

## Stage 1 params
- CLIENT_NAME: `Palecek`
- SHORTNAME: `pf`
- ORG_ID: `55`
- YYYY-MM-DD: use today's date (so the eval run dir does not collide)

## Stage 2–4 params
- REPORT_DATE_DISPLAY: today's date, long form (e.g. `June 16, 2026`)
- PERIOD_END: the month before the run date
- PERIOD_START: 12 months before PERIOD_END
- BUNDLE_LABEL: `iPad + eCat Online`

## Coverage Profile
- HAS_PORTAL_ORDERS=false (iPad-only path — no ERP data)
- HAS_SALES_SECTION=true
- HAS_CLICKY=false (§6 excluded)
- HAS_CART=false
- No ERP enrichment queries (Q-51–Q-57 all N/A)
- Tests graceful degradation when ERP data is absent

Why included: Exercises the iPad-only path where ERP enrichment is completely
absent. Validates that the report degrades gracefully without Q-51–Q-57 and
that no "total business" language leaks into sections when HAS_PORTAL_ORDERS=false.
