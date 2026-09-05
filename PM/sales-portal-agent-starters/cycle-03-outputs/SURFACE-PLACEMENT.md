# SURFACE PLACEMENT — Bet F (v0)

**Date:** 2026-07-24 · **Phase:** 2 shape pack · **Isolation:** ON · **Does not unlock Bet A GO**
**Source of truth:** `PERSONA-RESEARCH-v0.md` §7 · Companions: `SETTINGS-hub-v1-AC.md` (Bet E), `INSIGHT-IR-v1-AC.md` (Bet C), `PORTAL-CAPABILITY-MAP.md`
**Job:** freeze which home each major job lives in — **Sales Portal** vs **Admin Console** vs **Insightful** — so no job silently migrates and no Admin Console rebuild creeps in.

---

## A. Placement table (by job)

| Job / reporting | Home | Persona lean | Why | Evidence |
|---|---|---|---|---|
| Invoiced total, territory-scoped, export = screen | **Sales Portal** (Customers / Invoices / Reports / Dashboard) | Rep + Owner | The trusted transactional answer per filter | `DEMO-SURFACE-CONTRACT`; EBR-40/91 |
| Invoiced sales (C1) + accounts fading (S1) + team activity | **Sales Portal → Intelligence** | Owner-leaning (some rep) | Computational answers off the same spine, surfaced in-portal | `INSIGHT-IR-v1-AC` AC-1/2/3 |
| Full computational report (Money Map C1–C24, S1, NRR, seasonality, leakage…) | **Insightful CEO report** | CEO (deep) | The deep factory already runs off the same tables; the portal surfaces only a **thin subset** | spine §3, F3; Capability §1–2 |
| Enablement / territory & data access / display / export config | **Admin Console → Portal & Access hub (Bet E)** | Admin/ops | The config plane; who-edits split | `SETTINGS` AC-E1/E2; control-plane |
| Revenue definitions (locked) | **Admin Console** (visible read-only 🔒) | SuperCat + INSIGHT | Changing them changes what "sales" means | `SETTINGS` AC-E3 |
| **Feature-usage / adoption reporting** — org-level logins, active users, feature-category mix, user leaderboard | **Admin Console** *(placement candidate — cite pattern, NO build spec)* | Admin/ops + GTM | Adoption is a GTM metric ("No Portal Usage" scored in EBR decks), **not** a portal end-user answer | F7; SERV-2421/2336 (parallel Mixpanel adoption, spine App. A) |

---

## B. Frozen boundaries (the decisions this file locks)

### B1 — Owner/VP portal seat vs Insightful CEO factory
**Frozen:** the portal "CEO/Owner" persona is the **Owner/VP Sales** seat consuming a **thin C1/S1/team subset** in Intelligence. The **deep CEO intelligence factory is Insightful**, which already runs the full computational report off the same invoiced ledger (spine §3, F3). The portal does **not** try to be the deep CEO factory; it surfaces the subset that reconciles to the filtered total. *(Whether an owner is a real portal end-user at all — vs Owner/VP + Ops being the true portal pair — stays Open Question §9.3 for customer validation.)*

### B2 — Team activity strip (Portal) vs feature-usage/adoption (Admin Console candidate)
**Frozen seed rule:** *behavior floor tied to a commerce answer* → **Portal Intelligence** (the team activity strip: Q-R1 logins always + Q-18 eCat GMV leaderboard **or** Q-01 engagement fallback, behavior only, no named rep→revenue lead). *Org-wide adoption / usage analytics* (logins, active users, feature-category mix, user leaderboard as a GTM metric) → **Admin Console feature-usage report**, which is a **placement candidate only** — cite the pattern, **do not spec a build** this cycle. The two overlap; freezing the exact line is a Phase-3 job (research §9.5, §7 boundary note).

### B3 — Settings hub = Admin/ops home (Bet E), client vs SuperCat gates
**Frozen:** the ops persona's config home is the **Admin Console → Portal & Access hub** (Bet E, AC frozen). Client org-admin self-serves Enablement / Territory & data access (synch, totals) / Display / Reports & export (~18 self-service survivors, `SETTINGS` AC-E2). SuperCat superadmin holds the locked levers: **Revenue definitions (🔒)**, **Territory match mode** (`territory_access_via_rep_number`, pairs with Bet A — never alone), **Experiments** canaries (`SETTINGS` AC-E3/E4/E5). One persona, permission tier — matches `PERSONA-ONE-PAGERS.md` Persona 3.

### B4 — No Admin Console rebuild this cycle
**Frozen:** Bet F places jobs; it does **not** rebuild the Admin Console, does **not** re-triage the 134 toggles (diff against control-plane only), and does **not** author a Feature Usage Report build. The adoption/feature-usage report is named as a *placement candidate* so the boundary is documented, not built.

> **Phase 4 CLOSE note (2026-07-24):** the eCat **Feature Usage Report** — Admin Console · SuperCat-admin only · Mixpanel → BigQuery adoption analytics (Courchesne track) — is a **separate PM/eng project**, not a Bet F deliverable. Bet F documents its *placement* only; it does not build, spec, or add a portal nav item for it. The Bet F persona-IA demo carries a matching out-of-scope line. **Project home:** `SuperCat 4.0/PM/Admin-console/`.

---

## C. Portal ↔ Insightful spine (shared ledger, two presentations)

Both the portal and the Insightful factory read the **same invoiced ledger** — `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap, STRONG ceiling. The warehouse dashboard rollup is **not** validation ground truth; label it "invoiced ledger" (roadmap §2, `DEMO-SURFACE-CONTRACT` §4). The portal surfaces a subset (C1 + S1 + team strip); Insightful runs the full Money Map. Placement must never imply the portal is the complete picture (Rule R5, STRONG-not-FULL).

---

## D. What this file is not

- **Not** an Admin Console Feature Usage Report spec (B2/B4 — candidate/pattern only).
- **Not** a re-triage of the 134 toggles (consume control-plane; `SETTINGS` no-go).
- **Not** a new Bet C metric or a new Bet E section — it places existing shaped work.
- **Not** a GO unlock; Bet A validation (Track 1) unlocks GO.

---

*Phase 2 surface placement. Portal = transactional + thin Intelligence subset; Admin Console = config + adoption candidate; Insightful = deep CEO factory. No Admin Console rebuild, no feature-usage build. Isolation ON. Does not unlock Bet A GO.*
