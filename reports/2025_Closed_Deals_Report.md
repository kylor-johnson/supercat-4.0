# 2025 Closed Deals Report

**Report Generated:** February 17, 2026  
**Data Source:** HubSpot via BigQuery  
**Period:** January 1, 2025 - December 31, 2025

## Executive Summary

### Overall Statistics

| Metric | Won Deals | Lost Deals | Total |
|--------|-----------|------------|-------|
| **Deal Count** | 24 | 87 | 111 |
| **Total Amount** | $251,742 | $999,174 | $1,250,916 |
| **Average Deal Size** | $10,489 | $11,618 | $11,269 |
| **Min Deal Size** | $2,340 | $1 | $1 |
| **Max Deal Size** | $25,200 | $49,032 | $49,032 |

### Key Insights

- **Win Rate:** 21.6% (24 won out of 111 closed deals)
- **Total Pipeline Value:** $1.25M closed in 2025
- **Won Revenue:** $251,742
- **Average Won Deal:** $10,489
- **Average Lost Deal:** $11,618

## Closed Won Deals (24 Deals - $251,742)

### Top Won Deals by Amount

1. **Coaster Fine Furniture - eCat** - $24,900 (Closed: Dec 5, 2025)
2. **Progress Lighting - eCat** - $25,200 (Closed: Dec 2, 2025)
3. **MAGIC LITE / NSL - eCat; eOL** - $22,680 (Closed: Nov 11, 2025)
4. **RATANA International - eOL w/ Sales Portal** - $14,220 (Closed: Feb 19, 2025)
5. **Wendover Art Group - eCat** - $17,040 (Closed: Feb 7, 2025)

### Won Deals by Owner

**Jon Vanderberg (jon@supercatsolutions.com):** 19 deals - $194,922
**Emery Rust (emery@supercatsolutions.com):** 5 deals - $56,820

### Monthly Won Deal Distribution

- **January 2025:** 1 deal - $16,200
- **February 2025:** 4 deals - $52,332
- **March 2025:** 5 deals - $34,812
- **April 2025:** 2 deals - $13,380
- **May 2025:** 1 deal - $9,480
- **June 2025:** 2 deals - $15,420
- **July 2025:** 2 deals - $9,480
- **August 2025:** 1 deal - $2,340
- **September 2025:** 1 deal - $8,700
- **October 2025:** 1 deal - $4,740
- **November 2025:** 2 deals - $31,380
- **December 2025:** 2 deals - $50,100

## Closed Lost Deals (87 Deals - $999,174)

### Top Lost Reasons

1. **No Response** - Most common reason
2. **Cost** - Price concerns
3. **Timing** - Not ready to buy
4. **Feature Limitation** - Product gaps
5. **No ICP Fit** - Not ideal customer profile

### Largest Lost Opportunities

1. **Hinkley - eCat** - $49,032 (Lost: Apr 1, 2025) - Reason: Timing
2. **Visual Comfort & Co - Direct** - $31,200 (Lost: Aug 31, 2025) - Reason: Cost
3. **LibAndCo eCat** - $26,220 (Lost: May 30, 2025) - Reason: No Response
4. **Wagonway - eCat** - $26,700 (Lost: Oct 31, 2025) - Reason: No Response
5. **Accent Decor - eCat** - $25,200 (Lost: Feb 10, 2025) - Reason: Timing

## Product Analysis

### Products in Won Deals
- **eCat** - Most popular product in won deals
- **eOL (eCat Online)** - Strong performance
- **Sales Portal** - Good add-on attachment
- **CPQ** - Several wins with CPQ add-on
- **Credit Card** - Small add-on deals

### Products in Lost Deals
- **eCat** - Highest volume but also highest loss rate
- **eCat w/ CPQ** - Several large lost opportunities
- **eOL** - Mixed results
- **Sales Portal** - Some standalone losses

## Recommendations

### To Improve Win Rate (Currently 21.6%)

1. **Address "No Response" Issue**
   - Implement better follow-up cadence
   - Improve initial engagement quality
   - Consider lead qualification improvements

2. **Price Optimization**
   - Review pricing strategy for deals lost to "Cost"
   - Consider value-based pricing or tiered options
   - Better ROI demonstration in sales process

3. **Feature Gap Analysis**
   - Prioritize features causing "Feature Limitation" losses
   - Consider product roadmap adjustments
   - Better expectation setting during sales

4. **Timing & Pipeline Management**
   - Better nurture campaigns for "Timing" losses
   - Implement re-engagement sequences
   - Track seasonal patterns

5. **ICP Refinement**
   - Focus on better-fit prospects
   - Reduce time spent on "No ICP Fit" opportunities
   - Improve lead scoring

## Detailed Deal List

### Query Used
```sql
SELECT 
  d.deal_id,
  d.properties_dealname as deal_name,
  d.properties_amount as amount,
  CASE WHEN d.properties_hs_is_closed_won = true THEN 'Won' ELSE 'Lost' END as status,
  d.properties_closedate as close_date,
  d.properties_createdate as create_date,
  d.properties_closed_won_reason as won_reason,
  d.properties_closed_lost_reason as lost_reason,
  o.email as owner_email,
  o.first_name as owner_first_name,
  o.last_name as owner_last_name
FROM hubspot__deal d
LEFT JOIN hubspot__owner o ON CAST(d.properties_hubspot_owner_id AS STRING) = o.owner_id
WHERE d.properties_hs_is_closed = true
  AND d.properties_closedate >= '2025-01-01'
  AND d.properties_closedate < '2026-01-01'
ORDER BY d.properties_closedate DESC
```

---

*For the complete detailed list of all 111 deals with full metadata, see the raw query results file.*
