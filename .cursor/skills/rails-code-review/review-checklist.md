# Detailed Code Review Checklist

Full reference for each review dimension. SKILL.md links here for depth.

---

## 1. Correctness

### Edge Cases
- [ ] Nil/null inputs handled (use `&.` safe navigation or explicit nil checks)
- [ ] Empty collections: does the code behave correctly with `[]`, `{}`, `""`?
- [ ] Zero and negative numbers where numeric input expected
- [ ] Boundary values (first/last element, max int, empty string vs nil)
- [ ] Unicode and special characters in string processing

### Error Handling
- [ ] `rescue` blocks catch specific exceptions, not bare `rescue` (avoid blind rescues)
- [ ] Errors are logged with sufficient context for debugging
- [ ] User-facing error messages are helpful without leaking internals
- [ ] External service failures degrade gracefully (API timeouts, network errors)
- [ ] Database constraint violations handled (uniqueness, foreign keys)

### Async / Background Jobs
- [ ] Jobs are idempotent (safe to retry)
- [ ] Race conditions addressed (optimistic locking, database-level uniqueness)
- [ ] Timeouts set for external calls
- [ ] Queue/priority appropriate for the job's urgency

### Data Integrity
- [ ] Migrations include rollback strategy
- [ ] Model validations match database constraints
- [ ] Foreign keys have `dependent:` strategy or DB-level cascades
- [ ] Transactions wrap multi-step writes that must be atomic

---

## 2. Readability & Clean Code

Grounded in [Ruby Style Guide](https://rubystyle.guide/) and Robert C. Martin's Clean Code.

### Naming (The Most Important Habit)
- [ ] Method names describe what they do: `calculate_shipping_cost`, not `calc` or `process`
- [ ] Variable names reveal intent: `unpaid_invoices`, not `list` or `data`
- [ ] Boolean methods end with `?`: `active?`, `can_ship?`
- [ ] Dangerous methods end with `!`: `save!`, `delete!`
- [ ] No single-letter variables outside tiny blocks (`items.each { |i| ... }` is OK; `i = Invoice.find(...)` is not)
- [ ] Constants use SCREAMING_SNAKE_CASE
- [ ] Classes/modules use CamelCase

### Method Design (Single Responsibility)
- [ ] Each method does one thing at one level of abstraction
- [ ] Methods read top-down: high-level orchestration calls lower-level details
- [ ] Extract till you drop: if a comment explains a block, extract it into a named method
- [ ] No side effects hidden in query methods (methods that return data shouldn't also modify state)

### Complexity
- [ ] Nesting depth <= 2 levels preferred; 3+ is a smell
- [ ] Cyclomatic complexity within project limit (8)
- [ ] Long conditionals extracted into predicate methods
- [ ] `case`/`when` preferred over long `if`/`elsif` chains

### Comments
- [ ] No "what" comments — code should say what; comments say why
- [ ] No commented-out code (use version control)
- [ ] TODO/FIXME/HACK annotations include a ticket or owner
- [ ] API-facing methods have clear parameter/return documentation if non-obvious

### Ruby Idioms
- [ ] Use `each_with_object`, `map`, `select`, `reject` over manual accumulation
- [ ] Prefer `&:method` shorthand where readable: `users.map(&:name)`
- [ ] Use `freeze` on constants where mutation would be a bug
- [ ] Prefer string interpolation over concatenation
- [ ] Use `%w[]` and `%i[]` for word/symbol arrays

---

## 3. DRY Analysis

### Within the PR
- [ ] No copy-pasted blocks (even with small variations — extract and parameterize)
- [ ] No duplicated query logic (same `.where` chain in multiple places)
- [ ] No repeated conditional patterns (extract into a method or concern)

### Against the Existing Codebase
- [ ] Search `app/services/` for overlapping service objects
- [ ] Search `app/models/concerns/` for existing shared behavior
- [ ] Search `app/models/` for similar scopes or class methods
- [ ] Search `app/helpers/` for duplicated view logic
- [ ] Grep for similar method names, ActiveRecord query patterns, or business terms

### Consolidation Strategies
- **Concern**: Shared behavior across models → `ActiveSupport::Concern`
- **Service object**: Shared business logic → `app/services/`
- **Scope**: Shared query patterns → model scopes
- **Helper/presenter**: Shared view logic → helpers or presenters
- **Configuration**: Shared constants → dedicated config or constant module

---

## 4. Performance

### Database
- [ ] No N+1 queries: `.includes` / `.preload` / `.eager_load` used for accessed associations
- [ ] Indexes exist for columns in `WHERE`, `ORDER`, `GROUP BY`, and foreign keys
- [ ] No `.all` without `.limit` on tables that could grow large
- [ ] `find_each` / `in_batches` used for iterating large result sets
- [ ] `select` used to limit columns when full records aren't needed
- [ ] `exists?` preferred over `.count > 0` or `.present?` for existence checks
- [ ] `pluck` preferred over `map` when only specific columns needed
- [ ] Counter caches considered for frequently counted associations

### Application
- [ ] Expensive operations not repeated in loops
- [ ] Memoization (`||=`) used for repeated expensive computations within a request
- [ ] External API calls not made synchronously when they could be backgrounded
- [ ] File I/O and network calls have timeouts
- [ ] Large collections paginated with Pagy (`pagy(@records)`) — not Kaminari or will_paginate's `.paginate`

---

## 5. Rails-Specific

### Security
- [ ] Strong parameters: all user input properly permitted via `params.require.permit`
- [ ] No raw SQL interpolation (use parameterized queries or Arel)
- [ ] No `html_safe` on user-provided content
- [ ] Authorization checks present for destructive actions
- [ ] Secrets not hardcoded (use credentials or environment variables)

### Project Custom Cops
- [ ] No `unscoped` usage (banned by `CustomCops::NoUnscoped`)
- [ ] No `module_function` inside a class body (banned by `CustomCops::ModuleFunctionInClass`)

### Conventions (from CODING_CONVENTIONS.md)
- [ ] Spaces, not tabs
- [ ] Format consistent within a file
- [ ] Clarity over cleverness
- [ ] Full English words over abbreviations
- [ ] Small, single-task commits
- [ ] No force push to main repo
- [ ] Commits don't break the test suite (git bisect-friendly)

---

## 6. Project Architecture Patterns

These patterns have surfaced repeatedly in code review and represent team-agreed Rails style. Each violation is a **Should Fix**.

### Multi-Tenancy Query Scoping
- [ ] Every AR query starts from an instance variable, never from the AR class itself
  - Good: `@current_org.rep_activities.active.includes(...)`
  - Bad: `RepActivity.where(organization: @current_org)`
- [ ] Chained scopes on `@records` are preferred over controller private filter methods

### Model vs. Service Placement
- [ ] Filter/scope methods live on the model, not as controller private methods
  - Good: `@activities.for_org_user(id).for_customer_query(q)`
  - Bad: `filter_activities_by_org_user; filter_activities_by_customer_query` in controller
- [ ] Simple record mutations (`soft_delete`, `restore`, `send_reminder`) are model instance methods, not service classes
  - Good: `activities.each(&:send_reminder)`
  - Bad: `RepActivities::SendDueReminders.new(activities:).run`
- [ ] A service class whose entire body would fit as a model method should be a model method instead

### Controller Design
- [ ] `before_action` contains only: authentication, permission enforcement, and resource lookup
- [ ] Business logic (date validation, param coercion, data filtering) lives inside the action or a model scope, not in a before_action callback
- [ ] Method names are fully descriptive; layout resolver methods name the decision being made (e.g., `modern_or_legacy_layout`, not `resolve_layout`)

### Service Object Standards
- [ ] New service objects are Plain Old Ruby Classes, not `ApplicationInteraction` subclasses
- [ ] Service classes are not created solely to wrap a single AR query or a handful of memoized associations (DAO pattern is a smell)
- [ ] When two service classes share logic, the shared logic belongs in the model, not duplicated across both classes
- [ ] No raw SQL strings (`<<~SQL`, `find_by_sql`, `connection.select_all`) when standard AR scopes/`where`/`joins` can express the same query
- [ ] No `Struct.new` whose fields mirror existing AR model columns — use the AR models directly (polymorphically), add instance/class methods to the models, or consider STI
- [ ] No hand-rolled `OFFSET`/`LIMIT` or `SELECT COUNT(*)` pagination — use Pagy with AR `.count`

### Serializers
- [ ] New serializers use a plain `to_h` method — `ActiveModel::Serializer` subclasses are not the project standard

### Pagination
- [ ] Pagination uses Pagy (`pagy(@records)`), not `paginate(page:, per_page:)`

### Model Mutation Methods
- [ ] Model methods that modify a record use `update` (returns boolean) not `update!` (raises)
- [ ] Method names reflect their bang status: a method using `update` is named `soft_delete`, not `soft_delete!`

### Mailers
- [ ] Mailer actions do not assign redundant instance variables for associations already reachable from the primary object
  - Good: `@activity` only; view calls `@activity.org_user`
  - Bad: `@activity`, `@org_user = activity.org_user`, `@customer = activity.customer`

### Controller Design
- [ ] No more than ~3 controller instance variables passed to a view — prefer helper methods, inline view expressions, or presenters
- [ ] Form default values computed inline in the view rather than via controller instance variables (e.g., `params[:date] || 30.days.ago.to_date` in the view)
- [ ] No redundant fallback chains where both controller and view apply `||` defaults for the same value

### Miscellaneous
- [ ] One-liner private methods called from a single site and adding no clarity are inlined or moved to the model
- [ ] Chains of single-line wrapper methods (e.g., `effective_x` → `filter_x || default_x` → literal) collapsed into a single inline expression

---

## 7. Testing

### Coverage
- [ ] New public methods have tests
- [ ] Changed behavior has updated tests
- [ ] Bug fixes include a regression test

### Quality
- [ ] Tests are independent (no reliance on execution order)
- [ ] Tests use `factory_bot` for test data, not fixtures with implicit dependencies
- [ ] No shared mutable state between tests
- [ ] Test names describe the scenario, not the implementation
- [ ] Assertions are specific (`assert_equal expected, actual` not just `assert result`)

### Scope
- [ ] Unit tests for models, services, validators
- [ ] Controller/integration tests for API endpoints and critical flows
- [ ] Edge cases covered (empty input, unauthorized access, validation failures)

---

## 8. Severity Classification

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Must fix** | Bugs, security holes, data loss risk, RuboCop failures, broken tests | SQL injection, N+1 in hot path, nil error on common input, missing authorization |
| **Should fix** | Performance issues, maintainability debt, DRY violations, readability score C or below | Duplicated service logic, missing index, deeply nested conditionals, unclear naming |
| **Nit** | Preferences beyond enforced rules, minor improvements | Slightly better variable name, optional refactor, cosmetic suggestions |

### Tone Guidelines
- Be constructive: explain *why* something is a problem, not just *that* it is
- Acknowledge what's done well — strong tests, clean extractions, good naming
- Don't bikeshed on things RuboCop/linters handle (or that are in the disabled cops list)
- Suggest concrete fixes, not vague criticism
