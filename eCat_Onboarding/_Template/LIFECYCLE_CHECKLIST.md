# {Client Name} — eCat iPad Onboarding Lifecycle

The full path from kickoff to maintenance. Each phase links to the skill that does
the work. (Skills live in `SuperCat 4.0/.cursor/skills/`.)

## 1. Discovery / Kickoff
- [ ] Org created; shortname confirmed
- [ ] Contacts, ERP/PIM, product lines, go-live date
- [ ] Pricing model + territories understood
- [ ] CLIENT_PROFILE.md filled in

## 2. Admin Console pre-flight
- [ ] Tradenames + collections (or confirm Auto-Create)
- [ ] Groups, then categories under them
- [ ] Custom product / inventory / customer fields registered ("Send to iPad")
- [ ] Price levels created (codes match `Price_<code>` columns)
- [ ] Option types defined (if options)
- [ ] Flags: Options import, 12-image, country validation as needed
- [ ] FTP credentials confirmed

## 3. Build  → skills: ecat-core-files, ecat-pricing-levels, ecat-options-and-mapping, ecat-images-ftp
- [ ] products.csv (→ stories → inventory → customers)
- [ ] options.csv + option_groups.csv (if options)
- [ ] pricing columns
- [ ] images named + staged

## 4. Import  → rules: ecat-import-ops, ecat-ground-truth
- [ ] Correct order: options → option_groups → products → stories → inventory → customers
- [ ] Via Tools/Upload or FTP `/data`
- [ ] File Import Status **error-free** (deletes only run on a clean import)

## 5. iPad review
- [ ] Hero images (product cutout first)
- [ ] Hideable / visible counts right
- [ ] Pricing correct per customer type
- [ ] Related items, options, smartlists
- [ ] Budget 2–3 fix cycles

## 6. Go-live  → skill: ecat-go-live
- [ ] User groups; price-level visibility
- [ ] Reps invited; territory codes aligned
- [ ] Order email recipient
- [ ] >= 3 PDF report formats
- [ ] Subscription provisioned; training scheduled

## 7. Maintenance  → skills: ecat-images-ftp, ecat-postgres-audit, ecat-session-handoff
- [ ] Image-assignment two-step as new photos arrive
- [ ] Recurring feeds (inventory/pricing) if applicable
- [ ] Status tracked (health scorecard / Postgres)
- [ ] HANDOFF.md updated each session
