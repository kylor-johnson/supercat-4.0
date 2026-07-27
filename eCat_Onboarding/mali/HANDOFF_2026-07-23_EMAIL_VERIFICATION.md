# Pre-Send Verification Handoff — Magic Lite / NSL (`mali`, org 285) · HS #14727

**Created:** 2026-07-23 (evening) · **For:** a fresh agent whose ONE job is to make the next client email 100% correct.
**Stakes:** escalated, churn-risk. The client (Jen Zorony / Jen Penton) has caught us being wrong before. **Every factual claim in the outbound email must be re-verified against the LIVE database before send — not against our own handoff docs, which are partially stale.**

> Read `HANDOFF_2026-07-23_HS14727_recovery.md` and `..._execution.md` for architecture + history, and `READINESS_CHECKLIST_2026-07-23_mali.md` for the intended state. **But do not trust the checklist's "live" numbers** — see §2. The parent agent re-ran the live queries on 2026-07-23 evening and found the checklist overstates the inventory state.

**Guardrails (non-negotiable):** Jira read-only. No frozen Insightful legacy folders. Postgres MCP `user-supercat-postgres-vpn` = read-only, org id **285**. Full product file every import (omitted = soft-delete on clean import). Inventory **hard-deletes + reloads** (must be clean). Do **NOT** blanket-unhide. Output markdown, no canvas.

---

## 1. VERIFIED-TRUE ledger (safe to say in the email — re-run to confirm before send)

Live Postgres, org 285, verified 2026-07-23 evening by parent agent:

| Claim | Verified value | Query basis |
|---|---|---|
| Active products | **683** (257 hideable); **0** missing story | `products where organization_id=285 and not deleted` |
| Price levels + currency | `mldn`/`mllist` = **CAD**, `nsldn`/`nsllist` = **USD** | `price_levels` |
| `net_price` retired | **Gone** — no such level, no key in prices | `price_levels` (only 4 rows) |
| Brand custom fields correctly restricted | `ML_UPC`/`CutSheetML`/`InstructionsML` → **ML Reps + eOL ML** only; `NSL_UPC`/`CutSheetNSL`/`InstructionsNSL` → **NSL Reps + eOL NSL** only | `custom_fields_user_types` |
| `NSL_Code` field | **Not built** (deferred — correct per plan) | not present |
| Library brand split | **ML Reps = 46 files, all `magiclite.com`, 0 NSL** · **NSL Reps = 131 files, all `nslusa.com`, 0 ML** · eOL sites match · Admin = All | `shared_resources_user_types` |
| Customer pricing defaults | `default_price_code` set on **all 3,418** (`nsldn` ×3,003 / `mldn` ×415, zero blanks) | `customers` |
| Images resolve | **681/683** active products have `image_exists=true` (2 missing) | `products.image_exists` |

**These support the email's strongest, safest message:** the brand split (pricing, UPCs, cut sheets/instructions, library) **is correctly built at the data/permission layer**. The "NSL shows ML info / both UPCs / ML library" reports are **Admin-view artifacts** — see §3.

---

## 2. VERIFIED-WRONG in our own docs — DO NOT let these into the email

The `READINESS_CHECKLIST` says inventory is clean/matched/GA-folded with 0 negatives. **The live database disagrees.** The last inventory import (event `1902214`, **21:12 UTC**) used a **stale, dirty 694-row file**, overwriting the clean 20:45 import (`1902192`) and the products import at 21:22.

| Checklist claims | Live DB actually shows | Evidence |
|---|---|---|
| 683 inventory rows, **0 ghosts** | **694 rows; 11 orphan/ghost codes** | `inventories` vs active `products` |
| GA fold-in landed: `SL-ID-30K-LP-20-A8` NSL=**405** | **NSL_QtyAvailable = 375** (pre-GA) | `inventories.custom_fields` |
| **0 negative** inventory cells | `SL-ID-30K-LP-20-A8` **ML_QtyAvailable = −1** | same |
| Both eOL sites `hide_products_marked_hideable=true` | **Both NULL/unset** (default = false) → hidden SKUs still show on eOL grid | `mobile_sites.properties` |

**The 11 ghost inventory codes** (products are soft-deleted, inventory rows orphaned):
`FL-ADM-30, FL-SH-30, FL-WG-30, FL-Y-15, FL-Y-30, LT-WIFI-AMP, LT-WIFI-CTRL, LV-RF103-EXHS, NFLX-L-SPLICE, NFLX-RGB-CK-6FT-O, SX-TP-WH`
(These match the "11 nowhere" bucket + FL flood accessories + Switchex `SX-*` the client asked about.)

**Why this is the #1 landmine:** `SL-ID-30K-LP-20-A8` is the **exact tape SKU Jen screenshotted** ("374 of what?"). If the email says "inventory is now accurate per pack size" and she opens that SKU on her iPad/NSL profile, she sees **NSL 375 (not the 405 we think we fixed)** and an **ML available of −1**. That is a fourth strike.

### ✅ The good news / the fix
The **staged `00_Import_Files/Ready_For_Import/inventory.csv` is CLEAN and CORRECT** (verified by parent agent):
- `SL-ID-30K-LP-20-A8` → `QtyAvailable=405, NSL_QtyAvailable=405, ML_QtyAvailable=0`, GA folded in
- **No ghost codes, no negatives**, 683 rows

**So the fix is: re-import the staged clean inventory.csv (clear FTP `/data` first, upload, import, verify File Import Status is warning-free) BEFORE the email claims inventory is accurate.** Until that import lands and is re-verified in the DB, the email must NOT assert inventory correctness.

---

## 3. The linchpin argument — and the trap inside it

The whole email rests on: *"most of what looks broken is because you're reviewing as Admin, which merges both brands; log in as your brand profile and it's correct."* **This is true and the data backs it (§1).** But there's a trap:

**Jen's own "rep" aliases are still Admin.** Verified:

| Account | Group | `is_admin` |
|---|---|---|
| `jen@magiclite.com` | Admin | true |
| `jen.penton@magiclite.com` | Admin | true |
| `jen+user@magiclite.com` | NSL Reps | **true** ← still admin |
| `jen.penton+user@magiclite.com` | NSL Reps | **true** ← still admin |
| *(no Jen ML Reps alias exists)* | — | — |

If we tell Jen "log into your NSL profile and you'll see it's clean," and that alias has `is_admin=true`, she will **see the same merged Admin view and conclude we're wrong again.** 

**Clean, genuinely non-admin reviewers that DO exist** (usable to prove the split): `pansy@magiclite.com` (ML Reps, is_admin=false), `jason@nslusa.com` / `michelle@nslusa.com` (NSL Reps, is_admin=false).

**Required before the email tells Jen to self-verify:** either (a) clear `is_admin` on `jen+user` and `jen.penton+user` and create a Jen **ML Reps** non-admin alias, or (b) hand her credentials to a known non-admin ML + NSL account. The fresh agent must confirm which, and confirm in code whether `is_admin=true` overrides user-group custom-field/library/price authorization on eOL (assume YES = sees everything).

---

## 4. Claims that are TRUE but frequently misstated — say them precisely

- **Images:** `image_exists=true` on 681/683 only means **the filename resolves to a file on the server** — NOT that the photo content is correct. The client's complaints are *wrong-content* (right code, wrong picture: DR-96, YH-SIGNAL-AMP=eStrip, sconces=SL-CC, drivers, trims, etc.). 130 filenames were repointed/re-uploaded this week, but a large residual still shares a primary image with unrelated SKUs. **Do NOT say "all images are corrected."** Say: "we corrected 130; here is the remaining list that needs your studio photos." Reconcile the residual count from live data before citing a number — our docs contain conflicting figures (**68 / 111 / 311**). Use the grounded shared-primary CSV, not the old 68/111.
- **eOL live inventory does not render at all.** Code-verified (recovery §4): eCat **Online** product detail has no path to show inventory custom fields; only the **iPad** shows live quantities. So "374 of what / I don't see a quantity" on the website is **real and unfixed**. The email must set the expectation: live quantities show on the **iPad**; eOL live-qty is a pending dev item — do not promise a date.
- **Pack/units:** the spool length is now in ShortDesc/LongDesc on the 8 Streamline SKUs (verify still live after any re-import). "374" ambiguity is addressed by the description text + per-SKU codes, not by a units field (UOM field optional/not built).
- **NSL divergent codes:** our docs disagree (**~57** in execution §5.1 vs **78 NSL-only / 87 ML-only** in the verification prompt). **Do not cite a number** until recomputed from the two AUG2025 xlsx. The safe message: most codes are identical; a minority differ; NSL reps currently see the shared (ML-origin) headline code; the `NSL_Code` field / training is the planned fix.
- **eOL per-customer pricing** (Jen's "customer should see their price on login"): needs **dev confirmation** — code caveat (recovery §6) is that eOL can fall to the *user-group* default unless an associated customer record exists. Do not promise the exact behavior until dev confirms.

---

## 5. The fresh agent's job (in order)

1. **Re-run the §1 and §2 SQL** (below) and record real numbers. Treat the DB as truth over any doc.
2. **Fix the inventory regression:** confirm the staged `Ready_For_Import/inventory.csv` is clean (405, no ghosts, no negatives), re-upload to FTP `/data`, re-import, and **verify File Import Status is warning-free** and the 11 ghosts + the −1 + the 375→405 are gone in the DB. Only then may the email claim inventory accuracy.
3. **Resolve the Jen-profile trap (§3):** get her a genuinely non-admin ML + NSL login (or clear `is_admin`), and confirm behavior.
4. **Red-team the email draft** (§6) line-by-line against the verified ledger. Flag every sentence that asserts something not in the §1 TRUE list or that contradicts §2/§4. Rewrite to "here's what's fixed / here's what we need from you / here's what's pending on our side."
5. Produce: (a) corrected factual claims, (b) the residual-photos list to attach with a defensible count, (c) a short "verify-it-yourself" script for Jen using non-admin logins.

---

## 6. EMAIL DRAFT TO RED-TEAM

> **PASTE THE CURRENT EMAIL DRAFT HERE.** Then check each claim against §1 (must be in the TRUE ledger), and ensure nothing violates §2 (inventory not yet clean) or §4 (images/eOL-qty/codes precision). Kyla drafted it without visibility into the parent agent's data work, so assume optimistic claims need downgrading to verified ones.

```
<email draft goes here>
```

---

## 7. Verification SQL (read-only, org 285)

```sql
-- counts + ghosts + negatives (the §2 landmine)
select (select count(*) from products where organization_id=285 and not deleted) active_products,
       (select count(*) from inventories where organization_id=285) inv_rows,
       (select count(*) from inventories i where i.organization_id=285
          and not exists (select 1 from products p where p.organization_id=285 and not p.deleted
                          and p.item_number=i.base_item_code)) ghost_inv_rows;

select base_item_code, custom_fields from inventories
where organization_id=285 and base_item_code='SL-ID-30K-LP-20-A8';   -- expect NSL 405 / ML 0 after clean re-import

-- mobile-site hide flag (checklist wrongly says true)
select id, url_key, properties->>'hide_products_marked_hideable' as hide_hideable,
       properties->>'display_quantity_available' as disp_qty
from mobile_sites where organization_id=285 order by id;

-- price levels (net_price should be absent)
select code, name, currency_code, position from price_levels where organization_id=285 order by position;

-- brand custom fields
select cf.field_name, array_agg(ut.name order by ut.name) visible_to
from custom_fields cf
left join custom_fields_user_types cfut on cfut.custom_field_id=cf.id
left join user_types ut on ut.id=cfut.user_type_id
where cf.organization_id=285 and cf.field_name in
  ('ML_UPC','NSL_UPC','CutSheetML','CutSheetNSL','InstructionsML','InstructionsNSL')
group by cf.field_name;

-- library split per group
select ut.name, count(distinct case when sr.value ilike '%magiclite.com%' then sr.id end) ml,
       count(distinct case when sr.value ilike '%nslusa.com%' then sr.id end) nsl
from user_types ut
left join shared_resources_user_types srut on srut.user_type_id=ut.id
left join shared_resources sr on sr.id=srut.shared_resource_id and sr.organization_id=285
where ut.organization_id=285 group by ut.name order by ut.name;

-- Jen profiles (the linchpin trap)
select u.email, ut.name grp, ou.is_admin
from org_users ou join users u on u.id=ou.user_id
left join user_types ut on ut.id=ou.user_type_id
where ou.organization_id=285 and u.email ilike '%jen%' order by u.email;
```

---

## 8. Definition of done (before Kylor hits send)
- [ ] Inventory re-imported from the clean staged file; DB shows 683 matched rows, **0 ghosts, 0 negatives**, `SL-ID-30K-LP-20-A8` NSL=405 / ML≥0; File Import Status warning-free.
- [ ] Jen has a working **non-admin** ML profile and NSL profile (or `is_admin` cleared on her aliases); confirmed she'll see a single brand.
- [ ] Every email sentence maps to a §1 verified fact; no claim of "all images fixed" or "eOL shows live qty" or a specific NSL-divergent-code number that isn't recomputed.
- [ ] Residual photography list attached with a count grounded in current data.
- [ ] Nothing written to Jira; no legacy folders touched.
