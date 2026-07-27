# Magic Lite / NSL (`mali`) — Library Handoff Prompt

Paste this into a fresh agent chat. Goal: **review current state and decide how to add brand-split docs to the eCat Resource Library** (ML vs NSL), then implement in Admin Console.

KB reference: [Resource Library (Admin)](https://supercatsolutions.com/knowledgebase/document-library)

---

## Context

Magic Lite (Canada) and National Specialty Lighting / NSL (US) share **one SuperCat org**: shortname `mali`. Two eCat Online sites exist (Magic Lite + National Specialty Lighting). Client feedback (2026-07-20): NSL site “doesn’t have a Library” / library content is ML-branded. Product-detail cut sheets are already split by custom field; the **site Library** (`shared_resources`) is still ML-only links.

There is **no CSV bulk import for Library**. Entries are Admin Console sections + file/link entries, authorized per user group. Prefer **link** entries to client-hosted PDFs (already on magiclite.com / nslusa.com).

---

## Source of truth

| What | Path |
|------|------|
| Working import files | `02_Implementation/Magic Lite/00_Import_Files/Ready_For_Import/` |
| Current products (doc URLs + pricing) | `…/Ready_For_Import/products.csv` |
| Curated family→PDF maps (best for Library build) | `07_Data_Scraping/pdf_links/*.json` (ML) and `07_Data_Scraping/pdf_links/nsl/*.json` (NSL) |
| Broader scrape (ML site only, noisier) | `07_Data_Scraping/pdf_scrape_2026-07-13.json` |
| Client profile | `CLIENT_PROFILE.md` |
| This handoff | `HANDOFF.md` |

`pdf_links` is the best Library source: **82 product families**, same titles on ML and NSL, each with `cutsheet`, `instructions`, `codes[]`, optional `code_overrides`. Domains are brand-correct (`magiclite.com` vs `www.nslusa.com`).

---

## Live org state (Postgres, org_id `285`) — verified 2026-07-20

### eCat Online sites

| Site | url_key | Library enabled | Default price level | Site org_user group |
|------|---------|-----------------|---------------------|---------------------|
| Magic Lite | `12` | yes | `mldn` **CAD** | `eOL  ML Public Site` |
| National Specialty Lighting | `13` | yes | `nsldn` **USD** | `eOL  NSL Public Site` |

Both sites: `allows_unauthenticated_users = false` (login required). Both sites’ **Default User Group for enrollment** is still `DefaultUserGroup` (sees all price levels / all custom fields) — separate issue from Library.

Library nav only appears if `enable_online_library` **and** the logged-in user’s group has ≥1 authorized library **resource** (file/link). See KB + `layouts/ecat/_nav.html.erb`.

### Current Library contents (all ML-branded)

Sections (directories):

1. Sale (has a stray uploaded `products-import-ready.csv` — likely remove)
2. Catalogues & Selection Guides (2 ML links)
3. Installation Instructions (~11 ML links)
4. Product Cut Sheets (~30 ML links)

**Zero NSL-domain URLs** in `shared_resources` today.

### User group Library auth (critical)

Per KB: entry-level checkboxes only work if the user group is set to **Selected** library entries. If the group is **All**, members see every entry even when unchecked.

| User group | `shared_resources_auth` | Meaning today |
|------------|-------------------------|---------------|
| Admin | `a` (All) | Sees everything |
| DefaultUserGroup | `a` (All) | Sees everything |
| ML Reps | `a` (All) | Sees everything (junction has 7 rows but ignored while All) |
| NSL Reps | `a` (All) | Sees everything — **including ML Library** |
| eOL ML Public Site | `a` (All) | Sees everything |
| eOL NSL Public Site | `a` (All) | Sees everything — **including ML Library** |
| z-SuperCat | `a` (All) | Sees everything |

So even if you add NSL entries, **you cannot hide ML docs from NSL users until those groups are switched to Selected (`c`) and only the right entries are checked.**

---

## Two different “docs” systems (do not confuse)

| Surface | Mechanism | Brand split today |
|---------|-----------|-------------------|
| **Product detail** Cut Sheet / Instructions | Custom fields `CutSheetML`, `InstructionsML`, `CutSheetNSL`, `InstructionsNSL` on products | Done — ML groups get ML fields; NSL groups get NSL fields |
| **Site / iPad Library** nav | Admin `shared_resources` sections + entries | **Not done** — ML links only; all groups All |

Product-field coverage in current `products.csv` (unique URLs):

- CutSheetML: 116 · InstructionsML: 63  
- CutSheetNSL: 100 · InstructionsNSL: 59  

Library does **not** need one entry per SKU. Prefer **one link per family PDF** (as in `pdf_links`), matching how the current ML Library was built.

---

## Decision the next agent must make

### Option A — Dual parallel libraries (recommended)

Mirror sections for each brand (or prefix labels), authorize by group:

- Sections e.g. `ML — Catalogues`, `ML — Cut Sheets`, `ML — Instructions` **and** `NSL — Catalogues`, `NSL — Cut Sheets`, `NSL — Instructions`  
  (or shared section names with clearly branded entry labels)
- Set these groups to Library = **Selected**: `ML Reps`, `NSL Reps`, `eOL  ML Public Site`, `eOL  NSL Public Site`
- Leave Admin / z-SuperCat on **All** (or Selected with both brands)
- Assign ML entries → ML Reps + eOL ML Public Site  
- Assign NSL entries → NSL Reps + eOL NSL Public Site  

**Pros:** Matches dual-site / dual-rep model; fixes “NSL has no Library of its own.”  
**Cons:** Admin work (~150+ link entries if full `pdf_links` coverage); must flip auth from All → Selected carefully so nobody loses access mid-flight.

### Option B — NSL-only additive Library

Keep existing ML sections as-is for ML audiences; add parallel NSL sections; flip **only** NSL Reps + eOL NSL Public Site to Selected with NSL entries only. Leave ML groups on All (they keep seeing current ML library).

**Pros:** Less change for ML.  
**Cons:** ML groups on All still see any NSL entries you add unless you also restrict ML groups to Selected.

### Option C — Thin Library (catalogues + key guides only)

Library = catalogues / selection charts / top install guides only; rely on product custom fields for per-SKU cut sheets.

**Pros:** Small Admin surface.  
**Cons:** Client already expects a browsable Library of cut sheets (ML site has one); NSL would still feel thin.

**Recommend starting with Option A**, scoped by collection priority (Linear / Streamline first — already partially in Library), then expand from `pdf_links`.

---

## Suggested build plan (after decision)

1. **Inventory gap**  
   Diff unique `cutsheet`/`instructions` URLs in:
   - `07_Data_Scraping/pdf_links/*.json` (ML)
   - `07_Data_Scraping/pdf_links/nsl/*.json` (NSL)  
   against live `shared_resources.value` for org 285. Produce a checklist of missing entries by section.

2. **Clean house**  
   - Remove or unshare Sale → `products-import-ready.csv` if not intentional client content.  
   - Confirm French ML docs stay ML-only (NSL typically EN).

3. **Create NSL sections + link entries**  
   Admin → Library → New Section / New Link.  
   Labels: use family titles from `pdf_links` JSON keys (same across brands).  
   URLs: NSL `cutsheet` / `instructions` fields only.  
   Prefer links (not uploads) — PDFs are already hosted; uploads capped at 30MB and sync to iPads ([KB](https://supercatsolutions.com/knowledgebase/document-library)).

4. **Flip user-group Library auth**  
   Users → User Groups → each brand group → Library Entries = **Selected**, check the right entries (and/or set checks while editing each entry — only works once group is Selected).  
   Verify with KB rule: All overrides entry checkboxes.

5. **Verify**  
   - Login as NSL Reps (not Admin) on NSL eOL site → Library shows NSL docs only.  
   - Login as ML Reps on ML site → ML docs only.  
   - Admin can still see both if left on All.

6. **Do not re-scrape unless needed**  
   `pdf_links` already has brand-split URLs. Only re-scrape if a family is missing or a URL 404s.

---

## Related open items (not Library, but same client thread)

- Pricing gaps from Jen’s spreadsheet were applied to `Ready_For_Import/products.csv` on 2026-07-20 (backup `products.backup_20260720_162000.csv`) — **re-import still needed**.
- ~70 SKUs remain ML-priced only (wrong NSL item codes per client — need NSL price list / correct codes).
- Reviewer accounts (Jen) are **Admin** → see all price levels (ML CAD) and both CutSheetML + CutSheetNSL. For brand QA use NSL Reps / ML Reps logins.
- Enrollment Default User Group on both sites still `DefaultUserGroup` — should become the matching eOL public site group.

---

## Postgres checks (read-only)

```sql
-- org
select id, shortname, name from organizations where shortname = 'mali';

-- library tree
select sr.id, coalesce(p.value,'(root)') as section, sr.resource_type,
       coalesce(sr.label, sr.value) as label, left(coalesce(sr.value,''),120) as url
from shared_resources sr
left join shared_resources p on p.id = sr.parent_id
where sr.organization_id = 285
order by coalesce(p.position, sr.position), sr.position;

-- group library auth
select name, shared_resources_auth from user_types where organization_id = 285;
```

MCP: `user-supercat-postgres-vpn` → `execute_sql`.

---

## Validation before calling Library “done”

- [ ] NSL eOL site, logged in as **NSL Reps** or browsing as **eOL NSL Public Site** user: Library nav visible
- [ ] NSL Library entries are `nslusa.com` (or NSL-labeled), not magiclite.com
- [ ] ML site / ML Reps: still see ML Library; no accidental wipe
- [ ] Groups that should be brand-scoped are Library auth **Selected**, not All
- [ ] Sale/test CSV entry removed or intentionally kept
- [ ] Product-detail CutSheet* fields unchanged (Library work is separate)

---

## Rules in effect (catalog — for context only)

- Org shortname: **`mali` only** (not a separate `nsl` org)
- Price levels: `mllist`/`mldn` CAD · `nsllist`/`nsldn` USD · do not authorize `net_price` for brand public groups
- Product custom fields for docs: `CutSheetML`, `InstructionsML`, `CutSheetNSL`, `InstructionsNSL`
- Collections: LL, UCL, DL, LAND, IL
- Tokistar out of scope
