---
name: rails-code-review
description: Review Rails pull requests for correctness, readability, performance, DRY violations, and adherence to project standards. Use when the user asks to review a PR, review a branch, perform a code review, check code quality, or evaluate changes on a git branch.
---

# Rails Code Review

Review a git branch against master in an isolated worktree, then produce a structured report covering correctness, readability, performance, DRY compliance, and project conventions.

## Quick Start

When the user provides a branch name (or PR number), run the review:

1. **Set up an isolated worktree** (never touch the current working tree)
2. **Run automated checks** (RuboCop, RubyCritic)
3. **Read and analyze the diff** against master
4. **Produce a structured review report**

## Phase 1: Isolated Worktree Setup

Run `scripts/setup-worktree.sh` from this skill's directory to create a temporary worktree:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/setup-worktree.sh <branch-name>
```

This creates a worktree at `/tmp/supercat-review-<branch>`. All subsequent commands run there. When finished, clean up:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/setup-worktree.sh --cleanup <branch-name>
```

## Phase 2: Automated Checks

Run these in the worktree directory:

```bash
# RuboCop on changed files only (mirrors bin/rubocop-branch)
git diff-tree -r --no-commit-id --name-only master@{u} HEAD | \
  xargs ls -1 2>/dev/null | \
  xargs bundle exec rubocop --force-exclusion

# Check if changed files appear in .rubocop_todo.yml (should not)
git diff-tree -r --no-commit-id --name-only master@{u} HEAD | while read f; do
  grep -q "$f" .rubocop_todo.yml && echo "WARN: $f is in .rubocop_todo.yml"
done

# RubyCritic on changed app/ files (readability scores)
changed_app_files=$(git diff-tree -r --no-commit-id --name-only master@{u} HEAD | grep '^app/')
if [ -n "$changed_app_files" ]; then
  echo "$changed_app_files" | xargs bundle exec rubycritic --no-browser --format console
fi
```

Record all output for the report.

**RuboCop must pass with zero offenses.** Any offense is a "Must fix" finding.

## Phase 3: Manual Review

Read the full diff: `git diff master...HEAD` in the worktree.

Work through each review dimension below. For the detailed checklist, see [review-checklist.md](review-checklist.md).

### 3a. Understand the Change

- Identify scope: new feature, bug fix, refactor, or chore.
- Read the commit messages — do they follow [Chris Beams's commit style](https://cbea.ms/git-commit/)?
- Are commits small and single-purpose per `CODING_CONVENTIONS.md`?

### 3b. Correctness

- Edge cases: nil, empty, zero, negative, boundary values.
- Error handling: rescue blocks, fallback behavior, user-facing error messages.
- Async/background jobs: race conditions, retry safety, idempotency.
- Off-by-one errors in loops, ranges, array/hash access.
- Database: migrations match model validations; foreign keys present where needed.

### 3c. Readability & Clean Code

Apply the [Ruby Style Guide](https://rubystyle.guide/) and Uncle Bob's Clean Code principles:

- **Naming**: Variables, methods, and classes express intent. Prefer full English words over abbreviations. No `d`, `tmp2`, `data` — use `elapsed_time_in_days`, `pending_orders`, etc.
- **Method size**: Methods should do one thing. Flag methods exceeding 15 lines (project limit) or with cyclomatic complexity > 8.
- **Class size**: Flag classes exceeding 150 lines (project limit).
- **Comments**: Code should be self-documenting. Comments explain *why*, never *what*. Flag stale or redundant comments.
- **Nesting depth**: Flag conditionals nested 3+ levels deep. Suggest guard clauses, early returns, or extract-method.
- **Magic numbers/strings**: Should be named constants.
- **Readability score**: Note RubyCritic scores. Anything rated C or lower warrants a "Should fix" finding.

### 3d. DRY & Duplication Analysis

This is critical — a PR must not introduce logic that already exists elsewhere.

- **Search the codebase** for similar method names, query patterns, service objects, or business rules that overlap with the new code.
- Use `rg` (ripgrep) to search for key terms, class names, and method signatures in the existing `app/` tree.
- Flag any net-new functionality that duplicates or reimplements existing behavior.
- Suggest extracting shared logic into concerns, service objects, or utility methods.
- Check for copy-pasted code blocks within the PR itself.

### 3e. Performance

- **N+1 queries**: Look for `.each` loops that trigger lazy-loaded associations. Suggest `includes`, `preload`, or `eager_load`.
- **Missing indexes**: If new queries filter/sort on columns, verify indexes exist in `db/schema.rb`.
- **Unbounded queries**: Flag `.all` or `.where` without `.limit` on large tables.
- **Expensive operations in loops**: API calls, file I/O, or complex computations inside iterators.
- **Memoization**: Appropriate use of `||=` for expensive computations; not over-applied to simple accessors.

### 3f. Rails-Specific Concerns

- **`unscoped` usage**: Banned by custom cop `CustomCops::NoUnscoped`. Flag any attempts to bypass.
- **`module_function` in classes**: Banned by custom cop `CustomCops::ModuleFunctionInClass`.
- **Strong parameters**: All user input properly permitted.
- **Callbacks**: Prefer explicit service objects over complex callback chains.
- **Scopes vs class methods**: Prefer scopes for simple queries, class methods for complex logic.

### 3g. Project Architecture Patterns

These patterns reflect the team's preferred Rails style and have repeatedly surfaced in code review. Flag each one as a **Should Fix**.

- **Multi-tenancy scoping**: AR queries must start from an instance variable, never from the AR class directly. `@current_org.rep_activities.active` not `RepActivity.where(organization: @current_org)`. This prevents accidental cross-tenant data leaks.
- **Filter methods belong on the model**: Controller private methods like `filter_by_customer`, `apply_filters` are a smell. Each filter should be a named model scope so the controller reads `@records.for_org_user(params[:org_user_id]).for_customer_query(params[:customer_query])`.
- **before_action for business logic**: `before_action` is for auth, permission, and resource lookup. Validation logic (e.g., parsing/checking date params) belongs inside the controller action or a model scope — not in a callback.
- **Service object overuse**: The project prefers model instance methods and scopes over service objects for simple operations. Flag any service class that wraps a single `update`, `destroy`, or query that would read naturally as a model method. Good test: if the entire call site becomes `record.method_name`, the service class is unnecessary.
- **ApplicationInteraction vs PORC**: New service objects should be Plain Old Ruby Classes, not `ApplicationInteraction` subclasses. Flag any new class inheriting from `ApplicationInteraction`.
- **DAO / query-wrapper classes are a smell**: Classes whose sole job is to memoize or wrap a handful of AR queries (e.g., a `DashboardData` service) should be replaced by model scopes or, where appropriate, inline AR calls in the controller or view. Memoization of eager-loaded associations is usually slower, not faster.
- **Raw SQL strings when AR queries suffice**: Flag raw SQL (`<<~SQL`, `find_by_sql`, `connection.select_all`, `connection.execute`) when the same result is achievable with standard AR scopes, `where`, `joins`, or Arel. Raw SQL is acceptable only when AR genuinely cannot express the query (e.g., window functions, recursive CTEs). UNION queries that combine two models should first attempt separate AR queries combined in Ruby.
- **Struct as an AR model substitute**: A `Struct` that mirrors columns from one or more AR models is a smell. It usually means the code should use the AR models directly (polymorphically), add a `to_timeline_entry` / `as_timeline_entries` instance or class method on each model, or use STI. Flag any `Struct.new` in a service object whose fields map to existing AR columns.
- **Manual pagination reimplementing Pagy**: Flag any service or controller that computes `OFFSET`/`LIMIT` by hand, or builds a custom `total_count` method that wraps `SELECT COUNT(*)`. If the data source is AR, use `pagy(@scope)`. For cross-model collections, use `Pagy.new(count:)` with the model's `.count`, not hand-rolled SQL counts.
- **Serializers use `to_h`**: The project standard is plain `to_h` methods, not `ActiveModel::Serializer`. Flag any new AMS subclass.
- **Pagy for pagination**: The project standard is Pagy. Flag `paginate(page:, per_page:)` (will_paginate / Kaminari `.paginate` API) and suggest migration to `pagy(@records)`.
- **`update` vs `update!` in models**: Model mutation methods should use `update` and return a boolean so callers can decide how to handle failure. Reserve `update!` for cases where an exception is explicitly the right behavior. If the method uses `update` (no bang), the method name should also drop the `!`.
- **Unnecessary mailer instance variables**: When a mailer already has `@record`, don't assign `@record.association` to separate instance variables. The view can call `@record.association` directly.
- **Tiny/unnecessary private methods**: A one-liner private method that is called in only one place and adds no clarity is noise. Either inline it or fold it into a model method. Chains of single-line wrapper methods (e.g., `effective_x` calls `filter_x || default_x`, where `default_x` returns a literal) are a particularly common form of this smell.
- **Controller instance variable proliferation**: More than ~3 controller instance variables passed to a view is a smell. Prefer helper methods, inline expressions in the view, or a presenter/view object. If a value is only used in the view for a form default, compute it inline in the view rather than assigning an instance variable.
- **Redundant view fallbacks**: When a controller already computes a fallback value (e.g., `@date = params[:date] || default`), the view should not add another `|| @date` layer. If the view needs its own fallback, remove the controller instance variable and put the full expression in the view instead.

### 3g. Testing

- Are there tests for new/changed code?
- Do tests cover happy path AND error/edge cases?
- Are tests isolated (no shared mutable state, proper `setup`/`teardown`)?
- Do tests use factories (`factory_bot`) appropriately?
- For bug fixes: is there a regression test that would have caught the bug?

## Phase 4: Report

Produce the review in this format:

```markdown
# Code Review: <branch-name>

## Summary
- **Scope**: [new feature | bug fix | refactor | chore]
- **Files changed**: N
- **RuboCop**: [PASS | FAIL (N offenses)]
- **RubyCritic**: [scores for changed files]

## What's Done Well
- [Acknowledge good patterns, clean code, thorough tests, etc.]

## Findings

### Must Fix
> Bugs, security issues, data loss risks, RuboCop failures

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | path/to/file.rb | 42 | Description | Suggestion |

### Should Fix
> Performance issues, maintainability concerns, DRY violations, low readability scores

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | path/to/file.rb | 42 | Description | Suggestion |

### Nit
> Style preferences beyond what RuboCop enforces, minor suggestions

| # | File | Line | Issue | Suggested Fix |
|---|------|------|-------|---------------|
| 1 | path/to/file.rb | 42 | Description | Suggestion |

## DRY Analysis
- [List any existing code that overlaps with new additions]
- [Recommend consolidation opportunities]
```

## Project-Specific Standards Reference

This project enforces these via `.rubocop.yml`:

| Metric | Limit |
|--------|-------|
| Method length | 15 lines (comments excluded; arrays/hashes/heredocs count as 1) |
| Class length | 150 lines |
| Module length | 150 lines |
| Block length | 50 lines |
| Cyclomatic complexity | 8 |
| ABC size | 20 |
| Parameters | 6 (keyword args excluded) |

Disabled cops (do not flag these as style issues): `LineLength`, `TrailingCommaInArguments`, `AndOr`, `Documentation`, `RedundantReturn`, `FrozenStringLiteralComment`, `GuardClause`, `AccessModifierDeclarations`, `IfUnlessModifier`, `SpaceInsideArrayLiteralBrackets`, `SpaceInsideHashLiteralBraces`, `SpaceInsideBlockBraces`, `FormatStringToken`.

See [review-checklist.md](review-checklist.md) for the full detailed checklist.
