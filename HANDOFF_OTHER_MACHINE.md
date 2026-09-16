# Other-machine setup — paste this into a fresh Cursor agent chat

> **Last updated**: 2026-09-16
>
> This prompt is for the **other Mac** (the one that is not already cloned).
> It does not migrate iCloud. It makes that Mac work from GitHub clones
> under `~/repos`.

---

## Two-Mac split

| Mac | Ops git working tree | Workspace file to open |
|---|---|---|
| **This Mac** | `~/repos/supercat-4.0` | `SuperCat.code-workspace` (Ops root = `~/repos/supercat-4.0`; live clients = iCloud `SuperCat_Simple_Final`) |
| **Other Mac** | `~/repos/supercat-4.0` | `SuperCat.macbook.code-workspace` (Ops root = `~/repos/supercat-4.0`; live clients = `~/repos/ecat-onboarding-workspace`) |

**iCloud `SuperCat 4.0` is an unread trap on both Macs.** Do not open it, do not
commit from it. Leave it on disk. Edit GitHub clones under `~/repos`.

**Do not iCloud-download** (leave cloud icons; never “Download Now”):

- `SuperCat 4.0/repos/` and `SuperCat 4.0/repos 2/` (Finder duplicates; nested clones)
- `node_modules`, `.next`, `.venv`, `.venv-renderer` anywhere under SuperCat 4.0
- Nested clones inside those `repos` folders (`agent-factory`, `ecat-onboarding-workspace`, `supercat-4.0`, `agent-factory-lab`)
- `cursor-to-claude-migration/`, `integrations/` secrets, Insightful 2.0/3.0 museums, Health venvs

Hang-tag spike **is** in this private repo: `hang-tag-spike/` inside
`kylor-johnson/supercat-4.0`. After clone/pull:

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npm install
npm run dev
```

See `hang-tag-spike/SPIKE.md`. Do not wait for iCloud to bring it.

Copy everything below the line.

---

# Other Mac: clone SuperCat repos and open the right workspace

You are on the **second Mac**. Do not touch iCloud `SuperCat 4.0` git except to
read. Do not `git add .` anywhere. Do not push to `company` /
`SuperCatSolutionsLLC/agentic_operations`.

## Goal

This computer edits GitHub clones under `~/repos`. Both Macs' ops tree is
`~/repos/supercat-4.0`. iCloud `SuperCat 4.0` is an unread trap.

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

Hang-tag spike is a folder inside `supercat-4.0`, not its own clone:

```bash
cd ~/repos/supercat-4.0/hang-tag-spike
npm install   # local only — never commit node_modules
npm run dev   # http://localhost:3000
```

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

`~/repos/supercat-4.0/SuperCat.macbook.code-workspace`

That workspace has three roots:

- **SuperCat Ops** → `~/repos/supercat-4.0`
- **eCat Implementation** → `~/repos/ecat-onboarding-workspace`
- **supercat-code** → `~/supercat-code`

Do **not** open

`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0`

as the working folder or as the git working tree on this Mac.

Prefer `SuperCat.macbook.code-workspace` on this Mac (live clients =
`~/repos/ecat-onboarding-workspace`). `SuperCat.code-workspace` Ops root is
also `~/repos/supercat-4.0`; its Implementation root is iCloud
`SuperCat_Simple_Final`.

## 5. How work is split

| Work | Repo |
|---|---|
| Skills, rules, onboarding-models, PM, foundation, reports | `~/repos/supercat-4.0` |
| Hang-tag Next spike (Kuzco / Avery) | `~/repos/supercat-4.0/hang-tag-spike` — pull, then `npm install` |
| Live client onboarding (Legrand, jcusa, Fine Art, …) | `~/repos/ecat-onboarding-workspace` → `02_Implementation/` |
| Company weekly agents / PRs | `~/repos/agent-factory` (branch `kjael/<topic>`) |

Switching Macs: pull, work, commit, push. Other Mac: pull.

`eCat_Onboarding/` inside `supercat-4.0` is kickoff + registry + pointers only.
**Do not recreate live client folders there.** Canonical client trees are
`02_Implementation/<Client Name>/`.

## 6. Do not

- Open iCloud `SuperCat 4.0` as the git tree or Cursor workspace on this Mac
- **Download Now** on iCloud for: `repos/`, `repos 2/`, `node_modules`, `.next`, `.venv`, `.venv-renderer`, nested `agent-factory` / `ecat-onboarding-workspace` / `supercat-4.0` inside those folders, `cursor-to-claude-migration/`, `integrations/` keys, Insightful 2.0/3.0, Health venvs
- Wait for hang-tag-spike via iCloud — it is `~/repos/supercat-4.0/hang-tag-spike` after pull; `npm install` locally
- `git add .` on any iCloud tree (dataless files hydrate)
- Commit `integrations/` HubSpot/Fathom/BigQuery service-account files (secrets)
- Commit `_archive/`, Health museums, Insightful 2/3/4, `agent-factory/` into 4.0
- Push `supercat-4.0` to `agentic_operations`
- Delete iCloud `SuperCat 4.0` or `SuperCat_Simple_Final` this week (CSV + museum leftover)
- Use `git add .` in Implementation (images / xlsx / Ready_For_Import stay ignored)
- Never commit Health museums, Insightful 2/3/4, nested `agent-factory/`, `_archive/`, or secrets

## 7. Report back

Paths, remotes, branches, and `git log -1 --oneline` for all three clones.
Confirm the workspace file opened with three roots.
