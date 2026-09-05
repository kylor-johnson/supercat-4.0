# Customer Intelligence Brief — Product Concept

> **Status**: Initial thinking — not yet designed or built
> **Date**: 2026-06-15
> **Parent system**: Insightful Product 2.0 (org-level intelligence report)
> **Relationship**: Sibling product — same data infrastructure, different aggregation lens and audience

---

## What this is

A per-customer intelligence brief that gives a sales rep everything they need to know about a specific account before they walk in the door. It takes the same data SuperCat already collects (orders, invoices, products, inventory, Mixpanel behavioral events, ERP sync) and flips the aggregation from org-level to customer-level.

## What it is NOT

- Not a replacement for the org-level Intelligence Report (Insightful Product 2.0)
- Not a CRM — it doesn't track contacts, deals, or pipeline
- Not a dashboard — it's a per-customer deliverable consumed before a sales call

## The core insight

The org-level report tells client leadership "how is your platform doing?" (quarterly, strategic, QBR cadence). The customer brief tells the rep "what do I need to know about THIS account?" (every visit, tactical, operational cadence).

| | Org Intelligence Report (today) | Customer Intelligence Brief (new) |
|---|---|---|
| **Audience** | VP Sales, CEO, client leadership | The individual rep |
| **Unit** | One report per org | One brief per customer |
| **Frequency** | Quarterly (QBR cadence) | Every sales call / pre-visit |
| **Question answered** | "How is our platform doing?" | "What do I need to know about this account?" |
| **Action proximity** | Strategic — informs decisions | Tactical — informs the next conversation |
| **Stickiness driver** | Impressive at renewal time | Daily operational dependency |

## Why it's monetizable

1. **Volume.** The org report is 1 per client. A customer brief is 1 per customer per visit. A client with 400 active dealers and 8 reps doing 3 visits/week = hundreds of briefs per quarter.

2. **Revenue attribution.** A rep who walks in knowing "they haven't tried your new collection, their top item is out of stock, and their order frequency is slipping" will sell differently. This creates stories: "I showed up knowing their favorite SKU was backordered, offered the alternative, and closed a $12K order."

3. **Lock-in.** Once reps depend on this before every call, it becomes operational infrastructure. The org report is impressive; the customer brief is addictive.

---

## Engineering requirement

**Zero.** Every data source needed is already in production. No new tables, no schema changes, no pipeline additions. The brief is buildable today from existing Postgres and BigQuery data using the same MCP connections the org-level report already uses.

The only confirmed data gap is end-customer web portal browsing attribution (Clicky/GA track visitors but not authenticated customer sessions). This would require instrumenting the portal login flow — a future enhancement, not a blocker.
