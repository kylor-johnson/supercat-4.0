# Wave 1.1 — Authoring Prompt for `_root/CONTRACTS.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/CONTRACTS.md` (replace stub contents)
> **Estimated authored length**: 80–140 lines

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is intentional. You are being used precisely because you have no bias toward any phrasing, structure, or assumption that emerged in prior planning sessions. Your job is to author **one file** — `Pricing Migration/_root/CONTRACTS.md` — to a high standard, using only the materials this prompt directs you to.

**You will not improvise.** If anything in this prompt is unclear, stop and ask the operator. Do not invent rules. Do not add scope beyond what this prompt specifies.

---

## Step 1: Required reading (in this exact order)

Read each of these files completely before writing anything. Echo the file path + last-updated date of each in your first response message so the operator can verify you've actually read them (the "manifest-echo contract" — see spec below; this is the contract you're about to author, and you're modeling it now).

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md` (the stub you're about to replace — read so you understand the "What this doc owns / does not own" boundary)
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/00_manifest.md` (also a stub; its header tells you what role manifests play and clarifies how CONTRACTS pairs with manifests)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` (read in full; the protocol you author must produce entries shaped like the one already there)

**Do NOT read** `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/`. The whole point of the system you're about to define is that archived material is superseded. If you find yourself wanting to read the archive to "see how they used to do it," stop — that's a signal that this prompt has a gap. Ask the operator.

---

## Step 2: What you are authoring

`CONTRACTS.md` is the **operating system** for the entire `_root/` doc set. It owns five invariants, and only those five. Below is the spec — your job is to render each invariant as clear, operational prose with concrete examples and crisp failure modes.

### Spec — the five invariants

**§1. Operator contract — "rules go to root, not chat."**
- A rule is binding only if it lives in a `_root/` doc AND has a corresponding entry in `_root/09_changelog.md`.
- Verbal direction, chat messages, Slack/email asides, comments inside CSVs, and TODO notes in archived files are NOT binding rules. They are signal that a rule may need to be written, but they do not constrain agent behavior until written.
- The operator commits to: when issuing a new rule or amending an existing one, the operator (or a delegated agent) must (a) write it into the owning `_root/` doc, (b) log it in `_root/09_changelog.md`, (c) bump the manifest's last-updated date for that doc.
- The operator commits to NOT issuing rules informally and expecting agents to retain them across sessions. State is in files, not in human memory or chat history.

**§2. Agent contract — "no improvisation. If no root doc covers it, stop and ask."**
- Before drafting any output, an agent must read every doc named in `_root/00_manifest.md` in the order specified.
- An agent must echo every root-doc title + last-updated date in the first message of any session (the "manifest-echo contract"). Failing to do so is grounds for the operator to discard the agent's output.
- If a situation arises that no `_root/` doc covers, the agent must:
  1. Stop drafting.
  2. Name the missing rule precisely (e.g. "no `_root/` doc tells me whether to use 'partner' or 'customer' for entity parents").
  3. Ask the operator to add it to the appropriate `_root/` doc.
  4. Wait. Do not proceed by inferring.
- Inferring a rule from "what the templates seem to suggest" or "what the previous draft did" is forbidden. That is the drift vector this system exists to prevent.

**§3. Rule-change protocol — how to safely edit any `_root/` doc.**
Every edit to any `_root/` doc follows this exact sequence:
  1. Identify the doc that **owns** the rule (per the manifest's "What this doc owns" lines). Edits never go in a doc that merely *references* the rule.
  2. Make the edit.
  3. Add a `_root/09_changelog.md` entry using the format already established in that file (date, doc(s) changed, what, why, affected downstream, manifest-bumped y/n).
  4. Bump the "Last updated" date in the affected doc's header AND in `_root/00_manifest.md`'s row for that doc.
  5. Identify and re-run any affected downstream drafts (per-account briefs / delivery emails). Do not assume "the new rule will apply going forward" — the rule must be applied retroactively to in-flight work or the inconsistency it was meant to fix returns.

**§4. Anti-archive rule — "never read `_archive/`."**
- `_archive/2026-05-22__pre-refactor/` and any future archive folder contains superseded artifacts. Reading them surfaces stale, contradictory, or replaced rules and silently re-introduces the drift this system was built to eliminate.
- If an agent believes a `_root/` doc has a gap and that the archive holds the answer, the answer is: a gap exists. Per §2, stop and ask. The archive is not an escape hatch.
- The only legitimate readers of the archive are: the operator (for historical reference) and an explicitly-instructed migration / extraction task (e.g. "pull the verbatim 'What's Coming in 2026' block from `_archive/.../format-a-notices/_brief-template.md` and inline it into `_root/03_what_we_sell.md`"). Both modes require the operator to direct the read.

**§5. Path-reference contract — "rules live in one place; everywhere else, reference."**
- A rule's text appears in exactly one `_root/` doc — the doc that owns it.
- Every other doc, template, prompt, or draft that needs to invoke that rule does so by reference: e.g. "Per `_root/04_communication_posture.md` §forbidden-phrases" — never by restating the rule's text.
- This is the single most important mechanical safeguard against drift. If an agent ever writes a rule's text in a non-owning doc, the system has two copies and they will diverge.
- Rationale (state this in the authored doc): every duplicated rule is a future drift event. The cost of a path reference is a single `grep` for the curious reader; the cost of a duplicated rule is silent divergence.

### Additional content the doc must include

- **Header block** matching the pattern in the other root-doc stubs (`> **Last updated**: 2026-05-22`, `> **Owner**: CEO`, `> **Supersedes**: pre-refactor implicit-protocol-in-chat`).
- **Section: "Verifying conformance."** A short procedure for the operator (or a QA agent) to spot-check that any given draft adheres to all five invariants: did the agent echo the manifest? does any rule appear restated in a non-owning doc (greppable)? is there a conformance block at the end of the draft?
- **Section: "Failure modes and what to do."** A short table of common failure modes and the prescribed response:
  - Agent did not echo manifest → discard output, restart session
  - Agent restated a rule from another doc → flag, remove the restatement, replace with a path reference
  - Agent read the archive without being directed → flag, restart session
  - Rule changed in chat but not committed to a root doc → not binding; remind operator of §1
  - Two root docs disagree → escalate to operator; the doc whose "owns" boundary covers the rule wins; the other gets corrected and logged

### What this doc does NOT include

- Any specific communication rule (voice, forbidden phrases, driver framing) — those live in `_root/04` and `_root/05`.
- Any specific data-pipeline rule — that lives in `_root/07`.
- The manifest itself — that's `_root/00_manifest.md`.
- The changelog itself — that's `_root/09_changelog.md`.
- The format of conformance blocks — that lives in `_root/08_quality_bar.md` (which will be authored later; until then, reference it as a forward link and note that the format is TBD).

---

## Step 3: Voice and format constraints

- Write in the same register as the other `_root/` doc headers and `AGENTS.md`: declarative, operator-facing, no marketing language, no hedging. This is system documentation, not a memo.
- Use second-person ("the operator must…", "the agent must…") for contract clauses. Use third-person for descriptive prose.
- Use numbered lists for sequenced protocols (the rule-change protocol). Use bullets for non-sequenced enumerations.
- Use Markdown tables for the failure-modes section.
- No emojis. No "Pro tip:" boxes. No exhortation ("This is critical!"). The doc's gravity is implicit in its position as `CONTRACTS.md`.
- Preserve the existing stub's frontmatter pattern (`> **What this doc owns**`, `> **What this doc DOES NOT own**`, `> **Last updated**`, `> **Owner**`, `> **Supersedes**`). Update these to match the final authored content.

---

## Step 4: Output

Replace the entire current contents of `Pricing Migration/_root/CONTRACTS.md` with the authored document.

Then, in your chat reply (NOT in the file), produce a **conformance block** in this format:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/CONTRACTS.md (replaced stub)
Files read:
  - Pricing Migration/AGENTS.md (last-updated: <date>)
  - Pricing Migration/00_README.md (last-updated: <date>)
  - Pricing Migration/_root/CONTRACTS.md [stub] (last-updated: <date>)
  - Pricing Migration/_root/00_manifest.md [stub] (last-updated: <date>)
  - Pricing Migration/_root/09_changelog.md (last-updated: <date>)
Files NOT read: Pricing Migration/_archive/** (per agent contract being authored)
Rule restatements detected in own output: <count and locations, or "none">
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. Do not propose Stage 3 work. Do not author other `_root/` docs. The operator will paste your output back to the planning agent for review, and only after that approval will the next wave begin.

---

## Step 5: If something is missing

If reading the required files reveals a gap, ambiguity, or contradiction this prompt does not resolve — stop and ask the operator before drafting. Do not infer. Do not assume. The whole point of this exercise is to produce a doc that itself models the agent contract you are authoring.
