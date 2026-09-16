# Health V3 Dashboard — Formatting Polish Prompt

Reusable prompt for polishing the HTML dashboard. Run this after every fresh dashboard build to apply the standard visual and readability pass.

**What this is:** A polish-only pass on an existing dashboard. Functional behavior (sort, filter, search, drilldown, queue priority logic, hero math) must be preserved with zero regressions. This is not a redesign — it is a visual hierarchy, typography, and audience-readability pass.

**Prerequisites:**

- `Health V3/dashboards/health_dashboard_{YYYY-MM-DD}.html` exists and opens in a browser without errors.
- `Health V3/runs/{YYYY-MM-DD}/client_health_scores_{YYYY-MM-DD}.csv` available for verification.
- `Health V3/METHODOLOGY.md` for tooltip and methodology-section copy.

**Hard rule:** edit in place. Same file path, same filename. No renames, no new files except `DASHBOARD_POLISH_PROMPT.md` (this file).

---

## The prompt

Everything below is the prompt body. Copy from this line to the end of the file and hand it to the agent.

---

You are polishing an existing HTML dashboard. Read the entire prompt before touching anything.

## Inputs

- **Existing file (edit in place):** `Health V3/dashboards/health_dashboard_{YYYY-MM-DD}.html`
- **Source CSV (read-only reference):** `Health V3/runs/{YYYY-MM-DD}/client_health_scores_{YYYY-MM-DD}.csv`
- **Methodology copy source:** `Health V3/METHODOLOGY.md`

Preserve all functional behavior — sort, filter, search, inline drilldown, queue priority order, hero math. No regressions. If it worked before, it works after.

---

## Section A — Visual hierarchy and typography

### A1. At-risk queue row layout

Currently the queue row header crams ~8 items on one horizontal line. Restructure each row as a **two-line card**:

**Top line:** band-colored composite pill (large) · org name (font-weight 600, ~16px) · ARR (formatted `$8.7K`, `$1.2M`) · cohort year · flag badges — right-aligned.

**Bottom line:** one-sentence narrative excerpt (~140 char, no mid-word truncation, wrap to 2 lines max).

**At-risk queue surfacing logic (deduped, in priority order):**
1. Critical band
2. At Risk band
3. Any org with `behavioral_floor_applied = true` not already listed above

That's it. Watch band is NOT in the queue — it belongs in the filterable full table. A queue of 14+ Watch accounts is not a queue; it's a filtered table. CS uses the Watch band filter chip to review those orgs separately.

**"Why queued" label:** immediately to the right of the composite pill, a small muted label explaining the priority reason. Derive it from the same priority logic used to populate the queue:

```
Critical band            → "Critical band"
At Risk band             → "At Risk band"
behavioral_floor_applied → "Behavioral floor"
```

Show only the **first matching reason** (same deduplication order as the queue).

Drop the "weakest dimension" text from the queue row header — it is redundant with the drilldown dimension cards.

### A2. Main table — desaturate the rainbow

Currently every score cell is colored bright red/amber/green. Tone this down:

- **Composite column:** keep colored text (band color). Bold.
- **Four dimension columns:** use plain `var(--text)` for the number. Color only the cell **background** with a very pale tint (6% opacity of the band color) when the score is below 60. Cells ≥ 60 stay neutral.
- Keep the band column dot + label unchanged.

Goal: the eye should land on the composite first, then on pale-tinted weak dimensions. Not on five competing colored numbers per row.

### A3. Date formatting

Replace every user-visible `YYYY-MM-DD` date string with `Month DD, YYYY` format. The internal `SCORE_DATE` constant stays ISO. Add this helper and use it everywhere a date renders:

```js
const fmtDate = iso => new Date(iso + "T00:00:00Z").toLocaleDateString("en-US", {
  year: "numeric", month: "long", day: "numeric", timeZone: "UTC"
});
```

### A4. Typography

| Element | Before | After |
|---|---|---|
| Body base | 14px | 15px |
| Table body cells | 13px | 14px |
| Narrative text in drilldown dimension cards | 12px | 14px, line-height 1.55 |
| Composite narrative in drilldown | 14px | 16px, line-height 1.6, max-width 720px |
| Queue narrative excerpt | 12px | 14px |
| Filter chips, flag badges | 12px | keep 12px |

### A5. Header

Restructure to two lines, left-aligned:

```
SuperCat Client Health Report         [22px, weight 700]
{fmtDate(SCORE_DATE)} · 104 clients scored · Health V3.2.4    [14px, muted]
```

Drop the inline date pill — the date is in the subtitle. Keep sticky behavior.

### A6. Hero topline sentence

Above the distribution bar, add a computed 2–3 sentence paragraph:

> `{thriving+healthy} of {total} clients ({pct}%) are Thriving or Healthy. {watch+atRisk+critical} require attention: {watch} Watch, {atRisk} At Risk, {critical} Critical. {floorCount} have the behavioral-floor cap applied — these are the priority CS conversations.`

Compute all numbers from `DATA` at render time. Do not hardcode. If `floorCount` is 0, omit the third sentence.

### A7. Footer

```
Health V3.2.8 · Generated from client_health_scores_{date}.csv (SHA-256: {sha}…)
Methodology and scoring spec: Health V3/README.md and Health V3/METHODOLOGY.md
```

Two lines, centered, 13px, 24px top/bottom padding, visible top border in `var(--border)`.

### A8. Band filter chips

Band filter chips: **Watch, At Risk, Critical only.** Do not show Thriving or Healthy chips — no CS rep needs to filter to accounts that are fine. The full table defaults to composite ascending (worst at top) so Thriving accounts naturally float to the bottom.

---

## Section B — Narrative readability

### B1. Jargon-translation layer

**V3.2.4 note:** `composite_narrative` is now written in plain English by the operator — no jargon translation needed. The translation layer is still used for dimension narratives (which contain "CS should" and similar CS-internal phrasing) and for flag notes.

Keep the `translateNarrative()` function as-is:

```js
function translateNarrative(text) {
  if (!text) return "—";
  return text
    .replace(/behavioral floor applied\s*[—–-]?\s*/gi, "Engagement and value delivery are both critically low — ")
    .replace(/behavioral floor applied/gi, "engagement and value delivery are critically low")
    .replace(/capping the composite at (\d+)/gi, "capping the overall score at $1")
    .replace(/the composite(?: score)?/gi, "the overall score")
    .replace(/composite\b/gi, "overall score")
    .replace(/near[- ]ghost/gi, "near-dormant (minimal active usage)")
    .replace(/ghost account/gi, "dormant account")
    .replace(/save play/gi, "account recovery")
    .replace(/CS should/gi, "Recommended action:")
    .replace(/\bCS\b/g, "the CS team")
    .replace(/behavioral signal/gi, "engagement signal")
    .replace(/behavioral floor/gi, "engagement + value delivery floor")
    .replace(/\bbanding\b/gi, "scoring tier")
    .replace(/sub-signal/gi, "component score");
}
```

Apply `translateNarrative()` to:
- The dimension narratives in the drilldown dimension cards.
- The `ghost_account_note` and `support_fire_notes` fields in the flag detail items.

Do **not** apply to `composite_narrative` — it is already exec-readable as of V3.2.4.

### B2. Drilldown layout — primary vs. detail

Currently the composite narrative and the dimension cards are treated as equal siblings. Restructure the drilldown to signal hierarchy:

1. **Executive summary block** (most prominent): the translated composite narrative, 16px, line-height 1.6, max-width 720px, slight left-border accent in the band color.
2. **Dimension cards** below it (supporting detail): four cards as before, 14px narrative text.
3. **Flags and data quality** at the bottom (footnote level): unchanged.

This makes the drilldown read top-to-bottom: "here's the situation → here's what's driving it → here's the metadata."

---

## Section C — Methodology context

### C1. Dimension column header tooltips

Add a hover tooltip to each dimension column header in the main table (and to the dimension card titles in the drilldown). Tooltip content (from `METHODOLOGY.md` §3, abbreviated):

| Column | Tooltip |
|---|---|
| Engagement | Login volume, active-user ratio, and login velocity over the trailing 90 days. Are the client's reps actually showing up? |
| Adoption | Share of configured features being actively used — one point per applicable feature, unweighted. Breadth of platform use. |
| Value Delivery | Share of channels producing observable business outcomes (iPad orders, quotes, portal activity, inventory data flow). |
| Ops Health | Catalog completeness, import-feed success rate, and data freshness relative to each feed's own normal cadence. |

Style: dark background tooltip, 220px wide, appears on hover with a 150ms delay. Same tooltip styling as the existing behavioral-floor tile tooltip.

### C2. "How this works" strip (always visible, between hero and at-risk queue)

Place a **"How this works"** strip as an always-visible section between the hero and the at-risk queue. No toggle, no collapse. Two cards side by side:

- **Left card — "How the score is built":** 2–3 sentences covering composite averaging, equal weights, and the two override rules (Ghost Account, Behavioral Floor).
- **Right card — "Health bands":** the 5-band table (band name with color pill, score range, one-line CS action). Pulled from `METHODOLOGY.md` §4:

| Band | Score | What it means for CS |
|---|---|---|
| Thriving | 80–100 | In good shape. Periodic check-in sufficient. |
| Healthy | 60–79 | Strong with room to grow. Coaching opportunity, not a rescue. |
| Watch | 40–59 | Meaningful gaps. Proactive outreach warranted this month. |
| At Risk | 20–39 | Significant problems. Prioritize for active recovery. |
| Critical | 0–19 | Severe disengagement. Urgent intervention; escalate if high ARR. |

**Remove** the collapsible "How scores are calculated" section from the bottom of the page entirely. Replace the footer with a simple one-line methodology reference (see C3).

### C3. Footer methodology link

Update the footer to include a plain-language link:

```
Health V3.2.8 · Generated from client_health_scores_{date}.csv (SHA-256: {sha}…)
Full methodology: Health V3/METHODOLOGY.md  ·  Health V3/README.md
```

---

## Verification before declaring done

1. **Open in browser.** No console errors.
2. **Hero numbers:** distribution counts (Thriving / Healthy / Watch / At Risk / Critical) and flag counts (behavioral floor, ghost, support fire) must match the latest `CHANGELOG.md` entry's distribution table, or `runs/{date}/run_metadata.md` for the current run. Do not hardcode — verify against the source.
3. **Hero topline sentence renders correctly** — all counts computed from data, not hardcoded.
4. **All 104 rows in table.** Count.
5. **Queue order unchanged.** Same orgs in same priority sequence as pre-polish.
6. **Queue membership correct:** confirm the queue contains only Critical band, At Risk band, and `behavioral_floor_applied = true` orgs (~8 orgs, not 14+). No Watch-only accounts in the queue. **"Why queued" label correct** for at least 3 rows (one Critical, one At Risk, one behavioral floor).
7. **Narrative rendering:** open the drilldown for any account. Confirm `composite_narrative` renders directly (no jargon translation applied — it is already exec-readable). Confirm dimension narratives do go through `translateNarrative()` — "CS should" in a dimension narrative should read "Recommended action:" in the rendered drilldown.
8. **Dimension tooltip test:** hover over "Engagement" in the table header. Confirm tooltip appears with the correct copy.
9. **"How this works" strip:** always visible between the hero and the at-risk queue (no toggle, no collapse). Left card shows "How the score is built." Right card shows the 5-band table with color pills. Confirm NO collapsible methodology section exists at the bottom of the page.
10. **Date format:** every user-visible date reads `Month DD, YYYY` — no ISO strings visible to the user.
11. **Sort + filter + search + drilldown:** still work. No regressions.
12. **File size** under 250 KB.
13. **Zero external network requests** at runtime (DevTools Network tab).

## Hard constraints

- Edit in place. No rename, no new files.
- Do not modify the inlined JSON data block.
- Apply `translateNarrative()` to dimension narratives and flag notes. Do **not** apply to `composite_narrative` — it is already exec-readable as of V3.2.4.
- Do not hardcode any numbers that can be computed from `DATA`.
- Do not add features outside this spec. If something is ambiguous, pick the simpler option and note it in your completion report.
