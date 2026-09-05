# SuperCat Cursor Workspace

> **Last updated**: 2026-09-04

## Always open this way

**File → Open Workspace from File… → `~/repos/supercat-4.0/SuperCat.code-workspace`**

Pin it in **File → Open Recent** so it stays at the top.

Do **not** open iCloud `SuperCat 4.0` as the working folder. The source of
truth is the GitHub clones under `~/repos`.

## What's in this workspace

| Root | Path | Purpose |
|------|------|---------|
| **SuperCat Ops** | `~/repos/supercat-4.0` | Skills, rules, onboarding-models, PM, foundation, reports |
| **eCat Implementation** | `~/repos/ecat-onboarding-workspace` | Live client onboarding (`02_Implementation/`) |
| **supercat-code** | `~/supercat-code` | `supercat_server`, `sarreid_ios` |

`SuperCat.code.macbook-workspace` is the same three-root file (kept for the other Mac).

## Do not

- Open iCloud `SuperCat 4.0` as a plain **folder** (splits agent chat history)
- Open `~/supercat-code` alone
- Use **Add Folder to Workspace** without saving — creates ephemeral workspaces and orphans chats
- Recreate live client folders under `eCat_Onboarding/` — those trees live in the private Implementation repo

## Finding old agent chats

Most history lives on disk even when the sidebar doesn't show it. Search:

- **`AGENT_CHAT_INDEX.md`** in SuperCat Ops — date, title, and chat ID for all transcripts
- Raw files: `~/.cursor/projects/Users-kylorjohnson-repos-supercat-4-0/agent-transcripts/`

## Open Recent cleanup

See **`OPEN_RECENT_CLEANUP.md`** for entries to remove from File → Open Recent (right-click → Remove from List). No folders are deleted — this only tidies the menu.

## Legacy workspace file

`SuperCat 4.0.code-workspace` pointed at iCloud. Ignore it. Use `SuperCat.code-workspace` from `~/repos/supercat-4.0`.
