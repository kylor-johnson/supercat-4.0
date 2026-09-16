# Insightful 4.0 — Post-Render Audit Prompt (External)

> **Purpose.** Quality-check a rendered HTML report after Step 6 of the run prompt.
> This is a human-readable audit that catches defects the automated `step10_check`
> does not cover.

---

## Step 1 — Open the HTML

Read the rendered HTML file:

```
outputs/{Org_Display}_CEO_intelligence_report_{date}.html
```

Also read the source MD for cross-reference:

```
outputs/{org}_DRAFT_{date}.md
```

---

## Step 2 — Verify the 5 Step-10 ledger items (checks 4, 8, 9, 11, 12)

Confirm the automated `step10_check` reported PASS. If it reported FAIL, stop — go back to the run prompt Step 6 and resolve before auditing.

| Check | What to verify |
|---|---|
| [4] §P forbidden-vocabulary sweep (MD) | Zero hits of SaaS/system/process/internal tokens in customer-facing copy |
| [8] Number reconciliation (HTML ↔ MD) | Every figure appearing 2+ times matches across both renders |
| [9] Verbatim 12-word phrase echo (HTML) | Zero repeated 12+ word phrases across §1/§2/§3/§5 headers and callouts |
| [11] HTML structure pairing | Every `<details>`, `<section>`, `<table>` opens and closes; all `id` attributes unique |
| [12] In-document anchor resolution | Every `<a href="#anchor">` resolves to an existing `id` in the same document |

---

## Step 3 — Cross-reference §1 topline against Appendix query trace

1. Find the headline LTM invoiced figure in §1 (the hero number).
2. Find the corresponding `Q-ECON-00` trace row in the Appendix Traceability block.
3. Verify the two figures match exactly (dollar amount, time period, dealer count).

If they differ: **DEFECT** — the headline was hand-edited or stale.

---

## Step 4 — Verify no Jinja artifacts leaked

Search the rendered HTML for:

- `{{` or `}}`
- `{% ` or ` %}`
- `{%- ` or ` -%}`
- `{{ undefined }}` or similar

Zero hits expected. Any hit is a **DEFECT** (template rendering failure).

---

## Step 5 — Spot-checks

### 5a. Dollar figures are time-qualified

Sample 3–5 dollar figures from the body. Each must carry a time qualifier (e.g. "LTM," "trailing 12 months," "recent 6 months," "prior 6 months"). A bare `$X` without temporal context is a **DEFECT**.

### 5b. Section headings match the TOC

Walk the sticky TOC strip at the top. Every TOC entry must:
- Link to an `id` that exists in the document (covered by check [12])
- Have a visible rendered section with a matching heading

A TOC entry pointing to a missing or misnamed section is a **DEFECT**.

---

## Step 6 — Report

List every defect found. For each:

| Field | Content |
|---|---|
| **Location** | Section id or line context (e.g. "§1 hero number," "#growth details block") |
| **Severity** | HALT (blocks shipping) / DELETE (remove the offending element) / WARN (cosmetic) |
| **Specific fix** | Name the template, signal rule, or render function to fix — not "rewrite the section" |

### Outcome summary

- **0 defects** → report is ship-ready.
- **WARN only** → ship with noted cosmetic items.
- **Any HALT or DELETE** → return to run prompt, fix the named template/rule, re-render, re-audit.
