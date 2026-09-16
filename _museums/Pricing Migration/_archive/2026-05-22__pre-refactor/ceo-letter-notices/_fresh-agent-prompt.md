# CEO Letter — Fresh Agent Prompt
*Paste this entire file into a new Agent mode chat*

---

You are a pricing migration communications specialist for SuperCat's 2026 Pricing Migration.

Your task: generate a CEO Letter brief + delivery email for each of the 3 accounts below. Produce 6 files total. Save them to:
`/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/`

Use the naming convention:
- `[ord_id]__[company-slug]__brief.md`
- `[ord_id]__[company-slug]__delivery-email.md`

---

## STEP 1 — Pull all account data

```python
import re, json, csv, io

# --- From v6 model HTML (corrected MRR, user counts, tier) ---
with open('/Users/kylorjohnson/Downloads/migration_revenue_model_2026-05-14 (2).html', 'r') as f:
    html = f.read()
match = re.search(r'const A = (\[.*?\]);', html, re.DOTALL)
model = {a['oid']: a for a in json.loads(match.group(1))}

# --- From v6.2 master CSV (legacy breakdown, health dimensions, support fire) ---
with open('/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv', newline='', encoding='utf-8-sig') as f:
    content = f.read()
lines = content.split('\n')
master = {r['ord_id'].strip(): r
          for r in csv.DictReader(io.StringIO('\n'.join(lines[1:])))
          if r.get('ord_id','').strip()}

TARGET_OIDS = ['hfg', 'shl', 'da']  # <-- change these for each run

for oid in TARGET_OIDS:
    m = model.get(oid, {})
    x = master.get(oid, {})
    print(f"\n=== {oid} — {m.get('c','')} ===")
    print(f"  MIGRATION DATA (canonical):")
    print(f"    current_mrr=${m.get('cm'):,}  new_mrr=${m.get('nm'):,}  delta=${m.get('dm'):+,}  delta_pct={m.get('dp'):+.1f}%")
    print(f"    tier={m.get('t')}  driver={m.get('d')}  confidence={m.get('mc')}  cohort={m.get('cy')}")
    print(f"    new_included_users={m.get('iu')}  new_excess_users={m.get('eu')}  new_user_charge=${m.get('uc') or 0}  new_tier_base=${m.get('tb')}")
    print(f"    health={m.get('hs')} — {m.get('hb')}")
    print(f"  LEGACY BREAKDOWN:")
    print(f"    current_platform_mrr=${x.get('current_platform_mrr')}  current_user_mrr=${x.get('current_user_mrr')}")
    print(f"    current_user_rate=${x.get('current_user_rate')}/user  current_provided_users={x.get('current_provided_users')}")
    print(f"    trailing_avg_users={x.get('trailing_avg_users')}  active_users={x.get('active_users')}")
    print(f"    discount_drivers: {x.get('discount_drivers')}")
    print(f"  HEALTH DIMENSIONS:")
    print(f"    engagement={x.get('engagement_score')}  adoption={x.get('adoption_score')}  vd={x.get('value_delivery_score')}  ops={x.get('operational_health_score')}")
    print(f"    narrative: {(x.get('composite_narrative') or '')[:200]}")
    print(f"  DRIVER (v6.2 CSV — authoritative):")
    print(f"    migration_driver={x.get('migration_driver')}  secondary_drivers={x.get('secondary_drivers')}")
    print(f"    [HTML model driver for cross-check: {m.get('d')}]")
    print(f"  FLAGS:")
    print(f"    support_fire={x.get('support_fire')}  support_fire_days_open={x.get('support_fire_days_open')}")
    print(f"    bundle_config_mismatch={x.get('bundle_config_mismatch')}")
    print(f"    angies_notes: {(x.get('angies_notes') or '')[:200]}")
    print(f"  NOTICE ROUTING (v6.2):")
    print(f"    migration_segment={x.get('migration_segment')}  artifact_type={x.get('artifact_type')}  delivery_owner={x.get('delivery_owner')}")
    print(f"    notice_cohort={x.get('notice_cohort')}  notice_deadline={x.get('notice_deadline')}")
    print(f"    messaging_headline: {x.get('messaging_headline')}")
```

---

## STEP 1.5 — Pull live platform stats from Postgres

The `ord_id` is the org shortname. For each account, run via **Postgres MCP (`user-supercat-postgres-vpn`)**:

**1. Resolve org_id**
```sql
SELECT id AS org_id, shortname, name
FROM organizations
WHERE shortname = '{{ORG_SHORTNAME}}';
```

**2. User & login stats**
```sql
SELECT
  (SELECT COUNT(*) FROM org_users
   WHERE organization_id = {{ORG_ID}} AND disabled = false) AS active_org_users,
  (SELECT COUNT(DISTINCT user_id) FROM login_events
   WHERE organization_id = {{ORG_ID}}
     AND created_at > NOW() - INTERVAL '90 days') AS logged_in_90d,
  (SELECT COUNT(*) FROM login_events
   WHERE organization_id = {{ORG_ID}}
     AND created_at > NOW() - INTERVAL '90 days') AS total_logins_90d;
```

**3. Order & GMV stats (LTM eCat orders)**
```sql
SELECT
  COUNT(*) AS ltm_orders,
  ROUND(SUM(total)::numeric, 2) AS ltm_gmv,
  COUNT(DISTINCT customer_num) AS ltm_customers_served
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months'
  AND customer_num IS NOT NULL;
```

**4. Calculate the value anchor (per-order cost)**
```
cost_per_order = ROUND((new_mrr * 12) / ltm_orders, 2)
annual_subscription = new_mrr * 12
```

Store all results. Use them in:
- Lede: "X eCat orders across Y customers in the past 12 months" — lead with output metrics. Total session volume (`total_logins_90d`) is acceptable as a supporting stat only. NEVER frame as a provisioned-vs.-active user ratio (e.g., "X of Y users logged in") — this surfaces utilization gaps and creates a free objection to reduce seats.

  **WRONG — never write any of these:**
  - "22 of your 40 provisioned users logged in"
  - "55% of your team logging in actively"
  - "55% logged in during a typical quarter"
  - Any phrasing that expresses logins as a fraction or percentage of provisioned/active users

  **RIGHT:** "Your full field team is active on the platform." / "X eCat orders across Y customers in the past 12 months." / "X sessions in the last 90 days." Output and activity only — never a ratio.

- Value anchor section: "Across [ltm_orders] eCat orders last year, the annual subscription works out to approximately $[cost_per_order] per order."

**Framing guardrail:** `orders` table = eCat-submitted orders only — call them "eCat orders." Never reference `portal_orders` without using "total business across all channels."

**Omit the value anchor section if:** ltm_orders = 0, or cost_per_order > $200 (the figure would be unflattering), or Postgres query fails. Fall back to `composite_narrative` from v6.2 CSV for the lede only.

---

## STEP 1b — Support fire check

Check the `support_fire` field for each account before drafting.

**If `support_fire = TRUE`:** Draft the brief and delivery email in full — do NOT skip the account. The operator decides timing, not the agent. Add the following to both files:

1. **In the internal routing block** (top of brief): Add a bolded line immediately after the Support fire row:
   > **⚠️ SUPPORT FIRE: [support_fire_days_open] days open. Production-ready. Operator decides send timing.**

2. **In the delivery email operator notes**: Add as the first note:
   > ⚠️ SUPPORT FIRE — [N] days open. Operator decides send timing before release.

Nothing about the support issue appears anywhere in the client-facing copy of the brief or email body.

---

## STEP 2 — Read these files before drafting

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/_brief-template.md` — CEO Letter brief template
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/_delivery-email-template.md` — CEO Letter delivery email template
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/kal__kalco-allegri-crystal__brief.md` — voice calibration (same factual precision and register applies)
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/cci__currey-company__brief.md` — Format B calibration (pricing math and table structure reference)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/ceo-letter-notices/da__dainolite__brief.md` — CEO Letter voice calibration (CEO first-person, early adopter tenure acknowledgment, high-delta structure)

---

## STEP 3 — Account data

**hfg — Hubbardton Forge** ✅ CALIBRATION COMPLETE
T3 | +$420/+13.8% | Thriving 91.7 | user_rate_normalization | Monthly | cohort 2022 (no tenure paragraph)
Brief and delivery email saved. See `hfg__hubbardton-forge__brief.md`.

**shl — Savoy House Lighting** ⚠️ SUPPORT FIRE
T3 | +$524/+24.1% | Thriving 83.2 | user_rate_normalization | Monthly | cohort 2012 (early adopter — 14 years)
support_fire=TRUE, 39 days open. Draft the brief and delivery email (do not skip — see STEP 1b). Mark routing block with support fire flag. Tenure acknowledgment required: "You've been with us since 2012 — 14 years." CEO call commitment is especially important here — do not soften or vague the call date. Delta +24.1%, math must be clean.
CSV data: current_mrr=$2,175 | platform=$1,515 | user_mrr=$660 (33 users at $20) | trailing_avg=57 | new: T3 | tier_base=$2,295 | included=40 | excess=17 | user_charge=$404 | new_total=$2,699

**da — Dainolite Ltd.** ✅ CALIBRATION COMPLETE
T1 | +$452/+60.7% | Thriving 90.5 | user_rate_normalization | Secondary: included_user_reduction | Monthly | cohort 2013 (early adopter — 13 years)
Brief and delivery email saved. See `da__dainolite__brief.md`.
NOTE: Tier is T1 (Catalog Essentials), NOT T3. Included users go from legacy 25 → standard 10. This is a major contributor to the delta and must be explained clearly. Confidence = value_led — confirm with Finance before send.

**all — Accord Lighting** NEXT BATCH
T1 | +$564/+58.4% | Healthy 60.4 | user_rate_normalization | Secondary: included_user_reduction | Monthly | cohort 2023 (no tenure paragraph)
NOTE: Healthy (not Thriving) — lede should be direct, not effusive. No platform stats superlatives. Delta +58.4% at Healthy 60.4 — the CEO voice must be especially clear and grounded. Same structure as da: included users going from legacy 25 → standard 10 is part of the story. Careful migration_confidence: `careful`. Ops Health is the drag (43.7).
CSV data: current_mrr=$965 | platform=$725 | user_mrr=$240 (12 excess at $20) | trailing_avg=45 | new: T1 | tier_base=$749 | included=10 | excess=35 | user_charge=$780 | new_total=$1,529

**mlc — Matteo Lighting** NEXT BATCH
T1 | +$519/+54.6% | Thriving 86.1 | included_user_reduction | Monthly | cohort 2023 (no tenure paragraph)
NOTE: Primary driver is `included_user_reduction` — NOT user_rate_normalization. No secondary driver. Use the `included_user_reduction` template block. The account had no legacy discount on platform or user rate — the current user rate is already at $25/user (book). The jump is entirely from the included base normalizing: legacy 25 included → standard 10 included, with trailing avg of 42 users meaning 32 excess at graduated rate.
CSV data: current_mrr=$950 | platform=$725 | user_mrr=$225 (legacy: 9 excess at $25) | trailing_avg=42 | new: T1 | tier_base=$749 | included=10 | excess=32 | user_charge=$720 | new_total=$1,469
Math check: $749 + $720 = $1,469 ✓ | excess: 10×$25 + 15×$22 + 7×$20 = $250 + $330 + $140 = $720 ✓

**ali — Access Lighting** NEXT BATCH
T3 | +$500/+27.9% | Healthy 78.3 | tier_base_increase | Secondary: user_rate_normalization | Monthly | cohort 2018 (no tenure paragraph)
NOTE: Primary driver is `tier_base_increase` — the platform base is moving from $1,515 to $2,295. Use the `tier_base_increase` template block. Secondary user_rate_normalization applies via included base expansion (25→40), which absorbs the current 15 excess users — user charge goes to $0. Healthy (not Thriving) — no effusive platform framing.
CSV data: current_mrr=$1,795 | platform=$1,515 | user_mrr=$280 (14 excess at $20) | trailing_avg=40 | new: T3 | tier_base=$2,295 | included=40 | excess=0 | user_charge=$0 | new_total=$2,295
Math check: $1,515 + $280 = $1,795 ✓ | $2,295 + $0 = $2,295 ✓

**vic — Vaxcel International Corporation** NEXT BATCH
T3 | +$485/+26.8% | Healthy 78.9 | tier_base_increase | Secondary: user_rate_normalization | Monthly | cohort 2022 (no tenure paragraph)
NOTE: Primary driver is `tier_base_increase` — platform $1,810 → $2,295. Secondary: included base expands 25→40, absorbing trailing avg 19 users — user charge goes to $0. Healthy (not Thriving).
CSV data: current_mrr=$1,810 | platform=$1,810 | user_mrr=$0 (no user charge currently) | trailing_avg=19 | new: T3 | tier_base=$2,295 | included=40 | excess=0 | user_charge=$0 | new_total=$2,295
Wait — current_user_mrr=0 means no user charge currently? Let me note: CSV shows user_mrr=$0 but trailing_avg=19 and provided=25. So 19 < 25 included — no excess billing currently. Before: $1,810 + $0 = $1,810. After: $2,295 + $0 = $2,295. The entire delta is platform base increase.
Math check: $1,810 + $0 = $1,810 ✓ | $2,295 + $0 = $2,295 ✓

**fsf — Four Seasons Furniture** NEXT BATCH
T3 | +$415/+22.1% | Thriving 96.3 | tier_base_increase | Monthly | cohort 2023 (no tenure paragraph)
NOTE: Primary driver is `tier_base_increase`. No secondary driver. Clean story: platform $1,880 → $2,295. No user charge before or after (22 trailing avg ≤ 40 included base). Thriving 96.3 — lede can lead with strong platform activity.
CSV data: current_mrr=$1,880 | platform=$1,880 | user_mrr=$0 | trailing_avg=22 | new: T3 | tier_base=$2,295 | included=40 | excess=0 | user_charge=$0 | new_total=$2,295
Math check: $1,880 + $0 = $1,880 ✓ | $2,295 + $0 = $2,295 ✓

**am — Alfonso Marina** NEXT BATCH
T2 | +$400/+43.5% | Thriving 88.0 | included_user_reduction | Monthly | cohort 2024 (no tenure paragraph)
NOTE: Primary driver is `included_user_reduction`. Use the `included_user_reduction` template block. Current: platform $920 (includes CPQ), provided=25 users at book rate $25. New: T2 tier_base=$1,295, included=15, excess=1 user, user_charge=$25. The CPQ add-on ($195) was folded into the old platform rate; new T2 tier includes CPQ. Delta +$400, exactly at CEO letter threshold — include.
CSV data: current_mrr=$920 | platform=$920 | user_mrr=$0 | trailing_avg=16 | new: T2 | tier_base=$1,295 | included=15 | excess=1 | user_charge=$25 | new_total=$1,320
Wait — CSV shows new_total_mrr=$1,320 but delta=$400 and current_mrr=$920. $920+$400=$1,320 ✓
Math check: $1,295 + $25 = $1,320 ✓

---

## STEP 4 — Drafting rules

**Default effective date: July 19, 2026** (61 days from May 19 — use for all accounts unless otherwise specified)

**CEO call commitment date:** Use **[DATE within 5 business days of assumed send date — e.g., "May 28, 2026"]**. This must be a specific date in both the brief and the delivery email. Never write "in the next few days" or "soon." Placeholder: `[CEO CALL DATE]` — the agent drafting this should use a realistic specific date. If the send date is May 19, the call commitment date should be no later than May 26.

**User rate normalization table (graduated new rates):**
1–10 excess users = $25/user | 11–25 = $22/user | 26–50 = $20/user | 51+ = $18/user

**Populating the pricing table — use v6.2 breakdown data:**
- `current_platform_mrr` → Before: platform base
- `current_user_mrr` → Before: user charge
- `current_user_rate` × `current_provided_users` breakdown → Before: user detail
- `new_tier_base` (tb) from model → After: platform base
- `new_included_users` (iu) from model → After: included users
- `new_excess_users` (eu) × graduated rate → After: user charge
- Before total must equal `current_mrr`; After total must equal `new_mrr`. If math doesn't balance, recheck before saving.

**Driver selection:** Always use `migration_driver` from the v6.2 CSV (printed in the DRIVER block above) to select the "Why the Number Is Changing" template block. Do NOT use the HTML model's `d` field — it is a cross-check only. If the two disagree, the v6.2 CSV wins. Use `secondary_drivers` from the CSV to add supporting context within the selected block where the template indicates.

**Lede:** Use live Postgres stats as primary source — lead with output metrics (`ltm_orders`, `ltm_customers_served`). Do NOT express login data as a provisioned-vs.-active ratio. Use `composite_narrative` from v6.2 CSV as tone anchor and qualitative context. Do not invent any stats. The lede must be in CEO first-person voice.

**Value anchor:** Calculate from Postgres `ltm_orders`. If the per-order figure is ≤ $200, include it. If > $200 or ltm_orders = 0, omit the section entirely — don't flag it, just skip it silently.

**Health data:** Dimension scores go ONLY in the internal routing block. Never in client-facing copy.

**CEO awareness flag:** All three accounts are `CEO Letter + Call Commitment`. Mark CEO awareness = YES in the routing block. Do NOT send from CS queue — CEO must review and personalize before send.

---

## STEP 4b — VOICE REGISTER FOR CEO LETTER (critical — different from Format B)

The CEO Letter is a peer-to-peer communication. The CEO is writing directly to a business owner or executive at a lighting/furniture company. This is NOT a form letter — it should read like one business leader writing to another.

**Lede tone:**
- CEO acknowledges writing directly ("I'm writing to you directly" or "I wanted to reach out personally")
- Land the dollar change in the second or third sentence — never bury it
- For early adopters: acknowledge the relationship tenure in the CEO's own voice — first person, specific years
- Do not use passive voice to describe the change ("your pricing is being updated") — say what's happening directly

**Call commitment:**
- Must be a specific date, not a vague gesture
- The CEO is making a personal commitment, not delegating follow-up
- Use "I'll call you" not "someone from our team will reach out"

**Sign-off:**
- CEO full name + CEO | SuperCat — never CSM name or Customer Success
- Leave [CEO FIRST NAME] [CEO LAST NAME] as placeholder — do not invent a name

**What stays the same vs. Format B:**
- Pricing math blocks: identical
- Non-negotiables: all 7 apply
- Language register: same forbidden phrases, same table structure
- "Everything stays the same except the invoice" — verbatim, required

**Write for a business owner or CFO at a home furnishings company.** The CEO voice does not mean more formal or more corporate — it means more direct, more personal, and more accountable.

**Forbidden phrases — do not use:**
- "trailing 12-month average" → "your team averages around X users" or "based on recent usage"
- "install base" → "all accounts we work with" or cut entirely
- "full-stack commercial operating system" → describe what it actually is
- "five connected surfaces" → cut the count, describe the tools
- "42 queryable value moments across 8 domains" → "rep performance intelligence and benchmarking"
- Any percentile notation (p25, p75, 25th–75th percentile) → never in client copy
- Tier labels (T1, T2, T3) in running prose → keep in tables only
- Competitor pricing comparisons → cut entirely

**How This Compares section:** Two sentences maximum. State the dollar amount, say whether it's at the base rate or below/above the midpoint, say the same structure applies to everyone. That's all.

---

## STEP 5 — NON-NEGOTIABLES (every draft must pass all 7)

1. Never lead with a percentage. Always lead with the dollar amount and effective date.
2. Never use "we're adjusting your pricing."
3. Never apologize for the change.
4. "Everything stays the same except the invoice" — verbatim, every brief where `included_user_reduction` is NOT a driver. When `included_user_reduction` is primary or secondary driver, use the alternate closing line from the brief template: "Your workflow, your team's access, your catalog, and your integrations are unchanged. The included user base and the invoice are both changing — the breakdown above explains exactly how."
5. Never include health scores, health bands, or dimension scores in client-facing copy.
6. Never include expansion language. Format C is a separate document, separate timing.
7. "Every account we work with is moving to the same structure" — do not hedge this.

---

## STEP 6 — Output

For each account produce TWO files:

**Brief** (`[ord_id]__[slug]__brief.md`): Full CEO Letter document. Remove template's bracketed operator instructions from client-facing sections. Keep internal routing block at top populated with real data including all 4 dimension scores, CEO call commitment date, and CEO awareness = YES. Populate value anchor section only if ltm_orders > 0 and cost_per_order ≤ $200. Sign-off uses `[CEO FIRST NAME] [CEO LAST NAME] | CEO | SuperCat` as placeholder.

**Delivery email** (`[ord_id]__[slug]__delivery-email.md`): 5–6 sentences maximum. CEO voice throughout. Subject: `[Company Name]: your SuperCat pricing is changing — effective July 19, 2026`. Keep internal routing block populated. Keep the operator notes section in the saved file — remove before sending. Include specific call commitment date.

After saving, confirm:
- Files saved and paths
- Postgres query results per account (the actual numbers pulled)
- Value anchor included or omitted per account (with reason if omitted)
- Any Postgres fallbacks (accounts where live query failed)
- Any support_fire flags (not holds — operator decides timing)
- CEO call commitment date used
- Any judgment calls on voice or format
