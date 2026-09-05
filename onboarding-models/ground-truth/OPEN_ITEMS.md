# Open items — flagged but not yet acted on

Everything surfaced during the onboarding-agent programme that needs a human decision or
action and hasn't had one. Started 2026-09-04. **Append as new items appear; strike
through rather than delete when closed, so the record of what was found stays intact.**

Each item says what was measured and what is inferred. Where a consequence hasn't been
proved, it says so — that distinction is why `SCORECARD.md § 12 R1` exists.

---

## A. Client-facing, live right now

### A1 — `ufi` Universal Furniture: 37,816 orders, no delivery mechanism visible
`order_email_recipient` empty, backup empty, `export_type` unset, no export URL,
**zero orders ever marked exported**, 8 sitting queued. 436 orders in the last 90 days.
**Measured.** *Not proved:* that nothing reaches them — a retrieval path outside these
fields may exist. Needs a direct question to whoever owns the account.

### A2 — `fms` Visual Comfort: 17,087 orders, empty recipient
`order_email_recipient` and `company_email` both empty. 27 report formats, so the org is
otherwise well configured. Same question as A1.

### A3 — Fleet: ~20% of orgs email orders nowhere
25 of the 121 orgs with `send_order_email_on_submit = true` have an empty recipient.
Bigger than any single-client finding. Wants a fleet sweep, not a per-org check.

### ~~A4 — `leg` Legrand: 13 registered filter fields, all empty~~ — CLOSED, was never a defect

**Closed 2026-09-04.** The 13 fields were POC/demo residue from the sales process, not part
of the real Legrand build. Kylor deleted the registrations on 2026-09-03.

The full picture, measured:

| where | state |
|---|---|
| `products.csv` (current build file) | all 13 columns **present, 0 populated across 1,020 rows** |
| `custom_fields` as of 2026-08-27 | all 13 registered, `send_to_ipad=true`, 9 as filters, 0 values |
| `custom_fields` as of 2026-09-04 | **deleted.** leg now has 5 fields, all well populated (Finish 1001, CountryOfOrigin 897, drop_ship 1020, shipped_via 1020, order_uom 851) |

They were empty in the file, empty in the registry, and are now gone from the registry.
**No data was ever dropped and nothing rep-facing was ever degraded.** My original framing —
"announced to the client as enabled and delivering nothing" — overstated it.

**Residual, minor:** `build_ecat_files.py` still emits the 13 empty columns, so every import
warns 13 times. Cosmetic; remove them from the generator when convenient.

**What this taught the harness — see G3.**

### A5 — `libco` Lib and Co: 3 filter chips that cannot match
`Dimmable` (880 values), `SlopeCeilingCompatible` (786), `MotionSensor` (162) are
registered `binary` but carry `Yes`/`No`; eCat filters match `Y`/`T`/digits.
**1,828 values across three dead chips.** Also `Rating`: registered `binary` with 907
non-Yes/No values — same family, different problem. Fix is `Yes`/`No` → `Y`/blank in
source plus a re-import.

### A6 — `leg`: Deco Combo, 50 SKUs never imported
Absent from the catalogue in any state — not hidden, not deleted. Sellable radiant
decorator-combo devices with descriptions. **The sheet carries no prices**, so this is not
a re-import fix; the price data has to come from somewhere. Client question.
Note: `Legrand/Notes/2026-09-04_deco_combo_gap.md`.

### A7 — `leg`: 12 discontinued SKUs are rep-visible
8 adorne + 4 radiant marked Discontinued in the client's own June price lists, live with
`hideable = false`, while 23 sheet-mates are already hidden — an incomplete pass.
**Visibility confirmed:** leg has no group restriction (26 of 26 groups `collections_auth='a'`
and `trade_names_auth='a'`) and 0 visible products lack an image, so the photo gate never
fires. `hideable=false` means rep-visible for this org.

### A8 — `leg`: two inventory files overwrite each other daily
Each import hard-deletes and reloads, so only one brand's stock exists at a time.
**The winner has flipped** — 439 rows / adorne on 2026-08-27, 755 rows / radiant as of
2026-09-04 06:01.

### ~~A17 — `leg`: no inventory display alias, "unlike 165 other orgs"~~ — DOWNGRADED, wrong denominator

**Corrected 2026-09-04 by the end-to-end review.** The registration counts are exact —
`i.qty_available` 165 orgs, `i.qty_on_hand` 44, plus six other quantity aliases, and the
`ic.` prefix for division orgs. **The denominator was wrong.**

Of the **187 orgs that actually carry inventory rows, 30 (16%) register no qty alias at
all** — `uhc` among them, and uhc has processed 20,034 orders.

**One in six is a pattern, not an outlier.** My "strong enough anomaly to put to the product
team" does not survive that denominator and is withdrawn. leg and mer having no alias is
unremarkable.

What survives, and is still worth knowing: `custom_fields.alias` is where the display field
is configured, which is the answer BUILD_SPEC B5 was missing. That part stands.

**Related and still open — see F4 in the review:** `mali` registers ten `ic.` aliases, and
the five `NSL_*` keys are absent from all 703 inventory rows while every row is
`LocationCode = 'ML'`. Five `send_to_ipad` display fields carrying the unqualified labels a
rep reads as defaults, with no data behind them. *Not proved:* what the iPad renders for an
absent JSONB key.

### ~~A9 — `drf`: every customer priced at a $1.00 placeholder~~ — CLOSED, by design

**Closed 2026-09-04 on client evidence.** drf is not an ICP client and does not use eCat the
way lighting/furniture clients do. From the 2026-04-29 onboarding call, Suzanne Fukunaga,
verbatim:

> *"There's not going to be any pricing on anything at this point. We don't charge for our
> half-yard cuts, and we don't charge for our waterfalls."* … *"maybe prices going forward
> just to give a, but Brian right now doesn't want prices."*

> *"This is purely to show customer samples and to show them a new product, to order
> waterfalls and samples."*

> *"95% of our business is from POs"* — 70% FOB China, EDI for the rest.

So eCat at drf is a **presentation tool for Showtime**, not an ordering system. No pricing
by design, no inventory (*"Nope"* when asked), and orders are sample requests at $0.00.

The `$1.00` net is a placeholder in a catalogue deliberately built without prices, and
**pricing does live in the stories file**, so a rep can check a price when needed. That is
the intended arrangement, not a workaround that failed.

**My framing was wrong twice over** — I called it a defect, then proposed switching
`DefaultPriceCode` to `list`, which would surface prices the client explicitly does not want
shown.

**Also declared, same source:** *"Our salesmen don't have territories, and we let all our
salespeople look at all our customers."* So drf needs no territory filtering either — B3
passing on drf is incidental, not a requirement.

→ belongs in `config_intent.yml` as `drf: presentation_only`, so no future check reports it.

### A10 — `drf`: order email still a placeholder
Flagged 2026-07-17 as temporary; unchanged. Stated intent on the 2026-05-18 call was
customer service, not the client contact.

### A11 — `pebl`: rep↔customer filtering broken, and it was explicitly designed — CONFIRMED

**Upgraded 2026-09-04. I doubted this one and was wrong.** Territory filtering at pebl was
designed, built, and confirmed to the client in writing. Kylor to Mandy, **2026-07-01**:

> *"I created the 'Pebl Managers' group and moved Priscilla, Mandy, Tom, and Vincent into it.
> You four see all 171 customers — no territory filtering. The nine reps (Annie, Daria, Dawn,
> Gavin, Joe, Marly, Rita, Theresa, Wisteria) stay in 'Peblers' and see only their assigned
> accounts. **Territory codes set** — each rep's territory code is set in their user account
> to match what's in the customer file."*

**Twenty-nine days later, on 2026-07-30**, Mandy re-imported all 171 customers with empty
territory codes (`'[]'`), destroying the customer half of that mapping.

The current state is worse than "empty," because the user half survived:

| user | group | user territory | matching customers |
|---|---|---|---|
| `sales13@peblfurniture.com` | Pebl sales oversea | `["daria"]` | **0** |
| `sales15@peblfurniture.com` | Pebl sales oversea | `["rita"]` | **0** |

Two reps carry a filter pointing at a value no customer holds. Depending on how sync
resolves an unmatched territory they see everything or nothing — neither is the design.

**And the structure has moved further:** the `Peblers` group named in that email no longer
exists, and seven of the nine named reps (Annie, Dawn, Gavin, Joe, Marly, Theresa, Wisteria)
are not in the current user list at all.

**Not proved:** what a rep actually sees on device with an unmatched territory code. That
needs the sync payload or a device. The measurement — designed, confirmed in writing,
subsequently broken — stands on its own.

### A12 — `pebl`: 12 orders reference a deleted price level
$264,130 against price level `project`, which no longer exists in the org.

### A13 — `mali`: empty order recipient, 4 dangling references
`order_email_recipient` and backup both empty. Dangling: an eOL site pointing at price
level 5722 (exists in no org — **since fixed**, both sites now resolve), a deleted
MobileSite link in an admin-training email, a bulk-invite link pointing **into org `tcd`**,
and a "we set up two Distribution Centers" email against `distribution_centers = 0`.

### A14 — `mer` 111Mercer: 0 images on all 102 products
Catalogue is correct and priced; nothing to show on the iPad yet.

### A15 — `uhc`: org's own record disagrees with where mail goes
`company_email = sales@uniwarehouseware.com`, order mail → `uniwarehs@gmail.com`.
20,032 orders have gone through it, so it works — but it is an accepted mismatch, not a
correct configuration. Re-examine first if delivery is ever reported flaky.

### A16 — `drf`: the support handoff didn't hold
Kyla declared handoff 2026-07-20 and last appeared 2026-07-29. Suzanne's 2026-08-11
message addressed to "Kyla or support person" was answered by Kylor. Four action items
Kyla promised "this week" have no answer anywhere in the corpus.

---

## B. Decisions needed, not defects

### B1 — `leg` MATRIX sheet: products or matrix options?
22 SKUs, header on row 4. 16 already in the catalogue as ordinary products (8 hidden,
3 live), so the current build already decided. **Recommendation: leave as products.**
`matrix_options.csv` hard-deletes and reloads on import, so building one speculatively is
the expensive mistake. Does Legrand price these as combinations? One line in the next email.

### B2 — `leg`: `Catalyst` and `Futura` user groups deviate
`Catalyst` is `shared_resources_auth='a'` with 0 scoped resources; its 23 peer agency
groups are `'c'` with 96. `Futura` has 95. Intended, or missed?

### B3 — Legrand image batches were never reconciled
~2,000 files diverging in both directions between the archived 4.0 tree and canonical.
`images_batch_02_NEW` is 500/0, `images_missing_batch` is 0/613. Needs someone who knows
which batches actually reached FTP.

### B4 — `00_KICKOFF_PROMPT.md` points at an archived folder
Still says copy `_Template/` → `<Client>/`; `_Template` moved to
`_ARCHIVE_superseded_2026-09-03/`. Repoint at `02_Implementation/_Template` or archive
the prompt.

---

### B5 — `pebl` has a fourth distributor group nobody has documented

Found 2026-09-04 while verifying a rep count. `whiteline`, holding
`hadi@whitelinemod.com`, sits alongside the three already known: `ICA`
(`ckirbeyi@ica.com.tr`, Turkey), `Albania-Sezon Dekor` (`info@sezondekor.com`) and `ETC`
(`eltecul@hotmail.com`).

Not a defect — a gap in our understanding. pebl's group structure has been described in
`SCORECARD` §9 and in `config_intent.yml` as six user types, and the distributor layer was
characterised from the three we happened to notice. There is a fourth.

**Why it matters:** anything that reasons about pebl's structure — the config checker's
conformance rule especially — is working from an incomplete picture, and an undocumented
group is exactly the shape that later gets flagged as an anomaly and wastes a cycle.

**Action:** confirm whiteline is a real distributor (whitelinemod.com is a furniture
brand), then record all four in `config_intent.yml` with the same treatment ICA and
Albania-Sezon Dekor already have. While there, re-derive the group list from the database
rather than from notes — if one was missed, others may be.

**Related:** `ica.com.tr` and `sezondekor.com` were originally mischaracterised as Turkish
suppliers and corrected to distributors on 2026-08-25 (`corpus.py` note). `whitelinemod.com`
should be checked for HelpScout tickets on the same basis — the three known distributors
have zero, which is why they stayed invisible to the corpus builder.

## C. Unexplained counts — chase when convenient

| # | item | detail |
|---|---|---|
| C1 | `mali` customers | source COMBINED 2.0 has 3,517 rows, live has 3,418 — 99 unaccounted |
| C2 | `leg` customer source | 1,133 live customers, no customer file anywhere in `Source Data/` |
| C3 | `drf` inventory | 0 rows live; verified count, not an assumption. By design? |
| C4 | `mer` customers | 0 live, no customer source in the folder |

---

### C5 — `pebl`'s group set changed under us; `ICA` is gone

**Measured 2026-08-25:** pebl had a user group named `ICA` holding `ckirbeyi@ica.com.tr`,
with 2 submitted orders. Recorded in `SCORECARD` §9 and in `corpus.py`'s pebl note as one of
two named distributors.

**Measured 2026-09-04:** six groups — `Pebl sales oversea` (9), `Pebl Managers` (3),
`Pebl sales domestic` (2), `Albania-Sezon Dekor` (1), `whiteline` (1), `ETC` (1). **No `ICA`,
and `ckirbeyi@ica.com.tr` has no `org_users` row at all** — not disabled, absent.

So between those dates the group and its user were removed, and `whiteline` appeared (B5).

**Two consequences, and the second is the important one:**

1. `SCORECARD` §9 and the `corpus.py` pebl note now describe a group that does not exist.
   Record ICA as *removed on or before 2026-09-04* with its prior state, so the next reader
   does not go looking for it.
2. **The group set is not stable, so no conformance rule may cache it.** B5 concluded
   "distributor-to-group mapping is not 1:1" — correct, and the reason is not that it never
   was, but that pebl's structure moved. Any config check must re-derive the group list
   every run.

**This is the third client whose structure changed mid-programme** — leg's 13 custom fields
deleted 2026-09-03, mali's price-level 5722 dangler resolved, pebl's groups here. It is the
strongest practical argument for the dated-measurement convention: two accurate readings
taken weeks apart will disagree, and without dates one of them just looks wrong.

---

## D. Programme work not done

- **Fine Art (`fal`) as a transacting control.** 6,734 products, 6,872 customers, 3,902 orders — the only genuinely transacting org in the set. Targeted queries, not a corpus. Would let "here's what healthy looks like" rest on observation instead of inference.
- **`SCORECARD.md` § 13 — the verdict.** repair / replace / reframe. Evidence points at *reframe*. Never written.
- **A second blind read of one client**, to test reproducibility. All five are single runs; two independent runs agreeing would be much stronger evidence than one run agreeing with the framework.
- **Session-prep skill** — agent #2, kickoff never written. Mostly assembly of `corpus.py` + `rawstate.py`.
- **Snapshot bridge**, then eve. Blocked on nothing but sequence.

### D6 — Use the whole fleet as corpus, not just the 6 source-file clients

Raised 2026-09-04. The idea is right but splits in two, and the halves have different
answers.

**Mapping (source → eCat): no, and it cannot be fixed retroactively.** Learning a mapping
needs input/output *pairs*. The database holds outputs for 200+ orgs, but the source files
are gone for nearly all of them — 3 of the 6 clients surveyed had no `Source Data/` folder
at all. The mapping corpus is those ~6 clients and more orgs do not enlarge it. Treat that
as a ceiling, and start archiving source files for every new client so the ceiling rises
over time.

**Validation, config profiling and error taxonomy: yes, and it is the most valuable
corpus available.** Proof of concept, one query: the inventory-display config turned out to
be `custom_fields.alias` with a 165 / 44 fleet split — a question five clients could not
have answered and that I would otherwise have guessed at.

Three things only the fleet provides:
1. **What "correct" looks like empirically** — not "leg has 26 user groups" but "orgs of this shape have N, configured this way." This is the config agent's missing expected-profile.
2. **The complete import error taxonomy** — every warning and error ever produced, ranked by frequency, instead of the handful of incident types five clients surfaced.
3. **Archetype config profiles** — lighting vs furniture vs fabric, what each actually enables.

**Timing — this is the part that matters.** Do NOT expand scope before Phase 0/1 land. But
the `import_events` YAML parser being written for A4 and B4 has a second job: written once
for one org, running it fleet-wide is nearly free, and it converts the entire import
history into the error taxonomy. Build that parser knowing it will be pointed at
everything.

**Caveat when it runs:** `import_events` is large enough that a naive `sum(length(data))`
across the whole table times out at 30s. Batch by org.

---

## E. Framework defects recorded but deliberately not fixed

| id | defect | why unfixed |
|---|---|---|
| D2 | Phases are a checklist, not a sequence — Phase 7 needs any two of four clauses, so Phase 6 is skippable by construction | needs a design decision, not a patch |
| D3 | No adoption state. Five clients, five distinct failure modes | same |
| D10 | Import tier is silent on catalogue correctness. Confirmed on drf, mali, leg | **not fixable from Postgres.** Bounds what any log-reading automation can know |
| D19 | The D1 at-risk fix false-positives on pre-sales orgs | `overrides.yml § project_start_date` now populated for `leg`; the *rule* still needs the guard before at-risk ships |

---

## F. My own errors, for the record

Kept visible because the pattern recurs and naming it is the only thing that stops it.

| # | error | cost |
|---|---|---|
| F1 | Claimed `qty_available` is "the field the iPad displays." NULLs were real; the consequence was invented | **Reached the client.** Legrand was told inventory couldn't be displayed. False. |
| F2 | Read leg's 26 user groups as scaffolding. They are deliberate per-agency Library scoping | wrong rule built into the config checker; corrected |
| F3 | Called Legrand's price-list files an encoding problem. They are XLSX with a `.csv` extension (`504b0304`) | would have shipped an encoding ladder that decodes ZIP as mac_roman and returns confident garbage |
| F4 | Said the CopperSmith Parts header is row 3. It is row 2 | minor; caught by the session |
| F5 | `rawstate.py` had `libco: 279`. libco is **288**; 279 has zero products | any libco check through that constant returns silent zeros |

| F6 | Prescribed a fix for G1 that would not have worked — "flatten to block level." The loop was *already* block-level; 09:56 seq 1 (Options) precedes 09:56 seq 2 (Option Groups), so the window still closes unremedied at block granularity | none — the session tested the prescription before applying it, by replaying the exact pebl sequence |

| F7 | Published a breakdown that did not sum to its own total. Reported leg inventory as "755 non-null, 704 greater than zero, 28 exactly zero" — 704 + 28 = 732, not 755. **23 values are negative**, one at −12,643 | caught by the session on recount. Committed in the same message where I endorsed the specimen rule; a sum check is the cheapest specimen there is |

**F7 adds a third shape:** not an unverified consequence (F1/F3/F5) nor an untested prescription (F6), but arithmetic that contradicted itself in plain sight. **Partitions must sum to the total** belongs beside the specimen requirement — same defence, cheaper.\n\n**F6 is a different shape and worth separating:** not an unverified consequence but a confidently-prescribed remedy that was never tested against the failing case. Diagnosing correctly and prescribing wrongly is its own error.\n\n**The shared shape of F1, F3 and F5:** a measurement was correct and the *consequence
asserted from it* was never checked. That is the rule in `SCORECARD § 12 R1`, and it has
now cost something three times.

---

## G. Harness defects found in testing

Defects in the tooling being built, as distinct from defects in client orgs (§A) or in the
framework (§E). Kept separate because these are ours to fix, and because the pattern
matters more than the instances.

### G1 — A4 (import-order check) false-positives when blocks share an event

Found 2026-09-04, on the newest case the check reported, on a live client.

A4's rule is *"is every Options import followed by an Option Groups import before the next
Options import"* — correct, because importing options nulls group membership and the log
reads clean either way. The implementation evaluates at **event** level. Blocks share
events, so it breaks:

```
pebl, 2026-09-04
  09:28   Options -> Option Groups     paired, correct
  09:32   Options                      <- FLAGGED as never followed
  09:46   Products
  09:54   Products
  09:56   Options -> Option Groups     <- the actual remedy, 24 min later
  10:25   Options -> Option Groups
```

09:32 **was** remedied at 09:56. The scan for "the next Options import" lands on 09:56's
Options block and closes the window unremedied, never seeing the Option Groups block
sitting beside it in the same event.

**Live state confirms no defect:** pebl has 423 option groups, **423 with membership**,
last updated 2026-09-04 10:25.

**Reported counts are therefore wrong and pending re-run** — leg 4/1, tcs 45/7, pebl 54/10.
Expect all three to drop; some of tcs's 7 and pebl's 10 are likely the same artifact. The
corrected numbers replace SCORECARD's *"groups imported before options at tcs and pebl"*,
which stays directionally right but gains a real figure.

**Fix:** evaluate at block level within the ordered event stream — flatten to
`(timestamp, sequence_within_event, block_type)` — not at event level. `rawstate.py`
already splits blocks with `regexp_split_to_table` preserving within-event order.

**Why it was findable:** the session implemented the rule twice, in Python and in SQL,
noted the two disagreed on "OG separated from Options by an unrelated file," and recorded
it as not arising in this data. It arose. **Writing it twice is what made this catchable
before it shipped** — worth keeping as a practice for any rule with sequence semantics.

**RESOLVED 2026-09-04, and the fix was not the one prescribed.** Granularity was never the
problem — the question was. The importer runs an event's blocks in order, so an event's net
effect is decided by its *last* Options/Option Groups block. Membership is a **running state
over the event stream**, not a lookahead:

- **FATAL** — standing state is nulled and nothing restored it
- **WARN** — nulled for a period, later restored

Corrected figures, both implementations agreeing on every one:

| org | nulled windows | avg | longest | never restored | standing violation |
|---|---|---|---|---|---|
| leg | 1 | 2.6 h | 2.6 h | **0** | **0** |
| tcs | 42 | 69 min | 25.8 h | **0** | **0** |
| pebl | 25 | 11.4 h | 276.5 h | **0** | **0** |

The old rule reported 18 defects; **live defects are 0**, corroborated in state — leg 11/11,
pebl 423/423, tcs 343/343 option groups carry membership, no empty group anywhere.

Note the transient counts went *up* (tcs 7→42, pebl 10→25): the old rule counted only a
subset of the windows it was misclassifying. **The severity collapsed, not the volume** —
this is a recurring-transient problem, not a live defect, and BUILD_SPEC §3.1 A4 now says so
with these numbers.

**One finding survives** — pebl was nulled 2026-04-10 → 2026-04-22, 11.5 days. `login_events`
shows activity inside it: 8 logins on 04-10, 2 on 04-14 (squarely mid-window), 7 on 04-22.
All `DefaultUserGroup`, so admin/testing rather than field selling, and a login is not proof
of sync nor of opening a product with options. **Client-safe phrasing:** *at least one user
was active during an 11.5-day window when option group membership was nulled.* Not *reps saw
broken options.*

### G2 — The standing rule this produced

**A harness finding must be confirmed against live state before it reaches a client.**

A4 would have told a client their option groups were nulled today. The database says 423
of 423 have membership. That is the same failure class as `SCORECARD §12 R1` — the
`qty_available` claim — pointing the other way: there, the data was right and the
consequence invented; here, the log was wrong and the data exonerated it.

Three times now a claim has survived only because someone checked live state rather than
trusting the derived signal. The harness reports *evidence*, never *verdicts a client
hears*, until live state agrees.

---

### G3 — B1b must separate "unregistered and populated" from "unregistered and empty"

Found 2026-09-04 via A4's closure. B1b flags source columns that carry no Admin
registration — correct, because the importer silently drops them. But the two cases have
opposite severity:

| case | consequence | severity |
|---|---|---|
| column **populated**, not registered | **data is silently discarded on every import** | BLOCKING |
| column **empty**, not registered | 13 warnings per import and nothing else | INFO / clutter |

leg is the second case: all 13 columns present in `products.csv`, **0 populated across
1,020 rows**, POC residue from the sales process. As written, B1b returns `exit 1` on every
future Legrand build — a false alarm on a file that is fine, which is how a gate gets
switched off.

**Fix:** B1b measures fill rate per unregistered column. Populated → BLOCKING. Empty →
INFO, with the advice to drop the column from the generator rather than register the field.

Same failure family as G1: the check was directionally right and its severity was wrong,
and the cost of that is an operator who stops reading it.
