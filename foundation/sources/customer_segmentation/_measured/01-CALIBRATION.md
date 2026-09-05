---
id: MEAS-01
title: Calibration — the register's stamped figures against live Postgres
version: 1.0
status: evidence pack
date: 2026-08-31
database: supercatprod
---

# Calibration

**Tagging:** every "Live 2026-08-31" figure in this file is `MEASURED` via the query id on its row.
Rows whose verdict cites the application repo are `CODE-AUDIT`; rows citing a permission failure are
`UNVERIFIABLE-FROM-DB`. Both are labelled inline.

Reproduce before extending. Every headline figure the register and `PERSONA-READOUT.html` rest on,
re-run today. **Failing to reproduce one is itself a finding**, so both numbers are recorded and a
verdict is stated. Nothing here has been silently corrected.

Drift note: the 90-day activity windows slide, so population counts move by tens of records week to
week. Movement inside that band is recorded as **reproduces (drift)**, not as an error.

---

## A. Population figures

| Register / readout says | Live 2026-08-31 | Query | Verdict |
|---|---|---|---|
| 2,365 admin records (register) → 2,460 (readout) | **2,460** | Q001 | **Reproduces exactly.** Readout's re-measure was right; the register's 2,365 was stale |
| 600 users active on both surfaces | **600** | Q001 | **Reproduces exactly** |
| Top 6 orgs hold 12,473 of 18,763 active buyers | **12,473 of 18,764**, 37 orgs | Q013 | **Reproduces exactly** |
| 18,763 active buyers on eCat Online | **18,763** | Q001 | **Reproduces exactly** |
| 4,058 / 4,059 active iPad reps | **4,026** | Q001 | Reproduces (drift) |
| 87,927 / 88,042 buyers enabled | **88,037 records** — but only **86,768** are actually `disabled IS NOT TRUE` | Q001 | **Reproduces the record count; the word "enabled" is wrong.** 1,269 of those records are disabled |
| 2,487 internal users active on eCat Online | **2,490** | Q001 | Reproduces (drift) |
| 7.5:1 buyers over internal on eCat Online | **7.54:1** on records | Q001 | Reproduces — **but 6.1:1 in people**, see §E |
| 617 agency reps active across 39 orgs | **590** active, `primary_rep_group` on 142 of 1,986 user types across **42** orgs | Q070 | Reproduces (drift) on reps; org count is 42 not 39 |
| 11,873 / 11,880 free-text company names | **11,799** internal distinct | Q071 | **Reproduces.** See §E for why the figure is the wrong argument |

## B. The two client-data gaps

| Register / readout says | Live 2026-08-31 | Query | Verdict |
|---|---|---|---|
| 38 of 109 roster orgs have an invoice feed | Unverifiable as stated — the roster is a CSV outside the repo. Measured against the live universe: **48 of 112** active orgs have any feed | Q003 | **Superseded.** Use 48/112 |
| Invoice feed missing at 65 of 113 active clients (readout) | **64 of 112** | Q003 | Reproduces (drift) |
| — *not claimed anywhere* — | Only **44** of the 56 feed orgs have an invoice dated in the last 12 months. **12 feeds have stopped** | Q003 | **New. Material.** For any current-year question the denominator is 44, not 48 |
| Territory master empty in 32 of 55 orgs [F11] | Superseded by the 08-27 measure | Q003 | Superseded |
| 122/123 of 145/146 orgs with active reps have no territory master | **121 of 144** | Q003, Q004 | Reproduces (drift) |
| 664 reps scopeable / 3,395 not | **655 / 3,371** | Q004 | Reproduces (drift) |
| 940 reps with no territory codes | **938** | Q004 | Reproduces (drift) |
| Launch population in 20 orgs | **20 orgs** | Q004 | **Reproduces exactly** |
| 23 of 145/146 rep orgs have a territory master | **23** | Q003 | **Reproduces exactly** |

## C. Feature and configuration counts

| Register / readout says | Live 2026-08-31 | Query | Verdict |
|---|---|---|---|
| **"Cart in 58 orgs"** (register, JTBD-081) | **58 sites across 55 distinct orgs** | Q002 | **WRONG — confirmed.** The flag is on `mobile_sites`; three orgs run more than one site. The readout already carries the correction ("55 of 258 orgs (58 sites)") and reproduces exactly |
| `enable_rep_activity` on 7 of 257 orgs | **7 of 258** | Q006 | **Reproduces.** Org total is 258, not 257 |
| Ungating `enable_rep_activity` serves JTBD-032/063 | Cannot be tested: **`rep_activities` returns permission denied** for this role | Q007 | The 08-27 pack's correction stands and is **not contradicted**. Recorded as `UNVERIFIABLE-FROM-DB` |
| 16 CPQ orgs | **21** orgs hold CPQ entitlement (plans 3+9+12); **17** on the main CPQ plan; option data in **92** orgs; configurator cascade in **7** | Q039, Q060 | **Depends entirely on definition.** "16" matches none of the three cleanly |
| Reports reach six clients / Territory Dashboard enabled for zero orgs | `CODE-AUDIT`, not testable here. **But** `mobile_sites.enable_sales_portal` is true for **50 orgs**, and **37 orgs pay for the Portal plan** | Q002, Q060, Q061 | **Partially superseded.** See §D — the denominator was never 258 |
| 179,577 of 938,394 active items have no image (roadmap) / 179,623 of 938,896 (readout) | **179,623 of 938,893** | Q005 | **Reproduces exactly** on the numerator |
| `tracking_number` on 1,121,123 invoices across 26 orgs; carrier 744,046; `ship_via` 2,712,248 | **1,123,291 / 26 orgs; 745,381; 2,711,216 across 37 orgs** | Q044 | **Reproduces.** The roadmap's correction to `data-gaps.md` B3 is confirmed |
| 134 toggles / 39 YAML flags / 6 layers [F10] | Not reproducible from the schema: `user_types` has 12 boolean columns, `organizations` 35 | Q070 | `CODE-AUDIT`. Left standing, not contradicted, but not confirmed either |

## D. The figures the register called unverifiable, that turned out not to be

| Register / readout says | Live 2026-08-31 | Query | Verdict |
|---|---|---|---|
| "Feature gates live in application YAML, not Postgres" | True for fine-grained gates. **False for plan-level commercial entitlement**, which is fully queryable in `subscription_plans` + `subscriptions` | Q060 | **Materially incomplete.** See finding 4 |
| "~13,800 additional active buyers from turning on purchase history"; "somewhere between 6,000 and 18,000" | Ceiling is **17,522** active buyer records at orgs that are both on the Portal plan and have a feed. Defensible range **~5,100 – ~17,500** | Q062 | **Bounded.** 13,800 sits inside the range but is not pinned. Naming the 6 orgs collapses it |
| "the switch lives in application config, not the database" | The **`:advanced_reports` sub-gate** does. The **Portal entitlement it sits inside** does not — 37 paying orgs | Q060, Q061 | Half right |

## E. Where the measurement changes the meaning, not just the digits

Four figures reproduce numerically but mean something different once measured properly.

1. **"4,059 active iPad reps" counts records, not people.** 4,026 records = **2,141 people**, 1.88
   org memberships each (Q051). Every rep-facing headcount in the register is inflated ~1.9×. The
   launch population is **559 people**, and 226 people are scopeable at one manufacturer and not
   another (Q052).

2. **"18,763 active buyers" is 12,972 people** (Q053). The buyer:internal ratio is **6.1:1**, not
   7.5:1.

3. **"11,880 free-text company names" is the wrong argument for declining PER-02.** It reproduces
   (11,799), but only **868 of 4,026 active reps have `company_name` populated at all** (Q071).
   The blocker is absence, not messiness. Same decision, better reason.

4. **"179,623 items have no image" is right and misleading.** 26,539 of them sit in orgs where *no*
   item has an image, and test/staging orgs contribute ~24,700 more (Q045, Q046). The register's
   companion figure — 189,471 items missing a price — is **roughly half configuration**: 25 orgs
   never use `net_price` at all. Genuine gaps: **153,084 images, 98,441 prices.**

---

## Must change in the readout

Figures in `../PERSONA-READOUT.html` that this work contradicts. Listed so the rebuild pass does not
carry them forward.

**Wrong, replace:**

| Readout says | Replace with | Query |
|---|---|---|
| "88,042 of them enabled" | 88,037 buyer records; **86,768 enabled** | Q001 |
| "4,059 Active iPad reps" | 4,026 records = **2,141 people** | Q001, Q051 |
| "664 Launch population · 16%" / "664 scopeable, 3,395 not" | 655 records = **559 people**; 3,371 records unscopeable | Q004, Q052 |
| "940 reps with no territory codes" | 938 | Q004 |
| "Missing at 65 of 113 active clients" | 64 of 112 — and only **44 of 112 have a live (12-month) feed** | Q003 |
| "Invoice feed 48/113" | 48/112 present, **44/112 live** | Q003 |
| "Territory file 23/146" / "123 of 146" | 23/144 · 121 of 144 | Q003 |
| "Reps scopeable 664/4,059" | 655/4,026 records · **559/2,141 people** | Q004, Q052 |
| "18,763 active — 7.5× the internal users" | 7.54× on records, **6.1× in people** | Q001, Q053 |
| "only 600 people are active on both" | 600 — correct, but these are *records*; state it as such | Q001 |
| "617 active across 39 orgs" (agency) | 590 active across **42** orgs | Q070 |
| "11,880 typed-in company names" | 11,799 — **and the real blocker is that 78% of active reps have no company name at all** | Q071 |
| "179,623 of 938,896 active items have no image" | 179,623 of 938,893 gross; **153,084 genuine** (excl. image-free catalogs), and test orgs contribute ~24,700 | Q005, Q045, Q046 |
| "16 orgs" (CPQ, JTBD-052) | 21 orgs entitled; option data in 92 orgs; configurator cascade in **7** | Q039, Q060 |
| "Turning on purchase history reaches somewhere between 6,000 and 18,000 active buyers" | Ceiling **17,522**; defensible range **~5,100–17,500** | Q062 |
| "that switch lives in application config, not the database" | The sub-gate does; the **Portal entitlement does not** — 37 orgs pay for it | Q060, Q061 |
| "Three figures come from the code and config audit… Feature gates live in application YAML, not Postgres" | Rewrite. Plan-level entitlement **is** in Postgres | Q060 |

**Needs restating precisely, currently ambiguous:**

- *"The Portal surface a rep would use is enabled for zero organisations — the flag resolves to nine
  internal SuperCat usernames."* This is presumably the rep **Territory Dashboard** specifically.
  As written it reads as "the Sales Portal is off everywhere," which is false:
  `mobile_sites.enable_sales_portal` is true for **50 orgs** and **37 orgs pay for the Portal plan**
  (Q002, Q060). Name the specific flag or the sentence misleads.

**Unchanged — reproduced exactly, use with confidence:**

2,460 admin records · 600 active on both · 12,473 buyers in the top 6 orgs · 18,763 active buyers ·
55 orgs / 58 sites for Cart · 7 of 258 orgs on `enable_rep_activity` · 20 launch orgs · 23 rep-orgs
with a territory master · 179,623 items with no image (gross) · the whole `tracking_number` /
`ship_via` correction in `03-ROADMAP.md`.

**New, worth adding to the readout:**

- The invoice-feed gap holds **49% of the rep base and 6% of buyers** (Q020) — the single most
  decision-relevant number in this pack.
- **64.1% of the missing order value sits in 6 orgs** (Q022).
- 70% of "active" reps wrote **zero** orders in 90 days; 8.8% wrote 86% of them (Q010).
- **25 orgs run Cart without a Cart subscription** (Q061).
- One order of **$464,039,002** distorts every value series that includes 2025Q2 (Q056).
