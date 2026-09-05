-- Q031 | LINE B (JTBD-015, 043): orphan rate by ERP order status, orders older than 90 days
-- Run: 2026-08-31
-- Result: reveals portal_orders.status is completely unnormalised. Same concept spelled many ways:
--         closed = 'C'(251,691) / 'Closed'(154,750) / 'CLOSED'(43,603)
--         cancelled = 'Cancelled' / 'Canceled' / 'CANCELLED' / 'Cancelled Order' / 'X' / 'X-Canceled'
--         open = 'Open' / 'OPEN' / 'Open Order' / 'Open order' / 'O' / 'OPEN ORDER - OD'
--         Some values are literal DATES ('09/01/2026') -- a malformed ERP field mapping.
--         Genuine orphan signal: status 'C' 19.6% no invoice (49,337 orders); 'Closed' 9.7%.
WITH po AS (SELECT organization_id, order_number, status::text AS st FROM portal_orders
  WHERE order_date >= (now()-interval '12 months')::date
    AND order_date < (now()-interval '90 days')::date AND btrim(COALESCE(order_number,''))<>''),
pi AS (SELECT DISTINCT organization_id, order_number FROM portal_invoices WHERE btrim(COALESCE(order_number,''))<>'')
SELECT po.st, count(*) AS n, count(*) FILTER (WHERE pi.order_number IS NULL) AS no_invoice,
 round(100.0*count(*) FILTER (WHERE pi.order_number IS NULL)/count(*),1) AS pct
FROM po LEFT JOIN pi ON pi.organization_id=po.organization_id AND pi.order_number=po.order_number
GROUP BY 1 ORDER BY 2 DESC;
