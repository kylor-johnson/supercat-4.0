# report_render — Insightful 4.0 HTML render pipeline

Deterministic MD → HTML renderer for the Insightful Product 4.0 CEO Intelligence
Brief. Takes a ratified profile + a PASS3 markdown output and produces a
Sarreid-quality HTML that visually + structurally matches the gold standard
`outputs/Sarreid_CEO_intelligence_report_2026-06-29.html`.

## What this is

The Phase-3 port of the Sarreid HTML shell into a reusable template, plus a
Step-10 HTML checker that closes ledger items **4 / 8 / 9 / 11 / 12** (the
HTML-side checks deferred during the MD-only Phase 1).

## What this is NOT

- A redesign. The Sarreid HTML is the layout authority; we port it verbatim.
- A re-pull of live data. The MDs already carry the live-pulled dollars; we render them.
- A WYSIWYG / live preview. Static HTML files only.
- An MD authoring tool. Profiles + MDs are locked inputs.

## Stack

- Python 3.14
- `markdown-it-py` 4.x — MD → HTML conversion
- `Jinja2` 3.x — template assembly
- `beautifulsoup4` + `lxml` — Step-10 structural / anchor checks

## Module layout

```
report_render/
├── __init__.py
├── templates/
│   └── report.html.j2          # the verbatim Sarreid CSS + JS shell
├── md_parse.py                 # MD → ParsedReport (chunks + mode + ledger)
├── md_render.py                # markdown-it-py wrapper (GFM tables, soft-breaks)
├── sections.py                 # chunk → section-HTML transformers
├── html_renderer.py            # CLI entry: profile + MD → final HTML
├── step10_check.py             # Step-10 ledger items 4/8/9/11/12
└── README.md                   # this file
```

## CLI

Render an org's PASS3 MD to HTML:

```
.venv-renderer/bin/python -m report_render.html_renderer \
    --md      outputs/{org}_PASS3_intelligence_report_2026-06-30.md \
    --profile profiles/{org}.md \
    --out     outputs/{Org_Display}_CEO_intelligence_report_2026-06-30.html
```

Run the Step-10 ledger checks against a rendered HTML:

```
.venv-renderer/bin/python -m report_render.step10_check \
    --html outputs/{Org_Display}_CEO_intelligence_report_2026-06-30.html \
    --md   outputs/{org}_PASS3_intelligence_report_2026-06-30.md
```

## Step-10 ledger items closed by this module

Per `operators/report_operator.md` Step 10, the 13-check render-gate ledger.
This module ports the HTML-only items (4, 8, 9, 11, 12); the rest run in the
MD pipeline (1–3, 5–7, 10) or against the live DB (13).

| # | Check | Where | Notes |
|---|---|---|---|
| 4 | §P forbidden-vocabulary regex sweep (HTML) | `step10_check._check_forbidden_vocab` | Skips `#appendix`, `footer-ledger`, and the entire Mode-2 Gate-STOP document (those are explicitly internal surfaces per §P.2 / §5b) |
| 8 | Number reconciliation (HTML ↔ MD) | `step10_check._check_number_reconciliation` | Approximation: a figure appearing 2+ times in either surface must appear in the other |
| 9 | Verbatim 12-word phrase echo (HTML) | `step10_check._check_phrase_echo` | Scope is the §1/§2/§3/§5 **headers / sub-headers / callouts** per spec — body prose is NOT in the dedup target |
| 11 | HTML structure pairing + unique-id | `step10_check._check_structure` | `<details>` / `<section>` / `<table>` open/close; `id` uniqueness |
| 12 | In-document anchor resolution | `step10_check._check_anchors` | Every `<a href="#…">` resolves to an in-doc `id` |

Item **13** (topline live-query parity re-pull) is out of scope for the
HTML port — it requires a live `Q-ECON-00` re-pull and belongs in the next
Mode-1 fresh run.

## Phase 4 Task A — 2026-06-30 renderer heuristic fixes

Five `sections.py` corrections applied after structural eye-check vs the Sarreid gold:

1. `_enrich_title` applied consistently to all section h2 headings (` — ` → ` · `).
2. `_enrich_title` applied to h3 subsection titles in `_render_subsection_section`
   and `render_team`.
3. `_BOLD_SECTION_LEAD` soft-boundary feature: `**Bold text:** ` standalone paragraphs
   in the no-H3 branch create `<h3 class="subsection-title">` elements (restores
   "eCat as a channel" in `#channels`).
4. Bold-colon → h3 in `_render_methodology_body` (restores "Two specific upgrades
   worth queuing" in `#methodology`).
5. `render_methodology` gaps h3 uses `_split_heading_prefix` — prefix-only (restores
   "What this report can't see" without the ` — and what to add next` suffix).

Step-10 ledger results unchanged after re-render.

## Phase 3 — 2026-06-30 ledger results

Rendered against the four cohort MDs + the Sarreid canary:

| Output | Mode | [4] §P | [8] # recon | [9] phrase echo | [11] struct | [12] anchors |
|---|---|---|---|---|---|---|
| Sarreid (regenerated canary) | 1 | **2 inherited** | pass | pass | pass | pass |
| Currey & Company (`cci`) | 1 | **pass** | pass | pass | pass | pass |
| Hubbardton Forge (`hfg`) | 1 | **pass** | pass | pass | pass | pass |
| Kalco Lighting (`kal`) | 1 | **1 inherited** | pass | pass | pass | pass |
| Shadow Catchers (`sca`) | 2 (Gate-STOP) | n/a (relaxed) | pass | pass | pass | pass |

### Inherited §P violations (NOT renderer defects)

These are real §P leaks in the source MDs (which are immutable per the Phase 3
contract). The checker is correctly surfacing them — fixing requires an edit at
the MD-authoring stage, not in this module.

- **Sarreid MD (pre-§P canary, 2026-06-29):**
  - `this run` × 2 in §6 Team (`…stands out as a discount problem this run.`)
  - `single-feed posture` × 2 in §11 Methodology (substitute per §P.1.C:
    *"one feed of your business"*)
- **kal MD (2026-06-30, post-§P but mis-graded):**
  - `cohort` × 1 in §9 Dealer base (`…first-timer cohort returned at 25.4%…`).
    Per §P.1.A `cohort` in a retention context is banned; the substitute is
    *"first-timer group"* or *"first-timer base"*.

## Determinism

Same MD + same profile + same renderer commit → byte-identical HTML. The
template is verbatim Sarreid (CSS + JS); the only sources of variance are:

1. Inputs (MD + profile + template).
2. Section-mapping heuristics in `sections.py` (which are pure functions of
   the MD source — no clock, no entropy).

If a re-run produces a different HTML, one of the inputs changed or a
heuristic was updated; both should land in `CHANGELOG.md`.
