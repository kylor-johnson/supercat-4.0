---
name: migration-audit
description: Diagnose admin v2 migration completeness by analyzing which controller actions can render in admin_v2/supercat_v2 layouts. Use when checking migration progress, finding gaps, verifying coverage, or when the user asks about remaining v2 work. Produces a structured gap report.
---

# Migration Audit Diagnostic

Programmatic analysis of which admin controller actions can render under the modern `admin_v2` / `supercat_v2` layouts versus falling through to the legacy `application` / `supercat` layout.

## When to Use

- Before planning a migration batch — identify which actions still need v2 views
- After completing a batch — verify coverage and track progress
- When a user reports a page rendering in the legacy layout unexpectedly
- To generate an updated gap report for planning or PR descriptions

## How It Works

A controller action is considered **"renderable in admin_v2"** when ALL of these are true:

1. The controller includes `UiSwitchable` (org pages) or `SupercatUiSwitchable` (global/SuperCat pages)
2. The action method contains a `modern_ui?` conditional
3. That conditional renders a `_v2` view with the `admin_v2` or `supercat_v2` layout
4. The `_v2.html.erb` view file exists on disk

Actions that only redirect, return JSON, stream data, or return `head :ok` are **skipped** — they don't render HTML layouts.

## Running the Audit

### Rake task (recommended)

```bash
bash -lc 'source ~/.rvm/scripts/rvm && rvm use 3.0.6 && cd /path/to/supercat_server && bundle exec rake migration:audit'
```

This produces a markdown report to stdout with:

1. **Summary** — total actions, done count, gap count, skip count
2. **Gap Report** — every HTML action that lacks a v2 path
3. **Per-Controller Detail** — each controller with per-action status and migration percentage

### Saving the report

```bash
bundle exec rake migration:audit 2>/dev/null > docs/design/migration-audit-report.md
```

## Understanding the Output

### Status values

| Status | Meaning | Action needed |
|--------|---------|--------------|
| `DONE` | `modern_ui?` check exists AND `_v2` view file found | None |
| `**GAP**` | Action renders HTML but has no `modern_ui?` branching or `_v2` view | Needs migration |
| `VIEW ONLY` | A `_v2` view file exists in the directory but the action doesn't reference it via `modern_ui?` | May need controller wiring |
| `PARTIAL` | `modern_ui?` exists but no matching `_v2` template found | View file missing |
| `redirect_only` | Action only redirects, no HTML render | Skipped (no migration needed) |
| `json_or_api` | Action renders JSON, streams data, or returns head | Skipped |

### Migration percentage

Each controller shows `X% migrated` — the ratio of DONE actions to total HTML-rendering actions. Controllers at 100% are fully migrated. Controllers showing 33% typically have `index` done but `new` and `edit` still pending.

## Key Files

| File | Purpose |
|------|---------|
| `lib/tasks/migration_audit.rake` | The rake task source |
| `docs/design/migration-audit-report.md` | Latest saved report |
| `docs/design/page-inventory.md` | Master tracker with CRUD Gap Analysis |
| `docs/design/admin-page-taxonomy.yaml` | Route taxonomy (primary actions) |

## Interpreting Results for Migration Planning

### Common patterns

**"Index-only" controllers (33% migrated):** The most common pattern. `index` has `modern_ui?` + `index_v2.html.erb`, but `new`, `edit`, and sometimes `show` still render legacy views. The legacy `_form.html.erb` partial is shared by both `new` and `edit`.

**Batch by shared form partial:** Many controllers share the same form pattern (`_form.html.erb` used by both `new.html.erb` and `edit.html.erb`). When migrating, create:
- `new_v2.html.erb` and `edit_v2.html.erb` using the `_form` archetype
- Wire `create` (failure) and `update` (failure) to re-render the v2 form
- The migration skill (`admin-page-migration/SKILL.md`) documents this pattern

**Redirect/API actions:** Actions that only redirect (e.g., `destroy`, `create` on success) or return JSON don't need v2 views. The audit skips these automatically.

## Workflow: Running After a Migration Batch

1. Complete a batch of migrations (e.g., all custom field controllers)
2. Run `rake migration:audit` to verify
3. Check that gap count decreased by the expected amount
4. Save updated report: `bundle exec rake migration:audit 2>/dev/null > docs/design/migration-audit-report.md`
5. Update `docs/design/page-inventory.md` batch tables with Done status

## Limitations

- The rake task uses static analysis (regex parsing of controller files), not runtime introspection. Complex conditional renders or metaprogrammed actions may be misclassified.
- `respond_to` blocks with both HTML and JSON formats may cause false positives/negatives.
- Actions that render via `before_action` callbacks aren't tracked.
- The audit doesn't verify visual fidelity — only that the wiring (controller + view file) exists.
