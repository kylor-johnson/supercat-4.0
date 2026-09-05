# Draft — reply to CTO (Bet A feedback)

**Use:** paste into Slack/email as Kylor. Not posted to Jira.  
**Context:** Response to 2026-07-20 feedback on the Bet A Decision Brief.  
**Related:** `CTO-FEEDBACK-2026-07-20.md` · `BUG-VALIDATION-PACK.md` (filled 2026-07-21)

---

## Suggested reply (post-validation)

Thanks again — pack is run.

**EBR-40 — still real, keep.** On wwjc (trust flagship), a multi-territory rep book has a clear T1 shrink target (e.g. cmallon’s YTD union ~1,404 / $1.46M → T1 `105:1 Gigi Lane` ~710 / $777k). The Kalco 2021 Ferguson/`0016` URLs are stale — that bill-to is territory `0999` today, not `0016`. Unfixed code still includes the ship-to bridge case mismatch and fail-closed empty-territory path. Optional 5-min UI confirm as cmallon; I’m not blocking the readout on screenshots.

**EBR-212 — keep paired, partial surface.** Same warehouse territory filter feeds the dashboard invoiced KPI. On wwjc, true multi-terr *reps* don’t have portal dashboard enabled (Office/SuperCat do, with all-customer totals). So I’m not claiming a clean “rep dashboard” click — but I won’t drop the surface from AC-A1.

**EBR-91 — still real as period drift; keep with rewritten AC.** Customers CY/LY blocks ignore the date dropdown; the selected-range export column only appears for `previous_ytd`/`custom` (substring gate still live). Ticket text stays empty — AC comes from this repro, not Jira.

**EBR-87 — park (not universal).** Live quote statuses only on `cci` (`Q`) and `ril` (`Quote`); both already exclude those from backlog. Kalco has **zero** quote portal orders today. Invoiced “sales” is `net_amount` on invoices — quotes don’t land there. Metric-law copy stays; no dedicated build in the GO ask.

**EBR-7 — close, don’t rebuild.** wwjc invoice spine is `net_amount` (total_amount null on the YTD book).

Isolation stays ON. Next touch is this validation readout — not a Dashboard/Intelligence walk. I’ll ask for `ISOLATION OFF — GO on EBR-40` only after you’re good with keep 40+91 (+212 paired) and park 87.

---

## Shorter variant (post-validation)

Validation done: **keep EBR-40 + 91** (wwjc territory book + Customers period/export drift); **keep 212 paired** (same mechanism; wwjc dash is Office/all-totals); **park EBR-87** (only cci/ril have quotes, both backlog-excluded; kal has none). EBR-7 doctrine close. Isolation ON until GO.

---

## Pre-validation draft (kept for history)

Thanks — really helpful, and I’m glad the sequence landed.

Agreed on assumptions: open Jira ≠ still real. I’ve written a live repro pack for EBR-40, 212, 91, and 87 (steps, org picks, keep/narrow/park). I’ll run those on named production orgs — territory checks on **wwjc** (trust flagship; not the same as a zero-exposure org), and I won’t claim territory truth on sarreid.

On quotes: your skepticism matches the ticket. EBR-87 is titled around eOL portal totals, and Chuck already asked why a quote would show in Portal Orders. I’m treating that as **provisional** — validate whether it still happens, and whether it’s limited to eCat/eOL-origin (or status-config) orgs — then follow up with impacted customers before we keep universal “quotes as sales” language in the Bet A ask.

On visuals: fair. The Dashboard / full program mockup was the wrong center of gravity for this decision. Next touch with you is a short **validation readout** (what we can still reproduce, what we narrow or park) — not another UI walk. Persona + IA / content A/B I’m parking on a parallel track so it doesn’t compete with the trust fix.

Isolation stays ON. No ask for `ISOLATION OFF — GO on EBR-40` until that readout.
