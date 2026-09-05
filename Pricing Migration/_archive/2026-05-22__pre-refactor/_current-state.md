# Pricing Migration Comms — Current State
*Last updated: 2026-05-19 | Session: [2a68d24a] (handoff execution)*

---

## What Exists

| Artifact | Location | Status |
|---|---|---|
| Account bucketing CSV (109 accounts) | `Pricing Migration/migration_comm_tiers_2026-05-19.csv` | Done |
| v6.2 Master Account CSV | `Pricing Migration/_master-account-data-v6.2.csv` | Done — PRIMARY source of truth |
| Execution plan v3.1 | `~/Downloads/2026-05-19__migration_execution_plan__v3_OUTLINE.md` | Done — stamped |
| Good News Notice template | `Pricing Migration/good-news-notices/_brief-template.md` | Done |
| Good News Notice calibrations (4 accounts) | `Pricing Migration/good-news-notices/` | Done — Option A locked |
| Format A brief template | `Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` | Done |
| Format A delivery email template | `Pricing Migration/format-a-notices/_delivery-email-template.md` | Done |
| Format A agent prompt | `Pricing Migration/format-a-notices/_fresh-agent-prompt.md` | Done — lede guardrail updated |
| Format A notices (15/15) | `Pricing Migration/format-a-notices/` | ✅ All drafted — see Format A status table below |
| Format B brief template | `Pricing Migration/format-b-notices/_brief-template.md` | Done — 7 fixes applied |
| Format B delivery email template | `Pricing Migration/format-b-notices/_delivery-email-template.md` | Done |
| Format B agent prompt | `Pricing Migration/format-b-notices/_fresh-agent-prompt.md` | Done — lede guardrail updated |
| Format B notices (19/19) | `Pricing Migration/format-b-notices/` | ✅ All drafted — see Format B status table below |
| CEO Letter brief template | `Pricing Migration/ceo-letter-notices/_brief-template.md` | Done — 7 fixes applied |
| CEO Letter delivery email template | `Pricing Migration/ceo-letter-notices/_delivery-email-template.md` | Done |
| CEO Letter agent prompt | `Pricing Migration/ceo-letter-notices/_fresh-agent-prompt.md` | Done — lede guardrail updated |
| CEO Letter notices (9/9) | `Pricing Migration/ceo-letter-notices/` | ✅ All drafted |
| Template test prompt | `Pricing Migration/_template-test-prompt.md` | Done |

---

## Template Fixes Applied (2026-05-19)

All 7 fixes are live in Format B and CEO Letter brief templates, and in all 3 agent prompts.

| Fix | Files Changed | What Changed |
|---|---|---|
| 1 | Format B + CEO Letter templates | `user_rate_normalization` block: conditional to explain platform base change when Before ≠ After |
| 2 | Format B + CEO Letter templates | `user_rate_normalization` block: billing-basis sentence after table |
| 3 | Format B + CEO Letter templates | `included_user_reduction` block: billing-basis sentence after table |
| 4 | Format B + CEO Letter templates | "Only thing changing" line: conditional fork for `included_user_reduction` accounts |
| 5 | Format B + CEO Letter templates | "Above the midpoint": required user-count clause now mandatory in guidance |
| 6 | Format B + CEO Letter templates | Value anchor: delta-per-order second sentence (gated at <$50) |
| 7 | All 3 agent prompts (Format A, B, CEO Letter) | Lede stat guardrail: provisioned-vs.-active ratio prohibited; output metrics required |
| 8 | CEO Letter template only | High-delta lede rule: delta >30% must name annual dollar impact in lede |

---

## Decisions Made

**Comm action framework — 7 tiers (locked):**
1. `CEO Pre-Call → Format B` — delta ≥ $600 (9 accounts)
2. `CEO Letter + Call Commitment` — delta $400–600 (9 accounts)
3. `Format B — Notice + Meeting Offer` — delta $150–400 or high % (19 accounts)
4. `Format A — 60-Day Notice` — delta ≤10% or ≤$80 absolute (15 accounts)
5. `Good-News Notice` — decrease, Healthy/Thriving (4 accounts)
6. `HOLD` — entity packet unresolved, health hold, unscored, VD override (51 accounts)
7. `Already Migrated` — 2 accounts

**Good News Notice design — LOCKED: Option A (email with inline table)**

**`support_fire` handling — LOCKED:** Draft anyway. Add ⚠️ flag in routing block and delivery email. Operator (CEO) decides timing. Never skip the draft, never reference support issue in client-facing copy.

**Source of truth hierarchy — LOCKED:**
1. v6.2 Master CSV (driver, pricing breakdown, health, flags)
2. HTML model (MRR/delta math cross-check)
3. Routing CSV (comm_action only)

**Lede stat rule — LOCKED:** Output metrics only (orders, customers). Never provisioned-vs.-active user ratio.

---

## CEO Letter Account Status

All 9 accounts drafted 2026-05-19. 9/9 complete.

| ord_id | Account | Delta | Driver | Status |
|---|---|---|---|---|
| hfg | Hubbardton Forge | +$420/+13.8% | tier_base_increase | ✅ Done |
| da | Dainolite Ltd. | +$452/+60.7% | user_rate_normalization + included_user_reduction | ✅ Done |
| fsf | Four Seasons Furniture | +$415/+22.1% | tier_base_increase | ✅ Done |
| vic | Vaxcel International | +$485/+26.8% | tier_base_increase | ✅ Done |
| ali | Access Lighting | +$500/+27.9% | tier_base_increase | ✅ Done |
| mlc | Matteo Lighting | +$519/+54.6% | included_user_reduction | ✅ Done — value anchor omitted (see note below) |
| all | Accord Lighting | +$564/+58.4% | user_rate_normalization + included_user_reduction | ✅ Done |
| am | Alfonso Marina | +$400/+43.5% | included_user_reduction | ✅ Done |
| shl | Savoy House | +$524/+24.1% | user_rate_normalization | ✅ Done — ⚠️ support fire (39 days open). Production-ready; operator decides send timing. Billing entity = Progressive Lighting. |

**mlc value anchor note:** Section omitted by drafting agent. Cost-per-order $154.62 qualifies under $200 threshold (section should be included), but delta-per-order $54.63 fails the $50 second-sentence gate and agent judged the section weaker without it. Operator decision: either add the first sentence only ("Across 114 eCat orders last year, the new annual subscription works out to approximately $154 per order.") before send, or accept omission. This is a known template deviation.

---

## Format A Account Status

All 15 accounts drafted 2026-05-19. 15/15 complete.

| ord_id | Account | Delta | Driver | Status |
|---|---|---|---|---|
| kal | Kalco Lighting / Allegri Crystal | +$219/+8.5% | user_rate_normalization | ✅ Done |
| sbmh | Somerset Bay and Modern History | +$50/+2.2% | user_rate_normalization | ✅ Done |
| ah | Alfresco Home | +$134/+9.2% | user_rate_normalization | ✅ Done |
| abol | America's Backyards | +$24/+3.3% | at_book_tier_shift | ✅ Done — ⚠️ DATA ACCURACY FLAG (Angie: cancelled cart, only eCat billed) |
| bp | Buster & Punch | +$44/+2.5% | included_user_reduction | ✅ Done — ⚠️ DATA ACCURACY FLAG (Angie: only eCat at $725+$25/user) |
| etl | ELICO LTD. | +$74/+10.2% | user_rate_normalization + included_user_reduction | ✅ Done — etl is 10.2%, borderline Format A/B |
| kii | Kennedy International | +$8/+0.6% | at_book_tier_shift | ✅ Done — ⚠️ ANNUAL CONTRACT (Finance must confirm renewal date) |
| lpf | Linon/Powell Furniture | +$65/+2.8% | user_rate_normalization | ✅ Done |
| lss | Lifestyle Solutions | +$24/+3.3% | at_book_tier_shift | ✅ Done |
| mh | Magnussen Home | +$138/+7.9% | user_rate_normalization + included_user_reduction | ✅ Done |
| ril | Ratana International Ltd. | +$140/+6.5% | tier_base_increase | ✅ Done |
| soi | Silver One | +$24/+3.3% | at_book_tier_shift | ✅ Done — ⚠️ bundle_config_mismatch |
| swc | Sauder Woodworking | +$24/+3.3% | at_book_tier_shift | ✅ Done |
| ufi | Universal Furniture | +$260/+9.0% | user_rate_normalization | ✅ Done — ⚠️ support fire (7 days open) |
| wwjc | Wildwood/Chelsea House | +$185/+8.0% | platform_discount_correction | ✅ Done — ⚠️ support fire (27 days open) |

---

## Format B Account Status

All 19 accounts drafted 2026-05-19. 19/19 complete.

| ord_id | Account | Delta | Driver | Status |
|---|---|---|---|---|
| cci | Currey & Company | +$305/+13.9% | user_rate_normalization | ✅ Done |
| gl | Golden Lighting | +$360/+18.6% | discount_correction | ✅ Done |
| ih | Interlude Home | +$395/+20.8% | user_rate_normalization | ✅ Done |
| afx | AFX, Inc. | +$318/+43.9% | user_rate_normalization + included_user_reduction | ✅ Done |
| bri | Bulbrite | +$349/+14.2% | included_user_reduction | ✅ Done |
| bsc | Butler Specialty Company | +$169/+29.1% | platform_discount_correction | ✅ Done |
| df | Designer's Fountain | +$296/+40.8% | included_user_reduction | ✅ Done |
| fal | Fine Art Handcrafted Lighting | +$344/+26.0% | included_user_reduction | ✅ Done |
| fc | Furniture Classics | +$285/+14.2% | tier_base_increase | ✅ Done |
| gblx | Globalux Lighting & Fans | +$279/+20.7% | included_user_reduction | ✅ Done — ltm_orders=0, composite narrative fallback |
| heb | Home Essentials & Beyond | +$274/+37.8% | user_rate_normalization + included_user_reduction | ✅ Done |
| hf | Hooker Furnishings | +$154/+18.8% | included_user_reduction | ✅ Done — image upgrade add-on absorbed into T1 |
| mli | Maxim Lighting | +$312/+15.7% | user_rate_normalization + multi_org_retirement + included_user_reduction | ✅ Done |
| ol | Oly Studio | +$180/+16.1% | tier_base_increase | ✅ Done — CPQ + PCI add-ons absorbed into T2 |
| rf | Rowe Furniture | +$290/+32.8% | user_rate_normalization + included_user_reduction | ✅ Done |
| sca | Shadow Catchers | +$224/+30.9% | user_rate_normalization + included_user_reduction | ✅ Done |
| uhc | Uniware Housewares Corp. | +$362/+49.9% | user_rate_normalization + included_user_reduction | ✅ Done |
| vl | Ciana Varaluz LLC | +$224/+17.4% | user_rate_normalization + included_user_reduction | ✅ Done |
| yw | Yutzy Woodworking | +$354/+71.5% | special_arrangement | ✅ Done — ⚠️ Finance sign-off required before send |

---

## What's Next (in priority order)

1. **mlc value anchor** — operator decision: add first sentence or accept omission before send
2. **shl support fire** — ⚠️ flagged in routing block and delivery email; operator decides send timing
3. **Data accuracy verification** — abol and bp (Angie flagged potential billing errors in both accounts)
4. **Format C** — not needed until wave 1 responses come in

---

## Key Data Files

| File | What it's authoritative for |
|---|---|
| `Pricing Migration/migration_comm_tiers_2026-05-19.csv` | Comm action, tier, flags for all 109 accounts |
| `~/Downloads/migration_revenue_model_2026-05-14 (2).html` | MRR, delta, health, tier math (cross-check) |
| `Pricing Migration/_master-account-data-v6.2.csv` | Driver, pricing breakdown, health scores, support_fire, composite_narrative (PRIMARY) |
| `Pricing Migration/format-b-notices/_brief-template.md` | Format B brief template (all 8 driver blocks) |
| `Pricing Migration/ceo-letter-notices/_brief-template.md` | CEO Letter brief template (all 8 driver blocks) |
