---
name: admin-page-migration
description: Migrate an admin page from legacy Bootstrap/jQuery layout to the modern Tailwind/Stimulus/ViewComponent design system. Use when migrating admin views, creating v2 views, building archetype partials, adding ViewComponents, or when the user references admin-page-taxonomy.yaml or admin-page-migration-steps.md. Does not require running or writing Rails tests, Playwright, or factory/seed setup as part of the workflow.
---

# Admin Page Migration

Repeatable process for migrating SuperCat admin pages from the legacy Bootstrap/jQuery UI to the modern Tailwind/Stimulus/ViewComponent design system with layout-level switching and full legacy opt-out.

## Architecture Context

Read these project files before starting any migration work:

- **Design system tokens:** `docs/design/supercat-design-system-llm-v2.md` — `sc-*` CSS vars, Geist fonts, brand palette
- **Page taxonomy:** `docs/design/admin-page-taxonomy.yaml` — every admin route with its `page_type`, controller, permissions, and feature gates
- **Migration plan:** `docs/design/admin-page-migration-steps.md` — full phased approach and developer guidelines
- **Storybook stories:** `../storybook/stories/pages/{PageType}.stories.js` — **visual-only** spec for each archetype (CSS classes and layout structure)
- **Admin shell helpers:** `../storybook/stories/helpers/adminShell.js` — `wrapInShell`, `headerBar`, `pageHeader`, `btn`, `badge`, `insightCard`
- **Sample data:** `../storybook/stories/helpers/sampleData.js` — test data shapes used by stories

### Critical Principle: Rails Is the Source of Truth

**The existing Rails view is the source of truth for every v2 migration.** The v2 view is a restyled version of the legacy view, not a rebuild from storybook. Storybook provides CSS classes, layout structure, and visual patterns — it does **not** define form fields, labels, field types, action URLs, hidden fields, or business logic.

Build each v2 view by:
1. **Starting from the legacy Rails view** — copy its form helpers, field names, labels, types, and actions
2. **Applying new CSS classes** from the storybook visual spec and `sc-*` design tokens
3. **Restructuring the wrapper HTML** as needed to match the new layout (wrappers, grid, flex containers)
4. **Preserving all Rails form semantics** — `form_tag`, `form_with`, field names, hidden fields, CSRF, validations

## Key Layers

| Layer | Location | Status |
|-------|----------|--------|
| CSS pipeline | **Tailwind v4** — both Rails (`tailwind_overrides.css` → `public/tailwind.css`) and storybook (`storybook/stories/tailwind.css` via `@tailwindcss/vite`) use identical `@theme` tokens. Rails CSS is compiled via `npm run build:css` (must re-run after adding new views). | Done |
| Design tokens | `tailwind_overrides.css` → `public/tailwind.css` with `sc-*` vars | Done |
| Storybook prototypes | `storybook/stories/pages/*.stories.js` | Done — visual reference only |
| Admin shell helpers | `storybook/stories/helpers/adminShell.js` | Done |
| Visual verification | `storybook/visual-verify/` — optional Playwright comparisons (not part of this skill’s required steps) | Done |
| Admin layout | `app/views/layouts/admin_v2.html.erb` | Done |
| Auth layout | `app/views/layouts/sign_v2.html.erb` | Done |
| Legacy admin layout | `app/views/layouts/application.html.erb` | In production |
| Legacy auth layout | `app/views/layouts/sign.html.erb` | In production |
| Shell ViewComponents | `app/components/sc/` | Done |
| `UiSwitchable` concern | `app/controllers/concerns/ui_switchable.rb` | Done |
| Stimulus controllers | `app/javascript/controllers/` | Partial — extend as needed |

### Local Ruby version (RVM)

The app’s `Gemfile` pins **Ruby ~> 3.0**. Before running any Ruby CLI in this repo (`bundle`, `rails`, `rubocop`, `rake`), select the project interpreter so Bundler matches CI and other developers:

```bash
rvm use 3.0.6
```

Use a **login shell** if your tool runner does not load RVM by default (e.g. `bash -lc 'rvm use 3.0.6 && cd /path/to/supercat_server && bundle exec …'`). Agents and scripts should assume `3.0.6` unless the repo documents otherwise.

## Phase 0 Prerequisites

Before migrating any pages, ensure these one-time foundations exist. Check each before proceeding; create if missing.

### 0.1 ViewComponent gem

Verify `view_component` is in the Gemfile. If not:

```ruby
# Gemfile
gem "view_component", "~> 3.0"
```

Run `bundle install`.

### 0.2 Application shell ViewComponents

Check for `app/components/sc/shell_component.rb`. If the `app/components/sc/` directory is missing, create these components by translating `adminShell.js` helpers:

| Component | Translates from |
|-----------|----------------|
| `Sc::ShellComponent` | `wrapInShell()` |
| `Sc::SidebarComponent` | sidebar nav in `wrapInShell()` |
| `Sc::HeaderBarComponent` | `headerBar()` |
| `Sc::PageHeaderComponent` | `pageHeader()` |
| `Sc::FlashComponent` | flash messages |
| `Sc::BadgeComponent` | `badge()` |
| `Sc::ButtonComponent` | `btn()` |
| `Sc::IconComponent` | Heroicon SVG paths |

### 0.3 Modern layout (`admin_v2.html.erb`)

Check for `app/views/layouts/admin_v2.html.erb`. If it doesn't exist, create it using the shell component. See `docs/design/admin-page-migration-steps.md` Phase 0.3 for the template.

### 0.4 `UiSwitchable` concern

Check for `app/controllers/concerns/ui_switchable.rb`. If missing, create it:

```ruby
module UiSwitchable
  extend ActiveSupport::Concern

  included do
    helper_method :modern_ui?
  end

  private

  def modern_ui?
    return false unless @current_org_user
    case @current_org_user.ui_preference
    when 'modern' then true
    when 'legacy' then false
    else @current_org.use_modern_ui?
    end
  end

  def resolve_layout
    modern_ui? ? 'admin_v2' : 'application'
  end
end
```

Requires migrations for `organizations.use_modern_ui` (boolean, default false) and `org_users.ui_preference` (string, default `'org_default'`).

## Code Quality Standards

Every migration should produce **lean** code in `app/`: the v2 path should have *fewer* lines than the legacy view it replaces — ViewComponents and archetype partials absorb the complexity. **Automated tests, factories, and CI checks are not part of this skill** — run them in your normal pipeline or add them outside this workflow if needed.

### Rubocop Constraints (application code)

When you touch Ruby under `app/`, the project Rubocop config (`.rubocop.yml`) enforces these limits:

| Metric | Max | Notes |
|--------|-----|-------|
| `Metrics/MethodLength` | 15 | `CountAsOne: [array, hash, heredoc]` |
| `Metrics/ClassLength` | 150 | Same `CountAsOne` |
| `Metrics/AbcSize` | 20 | Generous for Rails params handling |
| `Metrics/CyclomaticComplexity` | 8 | |
| `Metrics/BlockLength` | 50 | DSL methods excluded |
| `Metrics/ParameterLists` | 6 | `CountKeywordArgs: false` |

Rubocop **excludes `test/`**. This skill does not require adding or maintaining test files.

### Line Reduction Targets

When building ViewComponents and v2 views, aim to *reduce* total line count vs. the legacy view:

- Extract repeated markup into components rather than duplicating
- Use ViewComponent `#initialize` keyword args — avoid long option hashes
- Prefer `content_for` slots and component composition over deep partial nesting
- Use Tailwind utility classes instead of custom CSS (no SCSS in v2 path)
- Controller changes should be 2-5 lines per action (the `if modern_ui?` conditional)

## Per-Page Migration Workflow

This is the repeatable unit. Follow these steps for every page.

### Step 1: Identify the page

Look up the page in `docs/design/admin-page-taxonomy.yaml`. Capture:

- **`id`** — e.g., `products_list`
- **`page_type`** — e.g., `index`
- **`controller`** — e.g., `ProductsController#index`
- **`path`** — e.g., `/:org/products`
- **`permission`** — e.g., `view_products`
- **`feature_gate`** — if any

### Step 2: Read the existing legacy view (primary source)

Read `app/views/{resource}/{action}.html.erb`. This is the **primary source** for the v2 view. Identify and capture:

- All instance variables (`@products`, `@total`, etc.)
- Partials rendered
- `content_for` blocks (`:page_title`, `:search`, `:actions`, `:head`)
- JavaScript dependencies (jQuery plugins, inline `<script>` blocks)
- **Form helpers and field definitions** — `form_tag`, `form_with`, `text_field_tag`, `select_tag`, etc.
- **Field names and labels** — these are the source of truth and must be preserved in the v2 view
- **Hidden fields, action URLs, CSRF** — carry forward exactly
- URL helpers used

### Step 3: Read the storybook visual spec

Open `storybook/stories/pages/{PageType}.stories.js` (e.g., `Index.stories.js` for page_type `index`). Extract **only**:

- CSS class patterns (Tailwind utilities with `sc-*` tokens)
- Layout structure (wrapper elements, grid/flex containers, spacing)
- Visual patterns (card styles, table layouts, button placement)

**Do NOT extract from storybook:**
- Form field names, labels, or types (these come from the Rails view)
- Placeholder text (match what the legacy form uses, or omit)
- Action URLs or form targets (these come from Rails routing)
- Business logic or data shapes (these come from the controller)

#### Verbatim CSS Class Rule

**Copy Tailwind class strings from storybook character-for-character.** Do not interpret, round, or "improve" any value. Specific prohibitions:

1. **Do not bump spacing** — if storybook says `mb-6`, use `mb-6`. Do not substitute `mb-8`.
2. **Do not bump sizing** — if storybook says `max-w-sm`, use `max-w-sm`. Do not substitute `max-w-md`.
3. **Do not bump text sizes** — if storybook says `text-sm`, use `text-sm`. Do not substitute `text-base`.
4. **Do not bump border widths** — if storybook says `border`, use `border` (1px). Do not substitute `border-[1.5px]`.
5. **Do not bump border radii** — if storybook says `rounded-xl`, use `rounded-xl`. Do not substitute `rounded-2xl`.
6. **Do not bump padding** — if storybook says `px-3 py-2.5`, use exactly that. Do not substitute `px-4 py-3`.
7. **Do not change focus ring values** — if storybook says `focus:ring-2 focus:ring-sc-border-lt`, copy it verbatim.

**Why this matters:** Tailwind utility classes are a precise visual specification. Each value (spacing, sizing, color, border) was chosen deliberately in the storybook prototype. Bumping values by even one step (e.g., `py-2.5` → `py-3`) compounds across every element on the page and produces a visibly different result — larger, looser, and heavier than the design intent.

**Workflow:** When building a ViewComponent template or v2 view, open the storybook story file side-by-side and copy each class string directly. If a class must change for a Rails-specific reason (e.g., adding a `data-*` attribute or swapping a raw `<input>` for a Rails form helper), document the deviation with a code comment.

### Step 4: Ensure archetype components exist

Check if the archetype-specific ViewComponents are built. Each `page_type` needs:

| `page_type` | Required components |
|-------------|-------------------|
| `index` | `Sc::DataTableComponent`, `Sc::FilterBarComponent`, `Sc::PaginationComponent` |
| `detail` | `Sc::DetailSectionComponent`, `Sc::AttributeListComponent` |
| `form` | `Sc::FormSectionComponent`, `Sc::FieldGroupComponent` |
| `report` | `Sc::ReportFiltersComponent`, `Sc::ResultsTableComponent` |
| `dashboard` | `Sc::InsightCardComponent`, `Sc::ChartPanelComponent` |
| `settings_form` | `Sc::SettingsSectionComponent`, `Sc::PermissionMatrixComponent` |
| `upload` | `Sc::FileDropzoneComponent`, `Sc::UploadProgressComponent` |
| `export` | `Sc::ExportFormComponent` |
| `media_library` | `Sc::AssetBrowserComponent`, `Sc::AssetPreviewComponent` |
| `workflow` | `Sc::WorkflowQueueComponent`, `Sc::ApprovalCardComponent` |
| `wizard` | `Sc::WizardStepComponent`, `Sc::StepIndicatorComponent` |
| `hub` | `Sc::CardGridComponent`, `Sc::SummaryCardComponent` |
| `utility` | `Sc::ToolFormComponent`, `Sc::ResultPanelComponent` |
| `auth` | `Sc::AuthCardComponent` |
| `profile` | `Sc::ProfileSectionComponent` |

If missing, build them by copying **exact Tailwind class strings** and layout structure from the corresponding storybook story (see the **Verbatim CSS Class Rule** in Step 3). Also check if an archetype partial exists at `app/views/shared/archetypes/_{page_type}.html.erb`.

### Step 5: Create the v2 view

Create `app/views/{resource}/{action}_v2.html.erb`. Start from the **existing Rails view** and restyle it. Use the archetype partial or compose ViewComponents, but preserve all form semantics from the legacy view:

```erb
<% content_for :page_title, "Products" %>
<%= render 'shared/archetypes/index',
    collection: @products,
    columns: [:sku, :name, :trade_name, :status],
    search_path: products_path(@current_org.shortname),
    new_path: new_product_path(@current_org.shortname) %>
```

Rules:
- **Tailwind only** — no custom SCSS, use `sc-*` design tokens
- **No jQuery** — use Stimulus controllers for interactivity
- **No modifications to the legacy view** — keep it working for opt-out customers

### Form Migration Rules

When a page contains a form, these rules are **mandatory**:

1. **Keep every Rails form helper** — `form_tag`, `form_with`, `text_field_tag`, `password_field_tag`, `select_tag`, `hidden_field_tag`, etc. Do not replace them with raw HTML `<input>` or `<form>` tags.
2. **Preserve field names exactly** — if the legacy form uses `:username`, the v2 form uses `:username`. Do not rename fields based on storybook labels.
3. **Preserve labels from the legacy view** — if the legacy label says "Username", the v2 label says "Username". Do not substitute storybook label text (storybook may use placeholder labels like "Email" that don't match the app's actual field semantics).
4. **Preserve submit button text** — if the legacy button says "Login", keep "Login".
5. **Carry forward all hidden fields** — `return_url`, CSRF tokens, etc.
6. **Preserve form action URLs** — the form must POST/PATCH to the same controller action.
7. **Only change CSS classes** — swap Bootstrap classes for Tailwind `sc-*` classes. Change wrapper structure (divs, grids, flex containers) as needed for layout.
8. **Match ALL form features from the legacy view** — if the legacy form has "Forgot password?" and "Email me a login link" and "Reset my password", all must appear in the v2 view (restyled, not removed).

### Step 5b: Rebuild Tailwind CSS

After creating or modifying any v2 view or ViewComponent template, **rebuild the compiled CSS** so Tailwind picks up new utility classes:

```bash
npm run build:css
```

This runs `tailwindcss -i tailwind_overrides.css -o ./public/tailwind.css --minify`. The `@source` directives in `tailwind_overrides.css` tell Tailwind v4 to scan `app/views/**/*.erb`, `app/components/**/*.erb`, and `app/javascript/**/*.js` for class usage.

**Why this is required:** `public/tailwind.css` is a pre-compiled file served statically. Tailwind v4 only emits CSS for classes it finds in scanned source files. If you add a v2 view with new classes (e.g., `py-2.5`, `max-w-sm`, `text-[13px]`) and skip this step, those classes will be missing from the CSS and the page will render incorrectly — elements will stretch full-width, inputs will have wrong metrics, and arbitrary values won't apply.

**During development:** Use `npm run build:css:watch` to auto-rebuild on file changes.

### Step 5c: Wire admin shell navigation (v2 sidebar)

When a page should appear in the org admin left nav, update both:

1. **`app/components/sc/sidebar_component.rb`** — `NAV_SECTIONS` / `TOOLS_SECTIONS`: add a child `id` (match `docs/design/admin-page-taxonomy.yaml`), `label`, and `permission` (same semantics as legacy `app/views/layouts/_navigation.html.erb`).
2. **`app/components/sc/sidebar_navigation.rb`** — add a `when` branch in `nav_href` for that `id` using the correct Rails path helper and `org` shortname.

Mirror permission rules from `_navigation.html.erb` so admins see the same entries in v2 as in legacy. Do not leave `href="#"` placeholders for shipped nav items.

**Org context:** `Sc::SidebarNavigation` resolves `sidebar_org` / `sidebar_org_user` when `params[:org_shortname]` is absent (e.g. global routes like My Account) so the nav matches `UiSwitchable` behavior. Use `sidebar_org` for links and visibility, not only `@current_org`.

### Step 6: Update the controller

Add the UI-conditional render:

```ruby
def index
  @products = # ... existing query unchanged ...
  if modern_ui?
    render :index_v2, layout: 'admin_v2'
  end
end
```

Ensure the controller includes `UiSwitchable` and has `layout :resolve_layout` if it should default to the resolved layout.

**Important:** If the action has error/failure render paths (e.g., failed form submission that re-renders the form), those paths must also check the UI preference and render the v2 view with the v2 layout:

```ruby
def create
  @product = Product.new(product_params)
  if @product.save
    redirect_to product_path(@current_org.shortname, @product)
  elsif modern_ui?
    render :new_v2, layout: 'admin_v2'
  else
    render :new
  end
end
```

For auth pages that use the `sign`/`sign_v2` layout pair instead of `application`/`admin_v2`, use the appropriate layout:

```ruby
# Auth pages: sign_v2 layout, not admin_v2
render :new_v2, layout: 'sign_v2'
```

### Step 7: Migrate interactive behaviors

For any jQuery behavior in the legacy view, create a Stimulus controller in `app/javascript/controllers/`. Wire it up with `data-controller` attributes in the v2 view.

### Step 8: Automated tests and previews (not required by this skill)

**This skill does not require writing or running Rails tests, FactoryBot setup, seeds, or background test jobs.** Those are easy to get wrong (flaky factories, ordering, CI-only data) and are not part of the migration checklist here.

If your team wants coverage, add it in a separate pass or rely on CI — see `test/` and `docs/design/admin-page-migration-steps.md` if the repo documents conventions. **ViewComponent previews** (`test/components/previews/`) are optional developer aids, not a gate for completing a migration in this workflow.

### Step 9: Visual fidelity verification (Playwright, optional)

If you choose to compare Rails vs storybook automatically, run a Playwright comparison against the storybook story to catch computed-style drift. **Skip this step** if you do not want to run Playwright or maintain comparison specs.

#### 9.1 Create the comparison spec

Copy `storybook/visual-verify/TEMPLATE.spec.js` to `storybook/visual-verify/compare-{page}.spec.js`. Customize:

- `PAGE_NAME` — descriptive slug (e.g., `auth`, `products-index`)
- `STORYBOOK_STORY_PATH` — iframe URL path for the story (find it in storybook's URL bar)
- `RAILS_PAGE_PATH` — the route to the v2 page in Rails
- `SELECTORS` — CSS selectors for key elements to compare (card, inputs, buttons, table, etc.)

Choose selectors that target **structural elements** shared between both pages. Both storybook and Rails use the same Tailwind v4 CSS pipeline and `sc-*` design tokens, so computed values should match exactly.

#### 9.2 Run the comparison

Start both servers, then run:

```bash
# Terminal 1: storybook (requires Node >= 20)
cd storybook && npm run storybook

# Terminal 2: Rails
cd supercat_server && rails s

# Terminal 3: run comparison
cd storybook && npx playwright test visual-verify/compare-{page}.spec.js
```

The test will:
1. Open both pages in headless Chrome at the same viewport size
2. Measure computed styles (padding, margin, font-size, border-width, border-radius, colors, max-width, gap) on each selected element
3. Compare values with a 2px tolerance
4. Save side-by-side screenshots to `storybook/visual-verify/screenshots/`
5. Print a diff table and fail if any property diverges

#### 9.3 Fix any differences

If the comparison reports diffs:
1. **Check the class string first** — the most common cause is a class that was paraphrased instead of copied verbatim (see Verbatim CSS Class Rule in Step 3)
2. **Check Rails-specific wrappers** — Rails form helpers may add wrapper elements or attributes that storybook doesn't have; adjust selectors or add CSS overrides as needed
3. **Document intentional deviations** — if a difference is correct (e.g., Rails uses a `<label>` wrapper that storybook doesn't), add a comment in the spec's `ignoreProperties` or adjust the selector

#### 9.4 Screenshot review

Even when metrics pass, visually review the two screenshots in `storybook/visual-verify/screenshots/`. Automated metrics catch sizing and spacing but can miss visual issues like color contrast, font rendering, or element ordering.

### Step 10: Ship checklist (minimal)

Before opening a PR, complete the items below. **This skill intentionally does not require** Rails tests, Rubocop green, Playwright, or seeded data — handle those in CI or a separate pass if your team needs them.

**From the `supercat_server` directory**, with Ruby 3.0.6 active (`rvm use 3.0.6`) where you run Ruby tooling:

#### 10a. CSS rebuild (required)

```bash
rvm use 3.0.6
npm run build:css
```

Ensure `public/tailwind.css` is freshly compiled with all classes from the new v2 views and components. Commit the updated `public/tailwind.css` alongside the view changes. Use a **current Node** (e.g. **Node 20+** via `nvm use 20` or `nvm use 22`) so `npm` runs; Tailwind v4 needs a compatible `@parcel/watcher` binary—if the build fails on `@parcel/watcher-darwin-*`, switch Node version or reinstall deps (`npm install`) for your platform.

#### 10b. Rubocop (optional here; may run in CI)

```bash
rvm use 3.0.6
bundle exec rubocop app/components/ app/controllers/{resource}_controller.rb app/controllers/concerns/ui_switchable.rb
```

Fix offenses on touched `app/` files when practical. Common traps: method too long, ABC size too high, class too long. Prefer fixing code over `rubocop:disable`.

#### 10c. Self-check code review

Before marking complete, review your own changes against this checklist:

**Efficiency checks:**
- [ ] v2 view has equal or fewer lines than the legacy view it replaces
- [ ] No markup duplicated between v2 views — extracted into ViewComponents
- [ ] Controller change is minimal (2-5 lines per action, the `if modern_ui?` block)
- [ ] No business logic duplicated — v2 path uses same instance variables and queries
- [ ] ViewComponent `#initialize` uses keyword arguments, not positional

**Rubocop / structure (when you run Rubocop on `app/`):**
- [ ] No `rubocop:disable` comments added unless truly necessary
- [ ] Methods are <= 15 lines where practical
- [ ] Classes are <= 150 lines where practical
- [ ] No frozen string literal comment needed (disabled in config)

**Form preservation (pages with forms):**
- [ ] All field names match the legacy view exactly (e.g., `:username` not `:email`)
- [ ] All labels match the legacy view (e.g., "Username" not "Email")
- [ ] All hidden fields carried forward (`return_url`, etc.)
- [ ] Form action URL unchanged (same controller action)
- [ ] Submit button text matches legacy view
- [ ] All form features present (links, checkboxes, secondary actions)
- [ ] Error/failure render paths check UI preference and render v2 view

**Visual fidelity checks:**
- [ ] Every Tailwind class in v2 view / ViewComponent matches the storybook story verbatim (no bumped spacing, sizing, borders, or radii)
- [ ] Spot-check at least 3 elements: compare class string in `.stories.js` vs `.html.erb` character-for-character

**Integrity checks:**
- [ ] Legacy view file has zero diff (`git diff app/views/{resource}/{action}.html.erb`)
- [ ] No jQuery or Sprockets dependencies in v2 path
- [ ] No custom SCSS — Tailwind utilities and `sc-*` tokens only

## File Naming Convention

| Type | Path |
|------|------|
| Legacy view | `app/views/{resource}/{action}.html.erb` |
| Modern view | `app/views/{resource}/{action}_v2.html.erb` |
| Archetype partial | `app/views/shared/archetypes/_{page_type}.html.erb` |
| ViewComponent | `app/components/sc/{name}_component.rb` |
| ViewComponent template | `app/components/sc/{name}_component.html.erb` |
| ViewComponent preview (optional) | `test/components/previews/sc/{name}_component_preview.rb` |
| ViewComponent test (optional; not part of this skill) | `test/components/sc/{name}_component_test.rb` |
| Controller test (optional; not part of this skill) | `test/controllers/{resource}_controller_test.rb` |
| Stimulus controller | `app/javascript/controllers/{name}_controller.js` |

## Sprint Order

| Sprint | Archetypes | Rationale |
|--------|-----------|-----------|
| 1 | `hub`, `auth`, `profile` | Simple pages, proves shell works end-to-end |
| 2 | `index`, `detail`, `form` | Core CRUD, unlocks bulk migration |
| 3 | `report`, `dashboard`, `upload`, `export` | Data-heavy but pattern-based |
| 4 | `settings_form`, `workflow`, `wizard`, `media_library` | Highest complexity |
| 5 | `utility` + remaining one-offs | Cleanup |

## PR Checklist

Copy this into migration PR descriptions. **Core migration and CSS items should be satisfied before merge;** tests, Playwright, and strict Rubocop can be tracked in CI or follow-up PRs per team policy.

```markdown
### Migration
- [ ] `_v2.html.erb` view created, renders under `admin_v2` layout (or `sign_v2` for auth pages)
- [ ] Controller updated with `modern_ui?` conditional (2-5 lines per action)
- [ ] Error/failure render paths also check UI preference
- [ ] Legacy view untouched (verified via `git diff` on original file)
- [ ] v2 view line count <= legacy view line count
- [ ] No jQuery or Sprockets dependencies introduced in v2 path
- [ ] `npm run build:css` run and `public/tailwind.css` committed with new classes

### Form Preservation (if page has forms)
- [ ] All field names identical to legacy view
- [ ] All labels identical to legacy view
- [ ] All hidden fields carried forward
- [ ] Form action URL unchanged
- [ ] All form features present (links, checkboxes, secondary actions)

### Visual Fidelity (optional)
- [ ] Playwright or manual spot-check: storybook vs Rails v2 page (if your team uses comparisons)
- [ ] Screenshots reviewed if you ran `storybook/visual-verify/`

### Code Quality
- [ ] New/modified `app/` code is readable and matches project patterns
- [ ] No business logic duplicated between UI paths
- [ ] Rubocop addressed if your team gates on it (optional for this skill’s workflow)
```

## Full Page Inventory

For the complete list of pages, their controllers, archetypes, and sprint assignments, see [page-inventory.md](page-inventory.md).
