# CONTRACTS — Operator and Agent Invariants

> **What this doc owns**: The five invariants that make this folder a stable, drift-resistant system — the operator contract, the agent contract, the rule-change protocol, the anti-archive rule, and the path-reference contract. The procedure for verifying conformance to all five. The catalogue of failure modes and the prescribed responses.
>
> **What this doc DOES NOT own**: Any specific rule about communication voice, driver framing, format routing, data fields, or quality checks. Those live in `_root/01` through `_root/08`. This doc owns the protocol; the other docs own the content.
>
> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Supersedes**: pre-refactor implicit-protocol-in-chat

---

## §1. Operator contract — rules go to root, not chat

A rule is binding on agents only if it satisfies both conditions:

1. It is written into a `_root/` doc — the one whose "What this doc owns" boundary covers it.
2. The edit is logged in `_root/09_changelog.md`.

Verbal direction, chat messages, Slack or email asides, comments inside CSVs, and TODO notes inside archived files are **not binding rules**. They are signal — they tell the operator that a rule may need to be written — but they do not constrain agent behavior until they are written and logged.

The operator commits to the following:

- When issuing a new rule or amending an existing one, the operator (or a delegated agent) must (a) write it into the owning `_root/` doc, (b) log it in `_root/09_changelog.md` per the format defined there, (c) bump the affected doc's "Last updated" date and the corresponding row in `_root/00_manifest.md`.
- The operator must not issue rules informally and expect agents to retain them across sessions. State lives in files, not in human memory or chat history. An agent that begins a fresh session has access to the `_root/` docs and nothing else; any rule absent from those docs is invisible to that agent.

The rationale is mechanical, not stylistic: agents do not carry context between sessions. The folder is the system's memory. Any rule that exists only in chat will disappear the moment the chat is closed.

## §2. Agent contract — no improvisation; if no root doc covers it, stop and ask

Before drafting any output, an agent must:

1. Read `_root/00_manifest.md`.
2. Read every doc listed in the manifest, in the order the manifest specifies.
3. Echo every root-doc title and last-updated date in the first message of the session. This is the **manifest-echo contract**. Failing to do so is grounds for the operator to discard the agent's output and restart the session.

If a situation arises that no `_root/` doc covers, the agent must:

1. Stop drafting.
2. Name the missing rule precisely. Vague reports ("I'm not sure how to handle this") are unacceptable; the report must take the form, "no `_root/` doc tells me whether <X> or <Y>."
3. Ask the operator to add the rule to the appropriate `_root/` doc.
4. Wait. Do not proceed by inferring.

Inferring a rule from "what the templates seem to suggest," "what the previous draft did," or "what feels consistent with the voice" is forbidden. That inference is the drift vector this system exists to prevent. Every improvised rule introduces an undocumented assumption that the next agent will either contradict or compound.

## §3. Rule-change protocol

Every edit to any `_root/` doc follows this exact sequence:

1. **Identify the owning doc.** Locate the doc whose "What this doc owns" line covers the rule. Edits never go in a doc that merely references the rule.
2. **Make the edit** in that doc.
3. **Log the change** in `_root/09_changelog.md`, using the format already established in that file: date, doc(s) changed, what, why, affected downstream, manifest-bumped y/n.
4. **Bump the "Last updated" date** in the affected doc's header AND in the corresponding row of `_root/00_manifest.md`.
5. **Identify and re-run affected downstream drafts.** This includes per-account briefs, delivery emails, and any in-flight artifact whose content depends on the rule that just changed. Do not assume the new rule will "apply going forward." The rule must be applied retroactively to in-flight work, or the inconsistency the change was meant to fix returns.

Step 5 is the step most often skipped. The cost of skipping it is that the rule change appears to have been made — it is in the doc, it is in the log — but its effects are unevenly distributed across the output set. The folder then contains two implicit rules, old and new, with no way for a reader to know which one was in force when any given draft was produced.

## §4. Anti-archive rule — never read `_archive/`

`_archive/2026-05-22__pre-refactor/` and any future archive folder contains superseded artifacts. Reading them surfaces stale, contradictory, or replaced rules and silently re-introduces the drift this system was built to eliminate.

If an agent believes a `_root/` doc has a gap and that the archive holds the answer, the answer is: a gap exists. Per §2, stop and ask. The archive is not an escape hatch.

The only legitimate readers of the archive are:

- The operator, for historical reference.
- An explicitly-instructed extraction task (e.g. "pull the verbatim 'What's Coming in 2026' block from `_archive/.../format-a-notices/_brief-template.md` and inline it into `_root/03_what_we_sell.md`").

Both modes require the operator to direct the read by file path. Browsing the archive folder to "see what's there" is not authorized under any condition.

## §5. Path-reference contract — rules live in one place; everywhere else, reference

A rule's text appears in exactly one `_root/` doc — the doc that owns it. Every other doc, template, prompt, or draft that needs to invoke that rule does so by reference, never by restatement.

A correct reference looks like: "Per `_root/04_communication_posture.md` §forbidden-phrases, do not use the word 'transition' in customer-facing copy."

A violation looks like: "Do not use the word 'transition' in customer-facing copy." Even if the violating doc is technically correct on the day it was written, the rule's text now exists in two places. The two copies will diverge — through a typo, a partial edit, or a rule change applied to one and not the other — and the divergence will be silent.

Every duplicated rule is a future drift event. The cost of a path reference is a single `grep` for the curious reader. The cost of a duplicated rule is silent divergence that no one notices until it produces a customer-facing inconsistency.

---

## Verifying conformance

The operator (or a QA agent) can spot-check any draft against the five invariants using this procedure:

1. **Manifest-echo check (verifies §2).** Open the first message of the session that produced the draft. Confirm it lists every `_root/` doc by title and current last-updated date. If absent or stale, the draft is non-conformant.
2. **Restatement check (verifies §5).** Pick a distinctive phrase from each `_root/` doc's owned rules. `grep` the entire folder for that phrase. It should appear in exactly one location: the owning doc. Any second occurrence in a template, prompt, or draft is a §5 violation.
3. **Conformance-block check (verifies §4 and corroborates §2).** Confirm the draft ends with a conformance block in the format defined by `_root/08_quality_bar.md`. The block must enumerate every file read and explicitly attest that `_archive/` was not read. A missing or malformed block, or a block that claims reads inconsistent with the draft's content, makes the draft non-conformant.
4. **Changelog check (verifies §1 and §3).** For any rule that appears to be in force in the draft, confirm the corresponding `_root/` doc has a "Last updated" date supported by an entry in `_root/09_changelog.md`. A rule whose presence in the draft cannot be traced through the log is a §1 violation; a rule whose log entry omits the §3 propagation steps is a §3 violation.

(The format of the conformance block is owned by `_root/00_manifest.md §5` (canonical, stamped 2026-05-22 at Stage 5). Earlier Stage 1–4 sessions used the per-prompt format specifications; Stage 5+ sessions use the manifest's canonical format.)

---

## Failure modes and what to do

| Failure mode | Prescribed response |
|---|---|
| Agent did not echo the manifest in its first message | Discard output. Restart the session. Per §2, the manifest-echo contract is a precondition for drafting. |
| Agent restated a rule from another doc instead of referencing it | Flag the restatement. Remove it. Replace with a path reference of the form "Per `_root/XX_name.md` §section." If the restated text had drifted from the owning doc's version, log the correction. |
| Agent read the archive without being directed to a specific file | Flag. Restart the session. Treat any content sourced from the archive as suspect and re-derive it from `_root/` docs. |
| Operator issued a rule in chat but did not commit it to a `_root/` doc | The rule is not binding. Remind the operator of §1. If the rule is real, complete the §3 protocol now: write it into the owning doc, log it, bump dates, re-run affected drafts. |
| Two `_root/` docs disagree | Escalate to the operator. The doc whose "What this doc owns" boundary covers the rule wins. The other doc gets corrected — its restatement removed or replaced with a reference — and the correction is logged. |
| Agent improvised a rule because no `_root/` doc covered the situation | Discard the improvised output. The agent should have stopped and asked per §2. Identify the missing rule, decide which doc owns it, author it there, log it, then re-run the draft. |

---

*Cross-references: `_root/00_manifest.md` (the required-reading map this contract presupposes; §5 owns the canonical conformance-block format); `_root/09_changelog.md` (the log this contract's §3 writes to); `_root/08_quality_bar.md` (the QA checklist that operationalizes this contract's checks).*
