# Where you tap in

**A point of view on Felix, the factory, the commercial-truth thesis, and the onboarding work — and what to do with all of it.**

23 October 2026 · for Kylor · one sitting

---

## The verdict, first

Do not bolt this onto Felix. Do not commercialize the four onboarding folders as four agents. Do not try to ship an "Onboarding Orchestrator" to a customer. Do not treat Data Health Monitor, Product Ingestion, Territory Coverage, and Config Check as separate products.

Build **one Felix-class agent** whose job is the commercial substrate: get the catalog truthful, get the ERP feed landing, and keep it from silently rotting after go-live. Give it one identity, one contract, two objectives, and a small set of atomic jobs — the same shape Felix has, for a different person, on a different surface, with a different never-emit list.

Keep everything you already built that only SuperCat staff can operate — mapping blessing, import orchestration, session prep, correspondence — as the **internal delivery harness**. That is how implementations get shipped and how the golden set gets written. It is not the product.

Your post-work role is the same job Kjael is doing for Felix this week: **judgment, not code.** You write the tests from the scars. You decide what the agent is told each turn. You define what every field and status means. You write the checks that block a claim with no fact behind it. Brent builds the platform seams. You own whether the answer is right.

The working name used below is **Substrate**. Factory folder: `agents/substrate/`. Customer-facing name can wait. The identity cannot.

---

## What this document is, and what I actually read

This is a decision memo, not a survey. It exists because you asked for a point of view on where you tap in, and because the company is currently holding two true statements that look like they contradict:

1. Product truth is the root wedge. SuperCat already holds the catalog. The prize is owning the revenue work layer, and that layer is only as good as the feed.
2. "Onboarding Orchestrator" fails the commercial scope gate because the operator is you.

Both are true. The mistake is treating (2) as a reason not to build (1).

I read the sources below in full, not by title. Where I could not open something, it is named at the end. Nothing in the verdict depends on an unread file.

**Factory and Felix**

- `~/repos/agent-factory` — README, AGENTS.md, layer map, live registry
- `agents/sales_assistant/` — CANON, OVERVIEW, ARCHITECTURE, CONTRACT, README, TOPOLOGY
- `standards/market_facing_agents.md` — Stage 0 lock, HITL law, the honesty-gates-ate-the-product scar
- `foundation/08_how_we_build.md` and `foundation/09_agent_factory.md` (and the factory mirrors)
- `foundation/CEO_SYSTEM_CONTEXT.md`, truth-discipline, personas, JTBD register
- `/Users/kylorjohnson/Downloads/Felix in plain English.md`
- `/Users/kylorjohnson/Downloads/Felix_Review_Plan_v1.1.docx` (extracted)

**Strategy pages (today)**

- [Agent Research POV, 2026-10-23](https://ceosystem.io/ceo-system/agent-research-2026-10-23)
- [Agentic Commercial Truth Layer](https://ceosystem.supercatsolutions.com/projects/agentic-commercial-truth-layer-strategy)

**Your onboarding tree**

- `onboarding-agents/README.md` and all four agents
- Ingestion: KICKOFF, BUILD_SPEC, SCORECARD (front and the incident sections), PHASE2_COMPLETE, MAPPING_FORMAT, BUDGET, FINDINGS_runner, runner/clients.toml shape, acceptance criteria A1–A4 / B1–B6 / §3.4
- Orchestrator skill + PHASE_GATES
- Config-check skill (through the contradiction prize and staff-exclusion rule)
- Session-prep skill (the diff-since-last-conversation contract)
- Correspondence FINDINGS (no HelpScout write path; 6.4h mirror lag; 57% already answered)
- Sales Portal onboarding skill (ERP history files, identity joins)
- Sales Data Scoping Framework
- Health V3 README (what it is and is not)
- CEO System `onboarding_reality` prompt (Lane A / Lane B, and the hard line that SuperCat-staff orchestrators are not `agent_research` candidates)

**Not opened (named, not smoothed over)**

- The Claude artifact at `claude.ai/artifact/WeXQHgJjRWSKBwzGV3vzWd` — login wall. If it is a Felix UX or north-star artifact, it would refine Phase 2 color, not the architecture decision.
- The GitHub web trees — 404 from here. The local clone at `~/repos/agent-factory` is what I used.
- The Notion Agent Factory page. The in-repo mirror is stamped 2026-07-28; Notion wins on conflict. I treated the mirror as orientation, the live `AGENTS.md` registry as current.

---

## 1. What Felix actually is

Strip the demo and the six starters. Felix is one product with this lock:

| Slot | Lock |
|---|---|
| Buyer | Manufacturer sales leadership |
| Recipient | Assigned field rep |
| Moment | Any field moment — prep, bag, book-protect |
| Input authority | SuperCat tenant data (Postgres; later price/inventory feeds) |
| Surface | SuperCat app (iPad conversation) |
| Two objectives | **A** protect the assigned book · **B** win the visit |
| Topology | Contemplated `tenant_conversation` — not `operator_skill`, not a scheduled report |
| Production home | `supercat_server` + public workers. Not Windmill. Not Cursor. |
| Honesty | Evidence engine owns facts. Doctrine owns judgment. Compiler leak-strips. Frontier writes the visit. |

The six canned prompts are **atomic elements and a handholding grammar**, not the product. OVERVIEW is explicit: a free-text "prep me" must still produce Prep substance. A seventh canned prompt is a failure. New objectives are other products.

That last sentence is the most useful thing in the whole Felix folder for your problem.

The review plan (v1.1, 14 Oct) is asking a harder question than "do the six starters work": is Felix becoming an exceptional sales partner, or an interface for preselected questions. The hardening brief (22 Oct, Kjael) translates that into factory language: six harness parts, three control functions, tests before fixes, launch checks before reps.

| Part | What it decides |
|---|---|
| Orchestration | Who is asking, which account, which tools, when to stop |
| Context | What Felix is told, in what order, and what wins when things conflict |
| Instructions / skills | How it behaves per job |
| Tools | Which facts exist, and what each field means |
| Verification | Whether the about-to-be-said claim is backed by a fact |
| Actions / presentation | What the rep sees, and what Felix may do |

Around those: **observe** (Langfuse traces), **evaluate** (test cases), **release** (a versioned record you can roll back). Six of the seven 19 Oct mistakes sat in tools, context, or verification. One sat partly in wording. "Just fix the prompt" is usually the wrong answer. That will be true for Substrate too.

The factory already wrote the cousin out loud. `sales_assistant/TOPOLOGY.md`:

> A new topology is justified when a second agent would reuse the same harness bundle. Likely later cousins: **a CS/onboarding copilot on the same instance**; a quote-to-order assistant.

So the company has already imagined your agent as a *cousin of Felix's harness*, not a feature inside Felix. That is the right instinct. Do not lose it.

---

## 2. What the strategy pages are actually saying today

The April thesis and the 23 Oct research board are the same argument at two altitudes.

**The thesis.** The home-furnishings market does not need a generic sales copilot. It needs a commercial truth layer: messy product reality → structured, orderable, channel-ready truth → then the downstream revenue workflows. SuperCat already holds the catalog, the orders, the reps, the dealers. The distance is extensions and intelligence, not a rebuild.

Three labor layers, in priority order:

| Layer | Work | Agentic role | Where Felix sits | Where you sit |
|---|---|---|---|---|
| I · Product truth | Ingest, normalize, config logic, pricing governance, syndication, QA | Automate the substrate | Downstream consumer | **This is the job** |
| II · Revenue service | Quotes, exceptions, dealer support, follow-up | Orchestrate the desk | Adjacent (quote-to-order is a later Felix bet) | Feed quality is the constraint |
| III · Relationship selling | Territory, visits, prep, CRM capture | Copilot the human | **Felix lives here** | You make Felix's numbers true |

Felix is a Tier III copilot standing on a Tier I floor you have spent a year proving is rotten in specific, named, recurring ways. A Felix that is perfectly traced and perfectly eval'd will still tell a Craftmade rep about 5,600 accounts if the assignment map is wrong, and it will still recommend a restock from inventory that another brand's feed silently overwrote last night. That is not a Felix problem. That is why Substrate exists.

**The 23 Oct board, ranked.**

| Rank | Candidate | What it really is | Operator the board named |
|---|---|---|---|
| 1 | Variant / Configuration Intelligence | Orderability rules before a broken SKU hits a rep | Customer's catalog admin / IT / ops |
| 2 | Data Health Monitor | Post-live ERP↔eCat integrity | Customer's catalog / ops admin |
| 3 | Territory and Account Coverage | Rep↔account attribution the sales leader can see | Customer's sales leader |
| 4 | Multi-Price / Pricing Display | Admin-configurable price/availability truth | Customer's catalog admin |
| 5 | Product Ingestion & Normalization | Pre-live and post-live catalog validation | Customer's catalog admin |

And, in the same document, **scope-flagged / failed**:

| Candidate | Why it failed |
|---|---|
| Integration Field Mapper | First-90-day operator is still SuperCat CTO/PS |
| Onboarding Orchestrator | Operator is SuperCat CS (you, Kyla) |
| Internal Order Recovery | Operator is SuperCat eng/support; customer-facing slice = DHM |
| NetSuite Order Export (PR #2663) | Bespoke engineering per customer; no self-serve mapping surface |

Read that table twice. The board is not saying "don't build ingestion." It is saying "don't sell a SuperCat-staff workflow as a customer product." That is the same rule as Line Brief vs Market Field Kit: **a shared GTM moment is not a shared product. Split when the operator or the input authority differs.**

The board's own `reconsider_when` lines tell you the conversion path:

- Field mapper becomes Substrate when a customer will operate the mapping.
- Orchestrator becomes a customer portal when self-serve onboarding is the delivery model.
- Order recovery becomes Substrate when the customer can remediate from Admin.
- NetSuite export becomes Substrate when the mapping is configurable across accounts.

Until those are true, those pieces stay in the internal harness. That is not a consolation prize. That is how Felix was built: the useful author lived in a skill for months; the hosted product had to earn the same substance bar before it replaced the author.

---

## 3. What you actually built — honest maturity

Four agents, one controller, and a pile of ecat-* skills. They are not four products. They are four *seams* of one job, written as skills because that is the tool you had.

### Agent 1 — Ingestion (`1-ingestion/`)

This is the only one that is already an agent in the factory sense: a pipeline with a contract, an acceptance bar, and measured reproduction.

- **Phase 0 profiler.** Folder-mode before column-mode. The expensive question is "which of these files is the one," not "how do I parse this column." Legrand's `Source Data/` is 91% not source data. mali has two customer files indistinguishable by name, header, or date.
- **Phase 1 `ecatlib`.** Twelve shared primitives, per-client *dialect* (never inferred). Naive merge would silently rewrite three clients' files. That finding is load-bearing: the dialect *is* the business dictionary Felix's review plan is asking for, applied to catalog fields instead of rep statuses.
- **Phase 2 mapping.** A build used to produce a script (~60 of them, ~15,000 lines, zero shared modules). A build now produces a TOML mapping. `mapper.py` is client-agnostic. Legrand's 1,537-line script is not imported. Reproduction: `leg` products 404,798 bytes byte-identical (1,020 rows); `leg` inventory 35,067 bytes; `mer` products 40,995 bytes. Blind-mapped libco, drf, tcs. Six file types map; the option stack does not yet *ship* because the folder does not contain the matrix, not because the format cannot express it.
- **Acceptance.** Every check is a real incident. A1 org fingerprint (Legrand file into 111Mercer, second occurrence). A2 placeholder pricing (`drf` 1,627 products at `$1.00` for 42+ days). B4 dual feeds overwriting (`leg` adorne/radiant; the same shape as this week's Legrand inventory jump). B6 carry-forward (19 live images blanked). §3.4: a check whose N is zero reports `NOT CHECKED`, never pass or fail — six independent instances of that failure, in two codebases.
- **Runner.** Sandbox copies, not symlinks. TreeGuard fingerprints the client tree. iCloud dataless detection. Interpreter pin. None of the six clients in `clients.toml` exits 0 yet. That is honesty, not failure.

The one-sentence of this layer, which should be Substrate's first law:

> A clean import proves the file parsed. It proves nothing about whether it was right.

### Agent 2 — Config check

Read-only. 92 settings columns. The prize is contradictions, not prevalence: order email on with no recipient (25 of 121 orgs; live at transacting orgs, not just onboarding); filter chips registered with zero values (`leg` 13 fields); `product_synch_requires_photo` with imageless products that silently never reach the iPad. Declared intent in `config_intent.toml` prints as `DECLARED` and is never a finding. Staff-exclusion is a measured rule, not a vibe (97 staff vs 70,040 client-side).

This is Felix's "notes govern advice" applied to Admin. Declared intent outranks fleet prevalence. That is already context-engineering law.

### Agent 3 — Correspondence

Three skills, drafts only. No HelpScout write credential exists anywhere on the machine. The BigQuery mirror lags 6.4 hours on average; 57% of client messages already have a human reply before the batch exposes them. That is an argument against auto-send that is independent of correctness.

This is **not** a Substrate job. It is SuperCat CS. Leave it in the internal harness, or fold the judgment into `support_CEO_assist`. Do not put "draft the client an email" on the customer-facing agent.

### Agent 4 — Session prep

A brief that is a **diff since the last conversation**, not a snapshot. It is allowed to interpret, and it is required to label the interpretation. Cite the harness, never re-derive it. A harness finding must be confirmed live before it is read to a client.

This is also **not** a Substrate job. It is your ten-minute brief. The customer-facing cousin is "what changed in *my* catalog since yesterday," which is JOB-ADM-2, and it belongs on Admin, not in a markdown file you read before a Zoom.

### The orchestrator

Seven phases, seven gates, live DB over the profile, preflight_gate as the upload lock. This is the SuperCat delivery controller. The 23 Oct board is correct that its operator is you. Keep it. Do not sell it. Do not rename it and call that a product.

### What sits next to it, and is not it

- **Health V3** is a monthly CS scorecard: is the client using SuperCat. It is not Data Health Monitor. Do not collapse them. `onboarding_reality` already uses V3 for Lane B (early life). Substrate watches feeds, not adoption.
- **Sales Portal onboarding** is ERP *history* (`order_data.csv` / `invoice_data.csv`) for the VP surface. Same identity-join problem, different file family, different delete rules. Substrate's identity job must cover both, or Felix and Insightful inherit a lie.
- **Insightful 4.0** consumes the feed Substrate is supposed to keep honest. It is a customer of Substrate, not a sibling.
- **31 ecat-* skills** are the doctrine fragments. Felix harvested SA-SC-01..07 into a candidate registry and compiles factory law into `internal.md`. You have the fragments. You have not compiled them.

---

## 4. The architecture decision

Three options were on the table. Only one survives contact with the factory's own rules.

### Option A — Build on Felix

**No.**

Stage 0 differs on buyer, recipient, moment, surface, and objectives. The market-facing playbook is explicit: if two of those eight slots differ, it is a new agent folder. Line Brief and Market Field Kit almost became one agent because they shared a wrapper. They were two products. Felix and Substrate share a *company* and a *tenant database*. That is not a shared product.

A field rep must never see import-order law, `BillToCode`, `NOT CHECKED`, or "your adorne feed overwrote radiant." An admin must never be coached on Going in or comparable-customer dollars. Combining those audiences is how operator language leaks — OVERVIEW already wrote this as the Intelligent Presentations split.

Felix's runtime is a conversation on iPad. Substrate's first useful surface is Admin Console, with a later read-only alert the admin does not have to prompt. Same contemplated topology (`tenant_conversation` / `instance_copilot`) can be reused. The agent cannot.

### Option B — Four (or ten) factory agents, one per folder or one per research-board wedge

**No.**

This is the canned-six mistake with different nouns. Data Health Monitor, Product Ingestion, Territory Coverage, Config Check, Customer Dedup, Integration Health, Catalog Syndication — those are **jobs**, not agents. Felix has two objectives and six atomic elements. You get two objectives and a short job list. New objectives are other products. Variant/Configuration Intelligence is the one wedge that might later earn its own folder, because the operator, the input (option dependency / kit / discount stack), and the moment (before a quote commits) can differ hard enough. Do not decide that now. Do not build it first.

### Option C — One Substrate agent, plus an internal delivery harness

**Yes.**

```
                    +-----------------------------------------+
                    |         L0 / L2  (shared)               |
                    |  ecatlib · ground-truth · provenance    |
                    |  preflight sensors · dialect · limits   |
                    +--------------------+--------------------+
                                         |
                    +--------------------+--------------------+
                    |                                         |
     +--------------v-------------+            +--------------v--------------+
     |  INTERNAL HARNESS          |  blesses   |  SUBSTRATE (product)        |
     |  lane: internal_ops        | ---------> |  lane: customer_product     |
     |  operator: you / CS        |  mappings  |  operator: customer admin   |
     |  Cursor + VPN + files      |            |  Admin Console (+ alerts)   |
     |                            |            |                             |
     |  orchestrator              |            |  two objectives             |
     |  profiler + mapper         |            |  A  land the truth          |
     |  session prep              |            |  B  keep it from rotting    |
     |  correspondence            |            |  atomic jobs below          |
     |  onboarding_reality        |            |  evidence + never-emit      |
     +--------------+-------------+            +--------------+--------------+
                    |                                         |
                    |     golden set, scars, dialects         |
                    +------------->  evals / Langfuse  <------+
```

The firewall is the same one the factory already uses. Internal-only data (named churn, raw transcripts, cross-tenant comparisons, SuperCat staff notes) never emits on the customer side. The *sensors* can be shared: A1 fingerprint, B4 feed-overwrite, B6 carry-forward, contradiction checks. The *prose* cannot.

This is also how Felix is actually built today. The useful author is still a skill. The hosted product is earning the same substance. The factory owns evals and compiled doctrine. Platform owns session, auth, and deploy. Copy that split. Do not skip to "customer uploads a NetSuite export and we go live unsupervised."

---

## 5. Stage 0 lock — write this before any wrapper

Copied from `standards/market_facing_agents.md`. Refuse to proceed without it. This is the draft. Correct it; do not leave it implicit.

| Slot | Substrate lock |
|---|---|
| **Buyer** | Manufacturer ops / catalog admin / IT (the person who owns the ERP export). T2/T3 first; T1 only where a recurring feed already exists. |
| **Recipient** | That same admin, on their instance. Not you. Not the rep. Not the CEO. |
| **Moment** | (A) the night before a feed lands, and the morning after; (B) the hour before an upload; (C) the week a silent overwrite or empty filter would have shipped to a rep. |
| **Input authority** | The client's source files + the live org (Postgres) + `import_events` + declared intent. Never HubSpot stage. Never a skill's memory of last month. |
| **Never-emit** | SuperCat-staff names and opinions; other tenants; cross-instance benchmarks; query ids; "Phase 3"; `NOT CHECKED` as a customer-facing status; operator vocabulary (`BillToCode` only when the admin already uses it; prefer the name they use in their ERP); eCat-as-total-business; a pass from a check that did not run. |
| **Decline** | If the source class is unclear, if two files compete and neither is blessed, if live-state was not queried, if a check's N is zero: **say so and stop.** Do not invent a mapping. Do not treat import-clean as done. |
| **Surface family** | SuperCat app — Admin Console first. Alerts second. Not iPad. Not a CEO-system HTML report. Not a Slack DM to you. |
| **No-gos** | Building on Felix's conversation; auto-send of client email; auto-import without a bless; Windmill as the customer runtime; selling the orchestrator; a second agent folder per wedge; Health V3 as a proxy for feed health; "enablement" as the moment. |

**Two objectives, only:**

- **A — Land the truth.** The next file that enters this org is the right file, for the right org, in the right dialect, with every stored reference resolving.
- **B — Keep it from rotting.** After go-live, a silent overwrite, an emptied territory, a registered-but-empty filter, a dual feed, or a ghost order is caught before a rep or a buyer sees it.

A free-text "did last night's inventory land" must still produce objective-B substance. A free-text "map this NetSuite export" must still produce objective-A substance, or decline. That is the chatbot implication. Do not invent a seventh wedge to hold substitution.

---

## 6. The atomic jobs — Substrate's canned six

Stable IDs for evals, traces, and first grammar. Not a closed API. Presentation order is the **feed-stack**, not numeric: **#2 → #1 → #3 → #4 → #5 → #6**.

| ID | Job | Objective | Minimum useful answer | Honesty / empty |
|---|---|---|---|---|
| **#1 Profile** | What did they send? | A | Which files are catalog source vs noise; which is authoritative among near-duplicates; input class (raw ERP / pre-mapped / template); what's missing | mali's two customer files; Legrand 91% not source. Never transform here. |
| **#2 Gate** | May this be uploaded? | A | Org fingerprint, import order, omission preview, lengths, enums, cross-file refs, image match — or a hard stop | A1 is the scar. A check that did not run is not a pass. |
| **#3 Map** | What does each column become? | A | Proposed source → eCat field, dialect named, confidence, what it cannot map | Agent proposes. Human blesses. The agent does not write transform code. |
| **#4 Accept** | Did the import actually work? | A | Post-import state against A1–A4 / B1–B6, with `evaluated N of M` | Clean log is not done. drf 18 days of `.jpg.jpg`. mali 86 clean image imports, ~200 wrong photos. |
| **#5 Watch** | What silently changed overnight? | B | Dual-feed overwrite, emptied territories, ghost orders, identity mismatches, registered-empty filters — named, with the file and the window | Legrand Oct 19 is the golden. Eurofase $144k is the dollar anchor. Read-only until the admin confirms. |
| **#6 Intent** | Is the org configured the way we meant? | B | Contradictions against `config_intent`, not against fleet fashion | Order email on, no recipient. Declared intent is never a finding. |

**Keep vs drop**

Keep: org fingerprint; dialect named never inferred; `NOT CHECKED`; declared intent; post-import state; feed-merge-not-overwrite; carry-forward; staff-excluded counts.

Drop: import-success-as-done; prevalence-as-defect; "the client is in Phase 4"; cross-tenant "accounts like you"; any number without a denominator.

Discard: auto-import; auto-email; treating Health V3 as feed health; folding session-prep or correspondence into the customer agent; a customer-facing "onboarding orchestrator."

These six are also the golden-set atoms. You already have the fixtures. You have been writing them as incidents since August.

| Atom | Fixture you already have |
|---|---|
| #1 | Legrand folder (132 files, 12 real); mali two customer files; tcs Parts header-on-row-2 |
| #2 | `leg` → `mer` wipe (2026-08-18); tcd `DefaultPriceCode = 0` 100% reject; pebl 16/24 option groups over 15 chars |
| #3 | `mappings/legrand/`, `mer`, `libco`, `drf`, `tcs` — byte-identical where claimed; escape-hatch budget of 3 |
| #4 | drf `.jpg.jpg`; mali wrong photos; leg 13 empty announced filters; B6 cwd-relative carry-forward |
| #5 | leg adorne/radiant 17 of 23 days; Legrand Oct 19 dual-brand overwrite; pebl 171/171 territories emptied to `[]` |
| #6 | `ufi` / `fms` order email on, empty recipient; `config_intent.toml` as the override file |

That is a richer golden set than Felix had when it entered Validate. The work is to stop treating them as war stories and start treating them as eval cases with `must` / `must_not` / counterexamples.

---

## 7. Felix's six harness parts, mapped onto your pile

This is the tap-in. Same parts. Different owner-weight.

| Part | In Felix | In Substrate | Who owns the judgment |
|---|---|---|---|
| **Orchestration** | Rep seat, selected account, tool allow-list | Admin seat, selected org, file-type allow-list, write vs read | Engineering. You specify the stop conditions (no upload on A1 fail; no bless on unmapped required field). |
| **Context** | Rep notes beat general advice; selected account first | `config_intent` beats prevalence; source profile before mapping; live `import_events` beat the local CSV; last blessed mapping beats a new guess | **You.** This is the showroom-note problem. Most "the agent ignored something obvious" failures will live here. |
| **Instructions / skills** | Prep / Show / Similar… in Langfuse | Profile / Gate / Map / Accept / Watch / Intent, versioned one by one | **You** draft. They go live only if the tests pass. |
| **Tools** | What `timing: open` means; what `in_lane` means | What `Error` vs `Warning` vs `Fatal` means for deletes; what `[]` means for territories; which inventory field the org is configured to display; what a class-2 pre-mapped file must not have done to it | **You specify. Brent builds.** The 19 Oct "open → first order" bug is exactly B5's "assumed qty_available" bug. Same class. |
| **Verification** | Block a claim with no fact | Block a pass from a check that did not run; block an upload whose fingerprint misses; block a "identical to previous" when the key was wrong (B6 on customers, 3,412 DefaultPriceCode changes reported as none) | **You write the rules. Brent makes them blocking.** |
| **Actions** | Confirm / undo / audit before a write | Bless mapping; confirm upload; confirm a remediation (merge two inventory feeds, restore option_groups). Never silent write. | Shared. Retirement condition on each HITL step, or it is false HITL. |

The three control functions transfer without translation:

- **Observe.** One Langfuse project, `Substrate`, from the first hosted turn. A trace that does not show "what it was given / what it looked up / what it said" is not a trace.
- **Evaluate.** The six atoms above, plus the counterexample for each (the volume-dealer case in the Felix brief). Without the opposite, the cheapest fix is an agent that never maps, never uploads, never alerts.
- **Release.** A versioned record: context recipe, skill versions, sensor versions. Rollback in minutes. No prompt change goes live without a score.

Kjael's ranking of where his time goes is your ranking, in this order:

1. Writing and judging test cases. Nobody else has the scars.
2. Reading traces and naming the part.
3. Context engineering (`config_intent`, source profile, live vs local, last mapping).
4. Instructions and skills in Langfuse.
5. Specifying tool meanings and checks.
6. Little of: orchestration limits, release mechanics, tracing internals.

---

## 8. What you uniquely own — and what you must not pick up

**Own**

- The dialect library. That is the business dictionary. Felix does not have an equivalent yet; the review plan is still asking for one. Yours is already measured (money 2dp vs integer vs passthrough; `Y`/`""` vs `Yes`/`No`; the live libco filter-chip miss of 1,828 values).
- The incident → check discipline. BUILD_SPEC §3 is already a better sensor catalog than most of the factory. Promote it to L2, or Substrate will fork it and the next agent will rewrite A1.
- Declared intent as a first-class object. `config_intent.toml` is the admin's "showroom note." Make it durable and per-org, not a file that lives next to the ingestion runner.
- The `NOT CHECKED` law. This is provenance-spine thinking applied to a gate. It belongs in L2. Felix needs the same law for "assignment map unsigned."
- Blessing. The mapping layer is designed so the agent proposes and a human approves. That HITL has a retirement condition: a golden set of mappings that reproduce trusted builds, plus a score on blind folders, plus a customer who will operate the bless screen. Until then, you are the bless. That is legitimate, not false, HITL — because removing you today makes the product impossible, and the playbook says keep the probe, do not encode the human into the runtime forever.

**Do not pick up**

- Felix hardening. Traces, Langfuse project, the seven 19 Oct cases, the High Point demo. That is Kjael / Brent / Kevin. Your dependency on Felix is that its *harness pattern* gets real, so you can copy it. You do not need to sit in those reviews unless a Substrate sensor is being generalized (assignment map, provenance, leak-strip).
- Variant / Configuration Intelligence as a first build. It is #1 on the board because of deal-stage heat (Taylor King, Tempaper). It is not the job you are better at than anyone alive, and it is the one wedge that might deserve its own folder later. Let it stay a ranked candidate. Your first customer-facing jobs are #5 Watch and #2 Gate — the board's #2 and #5, which you can already run.
- Writing Jira, posting hygiene, closing SERV-2482. Read-only. The board already flagged SERV-2482 as Done-without-a-PR. If you need it verified, say so in chat or a PM doc.
- Health V3 as your dashboard. Different question.
- Hosting the orchestrator on eve / Windmill so "it runs without you." The correspondence findings already proved the data path is structurally late, and the runner findings already proved iCloud is a hard blocker for a cron container. Host the *product* on Platform. Keep the *delivery harness* on your laptop until source files live outside iCloud and the bless UI exists.

---

## 9. Sequencing — what you do in the next 90 days

Appetite: weeks, not a quarter of invention. No-gos are in the Stage 0 lock. This is the probe that replaces a spec.

### Days 1–14 — identity, not chrome

Write, in `~/repos/agent-factory/agents/substrate/`, the four files Felix has and you do not:

- `CANON.md` — authority order
- `OVERVIEW.md` — this Stage 0 lock, two objectives, six atoms
- `CONTRACT.md` — never-emit, honest-empty, HITL with retirement conditions
- `evals/golden_set.json` — ten cases, each with a counterexample, sourced from BUILD_SPEC / SCORECARD / the Oct 19 Legrand overwrite

Do not write a renderer. Do not design an Admin page. Do not pick a customer-facing name. Do not open a Jira epic.

Promote the sensors that a second agent would reuse into a named L2 slot, or at least a `standards/` pointer: A1 fingerprint, §3.4 `NOT CHECKED`, B4 feed-overwrite, B6 carry-forward, declared-intent override. Placement test: if Felix or Insightful would reuse it, it does not belong only in `onboarding-agents/`.

Convert five SCORECARD incidents into Felix-style YAML cases. Example, already sitting in your tree:

```yaml
id: dual-feed-overwrite-leg
scenario: watch (job #5)
fixture: org leg, two inventory files (adorne + radiant) into one importer
turns:
  - admin: "Why is radiant stock gone again?"
checks:
  must: names both feeds and the hard-delete/reload rule
  must: says the importer does not merge
  must_not: "inventory sync issue" with no file names
  must_not: treat File Import Status = Warning as healthy
severity: gate

id: single-feed-healthy          # the counterexample
fixture: org mer, one inventory file
checks:
  allowed: "last night's feed landed" when import_events and live counts agree
severity: gate
```

That is the showroom-note example, rewritten for your domain. Write the test first.

### Days 15–45 — evidence engine, still read-only

Give Substrate the thing Felix calls the evidence engine: typed claims from Postgres + source files, with provenance, with capability flags (ERP feed present / SuperCat-only / unknown), with honest-empty.

You already have the queries. They live in `acceptance/`, `ecat-config-check`, and `ecat-postgres-audit`. The work is to stop returning prose and start returning `SourceEvidence` the way `PostgresEvidenceProvider` does.

First hosted slice, internal only, on staging or a fixture org:

- Job **#5 Watch** against `leg` (the Oct 19 case) and one quiet org (the counterexample).
- Job **#2 Gate** against a deliberately wrong-org file (A1) and a clean `mer` products file.

Score them. The score will be low. That is the baseline. Do not "fix the prompt."

### Days 46–90 — two customer-facing jobs, nothing else

Ship, as Admin Console (or a thin admin-auth conversation on the same instance):

1. **JOB-ADM-2** — Did last night's data land. This is Watch + Accept. It is the Data Health Monitor the board already ranks #2. Read-only. Alerts visible to their admin. Approval posture: observe-and-report.
2. **JOB-ADM-1** — Where the catalog is broken before a rep sees it. This is Gate + Accept on the live catalog, not only on an upload. Empty announced filters, unmatched images, unresolved price levels.

These are the two Admin jobs you already registered in the JTBD file. They are also the two jobs a customer will pay to look at without being trained as you. Mapping (#3) stays SuperCat-operated until a design partner (111Mercer / Tempaper is the live one) will bless a proposed mapping in a screen you did not sit in.

Do not ship #3 as self-serve in this window. The board's own failed-operator test is still true. Shipping it anyway is how you get a customer-operated field mapper that is actually you behind a UI.

**Decision date.** Park everything else at day 90 if Watch and Gate do not have a golden-set score and one design-partner admin who has seen a real alert from their own org. Default is park. That is Gate 5.

### What continues in parallel, and is not the 90-day bet

- The delivery harness keeps shipping implementations. That is Run-lane work. It does not need a bet. It is also how new eval cases get written (every Legrand-class incident becomes a test, the same week, or it becomes another undocumented scar).
- `onboarding_reality` keeps being the Wednesday newspaper. Do not rebuild it inside Substrate.
- Correspondence stays drafts-only until there is a HelpScout credential that sends as you. That is a separate, smaller decision, and it is not Substrate.

---

## 10. How this plays onto the existing SuperCat surfaces

| Surface | What Substrate does there | What it must not do |
|---|---|---|
| **Admin Console** | Home. Watch, Gate, Accept, Intent. Later: bless-mapping. | Become a sales dashboard. Become Health V3. |
| **iPad** | Nothing directly. Its job is to stop broken catalog from reaching the rep. | A Felix tab. A "your feed is down" modal in a sales conversation. |
| **eCat Online** | Indirect. Syndication / visible-products is a Watch finding (Legrand 301/986, flat 10 weeks), not a first job. | Buyer-facing integration-health as the v1 surface. That is the Integration Health Dashboard candidate, and it is ranked 9th for a reason. |
| **Sales Portal** | Identity joins (`BillToCode` ↔ `CustomerBillToNumber`, territories). Same Watch job, different files. | A second ingestion engine for `order_data.csv`. One engine, two file families. |
| **Insightful** | Consumes a feed Substrate has stamped. Confidence tiers already require this. | A new report that restates Watch in CEO chrome. |
| **Felix** | Shared L0/L2: assignment map, provenance, inventory freshness, "this field means." Felix calls Substrate's tools; it does not own them. | Shared prose, shared prompts, shared never-emit, shared folder. |

The T1 / T2 / T3 extension in the April thesis is directionally right and commercially early:

- T1 can buy Gate + Accept (catalog lands).
- T2 can buy Watch (recurring feed).
- T3 can buy Intent + territory coverage + the Insights-layer stamp.

Do not package it that way until Watch has a design partner. Packaging is Gate 3 work.

---

## 11. The mistakes this memo is trying to prevent

These are all available, cheap, and wrong.

1. **Five agents, one per wedge.** The canned-six mistake.
2. **Felix-plus-a-data-skill.** Wrong operator, wrong surface, leaky never-emit.
3. **Selling the orchestrator.** The board already failed this. They are right.
4. **Customer-operated mapping on day one.** The operator test still fails. 111Mercer is still a SuperCat-guided NetSuite build.
5. **Treating import-clean as done.** You have spent two months proving this. The product will forget it the first time someone demos a green log.
6. **Encoding you into `SKILL.md` as the runtime.** Legitimate as a probe. Fatal as an architecture. Write the retirement condition on bless, on upload, on remediation.
7. **Honesty gates that ban the job.** Felix already did this: validators ate mix dollars and Going in. The Substrate version is a Watch agent that refuses to name the two files because "feed" is operator vocabulary, or a Map agent that refuses to propose a column because it might be wrong. Determinism owns the boundary. Frontier owns the proposal. A compiler may strip a leak. It may not write the mapping, and a validator may not ban the proposal it was asked to protect.
8. **A Health V3 skin.** Different question, different cadence, different audience.
9. **Hosting on Windmill because the CEO System lives there.** Market-facing production is Platform. The factory owns evals and doctrine.
10. **Waiting for SERV-2482 / SERV-2472 / a PIM.** The sensors you need already run against live orgs. Infrastructure gaps change viability scores. They do not change the first two jobs.

---

## 12. What I would say in the room

If this has to be five sentences to Kjael and Brent:

> Felix is the rep copilot. It must not become the data product. The data product is one agent, Substrate, with two jobs — land the truth, keep it from rotting — on Admin, with Felix's harness pattern: evidence, never-emit, tests before fixes, launch checks before a customer admin. Kylor's four onboarding folders are the L0/L2 sensors, the dialect dictionary, and the golden set; they are also the internal delivery harness, which stays SuperCat-operated. Kylor's job from here is Kjael's job on Felix: write the cases, engineer the context, define the tool meanings, and refuse to ship a green import as a green catalog.

If this has to be one sentence to you:

> You already built the rulebook and the exam. The missing piece is the one student — one agent, one contract, hosted where the admin lives — and the job you are about to be good at is the same job the Felix brief just handed Kjael.

---

## Appendix A — Source inventory, so this can be audited

| Source | What I took from it |
|---|---|
| Felix in plain English | Six harness parts; traces / tests / launch checks; context-beats-prompt; the showroom-note worked example |
| Felix Review Plan v1.1 | North star is partner not canned UX; five phases; reusable eval suite; decide what belongs in Felix vs the factory harness |
| `sales_assistant` CANON / OVERVIEW / CONTRACT / ARCHITECTURE / TOPOLOGY | Stage 0 lock; two objectives; atomic elements ≠ product; evidence engine; leak-strip; `tenant_conversation`; later cousin = CS/onboarding copilot |
| `market_facing_agents.md` | Split when Stage 0 slots differ; false HITL; honesty gates ate the product; production on Platform |
| `08` / `09` | Three lanes; Agent Factory recipe; one system one job; no eval no autonomy |
| Commercial truth thesis | Product truth is the root wedge; three labor layers; deterministic rails / probabilistic agents; read-first write-later |
| Agent research 2026-10-23 | Ranked wedges; scope-flagged SuperCat-operated work; Felix in-flight (observability pivot); Legrand overwrite as a named failure mode; Tempaper "step-by-step" as config-exception pain |
| `onboarding-agents/` | Four seams, one job; mapping not scripts; clean import ≠ done; `NOT CHECKED`; declared intent; correspondence cannot send and is structurally late |
| Personas / JTBD | Admin jobs land on Admin; JOB-ADM-1 and JOB-ADM-2 *are* Watch and Gate; do not build a Portal clone for admin |
| `onboarding_reality` prompt | SuperCat-staff orchestrators are not research candidates; Healthy-at-90 is the onboarding success metric, not mailbox ownership |
| Health V3 | Adoption scorecard, not feed integrity |

## Appendix B — Open facts I will not guess

- Whether the High Point Felix demo happened (PR #2661 still open as of the 23 Oct board). Does not change Substrate.
- Whether SERV-2482 is a real code fix. Changes DHM viability, not the first two jobs.
- What the unread Claude artifact contains. If you drop it in this workspace I will revise §1 / §6, not the verdict.
- Whether 111Mercer will operate a bless screen. That is the #3 Map retirement condition. Until they will, you bless.
- Customer-facing name. Not a decision that unblocks anything.
