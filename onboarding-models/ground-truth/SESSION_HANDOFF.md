# Session handoff — onboarding agent programme

**Written 2026-09-03, updated 2026-09-09.** Covers 2026-08-18 → 09-09. Read this first;
it tells you what exists, what is true, and what to do next.

**09-04:** config-check shipped; the §3 harness was built, reviewed end to end and
repaired (6,515 findings → 175); Phase 0 and Phase 1 passed their acceptance tests; and the
deployment question was settled — see § *Where each agent runs*, which supersedes
constraint 1's implications.

**09-10 — eve is deployed.** `https://ecat-agents.vercel.app`. Both agents triggerable;
health, auth (401/400/200) and durable sessions verified. `ANTHROPIC_API_KEY` set in
production (Vercel AI Gateway was abandoned: Pro does not cover model spend, and Opus 5 is
gated behind paid gateway credits — the direct provider is the path that produced the only
working brief). **Blocked on one thing: a read-only BigQuery service account**
(`ecat-eve-reader`, jobUser + dataViewer on `supercat-data-pipeline`), requested from infra
2026-09-10. Without it the model runs and every tool fails.

**Cron is DISABLED**, parked at `disabled/correspondence.ts`. Three reasons, and the first
was found only by asking what the first unattended fire would do:

1. **The schedule passed a constant address `"daily"`.** In eve, `send()` to an
   already-owned address *continues* that session. Monday creates it, Tuesday appends,
   Wednesday carries both inboxes forward until compaction silently drops the oldest. **It
   would have read as model drift, not an addressing bug.** Fixed, date-stamped.
2. **The run document goes nowhere a human sees** — the completion handler logs a character
   count. A daily push agent needs a delivery target; Slack incoming webhook is the
   decision, not yet built.
3. Cost per run has never been measured, and it was scheduled 5×/week unattended.

**Memory is not enabled** (`agent/memory/` does not exist; `defineState()` dies with the
session). Correspondence therefore has no record of what it already drafted. A ticket you
*reply* to drops off correctly via thread structure; a ticket you **read and dismiss**
changes nothing in HelpScout — which the agent cannot write to — so it will re-draft it
every weekday forever. `fileMemory()` writes to Vercel Blob on deploy; Blob needs
provisioning.

**Auth is correct and needs no work:** `placeholderAuth()` was deliberately removed,
replaced with a `vercelOidc() → httpBasic() → localDev()` walk, Node pinned to `24.x`.

**09-09:** **all four agents exist.** Agent 4 (correspondence) shipped. Session prep was
verified **off-VPN** and the BigQuery key authenticates off-network — measured, the
18-August portability assumption is retired. eve was scoped properly for the first time.
Phase 2b closed: six file types map, **four ship**. The stale `~/repos/supercat-4.0` clone
was **deleted** — see § *The clone that broke three sessions*.

**09-05 (late):** A3 re-tiered on a *measured* consequence (INFO — no downstream effect);
D19's at-risk rule shipped with the `created_at` guard; **Phase 2 closed on five clients**;
and the **session-prep skill shipped**, which is agent 3 of four.

**09-05:** **F6 shipped** — one severity vocabulary, `FATAL` retired, stage / demotion /
`repair_channel`, and an org-state header that made three orgs' dormancy visible for the
first time. **Phase 2 mapped four clients** — `leg`, `mer`, `libco`, `drf` — with `libco`
and `drf` run **blind**, and the class-2 rule enforced in code after the blind run got it
wrong 3 for 3. All config moved YAML → TOML; the hand-rolled parser is gone.

---

## What this project turned out to be

It started as "help me build an onboarding agent on Vercel eve." It became: **validate
the untested assessment framework first, because deploying an unvalidated spec onto
unfamiliar infrastructure means debugging two unknowns at once.**

That validation is now **complete**, and it produced more than a verdict — it found 19
defects, seven of them live in client orgs, plus a body of evidence about what an
ingestion agent must get right.

---

## The three facts that constrain everything

1. **eve cannot reach Postgres.** `mcp-postgres-tools.tools.supercatsolutions.com` is
   split-horizon DNS — NXDOMAIN on public resolvers, resolvable only through the VPN
   (verified 2026-08-18: `dig @8.8.8.8` → NXDOMAIN; VPN resolver → 172.100.120.49).
   No credential fixes this. Anything deployed outside the network needs a snapshot
   bridge: collector inside the VPN → BigQuery → agent reads snapshots.

2. **There are no direct Postgres credentials.** No `DATABASE_URL`, no `~/.pgpass`,
   psycopg2 not installed. The only DB access is the `supercat-postgres-vpn` MCP.
   Everything here runs through it. The one outstanding credential ask is a read-only
   `DATABASE_URL` against a replica, which would make the collector cron-able.

3. **BigQuery is already portable.** The `bigquery-admin` MCP uses a service-account key
   at `integrations/bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json`.
   Non-interactive, works anywhere. Fathom + HelpScout are already in BigQuery and fresh.

---

## What was built

```
onboarding-models/
  collector/       ~1,550 loc  corpus.py (Fathom+HelpScout corpus), rawstate.py (L1 DB
                               state), queries.py, collector.py, RECONCILIATION.md
  profiler/        ~1,720 loc  Phase 0 — folder_mode, file_mode, ecat_aliases, ecat_vocab
  ecatlib/                     Phase 1 — 19 primitives, dialect-aware. parse_int and
                               round_decimals were added rather than take a 4th escape hatch
  mapping/                     Phase 2 CODE — mapper.py (631 loc, client-agnostic, the only
                               code that runs), inputclass.py, validate.py, pins.py,
                               bless.py, score_blind.py, required_check.py, preupload_check.py
  mappings/<client>/*.toml     Phase 2 DATA — leg, mercer, libco, drf. Code and data are
                               deliberately separate trees
  acceptance/      ~1,730 loc  Phase 3 — a1_fingerprint, a4_b4, b1_fields, import_log,
                               state_checks, intent.py
  config_intent.toml           declared intent, WIRED (F5). stdlib tomllib, fails closed
  overrides.toml               likewise. project_start_date.leg now actually loads — it had
                               been inert since D19
  ground-truth/
    SCORECARD.md               ~680 lines. Every finding, every verification. §12 =
                               retractions — two findings were wrong
    OPEN_ITEMS.md              ~670 lines, §A–G. THE live record of what is flagged and
                               unactioned. §F is my own errors; read it before repeating one
    BUILD_SPEC.md              §2 library boundary + dialect problem, §3 acceptance criteria,
                               §4 empirical config profile across 127 orgs
    KICKOFF_config_check.md    shipped
    KICKOFF_ingestion.md       Phases 0–1, both DONE — the wrong door for new work
    KICKOFF_mapping.md         Phase 2 — the live one
    SPEC_F6_severity.md        the F6 spec: five decisions, shipped 09-05
    SESSION_HANDOFF.md         this file
    clients/<sn>/  ×5          CORPUS, RAWSTATE, JOURNEY, GAPS — the blind reads
```

`~/.claude/skills/ecat-config-check/` — shipped, read-only, iterated to quiet.

Framework bumped **v3.5 → v3.6** (`Phase_Anchors.md`, `Phase_Progression_Framework.md`).

---

## The method, and why it worked

For each client an agent in a **fresh session** read every Fathom transcript and
HelpScout thread chronologically, **blind** — explicitly forbidden from opening
`CLIENT_PROFILE.md`, `HANDOFF.md`, or any framework document — and wrote its own
timeline. Then those claims were verified against live Postgres.

**Result: ~55 claims across 5 clients, one immaterial slip** (nine price levels, not
eight). Three times a blind read survived a direct challenge from the reviewer and was
right.

**Four defects were found in the audit tooling itself, by the agents, not the reviewer.**
The most instructive: a query reporting "every customer has a territory" when none did,
because the empty value is stored as the literal string `[]`, not `''`.

Two rules made this work and should be kept if it is repeated:
- **The blind rule.** Give the agent the *phase questions* but never the framework's
  anchors. It produces comparable output *and* can tell you the model is wrong-shaped —
  which it could not do if handed the rules.
- **Ask the questions the model doesn't.** The most valuable findings every time came
  from "did this client go backwards," "adoption separate from go-live," and "was the
  catalogue wrong while imports looked clean."

---

## The verdict on the framework

**Phase 1–3 machinery is correct.** Every backtestable transition matched.

**The structural defects are not patchable** — they are the model being the wrong shape:

- **D1** no regression state → *fixed in v3.6, but see D19*
- **D2** phases are a checklist, not a sequence — Phase 7 needs any two of four clauses, so Phase 6 is skippable by construction. Recorded, not resolved.
- **D3** no adoption state. Five clients, five distinct failure modes. Recorded, not resolved.
- **D10** import tier is silent on correctness. Confirmed on drf, mali, leg. **Not fixable from Postgres** — it bounds what any log-reading automation can ever know.
- **D13 / D16** three sources nothing reads: `audit_log_entries`, `organization_invitations`, `login_events`.
- **D19** the D1 fix has a false-positive mode. `organizations.created_at` is not the project start; `leg`'s org predates its contract by a year, so the at-risk rule would have alarmed for nine months about a client that hadn't signed. **Fix before the at-risk state ships:** derive project start from HubSpot closed-won, and populate `overrides.toml § project_start_date` (currently empty).

Fixed in code: D6 (`import_active` dead — 0 of 257 orgs), D7 (`ipad_visible_products`),
D11 (`territory_codes = '[]'`), D14 (login is two surfaces — iPad *and* eOL), D15
(`is_submitted` is nullable; a bare `WHERE is_submitted` drops rows).

---

## Open client issues (verify before acting — these move)

| org | issue | status at 2026-09-04 |
|---|---|---|
| `mer` | 0 images on all 102 products | open |
| `drf` | ~~all 389 customers at a $1.00 placeholder~~ | **CLOSED — by design.** Presentation-only client; pricing lives in stories. Now DECLARED |
| `drf` | `order_email_recipient` still a placeholder | open |
| `drf` | 2 filter chips that cannot match | open, real |
| `pebl` | all 171 customers have empty territory codes | open, real, and **designed that way** — see OPEN_ITEMS A11 |
| `pebl` | 12 orders ($264,130) reference a deleted price level | open |
| `mali` | option-group membership + 4 dangling references | open, real |
| `leg` | ~~`qty_available` null~~ | **RETRACTED — never a defect.** SCORECARD §12 R1 |
| `leg` | ~~13 registered filter fields empty~~ | **CLOSED — deliberately deleted, POC residue** |
| `leg` | **two inventory files overwrite each other daily** | open. Now confirmed THREE independent ways — see below |
| `mer` | Legrand catalogue imported into it 2026-08-18 | **FIXED** 2026-08-27 |

### A8 is the result worth understanding

`leg`'s two-inventory-file overwrite was found first in the **conversation record** (blind
read of Fathom + HelpScout), then independently reproduced by **B4 from `import_events`
alone** — a check calibrated on four entirely different orgs — and then explained by a
third route: the files arrive as **email attachments**, `LegrandAdorneInventory.xlsx` and
`LegrandRadiantInventory.xlsx`, every day including weekends, against one import slot.
`inventory.csv` hard-deletes and reloads, so each day one file erases the other. Resident
row count flips: 439/adorne 08-27, 755/radiant 09-04.

It is the first time the harness recovered something previously classed as visible only in
the corpus. The reusable part: **A8 is a shape over time, and every check that had read
`import_events` before read events one at a time.** Point that lens at the other
sequence-shaped questions before assuming they need a corpus.

## Client issues added 2026-09-05

| org | issue | how it surfaced |
|---|---|---|
| `cl` | **212 users, no import in 134 days, no order since 2025-02-28** | F6's org-state header, on an org that had been returning clean. Business signal, not a defect — A24 |
| `ufi` / `clli` / `pebl` | 15 / 13 / 10 users in `login_events` with no `org_users` row | accounts destroyed rather than deactivated. `pebl`'s ten explain its 27 orders with NULL `org_user_id` |
| `libco` | 199 of 1,992 image refs missing — **9 of them primary**, so 9 products have no image at all | blind mapping run, confirmed live via `images_json` — A21 |
| `libco` | three registered binary filters carry `Yes`/`No`, not `Y`/`N` | blind run — **this is A5, re-derived independently.** Merged, not added |
| `drf` | source folder holds **one season's supplement** — 884 of 1,627 built SKUs (54.3%) belong to families absent from it, and nothing says so | blind run reconciliation. The drf failure reproduced exactly |
| `leg` | `LongDesc` capped at 50 where the importer allows 255; **386 of 1,020 word-boundary truncated** | Phase 2. Client question, not a code question |

**Two filings were refuted against live and that is the point** — `libco` UPC float-tails
(0 of 912 live) and `FinishCode` case-duplicates (0 pairs live) were both true of the
source and false of the org. They had been filed into §A with a *"confirm before this
reaches the client"* caveat, which was correct and insufficient. §A now means **confirmed**
— see A23.

## Where things live (changed 2026-09-03)

**Canonical implementation tree is `SuperCat_Simple_Final/02_Implementation/<Client Name>/`**,
full names not shortnames. `SuperCat 4.0/eCat_Onboarding/` was a drifted partial copy
carrying 41 duplicate build scripts; its client folders are now under
`eCat_Onboarding/_ARCHIVE_superseded_2026-09-03/`, and everything newer was merged
across (manifest: `02_Implementation/_MERGE_FROM_SUPERCAT4_2026-09-03.md`).
Images were deliberately NOT merged — they diverge both ways.

## The clone that broke three sessions — deleted 2026-09-09

`~/repos/supercat-4.0` was a Sep-4 clone that predated every Phase 2 artifact. Three
separate sessions searched it, concluded work was missing, and reported confidently:

| session | claimed missing | reality |
|---|---|---|
| eve recon | `ecat-session-prep`, `ecat-correspondence` skills | both exist, 708 and 578 lines |
| config-check | (inverse) claimed config-check was installed | it was not — install never happened |
| ingestion runner | `mapping/`, `b7_lossy`, `required_check`, `PHASE2_COMPLETE.md` | all exist in iCloud |

The runner session then built ~13 minutes of work into that tree; **none of its output
exists on disk.** It also invoked `build_ecat_files.py` unsandboxed and overwrote
`Legrand/Build/stories.csv` in the live client tree (restored from git, verified clean).

**Root cause was the prompts, not the sessions** — none of them named the canonical path.
**Every prompt from here names it explicitly:**

```
/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/onboarding-models
```

`~/repos/ecat-onboarding-workspace` still exists and should stay — it is the deliberate
git-backed subset of `SuperCat_Simple_Final` (5.7 GB, unpushable). It holds no `Source
Data`, so it cannot mislead a source run, but it does hold `Build/` dirs for 13 clients.
Absolute paths, always.

## Where the skills live — fixed 2026-09-09

`~/.claude/skills/` is what Claude Code loads and is **not under git and not in iCloud**.
`SuperCat 4.0/.cursor/skills/` is the iCloud-synced mirror. They had drifted both ways:

- **`ecat-config-check` existed only in iCloud** — so agent 2 had never once been loadable
  by Claude Code, five days after it shipped. Now installed and confirmed live.
- **`ecat-session-prep` (708 lines) and `ecat-correspondence` (578) existed only in
  `~/.claude`** — the two eve-bound agents, on one machine, no git, no iCloud. Now mirrored.

`ecat-admin-write` and `supercat-jira` remain iCloud-only, deliberately — one writes to the
Admin Console and one touches Jira, and both are Kylor's call to install.

## Where each agent runs — settled 2026-09-04

The original plan was "build everything, port it all to eve behind a snapshot bridge."
That was wrong. The four agents split into two kinds of thing:

| | agent | what it actually is | runtime |
|---|---|---|---|
| 1 | **Ingestion** | ~5,900 loc deterministic Python + SQL, one judgment step | inside the VPN |
| 2 | **Config check** | read-only Postgres, rules with reasons | inside the VPN |
| 3 | **Session prep** | reads BigQuery (Fathom + HelpScout) — **portability MEASURED** | **eve** |
| 4 | **Correspondence** | BigQuery reads; **drafts only, no HelpScout write path exists** | **eve** |

Agents 1 and 2 are not agents. They are pipelines with a small review step, and their value
is the code, not the prompting. Run them where the database is — Agent SDK in a container
inside the VPN, on a cron. **The snapshot bridge is off the critical path**; it was only
ever needed to force 1 and 2 into the wrong home.

Agents 3 and 4 are the genuinely agentic ones, and their sources are already portable. They
can deploy to eve without the bridge that has been blocking everything.

## Where the harness stands — final

Thirteen orgs, after F6 + the A3 re-tier + D19:

```
BLOCKING      5     all five real and actionable
WARN         77
INFO        112
findings    194
DECLARED      2     counted separately — intent, not a finding
NOT CHECKED  32     counted separately — method, not a finding
```

**The five BLOCKING:** `pebl` B3 territory codes 171/171 empty against 9 reps · `mali` A4
option-group membership nulled now, 2 of 2 · `leg` B4 two inventory feeds (A8) · `drf`
B1a ×2 empty registered multi-filters (`OriginalProduct`, `SampleType`, 0 of 1,627).

**A3 dropped from BLOCKING to INFO on a measurement, not a judgement.** A dangling
`orders.price_level` has no downstream consequence: totals are stored not recomputed (421
of 421 non-null at `ufi`, $3.94M), `orders` carries exactly two foreign keys and
`price_level` is not one, and Sales Portal reporting runs on `portal_orders`, which has no
`price_level` column at all.

The confound is the part worth keeping. Dangling orders showed **18.3% zero-total against
0.7%** for resolving orders — a 26× gap that looked like a real consequence. Per level it
vanished: `H` and `C` are **status codes pooled into a column named "price level"**, 74
orders and $625 across four years. Exclude them and it is 1.2% against 0.7%.
`customers.default_price_code` stays BLOCKING — that one is forward-looking, and a customer
on a missing level breaks the *next* order rather than describing an old one.

**D19's at-risk rule shipped with its guard demonstrated.** Seven `project_start_date`
values derived from HubSpot closed-won, expansion and renewal deals deliberately excluded.
Six orgs have no derivable date and report `NOT CHECKED` rather than falling back to
`organizations.created_at` — with the fallback restored, `cl` reads *"4,527 days in
onboarding"* on a twelve-year-old client that is not onboarding. That is D19 reproduced on
demand. `mer` and `tcd` sit at exactly 2 core file types with zero margin.

**The header is what fixed the cold read**, and it earned itself immediately — see A24.

## Phase 2 — six file types map, FOUR SHIP

`leg` `mer` `libco` `drf` `tcs`, three input classes, zero bespoke loaders. Escape hatches:
leg 1 · mer 3 · libco 0 · drf 0 · tcs 2, against a budget of 3 re-derived from four
measured counts. No client has a required field lacking a plausible source column.

**`options` and `option_groups` map but cannot ship.** The membership metric was wrong —
it counts distinct sets, and Finish is 2 of 311 sets applying to 375 of 379 products. The
metric that matters is per-product option availability: **0 of 379 exact**, recall 85.5%,
precision 83.2%, **1,312 MISSING and 1,561 EXTRA**. EXTRA is the dangerous direction — a
rep can order a configuration that may not fit and nothing objects. Two client asks block
it: 13 codes exist in no file in the folder (`COPPER` is a finish on 375 of 379), and the
1,561 extra offers. Supplying the codes alone reaches 51.2%.

The `LR` root cause is worth keeping: **the catalogue's option type is per CODE, the
matrix's is per COLUMN.** `Ladder Rests` is a POST & PIER MOUNT in the catalogue and a
ceiling mount in the matrix; 68 of 100 wrong sets differed by exactly that one code.

`OptionSet` ceiling is **20, not 5** — CLAUDE.md said 5 and was wrong (30 orgs above 5,
37,803 references). The mapper never capped, but never refused out of range either:
`OptionSet21` imports as a silently ignored column and takes the whole axis with it. Now
refuses at build time.

## eve — scoped properly for the first time

**The markdown ports. The toolbelt does not.** eve is filesystem-first
(`agent/skills/<name>/SKILL.md`, frontmatter needs `description`), so translating 708 lines
is an afternoon. But eve ships only `bash`, `read_file` and `write_file` against its own
sandbox — **every `bq` call and every `mcp__*` invocation becomes a `defineTool` TypeScript
file.** That is the real work and no plan had a line item for it.

**Measured off-VPN 2026-09-09, tunnel genuinely down:** the BigQuery service-account key
authenticates off-network — 43,563 rows returned. Auth is a local JWT signature plus a POST
to `oauth2.googleapis.com`; no VPN-reachable dependency exists in the path. **The 18 August
assumption is retired.**

| | |
|---|---|
| **The one hard stop** | org→domain resolution is a Postgres read. Off Postgres, session-prep falls back to a static **6-client registry** — a seventh client cannot be briefed. Ship an org→domain table to BigQuery. |
| **Plan** | Hobby is disqualifying twice over: **non-commercial use only**, and cron floors at once-per-day at ±59 min. Pro, $20/seat/mo. A terms problem, not an engineering one. |
| **Credentials** | `process.env`, 64 KB cap, key is ~2.4 KB. Inline `credentials` object, **not** `GOOGLE_APPLICATION_CREDENTIALS` — the function filesystem is read-only outside `/tmp`. |
| **Service account** | Two exist — `bq-admin@` and `cursor-gc-mcp@`. **Provision a new least-privilege read-only SA**; do not paste an admin key into an env var. |
| **Triggers** | session-prep is **event**-shaped → calendar webhook into `POST /eve/v1/session`. correspondence is cron-shaped → a **TypeScript** schedule handler, never markdown (markdown runs in task mode and cannot park for a human). |
| **Network** | Outbound HTTPS unrestricted in the app runtime. No allowlist. |
| **Connect** | HelpScout is not in the catalog; BigQuery is not a listed Google connector. Both land on plain env vars. |

The Postgres failure signature from eve is exactly `mcp-remote: fetch failed` — no
hostname, no reason, no hint a VPN is involved. **An agent will read that as a retryable
blip.** Treat it as permanent.

## What to do next — two prompts, that is all that is left

1. **Finish agent 1** — a single entrypoint over the real `mapping/` layer, plus four live
   bugs: `build_ecat_files.py` ignores `--out` and writes beside itself (this clobbered
   `Legrand/Build/stories.csv` on 09-09); **five of Legrand's eleven source files were
   iCloud dataless placeholders**, invisible to `find -name '*.icloud'` but caught by the
   `UF_DATALESS` flag; `openpyxl` is on `/usr/bin/python3` and not on Homebrew 3.12; and
   `build_ecat_files.py:39` hardcodes an image path into `~/Downloads` and warns-then-
   continues.
2. **Build eve for real** — both agents, per the table above.

**The database half of the cron ask needs no approval.** `collector.py:197-217` already has
a working `DATABASE_URL` + psycopg2 path; all four acceptance modules have **zero**
`DATABASE_URL` support (`--emit-sql` / `--from-results` only). So the replica credential
alone still leaves the gate unable to run in a container — those ~10 lines need replicating
four times. Profiler and ecatlib touch no database at all.

## Things that will bite you

- **`territory_codes` empty value is `'[]'`**, not `''` or NULL.
- **`is_submitted` is nullable.** `WHERE is_submitted` silently drops rows.
- **Two login columns**: `last_ipad_login_at` and `last_ecat_online_login_at`. Measuring one misreports any org with eOL.
- **`orders.submit_date` is the business event; `orders.created_at` is the row.** They
  diverge on backfills and re-syncs. `clli` order `63390-022021-7` (THE LIGHTING BOUTIQUE,
  $20,252.25) was submitted **2021-02-21** and its row created **2026-08-05** — five and a
  half years apart. Rare but extreme: 5 of 1,362 at `clli` (max lag 2,002 days), 80 of
  3,909 at `fal` (641), 22 of 37,817 at `ufi` (**4,751 days**). Any recency filter keyed on
  `created_at` will surface a thirteen-year-old order as new; keyed on `submit_date` it
  will miss that the row changed last month. Report both.
- **THREE column pairs now look like they answer the same question and do not.**
  `qty_available` / `qty_on_hand` (§ 12 R1), `org_users.last_ipad_login_at` /
  `last_ecat_online_login_at` plus `login_events` (D14), and `orders.submit_date` /
  `created_at` (above). It is a recurring shape in this schema, not three coincidences:
  **before using any column as "the" answer, look for its sibling.**
- **Fathom summaries ↔ transcripts join on `Recording Share URL`, never `ID`** — the ID columns match on 0 of 933 rows.
- **Fathom calls are duplicated 2–4×** (multiple recorders). Dedupe on `(meeting_title, meeting_start)`.
- **HelpScout tickets duplicate**: 21 of 31 tcd tickets were captures of 9 conversations. Collapse on subject minus `Re:`/`Fwd:`/`FW:`.
- **Two orgs are named "legrand"** — live is `leg` id 273; `lna` id 93 is an inactive 2015 org.
- **`customers.company_name` does not exist.** The column is `customers.name`. This bug meant Phase 7 could never complete a run.
- **Images dominate `import_events`** — 674 of 1,431. Never window by "last N rows."
- **A measurement is not its consequence.** "NULL on 439 rows" is a fact; "therefore the iPad shows nothing" is a separate capability claim needing separate proof. Getting this wrong sent a false statement to a client — SCORECARD § 12 R1.
- **Empty user groups are not a defect.** leg's 24 agency groups exist to scope Library links per agency. Check conformance to the org's own pattern, not fleet prevalence — § 12 R2.
- **A CSV taxonomy value is a NAME; the database stores a CODE. Never compare them
  directly.** Verified fleet-wide 2026-09-09: `taxonomies` resolves code→name for **four**
  types — `Collection` (65,896 terms across 239 orgs), `Category` (13,207 / 243), `Group`
  (6,477 / 243), `TradeName` (1,336 / 243). `leg`'s file carries `adorne`;
  `products.trade_name_code` stores `TN2`; `taxonomies` maps `TN2 → adorne`.

  B7's spot-check hit this and reported **100% disagreement on a byte-identical file** —
  it would have cried wolf on every org forever. Fixed for `TradeNameCode`, but the same
  join is required for **`CollectionCodes`, `CategoryCodes` and Group**, which are far more
  prevalent. Any check comparing a file value to a stored value must resolve through
  `taxonomies` first.

  Distinct from, and compounding, the standing rule that whatever string you send in those
  columns **becomes the iPad label** — so never ship `COL37`/`TN1`.
- **FOUR sibling-column pairs now look like one answer and are not:**
  `qty_available`/`qty_on_hand`, the two login columns plus `login_events`,
  `orders.submit_date`/`created_at`, and **`products.images`/`images_json`** — the latter
  empty on all 915 `libco` rows while `images_json` carries the data. Before using any
  column as "the" answer, look for its sibling.
- **Every check must state its coverage — `evaluated N of M candidates`.** Now BUILD_SPEC
  §3.4, added after the **sixth** instance of one failure across two independently written
  codebases: a check with nothing to measure reporting a pass or a fail. Five of the six
  were caught only because somebody happened to look at an adjacent number.
- **A lookup that returns nothing must not report it as an answer.** Instances:
  `territory_codes = '[]'` (reported "everyone has a territory" when nobody did); B4's
  `sig <> '0/0'`; and F6's `_key()`, where `file:option_groups` never matched the event
  key `Option Groups`, so 73 windows sat at WARN *looking evaluated*. A silent miss is
  indistinguishable from a real negative unless you make it say so.
- **A score over an empty intersection is not a score.** `score_blind.py` reported 21
  byte-exact columns for `drf` over **0 shared rows** — the build is keyed pattern ×
  colourway, the source only carries pattern. Structurally the same vacuity as a test that
  cannot go red.
- **A fatal import block's signature is NOT `0/0`.** 1,594 fatal blocks across 13 orgs;
  **1,292 of them (81%) also carry warnings or errors**, so their signature looks like any
  other. Reasoning from the name of a sentinel to a claim about severity cost a wrong
  prediction — OPEN_ITEMS §F8. A fatal import means the whole file was rejected and
  **nothing changed**, so for any question about what overwrote what, fatal blocks must be
  dropped from the stream, not merely distinguished.
- **A green check is only as good as its declared scope.** The recurring failure in the
  harness was never wrong logic — it was correct logic whose applicability was never
  bounded, verified against the org that motivated it and never against one shaped
  differently. Every check states what it did NOT evaluate.
- **Don't infer adoption from order counts.** eCat is a selling instrument; consummation legitimately happens in the ERP. `mali` deliberately keeps Dynamics GP as system of record; `drf` is a free-sample catalogue where $0.00 is the design. (`truth-discipline` principle 2.)

---

## Not done

- **Phase 2b — `options`, `option_groups`, `customers`, `stories`.** Four of six eCat file
  types are unmapped. Options first: `tcs` cannot ship without them.
- **Correspondence agent** (4 of 4). Not started. Scope now includes the email ingestion
  path — client files arrive as attachments into `active_storage_blobs`.
- **Six orgs have no `project_start_date`** and so are unassessed by the at-risk rule:
  `cl` `clli` `sp` `uhc` `ufi` `fal`. HubSpot holds only expansion deals or open
  subscription records for these. **`cl` is the one that matters** — it is genuinely below
  threshold and currently NOT CHECKED.
- **Phase 0 false negative:** folder mode reports `options.csv` MISSING when the options
  are present but transposed into a product sheet (`tcs`, 57 columns → `OptionSet1–8`).
- Reproducibility of the blind method: **one data point now, and it held** — `libco`'s
  Yes/No filter finding is A5 re-derived by an agent that had never read A5.
- The **email ingestion channel** is still undocumented in `BUILD_SPEC`.
- `SuperCat_Simple_Final` needs a `.gitignore` before either folder is pushed — 5.7 GB,
  10,217 binaries. **And `~/repos/supercat-4.0` is a stale checkout whose commit message
  claims source-of-truth; iCloud is canonical.** Resolve before any push.
