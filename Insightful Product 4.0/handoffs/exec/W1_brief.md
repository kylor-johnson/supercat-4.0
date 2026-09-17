# W1 — P0-7, P0-8, P0-10 (Phase 1 investigation defects)

> **Open a fresh Claude Code session in `~/repos/supercat-4.0` with this prompt:**
>
> `Read "Insightful Product 4.0/handoffs/exec/W1_brief.md" and execute it. Work on branch exec/W1. Do not touch anything outside the scope list.`

**Read first:** `AUDIT_FINDINGS.md` §4, §7, §9 · `EXECUTION_PLAN.md` (stamp protocol).

**W1 needs no VPN, no Postgres and no API key.** Everything runs from the
on-disk cache in ~10s. Confirmed 2026-09-17: `bmc` reproduces its failure
offline, and all 8 catalogs P0-7/P0-8 need are cached.

**Verify with:**
```bash
cd "Insightful Product 4.0"
make check                      # pytest + golden + cohort diff
./tools/cohort_diff.sh --full   # per-org visible-text delta
```
Runs must pin `--date` (`run.sh` defaults to today and then needs Postgres).
`tools/cohort.conf` holds the org→date map.

---

## P0-10 — the deterministic fallback is broken at PARTIAL confidence (do this first)

`bmc` is the **only org in the cohort that still cannot ship**.

```
$ ./run.sh bmc --date 2026-07-09
preflight: mode=Mode 1 - Tier-1 degraded confidence=PARTIAL tier=1
slots: all skipped (no API key)
smoke_check: FAIL
  - SENSITIVITY HEDGE: $2.27M in ## The 60-second read without marker (confidence=PARTIAL)
  - SENSITIVITY HEDGE: $218K in ## Do this month without marker (confidence=PARTIAL)
  - SENSITIVITY HEDGE: $0.33M in ## Do this month without marker (confidence=PARTIAL)
```

No API key → all six prose slots skip → the deterministic templates emit Tier-A
dollar claims with no §Q hedge marker → `smoke_check` fails the run.

**This falsifies a load-bearing claim in `README.md`:** *"a run still ships with
`--no-narrative` / no API key / no prose file."* It does not, at PARTIAL. The
deterministic fallback is the entire safety story of the v9 architecture and it
is untested there.

**Task:** make the deterministic templates satisfy §Q at PARTIAL. The hedge
requirement is real — do not weaken `smoke_check` to make it pass. Add the
marker phrasing to the template paths that emit Tier-A dollars when
`posture.commerce_confidence != "STRONG"`. §Q lives in
`report_product/report_editorial_rules_v4.md`; the canonical marker phrases are
in `_macros.md.j2`.

### The escape hatch is also unreachable (verified 2026-09-17)

`README.md` documents `--no-narrative`, but **`run.sh` does not accept it**:

```
$ ./run.sh sarreid --date 2026-07-02 --no-narrative
Unknown flag: --no-narrative          # run.sh:51
```

It exists only on the Python module. Via that path the split is clean:

```
$ .venv-renderer/bin/python -m pipeline.run_report --org sarreid --date 2026-07-02 --no-narrative
preflight: confidence=STRONG    smoke_check: PASS     # STRONG is fine
$ .venv-renderer/bin/python -m pipeline.run_report --org bmc --date 2026-07-09 --no-narrative
preflight: confidence=PARTIAL   smoke_check: FAIL     # same 3 hedge violations
```

So the deterministic-only path is **unreachable through the documented
entrypoint AND broken at PARTIAL**. Both halves are yours.

**DoD:** `bmc` reaches SHIP with `smoke_check: PASS` and `step10: PASS`; hedges
read as English a CEO would accept, not as a bracket; deterministic-only mode is
verified on **at least one PARTIAL and one STRONG org** (use the module form
above, or add the flag to `run.sh` — your call, but say which and why); no other
org changes outcome; `README.md`'s claim is either made true or amended.

---

## P0-7 — a $2.5M project is 6% of HFG's year and the report never names it

HFG's top-12 items are 25% one-off custom SKUs, 1 dealer each:

```
9N00145405-3-14-DL105 …  $1,079K   20 units   1 dealer
9N00145405-2-14-DL104 …  $  843K   20 units   1 dealer
9N00145405-1-14-DL103 …  $  578K   12 units   1 dealer
```

They crowd the real catalog story out of §8 — and the far more interesting fact,
that **a single ~$2.5M custom project in one door drove 6% of a $41.2M year**,
is never stated.

**Task:** decide whether single-door project concentration is detectable
generically (candidate rule: `dealer_count == 1 AND item_revenue > ~2% of
inv_ltm_net`, clustered by SKU-prefix) or whether it needs a profile field.
**This is design work — propose, do not unilaterally ship a new signal.** Write
the recommendation with a cohort-wide sweep showing what such a rule would fire
on for all 11 orgs (false positives matter more than coverage here).

If the rule is clean, implement it as a signal + a §8 lead sentence, with
thresholds scaled to org size — **not absolute dollars** (see `AUDIT_FINDINGS.md`
§2.1; absolute constants are the Sarreid overfit this whole programme exists to
undo).

**DoD:** a written recommendation with the sweep table; if implemented, HFG's §8
names the project, no other org gains a false positive, thresholds are
size-relative.

---

## P0-8 — SKU descriptions render as raw spec strings

`9N00145405-3-14-DL105 – TYPE DL-105 – 34.5" H x 64.5" D x 92.5" L – OPEN CENTER,
ACRYLIC BOTTOM AND TOP DIFFUSERS` reaches the client verbatim.

Residual ALL-CAPS across the cohort is now confined to these
(`NOTTAWAY LARGE BRONZE CHANDELI`, `FLMNT RND`, `MULTI DROP`) — P0-5 handled
account and rep names and deliberately left product text alone.

**Task:** a truncation/normalisation rule that survives **all 11 catalogs**.
Keep the identifying head, drop the dimensional tail, never invent a name, never
collapse two different SKUs to the same label. `pipeline/gather.normalize_account_name`
is the precedent for case handling but product text is not a company name — do
not reuse it blindly (`FLMNT RND` must not become `Flmnt Rnd` if that is worse).

**DoD:** every org that *has* a catalog is checked, not just HFG; no two SKUs
collide; the before/after table for every affected org is in the evidence file.

**Catalog coverage is 8 orgs, not 11** (verified 2026-09-17): sarreid, cci, clc,
hfg, kal, ali, bmc, bri each carry 25 `Q-PROD-TOP` rows. `da` has no product
CSVs at all; `sca` and `bsc` have the files with zero rows. All three are
behavior-only / gate-stop and legitimately have no catalog — that is full
coverage of what exists, not three gaps.

---

## Scope

**In:** `pipeline/templates/*.j2`, `pipeline/gather.py`, `pipeline/signals.py`,
`pipeline/fact_bundles.py`, `report_render/sections.py`, `tests/**`,
`README.md` (P0-10 only), `handoffs/exec/W1_evidence.md`.

**Out — do not touch:** `config/golden_set.json` (reviewer re-stamps at Phase 2),
LIVE SQL bodies in `foundation/**` / `operators/**`, `pipeline/cache/**`,
`outputs/*_prose_*.json` (authored client inputs), anything outside
`Insightful Product 4.0/`.

**Do not enable `validate_slot` on the prose-file path.** It was tried and backed
out — it rejects `$0.84` and `$1` from "spent $0.84 for every $1". That is
Phase 8. See `AUDIT_FINDINGS.md` §7.

**P0-6 is not yours** — it is blocked on a cache refresh needing VPN + Postgres.

## Evidence file

Write `handoffs/exec/W1_evidence.md`: files changed; every verification command
with **real pasted output**; the per-org cohort delta; one line of justification
per changed golden checksum; and a self-assessment against each DoD line above.
