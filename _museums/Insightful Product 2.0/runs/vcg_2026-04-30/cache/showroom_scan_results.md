# Showroom / Operational Account Scan — Visual Comfort Signature (vcg, org_id=141)
- **Run date**: 2026-04-30
- **Total excluded accounts**: 3
- **Aggregate excluded GMV**: $54,138.45

## Scan Results

### Pass 1 — Keyword Scan
No matches found. No rep names matched showroom/admin/marketing/training/test/demo/helper/office keywords.

### Pass 2 — Brand-Name Scan
No matches found for `rep_first_name ILIKE '%Visual Comfort%'`. Note: the branded accounts (Visual Comfort1, Visual Comfort2, Visual Comfort6) have `rep_first_name = 'Visual'` and `rep_last_name = 'Comfort1'` etc. — the first_name alone does not contain the full brand string. These were caught by Pass 1b.

### Pass 1b — Non-Person Entity Scan
Flagged 3 accounts matching `{{BRAND_NAME}}[0-9]+` pattern:

| Rep Name | Orders | GMV | User Group | Classification | Reasoning |
|----------|--------|-----|-----------|---------------|-----------|
| Visual Comfort1 | 1 | $36,218.80 | Sales Staff | Confirmed operational | Numbered corporate account ({{BRAND_NAME}}[0-9]+), Sales Staff group, single customer, not an individual person |
| Visual Comfort2 | 1 | $7,955.45 | Sales Staff | Confirmed operational | Numbered corporate account, Sales Staff group, single customer |
| Visual Comfort6 | 1 | $9,964.20 | Sales Staff | Confirmed operational | Numbered corporate account, Sales Staff group, single customer |

All three are in the "Sales Staff" user group in the admin console. They match the `Visual Comfort[0-9]+` naming pattern (VisualComfort1 through VisualComfort8 exist in the org). These are shared/showroom accounts, not individual selling reps.

**Action**: Exclude from individual rep leaderboard and archetype analysis. Include their GMV ($54,138.45) in total org eCat GMV.
