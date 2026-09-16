# Q-38a — Product Velocity Trend

- **Org:** Sarreid · org_id = 1
- **Period:** LTM
- **Row count:** 0 (usable product-level rows)
- **Run date:** 2026-04-17
- **Exclusions:** None

---

> **Data Gap:** The portal_order_items table contains 61,220 rows for this org, but the `ecat_item_number` column is empty (NULL/blank) for all rows. The query returned aggregate monthly totals but no product-level detail could be extracted.
>
> This means product velocity trends (item-level sales over time via eCat) cannot be computed from portal_order_items for Sarreid. ERP invoice data (used in Q-37 and Q-39) provides product-level sales but without eCat-specific attribution.
>
> **Root cause:** The eCat item number is not being populated on order line items for this org — likely a configuration or integration issue with how order items are synced from the iPad app.
