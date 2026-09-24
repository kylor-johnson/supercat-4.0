# Handoff — reconstruct the Terracotta Designs (`tcd`) onboarding, blind

Paste this whole file into a fresh Claude Code session in the **SuperCat 4.0**
workspace. It is self-contained.

---

## What you are doing, and why it has to be blind

You are building an **independent ground truth** for one client's onboarding, from
raw evidence only, so that a separate assessment framework can be graded against it.

The framework being graded has never been run. The existing hand-written client notes
are known to be wrong — this client's own profile once claimed "go-live blocked, 0
customers imported" while the live database held 346. If you read those notes first,
you will reproduce their conclusions and their errors, and this exercise produces
nothing.

**So: you must not read any of these until you have written your timeline.**

```
❌ eCat_Onboarding/tcd/CLIENT_PROFILE.md
❌ eCat_Onboarding/tcd/HANDOFF.md
❌ eCat_Onboarding/REGISTRY.yaml
❌ onboarding-models/Phase_Anchors.md
❌ onboarding-models/Phase_Progression_Framework.md
❌ onboarding-models/Flags_and_Signals.md
❌ onboarding-models/Output_Contract.md
❌ onboarding-models/RUN_PROMPT.md
❌ any ecat-* skill that describes what phases mean
```

If you read one by accident, say so at the top of your output. A contaminated run that
admits it is useful. One that hides it is worse than none.

---

## Your inputs

| file | what it is |
|---|---|
| `eCat_Onboarding/tcd/_ground_truth/CORPUS_tcd.md` | **~71k tokens.** Every Fathom call transcript and HelpScout thread for this client, deduplicated, in chronological order. Read it start to finish. |
| `eCat_Onboarding/tcd/_ground_truth/RAWSTATE_tcd.json` | The live database right now — counts, price levels, reps, orders, and the full import history parsed to block level. Raw, no interpretation. |

You also have the `supercat-postgres-vpn` MCP (read-only SQL) and `bigquery-admin`
MCP. **Use them freely** to check a fact, pull a detail the corpus lacks, or confirm
something a thread claims. Querying live data is encouraged; reading interpretation
documents is not.

Org id is `282`, shortname `tcd`. VPN must be up.

---

## The seven phases — questions only, deliberately

These are the questions the framework asks. You are being given the *questions* so your
output is comparable, and deliberately **not** the rules it uses to answer them —
those rules are the thing under test.

1. **Discovery / Kickoff** — Have we kicked off this client?
2. **Initial Import** — Has at least the products file been imported?
3. **Progress** — Is more than one core file in, without fatal errors on the most recent of each?
4. **Catalog Completeness** — Is the catalog actually buildable as a live iPad?
5. **Reps Signed In** — Are reps actually logging into the iPad?
6. **Admin Training** — Has the admin been trained, with ongoing operations covered?
7. **Go-Live** — Has the formal handoff to support happened, with ongoing client activity?

Answer each from evidence. Decide for yourself what "done" looked like *for this
client*, and say what convinced you.

**If the real story doesn't fit these seven phases, say so.** A finding that the phase
model is wrong-shaped for this client is a more valuable result than a forced fit.

---

## What to produce

### 1. `eCat_Onboarding/tcd/_ground_truth/JOURNEY_tcd.md`

Start with a 10–20 line narrative: what actually happened to this client, in plain
language, as you'd tell a colleague. Then:

**A. Cast** — every person who appears, their email, which side they're on, and when
they first and last show up. Note anyone whose role changes (e.g. SuperCat authorship
shifting from one person to another — when, and to whom).

**B. Phase transitions.** One entry per transition:

```markdown
### Phase 2 → 3 · 2025-12-19 · confidence: high

**What changed:** <one sentence>

**Evidence:**
- [HS #14201, 2025-12-19T14:22, scott.tang@terracottalighting.com (customer)]
  > "verbatim quote"
- [DB] import_history: Products clean 2025-12-19, Inventory warning 2025-12-19

**Against:** <anything that argues the other way, or "none">
```

Rules:
- **Every transition needs a date and at least one piece of evidence** — a verbatim
  quote with author and timestamp, or a specific fact from `RAWSTATE_tcd.json`.
- Confidence: `high` (unambiguous), `medium` (inferred from convergent signals),
  `low` (best guess).
- **If you cannot date a transition, write it as `undetermined` and explain why.
  Do not guess.** An honest gap is the correct output; a plausible invention destroys
  the test.
- Quote real text. Never paraphrase inside quote marks.

**C. Current phase** as of today, with the same evidence standard.

**D. Turning points** — the 3–5 moments that actually moved or blocked this project,
whether or not they map to a phase boundary. Blockers, re-imports, escalations,
decisions.

### 2. `eCat_Onboarding/tcd/_ground_truth/GAPS_tcd.md`

- What you could not determine, and what evidence would have settled it
- Which tier B/C tickets you judged irrelevant, and why (see the corpus manifest —
  8 tier-B and 7 tier-C tickets are included unfiltered on purpose)
- Contradictions between sources — a thread saying one thing, the DB another
- Anything in the corpus that looks like it's missing (a reply with no question, a
  reference to a call or file you never see)

---

## Reading notes for this specific corpus

- **31 tickets, 174 threads, 5 calls.** Tiering: **A** = customer of record is on
  `terracottalighting.com`. **B** = internal SuperCat thread mentioning Terracotta.
  **C** = a third party's thread mentioning them. B and C are unfiltered — judging them
  is your job.
- **This client's reps are mostly on personal and rep-agency email**
  (gmail, yahoo, charter.net, plus agencies like carolinafixturesales.com,
  rickylights.com, markneallighting.com). Do not assume an off-domain address means an
  outsider — for tcd it usually means a sales rep. Only one admin sits on
  `terracottalighting.com`.
- **4 HelpScout tickets sit on `gmail.com`** and would be invisible to a domain-based
  search. They are in the corpus. Work out who those people are.
- The corpus starts **2024-09-19**, more than a year before the org was created
  (2025-10-16). Early tickets may be pre-sales or a different relationship entirely.
  Decide what that early material is; don't assume it's onboarding.

---

## Before you finish — check yourself

1. Does every transition have a date and evidence, or an explicit `undetermined`?
2. Is every quote verbatim, with author and timestamp?
3. Did you read the whole corpus, or did you skim the middle? Say which.
4. Did you avoid all the forbidden files? Confirm explicitly.
5. Does your narrative contradict `RAWSTATE_tcd.json` anywhere? If so, flag it — the DB
   is not automatically right either, and a real contradiction is a finding.

Write both files, then stop. Do not update `CLIENT_PROFILE.md` or `HANDOFF.md` — the
whole point is that those stay untouched so they can be diffed against your work.
