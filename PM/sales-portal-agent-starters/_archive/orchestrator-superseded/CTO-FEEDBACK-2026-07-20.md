# CTO feedback — Bet A Decision Brief (2026-07-20)

**Source:** Leadership share of the Sales Portal Bet A Decision Brief (Notion) + pitch/internal demos.  
**Owner:** Kylor · **Captured:** 2026-07-21 · **Superseded for GO:** see `CTO-FEEDBACK-2026-07-24.md`  
**Related:** `BUG-VALIDATION-PACK.md` · `IA-PERSONA-TRACK.md` · `DRAFT-CTO-REPLY-validation.md` · `CEO-CTO-FRIDAY-SHARE.md` · `TRD-Bet-A-filter-truth.md` · **`CTO-FEEDBACK-2026-07-24.md`**

---

## What landed

Content and sequence are right: trust foundation first, then Intelligence / Settings / LLM. No pushback on the Bet A → Bet C order.

---

## Three themes → actions

| # | CTO theme (paraphrase) | What it means | Action |
|---|---|---|---|
| 1 | **Define assumptions — verify the old EBRs** | Tickets open since 2021–22 are not proof the bugs still bite. Need steps to reproduce, see each issue in action, confirm still real. | Run `BUG-VALIDATION-PACK.md` on named orgs before any GO ask. |
| 2 | **Dubious of “quotes as sales/orders”** | Sales data often comes from 3rd-party ERPs. Quote pollution may only apply where orders originate from eCat/eOL. Validate with impacted customers. | **Done 2026-07-21:** **Parked** EBR-87 — not universal; only `cci`/`ril` have quotes and both already exclude from backlog. |
| 3 | **Visuals are distractors** | Dashboard / polished UI is largely unrelated to this batch. Separate persona ID + IA recommendation; continue A/B content tests with customers. | Split **Track 2** (`IA-PERSONA-TRACK.md`). Next leadership touch = validation readout, not another UI walk. Pitch demo only if a visual is needed. |

---

## Gate status (2026-07-21 → closed 2026-07-24)

```
Validation pack COMPLETE (SQL + Rails)
        │
        ▼
Scope locked: keep 40+91 (+212 paired) · park 87 · close 7
        │
        ▼
CTO 2026-07-24: Bet A ready for EBR → SERV
        │
        ▼
ISOLATION OFF — GO on EBR-40   ← see CTO-FEEDBACK-2026-07-24.md
```

---

## Two tracks

| Track | Name | Unlocks GO? | Artifact |
|---|---|---|---|
| **1** | Trust validation — repro EBR-40 / 212 / 91 / 87 | **Yes** (GO 2026-07-24) | `BUG-VALIDATION-PACK.md` |
| **2** | Persona + IA + customer content A/B | **No** | `IA-PERSONA-TRACK.md` |

Track 2 may run in parallel. It does not substitute for Track 1 and does not expand Bet A into a Dashboard redesign.

---

## Scope posture after validation

| Outcome | Disposition |
|---|---|
| Territory limits list **and** total (EBR-40, EBR-212) | **Keep** — 40 core; 212 paired (partial dash surface on wwjc) |
| Customers period + export (EBR-91) | **Keep** + rewrite AC-A2 (period drift / SERV-2395) |
| Quotes never counted as sales (EBR-87) | **Park** — no dedicated build; metric-law copy only |
| Close EBR-7 via `net_amount` doctrine | **Close, don’t rebuild** |
| Answer-first list tabs / Dashboard polish | **Not** the Bet A proof story — Track 2 |

---

## Comms corrections triggered by this feedback

1. **wwjc ≠ zero-exposure** — wwjc is the trust flagship (intersection of territory bugs). Zero-exposure orgs are an *alternative* verify target. Do not conflate.
2. **Next share** — validation readout, not GO-from-demo. Lead with pitch only if a click-through is needed; keep internal demo off the default path.
3. **Assumptions section** required on the brief / TRD / Notion mirror — see updated `CEO-CTO-FRIDAY-SHARE.md` and `TRD-Bet-A-filter-truth.md`.

---

## Success for the response to this feedback

- [x] This file on disk  
- [x] `BUG-VALIDATION-PACK.md` written  
- [x] `BUG-VALIDATION-PACK.md` **executed** (pass/fail filled 2026-07-21)  
- [x] EBR-87 **parked** with evidence  
- [x] CTO validation readout held → **2026-07-24 go-ahead** (`CTO-FEEDBACK-2026-07-24.md`)  
- [x] GO phrase: `ISOLATION OFF — GO on EBR-40`  

---

*Historical capture of 2026-07-20 themes. GO authority moved to `CTO-FEEDBACK-2026-07-24.md`.*
