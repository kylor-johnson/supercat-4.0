# 08 — How We Build

> **What this is**: SuperCat's product management and development operating model. It is
> the answer to four questions: *how does an idea become a bet, how does a bet become
> product, who is allowed to decide what, and how do we stop.*
>
> **Last updated**: 2026-07-30 · **Owner**: CEO + CTO · **Review cadence**: Quarterly, or when the capacity dial or the gates change
>
> **Status**: v1. This closes gap #2 in [`06_how_we_operate.md`](06_how_we_operate.md) —
> "decision rhythm at the human layer."
>
> **Companions**: [`07_how_we_establish_truth.md`](07_how_we_establish_truth.md) governs what we're allowed to
> claim. The **Touchstone Agent Factory Overview** governs how a commercializable agent is
> built and run. This doc governs what we choose to build and when we stop.

---

## Why this exists

Building software is no longer the expensive step.

For most of SuperCat's life, engineering capacity was the scarce resource, and every
process we inherited was designed to protect it. You wrote a specification because
building the wrong thing cost weeks. You held a planning meeting because a wrong
turn was expensive to reverse. You kept a backlog because demand exceeded supply by
an order of magnitude and something had to hold the queue.

That constraint has largely dissolved. A working prototype now costs hours. The
people closest to customers — sales, customer success, onboarding, the CEO — can
produce credible workflows, interfaces, and analyses without a handoff to
engineering. This is the single largest change to how this company operates, and
almost every process we would have adopted two years ago is now solving a problem
we no longer have.

But the hard parts did not move. Choosing the right problem is still hard. Knowing
whether the data is honest enough for the promise is still hard. Deciding what to
stop is still hard — and it got harder, because cheap building means more things
get started.

So the model is simple to state:

> **Decentralize invention. Centralize integrity.**

Anyone may find a problem, shape a bet, and build a prototype. Nobody needs
permission to do that. The company centrally protects a short list of things that
must stay coherent — what customers see, what our shared words mean, what we
commit production capacity to, what actually ships, and when we decide.

Five gates. Everything else is open.

---

## Who builds

| Person | Role | Lanes |
|---|---|---|
| Brent Sanders | CTO | Run, Platform, Agentic |
| Bruce White | Senior Engineer | Run, Platform |
| Kjael Skaalerud | CEO | Agentic |
| Kylor Johnson | Customer Success | Platform, Agentic |
| Kyla Bosch | Support & Adoption | Run, Platform |

Five people write code. Three of them have full-time jobs that are not engineering.
Every design choice in this document is sized to that reality — if a mechanism
needs a fifth person to work, it does not belong here yet.

**There is no product manager, and we are not hiring one.** Product management is
a set of jobs, not a person: finding the problem, shaping the bet, validating it,
deciding what ships, and deciding what dies. This document distributes those jobs
and puts guardrails around them. If it works, we get product management from
everyone. If it fails, we will know because bets will be shaped badly, and that is
a fixable and visible failure.

---

## 1. What changed, and what did not

### What changed

| Old assumption | What we operate on now |
|---|---|
| Building requires a handoff to engineering. | Anyone close to the problem can produce a working first version. |
| You write a specification, then you build. | You run a probe: an audit if the surface exists, a prototype if it doesn't. |
| Planning starts with tasks and estimates. | Planning starts with a customer problem, an appetite, and a no-go list. |
| A prototype is speculative; code is progress. | A prototype is cheap. Trusted, adopted, maintained product is progress. |
| The backlog is the source of truth. | Active bets, the capacity dial, and production telemetry are the source of truth. |
| More engineering capacity means more product. | More *acceptance, release, and stopping* capacity means more product. |

### What did not change

- Choosing the right customer problem.
- Knowing whether the data is honest enough for the promise being made.
- Protecting the product's language, security, and architecture.
- Owning what you ship after it ships.
- Killing weak work fast enough that it doesn't consume the strong work.

Agents compress implementation. They do not compress judgment, customer
understanding, or accountability — and they do not compress *maintenance*. Every
surface we create is a surface we own forever.

---

## 2. The three lanes

All engineering work at SuperCat is in exactly one of three lanes. The lane
determines the intake, the gates, and the build path.

### Run

Bugs, incidents, support escalations, onboarding commitments, client projects,
infrastructure, and debt paydown.

Run work needs **no bet and no shaping**. It arrives from support, CS, onboarding,
or an incident, and it is governed by SLA and by the daily standup. Trying to make
Run work pass through a bet process would be the fastest way to get this whole
model ignored.

*Owners: CTO and Senior Engineer.*

### Platform

Work on the SuperCat product that exists today and has paying customers — the
sales portal, eCat, analytics, integrations, admin experience. Anything from a UX
correction to a net-new accretive feature.

This is conventional software development, done prototype-first. It follows normal
engineering standards: pull request, review, QA, release record.

*Owner: CTO.*

### Agentic

New agent surfaces intended to be sold — the commercializable agent product line.

Same shaping discipline as Platform, but a different build-and-certify path: the
**Agent Factory**. Lane and firewall contract, topology template, inherited
sensors, golden-set evals, and the sandbox-to-production autonomy ladder.

*Owners: CTO and CEO.*

### Why the lanes are separate

Because the alternative is a category error in both directions. Routing a sales
portal analytics improvement through Agent Factory intake — lane firewalls,
topology selection, eval harnesses — would be absurd overhead on conventional
software. And shipping a commercializable agent *without* that apparatus is how
you ship something that confidently tells a customer something false.

**Do not route Platform work through the Agent Factory. Do not commercialize an
agent without it.**

Size is not a lane. A two-hour fix and a five-week feature are both Platform; the
appetite tells you which.

---

## 3. The capacity dial

The mix across the three lanes is a **decision the company makes and publishes**,
not an outcome we discover at the end of a quarter.

| Lane | Today (estimated) | Two-quarter target |
|---|---:|---:|
| Run | ~75% | 40% |
| Platform | ~20% | 40% |
| Agentic | ~5% | 20% |

**The "today" column is an estimate, not a measurement.** We do not yet instrument
engineering time by lane. Per [`07_how_we_establish_truth.md`](07_how_we_establish_truth.md), it is labeled
as such and carries no more weight than an estimate deserves. Making it a real
number is an early adoption task.

Moving this dial is the single most important thing this operating model is for.
The last year was correctly spent on debt, database migration, and hosting — that
work had to happen, and it is why Run dominates. It is finished. The next year has
to be net-new, accretive, needle-moving product, and that will not happen by
intention alone. It happens by naming the ratio, publishing it, and defending it
at the roundup when Run tries to eat everything, which it will.

The dial is reset at a roundup, deliberately, and only there.

---

## 4. How to shape a bet

This is the part that decentralizes. If you are not an engineer and you have never
done this, this section is the whole job.

A bet is a claim that a specific customer problem is worth a specific amount of
our time. That is all it is.

### Step 1 — Name the customer, the job, and the moment

Not a persona. A named customer or a specific, recognizable class of them. What
job are they trying to do, and at what moment does it hurt? If you cannot name the
moment, you do not have a bet yet — you have a topic.

### Step 2 — Set an appetite and the no-gos

**Appetite is not an estimate.** An estimate asks "how long will this take?" An
appetite says "this problem is worth *this much* and no more." Three sizes:

| Appetite | Meaning |
|---|---|
| **Hours** | A probe, a fix, an experiment. No approval needed, ever. |
| **Days** | A small bet. Up to a week. |
| **Weeks** | A real bet. Maximum three roundups — six weeks — before it must be re-bet. |

Write the **no-gos** at the same time: what this explicitly will not do, and which
rabbit holes are off-limits. No-gos are what make a small appetite survivable.

We did not adopt six-week cycles. But nothing gets more than three roundups of
runway without someone deliberately choosing to continue it.

### Step 3 — Run the probe

**This is the step that replaces writing a specification.**

A probe is a few hours spent answering the question that actually decides the bet.
There are two kinds, and picking the wrong one is the most common way to waste the
hours.

| | **Audit probe** | **Prototype probe** |
|---|---|---|
| **Use when** | The surface, workflow, or data already exists | The thing does not exist yet |
| **Question** | What does the system actually do today, on real data? | Would this workflow be better? |
| **Output** | A one-page findings note | A working artifact people can click |

**On an existing surface, audit before you prototype.** The dominant uncertainty
is almost never "would this design be better" — it is "what does it do now, and
why doesn't it work?" Prototyping first skips that and quietly bakes in
assumptions about current behavior that are often wrong. The classic waste is
rebuilding, badly, something the platform already does behind a config flag nobody
knew about.

**The audit must hit real data.** Reading the code tells you what was intended.
Querying production tells you what is true. Only the second one settles anything.

Often the two are sequential: audit for an afternoon, and *if* the problem
survives, prototype. Frequently it won't survive — the system already does it, or
the real problem is data quality or configuration rather than product. That is the
cheapest possible outcome and the audit is what produces it.

For a genuinely new surface there is nothing to audit. Build the thing. Badly is
fine — use agents, fake data, hard-code whatever you need. An argument about a
working screen is worth ten arguments about a paragraph describing a screen.

There is no shaping clinic. There is no brief to submit. There is no approval for
either kind of probe — an hours-appetite probe is always yours to spend.

**Why this is not a return to specifications.** What we removed was the
*speculative* document — an argument about a thing that does not exist. An audit
is the opposite: an empirical finding about a system that does, produced by
querying it. The prototype and the audit are both learning by doing. Neither is a
spec.

### Step 4 — Kill it or carry it

Most probes should die here, quietly and without ceremony. That is the system
working. A probe that dies in three hours is the cheapest possible outcome, and an
audit that kills a bet before anyone builds anything is cheaper still.

If it survives, bring it to the roundup. Only now — and only if it trips Gate 3 —
does anything get written down.

Keep the audit notes somewhere findable. They accumulate into the map of the
platform that no one has ever written down, and the second person to touch that
surface should not have to rediscover it.

### What survives from Shape Up

**Appetite**, **no-gos**, and the **circuit breaker** — when the appetite is
exhausted, the work stops rather than silently extending. Everything else about
six-week cycles, cooldowns, and shaping-before-building assumed expensive
building. We do not.

---

## 5. The fidelity ladder

The most common way to get this wrong is to show someone a rough thing and have
them react to the roughness instead of the idea. The rule that prevents it:

> **Fidelity is set by the audience, not by the stage.**

| Tier | Audience | Bar |
|---|---|---|
| **Probe** | You, and whoever you drag over to look | None. Ugly is fine. Synthetic data is fine for a prototype; an audit must use real data. Never leaves the building. |
| **Demonstrable** | Colleagues, the roundup | Recognizable as the real product. Real data, or *visibly* labeled synthetic. |
| **Customer-facing** | Any customer, prospect, or design partner | Full bar — see Gate 1. |

A probe you would be embarrassed to show a customer is not a problem. A probe you
*do* show a customer is a serious one, because you have spent credibility to learn
something you could have learned for free.

The middle tier is where most of the value is. A demonstrable at the roundup, on
real data, is the highest-information artifact this company produces.

---

## 6. The five gates

These are the only places the company says no. If a piece of work does not trip a
gate, nobody needs to approve it.

### Gate 1 — Customer exposure

*Trips when: anything goes in front of a customer, prospect, or design partner.*

Requires: the customer-facing fidelity bar (design system, real data), the honesty
discipline in [`07_how_we_establish_truth.md`](07_how_we_establish_truth.md) — declared confidence, no claim the
data cannot support, suppression over guessing — and a **named owner** who handles
what comes back.

The working precedent is the `thin_defer` doctrine in the brand-to-customer skill:
when the underlying data cannot honestly support the story, you do not ship a
weaker version of the story. You do not ship.

*Approver: the lane owner.*

### Gate 2 — Shared kernel

*Trips when: work defines or redefines a term the rest of the company uses.*

Account, customer, rep ownership, catalog, order, inventory, opportunity,
confidence. These have one definition and a named owner each.

**No prototype, agent, or new surface may quietly redefine a shared term.** This
is the gate that matters most as building gets cheaper, because the failure mode
of cheap surface creation is four surfaces that each mean something different by
"active account," and no way to reconcile them after the fact.

*Approver: the domain owner named in the glossary.*

### Gate 3 — Production commitment

*Trips when: appetite is **weeks**, OR the work becomes customer-facing, OR it changes the shared kernel.*

This is the **only** place a written contract is required. It is where a personal
bet becomes a company commitment and where the capacity dial gets debited.

The contract is one page (see the appendix). Below this threshold — an hours or
days probe on internal Platform work — write nothing.

*Approver: the roundup.*

### Gate 4 — Release

*Trips when: code reaches production.*

Three named accountabilities, every time:

| Accountability | Who |
|---|---|
| **Acceptance** — the work does what it claimed | Named per bet at Gate 3 |
| **Merge** — it lands cleanly | Named per bet at Gate 3 |
| **Release record** — deployment state is observable | Agent scrum manager, writing deploy state back to Jira |

The release record is the load-bearing piece. Today we cannot reliably answer "is
this in production?", which means support cannot tell a customer when their fix
ships. That is the gap — not the queue depth in Jira, which is a hygiene artifact
and is being fixed in parallel.

**Every change that reaches a customer gets a release record, whether or not a
ticket preceded it.** Light at intake, strict at egress.

### Gate 5 — Decision date

*Trips when: a bet passes Gate 3.*

Every production bet carries a review date and a **default action if the review
does not happen**. The default is to park.

This is deliberately a default rather than a meeting. Reviews that depend on
someone remembering to call them do not happen, and the work stays alive on
inertia. A bet that nobody cared enough to review is a bet nobody cared enough to
continue.

*Enforced by: the artifact, not a person.*

---

## 7. Decision rights

| Decision | Owner | Needs |
|---|---|---|
| Find a problem, build an hours-probe | Anyone | Nothing |
| Spend a days-appetite on a probe | Anyone | Tell your lane owner |
| Show something to a customer | Lane owner | Gate 1 |
| Change a shared term | Domain owner | Gate 2 |
| Commit production capacity | Roundup | Gate 3 |
| Release to production | Lane owner | Gate 4 |
| Scale, iterate, park, or kill | Roundup | Gate 5, outcome evidence |
| Reset the capacity dial | CEO + CTO | Roundup |

### What leadership does here

Set the capacity dial and defend it. Keep the number of concurrent
weeks-appetite bets small enough that they finish. Resolve cross-lane conflicts.
And insist that outcomes rather than enthusiasm decide what scales — including
when the enthusiasm is leadership's own, which is the harder case and the more
common one.

---

## 8. Cadence

**Two standing meetings. Both already exist. We are not adding a third.**

| Rhythm | Purpose | Who | Output |
|---|---|---|---|
| **Daily engineering standup** | Run lane. Unblock, triage, fix. | Engineering | Today's Run queue |
| **Biweekly technology & product roundup** | Everything else. | Whole team | Demos, gate decisions, dial resets |

The roundup already does the most important thing — people demo what they built
and the company sees it. This model adds three jobs to it and nothing else:
**decide Gate 3** on bets asking for production capacity, **act on Gate 5**
reviews that came due, and **reset the capacity dial** when it needs it.

Everything else that a heavier process would put in a meeting is an **artifact**
instead: bet state, release records, and lane capacity are produced by the agent
scrum manager and Jira and read asynchronously. If a mechanism in this document
requires a recurring meeting to function, it is wrong and should be redesigned.

This is not a preference for asynchronous work. It is arithmetic. Five people
write code and three of them do other jobs. Meeting time is the most expensive
capacity we have.

---

## 9. Shared language

Cheap surface creation makes a glossary load-bearing. Four rules:

1. **Every shared business concept has one definition and one named owner.**
2. **No prototype or agent may redefine a shared term.** Adapt at the boundary instead.
3. **Enums are locked.** If a taxonomy exists, use it — do not invent a parallel one.
4. **When a legacy system means something different, write an explicit adapter.** Do not let two meanings quietly coexist.

The working example is the `0a / 0b / 0c` doctrine in the brand-to-customer skill:
locked taxonomies, an explicit "do not invent new enums" rule, and a named
resolver for the mapping. That pattern is what we generalize — not a heavyweight
domain-modeling apparatus, which we neither need nor have the people for.

Bounded contexts let surfaces move independently. The field sales assistant, the
intelligent presentation, and the sales portal can each own their workflow and
vocabulary while sharing the same commercial truth underneath. What they may not
do is each invent their own version of what "rep ownership" means.

---

## 10. The two build paths

Both lanes shape bets the same way. They diverge at build.

| | Platform | Agentic |
|---|---|---|
| **Build standard** | Conventional engineering | Agent Factory |
| **Requires** | PR, review, QA, release record | All of that, plus lane + firewall contract, topology template, inherited sensors |
| **Certification** | Acceptance owner confirms behavior | Golden-set evals; autonomy graduates only as evals pass |
| **Trust model** | Tested code | No eval, no autonomy |

For agentic surfaces there are three additional non-negotiables: **provenance**
for any material claim, an explicit **fallback** when confidence is weak, and
**test cases for the outputs that would be most damaging if wrong**.

A demo that impresses is not evidence of readiness. For an agent, readiness is an
eval score.

---

## 11. What we stop doing

- Writing a specification before running the probe.
- Proposing a change to an existing surface without first establishing what it does today, on real data.
- Treating a successful demo as proof of customer value or production readiness.
- Requiring approval to spend hours on a probe.
- Letting agents or prototypes invent new meanings for shared business terms.
- Extending an appetite by default when time runs out.
- Keeping low-conviction work alive because it is already partly built.
- Measuring product work by output volume rather than outcomes.
- Shipping anything to production without a release record.
- Adding a meeting to solve a problem an artifact could solve.

---

## 12. Worked examples

### A — Customer Success spots a pain (Platform)

Onboarding keeps stalling on catalog admin before go-live. It has shown up in
enough retros to be structural.

Kylor names it: *catalog administrators at pre-go-live customers, in the two weeks
before launch, cannot tell which of their product records are broken.* Appetite:
days. No-gos: not building an import tool, not touching pricing.

Catalog admin already exists, so he starts with an **audit probe**, not a
prototype. An afternoon against real customer catalogs, answering one question:
what does the system surface about broken records today? The one-pager finds that
the validation exists but only fires at import, that three orgs have it disabled
by config, and that nothing re-checks a record after go-live.

That changes the bet. It is not a missing feature — it is validation that runs
once and never again. Had he prototyped first, he would have rebuilt the
validation he already had.

Now he prototypes against that finding, and brings both to the roundup. Because
the appetite for the real version is weeks and it will be customer-facing, it
trips **Gate 3**, so a one-page contract gets written: outcome, acceptance owner,
merge owner, decision date at 30 days post-release. It debits the Platform share
of the dial. The CTO builds it, it passes **Gate 4** with a release record, and at
the decision date the roundup looks at whether onboarding actually got faster.

Total written documentation before anyone committed capacity: none.

### B — An engineer has a hunch (Platform, dies correctly)

Bruce thinks the sales portal analytics page should be a live dashboard. He spends
two hours building one. Hours appetite, no approval needed, nobody told.

He shows three people. Nobody can name the moment they would open it. He deletes
it.

This is a success. It cost two hours, and the alternative was a quarter of
someone's roadmap.

### C — A commercializable agent (Agentic)

The CEO's simulation work suggests a rep-facing coaching surface has value where a
named field owner exists. Design partner reactions support it.

It is Agentic, so it takes the Agent Factory path: lane and firewall contract
(customer-product, so internal-only data can never surface), topology template
(operator skill, inheriting provenance gates and a fallback matrix), and a golden
set before it touches a customer instance.

It trips **Gate 1** the first time a design partner sees it — full fidelity bar,
declared confidence, and a rule that it must decline to answer rather than invent
a book that isn't there. It trips **Gate 3** for production capacity. It graduates
autonomy only as evals pass.

The contrast with example A is the point: same shaping, different build path.

---

## 13. Adoption

### Preconditions running in parallel

Two things must land for this model to be measurable. Neither is part of the model
itself, and neither blocks starting.

- **Jira rigor**, via the agent scrum manager. Today, queue states do not reflect reality and most commits carry no ticket reference. Until that is fixed, lane capacity and release state are estimates.
- **The release record.** Gate 4 is inert without it. This is the highest-value single build in this document.

### First 30 days

- Adopt the three lanes, the fidelity ladder, and the five gates. Publish the capacity dial.
- Name domain owners and publish the shared glossary.
- Roundup takes on Gate 3 decisions and dial resets. No new meetings.
- Run two or three real bets through the model end to end.

### Days 31–60

- Every production commitment has a contract, an acceptance owner, a merge owner, and a decision date.
- Release records exist for everything reaching production.
- First Gate 5 reviews come due. Park something.

### Days 61–90

- Replace the estimated capacity dial with a measured one.
- Review whether the model is actually decentralizing — count bets shaped by non-engineers.
- Tune the gates. If one never fires, delete it. If work is routing around one, find out why.

### How we will know it worked

| Signal | Why it matters |
|---|---|
| Capacity dial moves toward the target | The whole point |
| Bets shaped by non-engineers | Decentralization is real, not aspirational |
| Merge-to-production latency | The measure of Gate 4 |
| Day-30 usage on every shipped surface | Catches things nobody uses, early |
| Things parked or killed per quarter | A model that never stops anything is not working |

That last one is the honest test. A portfolio that only ever adds is not a
portfolio.

---

## Appendix — The audit one-pager

The output of an audit probe. One page, a few hours, no approval to start. It
reports what is; it does not propose what should be.

**Surface** — what you looked at, and the boundary of what you did not.

**What it does today** — actual current behavior, in plain language.

**On real data** — what you found when you queried production. Which orgs, how
many records, how often. Cite the query or the table.

**Where it breaks** — the failure cases you could reproduce, and the ones you
suspect but could not.

**Config and variance** — what differs by org, what is flag-controlled, what is
hard-coded. This is usually where the surprise is.

**Shared terms it touches** — relevant to Gate 2 if the bet proceeds.

**Verdict** — one of: *real product gap* · *config or data-quality problem* ·
*already supported* · *needs a deeper look.*

That last line is the point of the whole exercise. Three of the four verdicts end
the bet without anyone building anything.

---

## Appendix — The one-page contract (Gate 3 only)

Keep it to one page. If it needs more, the bet is too big.

**Outcome** — customer, job, the moment, and what "better" measurably means.

**Evidence** — what the probe showed, what is still a hypothesis, who has seen it.
Grade each claim: *Believe* (directly evidenced) · *Validate* (testable next) ·
*Hypothesize* (extrapolated).

**Appetite and no-gos** — hours, days, or weeks. What this will not do.

**Domain** — which shared terms it touches, and the owner's sign-off if it changes any.

**Trust contract** — what the system may assert, how it signals uncertainty, what
it does when confidence is weak.

**Owners** — acceptance owner, merge owner, and who owns it after release.

**Decision date and default** — when we review, and what happens automatically if
we don't. Default is park.

The *Believe / Validate / Hypothesize* grading comes from the field assistant value
thesis, which is the strongest example of this discipline the company has produced.
Copy it. Grading confidence is what separates a contract from a wish.

---

## Appendix — Release record fields

Owned by the agent scrum manager, written back to Jira.

| Field | Why |
|---|---|
| What changed | Human-readable, not a commit list |
| Commit / PR reference | Traceability |
| Deployed at (timestamp) | Answers "is it live?" |
| Environment | Staging vs production |
| Acceptance owner | Who confirmed it works |
| Customer-visible? | Determines whether support needs to know |
| Related tickets | May be empty — the record exists regardless |

The last row is the important one. **The absence of a ticket is not permission to
skip the record.**
