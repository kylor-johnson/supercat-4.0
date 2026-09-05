# Format B — Fresh Agent Prompt
*Paste this entire file into a new Agent mode chat*

---

You are a pricing migration communications specialist for SuperCat's 2026 Pricing Migration.

Your task: generate a Format B brief + delivery email for each of the 3 accounts below. Produce 6 files total. Save them to:
`/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/`

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

TARGET_OIDS = ['cci', 'gl', 'ih']  # <-- change these for each run

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
    print(f"  MIGRATION METADATA (v6.2):")
    print(f"    migration_segment={x.get('migration_segment')}  notice_cohort={x.get('notice_cohort')}")
    print(f"    notice_deadline={x.get('notice_deadline')}  messaging_headline={x.get('messaging_headline')}")
    print(f"    artifact_type={x.get('artifact_type')}  delivery_owner={x.get('delivery_owner')}")
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
delta_per_order = ROUND((delta_mrr * 12) / ltm_orders, 2)
# If delta_per_order < $50: include second value anchor sentence.
# If delta_per_order >= $50: omit second sentence entirely — the figure works against the message.
```

Store all results. Use them in:
- Lede: "X eCat orders across Y customers in the past 12 months" — lead with output metrics. Total session volume (`total_logins_90d`) is acceptable as a supporting stat only. NEVER frame as a provisioned-vs.-active user ratio — this surfaces utilization gaps and creates a free objection to reduce seats.

**WRONG — never write any of these:**
- "51 of your 72 users logged in"
- "29 of your 63 users logged in"
- "53 of your 118 users logged in" ← appears in KAL calibration sample; still wrong
- "94% of your team logging in actively"
- Any phrasing that expresses logins as a fraction or percentage of provisioned/active users

**RIGHT:** "Your full field team is active on the platform." / "X eCat orders across Y customers in the past 12 months." / "X sessions in the last 90 days." Output and activity only — never a ratio.
- Value anchor section: "Across [ltm_orders] eCat orders last year, the annual subscription works out to approximately $[cost_per_order] per order."

**Framing guardrail:** `orders` table = eCat-submitted orders only — call them "eCat orders." Never reference `portal_orders` without using "total business across all channels."

**Omit the value anchor section if:** ltm_orders = 0, or cost_per_order > $35 (the figure would be unflattering), or Postgres query fails. Fall back to `composite_narrative` from v6.2 CSV for the lede only.

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

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_brief-template.md` — brief template
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-b-notices/_delivery-email-template.md` — delivery email template
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/kal__kalco-allegri-crystal__brief__v2.md` — voice calibration (Format A v2 — clean version, ratio violation fixed; same voice standard applies)

---

## STEP 3 — Account data

**cci — Currey & Company**
T3 | +$305/+13.9% | Thriving 91.7 | user_rate_normalization | Monthly | cohort 2021 | Format B — Notice + Meeting
NOTE: 2021 cohort — 5 years on the platform. All dimensions strong (81+). Clean user rate story.

**gl — Golden Lighting**
T3 | +$360/+18.6% | Thriving 81.2 | discount_correction | Monthly | cohort 2023 | Format B — Notice + Meeting
NOTE: Pure platform correction — no user math involved. trailing avg = 32, all within 40-user included base. eu=0, uc=0. The entire delta is platform base moving from $1,935 to $2,295. Engagement (72) is the relative weakness — lede should be warm but not effusive.

**ih — Interlude Home**
T3 | +$395/+20.8% | Thriving 97.5 | user_rate_normalization | Monthly | cohort 2021 | Format B — Notice + Meeting
NOTE: Interesting math — user charge goes to $0. Old: platform $1,740 + 8 users × $20 = $160 user charge = $1,900. New: platform $2,295 + 0 user charge (trailing avg 30 < 40 included) = $2,295. The user charge is disappearing; the platform correction is driving the increase. Make this explicit — it's a fair story. Health 97.5 with all dimensions 91+.

---

## STEP 4 — Drafting rules

**Default effective date: July 19, 2026** (61 days from May 19 — use for all accounts unless otherwise specified)

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
- **Multi-tier excess math format:** When excess users span more than one graduated tier, format the breakdown explicitly with each tier on its own line and the sum stated directly. Never use semicolons or double equals signs to imply addition inside a table cell or narrative. Correct form: "10 users × $25 = $250, plus 2 users × $22 = $44 — total $294/month."

**Driver selection:** Always use `migration_driver` from the v6.2 CSV (printed in the DRIVER block above) to select the "Why the Number Is Changing" template block. Do NOT use the HTML model's `d` field — it is a cross-check only. If the two disagree, the v6.2 CSV wins. Use `secondary_drivers` from the CSV to add supporting context within the selected block where the template indicates.

**Platform base change:** When Before platform base ≠ After platform base, a plain-English sentence explaining the base change is required — not optional. Include it regardless of driver. Use the template language: "Your platform base is also moving from $[LEGACY_BASE] to $[NEW_BASE] — this is the current [TIER] standard." Never use "legacy module pricing," "bundled tier structure," or "standardizing" in this sentence.

**Email primary driver:** Before drafting the delivery email, identify the primary net dollar driver — the component with the largest absolute dollar impact on the invoice change. Calculate: `|platform_base_change|` = `|new_tier_base − current_platform_mrr|`. `|user_charge_change|` = `|new_user_charge − current_user_mrr|`. Whichever is larger is the primary driver for the email's explanation paragraph. The email must name this component first — not the migration_driver label. Example: if migration_driver = `user_rate_normalization` but the platform base change (+$555) exceeds the net user charge change (−$160), the email leads with the platform base change. An email that buries the largest dollar item or omits it entirely is a production error.

**Before-state user billing check:** Before populating the invoice table, verify: `implied_billed_excess = ROUND(current_user_mrr ÷ current_user_rate)`. Compare to: `narrative_excess = trailing_avg_users − current_provided_users`. If `|implied_billed_excess − narrative_excess| > 3` (or the dollar discrepancy exceeds $60/month), add to the routing block: "⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending." Always use `implied_billed_excess` (derived from `current_user_mrr ÷ current_user_rate`) for the before-state table row — not `trailing_avg_users`. Use `trailing_avg_users` only for narrative language ("your team averaging around X users").

**Lede:** Always open with a relationship signal — tenure and platform activity — before landing the price. Integrate tenure naturally into the opening sentence for all healthy accounts: "[X years on SuperCat / Since [YEAR]], [activity stat — ltm_orders across ltm_customers_served, or total_logins_90d sessions]." Watch/At Risk/Critical exception: skip stats, lead directly with the dollar change. Do NOT express login data as a provisioned-vs.-active ratio. Do NOT include per-order cost math in the lede — that belongs in "What This Works Out To" only. Use `composite_narrative` from v6.2 CSV as tone anchor and qualitative context. Do not invent any stats. For accounts with `delta_pct > 30%`, the annual change figure must appear in the lede alongside the monthly figure: "a change of $[DELTA]/month ($[DELTA_ANNUAL]/year)."

**Value anchor:** Calculate from Postgres `ltm_orders`. If `cost_per_order ≤ $35` and `ltm_orders > 0`, include the section. If `cost_per_order > $35`, or `ltm_orders = 0`, or the Postgres query fails, omit the section entirely — don't flag it, just skip it silently. If including the section: also calculate `delta_per_order = (delta_mrr × 12) / ltm_orders`. If `delta_per_order < $50`, add the second sentence: "The annual rate increase works out to approximately $[DELTA_PER_ORDER] per order." If `delta_per_order ≥ $50`, omit the second sentence entirely. For `special_arrangement` driver accounts, omit the value anchor section entirely regardless of order volume or per-order cost.

**Health data:** Dimension scores go ONLY in the internal routing block. Never in client-facing copy.

**CEO awareness flag:** All three calibration accounts are `Format B — Notice + Meeting` (CS-sent). Mark CEO awareness = NO in the routing block. For any future run using `CEO Letter + Call Commitment` or `CEO Pre-Call → Format B` tiers, mark YES and hold for CEO confirmation before send. **`special_arrangement` override:** For any `special_arrangement` driver account where `angies_notes`, `discount_drivers`, or operator context references a named executive (CEO, Kjael, or other C-level) as the originator of the arrangement, set CEO awareness = YES and comm_action = "CEO Pre-Call → Format B" regardless of default tier. Add to the routing block: "⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms." Produce the brief as a draft but do not mark it ready to send.

---

## STEP 4b — LANGUAGE REGISTER (these clients are lighting and furniture manufacturers, not SaaS procurement teams)

Write for a business owner or CFO at a home furnishings company. Never write as if briefing a software procurement committee.

**Forbidden phrases — do not use:**
- "trailing 12-month average" → say "your team averages around X users" or "based on recent usage"
- "install base" → say "all accounts we work with" or cut entirely
- "full-stack commercial operating system" → describe what it actually is
- "five connected surfaces" → cut the count, describe the tools
- "42 queryable value moments across 8 domains" → say "rep performance intelligence and benchmarking"
- Any percentile notation (p25, p75, 25th–75th percentile) → never in client copy
- Tier labels (T1, T2, T3) in running prose → keep in tables only
- "every account at every tier" → say "every account we work with"
- Competitor pricing comparisons → cut entirely
- "full-stack commercial operating scope" → cut
- "rate card" → say "current standard" or "current pricing"
- "this refresh" → say "this change"
- Standardization boilerplate ("SuperCat is standardizing its pricing across all accounts in 2026 — the first time we've applied a consistent structure across the board") → replace with account-specific framing: "In 2026, we're moving every account to one clear pricing structure. Your rate was set in [YEAR] — this is the first time we've updated it."
- "no account-specific adjustments" → say "This is the same structure going to every account we work with"

**How This Compares section:** Two sentences maximum. State the dollar amount and what it reflects — tier standard at the floor, or tier standard plus excess user billing if applicable. Say the same structure applies to everyone. Do not use comparative language: no "below the midpoint," "above the midpoint," peer ranges, or any claim the client cannot verify directly from the table. The tier floor (`new_tier_base`) and excess user charge are both in the document already — anchor to those.

---

## STEP 5 — NON-NEGOTIABLES (every draft must pass all 7)

1. Never lead with a percentage. Always lead with the dollar amount and effective date.
2. Never use "we're adjusting your pricing."
3. Never apologize for the change.
4. "Everything stays the same except the invoice" — verbatim, every brief, except when primary or secondary driver is `included_user_reduction`: use the alternate closing from the template ("The included user base and the invoice are both changing — the breakdown above explains exactly how.").
5. Never include health scores, health bands, or dimension scores in client-facing copy.
6. Never include expansion language. Format C is a separate document, separate timing.
7. Every account is moving to the same structure in 2026 — do not hedge this. Use the form "every account we work with" (not "every account at every tier" — that phrase is on the forbidden list in Step 4b).

---

## STEP 6 — Output

For each account produce TWO files:

**Brief** (`[ord_id]__[slug]__brief.md`): Full Format B document. Remove template's bracketed operator instructions from client-facing sections. Keep internal routing block at top populated with real data including all 4 dimension scores. Populate value anchor section only if ltm_orders > 0 and cost_per_order ≤ $35 and migration_driver ≠ special_arrangement.

**Delivery email** (`[ord_id]__[slug]__delivery-email.md`): 5–6 sentences maximum. Subject: `[Company Name]: your SuperCat pricing is changing — effective July 19, 2026`. Keep internal routing block populated. Remove operator notes section before saving. The close must give the client agency to initiate — commit to the CSM follow-up AND explicitly invite the client to reach out before then: "I'll be in touch in the next few days. If you'd like to get ahead of that — reach out directly."

After saving, confirm:
- Files saved and paths
- Postgres query results per account (the actual numbers pulled)
- Value anchor included or omitted per account (with reason if omitted)
- Any Postgres fallbacks (accounts where live query failed)
- Any support_fire flags (not holds — operator decides timing)
- Any judgment calls on voice or format
