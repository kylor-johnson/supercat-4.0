# Session handoff — onboarding agent programme

**Written 2026-09-03.** Covers ~3 weeks of work (2026-08-18 → 09-03). Read this first;
it tells you what exists, what is true, and what to do next.

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
  collector/
    corpus.py          builds CORPUS_<sn>.md — deduped chronological Fathom + HelpScout
    rawstate.py        builds RAWSTATE_<sn>.json — L1 raw DB state, 6 statements
    queries.py         schema-verified SQL, all columns checked against information_schema
    collector.py       the framework collector: block parser, domain resolution, BQ loader
    RECONCILIATION.md  11 deltas between the framework spec, the skills, and live schema
    README.md
  ground-truth/
    HANDOFF_<sn>.md    ×5 — the blind-read prompts (tcd, drf, pebl, mali, leg)
    SCORECARD.md       ~680 lines. Every finding, every verification. THE artifact.
    BUILD_SPEC.md      what an ingestion agent must do (read with SCORECARD)
    SESSION_HANDOFF.md this file

onboarding-models/ground-truth/clients/<sn>/    ×5 clients   (moved here 2026-09-03)
    CORPUS_<sn>.md     the raw record the agent read
    RAWSTATE_<sn>.json live DB state at read time
    JOURNEY_<sn>.md    the blind reconstruction
    GAPS_<sn>.md       what it could not determine
```

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
- **D19** the D1 fix has a false-positive mode. `organizations.created_at` is not the project start; `leg`'s org predates its contract by a year, so the at-risk rule would have alarmed for nine months about a client that hadn't signed. **Fix before the at-risk state ships:** derive project start from HubSpot closed-won, and populate `overrides.yml § project_start_date` (currently empty).

Fixed in code: D6 (`import_active` dead — 0 of 257 orgs), D7 (`ipad_visible_products`),
D11 (`territory_codes = '[]'`), D14 (login is two surfaces — iPad *and* eOL), D15
(`is_submitted` is nullable; a bare `WHERE is_submitted` drops rows).

---

## Open client issues (verify before acting — these move)

| org | issue | status at 2026-09-03 |
|---|---|---|
| `mer` | 0 images on all 102 products | open |
| `drf` | all 389 customers at a $1.00 placeholder price level | open |
| `drf` | `order_email_recipient` still a placeholder | open |
| `pebl` | all 171 customers have empty territory codes since 2026-07-30 | open |
| `pebl` | 12 orders ($264,130) reference a deleted price level | open |
| `mali` | 4 dangling references incl. an invite link into org `tcd` | open |
| `leg` | ~~`qty_available` null~~ | **RETRACTED — was never a defect.** SCORECARD § 12 R1 |
| `leg` | 13 registered filter fields empty | open |
| `leg` | two inventory files overwriting daily | open |
| `mer` | Legrand catalogue imported into it 2026-08-18 | **FIXED** 2026-08-27 |

---

## Where things live (changed 2026-09-03)

**Canonical implementation tree is `SuperCat_Simple_Final/02_Implementation/<Client Name>/`**,
full names not shortnames. `SuperCat 4.0/eCat_Onboarding/` was a drifted partial copy
carrying 41 duplicate build scripts; its client folders are now under
`eCat_Onboarding/_ARCHIVE_superseded_2026-09-03/`, and everything newer was merged
across (manifest: `02_Implementation/_MERGE_FROM_SUPERCAT4_2026-09-03.md`).
Images were deliberately NOT merged — they diverge both ways.

## What to do next

**Immediate: build the config-check skill in Claude Code.** Not eve — see constraint 1.
`BUILD_SPEC.md § 4` has the empirical config profile (prevalence across 127 orgs) and
the cross-field contradictions worth detecting. Read-only v1. Iterate against `leg`,
`mer`, `fal` and a few active orgs until the output stops surprising you; that iteration
*is* how the expected-config profile gets written.

Then: session-prep skill (≈80% built — `corpus.py` + `rawstate.py` already do the work),
then the snapshot bridge, then port to eve. Ingestion agent third; correspondence last.

**Write both as `ecat-*` skills.** eve consumes markdown skills natively, so a skill
written now ports rather than being discarded.

---

## Things that will bite you

- **`territory_codes` empty value is `'[]'`**, not `''` or NULL.
- **`is_submitted` is nullable.** `WHERE is_submitted` silently drops rows.
- **Two login columns**: `last_ipad_login_at` and `last_ecat_online_login_at`. Measuring one misreports any org with eOL.
- **Fathom summaries ↔ transcripts join on `Recording Share URL`, never `ID`** — the ID columns match on 0 of 933 rows.
- **Fathom calls are duplicated 2–4×** (multiple recorders). Dedupe on `(meeting_title, meeting_start)`.
- **HelpScout tickets duplicate**: 21 of 31 tcd tickets were captures of 9 conversations. Collapse on subject minus `Re:`/`Fwd:`/`FW:`.
- **Two orgs are named "legrand"** — live is `leg` id 273; `lna` id 93 is an inactive 2015 org.
- **`customers.company_name` does not exist.** The column is `customers.name`. This bug meant Phase 7 could never complete a run.
- **Images dominate `import_events`** — 674 of 1,431. Never window by "last N rows."
- **A measurement is not its consequence.** "NULL on 439 rows" is a fact; "therefore the iPad shows nothing" is a separate capability claim needing separate proof. Getting this wrong sent a false statement to a client — SCORECARD § 12 R1.
- **Empty user groups are not a defect.** leg's 24 agency groups exist to scope Library links per agency. Check conformance to the org's own pattern, not fleet prevalence — § 12 R2.
- **Don't infer adoption from order counts.** eCat is a selling instrument; consummation legitimately happens in the ERP. `mali` deliberately keeps Dynamics GP as system of record; `drf` is a free-sample catalogue where $0.00 is the design. (`truth-discipline` principle 2.)

---

## Not done

- **Fine Art (`fal`) as a transacting control.** 6,734 products, 6,872 customers, 3,902 order rows, 2 user types, 73 users — the only genuinely transacting org in the set, and a Sales Portal engagement rather than iPad. Targeted queries, not a corpus. Would let the "what does healthy look like" claim rest on observation instead of inference.
- **§ 12 of SCORECARD** — the repair/replace/reframe verdict. Evidence points to *reframe*.
- A second blind read of one client to test **reproducibility** (all five so far are single runs).
