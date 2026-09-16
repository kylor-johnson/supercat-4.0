# Q-46: eCat Selling Workflow Maturity — Visual Comfort - Studio /Fans (fms, org_id=108)
- **Run date**: 2026-04-30

## Postgres Side (Numerator)
- Submitted eCat orders (90d): 181

## Mixpanel Side (Denominator — all-time from Q-22)
- Customer targeting events: 29,495 (select_a_customer: 11,235 + search_for_customer: 18,260)
- Product discovery events: 56,722 (search_products: 55,177 + filter_products: 1,545)
- Presentation events: 2,853 (create_pdf_catalog: 2,220 + email_item_info: 599 + share_my_list: 34)

## Band Classification
- Submit rate not directly calculable from all-time Mixpanel vs 90d Postgres (different time windows)
- All-time submit_order: 2,035 vs all-time total_events: 199,873 = 1.0% of total activity
- Platform role: Enablement-heavy — eCat is primarily a selling/presentation layer with partial order capture
