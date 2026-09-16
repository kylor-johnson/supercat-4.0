# Decision memo — get v4 to complete reports (v3-level) with zero northstar drift

**Date:** 2026-07-09
**Author:** synthesis of three mode audits (`audit_cci_mode1`, `audit_da_mode2`, `audit_bmc_mode3`) against the v4 foundation.
**Question answered:** how do we make v4 produce *complete* reports (the thing v3 did well) while keeping every "dope v4 addition" — the provenance spine, `query_library_v2`, the value-moment catalog — intact and without adding complexity that causes new drift.

**One-sentence finding:** the blank/alarm-board reports are **not** what the spine or the value-moment catalog prescribe — the *renderer* under-implements the catalog it already ships with. The fix is **additive and catalog-authorized**, not a loosening of any guardrail and not a new mode.

> **Red-team applied (2026-07-09, rev 2).** A critique pass hardened this memo. The four surviving pillars (root cause = cached-then-dropped datasets; no new Mode-3; Track-D honesty; additive/zero-drift) stand. Seven findings were folded in: **(1)** the eCat-SALE filter fails open (`COALESCE→'Confirmed'`), so eCat may not *lead* without a per-org confirmed-ratio pre-check; **(2)** STALE "as-of" stamp applies to ERP dollars only — eCat is a *live* window and must be stamped "live through today," or the inversion self-destructs; **(3)** the Sarreid/cci golden is re-baselined **once, last** (F→A+D→B→C→E) so Track B doesn't rot it — *owner choice: single end-review*; **(4)** Track E carries an explicit reviewer checklist; **(5)** only platform-readiness is truly always-on — rep-behavior + eCat are omit-not-stub; **(6)** a fourth posture, PROVABLY-INCOMPLETE (`sc`), gets a treatment this pass — *owner choice: build now*; **(7)** an eCat hero number carries an explicit "not your total business" sentence, not just a scope label.

---

## 0. Northstar — the guardrails that DO NOT MOVE

Pinned first, on purpose. Every change below is checked against these. If a proposed change requires relaxing one of these, it is out of scope.

| Guardrail | Source | Stays exactly as-is |
|---|---|---|
| ERP invoiced-net is the only commercial-truth topline | `provenance_spine.md` §1 | ✅ |
| Capture (eCat) = fact in absolute $; capture *rate* only at `FEED_COMPLETENESS=CORROBORATED` + conf ≥ STRONG | Spine §4 | ✅ |
| Every total carries `FEED_COMPLETENESS` + confidence; suppress rather than guess | Spine §5, §6.3 | ✅ |
| `FULL` unreachable for economics (single feed → STRONG ceiling) | Spine §6.3, catalog How-to-Read | ✅ |
| Rep→revenue only at identity Tier 2; Tier 1 = number grain; Tier 0 = behavior-only | Spine §7.1 | ✅ |
| Hard gaps (margin/COGS, AR/DSO, claims) suppressed, never estimated | Spine §6.9 | ✅ |
| `invoiced ≠ collected`; date-clamp every window to `report_through_date` | Spine §6.4, §6.7 | ✅ |
| Confidence ceilings + binding gates in the Unified Stack Rank | `value_moment_catalog.md` | ✅ |
| **(red-team F1) eCat may only *lead* a report after a per-org eCat-SALE check.** Spine §6.5 fails open: `COALESCE(...,'Confirmed')` counts blank `order_type` as a sale. Before eCat is the hero (NONE/STALE), verify `confirmed_gmv ÷ all-eCat GMV` and the blank/Confirmed-defaulted `order_type` share; if a material share defaults in, cap the eCat figure's confidence + add "includes orders without an explicit sale status." Never promote an unverified eCat number to hero. | Spine §6.5 | ✅ new |
| **(red-team F2) the `report_through_date` clamp binds ERP/invoiced dollars; the eCat live window is the sanctioned exception** — eCat capture is windowed to `CURRENT_DATE` (Spine §6.5) and stamped "live through today," never the stale invoice clamp. | Spine §6.4 (carve-out) | ✅ new |

**The reconciliation in one line:** the spine's dollar-honesty caution (your original instinct) and v3-level completeness are **not in tension** — the spine itself mandates a behavior-only layer for NONE feeds (§1, §5.1 "offer the behavior-only (Rep) layer instead") and treats eCat capture as reportable fact (§4). Completeness comes from *rendering the always-on floor the catalog already defines*, not from reporting invoice numbers we can't defend.

---

## 1. Evidence — three audits, one root cause

| | cci (Mode 1, STRONG) | da (NONE) | bmc (STALE) | sc (PROVABLY-INCOMPLETE) |
|---|---|---|---|---|
| Posture | $70.7M inv, Tier-2, STRONG | $0 inv, $4.87M eCat, Tier-0, NONE | $6.9M inv (223d stale), $635K eCat, Tier-1, PARTIAL | invoice feed present but eCat capture ≈ **126%** of invoiced net (catalog VM-CHAN-1 gate `sc🔴`) |
| Report verdict | competent QBR, best finding buried | ~90% blank | alarm board on 7-month-old data | *not audited* — invoice-as-topline would over-imply "total business" |
| Shared failure | 4/20 cached datasets never rendered | every invoice section suppressed; eCat floor unbuilt | decay rendered present-tense; eCat "still alive" buried in one cell | fourth posture the memo now treats (Finding 6, build-this-pass) |

**Fourth posture (red-team Finding 6, build now).** `sc` has a live, present invoice feed that is *provably a channel subset* (eCat > 1.05× invoiced net → invoices can't be the whole business, Spine §6.3). It is neither NONE nor STALE, yet it's where "invoiced net is the topline" (Spine §1) is *most* misleading and where the eCat-vs-invoiced **rate must be suppressed** (report both in absolute $). Treated as a framing flag alongside STALE — see Track C.

**The failure is the same in all three modes and is NOT the gating:**
1. **`gather.py` coverage gaps** — datasets are queried, cached, typed, then dropped before rendering (`Q-ECON-NRR`, `Q-ECON-LEAK`, `Q-CHAN-05`, `Q-08–11`, lifters/decliners). cci proves this happens even at the richest posture (88.2% NRR computed and discarded — `audit_cci` §5.2).
2. **The always-on floor is unbuilt** — the catalog's FULL/owned, "never dark" VMs (R1–R4 rep behavior; VM-08–11 platform; VM-37; VM-41 first-time eCat) have **no live template**. Only `_archive/activation.md.j2` ever referenced them (`audit_cci` §5.4).
3. **No stale-feed framing** — a `feed_completeness=STALE` org renders Mode-1 present-tense prose over a clamped-old window (`audit_bmc` §2, §4).

None of these is a gate that's too strict. They are lanes the renderer never built.

---

## 2. Root-cause reframe (this is the anti-drift crux)

The report renderer implements **only the invoiced-outcome lane** (Domains 9–11 economics, in Sarreid-shaped sections). It skips the two other lanes the value-moment catalog already specifies:

- **The always-on owned floor** — Domain 2 (VM-08–11), Domain 12 (VM-R1–R4). Catalog ceiling `FULL (owned)`, gate *"never dark,"* live-proven on `da`.
- **The eCat-cousin lane** — Register A: *"the only option when no invoice feed exists."* Absolute-$ eCat capture (VM-CHAN-1/C14, VM-41).

So "make reports complete" = **build the two missing lanes the catalog already authorizes**, at the confidence ceilings the catalog already assigns. That is definitionally zero-drift: we are conforming the renderer to the spine + catalog, not amending them.

**Corollary — do NOT add a Mode 3 template.** `mode_collapse_phase1.md` already decided "one spine, graceful fallback." That decision was right; only its fallback *content* was never built. Re-introducing a separate Mode-3 template would re-add the complexity mode-collapse removed and create a new drift surface. The stale case is a **framing treatment inside the one spine**, not a fork (see Track C).

---

## 3. The decision

Finish the single spine's fallback content so that **no report is ever blank and no report is ever an alarm board**, using only catalog-defined VMs at their assigned ceilings:

1. **Every report renders a non-blank floor — but only platform readiness is truly always-on** (red-team F5). The always-on *minimum* is platform readiness (VM-08–11, FULL/owned, MCP, ~100% coverage). Rep-behavior (VM-R1–R4) and eCat capture render **when present and are omitted-not-stubbed when absent** — no empty headings (the exact bmc §3 defect we're killing). *Correct mechanism:* the rep floor is gated on **in-app coverage** (Mixpanel / `login_events` / order-authorship) and is ERP-optional per Spine §7.1 — it is **not** gated by the ERP rep-identity Tier (a Tier-0 org like da can still have an in-app rep floor); eCat capture is $0 for invoice-only orgs.
2. **eCat is a first-class figure, labeled by scope** ("GMV (eCat)" / "invoiced net"), not a euphemized sidebar. Fix the multi-eCat-number contradiction by reading one source. **When eCat is the hero (NONE/STALE)** it carries (a) the F1 confirmed-ratio pre-check and (b) an explicit sentence, not just a column label: *"This is confirmed order volume through SuperCat — not your total business, which we can't size without an invoice feed"* (red-team F7; Spine §4 forbids presenting capture as total business).
3. **STALE feeds invert framing** — lead with the **live** eCat signal (stamped **"live through today"**), render invoiced findings as *historical context* stamped **"as of `report_through_date`"** — **the as-of stamp binds ERP/invoiced dollars only; eCat is exempt** (red-team F2). The contrast between the two dates *is* the finding. Replace "Do this week" with "refresh the feed + what the live channel shows."
3b. **PROVABLY-INCOMPLETE feeds** (eCat > 1.05× invoiced, e.g. `sc`) — present invoiced net **and** eCat both in absolute $, **suppress the eCat-vs-invoiced rate**, and never call invoiced net "complete / total business" (red-team F6; Spine §6.3).
4. **Wire the already-cached datasets** into existing sections (NRR into the hero's own placeholder, leakage-by-customer into coaching, platform into a collapsed readiness block).
5. **Re-baseline the Sarreid golden checksum once, LAST** (red-team F3, owner choice = single end-review). The byte-identical guardrail stays red from Track A through C (expected; do not silently disable it), then a single reviewed re-freeze after Track C freezes the golden against final bytes.

---

## 4. Change tracks (each mapped to authority; drift-checked)

Independent, scoped, different risk. One fresh agent per track.

### Track A — Wire cached-but-unused datasets + build the floor (LOW risk, HIGH value)
- **Do (wiring):** add `gather.py` loaders + `GatherBundle` fields for `Q-ECON-NRR`, `Q-ECON-LEAK`, `Q-CHAN-05`, lifters/decliners; render into slots that already exist (NRR → hero "YoY vs prior LTM" placeholder `section_01_hero.md.j2:115`; leakage-by-customer → §6 coaching; contributor detail → §1/§8).
- **Do (floor):** build the non-blank floor — **platform readiness (VM-08–11) is the always-on minimum**; **rep-behavior (VM-R1–R4) and eCat capture render when present, omit-not-stub when absent** (F5, no empty headings). Rep floor gated on in-app coverage, not the ERP rep Tier (§7.1). eCat capture applies the eCat-SALE filter (§6.5) **and** the F1 confirmed-ratio pre-check before it may lead.
- **Authority:** VM-C17 (NRR), VM-K7/C2 (leakage), VM-CHAN-1/C14 (split), VM-08–11 + VM-R1–R4 + VM-41 (floor). All at the ceilings the catalog assigns; gates satisfied by the cached data.
- **Drift check:** none — these VMs and their gates already exist; we render what passed them.
- **Guardrail note:** changes Sarreid bytes → the golden test stays **red from here until Track E** (now last). Do **not** silently disable it; note the break for E.

### Track B — eCat scope-labeling + fix the number contradiction (MEDIUM)
- **Do:** read eCat $ from a single source (kill the 11.4% vs 11.5% split — `audit_cci` §4.1); label figures by scope in column headers/card labels ("GMV (eCat)" vs "invoiced net") per Spine/catalog, **not** inline bracket tags (v3 `shared_rules` bans inline tags — `audit_cci` §4.5); surface `ecat_recon_ratio`/`ecat_tag_status` where relevant.
- **Do (F1):** implement the per-org eCat-SALE confirmed-ratio pre-check (`confirmed_gmv ÷ all-eCat GMV` + blank/Confirmed-defaulted `order_type` share); when a material share defaults in via §6.5's COALESCE, cap the eCat figure's confidence and add "includes orders without an explicit sale status."
- **Do (F7):** where eCat is the hero (NONE/STALE), render the explicit *"confirmed order volume through SuperCat — not your total business"* sentence, not just a scope label.
- **Authority:** Spine §4 (capture in absolute $), §6.5 (eCat-SALE), catalog VM-CHAN-1/C14.
- **Drift check:** none — enforces §4 (adds the F1/F7 honesty guards), never relaxes it.
- **Guardrail note:** Track B changes the eCat/channel section of **every eCat org, including Sarreid and cci** — this is why the golden re-baseline is single-and-last (Track E after C), so B doesn't rot a golden frozen earlier (red-team F3).

### Track C — posture framing treatments: STALE + PROVABLY-INCOMPLETE (MEDIUM-HIGH)
- **Do (STALE):** detect on `feed_completeness == STALE` (LOW: drop the `confidence ≥ PARTIAL` clause — STALE already forces PARTIAL, so it's a no-op). Then (a) stamp **"as of `report_through_date`" on ERP/invoiced dollars only** — eCat is windowed to `CURRENT_DATE` and stamped **"live through today"** (red-team F2; the two-date contrast *is* the finding); (b) past-tense the decay sections; (c) lead with live eCat + a "refresh the feed" recovery block. LOW: make the staleness *wording* proportional (state actual `days_since_last_invoice`), keep the binary gate.
- **Do (PROVABLY-INCOMPLETE, F6, build now):** detect on `feed_completeness == PROVABLY_INCOMPLETE` (eCat > 1.05× invoiced). Present invoiced net **and** eCat both in absolute $, **suppress the eCat-vs-invoiced rate** (VM-CHAN-1 gate), and replace any "total/complete business" language with "invoiced net (a channel subset — eCat capture alone exceeds it)."
- **Both are framing flags on the single spine — NO new template file.**
- **Authority:** Spine §6.3 (STALE + PROVABLY-INCOMPLETE definitions), §6.4 clamp (ERP-only, eCat exempt per §0). v3 Mode-3 spec informs framing but is a treatment, not a mode.
- **Drift check:** none — makes two existing `FEED_COMPLETENESS` states honest; adds no mode path.

### Track D — Template-honesty fixes (LOW)
- **Do:** RS-01 has no YoY column so every rep renders "new" (`audit_cci` §2) — either add a prior-year window to the query or stop printing "First-year book"; "Family performance is steady" prints over a table where every family is down 35–92% (`audit_bmc` §4, line 261) — make canned prose data-aware; add a family-coverage check so an 8.3%-of-revenue family isn't framed as "driving the topline" (`audit_cci` §3.1).
- **Authority:** Spine §8 "action-first, no fabricated framing"; catalog Forbidden Claims.
- **Drift check:** none — removes statements that contradict the data.

### Track E — Re-baseline the Sarreid golden checksum (GATING, one-time, runs LAST)
- **Do:** **after Tracks A, D, B, and C** (red-team F3, owner choice = single end-review), regenerate Sarreid + cci, **human-review the diff**, re-freeze `golden_set.json` with both. Running last means the golden is frozen once against final bytes and Track B can't rot it.
- **Reviewer checklist (F4) — all must hold before re-freeze:**
  1. every pre-existing rendered number is byte-identical **except** the intended additions (NRR → hero placeholder, leakage → §6, platform → collapsed block);
  2. no section that rendered before now suppresses, and none changed its `FEED_COMPLETENESS`/confidence stamp;
  3. the added figures match the cache exactly (e.g. Sarreid NRR vs its `Q-ECON-NRR.csv`);
  4. no §P / forbidden-vocab regression.
- **Drift check:** the *controlled*, checklisted release of the byte-identical guardrail — reviewed, not silent. An UNEXPECTED diff = a regression until proven otherwise; hand it back to A/D/B/C, don't patch here.

### Track F — §P eCat allow-list (SMALL, gates B/C)
- **Do:** `report_render/step10_check.py` bans `\beCat\b` outside `channels`/`methodology` (`audit_cci` §4.2). The floor/eCat-first content needs eCat nameable in §1 and the floor section.
- **Coupling (F7):** allowing eCat in the hero is what *lets* a NONE/STALE report lead with eCat — so it is coupled to the F7 "not your total business" sentence and the F1 confirmed-ratio check (both land in Track B). F only opens the vocab door; B supplies the honesty guard that must accompany a hero eCat number.
- **Drift check:** the catalog already treats eCat capture as reportable; this aligns the vocab gate with the catalog. Keep every *other* §P ban intact.

---

## 5. What explicitly stays frozen (the anti-drift fence)

- **No new modes, no new templates.** One spine; the floor + stale-treatment live inside it.
- **No relaxation of `FEED_COMPLETENESS`, confidence ceilings, capture≠attribution, rep-identity tiers, or hard-gap suppression.** (§0.)
- **Segmentation stays 🧊 FROZEN** (Spine §8); no fit scores, no TAM LLM columns.
- **No new SQL invented in the pipeline** — pipeline renders VMs whose SQL already lives in `query_library_v2.md` (catalog Query-ID discipline). If a floor VM needs a query not yet in the library (e.g. per-account eCat activity for the "still-alive" breakdown, `audit_bmc` §5), it is authored in `query_library_v2.md` first, then rendered.
- **`vm_runtime_index.md` is the section↔VM menu of record** — implementers pick from it, don't ad-hoc new sections.

---

## 6. Sequencing + gold-standard anointing

1. **Order (red-team F3, revised):** **Track F** (unblocks vocab) → **Track A + D** (wiring + floor + honesty, in parallel) → **Track B** (eCat labeling) → **Track C** (STALE + PROVABLY-INCOMPLETE framing) → **Track E** (single reviewed golden re-baseline, LAST). The byte-identical golden test is expected-red from A through C; E closes it once against final bytes.
2. **Gold standards, anointed as OUTPUTS (not inputs), at Track E:**
   - **cci** — Mode-1 gold standard; re-frozen at E (now includes NRR).
   - **da** — the **floor** gold standard, after the floor lane exists. Do not freeze it blank.
   - **bmc** — the **STALE-treatment** gold standard, after Track C.
   - **sc** — the **PROVABLY-INCOMPLETE** treatment is built this pass (F6), but gold-standard anointing waits until an `sc` render is audited (no `sc` audit exists yet — validate before freezing).
3. Each becomes a `golden_set.json` checksum + regression case only once its lane renders substantively.

---

## 7. Execution model (keeps orchestration from sprawling)

- **This memo is the source of truth.** Implementers read it + the relevant audit sections, not the originating chat.
- **One fresh, scoped agent per track** (A–F), each with: this memo, the cited audit sections, the spine/catalog anchors, and a "do not touch §0 guardrails" instruction.
- **Red-team pass — DONE (2026-07-09).** One agent red-teamed this memo; seven findings folded in (see the changelog at the top). The critic stays critic-only; the fixes were made by the memo owner and the track prompts re-synced. An optional final light re-read by a *fresh* agent (not the critic) is fine before building.
- **Do not build in the analysis chat.** (Context-fidelity.)

---

## 8. Decisions

### Resolved — red-team forks (2026-07-09)
- **Golden re-baseline sequencing** → **single review at the very end** (F→A+D→B→C→E). ✅
- **PROVABLY-INCOMPLETE (`sc`)** → **build the treatment this pass** (folded into Track C). ✅

### Original open decisions (recommended defaults assumed unless overridden)
1. **Re-baseline Sarreid?** Track A can't land otherwise. → **yes, human-reviewed (Track E), now last.** — [x]
2. **§P: let "eCat" appear in §1 + the floor section?** Needed for eCat-first framing; keep all other bans. → **yes, scoped to floor + hero, coupled to the F7 sentence.** — [x]
3. **STALE treatment = past-tense rewrite vs. section-gate + recovery block?** → **recovery block + "as of" (ERP-only) + past-tense.** — [x]
4. **Per-account eCat "still-alive" breakdown** (needs a new `query_library_v2` VM) — build now or defer? → **defer to fast-follow; aggregate eCat floor closes most of the gap.** — [x]

---

### Appendix — source artifacts
- Audits: `handoffs/audit_cci_mode1_2026-07-09.md`, `handoffs/audit_da_mode2_2026-07-09.md`, `handoffs/audit_bmc_mode3_2026-07-09.md`
- Northstar: `foundation/provenance_spine.md` (§1,§4,§5,§6.3,§7.1), `foundation/value_moment_catalog.md` (Unified Stack Rank; VM-R1–R4, VM-08–11, VM-37, VM-41, VM-CHAN-1/C14, Register A), `foundation/query_library_v2.md`
- Design history: `handoffs/mode_collapse_phase1.md` (one-spine decision), `vm_runtime_index.md` (section↔VM menu)
