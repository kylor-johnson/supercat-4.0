# PITCH — Bet F · Persona-priority IA

**Date:** 2026-07-24 · **Author:** shaping agent · **Phase:** 2 of Bet F (shape pack) · **Lane:** 1 Legible/UX (IA layer)
**Isolation:** ON · **Does not unlock Bet A GO** · Parallel to Bet A
**Appetite:** Small batch (1–2 weeks) — research already done (Phase 1 PASS); this pack shapes; optional HTML is Phase 4
**Phase-1 SoT:** `PERSONA-RESEARCH-v0.md` (PASS) · **Doctrine:** `00a-DOCTRINE-shapeup-ddd-affinity.md` §1.2–1.6

---

## 0. One-line frame

Bet F decides **who sees what first** in the Sales Portal — **role-aware defaults over one shared surface**, not a forked role-based product. It reinforces Bet A's appetite; it does not gate, rewrite, or replace it.

---

## 1. Problem

**Baseline story (the god-view that betrays the rep).**
Today the portal is a single org-wide "god view": one sidebar, one org switcher, no role split (confirmed in `sales-portal-internal-demo.html` nav — Dashboard → Customers → Orders → Invoices → Reports → Intelligence → [Later] Settings → What's broken). Every persona lands on the same Dashboard and sees the same chrome.

A **sales rep** opens the portal to answer one question — "how much did **my** customers buy, and what did we invoice in **my** territory?" — picks a territory, and **still sees the wrong book** (whole org / none / someone else's accounts). So they distrust every number and rebuild it in Excel. This is validated live: on wwjc, `cmallon` YTD is 1,404 / $1.46M but does not scope to territory `105:1 Gigi Lane` (710 / $777k) [EBR-40; `PERSONA-RESEARCH-v0` §2.4]. The dashboard variant has been stalled since 2022 [EBR-212]. Export/period drift compounds it [EBR-91].

The same single surface that betrays the rep is *fine* for an **owner** who genuinely wants the whole org — so the fix is not "one more filter," it is **whose defaults win on which surface**. And a third job hides underneath both: an **admin / sales ops** person who just needs the portal to turn on for the right people and the export to match the screen, and who today can't answer "why can't this user see the portal?" without a SuperCat ticket (134 toggles / 6 layers / 39 YAML flags, no admin surface) [F10; `PERSONA-RESEARCH-v0` §4].

**Who feels it, how often, why now.** The rep feels it every filtered session (F1 — the portal is the KPI shelf; trust breaks when territory lies). The owner feels it second-order — an Intelligence surface built on an untrustworthy total is untrustworthy at the root. Ops feels it as a ticket queue. It matters *now* because Bet A is about to fix the total's truth; Bet F makes sure the *right persona's* question is the first thing each surface answers once that total is trustworthy — otherwise we ship a trustworthy number buried in a god-view that still makes the rep scroll past the owner's org-wide chrome.

---

## 2. Appetite

**Small batch (1–2 weeks of shaping) — this pack is the deliverable.**

- Persona research is **already done and PASSED** (`PERSONA-RESEARCH-v0.md`). This phase does **not** re-run research or interviews.
- The payout is **documents + an IA recommendation a betting table can read** — the SoT is the five markdown files, not code and not a UI.
- **Optional HTML illustration is Phase 4** — explicitly not built now.
- This is **not** a Dashboard redesign, **not** Rails, **not** a nav fork. It is the smallest artifact that freezes "who sees what first" so Bet B (answer-first shell) and Bet E (control plane) can honor it.

Why this much time is the right price: the hard thinking (evidence, contradictions, fail-closed rules) is finished in Phase 1. What remains is to *freeze* it into betting-grade priority tables and one-pagers — a shaping job, not a build.

---

## 3. Solution (elements)

The shaped solution is **role-aware defaults over a shared surface** — the same seven surfaces every persona already has, with a recommended default landing and a hero-priority order per persona, plus fail-closed rules so one surface can serve two personas honestly. Concretely:

1. **Three personas v0 (locked):** **Sales rep** · **CEO/Owner** (= Owner/VP Sales for the portal seat) · **Admin / sales ops**. Manager **folds under CEO/Owner** (oversight + scoping) for v0. Admin is **one persona with a permission tier** (client org-admin vs SuperCat), not two one-pagers. → `PERSONA-ONE-PAGERS.md`.

2. **Persona × surface priority matrix** — for Dashboard · Customers · Orders · Invoices · Reports · Intelligence · Settings (+ What's broken = teaching only), each persona gets **must-see / nice / hide**. This is the ordering law Bet B reads for each surface's lead answer. → `IA-PRIORITY-MATRIX.md`.

3. **Five fail-closed rules (AC-grade given/when/then)** — promoted from research §6 so Bet B and Bet E can honor them: assigned-book default; suppress named rep→revenue below Tier 2; revenue definitions visible-but-locked; client vs SuperCat gates; STRONG single-feed caveat (never FULL). → `IA-PRIORITY-MATRIX.md` §rules.

4. **Surface placement** — Portal vs Admin Console vs Insightful for each major job, freezing: Owner/VP portal seat vs deep CEO Insightful factory; team activity strip (Portal) vs feature-usage/adoption (Admin Console candidate — **no build spec**); Settings hub = Admin/ops home (Bet E) with client vs SuperCat gates; **no Admin Console rebuild this cycle**. → `SURFACE-PLACEMENT.md`.

5. **Role-aware defaults, NOT a forked UI** — the DDD read (research §6) is that these are permission/bounded-context boundaries, not five products. v0 ships as *what's shown first + what's gated* on one shared surface. Whether the recommended default home is nav-level or hero-priority-per-surface is captured as the standing customer-A/B question (research §9.7), with the recommended default = **hero-priority-per-surface** (least-forking option that still serves persona priority). → `IA-RECOMMENDATION-v0.md`.

**Copy discipline:** every client-facing label uses the `COPY-AUDIT` approved list — *invoiced total*, *accounts fading*, *the list and the total*, *only your territory's customers*. Banned as client copy: *hero*, *True Topline*, *Quietly dying*, *the book*, SaaS jargon. Internal capability IDs (C1, S1, Q-R1) appear only in parentheses for eng traceability.

---

## 4. Rabbit holes (patched)

| Risk (rabbit hole) | Patch / decision already made |
|---|---|
| **Manager becomes a fourth persona** and forks the model | **Fold under CEO/Owner** for v0 (oversight + rep-style scoping). No manager-specific job/question/trust-failure exists that CEO/Owner + rep don't already hold. A fourth one-pager only if Phase-2 interviews produce a manager job the other two can't hold (research §5, §9.1). |
| **"The CEO isn't really a portal user"** paralyzes the persona | Documented split (locked): portal "CEO/Owner" = **Owner/VP Sales** (thin C1/S1/team subset); the deep CEO factory = **Insightful**. The portal seat is real; the deep report home is Insightful (research §3, §11; `SURFACE-PLACEMENT.md`). |
| **Nav fork / role-based product** — building three portals | v0 = **role-aware defaults over one shared surface** (hero-priority-per-surface recommended). Nav-level role landing is a customer-A/B question, not a v0 build (research §9.7). |
| **Admin Console rebuild** creeps in via the ops persona | Ops persona's config home = **Bet E Portal & Access hub** (already shaped, AC frozen). Feature-usage/adoption is an Admin Console **placement candidate only — cite the pattern, no build spec**. No re-triage of 134 toggles (research §7, §8; `SETTINGS-hub-v1-AC`). |
| **Contaminating Bet A** — this pack drifting into a filter fix or a new AC | Bet F is **parallel**; it reuses Bet A's rep/ops trust failures as *reinforcement* of the appetite, adds **no new Bet A AC**, and **does not** unlock `ISOLATION OFF — GO on EBR-40`. Validation (Track 1) unlocks GO, not this. |
| **Inventing customer verbatims** to justify default homes | No raw interview transcripts exist in the reading set (research §0.8, Annex provenance note). Default homes are labeled **HYPOTHESIS / recommended pending feedback**; true verbatims are marked as the next Phase-3 input. |

---

## 5. No-gos (explicit)

- **No** rewrite of `FILTER-TRUTH-AC.md`, the Bet A TRD, or any Bet A AC.
- **No** edits to `design-system/app/sales-portal-bet-a-pitch-demo.html` or `sales-portal-internal-demo.html` (Friday demos).
- **No** `ISOLATION OFF — GO` unlock on EBR-40, Bet A, or Bet E; **no** Rails / `supercat-code/` edits.
- **No** Admin Console **Feature Usage Report build spec** — placement candidate / pattern citation only.
- **No** fourth (Manager) persona one-pager invented this cycle.
- **No** nav fork / forked role-based product — role-aware defaults only.
- **No** HTML illustration this phase (Phase 4 optional).
- **No** new metrics outside `PORTAL-CAPABILITY-MAP` / `INSIGHT-IR-v1-AC`; no margin/COGS/AR; no RS-01 named-rep-revenue lead; no EBR-772/776; no FULL completeness claim.
- **No** inventing customer verbatims; **no** Jira writes (read-only).
- **No** Phase-3 spine/roadmap edits (separate worker).

---

## Done means

The five deliverables (`PERSONA-ONE-PAGERS.md`, `IA-PRIORITY-MATRIX.md`, `SURFACE-PLACEMENT.md`, `IA-RECOMMENDATION-v0.md`, + this pitch) are on disk, internally consistent with `PERSONA-RESEARCH-v0.md` and the Orchestrator locks, in `COPY-AUDIT` voice for client-facing strings, with `IA-PERSONA-TRACK.md` updated to **Shaped (Phase 2 pack)** — not "ready to build." Customer A/B on default homes remains open. This pack is the SoT; HTML is optional and later.

---

*Shape Up pitch for the betting table. Comments poke holes — they don't approve build. Isolation ON. Does not unlock Bet A GO.*
