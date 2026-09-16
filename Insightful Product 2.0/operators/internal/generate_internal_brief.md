# Operator: Generate Internal Intelligence Brief

> **When to use**: Before a QBR or client meeting where we present the external Customer Intelligence Report
> **Input**: Client shortname (e.g., `cci`) provided by the user
> **Output**: One markdown document + one styled HTML document — internal CS operating brief
> **Time**: ~5-8 minutes
> **Prerequisite**: The external report should be generated first (for Meeting Playbook cross-references), but is not strictly required

---

Read these files before generating the brief:

| File | What It Provides |
|---|---|
| `operators/internal/internal-brief/DESIGN.md` | Section specs, rendering format, generation logic |
| `operators/internal/internal-brief/QUERIES.md` | All SQL/MCP queries, tag vocabulary, execution order |
| `operators/internal/internal-brief/TEMPLATE.html` | HTML template with CSS design system, placeholder tokens, component patterns |
| `Health V2/README.md` | Scoring specification — needed to explain dimensions in plain English |

Generate the internal brief for the client specified by the user.

---

## Step 0: Resolve Client Identity

**0a. Find the client in Health V2 CSV:**

Read `Health V2/runs/{latest}/client_health_scores_{date}.csv` and filter to `org_shortname = '{shortname}'`.

If the client is NOT in the Health V2 CSV, STOP and tell the user. The brief requires health data.

**0b. Load org_summary:**

Run Q-IB-ORG to get config flags (`has_clicky_portal`) and confirm display name.

**0c. Resolve email domains:**

Check `Health V2/cache/pg_domain_map.csv` for the client's email domains. Filter to `org_shortname = '{shortname}'`. Use only the corporate/company domains (not the hundreds of dealer/customer domains) for HelpScout attribution.

If the cache is unavailable, run Q-IB-DOMAIN against Postgres.

If no domains are found, HelpScout attribution is not possible for this client. Note in the brief: "Support data unavailable — no email domain mapping."

---

## Step 1: Query Support Data (HelpScout)

Run these queries in parallel via `user-bigquery-admin` → `query` (the `sql` param):

- **Q-IB-HELP-AGG** → summary metrics (total, open, escalations, severity, jira-linked)
- **Q-IB-HELP-DETAIL** → individual conversations with tag JSON
- **Q-IB-HELP-THEMES** → tag distribution grouped by dimension
- **Q-IB-HELP-AGING** → all open tickets with age

If Q-IB-HELP-AGG returns < 3 conversations in 90 days, extend to 180 days with Q-IB-HELP-EXTENDED.

**Parse tags from Q-IB-HELP-DETAIL**: For each conversation, extract:
- Escalation level (l1/l2/l3/l4) — from tags matching `l_ -`
- Severity (s1/s2/s3/s4) — from tags matching `s_ -`
- Type — from tags matching `type:`
- Product — from tags matching `product`
- Status flags — from tags matching `status:`

---

## Step 2: Query Jira Data

**2a. Cloud ID** (known constant): `3aea3e61-c30d-422a-9b0e-b5bab9b4c92a`

**2b. Search for client tickets:**
Run Q-IB-JIRA-SEARCH with the client name, then shortname. Filter results to those genuinely related to this client.

If the Jira MCP is unavailable, note Jira as unavailable and proceed — the brief is degraded but not blocked. Use the HelpScout `status: logged on jira` signal (the `jira_linked` count from Q-IB-HELP-AGG) as a fallback. There is **no BigQuery fallback for Jira** (the old `WELD_RAW.jira_issues` path was retired 2026-06-04 — Jira lives only in the Atlassian integration).

---

## Step 3: Generate Section 2 — Health at a Glance

Using the Health V2 CSV row:

**Stat cards**: health_score + health_band, classification. Do NOT include growth_score or growth_band.

**Dimension breakdown**: For each of the 5 dimensions, write a plain-English "Why" based on:
- The score value and its band
- The client's bundle (determines what Value Delivery measures)
- Known thresholds from Health V2 README §4
- Any context from the external report (e.g., stale config data, peer comparison)

**Dimension "Why" generation rules**:
- **Engagement**: Interpret in terms of login frequency and active user ratio. Reference peer comparison if available.
- **Adoption**: State how many features are used vs available for their bundle. Reference the feature catalog in Health V2 README §4.2.
- **Value Delivery**: MUST be bundle-specific. See the bundle formula table in DESIGN.md.
- **Operational Health**: Reference import success, catalog completeness, and data freshness. If the score is low, identify which sub-component is likely dragging it down.
- **Trajectory**: Describe as Q/Q trend. Positive = accelerating, flat = stable, negative = declining.

**Growth components**: OMIT. Do not include growth_score, growth_band, or the Growth Components section (bundle_upgrade_signal, feature_gap_score, customer_headroom_score, peer_benchmark_gap). Classification is retained as it describes the action mode.

**Flags**: List any active flags (churn_risk, risk_modifier_applied, warning flags: hs_lifecycle_stale, hs_join_missing, arr_data_gap). If none, write "No flags." Do not include expansion_ready (growth-related).

**Model explainer**: Include the collapsible explainer box with bundle-specific Value Delivery description.

---

## Step 4: Generate Section 3 — Support & Issue Themes

Using HelpScout query results:

**Summary one-liner**: Synthesize from Q-IB-HELP-AGG.
Pattern: "{total} conversations in 90 days. {tenor}. {fire status}."

- Tenor is derived from dominant type tag and escalation profile
- Fire status: "No active fires" if no S1/S2 open tickets; otherwise flag the fire

**Theme analysis**: From Q-IB-HELP-THEMES, identify the top 2-3 type tags by conversation count. For each theme:
1. Name it concisely
2. List 2-3 supporting ticket subjects from Q-IB-HELP-DETAIL
3. Assess impact (what does this pattern mean?)
4. Identify root driver (why does this keep happening?)
5. Suggest an action (what should we do?)

**Escalation profile**: One-liner from escalation level distribution.

**Open tickets**: From Q-IB-HELP-AGING, list each open ticket with:
- Subject, days open, severity (from tags), level (from tags)
- Conversation state: attempt to classify, default to UNKNOWN if thread data unavailable
- Action flag: RED if > 14 days open, YELLOW if > 7 days open

**Cross-link**: If any conversation has `status: logged on jira` tag, note it and connect to Section 4.

---

## Step 5: Generate Section 4 — Active Engineering & Projects

Using Jira query results:

**Ticket table**: List open tickets with key, summary, project, status, priority, assignee, age, days since update.

**Flags**:
- Flag stale tickets (no update in 14+ days)
- Flag high-priority tickets (P1/P2, Critical/High)
- Flag blocked tickets

**Cross-surface links**:
- Match Jira tickets to support themes by keyword/topic similarity
- Connect to HelpScout tickets tagged `status: logged on jira`

If no Jira data: "No active Jira tickets found for this client. Search strategies attempted: [list JQL queries used]."

---

## Step 6: Generate Section 5 — Meeting Playbook

**Cross-surface connections** (2-4 bullets):
Read the external report output (if available in the run directory) and connect its findings to:
- Health dimension scores ("External report highlights X — internally, dimension Y is at Z")
- Support themes ("Support theme of [training/config/integration] aligns with external report finding on [topic]")
- Jira work ("Jira ticket [KEY] addresses [external report finding or support theme]")

If external report is not available, generate connections from health data and support data only.

**Not in the external report**:
- Health score and classification (always internal-only)
- Churn risk assessment
- Expansion readiness and type
- Support history and patterns
- Data quality warnings (hs_lifecycle_stale, etc.)

**SuperCat action items** — check each:
- [ ] `has_clicky_portal = false`? → "Enable Clicky Analytics for portal traffic intelligence"
- [ ] Operational Health < 70 due to data freshness? → "Refresh stale configuration data"
- [ ] Open support tickets aging > 7 days? → "Resolve open tickets before meeting"
- [ ] Jira tickets stale > 14 days? → "Update or close stale client tickets"

---

## Step 7: Generate Section 1 — Account Verdict (WRITE LAST)

This is the executive summary. Write it AFTER all other sections are complete.

**Verdict paragraph**: 2-3 sentences that answer:
1. Is this account healthy or in trouble?
2. What's the overall tenor? (stable, growing, declining, at risk)
3. What should the meeting be about? (offense/optimization vs defense/firefighting)

**Three Things That Matter**: Select the 3 most important facts by priority:
1. Any active fire (churn risk, high-severity open ticket, critical Jira issue, risk modifier)
2. The biggest opportunity or talking point from the external report
3. The most significant support theme or pattern
4. Anything the team needs to be aware of that isn't in the external report

Each item: bold title (< 10 words) + 1-2 sentence body.

**Tone**: Zero spin. Honest. Decision-grade. If the account is healthy and boring, say so. If there's a fire, lead with it.

---

## Step 8: Save Markdown File

Save the brief to:
```
Insightful Product 2.0/runs/{shortname}_{date}/output/{shortname}_{date}_internal_brief.md
```

If the run directory doesn't exist yet (external report not generated), create the directory.

---

## Step 9: Generate HTML Version

Convert the markdown brief into a styled HTML document for team hosting.

**Template**: Read `operators/internal/internal-brief/TEMPLATE.html` — this is the authoritative HTML structure with all CSS, component patterns, and placeholder tokens.

**Design system notes** (what makes the internal brief visually distinct from the external report):
- **Accent color is blue-steel** (`--accent: #4A6A8C`) instead of the external report's warm copper (`--accent: #C47A4A`). This prevents mix-ups.
- **Red "INTERNAL USE ONLY" banner** in the header
- **Dashed-border "Not in the External Report" box** with muted background
- **Clickable action item checkboxes** in the Meeting Playbook

**Section → HTML component mapping**:

| Brief Section | HTML Components |
|---|---|
| Account Verdict | `.verdict` block + `.highlights` numbered list |
| Health at a Glance | `.metrics` grid (stat cards) + `table` (dimensions) + `details` (model explainer) |
| Support & Issue Themes | `.theme-card` cards + `table` (open tickets) + `.callout` boxes |
| Active Engineering & Projects | `table` (recent) + `details` (backlog, collapsible) + `.callout.insight` (cross-links) |
| Meeting Playbook | `.highlights` (talking points) + `.internal-only` (not in report) + `.action-list` (action items) |

**Badge class mapping**:
- Health band Thriving/Healthy → `.badge.ok`
- Health band Watch → `.badge.warn`
- Health band At Risk/Critical → `.badge.danger`
- Jira status Approved/In Progress → `.badge.info` or `.badge.warn`
- Jira status To Do/Triaging → `.badge.muted`
- Priority High/Highest → `.badge.danger`
- Open ticket > 14 days → `tr.row-danger` + `.badge.danger`
- Open ticket > 7 days → `tr.row-warn` + `.badge.warn`

**Process**: Replace all `{{PLACEHOLDER}}` tokens in the template with the data from the markdown brief. Use proper HTML entities (`&amp;`, `&mdash;`, `&rsquo;`, `&times;`, etc.). Link Jira tickets with `class="jira-link"`.

Save to:
```
Insightful Product 2.0/runs/{shortname}_{date}/output/{shortname}_{date}_internal_brief.html
```

**Dual-save**: Also copy the HTML file to the hosted-internal directory for team viewing:
```
Insightful Product 2.0/hosted-internal/{shortname}_{date}_internal_brief.html
```

---

## Step 10: Validation Report (Optional — enable for QA runs)

Generate a structured validation report that audits the brief for accuracy. Save alongside the brief outputs.

**When to run**: Include this step when the user specifies `--validate` or during initial QA batches. Skip for production runs once validation is proven clean.

**Validation checks**:

### V1: Health Data Integrity
- [ ] Re-read the Health V2 CSV row for this client
- [ ] Confirm health_score in brief matches CSV exactly
- [ ] Confirm each dimension score (Engagement, Adoption, Value Delivery, Operational Health, Trajectory) matches CSV
- [ ] Confirm classification matches CSV
- [ ] Confirm health_band matches CSV
- [ ] Confirm flags (churn_risk, expansion_ready, risk_modifier) match CSV

### V2: Support Data Integrity
- [ ] Re-run Q-IB-HELP-AGG (the aggregate count query) and confirm the total conversation count in the summary one-liner matches
- [ ] Confirm the number of open tickets in the table matches Q-IB-HELP-AGING result count
- [ ] Confirm theme ticket counts sum to ≤ total (themes can overlap, but no theme count should exceed total)
- [ ] Confirm escalation profile numbers are consistent with Q-IB-HELP-DETAIL tag data

### V3: Jira Data Integrity
- [ ] Confirm every Jira key in the brief exists and links to the correct URL (`https://supercatsolutions.atlassian.net/browse/{KEY}`)
- [ ] Confirm ticket summaries match what Jira returned
- [ ] Confirm status and priority labels match Jira data

### V4: Cross-Contamination Check
- [ ] Search the entire brief text for any org_shortname or org_name that is NOT this client — flag if found
- [ ] Confirm the header, footer, and file names all reference the correct client

### V5: Internal Consistency
- [ ] Verdict references data that appears in Sections 2-5 (no phantom claims)
- [ ] "Three Things That Matter" items each trace to a specific section finding
- [ ] "Not in the External Report" items are genuinely absent from the external report (spot-check if external report exists in run directory)
- [ ] SuperCat Action Items are supported by findings in the brief (e.g., "resolve open tickets" → open tickets actually exist)

### V6: HTML Parity
- [ ] Confirm the HTML file exists alongside the markdown
- [ ] Spot-check 3 data points across both formats match (health score, open ticket count, Jira ticket count)
- [ ] Confirm the HTML header shows the correct client name, date, and bundle

**Output format**: Save as a markdown checklist with PASS/FAIL per check and notes on any failures:

```
Insightful Product 2.0/runs/{shortname}_{date}/output/{shortname}_{date}_validation.md
```

**Validation report template**:
```markdown
# Validation Report — {Client Name}
*{date} · Internal Brief QA*

## Summary
- **Overall**: PASS / FAIL
- **Checks run**: X / 20+
- **Failures**: {count}

## V1: Health Data Integrity
- [x] health_score: CSV={X}, Brief={X} ✓
- [x] engagement_score: CSV={X}, Brief={X} ✓
...

## V2: Support Data Integrity
...

## V3: Jira Data Integrity
...

## V4: Cross-Contamination Check
...

## V5: Internal Consistency
...

## V6: HTML Parity
...

## Notes
{Any observations, edge cases, or recommendations}
```

---

## Degradation Rules

The brief can be generated with partial data. Degradation levels:

| Missing Source | Impact | Action |
|---------------|--------|--------|
| Health V2 CSV | **BLOCKED** | Cannot generate brief. Stop. |
| HelpScout (no domain map) | Degraded | Omit Section 3. Note in Verdict. |
| HelpScout (BigQuery down) | Degraded | Omit Section 3. Note in Verdict. |
| Jira (MCP unavailable) | Degraded | Omit Section 4. Note in Verdict. Use HelpScout `status: logged on jira` tags as fallback signal. |
| org_summary (BigQuery down) | Minor | Use Health V2 CSV for org_name. Default `has_clicky_portal` to unknown. |
| MAL CSV (unavailable) | Minor | Omit cohort_year. |
| External report (not generated) | Minor | Meeting Playbook uses health + support data only. |
