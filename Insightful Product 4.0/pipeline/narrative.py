"""Prose-slot orchestrator — generates all 6 LLM narrative blocks.

Slot A  hero_framing        §1  "The 60-second read" (original generate_hero_framing)
Slot B  talking_points      §2  per-account talking points
Slot C  coaching_narratives §6  per-rep coaching cards
Slot D  play_framing        §3  play body prose
Slot E  growth_connective   §5  growth-layer connective tissue
Slot F  outreach_framing    §2  call-list header callout

Entry points
─────────────
generate_hero_framing()      — unchanged legacy path (Slot A only)
generate_all_slots()         — async orchestrator, runs all 6 in parallel
generate_all_slots_sync()    — sync wrapper via asyncio.run()
generate_slot()              — single-slot generator (build → prompt → LLM → validate)

Every dollar cited must trace to the fact bundle passed in. The system prompt
(communication guideline + industry context + profile + absolute constraints)
is built once and cached across all six calls via Anthropic prompt caching.
"""
from __future__ import annotations

import asyncio
import json
import os
import re as _re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Optional

from .gather import GatherBundle
from .preflight import RunPosture
from .signals import Signal

try:
    from .slot_validator import validate_slot
except ImportError:
    def validate_slot(slot_name: str, output: Any, fact_bundle: Any = None, expected_count: int = 0) -> tuple[bool, list[str]]:
        """Stub — passes everything when slot_validator doesn't exist yet."""
        return True, []

from . import config

# ─── Constants ────────────────────────────────────────────────────────────────

HERO_FRAMING_PLACEHOLDER = (
    "<!-- §1 HERO FRAMING NOT GENERATED — see narrative.py logs; "
    "fill by hand per pipeline/SURGICAL_EDIT_GUIDE.md -->"
)

_KNOWLEDGE_DIR = config.WORKSPACE_ROOT / "knowledge"

_SLOT_NAMES = [
    "hero_framing",
    "talking_points",
    "coaching_narratives",
    "play_framing",
    "growth_connective",
    "outreach_framing",
]

_SLOT_MODEL_ENV = {
    "hero_framing":        "INSIGHTFUL_HERO_MODEL",
    "coaching_narratives": "INSIGHTFUL_COACHING_MODEL",
}

_ABSOLUTE_CONSTRAINTS = """\
Absolute constraints (apply to EVERY slot):
1. Every dollar you cite must come from the fact bundle or signals passed in. No new numbers.
2. No forbidden vocab: posture, feed(s), pipeline (as verb), house-rep, NRR, cohort, playbook.
3. Markdown formatting only — no code fences, no JSON wrappers, no meta commentary.
4. Use derived_facts where present; do NOT recompute ratios or deltas from raw facts.
5. If a fact is absent or null, skip it — never hallucinate a placeholder number."""

# ─── Slot prompt templates ────────────────────────────────────────────────────

SLOT_PROMPTS: dict[str, str] = {
    "hero_framing": "__hero__",  # sentinel — hero uses _build_prompt()

    "talking_points": (
        "Write a unique 1-2 sentence talking point (markdown — bold/emphasis "
        "allowed) for each of the {N} accounts below. The talking point is "
        "what the rep says on the call — direct, specific, named.\n\n"
        "Accounts flagged is_cadence_cliff=true are GROWING accounts that "
        "skipped a beat — do NOT use decline language. Accounts flagged "
        "is_real_decline=true are real declines — be direct about the slope.\n\n"
        "Use only numbers from the facts and derived_facts below. Do not "
        "compute new ones.\n\n"
        "Fact bundle:\n{bundle_json}\n\n"
        "Return a JSON array of {N} markdown strings, one per account, "
        "same order. No code fences, no commentary."
    ),

    "coaching_narratives": (
        "Write a coaching card narrative (2-4 sentences, markdown) for each "
        "rep below. The narrative must: (a) name the top at-risk account and "
        "its dollar figure from derived_facts.decay_dollars (NOT the full LTM); "
        "(b) express whether it's a real decline or a beat-skip using "
        "derived_facts.beat_skip_label; (c) give one specific action. If "
        "territory_cluster is present, name the cluster pattern.\n\n"
        "Use only numbers from the facts and derived_facts below. Do not "
        "compute new ones.\n\n"
        "Fact bundle:\n{bundle_json}\n\n"
        "Return a JSON array of {N} markdown strings. No code fences."
    ),

    "play_framing": (
        "Write the narrative body (2-5 sentences, markdown) for each of the "
        "{N} plays below. Each play already has its type, numbers, and action "
        "decided — you provide the framing prose that makes the numbers land "
        "as a specific recommendation. Lead with the dollar and the name, not "
        "the concept. Use derived_facts for upside estimates and flag them as "
        "DIRECTIONAL/ESTIMATED.\n\n"
        "Use only numbers from the facts and derived_facts below. Do not "
        "compute new ones.\n\n"
        "Fact bundle:\n{bundle_json}\n\n"
        "Return a JSON array of {N} markdown strings. No code fences."
    ),

    "growth_connective": (
        "Write 1-2 connective sentences per growth layer (markdown) that tie "
        "the numbers into a narrative about where the topline actually lives. "
        "Not arithmetic narration (\"$X offset $Y\") but synthesis (\"the "
        "engine is broad-based dealer reorder, not one account dressed up as "
        "a year\").\n\n"
        "Use only numbers from the facts and derived_facts below. Do not "
        "compute new ones.\n\n"
        "Fact bundle:\n{bundle_json}\n\n"
        "Return a JSON object with keys \"layer_1\", \"layer_2\", \"layer_3\", "
        "each a markdown string. No code fences."
    ),

    "outreach_framing": (
        "Write a 2-3 sentence callout (markdown) that frames the call list "
        "for the reader. If the list contains both real declines and beat-skips "
        "(growing accounts that merely paused), explicitly warn the reader not "
        "to conflate the two conversations — name which rows are which. If all "
        "rows are declines, frame it as a unified decline list.\n\n"
        "Use only numbers from the facts and derived_facts below. Do not "
        "compute new ones.\n\n"
        "Fact bundle:\n{bundle_json}\n\n"
        "Return a single markdown string. No code fences, no commentary."
    ),
}

# ─── Knowledge-doc loader (lazy, cached) ──────────────────────────────────────

_knowledge_cache: dict[str, str] = {}


def _load_knowledge(filename: str) -> str:
    if filename not in _knowledge_cache:
        p = _KNOWLEDGE_DIR / filename
        if p.exists():
            _knowledge_cache[filename] = p.read_text(encoding="utf-8")
        else:
            _knowledge_cache[filename] = ""
    return _knowledge_cache[filename]


# ─── System prompt (shared across all slots, cached by Anthropic) ─────────────

def _build_system_prompt(profile_text: str = "") -> str:
    """Build the shared system prompt with communication guideline, industry
    context, client profile, and absolute constraints."""
    comm = _load_knowledge("communication_guideline.md")
    industry = _load_knowledge("industry_context.md")

    parts = [
        "You are the prose engine for Insightful Product 4.0, a CEO intelligence "
        "brief produced by Kylor Johnson. Your outputs are slotted directly into "
        "the report — no meta commentary, no code fences.",
    ]
    if comm:
        parts.append(f"## Communication guideline\n\n{comm}")
    if industry:
        parts.append(f"## Industry context\n\n{industry}")
    if profile_text:
        parts.append(f"## Client profile\n\n{profile_text}")
    parts.append(_ABSOLUTE_CONSTRAINTS)
    return "\n\n".join(parts)


# ─── Few-shot loader (hero only) ─────────────────────────────────────────────

_SARREID_FEW_SHOT: Optional[str] = None


def load_few_shot() -> str:
    """Read the existing Sarreid §1 block as the few-shot voice example."""
    global _SARREID_FEW_SHOT
    if _SARREID_FEW_SHOT is None:
        path = config.OUTPUTS_DIR / "Sarreid_CEO_intelligence_report_2026-06-29.md"
        if not path.exists():
            return ""
        text = path.read_text(encoding="utf-8")
        start = text.find("## The 60-second read")
        if start < 0:
            return ""
        rest = text[start:]
        next_h2 = rest.find("\n## ", 10)
        _SARREID_FEW_SHOT = rest[:next_h2] if next_h2 > 0 else rest
    return _SARREID_FEW_SHOT


# ─── Hero prompt builder (Slot A — unchanged logic) ──────────────────────────

def _build_prompt(
    posture: RunPosture,
    top_signals: list[Signal],
    profile_text: str,
    gather: GatherBundle,
) -> str:
    """Build the constrained prompt for the hero slot.

    Two branches: with-signals (full §1 in Sarreid shape) vs without-signals
    (thin §1 honest about the pre-detector state).
    """
    few_shot = load_few_shot()

    if top_signals:
        sig_facts = "\n".join(
            f"- [{s.kind} · {s.section}] {s.headline} · ${s.dollar_impact:,.0f}"
            for s in top_signals[:7]
        )
        signal_block = f"""Top ranked signals (pick three "things you wouldn't have known" from this list — do not use anything else):
{sig_facts}
"""
        finding_directive = (
            "- Exactly 3 \"things you wouldn't have known\" as numbered items, "
            "each 1-2 sentences, each traced to a signal above."
        )
        actions_directive = (
            "- Priority-actions block: 1 \"This week\" call, 1 \"This week\" "
            "territory or coaching review, 1 \"This month\" play — each pulled "
            "from the signals above."
        )
    else:
        signal_block = (
            "No ranked signals were produced this run (signals.detect_all is "
            "still empty in the current pipeline state). Do NOT invent findings.\n"
        )
        finding_directive = (
            "- Skip the numbered findings block. In its place write one short "
            "paragraph naming the sections that carry the material findings "
            "(§2 Do this week, §5 What's driving, §6 The team, §8 What's selling, "
            "§9 The dealer base) and telling the reader those sections do the work."
        )
        actions_directive = (
            "- Skip the priority-actions block. In its place write one sentence "
            "pointing the reader to §2 for named accounts + §3 for the month's plays."
        )

    if posture.is_stale:
        posture_directive = (
            "\nSTALE-FEED FRAMING (critical — the invoice feed is frozen "
            f"{posture.stale_age_phrase} old, {posture.erp_asof_stamp}):\n"
            "- LEAD with the LIVE signal: the ${:,.0f} of confirmed eCat order "
            "volume, which is current (\"live through today\"). Open on the "
            "recovery — the org is still ordering through the platform even "
            "though the invoice feed stopped.\n".format(posture.ecat_ltm_confirmed_gmv)
            + "- Frame every invoiced/decline figure in the PAST TENSE and stamp "
            f"it \"{posture.erp_asof_stamp}\" — it describes where the business "
            "was, not where it is. NEVER stamp the eCat number with the stale "
            "date; eCat is live.\n"
            "- Replace \"do this week\" urgency with \"refresh the feed, then "
            "work the live channel.\"\n"
        )
    elif posture.is_provably_incomplete:
        posture_directive = (
            "\nPROVABLY-INCOMPLETE FRAMING (confirmed eCat capture EXCEEDS "
            "invoiced net — the invoice feed is provably a channel subset):\n"
            "- Present invoiced net AND eCat both in absolute dollars. Do NOT "
            "state an eCat-vs-invoiced percentage or capture rate.\n"
            "- NEVER call invoiced net the \"total\" or \"complete\" business — "
            "it is a channel subset that eCat capture alone exceeds.\n"
        )
    else:
        posture_directive = ""

    return f"""You are drafting §1 "The 60-second read" for a CEO intelligence brief in the voice of Kylor Johnson (Insightful Product 4.0). Match the following few-shot's tone exactly — direct, specific, no hedging, no vocabulary from the internal §P forbidden list (posture, feed, pipeline used as a verb, house-rep, etc.).

Facts (use these verbatim; do not invent numbers):
- Org: {posture.org}
- Invoiced LTM: ${posture.inv_ltm_net:,.0f} across {posture.n_inv_ltm:,} invoices
- Report-through date: {posture.report_through_date}
- eCat confirmed GMV (LTM): ${posture.ecat_ltm_confirmed_gmv:,.0f} ({(posture.ecat_ltm_confirmed_gmv * 100 / posture.inv_ltm_net) if posture.inv_ltm_net else 0:.1f}% of invoiced)
- Report mode: {posture.report_mode}
- Rep-identity tier: {posture.rep_identity_tier} (bridge {posture.name_bridge_pct}% · {posture.distinct_repnum} distinct)
- Channel gate: {posture.channel_posture} ({posture.distinct_origins} distinct origins)
- Feed state: {posture.feed_completeness} · {posture.days_since_last_invoice} days since last invoice
{posture_directive}
{signal_block}
Constraints:
- Open with a 2-3 sentence 60-second read paragraph that leads with the topline dollar and states the honest shape of the year.
- Then a 4-row summary table with the format `| label | value |` — the header row is blank pipes `| | |` and separator `|---|---|`. Rows are: same-dealer $ story, growth-family $ story, top-rep $ story, $-at-risk story. If any of those aren't in the signals above, use "see §{{section}}" as the value.
{finding_directive}
{actions_directive}
- Every dollar you cite must come from the facts above or the signals list. No new numbers.
- No forbidden vocab.

Few-shot for voice (do not copy content — just tone and shape):
{few_shot}

Return only the §1 body — no top-level heading (the template already emits "## The 60-second read"), no code fences, no meta commentary."""


# ─── Validation (hero — unchanged) ───────────────────────────────────────────

_FORBIDDEN_VOCAB = _re.compile(
    r'\b(?:posture|feed(?:s)?|pipeline|house[- ]rep|NRR|cohort|playbook)\b',
    _re.IGNORECASE,
)

_DOLLAR_PATTERN = _re.compile(r'\$[\d,]+(?:\.\d+)?[KMB]?')


def _validate_hero(
    text: str,
    posture: "RunPosture",
    top_signals: list["Signal"],
) -> tuple[bool, list[str]]:
    """Post-LLM validation of the hero framing block.

    Returns (all_critical_passed, list_of_warnings). Warnings are logged
    but do not block the output. If all three structural checks fail,
    all_critical_passed is False and the caller should fall back to the
    template placeholder.
    """
    warnings: list[str] = []

    for m in _FORBIDDEN_VOCAB.finditer(text):
        warnings.append(f"FORBIDDEN VOCAB: '{m.group()}' at position {m.start()}")

    prompt_dollars = set()
    if posture:
        for attr in ("inv_ltm_net", "ecat_ltm_confirmed_gmv"):
            val = getattr(posture, attr, 0)
            if val:
                prompt_dollars.add(f"${val:,.0f}")
                prompt_dollars.add(f"${val/1000:,.0f}K")
                prompt_dollars.add(f"${val/1_000_000:,.2f}M")
    for s in (top_signals or []):
        prompt_dollars.add(f"${s.dollar_impact:,.0f}")
        prompt_dollars.add(f"${s.dollar_impact/1000:,.0f}K")
        prompt_dollars.add(f"${s.dollar_impact/1_000_000:,.2f}M")

    output_dollars = _DOLLAR_PATTERN.findall(text)
    for d in output_dollars:
        normalized = d.replace(",", "")
        if d not in prompt_dollars and not any(normalized in pd.replace(",", "") for pd in prompt_dollars):
            warnings.append(f"UNTRACED DOLLAR: {d} not found in prompt facts/signals")

    has_paragraph = len(text.strip().split("\n\n")) >= 2
    has_table = "|" in text and "---|" in text
    has_actions = "this week" in text.lower() or "priority action" in text.lower()

    if not has_paragraph:
        warnings.append("STRUCTURE: missing multi-paragraph body")
    if not has_table:
        warnings.append("STRUCTURE: missing summary table")
    if not has_actions:
        warnings.append("STRUCTURE: missing priority actions block")

    all_critical_passed = has_paragraph or has_table or has_actions
    return all_critical_passed, warnings


# ─── LLM call (shared, with prompt caching) ──────────────────────────────────

def llm_call(user_prompt: str, system_prompt: str = "", *, model_override: str = "") -> str:
    """Anthropic Claude call with prompt caching on the system prompt.

    Module-level so tests can monkey-patch.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    from anthropic import Anthropic
    client = Anthropic()

    model = (
        model_override
        or os.environ.get("INSIGHTFUL_NARRATIVE_MODEL", "claude-sonnet-4-5-20250929")
    )

    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    if system_prompt:
        kwargs["system"] = [
            {"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}},
        ]

    msg = client.messages.create(**kwargs)
    return msg.content[0].text if msg.content else ""


# ─── Legacy entry point (Slot A only — unchanged behavior) ───────────────────

def generate_hero_framing(
    *,
    posture: RunPosture,
    top_signals: list[Signal],
    profile_text: str,
    gather: GatherBundle,
) -> Optional[str]:
    """Construct the constrained prompt, call the LLM, return the framing.

    Fail-soft: returns None on any failure so assemble.py drops in the
    "NOT GENERATED" placeholder comment for the surgical editor to fill.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        import sys
        print("narrative.generate_hero_framing: ANTHROPIC_API_KEY not set — skipping", file=sys.stderr)
        return None
    try:
        prompt = _build_prompt(posture, top_signals, profile_text, gather)
        system = _build_system_prompt(profile_text)
        result = llm_call(prompt, system)
        if not result or not result.strip():
            return None
        passed, warnings = _validate_hero(result, posture, top_signals)
        if warnings:
            import sys
            for w in warnings:
                print(f"narrative._validate_hero: {w}", file=sys.stderr)
        if not passed:
            print("narrative._validate_hero: ALL structural checks failed — falling back to placeholder", file=sys.stderr)
            return None
        return result
    except Exception as e:
        import sys
        print(f"narrative.generate_hero_framing: {type(e).__name__}: {e}", file=sys.stderr)
        return None


# ─── Response parsing ─────────────────────────────────────────────────────────

def _parse_slot_output(slot_name: str, raw: str) -> Any:
    """Parse the raw LLM output into the expected shape for each slot."""
    text = raw.strip()
    if text.startswith("```"):
        first_nl = text.find("\n")
        last_fence = text.rfind("```")
        if first_nl > 0 and last_fence > first_nl:
            text = text[first_nl + 1:last_fence].strip()

    if slot_name == "hero_framing":
        return text

    if slot_name in ("talking_points", "coaching_narratives", "play_framing"):
        return json.loads(text)  # list[str]

    if slot_name == "growth_connective":
        return json.loads(text)  # dict with layer_1/2/3

    if slot_name == "outreach_framing":
        try:
            parsed = json.loads(text)
            if isinstance(parsed, str):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        return text

    return text


# ─── Single-slot generator ───────────────────────────────────────────────────

def generate_slot(
    slot_name: str,
    fact_bundle: dict,
    profile_text: str,
    expected_count: int = 0,
) -> tuple[Any | None, str]:
    """Generate one slot. Returns (result, status_str).

    result is the parsed output (str/list/dict) or None on failure.
    status_str is "✓" or "FELL BACK (reason: ...)"
    """
    import sys

    if slot_name == "hero_framing":
        return None, "FELL BACK (reason: hero uses generate_hero_framing)"

    template = SLOT_PROMPTS.get(slot_name)
    if not template:
        return None, f"FELL BACK (reason: unknown slot '{slot_name}')"

    system = _build_system_prompt(profile_text)
    bundle_json = json.dumps(fact_bundle, indent=2, default=str)
    user_prompt = template.format(N=expected_count, bundle_json=bundle_json)

    env_key = _SLOT_MODEL_ENV.get(slot_name)
    model_override = os.environ.get(env_key, "") if env_key else ""

    try:
        raw = llm_call(user_prompt, system, model_override=model_override)
        if not raw or not raw.strip():
            return None, "FELL BACK (reason: LLM returned empty)"
    except Exception as e:
        print(f"narrative.generate_slot({slot_name}): LLM error: {e}", file=sys.stderr)
        return None, f"FELL BACK (reason: LLM error: {type(e).__name__})"

    try:
        parsed = _parse_slot_output(slot_name, raw)
    except Exception as e:
        print(f"narrative.generate_slot({slot_name}): parse error: {e}", file=sys.stderr)
        return None, f"FELL BACK (reason: parse error: {type(e).__name__})"

    output_str = json.dumps(parsed) if not isinstance(parsed, str) else parsed
    passed, warnings = validate_slot(slot_name, output_str, fact_bundle, expected_count)
    if warnings:
        for w in warnings:
            print(f"narrative.generate_slot({slot_name}): {w}", file=sys.stderr)
    if not passed:
        untraced = [w for w in warnings if "untraced" in w.lower() or "parity" in w.lower()]
        reason = untraced[0] if untraced else "validation failed"
        return None, f"FELL BACK (reason: {reason})"

    return parsed, "✓"


# ─── Orchestrator ─────────────────────────────────────────────────────────────

async def generate_all_slots(
    *,
    posture: RunPosture,
    gather: GatherBundle,
    signals: list[Signal],
    profile_text: str,
) -> dict[str, Any]:
    """Run all 6 prose slots in parallel. Returns a dict keyed by slot name
    (hero_framing, talking_points, coaching_narratives, play_framing,
    growth_connective, outreach_framing). Each value is the LLM output
    (str or list[str] or dict) or None on failure.

    Also returns a 'slot_status' key with the console status line.
    """
    import sys

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("narrative.generate_all_slots: ANTHROPIC_API_KEY not set — all slots skipped", file=sys.stderr)
        result: dict[str, Any] = {name: None for name in _SLOT_NAMES}
        result["slot_status"] = "all skipped (no API key)"
        return result

    system = _build_system_prompt(profile_text)

    # Slot A: hero — uses the legacy path with its own prompt + validation
    hero_model_env = os.environ.get("INSIGHTFUL_HERO_MODEL", "")

    def _run_hero() -> tuple[Any | None, str]:
        try:
            prompt = _build_prompt(posture, signals, profile_text, gather)
            raw = llm_call(prompt, system, model_override=hero_model_env)
            if not raw or not raw.strip():
                return None, "FELL BACK (reason: LLM returned empty)"
            passed, warnings = _validate_hero(raw, posture, signals)
            if warnings:
                for w in warnings:
                    print(f"narrative.hero: {w}", file=sys.stderr)
            if not passed:
                return None, "FELL BACK (reason: validation failed)"
            return raw, "✓"
        except Exception as e:
            print(f"narrative.hero: {type(e).__name__}: {e}", file=sys.stderr)
            return None, f"FELL BACK (reason: {type(e).__name__})"

    # Build per-slot fact bundles via fact_bundles.py
    try:
        from . import fact_bundles as fb
    except ImportError:
        fb = None  # type: ignore[assignment]

    top_signals = sorted(signals, key=lambda s: s.rank, reverse=True)[:7] if signals else []

    # Build bundles for each slot
    bundles: dict[str, dict] = {}
    expected_counts: dict[str, int] = {}

    if fb:
        bundles["hero_framing"] = fb.build_hero_bundle(posture, top_signals, gather)
        outreach_list = list(gather.outreach_list)
        bundles["talking_points"] = fb.build_talking_points_bundle(outreach_list, posture, profile_text)
        expected_counts["talking_points"] = len(outreach_list)

        card_reps = [r for r in gather.rep_risks if r.accounts_at_risk > 0][:5]
        bundles["coaching_narratives"] = fb.build_coaching_bundle(card_reps, gather.decay, posture)
        expected_counts["coaching_narratives"] = len(card_reps)

        plays = fb.build_plays_from_gather(gather, posture, signals)
        bundles["play_framing"] = fb.build_play_framing_bundle(plays, gather, posture)
        expected_counts["play_framing"] = len(plays)

        bundles["growth_connective"] = fb.build_growth_connective_bundle(gather, posture)
        expected_counts["growth_connective"] = 3

        bundles["outreach_framing"] = fb.build_outreach_framing_bundle(outreach_list)
        expected_counts["outreach_framing"] = 1
    else:
        fallback_bundle = {
            "facts": {"inv_ltm_net": posture.inv_ltm_net},
            "derived_facts": {},
        }
        for s in _SLOT_NAMES:
            bundles[s] = fallback_bundle
            expected_counts[s] = 0

    non_hero_slots = [s for s in _SLOT_NAMES if s != "hero_framing"]

    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {}
        futures["hero_framing"] = loop.run_in_executor(pool, _run_hero)
        for slot in non_hero_slots:
            futures[slot] = loop.run_in_executor(
                pool,
                generate_slot,
                slot, bundles.get(slot, {}), profile_text, expected_counts.get(slot, 0),
            )

        results: dict[str, Any] = {}
        statuses: list[str] = []
        for slot_name in _SLOT_NAMES:
            value, status = await futures[slot_name]
            results[slot_name] = value
            letter = {"hero_framing": "A", "talking_points": "B",
                      "coaching_narratives": "C", "play_framing": "D",
                      "growth_connective": "E", "outreach_framing": "F"}[slot_name]
            statuses.append(f"{letter} {status}")

    _name_to_letter = {"hero_framing": "a", "talking_points": "b",
                       "coaching_narratives": "c", "play_framing": "d",
                       "growth_connective": "e", "outreach_framing": "f"}
    results["slot_status"] = "[narrative] slot " + " · ".join(statuses)
    results["bundles"] = {
        f"slot_{_name_to_letter[k]}_bundle": v
        for k, v in bundles.items()
        if k in _name_to_letter
    }
    return results


def generate_all_slots_sync(
    *,
    posture: RunPosture,
    gather: GatherBundle,
    signals: list[Signal],
    profile_text: str,
) -> dict[str, Any]:
    """Sync wrapper for generate_all_slots using asyncio.run()."""
    return asyncio.run(
        generate_all_slots(
            posture=posture,
            gather=gather,
            signals=signals,
            profile_text=profile_text,
        )
    )
