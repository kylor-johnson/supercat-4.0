---
name: supercat-data-routing
description: >
  Use for ANY question about a SuperCat org, account, or customer — including
  "does org shortname X have Y enabled", eOL / eCat Online / sales portal / iPad access,
  user groups, price levels, imports, inventory, adoption, health, support history, or
  billing. Routes each question to the correct data source, and enforces identity + source
  checks before answering or drafting. Consult BEFORE any query or any customer-facing draft.
---

# SuperCat Data Routing

Decide **which data source owns a question** before you query, and enforce two hard
preconditions before you answer or draft anything about a person. This skill exists because
data lives across several sources and Claude has previously (a) declared a domain
"unavailable" after only searching the MCP registry — while the answer sat in a BigQuery
dataset that was loaded the whole time — and (b) nearly sent an internal-voice memo addressed
TO a customer. Both are routing/identity failures this skill prevents.

## When to use

Consult this skill FIRST for:

- Any question naming an org **shortname** (e.g. `libco`, `mali`) or a customer/account.
- Any "does org X have Y enabled?" question (eOL, eCat Online, sales portal, iPad, a feature,
  a user group, a price level).
- Anything about imports, inventory, products, users, groups, sites, adoption, usage, health,
  support history, deals, lifecycle, billing, or subscriptions.
- **Before any customer-facing draft** (email, memo, reply, summary sent to or about a named
  person).

If the question touches a SuperCat org/account/customer at all, route it here first.

---

## 1) Routing table (authoritative — hardcoded)

Do **NOT** regenerate this table from a live scan. BigQuery contains junk/test datasets that
would pollute routing. Use exactly this mapping:

| Question domain | Data source | Location |
|---|---|---|
| Org config, users, groups, sites, products, imports, inventory | **supercat-postgres-vpn** | Postgres (VPN) |
| Support tickets & customer conversations | **bigquery-admin** | `helpscout.conversations` / `helpscout.conversation_threads` |
| eOL / portal web analytics | **bigquery-admin** | `google_analytics_ecat_online` |
| iPad app analytics | **bigquery-admin** | `google_analytics_ecat` |
| Deals, lifecycle, CSM ownership | **bigquery-admin** | `hubspot` / `hubspot_views` |
| Billing & subscriptions | **bigquery-admin** | `stripe` |
| Health scoring / onboarding state | **bigquery-admin** | `scorecard`, `onboarding_assessment` |
| Meeting recordings & transcripts | **Fathom** (if available), else **bigquery** | Fathom MCP, else BigQuery Fathom |

**NEVER use `supercat-cs-tools` — it is retired. Do not reference it, query it, or suggest it.**

Notes on "enabled?" questions:
- Whether a feature/module (eOL, portal, iPad) is **enabled/provisioned** is org **config** →
  start in **supercat-postgres-vpn**.
- Whether it is **used** (traffic, adoption) → the matching **analytics** dataset in
  bigquery-admin (`google_analytics_ecat_online` for eOL/portal, `google_analytics_ecat` for
  iPad).
- A complete "do they have eOL?" answer often needs BOTH: config (provisioned) + analytics
  (actually used) + support history for context.

---

## 2) Two HARD preconditions (must-do rules, not tips)

### Precondition A — Negative results don't prove absence

Before concluding that a data source or domain is **unavailable**, you **MUST** list the
BigQuery datasets via **bigquery-admin (`list_datasets`)** and check there. An MCP registry
search returning nothing does **NOT** mean the domain is missing.

- Do not say "HelpScout isn't available" (or any domain) based on a registry/tool search alone.
- Concrete failure this prevents: a prior session concluded a source was unavailable without
  checking BigQuery — it searched the MCP registry, got nothing, and declared the domain
  missing while the dataset was loaded in `bigquery-admin` the whole time. The correct move
  was `list_datasets` on bigquery-admin.
- Rule: **registry silence → run `list_datasets` → then decide.** Only conclude "unavailable"
  after the dataset list confirms it.

### Precondition B — Resolve identity before drafting

Any **named person** must be looked up to determine whether they are a **CUSTOMER** or
**internal/SuperCat staff** BEFORE you write anything to or about them.

Look them up in:
- **Postgres (supercat-postgres-vpn):** `org_users` / `users`
- **BigQuery (bigquery-admin):** `helpscout.customers`

Rules:
- **Never draft internal-voice text addressed to a customer.** Internal-voice memos are for
  SuperCat staff; customer-facing text is a different voice and audience.
- Do not characterize a person's portal/product usage without checking the relevant analytics
  or config source first — do not guess or infer usage from support tickets alone.
- Concrete failure this prevents: a prior session drafted about a named person without first
  confirming whether they were a customer or internal staff — nearly sending internal-voice
  text addressed TO a customer and mischaracterizing their portal usage. Identity + source
  lookup would have caught both.

If identity cannot be resolved, **stop and ask** rather than drafting.

---

## 3) Known-junk note (so schema discovery isn't fooled)

When exploring BigQuery schemas, ignore these known artifacts in the `helpscout` dataset:

- **Facebook Ads tables** are mixed in — not HelpScout support data.
- **`test20260311*`** leftover tables — test data, not real conversations.
- **Zero-row tables:** `helpscout.teams`, `helpscout.team_members`,
  `helpscout.inbox_custom_fields` — empty; do not treat their emptiness as "no data."

Real support volume lives in `helpscout.conversations` and `helpscout.conversation_threads`.

---

## After the data answer — who owns the follow-up

This skill tells you whether something is **provisioned or used** — it names no skill for
the next step. Once the data question is answered, route the follow-up work:

| Follow-up need | Route to |
|---|---|
| eOL config, Cart, enrollment, My Account pricing | `ecat-online` |
| Sales Portal build / ERP order-invoice reporting | `ecat-sales-portal-onboarding` |
| iPad runtime behavior and rep-facing diagnosis | `ecat-ipad-app` |
| iPad file builds and imports | `ecat-core-files`, `ecat-customers-build`, `ecat-pricing-levels`, `ecat-options-and-mapping`, `ecat-images-ftp` |
| a reactive ticket or client email | `ecat-support-triage` |
| live DB state by shortname | `ecat-postgres-audit` |

---

## Quick procedure

1. Identify the question domain → pick the source from the **routing table**.
2. If a named person is involved or you might draft → run **Precondition B** (identity lookup)
   first.
3. If a tool/registry search comes up empty → run **Precondition A** (`list_datasets` on
   bigquery-admin) before concluding anything is missing.
4. Query the correct source; ignore known-junk tables during schema discovery.
5. Before answering or drafting, hand off to **`truth-discipline`** — it governs what
   the result is allowed to claim: confidence and completeness tiers, capture vs.
   attribution, invoiced-ERP truth vs. app-order intent, billed ≠ collected, and
   suppress-rather-than-guess. This skill routes you to the right source; it does not
   license the number you found. Then answer — or draft in the correct voice for the
   resolved audience — and route the follow-up work per the "After the data answer"
   section.
