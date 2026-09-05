# Track 2 — Persona + information architecture (not Bet A GO)

**Status:** **Shaped (Phase 2 pack) · Phase 3 SoT wire COMPLETE · Phase 4 HTML illustration COMPLETE + CLOSED · Phase 5 betting brief COMPLETE — READY FOR BETTING TABLE (2026-07-24)** — NOT "ready to build" · Opened 2026-07-21 after CTO feedback; Phase 1 research 2026-07-24; Phase 2 shape pack 2026-07-24; Phase 3 wired into spine §5 + roadmap + SPEC-GAP + contract/AC footnotes 2026-07-24; Phase 4 additive persona-IA illustration (`sales-portal-persona-ia-demo.html`) — per-tab persona dynamics landed + CLOSED + POLISHED to internal-demo craft 2026-07-24; Phase 5 betting brief finalized in `IA-RECOMMENDATION-v0.md` 2026-07-24. **Ready for the betting table (shaped, parallel Lane-1 — not a Rails GO).** Feature Usage Report (Admin Console adoption analytics) **deferred to a separate PM/eng project** — not part of Bet F.  
**Owner:** Kylor · **Isolation:** N/A (research / content experiments — not Rails Bet A)  
**Triggered by:** `CTO-FEEDBACK-2026-07-20.md` (“Visuals are distractors… separate specification for persona + IA”)

**Phase 2 shape pack (Bet F) — the five files that shape "who sees what first":**
- `PITCH-bet-f-persona-ia.md` — Shape Up pitch (problem / appetite / solution / rabbit holes / no-gos)
- `PERSONA-ONE-PAGERS.md` — CEO/Owner · Sales rep · Admin/ops (+ Manager folded)
- `IA-PRIORITY-MATRIX.md` — persona × surface must/nice/hide + five fail-closed AC rules
- `SURFACE-PLACEMENT.md` — Portal vs Admin Console vs Insightful (no Admin Console rebuild)
- `IA-RECOMMENDATION-v0.md` — betting-table memo + Phase-5 betting-brief stub

**Does not unlock GO.** Bet F is parallel to Bet A; validation (Track 1, `BUG-VALIDATION-PACK.md`) unlocks `ISOLATION OFF — GO on EBR-40`, not this pack.

---

## Why this track exists

Bet A is a **trust / filter / metric-law** fix. Dashboard polish, answer-first chrome, Intelligence previews, and Settings hub mocks are useful later — and distracting when the decision is “do these old EBRs still bite?”

CTO ask: identify **user personas**, recommend **information architecture** (what they want to see, in priority order), and continue **A/B-style testing** of content, grouping, aggregation, and annotation with customers.

This track **does not** unlock `ISOLATION OFF — GO on EBR-40`. Track 1 (`BUG-VALIDATION-PACK.md`) does.

---

## Relationship to Bet A / B / C

| Work | Track | Unlocks GO? |
|---|---|---|
| Territory / export / quotes validation + fix | 1 — Trust | Yes (after readout) |
| Persona ID + IA priority + content A/B | **2 — This doc** | No |
| Answer-first list tabs (Bet B shell) | May reuse Track 2 findings | No by itself |
| Intelligence (Bet C) | After trusted totals | Separate GO |
| Dashboard redesign | Out of Bet A | Separate shaping |

List-tab “hero = answer, list = evidence” experiments are **content/IA tests** for this track — not proof that Bet A is done.

---

## Method (lightweight)

1. **Personas (draft)** — start from portal jobs, not job titles:
   - Field rep (“my book / my customers”)
   - Regional / sales manager (“what the rep sees / woodshed”)
   - Sales ops / admin (“export reconciles / config”)
2. **Jobs-to-be-done per surface** — one primary question per tab (already sketched in demos; validate with customers).
3. **IA recommendation** — ordered: what must be above the fold vs secondary vs hide; explicitly separate **invoiced** vs **backlog** vs **quotes**.
4. **Customer A/B** — small content variants (grouping, aggregation labels, annotation), not a full UI redesign. Share with 2–3 impacted accounts after Track 1 names who still hits the bugs.
5. **Spec out** — write a short IA memo (new file) when (1)–(4) have evidence; do not fold into Bet A TRD.

---

## Out of scope for this stub

- Running interviews this session
- Changing production Rails
- Shipping What’s broken as product nav
- Treating the internal demo Dashboard as the IA recommendation

---

## Next concrete steps (when ready)

- [x] Draft 3 persona one-pagers (goals, primary questions, trust failures) — Phase-1 memo → **frozen in `PERSONA-ONE-PAGERS.md`** (Phase 2)
- [x] Priority IA table: what to show first per persona per surface — **done in `IA-PRIORITY-MATRIX.md`** (Phase 2)
- [x] Freeze surface placement (Portal / Admin Console / Insightful) — **done in `SURFACE-PLACEMENT.md`** (Phase 2)
- [x] Write `IA-RECOMMENDATION-v0.md` (betting-table memo, docs = SoT) — **done** (Phase 2)
- [x] **Phase 3 — wire the recommendation into SoT / spine + refresh roadmap** — **done 2026-07-24**: spine §5 Bet F + router note; roadmap §5b + bet map + annex; `SPEC-GAP-CHECKLIST` Bet F rows; `DEMO-SURFACE-CONTRACT` illustration/ordering note; `INSIGHT-IR-v1-AC` + `SETTINGS-hub-v1-AC` footnotes; `05d` reboot + `README-RUN-ORDER`
- [x] **Phase 4 (optional) — HTML illustration** of role-aware defaults — **done + CLOSED 2026-07-24**: `design-system/app/sales-portal-persona-ia-demo.html` (clone of internal demo + additive persona layer, per-tab persona dynamics via `currentPersona` + `applyPersonaToView` + `BETF_VIEW_MATRIX`) · runbook `BET-F-PERSONA-DEMO-RUNBOOK.md`. Illustration only; docs remain SoT; does not unlock GO. **Feature Usage Report (Admin Console adoption analytics) explicitly OUT of scope — separate PM/eng project.**
- [x] **Phase 5 — betting brief** (Orchestrator owns final PASS): finalized the brief under `## Betting brief` in `IA-RECOMMENDATION-v0.md` — **ready for the betting table** (shaped, parallel Lane-1; not a Rails GO) 2026-07-24
- [ ] **Customer A/B still open** — rep default home (Customers vs Invoices); is CEO a portal end-user; IA depth (hero-priority vs nav landing); adoption/feature-usage boundary; Manager fold vs split. Recruit from Track-1 impact list (wwjc / sarreid / cci / ufi), not random.

---

## Phase 1 complete — Bet F persona research (2026-07-24) — *historical*

> **Historical (superseded by Phase 2/3 below).** This block's "Research-in-progress" label is
> retained for lineage only; the live status is **Shaped (Phase 2) · Phase 3 wired** (see header
> and the Phase 2/3 sections below). Do not read "Research-in-progress" as the current state.

Evidence-backed persona memo written: `cycle-03-outputs/PERSONA-RESEARCH-v0.md` (PASS).

- 3 personas grounded (Sales rep = only ticket-grade evidence; CEO/Owner = mostly
  Insightful audience, thin portal surface; Admin/ops = config + reconciliation).
- Manager = **fold under CEO/Owner** for v0 (open question for Orchestrator; no 4th
  one-pager invented).
- 5 fail-closed contradictions + surface placement seeds (Portal / Admin Console /
  Insightful) + ≤7 open questions for the Orchestrator.
- Does **not** unlock Bet A GO; parallel to Bet A. Next (now done): Orchestrator Review Card → Phase 2 shape pack.

---

## Phase 2 complete — Bet F shape pack (2026-07-24)

**Status: Shaped (Phase 2 pack)** — NOT "ready to build". Five files written under `cycle-03-outputs/`:
`PITCH-bet-f-persona-ia.md`, `PERSONA-ONE-PAGERS.md`, `IA-PRIORITY-MATRIX.md`,
`SURFACE-PLACEMENT.md`, `IA-RECOMMENDATION-v0.md`.

- **Recommendation:** role-aware defaults over one shared surface (hero-priority-per-surface,
  not a nav fork). Default homes: rep → Customers · owner → Intelligence · ops → Settings hub
  (all HYPOTHESIS, pending customer A/B).
- **Locks honored:** 3 personas; Manager folded under CEO/Owner; Admin = one persona, permission
  tier; CEO portal seat = Owner/VP (deep CEO = Insightful); adoption = Admin Console candidate
  (no build); COPY-AUDIT voice; parallel to Bet A.
- **Five fail-closed rules** promoted to AC-grade (assigned-book / suppress rep→revenue < Tier 2 /
  revenue defs locked / client vs SuperCat gates / STRONG-not-FULL), each inheriting a standing AC.
- **Does not** unlock Bet A GO, touch Bet A AC / TRD / Friday demos, spec an Admin Console
  feature-usage build, or edit the spine/roadmap (Phase 3). No HTML (Phase 4 optional).
- **Next:** Orchestrator Review Card — Phase 2 → then Phase 3 (wire SoT/spine, separate worker);
  customer A/B remains the open input.

---

## Phase 3 complete — Bet F SoT wire (2026-07-24)

**Status: SoT wire COMPLETE** — Bet F is now visible in the spine + roadmap and footnoted into the
contracts/ACs. Isolation held; no Bet A contamination. Files touched:

- `00-PROGRAM-SPINE.md` — new **Bet F** section in §5 (problem / appetite / elements / recommendation /
  no-gos), an F1/F7 + IA-track **router note**, header + footer stamps.
- `PROGRAM-ROADMAP-cycle03.md` — Bet F row in the bet map (parallel research→shaped, no GO), a **§5b**
  shaped summary, and annex-index pointers.
- `SPEC-GAP-CHECKLIST.md` — **Bet F** section (F1–F7): shaped pack ✅, SoT wire ✅, customer A/B open,
  Phase 4 HTML optional, Phase 5 stub, **not build-ready**.
- `DEMO-SURFACE-CONTRACT.md` — light note: persona priority / default homes are **illustration + ordering
  authority for future Bet B work**, not a Friday-demo HTML change; nav + primary jobs unchanged.
- `INSIGHT-IR-v1-AC.md` + `SETTINGS-hub-v1-AC.md` — short footnotes (owner-leaning surface / ops home;
  RS-01 still gated; R3/R4 = the hub's gates). No AC bodies rewritten.
- `05d-ORCHESTRATOR-REBOOT-cycle03.md` + `README-RUN-ORDER.md` — Bet F added to reboot map + run order
  (parallel, no GO; Phase 4/5 next).

**Held as locked:** parallel to Bet A; does **not** unlock GO; no Bet A TRD / `FILTER-TRUTH-AC` body edits;
no Friday-demo HTML; no Admin Console feature-usage build; no Jira writes.
Customer A/B on default homes stays open. Phase 5 betting brief remains a stub (Orchestrator owns final PASS).

- **Next:** Phase 5 betting brief; customer A/B recruiting (wwjc / sarreid / cci / ufi).

---

## Phase 4 complete — Bet F HTML illustration (2026-07-24)

**Status: Illustration built (optional phase) — NOT a build unlock.** New file only:
`design-system/app/sales-portal-persona-ia-demo.html`, cloned from `sales-portal-internal-demo.html`
with an **additive** Bet F layer on top (same `.kshell`, tokens, nav order, COPY-AUDIT voice — a shared
surface, not a forked product). Runbook: `BET-F-PERSONA-DEMO-RUNBOOK.md`.

- **Additive delta only:** title + always-visible banner (*Illustration only · docs are SoT · does not
  unlock Bet A GO · Friday demos untouched*); persistent persona switcher (Sales rep · Owner/VP · Admin/ops);
  on-switch land on the recommended default home (HYPOTHESIS-labeled) — rep → Customers · owner → Intelligence ·
  ops → Settings — with the must-see lead per `IA-PRIORITY-MATRIX.md`; and ≥2 always-on fail-closed cues
  (R1 empty-territory → never whole-org; R3/R4 Settings 🔒), plus a dynamic per-persona cue (R1 / R2 / R3–R4).
- **Held as locked:** did **not** modify `sales-portal-internal-demo.html`, `sales-portal-bet-a-pitch-demo.html`,
  or any other existing `sales-portal-*.html`; did not touch `supercat-code/`; did not regenerate the HTML from
  scratch. Docs remain SoT; default homes stay HYPOTHESIS; does not unlock Bet A GO.

### Phase 4 FIX — per-tab persona dynamics (2026-07-24)

Prior Phase 4 FAIL: persona only drove a default-home jump + one global note (one persona → one tab).
Fix makes the persona reshape **every** surface via a persistent `currentPersona` and a new
`applyPersonaToView(persona, view)` called from **both** `setPersona()` **and** `nav()` / `navReports()`.
`setPersona` still jumps to the recommended default home once, but any tab clicked afterward re-themes to
the active persona (no stale owner copy on a rep session). A per-view cue lives **ON the active tab** showing
that surface's rank for the persona — **MUST / nice / not-your-landing / HIDE / teaching** — driven by
`IA-PRIORITY-MATRIX.md` §A × R1–R5; demote/hide surfaces are visibly dimmed. Runbook updated with a walk that
switches persona in-place on a tab, then clicks across ≥3 tabs per persona. Surgical StrReplace only; the two
Friday demos and all other `sales-portal-*.html` untouched.

### Phase 4 CLOSE (2026-07-24)

Accepted current HTML as the Phase 4 illustration bar — per-tab persona dynamics (`currentPersona` +
`applyPersonaToView` + `BETF_VIEW_MATRIX`) already prove the 4-min walk re-themes **every** tab for all three
personas. Close-out was docs + one out-of-scope chrome line only:

- **Runbook** — added an explicit note that the eCat **Feature Usage Report** (Admin Console · SuperCat-admin
  only · Mixpanel → BigQuery / Courchesne track) is a **separate PM/eng project**, not part of this Bet F demo.
- **HTML** — one small "Out of scope" line on the existing Bet F banner chrome (no new nav item, KPI dashboard,
  charts, or leaderboard).
- **Deferred:** Feature Usage / adoption analytics UI, Admin Console analytics dashboard, Mixpanel/BigQuery work,
  and any new adoption nav item → **separate project, later**. Phase 4 does **not** build, port, or clone it.
- **Next:** Phase 5 betting brief (Orchestrator-owned). Did **not** modify the Friday demos
  (`sales-portal-bet-a-pitch-demo.html`, `sales-portal-internal-demo.html`) or any other `sales-portal-*.html`;
  no `supercat-code/`, Rails, BQ, taxonomy, or Jira writes. Does not unlock Bet A GO.

### Phase 4 POLISH — match internal-demo craft (2026-07-24)

Prior Phase 4 CLOSE passed on docs but **FAILED on craft**: the persona demo looked like a review overlay
(stacked banner + note + fail-closed strip + out-of-scope strip pushing real content down; fat per-tab
MUST/HIDE billboard above the H1; opacity/grayscale dimming of demote/hide surfaces). Polished to the
internal-demo bar — **per-tab persona logic unchanged** (`currentPersona`, `BETF_VIEW_MATRIX`,
`applyPersonaToView` on `setPersona` + `nav`/`navReports`):

- **One compact persona control** moved into the **topbar-right** ("View as" segmented switch) — the four
  stacked chrome bars are gone.
- **Per-tab cue** is now **one quiet line under the page title** (small rank pill + persona + lead + rule;
  `default home · HYPOTHESIS` tag on the persona's home), not a billboard above the title.
- **All view dimming removed** (opacity/grayscale) — full density on every tab; the pill color carries rank.
- Long rationale (fail-closed R1–R5, default-home hypotheses, out-of-scope Feature Usage) moved to the
  **runbook + a one-line footer**; illustration disclaimer is one short line.
- **EDIT-ONLY isolation held:** only `sales-portal-persona-ia-demo.html`, `BET-F-PERSONA-DEMO-RUNBOOK.md`,
  and this note. Friday demos and all other `sales-portal-*.html` untouched; no `supercat-code/`; no Feature
  Usage UI; no Phase 5. Open side-by-side with `sales-portal-internal-demo.html` — first screen reads as the
  same product + a persona switch.

---

*Parallel to Bet A. Does not authorize build. Does not replace validation.*
