# Open Recent Cleanup

**Status (2026-09-15):** Keep using the iCloud workspace file on this Mac.
`SuperCat (Workspace)` is pinned and first in the list.

This only hides menu entries. **No folders or files are deleted.**

## Use going forward (this Mac)

```
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace
```

That iCloud folder **is** the `kylor-johnson/supercat-4.0` git working tree.
Open the **workspace file**, not the `SuperCat 4.0` folder — a plain-folder
open splits agent chat history.

Pin **SuperCat (Workspace)** in File → Open Recent.

## macOS: right-click does NOT work in the menu bar

**File → Open Recent** in the top menu bar has no right-click on individual items on macOS.
Use the quick pick instead:

1. `Cmd+Shift+P` → **Open Recent**
2. Hover an entry → click the **pin** or **×** icons on the right

Individual `.md` / `.py` files still show under workspaces in the menu — that's normal.
They don't split agent chat history; only workspace/folder entries do.

---

## Remove — splits SuperCat agent chat history

| Menu label | Why remove |
|------------|------------|
| `SuperCat 4.0/6-3 (Workspace)` | Superseded by `SuperCat.code-workspace` |
| `SuperCat 4.0` (folder) | Same work, different chat bucket than the workspace file |
| `supercat-code` (folder) | Opens code only — no ops context, separate chats |

## Remove — dead or legacy SuperCat entry points

| Menu label | Why remove |
|------------|------------|
| `SuperCat - Cursor 2.0` | Legacy; folder may no longer exist |
| `SuperCat - Cursor 3.0` | Legacy; folder may no longer exist |
| `SuperCat - Cursor` | Legacy; folder may no longer exist |
| `KYLOR 2.0 (Workspace)` | Old multi-root workspace pointing at dead folders |

## Keep (not SuperCat — leave unless you want a shorter menu)

| Menu label | Notes |
|------------|-------|
| `App Ideas` | Separate project |
| `KB Automation` | Separate project |
| `KB Creation (Workspace)` | Separate project |

## Pin after cleanup

`SuperCat (Workspace)` should stay pinned. To verify or re-pin:

1. `Cmd+Shift+P` → **Open Recent**
2. Find `SuperCat (Workspace)` → click the **pin** icon on the right

Or: **File → Open Workspace from File… →**
`~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace`

---

## Full paths (for reference)

**Remove from Open Recent (do not delete these folders):**
```
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/6-3.code-workspace
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0   ← folder open only
~/supercat-code   ← folder open only
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat - Cursor 2.0
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat - Cursor 3.0
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat - Cursor
~/Library/Mobile Documents/com~apple~CloudDocs/KYLOR 2.0.code-workspace
```

**Use going forward:**
```
~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/SuperCat.code-workspace
```
