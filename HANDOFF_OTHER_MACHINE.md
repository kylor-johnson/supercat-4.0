# Other-machine setup — paste this into a fresh Cursor agent chat

> **Last updated**: 2026-09-04
>
> This prompt is for the **other Mac** (the one that is not already cloned).
> It does not migrate iCloud. It makes that Mac work from GitHub.

---

Copy everything below the line.

---

# Other Mac: clone SuperCat repos and open the right workspace

You are on the **second Mac**. Do not touch iCloud `SuperCat 4.0` git except to
read. Do not `git add .` anywhere. Do not push to `company` /
`SuperCatSolutionsLLC/agentic_operations`.

## Goal

This computer edits GitHub clones under `~/repos`, same as the first Mac.

## 1. Auth

Confirm GitHub works as `kylor-johnson`:

```bash
gh auth status
ssh -T git@github.com
```

Fix auth before cloning if either fails.

## 2. Clone (skip a repo if the folder already exists — pull instead)

```bash
mkdir -p ~/repos
cd ~/repos

git clone --branch main git@github.com:kylor-johnson/supercat-4.0.git supercat-4.0
git clone --branch main git@github.com:kylor-johnson/ecat-onboarding-workspace.git ecat-onboarding-workspace
git clone git@github.com:SuperCatSolutionsLLC/agent-factory.git agent-factory
```

If `supercat-4.0` already exists and is still on `ecat-onboarding-main`:

```bash
cd ~/repos/supercat-4.0
git fetch origin
git checkout main
git pull
```

If clone of `supercat-4.0` fails on `main`, the rename has not landed — clone
`--branch ecat-onboarding-main` and report that.

Product code (separate): confirm `~/supercat-code` exists. If missing, clone
that repo the same way Kylor already does on the first Mac. Do not invent a
remote.

## 3. Verify

```bash
git -C ~/repos/supercat-4.0 remote -v
git -C ~/repos/supercat-4.0 branch -vv
git -C ~/repos/supercat-4.0 log -1 --oneline

git -C ~/repos/ecat-onboarding-workspace remote -v
git -C ~/repos/ecat-onboarding-workspace log -1 --oneline

git -C ~/repos/agent-factory log -1 --oneline
```

Expect:

| Clone | Remote | Branch |
|---|---|---|
| `~/repos/supercat-4.0` | `kylor-johnson/supercat-4.0` (private) | `main` |
| `~/repos/ecat-onboarding-workspace` | `kylor-johnson/ecat-onboarding-workspace` (**private**) | `main` |
| `~/repos/agent-factory` | `SuperCatSolutionsLLC/agent-factory` | `main` |

`ecat-onboarding-workspace` is private because it holds live client CSVs
(customers, order/invoice, dealers, territories). Do not make it public.

## 4. Open Cursor correctly

**File → Open Workspace from File… →**

`~/repos/supercat-4.0/SuperCat.code-workspace`

That workspace has three roots:

- **SuperCat Ops** → `~/repos/supercat-4.0`
- **eCat Implementation** → `~/repos/ecat-onboarding-workspace`
- **supercat-code** → `~/supercat-code`

Do **not** open

`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0`

as the working folder.

## 5. How work is split

| Work | Repo |
|---|---|
| Skills, rules, onboarding-models, PM, foundation, reports | `~/repos/supercat-4.0` |
| Live client onboarding (Legrand, jcusa, Fine Art, …) | `~/repos/ecat-onboarding-workspace` → `02_Implementation/` |
| Company weekly agents / PRs | `~/repos/agent-factory` (branch `kjael/<topic>`) |

Switching Macs: pull, work, commit, push. Other Mac: pull.

`eCat_Onboarding/` inside `supercat-4.0` is kickoff + registry + pointers only.
**Do not recreate live client folders there.** Canonical client trees are
`02_Implementation/<Client Name>/`.

## 6. Do not

- `git add .` on any iCloud tree (dataless files hydrate)
- Commit `integrations/` HubSpot/Fathom/BigQuery service-account files (secrets)
- Commit `_archive/`, Health museums, Insightful 2/3/4, `agent-factory/` into 4.0
- Push `supercat-4.0` to `agentic_operations`
- Delete iCloud `SuperCat 4.0` or `SuperCat_Simple_Final` this week (CSV + museum leftover)
- Use `git add .` in Implementation (images / xlsx / Ready_For_Import stay ignored)

## 7. Report back

Paths, remotes, branches, and `git log -1 --oneline` for all three clones.
Confirm the workspace file opened with three roots.
