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


# ─── Gate 4: Slot D play-title vs body alignment ────────────────────────────

_PRICING_TOKENS = (
    "leak",
    "discount",
    "pricing",
    "price-discipline",
    "price discipline",
)
_RETENTION_TOKENS = (
    "second-year",
    "second year",
    "return rate",
    "new dealer",
    "first-time",
    "reorder",
)
_CROSS_SELL_BAN = (
    "leak rate",
    "discount leakage",
    "discretionary-price",
    "discount-authority",
    "discount authority",
)


def _body_matches_play_type(play: dict, body: str) -> bool:
    """True when *body* is about the play's type, not a different play."""
    ptype = play.get("type") or ""
    body_l = (body or "").lower()
    if ptype == "pricing":
        return any(t in body_l for t in _PRICING_TOKENS)
    if ptype == "retention":
        if any(t in body_l for t in _CROSS_SELL_BAN):
            return False
        return any(t in body_l for t in _RETENTION_TOKENS)
    if ptype == "cross_sell":
        if any(t in body_l for t in _CROSS_SELL_BAN):
            return False
        family = str(play.get("target_family") or "").strip()
        if family and family.lower() in body_l:
            return True
        anchor = str(play.get("anchor_item") or "").strip()
        if anchor and anchor.lower() in body_l:
            return True
        return any(
            t in body_l
            for t in ("cross-sell", "cross sell", "never bought", "overlap", "family")
        )
    return True


def check_play_alignment(
    plays: list[dict], play_framing: list[str] | None
) -> list[str]:
    """Fail the run when slot-D bodies are zipped onto the wrong play title.

    ``play_framing[i]`` must describe ``plays[i]``. A pricing/leakage body
    under a cross-sell or second-year title is the ali/hfg defect.
    """
    if not play_framing:
        return []
    violations: list[str] = []
    if len(play_framing) != len(plays):
        violations.append(
            f"Slot D: expected {len(plays)} play_framing strings "
            f"(one per selected play), got {len(play_framing)}"
        )
        return violations
    for i, (play, body) in enumerate(zip(plays, play_framing)):
        ptype = play.get("type") or "unknown"
        if not _body_matches_play_type(play, body):
            violations.append(
                f"Slot D[{i}]: play type {ptype!r} does not match framing body "
                f"(title/body mismatch)"
            )
    return violations


def reorder_play_framing(
    plays: list[dict], play_framing: list[str] | None
) -> list[str] | None:
    """Re-key a Slot-D array onto the selected plays, matching on play type.

    Handles two kinds of drift between an authored prose file and the plays the
    pipeline selects at run time:

    * **reorder** — same bodies, different rank order (signal ranking changed).
    * **superset** — the prose file describes plays that are no longer selected.
      `kal` authored a cross-sell body and a pricing body; only the cross-sell
      play now survives selection. The orphaned body is dropped, not treated as
      a mismatch — nothing is wrong, the file simply describes more plays than
      were chosen.

    Succeeds only when every selected play has exactly one matching body.
    Otherwise the original array is returned unchanged so
    ``check_play_alignment`` still fails the run on a real title/body mismatch.
    A *subset* (fewer bodies than plays) cannot be covered and is returned as-is.
    """
    if not play_framing or len(play_framing) < len(plays):
        return play_framing
    remaining = list(enumerate(play_framing))
    reordered: list[str] = []
    for play in plays:
        matches = [
            (index, body)
            for index, body in remaining
            if _body_matches_play_type(play, body)
        ]
        if len(matches) != 1:
            return play_framing
        matched_index, matched_body = matches[0]
        reordered.append(matched_body)
        remaining = [
            pair for pair in remaining if pair[0] != matched_index
        ]
    return reordered


# Corporate suffixes an author drops when writing prose: the ERP row says
# "The Swan's Nest Inc" and the body says "The Swan's Nest".
_ACCOUNT_SUFFIXES = (
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "co", "co.", "corp", "corp.",
    "dba", "company", "group", "llp", "plc", "lp", "&", "and",
)


def _account_keys(account) -> list[str]:
    """Identity tokens a Slot-B body might use to name this account.

    Includes progressively shorter forms, because prose names an account the way
    a person would ("OP Jenkins"), not the way the ERP stores it
    ("OP JENKINS FURNITURE & DESIGN"). Longest first so the most specific match
    is tried before a looser one.
    """
    keys: list[str] = []
    name = (getattr(account, "bill_to_name", None) or "").strip()
    number = (getattr(account, "bill_to_number", None) or "").strip()
    if name:
        keys.append(name)
        words = name.split()
        # drop trailing corporate suffixes
        trimmed = list(words)
        while trimmed and trimmed[-1].strip(".,").lower() in _ACCOUNT_SUFFIXES:
            trimmed.pop()
        if trimmed and len(trimmed) != len(words):
            keys.append(" ".join(trimmed))
        # a two-word head is usually the recognisable name
        if len(trimmed) > 2:
            keys.append(" ".join(trimmed[:2]))
    if number:
        keys.append(number)
    # longest first, de-duplicated
    seen: set[str] = set()
    out: list[str] = []
    for k in sorted(keys, key=len, reverse=True):
        if k.lower() not in seen:
            seen.add(k.lower())
            out.append(k)
    return out


def _body_names_account(body: str, keys: list[str]) -> bool:
    low = (body or "").lower()
    return any(k.lower() in low for k in keys if k)


def align_talking_points(outreach_list, talking_points):
    """T1-2: re-key Slot B onto the post-screen call list instead of dropping it.

    Slot B is an array zipped onto call-list rows BY INDEX. `outreach_screen`
    re-ranks that list by actionability and drops house/DTC rows, so the old
    code nulled the WHOLE array whenever either happened — and every row fell
    back to the template. That is why Sarreid shipped five near-identical
    "Pace has collapsed N% in six months" rows while
    `outputs/sarreid_prose_2026-07-02.json` still held the authored,
    account-specific bodies.

    The fix is the one the same function already applies to Slot C and Slot D:
    re-key by identity rather than position. Each remaining row takes the body
    that names it; a row with no matching body gets "" so the deterministic
    per-row template fills just that row.
    """
    if not outreach_list:
        return None
    if not talking_points:
        return talking_points
    remaining = list(enumerate(talking_points))
    aligned: list[str] = []
    used: set[int] = set()
    for account in outreach_list:
        keys = _account_keys(account)
        hits = [
            (i, body) for i, body in remaining
            if i not in used and _body_names_account(body, keys)
        ]
        if len(hits) == 1:
            i, body = hits[0]
            used.add(i)
            aligned.append(body)
        else:
            aligned.append("")
    return aligned if any(aligned) else None


def _coaching_rep_keys(rep) -> list[str]:
    keys: list[str] = []
    name = (getattr(rep, "rep_name_tier2", None) or "").strip()
    number = (getattr(rep, "rep_number", None) or "").strip()
    if name:
        keys.append(name)
    if number:
        keys.append(number)
        if not number.lower().startswith("rep "):
            keys.append(f"rep {number}")
    return keys


def _body_mentions_rep(body: str, keys: list[str]) -> bool:
    text = (body or "").casefold()
    for key in keys:
        token = key.strip()
        if len(token) < 2:
            continue
        if token.casefold() in text:
            return True
    return False


def align_coaching_narratives(
    card_reps: list, narratives: list[str] | None
) -> list[str] | None:
    """Keep Slot C when cards remain; re-key by rep identity if the array drifted.

    Never drop the whole array while ``card_reps`` is non-empty. A 1:1 length
    match keeps positional order (the common Track-2 rewrite). A length
    mismatch unique-matches each remaining card to a narrative that names
    that rep; unmatched cards get an empty string so the template fallback
    (slope-aware) fills them.
    """
    if not card_reps:
        return None
    if not narratives:
        return narratives
    if len(narratives) == len(card_reps):
        return list(narratives)
    remaining = list(enumerate(narratives))
    aligned: list[str] = []
    used: set[int] = set()
    for rep in card_reps:
        keys = _coaching_rep_keys(rep)
        hits = [
            (idx, body)
            for idx, body in remaining
            if idx not in used and _body_mentions_rep(body, keys)
        ]
        if len(hits) == 1:
            aligned.append(hits[0][1])
            used.add(hits[0][0])
        else:
            aligned.append("")
    return aligned
