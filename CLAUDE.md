# CLAUDE.md — ported from Cursor alwaysApply rules
# Generated: 2026-07-16T14:59:41.788574+00:00

<!-- from craftcms-graphql.mdc -->
# CraftCMS GraphQL Best Practices

**CRITICAL**: When working with CraftCMS GraphQL, NEVER introspect the full schema - it causes timeouts and context overflow.

## ❌ NEVER DO THIS

```graphql
# This will timeout and overflow context
{
  __schema {
    types {
      name
      fields {
        name
      }
    }
  }
}
```

## ✅ ALWAYS USE TARGETED INTROSPECTION

### 1. Test Connection First

```graphql
{
  ping
}
```

### 2. Introspect ONE Type at a Time

```graphql
{
  __type(name: "knowledgeBase_knowledgeBase_Entry") {
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

### 3. List Mutation Names Only

```graphql
{
  __type(name: "Mutation") {
    fields {
      name
    }
  }
}
```

### 4. Sample Real Entries to Discover Structure

```graphql
{
  entries(section: "knowledgeBase", limit: 1) {
    id
    title
    ... on knowledgeBase_knowledgeBase_Entry {
      articleSections {
        __typename
        ... on text_Entry {
          id
          body
        }
      }
    }
  }
}
```

## Key Principles

- **Query ONE type at a time** using `__type(name: "TypeName")`
- **Never request all fields from all types**
- **Use inline fragments** for union types
- **Request only fields you actually need**
- **Test incrementally** - start small, expand as needed

---

<!-- from ecat-data-model.mdc -->
# eCat Data Model Reference

## Admin Console Navigation

- **Products:** `Products > Products` (view only - cannot edit individual items in Admin Console)
- **Customers:** `Customers > Customers` (can edit directly in Admin Console OR via CSV import)
- **Inventory:** `Tools > Import Data > Inventory` (upload only, no manual editing)
  - Custom inventory fields can be configured (Qty On Hand, Next Ship Date, Next Available Qty)

## File Distinctions

### LongDesc vs ShortDesc vs ProductStory (IMPORTANT)
- **LongDesc** (in products.csv) = Primary product name shown in eCat catalog, detail views, and orders
- **ShortDesc** (in products.csv) = Compact product name for admin views and order forms (optional, falls back to LongDesc if blank)
- **ProductStory** (in stories.csv) = Extended marketing description / product romance copy
- These are THREE DIFFERENT fields across TWO DIFFERENT files

### Order/Invoice Files (IMPORTANT)
- **order_data.csv** = Imported order history for Portal reporting (from ERP/accounting)
- **invoice_data.csv** = Imported invoice history for Portal reporting (from ERP)
- These are IMPORT files for Sales Portal reporting, NOT iPad-submitted orders
- eCat can also EXPORT orders.csv/invoices.csv - that's different from these imports

### Options Files
- **options.csv** = Individual option values (e.g., 100=Black, 101=White)
- **option_groups.csv** = Groups containing option codes (e.g., FIN=Finishes contains 100,101,102)
- Products reference groups via OptionSet1..OptionSet**20** fields (verified 2026-09-05:
  fleet max is 20; **30 orgs use more than 5**, with 37,803 references above OptionSet5).
  This doc previously said 5 — a mapper written to that limit silently drops sets 6+
- Matrixed options use matrix_options.csv for combination pricing

## Key Links
- **BaseItemCode** = Master key linking products to inventory, stories, orders, options
- **TerritoryCodes** = Links customers to sales reps (KB says required; importer does NOT make it fatal — see `ecat-ground-truth`)
- **DefaultPriceCode** = Links customers to pricing levels (truly required by importer; must match an Admin price level code)

## Customer File Required Fields (importer-fatal)
- BillToCode, BillToName, BillToAddress1, BillToCity, BillToState, BillToPostCode, DefaultPriceCode
- ShipToAddress1, ShipToCity (required on ship-to rows)
- TerritoryCodes is KB-required but NOT importer-fatal (see `ecat-ground-truth`)

## Inventory File Required Fields
- **BaseItemCode** is the only importer-required field (KB lists QtyAvailable as required, but the importer does not enforce it — see `ecat-ground-truth`)
- Optional columns: QtyAvailable, QtyOnHand, QtyReserved, QtyInShowroom, QtyInTransit, QtyOnBackorder, QtyOnPOrder, QtyOverseas, NextReceiptDate (real date), NextReceiptQty, Option1-Option20, plus org-configured custom fields

## Product Importer Field Names
- CSV headers are case-insensitive (downcased before matching)
- Promotional price header: `promotionprice` (PromoPrice and PromotionPrice both work)

---

<!-- from ecat-ground-truth.mdc -->
# eCat iPad — Import Ground Truth

Scope: **eCat iPad app only** (not eCat Online/eOL or Sales Portal). When a KB
article describes per-browser "My Account" markup pricing, that is **eOL**, not
iPad — ignore it for iPad work.

## Omitted-record behavior (the #1 trap)

A "full file" replaces that file's data. What happens to records you leave OUT
differs per file — verified in `supercat_server` importer code:

| File | Omitted record |
|------|----------------|
| `products.csv` | **Soft-delete** (`deleted=true`) — only on an error-free import |
| `products_1.csv` (supplement) | No delete; updates existing by BaseItemCode |
| `stories.csv` | Sets `story=null` (does NOT delete the product) |
| `customers.csv` | **HARD-deletes ALL customers + ship-tos**, then reloads |
| `inventory.csv` | **HARD-deletes ALL inventory**, then reloads |
| `options.csv` | **HARD-deletes ALL options** + nulls group membership |
| `option_groups.csv` | **HARD-deletes ALL groups**, then reloads |
| `matrix_options.csv` / `contract_prices.csv` | **HARD-deletes ALL**, then reloads |

**Deletes only happen on a clean import.** If the file has any `Error` rows,
obsolete records are left in place (file imports the good rows but skips deletes).
Only `Warning`-only imports remove omitted records.

## Mandatory import order

`options.csv` → `option_groups.csv` → `products.csv` → `stories.csv` →
`inventory.csv` → `customers.csv`

Always re-send `option_groups.csv` after `options.csv` — importing options
**nulls group membership**.

## KB-vs-reality corrections (code-verified)

- **`TerritoryCodes`** (customers): KB marks required; importer does NOT make it
  fatal. Needed for rep↔customer filtering, not for a successful import.
- **`QtyAvailable`** (inventory): KB marks required; importer only requires
  `BaseItemCode`.
- **Option / option-group `Code`**: KB says max 8 / name 25; DB actually allows
  **15 / 50**.
- **`BaseItemCode` length**: KB/lessons say max 20, but the **20-char limit is advisory,
  not importer-fatal** — the real importer cap is **40 chars** (`Product::ATTR_LENGTHS`);
  a row whose `BaseItemCode` exceeds 40 chars gets a **validation error** and is rejected.
  So 21-char codes are fine (under 40) — verified live: org `mali` has 4 active 21-char
  codes (e.g. `LV-HS-PD20-24V-100-WW`). Keep codes short for image filenames / grid
  display, but only reject a row for length once it passes 40 chars.
- **Product images**: **6 by default, 12** only with the paid
  `enable_twelve_product_images` flag.
- **SmartList item-list**: KB says comma-separated; the app/importer expects
  **newline-separated**. Commas = one giant invalid item number.
- **Auto-Create taxonomy**: whatever string you put in `CollectionCodes`/
  `CategoryCodes`/`TradeNameCode` becomes the **iPad label** — never ship cryptic
  internal codes (`COL126`, `TN1`). **Groups never auto-create** from a product
  import; create them first.
- **Missing a standard text column** (e.g. `Materials`, `Features`) does NOT
  clear it — send the column with empty values to clear.

## iPad pricing in one line

Rep selects customer → customer `DefaultPriceCode` sets the price level → the
**User Group** controls which levels the rep can see. Hide list/net by not
authorizing `net_price` for the group.

---

<!-- from ecat-import-ops.mdc -->
# eCat iPad — Import Operations

## Where files go

| Asset | FTP folder | Admin Console tool |
|-------|------------|--------------------|
| CSV data files | `/data` | Tools → Upload Data / Import Data |
| Product images | `/images` (**flat root only — subfolders are ignored**) | Tools → Import Images → Product Photos |
| Option images | `/option_images` | Tools → Import Images → Option Photo |

- FTP processed files are **deleted on success** — not data loss.
- Product images: `.jpg` lowercase, sRGB, up to 6 (or 12), primary first, names
  match `ImageFileName` exactly (no spaces/punctuation except `-` `_`), ≤15 MB,
  ≤500/batch, **30–45 min** processing.
- Option images: square **300×300**, default filename `{code}.jpg`.

## Verify every import

Tools → Admin Reports → **File Import Status**. If the timestamp is a **blue
link**, there were problems — click it for line numbers.

| Tier | Effect |
|------|--------|
| **Fatal** | Whole file rejected, nothing changes |
| **Error** | File imports good rows, skips error rows, AND skips all deletes of omitted records |
| **Warning** | Imports including warning rows; omitted records ARE removed |

So if expected deletes didn't happen, look for an `Error` row.

## Multi-file product import

`products.csv` (must include `BaseItemCode`, `TradeNameCode`, `CollectionCodes`,
`CategoryCodes`) + `products_1.csv`, `products_2.csv`… + a final `sentinel.csv`
to trigger the merge. Supplemental rows keyed by `BaseItemCode`; their columns
must be valid standard or pre-registered custom fields.

## Custom fields

Must be pre-registered in Admin (Products → Custom Fields, "Send to iPad") before
import; matched case-insensitively. Same for inventory and customer custom fields.

---

<!-- from insightful-legacy-frozen.mdc -->
# Insightful Product — legacy folders frozen

These folders are **frozen**. Do not use them unless the user explicitly asks for
that specific legacy version in that conversation.

| Folder | Location |
|--------|----------|
| `Insightful Product` (original) | `iCloud Drive/Insightful Product/` (sibling to SuperCat 4.0) |
| `Insightful Product 2.0` | `SuperCat 4.0/Insightful Product 2.0/` |
| `Insightful Product 3.0` | `SuperCat 4.0/Insightful Product 3.0/` |

## Active project

**Insightful Product 4.0/** (`SuperCat 4.0/Insightful Product 4.0/`) is the
current Insightful work. Prefer files there for report pipeline, authority docs,
scripts, and operators.

## Do not (by default)

- Read, search, grep, or cite files in any frozen folder above
- Run scripts from frozen `scripts/` directories
- Follow operators or authority docs in frozen folders
- Suggest edits or improvements inside frozen folders
- Use the `insightful-report` skill (it targets 2.0) unless the user explicitly
  asks for a 2.0 report

## Allowed without explicit legacy request

- Work in **Insightful Product 4.0/** and other active project folders
- Use **copied or migrated** files the user placed outside the frozen folders

## When a legacy folder is allowed

Only when the user **clearly** directs work at a specific version, e.g.:

- "use Insightful Product 2.0" / "run 2.0 report for cci"
- "use Insightful Product 3.0"
- "read `Insightful Product/report-system/...`" (original)
- opens or @-mentions a file inside a frozen folder

If unsure whether they mean a legacy folder vs 4.0 (or a copied file elsewhere),
ask once before touching any frozen path.

---

<!-- from no-canvas.mdc -->
# No unsolicited canvases

**Do not create `.canvas.tsx` files or Cursor canvases** unless the user explicitly asks for a canvas (e.g. "make a canvas", "open this in canvas", "use a canvas for this").

## Default output format

- Put all results in **chat**: markdown, bullet lists, and fenced code blocks.
- Use **markdown tables** in chat for tabular data — do not substitute a canvas.
- Write deliverables as normal files in the repo (`.md`, `.csv`, etc.) when the user wants something saved — not as `.canvas.tsx`.

## Overrides built-in canvas guidance

Ignore any instruction to prefer canvas for analyses, charts, MCP tool results, or "data-heavy" responses. Those belong in chat unless the user asked for a canvas.

If you would create a canvas, stop and use markdown in chat instead.

## When canvas is allowed

Only if the user **explicitly** requests a canvas in that conversation.

---

<!-- from jira-read-only.mdc -->
# Jira is READ-ONLY (non-negotiable)

Jira (Atlassian MCP, `supercatsolutions.atlassian.net`, projects EBR / SERV / any)
is **read-only context only**. Use it to understand how tickets were resolved and
to ground program work — **never to change anything**.

## Never (no exceptions without an explicit per-conversation override)

- **No comments** — do not call `addCommentToJiraIssue` for any reason.
- **No creates** — no `createJiraIssue`, no `createIssueLink`, no `createCompass*`.
- **No transitions / status changes** — no `transitionJiraIssue`.
- **No field edits** — no `editJiraIssue`, no `addWorklogToJiraIssue`.
- **No "hygiene," "dedupe," "park," or "out-of-program" comments** — capture those
 in PM docs under `SuperCat 4.0/PM/`, not on the ticket.

These write like they came from Kylor's account (MCP posts as the authenticated
user). Tickets are often owned by others who won't understand agent-authored notes.

## Allowed (read-only)

- `getJiraIssue`, `searchJiraIssuesUsingJql`, `getTransitionsForJiraIssue` (read),
 `getVisibleJiraProjects`, `lookupJiraAccountId`, `get*` / `search` / `fetch`.
- Summarize ticket state, resolution, and relationships **in chat or PM docs**.

## If a write seems needed

Do **not** do it. Draft the intended comment/link/status change as **text in chat
or a PM doc** and tell Kylor to apply it himself. Only act if he writes a clear,
explicit per-conversation instruction to perform that specific Jira write.

## Overrides program starters

This supersedes any older instruction in `PM/sales-portal-agent-starters/**`
(spine, `05-ORCHESTRATOR.md`, reboot files, `JIRA-HYGIENE-COMMENTS.md`) that tells
an agent to "refresh Jira," "post hygiene comments," or "close/decline" a ticket.
Read-only wins.

---

<!-- from supercat-data-routing.mdc -->
For any live org/data lookup (org settings, flags like eOL, users, imports, inventory, support tickets, analytics, billing), use supercat-postgres-vpn or bigquery-admin per the supercat-data-routing skill. Never use supercat-cs-tools (retired).
