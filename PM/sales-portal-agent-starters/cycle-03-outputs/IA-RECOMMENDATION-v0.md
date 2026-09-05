# IA RECOMMENDATION v0 — Bet F (persona-priority IA)

**Date:** 2026-07-24 · **Phase:** 2 shape pack · **Isolation:** ON · **Does not unlock Bet A GO**
**For:** the betting table (read in ≤5 minutes) · **Source of truth:** `PERSONA-RESEARCH-v0.md` (Phase 1 PASS)
**Pack:** `PITCH-bet-f-persona-ia.md` · `PERSONA-ONE-PAGERS.md` · `IA-PRIORITY-MATRIX.md` · `SURFACE-PLACEMENT.md` · this memo

---

## 1. Summary recommendation

Ship **role-aware defaults over one shared surface** — not a forked role-based product. The portal keeps its seven surfaces and one nav; Bet F adds a **recommended default home + a hero-priority order per surface per persona**, governed by five fail-closed rules.

- **Personas v0 (locked):** **Sales rep** · **CEO/Owner** (portal seat = Owner/VP Sales) · **Admin / sales ops**. Manager **folds under CEO/Owner**; Admin is **one persona with a permission tier**.
- **Recommended default homes (HYPOTHESIS, pending customer A/B):** rep → **Customers** (Invoices runner-up); owner → **Intelligence** (Reports secondary); ops → **Settings hub** (Reports/Invoices for reconciliation).
- **IA depth (recommended):** implement persona priority as **hero-priority-per-surface**, the least-forking option — *not* a nav fork. A nav-level role landing is a customer-A/B question, not a v0 build (research §9.7).
- **Five fail-closed rules** (`IA-PRIORITY-MATRIX` §B) let one surface serve two personas honestly: assigned-book default (R1); suppress named rep→revenue below Tier 2 (R2); revenue definitions visible-but-locked (R3); client vs SuperCat gates (R4); STRONG single-feed caveat (R5). Each inherits a standing AC — **no new metric law**.
- **Placement frozen:** portal = transactional + thin Intelligence subset; Insightful = deep CEO factory; Admin Console = config (Bet E) + adoption *candidate only, no build* (`SURFACE-PLACEMENT`).
- **Copy:** client-facing labels from `COPY-AUDIT` only (invoiced total / accounts fading / the list and the total / only your territory's customers).

---

## 2. What "done" means for Bet F

**Done = the docs are the SoT.** The five files above are on disk, internally consistent with `PERSONA-RESEARCH-v0` and the Orchestrator locks, in COPY-AUDIT voice for client-facing strings, with `IA-PERSONA-TRACK` marked **Shaped (Phase 2 pack)**. There is no code, no UI, and no Bet A AC change in this definition of done.

- **Fully baked now:** the persona set, the priority matrix, the fail-closed rules, and the placement boundaries — a betting table can read them and decide.
- **Optional later (Phase 4):** an HTML illustration of the role-aware defaults. Not built this phase; not required for done.
- **Phase 3 (separate worker):** wire the recommendation into the SoT / spine and refresh the roadmap. Not this pack.

---

## 3. What still needs customer A/B (open, not assumed)

No raw customer interview transcripts exist in the reading set (research §0.8) — so these stay open and are the recruiting targets for Phase 3 (pull from the Track-1 impact list: wwjc, sarreid, cci, ufi — research §9.6):

1. **Rep default home** — Customers vs Invoices (research §9.2). Recommended: Customers, pending one owner/VP + one lead-rep reaction.
2. **Is the CEO a portal end-user at all,** or is the true portal pair Owner/VP + Ops, with the CEO served by Insightful? (research §9.3)
3. **IA depth** — hero-priority-per-surface (recommended) vs a nav-level role landing (research §9.7).
4. **Adoption/feature-usage boundary** — exact line between the Portal team activity strip and an Admin Console usage report (research §9.5; `SURFACE-PLACEMENT` B2).
5. **Manager fold vs split** — fold holds for v0; a fourth one-pager only if interviews surface a job CEO/Owner + rep can't hold (research §9.1).

---

## 4. Explicit non-authorizations

- **Does NOT unlock Bet A GO.** Bet F is parallel; Bet A validation (Track 1, `BUG-VALIDATION-PACK`) unlocks `ISOLATION OFF — GO on EBR-40` — this pack does not.
- **No new Bet A AC**; no rewrite of `FILTER-TRUTH-AC`, the Bet A TRD, or the Friday demos.
- **No Admin Console feature-usage report build spec** (placement candidate only). The eCat **Feature Usage Report** (Admin Console · SuperCat-admin only · Mixpanel → BigQuery / Courchesne track) is a **separate PM/eng project** — Bet F (and its Phase 4 demo) documents placement only and does not build, port, or add a portal nav item for it.
- **No nav fork / forked product**; **no** new metrics, margin, RS-01 lead, or FULL claim; **no** EBR-772/776; **no** Jira writes; **no** HTML this phase; **no** Phase-3 spine/roadmap edits.

---

## Betting brief

*Ready for the betting table. Read-in-5 above; this is the one-screen bet.*

- **What Bet F is.** It shapes **who sees what first** in the Sales Portal — **role-aware defaults over one shared surface** (recommended default home + hero-priority order per persona, five fail-closed rules), not a forked role-based product and not a new filter.
- **Appetite.** Small batch — the **docs are the source of truth** (five files); research was done and passed in Phase 1. The optional **HTML illustration is done** (`sales-portal-persona-ia-demo.html`) — a picture of the bet, not part of the deliverable.
- **What the room is asked to acknowledge.** Accept this as a **shaped, parallel Lane-1 (Legible/UX) recommendation** — "yes, this is the right who-sees-what-first frame to build Bet B/E against later." It is **not a Rails build GO** and needs no vote to unlock code.
- **What it informs.** Gives **Bet B** its per-surface ordering law and **confirms Bet E** as the admin/ops home; **reinforces Bet A's appetite** (fixing the total's truth) without gating or rewriting it.
- **Explicit non-authorizations.** Does **not** unlock `ISOLATION OFF — GO on EBR-40`; **no** Dashboard redesign; **no** Admin Console Feature Usage build (separate PM/eng project); default homes (rep → Customers · owner → Intelligence · ops → Settings hub) stay **HYPOTHESIS pending customer A/B**.
- **Pointers.** Pack: `PITCH-bet-f-persona-ia.md` · `PERSONA-ONE-PAGERS.md` · `IA-PRIORITY-MATRIX.md` · `SURFACE-PLACEMENT.md` · this memo. Illustration only: `design-system/app/sales-portal-persona-ia-demo.html` (`BET-F-PERSONA-DEMO-RUNBOOK.md`).

---

*Phase 2 IA recommendation. Docs = SoT; HTML optional later. Default homes = HYPOTHESIS pending customer A/B. Isolation ON. Does not unlock Bet A GO.*
