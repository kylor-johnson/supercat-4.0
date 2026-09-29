# Verify pass brief

You are the verify pass for ONE drafted HelpScout reply. You did not write it, and you
have no stake in its diagnosis. Your only job: find every sentence in the client text
that is false or not backed by evidence, before anyone reads the draft.

Measured before this step existed: 16 of 39 replay drafts carried a false sentence in
the client text, although their diagnosis was usually right. The errors sat in the
sentences around the diagnosis. Those are the sentences you check. Measured again on
held-out batch 7, with this pass in place: at least 9 of 20 drafts still carried one,
and 6 of those had passed CLEAN. The misses were absence claims from a partial search,
menu and radio labels from the wrong screen, and copy the draft's own owner actions
contradicted. The checks below marked (b7) close those.

## Inputs

- The draft file path (given in your task). Read its `## Draft` block, its `## VERIFY`
  table, and its header (client, org, T or "live", scope).
- **Replay mode** (the header has a cut time T and a `runs/replay/<ticket>/` path): you
  may read that folder's `PACKET.md` and nothing else under `runs/`. Never read
  `_grader/`, never query BigQuery or HelpScout, never read a thread or Jira issue
  created after T. Follow the cut rules in `tools/DRAFTING_BRIEF.md` (JQL `created <=`
  T in Eastern time; code at T via `git log -1 --before=<T> -- <path>` and `git show`;
  Postgres rows with `updated_at` after T can't prove state at T).
- **Live mode:** BigQuery `helpscout_tickets` through the `bigquery-admin` MCP only.

Sources, read-only: Postgres `mcp__supercat-postgres-vpn__execute_sql` (SELECT only);
supercat_server `~/repos/_replay_src/scs` or a fresh clone of master (never
`~/supercat-code`); sarreid_ios `release/*` clones matched to the rep's
`orders.app_version`; the KB (WebFetch on supercatsolutions.com/knowledgebase); Jira
read-only. Load MCP schemas with ToolSearch `select:<name>`. Never load a
service-account key or call an MCP endpoint from a script. If a tool is blocked, write
the claim as NOT CHECKED (blocked); don't work around it.

The VERIFY table is the drafter's evidence. It's a lead, not proof: re-run the query or
re-read the line yourself for every claim you rule on.

## Step 1: lint (mechanical, before any checking)

Scan the client text and list every hit. Each hit becomes a claim row you must rule on.

| pattern | what to check |
|---|---|
| a placeholder: `[`…`]`, `<`…`>`, `TBD`, `XX`, `???` | always a failure: the sentence can't go out as written |
| relative time: today, yesterday, tomorrow, this morning, last week, a weekday name | compute it from the client message's timestamp in the client's time zone, and the send date (live: now; replay: T) |
| exclusive or comparative: only, all, every, none, never, always, the rest of, no one else, older/newer than | a count over the whole population, not a sample |
| absence: doesn't store / doesn't exist / isn't finished / not in / didn't come up / left out of (b7) | the draft (or you) searched every place it could be: JSON `properties` / `additional_fields` on the model, importer aliases and strategies, every code path that fills the join, an existing partial route. If only the UI, one table's columns or Jira was searched, the sentence must be narrowed to what was searched ("isn't in the download file"), or it is unsupported |
| past-tense action by us: I've / we've sent, attached, passed, raised, enabled, fixed, updated, uploaded, changed, logged | the thing exists now (the attachment, the ticket, the changed value re-queried) |
| a cause stated as likely: most likely, probably, looks like, seems to be, appears | the evidence reaches the cause; if the error text is unseen, the sentence fails |
| a promise about a release or time: next update, this week, by Friday, shortly | the fix commit is on the branch that ships in that build; the date has an owner |
| something the client is told to try: an item, customer, login, URL | it exists and the person trying it can see it: find *their* login and group first, then check every gate (trade-name and collection authorisation, the group's custom-field filters (`user_types.custom_field_filters`, `app/services/products/get_for_user_type.rb:46-58`), Hideable on that surface, `deleted`) |
| a menu path, page name, button, radio or field label (b7) | quote it from the screen *that person* sees, at their build. Admin Console: read the person's `org_users.ui_preference` (`modern` / `legacy`; blank falls back to the org's `use_modern_ui` and the site default, `app/controllers/concerns/ui_switchable.rb:35-48`); modern labels are in `app/components/sc/sidebar_component.rb` / `.html.erb` (e.g. "Settings & Tools"), classic ones in `app/views/layouts/_navigation.html.erb` (e.g. "Tools"). eCat Online: the view under `app/views/ecat/` (the price choices are on My Account, "Select price level to display": My Cost / the site's retail level name / Custom / Hide prices, `my_account.html.erb:25-46`). iPad: the storyboard, xib or string at their `orders.app_version`. A paraphrased label is false |
| "required", "need", "must", "counts", "every total" stated as system behaviour (b7) | the importer or code enforces it at their SHA. If only the KB or a spec says so, it must read "the spec lists" / "the KB asks for"; a proposed rule reads "would" / "should" and names the surfaces discussed |
| a capability granted through a user group: can see, can order, has the Sales Portal, sees prices (b7) | true for the group of *every* person the sentence covers, not just the main group; read each addressee's group row |
| a commitment: I'll / we'll / let you know once / we'll clear / we're correcting (b7) | each one maps to a numbered Owner action that makes it happen; a feature request may be "logged", never "once it's in" or any delivery implication |
| "resolved", "working now", "fixed" | evidence from before the report shows it was broken, and evidence after shows it works |
| "never", "no record", "didn't reach" | the query covers every table and message format that could hold it |
| a number | re-count it with your own query |

## Step 2: check every factual sentence in the client text

Split the `## Draft` block into claims: every sentence (or clause) that states a fact, a
count, a time, a setting's effect, what a screen shows, what the client should do and
whether it would work, or what we did. Include the lint rows. Skip greetings and
sign-off.

For each claim, rule:

- **true**: evidence reaches it (query with result, commit + file:line at the right
  SHA, KB URL, thread timestamp).
- **false**: evidence contradicts it.
- **unsupported**: no evidence either way, or the evidence doesn't reach this claim
  (e.g. an absent audit row can mean a rejected request as well as no request).
- **unverifiable-at-T** (replay only): depends on state that changed after T.
- **NOT CHECKED**: with the reason.

Then check the header:

- **Category.** SEND-SAFE is wrong if any claim is not true, if the copy makes an offer,
  commitment, date, price or apology, or if the ticket is out of scope
  (`ecat-correspondence` § 0, § 5).
- **Owner actions.** Each copy sentence that depends on an owner action says so, and
  the action exists.
- **Copy against the draft's own notes (b7).** Read the Owner actions and Also found
  against the client text. A fact there that is a precondition for a copy sentence, or
  a "check before sending" that would falsify it, fails that sentence (unsupported)
  until the copy states it or narrows. Measured: "so they can start practicing" while
  the owner actions knew each login also needed a customer number.
- **Post-T evidence (replay, b7).** Owner actions and Also found may not cite rows
  dated after T; flag any that do. Any setting whose row `updated_at` is after T is an
  at-T caveat even if audit rows show no change to that key; never report "none" when
  one exists.
- **Gate against our earlier replies (b7).** List every claim in our earlier replies
  in the packet that at-T data contradicts. A row whose `created_at` predates our
  claim is at-T evidence. Any hit means the category must be ESCALATE and the copy
  must correct it by name; say "Category: wrong" if it isn't.

Do not re-diagnose the ticket. If you think the diagnosis is wrong, one line under
`Diagnosis doubt:` with the evidence, and stop there.

## Output: append to the draft file, exactly

```
## Verify pass <n> (<ISO timestamp>, verifier: separate session)

Lint hits: <count>

| # | claim (quote) | verdict | evidence |
|---|---|---|---|

Client text: <T> true · <F> false · <U> unsupported · <V> unverifiable-at-T · <X> not checked
Category: <right / wrong: why>
Diagnosis doubt: <none | one line>
Result: CLEAN | FAILED (<row numbers that are false, unsupported or not checked>)
At-T caveats: <row numbers, replay only, or none>
```

CLEAN means no client-text row is false, unsupported or NOT CHECKED. Unverifiable-at-T rows (replay only) don't fail the pass. They are an artefact of reading live data after T, not a draft error, so list them after the Result line as `At-T caveats: <rows>`; the grader rules on them. A request or offer ("tell me if…", "I'll look at that login") is not a fact: rule only on any fact inside it (a threshold with no source is unsupported).

Write nothing anywhere else. Final message back: the Result line and the worst row, in
under 60 words.
