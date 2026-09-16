# Validation: §8 Platform & Feature Utilization

| Check | Status | Evidence |
|-------|--------|----------|
| Subsection 1: Catalog Health | PASS | `<div class="subsection-title">Catalog Health</div>` found (line 13) |
| Subsection 2: Data Health Report | PASS | `<div class="subsection-title">Data Health Report</div>` found (line 42) |
| Subsection 3: Data Pipeline Health | PASS | `<div class="subsection-title">Data Pipeline Health</div>` found (line 83) |
| Subsection 4: Platform Configuration Alerts | PASS | `<div class="subsection-title">Platform Configuration Alerts</div>` found (line 129); alerts present so subsection required |
| Subsection 5: Feature Usage Intensity | PASS | `<div class="subsection-title">Feature Usage Intensity</div>` found (line 148) |
| Subsection 6: Smart Stack Performance | PASS | `<div class="subsection-title">Smart Stack Performance</div>` found (line 205); gate met (83 smart stacks > 0) |
| section-contents completeness | PASS | Lists all 6 subsections middot-separated: "Catalog Health · Data Health Report · Data Pipeline Health · Platform Configuration Alerts · Feature Usage Intensity · Smart Stack Performance" |
| Fragment contract: id | PASS | Opens with `<details class="section-collapse" id="platform">` — correct per §8=platform |
| Fragment contract: wrapper | PASS | Starts with `<details`, ends with `</details>`, nothing before or after |
| Fragment contract: no forbidden tags | PASS | No `<html>`, `<head>`, `<body>`, `<style>` tags found |
| Fragment contract: no HTML comments | PASS | Zero `<!-- -->` matches |
| Fragment contract: section-sub | PASS | "3,622 products at 99.9% completeness · 10 of 22 entities Fresh, 12 Stale 239+ days · 83 smart stacks · 50 of 74 users active" — data-dense stat line |
| Fragment contract: expand-hint | PASS | `<span class="expand-hint">&#9662; Click to expand</span>` present (line 8) |
| Fragment contract: inner section | PASS | `<section class="section" ...>` wrapper present (line 10) |
| Structure: subsection-title first child | PASS | All 6 subsections have `subsection-title` as first child element |
| Structure: what-this-means closes | PASS | `<div class="what-this-means">` found for all 6 subsections (lines 36, 77, 123, 142, 199, 219) |
| Forbidden: "health score(s)" | PASS | Zero matches |
| Forbidden: "portal orders/ordering" | PASS | Zero matches — entity labeled "All-Channel Orders" throughout |
| Forbidden: "net-new customers" | PASS | Zero matches |
| Forbidden: "ERP" | PASS | Zero matches |
| Forbidden: "Mixpanel" | PASS | Zero matches |
| Forbidden: "Clicky" | PASS | Zero matches |
| Forbidden: segment labels | PASS | Zero matches for "Platform-Embedded", "Commerce-Active", "Catalog-Focused" |
| Forbidden: internal identifiers | PASS | Zero matches for VM codes, query IDs, table names, column names, org IDs, dataset paths |
| Forbidden: "bounce_rate" | PASS | Zero matches |
| Forbidden: code literals | PASS | Zero matches for `order_source = 'ipad'` or similar |
| Forbidden: internal signal labels | PASS | Zero matches for "benchmark_confidence", "peer_group_level", "peer_group_n" |
| Hard Rule 7: time qualifiers | FAIL | 2 metric cards lack time qualifiers — see evidence below |
| Hard Rule 8: projections tagged | PASS | No projections found; no [HYPOTHETICAL] tag required in fragment body |
| Hard Rule 9: extrapolations tagged | PASS | No extrapolations found; no [ESTIMATED] tag required in fragment body |
| Hard Rule 2: VM-27/28/29/36/48 | PASS | Zero matches for any suppressed VM content |
| Hard Rule 2: VM-38b | PASS | Not surfaced (pending_engineering) |
| Hard Rule 4: portal_orders framing | PASS | "All-Channel Orders" used as entity label; never framed as buyer self-service |
| Rendering: freshness 3-label only | PASS | Only Fresh / Monitor / Stale labels used; no 5-label system |
| Rendering: portal_orders entity label | PASS | Labeled "All-Channel Orders" in freshness table (line 55) and pipeline table (lines 110, 116) |
| Rendering: config alerts 4-column table | PASS | Columns: Feature / Status / Issue / Action (line 133) |
| Rendering: config alerts badge vocabulary | PASS | Badges are "Not Established", "Stale", "Drift" only — matches spec |
| Rendering: smart stack gate | PASS | 83 smart stacks > 0; subsection correctly rendered |
| Rendering: no feature gap listings | PASS | No CPQ, Online Ordering, or unlicensed products listed as "gaps" |
| Highlight file: exists | PASS | `cache/section_08_highlights.md` present |
| Highlight file: count | PASS | 4 highlight candidates (within 2–4 range) |
| Highlight file: format | PASS | All 4 have **bold headline**, context sentence, and `[→ §platform]` link |
| Highlight file: priority action | PASS | 1 candidate with HIGH urgency and [HYPOTHETICAL] tag |

## Hard Rule 7 — Failed Metric Cards

### 1. Completeness Score (Catalog Health subsection)
```html
<div class="metric-card">
  <div class="metric-val">99.9%</div>
  <div class="metric-label">Completeness Score</div>
  <div class="metric-note ok">4 missing images &middot; 0 missing prices</div>
</div>
```
**Issue:** `metric-note` provides detail breakdown but no time qualifier. Should include "Current snapshot" or similar.

### 2. Active Users (Feature Usage Intensity subsection)
```html
<div class="metric-card">
  <div class="metric-val">50</div>
  <div class="metric-label">Active Users</div>
  <div class="metric-note ok">67.6% activation rate</div>
</div>
```
**Issue:** `metric-note` provides derived rate but no time qualifier. "Active" is inherently time-bounded — should specify period (e.g., "All-time cumulative" or trailing window).

**VERDICT: FAIL**
