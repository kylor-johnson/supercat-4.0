# SuperCat Cursor Workspace

> **Last updated**: 2026-09-16

## This Mac — always open this way

**File → Open Workspace from File… →**
`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace`

Pin **SuperCat (Workspace)** in **File → Open Recent** so it stays at the top.

That iCloud folder **is** the `kylor-johnson/supercat-4.0` git working tree.
`~/repos/supercat-4.0` does not exist on this Mac. Do not clone it here.

## What's in this workspace

| Root | Path | Purpose |
|------|------|---------|
| **SuperCat Ops** | iCloud `SuperCat 4.0` | Skills, rules, onboarding-models, PM, foundation, reports |
| **eCat Implementation** | `~/repos/ecat-onboarding-workspace` | Live client onboarding (`02_Implementation/`) |
| **supercat-code** | `~/supercat-code` | `supercat_server`, `sarreid_ios` |

Hang-tag spike (tracked in this ops git): `SuperCat Ops/hang-tag-spike` — see `SPIKE.md`. Other Mac: `~/repos/supercat-4.0/hang-tag-spike` after pull, then `npm install`.

`SuperCat.code.macbook-workspace` keeps `~/repos/supercat-4.0` roots for the
**other Mac** after it clones from GitHub. Do not use it on this Mac.

## Do not

- Open iCloud `SuperCat 4.0` as a plain **folder** (splits agent chat history) — open the `.code-workspace` file
- Open `~/supercat-code` alone
- Use **Add Folder to Workspace** without saving — creates ephemeral workspaces and orphans chats
- Recreate live client folders under `eCat_Onboarding/` — those trees live in the private Implementation repo
- `git add` Health / Insightful museums, nested `agent-factory/`, or `integrations/` keys

## Finding old agent chats

Most history lives on disk even when the sidebar doesn't show it. Search:

- **`AGENT_CHAT_INDEX.md`** in SuperCat Ops — date, title, and chat ID for all transcripts
- Raw files: `~/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-comappleCloudDocs-SuperCat-4-0/agent-transcripts/` (and leftover `.../Users-kylorjohnson-repos-supercat-4-0/` metadata from the old clone path)

## Open Recent cleanup

See **`OPEN_RECENT_CLEANUP.md`** for entries to remove from File → Open Recent. No folders are deleted — this only tidies the menu.

## Legacy workspace file

`SuperCat 4.0.code-workspace` is gitignored. Ignore it. Use `SuperCat.code-workspace` from this folder.
