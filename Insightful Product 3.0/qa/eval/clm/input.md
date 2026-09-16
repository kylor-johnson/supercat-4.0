# clm eval inputs — Crystorama

## Stage 1 params
- CLIENT_NAME: `Crystorama`
- SHORTNAME: `clm`
- ORG_ID: `64`
- YYYY-MM-DD: use today's date (so the eval run dir does not collide)

## Stage 2–4 params
- REPORT_DATE_DISPLAY: today's date, long form (e.g. `June 12, 2026`)
- PERIOD_END: the month before the run date
- PERIOD_START: 12 months before PERIOD_END
- BUNDLE_LABEL: `iPad + eCat Online + Sales Portal`

Expected coverage profile: HAS_CLICKY=true (§6 included), HAS_CART=false, VM45 not rendered.
