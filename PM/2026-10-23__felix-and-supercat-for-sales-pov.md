# Felix, SuperCat for Sales, and what just happened

> **Written:** 23 October 2026, after the Tech & Product Roundup
> **For:** Kylor, coming back into the two highest-leverage bets
> **Status:** Point of view from primary sources. Not a status report. Not a plan.
> **Last updated:** 2026-10-23

This is a catch-up document. It answers four questions:

1. What are these things, actually — and how do the names collide?
2. How was Felix created, and how does it run today (not how the docs wish it ran)?
3. What is SuperCat for Sales, and what was Brent doing with the SFS board today?
4. What is the real leverage point, and what is fog?

Sources are named as they are used. Figures from other people's docs are stamped `[from-doc]`. Anything I could not verify is marked.

The Claude artifact (`claude.ai/artifact/WeXQHgJjRWSKBwzGV3vzWd`) did not load — Claude returned an empty page. The Oct 22 "Felix in plain English" note, the Oct 14 Review Plan v1.1, and Foundation & Beta v9.1 on `agent-factory` `origin/main` cover the same ground and are treated as the working set.

---

## 0. The map in one page

SuperCat's install-base center of gravity is still the **eCat iPad app** — an Objective-C selling instrument, fully offline, used by most of the book. That is the old codebase. Two new things are being built to replace and outgrow it.

| Name you will hear | What it actually is | Repo / home | Who owns the runtime |
|---|---|---|---|
| **SuperCat for Sales** | The new selling instrument: a Hotwire Native iOS shell wrapping a new Rails catalog (eCat Web / `ecat_web` flag). | `SuperCatSolutionsLLC/supercat_for_sales` (native) + `supercat_server` `spike/ecat-web` / `staging` (web) | Brent |
| **Felix** (also **Sales Assistant**, also **Rep Assistant**) | The AI sales partner for a manufacturer's assigned field rep. A chat that is supposed to help cover the book and win the visit, grounded in tenant commercial data. | Factory law: `agent-factory/agents/sales_assistant/`. Runtime: Rails `RepAssistant::*` on staging. | Product intent: Kjael. Rails: Brent. Harness/evals: Kevin. |
| **`supercat_ds`** | The design system both of the above consume. Vilni (Alex) owns it. Felix has its own gold / gradient mark. | `SuperCatSolutionsLLC/supercat_ds` (v4.6.2, 21 Oct) | Alex Malyshev / Vilni |

They meet in one native chrome. It is **not** four equal tabs. The code is explicit:

```
  [ Catalog ]  [ Orders ]  [ Scan ]     ( ○ Felix )
       glass capsule                         circle
                    │
        Hotwire Native iOS shell
        loading Rails eCat Web pages
        from staging.k8s.supercatsolutions.com
```

`EcatTabs.swift`: Catalog, Orders, Scan, then Felix last. `EcatTabBarController.swift`: "the capsule draws the first three, the circle beside it draws Felix." Felix's URL is `/{org}/e/{mobile_site}/rep_assistant/conversations`. After sign-in the catalog opens at `/{org}/e/{mobile_site}/products`.

That is the whole architecture. SuperCat for Sales is not the Sales Portal rewritten. It is the attempt to move the company's most important surface onto a new codebase before December 1, with Felix as the gold circle. The Sales Portal remains HQ analytics. eCat Online remains the buyer web catalog, and must not break when the `ecat_web` flag is off.

**A naming collision you must not blur.** There is a second, older "Felix": an internal SuperCat support LLM (HelpScout / ticket research). That is `EBR-695` / `SERV-2269` (`/maketicket`). It is not this product. When a 2025 ticket says "Felix," check the project. Customer-facing Felix is the Sales Assistant.

**A second collision, from today's call.** Kjael also said Felix should eventually be trained on the SuperCat-for-Sales codebase so "how do I do this" questions route there, and that ideally there is no KB 2.0 — just natural language. That is Felix-as-product-help. It is a later, different job from Felix-as-sales-partner. Do not let the help-desk version dilute the partner version.

---

## 1. The POV, before the history

Four things are true at the same time.

**First.** These are the right bets. The iPad is the product. A new selling instrument that also runs on phone and desktop, plus an agent that can sit inside a real visit, is the only path that widens the moat rather than polishing the old app. Foundation already named the field sales assistant as a bounded context that must share commercial truth and must not invent its own meaning of "rep ownership." WizCommerce already ships Kai. SuperCat's answer cannot be "we have a chatbot with six buttons."

Brent said the deeper reason out loud today, and it is the 10-year bet hiding under December 1:

> The reason a lot of the things that we've thought about are really hard is because we have an iPad involved. So if we own the website and you can just configure it, we can preview it. We can do all these things you just can't do with a native app.

The stretch he named: *you don't need to onboard with us — you can just sign up and use it.* That is a traditional SaaS company. SuperCat for Sales is the front-end of that. Felix is the intelligence inside it. Admin/sandbox (spreadsheet instead of FTP, live preview, hang-tag-style field placement) is the track *after* Q1. Sequencing SuperCat for Sales first is how the later tracks become possible.

**Second.** The company is earlier than the documents sound. The factory canon (Foundation & Beta v9.1, Execution v10, G1–G7 scorecard, HARNESS.md, `releases/felix-v0.json`) is unusually good. It is also mostly a plan. As of this afternoon:

- Felix's six typed tools live on **staging / `spike/ecat-web`**, not on `master`. Those two branches are the same commit: `e87135475`, 15 Oct, "Improve Felix customer picker UX." Production `master` moved today (`#2667`, Lib&Co export) and still has the June hybrid (`query_territory_data` + old canned tools). On `master`, access is **`is_admin?` only**. On staging eCat Web, access is the org flag `ecat_rep_assistant` or the `ecat_rep_assistant` feature flag, plus visibility, and buyers are blocked. Superadmin is not the only seat on staging. Whether a non-admin can actually open it today is still unverified by me — I did not invoke staging.
- All seven release gates (G1–G7) are **OPEN**. `felix-v0.json` exists as a development baseline. It pins the staging SHA, Anthropic `claude-sonnet-4-6`, and says every gate is open. No external beta is authorized.
- Observe (C1) is `not_implemented`. `#2626` was closed unmerged. Replacements `#2668` / `#2669` are still open against `staging`. Langfuse is the intended flight recorder. Prompts still live in Rails; Langfuse serving is "not configured."
- A reply-guard and `never_say.yml` are pinned in `felix-v0` as R5 "implemented." That is not G1. The typed claim-binding contract is explicitly "not yet proven."
- No working rep has used Felix as a working tool. High Point was a demo. The 19 Oct review was local Rails turns on one pinned Kuzco account.
- SuperCat for Sales has a TestFlight native shell (internal, ~12 Oct `[from-doc]`) and a web catalog behind `ecat_web`. The SFS board is 21 tickets, all created yesterday, all still `To Do` / `Unprioritized` tonight, all labeled `dec-1` / `ecat-v2`. That is a Dec 1 catalog/navigation/pricing slice, not a finished product.

**Third.** The failure mode in front of you is not "we don't know what to build." It is **two clocks running on one company, now spoken aloud, without a named join.**

Today Brent put dates on both, in the same whiteboard:

| Clock | Date Brent said | What "done" means in his words | Who |
|---|---|---|---|
| **A. SuperCat for Sales** | **December 1** — "we kind of opened our mouth and said to VCG" | Close the demo gap. Parity with eCat. Turn it on for specific users/orgs. Reps can write orders. Artifacts (lists/PDFs) start generating on the server. Analytics wired. Legacy eOL with the flag off never breaks. | Brent, Kyla, Jon, Alex/Vilni, Lucas, QA |
| **B. Felix quality** | **Q1** — "by Q1, we have confidence in the quality of Felix, it's data, it's not hallucinating, and it has a very specific honed perspective" | G1–G7 signed. A named 6–10 rep cohort. A wrong number cannot reach a buyer. | Kjael + Kevin ("lane views" / grading). Brent merges Rails. |
| **C. Admin / sandbox** | After that | Spreadsheet instead of FTP. Live preview. LLM-assisted product file. Hang-tag-style "put these fields on the card." Slim the 18-tab admin. Sign-up-and-use. | Named as the next platform track, not this quarter |

Kjael drew the whiteboard as two colors: **blue = platform, the other = agentic.** Felix "absorbs pretty much everything" as a new front end to catalog / ordering / history / artifacts / library — eventually. December 1 is not that. December 1 is the platform track closing the demo gap.

**Fourth.** Trey already heard about Felix "from around town." You said that in the first ninety seconds, after cancelling LeGron. The market is ahead of the gates. That is a gift and a risk. Do not let a rumor become a commitment.

If you only take one action from this document: **name the join, in a room, in one sentence.** Who decides what December 1 must include, what Felix is allowed to be on that date (working gold circle vs. partner a rep may quote), and who is allowed to slip which clock. A default is in §9 so you are not asking.

---

## 2. SuperCat for Sales

### What it is

A **new codebase** that is trying to become the selling instrument. Two halves, one product, plus the design system.

**Native half** — `supercat_for_sales`. Seven commits, all Brent, 3–13 Oct 2026. Last push 13 Oct. Hotwire Native (the Basecamp pattern: native navigation chrome, web content). Default host `https://staging.k8s.supercatsolutions.com`. Login is the existing SuperCat session (`/supercat/sessions/new`); after sign-in, org + mobile site drive every tab. Path configuration is a JSON file that tells the shell which URLs are tab roots, stacks, modals, or Felix. Native work that cannot be web: barcode camera, keyboard-wedge scanner, floating tab chrome, session gate, phone-call / email bridges, scan-order as a pushed stack. CI: unit tests on PR; Fastlane beta to Firebase / TestFlight on push to `main`. Bundle ID `com.supercat.supercatforsales` (Fastlane still signs `com.supercat.Supercat-For-Sales`). Internal TestFlight existed around 12 Oct `[from-doc]`.

**Web half** — Rails eCat Web, feature flag `ecat_web`, living on `spike/ecat-web` which currently **is** `origin/staging` (`e87135475`, 15 Oct). This is the actual catalog: products grid, PDP, cart, customer picker, quotes, saved orders, scan, library, lists, and the Felix conversation pages. When `ecat_web` is on, Felix uses the `ecat_v2` layout. Legacy eCat Online must keep working with the flag off. That constraint is written into every SFS ticket's definition of done.

**Design half** — `supercat_ds`. "The design is the specification" is the ticket text on SFS-20, and Brent said it on the call: *don't make Alex update every button like a monkey; the developer's job is to map the design to the system.* Products vendor a released version and are forbidden from writing local visual CSS. Latest release is **4.6.2 on 21 Oct** (Alex): big-screen nav rows, Felix's glow dithered with a band under the composer instead of a tinted veil, catalog filter collections as a checklist. Felix's mark, composer, and direct actions keep gold / gradient across app styles; everything around them stays ordinary style roles.

### What it is not

- It is not the Sales Portal. Portal is HQ (dashboards, invoices, territories). SuperCat for Sales is the rep (and buyer) selling surface. Sales-portal data on the customer chooser was explicitly **punted** today.
- It is not a rewrite of the Objective-C iPad app. Kjael said this at the end of the call and it is the load-bearing frame: **eCat is iOS; SuperCat for Sales is a new codebase.** Old iPad bugs do not automatically apply. Old *feature requests* and *admin-setting contracts* do.
- It is not finished. Native last moved 13 Oct. Web last moved 15 Oct. Foundation called `spike/ecat-web` "open, 223 commits across 948 files, conflicts" as of 14 Oct `[from-doc, unverified today]`.

### Why December 1 is the date

It is not a board-stamped launch memo. It is a promise. Brent, today:

> We kind of opened our mouth and said to VCG, December 1st is a first release. So we kind of focused high level on like December 1st. We have to close the demo gap. So stuff that is in Alex's demo that's not on SuperCat for Sales needs to be built. And the maxim there is like we need parity.

SFS-19 restates the constraint: the iOS app must work on real devices **before 1 December**, and legacy eCat Online with the flag off must never be disrupted. Treat the date as a customer-facing commitment to VCG plus Brent's working target. I did not independently confirm what VCG was shown.

"Parity" on the call meant: work like eCat, do not add new users or a new product category, turn it on for specific orgs/users. One exception was named and celebrated: **applicable-only filters** (SFS-26/27) are "nice sauce," not eCat parity — eCat lets you filter yourself into zero results. Brent is working the performance spike now and said it may slip past December 1 if it is slow.

---

## 3. The SFS board, and what Brent was actually doing today

**Meeting:** Tech & Product Roundup — 23 October, 44 minutes. [Fathom](https://fathom.video/calls/871819569) (share URL in BQ: `https://fathom.video/share/axz3Y6JjVuzu_-JAftr_8zpzGGWmUvm-`). Invitees on the recording: Brent, Kylor, Kjael, Angela, Kyla, Jon, Alex (Vilni), plus Olga, Kevin Lewis, Emery Rust, Lucas. Spoken: Brent, Kylor, Kjael, Angela, Kyla, Jon, Alex. Kevin was invited and did not speak; he is the Felix harness owner, not this agenda.

I have the full transcript from BigQuery (`Fathom.call-transcripts` ID `135607689`, 48,170 characters). The tickets *and* the talk are the middle.

### The operating idea Brent is installing

He said it three ways, and they are one idea:

> We're trying to flatten this and use LLM so we can all contribute.

> I'm trying to get out of writing the tickets. I'm just going to be honest, guys.

> We talk about something, it's recorded, we don't have to write it separately. And then if we can get the test thing working, that's sort of the holy grail.

The loop:

```
working session (recorded, walking Alex's designs or the demo)
        → LLM PM helper skill writes SFS tickets
           (plain English, no T1/T17 codes; shared concepts live
            in a Shared Concepts / "kernels" doc — Kjael's word)
        → tickets carry Why / Scope / AC / Gherkin examples /
           starting-point file paths / t-shirt size /
           "design is the spec unless overridden" /
           DoD = external QA test + iOS check + ecat_web flag
        → SuperCat PDV (post-deployment verification):
           Kyla / Jon record a Loom + a Playwright session
           on demo fixtures, not live customer data
        → that becomes both the ticket and the regression
        → Brent deploys, the suite runs, sanity instead of Olga-memory
```

He wants this **gamified**: weekly "stump the suite." Credit for the person who finds the thing the tests do not have — Bulbright contract pricing, Hubbardton Forge, Jonathan Charles, the configuration that only one customer uses. His line: *data and configuration are more important than code.* Isolated unit tests prove one-plus-one. PDV proves what production actually does.

That is why the tickets look the way they do. They are not engineering tasks. They are executable requirements, written so a recording plus a design file can produce them again. The skill lives in Confluence and was shared in the product channel. I did not fetch the Confluence page.

T-shirt sizes, as he defined them: Small = less than a day, Medium ≈ a day, Large = a couple of days, XL ≈ a week — and he wants the estimate to be *group-through-production*, not developer-time, because "the developer writing the code is now probably the shortest part."

Jon and Kyla both liked it. Kyla asked two things that matter: (1) will Playwright catch the console/error why, and (2) documentation has to ship with the new UI — do we keep a KB, make a 2.0, or let Felix answer it. Kjael: train Felix on the codebase; ideally no KB pass. You: "I just broke my brain thinking about that." Park it. It is a real question and it is not this quarter.

### The board he stood up yesterday and walked today

Project `SFS`, 21 issues, keys **SFS-14 through SFS-34** (nothing exists below 14). All created **22 Oct 16:18–16:19 ET** by Brent, in one burst. All still `To Do` / `Unprioritized` this afternoon. Stories SFS-20 through SFS-32 were touched again **today 11:51–11:55 ET** during or just after the roundup — descriptions tightened, not status changed. Reporter: Brent. No assignees. Jon and Alex 404'd the first link; Kjael told people to search "SuperCat for Sales" inside Jira. Brent will grant access.

Five epics, fifteen children. Kjael: *don't over-taskify — these are the four big beats, and Release Quality is persistent.*

```
SFS-14  Shell and Navigation
        SFS-20  Navigation labels + default order          [Small]
                org-renamed "Library" → "Customer resources"
                "the design is the specification"
        SFS-21  Unified nav: web hamburger vs iOS tabs?    (spike)
                Brent on the call: native tabs may be a bad idea
                because now there are two navs. "We just need
                an everything-else nav."

SFS-15  Customer Context
        SFS-22  Customer chooser (search, sections,
                switch-with-cart confirmation)             [Medium]
                Out of scope today: sales-portal data on the row
                (targets, credit). Switching with 3 lines for
                Carroway saves a draft. Buyers never see it.

SFS-16  Catalog Browsing
        SFS-23  Infinite scroll (restore; Alex designed
                pagination; "how it works in eCat now wins") [Small]
        SFS-24  Quick sort + sort modal                    [Small]
        SFS-25  Text search parity with legacy eOL         [Small]
                "rustic chair" → fields containing both words
        SFS-26  Spike: applicable-only filter performance  [Large]
                2-day timebox. Brent is on it now.
                May slip past Dec 1.
        SFS-27  Filters show only applicable values        [Large]
                depends on 26. "Nice sauce," not parity.
        SFS-28  Taxonomy nav + breadcrumbs                 [Medium]

SFS-17  Product Card Actions
        SFS-29  Quick cart on the card (options → picker)  [Medium]
        SFS-30  Save to List (reps) / Project (buyers)     [Small]

SFS-18  Pricing
        SFS-31  Pricing + customer-context regression
                tests FIRST                                [Small]
        SFS-32  Price View modal (showroom mode)           [Medium]
                Display markup never changes the cart.
                Depends on 31.

SFS-19  Release Quality
        SFS-33  Legacy eOL flag-off regression suite
                (new external project — SuperCat PDV —
                not more tests in supercat_server)
        SFS-34  iOS device-matrix QA pass
```

Read the board as a product argument:

1. **Customer context is the spine.** Who the customer is decides prices, cart, and what the rep can see. Switching with lines in the cart must save the old order as a draft. Buyers never see the chooser.
2. **Pricing is the most damaging bug class**, so tests lock current behavior *before* the Price View UI moves. Display markups never change the cart price. That is eCat's oldest invariant, restated for a new surface.
3. **Catalog must feel like eCat Online**, not like a redesign that paginates. Infinite scroll, search parity, taxonomy breadcrumbs. Applicable-only filters are the one licensed improvement, and they are allowed to slip.
4. **Legacy must not move.** Flag-off eOL gets its own external Playwright suite. The new app does not get to borrow safety from the old one.
5. **Admin settings must express.** Org-renamed "Library" → "Customer resources" has to show up. This is Kjael's point from the end of the call, already in SFS-20.

What is *not* on the board: Felix quality, offline, a menu builder, advanced search, related-items quick cart, native-tab-vs-hamburger as a decision (that is the SFS-21 spike). Brent's own sizing of what *is* on the board: "maybe a week, week and a half, maybe two weeks." Then, in about three weeks, "everything under the sun in Jira that's part of this new SuperCat for Sales," and *then* RICE scoring against the six-year backlog. These tickets will all score high because the product has to work.

### Your Jira question, and Kjael's correction

You asked whether the new tickets contemplate previous Jira — bugs, feature requests. Brent: *not at all. That would be a great LLM cast.* You offered to pull existing requests against this direction and come back with a point of view. He said yes, after the current slice, with RICE.

Kyla's caution, which you should carry when you do that pass: a lot of old tickets look like front-end and are actually data-infrastructure. Numeric filters. Server processing. Database shape. Brent's worked example: Bulbright contract pricing — no other customer has it; Hubbardton Forge and Jonathan Charles are the same class. You cannot place those orders on production to find out. The PDV answer is **fixtures** (a Bulbright-like environment), not a tour of live orgs. He also pointed at a Felix-shaped version of the same problem: *you've run into this with Felix — we can't query certain data, we have to have that in the ETL.*

Then Kjael's frame, the last ninety seconds, which you restated correctly:

> eCat is written in iOS. SuperCat for Sales is a new codebase. It still needs to connect to the admin portal. It is useful to mine Jira for OG — less bugs, because those bugs surely apply to a codebase we're moving away from. Maybe feature requests to add density. Admin settings expressing in SuperCat for Sales and making sure that works.

You: *focusing less on bugs than more on feature requests that are actually legitimate.*
Kjael: *Yeah.*

That is the right frame and it is already half-in the tickets (SFS-20 org labels, SFS-31/32 price view, SFS-22 customer switch). The risk is the other half: if the team treats SERV/ECAT history as a bug backlog to port, they will rebuild the old app's scars on a new stack. Mine **admin contracts and requested capability**, not crash reports.

### Next steps Brent asked for, on the call

- **Two or three more sessions this week** to step through Alex's designs and keep collecting requirements. He will throw times.
- **One or two sessions with Jon and Kyla** to stand up SuperCat PDV / Playwright and let them capture a couple of tickets themselves.
- Grant Jira access to whoever 404'd.
- You, in the background if you want: the old-Jira density pass. He did not make it a Dec 1 gate.

### What this meeting was not

It was not a Felix review. Felix appears as the gold circle, in `#2661` as demo polish, and on the whiteboard as the agentic color and the Q1 quality clock. The SFS board does not contain a Felix epic. Clock A is what Brent was running. Clock B is what Kjael was writing yesterday and is running with Kevin. They were in the same Zoom. They were not the same agenda.

---

## 4. How Felix was created

Felix is not one invention. It is four layers laid on top of each other, each of which is still visible in the code. If you read only the latest plan you will think the earlier layers were replaced. They were not. They were wrapped.

### Layer 1 — Doctrine and simulations (summer 2026)

Home: `agent-factory/agents/sales_assistant/`. Local checkout on this machine is **stale** (22 Sep). Everything below is from `origin/main` (fetched today; tip `a366727e`, 23 Oct).

Kjael's factory built a **field sales assistant** as SuperCat's primary product priority. The product law in `OVERVIEW.md` is still the best description of what Felix is *for*:

- Buyer: the manufacturer's sales leadership, who pays for SuperCat.
- Recipient: an assigned manufacturer field rep. Not a manager. Not a buyer. Not SuperCat.
- Two jobs only: **cover the book** (who is quiet, who is nearby, who is assigned-and-dark) and **win the visit** (prep, bag, social proof).
- Substance, not a closed API: six atomic questions that a bad prompter can tap, and that a free-text turn of the same kind must still hit.

| ID | Rep question | Job | Minimum useful answer |
|---|---|---|---|
| #1 Prep | Prep me for this customer | Visit | Identity, mix dollars, Going in |
| #3 Show | What should I show? | Visit | Short ranked bag, price, stock, SKU-specific why |
| #4 Similar | What are similar customers buying? | Visit | One expansion opening + actual vs expected $ |
| #6 Nearby | Who else nearby? | Book | Eligible stops, or honest empty |
| #2 Attention | Who needs attention this week? | Book | Prioritized list with a reason |
| #5 New accounts | Where are new opportunities? | Book | Assigned-and-dark only |

Honesty rules were written before the chat existed, because the factory had already been burned: eCat GMV treated as total business, ZIP-3 treated as miles, "not in your book" treated as dormant, designer accounts put on a reorder cadence, other-rep books leaked. `CONTRACT.md` still owns never-emit (query ids, lens names, ownership class tokens, assignment proof, ZIP-3 counts, the word `eCat` as operator machinery). Compile strips operator language. The model is not allowed to invent price, stock, or ownership.

What existed in this layer: authored six-turn **simulator packets** (Markdown / PDF) for design partners, a typed **evidence engine** against read-only Postgres, and a live-prep / live-wave-a path for Prompts #1 and #3. What did not exist: a hosted chat a rep could open. `SKILL.md` is still the simulator author. It is explicitly **not** the product.

August 31 is a scar worth remembering. Kjael rejected the latest simulations as "substantially diminished." The live path had no model-driven synthesis — it was templating advice from a thin profile. Usefulness and honesty are different gates. Passing tests did not mean a Craftmade rep would use the answer.

### Layer 2 — Brent ships a Rails agent (June)

Home: `supercat_server` `RepAssistant::*`. Ticket: `SERV-2424` (Done, Brent, created 16 Jun, closed 22 Jun). PR `#2556` ("Feature/rep agent prototype") merged 19 Jun.

This is the runtime that still runs.

Brent's insight was architectural, and it is still the security model: **you cannot enumerate every question a rep will ask, so you do not try.** You give the model a `query_territory_data` tool that writes a SELECT, and the server **always** prepends the existing `WarehouseAccess` territory CTE, injects the org filter, validates read-only SQL, runs in a read-only transaction with a timeout and a row cap, and asserts the result is still in scope. Identity flows down from the session. The model never gets to say *who* it is querying as.

Canned tools (`customer_profile`, later catalog / inventory / enrollment / presentations) were a fast path for quality, not for security. The chat was Turbo Streams, mobile-responsive, Anthropic, voice input. Access on production `master` is still **`is_admin?` only**. There is no sidebar link. The URL is:

```
https://app.supercatsolutions.com/{org}/{mobile_site}/rep_assistant/conversations
```

On 19 Jun Brent posted a gap-closure comment on `SERV-2424`: claim rules, tone guidance, a 6th canned prompt (`nearby_accounts`), declining-velocity / inventory-cross-ref / category-whitespace / coverage-gap workflows. Eighteen tests green. That is the June agent. It is what production still is.

The Review Plan's early clue is exactly this layer: "the Rep Assistant implementation document describes a hybrid of flexible territory-scoped SQL and canned tools. That architectural intent must be checked against staging behavior; it should not be treated as proof that flexible exploration is working."

### Layer 3 — Six typed jobs on the warehouse (September–October)

The factory then tried to replace free SQL for the six jobs with **typed facts packets**. Prep / Show / Similar / Nearby / Attention / New accounts were specified as handoffs. Membership is territory on the buyer file. Headline dollars are membership-visible on the channel register. One door or a location list with no dollars. Never invent stock.

PRs `#2635`–`#2637` (typed Prep / Show / Similar) were **closed unmerged** on 29 Sep. Brent replaced the stack with `#2647` — **Add the six Sales Assistant tools on WarehouseAccess** — merged **5 Oct into `spike/ecat-web`**, not into `master`.

Staging today registers thirteen tools. I read `origin/staging:app/services/rep_assistant/tool_registry.rb`:

```
prep_account
show_account
similar_account
nearby_accounts
attention_account
new_accounts
query_territory_data          ← the June escape hatch, still live
catalog_search
inventory_lookup
customer_profile
enrollment_pipeline
generate_presentation
record_account_note           ← added for High Point
```

Two more tool *files* exist on staging and are **not registered**: `add_to_order.rb`, `set_order_customer.rb`. That matches the "cart tools were pulled for High Point" note. They are on disk. They are not in the model's hands.

So the "six starters" you will hear argued about are real, but they are **not the whole agent**. Free SQL is still registered. That is why the 19 Oct review could invent a stall story: the model can still wander.

`#2657` / `#2658` (12–13 Oct) hardened Felix for the **High Point demo (Thu 15 Oct)**. The load-bearing fix in `#2658`: warehouse queries on customers, ship-tos, orders, and invoices were org-scoped only. A Craftmade territory rep asking "How many accounts do I have?" was told **5,600 against a book of 197**. `CustomerScopeFilter` now adds the rep's customer condition. Failures that used to kill the stream mid-turn (warehouse drop, Anthropic 529, timeout) now fail closed to the model. Notes became writable.

`#2661` (still **open**, against `spike/ecat-web`, created 14 Oct) polishes Felix for the **native app / TestFlight**: "All customers" as a default so a book-level question is not forced through a customer chip; clearer starter labels; ChatGPT-style suggestion chips; cancellable pickers. Server-rendered, so it reaches the iOS app on a staging deploy with no app rebuild. If you open TestFlight Felix and the customer chip still forces an account, this PR is not deployed.

### Layer 4 — The partner thesis and the harness (14–22 Oct)

This is the layer you walked into.

**14 Oct — Review Plan v1.1** (the Word doc). Working hypothesis, not a conclusion: the company may have over-invested in six canned prompts and tightly scoped retrieval, relative to reusable domain context, semantic understanding, proactive intelligence, sustained conversation, and authorized action. The question the plan exists to answer:

> Are we building the right thing? Are we building it the right way? What should we do differently?

Five phases: recover commercial intelligence independently of the six starters → define the partner experience → audit staging against that north star → pressure-test ~15 real situations → make 3–5 investment decisions. The CTO's point, carried into the plain-English note: **getting traces flowing is the easy part; deciding what the tests check is the real work.**

**19 Oct — pinned local review** (Kuzco, one account, local Rails turns). Seven failures. Six of them are not prompt problems:

| Job | What Felix did | Class | Harness part |
|---|---|---|---|
| Prep | Invented a product-code gloss from "Newport CBOX" | Invented meaning | Verification |
| Show | Invented collection history (Lorna) | Invented history | Verification |
| Attention / Nearby | Whole-account revenue attributed to a leading category | Wrong subject | Verification |
| Similar | `in_lane` read as "in line" | Field misread | Tools |
| New accounts | `timing: open` became "quiet" or "first order" | Status upgraded | Tools + verification |
| Unscripted | A stall narrative the data did not support | Unsupported causal story | Orchestration + instructions |
| Returning account | Showroom note was retrieved; advice ignored it | Constraint not applied | Context |

The review's own limit, which Foundation states cleanly: this does **not** prove the six jobs are the wrong product, does **not** prove a welcome or visit-capture is valuable, and does **not** prove staging or multi-manufacturer readiness. It proves that **correct digits attached to the wrong noun will reach a buyer unless something deterministic stops them.**

**20–21 Oct — Foundation & Beta v9.1 + Execution v10** on `agent-factory` `origin/main`. Canonical *working* product document. CTO ratification of ADR 006 still pending. The thesis, in Kjael's words:

> A capable analytics chatbot leaves the rep responsible for knowing what to ask. A sales partner shares responsibility for knowing what deserves attention and what to do about it.

The six jobs stay as the **regression floor**, not the ceiling. The beta concentrates on **before the visit and in the conversation**. Unprompted welcome, visit capture, cross-session memory, and writes are hypotheses or concept tests — not funded until beta evidence says so. D2 is decided: Rails `Sales::*` is the fact path; do not port `pipeline.py` into production. D5 is decided: no unprompted welcome in the beta. D17 is decided: prompts may move to Langfuse (CTO endorsed 21 Oct) only behind a test-gated promotion step. D4 (name the owners) and D12 (how Felix reaches iPad reps) are still open.

The harness is the operating system for that bet. Six runtime layers on every turn (R1 tools, R2 context, R3 instructions, R4 orchestration, R5 verification, R6 presentation) and three control functions across turns (C1 observe, C2 evaluate, C3 release). Safety is deterministic in tools, verification, and actions — never "we told the prompt not to."

**22 Oct — "Felix in plain English."** Kjael translating the harness for himself and for anyone who already runs CEO-system agents. The difference that matters: with the CEO system, *you* are the reader and you catch mistakes by eye. With Felix, reps read the answers and you never see them. So traces, test cases, scores, and launch checks have to become a system. His job this week, as he wrote it: get into Langfuse, ask Brent whether Felix is on staging and who deploys it, name owners he will not hold himself (especially context and releases), book Stage 0 decisions, look at one trace for twenty minutes.

**22 Oct — `releases/felix-v0.json`.** The first release record. Status: `development`. Pins `spike/ecat-web@e87135475`. Pins the factory SHA. Pins the model. Every gate open. Rollback owner: null. This is the receipt the loop is supposed to write every time. It exists. It has not passed anything.

That is how Felix was created. Doctrine first. A secure-but-loose Rails agent second. Typed jobs third, on the new web branch. A partner standard, a quality loop, and a development release record fourth — after the demo and the Kuzco review showed that the jobs can be fluent and still be wrong.

---

## 5. How Felix runs — the honest current path

### What a turn does today (staging)

1. Rep is in eCat Web or the TestFlight app, signed in as an org user, looking at a customer (or, if `#2661` is on, "All customers").
2. They tap a starter or type free text. The request hits `RepAssistant::ConversationsController` / `MessagesController`.
3. The controller builds a **frozen Scope** from the session (`org_user_id`, territories, org). Masquerade, if a superadmin is sitting in a rep seat, scopes to the impersonated org user. The model never sees identity as a parameter.
4. Access check: on eCat Web, not-buyer + visibility + (`org.ecat_rep_assistant?` OR feature flag), or admin. On the June layout (flag off / `master`), admin only.
5. `RepAssistant::Agent` loads the thread, builds context (`context_builder.rb`) + system prompt + the thirteen tool definitions, calls Anthropic (`claude-sonnet-4-6` per `felix-v0`).
6. The model picks tools. Typed jobs hit `Sales::*`-shaped packets (`prep_account` etc.) on `WarehouseAccess`. Anything else can still hit `query_territory_data` (validated SELECT + CTE).
7. Tool JSON goes back to the model. The model writes the reply. A reply-guard / `never_say.yml` / `claim_rules.md` run as they exist today — pinned, not G1. Turbo Stream renders it. A turn can take on the order of **20 seconds** locally for Prep `[from-doc, 21 Oct HARNESS / Foundation]` — almost all of it the second model call, not the query (~0.3 s).
8. Conversation rows persist under the org user in the session.

There is **no versioned context recipe** and **no named context owner**. There is **no Langfuse span** on staging or production. Prompts still live in Rails. The release record exists and has passed nothing.

### What the four places are (Kjael's table, still correct)

| Place | What it is | Who changes it |
|---|---|---|
| **`supercat_server`** (Rails, staging) | Where Felix actually runs | Brent merges |
| **`agent-factory/agents/sales_assistant`** | Rulebook, test cases, decision records, `felix-v0` | Kjael / Kevin can merge docs; runtime law needs review |
| **Langfuse** | Intended flight recorder, test lab, later prompt store | Not operational for Felix yet. C1 `not_implemented`. |
| **Execution Guide + Jira** | Checklist. Jira status is explicitly *not* evidence of a gate. | Everyone ticks their own |

### What is not true, however often it is implied

- Felix is not on production for reps. Production `master` is the June agent, admin-only, without the six typed tools. Do not poke production and think you are testing the product.
- The six starters are not the product. They are the first grammar and the eval floor. Foundation is explicit: if Felix's best answers would be just as good with no knowledge of the situation, we built the chatbot.
- A merged PR is not a launch check. `#2658` fixed the 5,600-vs-197 leak and "merged 10/13 without recorded review." Cross-tenant isolation (`#2625`) is still an open draft.
- "It's in Jira" is the red flag Kjael wrote down. G1–G7 require traces, isolation reports, a live non-admin journey, and a signed scorecard.
- The factory Python evidence engine is **not** the beta fact path. D2 decided Rails `Sales::*`. Do not port `pipeline.py`. The older "W2 migrate to Python" packet is superseded.
- Intelligent Presentations (the customer-facing letter) is a later reuse of the same commercial truth. It is not a gate on Felix and must not share authored prose with the rep.
- Felix-as-KB-replacement (today's aside) is not Clock B. Clock B is "a rep may repeat this number to a buyer."

### Who does what, if the harness is taken seriously

| Part | What it decides | Owner named in the docs |
|---|---|---|
| R1 Tools | What each field means | You specify; Brent builds |
| R2 Context | What Felix is told each turn, and what wins | **Not named.** This is the hole Kjael flagged. "Not Brent." |
| R3 Instructions / skills | How it speaks, per job | Product lead (Kjael, for now), via Langfuse once gated |
| R4 Orchestration | Who, which account, which tools, when to stop | Brent + Kevin (ADR 005 amendment pending) |
| R5 Verification | Block claims with no fact behind them | Brent builds; Kevin judges |
| R6 Presentation | Conclusion first; one next step; no writes | Product DRI |
| C1 / C2 Observe & evaluate | Traces, scores | Kevin |
| C3 Release | Manifest, flags, rollback | **Not named** |

The 19 Oct failures live in tools, context, and verification. "Just fix the prompt" is the wrong move on six of seven. That is the whole point of the harness. It is also why "every task landing on Brent" is the red flag in the plain-English note: he already holds R1, R4, and R5.

---

## 6. How the two bets join — and where they currently don't

### Where they already join

- **Same app.** Felix is the gold circle. `#2661` is explicitly "polish Felix for the native app demo." A staging deploy of Rails reaches the TestFlight app without a rebuild.
- **Same customer context.** SFS-15/22 is the chooser Felix also depends on. If the selected account is wrong, Felix's "context before questions" principle is fiction.
- **Same pricing spine.** SFS-31/32. Felix quoting a price the catalog does not show — or a Price View markup the cart will not honor — is a trust-killer that no prompt can fix.
- **Same design system.** Felix's gold mark is already a DS rule (4.6.1/4.6.2 this week). The catalog is the `app` surface. Vilni is on both.
- **Same admin.** Flags, user groups, org labels, price levels, territories. Kjael's "admin settings expressing" is the integration test for both bets.
- **Same warehouse / ETL constraint.** Brent said it to you on the call: Felix cannot query what is not in the warehouse. SuperCat for Sales cannot show what is not in the catalog. The fixtures problem and the Felix data problem are cousins.

### Where they do not join yet

- **Different definition of done.** Dec 1 success is "catalog + cart + customer + price view work on a device, legacy eOL untouched, VCG can be turned on." Felix success is "G1–G7 signed, a named 6–10 rep cohort, a wrong number cannot reach a buyer" — and Brent himself put that in **Q1**. Those are not the same date and should not be.
- **Different evidence.** SFS is accumulating Given/When/Then and will accumulate Playwright. Felix is accumulating doctrine and has a development release record with every gate open. Do not let either team borrow the other's artifacts as proof.
- **Different risk.** A late filter facet is embarrassing. A Felix "first order" said to a buyer who has never bought is a relationship event. The harness exists because the second risk is a different species.
- **Unnamed owners on the Felix side.** Context-recipe owner and release owner are blank. Brent is already the merge bottleneck.
- **Two Felix jobs in one name.** Sales partner (Clock B) versus product-help / KB replacement (today's aside) versus the old internal support bot (`EBR-695`). Three products. One word.

### The competitive and commercial why (so the join has a purpose)

Foundation still positions SuperCat against WizCommerce as **analytical intelligence vs. generative AI**, with the Insights Layer as the T3 differentiator. Felix is the first time that intelligence is supposed to show up *in the visit*, not in a CS-authored report.

If SuperCat for Sales ships as a prettier catalog and Felix stays a demo circle, we have spent the company's two highest-leverage bets on a redesign — and we have still made the 10-year bet possible, because the web surface is the one that can grow an admin and a sandbox. That is not nothing. It is also not the partner.

If Felix ships fluent and wrong, we have spent them on a liability, and Trey has already heard the name.

The only version that is worth this much attention is: **a new selling instrument the install base can move to, with a partner inside it that is allowed to speak only when the facts will survive contact with a buyer.** December 1 is the instrument. Q1 is the partner. Do not swap those dates.

---

## 7. What is fog, on purpose

I watched the whole Fathom via the BigQuery transcript. If a decision was made that contradicts the board (a date change, a cut, an owner), it is not in Jira as of this afternoon — every SFS issue is still To Do / unassigned. The VCG December 1 promise is verbal, from Brent, on this call. I did not confirm what VCG was shown or who said it to them.

I did not invoke staging. I did not open Langfuse. I did not run Felix. I did not open TestFlight. Claims about "what's on staging" come from `origin/staging` / `origin/spike/ecat-web` at `e87135475` (15 Oct), from `felix-v0.json`, and from Foundation's own caveats. **Verify before relying:** whether a non-admin can open Felix on staging today, whether `#2661` is deployed, whether the 19 Oct Kuzco note mutation was on an isolated database (FB-20, still on the scorecard), whether ClickHouse on the Langfuse host is still full (that claim was in the earlier draft from factory chatter; I did not re-verify it today).

The Mixpanel window in Foundation (390,100 product searches, 166,395 customer searches, 81,299 customer selections, 9,980 PDF catalogs, 27,113 order submissions, 15 Jul–12 Oct) is `[from-doc]`. The doc itself says ids may be devices, admins and staging are unfiltered. Directional only. It is evidence of an established workflow, not a unique-rep count.

`master` of `supercat_server` moved today (Lib&Co export, `#2667`). That does not include Felix's six tools.

The Claude artifact did not load. If it is a third framing of the same Oct 14–22 material, the working set already covers it. If it is something else, I have not seen it.

Local `~/repos/agent-factory` is a month behind `origin/main`. Anyone working Felix from that checkout is reading September law. Use `origin/main`.

---

## 8. What I would do in your seat this week

Not a plan. A sequence that matches the actual bottlenecks.

**1. Sit in the product, not the docs.** On VPN, staging, a real non-admin rep seat if one exists (ask Brent — this is Kjael's question and it is still the right first question). Open SuperCat for Sales in TestFlight if you have the build. Open Felix from the gold circle. Ask Prep / Show / Similar for one Craftmade door (`70680` or `9800`) and one Kuzco door (`LLC-T00000007`), exactly as `PRODUCTION_PLAN.md` specified. Write down what comes back. Thirty minutes. You will know more than another hour of Foundation & Beta. You will also know whether `#2661` is live.

**2. Name the join in one sentence, in a room with Brent and Kjael.** Suggested default, so you are not asking:

*December 1 is SuperCat for Sales catalog / customer / pricing / artifacts on web + iOS, flag-safe, turn-on-able for VCG. Felix on that date is a working gold circle on staging with tracing on, not a trusted beta. External Felix seats wait on G1–G4 and G6, aimed at Q1. Brent owns Clock A. Kjael owns Clock B product judgment. Kevin owns the loop. Context-recipe owner is named in that meeting or it stays Kjael by default. The internal support-Felix and the KB-replacement Felix do not share this name in customer conversation.*

**3. Do not let the SFS board become the Felix board.** If Felix work needs tickets, they are behavior tickets against G1–G7 (the factory already has a template and a 24-story crosswalk that was deliberately **not** imported). Mixing them into `dec-1` will make December 1 slip or make Felix ship ungated. Kjael already drew two colors. Keep them.

**4. Protect Brent's new loop, and aim it.** Recorded session → LLM ticket → Playwright PDV is how Clock A gets done with this headcount. Your leverage is making sure the sessions he is about to book include **admin-setting expression** and **customer/price invariants**, and do not include a tour of old iPad bugs. The "stump the suite" game is the right instinct if the fixtures are honest (Bulbright-like, not live Bulbright).

**5. Do the old-Jira pass he already said yes to — on Kjael's frame, not as a bug port.** Feature requests that add density. Admin settings that must express. Recurring themes, RICE'd, after the current two-week slice, not instead of it. Kyla's filter: drop anything whose real work is data infrastructure that is not done. I can run that pass from SERV / ECAT / EBR against the SFS epic list when you want it. It is not this document.

**6. On Felix, your scarce input is the same one the CTO named.** What a right answer must and must not say, for real rep situations. The seven 19 Oct cases plus their counterexamples are the first test set. You can write those without waiting for Langfuse to work. You cannot usefully edit prompts until the tests exist — that is how you get a Felix that never says "first order" because it never says anything.

**7. Keep the three Felixes apart in your own head, and soon in other people's.** Internal support-Felix is a CS productivity tool. Customer Felix is a product that can speak to a buyer through a rep's mouth. Felix-as-KB is a help surface for SuperCat for Sales. They should not share a name much longer. If you do one cheap thing for the company this month, retire "Felix" on the internal bot. Trey has already heard the customer one.

---

## 9. Source trail

| Source | What I took from it |
|---|---|
| `agent-factory` `origin/main` `agents/sales_assistant/{CANON,OVERVIEW,CONTRACT,HARNESS}.md` | Product law, six jobs, never-emit, six+three harness, current-vs-target as of 21 Oct |
| `agent-factory` `origin/main` `plan/{README,FOUNDATION_AND_BETA,BETA_RELEASE_SCORECARD}.md` v9.1 / v10 | Partner thesis, 19 Oct failures, G1–G7, D2/D5/D17 decided, owners still open |
| `agent-factory` `origin/main` `releases/felix-v0.json` (22 Oct) | Development baseline pinning `e87135475`, model, every gate open |
| `/Downloads/Felix in plain English.md` (22 Oct, Kjael) | The loop, the six parts, the showroom-note worked example, this-week jobs |
| `/Downloads/Felix_Review_Plan_v1.1.docx` (14 Oct) | The strategic question, five-phase review, hybrid-SQL clue |
| `supercat_server` `origin/master` `RepAssistant::BaseController` | June runtime; `is_admin?` gate |
| `supercat_server` `origin/staging` tool registry + `BaseController` | Thirteen registered tools; eCat Web flag/org-flag access; cart files unregistered |
| PRs `#2556 #2647 #2657 #2658 #2661 #2664 #2668 #2669 #2625` | What shipped, onto which branch, what is still open |
| `SERV-2424`, `EBR-695`, `SERV-2269` | Rails origin ticket; the other Felix |
| `SFS-14`–`SFS-34` (Jira, evidence view, this afternoon) | Dec 1 board, created 22 Oct, descriptions touched 23 Oct 11:51–11:55 ET |
| `supercat_for_sales` `main` (7 commits, 3–13 Oct) | Native shell, capsule + Felix circle, path configuration, staging host |
| `supercat_ds` commits 21 Oct, v4.6.2 | Design-as-spec, Felix gold/composer band |
| Fathom 871819569 / BQ ID 135607689 (full transcript) | VCG Dec 1 promise; two-color whiteboard; PDV/Playwright loop; Q1 Felix; Kjael's new-codebase frame |
| `foundation/01`, `05`, `08`; `CEO_SYSTEM_CONTEXT.md` | Why the iPad is the center of gravity; field assistant as a bounded context; Kai as the competitive AI |
| Claude artifact WeXQHgJjRWSKBwzGV3vzWd | **Did not load.** Not used. |

Companion factory docs I read enough of to trust the citations, not enough of to claim I ingested every appendix: `AGENT_ENGINEERING_EXECUTION.md`, `BEHAVIOR_CONTRACTS.md`, the 24-story CSV, `VALIDATION_EXECUTION_LEDGER.md` (August novel), `design/EXPERIENCE_SPEC.md`. If a later appendix quietly changed a gate, the scorecard on `main` and `felix-v0.json` still say all seven OPEN.
