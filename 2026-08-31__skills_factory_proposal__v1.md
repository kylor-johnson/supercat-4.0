# From Agent Factory to Skills Factory

**A proposal — 2026-08-31**
Read-only review of `SuperCat 4.0/` (local) and `SuperCatSolutionsLLC/agent-factory` (GitHub).

---

## The short version

The Agent Factory is a good model that picked the wrong unit. It builds **agents** — each one a bundle of judgment, procedure, data access, and rendering, promoted through its own lifecycle with its own eval set. Eleven of them now exist in the repo.

Only one of those four ingredients is scarce. Judgment is the asset. Procedure is a checklist, data access is a query, rendering is a template — all three are near-free now and getting cheaper. Bundling the scarce thing inside eleven separate agents means it can only be used eleven specific ways.

A **skills factory** inverts it. The unit of production is a skill: a portable piece of judgment with a trigger, a refusal, and a proof. Agents become thin shells that pick up skills and run.

Skills are an open standard now — one file, every tool, shareable across a team. So the question is no longer how to package judgment. It is whose judgment ends up on the shelf, and whether their name is on it.

You already have twenty-four skills driving real client work, portable across two harnesses. You built the thing. It just isn't named, isn't versioned where anyone can see it, and isn't the org's stated model.

This proposes naming it, and gives the first ten skills to extract.

---

## 1. What the Agent Factory actually is

Worth being precise, because the answer changes what to propose.

It is not Kevin's invention and it is not SuperCat's. It is a **Touchstone / Skaling Ventures operating model**, dated 2026-07-09, owner "CEO + CTO," canonical source a Notion page. Your own `foundation/09_agent_factory.md` says so in its header: *"This file is a rendering mirror, not a second source of truth... Where the two disagree, Notion wins."*

Its bones, stripped down:

| Piece | What it says |
|---|---|
| **L0–L4 layer stack** | Sort assets by shared vs. agent-specific. "If a second agent would reuse it, it belongs in L0–L2." |
| **Lane** | A firewall, not a folder. Internal-ops / customer-product / shared, with an outbound denylist. |
| **Four topologies** | Scheduled report · operator skill · outbound automation · MCP tool-server. Each ships a default bundle of guides + sensors. |
| **The stack** | GitHub = truth, Windmill = control room, Kubernetes = floor, Langfuse = flight recorder. One system, one job. |
| **One quality bar** | Same bar both lanes; only intake differs. |
| **The ladder** | Sandbox → read-only → notify → approve → autonomous. No golden set, no autonomy. |

The philosophy underneath is sound and worth keeping: **a factory is variety reduction.** Commit to a few repeatable patterns so quality is engineered once instead of hand-built per agent. And: **agent = model + harness**; the model is commodity, the harness is the leverage.

Two of its principles matter most for what follows:

> **One system, one job.** Never let two systems quietly become the source of truth for the same thing.

> **Rules cite their scar.** Add governance only in response to a specific failure.

Hold onto both. They are about to indict the current arrangement.

---

## 2. Where the model already broke its own rule

The repo has 400 commits and eleven agents. It also has one folder that does not fit the model at all: `standards/doctrine/` — seven skills that are **not agents**, are loaded by multiple agents, and are compiled to three different consumers off an allow-list.

That folder is six weeks old and is the smallest thing in the repo. It is also the only part that treats judgment as a portable object rather than as something trapped inside an agent.

It got built because the agent unit stopped working. Once you have eleven agents, the same rule — *don't name another rep's account, don't imply MSRP from a net price column, don't fill a slot from the nearest available material* — has to be written eleven times or centralized once. Doctrine is what centralizing it looks like.

So the skills factory is not a departure from the Agent Factory. It is the direction the Agent Factory already started moving under load. The proposal is to finish the move deliberately instead of letting it accrete one folder at a time.

---

## 3. Why the agent is the wrong unit now

Plain English, four reasons.

**An agent bundles four things; only one is scarce.** Judgment (what's true, what to refuse, what to suppress), procedure (do this, then this), access (a query, an API), rendering (an HTML template). Judgment took years and real scars. The other three are close to free now.

**Eleven agents is variety, not variety reduction.** Each carries its own L3 doctrine folder, its own golden set, its own renderers. The factory doc says a factory exists to prevent exactly this. The doctrine folder is the correction, applied to seven rules out of hundreds.

**Skills are a standard now; agents are not.** One skill file loads into Claude Code, Cursor, the API, the desktop app, and a Windmill job unchanged — and teams can share one set. Your twenty-four are already byte-identical copies across two harnesses. Portability stopped being a design goal and became a property of the file format. There is nothing equivalent for an agent.

A consequence worth naming: `standards/doctrine/compile.py` concatenates allow-listed skills into three generated files under `context/doctrine_runtime/`, which agents then `read_file`. That is a bespoke distribution format for something that already has an open one. Reasonable in August; a maintenance liability now, and the main thing standing between that shelf and anyone outside the repo using it.

**A skill is a thing anyone can pick up; an agent is a thing someone has to run.** That is the whole argument. An agent requires an owner, a schedule, a promotion path, and a container. A skill requires a trigger and a reader. When you want the knowledge in a new place, one of those is a project and the other is a copy.

The shift, side by side:

| | Agent factory | Skills factory |
|---|---|---|
| Unit of production | An agent | A skill |
| What you version | A pipeline | A judgment |
| How it spreads | Build another agent | Another agent loads it |
| Proof of quality | The agent's golden set | The skill's own trip fixture |
| What an agent becomes | The product | A thin shell: pick skills, run |
| Cost of a new use case | A promotion cycle | A line in a manifest |

Keep every bone that still works: the lane firewall, the shared quality bar, "no eval no autonomy," "one system one job," "rules cite their scar." Change the noun.

---

## 4. The factory was built at the wrong end

The setup order that actually works, and why:

| # | Layer | Why it comes first |
|---|---|---|
| 1 | Memory and context | Everything downstream reads from it |
| 2 | Projects | A place, not a chat. Holds context and files per job |
| 3 | Skills | A project holds context; a skill holds a *method* |
| 4 | Connectors | A skill without access to your tools is just text |
| 5 | Automation | Last, once you know the thing works |

> Skip to automation and you get a schedule that produces something wrong every morning at eight.

The Agent Factory starts at layer five. Windmill schedules, Kubernetes containers, a Langfuse improvement loop, a promotion ladder — excellent infrastructure for running things on a timer. The skills layer underneath it is six weeks old and contains seven files.

That is a diagnosis of where the next investment goes, not a criticism of the build order. The scheduling is solved. The method layer is barely started. And the method layer is the part that is yours.

One more thing the order implies, and it is the sharpest test in the model: **a skill is written by doing the work twice, then writing down what you actually did.** Skills written from imagination are guesses about your own process. The repo's seven were extracted from a single craft packet on a single day. Yours came out of nine client builds, 104 scored orgs, and 23 dated cohort runs. That difference is the whole argument for whose shelf should be canonical.

---

## 5. You already run one

This is the part that should reframe the whole conversation. Read-only review of `SuperCat 4.0/` found a working skills factory that nobody named:

| Asset | Scale | What it is |
|---|---|---|
| Skills | **24** | eCat build/runtime, reporting, engineering, company context — each with a trigger-bearing description and a routing contract |
| Always-on rules | **8** | Import ground truth, data model, Jira read-only, canvas ban, legacy freeze |
| Live client workspaces | **9** | `drf` `leg` `libco` `mali` `pebl` `tcd` `tcs` + Fine Art + template, keyed by org shortname |
| Insightful Product 4.0 | **188 md files** | Precedence chain, reading contract, provenance spine, 5,613-line query library, 763-line editorial ruleset, 16 client profiles |
| Onboarding phase framework | **v3.6** | 7-phase lifecycle, flag taxonomy, output contract, HTML artifact contract, 23 dated cohort runs |
| Client health model | **v3.2.13** | Four equal dimensions, two overrides, run across 104 orgs, 731-line operating spec |
| Segmentation | **v4.0** | 109-row roster, stamped, corrected through three post-stamp rounds |
| Foundation | **10 docs + sources** | Company context with a stated precedence: on conflict, the stamped source wins |

And the discipline is already there. The factory constitution *asserts* "rules cite their scar." Your phase framework **practices** it — every version bump from 3.0 to 3.6 names the run that broke it:

- v3.6 — validated against a blind reconstruction of TCD built only from raw transcripts and the live DB by an agent barred from reading any interpretation doc. Both backtestable transitions matched exactly. Three fixes fell out, including a schema error that had been throwing `UndefinedColumn` on every Phase 7 evaluation — the framework could never complete a run.
- v3.5 — thread-count floor of 5 after TCD's Phase 7 clause fired at 100% on a denominator of 2.
- v3.4 — flag codes banned from the client-facing body after ALL-CAPS internal codes leaked into standup tables.

That is a better changelog than the repo's, and it is sitting in iCloud where it has no timestamp anyone else can see.

---

## 6. The proposal

Five moves. Deliberately small — the failure mode here is building a governance apparatus instead of shipping the shelf.

### 6.1 One shelf, one home

Skills currently live in three places as **manual copies**: `.cursor/skills/` (22), `~/.claude/skills/` (22 independent copies), `.claude/skills/` (2). Your own AGENTS.md warns: *"these are copies, not symlinks — when you edit one, update both or they drift."*

That is a direct violation of the factory's own principle 7. Pick one home, put it in git, generate the rest. This is a half-day and it is the single highest-value move on the list.

### 6.2 The unit is a skill, in the standard shape

A good skill names five things: **when to use it**, **what it needs from you**, **the steps**, **what the output should look like**, and **what it must never do**. Missing the last two is why most skills produce something almost right.

You don't have to invent that form. The doctrine folder already runs it — *When · Inputs · Steps · Outputs · Hard rules* — plus *Empty / fail* and a *Proof this exists* fixture the shared runner executes. That is the community standard with a refusal path and a test bolted on, which is strictly better. Adopt it as-is and add one thing: a **refusal** — what to do when the evidence isn't there. A rule with no honest way to decline is a preference.

Nothing else goes in. Not the SQL, not the renderer, not the checklist. Those are runtime and they live in code.

### 6.3 Three shelves, and most things aren't skills

Sort every asset once:

| Shelf | Holds | Test |
|---|---|---|
| **Skill** | Judgment that constrains output | Would a competent stranger get this wrong? |
| **Context** | Facts, dated, expiring | Will this be wrong in a quarter? |
| **Runtime** | Queries, renderers, scripts | Is it code? |

Most of your corpus is context and runtime. That's fine and expected. The skills are the thin layer of refusals threaded through it — and that thin layer is the whole asset.

### 6.4 Publish, with provenance

Whoever commits first owns the canonical path and writes the provenance line. Right now that is always the other side, because your work only exists on a laptop and in iCloud.

Your material is already in his repo — `health_v3/FACTORY.md` says *"copied from Kylor's 2026-08-06 package"*; segmentation v4.0 says *"imported 2026-07-10... authored in a separate build project."* Both credited in a prose aside. Neither is authorship. None of the seven doctrine skills carry provenance pointing at your work.

The fix is not to withhold. It is to publish with your name on the provenance line, so the shared layer cites you instead of absorbing you.

### 6.5 Proof travels with the skill

Golden fixtures move from the agent to the skill. Each skill carries one pair: the artifact that gets it wrong, and the artifact that gets it right. That is what makes a skill safe to hand to someone else — and it is the same ship rule the doctrine folder already enforces.

---

## 7. The first ten skills

Extracted from what is already written down and already scarred. Law, where it lives, what taught it.

**1. `import-omission-law`**
A full file replaces that file's data — and what happens to the records you leave out differs per file. `customers.csv` hard-deletes every customer and ship-to, then reloads. `products.csv` soft-deletes. `stories.csv` nulls the story but keeps the product. Deletes only fire on an error-free import: any `Error` row and obsolete records silently stay.
*Source:* `CLAUDE.md` / `ecat-ground-truth.mdc`, verified against importer code.

**2. `kb-vs-code-truth`**
The knowledge base is not the importer. `TerritoryCodes` is KB-required and not importer-fatal. `QtyAvailable` likewise. `BaseItemCode` caps at 40, not the documented 20. SmartList item lists are newline-separated, not comma. Option codes allow 15/50, not 8/25. When the KB and the code disagree, the code wins and you say so.
*Source:* same, each line code-verified with a live org named.

**3. `provenance-spine`**
Every number carries a confidence tier and a completeness state. No bare numbers. Invoiced net is the revenue spine; `total_amount` is not the sales figure. Invoiced ≠ collected. Capture is a fact, attribution is a gated estimate — never present one as the other. A composite inherits the *lowest* confidence of its inputs, or it is suppressed.
*Source:* `Insightful Product 4.0/foundation/provenance_spine.md`.

**4. `rekeying-distortion`**
Almost no order flows straight from the iPad to the ERP. A human re-keys it. So the order→invoice join is effectively ~0%: never join eCat orders to invoices at row level, only at cohort/period grain. An eCat order is intent, not a transaction. What we see through our rails is structurally partial.
*Source:* same, §2. This one rule explains most of the wrong numbers anyone would otherwise produce.

**5. `health-score-honesty`**
Equal weights on purpose — we don't have the outcome data to weight, and gut-feel coefficients create false precision. No growth signals: health is current state, not opportunity. No trajectory scoring. Seasonality is flagged, not suppressed. And overrides cap downward because operational health can score green on infrastructure nobody is using.
*Source:* `Health V3 Backfill/METHODOLOGY.md` v3.2.13, 104-org run.

**6. `phase-gate-law`**
Anchor = the last *fully-Done* phase, evaluated contiguously; a failed lower phase blocks every higher one even when the higher one would pass alone. Phases are not a ratchet — an at-risk regression is a real state. Deduplicate HelpScout threads on normalized subject and require ≥5 before any ratio fires.
*Source:* `onboarding-models/`, v3.6, validated against a blind reconstruction.

**7. `ambiguity-is-output`**
Contradictions between signals get surfaced as flags, not smoothed. The standup decides; the agent doesn't. No metric without a tool call. Evidence is a verbatim quote with a source, or it isn't evidence.
*Source:* `onboarding-models/Flags_and_Signals.md`.

**8. `visibility-chain`**
"The server sent it" is not "the rep can select it." What a human sees is decided by user group × territory × `DefaultPriceCode` × distribution center. "Everyone disappeared from my customer list" is a configuration truth, not a bug.
*Source:* `ecat-ipad-app`, `ecat-go-live`, `ecat-pricing-levels`.

**9. `live-org-write-safety`**
Read first. Dry-run. One step at a time. Never report a write you did not confirm. Jira is read-only *because the MCP posts as you* — an agent-authored comment lands on a colleague's ticket under your name.
*Source:* `supercat-mcp-access`, `jira-read-only.mdc`.

**10. `plain-language-contract`**
No internal flag codes in a client-facing body, anywhere. Expand every acronym. Lead with what happened, not the machinery. The "no shit" test: if the reader already knew it, cut it. Never narrate the client's own business back to them.
*Source:* `Output_Contract.md` § Voice, `Insightful 4.0/knowledge/communication_guideline.md`.

Ten skills, all already written down, all already scarred, none of them in anyone's repo.

---

## 8. What not to build

The failure mode is governance theater. Explicitly out of scope:

- **No compiler until two consumers actually disagree.** The repo's allow-list machinery exists because three surfaces needed different subsets. You have one shelf and one reader. A `consumers.yml` right now is cosplay.
- **No skill for something a fresh agent gets right anyway.** If the model does it correctly without being told, it isn't a skill.
- **No procedure dressed as judgment.** Most of the eCat corpus is *how to build a file*. That's runtime. Only the refusals inside it are skills.
- **No competing constitution.** You don't need your own factory model. The L0–L4 / lane / topology frame is fine and it isn't the argument. You need your shelf inside it, with your name on it.
- **No new folder taxonomy before the first ten ship.** Sort as you extract.

---

## 9. Sequence

| # | Move | Done when |
|---|---|---|
| 1 | Collapse the three skill copies to one git-tracked home | One shelf; the other two are generated or gone |
| 2 | Get commit access and start committing | Your first commit exists in a repo someone else can read |
| 3 | Extract the ten skills above, each with a trigger, a refusal, and a paired fixture | Ten files, ten provenance lines with your name and a date |
| 4 | Retire the copies that drift; make the shelf the only source | Editing one file is the whole edit |
| 5 | Offer the shelf to the factory as a bound consumer | Their agents load your skills, citing you |

Steps 1–3 are the work. Steps 4–5 are consequences.

---

## 10. What I did and did not read

**Read in full:** the GitHub repo's doctrine folder (7 skills, `consumers.yml`, `compile.py`, `HELD.md`), the skill standard, ADR 001, the craft-layer inventory, the doctrine golden set, the repo commit history; and locally: `AGENTS.md`, `CLAUDE.md`, `WORKSPACE.md`, `foundation/09_agent_factory.md`, `Health V3 Backfill/METHODOLOGY.md`, `Insightful Product 4.0/CANON.md` and `provenance_spine.md`, `onboarding-models/Phase_Progression_Framework.md` and `Output_Contract.md`, plus directory-level inventory of every other folder.

**Sampled, not read line by line:** the 5,613-line query library, the 763-line editorial ruleset, the 731-line health spec, `PM/` (100 files), `eCat_Onboarding/` client workspaces (91 files), `Customer Intelligence/`, `EBR 2.0/`, `ttfv/`, `Peer Benchmark/`, `Pricing Migration/`, `reports/` (47), `kb-articles/`.

**Not opened:** `_archive/`, `scratch/`, `files 2/`, and the frozen Insightful 2.0/3.0 folders, per your own rules.

Nothing was modified. This was read-only throughout.

**On the source you sent:** three things from it are load-bearing here.

1. Skills follow an open standard — one file works across tools and a team can share one set. That is the argument for a shelf rather than a compiler.
2. A skill is written by doing the work twice and writing down what you actually did. Skills written from imagination are guesses about your own process.
3. The order is memory → projects → skills → connectors → automation, because a skill without access is just text, and automation on top of an unbuilt method layer is wrong output on a schedule.

Sections 3, 4 and 6 are built on those three points.
