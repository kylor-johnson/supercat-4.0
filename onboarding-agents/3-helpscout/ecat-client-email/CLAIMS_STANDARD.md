# Claims standard: how a sentence in the client text may state a fact

**The single reference for what a client-facing sentence is allowed to claim.** The
drafter writes to it; the verify pass (`tools/VERIFY_PASS_BRIEF.md`) checks against it.
Voice (warm, declarative, no em-dashes, "Best, Kylor") is in `SKILL.md` and is not the
problem this file solves.

Why it exists: across two held-out batches, about 45% of drafts carried a false or
unsupported sentence in the client text after verification. In 18 of 21 of those
errors the finding underneath was roughly right; the sentence claimed more than the
evidence reached. None of them broke a voice rule.

---

## 1. Four non-negotiables

1. **A sentence claims only what its evidence reaches.** If the query covered one
   table, the sentence covers one table. If the log shows a mismatch, the sentence
   says mismatch, not why.
2. **No cause you didn't observe.** "Because", "so", "which is why", "most likely"
   join an observation to an explanation. Write the observation; state the cause only
   if a log, a code path or the client showed it. Otherwise ask for the one thing
   that would show it.
3. **Past tense only for what happened.** Anything we did (sent, attached, asked,
   raised, enabled, fixed) has a record you can point to, or it is written "I'll …"
   with an owner action. Concessions ("you're right", "fair point", "that's on me")
   are claims about what we did, and need the thread or transcript that shows it.
4. **Quote, never paraphrase, anything the client will look for.** Menu paths,
   buttons, radio options, field names and column headers come verbatim from the
   screen or file *that person* uses.

## 2. Don't write → write instead

Each row is a sentence shape that passed review and was wrong.

| don't write | write instead |
|---|---|
| "X doesn't store / doesn't exist / isn't there" after searching one place | "X isn't in the [download file / Admin list / table you searched]", naming the place |
| "the file failed because the column names were shortened" | "the file's headers didn't match: it had BASEITEM where the importer expects BaseItemCode" |
| "the setup is right, so it's the iPad" | "the setup checks out on [the three things checked]. Next I need [the one fact] to narrow it" |
| "most likely it's X" (error text unseen) | "the log shows [what it shows]. Send me the exact error text and I'll confirm the cause" |
| "each rep / every user / all your accounts will …" | the counted group: "the 8 reps without an existing login will …" |
| "you're the only one on the older build" | the counted fact: "your iPad is on 20260818; 4 others on your team are too" |
| "I asked engineering to confirm …" (only an internal note exists) | "I'll ask engineering to confirm …" plus an owner action |
| "I've attached …" before the file exists | attach it first, or "I'll send … by [owner action]" |
| "fair point" / "you're right" on something the record contradicts | state what happened, with its date, then the next step |
| "once the [X] correction is finished" (our own earlier framing, unchecked) | check the framing at T first; if it holds, cite it; if not, drop it |
| "Tools > Admin Reports" for a user on the modern menu | the label from their screen: "Settings & Tools → Admin Reports → File Import Status" |
| "set it to your price, retail, or no price" | the words on the page: "My Account → Select price level to display: My Cost / [retail level name] / Custom / Hide prices" |
| "we need [KB-listed fields]" | "the importer requires [code-enforced fields]; the KB also lists [others]" |
| "this looks resolved" from evidence after the report | only if the same evidence was absent before the report; otherwise "this looks right now; tell me if you still see it" |
| "I can see your sign-in at 5:07" from one row | name the event you saw ("the app checked in with our server at 5:07") or query the event you mean |
| "yesterday" / "Thursday" | the date, unless it's certain from the send date |
| "so they can start practicing" when a precondition is missing | state the precondition in the same sentence |
| "I can't open the attachment" | never client text; it becomes an owner action |
| "the fix ships in the next update" | only if the fix commit is on the branch that ships in that build; otherwise "I'll confirm when it's live" |

## 3. The claim budget

Every factual sentence in an email is a chance to be wrong, and the longest drafts
carried the most errors. So:

- **The client text carries only the facts the client needs in order to act**, plus
  the one or two facts that answer their question. Diagnostic detail, counts that
  don't change what they do, and anything you're less than sure of go in VERIFY or
  Also found.
- **The answer stays.** A verified cause or fix that answers the question is in the
  copy, stated at the confidence the evidence gives it. Cutting a reply down to a
  holding note is a failure, not a safe choice.
- **Don't ask for what you can read.** A question to the client whose answer is in
  the packet, the attachment they sent, or a query you can run is removed.

## 4. Confidence, stated in the sentence

Use the wording that matches what you have:

| you have | write |
|---|---|
| a row, a log line, a code path | a plain statement: "The import on June 3 was rejected with …" |
| a strong inference from several observations | say both: "Every file since May has the same error, so the export is still using the old headers." Only when each observation is cited in VERIFY |
| a hypothesis | say it's one and give the check: "One thing that fits is X. Can you tell me Y?" |
| nothing | don't write the sentence |

## 5. Before the draft goes to the verify pass

- [ ] Every factual sentence in the client text maps to a VERIFY row
- [ ] No sentence claims wider scope than its search (§ 1.1), and every "each / all / only / never" is counted over the whole population, shown in VERIFY
- [ ] No cause without an observation behind it (§ 1.2)
- [ ] Past tense and concessions only with a record (§ 1.3)
- [ ] Every label is quoted from that person's screen, at their build (§ 1.4): Admin Console modern vs classic per their `org_users.ui_preference` (`app/controllers/concerns/ui_switchable.rb:35-48`; modern sidebar "Settings & Tools" in `app/components/sc/sidebar_component.rb`, classic "Tools" in `app/views/layouts/_navigation.html.erb`), eOL from `app/views/ecat/`, iPad at their build
- [ ] Every example the client is told to try (an item, a customer, a login, a URL) is one that person can see: find their login and group, then check every gate (trade-name and collection authorisation, the group's custom-field filters (`user_types.custom_field_filters`, `app/services/products/get_for_user_type.rb:46-58`), Hideable on that surface, `deleted`, and on the iPad `product_synch_requires_photo`), plus price authorisation
- [ ] Every "shows" / "displays" names the surface: Admin Console page, Admin CSV export, eOL order page, eOL invoice page, Orders/Invoices list, or iPad
- [ ] No release or date promised for a fix unless the fix commit is on the branch that ships in that build
- [ ] No promise to edit a value the client's own import file controls (it comes back on their next upload): name the file and column they change
- [ ] Relative time words match the send date in the client's time zone; otherwise write the date
- [ ] No placeholder (`[N]`, `<name>`, `TBD`, `XX`): an unfillable value means the sentence comes out
- [ ] Every person named is checked against `users.first_name` / `last_name`, never a username; a first name shared by a SuperCat person and a client contact is written in full
- [ ] Nothing in Owner actions or Also found contradicts or is a missing precondition of a copy sentence
- [ ] The copy still answers the question (§ 3), and asks for nothing the run could read
