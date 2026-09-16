# Selling & Customer — Exception-Push Synthesis Layer

> **"I'd pay for answers, not dashboards. Tell me 'these 12 accounts are at risk, worth $1.4M, here's who to
> call' and 'you leaked $340K, concentrated in these three reps.' Push me the exceptions and the dollar
> impact. Don't make me go fishing."**
>
> This layer sits **on top of** the hardened Domain-10 queries in [`query_library_v2.md`](query_library_v2.md).
> Where the library answers a question when asked, this layer **decides what is worth saying** and pushes it
> with a dollar figure and a name attached. It inherits the `Q-ECON-00` gate and every hard-gap guardrail.
> Phase C of [`selling_customer_hardening_plan`](../../.cursor/plans). Aligned to Customer-Intelligence v4
> design ([`../../Customer Intelligence/09_v4_design.md`](../../Customer%20Intelligence/09_v4_design.md)) §15
> (revenue-at-risk) and §16 (alert banners).

## The exception object

Every exception the system pushes is one row of this shape — never a chart, never a table the reader must
mine:

| field | meaning |
|---|---|
| `type` | exception family (S1 account-health, C2 leakage-by-rep, …) |
| `severity` | CRITICAL / WARNING / INFO (tiered per §16) |
| `dollar_impact` | the single number that earns attention ($ at risk or $ leaked) |
| `subject` | the account or rep the exception is about (name-resolved — R11) |
| `who_to_call` | the rep/owner to act (from rep identity on the record) |
| `one_line` | the pushed sentence ("X is down 79% over 6 months, $70K LTM at risk — call rep MKJ") |
| `evidence` | the 2–3 numbers that back it (recent vs prior, leak rate, days silent) |
| `confidence` | `LEAST(own ceiling, COMMERCE_CONFIDENCE)` from `Q-ECON-00`: **NONE → suppress**, **PARTIAL → present the dollar as a labeled floor (never a hard pushed CRITICAL)**, STRONG → push normally. `FULL` is unreachable for economics. |

**Ranking rule:** sort the daily push by `dollar_impact × severity_weight`, cap at ~12 items (per §14 — beyond
that it reads as "everything is on fire"). Everything else stays queryable but unpushed.

---

## Exception S1 — Account-Health $-at-Risk (the "quietly dying" alarm)

**Fires when** a material account's **last-6-month** invoiced revenue falls materially below its **prior
6-month** revenue (equal windows), OR it has gone silent past 2× its normal order gap. Dollar impact = the
account's LTM revenue (what's on the table if it churns). Detects the decline **90 days before** a hard
dormancy flag because it watches the slope, not just the last order date.

> **Hardening refinement (validated live, cci):** the decay comparison **must use equal-length windows**
> (last 6mo vs the 6mo before it). An early build compared 6mo vs prior-18mo and flagged **WAYFAIR ($7.9M) as
> at-risk while it was actually accelerating** ($424K/mo recent vs $298K/mo prior) — a reputation-killing false
> positive. The equal-window form removes every accelerating account and surfaces only genuine decay.

**PRECONDITION (Defect J fix):** run `Q-ECON-00` (which carries the `Q-PROV-00` logic) **first** and read
`commerce_confidence` + `report_through_date`. **If `commerce_confidence = 'NONE'` → suppress S1 entirely**
(no invoice feed; the $-at-risk is unknowable). **If `'PARTIAL'`** (stale or provably-incomplete feed, e.g.
`bmc`/`sc`) → the LTM dollar is a **floor**; present it labeled *"at-risk ≥ $X (partial feed)"* and never push
it as a hard CRITICAL figure. The query anchors every window on `{{REPORT_THROUGH_DATE}}` so a stale feed
measures decay against its own last real invoice, not against empty recent months.

```sql
-- S1: per-account decay, equal 6mo windows, $ at risk = LTM revenue, who-to-call = rep
-- Windows anchored on {{REPORT_THROUGH_DATE}} (= Q-ECON-00.report_through_date; defaults to CURRENT_DATE).
-- Name bridge (R11 / Spine §7.1): subject carries the customer NAME (portal_invoices.customer_bill_to_name)
-- and who_to_call is name-resolved to the rep via portal_orders — codes are kept as the fallback so a
-- Tier-1 org (or an unmapped rep) still renders "rep <n>" rather than a blank. The pipeline decides
-- whether to show the name (Tier 2) or the code (Tier 0/1); the query never drops either.
WITH rep_names AS (   -- invoices carry rep_number only; bridge to name via portal_orders (same source as RS-01)
  SELECT DISTINCT ON (rep_number) rep_number, rep_name   -- one deterministic name per rep_number
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> ''
  ORDER BY rep_number, rep_name
),
c AS (
  SELECT customer_bill_to_number AS cust,
         MAX(customer_bill_to_name) AS cust_name,
         MAX(rep_number) AS rep,
         COUNT(*) AS n_inv,
         MIN(invoice_date) AS first_d, MAX(invoice_date) AS last_d,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') AS ltm_rev,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= {{REPORT_THROUGH_DATE}}::date - INTERVAL '6 months')  AS r_recent,
         SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months'
                                                    AND invoice_date <  {{REPORT_THROUGH_DATE}}::date - INTERVAL '6 months')  AS r_prior
  FROM portal_invoices
  WHERE organization_id = {{ORG_ID}}
    AND invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '24 months' AND {{REPORT_THROUGH_DATE}}::date   -- R1 clamp
  GROUP BY customer_bill_to_number
  HAVING COUNT(*) >= 6
     AND SUM(net_amount) FILTER (WHERE net_amount>0 AND invoice_date >= {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') > 20000
)
SELECT c.cust AS subject,
       COALESCE(NULLIF(TRIM(c.cust_name),''), c.cust)             AS bill_to_name,   -- R11: named account (code fallback)
       c.rep AS who_to_call,
       rn.rep_name                                                AS rep_name,       -- §7.1: named rep (NULL → template renders "rep <n>")
       ROUND(c.ltm_rev::numeric,0)                                AS dollar_impact,   -- $ at risk (a FLOOR on PARTIAL feeds)
       ({{REPORT_THROUGH_DATE}}::date - c.last_d)                 AS days_silent,
       ROUND(c.r_recent::numeric,0) AS recent_6mo, ROUND(c.r_prior::numeric,0) AS prior_6mo,
       ROUND(100.0*(c.r_recent - c.r_prior)/NULLIF(c.r_prior,0),0) AS change_pct,
       -- CRITICAL on cadence side: scale to the account's own reorder cadence (4× mean gap),
       -- with a 14-day absolute floor so a daily-cadence book (e.g. a 590-invoice account at
       -- ~1 day mean gap) does NOT trip CRITICAL on a 1.5-day silence. WARNING (the WHERE
       -- clause below) still fires at 2× mean gap — only the CRITICAL escalation is gated.
       CASE WHEN c.r_recent < 0.4*c.r_prior
              OR ({{REPORT_THROUGH_DATE}}::date - c.last_d)
                   > GREATEST(14, 4*((c.last_d - c.first_d)::numeric/NULLIF(c.n_inv-1,0)))
            THEN 'CRITICAL' ELSE 'WARNING' END                    AS severity
FROM c
LEFT JOIN rep_names rn ON rn.rep_number = c.rep
WHERE (c.r_prior > 0 AND c.r_recent < 0.6*c.r_prior)                                  -- equal-window decay
   OR ({{REPORT_THROUGH_DATE}}::date - c.last_d) > 2*((c.last_d - c.first_d)::numeric/NULLIF(c.n_inv-1,0))   -- early dormancy (WARNING)
ORDER BY c.ltm_rev DESC
LIMIT 12
```

**Pushed example (cci, live):** *"HATCH P is down 79% over the last 6 months ($58K → $12K), $70K LTM at risk —
call rep MKJ."* · *"JGASTON has gone 82 days silent, $69K LTM at risk — call rep ROBB."*

**Gating:** requires `invoice_feed_present`; **suppressed at `NONE`, floored/labeled at `PARTIAL`** per the
precondition above. Name-resolve `subject` via the `customers` join (R11 — clli-type orgs have blank invoice
names; naming requires the Spine §7.1 Tier-2 bridge). Confidence inherits `LEAST(STRONG, COMMERCE_CONFIDENCE)`.

**CRITICAL severity is cadence-scaled with a 14-day floor (2026-06-30).** The original `> 2× mean gap`
escalation tripped CRITICAL on ~1.5 days of silence for high-velocity books (e.g. a 590-invoice account with a
~1-day mean gap, where 2× = ~2 days). CRITICAL now requires `silent > GREATEST(14, 4 × mean_gap)` — daily-cadence
books need ≥14 days silent, weekly books ≥28 days, monthly books ≥120 days, quarterly books ≥360 days, all
scaled to the account's own rhythm rather than an absolute day count. The WARNING WHERE clause (`> 2× mean_gap`)
is unchanged — the account still surfaces; only the CRITICAL framing waits for material silence.

---

## Exception C2 — Leakage-by-Rep (the "rogue discounting" alarm)

**Fires when** discretionary price leakage (the **tier-aware** `Q-ECON-LEAK` dispersion) concentrates in
specific reps. Dollar impact = the rep's leaked dollars (after the tier & volume guards); severity keys on the
rep's **leak rate** (leaked ÷ that rep's revenue), which separates a rogue discounter from a big book with a
normal rate.

> **Audit-remediation correction (validated live, asi, 2026-06-29):** the earlier build (trimmed mean, no tier/
> volume guard) reported **"Rep 69 leaked $1.35M = 42% of revenue (rogue)"** — a **false positive**. Under the
> tier-aware engine (true median + tier guard + volume guard), rep 69 is a **normal $68K / 2.1%**; the entire
> "42%" was negotiated price tiers and volume accounts, not discretionary leakage. The corrected standout is a
> mild **rep 12 at $163K / 5.9%**. This is exactly the reputation-killer the guards exist to prevent — present
> both the leaked dollars and the leak-rate, both computed after the guards.

```sql
-- C2: TIER-AWARE dispersion leakage rolled up by rep (inherits the redesigned Q-ECON-LEAK)
WITH rep_names AS (   -- §7.1 name bridge: rep_number → rep_name via portal_orders (same source as RS-01/S1)
  SELECT DISTINCT ON (rep_number) rep_number, rep_name
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> ''
  ORDER BY rep_number, rep_name
),
custagg AS (   -- customer grain; rep = the rep on that customer-SKU (most customers carry one)
  SELECT pii.item_number AS item, pi.customer_bill_to_number AS cust, MAX(pi.rep_number) AS rep,
         SUM(pii.quantity_invoiced) AS qty,
         SUM(pii.quantity_invoiced*pii.unit_price)/NULLIF(SUM(pii.quantity_invoiced),0) AS realized
  FROM portal_invoice_items pii
  JOIN portal_invoices pi ON pi.invoice_number=pii.invoice_number AND pi.organization_id=pii.organization_id
  WHERE pii.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months' AND {{REPORT_THROUGH_DATE}}::date
    AND pi.net_amount>0 AND pii.quantity_invoiced>0 AND pii.unit_price>0
    AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'ZZ%'              -- R-LEAK-B: house/sample auto-exclude
    AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'ACCOM%' AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'SAMPLE%'
    AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'HOUSE%' AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'DISPLAY%'
    AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'SHOWROOM%' AND COALESCE(pi.customer_bill_to_number,'') NOT ILIKE 'TEST%'  -- (confirm full prefix set per org)
  GROUP BY pii.item_number, pi.customer_bill_to_number
),
itemagg AS (SELECT item, COUNT(*) ncust, SUM(qty) tot_units FROM custagg GROUP BY item HAVING COUNT(*)>=5),
ranked AS (SELECT c.item,c.realized, ROW_NUMBER() OVER (PARTITION BY c.item ORDER BY c.realized) rn, COUNT(*) OVER (PARTITION BY c.item) cnt FROM custagg c JOIN itemagg i ON i.item=c.item),
ref AS (SELECT item, AVG(realized) ref_price FROM ranked WHERE rn IN (FLOOR((cnt+1)/2.0), CEIL((cnt+1)/2.0)) GROUP BY item),  -- true median
tier AS (SELECT c.item, ROUND(c.realized,2) px FROM custagg c JOIN itemagg i ON i.item=c.item GROUP BY c.item, ROUND(c.realized,2) HAVING COUNT(*)>=5),  -- tier guard
scored AS (SELECT c.rep, c.qty, c.realized, r.ref_price,
                  (t.px IS NOT NULL) AS at_tier, (c.qty >= 0.10*i.tot_units) AS strategic   -- volume guard
           FROM custagg c JOIN itemagg i ON i.item=c.item JOIN ref r ON r.item=c.item
           LEFT JOIN tier t ON t.item=c.item AND t.px=ROUND(c.realized,2))
SELECT COALESCE(NULLIF(TRIM(s.rep),''),'(unattributed)')                               AS who_to_call,
       MAX(rn.rep_name)                                                                 AS rep_name,   -- §7.1 named rep (NULL → "rep <n>")
       ROUND(SUM(qty*(ref_price-realized)) FILTER (WHERE realized<ref_price*0.9 AND NOT at_tier AND NOT strategic)::numeric,0) AS dollar_impact,
       ROUND(100.0*SUM(qty*(ref_price-realized)) FILTER (WHERE realized<ref_price*0.9 AND NOT at_tier AND NOT strategic)
             /NULLIF(SUM(qty*realized),0),1)                                            AS leak_rate_pct,
       CASE WHEN 100.0*SUM(qty*(ref_price-realized)) FILTER (WHERE realized<ref_price*0.9 AND NOT at_tier AND NOT strategic)
                 /NULLIF(SUM(qty*realized),0) >= 10 THEN 'CRITICAL' ELSE 'WARNING' END  AS severity
FROM scored s
LEFT JOIN rep_names rn ON rn.rep_number = s.rep
GROUP BY 1
HAVING SUM(qty*(ref_price-realized)) FILTER (WHERE realized<ref_price*0.9 AND NOT at_tier AND NOT strategic) > 0
ORDER BY dollar_impact DESC
LIMIT 12
```

**Pushed example (asi, live, tier-aware):** *"Rep 12 carries the widest discretionary spread — ~$163K, 5.9% of
their book, above the ~2% peer norm. Worth a discount-discipline conversation."* (Rep 69, previously mis-flagged
as a $1.35M/42% rogue, is normal at 2.1%.)

**Gating:** requires `leakage_dispersion_ok` (**priced invoice lines** ≥60% — NOT a products join). **Confidence
caps at `COMMERCE_CONFIDENCE`** — suppress the rep dollar on PARTIAL/stale feeds. Naming the rep also requires
the Spine §7.1 **Tier-2 name bridge** (≥80%); on Tier-1 orgs report at `rep_number` grain only. **Mandatory
human gut-check before client delivery** (worksheet A.5.6); house/sample accounts are **auto-detected + flagged**
(same `house_suspect` logic as `Q-ECON-LEAK` — `ZZ*` dropped, `ACCOM*`/`SAMPLE*`/… + tiny-rev/huge-leak flagged)
and excluded pending per-org owner review. Never frame as "% off list". **Client-facing label APPROVED
2026-06-29** (`selling_customer_label_signoff.md`).

---

## Roadmap (next exception types, not yet built)

| id | exception | source | status |
|---|---|---|---|
| S2 | Competitive displacement (eCat down while total business up) | CI v4 §16 banner + Q-CHAN-05 | designed, CI-side |
| S3 | Stock-out on a top-15 item with live demand | Q-37 | designed |
| C3 | Returns spike by SKU (dollar-based) | Q-ECON-RETURNS | candidate |
| C4 | Vanity-quoting org (quote→purchase < ~15%) | Q-SELL-QC | candidate (org-level) |

**Hard gaps that will NOT generate exceptions** (no data — do not fabricate): margin-at-risk, AR/credit-risk,
damage-by-carrier, quoted-lead-time miss, market/showroom ROI.
