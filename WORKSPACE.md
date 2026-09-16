# SuperCat Cursor Workspace

> **Last updated**: 2026-09-16

## This Mac — always open this way

**File → Open Workspace from File… →**
`~/repos/supercat-4.0/SuperCat.code-workspace`

Pin **SuperCat (Workspace)** in **File → Open Recent** so it stays at the top.

That folder **is** the `kylor-johnson/supercat-4.0` git working tree
(remotes `origin` / `personal`). Location map: [`WHERE.md`](WHERE.md).

**iCloud `SuperCat 4.0` is an unread trap.** Do not open it, do not commit from
it. Leave it on disk; it is not the working tree.

## What's in this workspace

| Root | Path | Purpose |
|------|------|---------|
| **SuperCat Ops** | `~/repos/supercat-4.0` | This git tree — skills, foundation, Insightful 4.0, Health V3 |
| **eCat Implementation** | iCloud `SuperCat_Simple_Final` | Live client onboarding (`02_Implementation/`) = `kylor-johnson/ecat-onboarding-workspace` (also `~/repos/ecat-onboarding-workspace` symlink) |
| **supercat-code** | `~/supercat-code` | `supercat_server`, `sarreid_ios` |

Hang-tag spike is tracked in this ops git at `hang-tag-spike/` — see `SPIKE.md`.
It is not a fourth workspace root. After clone/pull: `cd hang-tag-spike && npm install`
(local only; `node_modules` gitignored).

Company factory is `~/repos/agent-factory` (`SuperCatSolutionsLLC/agent-factory`).
Never open the nested copy inside iCloud SuperCat 4.0. Factory is not a workspace
root on this Mac.

`SuperCat.macbook.code-workspace` is for the **other Mac** (ops =
`~/repos/supercat-4.0`; live clients there =
`~/repos/ecat-onboarding-workspace`). This Mac's live clients are iCloud
`SuperCat_Simple_Final` (the `~/repos/ecat-onboarding-workspace` symlink
resolves to the same folder).

## Do not

- Open iCloud `SuperCat 4.0` as a workspace, folder, or git working tree — it is a trap copy
- Open `~/supercat-code` alone
- Use **Add Folder to Workspace** without saving — creates ephemeral workspaces and orphans chats
- Recreate live client folders under `eCat_Onboarding/` — those trees live in iCloud `SuperCat_Simple_Final`
- `git add` Health / Insightful museums, nested `agent-factory/`, or `integrations/` keys

## Finding old agent chats

Most history lives on disk even when the sidebar doesn't show it. Search:

- **`AGENT_CHAT_INDEX.md`** in SuperCat Ops — date, title, and chat ID for all transcripts
- Raw files: `~/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-comappleCloudDocs-SuperCat-4-0/agent-transcripts/` (and leftover `.../Users-kylorjohnson-repos-supercat-4-0/` metadata from the old clone path)

## Open Recent cleanup

See **`OPEN_RECENT_CLEANUP.md`** for entries to remove from File → Open Recent. No folders are deleted — this only tidies the menu.

## Legacy workspace file

`SuperCat 4.0.code-workspace` is gitignored. Ignore it. Use `SuperCat.code-workspace` from this folder.
