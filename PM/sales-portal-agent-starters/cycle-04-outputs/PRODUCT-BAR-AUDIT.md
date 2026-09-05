# Product bar audit — Sales Analytics (cycle-04)

**Date:** 2026-07-24 · **Cycle:** 04 · **Isolation:** ON (docs only — no Rails, no Jira writes)
**Judged against:** a serious B2B SaaS analytics product for manufacturer sales orgs — not a demo, not a Friday share.
**Authority consumed:** `00-PROGRAM-SPINE.md` · `05e-ORCHESTRATOR-REBOOT-saas-product-bar.md` · `cycle-03-outputs/{BET-TRIAGE-BOARD, SPEC-GAP-CHECKLIST, CTO-FEEDBACK-2026-07-24, FILTER-TRUTH-AC, DEMO-SURFACE-CONTRACT, LIST-TABS-AC, INSIGHT-IR-v1-AC, SETTINGS-hub-v1-AC, IA-PRIORITY-MATRIX, IA-RECOMMENDATION-v0}.md`
**HTML inspected (read-only):** `design-system/app/sales-portal-internal-demo.html` (2,787 ln) · `sales-portal-cycle03-mockup.html` (321 ln) · `sales-portal-persona-ia-demo.html` (3,007 ln)

**This file authorizes nothing.** It does not change `FILTER-TRUTH-AC.md`, does not touch Bet A / SERV-2447–2449, does not unlock any `ISOLATION OFF — GO`.

---

## 1. Verdict

Bet A is the only surface stamped as **product**. Everything after it is stamped as **documents**.

The distinction matters because the cycle-03 gap checklist reads as if four surfaces are ready. Its ✅ marks certify *an artifact exists and is internally coherent* — which is true, and in several cases the artifacts are genuinely strong. They do not certify that a client could sit in front of the thing and leave trusting it. Against that second bar, the current HTML fails on the one attribute this product sells: **the numbers do not agree with each other.**

That is the headline. The persona switcher is the most visible embarrassment, but it is downstream. Fix who-sees-what on top of figures that contradict each other and you have shipped a better-looking trust problem.

---

## 2. Stamped · half-baked · wrong

| Surface | Grade | Why | Stamped-as-product looks like |
|---|---|---|---|
| **A** Filter truth | **Stamped** | Mechanism, live evidence on `wwjc` (`cmallon` YTD 1,404 / $1.46M → T1 710 / $777k), eng file:line, SERV-2447/2448/2449 in sprint | Prod verify closes `A1.2` (dashboard path, still unchecked at `FILTER-TRUTH-AC.md:97`) and `A2`; SERV-2196 ship-to over-grant sequenced before any territory-scoped client demo |
| **B** List tabs | **Half-baked** | `LIST-TABS-AC.md` is real Given/When/Then and should survive. But all four pre-build verifies are open (`LIST-TABS-AC.md:87–90`), and the artifact backing them ships two bug simulators (`internal-demo:1383`, `:1566`) | One dataset behind all four tabs; export-equals-hero demonstrated live rather than asserted in copy |
| **C** Intelligence | **Data-gated** | `C4` (re-stamp `cci` + `kll`) is ❌ in `SPEC-GAP-CHECKLIST.md:59`. `AC-1` requires reproducing ~$15.98M / ~$71.23M — and the mockup cannot reproduce sarreid against its own footnote (§3 below) | Grade orgs re-stamped; every figure carries the AC-5 provenance quad; **one** hero that is completely honest beats three illustrative ones |
| **E** Settings hub | **Well shaped, badly demoed** | `SETTINGS-hub-v1-AC.md` is the strongest pack in the folder — real Rails cites (`ecat_permissions_helper.rb:20–58`, `eol_left_nav_dataflow.rb:336–352`), a countable win (E6). The demo renders the eng backlog as UI: Wave badges (`:1870, :1885, :1893, :1909, :1920`) and `Delete (Wave 0)` buttons (`:1925–1929`) | Enablement decision tree only, as a client-usable answer to "why can't this rep see the portal?" — waves, flags, and ticket IDs invisible |
| **F** Persona IA | **Hypothesis rendered as product** | `IA-RECOMMENDATION-v0.md:34` states no customer transcripts exist in the reading set, then §3 lists five open questions — including whether the CEO is a portal user at all. The demo already ships a `View as` switcher (`persona-ia-demo:1264–1269`) that stamps surfaces `HIDE · not for you` | Either §3 is answered by the sessions specced in §7 below, or the switcher stays internal and persona remains a docs-only ordering law for Bet B |

---

## 3. Finding P1 — the demos contradict themselves on revenue

This is disqualifying on its own, because metric trust is the product.

**Within `sales-portal-cycle03-mockup.html`:**

| Element | Line | Value |
|---|---|---|
| C1 hero | 202 | `$15.98M` |
| Hero sub-counts | 203 | `11,702 invoices` · `1,413 active customers` |
| Its own footnote | 315 | `verified live $16.02M / 11,729 inv / 1,417 custs` |

The hero disagrees with the footnote directly beneath it, on all three figures.

**Within `sales-portal-internal-demo.html`:**

| Element | Line | Value |
|---|---|---|
| Reports → Summary | 1649 | `$8.12M` · sub-label `Current YTD · not booked orders` (:1650) |
| Reports → Monthly, YTD footer | 1764 | `Jan – Jul 2026 YTD` · `Total invoiced: $8,920K` |
| Footnote beneath both | 1767 | `Reports · Summary total = invoiced net = Dashboard invoiced = Intelligence C1` |

Same YTD context, ~$800K apart — and the footnote at line 1767 asserts the exact parity the two figures above it break. The surface claims `LT-RPT.2` compliance in prose while failing it in arithmetic, roughly 100 pixels apart. A client who reads the footnote and then adds the column finds this immediately.

**Across files** — same org, same cohort, different answers:

| Fact | `internal-demo` | `cycle03-mockup` |
|---|---|---|
| S1 quietly-dying cohort | `25` accounts / `$1.69M` (:1808) | `55` accounts / `$2.38M` (:228–229) |
| Owner of account `29925` | `Rep 546` (:1812) | `Rep 099` (:236) |
| Team strip | `42` logins / `15` writers (:1829–1830) | `77 / 42 / 12` (:261–271) |

**Why this is structural, not sloppy.** Three files hold hand-maintained numbers. `persona-ia-demo.html` is a ~220-line fork of `internal-demo.html` and already shares its Reports contradiction. Every future edit multiplies by three. The fix is not proofreading — it is one stamped dataset that every surface reads.

**AC violated:** `AC-A4` (all totals labeled sales use one definition), `LT-RPT.2` (Reports total = Dashboard KPI = Intelligence C1), `AC-5` (every number carries a provenance stamp — these carry a contradicting one).

---

## 4. Finding P2 — "Names masked" is cosmetic

The topbar asserts `Names masked` (`internal-demo:1185`) and a table header reads `Account (masked)` (`cycle03-mockup:233`). The cells show `Account 29925`, `Account 32162`, `Account 31098` (`internal-demo:1415–1417`, `cycle03-mockup:236–240`) alongside `Rep 546` / `Rep 099`.

Those are sarreid's real bill-to keys — they trace directly to the stamped S1 cohort in `IR-v1-QUERIES.md`, which `LT-CUST.5` cites by number. Company names are pseudonymised; the join keys are not. Showing one manufacturer another manufacturer's ERP account numbers is a confidentiality exposure, not a polish item.

**Rule for any client-facing artifact:** synthetic keys only, mapped once, mapping stored outside the file.

---

## 5. Finding P3 — teaching surfaces and eng backlog are in the UI

Inventoried so the client-review brief can name them as no-gos:

| Category | Receipts |
|---|---|
| Teaching nav | `What's broken` (`internal-demo:1158`); cross-link `Territory filter · see What's broken` (`:1231`) |
| Bug simulators | `Simulate today's filter bug` (`:1383`, `:1566`); `Broken (today)` / `Fixed` switch (`:1953–1954`); `Broken · filter does nothing` (`:1972`) |
| Eng backlog as UI | Wave badges (`:1870–1920`); `Delete (Wave 0)` / `Delete flag (Wave 0)` (`:1925–1929`); static permission tree naming `enable_sales_portal`, `should_show_portal` (`:1871–1877`) |
| Internal identity | Title `Sales Portal — Internal Demo` (`:6`); `Kylor Johnson` in sidebar (`:1165`); org switcher across two real clients (`:1107–1113`) |
| Contradictory chrome | `Live · read-only` (`:1184`) sitting beside `Cycle 03 · mockup-only` (`:1186`) |
| Persona theater | `View as` switcher (`persona-ia-demo:1264–1269`); injected rank cues `MUST` / `not your landing` / `HIDE · not for you` / `teaching` (`:2536–2586`) |

Note the self-aware disclaimers the files carry — `Wave badges = demo chrome ≠ eng directive` (`:1856`), `Delete buttons = demo chrome — not an eng directive until GO` (`:1921`). **A disclaimer inside the artifact is the tell.** When a surface has to explain that parts of itself aren't real, it is an internal teaching aid, and that is fine — it just isn't the thing a client sees.

---

## 6. Finding P4 — green checks certify documents, not product

`SPEC-GAP-CHECKLIST.md` marks `A4` ("Demo surfaces show filter/export/quote truth") and `B2` ("Internal HTML") as ✅. Both are accurate statements about documents. Neither is a statement about product readiness, and nothing in the folder distinguishes the two.

This is the mechanism that let the program believe four surfaces were near-ready. Recommend the checklist grow a second axis — **Doc ✅ / Product ✅** — where product-✅ requires: verifies closed, numbers reconciled from one source, and no in-artifact disclaimers. Not proposing the edit here; flagging it as a spine call for Kylor.

---

## 7. Finding P5 — persona is a hypothesis, and here is the study that resolves it

Kylor's call (2026-07-24): **keep Bet F, and specify the customer A/B that closes `IA-RECOMMENDATION-v0.md` §3.** The pack is not wrong — it is unvalidated, and it says so. What follows is the study design, not a park.

### 7.1 Recruiting frame

Four orgs from the Track-1 impact list, chosen for what each can and cannot prove:

| Org | Why | Constraint the session must respect |
|---|---|---|
| **wwjc** | Trust flagship — sits at the intersection of comma-rep and ship-to over-grant; Bet A verify org | Only org where "the filter now tells the truth" is demonstrable post-prod |
| **cci** | $71.23M, Tier-0, backlog exclusions `["C","Q","X","Z"]` | Tier-0 → `R2.1` suppresses named rep→revenue; do **not** run a "who are my top reps" probe here |
| **sarreid** | Golden density, 99.8% multi-territory bill-tos | **Never** demo territory scoping here until SERV-2196 is honest (`FILTER-TRUTH-AC.md:36`) |
| **ufi** | Largest raw surface (120,663 invoices), Tier-0 | Same `R2` suppression as cci; good for volume/latency reactions |

**Seats:** one Owner/VP and one lead rep per org (8 sessions), plus **two** admin/ops seats total across cci and wwjc. Ops is the smallest sample because its default home (Settings hub) is the least contested claim.

### 7.2 What each open question needs

| § | Question | Who | Probe | A decisive answer sounds like | What it changes |
|---|---|---|---|---|---|
| 3.1 | Rep default home — Customers vs Invoices | Lead reps (4) | Open the portal cold, unprompted: *"It's Monday. Show me what you check first."* Do not offer the two options | Rep navigates without hesitating, and the reason is a job ("I need to know who to call") not a preference | Freezes the rep default in `IA-PRIORITY-MATRIX` §A, or splits it by org shape |
| 3.2 | Is the CEO a portal end-user at all | Owner/VP (4) | *"When you want the number, where do you go today?"* Then show Intelligence. Watch for "I'd have my ops person pull that" | Owner either drives it themselves or names a delegate — both are decisive | If delegated, the true portal pair is Owner/VP + Ops and Intelligence stops being an owner default; CEO is served by Insightful |
| 3.3 | IA depth — hero-priority vs nav-level role landing | All 10 | Show one surface twice: reordered heroes vs a role landing. Ask which felt like *their* portal | Preference is stable across ≥7 of 10, or clearly splits by role | Hero-priority-per-surface stays the recommendation, or a nav landing enters Bet B scope |
| 3.4 | Adoption boundary — team strip vs Admin Console report | Ops (2) + Owner/VP (4) | *"Who in your company should see how much the team is using this?"* | Named role + named surface | Draws the line in `SURFACE-PLACEMENT` B2 without opening the Admin Console project |
| 3.5 | Manager fold vs split | Owner/VP (4) | *"Is there someone between you and the reps who needs a different view?"* | A job surfaces that neither Owner/VP nor rep can hold | A fourth one-pager — otherwise the fold holds for v0 |

### 7.3 Hard constraints on these sessions

- Run **after** Bet A is verified in prod. A rep asked to trust a territory filter that still lies will answer the wrong question.
- Do **not** show the current `View as` switcher. It pre-loads the answer to 3.3 and displays `HIDE · not for you`, which reads as the product deciding what a paying user may see.
- Do **not** probe named rep→revenue on cci, ufi, or any Tier-0 org — `R2.1` suppresses it, so the question describes a product we cannot ship there.
- Sessions produce **AC deltas**, not feature requests. Anything that isn't a change to an existing AC goes to a parking list.

---

## 8. Finding P6 — verify paths are open

| Pack | Open item |
|---|---|
| `FILTER-TRUTH-AC.md:97` | `A1.2` dashboard path on a dash-enabled user — unchecked |
| `LIST-TABS-AC.md:87–90` | All four pre-build verifies — unchecked |
| `SPEC-GAP-CHECKLIST.md:59` | `C4` cci + kll re-stamp — ❌, human/data gate before build |
| `SETTINGS-hub-v1-AC.md:286–293` | Eight-item pre-build checklist — unchecked (correct; Bet E has no GO) |

Bet A's own AC has one open verify. That is the single most valuable thing to close this week, because everything in §7 depends on it.

---

## 9. What is genuinely good (do not rewrite)

Being fair matters here — the shape work is not the problem.

- `FILTER-TRUTH-AC.md` — mechanism-first, live evidence, honest about what validation *disproved* (EBR-87 parked with receipts rather than shipped on assumption).
- `SETTINGS-hub-v1-AC.md` — real Rails cites, a countable win (134 → ~30 / ~18 self-service), and `AC-E4.4` pre-emptively forbids the hub implying filter truth is fixed. That is disciplined.
- `LIST-TABS-AC.md` — the Given/When/Then survives contact with eng as written.
- `IA-PRIORITY-MATRIX.md` §B — the five fail-closed rules each inherit a standing AC and add no new metric law. This is the right way to add a layer.

The failure is not shape quality. It is that no artifact converts shape into something a client can touch.

---

## 10. What "stamped as product" means (proposed definition)

A surface is product-stamped when all five hold:

1. **One source.** Every figure on it derives from a single stamped dataset — no hand-typed numbers, no per-file drift.
2. **Reconciles.** Its total equals the same-scope total on every other surface, and equals its own export.
3. **Verifies closed.** Its AC's pre-build checklist has no open boxes.
4. **No in-artifact disclaimers.** Nothing on screen explains that part of the screen isn't real.
5. **Names are safe.** No real ERP keys, no other client's identifiers, no staff names.

By this definition: **A** passes on 3–5 and passes 1–2 once shipped. **B, C, E, F** pass none of 1–3 today.

---

## 11. Open human calls

1. **Does the gap checklist grow a Doc-✅ / Product-✅ axis?** (§6) — small edit, large effect on how the program reads its own state.
2. **Which org is the client-review pilot?** Recommend **wwjc** — it is the Bet A verify org, so the review can show a fixed filter on their own data.
3. **Do the §7 sessions wait for Bet A prod?** Recommended yes. If no, sessions must avoid every territory-scoped surface, which removes most of the rep probe.
4. **Who owns the stamped dataset?** It is a build-time data task (`ENG-HANDOFF` §E.3 treats the Mixpanel map the same way) but has no named owner.

---

## 12. Status

**Hill chart:** Bet A — over the hill, descending (in sprint, one verify open). Bets B/C/E — shaped, still climbing; blocked on the reconciliation fix, not on more shaping. Bet F — over the research hill, but the validation hill has not been started; §7 is the climb.

**Next artifact:** `CLIENT-REVIEW-HTML-BRIEF.md` (this cycle, alongside this file) — the bar the review artifact must clear, the single-dataset rule, and the rebuild-vs-new call.

---

*Cycle-04 product bar audit. Docs only. Does not change Bet A AC, does not unlock any GO, does not touch Jira.*
