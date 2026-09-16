# Completeness rollout — post order & status

**Goal:** get v4 to complete reports (v3-level) with zero northstar drift, per
`../decision_completeness_no_drift_2026-07-09.md`.

**How to use this folder:** each file below is a standalone agent prompt. Open a
**fresh Cursor chat**, paste the file's contents, let it finish, glance at the
result, then move to the next. Do not run two dependent tracks in the same chat
(context bloat = drift — the whole reason this is staged).

---

## Post order

Order revised after the red-team (E moved to last so Track B can't rot an earlier golden freeze): **F → A+D → B → C → E**.

| # | Post this | What it does | Blocks on | Human gate after |
|---|---|---|---|---|
| ✅ done | `00_redteam.md` | Attacked the memo; 7 findings folded in (2026-07-09) | — | done — memo + prompts re-synced |
| ✅ done | **§8 decisions** | 4 originals + 2 red-team forks resolved (memo §8) | — | done |
| ✅ done | `track_F_vocab.md` | §P vocab: allow "eCat" in hero + floor | — | done — landed bundled in `08f5af0` |
| 2a | `track_A_wire_datasets.md` | Wire dropped datasets + build non-blank floor (platform = min; rep/eCat omit-not-stub) | F | glance |
| ✅ done | `track_D_honesty.md` | Kill canned prose that contradicts the data | F (parallel w/ A) | done — see below |
| ✅ done | `track_B_ecat_labeling.md` | Single eCat source + scope labels + F1 cap + F7 "not total business" sentence | A + D done | done — see below |
| 4 | `track_C_stale_framing.md` | STALE (live-eCat-first, ERP-only "as of") + PROVABLY-INCOMPLETE framing | B | glance |
| 5 | `track_E_rebaseline_sarreid.md` | Regenerate Sarreid+cci, **you review diff vs F4 checklist**, re-freeze golden | C done | ✅ you review diff |
| — | **Anoint gold standards** | Freeze cci / da / bmc (sc after an audited render) | E done | ✅ you eyeball reports |

2a and 2b can run at the same time (mostly different files). The Sarreid golden test is **expected-red from Track A through C** — do not disable it; Track E closes it once at the end.

---

## ✅ Red-team applied (2026-07-09) — prompts already re-synced

The red-team pass ran and returned material findings (not "memo is sound"). All seven
were folded into the memo, and the affected track prompts (**A, B, C, E, F**) + this
README were reconciled to match — including the F→A+D→**B→C→E** reorder, the eCat-SALE
F1 pre-check, the ERP-only "as of" stamp (F2), the platform-is-the-only-always-on-leg
correction (F5), and the new PROVABLY-INCOMPLETE treatment (F6). **The prompts below are
in sync with the current memo — post them as-is.** (Optional: a fresh, non-critic agent
can do a final light re-read of the memo before building.)

---

## Status checklist (tick as you go)

- [x] Red-team pass — findings folded in, prompts re-synced
- [x] Gate: decisions resolved (memo §8 — 4 originals + 2 red-team forks)
- [x] 1. Track F — vocab *(landed bundled into the Track A/D commit `08f5af0`: `report_render/step10_check.py` `_ECAT_ALLOWED_SECTIONS` = `{summary, platform-readiness, channels, methodology}` — confirmed live + step10-passing during Track B verification, 2026-07-09)*
- [x] 2a. Track A — wire datasets + floor, **wiring/floor only** *(already landed in the working tree pre-Track-D; NRR/platform-floor/rep-risk wiring confirmed live in `gather.py` + `section_05_layers.md.j2` — not verified against this checklist before now)*
  - [x] Track A's F1 piece (eCat-SALE confirmed-ratio pre-check gating whether eCat may lead) — built in Track B (memo §4 Track B "Do (F1)"): `Q-CHAN-06` in `foundation/query_library_v2.md`, wired into `pipeline/preflight.py` (`RunPosture.ecat_confidence_capped`), verified `da` CLEAN + `bmc`'s real all-time order_type shape (14.92% blank share) trips the cap.
- [x] 2b. Track D — honesty fixes (2026-07-09) — RS-01 "First-year book," bmc "Family performance is steady," cci family-coverage framing
- [x] 3. Track B — eCat labeling (+ F1 cap, F7 sentence) — 2026-07-09. Single eCat source (`RunPosture.ecat_pct_of_invoiced`; killed the `Q-CHAN-10`-sourced divergent calc in `signals.detect_ecat_minority`), scope-labeled column headers (no inline brackets), `ecat_recon_ratio`/`ecat_tag_status` surfaced in §10 STRONG-CANDIDATE, F1 query + cap/caveat, F7 hero sentence. Verified: `da`/`cci`/`bmc`/`sarreid` all pass `step10_check` (4/8/9/11/12) + `smoke_check`.
- [x] 4. Track C — STALE + PROVABLY-INCOMPLETE framing — 2026-07-09. Two framing flags on the single spine (NO new mode/template — still 15 templates, `Mode`/`FeedCompleteness` enums untouched). Added `RunPosture` properties `is_stale`/`is_provably_incomplete`/`erp_asof_stamp`/`ecat_live_stamp`/`stale_age_phrase`/`suppress_ecat_vs_invoiced_rate`/`invoiced_channel_subset_sentence` (`pipeline/preflight.py`). STALE: §1 leads with the live eCat floor + "refresh the feed" recovery block, ERP dollars stamped "as of {report_through_date}", eCat stamped "live through today" (F2 carve-out — eCat NEVER stamped stale), decay sections (§2/§5/§7/§9) past-tensed + carry a historical `stale_historical_banner` (scrubbed of the literal "eCat" so §P holds outside the Track-F allow-list), priority actions replaced with refresh-then-work-live-channel. PROVABLY-INCOMPLETE: invoiced net + eCat both in absolute $, eCat-vs-invoiced RATE suppressed (hero + §10), "total/complete business" replaced with the channel-subset sentence. LLM hero path (`narrative.py`) also made stale/subset-aware. Verified: `bmc` (STALE) full pipeline SHIP — smoke PASS + step10 [4 8 9 11 12] PASS; synthetic PROVABLY-INCOMPLETE fixture rendered + step10 PASS (fixture removed after); `da`/`cci` unchanged except +2 cosmetic blank lines under the §1 heading (expected golden churn — Track E re-baselines).
- [x] 5. Track E — Sarreid+cci re-baselined (diff reviewed vs F4 checklist) — 2026-07-09. Regenerated both on current cache; the diff surfaced 2 real 🔴 defects (not template-honesty items — actual bugs) that were fixed *within* Track E (small, clearly-scoped, approved by owner rather than handed to a fresh agent): (1) `section_05_layers.md.j2`'s "Platform readiness floor" heading always printed even with no Q-08–11 data, leaking a literal `<!-- QUERY-NEEDED -->` string as visible client-facing text — now omit-not-stub, heading included; (2) `section_10_channels.md.j2` displayed `chan_split.ecat_gmv` (Q-CHAN-05) instead of the canonical `posture.ecat_ltm_confirmed_gmv` (Q-ECON-00) in 3 of its 6 eCat-dollar render sites — live-diverged on Sarreid ($2.04M vs $2.05M, the same contradiction class as the original 11.4%-vs-11.5% bug Track B was chartered to kill, just resurfaced in dollar form). `preflight.py`'s false "these two sources are identical" comment corrected. Re-diffed clean against F4 post-fix; owner signed off. Gold-standard byte counts are real disk bytes (`wc -c`/`sha256sum`, stable across 3 independent renders) — `run.sh`'s own console log undercounts (prints `len(str)` not encoded bytes) and should not be trusted for checksum work.
- [x] Gold standards anointed: cci ☑ (2026-07-09, Track E)  da ☑ (2026-07-09, Track A floor — Tier-0/floor gold standard, live Q-R1/R2/R4)  bmc ☐ (not yet attempted)  (sc after audited render)

**Next wave (logged, not dropped):** see `next_wave_followups.md` — (1) ~~class-wide comment-leak fix at the renderer level~~ **✅ DONE 2026-07-09** (`md_render.py` strip + Jinja hygiene — sarreid/cci golden byte-identical, no re-baseline needed), (2) ~~rep-behavior floor (VM-R1–R4) build-or-defer decision~~ **✅ DONE 2026-07-09** (floor built + `da` anointed as Tier-0/floor gold standard — golden_set.json v5), (3) `hfg`/`kal`/`sca`/`ali` collaterally-stale golden checksums — **now folded into the 99 review as Phase 2** (`99_review_after_E.md`): a gated, reviewed re-baseline that fires only after a SHIP verdict. Regression showing `4 FAIL` until then is expected, not an incident.

**Finish line:** ~~`da` rep-floor wrap-up~~ **✅ DONE** → run `99_review_after_E.md` (Phase 1 acceptance + Phase 2 four-org re-baseline → GREEN suite) → **done.** Net-new client E2E is an optional confidence lap, not a blocker.

---

## The one rule every prompt repeats

Do **not** touch the §0 guardrails in the memo (FEED_COMPLETENESS, confidence
ceilings, capture≠attribution, rep-identity tiers, hard-gap suppression,
segmentation freeze). Every change conforms the renderer to the spine + catalog;
none amends them. If a task seems to require relaxing a guardrail, stop and flag.
