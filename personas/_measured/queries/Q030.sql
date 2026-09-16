-- Q030 | LINE B (JTBD-041, 082): ERP orders with no matching invoice
-- Run: 2026-08-31. Join is organization_id + order_number (no FK exists).
-- Result: 1,279,729 portal orders in 12m across 43 orgs; 167,884 (13.1%) have no invoice row.
--         All 43 orgs affected.
WITH po AS (SELECT organization_id, order_number FROM portal_orders
  WHERE order_date >= (now()-interval '12 months')::date AND btrim(COALESCE(order_number,''))<>''),
pi AS (SELECT DISTINCT organization_id, order_number FROM portal_invoices
  WHERE btrim(COALESCE(order_number,''))<>'')
SELECT count(*) AS portal_orders_12m, count(DISTINCT po.organization_id) AS orgs,
 count(*) FILTER (WHERE pi.order_number IS NULL) AS orders_no_invoice,
 round(100.0*count(*) FILTER (WHERE pi.order_number IS NULL)/count(*),1) AS pct_no_invoice,
 count(DISTINCT po.organization_id) FILTER (WHERE pi.order_number IS NULL) AS orgs_affected
FROM po LEFT JOIN pi ON pi.organization_id=po.organization_id AND pi.order_number=po.order_number;
