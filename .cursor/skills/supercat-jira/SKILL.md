---
name: supercat-jira
description: >
  Search SuperCat's Jira before proposing engineering work, and write tickets in house
  format. Use whenever the answer to a support issue is "this needs a ticket", when asked
  "is there already a ticket for X", "has this been fixed", "is this tracked", or when
  filing/updating anything in SERV, ECAT, EBR, or CSP. Enforces a duplicate search BEFORE
  any ticket is drafted or filed. Consult BEFORE telling a client or a teammate that
  something is or is not a known issue.
---

# SuperCat Jira

Cloud ID: `3aea3e61-c30d-422a-9b0e-b5bab9b4c92a` (`supercatsolutions.atlassian.net`).
Every `mcp__atlassian__*` call needs it.

Two phases, in order. **Phase 1 is a gate.** Never draft or file a ticket, and never tell
anyone "that's a known issue" or "there's no ticket for that", until Phase 1 has run.

---

## Projects

| Key | Name | What lands here |
|-----|------|-----------------|
| **SERV** | Server | Rails/server work: eOL, importers, Admin Console, API, Sales Portal backend |
| **ECAT** | eCat | iPad app work (Objective-C client, sync, on-device rendering) |
| **EBR** | Enhancements and Bug Requests | Customer-originated requests awaiting triage. Statuses skew `Submitted` / `Triaging`. Summaries often prefixed `FEA:` |
| **CSP** | Client Support Projects | Per-client engagement umbrellas, not code work |

Observed pattern, not a written rule: a diagnosed server-side defect or feature with
acceptance criteria goes to **SERV**; a raw customer ask that has not been scoped goes to
**EBR**. If genuinely unsure which, say so rather than guessing.

A server-side symptom can have an ECAT twin (the iPad resolves some things client-side).
Search both before concluding it's untracked.

---

## Phase 1 — Duplicate search (mandatory)

`text ~` in JQL is **fuzzy word matching, not semantic**. One query proves nothing. Run
all three passes:

**Pass 1 — summary scan, per project.** Broad, cheap, high recall.

```
project = SERV AND (summary ~ "<domain noun>" OR summary ~ "<surface>") ORDER BY created DESC
```

Read every row. Repeat for ECAT and EBR when the surface could live there.

**Pass 2 — full text, multiple phrasings, all projects.** Clients and engineers name the
same thing differently. Use 4-6 alternatives covering the customer's words *and* the
engineering words:

```
text ~ "hide inventory" OR text ~ "suppress inventory" OR text ~ "inventory anonymous" ...
```

**Pass 3 — read the near misses.** Open anything plausible with `getJiraIssue` and read the
description. Titles lie. In practice the most useful hit is often the ticket that *created*
the behavior now being complained about.

### Reporting the verdict

State what you searched and hedge honestly. "Net-new with high confidence, here are the
three nearest neighbors and why each is not it" is a real answer. "I searched Jira and
found nothing" is not.

### Status vocabulary (a closed ticket is not always "Done")

`To Do` · `In Progress` · `Ready to Accept` · `Done` · `Closed` · `Hold` · `Back Burner` ·
`Triaging` · `Submitted` · `Pending SuperCat` · `Already Implemented` · **`Archieved`** (sic,
that is the real spelling in Jira — match it exactly in JQL).

"Has this been solved?" means checking for `Done`, `Closed`, **and** `Already Implemented`.
`Archieved` and `Back Burner` mean *dropped*, not fixed — a client-facing answer must not
imply a fix is coming.

### Token mechanics (this will bite you)

Unbounded JQL blows the response limit and dumps to a file. Avoid it:

- Always pass a narrow `fields` array: `["key","summary","status","resolution","created"]`.
- Never request `description` in a multi-row search. Fetch it per-issue in Pass 3.
- If a result does overflow to a file, do not read it linearly. Use jq:

```bash
jq -r '.issues.nodes[] | [.key, .fields.status.name, .fields.summary] | @tsv' "$FILE" | column -t -s $'\t'
```

---

## Phase 2 — Writing the ticket

### Before you cite any code

**Verify the local checkout is current.** `git log -1 origin/master` after a `git fetch`.
A stale clone will hand you file paths, method names, and control flow that no longer match
production, and a ticket built on that sends engineering to the wrong place.

```bash
git -C ~/supercat-code/supercat_server fetch origin master
git -C ~/supercat-code/supercat_server log -1 --format="%h %ci" origin/master
git -C ~/supercat-code/supercat_server show origin/master:<path>   # read prod, not HEAD
```

Cite line numbers from `origin/master`, not from the working tree.

### Reproduce before asserting

A ticket claiming behavior should carry evidence someone else can re-run: an anonymous
`curl` against the live page, a SQL count, an exact rendered string. State the date the
observation was made — config changes underneath these claims.

### Which type

| Type | Use when |
|------|----------|
| **Story** | The control or capability never existed. Missing setting, new behavior, changed UX |
| **Bug** | Something is broken against its own spec. A permission not honored, a regex that misses, a crash |
| **Task** | Distinct piece of work with no user-facing goal (infra, cleanup, migration) |
| **Epic** | Umbrella for a set of the above |

Missing-control issues read like bugs to the client but file cleanest as **Story**, because
the fix needs acceptance criteria and a design decision, not a patch.

### Summary line

Prefix with the surface: `eOL: `, `eCat: `, `Sandbox: `, `Enrollment: `. Then the defect or
goal in engineering terms, not the client's symptom. Name the org shortname in the summary
only when the issue is org-specific.

Good: `eOL: Option inventory quantities ignore user group Available Quantity permission`
Weak: `Alden can't hide inventory`

### Story template

```markdown
* [#<HS number> <subject> - <Client Name>](https://secure.helpscout.net/conversation/<id>/<number>/)

Request:

> <verbatim quote of what the client actually asked for>

# Background

<What is happening and why, in engineering terms. Named files, methods, line numbers from
origin/master. Which settings are and are not involved, including the ones someone would
reasonably assume are involved but are not.>

<Verified reproduction, with date. Scope: how many rows / orgs / products are affected.
What the client had to do as a workaround and what that cost them.>

# Acceptance Criteria

AC1. <Primary behavior, testable.>
AC1.1. <Edge case, e.g. the anonymous public-site user.>
AC1.2. <What must stay the same for users who currently see it.>
AC2. Existing orgs see no change on upgrade. <State the default explicitly.>
AC3. No change to <adjacent surface> behavior.

# Open question for elaboration

<Any design fork you are not entitled to settle. Name the alternatives, recommend one,
hand the decision to refinement.>

Related: SERV-xxx (<why>), SERV-yyy (<why>).
```

### Bug template

```markdown
## Summary

<Symptom, which surfaces show it, which do not. Org shortname and affected data.>

## Root Cause

<The actual mechanism. Quote the offending expression. Explain why it fails.>

## Why <other surface> Works

<When one client works and another doesn't, explain the divergence. Prevents a wrong fix.>

## Fix

1. `<file>`: <specific change>
2. ...

Related: SERV-xxx, SERV-yyy
```

Exemplars worth reading before writing: **SERV-2445** (model Bug), **SERV-1936** (model
Story with clean AC/AC1.1 structure), **SERV-2474** (model Story with Background +
open-question section).

### Fields

Required on create: `project`, `issueTypeName`, `summary`, `reporter` (defaults to you).
Everything else goes in `additional_fields`:

```json
{"priority": {"name": "High"}}
```

- **Priority**: `Highest` `High` `Medium` `Low` `Lowest` `Unprioritized`. Data exposure or a
  client forced into a damaging workaround is `High`. Cosmetic is `Medium`.
- **Components**: left empty across SERV in practice. Don't invent one.
- **Labels**: leave empty. `elaborated` is applied by the team during refinement and
  `helpscout` / `hs_stage_*` are applied by automation. Do not self-apply either.
- **Assignee**: leave unassigned. Triage assigns.

### Links

Add `Relates` links to the neighbors surfaced in Phase 1, in addition to the `Related:` line
in the body. Link types available: `Blocks`, `Cloners`, `Duplicate`, `Relates`.

```
createIssueLink(inwardIssue: <new>, outwardIssue: <neighbor>, type: "Relates")
```

---

## Hard rules

1. **Never file without Phase 1.** Present the duplicate verdict and the drafted ticket for
   approval before creating anything.
2. **Never cite code from a stale checkout.** Fetch, then read `origin/master`.
3. **Never claim a fix is coming because a ticket exists.** Check the status first, and
   remember `Archieved` and `Back Burner` mean dropped.
4. **Ticket bodies are internal.** HelpScout links, org shortnames, table names, and
   `*.html.erb` paths belong here and never in client copy. For the client-facing half,
   use `ecat-client-email`.
