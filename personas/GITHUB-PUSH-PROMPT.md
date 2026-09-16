# Prompt — commit & push persona work, leave org-level v4.0 untouched

> **2026-09-16:** this tree now lives at top-level `personas/` (see `00-PERSONA-GROUPS.md`).
> Paths listed below are the **2026-09-15** commit set, when the files still sat under
> `foundation/sources/customer_segmentation/`. Do not follow them as current locations.

Paste everything below the line into a fresh agent. Do not edit the allowlist or the freeze list unless Kylor says so.

---

You are on Kylor’s Mac. Working tree:

`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0`

This folder **is** `kylor-johnson/supercat-4.0`. Remote name is **`personal`**, not `origin`.

```
git remote -v
# personal  git@github.com:kylor-johnson/supercat-4.0.git
```

Open **File → Open Workspace from File… → SuperCat.code-workspace** if you need the multi-root workspace. Do not recreate `~/repos/supercat-4.0`.

## What this commit is

Persona / JTBD / surface work from mid-September 2026. SuperCat personas are **five consumption roles** (Admin, VP of sales, executive, sales rep, buyer). Selling motion stays on the **already-stamped org-level v4.0 roster**. Buyer analytics → eCat Online. Rep analytics → a **new** web component inside the offline iPad (`iPad-EC`). Factory copy of this work is still **Hold**.

This is **not** a re-segmentation of clients. The July 9, 2026 org-level work is the authority for “what game is this client playing.”

## Hard freeze — never stage, never edit, never delete

Treat these as sacred. If `git status` or `git diff` shows anything under them, **stop and tell Kylor**. Do not “tidy,” restyle, rename, or “fix the space in the filename.”

```
Customer Segmentation/
Customer Segmentation/current/
Customer Segmentation/v4/
Customer Segmentation/v4/v4.0_archive/
Customer Segmentation/v4/v4.0_archive/SuperCat_Client_Segmentation_v4.0 2.html
```

That archive HTML (`SuperCat_Client_Segmentation_v4.0 2.html`) is the visual sibling of the stamped v4.0 client roster (dark Inter, `--bg #0c0c0f`, `--accent #7f5af0`, luxury gold / premium purple / midmarket green / volume red). The persona review HTML was restyled to match it. **Matching the look is not permission to rewrite the roster.**

Also frozen for this commit (unrelated dirty tree — leave it):

```
Insightful Product 4.0/
.cursor/skills/ecat-session-prep/SKILL.md
```

Do **not** copy anything into `~/repos/agent-factory`. Factory persona splice is Hold until Kylor says otherwise.

Jira is read-only. Do not comment, create, or transition tickets.

Do not create a canvas.

## Do this

1. `cd` into the SuperCat 4.0 tree above.
2. `git status` and `git diff --stat`. Confirm `Customer Segmentation/` is **clean vs HEAD**. If it is not, abort.
3. Stage **only** the allowlist below. Explicit `git add --` paths. Never `git add .` / `git add -A`.
4. Confirm the index with `git diff --cached --stat`. The cached list must not contain `Customer Segmentation/` or `Insightful Product 4.0/`.
5. Commit with the message at the bottom (HEREDOC, no `--no-verify`).
6. `git status` after commit. Working tree should still show Insightful 4.0 dirt and `ecat-session-prep` as unstaged.
7. Push: `git push personal main`.
8. Return the commit SHA and the GitHub URL. Do not open a PR (this is `main`).

User-level copy at `~/.claude/skills/supercat-foundation/SKILL.md` should already match the in-repo `.cursor` / `.claude` copies. It is **outside the git tree** — do not try to commit it. If it still says “motion × seat,” update it to match the in-repo skill, then leave it.

## Stage this (allowlist)

Foundation runtime (persona splice into who-we-serve / what-we-do / CEO context):

```
foundation/00_README.md
foundation/01_what_we_do.md
foundation/02_who_we_serve.md
foundation/CEO_SYSTEM_CONTEXT.md
```

Persona source (the new work):

```
foundation/sources/customer_segmentation/00-SYNTHESIS.md
foundation/sources/customer_segmentation/ASSUMPTIONS.md
foundation/sources/customer_segmentation/CEO-BRIEF.html
foundation/sources/customer_segmentation/CEO-READOUT.html
foundation/sources/customer_segmentation/CHANGELOG.md
foundation/sources/customer_segmentation/DEEP-DIVE-BRIEF.md
foundation/sources/customer_segmentation/FOUNDATION-CORRECTIONS.md
foundation/sources/customer_segmentation/HANDOFF.md
foundation/sources/customer_segmentation/PERSONA-READOUT.html
foundation/sources/customer_segmentation/PERSONA-GROUPS-REVIEW.html
foundation/sources/customer_segmentation/GITHUB-PUSH-PROMPT.md
foundation/sources/customer_segmentation/README.md
foundation/sources/customer_segmentation/_measured/00-FINDINGS.md
foundation/sources/customer_segmentation/_measured/06-SEGMENT-VARIATION.md
foundation/sources/customer_segmentation/_measured/README.md
foundation/sources/customer_segmentation/analytics/jtbd-register.md
foundation/sources/customer_segmentation/engineering/01-NO-NEW-DATA-PACK.md
foundation/sources/customer_segmentation/engineering/02-IPAD-ACCOUNT-BRIEF-SPEC.md
foundation/sources/customer_segmentation/engineering/03-ROADMAP.md
foundation/sources/customer_segmentation/personas/00-PERSONA-GROUPS.md
foundation/sources/customer_segmentation/personas/PER-00-persona-set.md
foundation/sources/customer_segmentation/personas/PER-01-independent-sales-rep.md
foundation/sources/customer_segmentation/personas/PER-02-rep-agency-principal.md
foundation/sources/customer_segmentation/personas/PER-03-vp-sales-sales-ops.md
foundation/sources/customer_segmentation/personas/PER-04-customer-service-order-entry.md
foundation/sources/customer_segmentation/personas/PER-05-product-merchandising.md
foundation/sources/customer_segmentation/personas/PER-06-owner-exec.md
foundation/sources/customer_segmentation/personas/PER-08-dealer-buyer.md
foundation/sources/customer_segmentation/product/data-gaps.md
foundation/sources/customer_segmentation/product/surface-mapping.md
```

Skill copies (in-repo only):

```
.cursor/skills/supercat-foundation/SKILL.md
.claude/skills/supercat-foundation/SKILL.md
```

If `git status` shows extra files under `foundation/sources/customer_segmentation/` that are **not** on this list (e.g. `PER-07`, archives under `_archive/`), include them only if they are clearly part of this persona-groups rewrite. If unsure, leave them unstaged and list them in the report.

## Do not stage

- Anything under `Customer Segmentation/` (current roster, MASTER CSV, HTMLs, `v4/v4.0_archive/`, the ` 2.html` file)
- Anything under `Insightful Product 4.0/`
- `.cursor/skills/ecat-session-prep/SKILL.md`
- Secrets, venvs, `Ready_For_Import/`, live client CSVs
- Nested `agent-factory/`

## Commit message

```
git commit -m "$(cat <<'EOF'
Lock SuperCat personas to five consumption roles on top of stamped v4.0.

Personas are Admin / VP of sales / executive / sales rep / buyer by product
surface. Org-level selling motion stays on Customer Segmentation v4.0 (109 orgs).
Buyer analytics stays on eCat Online; rep analytics is a new offline iPad
component. Does not rewrite the client roster.

EOF
)"
```

## After push

Confirm with:

```
git status
git log -1 --oneline
git ls-tree -r HEAD --name-only | grep -E 'Customer Segmentation/(current|v4)' | head
```

The v4.0 files must still be in HEAD, byte-identical to before this commit. `git show HEAD:"Customer Segmentation/v4/v4.0_archive/SuperCat_Client_Segmentation_v4.0 2.html"` must still exist.

Report: SHA, `personal/main` URL, what was committed, confirmation that `Customer Segmentation/` was not in the commit, Insightful dirt still local.
