# SuperCat 2026 Pricing Migration — Fresh Agent Handoff
*Paste into a new Agent mode chat. Read fully before doing anything.*
*Last updated: 2026-05-20*

---

## Status Snapshot

SuperCat is migrating 109 accounts from legacy pricing to a standardized tier architecture. +$32,650/month modeled MRR. 60-day notice window is open — default effective date July 19, 2026.

| Layer | Status |
|---|---|
| Comm templates (Format A, B, CEO Letter, Good-News Notice) | ✅ All built, production-ready |
| CEO Letter accounts (9/9) | ✅ All drafted — see `ceo-letter-notices/` |
| Format A accounts (15/15) | ⚠️ All drafted — regeneration required. Template updated (S1–S7); existing briefs are pre-edit. See account holds below. |
| Format B accounts (19/19) | ✅ All drafted — see `format-b-notices/` |
| Good-News Notices (4/4) | ✅ All drafted — see `good-news-notices/` (dccl, jyc, pf, rw) |
| CEO Pre-Call accounts (9, delta ≥$600) | Not yet drafted |
| HOLD accounts (51) | Entity-gated, Watch-band, Annual, and VD-override accounts — see routing CSV for per-account status |
| Format C — Expansion/Upgrade Notice | Not built — not needed until wave 1 responses come in |

**shl (Savoy House):** CEO Letter drafted. ⚠️ Support fire (39 days open) — flagged in routing block and delivery email. Draft is production-ready; operator decides send timing. Billing entity = Progressive Lighting.

**mlc (Matteo Lighting):** CEO Letter drafted — value anchor section omitted (cost-per-order $154.62 qualifies under $200 threshold, but delta-per-order $54.63 fails the <$50 second-sentence gate). Add the first sentence only or accept — operator's call before send.

---

## Format A Account Holds

| Account | Flag | Reason | Action Required |
|---|---|---|---|
| ah (Alfresco Home) | ⛔ DO NOT RELEASE | Two "[NEEDS CSM DATA]" placeholders in client-facing sections (lede + value) | CSM must supply rep login volume, trailing order count, or GMV before send |
| ufi (Universal Furniture) | ⚠️ HOLD — support fire | Support issue open 7 days | Operator decides timing; support_fire flagged in routing block |
| wwjc (Wildwood/Chelsea House) | ⚠️ HOLD — support fire | Support issue open 27 days | Operator decides timing; support_fire flagged in routing block |
| mh (Magnussen Home) | ⚠️ CSM REVIEW | 63 active users on T1 (10-user included base); user overages exceed platform base cost | CSM should assess whether T2 migration conversation is warranted before sending T1 increase notice |
| kal (Kalco-Allegri Crystal) | ⚠️ REGENERATE | Calibration sample — predates S1–S7 template edits; lede uses forbidden utilization ratio; "How This Compares" midpoint calculation error | Regenerate under updated template before use as voice calibration |

---

## Your First Task

**Read the status table above. Then draft communications for any account with a clear format assignment and no active hold flag.**

**Entity rule — non-negotiable:** All entity-gated accounts stay in HOLD until all sibling brands are ready to move together. Never draft or send one account in an entity group without all others. Individual accounts within an entity cannot be drafted or sent independently.

---

## Data Corrections (routing CSV was wrong on these)

| Account | CSV Said | Correct Routing | Reason |
|---|---|---|---|
| rac (Godinger) | CEO Letter | CEO Pre-Call → Format B | delta +$734 ≥ $600 threshold |
| wac (WAC Group) | CEO Letter | CEO Pre-Call → Format B | delta +$744 ≥ $600 |
| sbl (WAC Group) | CEO Letter | CEO Pre-Call → Format B | delta +$672 ≥ $600 |
| big (Holladay Design) | (listed as ufi in CSV) | HOLD — VD Override | big = Baker-McGuire; VD=33.3; entity disambiguation with Samson Holding/ufi needed |
| kl (Coleto Brands) | Annual | Monthly | CSV error — only prog is Annual |

---

## File Paths

All paths relative to `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/`

**Data sources (SOURCE OF TRUTH HIERARCHY):**
1. `Pricing Migration/_master-account-data-v6.2.csv` — primary: `migration_driver`, `secondary_drivers`, health scores, `support_fire`, pricing breakdown
   *(Also at: `~/Downloads/_Pricing Refresh Master Data V2 - v6.2 Master Account.csv`)*
2. `~/Downloads/migration_revenue_model_2026-05-14 (2).html` — cross-check MRR/delta math only
3. `Pricing Migration/migration_comm_tiers_2026-05-19.csv` — comm_action routing (see data corrections above)

**If HTML model and v6.2 CSV disagree on driver → v6.2 CSV wins. Log conflict in routing block.**

**Templates:**
- Format A: `Pricing Migration/format-a-notices/_fresh-agent-prompt.md` (loads brief + delivery email templates)
- Format B: `Pricing Migration/format-b-notices/_fresh-agent-prompt.md`
- CEO Letter: `Pricing Migration/ceo-letter-notices/_fresh-agent-prompt.md`
- Good-News Notice: `Pricing Migration/good-news-notices/_brief-template.md`

**Voice calibration (read before drafting):**
- `format-a-notices/kal__kalco-allegri-crystal__brief.md` — ⚠️ NEEDS REGENERATION — predates S1–S7 template edits. Do not use as voice standard until regenerated.
- `format-b-notices/cci__currey-company__brief.md` — Format B
- `ceo-letter-notices/da__dainolite__brief.md` — CEO Letter

**Management files:**
- `Pricing Migration/_current-state.md` — artifact inventory
- `Pricing Migration/_roadmap.md` — priority queue

---

## Data Pipeline — Three Sources for Every Brief

**Source 1 — HTML model:**
```python
import re, json
with open('/Users/kylorjohnson/Downloads/migration_revenue_model_2026-05-14 (2).html', 'r') as f:
    html = f.read()
match = re.search(r'const A = (\[.*?\]);', html, re.DOTALL)
model = {a['oid']: a for a in json.loads(match.group(1))}
# cm=current_mrr, nm=new_mrr, dm=delta_mrr, dp=delta_pct, t=tier,
# iu=new_included_users, eu=new_excess_users, tb=new_tier_base
```

**Source 2 — v6.2 CSV:**
```python
import csv, io
with open('/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv', newline='', encoding='utf-8-sig') as f:
    content = f.read()
lines = content.split('\n')
master = {r['ord_id'].strip(): r for r in csv.DictReader(io.StringIO('\n'.join(lines[1:]))) if r.get('ord_id','').strip()}
# current_platform_mrr, current_user_mrr, current_user_rate, current_provided_users,
# trailing_avg_users, migration_driver, secondary_drivers, support_fire,
# support_fire_days_open, composite_narrative, value_delivery_score
```

**Source 3 — Postgres MCP (`user-supercat-postgres-vpn`):**
```sql
SELECT id AS org_id FROM organizations WHERE shortname = '{{ORD_ID}}';

SELECT
  (SELECT COUNT(*) FROM org_users WHERE organization_id = {{ORG_ID}} AND disabled = false) AS active_org_users,
  (SELECT COUNT(DISTINCT user_id) FROM login_events WHERE organization_id = {{ORG_ID}} AND created_at > NOW() - INTERVAL '90 days') AS logged_in_90d,
  (SELECT COUNT(*) FROM login_events WHERE organization_id = {{ORG_ID}} AND created_at > NOW() - INTERVAL '90 days') AS total_logins_90d;

SELECT COUNT(*) AS ltm_orders, ROUND(SUM(total)::numeric,2) AS ltm_gmv,
  COUNT(DISTINCT customer_num) AS ltm_customers_served
FROM orders WHERE organization_id = {{ORG_ID}} AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at > NOW() - INTERVAL '12 months' AND customer_num IS NOT NULL;
```

**Pipeline rules:**
- `support_fire = TRUE` → Draft anyway. ⚠️ flag in routing block + delivery email. CEO decides timing. Never reference support issue in client copy.
- Postgres fails → fall back to `composite_narrative` from v6.2 CSV for lede only. Note fallback.
- Lede stats: Lead with unambiguous platform metrics — users active, session volume, surfaces in use, tenure. Order counts (`ltm_orders`, `ltm_customers_served`) are supporting evidence, not headline proof. If used, scope to "submitted through SuperCat" — never the account's total order volume. Do not calculate per-order subscription costs in the lede. Never frame stats as provisioned-vs.-active ratio ("X of Y users logged in").

---

## Non-Negotiables — Every Draft Must Pass All 9

1. Never lead with a percentage. Lead with the dollar amount and effective date.
2. Never use "we're adjusting your pricing."
3. Never apologize for the change.
4. Confirm early that operations are unchanged. Use verbatim: **"Your workflow, your team's access, your catalog, and your integrations are unchanged. The only thing changing is the invoice."** EXCEPTION: if `included_user_reduction` is primary or secondary driver, use instead: **"Your workflow, your catalog, and your integrations are unchanged. The invoice and the included user count are both changing — the breakdown above explains exactly how."**
5. Never include health scores, health bands, or dimension scores in client-facing copy.
6. Never include expansion language in migration notices. Format C is a separate document, sent only after confirmed positive migration signal.
7. "Every account we work with is moving to the same structure" — do not hedge this.
8. Lede stats: unambiguous platform metrics first. No provisioned-vs.-active user ratios. No per-order subscription cost calculations in the lede.
9. Every Format A brief includes the "What's Coming in 2026" section — verbatim from the template. Required in every output. Do not skip.

---

## Language Register

These clients are lighting and furniture manufacturers. Write for a business owner or CFO — not a software procurement team.

**Forbidden:**
- "trailing 12-month average" → "your team averages around X users"
- "install base" → "all accounts we work with"
- "full-stack commercial operating system" / "five connected surfaces" → describe what it actually is
- Percentile notation (p25, p75) → never in client copy
- T1/T2/T3 in running prose → tables only; describe what they have in words
- Competitor pricing comparisons → cut
- "rate card" → "our current standard pricing"
- "as part of this refresh" → "going forward" (not "with this refresh")
- "There are no account-specific adjustments in how [ACCOUNT_NAME]'s number was calculated." → **delete. Never write this sentence.**
- "SuperCat is standardizing its pricing... first time we've applied a consistent commercial structure..." → replace with: "In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you."
- "Your rate at signing predates the current rate card and we're bringing it in line with the standard structure." → replace with tenure-aware variant: (≤5 years) "Your rate was set in [YEAR] — this is the first time we've updated it." / (10+ years) "Your rate has been unchanged since [YEAR] — this is the first time we've adjusted it."

**"How This Compares":** Two sentences. Dollar + position (at base rate / below midpoint / above midpoint). When "above the midpoint" — REQUIRED: clause tying the position to user count, not tier premium: "…is above the midpoint of what [TIER] accounts pay after migration, driven by your team size at [N] users — the platform base itself is at the [TIER] standard." Never state "above the midpoint" without this clause.

---

## Driver Framing

Always use `migration_driver` from v6.2 CSV. If v6.2 CSV and HTML model disagree, v6.2 wins.

| Driver | What it means | Key framing |
|---|---|---|
| `user_rate_normalization` | Rate locked at signing, moving to graduated standard | Show old rate → new table → math. If platform base also changes, explain it. |
| `platform_discount_correction` | Discount at signing being retired | "reflects a discount applied at signing that's being retired" |
| `tier_base_increase` | Platform base moved from old book rate to current standard | Tier unchanged, only the rate. |
| `included_user_reduction` | Legacy expanded allotment normalizing to tier standard | Show included-base change + new excess calc. Add billing-basis sentence after table. Use alternate close. |
| `multi_org_retirement` | Multi-org program retired | Each entity to individual standard pricing. |
| `annual_discount_retirement` | Annual commitment discount retired | Standard monthly rate; annual prepay still available. |
| `at_book_tier_shift` | Already at book, minor adjustment | Near-zero delta. When base increases: include "The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today." Do not leave a base increase unexplained. |
| `module_compression` | Price decrease | Good-News Notice format. |
| `special_arrangement` | Custom arrangement to standard | Be direct. Delta >30% → CEO involvement. |

`secondary_drivers`: add as supporting context within the primary driver block — never a separate section.

---

## Format Routing Rules

| Condition | Format |
|---|---|
| delta_mrr decrease | Good-News Notice |
| delta_pct ≤10% OR delta_mrr ≤$80 | Format A — 60-Day Notice |
| delta_mrr $81–$399 | Format B — Notice + Meeting |
| delta_mrr $400–$599 | CEO Letter + Call Commitment |
| delta_mrr ≥$600 | CEO Pre-Call → Format B (not yet drafted) |

Health modifier: Watch → no effusive framing; do not send without health check-in confirmation. At Risk → do not draft migration notice.
Annual modifier: 90-day notice window applies. Confirm renewal date before sequencing.

---

## Key Reference Tables

**User rate normalization (graduated):**

| Excess users above included base | Rate |
|---|---|
| 1–10 | $25/user |
| 11–25 | $22/user |
| 26–50 | $20/user |
| 51+ | $18/user |

**Peer range (internal only — never cite in client copy):**
| Tier | Floor | ~Midpoint | Ceiling |
|---|---|---|---|
| T1 | $774 | ~$1,200 | $1,629 |
| T2 | $1,295 | ~$1,440 | $1,589 |
| T3 | $2,295 | ~$2,585 | $2,875 |

---

## Quality Bar — Every Draft Before Send

- Math balances: Before total = `current_mrr`, After total = `new_mrr` exactly
- Zero forbidden language (see Language Register above)
- No health scores or expansion language in client-facing sections
- No duplicate sentences
- Correct driver block per v6.2 CSV `migration_driver`
- `included_user_reduction` accounts → alternate closing line; included user reduction rule applied (explicit change acknowledgment + threshold check: headroom sentence ONLY if `trailing_avg_users < new_included_users` AND within 3 of base; if already in excess, overage is in the table — no "room" framing)
- Tone check: sentence one names the relationship before the price change for accounts with 3+ years tenure; lede proves you looked at this specific account
- Platform base increase (any driver) → base repricing justification sentence present: "The platform has grown considerably since [YEAR]…"
- Delta >30% → lede names the annual dollar impact ($[delta × 12]/year)
- "Above the midpoint" → user-count clause in "How This Compares"
- `support_fire = TRUE` → ⚠️ flag in routing block, NOT skipped
- Value anchor: include if `ltm_orders > 0` and `cost_per_order < $200`. Add second sentence ("annual rate increase = $[X]/order") only if `delta_per_order < $50`
- "What's Coming in 2026" section present and verbatim
