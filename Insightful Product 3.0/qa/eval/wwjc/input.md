# wwjc eval inputs — Wildwood/Chelsea House

## Stage 1 params
- CLIENT_NAME: `Wildwood/Chelsea House`
- SHORTNAME: `wwjc`
- ORG_ID: `8`
- YYYY-MM-DD: use today's date (so the eval run dir does not collide)

## Stage 2–4 params
- REPORT_DATE_DISPLAY: today's date, long form
- PERIOD_END: the month before the run date
- PERIOD_START: 12 months before PERIOD_END
- BUNDLE_LABEL: `iPad + Online Catalog + B2B Cart + Sales Portal`

Expected coverage profile: HAS_CLICKY=false (§6 skipped), HAS_CART=true, VM45 rendered.
