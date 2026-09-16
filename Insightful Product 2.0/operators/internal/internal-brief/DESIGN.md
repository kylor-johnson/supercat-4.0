# Internal Intelligence Brief — Design Specification

Version: 1.0
Date: 2026-04-20

## Purpose

A lightweight CS operating doc that gives the internal team proper context before a meeting where we show the client their external Customer Intelligence Report.

**Audience**: CEO, CTO, CS team — walking into a client meeting with 5 minutes to prepare.

**This is NOT**:
- A client-facing document (the external report handles that)
- A 10-section deep-dive (it's 1-2 pages, scannable)
- A data dump (it's synthesized — themes, verdicts, connections)

**This IS**:
- An honest account verdict with 3 things that matter
- A plain-English health explainer (for readers who don't know how health is calculated)
- A pattern-based support read (themes, not ticket lists)
- A meeting playbook that connects internal data to what the client will see

---

## Authority Hierarchy

| # | Source | Role |
|---|--------|------|
| 1 | `Health V2/README.md` | Health/Growth scoring specification — all score interpretations flow from here |
| 2 | `Health V2/runs/{latest}/client_health_scores_{date}.csv` | Scored output — single source of truth for all health metrics |
| 3 | `Insightful Product 2.0/SKILL.md` | Data source schemas, semantic guardrails |
| 4 | This file (`DESIGN.md`) | Brief structure, section specs, rendering rules |
| 5 | `QUERIES.md` (sibling file) | All SQL/MCP queries needed to populate the brief |

If a query interpretation or section content conflicts with the Health V2 README, the README wins.

---

## Data Sources

| Source | System | Connection | What It Provides |
|--------|--------|------------|------------------|
| Health V2 CSV | Local file | Filesystem read | Health score, growth score, 5 dimensions, classification, risk modifiers, flags, score_explanation |
| HelpScout | BigQuery | MCP `user-bigquery-admin` → `query` | Support conversations, tags (escalation/severity/type/product/status), conversation age |
| Jira | Atlassian | MCP `plugin-atlassian-atlassian` → `searchJiraIssuesUsingJql` | Active engineering/support tickets for the client |
| org_summary | BigQuery | MCP `user-bigquery-admin` → `query` | Org identity, config flags (`has_clicky_portal`), display name |
| Domain map | Postgres cache | `pg_cache/pg_domain_map.csv` | Email domain → org_shortname mapping for HelpScout attribution |
| MAL CSV | Local file | Filesystem read | `cohort_year`, `mrr`, `arr` (authoritative for ARR) |

---

## Section Specification

The brief has 5 sections. Total target length: 1-2 pages (markdown). Every section is designed to be skippable — the Verdict carries enough context to walk into a meeting cold.

---

### Section 1: Account Verdict

**Position**: Top of the brief. This is what you read if you have 15 seconds.

**Contains**:
- **One-paragraph honest assessment** — plain English, no jargon. Covers: is this account healthy or in trouble? What's the overall tenor? What should the meeting be about (offense vs defense)?
- **Three Things That Matter** — 3 items, each with a short `title` (bold, < 10 words) and a `body` (1-2 sentences). These are the three most important things to know walking into the meeting. They should span the data sources — not three health facts or three support facts, but a cross-surface synthesis.

**Data sources**: All — this section synthesizes Health V2 + HelpScout + Jira + external report awareness.

**Generation logic**: The operator reads all downstream sections first, then writes the Verdict last (like an executive summary). The three things should be selected by impact priority:
1. Any active fire (churn risk, high-severity open ticket, critical Jira issue)
2. The biggest opportunity or talking point from the external report
3. Anything the team needs to be aware of that isn't in the external report

**Tone**: Borrowed from the CEO system — zero spin, honest assessment, decision-grade. Example:

> Currey & Company is a healthy, stable account in standard-cadence mode. Platform deeply adopted, engagement is 2× peer median. No fires. The meeting should focus on two optimization opportunities — the rep presentation gap ($230K potential) and the 240-day stale config data that's dragging Operational Health.

**Format**: Markdown. Verdict paragraph followed by a numbered list of three items with bold titles.

---

### Section 2: Health at a Glance

**Position**: After the Verdict. This section answers: "What do the numbers say and what do they mean?"

**Contains three layers** (each layer is scannable independently):

#### Layer 1: Stat Cards
Two key metrics displayed as compact cards:

| Card | Value | Detail |
|------|-------|--------|
| Health Score | `{health_score}` / 100 | `{health_band}` band |
| Classification | `{classification}` | Action mode |

Growth Score and Growth Band are **omitted** from the brief.

Plus the one-line `score_explanation` from Health V2, **adapted** to remove growth references (e.g., "76 Health / 50 Growth → Maintain" becomes "76 Health → Maintain").

#### Layer 2: Dimension Breakdown

A table with one row per health dimension. The "Why" column is the key value-add — it translates the raw score into plain English specific to this client's bundle and data.

| Dimension | Score | Band | Why |
|-----------|-------|------|-----|
| Engagement (25%) | X | color | Plain English: what the login/active-user data says |
| Adoption (20%) | X | color | Plain English: how many features they're using out of how many apply |
| Value Delivery (30%) | X | color | Plain English: bundle-specific — what value metric drives this score |
| Operational Health (15%) | X | color | Plain English: import health, catalog completeness, data freshness |
| Trajectory (10%) | X | color | Plain English: Q/Q trend direction and magnitude |

**Color logic** (for rendering):
- Green (Thriving/Healthy): score >= 60
- Yellow (Watch): score 40-59
- Red (At Risk/Critical): score < 40

**Bundle-specific Value Delivery explanation**:
The "Why" for Value Delivery must be tailored to the client's bundle because the formula differs:

| Bundle | VD Formula | What to Explain |
|--------|-----------|-----------------|
| iPad-only | presentation_score | Presentation tool usage (email, PDF, sharing) |
| iPad+Catalog | presentation_score | Same as iPad-only |
| iPad+Catalog+Cart | (order_volume + customer_activation + eol_share) / 3 | Order volume, buyer activation rate, online vs iPad mix |
| iPad+Catalog+Portal | (presentation + portal_engagement) / 2 | Presentation tools + Sales Portal usage |
| Full | (order_volume + customer_activation + eol_share + portal_engagement) / 4 | All four components |

#### Layer 3: Flags

Growth Components are **omitted** from the brief (bundle_upgrade_signal, feature_gap_score, customer_headroom_score, peer_benchmark_gap).

**Flags check** — one-line each, only if relevant:
- Risk modifier fired? Which one, what severity?
- Churn risk? Severity level?
- Warning flags: `hs_lifecycle_stale`, `hs_join_missing`, `arr_data_gap`

#### Model Explainer Box (collapsible)

For readers who don't know how health is calculated (CEO, CTO). Include once per brief:

> **How Health Scoring Works**: The health score (0-100) combines five dimensions weighted by importance. For {client}'s bundle ({bundle}), the formula is:
> - Engagement (25%) — Are users logging in and actively using the platform?
> - Adoption (20%) — How many available features are being used above minimum thresholds?
> - Value Delivery (30%) — Is the platform generating business value? For {bundle} bundles, this measures {bundle-specific metric description}.
> - Operational Health (15%) — Is client data clean and current? Import success, catalog completeness, data freshness.
> - Trajectory (10%) — Is activity trending up, flat, or down vs. last quarter?
>
> **Classification** determines the recommended action cadence:
> - **Expand** — healthy account with strong expansion signals
> - **Maintain** — healthy, protect with standard cadence
> - **Stabilize First** — needs health improvement before expansion
> - **Intervene** — immediate save/recovery plan needed

---

### Section 3: Support & Issue Themes

**Position**: After Health. This section answers: "What's the support story with this account?"

**Design principle**: Themes, not ticket lists. Pattern recognition, not inventory. Borrowed from the CEO system's Support Reality "Top 5 Inbox Themes" structure, condensed for per-client scope.

**Contains**:

#### Summary One-Liner
A single sentence that gives the support tenor:
> "{N} conversations in {window}. {tenor description}. {fire status}."

Example: "5 conversations in 90 days. Training-forward, low volume. No active fires."

#### Theme Analysis

Group conversations by `type:` tag to identify recurring patterns. For each theme (max 3):

| Field | Content |
|-------|---------|
| **Theme name** | Concise label (e.g., "Training & admin workflows") |
| **Ticket count** | How many conversations fall under this theme |
| **Supporting tickets** | 2-3 ticket subjects as evidence |
| **Impact** | What this pattern means for the account relationship |
| **Root driver** | Why this keeps happening |
| **Suggested action** | What to do about it (for the meeting or internally) |

#### Escalation Profile
One-line summary: L1/L2/L3/L4 distribution + highest severity encountered.
Example: "6 L1, 1 L2, 2 L3. Peak severity: S3 (Amex payment gateway). No L4 executive escalations."

#### Open & Aging Tickets

Table of currently open tickets:

| Subject | Days Open | Severity | Level | Conversation State | Action Needed? |
|---------|-----------|----------|-------|--------------------|----------------|

**Conversation state**: Attempt to classify based on available data:
- **AGENT_WAITING** — last activity was customer message; we need to respond
- **CUSTOMER_WAITING** — last activity was agent message; ball in their court
- **UNKNOWN** — cannot determine from BigQuery (thread data unavailable)

Flag any ticket open > 7 days. Red-flag any ticket open > 14 days.

**Cross-link**: If any ticket has the tag `status: logged on jira`, note it and connect to Section 4.

#### Time Window
Default: 90 days (matches Health V2 scoring period). Show 180-day context if the 90-day view is sparse (< 3 conversations).

---

### Section 4: Active Engineering & Projects

**Position**: After Support. This section answers: "Is there any engineering work in flight for this client?"

**Data source**: Jira MCP (`searchJiraIssuesUsingJql`).

**Contains**:

#### Active Tickets Table

| Key | Summary | Project | Status | Priority | Assignee | Age (days) | Days Since Update |
|-----|---------|---------|--------|----------|----------|------------|-------------------|

#### Flags
- **Stale**: Any ticket with no update in 14+ days
- **Blocked**: Any ticket in a blocked status
- **High priority**: Any P1/P2 or Critical/High priority ticket

#### Cross-Surface Links
- Connect Jira tickets to support themes (does any Jira work address a recurring support pattern?)
- Connect to HelpScout tickets tagged `status: logged on jira`

#### When Jira Data Is Unavailable
If the Jira MCP is inaccessible or returns no results:
- Check HelpScout for `status: logged on jira` tags and surface those connections
- Note: "No Jira tickets found for this client. Verify: [search strategy used]."

**JQL Strategy**: Search for the client by name and shortname. Try multiple approaches:
1. `text ~ "{client_name}" ORDER BY created DESC`
2. `text ~ "{shortname}" ORDER BY created DESC`
3. If a client-specific project exists: `project = "{project_key}" ORDER BY created DESC`

Open question: How Jira tickets are tagged by client is not yet confirmed. The operator should try multiple search strategies and document which one works.

---

### Section 5: Meeting Playbook

**Position**: Last section. This is the "so what" — connecting everything for the meeting.

**Contains**:

#### Cross-Surface Connections (2-4 bullets)
Each bullet connects two or more data sources to create an insight the meeting team should have:

Pattern: "[External report finding] — internally, [health/support/jira context], so [implication for meeting]."

Examples:
- "External report highlights $185K in dormant account value — internally, their Value Delivery score is 80 (Healthy) but Customer Headroom is N/A for their bundle, so the dormant reactivation push is pure upside with no health risk."
- "External report flags 240-day stale config data — internally, this drags Operational Health to 64. This is a SuperCat action item; prepare to explain what a config refresh involves."

#### What's NOT in the External Report
Things the team should know that the client won't see:
- Health score and classification (internal only per semantic guardrails)
- Churn risk assessment (if any)
- Expansion readiness and type
- Support history and patterns
- Any data quality gaps (missing data flags, scoring status)

#### SuperCat Action Items
Things on our side to do before/after the meeting:
- Clicky enablement (if `has_clicky_portal = false`)
- Configuration data refresh (if Operational Health is low due to data freshness)
- Open support ticket resolution (if any tickets are aging)
- Jira ticket follow-up (if any client-related tickets are stale)

---

## Output Format

### File Naming
```
Insightful Product 2.0/runs/{shortname}_{date}/output/{shortname}_{date}_internal_brief.md
```

Saved alongside the external report in the same run directory.

### Markdown Structure

```markdown
# Internal Intelligence Brief — {Client Name}

*{date} · Prepared for client meeting · INTERNAL USE ONLY*

---

## Account Verdict

{verdict paragraph}

**Three Things That Matter:**

1. **{title}** — {body}
2. **{title}** — {body}
3. **{title}** — {body}

---

## Health at a Glance

| | Health | Classification |
|---|---|---|
| **Score** | {health_score}/100 | {classification} |
| **Band** | {health_band} | |

> {score_explanation}

### Dimensions

| Dimension | Score | Status | Why |
|---|---|---|---|
| Engagement (25%) | {score} | {color} | {explanation} |
| ... | ... | ... | ... |

### Flags
- {flag items, if any — otherwise "No flags."}

<details>
<summary>How Health Scoring Works</summary>

{model explainer text, bundle-specific}

</details>

---

## Support & Issue Themes

> {summary one-liner}

### Themes

**1. {Theme name}** ({N} tickets)
- {Supporting ticket subjects}
- **Impact**: {impact}
- **Root**: {root driver}
- **Action**: {suggested action}

### Escalation Profile
{one-liner}

### Open Tickets ({count})

| Subject | Days Open | Severity | Level | State | Action? |
|---|---|---|---|---|---|

---

## Active Engineering & Projects

| Key | Summary | Status | Priority | Age | Last Update |
|---|---|---|---|---|---|

{flags and cross-links}

---

## Meeting Playbook

### Talking Points
1. {cross-surface connection}
2. {cross-surface connection}
3. {cross-surface connection}

### Not in the External Report
- {item}
- {item}

### SuperCat Action Items
- [ ] {action item}
- [ ] {action item}
```

---

## Generation Sequence

The operator generates the brief in this order:

1. **Resolve client identity** — org_shortname, org_name from Health V2 CSV or org_summary
2. **Load Health V2 data** — read the CSV row for this client
3. **Load org_summary** — config flags, display name
4. **Resolve email domains** — from `pg_domain_map.csv` or Postgres query
5. **Query HelpScout** — support conversations + tag analysis + aging
6. **Query Jira** — active tickets for this client
7. **Read external report awareness** — if the external report has been generated for this run, scan it for key findings to reference in Meeting Playbook
8. **Generate Sections 2-5** — Health, Support, Jira, Playbook
9. **Generate Section 1 (Verdict)** — written LAST, synthesizing all other sections

---

## Open Questions

### Confirmed
1. **HelpScout attribution works** via email domain matching. CCI = `curreyco.com`. Coverage is ~95% of eligible entities per the domain map.
2. **Tag vocabulary is well-structured** — 4 escalation levels (L1-L4), 4 severity levels (S1-S4), 8+ type tags, 5 product tags, 7 status tags. Theme analysis is viable.
3. **Health V2 CSV has all needed columns** — every dimension score, growth components, risk modifiers, flags, and score_explanation.

### Unresolved
1. **Jira ticket attribution**: How are client tickets identified in Jira? Possible strategies: client name in summary, label/tag, custom field, client-specific project. Needs manual verification with the Jira MCP in Agent mode.
2. **Conversation state from BigQuery**: The `helpscout.conversations` table does not include thread-level data. Determining AGENT_WAITING vs CUSTOMER_WAITING requires either (a) the native `helpscout.conversation_threads` table (~39k rows; thread-level messages, join on conversation `id`), or (b) accepting UNKNOWN state. The operator should attempt the threads table first and fall back gracefully. (The old Weld `helpscout__help_scout_tickets` denormalized table is retired with the vpn/Weld layer.)
3. **Cohort year**: Available in the MAL CSV but not in the Health V2 output CSV. The operator needs to read the MAL CSV separately to get this field.
4. **External report awareness**: The Meeting Playbook is most useful when it references specific findings from the external report. This creates a dependency — either generate the external report first, or have the brief operator independently query the same data and infer what the external report would highlight.
