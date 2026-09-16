# Customer Intelligence — How to Run (Operator Guide)

A SuperCat Customer Intelligence Brief is a per-customer sales-prep document built
entirely from live SuperCat data (Postgres + BigQuery), via Cursor MCP connections.
This guide gets you from zero to a finished brief. No prior context required.

---

## 1. What you're producing

For a single customer account, a `brief.md` covering ~20 sections: account health
score, spend trajectory, buying rhythm, category/item purchase DNA, fill rate,
cross-sell gaps, and a strategic pre-meeting summary. Every number traces to a SQL
query — nothing is fabricated or estimated.

Example finished briefs already live under `runs/` (e.g. `runs/ufi/3002/brief.md`,
`runs/wwjc/21762/brief_v4.html`). Open a couple to see the target output.

---

## 2. Prerequisites (do this first)

You **cannot** run these without live data access:

1. **VPN active** — both data sources require it.
2. **Cursor with two MCPs enabled:**
   - `user-supercat-postgres-vpn` (tool: `execute_sql`, param: `sql`) — main data source
   - `user-bigquery-admin` (tool: `sql`) — only needed for the Rep Engagement section
3. **This whole folder** available to the agent (authority + operators + template).

Quick connection test before a real run — ask the agent to run, via the Postgres MCP:

```sql
SELECT id, shortname, name FROM organizations WHERE shortname = 'ufi';
```

If that returns a row, you're connected. If it errors, fix VPN / MCP before going further.

> Everything is **read-only**. Every query is a SELECT. The workflow never writes,
> updates, or deletes data.

---

## 3. Running ONE brief (the common case)

You need 4 things about the customer:

| Parameter | What it is | How to find it |
|-----------|------------|----------------|
| Shortname | org's short code (e.g. `ufi`, `sc`, `clm`) | you usually know it, or look it up in `organizations` |
| Org ID | integer org id | `SELECT id FROM organizations WHERE shortname = '<short>'` |
| Customer code | the bill-to code | see "find a good customer" below |
| Client name | display name | from `organizations.name` |

**Find a strong customer to profile** (most data = best brief):

```sql
SELECT customer_bill_to_number AS customer_code,
       c.name AS customer_name,
       COUNT(*) AS orders_ltm,
       ROUND(SUM(po.total_amount)::numeric, 2) AS ltm_revenue
FROM portal_orders po
LEFT JOIN customers c ON c.code = po.customer_bill_to_number
                     AND c.organization_id = po.organization_id
WHERE po.organization_id = <ORG_ID>
  AND po.order_date >= NOW() - INTERVAL '12 months'
  AND po.customer_bill_to_number IS NOT NULL
GROUP BY 1, 2
HAVING COUNT(*) >= 10
ORDER BY ltm_revenue DESC
LIMIT 10;
```

Pick a high-revenue customer with 10+ orders.

**Then start a fresh Cursor agent chat and paste this:**

```
Follow the run prompt in: Customer Intelligence/operators/customer_brief_run_prompt.md

Client name:   <CLIENT NAME>
Shortname:     <SHORTNAME>
Org ID:        <ORG_ID>
Customer code: <CUSTOMER_CODE>
Run date:      <TODAY'S DATE>

Run the full workflow and save the brief to its run directory.
```

The agent reads the authority files, runs a pre-flight readiness check, gathers data,
builds sections, and writes:

```
Customer Intelligence/runs/<shortname>/<customer_code>/brief.md
```

**Runtime:** ~3–8 minutes per brief.

---

## 4. Running MANY briefs (batch / pilot)

To profile a set of clients at once, use the batch prompt instead:

`operators/pilot_batch_prompt.md`

It runs in two phases:
1. **Agent 1 — Discovery:** finds active orgs, scores their data richness, picks the
   best clients + 2 customers each, and writes `runs/pilot_manifest.md`.
2. **Agents 2–5 — Generation:** each takes a slice of the manifest and produces briefs
   in parallel (run sequentially in one chat is fine too, just slower).

Start with Phase A (Agent 1). Once `pilot_manifest.md` exists, launch the generation
agents with the launch snippet at the bottom of `pilot_batch_prompt.md`.

---

## 5. What's in this folder

| Path | What it is |
|------|------------|
| `operators/customer_brief_run_prompt.md` | **The main prompt** — single-customer workflow |
| `operators/pilot_batch_prompt.md` | Batch/multi-client workflow |
| `operators/org_readiness_profiler.md` | Org-level pre-flight (which sections will render) |
| `authority/customer_query_library.md` | Every SQL query (CQ-01…CQ-26) — source of truth |
| `authority/customer_brief_sections.md` | How each section renders |
| `authority/customer_gate_rules.md` | The 11 gates that decide which sections appear |
| `authority/health_score_spec.md` | Health + engagement score formulas |
| `template/brief_v4_template.html` | HTML template for polished output |
| `runs/` | Existing finished briefs (examples + prior output) |
| `00`–`09`, `CHANGELOG.md` | Design history / background reading (optional) |

If short on time, the agent only strictly needs the `operators/` + `authority/` files.

---

## 6. Ground rules (tell the agent these)

- **Read-only.** SELECT only. Never modify data.
- **If anything fails, stop and report** (single-brief mode). Don't improvise around
  missing data or broken queries. (Batch mode is the exception: it skips and continues.)
- **No fabrication.** Every claim must trace to a query result. No "approximately."
- **Use queries exactly as written** in `customer_query_library.md`. Don't rewrite them.
- If an org's data richness score is 0, there isn't enough data — skip it.

---

## 7. Quick troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| MCP/connection error | VPN down or MCP not enabled | Reconnect VPN, enable both MCPs in Cursor |
| "Insufficient data" | org has almost no order history | Pick a different, more active org/customer |
| Rep Engagement section missing | BigQuery (Mixpanel) gate false or BQ MCP off | Expected for many orgs — fine to proceed |
| Brief missing many sections | low data richness for that org | Normal — sections are gated by available data |
| Query errors mid-run | schema/data edge case | Stop, capture the error, send to Kylor |

---

*Questions Kylor can't answer async: the design rationale is in `00_product_concept.md`
and `09_v4_design.md`; the full change history is in `CHANGELOG.md`.*
