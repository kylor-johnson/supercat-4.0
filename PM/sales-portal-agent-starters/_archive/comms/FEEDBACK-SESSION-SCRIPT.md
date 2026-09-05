# Feedback session script — Sales Portal IR v1 (C1 + S1 + team strip)

**Date:** 2026-07-17 · **Bet:** B → freezes AC for Bet C  
**Duration:** 35–45 min · **Facilitator:** Kylor (or designee)  
**Artifact to update after:** [`UX-brief-c1-s1-team-strip.md`](UX-brief-c1-s1-team-strip.md) post-feedback table  
**Mockup (customer session):** `design-system/app/sales-portal-cycle03-mockup.html` (C1 + S1 + team strip; wireframe rail — use this for customer feedback)  
**Mockup (internal demo only):** `design-system/app/sales-portal-cycle03-chrome.html` (same content on shared `<sc-app-sidebar>` chrome — for internal team demos, not the customer session)  

**Audience (ideal):** 1 owner / VP Sales + 1 CSM or lead rep from a portal-live org. Prefer orgs that map to demo shapes: dense (`sarreid`-like) **or** Tier-0 / diversified (`ufi`/`cci`-like).  

**Isolation:** Session is product feedback only — no Rails promises, no LLM demos.

---

## 0. Pre-flight (5 min before call)

- [ ] Open mockup in browser (light mode); have spine numbers ready: sarreid ~$16M LTM, cci ~$71M (rounded OK).  
- [ ] Print or have this script + note sheet.  
- [ ] Decide demo pair: **A** concentrated (topline + risk language) vs **B** diversified / Tier-0 (team strip shines).  
- [ ] Do **not** demo territory-scoped “only my book” claims unless filter truth is honest for that org.  
- [ ] Confirm: no RS-01 named invoiced-rep revenue in the walkthrough.

---

## 1. Open (2 min)

> Thanks for the time. We’re shaping a Sales Portal Intelligence surface — not a redesign of the whole catalog. Goal today: validate three answers we’d put above the fold. Nothing is built yet; your reactions freeze the acceptance criteria.

**Rules for facilitator:** Soft “interesting, maybe someday” on feature requests outside the three panels. Capture as raw ideas; do not commit.

---

## 2. Context (3 min) — one spine

Show / say:

1. **True Topline** = invoiced ledger (`net_amount`), not booked orders or quotes.  
2. Every number is “as invoiced through our feed” — not claiming complete cross-channel.  
3. We’re testing **answer-first** layout (App kit), not a Phase-3 marketing shell.

Ask once: *When you open Sales Portal today, what’s the first number you wish was already answered?*

---

## 3. Walkthrough — Hero 1 True Topline (6 min)

**Show:** Big number + provenance chip (“Invoiced net · reconciles to ledger”) + range control.

| # | Ask | Listen for |
|---|---|---|
| Q1 | Is **invoiced trailing-12-months** the number you trust as the default hero — or do you mentally convert to booked / backlog / YTD calendar? | Default period; synonym fights |
| Q1b | If we change the date range at the top, do you expect **every** number on the page to move with it? | SERV-style range trust |

**Capture:** Preferred default window · must-have caveat wording · deal-breakers.

---

## 4. Walkthrough — Hero 2 Quietly dying / S1 (10 min)

**Show** Hero 2 panel (S1 quietly dying):

> Second answer: accounts whose recent 6 months are down vs the prior 6 months, with dollars at risk and who should call them. Hot/cold customers — [EBR-198](https://supercatsolutions.atlassian.net/browse/EBR-198).

Optional: briefly flash concentration (“one account is 30% of the book”) and ask which they’d rather see as hero #2.

| # | Ask | Listen for |
|---|---|---|
| Q2 | For **your** book, is “quietly dying accounts” more useful than “single-account concentration”? | S1 vs C3 winner |
| Q2b | After seeing a dying account, what’s the **one** follow-up you want next — products, order cadence, or who to call? | Drill path (EBR-687) |
| Q4 | On a QBR screenshot, do you want **real customer names** or masked by default? | Privacy / shareability |

**Capture:** Hero-2 choice · threshold feel (“too noisy?”) · name policy.

---

## 5. Walkthrough — Team strip (8 min)

**Narrate:**

> Below the commerce heroes: who’s logging in, writing eCat orders, going quiet — **activity**, not “whose invoices.” For some manufacturers we literally cannot attribute invoiced dollars to named reps; activity still ships.

| # | Ask | Listen for |
|---|---|---|
| Q3 | Is a **behavior** team strip useful when we **cannot** show named invoiced-rep revenue? | Universe B–D value |
| Q3b | Rank by eCat order activity vs login/engagement — which would you glance at weekly? | Q-18 vs Q-01 |
| Q3c | Would you be angry if a “rep leaderboard” showed revenue but dropped unmapped reps? | Fabricated leaderboard risk |

**Capture:** Keep / cut team strip · preferred leaderboard mode · any “must not show.”

---

## 6. Craft / chrome (4 min)

| # | Ask | Listen for |
|---|---|---|
| Q6 | Does this App kit look feel like an upgrade over classic portal, or too far from what reps recognize? | Overlay appetite |
| Q6b | One screen — too much, or still missing the one thing you’d open Excel for? | Scope hammer |

---

## 7. Close (3 min)

> Three decisions we’ll write down: (1) default hero number, (2) second hero S1 vs concentration, (3) team strip keep/cut. LLM / talk-to-data is explicitly later — not this slice.

Thank them. Offer one follow-up email with a still of the mockup if useful.

---

## 8. Facilitator note sheet (fill live)

| Decision | Choice | Quote / note |
|---|---|---|
| Default topline window | invoiced T12 / YTD / other | |
| Hero 2 | S1 / C3 / both (S1 primary) | |
| Team strip | keep / cut / later | |
| Leaderboard mode | Q-18 eCat / Q-01 engagement / neither | |
| Customer names | real default / masked default | |
| S1 follow-up | products / cadence / who-to-call | |
| App kit | upgrade / too foreign / neutral | |
| Out-of-scope asks (raw) | | |

---

## 9. After the call (Orchestrator / UX — same day)

1. Fill **Post-feedback AC updates** in `UX-brief-c1-s1-team-strip.md`.  
2. Patch `INSIGHT-IR-v1-AC.md` only where feedback changes a must-have.  
3. Update `SHIP-READINESS-bet-c.md`: mark feedback session done.  
4. Paste notes into Orchestrator for a Review Card.  
5. Do **not** lift isolation or schedule EBR-772.

---

## Invite blurb (paste into calendar)

**Subject:** Sales Portal — 40 min feedback on Intelligence answers (not a demo of AI)

Hi — I’d like 35–45 minutes to walk a **mock** Sales Portal Intelligence view and get your reaction to three answers: (1) true invoiced topline, (2) quietly dying accounts, (3) team activity strip. No build commitment; your feedback locks what we specify next. Bring one thing you currently export to Excel to answer.

---

*Script pairs with `UX-brief-c1-s1-team-strip.md` and reboot `05d-ORCHESTRATOR-REBOOT-cycle03.md`.*
