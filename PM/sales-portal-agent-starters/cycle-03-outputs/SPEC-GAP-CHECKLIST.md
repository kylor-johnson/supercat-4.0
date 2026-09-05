# Spec gap checklist — Sales Portal program (cycle-03)

**Date:** 2026-07-17 · **Updated:** 2026-07-24 (Bet A GO; sprint pack + triage board)  
**Isolation:** **OFF for Bet A only** — `ISOLATION OFF — GO on EBR-40` · C/E/F still gated  
**Eng entrypoint (SoT):** **`ENG-HANDOFF-bet-a-b-c-e.md`** (A+B+C+E — cites the ACs below)  
**Sprint:** `SPRINT-PACK-bet-a.md` · **Triage:** `BET-TRIAGE-BOARD.md` · **CTO:** `CTO-FEEDBACK-2026-07-24.md`  
**Detail:** `TECHNICAL-PLAN.md` · `FILTER-TRUTH-AC.md` · `LIST-TABS-AC.md` · `IR-v1-QUERIES.md` · `DEMO-SURFACE-CONTRACT.md` · `SETTINGS-hub-v1-AC.md` · `SHIP-READINESS-bet-e.md`

**Legend:** ✅ Done · 🟡 Partial · ❌ Missing · 🚫 Blocked · 👤 Human gate

---

## Program gates

| # | Item | Status | Artifact / next step |
|---|---|---|---|
| G1 | Customer feedback (optional) | 👤 | Nice-to-have |
| G2 | Post-feedback AC table | 🟡 | Skip until session |
| G3 | AC freeze (Bet C) | 🟡 | Internal OK; re-open if feedback moves heroes |
| G4 | Betting table | 🟡 | A **GO’d**; confirm C next; E Wave 0–1 ride-with-A still open |
| G5 | Isolation lift (Bet A) | ✅ | `ISOLATION OFF — GO on EBR-40` (2026-07-24) · C/E still need own GO |
| G6 | Jira handoff | ✅ | SERV-2447/2448/2449 linked + sprint June 2026; EBR-40/91 → Approved; no hygiene comments |

---

## Bet A — Filter + metric law

| # | Item | Status | Artifact |
|---|---|---|---|
| A1 | Pitch | ✅ | `PITCH-phase1-filter-metric-law.md` |
| A2 | Unified AC | ✅ | `FILTER-TRUTH-AC.md` |
| A3 | Eng diagnosis file:line in eng entrypoint | ✅ | **`ENG-HANDOFF` §C.1** — AC→code map (warehouse_access.rb:424–434, territory_to_ship_to_bridge.rb:25/37, ecat_customers_controller.rb:294) from FIX-diagnosis |
| A4 | Demo surfaces show filter/export/quote truth | ✅ | Invoices = Bet A proof; Customers/Orders dense |
| A5 | What’s broken plain-English (not AC wall) | ✅ | Last nav · non-shipping teaching |
| A6 | List-tab Given/When/Then | ✅ | **`LIST-TABS-AC.md`** |
| A7 | Build | 🟡 | GO lifted — eng via SERV; verify on wwjc |

---

## Bet B / demo surfaces

| # | Item | Status | Note |
|---|---|---|---|
| B1 | UX brief | ✅ | List-tab density bar noted |
| B2 | Internal HTML | ✅ | Answer-first list heroes · Dashboard default · What’s broken last |
| B3 | Demo → prod contract | ✅ | **`DEMO-SURFACE-CONTRACT.md`** — four list tabs eng-cite |
| B4 | List-tabs AC | ✅ | **`LIST-TABS-AC.md`** |
| B5 | Feedback script | ✅ | Optional |

---

## Bet C — IR v1

| # | Item | Status | Artifact |
|---|---|---|---|
| C1 | AC | ✅ | `INSIGHT-IR-v1-AC.md` |
| C2 | Stamped SQL sarreid | ✅ | `IR-v1-QUERIES.md` |
| C3 | Customers → S1 hook | ✅ | Quietly dying → `#intel-s1` |
| C4 | Grade orgs cci+kll re-stamp | ❌ | 👤 Before build (human/data gate) |
| C5 | Mixpanel CORROBORATED map | ✅ | **`ENG-HANDOFF` §E.3** — explicit degrade-default (status NONE→PRESENT→CORROBORATED; depth renders only when CORROBORATED); map is build-time data task |
| C6 | JSON read-model | ✅ | **`ENG-HANDOFF` §E.2** — org_id → heroes + AC-5 provenance schema |
| C7 | Build | 🚫 | After G5 |

---

## Bet D / E

| # | Item | Status | Artifact / next step |
|---|---|---|---|
| D1 | LLM park | ✅ | `PARK-llm-ebr-772-776.md` |
| E1 | Control-plane triage | ✅ | `PORTAL-SETTINGS-CONTROL-PLANE.md` |
| E2 | Demo hub IA + Settings view | ✅ | `SETTINGS-hub-v1-DEMO-SPEC.md` · internal-demo |
| E3 | Build AC (E0–E6) | ✅ | **`SETTINGS-hub-v1-AC.md`** |
| E4 | Ship readiness | ✅ | **`SHIP-READINESS-bet-e.md`** — NOT READY TO BUILD until GO |
| E5 | Confluence 1813676033 ~47 Org rows | 👤 | Before Wave 2 hub |
| E6 | Dormant-wired ship/cut (4 flags) | 👤 | Product call |
| E7 | Betting table include E | 👤 | Wave 0–1 may ride with A |
| E8 | Isolation lift | 🚫 | `ISOLATION OFF — GO on Bet E` |

---

## Bet F — Persona-priority IA (parallel; **not build-ready**)

| # | Item | Status | Artifact / next step |
|---|---|---|---|
| F1 | Persona research (Phase 1) | ✅ | `PERSONA-RESEARCH-v0.md` (PASS) |
| F2 | Shape pack complete (Phase 2) | ✅ | `PITCH-bet-f-persona-ia.md` · `PERSONA-ONE-PAGERS.md` · `IA-PRIORITY-MATRIX.md` · `SURFACE-PLACEMENT.md` · `IA-RECOMMENDATION-v0.md` |
| F3 | SoT wire (Phase 3) | ✅ | Spine §5 Bet F · roadmap §5b/bet map · this checklist · contracts/ACs footnoted |
| F4 | Customer A/B on default homes | ❌ 👤 | **Open** — rep Customers-vs-Invoices; is CEO a portal end-user; IA depth (hero-priority vs nav landing); adoption/feature-usage boundary; Manager fold vs split. Recruit from wwjc/sarreid/cci/ufi |
| F5 | Phase 4 HTML illustration | 🟡 (optional) | Not built; not required for done |
| F6 | Phase 5 betting brief | ✅ | Finalized under `## Betting brief` in `IA-RECOMMENDATION-v0.md` — ready for the betting table (shaped, parallel Lane-1; not a Rails GO) |
| F7 | Build | 🚫 | **Not build-ready** — parallel to Bet A; does not unlock GO; Bet A validation (Track 1) unlocks GO |

---

## Elite order

1. Show Dashboard → **Invoices (Bet A)** → Customers → Orders → Reports → Intelligence; Settings = Bet E shaped (skip unless asked); What’s broken only if asked  
2. Eng entrypoint = **`ENG-HANDOFF-bet-a-b-c-e.md`** (A+B+C+E; cites `DEMO-SURFACE-CONTRACT` + `LIST-TABS-AC` + FILTER/IR AC + `SETTINGS-hub-v1-AC` / `SHIP-READINESS-bet-e`)  
3. 👤 Betting table A then C (+ E?)  
4. 🚫 GO → build  

---

*Gap tracker. Bet E AC + ship-readiness 2026-07-18.*
