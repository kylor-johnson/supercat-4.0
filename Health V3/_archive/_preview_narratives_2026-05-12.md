# Composite Narrative Preview — Option B (3-pattern simplified)

**Read side-by-side and decide:** does the proposed style preserve the "elite" feel while reducing complexity, or does it read worse than today?

For each org, **CURRENT** is what's in `runs/2026-05-11/client_health_scores_2026-05-11.csv` right now (7-pattern engine). **PROPOSED** is what the simplified engine would produce — 2–3 sentences leading with score-shape, naming numbers, ending in one action sentence tuned to band severity.

---

## 1. `ih` — Interlude Home — Thriving (97.7), clean all-green

> bundle: iPad+Catalog+Portal · arr: $22,140 · cohort: 2021
> e=90.7 a=100 v=100 o=99.9

**CURRENT:**
> Interlude Home is performing at a high level — engagement, adoption, value delivery, and operational health are all strong, putting the composite firmly in the Thriving band. The score reflects consistent performance across every pillar rather than one outlier carrying the others. No immediate action required — monitor at standard cadence.

**PROPOSED:**
> Interlude Home is performing across the board — every dimension lands at 91 or above and the composite (98) reflects consistent strength rather than one pillar carrying the others. No CS action required; monitor at standard cadence.

---

## 2. `gl` — Golden Lighting — Thriving (81.2), borderline with relative drag

> bundle: Full · arr: $24,310 · cohort: 2023
> e=71.7 a=75 v=83.3 o=94.7

**CURRENT:**
> Golden Lighting is performing at a high level — engagement, adoption, value delivery, and operational health are all strong, putting the composite firmly in the Thriving band. The score reflects consistent performance across every pillar rather than one outlier carrying the others. No immediate action required — monitor at standard cadence.

*Note: identical Pattern 1 narrative as `ih`, despite Golden Lighting being 16 points lower on composite and right at the Thriving boundary. The current engine doesn't differentiate clean-Thriving from borderline-Thriving.*

**PROPOSED:**
> Golden Lighting is in the Thriving band (81), but the composite sits right at the boundary — engagement (72) is the relative drag while operational health (95) and value delivery (83) carry the score. A check-in focused on rep engagement would solidify Thriving status before drift sets in.

---

## 3. `kii` — Kennedy International — Healthy (63.6), mixed profile with ops drag

> bundle: iPad+Catalog+Cart · arr: $16,643 · cohort: 2015
> e=66 a=71.4 v=60 o=56.9

**CURRENT:**
> Kennedy International, Inc. is healthy overall, though the composite reflects a mixed profile — adoption is the strength while operational health is a meaningful drag. The strongest area is adoption (71); the weakest is operational health (57), which is the primary drag on the composite score of 64. Address the ops gaps in the next CS cycle; clean infrastructure is the clearest path toward Thriving.

**PROPOSED:**
> Kennedy International is in Healthy territory (64) with a mixed profile — adoption (71) is the strongest area, operational health (57) is the drag. The infrastructure gap is the most actionable lever; addressing catalog and import health in the next CS cycle is the cleanest path back toward Thriving.

*Roughly equivalent — slightly tighter, same content.*

---

## 4. `ihm` — International Home Miami — Watch (54.7), adoption breadth gap, 2024 cohort

> bundle: iPad-only · arr: $8,404 · cohort: 2024
> e=66.7 a=40 v=33.3 o=78.8

**CURRENT:**
> International Home Miami has reps logging in at a limited rate, but they are not using the full breadth of what the platform offers — this is a feature adoption gap, not an engagement problem. Engagement (67) is the account's strength; adoption (40) is what's holding the composite to Watch. Value delivery (33) also reflects the breadth gap — unused features are not generating outcomes. For a 2024 cohort with minimal business outcomes, proactive outreach is warranted — not just a coaching session. CS should run a targeted feature coaching session; identify the one or two unused capabilities with the clearest ROI for this team's workflow.

**PROPOSED:**
> International Home Miami's reps are logging in (engagement 67), but they are not using the full breadth of what the platform offers — adoption (40) and value delivery (33) reflect a feature-usage gap, not an engagement problem. For a 2024 cohort showing minimal business outcomes, this is proactive-outreach territory rather than just coaching: identify the one or two unused capabilities with the clearest ROI for their workflow.

*Same interpretive depth (cohort-aware urgency), 5 sentences → 2.*

---

## 5. `dals` — DALS Lighting — Watch (43.8), behavioral concern + critical ops collapse

> bundle: iPad-only · arr: $8,700 · cohort: 2023
> e=40 a=75 v=50 o=10

**CURRENT:**
> The platform is generating business outcomes for DALS Lighting, but rep engagement is thin — a small slice of the team is doing most of the work. Value delivery (50) is holding its own; engagement (40) is the structural weakness pulling the composite into Watch territory. Adoption (75) is solid, suggesting the reps who are active know how to use the platform — the challenge is coverage, not capability. The data infrastructure is in critical condition (ops 10) — catalog completeness and import health need immediate ops attention, which is likely constraining rep effectiveness in the field. CS should focus on rep activation: identify which reps have gone dark and whether there are coverage or enablement gaps driving the low participation.

**PROPOSED:**
> DALS Lighting is in Watch (44) on a behavioral-and-infrastructure double — engagement (40) is thin and ops (10) is in critical condition with catalog at 33% and a broken Products feed. The platform is generating some outcomes (value delivery 50), suggesting the few active reps know how to use it, but the infrastructure failure is likely constraining the rest of the team. Escalate ops and rep activation in parallel — the engagement gap won't close until the data infrastructure is fixed.

*Same content, 5 sentences → 3. Sharper because the "behavioral-and-infrastructure double" framing is explicit.*

---

## 6. `mfc` — Morgan Fabrics — Watch (40.0), behavioral floor APPLIED

> bundle: iPad+Catalog · arr: $13,440 · cohort: 2012
> e=50 a=60 v=33.3 o=46.7 · floor=True

**CURRENT:**
> Behavioral floor applied — engagement and value delivery are both below threshold, capping the composite at 40 regardless of catalog and import health. Operational health also has gaps that need addressing alongside the re-engagement work.

*Note: this is the override-path template. It produces the SAME exact text for any org where the floor fires, regardless of how dim-scored they are.*

**PROPOSED:**
> Behavioral floor applied — engagement (50) and value delivery (33) are both below threshold, capping the composite at 40 (top of Watch). Adoption (60) and ops (47) are not enough to compensate when the underlying behavioral signal is this thin. CS should treat this as a near-ghost: re-establish contact, identify whether reps have gone dark on a coverage or product issue, and determine whether a save play is warranted.

---

## 7. `tel` — Tomlinson Companies — Critical (14.6), behavioral floor APPLIED + dimensions at floor

> bundle: iPad+Catalog · arr: $13,440 · cohort: 2015
> e=13.3 a=25 v=0 o=20 · floor=True

**CURRENT:**
> Behavioral floor applied — engagement and value delivery are both below threshold, capping the composite at 40 regardless of catalog and import health. Operational health also has gaps that need addressing alongside the re-engagement work.

*Note: same exact narrative as `mfc` above, despite `tel` being literally the worst account in the portfolio — 13 engagement, 0 value delivery, sub-20 on every dimension. A reader cannot tell from the narrative whether this is a borderline Watch case or a five-alarm Critical fire.*

**PROPOSED:**
> Behavioral floor applied, but the composite (15) is well below the Critical band on its own merits — engagement (13) and value delivery (0) are functionally zero, and adoption (25) and ops (20) aren't far behind. This is an immediate save-play candidate at this ARR level: escalate to CS leadership for a senior re-engagement conversation, or determine that the account is past saving.

---

## Summary of what changes

| Org | Current behavior | Proposed behavior | Improvement? |
|---|---|---|---|
| `ih` | Clean Pattern 1 narrative | Slightly tighter, same content | Equivalent |
| `gl` | Identical to `ih` despite being 16 pts lower | Names the borderline-Thriving condition + relative drag | **Better** |
| `kii` | Sharp interpretive Pattern 7 | Tighter, same content | Equivalent |
| `ihm` | 5-sentence Pattern 3 with cohort escalation | 2 sentences, same depth | Tighter, same elite feel |
| `dals` | 5-sentence Pattern 4 with ops injection | 3 sentences with explicit "behavioral-and-infrastructure double" framing | **Sharper** |
| `mfc` | Generic floor template | Org-specific narrative with score-aware action | **Better** |
| `tel` | Identical template to `mfc` despite Critical band | Distinct narrative reflecting actual score severity | **Significantly better** |

## What the simpler engine looks like in pseudo-code

```python
def _build_composite_narrative(org_name, score, band, e, a, v, o, bundle, arr, cohort_year):
    # OVERRIDE PATHS (ghost, floor) get org-specific prose using the actual scores,
    # not the template-identical strings currently used.

    if ghost_account:
        return f"{org_name} is a ghost account: ARR ${arr:,.0f} with zero logins in 90d. ..."
    if behavioral_floor_applied:
        # branch on band severity (Watch vs At Risk/Critical) for tone
        ...

    # NON-OVERRIDE PATHS — 3 shape categories:
    if all_dims_strong(e, a, v, o):           # all >= 70
        return _clean_band_narrative(...)     # tone varies for boundary-Thriving vs clean-Thriving
    if engagement_or_value_weak(e, v):        # behavioral concern
        return _behavioral_concern_narrative(...)
    if ops_dragging(o, e, v):                 # infrastructure drag
        return _ops_concern_narrative(...)
    return _mixed_profile_narrative(...)      # catch-all w/ strongest+weakest
```

Approximately 80 lines of Python (down from 244). No `action_map` lookup of 25 entries — the action sentence is generated inline from `(band, score_shape)` with maybe 6 conditional clauses, not 25.

---

## Decision

Read the 7 samples. Then:

- **Ship Phase 3** — if they read at least as well as the current narratives, with `mfc`, `tel`, and `gl` reading meaningfully better.
- **Iterate** — if any of them feel like a step down, point to which ones and I'll revise the style before writing code.
- **Keep A** — if you don't like the direction overall, no harm done. The preview file gets archived, the operator stays as it is.

The behavior on the other 97 orgs follows the same patterns shown above.
