# Rung-4 Option A — Coaching Juxtaposition Operator (internal-only, Tier-2)

> **What this is.** The **runnable** Rung-4 operator: an **internal sales-management coaching digest** that, for a
> single Tier-2 org, **ranks reps by the dollars their own book is bleeding** (C2 leakage + S1 revenue-at-risk)
> and shows their Mixpanel **feature-depth / presentation-cadence beside that dollar as context**. It is the
> *application* of the sanctioned scope in [`rung4_fusion_decision_brief.md`](../handoffs/rung4_fusion_decision_brief.md)
> (Option A, owner GO 2026-06-29, re-confirmed to start 2026-06-29).
>
> **It produces NO fused single number.** There is no "coached-dollar," no composite score, no leaderboard rank
> that blends behavior and outcome. The two axes sit **side by side**; a human sales manager connects them. This
> is a **coaching hypothesis ranked by dollars — not attribution, not a scoreboard.** (Option B, the fused
> metric, and Option C, client-facing, remain **deferred** — do not build them here.)
>
> **Consume, do not re-author.** Every number comes from a locked, already-validated source: C2/S1 from
> [`selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md), C4/C6 (Q-01, Q-63/64/65) from
> [`query_library_v2.md`](../foundation/query_library_v2.md), the identity tier + `COMMERCE_CONFIDENCE` cap from
> [`rep_copilot_operator.md`](rep_copilot_operator.md) (RP-1/RP-2) and `provenance_spine.md`. This operator is
> **assembly only** — it adds no new economics mechanism.
>
> **Trigger.** "run the rung-4 coaching digest for {org}", "coaching juxtaposition / rep fusion for {org}",
> "behavior × outcome for {org}".
>
> **Inputs.** `{org_shortname}` (required, **must be Tier 2**). The operator resolves `{ORG_ID}` /
> `{ORG_SHORTNAME}` / `{REPORT_THROUGH_DATE}` itself via the RP preflight.
>
> **MCP.** `user-supercat-postgres-vpn` (`execute_sql`, read-only) for the outcome axis; `user-bigquery-admin`
> (`query`, read-only) for the behavior axis. **Read-only throughout.** Live figures `[from-live]`.
>
> **Status: APPLIED OPERATOR — Option A only.** Internal-only, Tier-2-only, capped at `COMMERCE_CONFIDENCE`,
> coaching-grade. **Dry-run-validated across all 8 Tier-2 orgs 2026-06-29** (§7); C2 execution **resolved** via
> `MATERIALIZED` CTEs (runs in-window to 300K / clc); bridge **deduped** (`DISTINCT ON`); house-rep screening added.

---

## 0. Order of operations (do not reorder)

```
GATE 0  Tier-2 admission  ──► if REP_IDENTITY_TIER < 2: REFUSE (this product does not exist below Tier 2)
        │
        ▼
RP-1/RP-2 preflight (consumed from rep_copilot_operator §1)
        │   emits COMMERCE_CONFIDENCE, report_through_date, REP_IDENTITY_TIER, house_suspect set, mhc dormancy
        ▼
AXIS O  Outcome (ERP, $) ──► O1 = C2 leakage-by-rep   +   O2 = S1 $-at-risk-by-rep   (named via the bridge)
        │   each capped at COMMERCE_CONFIDENCE: NONE→suppress, PARTIAL→labeled floor, STRONG→show
        ▼
AXIS B  Behavior (Mixpanel, context) ──► B1 = C4 feature depth  +  B2 = C6 cadence/conversion  (by username)
        │   never carries a dollar; STRONG behavior confidence; degrade on LOGINS-ONLY (mhc), never infer absence
        ▼
JOIN    Soft username↔rep_name match (LABELED match-confidence; NEVER drop either side)
        │
        ▼
ASSEMBLE  Rank by AXIS O dollars; print AXIS B beside each row as context; NO fused number; coaching framing
```

**One line:** *rank the reps by the money their book is losing, set their app behavior next to it, and hand a
manager a 1:1 agenda — without ever multiplying the two together.*

---

## 1. GATE 0 — Tier-2 admission (the hard door)

This product **only exists for the 8 Tier-2 orgs** (name bridge ≥80%, per `rep_copilot_operator.md` §1):

| Tier-2 org | bridge % | Note |
|---|---|---|
| sarreid | 100 | |
| clc | 100 | |
| **mhc** | 100 | ⚠ **DORMANT** — pin `report_through_date` to last real invoice; banner every row; **never push $-at-risk as live** |
| cci | 100 | |
| wwjc | 98.8 | |
| pf | 89.7 | |
| ril | 87.7 | |
| **bcf** | 81.8 | boundary org; reps are **agencies** (see §3 soft-join lesson) |

**If `{org}` is Tier 1 or Tier 0 → REFUSE and stop.** Do not "degrade" into a `rep_number`-grain fusion. The
behavior axis is named (`username`) but the outcome axis is `rep_number`-only at Tier 1 / absent at Tier 0, so any
join would either fabricate a name or mis-hang a dollar (decision brief §2, §4.3). Tier 1/0 orgs get the rep
copilot's existing unfused side-by-side (named behavior scorecard + anonymous outcome) — **not** this operator.

Run the **RP-2 tier preflight from `rep_copilot_operator.md` §1** (one org per call, the `LEFT JOIN` form) to
confirm tier ≥ 2 live before proceeding. Carry **bcf = Tier 2** and **mhc = Tier 2-DORMANT** as hard-coded flags.

---

## 2. The two axes (consumed verbatim — capped/gated at the source)

### AXIS O — Outcome (the dollars; ERP; capped at `COMMERCE_CONFIDENCE`)

Both are the exception-layer queries rolled to the rep and **named via the portal_orders bridge** (Tier-2 only).
NONE → suppress the dollar; PARTIAL → present as a **labeled floor** ("≥ $X, partial feed"), never CRITICAL;
STRONG → show. House/sample bill-tos excluded (`ZZ*`/`HOUSE*`/`ACCOM*`/`SAMPLE*`/…) pending per-org confirmation.

**O1 — C2 leakage-by-rep** (tier-aware `Q-ECON-LEAK`; true-median + tier guard + volume guard). Report **both**
leaked-$ **and** leak-rate. Framing **locked to "discount-discipline / coaching," NEVER "rogue."** Mandatory human
gut-check before anything is acted on (the asi rep-69 "$1.35M / 42%" false-positive lesson — it was a normal 2.1%
once tiers/volume were excluded).

> **Execution fix — RESOLVED 2026-06-29 (the canonical runtime form).** The plain C2 query times out at the 30s
> restricted-MCP limit on **every** real book (ril 17K, bcf 25K, cci 171K, clc 300K all timed out) — *not* a size
> issue, a **pathological plan**: Postgres inlines the `custagg` CTE and re-executes the line-item scan ~4×. The
> fix is the **`MATERIALIZED` keyword** on `inv` / `custagg` / `itemagg` so the scan runs once. With it, C2 returns
> in-window on **all** Tier-2 books incl. clc (300K). **Do NOT use `PERCENTILE_CONT … WITHIN GROUP`** — the MCP
> validator hard-rejects ordered-set aggregates (even a one-liner); keep the two-middle-rows `ROW_NUMBER` median.

```sql
-- O1: C2 tier-aware leakage rolled to rep. MATERIALIZED CTEs (perf) + DISTINCT ON bridge (dedup). Read-only.
-- HOUSE SCREEN — TWO LAYERS (see config/house_rep_exclusions.md):
--   (1) customer-side bill-to patterns (inlined below).
--   (2) rep-label screen: AUTO-RULE (rep_label ILIKE 'house%' or '% house account%') + per-org EXCLUDE list
--       templated in by the operator at run time. The HAVING clause at the end drops rep-label-excluded rows
--       from the digest so a house bucket never leads a coaching card.
WITH rtd AS (SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS d FROM portal_invoices WHERE organization_id = {{ORG_ID}}),
inv AS MATERIALIZED (                                   -- MATERIALIZED: stop the 4× re-scan that causes the 30s timeout
  SELECT invoice_number, customer_bill_to_number AS cust, rep_number
  FROM portal_invoices, rtd
  WHERE organization_id = {{ORG_ID}} AND net_amount>0
    AND invoice_date BETWEEN (SELECT d FROM rtd)-INTERVAL '12 months' AND (SELECT d FROM rtd)
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'ZZ%'    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'HOUSE%'
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'SAMPLE%' AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'ACCOM%'
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'DISPLAY%' AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'SHOWROOM%'
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'TEST%'),
custagg AS MATERIALIZED (
  SELECT pii.item_number AS item, inv.cust, MAX(inv.rep_number) AS rep, SUM(pii.quantity_invoiced) AS qty,
         SUM(pii.quantity_invoiced*pii.unit_price)/NULLIF(SUM(pii.quantity_invoiced),0) AS realized
  FROM portal_invoice_items pii JOIN inv ON inv.invoice_number=pii.invoice_number
  WHERE pii.organization_id = {{ORG_ID}} AND pii.quantity_invoiced>0 AND pii.unit_price>0
  GROUP BY pii.item_number, inv.cust),
itemagg AS MATERIALIZED (SELECT item, SUM(qty) tot_units, COUNT(*) cnt FROM custagg GROUP BY item HAVING COUNT(*)>=5),
ranked AS (SELECT c.item,c.realized, ROW_NUMBER() OVER (PARTITION BY c.item ORDER BY c.realized) rn, i.cnt
           FROM custagg c JOIN itemagg i ON i.item=c.item),
ref AS (SELECT item, AVG(realized) ref_price FROM ranked WHERE rn IN (FLOOR((cnt+1)/2.0), CEIL((cnt+1)/2.0)) GROUP BY item),  -- true median
tier AS (SELECT item, ROUND(realized,2) px FROM custagg GROUP BY item, ROUND(realized,2) HAVING COUNT(*)>=5),                 -- tier guard
scored AS (SELECT c.rep, c.qty, c.realized, r.ref_price, (t.px IS NOT NULL) AS at_tier, (c.qty >= 0.10*i.tot_units) AS strategic  -- volume guard
           FROM custagg c JOIN itemagg i ON i.item=c.item JOIN ref r ON r.item=c.item
           LEFT JOIN tier t ON t.item=c.item AND t.px=ROUND(c.realized,2)),
rep_names AS (SELECT DISTINCT ON (rep_number) rep_number, rep_name FROM portal_orders                       -- DISTINCT ON: one name per rep_number (dedup)
              WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name<>'' ORDER BY rep_number, rep_name),
agg AS (
  SELECT COALESCE(rn.rep_name, 'rep '||COALESCE(NULLIF(TRIM(s.rep),''),'(unattributed)')) AS rep_label,
         SUM(qty*(ref_price-realized)) FILTER (WHERE realized<ref_price*0.9 AND NOT at_tier AND NOT strategic) AS leaked_raw,
         SUM(qty*realized) AS scope_rev
  FROM scored s LEFT JOIN rep_names rn ON rn.rep_number = s.rep
  GROUP BY 1
)
SELECT rep_label,
       ROUND(leaked_raw::numeric, 0) AS leaked_dollars,
       ROUND(100.0*leaked_raw/NULLIF(scope_rev,0), 1) AS leak_rate_pct
FROM agg
WHERE leaked_raw > 0
  -- REP-LABEL house screen (auto-rule; per-org EXCLUDE rows templated in by the operator from config/house_rep_exclusions.md)
  AND COALESCE(rep_label,'') NOT ILIKE 'house%'
  AND COALESCE(rep_label,'') NOT ILIKE '% house account%'
  -- AND rep_label NOT IN (<per-org EXCLUDE list for {{ORG_ID}}>)   -- e.g. for clc: NOT IN ('Capital Lighting Fixture')
ORDER BY leaked_dollars DESC LIMIT 12;
```

C2 is also canonically validated on **asi (rep 12 = $163K / 5.9%)** in the exception layer. **Screen the rep_name
side for house entities** (see §3, gotcha G-B): a rep literally named `HOUSE ACCOUNT` (cci) / `12 House Account`
(wwjc) passes the customer-side filter — exclude it in the per-org confirm.

**O2 — S1 $-at-risk-by-rep** (per-account decay, **equal 6-month windows** anchored on `report_through_date`,
rolled up by the account's owning `rep_number`). Dollar = LTM revenue on accounts that are decaying or early-dormant.

```sql
-- O2: S1 revenue-at-risk rolled to the owning rep, named via the Tier-2 bridge. Read-only.
-- Equal-window decay (last 6mo < 0.6 × prior 6mo) OR early dormancy (silent > 2× normal gap). House excluded.
-- HOUSE SCREEN — TWO LAYERS (see config/house_rep_exclusions.md):
--   (1) customer-side bill-to patterns (inlined below).
--   (2) rep-label screen: AUTO-RULE + per-org EXCLUDE list — applied in the final SELECT.
--       Closes the kal 'House Account' rep 0999 $695K-at-risk defect (PASS1 2026-06-30).
WITH rtd AS (SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS d FROM portal_invoices WHERE organization_id = {{ORG_ID}}),
c AS (
  SELECT customer_bill_to_number AS cust, MAX(rep_number) AS rep, COUNT(*) AS n_inv,
         MIN(invoice_date) first_d, MAX(invoice_date) last_d,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= (SELECT d FROM rtd)-INTERVAL '12 months') AS ltm_rev,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= (SELECT d FROM rtd)-INTERVAL '6 months')  AS r_recent,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= (SELECT d FROM rtd)-INTERVAL '12 months'
                                                    AND invoice_date <  (SELECT d FROM rtd)-INTERVAL '6 months')  AS r_prior
  FROM portal_invoices, rtd
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN (SELECT d FROM rtd)-INTERVAL '24 months' AND (SELECT d FROM rtd)
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'ZZ%'    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'HOUSE%'
    AND COALESCE(customer_bill_to_name,'')   NOT ILIKE 'HOUSE ACCOUNT%'
    AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'SAMPLE%' AND COALESCE(customer_bill_to_number,'') NOT ILIKE 'ACCOM%'
  GROUP BY customer_bill_to_number
  HAVING COUNT(*) >= 6
     AND SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= (SELECT d FROM rtd)-INTERVAL '12 months') > 20000
),
atrisk AS (
  SELECT cust, rep, ltm_rev FROM c
  WHERE (r_prior>0 AND r_recent < 0.6*r_prior)
     OR ((SELECT d FROM rtd)-last_d) > 2*((last_d-first_d)::numeric/NULLIF(n_inv-1,0))
),
rep_names AS (SELECT DISTINCT ON (rep_number) rep_number, rep_name FROM portal_orders   -- DISTINCT ON: one name per rep_number (dedup; see §3 G-A)
              WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> '' ORDER BY rep_number, rep_name),
labeled AS (
  SELECT COALESCE(rn.rep_name, 'rep '||a.rep) AS rep_label, (rn.rep_name IS NOT NULL) AS named, a.ltm_rev
  FROM atrisk a LEFT JOIN rep_names rn ON rn.rep_number = a.rep
)
SELECT rep_label, named,
       COUNT(*) AS at_risk_accounts, ROUND(SUM(ltm_rev)::numeric,0) AS dollars_at_risk
FROM labeled
WHERE COALESCE(rep_label,'') NOT ILIKE 'house%'                  -- AUTO-RULE: catches cci HOUSE ACCOUNT, kal House Account
  AND COALESCE(rep_label,'') NOT ILIKE '% house account%'        -- AUTO-RULE: catches wwjc "12 House Account" forms
  -- AND rep_label NOT IN (<per-org EXCLUDE list for {{ORG_ID}}>)   -- e.g. for ril: NOT IN ('Ratana','Thomas York*DoNoUse')
GROUP BY rep_label, named ORDER BY dollars_at_risk DESC LIMIT 12;
```

Unmapped `rep_number`s render as `rep <n>` and are **NEVER dropped** (the §7.1 red line — silently dropping them
fabricates the ranking).

### AXIS B — Behavior (the context; Mixpanel; NEVER a dollar)

Consumed from the patched library, keyed on `username`. **Standalone behavior stays demoted** — it is *context
beside a dollar*, never itself a lead (no dollar = not a lead, per the north-star).

- **B1 — C4 feature depth** (Q-01, `mixpanel.user_feature_usage_report`): per-rep breadth across the 6 dimensions
  (customer targeting, product discovery, config/bundling, presentation, information, engagement) + `days_active`,
  `submit_order`. Use to spot the deficit to coach (e.g. low presentation/share, low discovery).
- **B2 — C6 cadence/conversion** (Q-63/64/65, `mixpanel.events` keyed `username`+`selected_bill_to_code`):
  presentations→order conversion, touches/account, selling-vs-admin. **`selected_bill_to_code` is only 18–76% of
  events** → report on the **covered subset** and degrade; **never infer "rep never presented" from absence.**
- **Coverage gate:** runs at `CORROBORATED` Mixpanel coverage; **mhc degrades to LOGINS-ONLY** (no feature depth —
  show login/order effort only, never fabricate engagement).

---

## 3. The JOIN — soft `username ↔ rep_name`, labeled, never fused

The behavior axis is keyed on **`username`** (a display handle); the outcome axis is named via **`rep_name`**
(the `portal_orders` bridge). **These do not share a key** — the match is a soft, human-readable association, and
**this is precisely why Option A produces no fused number** (decision brief §4.3: soft-join misattribution is the
core risk). Rules:

1. **Present both ranked lists; attach a `match` column** with confidence: `exact` (handle ↔ name unambiguous),
   `likely` (surname/first-initial match), `unmatched` (no confident counterpart).
2. **Never drop a rep from either side** for failing to match. An outcome rep with no behavior match shows
   "behavior: —"; a behavior rep with no outcome shows "$: —". Dropping fabricates a clean story.
3. **Never multiply or sum across the axes.** No "coached-dollar," no behavior-weighted dollar, no blended rank.
4. **The human owns causation.** Print the juxtaposition; the manager decides whether low cadence *explains* the
   at-risk dollars. The operator must not assert that it does (decision-brief §4.4 causal-overclaim guard).

**Two bridge gotchas the cohort dry-run surfaced (2026-06-29) — handle these before any digest ships:**

- **G-A — one `rep_number` → many `rep_name` spellings inflates the digest.** The raw bridge is many-to-one:
  clc carries `KTR Associates LLC` **and** `KTR Associates` (same rep, identical $1.85M), `Philip Winston, Inc.`
  vs `Philip Winston Inc`, etc. A plain `DISTINCT` join fans out and prints **phantom duplicate reps**. **Fix
  (baked into the O1/O2 queries):** `SELECT DISTINCT ON (rep_number) … ORDER BY rep_number, rep_name` — collapse
  to one deterministic name per `rep_number`. *(Note: distinct rep_numbers with a typo'd name — sarreid
  `Deborah Klein` vs `Deborah Klien` — are correctly kept separate; flag as a soft "possibly same human" note,
  do not auto-merge.)*
- **G-B — house entities ride in on the rep_name side.** The customer-side house filter doesn't catch a *rep*
  literally named `HOUSE ACCOUNT` (cci, top C2 row), `12 House Account` (wwjc, #1 at-risk $1.6M), or a
  brand/distributor that books as a rep (`Ratana` on ril is the #1 at-risk **and** #1 leaker; `Capital Lighting
  Fixture` tops clc). **The rep-label screen is now baked into both O1 and O2 SQL (2026-06-30):** the
  `house%` / `% house account%` AUTO-RULE fires on every org (closes cci/kal PASS1 defects), and the
  per-org `EXCLUDE` rows from [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md) are
  templated into the final `WHERE` clause at run time for non-`house*`-named house entities (clc / ril / pf /
  mhc / bcf). A digest run that omits either layer is non-compliant; `report_operator.md` Step 10 enforces
  this in the `HOUSE-LEAK` render check.

> **Live lesson — bcf (2026-06-29).** bcf's outcome reps are **agency names** (`Todd Teague (Twinco Inc.)`,
> `SVB Enterprises Inc/Steve Bill`, `Jerry Montini (Beachside Furn)`, `Home Decor/Jack Johnson`) while behavior
> handles are **individuals** (`tteague`/`ateague`, `sbillingsley`, `jmontini`, `jackj`). Even the "obvious"
> matches are ambiguous (two Teague handles → one Teague agency). This is the soft-join risk made concrete and the
> reason a fused number would be **wrong here** — Option A shows them adjacent with a `match` label and lets the
> bcf manager bridge them. **A validated `username↔rep_name` resolver is the precondition for Option B** — until
> it exists, the fusion stays unfused.

---

## 4. The deliverable (internal coaching digest — the shape)

Per Tier-2 org, one page. **Header** carries `COMMERCE_CONFIDENCE`, `report_through_date`, and the standing frame:
*"Coaching hypothesis ranked by dollars at risk — not attribution, not a rep scoreboard. Behavior shown as context
only. Internal sales-management use."* Then the **ranked juxtaposition**, sorted by AXIS-O dollars, ~12 rows:

| Rank | Rep (outcome name) | $ at risk (S1) | Leak $ / rate (C2) | Behavior match | Feature depth (C4) | Cadence / conversion (C6) | Coaching read (human) |
|---|---|---|---|---|---|---|---|

- **Sort key = AXIS-O dollars only** (S1 $-at-risk primary; C2 leakage secondary). Behavior never moves a rank.
- Each dollar carries its confidence label; **PARTIAL → floor**, NONE → suppressed cell.
- **Coaching read** is a human-written hypothesis (e.g. *"$133K at risk across 4 accounts; cadence shows 19
  accounts engaged but presentation depth low — book a coverage review"*), explicitly a hypothesis.
- mhc rows carry the **dormancy banner** and no live $-at-risk.

**Cap at ~12 rows** (beyond that it reads as "everything's on fire"). No charts; this is a push, not a dashboard.

---

## 5. Hard guardrails (carried from the stack; non-negotiable)

1. **No fused number, ever** (Option A's defining constraint). No coached-dollar, no composite, no blended rank.
2. **Tier-2 only.** Refuse below Tier 2; never name a rep the bridge can't reach; never drop an unmapped `rep_number`.
3. **Cap at `COMMERCE_CONFIDENCE`** (never FULL; realistically STRONG/PARTIAL). Lowest input wins (`LEAST`).
   NONE → suppress the dollar.
4. **Internal-only.** Sales-management audience. **Not client-facing** (that's Option C, deferred). C2 framing
   locked to "discount-discipline / coaching," never "rogue"; mandatory human gut-check before acting on leakage.
5. **House accounts** auto-flagged + excluded pending per-org confirmation (per-report step) — **screen both the
   bill-to side AND the rep_name side** (a rep literally named `HOUSE ACCOUNT` / `12 House Account` / a house brand
   like `Ratana` rides in on the bridge; see §3 G-B).
6. **Behavior is context, never a lead.** No standalone behavior score as a finding; never infer absence
   (`selected_bill_to_code` null ≠ "never presented"); degrade on LOGINS-ONLY.
7. **Revenue ≠ margin ≠ cash.** Invoiced-revenue-shaped only; never imply margin or collection. Suppress the hard
   gaps (true/gross margin, AR/DSO, damage-by-carrier, inventory aging, quoted lead time, market/showroom ROI).
8. **Correlation, not cause.** The juxtaposition is a hypothesis; the human asserts any causal link, not the operator.

---

## 6. mhc — the dormant Tier-2 case

mhc clears the bridge (100%) but is **dormant** (last invoice 2025-12-22, last login 2026-02-28). Therefore:
`report_through_date` pins to its last real invoice; **every row carries a dormancy banner**; **$-at-risk is shown
historical, never pushed as live**; Mixpanel is **LOGINS-ONLY** (no C4 feature depth) so AXIS B degrades to
login/order effort. Run mhc only on explicit request and label the whole digest "DORMANT — historical."

---

## 7. Live validation `[from-live]` (read-only, 2026-06-29)

**Cohort dry-run — all 8 Tier-2 orgs (`report_through_date` / freshness, oid):** sarreid (1, 2026-06-29 fresh),
clc (40, 2026-06-27 fresh, **300K lines**), wwjc (8, 2026-06-29 fresh), pf (32, 2026-06-26 fresh), ril (245,
2026-06-26 fresh), cci (161, 2026-06-26 fresh), bcf (171, 2026-06-26 fresh, Tier-2 boundary 81.8%), mhc (46,
**DORMANT** last invoice 2025-12-22). All STRONG except mhc (dormant).

**AXIS O — both axes returned cleanly per org (deduped bridge + MATERIALIZED C2):**

| Org | Top S1 $-at-risk rep | Top C2 leakage rep | Per-org flag caught |
|---|---|---|---|
| **cci** | VIVI MIRA-CULMER $965K (23 accts) | rep leak rates all <2% (healthy book) | `HOUSE ACCOUNT` tops C2 ($68K) → exclude (G-B) |
| **clc** (300K) | Capital Lighting Fixture $12.9M (16) | Capital Lighting Fixture $460K / 2.5% | dup spellings KTR/Philip Winston → `DISTINCT ON` (G-A); Capital Lighting likely house (G-B) |
| **wwjc** | `12 House Account` $1.6M (21) | `12 House Account` $36K | #1 at-risk is a house rep → exclude (G-B); reps carry rep-code prefixes |
| **pf** | DILAURO DONALD $1.28M (15) | — (mid-size, runs in-window) | clean named agencies |
| **ril** | Ratana $2.49M (24) | Ratana $142K / **26.9%** | `Ratana` = furniture brand/house → the gut-check case (both axes) |
| **sarreid** | Charles Hoffman $786K (7) | — (runs in-window) | `Deborah Klein` vs `Deborah Klien` = 2 rep#s, typo (soft note) |
| **bcf** | Todd Teague (Twinco Inc.) $1.07M (9) | (validated in build) | reps are agencies; `rep 3` unmapped, **not dropped** ✅ |
| **mhc** | — (DORMANT — historical only) | — | LOGINS-ONLY; dormancy banner; no live $-at-risk |

**AXIS B — Mixpanel behavior (bcf, 90d):** C6 cadence returned 25 handles (`bharper2` 45 accts/432 presentations,
`jmontini` 19/237…); C4 feature depth returned the 6-dimension breadth per `username`. Both axes live + named.

**The join lesson (bcf):** outcome `rep_name` = agency strings, behavior `username` = individual handles
(`tteague`/`ateague` ↔ `Todd Teague (Twinco Inc.)`; `sbillingsley` ↔ `SVB…/Steve Bill`). Confirms the
no-fused-number design and re-affirms **Option B is blocked on a validated `username↔rep_name` resolver.**

**C2 execution — RESOLVED:** the `MATERIALIZED` form runs in-window on **all** Tier-2 books incl. clc (300K). The
plain form timed out on every org (plan pathology, not size); `PERCENTILE_CONT … WITHIN GROUP` is validator-blocked
by the MCP. Canonical leakage logic also validated on asi (rep 12 = $163K / 5.9%).

---

## 8. Status, owner gates, open items

- **Owner gate:** Option A is **owner-approved** (GO 2026-06-29) and **re-confirmed to start** 2026-06-29. Options
  B (fused dollar) and C (client-facing) remain **deferred** — do not build.
- **Standing runtime gates** (inherited, not bypassed): per-report human gut-check on C2 leakage; per-org
  `house_suspect` confirmation **screening rep labels too** (G-B); deduped bridge (G-A); mhc dormancy banner;
  Tier-2 admission.
- **~~Open item — C2 execution~~ ✅ RESOLVED 2026-06-29:** `MATERIALIZED` CTEs run C2-by-rep in-window on every
  Tier-2 book (validated to 300K / clc). No non-restricted connection needed.
- **~~Remaining — per-org house-rep allow/deny list~~ ✅ CLOSED 2026-06-29; AUTO-RULE added 2026-06-30:** captured +
  owner-confirmed for all 8 Tier-2 orgs in [`house_rep_exclusions.md`](../config/house_rep_exclusions.md) (13 EXCLUDE
  rows; sarreid = none); **AUTO-RULE `rep_label ILIKE 'house%' OR '% house account%'` is now baked into both O1 and O2
  SQL** so a never-onboarded org (kal in PASS1) still gets screened. Reruns are deterministic — consume that file
  *plus* the auto-rule when screening the S1/C2 rep_name side (G-B). Re-confirm an org only if its account-code/
  rep-code scheme changes (D4).
- **Remaining (lower-priority):** Option B (fused dollar) stays blocked on the `username↔rep_name` resolver.

---

## Appendix — provenance & supersession

- **Read-only** throughout (`user-supercat-postgres-vpn` `execute_sql`; `user-bigquery-admin` `query`), 2026-06-29.
- **Consumes, does not re-author:** `selling_customer_exception_layer.md` (C2, S1); `query_library_v2.md` (Q-01,
  Q-63/64/65 — patched onto native `mixpanel.events`); `rep_copilot_operator.md` (RP-1/RP-2 preflight, tier gate,
  house flag, mhc dormancy); `provenance_spine.md` (§5 tiers, §6.8 caps, §6.10 leakage, §7.1 the 3-tier gate);
  `rung4_fusion_decision_brief.md` (the sanctioned Option-A scope).
- **Constraints honored:** no fused number; Tier-2 only; every dollar capped at `COMMERCE_CONFIDENCE` or
  suppressed; behavior is context (never a lead, never inferred from absence); internal-only; correlation not cause;
  no margin/AR/cash implied; house accounts flagged; soft join labeled, never dropped, never fused.
- **Status:** APPLIED OPERATOR — Option A. Two-axis live-validated on bcf, outcome axis on cci. B & C deferred.
