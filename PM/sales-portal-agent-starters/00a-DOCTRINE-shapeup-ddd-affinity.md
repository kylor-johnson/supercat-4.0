# Sales Portal PM Context Pack
## Shape Up × Domain-Driven Design × Affinity Mapping

**Purpose:** Give a fresh agent (or human PM) everything needed to product-manage a **build-out / refresh of SuperCat’s Sales Portal** without re-reading the source materials from scratch.

**Created:** 2026-07-16  
**Audience:** Fresh Cursor agent / PM co-pilot  
**How to use:** Paste this file (or `@`-mention it) at the start of a new chat. Treat it as operating doctrine, not optional flavor.

---

# 0. Mission frame (read first)

You are helping PM a **Sales Portal** refresh / build-out for SuperCat (eCat Online Sales Portal — reporting surface for manufacturer sales orgs: dashboard, orders, invoices, customers, reports).

This is **not** the eCat iPad catalog. Sales Portal ≠ catalog/checkout. Same eOL URL space historically (`/:org/e/:site`), but different product job.

### How these three assets work together

| Asset | Role in this program |
|---|---|
| **Affinity Mapping** | Upstream synthesis. Turn messy qualitative signal (rep interviews, support tickets, screenshots, stakeholder rants, “what’s broken”) into **decision-grade findings** and a shared language of problems. |
| **Domain-Driven Design (DDD)** | Middle layer. Turn findings into a **correct product model**: bounded contexts, ubiquitous language, aggregates, anti-corruption layers to ERP/legacy. Prevents “pretty UI over wrong nouns.” |
| **Shape Up** | Delivery system. Turn shaped problem+solution into **bets with appetites**, six-week (or adapted) cycles, circuit breakers, scopes, hill charts — so the refresh ships in meaningful slices instead of a grab-bag redesign. |

### Operating sequence (default)

```
1. Affinity map raw research / feedback
        ↓ findings + decisions named
2. DDD: name the domain, contexts, ubiquitous language
        ↓ model + boundaries agreed
3. Shape Up: set appetite → shape → pitch → bet → build → ship
        ↓ next cycle cool-down
4. New feedback → back to affinity / reshape (never backlog forever)
```

### Anti-patterns this pack exists to prevent

- Grab-bag: “Sales Portal 2.0” / “redesign the dashboard” with no problem, no appetite, no no-gos.
- Wireframe-first: high-fidelity mocks before the domain language is settled.
- Backlog theater: infinite tickets, no bets, no circuit breaker.
- Top-down affinity: buckets named before cards exist.
- Tech-first DDD: microservices cosplay without ubiquitous language.
- Pretty empty shells: visual polish without metric / domain discipline.

---

# 1. Shape Up — full operating manual
**Source:** [Shape Up](https://basecamp.com/shapeup) by Ryan Singer (Basecamp / 37signals)  
**Also:** printable PDF at https://basecamp.com/shapeup/shape-up.pdf

Shape Up is Basecamp’s product development method: **shape work before committing**, **bet in fixed cycles**, **hand teams responsibility**, and **target the risk of not shipping on time**.

It is explicitly *not* Scrum, Kanban, velocity tracking, daily standups, or backlog grooming.

---

## 1.1 Core thesis

1. **Six-week cycles** — long enough to ship something meaningful; short enough that the deadline is felt from day one.
2. **Shape before you schedule** — a small senior group defines key elements of a solution (rough, solved, bounded) before a team is committed.
3. **Appetite over estimate** — ask “how much is this worth?” not “how long will it take?”
4. **Assign projects, not tasks** — integrated designer + programmer teams discover their own tasks inside shaped boundaries.
5. **Target shipping risk** — de-risk rabbit holes in shaping; circuit-breaker if a bet doesn’t finish; integrate vertical slices early.

Virtuous circle: better shaping → clearer boundaries → more team autonomy → less senior babysitting → more senior capacity to shape.

---

## 1.2 Part 1 — Shaping

Shaping is **closed-door creative work** on a separate track from building. Unshaped work is private until bet. You may shelf or kill shaped ideas with no guilt.

### Properties of shaped work

| Property | Meaning |
|---|---|
| **Rough** | Unfinished on purpose. Room for designers/programmers to apply judgment. Fat markers / breadboards, not wireframes. |
| **Solved** | Main elements exist at the macro level and connect. Open questions / rabbit holes removed or patched. |
| **Bounded** | Appetite + explicit no-gos tell the team where to stop. |

### Wrong levels of abstraction

- **Wireframes / hi-fi too early** → concrete enough to kill creativity; hide implementation complexity; freeze scope when scope must stay variable.
- **Words alone** (“add a calendar”, “improve reports”) → too abstract; team mind-reads; scope expands unboundedly.

**Right level:** concrete enough to know what’s in/out; abstract enough that the build team still designs the interesting details.

### Case study: Dot Grid Calendar (canonical)

Customers asked for “a calendar.” A full calendar is ~6 months of drag/drop, multi-day wrapping, month/week/day views, color coding, desktop vs mobile, etc. Appetite was **six weeks**, not six months. Research narrowed the pain to **see free spaces for scheduling**. Solution: 2-month read-only grid, dots for events, agenda list below, tap day → scroll to events. Explicitly out: drag, spanned pills, color categories. Shipped inside appetite.

**Lesson for Sales Portal:** never shape “rebuild analytics.” Shape “rep can’t answer X in under Y clicks against baseline Z.”

### Who shapes

- Creative + integrative: interface ideas × technical possibility × business priority.
- Primarily **interaction design from the user’s perspective** — what it does, how it works, where it fits.
- Need technical literacy (what’s hard/easy), not necessarily coding.
- Strategic: why this problem, who benefits, opportunity cost.
- Small room: alone or 1–2 trusted collaborators. Fast, frank, private.

### Two tracks

| Track | During a cycle |
|---|---|
| **Building** | Teams build previously shaped bets |
| **Shaping** | Shapers prepare *future* potential bets |

### Four steps of shaping

1. **Set boundaries** (appetite + narrowed problem)
2. **Find the elements** (breadboard / fat marker)
3. **Risks & rabbit holes** (de-risk)
4. **Write the pitch** (five ingredients)

---

### Step A — Set boundaries

#### Appetite (time budget, not estimate)

- **Small batch:** 1 designer + 1–2 programmers, **1–2 weeks** (batched into a six-week cycle).
- **Big batch:** same team size, **full six weeks**.
- If bigger than six weeks: narrow the problem or break off a meaningful six-week piece. Do not “estimate bigger.”

**Fixed time, variable scope.** Appetite starts with a number and ends with a design. Estimates start with a design and end with a number. “Good” is relative to constraints — a hot dog can be the right meal.

#### Responding to raw ideas

Default response: **“Interesting. Maybe some day.”** Soft no. No backlog entry required. Don’t commit on first contact. Poker face — too much enthusiasm creates false promises.

#### Narrow the problem

Flip from “what could we build?” to **“what’s really going wrong?”** Call customers; ask *when* they wanted the thing, not *what it should look like*. Find the baseline workflow that breaks.

**Grab-bag warning:** “redesign Files,” “Sales Portal 2.0,” “refactor reporting” are not projects. Recover by splitting into appetite-sized problems with done criteria (“Better file previews,” “Custom folder colors”).

Boundaries ready when you have: **raw idea + appetite + narrow problem definition**.

---

### Step B — Find the elements

Move fast with the right people (or alone). Avoid wireframe fidelity.

Questions to answer:
- Where does the new thing fit in the current system?
- How do you get to it?
- Key components / interactions?
- Where does it take you?

#### Breadboarding (from electrical engineering)

Prototype with **places, affordances, connections** — no visual styling.

1. **Places** — screens, dialogs, menus (name underlined)
2. **Affordances** — buttons, fields, copy the user acts on (listed under the place)
3. **Connection lines** — how affordances move the user between places

Use words, not pictures. Debate topology and use-case fit. Example flow debates (Autopay) surface deep product questions without layout fights.

#### Fat marker sketches

When the idea is inherently visual / 2D layout *is* the problem: sketch with strokes so thick detail is impossible (Sharpie / fat iPad brush). Purpose: force the right fidelity band; name the stage so you don’t skip it.

#### Output = list of elements

Not a deliverable yet. Not a bet yet. Clay still wet — you can walk away.

Examples of good element lists:
- Autopay: checkbox on Pay Invoice; disable option on invoicer side
- Dot Grid: 2-up monthly grid; dots not pills; agenda below that scrolls on tap

Leave room for designers later. Over-specified mocks from seniors become accidental direction.

---

### Step C — Risks and rabbit holes

Goal: thin-tailed delivery risk. One unpatched hole can burn ⅓ of a cycle.

Walk the use case in slow motion. Ask:
- New technical work we’ve never done?
- Assumptions about how parts fit?
- Assuming a design solution exists that we couldn’t invent ourselves?
- Hard decisions that should be settled now so they don’t trip the team?

**Patch holes in shaping** (e.g. To-Do Groups: don’t redesign completed items — append group name). Call out **out of bounds** use cases. **Cut back** exciting-but-unnecessary pieces (color-coding groups → nice-to-have).

**Present to technical experts** before writing the pitch:
- Frame as potential bet, not committed work.
- Ask “possible in six weeks?” not “possible?”
- Hunt time bombs. Keep clay wet — redraw on whiteboard; then invite revisions.
- Validate or go back for another shaping round.

De-risked = elements + patches + fences → ready to write pitch.

---

### Step D — Write the pitch (five ingredients)

A pitch presents a **good potential bet**. Always include:

1. **Problem** — raw idea / use case / observed pain. Best form: **one specific story** showing why status quo fails (baseline). Problem without solution = unshaped. Solution without problem = un-testable fitness.
2. **Appetite** — 2 weeks or 6 weeks (or adapted). Turns everyone into partners of constraint.
3. **Solution** — core elements, understandable immediately. Help them see it with selective embedded / annotated fat-marker sketches for linchpin parts. Still not wireframes.
4. **Rabbit holes** — called-out patches / technical constraints (e.g. “no custom domains for v1 URLs”).
5. **No-gos** — explicitly excluded functionality / use cases.

Present async first (posted write-up). Betting table decides yes/no — comments poke holes, they don’t approve.

---

## 1.3 Part 2 — Betting

### Bets, not backlogs

Backlogs accumulate guilt and grooming cost. Instead: **a few well-shaped pitches** considered at a betting table. Unchosen pitches die unless someone independently revives and re-lobbies them. Important ideas come back; unimportant ones don’t.

**Decentralized lists OK** (Support’s top issues, Product’s shaping candidates, eng’s bug list) — none are automatic betting-table inputs. Cross-pollinate in infrequent one-on-ones.

### Cycle structure

| Piece | Default (Basecamp) |
|---|---|
| **Cycle** | 6 weeks uninterrupted build |
| **Cool-down** | 2 weeks after each cycle: breathe, ad-hoc, bugs, betting table |
| **Big batch team** | 1 designer + 1–2 programmers on one project all cycle |
| **Small batch team** | Same size team; several 1–2 week projects; self-juggle; all ship by cycle end |
| **QA** | Joins later for edge cases; not a gate for basic quality |

### Betting table

- Held in cool-down.
- Stakeholders with real authority (at Basecamp: CEO/product last word, CTO, senior eng, product strategist).
- Short (≤1–2 hours). Pitches read in advance.
- Output = cycle plan: what + who. No “step two” approval. No after-the-fact interruption.

### Meaning of a bet

1. **Payout** — meaningful finished thing at end, not “progress on tasks.”
2. **Commitment** — uninterrupted time; no “just one day” pulls (momentum is second-order).
3. **Capped downside** — circuit breaker: if it doesn’t ship in the bet, **default = no extension**.

### Circuit breaker

- Prevents runaway projects.
- Signals shaping failure → reshape, don’t sunk-cost extend.
- Motivates scope hammering and ownership.

Rare extension rules: remaining work must be true must-haves that survived hammering, **and all downhill** (no unknowns). Prefer cool-down slack over extension habit.

### Bugs

Bugs are not automatically more important than everything else. Strategies:
1. Cool-down fixes
2. Shape + bet big bugs at the table
3. Occasional “bug smash” cycle

True crises (data loss, outage) can break the rule. Most bugs can wait.

### Keep the slate clean

Bet **one cycle at a time**. Never carry scraps without reshaping. Multi-cycle visions still ship a complete working slice each cycle.

### Modes (where you are in product life)

| Mode | When | Shape? | Ship expectation |
|---|---|---|---|
| **Existing product** | Adding to built house | Full shape | Ship to customers end of cycle |
| **R&D mode** | New product theory | Fuzzy; senior team spikes | Learn / settle architecture; may not ship |
| **Production mode** | Core settled; filling features | Deliberate pitches | Merge “done”; may still cut before public launch |
| **Cleanup mode** | Pre-launch | No formal shaping | Continuous small merges; ≤2 cycles; final cut |

**Sales Portal refresh note:** Treat “chrome-only reskin” vs “answer-first analytics platform” as different modes. Platform-grade work may need R&D spikes before production-mode bets. Do not pretend a grab-bag redesign is one big-batch pitch.

### Betting table questions

1. Does the problem matter? (vs other problems *right now*)
2. Is the appetite right?
3. Is the solution attractive? (incl. opportunity cost of UI real estate)
4. Is this the right time? (morale, splash vs cleanup, area fatigue)
5. Are the right people available?

Then post a kick-off message: bets + who.

---

## 1.4 Part 3 — Building

### Hand over responsibility

- Assign the **whole project**, not shredded tasks.
- Done = **deployed** (or merged as “shipped” definition for unreleased products).
- Kick-off: post pitch; short call for clarifying questions.
- First days: orientation silence is normal (≈3 days max before check-in). Respect learning the lay of the land.
- **Imagined vs discovered tasks:** most real work appears by doing real work.

### Get one piece done

Integrate a **vertical slice** early (UI + code), not horizontal layers.

Pick first slice that is:
1. **Core** — central to the concept
2. **Small** — finishable in a few days
3. **Novel** — eliminates real uncertainty

Practices:
- Programmers don’t wait for pixel-perfect design — pitch is enough to start modeling.
- **Affordances before beauty** — endpoints, buttons, fields first; style later.
- Program just enough for the next step (scaffolding OK).
- **Start in the middle** — stub login/setup; attack the interesting problem first.
- First make it work, then make it beautiful.

### Map the scopes

Organize by **structure of the problem**, not by person/role.

**Scopes** = independently finishable integrated slices (bigger than tasks, smaller than the project). Track as named to-do lists. They become the **language of the project**.

Discover scopes by walking the territory — expect reshuffling in week 1–2.

**Scopes are right when:**
- You can see the whole project; nothing scary is hidden
- Conversation flows using scope names
- New tasks have an obvious bucket

**Redraw when:**
- Hard to say how done a scope is (unrelated tasks inside)
- Grab-bag names (“front-end”, “bugs”)
- Too big to finish soon

Scope types:
- **Layer cake** — thin even backend under UI surface (default for many info systems)
- **Iceberg** — heavy backend or heavy UI; factor separately; question necessity first
- **Chowder** — ≤3–5 loose tasks; if longer, find the missing scope
- **Nice-to-haves** — prefix `~`; cut first

### Show progress — Hill Chart

Work has two phases:
- **Uphill** — figuring out approach / unknowns
- **Downhill** — known execution

Plot each **scope** on the hill (unknown → known → done). Status without nagging. Stuck dots = raised hand. Refactor scopes if a stuck scope is actually multiple things. Build uphill with hands (validate), not heads (theory). Sequence scary/novel scopes uphill first (inverted pyramid).

### Decide when to stop

- Compare to **baseline**, not ideal perfection.
- Limits motivate trade-offs.
- Scope grows like grass — give teams authority to cut continuously.
- Cutting scope ≠ lowering quality; it differentiates the product.
- **Scope hammer** questions: must-have? ship without? new vs pre-existing pain? likelihood? who sees it? impact? audience alignment?
- QA for edges; basic quality owned by the team. QA findings start as nice-to-haves unless elevated.

### Move on

- Let post-ship storm pass; avoid knee-jerk.
- Stay debt-free: soft “no” to raw requests; don’t poison next cycle’s clean slate.
- Feedback → raw ideas → must be **shaped** again before betting.

---

## 1.5 How to begin (adapt to size)

**Basic truths (keep):** shaping, deliberate bets with capped downside, distinguish known vs unknown while building.

**Practices (scale):** six weeks / cool-down / formal table — optional when tiny; necessary when coordination breaks.

Options:
- **A:** One six-week experiment (shape one project; protect a team; no interruptions)
- **B:** Start with shaping only (if you don’t control eng time)
- **C:** Start with cycles (kill two-week sprint overhead first)
- Always: **fix shipping before fancy discovery**

### Shape Up glossary (complete)

| Term | Definition |
|---|---|
| Appetite | Time we *want* to spend; not an estimate |
| Baseline | What customers do without the thing we’re building |
| Bet | Commit a team for one cycle, uninterrupted, expectation to finish |
| Betting table | Cool-down meeting to choose pitches for next cycle |
| Big batch | One project fills the whole cycle |
| Breadboard | Places + affordances + connections; no styling |
| Circuit breaker | Default: cancel unshipped bets instead of extending |
| Cleanup mode | Unstructured pre-launch fix cycle(s) |
| Cool-down | ~2 weeks between cycles |
| Cycle | ~6 weeks uninterrupted shaped work |
| De-risk | Remove rabbit holes so odds of shipping rise |
| Discovered tasks | Found by doing real work |
| Downhill | Unknowns solved; execution remains |
| Fat marker sketch | Thick-line low-fidelity UI sketch |
| Hill chart | Status from unknown → known → done per scope |
| Iceberg | Scope with asymmetric UI vs backend complexity |
| Imagined tasks | Tasks invented before real work |
| Layer cake | Scope estimable from UI surface area |
| Level of abstraction | How much detail to leave in/out |
| Must-haves | Required for scope done |
| Nice-to-haves | Prefixed `~`; cut if time runs out |
| Pitch | Shaped write-up for the betting table |
| Production mode | Settled architecture; standard Shape Up |
| Rabbit hole | Too unknown/complex/open to bet |
| R&D mode | Senior spike to find architecture |
| Raw ideas | Unshaped requests in words |
| Scopes | Independently integrable finishable parts |
| Scope hammering | Forceful questioning to fit the time box |
| Shape | Make abstract idea concrete enough to bet |
| Small batch | Set of 1–2 week projects in one cycle |
| Time horizon | Longest deadline you can feel from the start (~6 weeks) |
| Uphill | Still has unknowns |

---

## 1.6 Pitch template (copy for every Sales Portal bet)

```markdown
# PITCH: <name>

## 1. Problem
- Specific story / baseline (what people do today that fails)
- Who feels it; how often; why it matters now

## 2. Appetite
- [ ] Small batch (1–2 weeks)  [ ] Big batch (6 weeks)
- Why this much time is the right price

## 3. Solution (elements)
- Element 1: …
- Element 2: …
- (Attach breadboard / fat-marker sketches)

## 4. Rabbit holes (patched)
- Risk → patch / decision already made

## 5. No-gos
- Explicitly out of this bet

## Done means
- Deployed / mergeable definition of done for this cycle
```

---

# 2. Domain-Driven Design (DDD) — full reference
**Source:** [GeeksforGeeks — Domain-Driven Design (DDD)](https://www.geeksforgeeks.org/system-design/domain-driven-design-ddd/)  
**Origin:** Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003/2004)

DDD prioritizes **understanding and modeling the problem domain** through collaboration with domain experts, then designing software that accurately represents that domain — not the other way around.

---

## 2.1 Etymology (what the name means)

1. **Domain** — the subject area the software addresses (banking → accounts, transactions, regulations; Sales Portal → backlog, invoices, territories, reps, customers…).
2. **Driven** — design choices are driven by domain understanding, not by tech fashion.
3. **Design** — the blueprint of components, interactions, and how requirements are met.

> “It is not the customer's job to know what they want.” — Steve Jobs (cited in source as reminder: domain expertise + design judgment required)

**Evans’ emphasis:** focus primarily on **business**, not primarily on technology. Beautiful architecture that doesn’t solve business needs is worthless.

---

## 2.2 Strategic design (the map of the territory)

Strategic design defines overall architecture aligned with the problem domain: how to organize concepts, partition the system, and set boundaries.

### Bounded Context

A specific area within the problem domain where a **particular model and language are consistently used**.

- Same word can mean different things in different contexts — and that’s OK if boundaries are explicit.
- Breaks large domains into manageable parts.
- Teams can evolve models per context without global confusion.

**Sales Portal starter contexts (hypotheses — validate via affinity + experts):**

| Context (candidate) | Likely language |
|---|---|
| **Portal Reporting / Analytics** | backlog, booked, invoiced, open order, concentration, date grain |
| **Order History Import** | order_data, ERP sync, line items (import files ≠ iPad-submitted orders) |
| **Invoice History Import** | invoice_data, ERP sync |
| **Customer / Territory** | bill-to, ship-to, territory, rep assignment |
| **Identity / Access** | portal user, permissions, org, site |
| **Catalog / eOL Commerce** | cart, product browse — *adjacent, often should stay separate* |
| **iPad Selling** | BaseItemCode, SmartLists, price levels — *different product* |

Do **not** force one “Order” model across import reporting, live iPad orders, and checkout. That’s the #1 DDD failure mode.

### Context Mapping

Defines relationships between bounded contexts: where they overlap/integrate, and communication agreements.

Common relationship styles (from strategic DDD practice; GFG mentions Partnership, Shared Kernel, Customer-Supplier):

| Pattern | Intent |
|---|---|
| **Partnership** | Two contexts succeed/fail together; coordinate closely |
| **Shared Kernel** | Small shared model subset; high coupling — use sparingly |
| **Customer–Supplier** | Downstream (customer) needs drive upstream (supplier) |
| **Conformist** | Downstream accepts upstream model as-is |
| **Anti-Corruption Layer (ACL)** | Translation layer protecting your model from alien/legacy models |
| **Open Host / Published Language** | Upstream offers a documented integration language |
| **Separate Ways** | Integration not worth it; solve independently |

### Shared Kernel

Shared subset of the domain model between contexts. Enables collaboration but **introduces coupling**. Keep tiny; manage ownership carefully.

### Anti-Corruption Layer (ACL)

Protects the core domain from external/legacy systems with different models/languages. Translates data/messages at the boundary so the core stays pure.

**Sales Portal ACL candidates:**
- ERP exports → portal_orders / portal_invoices tables
- Legacy eOL layout/nav → new analytics UI shell
- iPad product language → portal reporting language (do not conflate)

### Ubiquitous Language

Shared vocabulary used by **all stakeholders** (PM, eng, design, support, domain experts) in conversation **and** in code/UI.

Rules:
- Precise terms with clear meaning
- Mirror real business language
- When language splits by context, **name the context** instead of forcing one word

**Exercise:** After affinity mapping, promote cluster names that are mechanism-true into candidates for ubiquitous language. Kill synonyms (“backlog” vs “open orders” vs “unshipped”) by explicit decision.

### Strategic patterns (as listed in source)

General guidelines including Aggregates, Domain Events, Anti-Corruption Layer — solutions to recurring structuring problems so architecture reflects the domain.

---

## 2.3 Tactical design patterns

Used **inside** a bounded context to structure the domain model.

### Entity

Domain object with **distinct identity and lifecycle**. Mutable state. Identity persists even when attributes change.

Example (banking): `BankAccount` with account number, balance, owner; methods deposit/withdraw/transfer.

Portal examples: `Customer` (bill-to code), `PortalUser`, `Territory`, maybe `Order` *within Portal Reporting context* identified by ERP order id.

### Value Object

Describes characteristics; **no unique identity**; immutable in concept; equality by value.

Example: `Money` (amount + currency). Portal: `DateRange`, `Money`, `Address` (if treated as values), `PercentOfBacklog`.

### Aggregate

Cluster of entities + value objects treated as **one consistency unit**. One **aggregate root** controls access. Changes applied atomically within the boundary.

E-commerce example: `Order` aggregate root with `OrderItem`s.

Portal example candidate: `CustomerBacklog` aggregate (customer + open order lines + money totals) — validate with real consistency rules before inventing.

### Repository

Separates persistence from domain model. Consistent interface to query/store aggregates. Hides DB/API details.

Example: `CustomerRepository`, `RideRepository`.

### Factory

Encapsulates complex creation logic so clients don’t know construction details.

Example: `ProductFactory`.

### Service (Domain Service)

Behavior that **doesn’t naturally belong** to a single entity/value object. Stateless. Orchestrates multiple objects / enforces domain rules.

Examples: `OrderService` (discounts, shipping); `RideAssignmentService`; portal: `BacklogConcentrationService`, `TerritoryRollupService`.

### Domain Events (from RideX example in source)

Something meaningful that happened in the domain, named in past tense: `RideRequestedEvent`, `RideAcceptedEvent`. Useful for decoupling contexts and modeling workflows.

Portal candidates: `OrdersImported`, `InvoiceImported`, `PortalEnabledForOrg` — only if they earn their keep.

---

## 2.4 Worked example from source: RideX (study the shape)

**Ubiquitous language:** User, Driver, Ride Request, Ride, Ride Status…

**Bounded contexts:** Ride lifecycle; User account; Driver account.

**Entities / VOs:** User, Driver, Ride Request, Ride; Location as VO.

**Aggregate:** Ride aggregate managing request → assign → status.

**Repository:** RideRepository.

**Services:** Ride Assignment, Payment.

**Events:** RideRequested, RideAccepted.

**Scenario:** request → accept → in progress → complete → fare/payment.

**Use this as a template** for writing a one-page domain sketch of Sales Portal before shaping UI bets.

---

## 2.5 Benefits (source)

- Better communication via common language
- Prioritize valuable areas of the domain
- Designs that adapt as business evolves
- Separation of domain logic from infra/UI
- More testable domain objects

## 2.6 Challenges (source)

- Complexity of accurate modeling; ambiguity management
- Aligning multiple bounded contexts
- Integration with existing systems; perf/scale concerns
- Team resistance / learning curve

## 2.7 Classic use cases (source)

Finance/banking, e-commerce/retail, healthcare, insurance, real estate — domains with rich rules and language. **B2B sales analytics portals qualify** when reporting rules, territories, and ERP semantics are non-trivial.

---

## 2.8 DDD deliverables a Sales Portal PM should produce

Before big UI bets, ensure these exist (even if lightweight):

1. **Domain glossary** (ubiquitous language) — terms + forbidden synonyms
2. **Context map** — boxes + relationship arrows (ACL called out)
3. **Core domain vs supporting vs generic** — where to spend design talent
4. **Aggregate sketch** for the riskiest consistency boundaries
5. **ACL notes** for ERP import realities (`order_data.csv` / `invoice_data.csv` are import reporting files, not iPad orders)

### Mini template

```markdown
# Sales Portal Domain Sketch

## Core domain
What we must be uniquely good at: …

## Ubiquitous language
| Term | Means | Not to be confused with |
|---|---|---|

## Bounded contexts
1. …
2. …

## Context map
A --ACL--> B
C --Customer/Supplier--> D

## Aggregates (v1)
- Root: … / consistency rule: …

## Open modeling questions
- …
```

---

# 3. Affinity Mapping — full method + Figma template
**Figma / FigJam template:** [Affinity Mapping template (UX Anudeep)](https://www.figma.com/community/file/973596233310955890/affinity-mapping-template)  
- FigJam board, CC BY 4.0, ~9.6k users  
- Purpose stated by author: **“Use this template for organizing your research insights.”**  
- Category: Affinity diagrams / whiteboarding  
- **Open in FigJam**, duplicate for each study / stakeholder dump  

**Method authorities synthesized here:**  
- Nielsen Norman Group — [Affinity Diagramming](https://www.nngroup.com/articles/affinity-diagram/)  
- KJ Method (Jiro Kawakita); design-thinking adoption (IDEO / d.school)  
- Practice detail from Talkful’s step-by-step research guide (verbatim-first, decision-tied synthesis)

---

## 3.1 What it is

Affinity diagramming / affinity mapping / collaborative sorting / snowballing / KJ method:

> Organize related observations, ideas, concepts, or findings into distinct clusters so structure **emerges from the data** instead of being imposed top-down.

Physical or virtual sticky notes. Best done as a team (discussion + decision), though solo is possible.

**Not the same as card sorting for IA** (though related visually). Affinity = thematic synthesis of ideas/findings; card sorting = users grouping labels for navigation structure.

### When to use (NN/g)

- Observations / ideas from research
- Concepts from ideation
- Strategy / vision language
- Anytime you have too much qualitative mess and need alignment + next steps

### Success criteria

Team alignment, robust design ideas, **and a set of next steps**. The journey (discussion) often matters more than the final board photo.

---

## 3.2 Why most affinity walls die (failure modes)

1. **Paraphrase cards instead of verbatim** → clusters become researcher taxonomy, not participant structure.
2. **Top-down buckets** (“Onboarding / Pricing / Support…”) before cards exist → filing, not synthesis.
3. **Stop at the photo** → clusters without quotes + decisions = wiki debris, not roadmap fuel.

---

## 3.3 NN/g three-step skeleton (workshop shape)

1. **Generate ideas as sticky notes** (diverge; 5–10 minutes if live ideation; longer if extracting research)
2. **Organize into clusters / themes** (group by similarity first; label after)
3. **Prioritize clusters + next steps** (dot vote; owners; actions = further research, design iterations, fixes)

### Dos / Don’ts (NN/g)

- Pre-filter huge datasets to avoid session fatigue; or split into parallel groups
- Invite varied perspectives; don’t ignore outliers / small clusters
- Don’t force a magic number of clusters
- Be willing to reorganize; duplicate a note into two clusters if needed
- Don’t overcategorize

---

## 3.4 Elite seven-step research synthesis (use this for Sales Portal)

### Step 01 — Decide what decision the synthesis serves

Write one sentence naming a **decision**, not a topic.

- Good: “Should we bet six weeks on an answer-first backlog view or a chrome-only Phase 3 reskin first?”
- Bad: “What did users say about the portal?”

If data was collected without a question, **slice** the data to the decision; park the rest.

### Step 02 — Extract observations (not summaries)

Each card = **one observation**, preferably verbatim, with participant ID + source link.

Rules:
- One observation per card (split compound statements)
- Stay verbatim / near-verbatim
- Attach source (who / when / transcript link)
- Expect ~150–300 cards for 20–30 voice responses × ~5 prompts; <50 often means over-paraphrased

Sources for Sales Portal: rep interviews, CSM notes, Help Scout tickets, sales-call transcripts, screenshot annotations, internal eng/support disagreements, live Postgres-derived “what’s possible” notes (as separate color).

### Step 03 — Read the wall once before grouping

Silent familiarisation pass (~15–20 min). No clustering yet. Prevents first-ten-cards anchoring.

### Step 04 — Cluster bottom-up, silence first

Everyone moves cards without talking ~20–40 min. No labels yet.

Expect:
- 6–12 candidate clusters
- piles of ~6–15 cards
- <3 clusters → too broad; >20 → too narrow
- 1–2 card piles = not yet themes; mark outliers
- >20 card piles = probably two themes

### Step 05 — Name clusters in participants’ phrasing

Names are **sentences with a verb**, not topic labels.

- Weak: “Users care about pricing”
- Strong: “First-time visitors compare two or three plans and stall when differences feel arbitrary”

For portal: prefer “Reps export to Excel because the portal can’t answer territory concentration for the quarter” over “Reporting issues.”

### Step 06 — Map relationships + stress-test outliers

Draw arrows: cause → effect; symptom vs root; contradictions (segment clash vs true conflict). Fold outliers that share a mechanism; keep true singletons.

Negative case: each named cluster should survive at least one pushback quote.

### Step 07 — Convert into a synthesized decision

Deliverable is **what changes Monday**, not the wall.

Output structure:
- 3–5 findings (one sentence each), each tied to a decision
- 2–3 verbatim quotes per finding (with IDs)
- “Unresolved” section for outliers / contradictions / clusters that didn’t earn a decision
- No methodology theater up front; n= in footer

---

## 3.5 How to use the Figma Community template

1. Open [Affinity Mapping template](https://www.figma.com/community/file/973596233310955890/affinity-mapping-template) → **Open in FigJam** → duplicate into your team.
2. Create a board per decision (not one eternal mega-board).
3. Suggested lanes / zones to add if the stock template is sparse:
   - **Inbox (unsorted)**
   - **Silent cluster zone**
   - **Named themes** (sentence headers)
   - **Relationships** (arrows)
   - **Outliers**
   - **Decisions / bets to shape** (parking lot that feeds Shape Up)
   - **Domain language candidates** (parking lot that feeds DDD glossary)
4. Color code by source type (rep / internal / support / data fact) — never by pre-chosen theme.
5. When done: export findings into the Shape Up pitch Problem section and DDD glossary — then archive the board with a date.

Remote tip: mute chat during silent sort; cameras on; everyone has edit access.

---

## 3.6 AI assist boundaries

AI is good at: transcript → candidate cards, timestamps, first-pass topic tags, draft cluster proposals.  
AI is **not** a substitute for: silent bottom-up grouping judgment, mechanism naming in participant language, or converting clusters into bets/decisions.

Use AI for volume; humans for structure and stakes.

---

## 3.7 Affinity → Shape Up / DDD bridge (critical)

| Affinity output | Feeds |
|---|---|
| Mechanism-named themes | Shape Up **Problem** stories + baseline |
| Prioritized clusters | Betting table candidates (still need shaping!) |
| Verbatim quotes | Pitch evidence; stakeholder alignment |
| Recurring nouns/verbs | DDD **ubiquitous language** candidates |
| Contradictions by segment | Bounded context / persona splits |
| “Unresolved” | Next research question — not fake certainty |

**Never** put affinity clusters straight onto an eng backlog as tickets. Clusters are raw ideas until shaped.

---

# 4. Combined operating playbook for Sales Portal

## 4.1 Program modes (pick consciously)

| Situation | Mode |
|---|---|
| Don’t know if answer-first analytics holds | **R&D** spikes (senior); affinity on live reps + Postgres shape |
| Chrome / IA refresh with known surfaces | **Existing product** Shape Up bets |
| Domain language still mushy | Pause UI bets → **DDD sketch + affinity** |
| Pre-launch of a new analytics surface | **Production** then **Cleanup** |

## 4.2 Suggested first six weeks (example experiment)

**Cool-down / week 0 (before bet):**
1. Affinity workshop on “What decisions should Sales Portal make easy in 2026?”
2. Draft domain glossary + context map (DDD)
3. Shape **one** big-batch pitch OR two small-batch pitches (not a portal rewrite)

**Example pitch shapes (illustrative — replace with real affinity winners):**
- Small: “Territory backlog concentration answer in ≤2 clicks for CCI-shaped data”
- Small: “Invoice vs open-order date-grain clarity (kill Excel export for this one question)”
- Big: “Answer-first home: one hero metric + 3 follow-ups, ACL’d to portal_orders/invoices”

**During cycle:**
- Assign project not tasks
- Vertical slice in week 1
- Scopes on a hill chart
- Scope hammer vs baseline (Excel / status quo portal)

**Circuit breaker:** if the shaped answer doesn’t ship, reshape — don’t quietly extend into an unshaped portal rewrite.

## 4.3 Grab-bags to refuse

Refuse or split these until narrowed:
- “Sales Portal 2.0”
- “Make it like Omni/Hex/Linear”
- “Rebuild reporting”
- “Phase 3 everything”
- “Add AI”

Demand: problem story + appetite + elements + no-gos.

## 4.4 Definition of ready (to bet)

A Sales Portal item is ready for the betting table only if:
- [ ] Affinity (or equivalent evidence) supports the problem — or problem is already crystal from experts
- [ ] Ubiquitous language terms in the pitch match the domain glossary
- [ ] Bounded context is named (which model of “order”?)
- [ ] Appetite set
- [ ] Solution elements listed (breadboard/fat marker)
- [ ] Rabbit holes patched or time-bombs called out
- [ ] No-gos listed
- [ ] Done = deployed/merged is explicit

## 4.5 Definition of done (to ship)

- [ ] Vertical slices integrated; core scopes downhill/done
- [ ] Must-haves complete; `~` nice-to-haves cut or deferred
- [ ] Compared to baseline and wins for the shaped use case
- [ ] Domain terms in UI match glossary
- [ ] No silent expansion into adjacent contexts (catalog, iPad, etc.)

---

# 5. Agent instructions (fresh chat)

When the user says they’re PMing the Sales Portal refresh:

1. **Do not** jump to hi-fi UI or `supercat_server` implementation unless they explicitly say GO on code.
2. Ask which **decision** is open right now. If unclear, propose an affinity pass.
3. Prefer **Shape Up language**: appetite, pitch, bet, rabbit hole, no-go, scope, hill, baseline, circuit breaker.
4. Prefer **DDD language**: bounded context, ubiquitous language, ACL, aggregate — especially around orders/invoices/ERP.
5. Prefer **affinity discipline**: verbatim → bottom-up clusters → mechanism names → findings with quotes → decisions.
6. Treat “redesign the portal” as a grab-bag; force a narrow problem.
7. Keep outputs in chat as markdown (pitches, glossaries, context maps, findings). No unsolicited canvases unless asked.
8. If live org data is needed, use Postgres MCP read-only patterns and mask PII in comps.

### Companion artifacts in Kylor’s world (optional pointers)

If available in workspace / Downloads, also read for product-specific state (this pack does **not** replace them):
- Sales Portal analytics handoff / Phase 3 CTO brief / destination mockups
- `supercat_server` portal routes (read-only until GO)
- Live orgs historically peeked: `sarreid`, `cci` (portal_orders / portal_invoices dense)

---

# 6. Source links (canonical)

| Asset | URL |
|---|---|
| Shape Up (book site) | https://basecamp.com/shapeup |
| Shape Up PDF | https://basecamp.com/shapeup/shape-up.pdf |
| DDD (GeeksforGeeks) | https://www.geeksforgeeks.org/system-design/domain-driven-design-ddd/ |
| Affinity Mapping FigJam template | https://www.figma.com/community/file/973596233310955890/affinity-mapping-template |
| Affinity method (NN/g) | https://www.nngroup.com/articles/affinity-diagram/ |

---

# 7. One-page cheat sheet

```
AFFINITY          →  What hurts, in their words, clustered into decisions
DDD               →  What the words mean, where models stop, how ERP translates
SHAPE UP          →  How much time it's worth, what's in/out, bet, build, ship

Refuse grab-bags. Fix shipping. Shape before schedule.
Appetite ≠ estimate. Circuit breaker > sunk cost.
Verbatim > paraphrase. Contexts > global nouns.
Baseline > perfection. Scopes > role swimlanes. Hills > % complete.
```

---

*End of context pack. Start the next chat by pasting this file and stating the open decision.*
