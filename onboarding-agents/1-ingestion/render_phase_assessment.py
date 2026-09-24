#!/usr/bin/env python3
"""
Render an Onboarding Phase Assessment HTML artifact from its JSON.

  python render_phase_assessment.py <data.json> [--out <out.html>]
  python render_phase_assessment.py <data.json> --check <example.html>

Inputs
  <data.json>            structured report data (see phase-assessment.schema.json)
  phase-assessment.template.html   the layout shell (sibling of this script)

Design
  The template is the single source of markup. This script only FILLS it:
  it clones `@repeat` regions, keeps/drops `@optional` regions, and substitutes
  {{TOKENS}}. No styling decisions live here — they live in phase-assessment.css.

Conventions
  • Plain-text fields are HTML-escaped here (author them with raw &, <, >).
  • Fields whose name ends in `_html` (detail_html, said_html, appendix items)
    are trusted inline HTML and inserted verbatim — that is where verbatim
    quotes live, wrapped in <blockquote class="oa-quote">.
"""

import argparse
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "phase-assessment.template.html")

STATUS_DOT = {"done": "oa-dot-done", "in_progress": "oa-dot-progress", "not_started": "oa-dot-todo"}
STATUS_WORD = {"done": "Done", "in_progress": "In progress", "not_started": "Not started"}
STATUS_STATE = {"done": "is-done", "in_progress": "is-progress", "not_started": "is-todo"}


def esc(s):
    return html.escape(str(s), quote=False)


def sub_tokens(text, mapping):
    for k, v in mapping.items():
        text = text.replace("{{%s}}" % k, v)
    return text


def _region_re(name):
    return re.compile(
        r"<!--\s*@(?:repeat|optional)\s+" + re.escape(name) + r"\b.*?-->(.*?)<!--\s*@end\s+" + re.escape(name) + r"\s*-->",
        re.DOTALL,
    )


def fill_repeat(text, name, items, render_item):
    """Clone the region's inner fragment once per item."""
    rx = _region_re(name)
    m = rx.search(text)
    if not m:
        raise ValueError("region not found: @repeat %s" % name)
    inner = m.group(1)
    rendered = "".join(render_item(inner, it) for it in items)
    return text[: m.start()] + rendered + text[m.end():]


def fill_optional(text, name, keep, render=None):
    """Keep (optionally transforming inner) or drop the whole region."""
    rx = _region_re(name)
    m = rx.search(text)
    if not m:
        raise ValueError("region not found: @optional %s" % name)
    inner = m.group(1)
    replacement = "" if not keep else (render(inner) if render else inner)
    return text[: m.start()] + replacement + text[m.end():]


def replace_region(text, name, content):
    """Replace the whole region with a ready-made string (used for agenda + appendix)."""
    rx = _region_re(name)
    m = rx.search(text)
    if not m:
        raise ValueError("region not found: %s" % name)
    return text[: m.start()] + content + text[m.end():]


# ── renderers ────────────────────────────────────────────────────────────

def render_step(inner, st):
    return sub_tokens(inner, {
        "STEP_NO": str(st["no"]),
        "STEP_LABEL": esc(st["label"]),
        "STATUS_DOT": STATUS_DOT[st["status"]],
        "STATUS_WORD": STATUS_WORD[st["status"]],
        "WHAT_WE_SEE": esc(st["what_we_see"]),
    })


def render_flag(inner, f):
    code = f.get("code")
    code_suffix = ' <span class="oa-code">(%s)</span>' % esc(code) if code else ""
    return sub_tokens(inner, {
        "FLAG_STEP": esc(f["step"]),
        "ISSUE": esc(f["issue"]),
        "CODE_SUFFIX": code_suffix,
        "SOURCE": esc(f["source"]),
        "SAID_HTML": f["said_html"],
    })


def integration_label(mode):
    return {
        "managed": "Us (Managed)",
        "certified": "Them (Certified)",
    }.get(mode, '<span class="kdt-empty">—</span>')


def render_cohort_row(inner, c):
    return sub_tokens(inner, {
        "SHORT": c["short"],
        "CLIENT_NAME": esc(c["name"]),
        "PHASE_N": str(c["phase_n"]),
        "PHASE_NAME": esc(c["phase_name"]),
        "WORKING_ON": esc(c["next_phase_name"]),
        "DAYS": esc(c["days"]),
        "INTEGRATION_LABEL": integration_label(c["integration"]["mode"]),
        "ONE_THING": esc(c["one_thing"]),
    })


def agenda_li(item):
    lead = esc(item["lead"])
    detail = item.get("detail_html", "")
    if item.get("urgent"):
        return ('<li class="oa-urgent"><span class="oa-urgent-chip">Resolve first</span> '
                "<b>%s</b> %s</li>" % (lead, detail))
    return "<li><b>%s</b> %s</li>" % (lead, detail)


def render_agenda_bucket(items):
    if not items:
        return '<li class="oa-agenda-empty">None this week</li>'
    return "".join(agenda_li(it) for it in items)


def render_client(client_fragment, c):
    frag = client_fragment
    integ = c["integration"]
    mode = integ["mode"]

    # where-they-are: exactly the 7 steps
    frag = fill_repeat(frag, "where-row", c["steps"], render_step)

    # integration row (Managed only)
    if mode == "managed":
        frag = fill_optional(frag, "integration-row", True, lambda inner: sub_tokens(inner, {
            "INTEG_DOT": STATUS_DOT[integ["status"]],
            "INTEG_WORD": STATUS_WORD[integ["status"]],
            "INTEG_WHAT_WE_SEE": esc(integ["what_we_see"]),
        }))
    else:
        frag = fill_optional(frag, "integration-row", False)

    # integration note (Certified only)
    if mode == "certified":
        frag = fill_optional(frag, "integration-note", True,
                             lambda inner: sub_tokens(inner, {"INTEGRATION_NOTE": esc(integ["note"])}))
    else:
        frag = fill_optional(frag, "integration-note", False)

    # flags section (omit entirely when 0 flags)
    flags = c.get("flags", [])
    if flags:
        def render_flags_section(inner):
            inner = fill_repeat(inner, "flag-row", flags, render_flag)
            return inner.replace("{{FLAG_COUNT}}", str(len(flags)))
        frag = fill_optional(frag, "flags-section", True, render_flags_section)
    else:
        frag = fill_optional(frag, "flags-section", False)

    # post-flags read / caveat (optional)
    note = c.get("note_html")
    if note:
        frag = fill_optional(frag, "client-note", True,
                             lambda inner: sub_tokens(inner, {"NOTE_HTML": note}))
    else:
        frag = fill_optional(frag, "client-note", False)

    # stepper states
    states = {}
    for st in c["steps"]:
        cls = STATUS_STATE[st["status"]]
        if st["no"] == c.get("current_step"):
            cls += " is-current"
        states["STATE_%d" % st["no"]] = cls

    scalars = {
        "SHORT": c["short"],
        "CLIENT_NAME": esc(c["name"]),
        "PHASE_N": str(c["phase_n"]),
        "PHASE_NAME": esc(c["phase_name"]),
        "NEXT_PHASE_NAME": esc(c["next_phase_name"]),
        "PRODUCT": esc(c["product"]),
        "DAYS": esc(c["days"]),
        "DAYS_QUALIFIER": esc(c.get("days_qualifier", "")),
        "ENGAGEMENT": esc(c["engagement"]),
        "NEXT_STEP": esc(c["next_step"]),
        "BOTTOM_LINE": esc(c["bottom_line"]),
        "MEETINGS": esc(c["activity"]["meetings"]),
        "SUPPORT": esc(c["activity"]["support"]),
        "IMPORTS": esc(c["activity"]["imports"]),
    }
    scalars.update(states)
    return sub_tokens(frag, scalars)


# ── path + cleanup ─────────────────────────────────────────────────────────

def adjust_paths(htmltext, out_dir):
    """Rewrite the template's relative asset paths for the artifact's location."""
    ds_dir = os.path.normpath(os.path.join(HERE, "..", "..", "design-system"))
    css_file = os.path.join(HERE, "phase-assessment.css")
    ds_rel = os.path.relpath(ds_dir, out_dir).replace(os.sep, "/")
    css_rel = os.path.relpath(css_file, out_dir).replace(os.sep, "/")
    htmltext = htmltext.replace('href="../design-system', 'href="%s' % ds_rel)
    htmltext = htmltext.replace('href="./phase-assessment.css"', 'href="%s"' % css_rel)
    return htmltext


def strip_comments(htmltext):
    htmltext = re.sub(r"<!--.*?-->", "", htmltext, flags=re.DOTALL)
    htmltext = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", htmltext)
    return htmltext


# ── build ──────────────────────────────────────────────────────────────────

def build(data, out_dir=None):
    with open(TEMPLATE, encoding="utf-8") as fh:
        text = fh.read()

    clients = data["clients"]

    # per-client cards (replace the client region with all rendered cards)
    rx = _region_re("client")
    m = rx.search(text)
    if not m:
        raise ValueError("region not found: @repeat client")
    card_fragment = m.group(1)
    cards = "".join(render_client(card_fragment, c) for c in clients)
    text = text[: m.start()] + cards + text[m.end():]

    # cohort rows
    text = fill_repeat(text, "cohort-row", clients, render_cohort_row)

    # agenda buckets
    agenda = data["agenda"]
    urgent_count = sum(1 for it in agenda.get("resolve", []) if it.get("urgent"))
    if urgent_count > 1:
        raise ValueError("at most one urgent agenda item allowed (found %d)" % urgent_count)
    text = replace_region(text, "agenda-resolve", render_agenda_bucket(agenda.get("resolve", [])))
    text = replace_region(text, "agenda-discuss", render_agenda_bucket(agenda.get("discuss", [])))
    text = replace_region(text, "agenda-ontrack", render_agenda_bucket(agenda.get("on_track", [])))

    # appendix
    appx = data.get("appendix", {})
    text = fill_repeat(text, "override-note", appx.get("overrides", []),
                       lambda inner, h: sub_tokens(inner, {"OVERRIDE_NOTE_HTML": h}))
    text = fill_repeat(text, "feedback-item", appx.get("feedback", []),
                       lambda inner, h: sub_tokens(inner, {"FEEDBACK_HTML": h}))

    # report-level
    rep = data["report"]
    text = sub_tokens(text, {
        "REPORT_TITLE": esc(rep["title"]),
        "SOURCE_MD": esc(rep["source_md"]),
        "RUN_METADATA": esc(rep["run_metadata"]),
    })

    if out_dir is not None:
        text = adjust_paths(text, out_dir)
    text = strip_comments(text)

    leftover = re.findall(r"\{\{[A-Z0-9_]+\}\}", text)
    if leftover:
        raise ValueError("unresolved tokens remain: %s" % ", ".join(sorted(set(leftover))))
    return text


# ── golden check ─────────────────────────────────────────────────────────

def _body(htmltext):
    start = htmltext.index('<main class="oa-shell">')
    end = htmltext.rindex("</main>") + len("</main>")
    return htmltext[start:end]


def _normalize(htmltext):
    s = re.sub(r"<!--.*?-->", "", htmltext, flags=re.DOTALL)
    s = re.sub(r">\s+<", "><", s)
    s = re.sub(r"\s+</", "</", s)  # ignore cosmetic whitespace before a closing tag
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def check(data, example_path):
    generated = build(data, out_dir=None)
    with open(example_path, encoding="utf-8") as fh:
        example = fh.read()
    a = _normalize(_body(generated))
    b = _normalize(_body(example))
    if a == b:
        print("MATCH — generated body is identical to %s" % os.path.basename(example_path))
        return 0
    # find first divergence
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
    print("*** DIFF at char %d" % i)
    print("generated: …%s" % a[max(0, i - 60):i + 60])
    print("example  : …%s" % b[max(0, i - 60):i + 60])
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a phase-assessment HTML artifact from JSON.")
    ap.add_argument("json", help="path to the report JSON")
    ap.add_argument("--out", help="output HTML path (default: alongside the JSON, .html)")
    ap.add_argument("--check", help="compare generated body against this reference HTML (no file written)")
    args = ap.parse_args(argv)

    import json
    with open(args.json, encoding="utf-8") as fh:
        data = json.load(fh)

    if args.check:
        return check(data, args.check)

    out = args.out or os.path.splitext(args.json)[0] + ".html"
    out = os.path.abspath(out)
    text = build(data, out_dir=os.path.dirname(out))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
