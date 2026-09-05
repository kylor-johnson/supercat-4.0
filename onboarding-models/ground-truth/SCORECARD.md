# Scorecard — framework v3.5 vs. blind ground truth

**Five clients reviewed: `tcd`, `drf`, `pebl`, `mali`, `leg` (2026-08-18 → 08-27).**
All against the live DB. § 1–5, § 7 = tcd. § 8 = drf. § 9 = pebl. § 10 = mali. § 11 = leg.

The blind run produced `JOURNEY_tcd.md` and `GAPS_tcd.md` without opening any
interpretation document. Two contamination disclosures were made voluntarily
(workspace `CLAUDE.md` auto-injection, skill descriptions visible in the tool listing);
neither defines phases, so the run stands.

---

## 1. Claim verification — every checkable claim held

| claim | verdict | evidence |
|---|---|---|
| All 7 orders belong to one rep, JC Gonzalez | **confirmed** | `orders` grouped by `rep_email`: 7/7 → `jc@finelightsales.com`, `COUNT(DISTINCT org_user_id) = 1` |
| 23 of 24 reps have never opened an order | **confirmed** | 24 reps in `Sales Reps`; 1 distinct order creator |
| SmartLists = 0 | **confirmed** | `smart_stacks` where org 282 → 0 |
| `import_active: false` is meaningless | **confirmed, and worse than stated** | `import_active` is true for **0 of 257 organizations** — dead database-wide |
| `product_synch_requires_photo` is on | **confirmed** | true for org 282 |
| ~half of tickets are duplicate captures | **confirmed** | 21 of 31 tickets collapse to 9 distinct conversations |

Zero corrections required. That is the strongest available signal that the blind method
works and is worth repeating for the other three.

---

## 2. Backtest — the framework agrees where it can be tested

Framework anchors evaluated at the blind run's dates, using only append-only sources:

| as-of | P2 anchor | latest Products tier | core types in 60d | any type latest-fatal | framework says | blind says |
|---|---|---|---|---|---|---|
| 2025-11-11 | ✅ | warning | 1 | 0 | **Phase 2** | Phase 2 ✅ |
| 2025-11-24 | ✅ | clean | 1 | 0 | Phase 2 | — |
| 2025-12-09 | ✅ | clean | **3** | 0 | **Phase 3** | Phase 3 ✅ |
| 2026-04-23 | ✅ | clean | 4 | 0 | Phase 3+ | Phase 4 ✅ |

**Both backtestable transitions agree exactly.** The Phase 1–3 anchors are sound; the
same-day 1→2 on 2025-11-11 is correctly produced by the framework (a warning-tier
Products block satisfies the anchor, and the done-when clause only excludes `:fatal`).

Phases 4–7 depend on mutable tables and cannot be reconstructed — the known limit,
unchanged.

---

## 3. Defects found

### D1 — No regression state. *(highest value finding)*

`core_types_60d` for tcd over the crisis window:

```
2026-01-15  3      2026-03-01  1   ← Phase 3 clause 1 FAILS
2026-02-01  2      2026-03-15  1   ← still failing
2026-02-15  2      2026-04-01  2   ← recovers
```

Phase 3's first clause requires ≥2 core types with an event in the last 60 days. For
roughly all of March 2026 tcd had **one**. A weekly run would have reported the client
*moving backwards* to Phase 2 — and the framework has no vocabulary for that. Phases are
presumed monotonic, so the dip reads as noise or as a stale "still Phase 3."

That window is exactly the near-churn the blind read found from the conversation record:
Scott writing that eCat "feels less like a mature commercial product and more like an
early-stage amateur implementation," and an internal Brent reply leaking into the
customer thread.

**The framework had the signal and could not say it.** Two independent methods converged
on the same date range from completely different evidence. This is the single most
useful thing the exercise produced.

**Fix:** add an at-risk / regressing state, triggered when a previously-passing anchor
stops passing. Do not let a phase silently hold.

### D2 — Phase order is not a sequence

Blind timeline: Go-Live 2026-04-28, Admin Training 2026-05-13. Terminal reached 15 days
*before* the training phase, and the training never happened as a session — three
scheduled, three no-shows, replaced by a written audit Scott accepted. Phases 4 and 5
also collapse into a single day.

Phase 7 needs any **two** of four clauses, and clauses 2+3 (reps active, real order) are
sufficient — so Phase 6 is skippable by construction. The seven-phase framing implies an
order the model doesn't enforce and this client didn't follow.

**Fix:** either state plainly that phases are a checklist rather than a sequence, or make
Phase 7 require Phase 6.

### D3 — No "live but not selling" state

Every Phase 7 condition is met. Also true: 1 rep wrote 100% of orders, 23 of 24 reps have
never opened one, 0 SmartLists, rep training never scheduled. Clause 2 counts *logins*;
clause 3 counts *one* matched order. Terminal Go-Live is reachable on a single active rep.

**Fix:** add rep-order concentration (distinct ordering reps / total reps) as a Phase 7
health metric. It is one query and it separates "launched" from "adopted."

### D4 — Author-shift rules have no minimum-volume guard

Phase 6 trigger #4 and Phase 7 clause 4 both fire at "≥40% of SuperCat-authored threads
in the last 30 days are non-Kylor." For tcd right now that denominator is **2** — both
Kyla, so 100%. A single reply satisfies a rule meant to detect a support handoff.

**Fix:** require a floor (≥5 SuperCat-authored threads) before the ratio is allowed to
fire; otherwise emit `INSUFFICIENT_VOLUME`.

### D5 — Duplicate ticket capture inflates every HelpScout count ~2×

21 of 31 tickets are duplicate captures of 9 conversations. Worst case: "terracotta
onboarding kickoff follow ups" exists as tickets 13421, 13448 and 14280 across 69 threads.
One of the duplicated subjects is literally `"welcome to supercat support, next steps:
admin training"` — the Phase 6 qualitative trigger regex, counted twice.

**Fix:** dedupe on normalized subject (strip `re:`/`fwd:`/`fw:`) before any thread count.

### D6 — `import_active` is dead across the database

True for 0 of 257 orgs. It is currently captured by `collector/queries.py` and
`collector/rawstate.py` as if meaningful. **Fixed — see § 7.**

### D7 — `visible_products` overstates iPad visibility

tcd: 397 visible, 396 with images, and `product_synch_requires_photo` is on — so one
product does not reach the iPad despite counting as visible. The metric measures
`hideable`, not what a rep can actually see.

**Fixed — see § 7:** `ipad_visible_products` now reports `visible AND (image_exists OR NOT requires_photo)`.

---

## 4. Verdict

**The framework's Phase 1–3 machinery is correct.** Both testable transitions matched a
blind reconstruction that got every checkable claim right.

**The defects are structural, not arithmetic** — missing states (regression, adoption),
missing guards (volume floors, duplicate collapse), and one dead field. None of them
would have been found by running the framework; they only surface when something
independent disagrees with it.

Net: v3.5 is closer to deployable than "never been run" suggested, provided D1 and D4
are fixed before anyone acts on its output.

---

## 5. Changes to the next three handoffs

1. **Ask for regression explicitly.** tcd's most valuable finding came from a window
   where things went backwards. The handoff should ask directly: *did this client ever
   move backwards, stall, or nearly churn — and when?*
2. **Ask about adoption separately from go-live.** "Who actually used it, how many, how
   often" is a distinct question the phase model doesn't ask.
3. **Warn about duplicate tickets up front** so the agent isn't misled by apparent volume.
   pebl (4 tickets / 94 threads) and mali (57 tier-B tickets) will look very different
   under dedup.
4. **Keep the phase-questions-only rule.** It worked — the agent produced a comparable
   timeline *and* told us the model was wrong-shaped, which it could not have done if
   it had been handed the anchors.

---

## 6. Found during drf L1 prep (before its blind read)

Recorded here because it is a framework defect, not a drf finding. The drf blind read
has not run yet and is not informed by any of this.

### D8 — Phase 7 clause 3 fires on a $0.00 order placed by the client's own admin

drf's 9 submitted orders were **all** placed by `Suzanne@dorellfabrics.com` — the client
admin and the `order_email_recipient`, not a sales rep. Eight are billed to "Suzanne" or
"Christine Son" and correctly fail the allowlist. But one names a real `customers` row
("AMALFI") and therefore **satisfies clause 3** — despite a total of **$0.00**, being
placed by the admin, and sitting alongside eight obvious self-tests.

The allowlist model (v3.2) fixed the denylist's failure mode, and it works for 8 of 9
here. The residue is that "matches a real customer name" is not sufficient when the
submitter is the org's own admin.

**Why a price floor will not fix it:** drf is a free-sample catalog. Every order is
$0.00 by design (one is $8.00). Order value cannot discriminate for this client, and
`sample_catalog` orgs are a recognised archetype.

**Fix:** exclude orders whose submitter is an org admin (`org_users.is_admin = true`) or
whose `rep_email` equals `organizations.order_email_recipient`, unless a non-admin has
also ordered. That is checkable, needs no maintained alias list, and would correctly
score drf as having never transacted through a rep.

### D3 looks systemic, not client-specific

| client | submitted orders | distinct ordering reps | total reps |
|---|---|---|---|
| tcd | 7 | **1** | 24 |
| drf | 9 | **1** (the admin) | 3 |

Two for two. `distinct_ordering_reps` is now collected by `rawstate.py`; worth watching
whether pebl and mali make it four for four. If so, "one person places every order" is
the normal post-go-live state, and a framework whose terminal phase is Go-Live is
measuring the wrong finish line.

### Live example of D1 you can watch

drf has had **no import of any kind since 2026-07-08**. Phase 3 clause 1 needs ≥2 core
file types within 60 days; drf currently has exactly 2 (Products 2026-07-06, Product
Stories 2026-07-08). On **2026-09-06** that window closes and the clause fails.

Under v3.5 drf would silently drop to Phase 2. Under v3.6 it correctly reports
`Phase 3 — AT RISK (regressed to 2)` with the failing clause named. This is the fix
working prospectively, on a real client, with a known date.

---

## 7. Changes applied

**Spec — `Phase_Anchors.md`, framework bumped to v3.6:**
- Phase 7 clause 3 → `customers.name` (the column that exists)
- HubSpot removed from `client_domains[]` resolution (also `RUN_PROMPT.md`)
- New § *Phase regression — the at-risk state* (D1)
- New § *Counting HelpScout threads* — dedupe + ≥5 floor, wired into Phase 6
  trigger #4 and Phase 7 clause 4 (D4, D5)
- Changelog entry recording what held, what changed, and what is knowingly unfixed
  (D2, D3 are recorded, not resolved — they need a design decision, not a patch)

**Code — `collector/`:**
- `import_active` dropped from `queries.py` (3 sites) and `rawstate.py`, reason inline
  so it doesn't get re-added (D6)
- `ipad_visible_products` added to both; verified live on tcd — 396 vs 397 (D7)
- `distinct_ordering_reps` and `smart_stacks` added to `rawstate.py`, so launched-vs-
  adopted is one query going forward (D3)

**Still open by design:** D2 and D3 are structural questions about what the model should
represent, and D8 needs a rule change to Phase 7 clause 3. None should be patched until
at least one more client's blind read is in.

---

## 8. Client 2 — `drf` (Dorell Fabrics), reviewed 2026-08-19

Blind run confirmed clean: no forbidden file opened, only the harness-injected workspace
`CLAUDE.md` disclosed. Corpus read in full (5,660 lines, explicitly stated as unskimmed).

### 8.1 Claim verification — zero corrections, again

| claim | verdict |
|---|---|
| `net_price` = 1.00 on all 1,627 active products | **confirmed** — exactly **1 distinct value** across the catalog |
| All 389 customers still `DefaultPriceCode = net` | **confirmed** — 389 of 389 |
| Customer file untouched since 2026-04-27 | **confirmed** — `max(updated_at)` 2026-04-27T18:59:15 |
| 1,418 products carry pricing inside the story | **confirmed** — matches Kylor's stated 1,340 + 78 exactly |
| Ten price levels created by Christine in ~6 minutes | **confirmed** — 2026-07-02 00:48:56 → 00:54:24 |
| `order_origins = []`, all orders `order_type = 'Confirmed'` | **confirmed** — 10 of 10 |
| Brian Frankel (CEO) provisioned, never logged in | **confirmed** — `last_ipad_login_at` NULL since 2026-05-03 |
| Claudia Frankel provisioned 2026-08-18, no login | **confirmed** |
| 1,512 products carry a story | **confirmed** |

**Two blind reads, two clients, zero corrections.** The method is reliable, not a fluke.

### 8.2 Backtest

| as-of | latest Products tier | core types 60d | any latest-fatal | framework | blind |
|---|---|---|---|---|---|
| 2026-04-27 | warning | 2 | 0 | **Phase 3** | Phase 2→3 same day ✅ |
| 2026-05-05 | **clean** | 2 | 0 | Phase 3 holds | "regressed" ⚠ see D10 |
| 2026-06-09 | clean | 2 | 0 | Phase 3 | firm Phase 3 ✅ |
| 2026-08-19 | clean | 2 | 0 | Phase 3+ | Phase 7 |

Phase 1–3 agree again. `core_types_60d` sits at exactly **2** at every checkpoint — the
threshold, with no margin.

### 8.3 D1, D2, D3 all replicated independently

The drf agent was never told about tcd's findings, and reproduced three of them:

- **D1** — it used the word **"regressed"** unprompted for Phase 2→3, and separately
  identified a six-week quiet period (2026-05-20 → 06-30).
- **D2** — **Phase 6→7 on 2026-07-20 precedes Phase 5→6 on 2026-07-21.** Go-live before
  admin training, exactly as tcd did (there, by 15 days). Two for two.
- **D3** — all 10 orders submitted by Suzanne, who is `is_admin = true`. **Zero field sales
  reps have ever been provisioned** — Chip, Andy and Danny have had territory codes in the
  customer file since 2026-04-27 and no accounts.

Order concentration now three for three:

| client | orders | distinct ordering users | field reps ordering |
|---|---|---|---|
| tcd | 7 | 1 of 24 reps | 1 |
| drf | 10 | 1 (the admin) | **0** |

**D3 is not a tcd quirk.** A framework whose terminal state is Go-Live is measuring the
wrong finish line.

- **D8 confirmed live** — drf's only real-customer-matched order (AMALFI) is **$0.00**, from
  the admin, alongside nine self-tests. Exactly the case D8 predicted.

### 8.4 New defects

#### D9 — `DefaultPriceCode` resolution is satisfied by a placeholder level

Phase 4 requires ≥99% of customers' `default_price_code` to resolve to a real
`price_levels.code`. drf scores **100%**: all 389 point at `net`, and `net` is a real level.

It is also a **$1.00 placeholder on all 1,627 products**. Christine built ten real price
levels on 2026-07-02, but the customer file has never been re-imported, so every customer
still points at the dollar. Kylor flagged it on 2026-07-08 — "Net is still a $1.00
placeholder" — and it is unchanged 42 days later.

The clause tests referential integrity, not whether the price is real. A catalog priced
entirely at $1.00 passes "Catalog Completeness."

**Fix:** flag when a price level referenced by >50% of customers resolves to a single
constant `net_price` across the catalog. One query.

#### D10 — import tier says nothing about catalog correctness *(the more serious one)*

On 2026-05-05 drf's Products imports were **clean ×5 and fatal ×1 on the same day**. The
most-recent-block rule resolves to `clean`, so the framework sees a healthy Phase 3.

That is the exact day Suzanne was looking at the iPad saying *"I don't understand why all
the colors are missing"*, and the day the entire product file was scrapped and rebuilt from
scratch — a two-week loss that cost them Showtime.

Every import clause in the framework measures whether the file *parsed*, never whether it
was *right*. A clean import of the wrong file is indistinguishable from success. The blind
agent caught this itself: the intervening imports "technically clear the fatal but on a
file everyone on the call agreed was wrong."

**This bounds what the framework can ever be.** Import tiers cannot detect a correct-looking
wrong catalog; only the conversation record can. Any future automation that reads
`import_events` alone will confidently report health during exactly this kind of crisis.

**Fix:** none available from Postgres. Record it as a stated limit of the model, and treat
the conversation record as a required input rather than colour commentary.

### 8.5 Client-actionable, outside the framework exercise

Independent of any of the above, these are live and worth acting on:

1. **All 389 drf customers price at $1.00.** Every product's `net_price` is 1.00 and every
   customer's `DefaultPriceCode` is `net`. The ten real price levels exist but nothing points
   at them. Reps see real numbers only because 1,418 products have prices typed into the
   story text as a workaround. **Fix is one customer-file re-import** changing
   `DefaultPriceCode` to `list`.
2. **`order_email_recipient` is still Suzanne's placeholder**, 32 days after Kylor flagged
   it. Stated intent on the 2026-05-18 call was customer service, not the client contact.
3. **`order_origins = []`** — all 10 orders post as `Confirmed`. Kyla's stated plan on
   2026-07-21 was a quote/sample default. Never configured.
4. **The support handoff did not hold.** Kyla declared handoff 2026-07-20 and has not
   appeared since 2026-07-29; Suzanne's 2026-08-11 message addressed to "Kyla or support
   person" was answered by Kylor. Four action items Kyla promised "this week" have no answer
   anywhere in the corpus.

---

## 9. Client 3 — `pebl` (Skyard Furniture / Pebl), reviewed 2026-08-25

Corpus read in full (4,916 lines). No forbidden file opened. **This run corrected me**,
which no previous run did.

### 9.1 Claim verification

| claim | verdict |
|---|---|
| 88 of 91 orders are locally-created-customer orders | **confirmed** — `local_customer_code` populated on 88 |
| `customer_po_num` empty on all 91 | **confirmed** — 91 of 91 |
| `is_exported` / `to_export` false on all 91 | **confirmed** — 0 and 0 |
| 12 orders point at price level `project`, which no longer exists | **confirmed** — 12 orders, **$264,130.00**, exact to the dollar; `project` is absent from all 13 current levels |
| All 171 customers point at `fob` | **confirmed** |
| Ten user accounts destroyed 2026-07-28 → 07-30 | **confirmed** — exactly 10 `OrgUser destroyd` events, 07-28 01:35 → 07-30 07:42 |
| The actor was Mandy | **confirmed** — org_user 152538 = Mandy Mai, `sales04@peblfurniture.com`, admin, Pebl Managers, and the org's top order creator (25) |
| All 171 customers re-imported with empty territory codes | **confirmed** — all created 2026-07-30 **07:48**, six minutes after the last destroy; `territory_codes = '[]'` on all 171 |
| No product at $1.00 or $0.00 | **confirmed** — 330 distinct net prices |
| 8 price levels created 2026-08-19, never used | **partially** — it is **9**, not 8. None has ever been used (0 orders, 0 customers). Immaterial to the argument. |

One numeric slip in ten claims, self-evidently immaterial.

### 9.2 It caught a bug in my code

The agent reported all 171 customers had empty territory codes. My verification query
returned **zero**, and I nearly filed it as the first wrong claim in three clients.

The agent was right. `territory_codes` stores an empty array as the literal string
**`'[]'`** — not `''`, not NULL. My test was:

```sql
WHERE territory_codes IS NULL OR btrim(territory_codes) = ''
```

which silently returns 0 and reports "every customer has a territory" when none does.

**D11 — this bug was in `collector/queries.py` and `collector/rawstate.py`**, i.e. in the
instrumentation built to audit the framework. Blast radius across the cohort:

| org | customers | broken test | corrected |
|---|---|---|---|
| pebl | 171 | 0 | **171** |
| libco | 267 | 0 | **6** |
| tcd / drf / mali / leg | — | 0 | 0 (genuinely fine) |

Fixed in both files with the reasoning inline. `Phase_Anchors.md` § Phase 6 health lists
"count of customers without TerritoryCodes" — any naive implementation carries the same
latent bug.

**The method caught a defect in its own measuring instrument.** That is a stronger result
than another agreement.

### 9.3 pebl breaks D3 — and replaces it with something sharper

pebl is the adoption case the other two are not: **8 distinct ordering users, 91 orders,
90 in the last 90 days, 6 user groups including two distributors**.

> **CORRECTED 2026-09-04. "8 distinct ordering users" was missing a third of the
> evidence.** Measured today: **93 submitted orders, 66 with an identifiable creator
> across 8 distinct users, and 27 with `org_user_id IS NULL` — 29.0% of the org's
> orders have no attributable creator.** Zero are dangling.
>
> **User deletion NULLIFIES order attribution rather than leaving a dangling id.**
> The creators of those 27 were deleted: Mandy's ten accounts on 2026-07-28..30
> (§ 9.1) plus the `ICA` group and `ckirbeyi@ica.com.tr` (removed between 08-25 and
> 09-04; see `config_intent.yml § pebl`). Grouping by `org_user_id` returns the 8
> users that still exist and silently drops the other 27 orders — so every read of
> "who is ordering at pebl", including this one, has been made on 66 of 93 orders.
>
> **Generalises beyond pebl:** deletion rewrites order attribution org-wide with no
> trace except `audit_log_entries` and `login_events` (D13/D16). Any adoption or
> rep-activity analysis must count NULL creators **explicitly**, not group by
> `org_user_id` and report the groups it happens to find. That is
> silence-is-not-zero with a named mechanism.
>
> (Order count also moved 91 → 93 between 2026-08-25 and 2026-09-04.)

But the blind read went further than "adopted": 58.2% of the $999,930.60 sits against
internal or literal test names ("Pebl", "Test", "Skyard", "dsbs"), one user placed 17
orders in a day using the order screen as a bundle-pricing calculator, and — decisively —
**no order has a PO number, none is exported, and the org has no ERP export configured.**

These are quotations, not bookings.

So the three clients give three distinct states, none of which the phase model can express:

| client | state |
|---|---|
| tcd | live, one rep of 24 transacting |
| drf | live, only the admin transacting, $0.00 |
| pebl | heavily used, 8 users, **but the system is a quoting tool, not a system of record** |

D3 should not be "live but not selling." It is **three** missing states, and the pebl one
is the subtlest: high engagement that never becomes a booking. A Go-Live terminal phase
scores pebl as the best client in the cohort.

### 9.4 New defects

#### D12 — orders can reference a deleted price level, and nothing notices

12 pebl orders worth $264,130 carry `price_level = 'project'`. No such level exists. The
framework's only pricing-integrity check is on `customers.default_price_code`; nothing
validates `orders.price_level`, so a level can be deleted out from under historical orders
silently.

**Fix:** one query — submitted orders whose `price_level` has no matching
`price_levels.code`.

#### D13 — `audit_log_entries` is a source the framework has never used

Ten user deletions and a full 171-row customer reload happened over three days, eleven
days after SuperCat called the rollout "one of the smoother rollouts we've seen." **Not one
word of it appears in HelpScout or Fathom.** It is invisible to every source the framework
reads.

It is recorded in `audit_log_entries` — a 13M-row global table keyed by
`(parent_type, parent_id)`, carrying `OrgUser destroyd`, `OrgUser created`, `user group
updated`, `Organization updated`. Nothing in the framework, the collector, or
`ecat-postgres-audit` touches it.

This is the single largest missing input identified so far. Destructive admin actions by
the client are exactly the events an onboarding tracker should surface, and they leave no
trace anywhere else.

**Fix:** add `audit_log_entries` to the collector, scoped to destructive events for the
org's `org_user` ids. Note the join is awkward — deleted users no longer exist in
`org_users`, so match on the `data` blob's `organization` key.

### 9.5 Client-actionable, live right now

1. **All 171 pebl customers have empty territory codes** since 2026-07-30. Rep↔customer
   filtering is off for the whole org. If reps see every customer, this is why.
2. **12 orders ($264,130) reference a deleted price level `project`.**
3. **Nine price levels created 2026-08-19 have never been used** — someone built a channel
   pricing model six days ago that nothing points at. All 171 customers are still on `fob`.
4. The blind read found evidence the org was **cloned from another client's template**
   (`zebra sales price` in `dach`, a `ZEBRA GROUP` login event). Worth confirming.

---

## 10. Client 4 — `mali` (Magic Lite | NSL), reviewed 2026-08-25

Both corpus parts read in full. No forbidden file opened. **This run corrected my own
instrumentation twice and corrected two statements I had made to the operator.**

### 10.1 Claim verification — all confirmed

| claim | verdict |
|---|---|
| ML Reps is 4 of 5 on eCat Online, not 0 | **confirmed** — ML Reps: 0 iPad, **4 eOL**. NSL Reps: 3 iPad, 1 eOL |
| The 3 iPad "NSL Reps" include SuperCat staff | **confirmed** — NSL Reps has **11** users (not 10), **2 on @supercatsolutions.com** |
| `is_submitted` is NULL, so `= 0` hides a row | **confirmed** — 1 order row, `is_submitted` NULL, `total` NULL, created **2026-07-15 17:25** |
| 5 invitations 2026-08-10 19:54:22, 3 redeemed | **confirmed exactly** — Dan French redeemed 19:56 (**2 min**), Mike Krause 22:32 same night, Josh Nelson 2026-08-17 17:57 against an 08-17 expiry; both Electra Sales invites expired unredeemed |
| `price_level_id` 5722 exists in no organization | **confirmed** — 0 rows table-wide |
| `distribution_centers` = 0 despite the "we have set up two" email | **confirmed** |
| All 86 Images imports clean/warning, never an error | **confirmed** — 86 events, **0** containing `:error` |

### 10.2 It corrected me, not the framework

Two of my own defects, both of which I had already reported to the operator as fact:

#### D14 — login recency is surface-specific, and I measured one surface

`RAWSTATE_mali.json` reported `ML Reps: ever_logged_in 0`. I relayed that as "the entire
Magic Lite rep team has never signed in." **Wrong.** `last_ipad_login_at` is one of two
login columns; `last_ecat_online_login_at` is the other, and 4 of 5 ML Reps have used
eCat Online. mali is a dual-product-line org and I reported half of it.

The framework has the same exposure: Phase 5 ("Reps Signed In") is defined on
`last_ipad_login_at` alone. For any org with eOL that under-reports adoption, and mali is
flagged dual-line in the registry.

**Fixed** in `collector.py::summarize_reps` — now reports `ever_logged_in_ipad`,
`ever_logged_in_eol`, and `ever_logged_in_any_surface` separately.

#### D15 — `is_submitted` is nullable and every count silently drops NULLs

`count(*) FILTER (WHERE o.is_submitted)` excludes NULL. mali's single order row has
`is_submitted` NULL — an empty server-side cart created by SuperCat's support account 25
minutes into a screen-share — so "0 orders" concealed the existence of an order row and,
more importantly, concealed *what* it was.

**Fixed** in `queries.py` — `order_rows_total` and `order_rows_unsubmitted_null` now
report alongside the submitted count, with `COALESCE(is_submitted,false)`.

Also corrected in `corpus.py`: Endeavour Solutions integrates **Dynamics GP, not Business
Central**, and the `.co` domains are **not typos** — they appear zero times in the corpus
and exist only as fabricated login addresses for two eOL service accounts. Both were my
descriptions, both wrong.

### 10.3 New framework defects

#### D16 — invitation and self-enrolment activity is invisible to every source

mali's beta launch — five invitations, three redemptions, two expiries — appears in
**neither the corpus nor `audit_log_entries`**. Self-enrolment writes no audit row, so the
org's audit trail simply stops on 2026-08-03 while real onboarding continues.

This survives the D13 fix. `organization_invitations` is a third source, separate from both
HelpScout/Fathom and the audit log, and nothing reads it.

**Fix:** add `organization_invitations` (issued / redeemed / expired, with timings) to the
collector. Redemption latency is a genuine engagement signal — Dan French redeemed in two
minutes; the Electra Sales pair never did.

#### D17 — dangling references are systemic, not a pricing quirk

D12 found orders pointing at a deleted price level. mali has **four** dangling pointers of
different kinds: an eOL site pointing at `price_level_id` 5722 (a row in no organization)
for eight days; an admin-training email linking a deleted MobileSite; a bulk-invite link
pointing into **org `tcd`**; and a "we have set up two Distribution Centers" email against
`distribution_centers = 0` — after Endeavour spent seven weeks building an export to that
withdrawn spec.

D12 should be generalised: **nothing validates that a stored id still resolves.**

#### D10 confirmed at scale

All 86 Images imports in mali's history are clean or warning — **not one error, ever** —
including 36 clean imports across 2026-03-19→24, straddling a 30-line client punch list
("The non-dimmable driver pictures are dimmable drivers"). Roughly 200 products carried a
wrong image while the log read clean. Two clients, two independent confirmations that
import tier is silent on correctness.

### 10.4 Zero orders is a decision, not a failure

Ship-tos were deliberately excluded ("I understand we are not entering orders through
SuperCat at this time"), order type is Quote, and GP remains the system of record. A
framework that treats orders as the go-live proof would score this client as failing at
something it deliberately chose not to do.

### 10.5 Live right now — mali's beta is expanding today

Three further invitations were issued **2026-08-25 20:46–20:47**, after the blind run:
`ryan@electrasalesltd.ca` (pending), `jim@nslusa.com` (pending), and
`jason@electrasalesltd.ca` — who let his 08-10 invite expire and this time **redeemed in
two minutes**. The Electra Sales relationship that looked dead on 08-17 is not.

---

## 11. Client 5 — `leg` (Legrand US), reviewed 2026-08-27 — THE FORWARD TEST

The only org with `status = 'onboarding'`, so this is the framework's entire live cohort.
Corpus read in full (2,051 lines). No forbidden file opened; the agent additionally
self-excluded the BigQuery datasets `onboarding_assessment` and `scorecard` on the
reasoning that they hold the framework under test — a judgement I did not ask for and
which was correct.

### 11.1 It overturned my framing, and mine was wrong

I staged this client saying the **285-day import gap was the flagship regression case** —
the ideal test of the at-risk state I had just added in v3.6.

It is not a regression. It is **pre-sales**.

- June 2025 was a speculative demo built from a public scrape of `legrand.us`. No contract,
  no Legrand account existed.
- HubSpot deal **"Legrand - Showroom TIER 1"** closed **2026-06-11 13:59:42**, $24,108
  (verified). A second deal, "Legrand - Electrical Distributor eCat" ($15,000), sits at a
  different stage with a 2025-12-31 close date.
- The demo was dismantled 2026-06-18; the first three Legrand accounts were created
  2026-06-19.

**The onboarding is seven weeks old, not fourteen months.** The gap is procurement — eleven
HubSpot close-date slips, blocked on a Central-marketing sign-off.

### 11.2 D19 — the D1 at-risk fix has a false-positive mode, and leg is it

This is the most consequential result of the whole exercise, because it is a defect **in the
fix I made last week**.

v3.6's at-risk rule fires when a previously-passing anchor stops passing. Run against leg,
it would have raised `PHASE_REGRESSED` continuously **from September 2025 to June 2026** —
nine months of escalation about a client that had not signed and whose "onboarding" was a
sales demo.

Root cause: **`organizations.created_at` is not the project start.** leg's org was created
2025-06-10 for a demo; the project began 2026-06-19. Every duration the framework computes
for this client is wrong by a factor of ten.

`overrides.yml` has a `project_start_date` field for exactly this, and it is **empty** —
`project_start_date: {}`. The mechanism exists and is unused.

**Fix, and it is required before the at-risk state ships:**
1. Suppress regression detection before a project-start date.
2. Derive project start from the **HubSpot closed-won date**, not `created_at`, falling back
   to the first user account created on a client domain.
3. Populate `overrides.yml § project_start_date` for `leg` = `2026-06-19`.

Without this, the fix I added produces a nine-month false alarm on the only client in the
cohort.

### 11.3 Claim verification — every checkable claim held

| claim | verdict |
|---|---|
| `qty_available` NULL on all 439 inventory rows | **NULLs confirmed; the "iPad displays it" claim was WRONG — see § 12** |
| The feed is two files that overwrite each other | **confirmed** — all 439 rows share one `updated_at` (2026-08-27 06:01): full hard-delete-and-reload daily. Two alternating signatures in the log (997 bytes / 10 not-found vs 23,108 bytes / 237 not-found). Only one file's rows survive at a time. |
| 13 filter fields warned, then went clean, still empty | **confirmed exactly** — 13 "Custom field is missing" warnings at 2026-07-23 21:41, clean at 22:42 (**61 min**), nine clean imports since. All 13 columns are **empty across all 1,020 products**; the `Finish` control has 1,001 populated. |
| Configuration froze 2026-08-18 15:58 | **confirmed** — last Products import, nothing since |
| Deal closed 2026-06-11 | **confirmed** — 13:59:42, $24,108 |

I challenged the two-file claim because 27 of 439 codes start with `AD` and I read that as
both brands being present. My prefix heuristic was wrong (adorne SKUs are not all
`AD`-prefixed); the single shared `updated_at` settles it. **Third time a blind read has
survived my challenge.**

### 11.4 Phase 5 returns a false positive here

By the framework's own rep definition, leg passes Phase 5: 5 non-admin users, 3 with iPad
logins, 3 active in the last 30 days.

All three are **Legrand employees doing acceptance testing**. Zero rep-agency accounts
exist. **22 of 23 user groups are empty** — every agency group is scaffolding. No rep has
ever opened this app.

Phase 5 asks "are reps signed in" and measures "are non-admin accounts logging in." For an
org whose entire user base is internal, those are different questions. Fourth client, fourth
distinct way the adoption question fails.

### 11.5 Live and actionable at leg right now

1. ~~**`qty_available` is NULL on all 439 rows.** The iPad displays that field.~~
   **RETRACTED 2026-09-03 — see § 12. The NULLs were real; the consequence was invented.**
2. **Only one of the two inventory files survives each day.** On 17 of 23 days only one
   brand's inventory existed in the app.
3. **13 announced fields deliver nothing.** ~~9 of them configured as iPad filters with
   `send_to_ipad = true`~~ — **MECHANISM CORRECTED 2026-09-04.** The 13 are columns in
   `products.csv` that were **never registered in Admin**: the importer warned
   `Custom field 'X' is missing` for each and dropped them. leg has **5** registered custom
   fields (`Finish`, `CountryOfOrigin`, `drop_ship`, `shipped_via`, `order_uom`), **all five
   well populated** (1001/897/1020/1020/851 of 1020). `numberofgangs` is not registered at
   all, so it was never a `send_to_ipad` filter carrying zero values.
   The client-visible outcome is unchanged — `# of Gangs` was announced and delivers nothing —
   but the fix is to REGISTER the fields, not to populate them. Detected by
   `acceptance/b1_fields.py` B1b.
4. **Configuration has not moved since 2026-08-18 15:58** while Tracy sent a 100-line library
   spec, Trey unblocked pricing, and Trey asked for agency testing "by the end of next week."
5. **`order_email_recipient` is empty.**

### 11.6 D10 confirmed a third time, at the worst moment

Nine consecutive clean Products imports over five weeks, while 13 client-visible filters sat
empty the entire time. Import tier is silent on correctness — now demonstrated on drf (18
days of `.jpg.jpg`), mali (86 clean image imports, ~200 wrong images), and leg (nine clean
imports, 13 empty announced filters).

**This is no longer a defect. It is a property of the data.** Any automation reading
`import_events` alone will report health during precisely the failures that matter.

---

## 12. Retractions (2026-09-03)

Two findings in this document were wrong. Both were reported to the operator as fact and
one reached a client. Recording them here because a scorecard that hides its own errors is
worth nothing.

### R1 — "`qty_available` is the field the iPad displays" — FALSE

**What I said:** leg's `qty_available` was NULL on all 439 inventory rows, therefore
inventory read blank to a rep. Filed Critical, twice, and put on a CEO-facing page.

**What is true:** the NULLs were real. The consequence was invented. I verified the NULL
count and repeated the display claim from the blind read without checking it.

**The fleet settles it.** Orgs running `qty_on_hand` with **zero** `qty_available`:

| org | inventory rows | qty_available | qty_on_hand |
|---|---|---|---|
| tam-staging | 6,569 | 0 | 1,197 |
| ta | 6,441 | 0 | 1,059 |
| tam | 6,445 | 0 | 1,045 |
| etl | 986 | 0 | 986 |
| ol | 129 | 0 | 129 |

And the exact inverse also runs live — `cl` (439 rows) and `cf` (6,438 rows) have
`qty_available` populated and `qty_on_hand` at zero. **Both fields work. Inventory display
is configurable.**

**Cost:** the operator told Legrand their inventory could not be displayed because they
were sending `QtyOnHand` instead of `QtyAvailable`. The client reacted badly. It was not
true, and the fix was to point the config at the field they were already sending.

**Root cause, named plainly:** `truth-discipline` § "the standard binds on capability
claims too" — *a skill is evidence, not proof*, and *name the inference*. "NULL on 439
rows" is a measurement. "That is the field the iPad displays" is a capability claim about
the product, and it needed the live artifact or the code, not a repeated assertion.

**Rule going forward:** a measurement and its consequence are two claims. Verify them
separately, or state the measurement alone.

### R2 — "22 of 23 user groups are empty scaffolding" — WRONG READING

**What I said:** leg has 26 user groups with one populated; the agency groups are
scaffolding for a rollout that hasn't happened.

**What is true:** they are deliberate and load-bearing. Legrand hosts a *per-agency*
Design Studio link in the Library, so each agency needs its own group to scope Library
access to its own URL. Verified: **24 agency groups, every one `shared_resources_auth='c'`
with 96 scoped resources.** That is careful configuration, not an empty shell.

Most clients do have `us-reps` / `canadian-reps`; others carry groups for eOL buyers or
Sales Portal users. **Group count is not a defect signal, and fleet prevalence is the wrong
lens for it.**

**The real findings were the deviations, which I missed by looking at the wrong thing:**

- **`Catalyst`** — `shared_resources_auth='a'`, **0 scoped resources**. The only agency group not following the pattern its 23 peers follow.
- **`Futura`** — 95 scoped resources where every peer has 96.

**Rule going forward:** for per-client structures, check **conformance to the org's own
pattern**, not prevalence across the fleet. "One of 24 differs" is a finding. "26 groups
exist" is not.
