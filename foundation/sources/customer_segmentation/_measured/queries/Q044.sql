-- Q044 | CALIBRATION (roadmap correction to data-gaps B3): shipment tracking coverage
-- Run: 2026-08-31. Reproduces the 2026-08-27 figures within drift.
-- Result: 4,940,517 invoices / 56 orgs
--         tracking_number  1,123,291 across 26 orgs   (08-27 pack: 1,121,123 / 26)  CONFIRMED
--         tracking_carrier   745,381                  (08-27 pack:   744,046)       CONFIRMED
--         ship_via         2,711,216 across 37 orgs   (08-27 pack: 2,712,248)       CONFIRMED
SELECT count(*) AS invoices, count(DISTINCT organization_id) AS orgs,
 count(*) FILTER (WHERE btrim(COALESCE(tracking_number,''))<>'') AS with_tracking,
 count(DISTINCT organization_id) FILTER (WHERE btrim(COALESCE(tracking_number,''))<>'') AS orgs_tracking,
 count(*) FILTER (WHERE btrim(COALESCE(tracking_carrier,''))<>'') AS with_carrier,
 count(*) FILTER (WHERE btrim(COALESCE(ship_via,''))<>'') AS with_ship_via,
 count(DISTINCT organization_id) FILTER (WHERE btrim(COALESCE(ship_via,''))<>'') AS orgs_ship_via
FROM portal_invoices;
