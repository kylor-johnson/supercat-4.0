#!/usr/bin/env python3
"""Health V3 consistency checker.

Verifies cross-file invariants identified by the V3.2.x audit arc.
Returns exit 0 if all pass, exit 1 if any fail. Stdlib only.

Run from anywhere; the script locates the ``Health V3/`` root from
``__file__`` and resolves every path relative to it.
"""
from __future__ import annotations

import ast
import hashlib
import re
import sys
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Patterns used by Invariant 4 (stale column-name references). Defined at
# module scope so the substring "support_fire_note" / "score_date" /
# "health_score" only appears inside regex literals, which are exempted from
# the scan by skipping the script file itself.
# ---------------------------------------------------------------------------
_STALE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("health_score", re.compile(r"\b" + "health_score" + r"\b")),
    ('"score_date"', re.compile(r'"' + "score_date" + r'"')),
    ("support_fire_note", re.compile(r"\b" + "support_fire_note" + r"\b")),
)

# Paths skipped entirely by Invariant 4. Directory names are matched against
# any parent component; filenames are matched against the path relative to
# the Health V3 root.
_INVARIANT_4_SKIP_DIRS = {"_archive", "cache", "runs", ".venv", "__pycache__"}
_INVARIANT_4_SKIP_FILES = {"outcomes.csv", "CHANGELOG.md", "check_consistency.py"}


class Result(NamedTuple):
    passed: bool
    name: str
    detail: str = ""
    note: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_root() -> Path:
    """Locate the ``Health V3/`` root by walking up from this file."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if parent.name == "Health V3":
            return parent
    raise SystemExit(
        "ERROR: could not locate 'Health V3/' root from script location "
        f"({here})"
    )


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_operator(root: Path) -> ast.Module:
    src = _read_text(root / "health_operator_v3.py")
    return ast.parse(src, filename="health_operator_v3.py")


def _find_main_function(tree: ast.Module) -> ast.FunctionDef | None:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node
    return None


def _latest_run_dir(root: Path) -> Path | None:
    runs = root / "runs"
    if not runs.is_dir():
        return None
    # Only YYYY-MM-DD directories are canonical runs. runs/ also holds
    # historical/, cohort/, cohort_v330/, _weighting_study/ and
    # _engine_baseline_v3.2.13/ — a plain name sort picked "historical" as the
    # newest run and failed four invariants against a file that never existed.
    candidates = sorted(
        (p for p in runs.iterdir()
         if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)),
        key=lambda p: p.name,
    )
    return candidates[-1] if candidates else None


def _latest_dashboard(root: Path) -> Path | None:
    dashboards = root / "dashboards"
    if not dashboards.is_dir():
        return None
    candidates = sorted(
        dashboards.glob("health_dashboard_*.html"),
        key=lambda p: p.name,
    )
    return candidates[-1] if candidates else None


def _version_tuple(s: str) -> tuple[int, int, int] | None:
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", s)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def _all_changelog_versions(text: str) -> list[str]:
    return re.findall(r"^##\s+(\d+\.\d+\.\d+)\s+—", text, re.MULTILINE)


# ---------------------------------------------------------------------------
# Invariant 1 — Version coherence
# ---------------------------------------------------------------------------

def check_version_coherence(root: Path) -> Result:
    name = "Invariant 1 — Version coherence (README, METHODOLOGY, CHANGELOG)"
    try:
        readme = _read_text(root / "README.md")
        methodology = _read_text(root / "METHODOLOGY.md")
        changelog = _read_text(root / "CHANGELOG.md")
    except OSError as exc:
        return Result(False, name, detail=f"Could not read source file: {exc}")

    rx_inline = re.compile(r"\*\*Version:\*\*\s+(\d+\.\d+\.\d+)")
    rx_heading = re.compile(r"^##\s+(\d+\.\d+\.\d+)\s+—", re.MULTILINE)

    m_readme = rx_inline.search(readme)
    m_method = rx_inline.search(methodology)
    m_change = rx_heading.search(changelog)

    if not m_readme:
        return Result(False, name, detail="README.md: no '**Version:** X.Y.Z' line found.")
    if not m_method:
        return Result(False, name, detail="METHODOLOGY.md: no '**Version:** X.Y.Z' line found.")
    if not m_change:
        return Result(False, name, detail="CHANGELOG.md: no '## X.Y.Z — ' heading found.")

    v_readme = m_readme.group(1)
    v_method = m_method.group(1)
    v_change = m_change.group(1)

    if v_readme == v_method == v_change:
        return Result(True, name)

    lines = [
        f"README.md       version: {v_readme}",
        f"METHODOLOGY.md  version: {v_method}",
        f"CHANGELOG.md    version: {v_change} (top entry)",
    ]
    counts: dict[str, list[str]] = {}
    for label, val in [("README", v_readme), ("METHODOLOGY", v_method), ("CHANGELOG", v_change)]:
        counts.setdefault(val, []).append(label)
    odd = [v for v, files in counts.items() if len(files) == 1]
    if odd:
        lines.append(f"Disagreeing file(s): {', '.join(counts[odd[0]])} (version {odd[0]}).")
    else:
        lines.append("All three versions disagree with each other.")
    return Result(False, name, detail="\n".join(lines))


# ---------------------------------------------------------------------------
# Invariant 2 — Live canonical SHA appears in top CHANGELOG entry
# ---------------------------------------------------------------------------

def check_changelog_sha(root: Path) -> Result:
    name = "Invariant 2 — Live canonical SHA recorded in top CHANGELOG entry"

    latest_run = _latest_run_dir(root)
    if latest_run is None:
        return Result(False, name, detail="No run directory under runs/ found.")

    date = latest_run.name
    canonical_csv = latest_run / f"client_health_scores_{date}.csv"
    if not canonical_csv.is_file():
        return Result(
            False,
            name,
            detail=f"Expected canonical CSV not found: {canonical_csv.relative_to(root)}",
        )

    try:
        live_sha = hashlib.sha256(canonical_csv.read_bytes()).hexdigest()
    except OSError as exc:
        return Result(False, name, detail=f"Could not read canonical CSV: {exc}")

    try:
        changelog = _read_text(root / "CHANGELOG.md")
    except OSError as exc:
        return Result(False, name, detail=f"Could not read CHANGELOG.md: {exc}")

    headings = list(re.finditer(r"^##\s+\d+\.\d+\.\d+\s+—", changelog, re.MULTILINE))
    if not headings:
        return Result(False, name, detail="CHANGELOG.md: no '## X.Y.Z — ' heading found.")

    start = headings[0].start()
    end = headings[1].start() if len(headings) > 1 else len(changelog)
    top_entry = changelog[start:end]

    if live_sha in top_entry:
        return Result(True, name)

    detail = (
        f"Live canonical SHA: {live_sha}\n"
        f"Source: {canonical_csv.relative_to(root)}\n"
        "Hint: the top CHANGELOG entry must record this SHA verbatim "
        "(e.g., 'Canonical SHA unchanged: <sha>' or 'New canonical SHA: <sha>')."
    )
    return Result(False, name, detail=detail)


# ---------------------------------------------------------------------------
# Invariant 3 — Canonical CSV header matches operator row dict
# ---------------------------------------------------------------------------

def _find_rows_append_dict(tree: ast.Module) -> ast.Dict | str:
    """Return the dict literal passed to ``rows.append(...)`` inside ``main()``.

    Returns a string error message instead of raising on structural problems.
    """
    main_fn = _find_main_function(tree)
    if main_fn is None:
        return "Could not find def main() in health_operator_v3.py."

    for node in ast.walk(main_fn):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (
            isinstance(func, ast.Attribute)
            and func.attr == "append"
            and isinstance(func.value, ast.Name)
            and func.value.id == "rows"
        ):
            continue
        if not node.args:
            return f"rows.append() at line {node.lineno} has no positional args."
        arg = node.args[0]
        if not isinstance(arg, ast.Dict):
            return (
                f"rows.append() at line {node.lineno} is not called with a dict literal "
                f"(got {type(arg).__name__})."
            )
        return arg
    return "No rows.append(...) call found inside def main()."


def _dict_keys_in_order(d: ast.Dict) -> list[str] | str:
    keys: list[str] = []
    for k in d.keys:
        if not isinstance(k, ast.Constant) or not isinstance(k.value, str):
            line = getattr(k, "lineno", "?")
            return f"Non-string-literal key in rows.append() dict at line {line}."
        keys.append(k.value)
    return keys


def check_canonical_header(root: Path) -> Result:
    name = "Invariant 3 — Canonical CSV header matches operator row-dict keys"

    latest_run = _latest_run_dir(root)
    if latest_run is None:
        return Result(False, name, detail="No run directory under runs/ found.")
    date = latest_run.name
    canonical_csv = latest_run / f"client_health_scores_{date}.csv"
    if not canonical_csv.is_file():
        return Result(False, name, detail=f"Canonical CSV missing: {canonical_csv.relative_to(root)}")

    try:
        first_line = canonical_csv.read_text(encoding="utf-8").splitlines()[0]
    except OSError as exc:
        return Result(False, name, detail=f"Could not read canonical CSV: {exc}")
    csv_header = [c.strip() for c in first_line.split(",")]

    try:
        tree = _parse_operator(root)
    except (OSError, SyntaxError) as exc:
        return Result(False, name, detail=f"Could not parse operator: {exc}")

    found = _find_rows_append_dict(tree)
    if isinstance(found, str):
        return Result(False, name, detail=found)
    keys = _dict_keys_in_order(found)
    if isinstance(keys, str):
        return Result(False, name, detail=keys)

    if csv_header == keys:
        return Result(True, name)

    csv_set = set(csv_header)
    op_set = set(keys)
    extra_csv = [c for c in csv_header if c not in op_set]
    missing_csv = [c for c in keys if c not in csv_set]
    lines = [
        f"CSV header   ({len(csv_header)} cols): {csv_header}",
        f"Operator keys ({len(keys)} cols): {keys}",
    ]
    if extra_csv:
        lines.append(f"In CSV but not operator: {extra_csv}")
    if missing_csv:
        lines.append(f"In operator but not CSV: {missing_csv}")
    if not extra_csv and not missing_csv:
        # Same set, different order
        order_diff = [
            f"position {i}: CSV={csv_header[i]!r} vs operator={keys[i]!r}"
            for i in range(min(len(csv_header), len(keys)))
            if csv_header[i] != keys[i]
        ]
        lines.append("Same columns but order differs:")
        lines.extend(order_diff[:5])
        if len(order_diff) > 5:
            lines.append(f"... and {len(order_diff) - 5} more order mismatches")
    return Result(False, name, detail="\n".join(lines))


# ---------------------------------------------------------------------------
# Invariant 4 — No stale column-name references
# ---------------------------------------------------------------------------

def _iter_in_scope_files(root: Path):
    """Yield (path, relpath) for every text file in scope for Invariant 4."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        parts = rel.parts
        if any(part in _INVARIANT_4_SKIP_DIRS for part in parts):
            continue
        if rel.name in _INVARIANT_4_SKIP_FILES:
            continue
        # Skip plainly binary files (e.g. .DS_Store). Detect by trying a
        # UTF-8 decode at read time below; here we cheaply filter very common
        # binary extensions and dotfiles.
        if rel.name.startswith("."):
            continue
        yield path, rel


def check_no_stale_names(root: Path) -> Result:
    name = "Invariant 4 — No stale column-name references in source-of-truth files"

    hits: list[str] = []
    for path, rel in _iter_in_scope_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for label, rx in _STALE_PATTERNS:
                if rx.search(line):
                    snippet = line.strip()
                    if len(snippet) > 200:
                        snippet = snippet[:197] + "..."
                    hits.append(
                        f"{rel}:{lineno} [{label}] {snippet}"
                    )

    if not hits:
        return Result(True, name)
    detail_lines = [f"Found {len(hits)} stale-name reference(s):"]
    detail_lines.extend(hits[:20])
    if len(hits) > 20:
        detail_lines.append(f"... and {len(hits) - 20} more")
    return Result(False, name, detail="\n".join(detail_lines))


# ---------------------------------------------------------------------------
# Invariant 5 — Dashboard footer agreement
# ---------------------------------------------------------------------------

_DASHBOARD_FOOTER_RX = re.compile(
    r"Health V(\d+\.\d+\.\d+) · Generated from <code>[^<]+</code> "
    r"\(SHA-256: ([0-9a-f]{8})…\)"
)


def check_dashboard_footer(root: Path) -> Result:
    name = "Invariant 5 — Dashboard footer SHA matches live canonical (version label may lag)"

    dashboard = _latest_dashboard(root)
    if dashboard is None:
        return Result(False, name, detail="No dashboards/health_dashboard_*.html file found.")

    try:
        html = _read_text(dashboard)
    except OSError as exc:
        return Result(False, name, detail=f"Could not read dashboard: {exc}")

    matches = _DASHBOARD_FOOTER_RX.findall(html)
    if not matches:
        return Result(
            False,
            name,
            detail=(
                f"Dashboard {dashboard.relative_to(root)} has no "
                "'Health V<ver> · Generated from <code>...</code> "
                "(SHA-256: <prefix>…)' line matching the footer template."
            ),
        )

    versions = {m[0] for m in matches}
    sha_prefixes = {m[1] for m in matches}
    if len(matches) > 1 and (len(versions) > 1 or len(sha_prefixes) > 1):
        return Result(
            False,
            name,
            detail=(
                f"Dashboard {dashboard.relative_to(root)} has {len(matches)} footer "
                f"matches that disagree internally. Versions seen: {sorted(versions)}; "
                f"SHA prefixes seen: {sorted(sha_prefixes)}."
            ),
        )

    dash_version = next(iter(versions))
    dash_sha_prefix = next(iter(sha_prefixes))

    # 5a — SHA prefix must match live canonical
    latest_run = _latest_run_dir(root)
    if latest_run is None:
        return Result(False, name, detail="No run directory under runs/ found (needed for SHA check).")
    date = latest_run.name
    canonical_csv = latest_run / f"client_health_scores_{date}.csv"
    if not canonical_csv.is_file():
        return Result(False, name, detail=f"Canonical CSV missing: {canonical_csv.relative_to(root)}")
    live_sha = hashlib.sha256(canonical_csv.read_bytes()).hexdigest()
    live_prefix = live_sha[:8]

    if dash_sha_prefix != live_prefix:
        return Result(
            False,
            name,
            detail=(
                f"Dashboard SHA prefix: {dash_sha_prefix}…\n"
                f"Live canonical SHA prefix: {live_prefix}…\n"
                f"Live canonical SHA: {live_sha}\n"
                "Dashboard is showing stale data — regenerate against the current canonical."
            ),
        )

    # 5b — Dashboard version must appear in CHANGELOG history
    try:
        changelog = _read_text(root / "CHANGELOG.md")
    except OSError as exc:
        return Result(False, name, detail=f"Could not read CHANGELOG.md: {exc}")
    known_versions = _all_changelog_versions(changelog)
    if dash_version not in known_versions:
        return Result(
            False,
            name,
            detail=(
                f"Dashboard version V{dash_version} does not appear as any "
                f"'## X.Y.Z — ' heading in CHANGELOG.md. Known versions: "
                f"{', '.join(known_versions[:10])}"
                + (f", ... ({len(known_versions)} total)" if len(known_versions) > 10 else "")
            ),
        )

    # Optional informational [NOTE]: dashboard lags current top version
    note = ""
    top_version = known_versions[0]
    dash_tup = _version_tuple(dash_version)
    top_tup = _version_tuple(top_version)
    if dash_tup and top_tup and dash_tup < top_tup:
        note = (
            f"Dashboard footer is V{dash_version} while current system is "
            f"V{top_version}; expected if intervening patches were SHA-neutral. "
            "Regenerate to refresh the label if desired."
        )

    return Result(True, name, note=note)


# ---------------------------------------------------------------------------
# Invariant 6 — Formatted CSV header matches `_fmt_cols`
# ---------------------------------------------------------------------------

def _find_fmt_cols(tree: ast.Module) -> list[str] | str:
    main_fn = _find_main_function(tree)
    if main_fn is None:
        return "Could not find def main() in health_operator_v3.py."
    for node in ast.walk(main_fn):
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue
        tgt = node.targets[0]
        if not (isinstance(tgt, ast.Name) and tgt.id == "_fmt_cols"):
            continue
        if not isinstance(node.value, ast.List):
            return (
                f"_fmt_cols assignment at line {node.lineno} is not a list literal "
                f"(got {type(node.value).__name__})."
            )
        cols: list[str] = []
        for elt in node.value.elts:
            if not isinstance(elt, ast.Constant) or not isinstance(elt.value, str):
                line = getattr(elt, "lineno", "?")
                return f"_fmt_cols list element at line {line} is not a string literal."
            cols.append(elt.value)
        return cols
    return "No `_fmt_cols = [...]` assignment found inside def main()."


def check_formatted_header(root: Path) -> Result:
    name = "Invariant 6 — Formatted CSV header matches operator `_fmt_cols`"

    latest_run = _latest_run_dir(root)
    if latest_run is None:
        return Result(False, name, detail="No run directory under runs/ found.")
    date = latest_run.name
    fmt_csv = latest_run / f"client_health_scores_{date}_formatted.csv"
    if not fmt_csv.is_file():
        return Result(False, name, detail=f"Formatted CSV missing: {fmt_csv.relative_to(root)}")

    try:
        first_line = fmt_csv.read_text(encoding="utf-8").splitlines()[0]
    except OSError as exc:
        return Result(False, name, detail=f"Could not read formatted CSV: {exc}")
    csv_header = [c.strip() for c in first_line.split(",")]

    try:
        tree = _parse_operator(root)
    except (OSError, SyntaxError) as exc:
        return Result(False, name, detail=f"Could not parse operator: {exc}")

    fmt_cols = _find_fmt_cols(tree)
    if isinstance(fmt_cols, str):
        return Result(False, name, detail=fmt_cols)

    if csv_header == fmt_cols:
        return Result(True, name)

    csv_set = set(csv_header)
    op_set = set(fmt_cols)
    extra = [c for c in csv_header if c not in op_set]
    missing = [c for c in fmt_cols if c not in csv_set]
    lines = [
        f"Formatted CSV header ({len(csv_header)} cols): {csv_header}",
        f"_fmt_cols            ({len(fmt_cols)} cols): {fmt_cols}",
    ]
    if extra:
        lines.append(f"In CSV but not _fmt_cols: {extra}")
    if missing:
        lines.append(f"In _fmt_cols but not CSV: {missing}")
    if not extra and not missing:
        order_diff = [
            f"position {i}: CSV={csv_header[i]!r} vs _fmt_cols={fmt_cols[i]!r}"
            for i in range(min(len(csv_header), len(fmt_cols)))
            if csv_header[i] != fmt_cols[i]
        ]
        lines.append("Same columns but order differs:")
        lines.extend(order_diff[:5])
    return Result(False, name, detail="\n".join(lines))


# ---------------------------------------------------------------------------
# Invariant 7 — `--score-date` is `required=True` in argparse
# ---------------------------------------------------------------------------

def check_score_date_required(root: Path) -> Result:
    name = "Invariant 7 — `--score-date` is `required=True` (no default) in argparse"

    try:
        tree = _parse_operator(root)
    except (OSError, SyntaxError) as exc:
        return Result(False, name, detail=f"Could not parse operator: {exc}")

    matches: list[ast.Call] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add_argument"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if (
            isinstance(first, ast.Constant)
            and isinstance(first.value, str)
            and first.value == "--score-date"
        ):
            matches.append(node)

    if len(matches) == 0:
        return Result(False, name, detail="No add_argument('--score-date', ...) call found.")
    if len(matches) > 1:
        lines_found = ", ".join(str(m.lineno) for m in matches)
        return Result(
            False,
            name,
            detail=f"Found {len(matches)} add_argument('--score-date', ...) calls (lines {lines_found}); expected exactly one.",
        )

    call = matches[0]
    kwargs = {kw.arg: kw.value for kw in call.keywords if kw.arg is not None}

    has_default = "default" in kwargs
    required_val = kwargs.get("required")
    required_is_true = (
        isinstance(required_val, ast.Constant) and required_val.value is True
    )

    if required_is_true and not has_default:
        return Result(True, name)

    def _kw_to_str(kw: ast.keyword) -> str:
        try:
            return f"{kw.arg}={ast.unparse(kw.value)}"
        except Exception:
            return f"{kw.arg}=<unparseable>"

    kw_strs = [_kw_to_str(kw) for kw in call.keywords]
    issues = []
    if not required_is_true:
        issues.append("missing or non-literal `required=True`")
    if has_default:
        issues.append("forbidden `default=` kwarg present")
    detail = (
        f"add_argument('--score-date', ...) at line {call.lineno}: "
        f"{'; '.join(issues)}.\n"
        f"Current kwargs: {kw_strs}"
    )
    return Result(False, name, detail=detail)


# ---------------------------------------------------------------------------
# Invariant 8 — Floor sub-shape names appear in both operator and README
# ---------------------------------------------------------------------------

_FLOOR_SUBSHAPES: tuple[tuple[str, str], ...] = (
    ("critically_low", "Critically low"),
    ("full_adoption_dark", "Full adoption, users dark"),
    ("clean_ops_dark", "Clean infrastructure, users dark"),
)


def check_floor_subshapes(root: Path) -> Result:
    name = "Invariant 8 — Floor sub-shape names present in operator and README"

    try:
        tree = _parse_operator(root)
    except (OSError, SyntaxError) as exc:
        return Result(False, name, detail=f"Could not parse operator: {exc}")
    main_fn = _find_main_function(tree)
    if main_fn is None:
        return Result(False, name, detail="Could not find def main() in operator.")

    assigned_names: set[str] = set()
    for node in ast.walk(main_fn):
        if not isinstance(node, ast.Assign):
            continue
        for tgt in node.targets:
            if isinstance(tgt, ast.Name):
                assigned_names.add(tgt.id)

    try:
        readme = _read_text(root / "README.md")
    except OSError as exc:
        return Result(False, name, detail=f"Could not read README.md: {exc}")

    missing: list[str] = []
    for ident, phrase in _FLOOR_SUBSHAPES:
        if ident not in assigned_names:
            missing.append(f"operator main(): no assignment to `{ident}`")
        if phrase not in readme:
            missing.append(f"README.md: phrase {phrase!r} not found")

    if not missing:
        return Result(True, name)
    return Result(False, name, detail="\n".join(missing))


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main() -> int:
    root = find_root()
    checks = [
        check_version_coherence,
        check_changelog_sha,
        check_canonical_header,
        check_no_stale_names,
        check_dashboard_footer,
        check_formatted_header,
        check_score_date_required,
        check_floor_subshapes,
    ]
    print("Health V3 Consistency Check")
    print("=" * 30)
    print()

    results = [c(root) for c in checks]
    for r in results:
        marker = "[PASS]" if r.passed else "[FAIL]"
        print(f"{marker} {r.name}")
        if not r.passed and r.detail:
            for line in r.detail.splitlines():
                print(f"       {line}")
        if r.note:
            for line in r.note.splitlines():
                print(f"       [NOTE] {line}")

    n_pass = sum(1 for r in results if r.passed)
    n_fail = len(results) - n_pass
    print()
    print(f"Summary: {n_pass} pass, {n_fail} fail")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
