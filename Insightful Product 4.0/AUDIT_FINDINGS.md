# AUDIT FINDINGS — Insightful 4.0 (2026-09-16)

> **What this is.** The evidence base for the remediation program in
> [`EXECUTION_PLAN.md`](EXECUTION_PLAN.md). Every finding carries a file:line or a
> reproducible command. Written so that a session with **no prior context** can
> read this file plus the plan and take over the reviewer seat without
> re-deriving anything.
>
> **Method.** Diffed `outputs/sarreid_PREVIEW_2026-07-02.html` (Jul 13, 3,260
> words) against the current shipped `Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html`
> (2,924 words); read the 4.0 outputs for hfg / cci / da / kal against the 3.0
> run archive in `_museums/Insightful Product 3.0/runs/`; read the pipeline
> source. Cohort baseline captured 2026-09-16 via `./tools/cohort_run.sh`.

---

## 0. The one-line diagnosis

4.0's **doctrine** is excellent and should not be softened. The regression is in
its **constants, its gates, and its enforcement mechanics**: the hardening pass
added blocking checks that fire on the qualities that made reports good, while
the checks that would catch real defects were never written.

**~95 of 3.0's queries still sit in `foundation/query_library_v2.md` marked
BACKLOG.** The gap between 3.0's richness and 4.0's thinness is a *wiring* gap,
not a data gap.

---

## 1. Sarreid regression — five mechanisms

### 1.1 Slot B is discarded, not rewritten  *(→ T1-2)*

`outputs/sarreid_prose_2026-07-02.json` **still contains the good prose**:

> "France and Sons — a $402K account — is down 56% in six months and placed an
> order within the last day, so this is a slip, not a goodbye."

The shipped report says *"Pace has collapsed 56% in six months. Get ahead of it
now, while the relationship is still warm."* — and rows 5, 6, 7 are the identical
sentence with a different number.

**Cause —** `pipeline/run_report.py:293`:

```python
if bundle.outreach_screened or bundle.outreach_reordered:
    prose_vars["talking_points"] = None
    prose_vars["outreach_framing"] = None
```

`outreach_screen.apply()` re-ranks by `outreach_sort_key` and compares to a
legacy LTM-only ordering. Sarreid's list moved The Swan's Nest 4→3 (correctly).
One row moved → the **entire authored array is discarded**.

Reproduce: `./run.sh sarreid --date 2026-07-02` →
`slots: dropped talking_points/outreach_framing (actionability ranking changed row order)`

**The fix already exists twice in the same function**: `align_coaching_narratives()`
re-keys Slot C by rep identity, `reorder_play_framing()` re-keys Slot D by play
type. Slot B is the only one that drops instead of re-keying.

### 1.2 The hero card component is keyed on an exact English string  *(→ T1-3)*

`report_render/sections.py:393`:

```python
def _is_three_things_lead(block: str) -> bool:
    return "three things you wouldn" in low and "have known" in low
```

That literal is the **only** trigger for the three big callout cards. Meanwhile
`pipeline/hero_sanitizer.py:96` rewrites that heading to `**What stands out:**`
whenever the numbered-item count ≠ 3. Presentation is coupled to prose wording
across a module boundary. Both Sarreid and HFG lost the cards.

### 1.3 The sanitizer is a whole-line destructive denylist

`pipeline/hero_sanitizer.py` operates on lines, not claims.
`_strip_ecat_rate_sentences()` deletes any sentence containing "eCat" *and* a
percentage. `_WATCHLIST_CLAUSE` amputates `", and $X across N accounts pulling
back"` mid-sentence. `_PRIORITY_ACTIONS` truncates after a bold heading — but
only if bold and alone on the line, which is why the shipped Sarreid HTML
carries a **stray orphaned `Priority actions, by cadence:` line**.

### 1.4 The voice gates enforce the opposite of the voice doctrine

`knowledge/communication_guideline.md` says: *"Translate jargon to money or
motion on first use: not 'NRR$ is 129%' but 'returning customers spent $1.29 for
every $1 last year.'"* The hardening moved the other way:

| PREVIEW | Shipped | Doctrine |
|---|---|---|
| "Same dealers, more spend" | "Same-dealer spend change" | translate to motion |
| "$ at risk on the watchlist / 12 named accounts fading" | "Revenue at risk / across 12 accounts pulling back" | name + dollar |
| "Book a territory review with Clyde Barnard — 3 at-risk accounts all declining at once" | "Walk the top coaching cards at **named-rep grain**" | FM3: machinery in a finding |
| "7 named calls — France and Sons, AFA Stores…" | "7 calls — FRANCE AND SONS · AFA STORES" | raw DB strings |

**Mechanism:** `pipeline/slot_validator.py` `_RE_CAUSAL` blocks
`because | due to | driven by | caused by | stems from`. The doctrine bans
*invented* causation; the gate bans *causal grammar*. `_RE_MACHINERY` catches the
word `feed`, used constantly in legitimate provenance prose. Combined with the
~90-token §P denylist, **the safest possible prose is prose that restates field
names** — the model is optimized toward the thing we don't want.

### 1.5 What the hardening got RIGHT — do not undo

The PREVIEW's Play 01 was a fabrication: *"anchor-SKU dealers who have never
bought a Jupe are a pre-qualified list."* `Q-CROSS-SELL` gap for Sarreid is **0**
— every Lilac dealer already buys Jupe. The hardened report says so and pivots
to depth. The number-parity gate earns its place. Likewise
`preflight.suppress_ecat_vs_invoiced_rate` (live numerator over frozen
denominator) is correct reasoning.

**The fix is not to loosen the gates.** It is to make them reject *claims*
instead of *vocabulary*, and to make a rejection fall back to something better
than five identical sentences.

---

## 2. Why non-Sarreid clients come out bare — five mechanisms

### 2.1 Every signal threshold is an absolute dollar constant  *(→ Phase 5)*

`pipeline/signals.py:140-155`:

```python
DECLINE_MIN_LTM_DOLLARS   = 50_000   # 0.12% of HFG; 1.7% of a $3M client
REP_ATRISK_MIN_DOLLARS    = 20_000
NEW_LINE_MIN_REVENUE      = 100_000  # 0.24% of HFG — noise
GROWTH_POCKET_MIN_DEALERS = 10
```

Tuned on Sarreid ($15.8M / 1,399 dealers). On HFG ($41.2M / 2,422 dealers) the
watchlist is **10 accounts**, and the month's only play is a **one-dealer**
cross-sell worth $7–12K. This is the literal mathematical overfit.

### 2.2 Rep identity is global and all-or-nothing  *(→ Phase 6)*

HFG bridges **45 of 58** reps (79.3%); promote threshold is 82%; the 78–82%
deadband is Tier 1 unless hand-listed in `config/tier_overrides.json` (one entry
today: `bcf`). So 45 known-good names are suppressed to protect against 13.

**Self-contradiction inside one document:** coaching cards say `rep 12328`
while the leaderboard four sections later prints `BrandJump, LLC`,
`Martha Graham & Assoc`, `Glassman Brands`. 3.0 named *The Hotel Design Group*
and *Tony Minutelli* for this same org.

Source: `operators/rep_copilot_operator.md` §RP-2; applied in
`pipeline/preflight.py:~420`.

### 2.3 The call list ranks by dollars, not by whether anything is wrong  *(→ T1-4)*

`pipeline/gather.py:84` `outreach_sort_key` = `actionability × ltm_rev`, where a
healthy account still scores `0.3`:

- HFG row 1: acct 1489, **+6.7%**, ordered 2 days ago → `0.3 × $602K = 181K`
- HFG row 3: acct 37085, **−81.9%**, real decline → `0.9 × $130K = 117K`

Confirmed on three orgs: HFG rows 1 & 6 and watchlist positions 9 (**+1.8%**)
and 10 (**+83.9%**); kal rows 1 (**+20.0%**) and 6 (**+24.2%**). Sarreid never
exposed it because its biggest accounts happened to be the declining ones.

### 2.4 Section gates test presence, not materiality  *(→ Phase 7)*

`pipeline/availability.py` gates on `bool(any_rows)`:
`products = bool(gather.products or gather.families)`, `team = bool(gather.rep_risks)`.
`fact_bundles.build_plays_from_gather` renders a cross-sell play at
`gap_count = 1`. Hence HFG's four `$1K at risk` coaching cards.
3.0 had a floor: *"Only coaching interventions worth > $50K estimated upside."*

### 2.5 `signal_summary_set()` is dead code  *(→ T1-1, highest-leverage fix)*

`pipeline/signals.py:683` implements the entire 3.0 narrative discipline:
momentum → intelligence → opportunity → risk, max 4 of 7 per section,
**≥3 positive findings**, **finding #1 must be positive**.

```
$ grep -rn "signal_summary_set" pipeline/ report_render/ tests/
pipeline/signals.py:103:  # comment
pipeline/signals.py:683:  def signal_summary_set(...)
```

**Zero callers.** Both hero paths use `sorted(fired, key=lambda s: s.rank,
reverse=True)[:7]` (`run_report.py:254`, `:365`). Since
`rank = surprise × dollar_impact × actionability` and declines carry the largest
dollar impact, **every 4.0 hero is decline-first**: Sarreid risk/risk/risk;
HFG risk/risk/one-door; Dainolite quiet-seats/untouched/stale-config.

3.0 `authority/shared_rules.md` §A0: *"The reader should finish this report
thinking 'I didn't know that about my business — I need to pay for this.' NOT:
'Everything is broken, I should churn.'"*

---

## 3. What 3.0 had that 4.0 lost

3.0 HFG: **11,037 words**. 4.0 HFG: **2,592**. 3.0 CCI: 14,416 → 4.0: 2,671.
3.0 ran **26 signals / 9 categories** over **six sources** (eCat orders,
all-channel ERP, Mixpanel app usage, catalog, inventory, customer master).
4.0 runs **14 detectors over one spine** (ERP invoices).

| 3.0 finding (Hubbardton Forge) | Value | 4.0 status |
|---|---|---|
| 20 high-value accounts with **zero eCat orders** (Illuminating Expressions, Lumens, Build.com) | **$12.8M** | `Q-53` BACKLOG |
| 16 reps running books **entirely off-platform** (BrandJump $5.5M, Grillo $3.3M) | **$33.5M** | `Q-51` BACKLOG |
| Accounts below their **own historical peak** | **$2.79M** | `Q-68` BACKLOG |
| Reorder collapse as a **ratio to that account's own cadence** (Hotel Design Group **30.7×**) | $1.26M | `Q-ORG-DECAY` BACKLOG |
| **30 zero-traction new items** + named warm leads | $1.02M line | `Q-61` BACKLOG |
| **Quote economics** — quotes 2.5× confirmed AOV, $14.7M pipeline | ~$600K | `Q-20/21` BACKLOG |
| **Presentation-to-close spread** (3.4% vs 55.6%) | $595K | `Q-63` BACKLOG |
| **83.9% fill rate**, 10,506 units unshipped | retention | `Q-59` BACKLOG |
| **9 sources 300 days stale** | reliability | `Q-08` **LIVE but no section in standard mode** |

### Three doctrinal losses
1. **Narrative arc** — written, never called (§2.5).
2. **"Patterns That Warrant a Conversation"** — 2–3 *questions*, not statements.
   The highest-trust move in the 3.0 corpus; a dashboard structurally cannot do it.
3. **Thin data handled by disclosure, not suppression.** 3.0's `DATA_MASS_TIER`
   was a **10-factor additive score**; at EARLY/MINIMAL it rendered *every*
   section plus a maturity banner (*"Never apologize, never dismiss"*).
   4.0's `preflight._derive_data_mass_tier` reads **two variables** and thin data
   removes sections. Endpoint: Dainolite — $4.87M eCat, 41 seats, 1,225 orders,
   **1,115 words / 4 sections**. 3.0's Dainolite was 7,382 words.

### The eCat suppression is the deepest cut
`report_render/step10_check.py:165` restricts the token `eCat` to five sections;
`hero_sanitizer._strip_ecat_rate_sentences()` deletes eCat sentences containing a
percentage. **SuperCat's own product — the most differentiated first-party data
source in the company — is banned by regex from every section where a finding
lives.** 3.0 opened HFG with *"eCat already carries $16.8M — nearly 40% of your
$42M total business."*

The suppression *rationale* is sound. The *implementation* is a global vocabulary
ban rather than a conditional rate gate. **Suppress the ratio; never the subject.**

---

## 4. Shipping defects (P0)

Bugs, not design debates. Must close before the golden freeze.

| ID | Defect | Location |
|---|---|---|
| **P0-1** | HFG states **1,075** and **1,080** for "prior-year accounts that went dark" in one report | `Q-ECON-NRR` vs `Q-DEALER-COHORT` |
| **P0-2** | Dainolite hero card reads `LTM invoiced $4.87M` above "There is no invoiced total in this window" | `section_01_hero.md.j2` |
| **P0-3** | Dainolite leaks raw markdown `--- \| --- \|` rows into HTML | `report_render/md_parse.py` |
| **P0-4** | Sarreid ships a duplicated orphaned `Priority actions, by cadence:` | `hero_sanitizer._PRIORITY_ACTIONS` |
| **P0-5** | `SCREAMING CAPS` account names in the priority card | render-time normalization |
| **P0-6** | 5-digit account numbers pass as display names (`1489`, `37085`) | `outreach_screen.looks_like_code` call sites |
| **P0-7** | HFG top-12 is 25% one-off custom SKUs (1 dealer each, $2.5M = 6% of the year) — **and the project is never named** | needs a new signal |
| **P0-8** | SKU descriptions render as raw spec strings | render-time truncation |
| **P0-9** | `kal` **cannot ship** — `SLOT-D-MISMATCH`, exit 1 | `run_report.py` / `check_play_alignment` |
| **P0-10** | `bmc` **cannot ship** — `smoke_check FAIL`, 3× unhedged dollars at `PARTIAL` | deterministic fallback vs §Q |
| **P0-11** | bsc GATESTOP says *"lift platform coverage past **0.0%**"* | `_macros.md.j2` floor copy |
| **P0-12** | `requirements-pipeline.txt` omits `pytest` despite claiming "self-sufficient" | **FIXED in Phase 0** |

### P0-9 / P0-10 detail (found by the Phase 0 cohort sweep)

**kal** — `Slot D: expected 1 play_framing strings, got 2`. Same class as §1.1:
the prose JSON is index-coupled to a re-derived list. Worse than Slot B, which
degrades silently — Slot D **fails the run**. `kal_prose_2026-07-02.json` is
dated Jul 27; play selection changed in Sept.

**bmc** — `commerce_confidence=PARTIAL`, no API key → all slots skipped →
deterministic templates emit unhedged Tier-A dollars → §Q gate fails.
**`README.md` claims "a run still ships with `--no-narrative` / no API key / no
prose file." That claim is false for PARTIAL-confidence orgs.** The deterministic
fallback — the entire safety story of the v9 architecture — is untested at PARTIAL.

### A documented improvement was reverted
`config/golden_set.json` v10 note (5): *"same-dealer metric card label is
adaptive — 'Same-dealer base — contracting' when lift is negative."* The Sept 15
Track 2.5 A3 change replaced it with the static `Same-dealer spend change`.
Visible in the `kal` baseline diff. v10 was right; A3 regressed it.

---

## 5. Repository state

- **Remote:** `git@github.com:kylor-johnson/supercat-4.0.git` — **PRIVATE**,
  personal account, last push 2026-09-16.
- **58 client reports were tracked in git** (named accounts, reps, revenue;
  every file footed *"Confidential — prepared for <client> use only"*).
  Untracked in Phase 0; **still present in history** — resolved by the Phase 11
  clean-repo extraction, not by `.gitignore`.
- **`./regression.sh --verify` was 0/4.** Not broken — *stale*. The pipeline is
  byte-reproducible (verified: fresh venv, pandas 3.0.5, different filesystem →
  identical output). Baseline was last stamped 2026-07-20; Tracks 2.5/3 landed
  2026-09-15/16 and `CHANGELOG.md` records *"No golden freeze — expected-red is
  accepted."* That is how a harness dies.
- **Tests:** 48 passing across 4 files. **Zero coverage** on `sections.py`
  (1,641 lines), `step10_check.py`, `smoke_check.py`, `run_report.py`,
  `cache.py`, `html_renderer.py`, `md_parse.py`, `naming.py`.
- **`run.sh` defaults `--date` to today** and then calls `populate_cache`, which
  needs VPN + Postgres. **Every offline run must pin `--date`.**
- **README is stale**: lists `ali` and `bri` as draft/preview-only; both have
  ratified profiles and SHIP today.

---

## 6. Phase 0 cohort baseline — 2026-09-16

`./tools/cohort_run.sh _baseline` — 11 orgs, **9.7 seconds**, fully offline.

| Result | Orgs |
|---|---|
| **SHIP (8)** | sarreid, cci, da, clc, hfg, ali, sca, bri |
| **REDIRECT (1)** — correct refusal | bsc |
| **FAIL exit 1 (2)** | kal (P0-9), bmc (P0-10) |
| **Excluded** | bcf — no ratified profile, empty cache (0 csv / 0 sql) |

Byte-identical to the previously-tracked artifact: **8 of 11**
(sarreid, cci, da, clc, hfg, ali, sca + bri/bmc had none).
Drifted: `kal`, `bsc` — their tracked copies were stale July artifacts.
