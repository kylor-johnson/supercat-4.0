# PERSONA ONE-PAGERS — Bet F (v0)

**Date:** 2026-07-24 · **Phase:** 2 shape pack · **Isolation:** ON · **Does not unlock Bet A GO**
**Source of truth:** `PERSONA-RESEARCH-v0.md` (Phase 1 PASS). One page each for the **three locked personas**.
**Personas v0 (locked):** CEO/Owner · Sales rep · Admin / sales ops. **Manager folds under CEO/Owner** (note below).
**Copy:** client-facing strings from `COPY-AUDIT-portal-mocks.md`; internal capability IDs (C1, S1, Q-R1) in parentheses for eng only.

> **Default-home labels are HYPOTHESIS** (recommended pending customer feedback). No raw customer interview transcripts exist in the reading set (research §0.8, Annex); true verbatims are a **Phase-3 input**, not assumed here.

---

## Persona 1 — Sales rep

**Job (not title):** *"Show me the truth about my accounts — what my customers bought and what we invoiced in my territory — so I don't have to rebuild it in Excel."*

**Primary questions → surfaces:**
- Q1 "How much did **my** customers buy in this range?" → **Customers** (selected-range invoiced total).
- Q2 "What did we **invoice** under my territory + dates?" → **Invoices** (invoiced total that moves with the filter — EBR-40).
- Q3 "What's **confirmed / still open** on my book (not quotes)?" → **Orders** (confirmed vs open quotes).

**Recommended default home (HYPOTHESIS — recommended pending feedback):** **Customers** *(with Invoices as the close runner-up)*.
Rationale: the rep's daily object is the account; the validated repro is invoice/account-scoped (`cmallon` → `105:1 Gigi Lane`). Not Dashboard (org-wide chrome) and not Intelligence (owner-leaning). **Customers vs Invoices is still open** — freeze as *"recommended: Customers, pending one owner/VP + one lead-rep reaction"* (research §9.2; feedback script Q-open).

**Trust failure:** Rep picks a territory and **still sees the whole org / wrong book** → distrusts every number → exports to Excel. Validated live: wwjc `cmallon` YTD 1,404 / $1.46M does not scope to `105:1 Gigi Lane` (710 / $777k) [EBR-40]; dashboard variant stalled since 2022 [EBR-212]; export/period drift compounds it [EBR-91]. Spine mechanism = **F1**.

**Must see / nice / hide:**
- **Must see:** invoiced total for *my territory + range*; the same total on export; confirmed-vs-quote split; account list limited to only my territory's customers.
- **Nice:** accounts fading (S1) for my accounts; light activity ("am I keeping up").
- **Hide by default:** whole-org totals; other reps' books; named rep→revenue leaderboard (RS-01) on orgs that can't attribute it.

**Data honesty gates:**
- **Fail-closed territory:** empty/zero territory keys → show *assigned only* (or nothing) — **never** whole-org [`FILTER-TRUTH-AC` A1.4; 32/55 orgs empty territory master, F11].
- **`access_all_customer_sales_totals` OFF by default** for a scoped rep — whole-book revenue is a granted privilege, not a default [control-plane A.5; `SETTINGS` AC-E2 #7].
- **No named rep leaderboard** where `REP_IDENTITY_TIER` < 2; never silently drop unmapped reps [Capability #27, F9].

**Evidence:** F1 (spine §4); EBR-40 / EBR-212 (affinity C1); EBR-91 (affinity C2); wwjc repro (`CEO-CTO-FRIDAY-SHARE` Assumptions / `BUG-VALIDATION-PACK`); `customer_synching` 962 All / 645 Associated / 327 None (control-plane A.4); feedback script §2 "first number you wish was answered." [`PERSONA-RESEARCH-v0` §2]

---

## Persona 2 — CEO / Owner  *(portal seat = Owner/VP Sales)*

**Job (not title):** *"Tell me the one true topline and who's quietly slipping — without me (or an analyst) grinding Excel + Claude + Power BI to get it."*

**Primary questions → surfaces:**
- Q1 "What did we **actually invoice** (the number that reconciles to the dollar)?" → **Intelligence** invoiced sales (C1) / **Reports** Summary (same spine).
- Q2 "Which **accounts are fading**, worth how much, who calls them?" → **Intelligence** accounts fading (S1 · EBR-198).
- Q3 "Is the **team** active — logins, who's writing orders, who's gone quiet?" → **Intelligence** team activity strip (behavior floor).

**Recommended default home (HYPOTHESIS):** **Intelligence** — the only surface built around owner answers; **Reports Summary** secondary.
**Important scope split (locked):** the portal "CEO/Owner" is the **Owner/VP Sales** seat consuming a *thin* C1/S1/team subset. The **deep CEO factory is Insightful**, not the portal (research §3, §11; `SURFACE-PLACEMENT.md`). Whether an owner is a real portal end-user at all — vs Owner/VP + Ops being the true portal pair — is Open Question §9.3, to validate with an owner/VP.

**Trust failure:** Second-order. If territory/export don't reconcile (Bet A: EBR-40/212/91), the Intelligence surface the owner relies on is **untrustworthy at the root** — *"three things must be true before Intelligence is trustworthy: territory scopes the book; export reconciles to UI; quotes never counted as sales"* [`CEO-CTO-FRIDAY-SHARE`]. Owner-specific failure: a topline that silently claims **completeness** it doesn't have (single feed, STRONG-not-FULL) [F8; Capability §5].

**Must see / nice / hide:**
- **Must see:** invoiced total (C1) with a plain provenance line ("invoiced net · reconciles to the ledger"); accounts fading (S1); team activity.
- **Nice:** concentration / YoY (C3/C10) as follow-ups; drill-down (EBR-687).
- **Hide by default:** named rep→revenue lead (RS-01); five Dashboard Top-N tables dumped onto Intelligence; anything margin/AR-shaped.

**Data honesty gates:**
- **STRONG ceiling, never FULL** — every topline carries the single-feed caveat; no "your total business is $X, complete" [Capability §4, F8].
- **No margin / COGS / AR / profitability** — schema-absent; suppress, never estimate [Capability §4].
- **No "$0 returns"** on gross-only orgs → "returns not represented" [Capability #24].
- **RS-01 named rep→revenue** only at Tier 2; not a v1 default lead [`INSIGHT-IR-v1-AC` AC-3].

**Evidence:** F3 (Insightful = CEO product spec, spine §4); spine §3 ("Insightful 4.0 already runs CEO reports off the same tables; invoiced `net_amount` = total business"); `INSIGHT-IR-v1-AC` (C1/S1/team = owner-leaning); Friday-share "three things must be true"; Capability §4/§5. [`PERSONA-RESEARCH-v0` §3]

---

## Persona 3 — Admin / sales ops  *(one persona, permission tier: client org-admin vs SuperCat)*

**Job (not title):** *"Make the portal work and make the numbers reconcile — turn it on for the right people, scope reps correctly, and make the export match the screen — without filing a SuperCat ticket for every change."*

**Primary questions → surfaces:**
- Q1 "**Why can't this user see the portal / their book?**" → **Settings hub** Enablement decision tree (Bet E, AC-E1).
- Q2 "Does the **export reconcile** to the on-screen total for the same filters?" → **Invoices / Customers / Reports** export = UI (EBR-91).
- Q3 "Who is **scoped to what** (territory / customer visibility / export)?" → **Settings hub** Territory & data access (`customer_synching`, `access_all_customer_sales_totals`).

**Recommended default home (HYPOTHESIS):** **Settings hub** (Enablement) for the config half; **Reports/Invoices** for the reconciliation half. Ops is the one persona that actually *lives* in Settings — the other two rarely touch it.

**Permission tier (one persona, two gates — locked, not two one-pagers):** a **client org-admin** self-serves enablement / territory & data access / display / export; a **SuperCat superadmin** holds the locked levers (Revenue definitions, Territory match mode, Experiments). Same job, different authority — a permission tier, not a separate bounded context. Whether to ever split into two personas is Open Question §9.4 (recommend: keep one, tier the gates).

**Trust failure:** Two shapes. (a) **Config opacity** — access rules hide in 134 toggles / 39 YAML flags across 6 layers with no admin surface (F10); ops can't answer "why is the portal off for this user?" without SuperCat. (b) **Reconciliation** — export ≠ displayed total (EBR-91) makes ops the person who fields "the CSV doesn't match" and rebuilds it. Both push work onto SuperCat tickets and Excel.

**Must see / nice / hide:**
- **Must see:** enablement decision tree; who-sees-what (synching / totals); unified export control; visible (read-only) revenue definitions.
- **Nice:** display polish self-service (currency, qty columns, customer graph); adoption glance (who's actually logging in).
- **Hide by default:** SuperCat-only levers — **Revenue definitions are visible-but-locked (🔒)**; Territory match mode, `force_portal_display`, and Experiments canaries are **not shown** to a client admin.

**Data honesty gates:**
- **Client admin must NOT see/edit SuperCat-only settings:** Revenue definitions locked (🔒, SuperCat + INSIGHT); Territory match mode superadmin-only; Experiments lab superadmin-only [`SETTINGS` AC-E3/E4/E5].
- **Settings must not imply filter truth is fixed** when Bet A hasn't shipped [`SETTINGS` AC-E4.4].
- Changing a revenue definition would silently change what "sales" means → **locked** to protect reconciliation to invoiced `net_amount` [control-plane B.1; `SETTINGS` AC-E3].

**Evidence:** F10 (spine §4); `PORTAL-SETTINGS-CONTROL-PLANE` (134/6/39; `customer_synching`; `access_all_customer_sales_totals`; decision tree B.3); `SETTINGS-hub-v1-AC` AC-E1/E2/E3/E4; EBR-91 (affinity C2); `IA-PERSONA-TRACK` ("export reconciles / config"). [`PERSONA-RESEARCH-v0` §4]

---

## Note — Manager folded under CEO/Owner (v0)

**Manager is not a fourth one-pager for v0.** It folds into **CEO/Owner** as the *oversight + scoping* variant: a manager is an owner-style viewer of the whole team who is *scoped* to several books rather than one. The "woodshed / what the rep sees" job is a **scoping variation**, solvable by the **same fail-closed territory + `access_all_customer_sales_totals`** mechanism (a permission tier), not a new bounded context. Manager-as-multi-territory is explicitly the **EBR-180 XL shelf / separate appetite** (F11), out of frame.

**Open (research §9.1):** a fourth one-pager only if Phase-3 interviews surface a manager job that CEO/Owner (oversight) + rep (scoping) genuinely cannot hold. Until then: fold.

---

*Phase 2 one-pagers. Client-facing labels = COPY-AUDIT. Default homes = HYPOTHESIS pending customer A/B. Isolation ON. Does not unlock Bet A GO.*
