# Migration Wave Routing Notes
*Last updated: 2026-05-14 (v2) | Source: migration_table_v6 × health_scores_2026-05-13*

---

## Brief Type Architecture (Corrected)

The migration is primarily a **price normalization event**, not a tier upgrade event. This distinction drives two separate brief types per account.

### Migration Brief (required for all migrating accounts)
Covers what's changing in pricing and why. Uses account's current tier and migration driver to frame the conversation.

| Brief Type | When | Driver |
|---|---|---|
| `value_justification` | Account staying in current tier; price correcting | user_rate_normalization, discount_correction, multi_org_retirement, module_compression, at_book_tier_shift |
| `none` | Account already migrated | already_migrated |

**107 of 109 accounts get a `value_justification` brief.** 2 are already migrated (no brief needed).

The framing in every `value_justification` brief:
- State the price change in the opening sentence. Do not bury it.
- Lead with the correction mechanic (the specific reason the number is changing)
- Show the value evidence (GMV, orders, users, products) as the case for why the new number is worth it — not as a softener before the price
- Anchor the new price to peer range: T1 p25–p75 = $774–$1,629/mo; T2 = $1,295–$1,589/mo; T3 = $2,295–$2,875/mo

### Expansion Brief (optional, layered on top of migration)
Covers the next capability unlock — what's available if the account wants to grow. Completely separate from the migration brief. Do not conflate these conversations.

| Brief Type | Applies To | Feature Unlock |
|---|---|---|
| `t1_to_t2` | T1 accounts | B2B Cart + Order & Invoice Tracking ($749 → $1,295) |
| `t2_to_t3` | T2 accounts | Sales Intelligence + 40 included users ($1,295 → $2,295) |
| `none` | T3 accounts | No tier above — brand expansion and services upsell only |
| `hold` | At Risk / Critical accounts | Do not present expansion until health improves |

**Distribution:**
- `t1_to_t2` expansion candidates: 55 accounts
- `t2_to_t3` expansion candidates: 17 accounts
- `hold` (health issue, expansion deferred): 1 account (`krb`)
- `none` (T3, already at top tier): 36 accounts

---

## Expansion Brief Sequencing — Signal-Based, Not Time-Based

**The expansion brief is NOT sent on a fixed timer after the migration brief.**

The sequence:
1. Migration brief (`value_justification`) is delivered by CS
2. CSM logs a **positive response signal** — explicit acknowledgment, verbal acceptance, or no pushback after 14 days of confirmed delivery
3. Only then is the expansion brief queued

**Silence does not clear the gate.** If the account receives the migration brief and goes quiet, the CS team needs to make contact and confirm reception before the expansion brief is sent. A customer who hasn't processed the price change is not ready to hear about spending more.

**Positive signal examples that clear the gate:**
- Customer explicitly acknowledges the migration and accepts the new price
- Customer asks questions about the new tier features (engagement signal)
- Customer confirms the new invoice during a call or email exchange

**Hold conditions — expansion brief is blocked regardless of timeline:**
- Customer has expressed any objection to the migration brief price
- Account is in Watch health band AND delta_pct > 20%
- Account is in At Risk or Critical health band (any delta)
- CSM has an open support issue with the account

The last hold condition is new: **Watch band + significant delta (>20%) = hold on expansion.** A Watch-band account getting a >20% price increase is a churn-risk conversation, not a growth conversation. The CS priority is retaining the account at the new price before layering in an upgrade ask.

---

## Wave Assignment Logic

| Wave | Criteria | Count |
|---|---|---|
| Wave 0 | Already migrated (no action) | 2 |
| Wave 1 | Thriving/Healthy health band + modest price delta (≤20%) | 39 |
| Wave 2 | Thriving/Healthy with high delta (>20%) OR Watch band OR Unscored | 67 |
| Wave 3 | At Risk, Critical, or Unscored with >30% delta | 1 |

**Start with Wave 1 to build execution muscle** — 39 accounts with strong health and manageable price changes. Low-risk migration conversations, high-probability expansion candidates. Run these first to stress-test the brief templates and CSM motion before hitting the harder accounts.

**Wave 2 is the main event.** 67 accounts. 42 of them face >30% price increases. This is 39% of the install base — not an exception category, not a tail. The migration's commercial and retention outcome is determined here. Every Wave 2 account needs a CS-reviewed brief (not raw template output) and a warm handoff plan before outreach goes out.

---

## Wave 1 Priority Order

Accounts sorted by delta ascending within Wave 1 (lowest delta first = easiest conversations):

Decreases first (pure win, send value_justification immediately):
- `clm` Crystorama — Thriving, -31.6% (price drop)
- `pf` Palecek — Thriving, -28.0% (price drop; also T1→T2 expansion candidate)
- `gc` Groupe Courchesne — Healthy, -8.5%
- `mah` Moda at Home — Healthy, -6.6%
- `ml` Millennium Lighting — Healthy, -4.2%
- `jyc` Jamie Young — Thriving, -2.3%
- `rw` RENWIL — Healthy, -1.8%

Near-flat (easiest true migration conversations):
- `bcf` Braxton Culler — Thriving, +0.6%
- `kii` Kennedy International — Healthy, +0.6%
- `mpc` Pioneer Morton — Healthy, +1.7%
- `sbmh` Somerset Bay — Thriving, +2.2%
- `bp` Buster & Punch — Healthy, +2.5%
- `lpf` Linon/Powell — Thriving, +2.8%

Pilot expansion candidates (migration + expansion brief in sequence):
- `pf` Palecek — T1 Thriving, delta -28.0% → **T1→T2 pilot** (gets a price decrease AND expansion opportunity)
- `gc` Groupe Courchesne — T2 Healthy, delta -8.5% → **T2→T3 pilot** (same)
- `wwjc` Wildwood/Chelsea House — T3 Thriving, delta +8.0% → value_justification only (already at T3)

---

## Flagged Accounts Requiring Human Review

### High Risk Delta (>30% price increase) — 42 accounts
These accounts are in Wave 2 or 3. Each requires a CS-reviewed brief before outreach. Do not use template without reviewing the specific discount drivers and account history.

Notable high-risk accounts:
- `sccon` Summer Classics Contract — Thriving health (93.3 score), +2,450% delta (multi-org rollup child; legacy pricing extreme)
- `kl` Kaleen Rugs — At Risk health + high delta (double flag: health AND price risk)
- `wac` WAC Lighting — high delta; likely large absolute dollar change
- `vce` Visual Comfort entities — multiple high-delta accounts in multi-org structure

### Low Health Flag — 1 account
- `krb` — At Risk band; expansion brief is `hold`; migration brief still needed but tone requires care

### Key Account Notes

**Summer Classics rollup entities (sc, sccon, scs):**
Multi-org discount program is being retired. These entities have been on a multi-org pricing structure that included cross-entity discounts. Each entity gets a separate `value_justification` brief. Do not send a single combined brief.

**WAC Lighting / Modern Forms (`wac`, `mf`):**
Large catalog (300k+ products), sophisticated operator. High delta. Brief should emphasize platform value at scale before leading with price.

**Palecek (`pf`):**
Getting a price *decrease* (module compression) but is a prime T1→T2 expansion candidate. Sequence: send `value_justification` first (good news — you're saving money), then follow with `t1_to_t2` expansion brief 2–4 weeks later when relationship is warm.

**Groupe Courchesne (`gc`) + Moda at Home (`mah`):**
Both getting price decreases AND are T2→T3 candidates. Same sequencing as Palecek.

---

## What's NOT in This Routing Table

- **New business prospects**: Routing is install-base only
- **Churned accounts**: Not included
- **Entities with no `ord_id` in migration table**: Check with Finance if missing

---

## Source Files
- Migration data: `2026-05-13__migration_table__v6.csv`
- Health data: `Health V3/runs/2026-05-13/client_health_scores_2026-05-13.csv`
- Pricing authority: `PRICING_CONSTITUTION (1).md` (D-004a, D-004b, D-003b, D-003e)
