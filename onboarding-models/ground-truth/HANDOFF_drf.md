# Handoff — reconstruct the Dorell Fabrics (`drf`) onboarding, blind

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace. It is self-contained. Client 2 of 4.

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
❌ eCat_Onboarding/drf/CLIENT_PROFILE.md
❌ eCat_Onboarding/drf/HANDOFF.md
❌ eCat_Onboarding/REGISTRY.yaml
❌ onboarding-models/Phase_Anchors.md
❌ onboarding-models/Phase_Progression_Framework.md
❌ onboarding-models/Flags_and_Signals.md
❌ onboarding-models/Output_Contract.md
❌ onboarding-models/RUN_PROMPT.md
❌ onboarding-models/ground-truth/SCORECARD.md
❌ any ecat-* skill that describes what phases mean
```

If you open one by accident, say so at the top of your output. A contaminated run that
admits it is useful. One that hides it is worse than none.

---

## Your inputs

| file | what it is |
|---|---|
| `eCat_Onboarding/drf/_ground_truth/CORPUS_drf.md` | **~153k tokens.** Every Fathom call transcript and HelpScout thread, deduplicated, chronological. Read it start to finish. |
| `eCat_Onboarding/drf/_ground_truth/RAWSTATE_drf.json` | The live database right now — counts, price levels, reps, all 9 orders, full import history. Raw, no interpretation. |

You also have `supercat-postgres-vpn` (read-only SQL) and `bigquery-admin` MCPs. **Use
them freely** to check a fact or pull detail the corpus lacks. Querying live data is
encouraged; reading interpretation documents is not.

Org id `290`, shortname `drf`. VPN must be up.

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
convinced you. **If the real story doesn't fit these seven phases, say so** — that's a
more valuable result than a forced fit.

---

## Three questions the phase model does not ask. Answer them anyway.

The first run of this exercise found that the most useful findings were the ones the
seven questions have no room for. So, explicitly:

**A. Did this client ever go backwards?** Stall, regress, nearly churn, threaten to
leave, go silent for a long stretch? When did it start, what triggered it, what ended
it? The phase model assumes forward motion; reality doesn't. On the previous client this
was the single most valuable finding, and it was invisible to all seven questions.

**B. Adoption — separate from go-live.** Who *actually used* the product, how many
people, how often, and doing what? "Live" and "being used" are different states and the
model conflates them. Be concrete: names, counts, dates.

**C. What is the current trajectory?** Improving, steady, or decaying — and on what
evidence? Note in particular that **no import of any kind has happened since 2026-07-08**
(six weeks before this handoff was written). Work out whether that is normal for this
client or a signal.

---

## Reading notes specific to drf

- **16 tickets, 62 threads, 11 calls.** Tier **A** = customer of record on
  `dorellfabrics.com` or `loomcraft.com`. Tier **B** = internal SuperCat thread
  mentioning Dorell (9 tickets — a large share here). No tier C. B is unfiltered;
  judging it is your job.
- **Duplicate tickets are common.** On the previous client, 21 of 31 tickets were
  duplicate captures of 9 real conversations — the same email arriving under several
  ticket numbers. **Ticket count overstates activity, roughly 2×.** Collapse on subject
  (ignoring `Re:` / `Fwd:` / `FW:`) before you conclude anything from volume.
- **`loomcraft.com` is a confirmed second domain**, not an outsider — `brian@loomcraft.com`
  attends drf onboarding calls. Work out the relationship between the two companies.
- **The corpus starts 2026-02-03; the org was not created until 2026-04-15.** Two months
  of contact precede provisioning. Decide what that period is.
- **This org has 0 options, 0 option_groups, 0 inventory rows.** Determine from the
  record whether that is by design or unfinished. Do not assume.
- **All 11 price levels are `ad-hoc` type** (net, list, mfr, whs, foblist, foblow,
  c2clist, c2clow, calist, calow, retail). That is a lot of price levels. Find out why.
- **The orders need care.** All 9 were submitted by `Suzanne@dorellfabrics.com` — the
  client's own admin and the order-email recipient, not a sales rep. Eight are billed to
  "Suzanne" or "Christine Son". Only one names a real customer ("AMALFI"), and its total
  is **$0.00**; every total is $0.00 except one at $8.00. Two were submitted the same day
  this handoff was written. **Work out from the record what these orders actually are** —
  testing, training, real sample orders, or something else. This matters: it decides
  whether this client has ever transacted.
- Only **3 reps** exist, 2 have ever logged in.

---

## What to produce

### 1. `eCat_Onboarding/drf/_ground_truth/JOURNEY_drf.md`

Open with a 10–20 line plain-language narrative of what actually happened. Then:

**A. Cast** — every person, email, which side, first and last appearance. Note role
changes, especially SuperCat authorship shifting between people (who, when).

**B. Phase transitions**, one entry each:

```markdown
### Phase 2 → 3 · 2026-05-05 · confidence: high

**What changed:** <one sentence>

**Evidence:**
- [HS #14638, 2026-05-05T14:22, suzanne@dorellfabrics.com (customer)]
  > "verbatim quote"
- [DB] import_history: Products clean 2026-05-05

**Against:** <what argues the other way, or "none">
```

- Every transition needs a date and at least one piece of evidence — a verbatim quote
  with author and timestamp, or a specific fact from `RAWSTATE_drf.json`.
- Confidence: `high` / `medium` / `low`.
- **If you cannot date a transition, write `undetermined` and explain why. Do not guess.**
  An honest gap is correct output; a plausible invention destroys the test.
- Quote real text. Never paraphrase inside quote marks.

**C. Current phase** as of today, same evidence standard.

**D. Turning points** — the 3–5 moments that actually moved or blocked this project,
whether or not they map to a phase boundary.

**E. The three extra questions** (A/B/C above), answered directly.

### 2. `eCat_Onboarding/drf/_ground_truth/GAPS_drf.md`

- What you could not determine, and what evidence would settle it
- Which tier B tickets you judged irrelevant, and why
- Contradictions between sources — a thread saying one thing, the DB another
- Corpus holes — a reply with no question, a reference to a call or file you never see

---

## Before you finish

1. Does every transition have a date and evidence, or an explicit `undetermined`?
2. Is every quote verbatim, with author and timestamp?
3. Did you read the whole corpus or skim the middle? Say which.
4. Confirm explicitly that you avoided all the forbidden files.
5. Does your narrative contradict `RAWSTATE_drf.json` anywhere? Flag it if so — the DB
   is not automatically right either, and a genuine contradiction is a finding.

Write both files, then stop. Do not touch `CLIENT_PROFILE.md` or `HANDOFF.md` — they
stay untouched so they can be diffed against your work.
