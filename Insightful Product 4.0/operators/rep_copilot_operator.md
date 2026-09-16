# Rep Copilot — Applied Operator (Layer 2, Rung 3)

> **What this is.** The **runnable** Rep Intelligence operator. It is the applied skill that drives a live
> Sales-Rep-Copilot run on the **invoiced provenance spine** (Layer 1), carrying the rep-identity tier and the
> two rep-side commercial levers. It is the *application* of the spec
> [`rep_intelligence_layer2_build.md`](../build_notes/rep_intelligence_layer2_build.md) (the design) on top of the patched
> [`query_library_v2.md`](../foundation/query_library_v2.md) (the SQL).
>
> **Supersession (read this first).** This operator **supersedes the frozen copilot foundation at runtime**.
> The foundation surface — `~/Downloads/copilot_simulation/SKILL.md` + `QUERY_REFERENCE.md` — is a **locked,
> read-only** delivery shell (6 canned prompts, phases, fallback matrix, channel-qualification rules). **Do not
> edit it.** When this operator and the foundation disagree on a *number's source*, an *identity rule*, or a
> *gate*, **this operator wins**: the foundation's booked-`portal_orders` toplines and loose `ILIKE` name guess
> are exactly the defects Rung 3 fixes. The foundation is kept for its *shape*; the truth comes from here.
>
> **Trigger.** "run the rep copilot for {org}", "rep copilot / rep intelligence for {org} [rep]", or any request
> for a re-anchored rep leaderboard / rep daily push.
>
> **Inputs.** `{org_shortname}` (required); `{rep}` name-or-number (optional — if omitted, present Tier-appropriate
> candidates). The operator resolves `{ORG_ID}` and `{REPORT_THROUGH_DATE}` itself (RP-1).
>
> **MCP.** `user-supercat-postgres-vpn` (`execute_sql`, read-only) required; `user-bigquery-admin` optional
> (R3 feature depth, native `mixpanel.events`). **Read-only throughout.** Live figures `[from-live]`, design
> figures `[ILLUSTRATIVE]`. Every money number carries confidence + completeness or is suppressed.
>
> **Status: APPLIED OPERATOR — client-facing flips ✅ APPROVED 2026-06-29** (see §8). **mhc named output held**
> (dormant); the **F2 leakage dollar requires a per-report human gut-check + per-org house-account confirmation**
> at every run (approval does not bypass these). The preflight is live-validated one-org-per-tier in §9.

---

## 0. The order of operations (do not reorder)

```
RP-1..RP-5  Rep Provenance Preflight  ──► sets COMMERCE_CONFIDENCE, REP_IDENTITY_TIER,
   (run FIRST, §1)                          Mixpanel coverage, rep-seat roster, house_suspect set
        │
        ▼
Identity-tier router (§2)  ──► Tier 2: named  |  Tier 1: rep_number grain  |  Tier 0: behavior-only
        │
        ▼
RS-01 re-anchored leaderboard (§3)  ──► invoiced net, name-bridged (T2), house-flagged
        │
        ▼
Commercial levers (§4)  ──► C2 leakage-by-rep + rep $-at-risk   (gated + capped + tier-named)
        │
        ▼
Behavior floor (§5, always-on)  ──► R1–R4; standalone Mixpanel score stays DEMOTED (no $ = not a lead)
        │
        ▼
6-prompt assembly (§6, foundation shell)  ──► numbers swapped onto the above; client flips ✅ APPROVED (§8)
```

**One line:** *the copilot already ships answers to a rep; this operator makes those answers true, adds the
dollar, and refuses to name a rep it cannot prove.*

---

## 1. RP — Rep Provenance Preflight (run FIRST; it sets the whole run's posture)

Run all five before any rep number is shown. They set one confidence + identity posture the entire run inherits.

| Step | Gate | Emits | Forces |
|---|---|---|---|
| **RP-1** | **`Q-ECON-00` LIVE** (Spine §6.8; doctrinal ancestor `Q-PROV-00` §6.1) | `TOTAL_BUSINESS_SOURCE`, `COMMERCE_CONFIDENCE` ∈ {STRONG, PARTIAL, NONE}, `report_through_date` | The cap every rep dollar inherits; clamps every window. |
| **RP-2** | Rep-identity tier (Spine §7.1) | `REP_IDENTITY_TIER` ∈ {0,1,2} | Named (T2) / `rep_number`-only (T1) / behavior-only (T0). |
| **RP-3** | Mixpanel coverage (Rep map §3.2) | `CORROBORATED` / `LOGINS-ONLY` | Whether R3 feature-depth runs or degrades to login/order effort. |
| **RP-4** | Active-rep roster (Rep map §3.3) | rep-seat set (`last_ipad_login_at IS NOT NULL` ∪ order authors) | Excludes B2B-buyer accounts from per-rep metrics. |
| **RP-5** | House-account flag (Spine §6.10) | `house_suspect` bill-to set | Excludes `HOUSE ACCOUNT`/`ZZ*`/`ACCOM*`/… from the rep headline. |

**RP-1 binding:** `COMMERCE_CONFIDENCE = NONE` → **suppress every rep dollar** (RS-01 invoiced columns, C2, rep
$-at-risk); run behavior-only. `PARTIAL` (stale > 45d or eCat > 1.05× invoiced) → every rep dollar is a
**labeled floor**, never a hard CRITICAL. `STRONG` → push normally. `report_through_date = LEAST(MAX(invoice_date),
CURRENT_DATE)` — clamps the fantasy-date orgs (clm carried 4107, jyc 2032).

**RP-2 — the canonical, date-aligned tier preflight (validated live, §9).** The numerator window is the SAME
12-month invoice `rep_number`s as the denominator, so `name_bridge_pct` caps at 100% and the boundary is
mechanically reliable. (The earlier un-dated bridge counted `rep_number`s across all time and could exceed 100%,
overstating gh/scw/sc into Tier 2.)

**Tier-bridge hysteresis band (2026-06-30, Spine §7.1).** The 80% boundary oscillates on real feeds (hfg moved
79.3% → 81.0% in 30h on natural data refresh, flipping its reported tier and report shape). The boundary is now
a band: **promote to Tier 2 at `name_bridge_pct ≥ 82%`; the 78%–82% deadband is Tier 1 unless the org is a
declared Tier-2 carry-over (the §1 cohort tier-map list below); below 78% drops out of Tier 2.** The SQL emits
Tier 2 at `≥82` only; the deadband-hold for declared carry-overs (currently `bcf` 81.8%) is applied at the
application layer in the cohort tier-map below, so the rule is fully deterministic — same run twice on a
boundary org returns the same tier with no implicit per-run state.

```sql
-- REP_IDENTITY_TIER for {{ORG_ID}}: 0 = no rep key, 1 = rep_number only, 2 = named reachable.
-- Hysteresis (2026-06-30): promote at >=82; 78-81.99 is the deadband and returns Tier 1 here.
-- Declared Tier-2 carry-overs in the deadband (currently bcf at 81.8%) are HELD at Tier 2 by the
-- operator at the application layer via the §1 cohort tier map, NOT re-promoted by this SQL.
WITH rtd AS (SELECT LEAST(MAX(invoice_date), CURRENT_DATE) AS d
             FROM portal_invoices WHERE organization_id = {{ORG_ID}}),
reps AS (   -- the SAME 12-month invoice rep_numbers used as the denominator
  SELECT DISTINCT NULLIF(pi.rep_number,'') AS rep_number
  FROM portal_invoices pi, rtd
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN rtd.d - INTERVAL '12 months' AND rtd.d
    AND pi.rep_number IS NOT NULL AND pi.rep_number <> ''
),
named_reps AS (   -- portal_orders is the SOLE bridge from invoice rep_number -> rep name
  SELECT DISTINCT rep_number FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> ''
)
SELECT
  COUNT(*)                                                       AS distinct_repnum,
  COUNT(*) FILTER (WHERE n.rep_number IS NOT NULL)               AS resolves_to_name,
  ROUND(100.0*COUNT(*) FILTER (WHERE n.rep_number IS NOT NULL)
        /NULLIF(COUNT(*),0),1)                                   AS name_bridge_pct,
  CASE WHEN COUNT(*) = 0 THEN 0
       WHEN 100.0*COUNT(*) FILTER (WHERE n.rep_number IS NOT NULL)
            /NULLIF(COUNT(*),0) >= 82 THEN 2     -- hysteresis: promote at >=82
       ELSE 1 END                                                AS rep_identity_tier
FROM reps r LEFT JOIN named_reps n ON n.rep_number = r.rep_number;
```

> **Performance note (live):** keep RP-2 to **one org per call** and bridge with a `LEFT JOIN` to a distinct
> `named_reps` set (above). The `EXISTS`-per-rep form in the build doc, and a multi-org `VALUES` fan-out, both
> time out at the 30s restricted-mode limit. The join form returns instantly on cci/clm/bcf.

**RP-2 cohort tier map (date-aligned, re-confirmed live 2026-06-29; hysteresis-banded 2026-06-30):**

| Tier | Orgs (date-aligned bridge %) | Rep reporting mode |
|---|---|---|
| **2 — named** (promote ≥82%, deadband-hold 78–82% only for declared carry-overs) | sarreid 100, clc 100, **mhc 100 ⚠ DORMANT**, cci 100, wwjc 98.8, pf 89.7, ril 87.7, **bcf 81.8 (deadband-hold, declared carry-over)** | Named rep → revenue allowed (capped by `COMMERCE_CONFIDENCE`). |
| **1 — `rep_number`-only** (9) | gh 39, scw 36, sc 3.2, clm 0, clli, bri, vic, shl, jyc | Attribute to `rep_number` grain; **no names**. |
| **0 — no rep key** (4) | **ufi, heb, kll, lpf** | **Suppress rep → revenue**; ship behavior-only. |

**Hysteresis band (2026-06-30; Spine §7.1).** The RP-2 SQL above emits Tier 2 only at `name_bridge_pct ≥ 82%`;
the 78–82% deadband returns Tier 1. The application-layer **declared Tier-2 carry-over list** below holds an
org at Tier 2 inside that deadband — the only carry-over today is `bcf` (81.8%). New deadband orgs default to
Tier 1 (the conservative posture — never name a rep we can't reliably bridge). The hfg case (79.3% → 81.0%
across a 30h feed refresh) now returns Tier 1 deterministically in both runs.

**Declared Tier-2 carry-overs (deadband-hold list, application-layer):**
- `bcf` (81.8%) — boundary org, reps are agencies, validated in §9 and `rung4_option_a_operator.md` §7.

**Two flags this operator hard-codes:**
- **bcf = Tier 2 at 81.8% (deadband-hold)** — it falls inside the 78–82% hysteresis band but is held at Tier 2
  via the declared-carry-over list above. bcf is Tier 2 in both the build doc
  (`rep_intelligence_layer2_build.md`) and this operator (live-confirmed 81.8% in §9).
- **mhc = Tier 2 (100%) but DORMANT** — last invoice 2025-12-22, last login 2026-02-28 (§9). Names are
  technically reachable, but **carry a freshness/dormancy banner** on every mhc named-rep output and never push
  its $-at-risk as live; `report_through_date` pins to its last real invoice.

---

## 2. The 3-tier identity router (named ONLY at Tier 2)

The foundation resolves names with a loose `ILIKE rep_first_name || '%'` guess that can mis-map and **silently
drops** unmapped `rep_number`s — a fabricated leaderboard, the Spine §7.1 red line. Replace it with:

| `REP_IDENTITY_TIER` | Leaderboard / outcome | Behavior layer (R1–R4) |
|---|---|---|
| **2 — named** | Named reps on invoiced net (RS-01, §3). Unmapped `rep_number`s shown as `rep <n>`, **never dropped**. Carry the mhc dormancy banner where applicable. | Full, named. |
| **1 — `rep_number`-only** | Rank at `rep_number` grain; label `rep <n>`; **no names**; do **not** invent a name from eCat order authorship for the outcome. | Full (eCat author names allowed for *in-app behavior*; the *outcome* stays `rep_number`). |
| **0 — no rep key** | **No rep → revenue at all.** Suppress RS-01/SUP-01 invoiced columns; booked-orders companion only if the client asks, clearly labeled. | Full **behavior-only** run — the default design, not a degraded one. |

**Verbatim rule (Spine §7.1):** *never rank reps by revenue while silently dropping the reps whose `rep_number`
did not resolve.* Suppress, or label at `rep_number` grain — never fabricate.

---

## 3. RS-01 — re-anchored rep leaderboard (invoiced net + name bridge + house flag)

The rep-side **D1 fix**: every "total business" number swaps from booked `portal_orders.total_amount` (off 4×–9×)
onto invoiced `portal_invoices.net_amount`, capped at `COMMERCE_CONFIDENCE`. `portal_orders` is kept only as a
labeled **"booked orders"** companion (and is the *only* source when `TOTAL_BUSINESS_SOURCE='ORDERS'`).

| Foundation query | Today (booked) | Re-anchored (invoiced) | Library source |
|---|---|---|---|
| `RS-01` leaderboard | `SUM(portal_orders.total_amount)` by rep | `SUM(portal_invoices.net_amount)` by `rep_number`, name via bridge, **house-flagged** | **Q-51** |
| `SUP-01` rep book stats | `SUM(po.total_amount)` | invoiced `net_amount`, clamped to `report_through_date` | Q-51 / Q-16 |
| `P1-02`/`P1-04` trends | booked monthly | invoiced monthly (booked = labeled companion) | Q-16 |
| `SUP-03` capture rate | eCat / booked | eCat-SALE / **invoiced** net; **only if `FEED_COMPLETENESS=CORROBORATED`** else absolute $ | **Q-45** |
| header `$X LTM GMV` | booked | **invoiced LTM net** + confidence label | Q-16 |

```sql
-- RS-01: rep leaderboard on INVOICED net, name-bridged (Tier 2), house-account flagged. Source: Q-51.
-- Tier 2 -> rep_label = name; Tier 1 -> rep_label = 'rep <n>'; Tier 0 -> this query does not run (RP-2 suppressed it).
--
-- HOUSE SCREEN (TWO LAYERS — both must be applied; see config/house_rep_exclusions.md):
--   1. CUSTOMER-side house_suspect (bill-to patterns — kept as-is below).
--   2. REP-LABEL screen (NEW 2026-06-30):
--        a) AUTO-RULE — drop any rep_label ILIKE 'house%' or like '% house account%'  (catches cci HOUSE ACCOUNT,
--           kal House Account rep 0999, wwjc "12 House Account" / "30440 Interim Rep House Account").
--        b) PER-ORG EXCLUDE list — drop the named entities in config/house_rep_exclusions.md for {{ORG_ID}}
--           (e.g. clc 'Capital Lighting Fixture', ril 'Ratana', pf 'PALECEK - LAGUNA SHOWROOM' …).
--      The per-org list is templated in at run time by the operator from the config file; the auto-rule is
--      hard-baked here so a never-onboarded org (kal in the 2026-06-30 PASS1) still gets screened.
WITH rep_names AS (   -- invoices carry rep_number only; bridge to name via portal_orders
  SELECT DISTINCT ON (rep_number) rep_number, rep_name   -- DISTINCT ON: one deterministic name per rep_number (G-A dedup)
  FROM portal_orders
  WHERE organization_id = {{ORG_ID}} AND rep_name IS NOT NULL AND rep_name <> ''
  ORDER BY rep_number, rep_name
),
flagged AS (
  SELECT pi.rep_number, pi.net_amount, pi.customer_bill_to_number AS cust,
         -- window tag: TRUE = trailing 12 months (LTM); FALSE = prior matching 12 months (12–24 mo back).
         -- Lets the leaderboard emit prior_ltm_invoiced so gather.load_reps() can compute a real YoY %.
         (pi.invoice_date > {{REPORT_THROUGH_DATE}}::date - INTERVAL '12 months') AS is_ltm,
         -- house_suspect (CUSTOMER side): SINGLE SOURCE OF TRUTH = Q-ECON-LEAK list (query_library_v2.md).
         (   COALESCE(pi.customer_bill_to_number,'') ILIKE 'ZZ%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'ACCOM%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'SAMPLE%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'HOUSE%'
          OR COALESCE(pi.customer_bill_to_name,'')   ILIKE 'HOUSE ACCOUNT%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'DISPLAY%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'SHOWROOM%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'TEST%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'MODEL%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'PHOTO%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'MISC%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'NOCHARGE%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'NO CHARGE%'
          OR COALESCE(pi.customer_bill_to_number,'') ILIKE 'COMP %'
         ) AS house_suspect
  FROM portal_invoices pi
  WHERE pi.organization_id = {{ORG_ID}}
    AND pi.invoice_date BETWEEN {{REPORT_THROUGH_DATE}}::date - INTERVAL '24 months' AND {{REPORT_THROUGH_DATE}}::date  -- 24mo: LTM + prior window for YoY
    AND pi.rep_number IS NOT NULL AND pi.rep_number <> ''
    AND pi.net_amount < 5000000   -- Spine §6.6 row cap
),
labeled AS (
  SELECT
    COALESCE(rn.rep_name, 'rep ' || f.rep_number) AS rep_label,
    (rn.rep_name IS NOT NULL)                     AS named,
    f.net_amount, f.cust, f.house_suspect, f.is_ltm
  FROM flagged f
  LEFT JOIN rep_names rn ON rn.rep_number = f.rep_number
),
screened AS (
  SELECT *,
    -- REP-LABEL screen (NEW 2026-06-30):
    --   AUTO-RULE: 'house%' or '<prefix> house account%' (case-insensitive). Fires on EVERY org.
    (   COALESCE(rep_label, '') ILIKE 'house%'
     OR COALESCE(rep_label, '') ILIKE '% house account%'
     -- PER-ORG EXCLUDE: templated in by the operator at run time from config/house_rep_exclusions.md.
     -- The operator MUST inject the {{ORG_ID}}'s rows here as additional rep_label literals, e.g.:
     --   OR rep_label IN ('Capital Lighting Fixture')        -- clc (org 40)
     --   OR rep_label IN ('Ratana','Thomas York*DoNoUse')    -- ril (org 245)
     --   OR rep_label IN ('PALECEK - LAGUNA SHOWROOM', 'GMASOUTH - SO/SO CAL TERRITORY', 'DC BRANDS INC', 'LUXECO / ELITE LIGHTING')  -- pf
     --   OR rep_label IN ('Ecom-Sidney','Multimeuble - Caribbean')   -- mhc
     --   OR rep_label IN ('Morgan Horwitz: E-Comm')          -- bcf
     -- If no rows for {{ORG_ID}} in the config, the auto-rule still fires.
    ) AS rep_label_excluded
  FROM labeled
)
SELECT
  rep_label, named,
  ROUND(SUM(net_amount) FILTER (WHERE is_ltm AND NOT house_suspect AND NOT rep_label_excluded)::numeric, 0)     AS invoiced_net_ltm,
  ROUND(SUM(net_amount) FILTER (WHERE NOT is_ltm AND NOT house_suspect AND NOT rep_label_excluded)::numeric, 0) AS prior_ltm_invoiced,
  ROUND(SUM(net_amount) FILTER (WHERE is_ltm AND (house_suspect OR rep_label_excluded))::numeric, 0)            AS house_net_excluded,
  COUNT(DISTINCT cust) FILTER (WHERE is_ltm AND NOT house_suspect AND NOT rep_label_excluded)                   AS accounts,
  BOOL_OR(rep_label_excluded)                                                                                    AS is_house_rep_label
FROM screened
GROUP BY rep_label, named
HAVING BOOL_OR(rep_label_excluded) = FALSE   -- house reps are EXCLUDED from the leaderboard render entirely
ORDER BY invoiced_net_ltm DESC NULLS LAST
LIMIT 25;
```

**Tier 1 variant:** drop the `rep_names` join entirely (or keep it but render `rep_label = 'rep ' || rep_number`
regardless) so no name leaks. **Tier 0:** do not run — RP-2 already suppressed rep → revenue.

**House-rep render rule (NEW 2026-06-30).** Rows with `is_house_rep_label = TRUE` are **excluded from the
leaderboard render entirely** (the `HAVING` clause drops them); they are surfaced separately in a *"House
buckets (not coached)"* row beneath the table with the dollar and account count, so the dollar is visible
but cannot anchor a finding. **Never render a house-rep label as a §2 leaderboard row, a §2 coaching card,
or a §3 mini-brief rep cell.** This closes the cci-HOUSE-ACCOUNT-at-#1 defect (PASS1 2026-06-30).

**Claim rules:** "total business" = invoiced net, labeled with `COMMERCE_CONFIDENCE`. On `PARTIAL` feeds present
as a directional floor. Never present capture as a *rate* of total business unless `FEED_COMPLETENESS=CORROBORATED`
(else absolute $). **House-flagged dollars are excluded from the rep headline** and surfaced separately for the
one-time per-org owner review (live: on cci the #1 raw "rep" is `HOUSE ACCOUNT` $10.1M / 112 accts — the auto-rule
now drops it; on kal `House Account` rep 0999 $1.60M is dropped by the same rule even though kal is not in the
EXCLUDE table). Reps with 0% eCat capture are legitimate findings.

---

## 4. The rep-side commercial levers (the missing dollar — wired from Layer 1)

The foundation answers "who needs attention" with eCat order velocity (behavior). This operator adds the two
**dollar-weighted** rep exceptions from [`selling_customer_exception_layer.md`](../foundation/selling_customer_exception_layer.md),
each one row of the exception object (`type, severity, dollar_impact, subject, who_to_call, one_line, evidence, confidence`).

### 4.1 C2 — Leakage-by-Rep (the "rogue discounting" alarm)
- **As-is** from the exception layer: tier-aware dispersion (`Q-ECON-LEAK`) rolled to `rep_number`, after the
  true-median + tier guard (price shared by ≥5 customers) + volume guard (account ≥10% of a SKU's units) +
  `house_suspect` exclusion. Never "% off list".
- **Rep-layer binding:** the rep **dollar is suppressed below STRONG** (cap at `COMMERCE_CONFIDENCE`); **naming
  the rep requires Tier 2** (else report at `rep_number`); requires `leakage_dispersion_ok` (priced lines ≥60%);
  **mandatory human gut-check before client delivery.**
- **Pushed shape (asi, live):** *"Rep 12 carries the widest discretionary spread — ~$163K, 5.9% of their book,
  vs ~2% peers. Worth a discount-discipline conversation."* (Rep 69, the old "$1.35M/42% rogue", is a normal 2.1%
  once tiers/volume are excluded — exactly the false-positive the guards exist to prevent.)

### 4.2 Rep-attributed Revenue-at-Risk (S1 rolled to the owning rep)
- **Source:** the `S1` per-account decay query (equal 6-month windows anchored on `report_through_date`). The
  account's `MAX(rep_number)` is the `who_to_call`; roll `$-at-risk` up by rep for a book-health view.
- **Gating:** S1's precondition — **NONE → suppress**, **PARTIAL → labeled floor** ("at-risk ≥ $X, partial feed"),
  **STRONG → push**. Rep naming again requires **Tier 2**. On **Tier 0** the per-account alarm still fires (it is
  customer-grain) but **without a rep owner** → routes to sales management, not a named rep.
- **Pushed shape (cci, live, Tier 2):** *"HATCH P is down 79% over 6 months ($58K → $12K), $70K LTM at risk —
  call rep MKJ."*

### 4.3 The rep daily push
Sort by `dollar_impact × severity_weight`, cap ~12 items (Spine §8 action-first). The behavior floor (R1–R4) is
the always-on context; these two exceptions are the **dollar-weighted lead** when (and only when) the feed +
identity tier permit.

---

## 5. The behavior floor (R1–R4) — always-on; vanity stays DEMOTED

- **R1 activity/cadence, R2 coverage, R3 feature depth, R4 quote→submit** ship exactly as in the Rep map —
  ERP-optional, FULL/STRONG, never dark. They are the foundation's Prompts #2/#5/#6 backbone and need no re-anchor.
- **R3 feature depth** runs at `CORROBORATED` Mixpanel coverage (20/21 cohort orgs, native `mixpanel.events`) and
  **degrades to login/order effort** at `LOGINS-ONLY` (**mhc**). Never fabricate feature engagement from absence.
- **The standalone Mixpanel "rep-engagement score" (0–10) stays DEMOTED.** Per the north-star it is **vanity
  until fused to a dollar** — **no dollar = not a lead.** Do **not** surface a behavioral score as a lead in the
  rep push. The behavior × outcome fusion (app usage × leakage/$-at-risk) is **Rung 4, owner-gated, explicitly
  NOT built here** (`rung4_fusion_decision_brief.md`).

---

## 6. The retrofitted 6-prompt map (foundation shell kept; data swapped)

| Prompt | Kept (behavior, from foundation) | Re-anchored / added here |
|---|---|---|
| #1 "Prep me for [Customer]" | eCat reorder cadence | "total business" trend → **invoiced** (Q-16); confidence label on the header |
| #2 "Who needs attention?" | dormant/declining eCat | **+ rep-attributed revenue-at-risk (S1, §4.2)** with $ + who-to-call, capped at `COMMERCE_CONFIDENCE` |
| #3 "What should I show?" | inventory × sales | unchanged (catalog/inventory, not a topline) |
| #4 "Customers like X buying?" | peer category | peer compare on **invoiced** category value where feed permits |
| #5 "Best new-account opps?" | activation/territory | opportunity sizing by **invoiced** GMV |
| #6 "Who else nearby?" | proximity | nearby account value → **invoiced**; booked labeled where invoices absent |
| header / leaderboard | — | **RS-01 invoiced + house flag + identity tier** (§2/§3); capture rate gated |
| daily push (new) | — | **C2 leakage-by-rep + rep $-at-risk**, ranked `$ × severity`, ~12 cap (§4) |

The foundation's Global Guardrails still apply verbatim: `orders.is_marked_deleted` guard, `NOT IN` null safety,
the `portal_orders` semantic-framing rule, the eCat-SALE filter, and the metric channel-qualification rule.

---

## 7. Phase-B query hygiene (consumed from the patched library — do not re-author)

These were specced in the build doc and are **already applied + live-validated in `query_library_v2.md`**
(2026-06-29). This operator **consumes** them; it does not re-author them:
- **Q-63/64/65** repointed `supercat-data-pipeline.WELD_RAW.mixpanel__events` → native
  `supercat-data-pipeline.mixpanel.events` (+ `LOWER(COALESCE(organization_shortname, current_organization_shortname)) = '{{ORG_SHORTNAME}}'`).
- **Q-69** (`orders.submitted_at` → `submit_date`, + `is_submitted`/`is_marked_deleted` filters) — eCat order
  *timing* (behavior), label accordingly.
- **Q-70** (`org_users.role/active/last_login` → `user_types`/`last_ipad_login_at`/`disabled`), invoiced
  re-anchor, **Tier-2 name gate** (the name join is Tier-2-only; Tier 1 = `rep_number` grain; Tier 0 cannot run).

---

## 8. Owner gates — ✅ APPROVED 2026-06-29 (with standing runtime gates)

The client-facing flips are **owner-approved** (2026-06-29), under the same discipline as
[`selling_customer_label_signoff.md`](../build_notes/selling_customer_label_signoff.md) — see
[`rep_intelligence_label_signoff.md`](../build_notes/rep_intelligence_label_signoff.md) for the signed rows. **Approval does
NOT bypass the standing runtime gates:**

1. **Named reps in client-facing output** (Tier 2 only) — ✅ **APPROVED** for the **7 fresh Tier-2 orgs**;
   **mhc named output HELD behind a dormancy flag** until its feed refreshes.
2. **The rep leakage dollar (C2)** — ✅ **APPROVED**, capped at `COMMERCE_CONFIDENCE` (never ships below STRONG),
   with a **mandatory human gut-check per report + per-org `house_suspect` confirmation per client** before any
   number ships. Framing **locked to "discount-discipline / coaching," NEVER "rogue"**; audience = sales manager.
3. **The rep $-at-risk push (S1-by-rep)** — ✅ **APPROVED**: NONE→suppress, PARTIAL→floor, STRONG→push; Tier 0
   routes to sales management.

**Frozen / deferred:** the behavior × outcome **fusion** is **Rung 4, owner-gated** — not here. Segmentation is
Rung 5, frozen. One-org-only signals (`sales_quotas`→sarreid, `commitment_reports`→ufi, `placement_reports`→
ufi/cci/clm) stay out of cohort runs — org-scoped conditionals at most.

---

## 9. Live validation `[from-live]` (read-only `user-supercat-postgres-vpn`, 2026-06-29)

**RP-2 identity-tier preflight — one org per tier (date-aligned bridge, the §1 SQL):**

| Org (oid) | distinct rep# (12mo) | resolves to name | name bridge % | `REP_IDENTITY_TIER` | Verdict |
|---|---|---|---|---|---|
| **cci (161)** | 54 | 54 | **100.0%** | **2 — named** | Named reps allowed (capped by `COMMERCE_CONFIDENCE`). |
| **clm (64)** | 47 | 0 | **0.0%** | **1 — `rep_number`-only** | Rank at `rep_number` grain; **no names**. |
| **ufi (18)** | 0 | — | — (62,170 invoices, **0** with `rep_number`) | **0 — no rep key** | **Suppress rep → revenue**; behavior-only. |

**Edge cases flagged by the task — both confirmed live:**

| Org (oid) | Finding | Consequence |
|---|---|---|
| **bcf (171)** | 33 distinct rep#, 27 resolve → **81.8%** date-aligned bridge; last invoice 2026-06-26 (fresh) | **Tier 2** (clears ≥80%) — bcf is Tier 2 in both the build doc and this operator (already corrected). |
| **mhc (46)** | bridge 100% but **DORMANT**: last invoice **2025-12-22**, last login **2026-02-28** | **Tier 2 but carry a dormancy banner**; pin `report_through_date` to last real invoice; do not push $-at-risk as live. |

The preflight correctly **names** on Tier 2, **de-names** on Tier 1, and **suppresses** on Tier 0; the boundary
(bcf 81.8%) and the dormant-but-named (mhc) cases both resolve as the spec requires. RS-01 + house flag were
live-validated on cci in the build doc (§9 there): #1 raw = `HOUSE ACCOUNT` $10.1M (112 accts) → excluded; top
*named* reps resolve via the bridge.

---

## Appendix — method, provenance, supersession

- **Read-only** throughout (`user-supercat-postgres-vpn` `execute_sql`), 2026-06-29.
- **Inherits (consume, do not re-author):** `provenance_spine.md` (§1 invoiced axiom, §5 tiers, §6.3/6.8 caps,
  §6.10 tier-aware leakage, §7.1 the 3-tier gate); `provenance_map_rep.md` (R1–R6); `rep_data_census_phaseA.md`
  (Phase A surface); `selling_customer_exception_layer.md` (C2, S1); `selling_customer_label_signoff.md`
  (approved labels); `query_library_v2.md` LIVE IDs per `WHAT_ACTUALLY_RUNS.md` — plus BACKLOG
  Mixpanel/rep bodies `Q-63/64/65`, `Q-69`, `Q-70` (patched in library; **not** in factory `QUERIES_ALL`);
  `rep_intelligence_layer2_build.md` (the design spec this applies).
- **Supersedes at runtime** the frozen `~/Downloads/copilot_simulation/SKILL.md` + `QUERY_REFERENCE.md` — kept
  for delivery shape only; not edited.
- **Constraints honored:** every rep dollar carries `COMMERCE_CONFIDENCE` + completeness or is suppressed; rep
  naming obeys the 3-tier gate (named only at Tier 2; bcf=Tier 2; mhc=Tier 2-DORMANT); leakage is dispersion
  (never "% off list"); no margin/AR/collection implied from invoices; behavior-only is the default; the
  standalone Mixpanel score stays demoted (no dollar = not a lead).
- **Status:** APPLIED OPERATOR, preflight live-validated one-org-per-tier. **Client-facing rep naming +
  leakage/$-at-risk ✅ APPROVED 2026-06-29** (mhc named output held, dormant; F2 keeps its per-report gut-check +
  per-org house confirm). Rung 4 (fusion) is owner-gated and separate.
