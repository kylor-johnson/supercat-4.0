# W11 — Phase 11: the clean company repo

**This is the goal the whole programme exists to reach.** Everything else is
report quality; this is the part that makes the work shareable.

**Requires:** nothing but the local tree. No VPN, no DB.

## The problem, stated plainly

The work currently lives in `git@github.com:kylor-johnson/supercat-4.0.git` —
a **private personal** repo. Its history contains **58 client intelligence
reports** with named accounts and invoiced dollars for Sarreid, Hubbardton
Forge, Currey & Company, Kalco, Dainolite, Capital Lighting, Bassett Mirror,
Bulbrite, Access Lighting, Shadow Catchers and Butler Specialty. The repo also
contains several unrelated projects (`hang-tag-spike`, `onboarding-models`).

You are NOT doing history surgery on 8,008 files. You are creating a fresh
repo that never contained client data.

## Read first

1. `handoffs/exec/TRAPS.md` — especially #12 (prose files are inputs) and #13
   (branches are repo-wide).
2. `EXECUTION_PLAN.md` Phase 11.
3. `.gitignore` in `Insightful Product 4.0/` — understand what is already
   excluded (`pipeline/cache/*/`, `_baseline/`, `_current/`, `outputs/` except
   prose) and why.

## What ships and what does not

**Ships — product:**
- `pipeline/`, `report_render/`, `report_product/`, `tools/`, `tests/`
- `config/` EXCEPT anything naming a client
- `foundation/`, `operators/`, `knowledge/` — the doctrine and query library
- `Makefile`, `regression.sh`, `run.sh`, `requirements-pipeline.txt`
- `README.md`, `CANON.md`, `CHANGELOG.md`, `EXECUTION_PLAN.md`, `TRAPS.md`

**Does not ship — client data:**
- `outputs/` in its entirety, including the `*_prose_*.json` files. They are
  pipeline INPUTS (TRAPS #12) but they are also authored prose about named
  client accounts. They move to the private sibling repo.
- `pipeline/cache/` — raw invoice extracts
- `profiles/*.md` for real orgs — these carry account codes and dollar figures
- `config/golden_set.json` as it stands — it names client artifact filenames
- `_baseline/`, `_current/`
- `handoffs/exec/W*_evidence.md` — these quote client numbers extensively

**The seam:** the product reads client data through a path resolved from an
env var (e.g. `INSIGHTFUL_DATA_ROOT`), defaulting to a sibling directory. The
private repo holds `cache/`, `outputs/`, `profiles/`. Nothing in the public
tree hardcodes a client shortname — `pipeline/cache.py` currently has
`_KNOWN_ORG_IDS` and `_KNOWN_ORG_NAMES` maps with real org ids and names.
**Those must move to the private side** (`config/org_ids.json` already exists
as the file-based fallback — make it the only path).

## The synthetic fixture

CI needs a golden that contains no client data. Build ONE synthetic org,
`example_co`:

- Invented company, invented dealers, invented reps, plausible but fabricated
  dollars. Do not derive it by scaling a real org — scaled real data is still
  real data.
- It must exercise the interesting paths: STRONG commerce confidence, a real
  decline, a cadence break, a growing family, a coaching card, an activation
  list row, and a house-screened account.
- Its cache CSVs are committed. It is the CI golden and the public demo.
- `make check` must pass against `example_co` alone with no private repo
  present. That is the acceptance test for the whole phase.

## Steps

1. Create the new repo under the company org (name it with the owner — the
   plan says `supercat/insightful`). Do NOT push anything yet.
2. Build the file manifest: for every path in the product list, confirm it
   contains no client shortname, account code, dealer name or dollar figure.
   Grep is your friend and it is not optional:
   ```
   grep -rniE 'sarreid|hubbardton|currey|kalco|dainolite|bassett|bulbrite|butler|shadow ?catcher|capital lighting|wayfair|lumens|lamps plus' <staged tree>
   ```
   Expect hits in `foundation/` and `operators/` — the doctrine cites real
   validation examples ("validated live, cci", "Pushed example (cci, live)").
   **Each hit is a decision:** either generalise the wording or move that
   document to the private repo. Record which you chose and why, per hit.
3. Copy the product files into the new tree. `git init`, one initial commit.
4. Build `example_co` and make `make check` pass on it alone.
5. Add a GitHub Action running `make check` on push and PR.
6. Write the new `README.md`: what the product is, how to run it, where
   client data lives and that it is deliberately absent.
7. Create the private sibling repo and move cache/outputs/profiles/org-ids
   into it. Verify the product still runs against it via the env var.

## The gate — the owner runs this personally

```
git log -p | grep -iE 'sarreid|hubbardton|currey|kalco|dainolite|bassett|bulbrite|butler|capital lighting'
```

Run against the NEW repo's full history. **It must return nothing.** If it
returns anything, the repo is not clean and no amount of subsequent commits
fixes it — start the repo again.

## Definition of done

- New repo exists, history clean, the grep above returns nothing
- `make check` green on `example_co` with no private data present
- GitHub Action passing
- Private sibling repo holds all client data; product runs against it
- `handoffs/exec/W11_evidence.md`: the full grep output at each stage, the
  per-hit decisions from step 2, and the `make check` run on the clean tree

## What will get you a REWORK

- Any client name, account code or real dollar figure in the new history
- A synthetic fixture derived by transforming real data
- `make check` that only passes because the private repo happens to be present
- Deleting client data from the OLD repo (do not touch it — it is the record)
