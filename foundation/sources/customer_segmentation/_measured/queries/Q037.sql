-- Q037 | LINE B (JTBD-014, 062): accounts down >30% on trailing 90 days vs their own prior 90
-- Run: 2026-08-31, on portal_invoices (invoiced truth) for the 40 orgs with feed coverage.
-- Result: 52,818 accounts active in either period across 40 orgs.
--         15,156 went completely silent | 7,862 more down >30% while still buying
--         => 23,243 accounts (44.0% of the base) would fire a naive rule
--         $112.9M of decline against a $302.7M prior-period base (-37.3% aggregate)
--         14,133 accounts newly buying in the current period.
-- A fixed 30% threshold flags nearly half the customer base. That is noise, not a work list.
-- It demonstrates -- rather than asserts -- the need for the A8 per-account baseline store.
-- CAVEAT (JUDGMENT): Jun-Aug vs Mar-May crosses a market cycle; seasonality inflates this.
--   That confound reinforces the same conclusion: the window must be account-aware.
WITH cur AS (SELECT organization_id, customer_bill_to_number AS acct,
    sum(COALESCE(net_amount,total_amount,0)) AS v FROM portal_invoices
  WHERE invoice_date >= (now()-interval '90 days')::date
    AND btrim(COALESCE(customer_bill_to_number,''))<>'' GROUP BY 1,2),
prv AS (SELECT organization_id, customer_bill_to_number AS acct,
    sum(COALESCE(net_amount,total_amount,0)) AS v FROM portal_invoices
  WHERE invoice_date >= (now()-interval '180 days')::date AND invoice_date < (now()-interval '90 days')::date
    AND btrim(COALESCE(customer_bill_to_number,''))<>'' GROUP BY 1,2),
j AS (SELECT COALESCE(cur.organization_id,prv.organization_id) AS org, COALESCE(cur.acct,prv.acct) AS acct,
      COALESCE(cur.v,0) AS cur_v, COALESCE(prv.v,0) AS prv_v
  FROM cur FULL OUTER JOIN prv ON prv.organization_id=cur.organization_id AND prv.acct=cur.acct)
SELECT count(*) AS accounts_active_either_period, count(DISTINCT org) AS orgs,
 count(*) FILTER (WHERE prv_v > 0 AND cur_v = 0) AS went_silent,
 count(*) FILTER (WHERE prv_v > 0 AND cur_v > 0 AND cur_v < prv_v*0.7) AS down_over_30pct,
 count(*) FILTER (WHERE prv_v > 0 AND cur_v < prv_v*0.7) AS at_risk_total,
 round(sum(prv_v - cur_v) FILTER (WHERE prv_v > 0 AND cur_v < prv_v*0.7)) AS dollars_at_risk,
 round(sum(prv_v) FILTER (WHERE prv_v>0)) AS prior_period_total,
 count(*) FILTER (WHERE prv_v = 0 AND cur_v > 0) AS newly_buying
FROM j;
