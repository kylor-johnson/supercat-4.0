---
id: PER-00
title: Login seats — who is on which surface (not the persona set)
version: 0.2
status: draft
date: 2026-09-15
owner: Kylor Johnson
axis: seat (who is logged in)
note: Demoted 2026-09-15. Product personas are motion × seat groups in 00-PERSONA-GROUPS.md.
source_lineage:
  - PM/sales-portal-agent-starters/cycle-03-outputs/PERSONA-ONE-PAGERS.md
  - Postgres (read-only), 2026-08-25
depends_on: [TAX-A]
---

# Login seats

**This file is not the persona set.** It is who is logged in, on which surface, with measured headcounts. The persona set for what to build is [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md) — selling motion × seat.

A seat does not tell you the job. An "independent sales rep" at a spec house (PG-01) and at a volume feeder (PG-07) share a device and almost no analytics job.

---

## Measured populations

`[MEASURED]` Postgres, 2026-08-25, across 253 orgs with users:

| Seat | Records | Active 90d | Surface |
|---|---:|---:|---|
| **Buyers** (`customer_number` present) | **87,927** | **17,532** on portal orgs · 21,260 eOL overall | eCat Online |
| **Reps / internal non-admin** | 23,424 | **4,058 iPad-active** across 146 orgs | eCat iPad |
| **Internal admins** (`is_admin`) | 2,365 | 377 iPad · **141 eOL** | Admin / Portal |
| Users active on **both** iPad and eOL | — | **593** | — |

**Reps and buyers are near-disjoint.** Only 593 users are active on both. `should_show_customers_tab` requires `customer_number.blank?` — a buyer cannot reach rep views. They do not share a screen, a session, or a mental model. Design the surfaces separately.

**The buyer is the largest population on any SuperCat surface** (7.7:1 on active logins). They are *our customer's customer*. Buyer jobs exist only if they pay the manufacturer.

**There is no incumbent rep analytics surface.** Territory Dashboard (`:portal_portal`) is enabled for zero organisations. Reports reaches six. Field-rep analytics is greenfield and belongs in an iPad-embedded component, not as a Portal redesign.

---

## Seat index (detail files)

These files keep evidence about the seat. They are **not** the build list. Start at [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md).

| Seat ID | Who | Maps into persona groups |
|---|---|---|
| PER-01 | Independent sales rep (iPad) | PG-01, PG-03, PG-05, PG-07 — **different jobs** |
| PER-02 | Rep agency principal | **Unservable** this cycle (no agency entity). Not a group. |
| PER-03 | VP Sales / sales ops | PG-HQ |
| PER-04 | Customer service / order entry | PG-HQ |
| PER-05 | Product / merchandising | PG-HQ |
| PER-06 | Owner / exec | PG-HQ |
| PER-08 | Dealer / designer / chain buyer | PG-02, PG-04, PG-06, PG-08 — **different jobs; do not fold** |

Dropped as analytics seats (unchanged): IT/integrations (job status, not analytics); Manager (permission tier inside PER-03); SuperCat-internal staff (out of frame).

---

## Retired doctrine

The Aug 25 claim that **only 4 of 31 jobs vary by selling motion** and that **one surface serves everyone** is withdrawn as product doctrine. It treated seats as personas. Structure (price-code count, catalog size) still parameterises **HQ** jobs and extract size. It does not make a spec-rep and a volume-rep the same persona.

Jobs: [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md). Surfaces: [`../product/surface-mapping.md`](../product/surface-mapping.md).
