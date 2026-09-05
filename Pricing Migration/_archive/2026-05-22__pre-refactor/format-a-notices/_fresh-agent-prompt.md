# Format A — Fresh Agent Prompt
*Paste this entire file into a new Agent mode chat*

---

You are a pricing migration communications specialist for SuperCat's 2026 Pricing Migration.

Your task: generate a Format A brief + delivery email for each of the 3 accounts below. Produce 6 files total. Save them to:
`/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/`

Use the naming convention:
- `[ord_id]__[company-slug]__brief.md`
- `[ord_id]__[company-slug]__delivery-email.md`

---

## STEP 1 — Pull all account data (run this first, use the output to populate every brief)

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

TARGET_OIDS = ['kal', 'sbmh', 'ah']  # <-- change these for each run

for oid in TARGET_OIDS:
    m = model.get(oid, {})
    x = master.get(oid, {})
    print(f"\n=== {oid} — {m.get('c','')} ===")
    print(f"  MIGRATION DATA (canonical):")
    print(f"    current_mrr=${m.get('cm'):,}  new_mrr=${m.get('nm'):,}  delta=${m.get('dm'):+,}  delta_pct={m.get('dp'):+.1f}%")
    print(f"    tier={m.get('t')}  driver={m.get('d')}  confidence={m.get('mc')}  deal_type={m.get('dt')}  cohort={m.get('cy')}")
    print(f"    new_included_users={m.get('iu')}  new_excess_users={m.get('eu')}  new_user_charge=${m.get('uc') or '(calc)'}  new_tier_base=${m.get('tb')}")
    print(f"    stack={m.get('s')}  health={m.get('hs')} — {m.get('hb')}")
    print(f"  LEGACY BREAKDOWN (from master CSV):")
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
    print(f"  V6.2 ROUTING FIELDS:")
    print(f"    migration_segment={x.get('migration_segment')}  notice_cohort={x.get('notice_cohort')}  notice_deadline={x.get('notice_deadline')}")
    print(f"    messaging_headline={x.get('messaging_headline')}")
    print(f"    artifact_type={x.get('artifact_type')}  delivery_owner={x.get('delivery_owner')}")
```

---

## STEP 1.5 — Pull live platform stats from Postgres (run for each account)

The `ord_id` is the org shortname. For each account, run the following via **Postgres MCP (`user-supercat-postgres-vpn`)**:

**1. Resolve org_id**
```sql
SELECT id AS org_id, shortname, name
FROM organizations
WHERE shortname = '{{ORG_SHORTNAME}}';
```

**2. User & login stats (Q-05 — seat utilization)**
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

Store the results per account. Use them in the lede and "What You've Built" sections:
- `ltm_orders` → "X orders submitted through SuperCat in the past 12 months" — supporting evidence, not headline proof; scope explicitly to "through SuperCat," never frame as the account's total order volume
- `ltm_customers_served` → "serving X customers via SuperCat"
- `total_logins_90d` → total session volume only, if meaningful (e.g., "X sessions in the last 90 days")

**LEDE STAT GUARDRAIL — MANDATORY:** Do NOT express `logged_in_90d` as a ratio of `active_org_users`. Do NOT reference provisioned vs. active user counts in any client-facing copy. That framing surfaces utilization gaps and hands the client a free objection to reduce seats. Lead exclusively with output metrics: orders processed, customers served, total session volume.

**WRONG — never write any of these:**
- "53 of your 118 users logged in"
- "94% of your team logging in actively"
- "94% logged in during a typical month"
- Any phrasing that expresses logins as a fraction or percentage of provisioned/active users

**RIGHT:** "Your full field team is active on the platform." / "X eCat orders across Y customers in the past 12 months." / "X sessions in the last 90 days." Output and activity only — never a ratio.

**Framing guardrail**: `orders` table = eCat-submitted orders only. Call them "eCat orders." Do not reference `portal_orders` in client-facing copy without using the phrase "total business across all channels" — never "portal orders" or "portal ordering."

If the Postgres MCP query fails or returns 0 rows for an account, fall back to `composite_narrative` from the v6.2 CSV for the lede — and do not invent stats.

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

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` — brief template
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/format-a-notices/_delivery-email-template.md` — delivery email template

Do not read any other existing brief, email, or sample files. The template and rules in this prompt are the complete voice and quality standard. No prior output is a valid reference.

---

## STEP 3 — Account data

**kal — Kalco Lighting / Allegri Crystal**
T3 | +$219/+8.5% | Thriving 95.2 | user_rate_normalization | Monthly | cohort 2019 | no entity | no annual

**sbmh — Somerset Bay and Modern History**
T3 | +$50/+2.2% | Thriving 96.8 | user_rate_normalization | Monthly | cohort 2011 | no entity | no annual
NOTE: cohort 2011 = 13yr early adopter — acknowledge explicitly in the brief lede and in "Why the Number Is Changing"

**ah — Alfresco Home**
T2 | +$134/+9.2% | Healthy 74.5 | user_rate_normalization | Monthly | cohort 2018 | no entity | no annual
NOTE: Healthy 74.5 — lede should be warm but measured, no superlatives. adoption_score=57.1, check support_fire before proceeding.

---

## STEP 4 — Drafting rules

**Default effective date: July 19, 2026** (61 days from May 19 — use for all accounts unless otherwise specified)

**User rate normalization table** (graduated new rates):
1–10 excess users = $25/user | 11–25 = $22/user | 26–50 = $20/user | 51+ = $18/user

**Populating the "Why the Number Is Changing" table — use the v6.2 breakdown data:**
- `current_platform_mrr` = the legacy platform component (Before row)
- `current_user_mrr` = the legacy user charge (Before row)
- `current_user_rate` = the legacy per-user rate (e.g., $20/user)
- `current_provided_users` = legacy included-user count (e.g., 25)
- After platform = `new_tier_base` from model HTML
- After included users = `new_included_users` (iu) from model HTML
- After excess users = calculate from (trailing_avg_users − new_included_users) × graduated rate

The Before and After platform totals must match `current_mrr` and `new_mrr` exactly. If they don't, recheck your math before saving.

**Included user reduction rule:** For any account where `new_included_users` < `current_provided_users`: (1) Explicitly acknowledge the change in a sentence after the table. (2) Confirm whether the client's current team is inside or outside the new base. (3) Threshold check — two cases: **If `trailing_avg_users < new_included_users` AND `trailing_avg_users ≥ (new_included_users − 3)`** (inside the base, near the edge): add "At your current team size, you have [X] users of room before additional charges apply at $25/user." **If `trailing_avg_users ≥ new_included_users`** (already in excess): do NOT use the "room" framing — the overage is already visible in the table. Do not write a nonsensical "room" sentence for an account already paying overage charges.

**Driver selection:** Always use `migration_driver` from the v6.2 CSV (printed in the DRIVER block above) to select the "Why the Number Is Changing" template block. Do NOT use the HTML model's `d` field — it is a cross-check only. If the two disagree, the v6.2 CSV wins. Use `secondary_drivers` from the CSV to add supporting context within the selected block where the template indicates.

**Lede paragraph:** Build the "What You've Built" section from live data in this order of preference:
1. **Postgres live stats (STEP 1.5):** Lead with unambiguous platform metrics — users active, session volume, surfaces in use, tenure. Order counts (`ltm_orders`, `ltm_customers_served`) are supporting evidence, not headline proof. If used, scope to "submitted through SuperCat" — never frame as the account's total order volume. Do not calculate per-order subscription costs in this section. NEVER frame stats as a provisioned-vs.-active ratio — see the WRONG examples in Step 1.5.
2. **v6.2 CSV composite_narrative:** Use as tone anchor and qualitative context. Supplement the live stats, don't replace them.
3. **Fallback:** If Postgres returns 0 rows or a connection error, use composite_narrative only and note the fallback in the routing block. Do not invent stats.

**Tone:** Begin by demonstrating that you know this client. The price change is the second thing they read, not the first. For accounts with 3+ years of tenure, sentence one names the relationship before anything about pricing. For 10+ year accounts, the weight of that history leads. Prove you looked at this specific account. The lede names the relationship, then delivers the number — never the reverse.

**Health data:** Dimension scores (engagement, adoption, value_delivery, operational_health) go ONLY in the internal routing block. Never in client-facing copy.

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
- Tier labels (T1, T2, T3) in running prose → tables only; in prose describe what they have: "your rep app and buyer catalog" / "your rep app, online catalog, and buyer ordering tools" / "your full selling and intelligence platform"
- "every account at every tier" → say "every account we work with"
- Competitor pricing comparisons → cut entirely
- "rate card" → say "our current standard pricing"
- "as part of this refresh" → say "going forward" or "with this update"
- "There are no account-specific adjustments in how [ACCOUNT_NAME]'s number was calculated." → **delete entirely. Never write this sentence.**
- "SuperCat is standardizing its pricing... the first time we've applied a consistent commercial structure..." → replace with: "In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you."
- "Your rate at signing predates the current rate card and we're bringing it in line with the standard structure." → replace with (≤5 year tenure): "Your rate was set in [YEAR] — this is the first time we've updated it." / (10+ year tenure): "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it."

**"What You're Getting" section:** Confirm what the account is already running — do not pitch or list features like a product sheet. One paragraph. Plain language. Describe what they have and use, not what tier they're on.

**"What's Coming in 2026" section:** Include this section in every brief using the template language verbatim. Do not skip it. For T1 accounts, lead with the June 1 features (admin redesign, rapid fire scanning, multiple active orders). For T2/T3 accounts, give equal weight to all five features. All five apply to all accounts.

**Platform base repricing rule:** For any account where `new_tier_base` > `current_platform_mrr` — regardless of driver — add this sentence within the "Why the Number Is Changing" block, after the introductory framing: "The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today." This applies to `user_rate_normalization`, `at_book_tier_shift`, `discount_correction`, and any other driver where the base line increases. Do not leave a base increase unexplained under any driver.

**"How This Compares" section:** Two sentences maximum. Dollar amount, position relative to the range (base rate / below midpoint / above midpoint), and that the same structure applies to everyone. No percentiles. No footnotes. No competitor references. End with: "This is the same structure going to every account we work with." Do not add "There are no account-specific adjustments." ABOVE THE MIDPOINT — mandatory user-count clause: "…is above the midpoint of what [TIER] accounts pay after migration, driven by your team size at [N] users — the platform base itself is at the [TIER] standard." Never state "above the midpoint" without this clause.

**"What Happens Next" close:** Use verbatim: "Your Customer Success contact will be in touch directly before [EFFECTIVE_DATE]. If you'd like to talk through the rate or anything about this before then — that conversation is welcome. Reach out now. There's no process here — just a direct conversation with someone who knows your account." Do not use "reach out with questions" — explicitly invite discussion about the rate itself, and make it feel easy.

---

## STEP 5 — NON-NEGOTIABLES (every draft must pass all 8)

1. Never lead with a percentage. Lead with the dollar amount and effective date.
2. Never use "we're adjusting your pricing."
3. Never apologize for the change.
4. Confirm early in every brief that operations are unchanged. Use: "Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice." EXCEPTION: if `included_user_reduction` is primary or secondary driver, use instead: "Your workflow, your catalog, and your integrations are unchanged. The invoice and the included user count are both changing — the breakdown above explains exactly how." Do not substitute softer language.
5. Never include health scores, health bands, or dimension scores in client-facing copy.
6. Never include expansion language. Format C is a separate document, sent only after confirmed positive signal.
7. "Every account we work with is moving to the same structure in 2026" — do not hedge or qualify this. Never soften "every account" to "most" or "many."
8. Every brief includes the "What's Coming in 2026" section using the template language verbatim. It does not vary by account. Do not skip it.

---

## STEP 6 — Output

For each account produce TWO files:

**Brief** (`[ord_id]__[slug]__brief.md`): Full Format A document. Populate all sections using real data from Step 1. Remove template's bracketed operator instructions from client-facing sections. Keep internal routing block at top populated with real data including all 4 dimension scores. "What's Coming in 2026" section is required — use template text verbatim.

**Delivery email** (`[ord_id]__[slug]__delivery-email.md`): Follow `_delivery-email-template.md`. 4 sentences maximum. Subject: `[Company Name]: your SuperCat invoice is changing — effective [EFFECTIVE_DATE]`. Use the DEFAULT "unchanged" line unless `included_user_reduction` is primary or secondary driver — then use the alternate line. Keep internal routing block populated.

After saving, confirm:
- Files saved and paths
- Postgres query results per account (the actual numbers pulled)
- Any Postgres fallbacks (accounts where live query failed — specify reason)
- Any support_fire flags (not holds — operator decides timing)
- Any judgment calls on voice or format
