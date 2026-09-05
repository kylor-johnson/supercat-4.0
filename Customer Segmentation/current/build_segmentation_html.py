#!/usr/bin/env python3
"""Generate SuperCat_Client_Segmentation_v4.0.html from the stamped current sources.

Reads:
  - SuperCat_Customer_Segmentation_v4.0_MASTER.csv  (rosters + medians)
  - SuperCat_Client_Segmentation_v4.0.md            (definitions, flags, prose)

Writes:
  - SuperCat_Client_Segmentation_v4.0.html

Post Round 3 (2026-07-09): identity-corrected 109-org universe; no Specialty bucket;
Gabriella White (`sc`) / Summer Classics (`scw`) / Summer Classics Contract (`sccon`)
are three separate Premium Trade Brand rows.
"""

from __future__ import annotations

import csv
import re
import statistics
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).parent
CSV_PATH = DIR / "SuperCat_Customer_Segmentation_v4.0_MASTER.csv"
MD_PATH = DIR / "SuperCat_Client_Segmentation_v4.0.md"
OUT = DIR / "SuperCat_Client_Segmentation_v4.0.html"

SEGMENTS = {
    "1. Luxury Specification": {
        "slug": "luxury",
        "short": "Luxury Specification",
        "color": "#B8860B",
        "bg": "#FDF8EC",
        "border": "#E8D5A0",
        "motion": "Designers put it in a project",
    },
    "2. Premium Trade Brand": {
        "slug": "premium",
        "short": "Premium Trade Brand",
        "color": "#6B4FBB",
        "bg": "#F5F0FC",
        "border": "#D4C4F0",
        "motion": "Dealers carry the line on brand reputation",
    },
    "3. Mid-Market Multi-Channel": {
        "slug": "midmarket",
        "short": "Mid-Market Multi-Channel",
        "color": "#1F8A5C",
        "bg": "#EDF7F1",
        "border": "#A8DCC0",
        "motion": "Trade + retail + online distribution",
    },
    "4. Volume Distribution": {
        "slug": "volume",
        "short": "Volume Distribution",
        "color": "#C44D4D",
        "bg": "#FDF0F0",
        "border": "#E8B4B4",
        "motion": "Commodity distribution, high volume",
    },
}

FLAG_ORGS = {"sbl", "fms", "wac", "ufi", "fal"}

KEY_CALLS = [
    ("4-segment model holds", "Specialty dissolved; 109 accounts land in 33 / 38 / 24 / 14."),
    ("Price = correlate, not classifier", "Selling motion segments; price is a continuous dimension within each bucket."),
    ("Identity corrected post-stamp", "sc = Gabriella White; scw = Summer Classics; sccon unchanged — three active billing entities."),
    ("Medians are real medians", "§3 figures from statistics.median() on the MASTER CSV — not hand-picked org values."),
    ("Enrichment ≠ reclassifier", "iPad users, invoice feed, catalog complexity explain scale within a segment."),
    ("Open human flags", "lna vs leg; whether sc/scw Brand-Building still fits given the family's retail footprint."),
]

FRAMEWORK_QUESTIONS = [
    ("What do they sell?", "Product vertical + price point — furniture, lighting, outdoor; $3/unit vs $9,100/unit."),
    ("How do they sell it?", "Specification, brand-building, multi-channel, or volume replenishment — the primary axis."),
    ("Who buys from them?", "Designers, dealers, retail chains, category managers, hospitality — follows selling motion."),
]

GLOSSARY = {
    "Best Price": "Most trustworthy unit-price signal (realized / scrubbed median / catalog avg). Continuous dimension, not a segment boundary.",
    "AOV": "Average order value — order dollars ÷ order count. High AOV ≈ project orders; low ≈ replenishment.",
    "Orders": "Lifetime eCat order count. Proxy for platform usage depth, not market volume.",
    "PCodes": "Distinct customer default price codes. More codes ≈ more complex channel pricing.",
    "Customers": "Customer records loaded in eCat — from dozens (bespoke) to 90k+ (dealer networks).",
    "Territories": "Distinct territory codes on customers. Zero means not configured — not proof of no coverage.",
    "iPad users": "org_users with a recorded last_ipad_login_at (active reps / buyers on device).",
    "Products": "Non-deleted product rows. Blank/zero often means portal-only ERP org.",
    "org": "Postgres shortname — internal identifier for the client billing entity.",
}


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def money(v) -> str:
    try:
        n = float(v)
    except (TypeError, ValueError):
        return "—"
    if n == 0:
        return "—"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"${n:,.0f}"
    return f"${n:,.2f}".rstrip("0").rstrip(".")


def num(v) -> str:
    try:
        n = float(v)
    except (TypeError, ValueError):
        return "—"
    if n == 0:
        return "—"
    if n == int(n):
        return f"{int(n):,}"
    return f"{n:,.2f}".rstrip("0").rstrip(".")


def fnum(v, default=None):
    try:
        if v is None or v == "":
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def median_of(rows, key, nonzero=False):
    vals = []
    for r in rows:
        v = fnum(r.get(key))
        if v is None:
            continue
        if nonzero and v == 0:
            continue
        vals.append(v)
    return statistics.median(vals) if vals else None


def load_csv():
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    by_seg = defaultdict(list)
    for r in rows:
        by_seg[r["v4_segment"]].append(r)
    for seg in by_seg:
        by_seg[seg].sort(key=lambda r: (-(fnum(r.get("best_price"), 0) or 0), r["Company"]))
    return rows, by_seg


def parse_definitions(md: str) -> dict:
    """Pull selling-motion / exemplars / price range from §4."""
    out = {}
    for seg_name, meta in SEGMENTS.items():
        short = meta["short"]
        # Match "### Segment N: Short Name (N orgs)" through next ### or ---
        pat = rf"### Segment \d+: {re.escape(short)} \(\d+ orgs\)\n\n(.*?)(?=\n### Segment |\n---\n)"
        m = re.search(pat, md, re.DOTALL)
        if not m:
            out[seg_name] = {}
            continue
        block = m.group(1)

        def field(label: str) -> str:
            fm = re.search(
                rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\n\*\*|\n\n###|\Z)",
                block,
                re.DOTALL,
            )
            return re.sub(r"\s+", " ", fm.group(1).strip()) if fm else ""

        def bullets(label: str) -> list:
            fm = re.search(
                rf"\*\*{re.escape(label)}:\*\*\n((?:- .+\n)+)",
                block,
            )
            if not fm:
                return []
            return [ln[2:].strip() for ln in fm.group(1).strip().splitlines()]

        out[seg_name] = {
            "motion": field("Selling motion"),
            "signature": bullets("Quantitative signature"),
            "price_range": field("Price range"),
            "exemplars": field("Exemplars"),
        }
    return out


def parse_ambiguous(md: str) -> list:
    m = re.search(
        r"## 5\. Accounts That Remain Ambiguous\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)+)",
        md,
    )
    if not m:
        return []
    rows = []
    for line in m.group(1).strip().splitlines():
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) >= 4:
            rows.append(cols[:4])
    return rows


def build_summary(by_seg: dict) -> list:
    """One row per segment for the median profile table."""
    rows = []
    for seg_name in SEGMENTS:
        rs = by_seg.get(seg_name, [])
        inv = [r for r in rs if (fnum(r.get("total_invoiced_net"), 0) or 0) != 0]
        rows.append(
            {
                "name": seg_name,
                "n": len(rs),
                "best_price": median_of(rs, "best_price", nonzero=True),
                "orders": median_of(rs, "order_count"),
                "aov": median_of(rs, "avg_order_value"),
                "pcodes": median_of(rs, "price_code_count"),
                "customers": median_of(rs, "customer_count"),
                "ipad": median_of(rs, "ipad_active_users"),
                "products": median_of(rs, "product_count", nonzero=True),
                "invoice_pct": round(len(inv) / len(rs) * 100) if rs else 0,
            }
        )
    return rows


def roster_row(r: dict) -> list:
    return [
        r["Company"],
        r["org"],
        money(r.get("best_price")) if fnum(r.get("best_price"), 0) else "—",
        num(r.get("order_count")),
        money(r.get("avg_order_value")) if fnum(r.get("avg_order_value"), 0) else "—",
        num(r.get("price_code_count")),
        num(r.get("customer_count")),
        num(r.get("territory_count")),
        num(r.get("ipad_active_users")),
        num(r.get("product_count")),
        r.get("what_they_sell") or "—",
        r.get("who_they_sell_to") or "—",
    ]


ROSTER_HEADERS = [
    "Company",
    "org",
    "Best Price",
    "Orders",
    "AOV",
    "PCodes",
    "Customers",
    "Territories",
    "iPad users",
    "Products",
    "What",
    "Who",
]


def render_table(headers: list, rows: list, org_col: int = 1) -> str:
    ths = []
    for i, h in enumerate(headers):
        tip = ""
        for key, gloss in GLOSSARY.items():
            if key.lower() in h.lower() or h == key:
                tip = f' title="{esc(gloss)}"'
                break
        cls = "num" if i > 1 and h not in ("What", "Who", "Issue", "Current Placement", "Data Says", "Account") else ""
        ths.append(f'<th class="{cls}"{tip}>{esc(h)}</th>')

    trs = []
    for row in rows:
        org = row[org_col] if len(row) > org_col else ""
        # org may be embedded in "Schonbek Lighting (sbl)" for ambiguous table
        org_key = org
        if "(" in str(org) and ")" in str(org):
            org_key = str(org).rsplit("(", 1)[-1].rstrip(")")
        flagged = org_key in FLAG_ORGS or (len(row) > 1 and row[1] in FLAG_ORGS)
        cls = ' class="flagged"' if flagged else ""
        tds = []
        for i, cell in enumerate(row):
            v = str(cell).strip()
            if v in ("", "—", "--", "??", "None"):
                tds.append('<td><span class="missing">—</span></td>')
            elif i == org_col and headers[org_col].lower() == "org":
                tds.append(f'<td><code class="org-tag">{esc(v)}</code></td>')
            elif i > 0 and (v.startswith("$") or re.match(r"^[\d,]+$", v.replace(",", ""))):
                tds.append(f'<td><span class="num">{esc(v)}</span></td>')
            else:
                badge = ""
                if i == 0 and flagged and headers[0] in ("Company", "Account"):
                    badge = '<span class="review-badge">flag</span>'
                tds.append(f"<td>{esc(v)}{badge}</td>")
        trs.append(f"<tr{cls}>{''.join(tds)}</tr>")

    return f"""<div class="table-wrap"><table>
<thead><tr>{''.join(ths)}</tr></thead>
<tbody>{''.join(trs)}</tbody>
</table></div>"""


def render_list(items: list) -> str:
    if not items:
        return ""
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def build_html(rows, by_seg, definitions, ambiguous, summary) -> str:
    total = len(rows)

    seg_cards = []
    for s in summary:
        meta = SEGMENTS[s["name"]]
        price = money(s["best_price"]) if s["best_price"] is not None else "—"
        seg_cards.append(f"""
        <a href="#seg-{meta['slug']}" class="seg-card seg-{meta['slug']}">
          <div class="seg-card-num">{s['n']}</div>
          <div class="seg-card-name">{esc(meta['short'])}</div>
          <div class="seg-card-price">median {esc(price)}</div>
        </a>""")

    profile_cards = []
    for s in summary:
        seg_name = s["name"]
        meta = SEGMENTS[seg_name]
        d = definitions.get(seg_name, {})
        profile_cards.append(f"""
    <article class="profile-card" id="profile-{meta['slug']}" style="--seg-color:{meta['color']};--seg-bg:{meta['bg']};--seg-border:{meta['border']}">
      <div class="profile-header">
        <span class="seg-pill" style="background:{meta['bg']};color:{meta['color']};border-color:{meta['border']}">{esc(meta['short'])}</span>
        <h3>{esc(meta['short'])}</h3>
        <span class="profile-count">{s['n']} accounts</span>
      </div>
      <p class="profile-defined"><strong>Selling motion:</strong> {esc(d.get('motion') or meta['motion'])}</p>
      <div class="profile-grid">
        <div class="profile-block">
          <h4>Quantitative signature</h4>
          {render_list(d.get('signature') or [])}
        </div>
        <div class="profile-block">
          <h4>Price range</h4>
          <p>{esc(d.get('price_range') or '—')}</p>
        </div>
        <div class="profile-block">
          <h4>Exemplars</h4>
          <p>{esc(d.get('exemplars') or '—')}</p>
        </div>
      </div>
      <a class="profile-jump" href="#seg-{meta['slug']}">View {s['n']}-account roster →</a>
    </article>""")

    summary_headers = [
        "Segment", "N", "Median Best Price", "Median Orders", "Median AOV",
        "Median PCodes", "Median Customers", "Median iPad", "Median Products", "Invoice feed %",
    ]
    summary_body = []
    for s in summary:
        summary_body.append([
            SEGMENTS[s["name"]]["short"],
            str(s["n"]),
            money(s["best_price"]) if s["best_price"] is not None else "—",
            num(s["orders"]) if s["orders"] is not None else "—",
            money(s["aov"]) if s["aov"] is not None else "—",
            num(s["pcodes"]) if s["pcodes"] is not None else "—",
            num(s["customers"]) if s["customers"] is not None else "—",
            num(s["ipad"]) if s["ipad"] is not None else "—",
            num(s["products"]) if s["products"] is not None else "—",
            f"{s['invoice_pct']}%",
        ])

    roster_html = []
    for seg_name, meta in SEGMENTS.items():
        rs = by_seg.get(seg_name, [])
        table = render_table(ROSTER_HEADERS, [roster_row(r) for r in rs])
        footnotes = ""
        if meta["slug"] == "luxury":
            footnotes = """
            <div class="footnotes">
              <p><span class="flag-dot">*</span> <strong>sbl $14:</strong> Only 1 Schonbek product has catalog <code>net_price</code>. Placement validated by AOV + brand position.</p>
              <p><strong>fms AOV:</strong> Inflated by Visual Comfort consolidated ordering — products are mid-range fans/studio lighting; kept in Specification for VC-family selling motion.</p>
            </div>"""
        if meta["slug"] == "premium":
            footnotes = """
            <div class="footnotes">
              <p><strong>Gabriella White family:</strong> <code>sc</code> = Gabriella White (parent LLC), <code>scw</code> = Summer Classics, <code>sccon</code> = Summer Classics Contract — three separately billed, simultaneously active orgs. Not a duplicate. Open flag: whether any sibling's retail/DTC footprint argues Multi-Channel.</p>
            </div>"""
        roster_html.append(f"""
        <details class="roster-block" id="seg-{meta['slug']}"{' open' if meta['slug'] == 'luxury' else ''}>
          <summary style="--seg-color:{meta['color']};--seg-bg:{meta['bg']};--seg-border:{meta['border']}">
            <div class="roster-summary-inner">
              <span class="seg-pill" style="background:{meta['bg']};color:{meta['color']};border-color:{meta['border']}">{esc(meta['short'])}</span>
              <span class="roster-title">{len(rs)} accounts</span>
              <span class="roster-desc">{esc(meta['motion'])}</span>
              <span class="expand-label">View roster</span>
            </div>
          </summary>
          <div class="roster-body">
            {table}
            {footnotes}
          </div>
        </details>""")

    key_calls_html = "".join(
        f'<div class="call-pill"><strong>{esc(t)}</strong><span>{esc(b)}</span></div>'
        for t, b in KEY_CALLS
    )
    questions_html = "".join(
        f'<div class="q-card"><strong>{esc(q)}</strong><span>{esc(a)}</span></div>'
        for q, a in FRAMEWORK_QUESTIONS
    )

    review_table = ""
    if ambiguous:
        review_table = render_table(
            ["Account", "Issue", "Current Placement", "Data Says"],
            ambiguous,
            org_col=0,
        )

    moved = [r for r in rows if r.get("segment_changed") == "YES"]
    moved_rows = [
        [r["Company"], r["org"], r["v3_segment"].split(". ", 1)[-1], r["v4_segment"].split(". ", 1)[-1]]
        for r in sorted(moved, key=lambda x: x["Company"])
    ]
    moved_table = render_table(
        ["Company", "org", "v3.2", "v4.0"],
        moved_rows,
    ) if moved_rows else "<p class='framework-lead'>No segment moves.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SuperCat Client Segmentation v4.0</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..700;1,9..40,400..700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #FAFAF8; --surface: #FFF; --panel: #F5F4F1; --border: #E8E5DE; --border-light: #F0EDE6;
  --text: #2C2925; --text-2: #6B6660; --text-muted: #9B958C;
  --accent: #4A6FA5; --accent-deep: #2E4A6E; --accent-glow: rgba(74,111,165,.08); --accent-border: rgba(74,111,165,.22);
  --ok: #1F8A5C; --ok-bg: #EDF7F1;
  --warn: #B8863A; --warn-bg: #FDF8EC; --warn-border: rgba(184,134,58,.3);
  --fd: 'DM Sans', system-ui, sans-serif; --fm: 'IBM Plex Mono', ui-monospace, monospace; --r: 10px;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font: 400 14px/1.65 var(--fd); color: var(--text); background: var(--bg); -webkit-font-smoothing: antialiased; }}
.page {{ max-width: 1100px; margin: 0 auto; padding: 0 28px 72px; }}

.hero {{ padding: 48px 0 36px; border-bottom: 1px solid var(--border); margin-bottom: 8px; position: relative; }}
.hero-top {{ display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 20px; }}
.eyebrow {{ font: 600 10px/1 var(--fm); letter-spacing: .14em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }}
.hero h1 {{ font: 700 36px/1.08 var(--fd); letter-spacing: -.02em; color: var(--text); max-width: 720px; }}
.hero-sub {{ font-size: 16px; color: var(--text-2); margin-top: 8px; max-width: 640px; }}
.status-badge {{ font: 600 10px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; padding: 8px 14px; border-radius: 20px; background: var(--ok-bg); color: var(--ok); border: 1px solid rgba(31,138,92,.25); white-space: nowrap; }}
.meta-grid {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.meta-chip {{ font: 500 11px/1.4 var(--fm); padding: 6px 12px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 6px; color: var(--text-2); }}
.meta-chip strong {{ color: var(--text); font-weight: 600; }}
.hero-accent {{ position: absolute; bottom: -1px; left: 0; width: 72px; height: 2px; background: var(--accent); }}

.toc {{ position: sticky; top: 0; z-index: 50; display: flex; gap: 6px; padding: 14px 0; margin-bottom: 28px; background: var(--bg); border-bottom: 1px solid var(--border); overflow-x: auto; }}
.toc a {{ padding: 6px 12px; font: 500 11px/1 var(--fd); color: var(--text-2); text-decoration: none; background: var(--panel); border: 1px solid var(--border-light); border-radius: 20px; white-space: nowrap; transition: .12s; }}
.toc a:hover, .toc a.active {{ color: var(--accent-deep); background: var(--accent-glow); border-color: var(--accent-border); }}

.section {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--r); padding: 28px 32px; margin-bottom: 20px; }}
.section-head {{ margin-bottom: 20px; }}
.section-head h2 {{ font: 700 22px/1.2 var(--fd); letter-spacing: -.015em; margin-bottom: 6px; }}
.section-head p {{ font-size: 13px; color: var(--text-muted); max-width: 720px; }}

.exec-lead {{ font-size: 15px; line-height: 1.6; color: var(--text-2); margin-bottom: 20px; max-width: 760px; }}
.exec-lead strong {{ color: var(--text); }}
.calls-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; }}
.call-pill {{ padding: 14px 16px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 8px; }}
.call-pill strong {{ display: block; font-size: 12px; font-weight: 600; color: var(--text); margin-bottom: 4px; }}
.call-pill span {{ font-size: 12px; color: var(--text-muted); line-height: 1.45; }}

.framework-lead {{ font-size: 14px; color: var(--text-2); line-height: 1.6; margin-bottom: 18px; max-width: 760px; }}
.q-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-bottom: 8px; }}
.q-card {{ padding: 14px 16px; background: var(--panel); border: 1px solid var(--border-light); border-radius: 8px; }}
.q-card strong {{ display: block; font-size: 13px; color: var(--text); margin-bottom: 4px; }}
.q-card span {{ font-size: 12px; color: var(--text-muted); line-height: 1.45; }}

.profile-card {{ border: 1px solid var(--border); border-left: 4px solid var(--seg-color); border-radius: var(--r); padding: 24px 28px; margin-bottom: 16px; background: var(--surface); }}
.profile-header {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }}
.profile-header h3 {{ font: 700 20px/1.2 var(--fd); color: var(--text); }}
.profile-count {{ font: 500 11px/1 var(--fm); color: var(--text-muted); margin-left: auto; }}
.profile-defined {{ font-size: 13px; color: var(--text-2); line-height: 1.55; margin-bottom: 16px; padding: 12px 14px; background: var(--seg-bg, var(--panel)); border-radius: 6px; }}
.profile-grid {{ display: grid; grid-template-columns: 1.4fr 1fr 1fr; gap: 14px; margin-bottom: 14px; }}
@media (max-width: 800px) {{ .profile-grid {{ grid-template-columns: 1fr; }} }}
.profile-block h4 {{ font: 600 10px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; color: var(--seg-color); margin-bottom: 8px; }}
.profile-block p {{ font-size: 13px; color: var(--text-2); line-height: 1.5; }}
.profile-block ul {{ list-style: none; padding: 0; }}
.profile-block li {{ font-size: 13px; color: var(--text-2); line-height: 1.45; padding-left: 14px; position: relative; margin-bottom: 5px; }}
.profile-block li::before {{ content: '—'; position: absolute; left: 0; color: var(--text-muted); }}
.profile-jump {{ font-size: 12px; font-weight: 600; color: var(--accent); text-decoration: none; }}
.profile-jump:hover {{ color: var(--accent-deep); text-decoration: underline; }}

.seg-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 4px; }}
@media (max-width: 900px) {{ .seg-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.seg-card {{ text-decoration: none; text-align: center; padding: 18px 12px; border-radius: var(--r); border: 1px solid var(--border); background: var(--surface); transition: transform .15s, box-shadow .15s; }}
.seg-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.06); }}
.seg-card-num {{ font: 700 32px/1 var(--fd); margin-bottom: 4px; }}
.seg-card-name {{ font: 600 11px/1.3 var(--fd); color: var(--text); margin-bottom: 6px; }}
.seg-card-price {{ font: 500 10px/1 var(--fm); color: var(--text-muted); }}
.seg-luxury {{ border-top: 3px solid #B8860B; }} .seg-luxury .seg-card-num {{ color: #B8860B; }}
.seg-premium {{ border-top: 3px solid #6B4FBB; }} .seg-premium .seg-card-num {{ color: #6B4FBB; }}
.seg-midmarket {{ border-top: 3px solid #1F8A5C; }} .seg-midmarket .seg-card-num {{ color: #1F8A5C; }}
.seg-volume {{ border-top: 3px solid #C44D4D; }} .seg-volume .seg-card-num {{ color: #C44D4D; }}

.table-wrap {{ overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; margin: 12px 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12.5px; }}
thead {{ background: var(--panel); }}
th {{ text-align: left; padding: 10px 12px; font: 600 9.5px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; color: var(--text-muted); border-bottom: 1px solid var(--border); cursor: help; }}
th.num {{ text-align: right; }}
td .num {{ display: inline-block; width: 100%; text-align: right; }}
td {{ padding: 9px 12px; border-bottom: 1px solid var(--border-light); vertical-align: top; }}
tr:last-child td {{ border-bottom: none; }}
tbody tr:hover {{ background: var(--accent-glow); }}
tr.flagged {{ background: var(--warn-bg); }}
tr.flagged:hover {{ background: #FBF0D8; }}
.missing {{ color: var(--text-muted); }}
.org-tag {{ font: 500 10.5px/1 var(--fm); padding: 2px 6px; background: var(--panel); border: 1px solid var(--border); border-radius: 4px; color: var(--text-2); }}
.num {{ font: 500 12px/1 var(--fm); font-variant-numeric: tabular-nums; }}
.review-badge {{ display: inline-block; margin-left: 6px; font: 600 8px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; padding: 2px 5px; border-radius: 3px; background: var(--warn-bg); color: var(--warn); border: 1px solid var(--warn-border); vertical-align: middle; }}
.flag-dot {{ color: var(--warn); font-weight: 700; margin-left: 2px; }}

details.glossary > summary {{ display: flex; align-items: center; gap: 10px; padding: 16px 20px; background: var(--panel); border: 1px solid var(--border); border-radius: var(--r); cursor: pointer; list-style: none; font-weight: 600; font-size: 14px; }}
details.glossary > summary::-webkit-details-marker {{ display: none; }}
details.glossary > summary::before {{ content: '▸'; color: var(--accent); transition: transform .15s; }}
details.glossary[open] > summary::before {{ transform: rotate(90deg); }}
details.glossary > summary .hint {{ margin-left: auto; font: 400 10px/1 var(--fm); color: var(--text-muted); text-transform: uppercase; letter-spacing: .06em; }}
.glossary-body {{ padding: 16px 4px 4px; margin-bottom: 20px; }}
.glossary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 10px; }}
.glossary-item {{ padding: 14px 16px; background: var(--surface); border: 1px solid var(--border-light); border-radius: 8px; }}
.glossary-item dt {{ font: 600 12px/1.3 var(--fd); margin-bottom: 6px; }}
.glossary-item dt code {{ font: 500 11px/1 var(--fm); color: var(--accent-deep); }}
.glossary-item dd {{ font-size: 12px; color: var(--text-2); line-height: 1.5; }}

.roster-block {{ margin-bottom: 12px; border: 1px solid var(--border); border-radius: var(--r); overflow: hidden; background: var(--surface); }}
.roster-block > summary {{ list-style: none; cursor: pointer; padding: 0; border-left: 4px solid var(--seg-color, var(--accent)); }}
.roster-block > summary::-webkit-details-marker {{ display: none; }}
.roster-summary-inner {{ padding: 18px 22px; display: grid; grid-template-columns: auto 1fr auto; grid-template-rows: auto auto; gap: 4px 14px; align-items: center; }}
.seg-pill {{ font: 600 10px/1 var(--fm); letter-spacing: .06em; text-transform: uppercase; padding: 5px 10px; border-radius: 5px; border: 1px solid; grid-row: span 2; }}
.roster-title {{ font: 700 16px/1.2 var(--fd); color: var(--text); }}
.roster-desc {{ grid-column: 2; font-size: 12.5px; color: var(--text-muted); line-height: 1.45; }}
.expand-label {{ grid-row: span 2; font: 600 9px/1 var(--fm); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); opacity: .7; }}
.roster-block[open] .expand-label {{ display: none; }}
.roster-block > summary:hover {{ background: var(--seg-bg, var(--panel)); }}
.roster-body {{ padding: 0 16px 16px; border-top: 1px solid var(--border-light); }}
.footnotes {{ margin-top: 12px; padding: 12px 14px; background: var(--panel); border-radius: 6px; font-size: 12px; color: var(--text-2); line-height: 1.55; }}
.footnotes p + p {{ margin-top: 8px; }}
.footnotes code {{ font: 500 10.5px/1 var(--fm); }}

.review-banner {{ display: flex; gap: 14px; padding: 16px 18px; background: var(--warn-bg); border: 1px solid var(--warn-border); border-radius: 8px; margin-bottom: 16px; align-items: flex-start; }}
.review-banner-icon {{ font: 700 18px/1 var(--fd); color: var(--warn); }}
.review-banner p {{ font-size: 13px; color: var(--text-2); line-height: 1.5; }}

.next-step {{ text-align: center; padding: 32px; background: linear-gradient(135deg, var(--surface), var(--accent-glow)); border: 1px solid var(--accent-border); border-radius: var(--r); }}
.next-step h2 {{ font: 700 20px/1.2 var(--fd); margin-bottom: 8px; }}
.next-step p {{ font-size: 14px; color: var(--text-2); max-width: 560px; margin: 0 auto; }}

@media print {{
  .toc {{ display: none; }}
  .roster-block {{ break-inside: avoid; }}
}}
</style>
</head>
<body>
<div class="page">

<header class="hero">
  <div class="hero-top">
    <div>
      <div class="eyebrow">SuperCat Ops · Customer Segmentation</div>
      <h1>Client Segmentation v4.0</h1>
      <p class="hero-sub">By how they sell and to whom — not by how they use eCat</p>
    </div>
    <span class="status-badge">Stamped · corrected</span>
  </div>
  <div class="meta-grid">
    <span class="meta-chip"><strong>Date</strong> July 9, 2026</span>
    <span class="meta-chip"><strong>Universe</strong> {total} accounts</span>
    <span class="meta-chip"><strong>Counts</strong> 33 / 38 / 24 / 14</span>
    <span class="meta-chip"><strong>Baseline</strong> v3.2 → stamped v4.0</span>
    <span class="meta-chip"><strong>Purpose</strong> Rep co-pilot buckets</span>
  </div>
  <div class="hero-accent"></div>
</header>

<nav class="toc" id="toc">
  <a href="#summary">Summary</a>
  <a href="#framework">Framework</a>
  <a href="#profiles">Profiles</a>
  <a href="#overview">Data</a>
  <a href="#glossary">Column key</a>
  <a href="#rosters">Rosters</a>
  <a href="#moves">Moves</a>
  <a href="#review">Flags</a>
  <a href="#next">Next</a>
</nav>

<section class="section" id="summary">
  <div class="section-head">
    <h2>Executive Summary</h2>
    <p>Kjael-stamped 2026-07-09; identity + enrichment corrections through Round 3 the same day.</p>
  </div>
  <p class="exec-lead">The <strong>4-segment selling-motion model holds</strong>. Specialty is dissolved. Headline counts match the stamp exactly — what changed post-stamp is which org two rows point at (Gabriella White / Summer Classics), plus enrichment backfill for five Round-1 matches. Price remains a continuous dimension inside each bucket, not the classifier.</p>
  <div class="calls-grid">{key_calls_html}</div>
</section>

<section class="section" id="framework">
  <div class="section-head">
    <h2>How We Segment</h2>
    <p>Stamped v3 → v3.2 framework, confirmed in v4. Selling motion classifies; price validates.</p>
  </div>
  <p class="framework-lead">This is <strong>not</strong> eCat usage segmentation. A company with 300k orders and a company with 2 can share a bucket if they sell the same way in the market. Grain is the <strong>billing entity</strong> — parent/sibling brands stay separate rows when separately billed.</p>
  <div class="q-grid">{questions_html}</div>
</section>

<section class="section" id="profiles">
  <div class="section-head">
    <h2>Segment Profiles</h2>
    <p>What they sell, how they sell, who buys — co-pilot context.</p>
  </div>
  {''.join(profile_cards)}
</section>

<section class="section" id="overview">
  <div class="section-head">
    <h2>Segment Data at a Glance</h2>
    <p>Medians recomputed from the MASTER CSV via <code>statistics.median()</code>.</p>
  </div>
  <div class="seg-grid">{''.join(seg_cards)}</div>
  <div style="margin-top:24px">
    <div class="section-head" style="margin-bottom:12px"><h2 style="font-size:17px">Median Profile by Segment</h2></div>
    {render_table(summary_headers, summary_body, org_col=-1)}
  </div>
</section>

<details class="glossary" id="glossary">
  <summary>Column Key <span class="hint">eCat &amp; data terms</span></summary>
  <div class="glossary-body">
    <div class="glossary-grid">
      {''.join(f'<dl class="glossary-item"><dt><code>{esc(k)}</code></dt><dd>{esc(v)}</dd></dl>' for k, v in GLOSSARY.items())}
    </div>
  </div>
</details>

<section class="section" id="rosters" style="padding:24px 28px">
  <div class="section-head">
    <h2>Segment Rosters</h2>
    <p>{total} accounts across four buckets. Rows marked <span class="review-badge">flag</span> are judgment calls from §5 — not automatic moves.</p>
  </div>
  {''.join(roster_html)}
</section>

<section class="section" id="moves">
  <div class="section-head">
    <h2>v3.2 → v4.0 Moves ({len(moved)})</h2>
    <p>All moves are from Specialty or unmatched (<code>??</code>) — no core-segment reclassifications.</p>
  </div>
  {moved_table}
</section>

<section class="section" id="review">
  <div class="section-head">
    <h2>Accounts That Remain Ambiguous</h2>
  </div>
  <div class="review-banner">
    <span class="review-banner-icon">⚑</span>
    <p><strong>Judgment calls, not data errors.</strong> Kept in current placement unless a human decides otherwise from real-world selling motion. Separate open flags: dormant <code>lna</code> vs active <code>leg</code>; Gabriella White family Brand-Building vs Multi-Channel.</p>
  </div>
  {review_table}
</section>

<section class="next-step" id="next">
  <h2>Next Step</h2>
  <p>Build <strong>personas within each segment</strong> for rep co-pilot initialization. Sources: <code>current/SuperCat_Client_Segmentation_v4.0.md</code> + MASTER CSV.</p>
</section>

</div>
<script>
(function() {{
  const toc = document.getElementById('toc');
  const links = [...toc.querySelectorAll('a')];
  const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const obs = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
      }}
    }});
  }}, {{ rootMargin: '-20% 0px -70% 0px' }});
  sections.forEach(s => obs.observe(s));
}})();
</script>
</body>
</html>"""


def main():
    rows, by_seg = load_csv()
    md = MD_PATH.read_text(encoding="utf-8")
    definitions = parse_definitions(md)
    ambiguous = parse_ambiguous(md)
    summary = build_summary(by_seg)
    html = build_html(rows, by_seg, definitions, ambiguous, summary)
    OUT.write_text(html, encoding="utf-8")
    counts = {SEGMENTS[s]["short"]: len(by_seg.get(s, [])) for s in SEGMENTS}
    print(f"Wrote {OUT}")
    print(f"  {len(rows)} accounts · {counts}")
    for s in summary:
        print(f"  {SEGMENTS[s['name']]['short']}: n={s['n']} median_best={s['best_price']} median_aov={s['aov']}")


if __name__ == "__main__":
    main()
