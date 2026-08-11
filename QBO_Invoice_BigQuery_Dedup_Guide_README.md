# QBO Invoice BigQuery Dedup Guide

**Use this README when querying `quickbooks__invoice` in BigQuery for balance, AR, overdue, or payment data.**

---

## The Problem

The `quickbooks__invoice` table in BigQuery (WELD_RAW) has two data quality issues:

1. **Duplicate historical rows** — Weld appends new row versions when an invoice is updated in QBO, but old rows with stale balances remain. A query like `WHERE balance > 0` picks up old snapshots of invoices that have since been paid.
2. **Missing updates** — Some invoices that were voided, deleted, or paid in QBO never had their updates synced to BigQuery. The only row is the original with the full balance.

---

## How to Query Correctly

### Step 1: Always deduplicate

Wrap every QBO invoice query in a CTE that takes the latest row per `doc_number`:

```sql
WITH latest_invoices AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY doc_number
      ORDER BY meta_data_last_updated_time DESC
    ) AS rn
  FROM quickbooks__invoice
)
SELECT *
FROM latest_invoices
WHERE rn = 1
```

### Step 2: Apply your filters on the deduplicated result

```sql
-- Example: Overdue AR
WITH latest_invoices AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY doc_number
      ORDER BY meta_data_last_updated_time DESC
    ) AS rn
  FROM quickbooks__invoice
)
SELECT customer_ref_name, doc_number, total_amt, balance, due_date
FROM latest_invoices
WHERE rn = 1
  AND balance > 0
  AND due_date < CURRENT_TIMESTAMP()
ORDER BY due_date ASC
```

### Step 3: Cross-check significant amounts against Stripe

Even after dedup, some QBO balances may be stale (the sync missed the update entirely). For any significant AR figure, verify against `stripe__invoice`:

```sql
SELECT number, customer_name, status, paid, amount_remaining / 100.0 AS remaining
FROM stripe__invoice
WHERE number = '<doc_number>'
ORDER BY created DESC
LIMIT 5
```

If Stripe shows `status = 'void'` or `paid = true` but QBO still shows a balance, the QBO data is stale — do not include it in AR totals.

---

## Rules

1. **Never** query `quickbooks__invoice` directly with `WHERE balance > 0` — always dedup first.
2. **Always** use `ROW_NUMBER() OVER (PARTITION BY doc_number ORDER BY meta_data_last_updated_time DESC)` and filter to `rn = 1`.
3. **Cross-check** any AR total > $1,000 against the corresponding Stripe invoice status.
4. **Do not** treat QBO BigQuery AR figures as authoritative until the Weld sync issue is resolved by the data team.
5. The Stripe `amount_due` and `amount_remaining` fields are in **cents** — divide by 100 for dollars.

---

## Background

In April 2026, a query on the raw QBO table returned ~$28.5k in overdue AR. After dedup and Stripe cross-checks, the real overdue was ~$4k. The difference was voided/paid/deleted invoices that BigQuery never updated. This has been flagged with the data team (Kev) for a permanent fix to the Weld sync configuration.

---

## References

- `BIGQUERY_WINDMILL_OPERATOR_GUIDE.md` — full BigQuery query rules and table reference (updated with QBO data quality section)
- `.cursor/rules/qbo-invoice-dedup.mdc` — Cursor rule that auto-triggers the dedup pattern
- `doc/BIGQUERY_WINDMILL_MCP_REFERENCE.md` — detailed table schemas and example queries
