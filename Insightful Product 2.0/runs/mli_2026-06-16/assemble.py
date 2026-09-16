#!/usr/bin/env python3
"""Assemble the final intelligence report from template + fragments."""
import re
from pathlib import Path

BASE = Path(__file__).parent
FRAG = BASE / "fragments"
OUT  = BASE / "output"
TMPL = BASE.parent.parent / "authority" / "html_report_template.html"

OUT.mkdir(exist_ok=True)

template = TMPL.read_text(encoding="utf-8")

style_start = template.index("<style>")
style_end   = template.index("</style>") + len("</style>")
style_block = template[style_start:style_end]

script_start = template.index("<script>")
script_end   = template.index("</script>") + len("</script>")
script_block = template[script_start:script_end]

fragments = {}
for sec in ["02", "03", "04", "05", "08"]:
    p = FRAG / f"section_{sec}.html"
    if p.exists():
        fragments[sec] = p.read_text(encoding="utf-8")

PARAMS = {
    "CLIENT_NAME": "Maitland-Smith / Theodore Alexander",
    "REPORT_DATE": "June 16, 2026",
    "PERIOD_START": "June 2025",
    "PERIOD_END": "June 2026",
    "PERIOD_LABEL": "Trailing 12 Months",
    "ORG_SHORTNAME": "mli",
    "BUNDLE_LABEL": "5",
    "REPORT_MODE": "standard",
    "REPORT_TYPE_LABEL": "Customer Intelligence Report",
    "REPORT_STAGE_BADGE": "5 &middot; iPad",
}

exec_summary = """\
  <section class="section" id="summary">
    <h2 class="section-title" style="font-size: 24px;">Executive Summary</h2>

    <ul class="highlights">
      <li><strong>eCat is your primary transaction system</strong> &mdash; $10.1M GMV through the platform with a 131% capture rate against total business volume. All 1,961 orders originated through the iPad; there is no eCat Online activity. <a href="#commerce">See Commerce Analytics</a></li>
      <li><strong>Top 3 reps generate 36% of eCat GMV ($3.7M)</strong> &mdash; Darren Clevenger (365 orders, $1.3M), NYSR New York ($1.5M), and NYSR2 New York ($938K) drive more than a third of all platform revenue. Three new reps &mdash; Fernando Ruiz, Anthony Luna, and Jessica Norby &mdash; are accelerating rapidly and adding depth to the team. <a href="#sales">See Sales Team Performance</a></li>
      <li><strong>Dustin Mirwaldt ($873K GMV) has completely disengaged</strong> &mdash; Your 4th-highest rep dropped from 41 logins and 25 orders in the prior 90-day window to zero across both metrics. Chuck Conlon ($295K) and Emil Duval show the same pattern. <a href="#sales">See Sales Team Performance</a></li>
      <li><strong>25 dormant accounts represent $1.5M in historical eCat GMV</strong> &mdash; The top 5 dormant accounts alone (Amy Cassell Atelier, Amy Storm &amp; Company, Calder Design Group, D and D Home Interiors, Devon Grace Interiors) account for $604K. Most lapsed 4&ndash;9 months ago. <a href="#customers">See Customer &amp; Buyer Intelligence</a></li>
      <li><strong>190 visible products have no price &mdash; blocking sales</strong> &mdash; 11.8% of your rep-facing catalog cannot be ordered because pricing has not been set. An additional 323 products are missing images. Visible catalog completeness stands at 68.2%. <a href="#product">See Product &amp; Inventory Intelligence</a></li>
      <li><strong>430 kit items are configured but have zero rep usage</strong> &mdash; No rep has ever viewed or ordered a kit despite extensive configuration. Additionally, 7 data entities (including price levels) have not been updated in 299 days. <a href="#platform">See Platform &amp; Feature Utilization</a></li>
    </ul>

    <h3 class="subsection-title" style="margin-top: 24px;">Priority Actions</h3>
    <div class="priorities">
      <div class="priority">
        <span class="priority-badge high">High</span>
        <div>
          <div class="priority-title"><a href="#sales">Re-engage Dustin Mirwaldt and disengaged reps</a></div>
          <div class="priority-desc">Your 4th-highest rep ($873K LTM GMV) has gone completely dark &mdash; zero logins, zero orders in the last 90 days. Chuck Conlon ($295K) shows the same pattern. Immediate outreach is critical before these relationships are permanently lost.</div>
        </div>
        <div class="priority-impact">$1.2M at risk</div>
      </div>
      <div class="priority">
        <span class="priority-badge high">High</span>
        <div>
          <div class="priority-title"><a href="#product">Add pricing to 190 visible products</a></div>
          <div class="priority-desc">Nearly 12% of your rep-facing catalog has no price and cannot be ordered. Every day these items remain priceless is a missed selling opportunity. This is the fastest path to expanding the orderable catalog.</div>
        </div>
        <div class="priority-impact">Unlocks catalog</div>
      </div>
      <div class="priority">
        <span class="priority-badge medium">Medium</span>
        <div>
          <div class="priority-title"><a href="#customers">Reactivate top dormant accounts</a></div>
          <div class="priority-desc">25 lapsed accounts with $1.5M in historical eCat GMV. The top 5 alone represent $604K. Most lapsed within the past 4&ndash;9 months, placing them within a reactivation window. Territory-focused outreach (IL and NY concentration) may be most efficient.</div>
        </div>
        <div class="priority-impact">$1.5M historical</div>
      </div>
      <div class="priority">
        <span class="priority-badge medium">Medium</span>
        <div>
          <div class="priority-title"><a href="#commerce">Investigate price erosion in top accounts</a></div>
          <div class="priority-desc">Your three most frequent ordering accounts &mdash; Robb &amp; Stucky (-35.9%), CAI Designs (-31.0%), and Loeffler (-25.7%) &mdash; are showing significant average item price declines. Determine whether this reflects intentional product mix shifts or emerging pricing pressure.</div>
        </div>
        <div class="priority-impact">Margin protection</div>
      </div>
    </div>
    <details>
      <summary>Additional action items</summary>
      <div style="padding: 12px 0;">
        <div class="priorities">
          <div class="priority">
            <span class="priority-badge medium">Medium</span>
            <div>
              <div class="priority-title"><a href="#platform">Refresh 7 stale data entities</a></div>
              <div class="priority-desc">Sales quotas, price levels, contract prices, and 4 other entities have not been updated since August 20, 2025 (299 days). Stale price levels could cause quoting errors.</div>
            </div>
            <div class="priority-impact">Data accuracy</div>
          </div>
          <div class="priority">
            <span class="priority-badge low">Low</span>
            <div>
              <div class="priority-title"><a href="#platform">Reintroduce kit items to the sales team</a></div>
              <div class="priority-desc">430 kit items are configured but have never been used. Rep training or in-app promotion could unlock bundling efficiency and improve AOV.</div>
            </div>
            <div class="priority-impact">AOV opportunity</div>
          </div>
        </div>
      </div>
    </details>
  </section>
"""

appendix = """\
  <section class="section section-light" id="appendix">
    <h2 class="section-title"><span class="section-num">&sect;9</span> Appendix</h2>
    <div class="section-sub">Data Sources &amp; Attribution</div>

    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">iPad</span> eCat iPad Orders</div>
      <div class="appendix-value">1,961 orders, $10.1M GMV &middot; Trailing 12 months (June 2025 &ndash; June 2026) &middot; Source: platform transaction records</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Total Business</span> Invoiced Orders</div>
      <div class="appendix-value">1,382 orders, $7.8M GMV &middot; Trailing 12 months &middot; Source: integrated business system records</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Catalog</span> Product Data</div>
      <div class="appendix-value">1,615 visible products, 1,865 hidden &middot; Last updated: June 15, 2026 &middot; Source: platform catalog</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Inventory</span> Inventory Records</div>
      <div class="appendix-value">386 inventory records &middot; Last updated: June 15, 2026 &middot; Source: platform inventory import</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Customers</span> Customer File</div>
      <div class="appendix-value">6,083 accounts on file &middot; Last updated: June 16, 2026 &middot; Source: platform customer import</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Behavioral</span> Platform Usage Analytics</div>
      <div class="appendix-value">91 users, 192,801 events &middot; Trailing 12 months &middot; Source: platform behavioral analytics</div>
    </div>
    <div class="appendix-row">
      <div class="appendix-label"><span class="data-tag">Options</span> Product Options</div>
      <div class="appendix-value">Last updated: May 21, 2026 &middot; Source: platform configuration</div>
    </div>

    <div style="margin-top: 16px; font: 400 11px/1.5 var(--fd); color: var(--text-muted);">
      <p>Note: All commerce figures in this report are derived from platform transaction records and integrated business system data for the trailing 12-month period ending June 16, 2026. eCat capture rates above 100% reflect orders placed through the platform that may differ in timing or classification from total business records.</p>
    </div>
  </section>
"""

html_parts = []

html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{CLIENT_NAME} — {REPORT_TYPE_LABEL}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..800;1,9..40,300..800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
""".format(**PARAMS))

html_parts.append(style_block)

html_parts.append("""
</head>
<body>

<div class="page">

  <header class="header" id="top">
    <div class="h-brand">
      <span>Insightful &middot; Customer Intelligence</span>
    </div>
    <div class="h-customer">{CLIENT_NAME}</div>
    <div class="h-type">{REPORT_TYPE_LABEL}</div>
    <div class="h-meta">{PERIOD_START} &ndash; {PERIOD_END} ({PERIOD_LABEL}) &middot; Report Date: {REPORT_DATE}</div>
    <div class="h-meta" style="margin-top: 4px;">
      <span class="badge badge-info">{REPORT_STAGE_BADGE}</span>
    </div>
    <div class="h-accent"></div>
  </header>

  <nav class="toc-strip" id="tocStrip">
    <a href="#summary">Executive Summary</a>
    <a href="#sales">Sales Team</a>
    <a href="#customers">Customer &amp; Buyer</a>
    <a href="#product">Product &amp; Inventory</a>
    <a href="#commerce">Commerce Analytics</a>
    <a href="#platform">Platform &amp; Utilization</a>
    <a href="#appendix">Appendix</a>
  </nav>

""".format(**PARAMS))

html_parts.append(exec_summary)
html_parts.append("\n\n")

for sec in ["02", "03", "04", "05", "08"]:
    if sec in fragments:
        html_parts.append(fragments[sec])
        html_parts.append("\n\n")

html_parts.append(appendix)

html_parts.append("""
  <footer class="footer">
    <div class="footer-brand">Insightful &middot; Customer Intelligence</div>
    <div class="footer-text">Generated {REPORT_DATE} &middot; {CLIENT_NAME} &middot; Confidential &mdash; prepared for {CLIENT_NAME} use only</div>
  </footer>

</div>
""".format(**PARAMS))

html_parts.append("\n")
html_parts.append(script_block)
html_parts.append("\n\n</body>\n</html>\n")

final_html = "".join(html_parts)

final_html = re.sub(r'<!--[\s\S]*?-->', '', final_html)

final_html = re.sub(r'\n{3,}', '\n\n', final_html)

remaining = final_html.count("{{")
if remaining > 0:
    import sys
    matches = re.findall(r'\{\{[^}]*\}\}', final_html)
    print(f"WARNING: {remaining} unresolved template parameters found: {matches[:10]}")

outpath = OUT / "mli_2026-06-16_intelligence_report.html"
outpath.write_text(final_html, encoding="utf-8")

import os
size = os.path.getsize(outpath)
print(f"Report written to: {outpath}")
print(f"File size: {size:,} bytes ({size/1024:.1f} KB)")
print(f"HTML comment check: {'PASS' if '<!--' not in final_html else 'FAIL'}")
print(f"Template param check: {'PASS' if remaining == 0 else f'FAIL ({remaining} remaining)'}")
