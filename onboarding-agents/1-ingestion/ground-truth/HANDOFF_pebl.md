# Handoff — reconstruct the Pebl / Skyard Furniture (`pebl`) onboarding, blind

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace. It is self-contained. Client 3 of 4.

---

## What you are doing, and why it has to be blind

You are building an **independent ground truth** for one client's onboarding, from raw
evidence only, so a separate assessment framework can be graded against it.

The existing hand-written client notes drift and are sometimes flatly wrong — a sibling
client's profile once claimed "go-live blocked, 0 customers imported" while the live
database held 346. If you read those notes first you will reproduce their conclusions
and their errors.

**Do not read any of these until your timeline is written:**

```
❌ eCat_Onboarding/pebl/CLIENT_PROFILE.md
❌ eCat_Onboarding/pebl/HANDOFF.md   (and any other pebl/*.md notes)
❌ eCat_Onboarding/REGISTRY.yaml
❌ onboarding-models/Phase_Anchors.md
❌ onboarding-models/Phase_Progression_Framework.md
❌ onboarding-models/Flags_and_Signals.md
❌ onboarding-models/Output_Contract.md
❌ onboarding-models/RUN_PROMPT.md
❌ onboarding-models/overrides.yml
❌ onboarding-models/ground-truth/SCORECARD.md and the other clients' JOURNEY_*.md
❌ any ecat-* skill that describes what phases mean
```

If you open one by accident, say so at the top of your output. A contaminated run that
admits it is useful. One that hides it is worse than none.

---

## Your inputs

| file | what it is |
|---|---|
| `eCat_Onboarding/pebl/_ground_truth/CORPUS_pebl.md` | **~86k tokens.** Every Fathom call transcript and HelpScout thread, deduplicated, chronological. Read it start to finish. |
| `eCat_Onboarding/pebl/_ground_truth/RAWSTATE_pebl.json` | The live database right now — counts, 13 price levels, 6 user groups, all 13 users with order counts, import history by month. Raw, no interpretation. |

`supercat-postgres-vpn` (read-only SQL) and `bigquery-admin` MCPs are available. **Use
them freely** — especially here, because this client's story is mostly *not* in the
corpus (see below). Querying live data is encouraged; reading interpretation documents
is not.

Org id `275`, shortname `pebl`. VPN must be up.

---

## The seven phases — questions only, deliberately

You get the *questions* so your output is comparable, and deliberately **not** the rules
the framework uses to answer them. Those rules are what's being tested.

1. **Discovery / Kickoff** — Have we kicked off this client?
2. **Initial Import** — Has at least the products file been imported?
3. **Progress** — Is more than one core file in, without fatal errors on the most recent of each?
4. **Catalog Completeness** — Is the catalog actually buildable as a live iPad?
5. **Reps Signed In** — Are reps actually logging into the iPad?
6. **Admin Training** — Has the admin been trained, with ongoing operations covered?
7. **Go-Live** — Has the formal handoff to support happened, with ongoing client activity?

Answer each from evidence. Decide what "done" looked like *for this client* and say what
convinced you. **If the real story doesn't fit these seven phases, say so.**

---

## Five questions the phase model does not ask. Answer them anyway.

Previous runs found the most valuable material lives outside the seven questions.

**A. Did this client ever go backwards?** Stall, regress, nearly churn, go silent? When,
what triggered it, what ended it? On both previous clients this was the highest-value
finding and was invisible to all seven questions.

**B. Adoption — separate from go-live.** Who actually used it, how many people, how
often, doing what? Be concrete: names, counts, dates.

**C. Current trajectory.** Improving, steady, or decaying, and on what evidence?

**D. Was the catalog ever *wrong* while the imports looked *clean*?** Import tiers only
record whether a file parsed, never whether its contents were right. On a previous client
the catalog was visibly broken on a day the import log showed clean. Look for moments
where someone describes something wrong on the iPad, and check what the import history
says about that same day.

**E. Is anything priced as a placeholder?** On a previous client every product carried a
$1.00 placeholder price and every customer pointed at it, while the import and pricing
checks all passed. This org has 330 distinct net prices so it is probably fine — but
verify rather than assume, and check whether the price levels people actually use match
the ones that exist.

---

## Reading notes specific to pebl — this client is unlike the others

- **The corpus is small and the database is large.** 8 tickets, 94 threads, and exactly
  **one** call (2025-12-10, titled "Discovery Call"). Against that: 91 orders worth
  **$999,930.60**, 171 customers, 713 products, 151 options across 382 option groups.
  **Most of what happened to this client is not written down anywhere you can read.**
  Expect to lean on the database far more than on the corpus, and expect more
  `undetermined` entries than usual. That is the correct outcome here, not a failure.

- **Brand ≠ legal name.** The org is `Skyard Furniture Co Ltd.`; the brand is Pebl; there
  is also a `skyard-outdoor.com` domain with an active user. Do not assume a name
  mismatch means a self-test or a wrong record.

- **The org was created 2025-07-24 but the first orders are 2026-05-13.** There is a long
  gap. Work out what the org was doing in it — and whether the real project start is the
  provisioning date or something much later.

- **Two distributors have their own Admin user groups:** `ICA` (`ckirbeyi@ica.com.tr`,
  Turkey, 2 orders) and `Albania-Sezon Dekor` (`info@sezondekor.com`, 0 orders). Neither
  has ever filed a HelpScout ticket, so they are absent from the corpus but present in the
  business. There is also an `ETC` group with one hotmail user. Six user groups total for
  a company this size is unusual — find out what the structure is for.

- **`kylor22johnson@gmail.com` is a SuperCat-side test account and it placed 6 orders** —
  the third-highest of any user. Exclude it when you count client adoption, and say so.

- **The order mystery — this is the most interesting thing in the data.** Only **3 of 91**
  orders have a `bill_to_company_name` matching a `customers` row. Do not jump to
  "self-tests": 88 unmatched orders alongside a million dollars of order value is a
  different shape from the self-test pattern. Possibilities worth testing against the
  data: reps typing free-text buyers, local/ad-hoc customers created on device, a customer
  file that doesn't cover the accounts reps actually sell to, or export/naming drift.
  Query it. Whatever you conclude, show the evidence.

- **13 price levels, almost all arithmetic channel markups** — FOB at 1.0 up through
  Suggested Retail at 3.5, plus two CNY levels. That is a channel-pricing model, not a
  customer-tier model. Consider what that implies about who the iPad is for.

- **Two fatal Products blocks in August 2026 are superseded** by a warning-tier import on
  2026-08-07, so nothing is currently outstanding. Question D above still applies.

- **0 inventory rows.** Determine from the record whether that is by design.

- **Duplicate tickets are common.** On a previous client 21 of 31 tickets were duplicate
  captures of 9 real conversations. With only 8 tickets here the effect is small, but
  collapse on subject (ignoring `Re:` / `Fwd:` / `FW:`) before drawing conclusions from
  volume.

---

## What to produce

### 1. `eCat_Onboarding/pebl/_ground_truth/JOURNEY_pebl.md`

Open with a 10–20 line plain-language narrative. Then:

**A. Cast** — every person, email, which side, first and last appearance, role changes.

**B. Phase transitions**, one entry each:

```markdown
### Phase 2 → 3 · 2026-05-13 · confidence: medium

**What changed:** <one sentence>

**Evidence:**
- [HS #13879, 2026-01-24T21:08, vincent@peblfurniture.com (customer)]
  > "verbatim quote"
- [DB] import_history: Products warning 2026-05-xx; Options clean 2026-05-xx

**Against:** <what argues the other way, or "none">
```

- Every transition needs a date and at least one piece of evidence — a verbatim quote
  with author and timestamp, or a specific fact from the DB.
- Confidence: `high` / `medium` / `low`.
- **If you cannot date a transition, write `undetermined` and explain why. Do not guess.**
  Given how thin this corpus is, expect several. Honest gaps are the correct output.
- Quote real text. Never paraphrase inside quote marks.

**C. Current phase** as of today, same evidence standard.

**D. Turning points** — the 3–5 moments that actually moved or blocked this project.

**E. The five extra questions** (A–E above), answered directly.

### 2. `eCat_Onboarding/pebl/_ground_truth/GAPS_pebl.md`

- What you could not determine, and what evidence would settle it
- Which tier B tickets you judged irrelevant, and why
- Contradictions between sources — a thread saying one thing, the DB another
- **Corpus holes.** Be thorough here. With one call and 8 tickets against a year of
  activity, the holes *are* the story: name every stretch where the database shows work
  happening and the corpus shows nothing.

---

## Before you finish

1. Does every transition have a date and evidence, or an explicit `undetermined`?
2. Is every quote verbatim, with author and timestamp?
3. Did you read the whole corpus or skim? Say which.
4. Confirm explicitly that you avoided all the forbidden files.
5. Did you exclude `kylor22johnson@gmail.com` from client adoption counts?
6. Does your narrative contradict `RAWSTATE_pebl.json` anywhere? Flag it — the DB is not
   automatically right either, and a genuine contradiction is a finding.

Write both files, then stop. Do not touch `CLIENT_PROFILE.md` or `HANDOFF.md`.
