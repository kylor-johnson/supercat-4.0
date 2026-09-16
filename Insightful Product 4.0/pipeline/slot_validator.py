"""Per-slot LLM output validation — number-parity + voice/industry lint.

The governing principle: the LLM expresses; it never selects or computes.
Any figure in the output that cannot be traced back to the slot's fact bundle
(facts UNION derived_facts) triggers an immediate REJECT, and the slot falls
back to deterministic template prose.

Two gates, both BLOCKING:
  1. check_number_parity — extract every dollar/percent/count from output,
     verify each traces to a value in the bundle (with rounding tolerance)
  2. check_voice_lint — forbidden vocabulary, cute labels, machinery-inside-
     a-finding, invented causation, un-rounded dollars, concentration/
     seasonality-as-finding
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any

# ─── Import forbidden-vocabulary patterns from step10_check ─────────────────
# The import can fail when running outside the full repo tree (e.g. CI on this
# file alone). Fall back to an empty list so the module stays importable.
try:
    from report_render.step10_check import _FORBIDDEN_COMPILED
except ImportError:
    _FORBIDDEN_COMPILED: list[tuple[re.Pattern, str]] = []  # type: ignore[no-redef]

# ─── Compiled regex patterns (module-level for performance) ─────────────────

# Dollar amounts: $1,234  $1.55M  $90K  $2,828,719
_RE_DOLLAR = re.compile(
    r"\$[\d,]+(?:\.\d+)?\s?[KMBkmb]?\b"
)

# Percentages: +79%  -3.2%  12%  79.0%
_RE_PERCENT = re.compile(
    r"[+\-−–]?\d{1,5}(?:\.\d+)?\s?%"
)

# Count-nouns: "304 doors", "1,200 dealers", "52 reps"
_RE_COUNT = re.compile(
    r"\b(\d{1,6}(?:,\d{3})*)\s+"
    r"(doors?|dealers?|reps?|accounts?|customers?|SKUs?|stores?|items?|"
    r"products?|locations?|orders?|invoices?|shipments?|days?|weeks?|months?)\b",
    re.IGNORECASE,
)

# Cute labels
_RE_CUTE = re.compile(
    r"\b(franchise|flywheel|treadmill|playbook|north\s*star)\b",
    re.IGNORECASE,
)

# Machinery-inside-a-finding (not in provenance/methodology context)
_RE_MACHINERY = re.compile(
    r"\b(system|platform|dashboard|pipeline|feed|posture|renderer)\b",
    re.IGNORECASE,
)
_RE_METHODOLOGY_CTX = re.compile(
    r"\b(methodology|provenance|appendix|source|data\s+note)\b",
    re.IGNORECASE,
)

# Causal connectors
_RE_CAUSAL = re.compile(
    r"\b(because|due\s+to|driven\s+by|caused\s+by|as\s+a\s+result\s+of|"
    r"attributed\s+to|stems?\s+from|a\s+function\s+of)\b",
    re.IGNORECASE,
)

# Un-rounded customer-facing dollars: exact-to-the-dollar amounts > $100K
# without K/M suffix and with more than 3 sig digits after leading digit.
_RE_UNROUNDED_DOLLAR = re.compile(
    r"\$(\d{1,3}(?:,\d{3})+)(?![\d,.])\s*(?![KMBkmb])"
)

# Concentration-as-finding
_RE_CONCENTRATION = re.compile(
    r"\bHHI\b|top\s.*?customer\s.*?holds?\s.*?%",
    re.IGNORECASE,
)

# Seasonality-as-finding: Q1 and Q2 in same sentence with decline language
_RE_QUARTER = re.compile(r"\bQ[1-4]\b")
_RE_DECLINE = re.compile(
    r"\b(dropped|fell|declined|softened)\b",
    re.IGNORECASE,
)
_RE_SAME_PERIOD = re.compile(
    r"vs\.?\s+same\s+period|same\s+period\s+last",
    re.IGNORECASE,
)

# Dollar range pattern: "$90K-$160K"
_RE_DOLLAR_RANGE = re.compile(
    r"\$[\d,]+(?:\.\d+)?\s?[KMBkmb]?\s*[-–—]\s*\$[\d,]+(?:\.\d+)?\s?[KMBkmb]?"
)

# Scale suffixes
_SCALE = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}


# ─── Helpers ────────────────────────────────────────────────────────────────

def _parse_dollar(raw: str) -> float:
    """Parse a dollar string like '$1,553,412', '$1.55M', '$90K' to float."""
    s = raw.replace("$", "").replace(",", "").strip()
    suffix = s[-1].lower() if s and s[-1].lower() in _SCALE else ""
    if suffix:
        s = s[:-1]
    try:
        val = float(s)
    except ValueError:
        return float("nan")
    if suffix:
        val *= _SCALE[suffix]
    return val


def _extract_numbers(text: str) -> list[tuple[str, float, str]]:
    """Extract all numeric figures from *text*.

    Returns list of (original_text, numeric_value, type) where type is one of
    ``"dollar"``, ``"percent"``, or ``"count"``.
    """
    results: list[tuple[str, float, str]] = []

    for m in _RE_DOLLAR.finditer(text):
        raw = m.group(0)
        results.append((raw, _parse_dollar(raw), "dollar"))

    for m in _RE_PERCENT.finditer(text):
        raw = m.group(0)
        s = raw.replace("%", "").replace(",", "").replace("\u2212", "-").replace("\u2013", "-").replace("\u2014", "-").strip()
        try:
            results.append((raw, float(s), "percent"))
        except ValueError:
            pass

    for m in _RE_COUNT.finditer(text):
        raw = m.group(0)
        num_str = m.group(1).replace(",", "")
        try:
            results.append((raw, float(num_str), "count"))
        except ValueError:
            pass

    return results


def _bundle_values(fact_bundle: dict[str, Any]) -> set[float]:
    """Recursively flatten every numeric value from *fact_bundle*."""
    vals: set[float] = set()

    def _walk(obj: Any) -> None:
        if isinstance(obj, (int, float)):
            vals.add(float(obj))
        elif isinstance(obj, str):
            # Try parsing numeric strings (e.g. "$1.29", "79.3")
            cleaned = obj.replace("$", "").replace(",", "").replace("%", "").strip()
            # Handle K/M/B suffix
            suffix = cleaned[-1].lower() if cleaned and cleaned[-1].lower() in _SCALE else ""
            num_part = cleaned[:-1] if suffix else cleaned
            try:
                v = float(num_part)
                if suffix:
                    v *= _SCALE[suffix]
                vals.add(v)
            except ValueError:
                pass
        elif isinstance(obj, dict):
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                _walk(v)

    for key in ("facts", "derived_facts"):
        if key in fact_bundle:
            _walk(fact_bundle[key])

    return vals


def _traces(value: float, allowed: set[float], tolerance: float = 0.5) -> bool:
    """Return True if *value* traces to any member of *allowed*.

    Tracing rules:
    - Exact match within *tolerance*
    - Standard rounding: an allowed value of 1_553_412 traces to 1_550_000
      (``$1.55M``) or 1_600_000 (``$1.6M``) or 1_553_000 (``$1,553K``)
    """
    if not allowed:
        return False

    for a in allowed:
        # Direct match within tolerance
        if abs(value - a) <= tolerance:
            return True
        # Check if value is a rounded representation of a
        if a != 0:
            ratio = value / a if a != 0 else float("inf")
            if 0.995 <= ratio <= 1.005:
                return True
        # Standard rounding: value could be a K/M/B rounded form of a
        # e.g. a=1_553_412, value=1_550_000 ($1.55M) or value=1_600_000 ($1.6M)
        for scale in (1_000, 1_000_000, 1_000_000_000):
            if scale > 1:
                rounded = round(a / scale, 2) * scale
                if abs(value - rounded) <= tolerance:
                    return True
                rounded_1 = round(a / scale, 1) * scale
                if abs(value - rounded_1) <= tolerance:
                    return True
                rounded_0 = round(a / scale, 0) * scale
                if abs(value - rounded_0) <= tolerance:
                    return True

    return False


# ─── Gate 1: Number parity ──────────────────────────────────────────────────

def check_number_parity(output: str, fact_bundle: dict[str, Any]) -> list[str]:
    """Extract every dollar/percent/count from *output* and verify each traces
    to a value in *fact_bundle*.

    Returns a list of untraced figures (empty list = PASS).
    """
    figures = _extract_numbers(output)
    allowed = _bundle_values(fact_bundle)
    untraced: list[str] = []

    # Also check range endpoints
    for m in _RE_DOLLAR_RANGE.finditer(output):
        range_text = m.group(0)
        parts = re.split(r"\s*[-–—]\s*", range_text)
        for part in parts:
            val = _parse_dollar(part)
            if val == val and not _traces(val, allowed):
                untraced.append(f"range endpoint {part!r} not in fact bundle")

    for original, value, fig_type in figures:
        # Skip NaN from failed parses
        if value != value:
            continue
        if not _traces(value, allowed):
            untraced.append(
                f"{fig_type} {original!r} (={value:,.2f}) not in fact bundle"
            )

    return untraced


# ─── Gate 2: Voice / industry lint ──────────────────────────────────────────

def _fact_bundle_tokens(fact_bundle: dict[str, Any]) -> set[str]:
    """Build a set of lowercased tokens from all keys and string values in the
    fact bundle, used for invented-causation checking."""
    tokens: set[str] = set()

    def _walk(obj: Any) -> None:
        if isinstance(obj, str):
            tokens.update(re.findall(r"[a-z]+", obj.lower()))
        elif isinstance(obj, dict):
            for k, v in obj.items():
                tokens.update(re.findall(r"[a-z]+", k.lower()))
                _walk(v)
        elif isinstance(obj, (list, tuple)):
            for v in obj:
                _walk(v)

    _walk(fact_bundle)
    return tokens


def check_voice_lint(output: str, fact_bundle: dict[str, Any]) -> list[str]:
    """Voice and industry lint gate.

    Returns list of violation descriptions (empty = PASS).
    """
    violations: list[str] = []

    # 1. Forbidden vocabulary (from step10_check)
    for pattern, ctx in _FORBIDDEN_COMPILED:
        if pattern.search(output):
            violations.append(
                f"forbidden vocabulary: {pattern.pattern!r} ({ctx})"
            )

    # 2. Cute labels
    for m in _RE_CUTE.finditer(output):
        violations.append(f"cute label: {m.group(0)!r}")

    # 3. Machinery-inside-a-finding
    for m in _RE_MACHINERY.finditer(output):
        start = max(0, m.start() - 80)
        end = min(len(output), m.end() + 80)
        window = output[start:end]
        if not _RE_METHODOLOGY_CTX.search(window):
            violations.append(
                f"machinery term in finding: {m.group(0)!r}"
            )

    # 4. Invented causation — causal connector followed by text not grounded
    #    in the fact bundle
    bundle_tokens = _fact_bundle_tokens(fact_bundle)
    for m in _RE_CAUSAL.finditer(output):
        after_start = m.end()
        after_end = min(len(output), after_start + 50)
        window_after = output[after_start:after_end]
        window_tokens = set(re.findall(r"[a-z]+", window_after.lower()))
        if not window_tokens & bundle_tokens:
            violations.append(
                f"invented causation: {m.group(0)!r} followed by "
                f"ungrounded text: {window_after.strip()!r}"
            )

    # 5. Un-rounded customer-facing dollars (>$100K, exact to dollar)
    for m in _RE_UNROUNDED_DOLLAR.finditer(output):
        raw_digits = m.group(1).replace(",", "")
        value = int(raw_digits)
        if value >= 100_000:
            sig_digits = len(raw_digits.lstrip("0") or "0")
            if sig_digits > 3:
                violations.append(
                    f"un-rounded dollar: ${m.group(1)} "
                    f"(>{3} significant digits, should use K/M)"
                )

    # 6. Concentration-as-finding
    if _RE_CONCENTRATION.search(output):
        has_qualifier = fact_bundle.get("has_second_qualifying_fact", False)
        if not has_qualifier:
            # Also check nested in facts/derived_facts
            for key in ("facts", "derived_facts"):
                sub = fact_bundle.get(key, {})
                if isinstance(sub, dict) and sub.get("has_second_qualifying_fact"):
                    has_qualifier = True
                    break
        if not has_qualifier:
            violations.append(
                "concentration-as-finding without second qualifying fact"
            )

    # 7. Seasonality-as-finding
    sentences = re.split(r"[.!?]+", output)
    for sentence in sentences:
        quarters = _RE_QUARTER.findall(sentence)
        if len(set(quarters)) >= 2 and _RE_DECLINE.search(sentence):
            if not _RE_SAME_PERIOD.search(sentence):
                violations.append(
                    f"seasonality-as-finding: quarterly decline without "
                    f"'vs same period' qualifier"
                )

    return violations


# ─── Gate 3: Structure ──────────────────────────────────────────────────────

def check_structure(
    output: str, slot_name: str, expected_count: int = 0
) -> list[str]:
    """Validate structural expectations per slot type.

    Returns list of violations (empty = PASS).
    """
    violations: list[str] = []
    slot = slot_name.upper()

    if slot == "A":
        return []

    if slot == "F":
        # Single string — bare unquoted string is fine
        try:
            parsed = json.loads(output)
            if not isinstance(parsed, str):
                violations.append(
                    f"Slot F: expected a single string, got {type(parsed).__name__}"
                )
        except json.JSONDecodeError:
            # Bare string without quotes — accept as-is
            if "\n" in output.strip() and output.strip().startswith("["):
                violations.append("Slot F: expected a single string, got multi-line array-like")

        return violations

    if slot == "E":
        try:
            parsed = json.loads(output)
        except json.JSONDecodeError as exc:
            violations.append(f"Slot E: invalid JSON — {exc}")
            return violations
        if not isinstance(parsed, dict):
            violations.append(
                f"Slot E: expected JSON object, got {type(parsed).__name__}"
            )
            return violations
        required_keys = {"layer_1", "layer_2", "layer_3"}
        missing = required_keys - set(parsed.keys())
        if missing:
            violations.append(
                f"Slot E: missing keys {sorted(missing)}"
            )
        return violations

    # Slots B, C, D — JSON arrays of strings
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        violations.append(f"Slot {slot}: invalid JSON — {exc}")
        return violations

    if not isinstance(parsed, list):
        violations.append(
            f"Slot {slot}: expected JSON array, got {type(parsed).__name__}"
        )
        return violations

    non_strings = [i for i, v in enumerate(parsed) if not isinstance(v, str)]
    if non_strings:
        violations.append(
            f"Slot {slot}: non-string elements at indices {non_strings}"
        )

    if slot == "B":
        if len(parsed) != expected_count:
            violations.append(
                f"Slot B: expected exactly {expected_count} strings, got {len(parsed)}"
            )
    elif slot == "C":
        if not (1 <= len(parsed) <= expected_count):
            violations.append(
                f"Slot C: expected 1–{expected_count} strings, got {len(parsed)}"
            )
    elif slot == "D":
        if len(parsed) != expected_count:
            violations.append(
                f"Slot D: expected exactly {expected_count} strings, got {len(parsed)}"
            )

    return violations


# ─── Top-level entry point ──────────────────────────────────────────────────

def validate_slot(
    slot_name: str,
    output: str,
    fact_bundle: dict[str, Any],
    expected_count: int = 0,
) -> tuple[bool, list[str]]:
    """Run all three validation gates on a single slot's LLM output.

    Returns ``(passed, list_of_all_violations)`` where *passed* is ``True``
    only when every gate returns an empty list.
    """
    all_violations: list[str] = []

    parity = check_number_parity(output, fact_bundle)
    all_violations.extend(parity)

    lint = check_voice_lint(output, fact_bundle)
    all_violations.extend(lint)

    struct = check_structure(output, slot_name, expected_count)
    all_violations.extend(struct)

    passed = len(all_violations) == 0

    if not passed:
        for v in all_violations:
            print(f"[slot_validator] {v}", file=sys.stderr)

    return passed, all_violations
