# Handoff Prompt — Build the Mali/NSL "Launch Readiness Checklist" (`mali`, org 285) · HS #14727

**Created:** 2026-07-23 · **For:** a fresh agent.
**Your one job:** produce a single **go/no-go Launch Readiness Checklist** that replaces the ad-hoc, item-by-item issue reviews we keep doing on calls. It is the single source of truth we send to the client (Jen Zorony / Jen Penton) **before the next meeting** and use to make a formal launch decision.

Do **not** re-litigate every past complaint in prose. Convert them into a small number of **gated, verifiable checklist rows**, each with a status, an owner, evidence, and whether it blocks launch.

---

## 0. Read these first (do not skip)
1. `HANDOFF_2026-07-23_HS14727_recovery.md` — architecture truth, importer guardrails, hidden-products correction, eOL inventory-render root cause.
2. `HANDOFF_2026-07-23_HS14727_execution.md` — the build/execution layer (files, image scrapes, decisions).
3. This session's outcome, in **§3 Current verified state** below (imports were run 2026-07-23; one went wrong — read it).
4. The **July 22 call** action items in **§4** and the **HelpScout thread** per **§2**.

**Guardrails (non-negotiable):** Jira is **read-only** (never write). Do not touch any frozen Insightful legacy folder. Postgres MCP `user-supercat-postgres-vpn` is **read-only**, org id **285**. Full product file every import (omitted = soft-delete on clean import); inventory **hard-deletes + reloads**. **Do NOT blanket-unhide** the 224 hideable SKUs. Output in **chat + a markdown file** — no canvas.

---

## 1. Deliverable spec — the Readiness Checklist

Produce `READINESS_CHECKLIST_2026-07-23_mali.md` with this shape:

**Header block**
- Client / org (`mali`, 285, ML=CAD, NSL=USD), decision date, target meeting date.
- **Overall recommendation:** `GO` / `CONDITIONAL GO (list conditions)` / `NO-GO` — one line, decided by the must-pass gates below.
- Launch scope being decided: beta reps in-hands (iPad) and/or eCat Online public.

**One table, grouped by domain.** Every row has these columns:
| # | Item | Domain | Status | Launch gate? | Owner | Evidence (query / ticket / screen) | Next action + ETA |

- **Status** vocabulary (use exactly): `✅ Ready` · `🟡 At-risk` · `🔴 Blocked` · `🧑‍⚖️ Decision needed` · `👀 Verify-on-rep-profile`.
- **Launch gate?** = `MUST-PASS` or `Nice-to-have`. Only `MUST-PASS` rows can force a NO-GO.
- **Owner** = `SuperCat` / `Client` / `Dev` / `Endeavour-IT (Brittni)`.
- **Evidence** must be concrete: a Postgres result, a HelpScout thread line, or "verified on Jen's NSL rep profile." No "should be fine."

**Domains (rows must cover all of these):**
1. **Data integrity** — product/inventory/stories/customers counts; clean File Import Status; zero ghost codes; zero dangling RelatedItems.
2. **Pricing** — ML CAD / NSL USD correct; `net_price` retired; **eCat Online per-customer pricing workflow** (logged-in customer with DN sees DN; list is public default) confirmed with Dev.
3. **Brand separation & rep experience** — Jen's ML + NSL rep/eCat-Online profiles exist; admin-view mixing understood/among-artifacts; UPC, cut sheets, instructions, and library each brand-restricted (verified on a rep profile, not Admin).
4. **Images** — 130 corrected & uploaded; residual needing client photography (authoritative count from `NEEDS_PHOTOGRAPHY_RESIDUAL.csv`); client image-delivery status.
5. **Inventory accuracy / pack-size mapping** — per-SKU quantities show per pack/length (SDL-5CCT 1/6/12/24P; SL-ID LP-20 vs LP-100 spools/feet); the **eOL inventory-render gap** (Dev); units-label decision.
6. **Variants / discoverability** — hidden pack-size/finish variants findable (via related-products or a real options build); **no blanket unhide**.
7. **Client enablement** — users/user-groups, rep invitations (note the ~1,274 missing BuyerEmail), NSL-code training on the ~57 divergent SKUs.
8. **Integration / automation** — Brittni SFTP (`/data/inventory.csv`, `PortNumber=22`) + GP export fix (`ROUND()`/int cast + null-filter) so files auto-feed instead of manual drop.
9. **Open dev decisions** — eOL inventory rendering; eOL pricing model. Each is a gate or an explicit "expectation set."

**Footer:** the **MUST-PASS gate list** (the short set that determines GO), and a dated "what changed since last review."

---

## 2. HelpScout #14727 — pull and map every item
Source: BigQuery MCP `user-bigquery-admin`, table `helpscout.conversations`, `number = 14727`; thread bodies live in `_embedded.threads`.
- Extract **every discrete client complaint/request** (Jen's numbered list + replies).
- Collapse duplicates and map each to exactly one checklist row (do not create a row per restatement).
- For each, mark whether this session already resolved it, whether it's an **Admin-view artifact** (retired by creating Jen's rep profile), or whether it's still open.
- Cross-check the ticket's "68 image mismatches" figure against our deeper pass (**111 residual** — see §3); use **111** as authoritative and note the reconciliation.

## 3. Current verified state (Postgres + this session, 2026-07-23)
- **Products import: SUCCEEDED.** Org 285 = **683 active** products (600 kept + 83 re-added discontinued/web SKUs), 274 soft-deleted. Only benign "custom field missing" warnings (8 registered-but-unused fields) + RelatedItems warnings that are **now fixed** (15 dangling refs to removed SKUs scrubbed). File: `00_Import_Files/Ready_For_Import/products.csv` (683 rows, 54 cols, `price_net_price` column dropped).
- **⚠️ Inventory import: WRONG FILE WAS IMPORTED — restore pending.** A different client's file (org **273 = `leg`**) was imported into mali. Inventory hard-deletes+reloads, so mali's real inventory was **wiped**; DB now holds **1,194 foreign rows, 0 matching any mali product** (`MGWL-06-6000K` gone). **Corrective action not yet done:** re-upload the correct `Ready_For_Import/inventory.csv` (683 mali rows, first code `SL-ID-30K-LP-20-A8`) to FTP `/data` (clear `/data` first) and re-import. This is a **MUST-PASS** row and currently `🔴 Blocked` until re-imported and verified.
- **net_price level:** still exists in DB (USD, position 5) — Admin deletion pending (column already removed from the file).
- **Images:** 130 corrected filenames (98 ML + 32 NSL) applied to products.csv and staged for FTP (`~/Downloads/Mali_Mismatched_Images/_FTP_UPLOAD/images/`, 130 JPGs). **111 residual** need client studio photography (`~/Downloads/Mali_Mismatched_Images/scrape_out_nsl/NEEDS_PHOTOGRAPHY_RESIDUAL.csv`).
- **Customers:** 3,418; `DefaultPriceCode` set on all (nsldn ×3,003 / mldn ×415).
- **Rep profiles for Jen (ML + NSL):** NOT yet created — the single highest-leverage open item (retires most Admin-view complaints).
- **`NSL_Code` custom field:** NOT built (deferred per execution §5.1; verify on rep profile first, then decide Option 1 field vs Option 2 two-org).

**Verification SQL to (re)run and cite as evidence:**
```sql
-- counts
select (select count(*) from products where organization_id=285 and not deleted) active_products,
       (select count(*) from inventories where organization_id=285) inventory_rows,
       (select count(*) from inventories i where i.organization_id=285
          and exists (select 1 from products p where p.organization_id=285 and not p.deleted
                      and p.item_number=i.base_item_code)) inv_matching_products,
       (select count(*) from customers where organization_id=285) customers;
-- price levels + currency (net_price should be gone after Admin delete)
select code, name, currency_code, position from price_levels where organization_id=285 order by position;
-- brand-restricted custom fields (UPC / cut sheets / instructions)
select cf.field_name, array_agg(ut.name order by ut.name) visible_to
from custom_fields cf
left join custom_fields_user_types cfut on cfut.custom_field_id=cf.id
left join user_types ut on ut.id=cfut.user_type_id
where cf.organization_id=285 and cf.field_name in
  ('ML_UPC','NSL_UPC','CutSheetML','CutSheetNSL','InstructionsML','InstructionsNSL')
group by cf.field_name;
-- library (shared_resources) brand split
select sr.id, sr.name, array_agg(ut.name order by ut.name) visible_to
from shared_resources sr
left join shared_resources_user_types srut on srut.shared_resource_id=sr.id
left join user_types ut on ut.id=srut.user_type_id
where sr.organization_id=285 group by sr.id, sr.name order by sr.name;
```

## 4. July 22 call — action items to fold into rows (Kyla ↔ Jen Z; recording: fathom.video/calls/754125371)
- **Brittni / Endeavour IT:** fix missed email + get her on a call this week — SFTP + GP export automation (the "big one" holding things up). → Integration domain, `🔴/🟡`.
- **eCat Online pricing workflow:** confirm with team/Dev — list price as public default, but a logged-in customer with a DN level should default to **their** price; then update Jen. → Pricing, `🧑‍⚖️ Decision needed`.
- **Cut sheets / instructions on NSL products:** remove ML ones from NSL (and vice versa) in eCat Online; **also rename** the bad NSL cut sheet on the first item (filename is "IP20 + Chinese characters + date"). → Brand separation, verify on rep profile.
- **Library:** NSL library entries under NSL, ML under ML (currently reads ML-branded in Admin view). → Brand separation, `👀`.
- **68 image mismatches** list to email Jen → reconcile to our **111 residual**; request replacement/internal images. → Images, `Client`.
- **Hidden pack-size variants** (e.g., `SDL-5CCT` 1/6/12/24P; `SL-ID` LP-20 vs LP-100): investigate why only one shows; unhide **only if needed** and only after rep-profile check. → Variants, `👀` (not blanket unhide).
- **Inventory per pack/length:** quantities must be listed **individually** ("374 of what?"). Send Jen an **example inventory file** for spools/feet; then implement mapping. Ties to the **eOL inventory-render gap**. → Inventory domain, `Dev`.
- **Create Jen's two eCat Online profiles** (ML + NSL, alias email + password) — so she reviews as a rep, not Admin. → Brand separation, `MUST-PASS`, `SuperCat`.
- **Admin-view mixing:** propose a way to switch/separate views in eCat Online so Admin doesn't merge both brands. → Brand separation / Dev.
- **Notes handover to Jen P** (back next week) + schedule a meeting with her re: filters/library.

**Framing to carry through:** the recurring own-goal is that Jen reviews everything logged in as **Admin**, which merges both brands. Most "it's broken" reports are Admin-view artifacts. Creating her rep profiles is the highest-leverage action and should be reflected as the gate that retires a cluster of rows at once.

---

## 5. How to work
1. Pull HS #14727 (BigQuery) + read the two handoffs + this doc.
2. Run the §3 SQL; record real numbers as evidence.
3. Build the checklist table; assign every row a Status, gate, owner, evidence, next action.
4. Decide the **MUST-PASS gate set** and the **overall GO / CONDITIONAL / NO-GO** line from it.
5. Write `READINESS_CHECKLIST_2026-07-23_mali.md` in `02_Implementation/Magic Lite/`; also paste the table in chat.
6. Keep it client-sendable: plain, specific, no internal blame, no cryptic codes.

## 6. Definition of done
- Every HS #14727 item and every July 22 action item appears in exactly one row (or is explicitly marked duplicate/retired-by-rep-profile).
- Each row has real evidence (query result / ticket line / rep-profile screen), not assumptions.
- The inventory-restore incident (§3) is a MUST-PASS row with current status.
- A clear MUST-PASS gate list and a single overall recommendation.
- Nothing written to Jira; no legacy folders touched; output is markdown (no canvas).
