# TRAPS — failure modes this programme has already paid for

Every entry below cost real time or shipped a wrong number into a client
report. None of it is inferable from reading the code. Read this before
touching the pipeline; re-read the relevant section before you claim a task
is done.

Written 2026-09-21, after the Phase 1–9 work. Ordered by how expensive the
mistake is, not by when it was found.

---

## 1. The stale DRAFT will lie to you

`run_report` writes `outputs/{org}_DRAFT_{date}.md` and THEN continues. If a
later step fails, the DRAFT from the previous run is still sitting there and
every downstream tool reads it happily. A "passing" render can be an artifact
of a run that died.

**Always check the exit code, not the file.** `./run.sh {org} --date {date};
echo $?`. `regression.sh --verify` reads whatever is on disk, so it will
cheerfully verify a stale artifact.

## 2. `regression.sh --update` does not write the manifest

Its own usage text claimed it did, for months. It only PRINTS checksums for a
human to paste. A re-stamp that silently keeps old hashes is worse than none:
`--verify` then fails on exactly the orgs you meant to bless.

**Use `tools/restamp_golden.py --note "..."`.** It re-derives every row from
`outputs/` and refuses a partial re-stamp when an artifact is missing.

## 3. Re-baselining is a deliberate act, in this order

```
./tools/cohort_diff.sh --full      # READ IT. every changed line, every org
make baseline                      # only after you believe every change
tools/restamp_golden.py --note ""  # only after that
make check                         # must be exit 0
```

`+N/-0` across the cohort means purely additive — usually safe. Any `-N` means
something was REMOVED and you must be able to name it. An org whose visible
text is `same` but whose `CORE-SHA` is `CHANGED` is the highest-signal warning
the harness produces (see #4).

## 4. Jinja comments leak into client reports

Two independent ways, both shipped:

- A comment whose TEXT contains a closing `#` + `}` **ends the block early**
  and dumps the remainder into the report. Section 6's header prose — tier
  tables, operator references — rendered into client briefs this way. The
  visible-text diff barely moved; only the byte count caught it.
- A bare comment placed between a block and a heading **emits a newline** and
  shifts every byte after it. bsc's core moved 5719 → 5720 on nothing.

**Keep notes inside the existing header comment block at the top of each
template, and keep Jinja delimiters out of comment prose.** Two tests guard
this: `test_no_jinja_comment_text_reaches_the_rendered_report` and
`test_every_template_comment_block_is_closed_exactly_once`.

## 5. `{% set %}` and `| first` under StrictUndefined

- `| first` on an empty sequence RAISES under `StrictUndefined`. It once blew
  up the entire hero. Materialise to a list and index instead.
- A `{% set %}` between `elif` branches belongs to the PREVIOUS branch's body,
  so the variable is undefined in the branch you thought you set it for.
  Hoist to the top of the macro.

## 6. Never edit a template by line number

A line-based edit mangled a comment block: it still parsed, leaked text, and
silently dropped bmc/bri cards from 4 to 0. Anchor on unique surrounding
strings and assert the match count is exactly 1 before replacing.

## 7. One definition, or the surfaces disagree

"This account has slipped" is `gather.account_needs_a_call()`. "This row can
be dialled" is `account_is_callable()`. "This desk is the house" is
`rep_label_is_house()`. "This bill-to is screened" is `bill_to_is_screened()`.

The coaching-card fix had to be applied to EIGHT surfaces before the report
stopped contradicting itself — call list, watchlist, hero card, footer,
cards, hero priority band, §6 heading, card identity. Each time one was
missed, the page showed two different numbers for the same thing:

> hfg: "~$0.04M of at-risk dollars to act on" directly above cards totalling $841K
> hfg: "leaderboard · $0.04M to coach against" directly above the same cards
> hfg: card said "rep 12328", call list said "Martha Graham & Assoc"

**When you change a definition, grep for every consumer and fix them in the
same commit.** Then render and read the page top to bottom.

## 8. Two detectors are dead. Know which and why

- **`signal_summary_set()`** had zero callers (fixed in Phase 1 — it now
  applies the narrative arc).
- **`is_cadence_cliff`** cannot fire: S1 does not select
  `mean_order_gap_days`, so all 88 decay rows carry `0.0`.
  `account_needs_a_call()` reads as three conditions and behaves as two.
  **DORMANT BY OWNER DECISION (2026-09-21)** — supplying the gap would widen
  who lands on a call list across every org. The cadence question is answered
  additively by Q-ORG-DECAY in §7 instead. Do not "fix" this without asking.

## 9. Screens are scoped. Do not widen them by accident

`account_is_screened` once dropped the whole ACCOUNT when its REP was the
house desk. Profiles scope the house rule to "excluded from the rep
leaderboard render" and the leakage math — NOT the call list. It had never
fired because those orgs had no rep labels; the moment S1 supplied them it
hid $0.21M of live decay on kal, Haverty's ($174K, -19%) on cci, and a $390K
account down 68% on clc.

**Rep-level exclusion belongs on rep-level surfaces** (leaderboard, coaching
cards). The dealers that desk services are ordinary accounts and stay on the
call list. `screen_rep_risks` and the card builder handle the rep side;
`bill_to_is_screened` handles the account side.

Conversely: hfg's two largest "unactivated accounts" are its OWN DTC
webstores, named in its profile §4. Any new named list MUST pass through
`bill_to_is_screened`, and must be loaded into the bundle BEFORE
`outreach_screen.apply()` runs — a list loaded after it is silently unscreened.

## 10. A blank bill-to is not an account

S1 and Q-53 both `GROUP BY` bill-to, so every invoice with a blank bill-to
collapses into ONE row. On ali that was $614K of unattributed invoices, and
it LED the call list as "(unnamed) · rep 75 · 81 days silent" — the top
instruction of the week was to phone nobody. It is not one account, so its
slope is not one account's slope. `account_is_identified()` gates it.

## 11. The renderer drops content in ways the text diff hides

- `_drop_leading_echo` removes the body's first paragraph when it repeats the
  collapsed-header teaser — but the teaser is only the paragraph's FIRST
  SENTENCE, so it deleted every sentence after it. Dainolite was silently
  dropping "No eCat share or attribution rate is claimed.", a Spine-required
  provenance disclaimer. Now only drops when nothing is lost.
- `_shorten_callout_title` truncated at 60 chars mid-phrase
  ("...carry no bill-to…"). Now 72 with a comma-clause fallback.
- `_extract_callout_num` returned a literal "·" when the copy had no figure,
  rendering a stray dot where neighbouring cards show a number. Now omits the
  stat line.
- `hero_sanitizer` once dropped every blank line, fusing blocks and killing
  callout cards on all authored-prose orgs. **Blank lines are structure.**

## 12. Prose files are inputs, not artifacts

`outputs/*_prose_*.json` is committed and **wins over the API** every time
(`run_report.py`). That is where determinism comes from. A `.gitignore` rule
of `outputs/*` once made them untracked, and a branch switch deleted them
along with a phase of fixes. The rule is `!outputs/*_prose_*.json`.

**Ignore artifacts, never inputs.**

When data is re-pulled, authored prose goes stale silently — it still passes
conformance. hfg's talking points said "Account 10317" beside a column reading
"Beautiful Things Lighting"; ali's said "down 59% on a $32K book" against a
stakes column reading "$30K · -55.3%" and named four accounts that no longer
existed. **Re-pull means re-read the prose.**

## 13. Branches are repo-wide

`git checkout` switches the ENTIRE working tree, not your folder. Another
session running `git checkout main` mid-task deleted work in a "totally
separate folder". This repo holds several unrelated projects; assume someone
else is in it. `hang-tag-spike` receives commits from a Cursor agent
regularly — merge, verify `git diff --stat HEAD^1 HEAD -- "Insightful
Product 4.0/"` is empty, then push.

## 14. Verify every MCP-mediated pull against the database

The MCP is a remote proxy, so data passes through an agent's context and is
retyped. That is a transcription path and it WILL eventually be wrong.

**Before importing, run a second independent aggregate query** — row counts,
two different sums, and an MD5 of the ranked identity pairs — and compare to
the file you wrote. Every pull in this programme did this and matched; the
discipline is why that is knowable rather than hoped.

## 15. Live-anchored vs pinned queries

`Q-R1/R2/R4`, `Q-53` and `Q-ORG-DECAY` use `NOW()`/`CURRENT_DATE`. The
invoice queries anchor on `{{REPORT_THROUGH_DATE}}`. On the pinned cohort the
platform half therefore describes today and the invoice half describes July.
Disclosed in all three confidence headers that can carry platform data. It
does not matter for a report generated and sent the same week. Do not
"align" it without an owner decision — it is a canon change to five queries
plus a full re-pull.

## 16. `printf` and `%`

`printf` treats `%` as a format directive. A commit message containing
"+6.7%" was truncated mid-sentence. Use a heredoc or `git commit -F`.
