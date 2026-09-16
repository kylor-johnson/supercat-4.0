"""
Insightful Product 3.0 — Report Assembler (deterministic)

Replaces the LLM-based Step 4 assembly (except Signal Summary composition).
Reads the HTML template, all section fragments, and gate_flags.md. Concatenates
fragments in fixed order, substitutes {{PARAM}} placeholders, strips HTML
comments, and writes the final report.

Signal Summary (§1) must already exist as fragments/section_01.html — it's
built by the Signal Summary agent (the only remaining LLM step in assembly).

No LLM calls. No network. Runs in < 1 second.

Usage:
    python assemble_report.py --shortname cci --run-date 2026-06-17
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASSEMBLY_ORDER = [
    ("section_01.html", "signals"),
    ("section_05.html", "team"),
    ("section_02.html", "accounts"),
    ("section_04.html", "commerce"),
    ("section_03.html", "product"),
    ("section_06.html", "platform"),
]


def parse_gate_params(gate_text: str) -> dict[str, str]:
    """Extract template parameters from gate_flags.md + org identity."""
    params: dict[str, str] = {}

    name_match = re.search(r"^# Gate Flags — (.+?) \((\w+), org_id=(\d+)\)", gate_text, re.MULTILINE)
    if name_match:
        params["CLIENT_NAME"] = name_match.group(1)
        params["ORG_SHORTNAME"] = name_match.group(2)

    for line in gate_text.split("\n"):
        if line.startswith("| ") and " | " in line and "---" not in line and "Flag" not in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 2:
                params[parts[0]] = parts[1]

    run_match = re.search(r"Run date.*?:\s*(\d{4}-\d{2}-\d{2})", gate_text)
    if run_match:
        from datetime import date
        d = date.fromisoformat(run_match.group(1))
        params["REPORT_DATE"] = d.strftime("%B %d, %Y")
        end_month = d.replace(day=1)
        start_month = end_month.replace(year=end_month.year - 1)
        params["PERIOD_END"] = end_month.strftime("%B %Y")
        params["PERIOD_START"] = start_month.strftime("%B %Y")
        params["PERIOD_LABEL"] = "Trailing 12 Months"

    params.setdefault("REPORT_TYPE_LABEL", "Customer Intelligence Report")
    params.setdefault("REPORT_MODE", "standard")
    params.setdefault("REPORT_STAGE_BADGE", "Full · iPad")

    return params


def extract_template_parts(template_path: Path) -> tuple[str, str, str, str]:
    """Split template into: head (doctype through <style>...</style>), 
    body_open (header + toc stub), body_close (footer), script+close."""
    text = template_path.read_text(encoding="utf-8")

    style_end = text.find("</style>")
    if style_end == -1:
        print("ERROR: </style> not found in template")
        sys.exit(1)
    style_end = text.find("\n", style_end) + 1
    head = text[:style_end]

    body_start = text.find("<body>")
    body_section = text[body_start:]

    script_start = text.find("<script>")
    script_section = text[script_start:]

    footer_start = text.find('<footer class="footer">')
    footer_section = text[footer_start:script_start]

    return head, body_section, footer_section, script_section


def build_toc(rendered_sections: list[str]) -> str:
    """Build TOC strip with only rendered sections."""
    toc_map = {
        "signals": ("Signal Summary", "#signals"),
        "team": ("Team Intelligence", "#team"),
        "accounts": ("Account Intelligence", "#accounts"),
        "commerce": ("Commerce Patterns", "#commerce"),
        "product": ("Product Intelligence", "#product"),
        "platform": ("Platform Context", "#platform"),
        "appendix": ("Appendix", "#appendix"),
    }
    links = []
    for sec_id in rendered_sections:
        if sec_id in toc_map:
            label, href = toc_map[sec_id]
            links.append(f'    <a href="{href}">{label}</a>')
    links.append('    <a href="#appendix">Appendix</a>')
    return '  <nav class="toc-strip" id="tocStrip">\n' + "\n".join(links) + "\n  </nav>"


def build_appendix() -> str:
    """Build a minimal attribution-only appendix."""
    return """<section class="section appendix" id="appendix">
  <h2 class="section-title"><span class="section-num">Appendix</span> Data Sources</h2>
  <table class="data-sources">
    <thead>
    <tr><th>Source</th><th>Coverage</th><th>Used For</th></tr>
    </thead>
    <tbody>
    <tr><td>eCat iPad Orders</td><td>Full LTM</td><td>Rep performance, order velocity, customer activity</td></tr>
    <tr><td>All-Channel Business Data</td><td>Full LTM</td><td>Total business context, order channel mix, digital enablement</td></tr>
    <tr><td>App Usage Analytics</td><td>Full LTM</td><td>Behavioral patterns, engagement scoring, archetype classification</td></tr>
    <tr><td>Product Catalog</td><td>Current</td><td>Catalog completeness, new item tracking</td></tr>
    <tr><td>Inventory System</td><td>Current</td><td>Stock-out detection, fill rate analysis</td></tr>
    <tr><td>Customer Master</td><td>Current</td><td>Territory mapping, customer segmentation</td></tr>
    </tbody>
  </table>
</section>"""


def strip_html_comments(text: str) -> str:
    """Remove all HTML comments."""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def substitute_params(text: str, params: dict[str, str]) -> str:
    """Replace {{PARAM}} placeholders with values from params dict."""
    def replacer(m):
        key = m.group(1)
        return params.get(key, m.group(0))
    return re.sub(r"\{\{([A-Z_]+)\}\}", replacer, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Insightful 3.0 — Deterministic Report Assembler")
    parser.add_argument("--shortname", required=True)
    parser.add_argument("--run-date", required=True)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    run_dir = project_root / "runs" / f"{args.shortname}_{args.run_date}"
    cache_dir = run_dir / "cache"
    fragments_dir = run_dir / "fragments"
    output_dir = run_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    template_path = project_root / "authority" / "html_report_template.html"
    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}")
        sys.exit(1)

    gate_text = (cache_dir / "gate_flags.md").read_text(encoding="utf-8")
    params = parse_gate_params(gate_text)
    print(f"Assembling report for {params.get('CLIENT_NAME', args.shortname)} ({args.shortname})")

    template_text = template_path.read_text(encoding="utf-8")

    style_start = template_text.find("<style")
    style_end = template_text.find("</style>") + len("</style>")
    style_block = template_text[style_start:style_end]

    script_start = template_text.find("<script>")
    script_end = template_text.find("</script>") + len("</script>")
    script_block = template_text[script_start:script_end]

    rendered_sections = []
    section_html_parts = []
    for filename, sec_id in ASSEMBLY_ORDER:
        fpath = fragments_dir / filename
        if fpath.exists():
            content = fpath.read_text(encoding="utf-8")
            section_html_parts.append(content)
            rendered_sections.append(sec_id)
            print(f"  + {filename} ({len(content):,} bytes)")
        else:
            print(f"  - {filename} (not found, skipping)")

    toc_html = build_toc(rendered_sections)
    appendix_html = build_appendix()

    header_html = f"""<header class="header" id="top">
    <div class="h-brand"><span>Insightful &middot; Customer Intelligence</span></div>
    <div class="h-customer">{params.get('CLIENT_NAME', args.shortname)}</div>
    <div class="h-type">{params.get('REPORT_TYPE_LABEL', 'Customer Intelligence Report')}</div>
    <div class="h-meta">{params.get('PERIOD_START', '')} &ndash; {params.get('PERIOD_END', '')} ({params.get('PERIOD_LABEL', 'Trailing 12 Months')}) &middot; Report Date: {params.get('REPORT_DATE', '')}</div>
    <div class="h-meta" style="margin-top: 4px;"><span class="badge badge-info">{params.get('REPORT_STAGE_BADGE', 'Full')}</span></div>
    <div class="h-accent"></div>
  </header>"""

    footer_html = f"""<footer class="footer">
    <div class="footer-brand">Insightful &middot; Customer Intelligence</div>
    <div class="footer-text">Generated {params.get('REPORT_DATE', '')} &middot; {params.get('CLIENT_NAME', '')} &middot; Confidential &mdash; prepared for {params.get('CLIENT_NAME', '')} use only</div>
  </footer>"""

    full_html = "\n".join([
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{params.get('CLIENT_NAME', '')} — Customer Intelligence Report</title>",
        style_block,
        "</head>",
        "<body>",
        "<div class=\"page\">",
        header_html,
        toc_html,
        "",
        "\n\n".join(section_html_parts),
        "",
        appendix_html,
        "",
        footer_html,
        "</div>",
        script_block,
        "</body>",
        "</html>",
    ])

    full_html = strip_html_comments(full_html)
    full_html = substitute_params(full_html, params)

    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", full_html)
    if unresolved:
        unique = set(unresolved)
        print(f"  WARNING: {len(unique)} unresolved placeholders: {', '.join(sorted(unique)[:10])}")

    output_path = output_dir / f"{args.shortname}_{args.run_date}_intelligence_report.html"
    output_path.write_text(full_html, encoding="utf-8")
    print(f"\n  Output: {output_path}")
    print(f"  Size: {len(full_html):,} bytes ({len(full_html)//1024} KB)")
    print(f"  Sections: {len(rendered_sections)}")
    print(f"  HTML comments remaining: {full_html.count('<!--')}")
    print(f"  Unresolved {{{{...}}}}: {len(unresolved)}")
    print("Done.")


if __name__ == "__main__":
    main()
