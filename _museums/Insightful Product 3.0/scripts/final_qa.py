#!/usr/bin/env python3
"""Final QA harness — validates assembled reports against operator rules + gold structure.

Checks per client: file integrity, sections present per manifest, §1/§6 structure,
confidence-tier labels vs computed tiers (with portal fallback), table thead coverage,
banned terms, what-this-means openers, coaching-card presence, ALL-CAPS entity names.

Usage: python final_qa.py [--run-date 2026-06-17] [shortname ...]
Exit 0 if all pass (warnings allowed), 1 if any FAIL.
"""
import argparse
import re
import sys
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "runs"

SECTION_IDS = {
    "signals": 1, "accounts": 2, "product": 3,
    "commerce": 4, "team": 5, "platform": 6, "appendix": "A",
}
TIER_FROM_LABEL = {
    "full picture": "FULL", "strong view": "STRONG",
    "partial view": "PARTIAL", "limited view": "LIMITED",
}
ALL_CLIENTS = ("afx all arl bri bp clc vl prog clli clm cci dals da df eglo_can eglo eli el "
               "fal gh gcl gl hfg hvl kal kll mlc mli ml ril shl sbl sca vic vcg wac").split()


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def computed_tiers(conf_text: str) -> dict[int, str]:
    """Parse '## Computed Tiers' rows '| §N Name | TIER | ...' -> {N: TIER}."""
    out = {}
    in_tbl = False
    for line in conf_text.splitlines():
        if line.startswith("## Computed Tiers"):
            in_tbl = True
            continue
        if in_tbl and line.startswith("|"):
            m = re.match(r"\|\s*§(\d+)\b[^|]*\|\s*([A-Z]+)\s*\|", line)
            if m:
                out[int(m.group(1))] = m.group(2)
    return out


def manifest_include(man_text: str) -> set[int]:
    inc = set()
    for line in man_text.splitlines():
        m = re.match(r"\|\s*([2-6])\s*\|.*\|\s*INCLUDE\s*\|", line)
        if m:
            inc.add(int(m.group(1)))
    return inc


def gate(flags_text: str, name: str) -> str:
    m = re.search(rf"\|\s*{re.escape(name)}\s*\|\s*([^|]+?)\s*\|", flags_text)
    return m.group(1).strip() if m else ""


def coaching_count(text: str) -> int:
    m = re.search(r"Candidates above (?:the )?floor[^0-9]*(\d+)", text)
    if m:
        return int(m.group(1))
    # fallback: count ranked rows | 1 | ... in the table
    return len(re.findall(r"^\|\s*\d+\s*\|\s*[A-Za-z]", text, re.MULTILINE))


def section_slices(html: str) -> dict:
    """Return {section_id: html_slice} by slicing between consecutive id= anchors."""
    marks = []
    for sid in SECTION_IDS:
        m = re.search(rf'id="{sid}"', html)
        if m:
            marks.append((m.start(), sid))
    marks.sort()
    slices = {}
    for i, (pos, sid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        slices[sid] = html[pos:end]
    return slices


def qa_client(shortname: str, run_date: str):
    base = RUNS / f"{shortname}_{run_date}"
    out = base / "output" / f"{shortname}_{run_date}_intelligence_report.html"
    fails, warns = [], []

    if not out.exists():
        return ["NO OUTPUT FILE"], [], {}
    html = read(out)
    low = html.lower()
    size = len(html)

    # 1. File integrity
    if size < 40_000:
        warns.append(f"small file ({size//1024}KB)")
    if "<!doctype" not in low:
        fails.append("missing <!DOCTYPE>")
    if "</html>" not in low:
        fails.append("missing </html>")
    nunres = len(re.findall(r"\{\{[A-Z_]+\}\}", html))
    if nunres:
        fails.append(f"{nunres} unresolved {{{{...}}}}")
    od, cd = html.count("<details"), html.count("</details>")
    if od != cd:
        fails.append(f"unbalanced details ({od} open / {cd} close)")

    conf = read(base / "cache" / "section_confidence.md")
    man = read(base / "cache" / "section_manifest.md")
    flags = read(base / "cache" / "gate_flags.md")
    tiers = computed_tiers(conf)
    include = manifest_include(man)
    has_portal = gate(flags, "HAS_PORTAL_ORDERS").lower() == "true"
    slices = section_slices(html)

    # 2. Sections present
    if "signals" not in slices:
        fails.append("§1 Signal Summary missing")
    for n, sid in [(2, "accounts"), (3, "product"), (4, "commerce"), (5, "team"), (6, "platform")]:
        if n in include and sid not in slices:
            fails.append(f"§{n} ({sid}) INCLUDE in manifest but MISSING from report")
    if "appendix" not in slices:
        warns.append("appendix missing")

    # 3. §1 structure (check against full html — id= anchor sits mid-tag)
    sig = slices.get("signals", "")
    if sig:
        if not re.search(r'<section[^>]*id="signals"', html):
            fails.append("§1 not an open <section> (should not be <details>)")
        if re.search(r'<details[^>]*id="signals"', html):
            fails.append("§1 wrapped in <details> (should be open <section>)")
        if 'class="highlights"' not in sig:
            fails.append("§1 missing <ol class=highlights>")
        if "priorit" not in sig.lower():
            warns.append("§1 missing priorities block")

    # 4. §6 structure
    plat = slices.get("platform", "")
    if plat and "data-confidence" in plat:
        fails.append("§6 has a data-confidence header (should not)")

    # 5. Confidence tiers (§2-§5)
    for n, sid in [(2, "accounts"), (3, "product"), (4, "commerce"), (5, "team")]:
        if n not in include or sid not in slices:
            continue
        blk = slices[sid]
        m = re.search(r'data-confidence-label"[^>]*>\s*([^<]+?)\s*<', blk)
        if not m:
            fails.append(f"§{n} missing data-confidence label")
            continue
        rlabel = m.group(1).strip().lower()
        rtier = TIER_FROM_LABEL.get(rlabel)
        ctier = tiers.get(n)
        if rtier is None:
            warns.append(f"§{n} unrecognized confidence label '{m.group(1).strip()}'")
        elif ctier and rtier != ctier:
            # documented fallback: computed FULL/STRONG can render PARTIAL when portal absent
            if ctier in ("FULL", "STRONG") and rtier == "PARTIAL" and not has_portal:
                pass  # legitimate fallback
            else:
                fails.append(f"§{n} tier MISMATCH: computed {ctier}, rendered {rtier} ({rlabel})")

    # 6. Table thead coverage (block-accurate: categorize each <table>...</table>)
    tables = re.findall(r"<table\b.*?</table>", html, re.DOTALL)
    ntab = len(tables)
    nthead = sum(1 for t in tables if "<thead>" in t)
    unwrapped = sum(1 for t in tables if "<thead>" not in t and re.search(r"<tr[^>]*>\s*<th", t))
    headerless = ntab - nthead - unwrapped  # no <thead> AND no <th> header row at all
    if headerless:
        fails.append(f"{headerless} tables with NO header at all")
    # appendix data-sources table is a known single unwrapped table — allow 1
    if unwrapped > 1:
        fails.append(f"{unwrapped} tables use <tr><th> without a <thead> wrapper (no header styling)")
    elif unwrapped == 1:
        warns.append("1 unwrapped header table (appendix data-sources)")

    # 7. Banned terms
    for term in ["mixpanel", "clicky", "health score", "portal orders", "portal ordering"]:
        if term in low:
            fails.append(f"banned term '{term}' ({low.count(term)}x)")
    # ERP as a standalone word, not 'Enterprise'
    erp = re.findall(r"(?<![A-Za-z])ERP(?![A-Za-z])", html)
    if erp:
        fails.append(f"banned 'ERP' standalone ({len(erp)}x)")

    # 8. what-this-means openers
    wtm = re.findall(r'class="what-this-means[^"]*">(.*?)</div>', html, re.DOTALL)
    bad = [w for w in wtm if not re.match(r'\s*<strong>\s*(Action|Bottom line|What this)', w)]
    if wtm and len(bad) > 0:
        warns.append(f"{len(bad)}/{len(wtm)} what-this-means not starting Action/Bottom line")

    # 9. Coaching cards
    cc = coaching_count(read(base / "cache" / "coaching_candidates.md"))
    if 5 in include:
        team = slices.get("team", "")
        has_cards = ("coaching-card" in team) or ("Coaching Opportunities" in team) or ("coaching-cards" in team)
        if cc >= 1 and not has_cards:
            fails.append(f"coaching_candidates lists {cc} but §5 has NO coaching cards")
        if cc == 0 and has_cards:
            warns.append("§5 shows coaching cards but candidates=0")

    # 10. ALL-CAPS entity cells (multi-word, looks like a mangled customer name)
    caps = re.findall(r"<td>([A-Z][A-Z&'./-]{2,}(?:\s+[A-Z][A-Z&'./-]{2,}){1,})</td>", html)
    caps = [c for c in caps if not re.fullmatch(r"[A-Z]{2,4}(\s+[A-Z]{2,4})*", c)]  # drop short acronym-only
    if caps:
        warns.append(f"{len(caps)} ALL-CAPS multiword cells (e.g. {caps[0][:30]!r})")

    info = {"size_kb": size // 1024, "include": sorted(include),
            "tiers": tiers, "portal": has_portal, "coaching": cc,
            "tables": ntab, "thead": nthead, "wtm": len(wtm)}
    return fails, warns, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-date", default="2026-06-17")
    ap.add_argument("clients", nargs="*", default=ALL_CLIENTS)
    a = ap.parse_args()
    clients = a.clients or ALL_CLIENTS

    total_fail = 0
    print(f"{'CLIENT':<10}{'SIZE':>6}  {'INCL':<12}{'RESULT'}")
    print("-" * 70)
    details = []
    for c in clients:
        fails, warns, info = qa_client(c, a.run_date)
        if not info:
            print(f"{c:<10}{'--':>6}  {'':<12}❌ {fails[0]}")
            total_fail += 1
            continue
        status = "✅ PASS" if not fails else f"❌ FAIL ({len(fails)})"
        if fails:
            total_fail += 1
        wtag = f"  ⚠️{len(warns)}" if warns else ""
        incl = ",".join(str(x) for x in info["include"])
        print(f"{c:<10}{str(info['size_kb'])+'k':>6}  {incl:<12}{status}{wtag}")
        if fails or warns:
            details.append((c, fails, warns))

    print("\n" + "=" * 70)
    for c, fails, warns in details:
        if fails:
            print(f"\n{c}  — FAILURES:")
            for f in fails:
                print(f"    ❌ {f}")
        if warns:
            print(f"{c}  — warnings:")
            for w in warns:
                print(f"    ⚠️  {w}")
    print("\n" + "=" * 70)
    print(f"RESULT: {len(clients)-total_fail}/{len(clients)} pass, {total_fail} with failures")
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
