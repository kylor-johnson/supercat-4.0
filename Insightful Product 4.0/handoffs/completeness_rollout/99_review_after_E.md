# Post-rollout acceptance review + final golden freeze — run AFTER Track E and the `da` rep-floor wrap-up

You are a **fresh, independent reviewer** and the **final acceptance gate** before v4's reports are
trusted for good. The "completeness rollout" (Tracks F→A+D→B→C→E) is finished; `da`'s rep-behavior
floor was built and `da` anointed (Option B — VM-R3/Mixpanel is a deferred fast-follow, not a blocker).

Two phases, in order:
- **Phase 1 — READ-ONLY acceptance review.** Produce a verdict + a severity-ranked findings list.
  **Do not build or fix anything.** If something is wrong, hand it back naming the exact owning track.
- **Phase 2 — GATED re-baseline (only if Phase 1 = SHIP).** The rollout's shared-template edits left
  `hfg/kal/sca/ali` golden checksums collaterally stale (`./regression.sh` shows 4 FAIL **by design** —
  see `next_wave_followups.md` item 3). ONLY after a clean Phase-1 verdict, re-baseline those four with
  full Track-E rigor (regenerate → diff → categorize expected-vs-unexpected → human sign-off) so the
  suite goes GREEN. This is the one sanctioned write; everything else is read-only.

You have no prior context; everything you need is below.

---

## 1. What this rollout was (context in 8 lines)
- v4's report renderer produced **blank** reports for data-light orgs (da) and **alarm-board**
  reports over stale data (bmc), even though the value-moment catalog already defined the
  missing content. The renderer had drifted from the spine/catalog — not the reverse.
- The fix was **additive and catalog-authorized**: render the always-on floor + eCat-cousin
  lane + posture framing, at the confidence ceilings the catalog already assigns. **No new
  modes, no relaxed guardrails.**
- Tracks: **F** (§P vocab) → **A** (wire cached datasets + floor) + **D** (template honesty)
  → **B** (single eCat source, scope labels, F1 pre-check, F7 sentence) → **C** (STALE +
  PROVABLY-INCOMPLETE framing) → **E** (single reviewed golden re-baseline, last).
- A memo governs it; a red-team hardened it with 7 findings. Your job is to confirm all of
  that actually landed and nothing drifted.

## 2. Read first (authority is top-down; on any conflict, the higher doc wins)
1. `foundation/provenance_spine.md` — Tier 0 truth/confidence rules (§1 invoiced-truth, §4
   capture≠attribution, §5 tiers, §6.3 FEED_COMPLETENESS, §6.5 eCat-SALE filter, §7.1 rep tiers).
2. `foundation/value_moment_catalog.md` — Unified Stack Rank; VM ceilings + binding gates.
3. `handoffs/decision_completeness_no_drift_2026-07-09.md` — the decision memo (read the
   changelog banner + §0 guardrails + §3 decision + §4 tracks + §6 sequencing). This is the spec.
4. `handoffs/audit_{cci,da,bmc}_*_2026-07-09.md` — the three audits that motivated the work.
5. `handoffs/completeness_rollout/track_*.md` — what each track was told to do.
6. Baseline commit before the rollout finished: `08f5af0` (mode-collapse + A + D). B/C/E commits
   follow it — `git log --oneline` to see them.

## 3. The rubric — the §0 guardrails MUST NOT have moved
Confirm each still holds in the shipped output (this is the anti-drift test):
- ERP invoiced-net is the only commercial-truth topline (Spine §1).
- Capture (eCat) reported in absolute $; a capture **rate** only at `FEED_COMPLETENESS=CORROBORATED`
  + conf ≥ STRONG (Spine §4). No bare eCat rate on da/bmc/sc.
- Every total carries `FEED_COMPLETENESS` + confidence; suppress rather than guess.
- `FULL` unreachable for economics (single feed → STRONG ceiling).
- Rep→revenue only at identity Tier 2; Tier 1 = number grain; Tier 0 = behavior-only (Spine §7.1).
- Hard gaps (margin/COGS, AR/DSO, claims) suppressed, never estimated (Spine §6.9).
- Segmentation still 🧊 FROZEN; no fit scores, no TAM LLM columns (Spine §8).
- **No new modes, no new template files** — floor + framing are flags on the one spine.

## 4. Per-track acceptance checks
Regenerate each org and read the output (`./run.sh <org> --date <cached-date>`), then verify:

**Track F (vocab):** `report_render/step10_check.py` §P allows `eCat` in hero + floor only;
every other §P ban intact. Grep the shipped HTML for forbidden vocab (e.g. "cohort") — zero hits.

**Track A (floor + wiring):**
- **da is NOT blank** — renders platform readiness (VM-08–11: Fresh/Monitor/Stale counts,
  imports, SmartLists, resources) + eCat capture. Rep-behavior floor renders only if da has
  in-app activity; if absent it is **omitted, not an empty heading**.
- NRR (`Q-ECON-NRR`), leakage (`Q-ECON-LEAK`), channel split (`Q-CHAN-05`), contributors are
  rendered (cci should show its ~88.2% NRR in the hero, not discard it).

**Track D (honesty):**
- No rep shows "First-year book"/"new" solely from a missing prior-year window (should read
  "No prior-year comp available"; YoY column "n/a").
- No "Family performance is steady" over a declining table (bmc families down 35–92% must read
  as a decline, not steady).
- A small family (e.g. cci ~2.4% of invoiced) is NOT framed as "driving the topline"; the
  "share of invoiced LTM" row is disclosed.

**Track B (eCat honesty — highest-risk track):**
- **One** eCat dollar figure everywhere (no cci 11.4% vs 11.5% contradiction).
- Scope labels in headers/labels ("GMV (eCat)" vs "invoiced net"), **not** inline `[eCat ONLY]` tags.
- **F1:** a canonical confirmed-ratio query exists in `query_library_v2.md` (NOT invented in the
  pipeline). Rule: cap + caveat only if `blank_default_share ≥ 5%`. **da must render CLEAN**
  (its blank share is ~0.8% — see §6). Find/confirm the org that legitimately trips the cap.
- **F7:** where eCat is the hero (da/bmc), the explicit sentence appears — *"confirmed order
  volume through SuperCat — not your total business…"* — not just a column label.

**Track C (posture framing):**
- **STALE (bmc):** leads with **live eCat** (stamped "live through today"); invoiced findings are
  past-tense and stamped **"as of `report_through_date`" — ERP dollars ONLY.** ❗The single most
  important check: the **live eCat number is NOT stamped with the stale date** (that reversal is
  the exact bug this track exists to prevent). Recovery block ("refresh the feed") present.
- **PROVABLY-INCOMPLETE (sc):** invoiced + eCat both in absolute $; eCat-vs-invoiced **rate
  suppressed**; no "total/complete business" language.
- **No new template file / no new mode path** was added (grep templates dir).

**Track E (re-baseline) — and the known collateral reds:**
- Sarreid + cci were re-frozen by Track E; `da` was re-frozen by the rep-floor wrap-up. Those
  three must be GREEN on `./regression.sh`.
- `hfg/kal/sca/ali` are **expected-RED going in** — the rollout's shared-template edits changed
  their bytes (collateral, flagged in `golden_set.json` notes + `next_wave_followups.md` item 3).
  Confirm each is collateral (only intended-addition/framing deltas), **not** a smuggled regression.
  **Phase 2 re-baselines them** — do NOT treat their current FAIL as a new incident.
- The re-baseline was reviewed against the 4-point checklist in `track_E_rebaseline_sarreid.md`:
  every pre-existing number byte-identical except the intended additions; no section newly
  suppresses; no confidence/completeness stamp changed; figures match cache. **Independently
  re-diff Sarreid** old→new and confirm every delta is an intended addition (NRR, honest prose,
  scope labels) — hunt for a smuggled regression.

## 5. Drift / regression probes (where this most likely went wrong)
1. **Golden masked a regression** — the biggest risk. Diff Sarreid pre-A (`08f5af0`) vs shipped;
   any changed *existing* number that isn't an intended addition = a regression the re-baseline hid.
2. **F1 too aggressive** — if da (or another clean org) got an F1 cap/caveat, the threshold is wrong.
3. **eCat rate leaked** — any capture *rate* on a non-CORROBORATED org violates Spine §4.
4. **Stale stamp on live eCat** (see Track C ❗).
5. **Empty floor headings** — a "Rep floor" heading with no content violates the omit-not-stub rule.
6. **New mode/template** snuck in — must be flags only.
7. **smoke_check** — note any org still failing (a pre-existing bmc hero SENSITIVITY-HEDGE failure
   was known at `08f5af0`; confirm whether it was fixed or is still out of scope — don't attribute
   it to this rollout without checking).

## 6. Ground-truth anchors (verified live 2026-07-09, read-only Postgres)
- **da** (`shortname='da'`): NONE invoice feed; eCat LTM hero ≈ **$4.87M**; `order_type` is
  **99.2% explicit 'Confirmed'**, only **~0.8%** blank/null (32 orders / $288K) → **da must render
  CLEAN under F1** (no cap). da is the floor gold standard (anointed via the rep-floor wrap-up; its
  rep-behavior floor renders VM-R1/R2/R4 from Q-R1/R2/R4 — VM-R3/Mixpanel is a deferred fast-follow).
  Confirm the floor renders and that any leg without data is **omitted, not an empty heading**.
- **cci**: STRONG, ~$70.7M invoiced, Tier-2, NRR ~88.2%. Mode-1 gold standard.
- **bmc**: STALE (~223 days), ~$6.9M invoiced, ~$635K eCat, Tier-1. STALE-framing gold standard.
- **sc**: PROVABLY-INCOMPLETE — eCat capture ≈ **126%** of invoiced net. Treatment built but
  NOT yet anointed (no sc audit); validate its render before any freeze.
- **Sarreid**: Mode-1 golden. Pre-rollout bytes 58,899 (v1) → 61,504 (mode-collapse v3) →
  ~63,557 after A/D → whatever Track E re-froze. Confirm the final frozen value is intentional.

## 7. Phase 2 — Gated re-baseline of hfg/kal/sca/ali (ONLY after a SHIP verdict)
Do this **only if your Phase-1 verdict is SHIP** (or SHIP-WITH-FIXES where the fixes do not touch
these four orgs). This is the single sanctioned write in this task.

For each of `hfg`, `kal`, `sca`, `ali`:
1. Regenerate on its cached date (`./run.sh <org> --date <cached-date>`).
2. Diff the fresh HTML against the last-good (pre-rollout) render. Categorize every delta as
   **intended** (the rollout's floor / framing / honesty / scope-label additions — the same classes
   you just accepted for Sarreid/cci) or **unexpected**.
3. If ANY unexpected delta appears (a changed pre-existing number that isn't an intended addition, a
   newly-suppressed section, a changed confidence/completeness stamp), **STOP** — that is a regression
   the rollout introduced on a non-golden org; downgrade the verdict and report it instead of freezing.
4. If all deltas are intended, record the new `wc -c` byte count + `sha256sum` (real disk bytes —
   `run.sh`'s console length undercounts; see README note).

Then present the four diffs + new checksums for **human sign-off**. On approval, re-freeze
`config/golden_set.json` for the four orgs and confirm `./regression.sh` exits 0 (sarreid, cci, hfg,
kal, sca, ali all GREEN; `da`/`bmc` per their own freeze status). **Do not re-freeze without the
human sign-off.**

## 8. What to return
1. **Verdict:** SHIP / SHIP-WITH-FIXES / BLOCK.
2. **Findings**, severity-ranked (🔴/🟠/🟡), each naming the owning track + the exact file/section.
3. **Gold-standard go/no-go:** may cci / da / bmc (/ sc) be frozen as regression checksums? For
   each: yes, or what's blocking.
4. **Guardrail attestation:** one line per §3 rubric item — held / violated (with evidence).
5. Explicitly separate **new problems** from **known/expected state** (§6, and the collateral-red
   hfg/kal/sca/ali that Phase 2 closes). Don't re-flag expected things as regressions.
6. **Phase 2 result:** the four re-baseline diffs (intended vs unexpected), new checksums, and the
   final `./regression.sh` status (GREEN, or still-red + why). If Phase 1 wasn't SHIP, say Phase 2 was
   correctly skipped.

**Read-only for Phase 1** (verdict + findings). **Phase 2 is the only sanctioned write** — a reviewed
re-freeze of the four collateral orgs' checksums, and only after a SHIP verdict + human sign-off. Never
modify pipeline code or templates — you are the gate, not a builder. Postgres is
`user-supercat-postgres-vpn` (read-only); label live figures `[from-live]`.
