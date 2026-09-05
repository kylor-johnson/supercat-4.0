# Bet F persona IA demo — illustration walk

**File:** `design-system/app/sales-portal-persona-ia-demo.html`
**Audience:** betting table, persona/IA conversation, customer A/B setup
**Status:** **Illustration only** — docs are the SoT (`IA-RECOMMENDATION-v0.md`, `IA-PRIORITY-MATRIX.md`, `PERSONA-ONE-PAGERS.md`). Does **not** unlock Bet A GO. Friday demos untouched.

---

## What this is (and is not)

This is a **cloned copy** of `sales-portal-internal-demo.html` with an additive Bet F layer on top — same `.kshell`, same tokens, same nav order, same COPY-AUDIT voice. It illustrates **role-aware defaults over one shared surface**, not a forked role-based product.

| Is | Is not |
|---|---|
| A visual of "who sees what first" (default home + must-see lead per persona) | A nav fork / a new product |
| An illustration of the five fail-closed rules | A build spec or a new Bet A AC |
| Default homes labeled **HYPOTHESIS** (pending customer A/B) | A GO unlock or a Friday-demo change |

Canonical authority stays the docs. Per `DEMO-SURFACE-CONTRACT.md`, the priority matrix is the **ordering authority for future Bet B work** — this HTML does not reorder nav or rewrite the per-surface primary jobs.

---

## Open in browser

```
file:///Users/kylorjohnson/Library/Mobile%20Documents/com~apple~CloudDocs/SuperCat%204.0/design-system/app/sales-portal-persona-ia-demo.html
```

First screen should feel like the **same product as `sales-portal-internal-demo.html`** with a persona switch added — real page content leads, Bet F chrome is secondary. Lands on the **Sales-rep** default (Customers).

**Chrome craft (Phase 4 POLISH — matches internal demo):**

- **One compact persona control** in the **topbar-right** ("View as · Sales rep / Owner/VP / Admin/ops"), sitting with the existing metatags — no stacked banner + note + fail-closed strip.
- **Per-tab cue = one quiet line under the page title** (small rank pill + persona + surface lead + rule), not a fat MUST/HIDE billboard above the H1.
- **No view dimming.** Opacity / grayscale removed entirely — full density on every tab, including demote/hide surfaces (the rank pill carries the honesty, not a greyed-out page).
- The illustration disclaimer is **one short footer line**; the fail-closed rules (R1–R5), the default-home hypotheses, and the out-of-scope Feature Usage note live **here in the runbook**, not in sticky chrome.

---

## The additive layer

- **Persona switcher (persistent, topbar-right):** Sales rep · Owner/VP · Admin/ops. The chosen persona is a **session state** (`currentPersona`) — it does not reset when you change tabs.
- **On switch → the persona jumps to its recommended default home once** (HYPOTHESIS), and the global note names the **must-see lead**:

| Persona | Default home (HYPOTHESIS) | Must-see lead | Fail-closed cue shown |
|---|---|---|---|
| **Sales rep** | **Customers** | only your territory's customers + invoiced total that moves with your book (EBR-40) | **R1** — empty/zero territory → empty book, never whole-org |
| **Owner/VP** | **Intelligence** | invoiced sales (C1) + accounts fading (S1) + team activity | **R2** — named rep→revenue (RS-01) never the default lead |
| **Admin/ops** | **Settings hub** | enablement + who-sees-what · Reports/Invoices for reconciliation | **R3/R4** — Revenue defs visible-but-locked 🔒 · SuperCat-only levers hidden |

- **Per-tab persona cue (the fix):** every surface re-themes to the active persona via `applyPersonaToView(persona, view)`, called from **both** `setPersona()` **and** `nav()` / `navReports()`. A **quiet one-line cue sits under the page title** showing that persona's rank for that surface via a small pill — **MUST** (green pill) / **nice** (grey) / **not your landing** (clay) / **HIDE · not for you** (red) / **teaching** (gold). On the persona's default-home surface the cue also tags `default home · HYPOTHESIS`. The page stays full-density in every case — the pill color carries the honesty, not a dimmed page. Switch persona while sitting on a tab, or click across tabs — no stale owner copy ever shows on a rep session.

**Per-surface rank (`IA-PRIORITY-MATRIX.md` §A × R1–R5):**

| Surface | Sales rep | Owner/VP | Admin/ops |
|---|---|---|---|
| **Dashboard** | not your landing (org chrome ≠ your book) | nice glance | nice glance |
| **Customers** | **MUST** — territory-scoped, export=screen (R1) | nice — whole-org rollup only if granted (R1) | nice — reconcile, export=screen |
| **Orders** | **MUST** — confirmed vs quotes (EBR-87) | nice — backlog ≠ sales | nice — quotes never counted as sales |
| **Invoices** | **MUST** — total moves with territory (EBR-40) | nice — org total | **MUST** — export = UI (EBR-91) |
| **Reports** | nice — my scope | **MUST** — invoiced net C1 spine | **MUST** — reconcile, export = total |
| **Intelligence** | nice — my accounts fading (S1) | **MUST** — C1 + S1 + team, never RS-01 lead (R2) | nice — read-only |
| **Settings** | **HIDE** — not for you | nice — read-only 🔒 (R3) | **MUST** — enablement + 🔒 gates (R3/R4) |
| **What's broken** | teaching | teaching | teaching |

- **Fail-closed rules (reference, not sticky chrome):** the five rules below are the always-true guardrails behind the demo. The active persona's per-tab cue surfaces the surface-specific rule inline (R1 / R2 / R3–R4 / EBR-40 / EBR-91 / C1); the full set lives here in the runbook and in a one-line footer, not in a stacked strip:
  - **R1** — empty / zero territory → only your accounts, never the whole org.
  - **R2** — named rep→revenue (RS-01) is never the default lead.
  - **R3/R4** — Settings 🔒 client vs SuperCat gates; revenue definitions visible-but-locked.
  - **EBR-40 / EBR-91** — invoiced total moves with territory; export = the screen.
  - **C1** — Sales Summary = invoiced net.

---

## 4-minute walk order — prove persona reshapes *every* tab

1. **Sales rep (loads here).** Lands on Customers → **MUST**, "only your territory's customers" (R1). **Stay a rep and click across tabs:** Invoices → **MUST** total moves with territory (EBR-40); Orders → **MUST** confirmed vs quotes; **Dashboard → "not your landing"** (clay pill, page still full-density); **Settings → "HIDE · not for you"** (red pill, page still readable). One persona, every tab re-themed — the cue pill changes, the page never greys out.
2. **Switch to Owner/VP while sitting on Settings.** The Settings tab re-themes in place: rep's "HIDE" flips to owner's **nice · read-only 🔒** — no stale copy. Then jump home to Intelligence → **MUST** C1 + S1 + team, never RS-01 (R2); Reports → **MUST** invoiced net (C1 spine); Customers → nice whole-org only if granted (R1).
3. **Switch to Admin/ops.** Lands on Settings → **MUST** enablement + 🔒 gates (R3/R4); Reports → **MUST** reconcile/export=total; Invoices → **MUST** export = UI (EBR-91); Intelligence → nice read-only.
4. Point at the **per-tab cue + the footer disclaimer**: same shared surface, honest to three personas by *what leads + what's gated* (fail-closed rules R1–R5, spelled out above), not a fork. Open side-by-side with `sales-portal-internal-demo.html` — the first screen is the same product plus a persona switch, not a review overlay.

Close: default homes are **HYPOTHESIS** pending customer A/B (rep Customers vs Invoices; is the CEO a portal end-user; hero-priority vs nav landing) — recruit from wwjc / sarreid / cci / ufi.

> **Separate project (not this demo):** the eCat **Feature Usage Report** (Admin Console · SuperCat-admin only · Mixpanel → BigQuery adoption analytics, Courchesne track) is a **separate PM/eng project** — it is **not** part of this Bet F demo. This walk does not build, port, or preview it; no adoption/feature-usage nav item, KPI dashboard, chart, or leaderboard lives here.

---

## Explicit no-gos

- Does **not** unlock Bet A GO; no new Bet A AC; no `FILTER-TRUTH-AC` / TRD / Friday-demo edits.
- Not a nav fork, not a forked product; no new metrics / margin / RS-01 lead / FULL claim.
- Default homes are recommendations, not decisions — do not present them as shipped.

---

## Spec pointers

`IA-RECOMMENDATION-v0.md` · `IA-PRIORITY-MATRIX.md` · `PERSONA-ONE-PAGERS.md` · `COPY-AUDIT-portal-mocks.md` · `DEMO-SURFACE-CONTRACT.md`

*Illustration only. Docs = SoT. Default homes = HYPOTHESIS pending customer A/B. Isolation ON. Does not unlock Bet A GO.*
