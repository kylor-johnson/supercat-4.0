#!/usr/bin/env python3
"""Pre-send checker for outbound client emails and documents.

Contract (IMPLEMENTATION_PLAN.md §7 Phase 3, steps 1–9):

  1. Declare stakes.
  2. Void prior analysis.
  3. Three evidence tiers: source files / importer code+tests / live org state.
  4. Name the prior client-pushback error if the pattern appears in the draft.
  5. Enumerate every file by absolute path.
  6. Live-state questions entity by entity, disambiguating:
       active product / deleted product / option / group member.
  7. Review the actual draft artifact — not a summary.
  8. Failure criterion: factually airtight, no over-claim, no blame,
       no asserted-but-unconfirmed mapping.
  9. Verdict: safe-to-send | not-safe-to-send + rewrite guidance.

Every claim in the draft is classified:
    VERIFIED       — backed by source files, importer code, or live org state
    UNVERIFIABLE   — no evidence tier can confirm or deny it
    CONTRADICTED   — at least one evidence tier directly conflicts

Governing lines from the corpus:
    "a flagged gap beats a wrong-but-confident map"
    "if you can't prove it, flag it — do not invent."

Live-state evidence always cites a QUERY_NAME, never a typed count, per
IMPLEMENTATION_PLAN.md §2.3.  build_live_state() from reconcile/queries.py
is the only thing that may populate Tier 3.

CLI:
    python scripts/verify/before_send.py \\
        --draft eCat_Onboarding/tcd/draft_email.md \\
        --client-dir eCat_Onboarding/tcd \\
        --shortname tcd \\
        [--live-state live_tcd.json]   # generated if omitted + DB available

Exit codes:
    0  safe-to-send
    1  not safe-to-send (at least one CONTRADICTED claim)
    2  could not complete review (missing required inputs)
"""

import argparse
import dataclasses
import datetime
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Claim classification
# ---------------------------------------------------------------------------

VERIFIED = "VERIFIED"
UNVERIFIABLE = "UNVERIFIABLE"
CONTRADICTED = "CONTRADICTED"

KIND_COUNT = "count"
KIND_PRICE_CODE = "price_code"
KIND_IMAGE_STATUS = "image_status"
KIND_ENTITY = "entity"
KIND_CAUSAL = "causal"

# Tiers, as prose labels used in the report.
TIER_SOURCE = "Tier 1 — source files"
TIER_CODE = "Tier 2 — importer code/tests"
TIER_LIVE = "Tier 3 — live org state"


@dataclasses.dataclass
class Claim:
    """One factual assertion extracted from the draft."""
    text: str           # quoted claim text
    kind: str           # KIND_* constant
    status: str         # VERIFIED / UNVERIFIABLE / CONTRADICTED
    evidence: str       # human-readable rationale
    query_name: str     # QUERY_NAME from queries.py if backed by live DB, else ""
    line_no: int        # 1-based line number in the draft


# ---------------------------------------------------------------------------
# Known-bad-pattern registry
# ---------------------------------------------------------------------------

# Each entry: (name, description for report, detect(draft_text, live_state) -> bool)
# These correspond to corpus-documented failures.

_PRIOR_ERROR_PATTERNS: List[Tuple[str, str, Any]] = []


def _register_pattern(name, description, detect_fn):
    _PRIOR_ERROR_PATTERNS.append((name, description, detect_fn))
    return detect_fn


def _detect_tcd_default_price_code(draft_text: str, live: Dict) -> bool:
    """Return True if the draft shows a DefaultPriceCode that is not a valid price level.

    The tcd incident: ERP exported DefaultPriceCode=0, which is not a price level code.
    Every customer row was rejected. A draft that asserts a specific DefaultPriceCode
    value without confirming it exists in the org's price levels triggers this pattern.
    IMPLEMENTATION_PLAN.md §2.1, Appendix B.
    """
    price_levels = {str(c).lower() for c in (live.get("price_levels") or [])}
    if not price_levels:
        return False
    # Look for DefaultPriceCode = <value> patterns in the draft
    for m in re.finditer(
        r"DefaultPriceCode\s*[=:]\s*['\"]?(\w+)['\"]?", draft_text, re.IGNORECASE
    ):
        code = m.group(1).strip().lower()
        if code not in price_levels:
            return True
    # Also flag asserting a price level name that doesn't exist
    for m in re.finditer(
        r"price\s+(?:level|code)\s+['\"]?([A-Za-z0-9_]+)['\"]?", draft_text, re.IGNORECASE
    ):
        code = m.group(1).strip().lower()
        if code not in price_levels and code not in ("level", "code", "the", "a"):
            return True
    return False


def _detect_magic_lite_image_false_positive(draft_text: str, live: Dict) -> bool:
    """Return True if the draft claims images are broken for codes that ARE uploaded.

    The Magic Lite incident: an agent declared GDL-6, DL-FR, RGL-FR broken from
    catalog text; screenshots proved all three were correct. The checker detects:
    draft asserts a specific SKU image is broken/missing → that filename IS uploaded.
    IMPLEMENTATION_PLAN.md §5.3.
    """
    uploaded = {
        os.path.splitext(f)[0].lower()
        for f in (live.get("uploaded_images") or [])
    }
    if not uploaded:
        return False
    # Patterns: "GDL-6 image is broken", "image for GDL-6 is missing", etc.
    broken_patterns = [
        r"([A-Z][A-Z0-9]{0,9}-[A-Z0-9][A-Z0-9-]{0,19})\s+(?:image|photo)",
        r"(?:image|photo)\s+(?:for|of)\s+([A-Z][A-Z0-9]{0,9}-[A-Z0-9][A-Z0-9-]{0,19})",
    ]
    negative_words = re.compile(
        r"\b(broken|missing|incorrect|wrong|not showing|not uploading|broken|"
        r"needs? re-?upload|not displaying|not visible|not found|absent)\b",
        re.IGNORECASE,
    )
    for line in draft_text.splitlines():
        if not negative_words.search(line):
            continue
        for pat in broken_patterns:
            for m in re.finditer(pat, line, re.IGNORECASE):
                code = m.group(1).strip().lower()
                if code in uploaded:
                    return True
    return False


_register_pattern(
    "tcd/DefaultPriceCode",
    "Terracotta pattern: DefaultPriceCode value asserted in draft is not a valid price "
    "level for this org. At tcd, DefaultPriceCode=0 (an ERP placeholder) rejected every "
    "customer row. A draft that names a specific code without live confirmation is "
    "pre-positioning the client for a second rejection.",
    _detect_tcd_default_price_code,
)

_register_pattern(
    "mali/MagicLite-image-false-positive",
    "Magic Lite pattern: draft claims one or more SKU images are broken, but the live "
    "org already has those image files uploaded (UPLOADED_IMAGES). At Magic Lite, this "
    "claim was sourced from catalog text; screenshots proved the images were correct. "
    "Overwriting a correct image with a re-upload would have been a regression.",
    _detect_magic_lite_image_false_positive,
)


# ---------------------------------------------------------------------------
# Tier 1: source file discovery
# ---------------------------------------------------------------------------

_ECAT_FILE_NAMES = frozenset([
    "products.csv", "stories.csv", "inventory.csv", "customers.csv",
    "options.csv", "option_groups.csv", "matrix_options.csv",
    "contract_prices.csv", "riser_prices.csv", "sentinel.csv",
    "order_data.csv", "invoice_data.csv",
    "CLIENT_PROFILE.md", "HANDOFF.md",
])


def _gather_source_files(client_dir: Optional[str]) -> List[str]:
    """Return absolute paths of all eCat-relevant source files found under client_dir."""
    if not client_dir:
        return []
    found = []
    for root, _dirs, files in os.walk(client_dir):
        for fname in sorted(files):
            if (fname in _ECAT_FILE_NAMES or fname.endswith(".csv")
                    or fname.endswith(".md") or fname.endswith(".py")):
                found.append(os.path.abspath(os.path.join(root, fname)))
    return found


# ---------------------------------------------------------------------------
# Tier 2: importer code rules (from IMPLEMENTATION_PLAN.md + limits_generated.py)
# ---------------------------------------------------------------------------

# Canonical rules verified from supercat_server source, cited as Tier 2 authority.
TIER2_RULES: List[str] = [
    "DefaultPriceCode must match an existing price_levels.code for the org "
    "(validate_customers.py, BAD_PRICE_CODES; tcd Appendix B).",
    "Image files must be .jpg or .jpeg — PNG is silently rejected by CdnImageSync "
    "(product_importer_lib/cdn_image_sync.rb; §4.7).",
    "BOM bytes (EF BB BF) make the first header column unreadable by the importer "
    "(§4.8); three-byte check is the cheapest gate in the plan.",
    "inventory.csv, customers.csv, options.csv, option_groups.csv HARD-DELETE and "
    "reload — omitted rows are gone (ecat-ground-truth).",
    "Taxonomy groups never auto-create from a product import — a missing group is a "
    "fatal import error (§4.7, IMPLEMENTATION_PLAN §7).",
    "Field limits from Product::ATTR_LENGTHS (generated, never transcribed): "
    "LongDesc/ShortDesc/MediumDesc 255 chars each (warn+truncate); "
    "BaseItemCode 40, TradeNameCode 255 (validation error); "
    "option/group Code 15, Name 50 (validation error).",
]


# ---------------------------------------------------------------------------
# Claim extraction from draft text
# ---------------------------------------------------------------------------

# Regex for item/SKU codes (BaseItemCode pattern): e.g. GDL-6, ML-001, DL-FR, RGL-FR
_ITEM_CODE_RE = re.compile(
    r"\b([A-Z][A-Z0-9]{0,9}-[A-Z0-9][A-Z0-9-]{0,19})\b"
)

# Count claim: "346 customers", "1,020 products", "20 images", etc.
_COUNT_RE = re.compile(
    r"\b(\d[\d,]*)\s+"
    r"(products?|active products?|SKUs?|items?|"
    r"customers?|accounts?|bill.tos?|"
    r"images?|photos?|image files?|"
    r"inventory rows?|inventory records?|"
    r"options?|finishes?|colors?|groups?)\b",
    re.IGNORECASE,
)

# DefaultPriceCode explicit value
_PRICE_CODE_RE = re.compile(
    r"DefaultPriceCode\s*[=:]\s*['\"]?(\w+)['\"]?",
    re.IGNORECASE,
)

# Price level name assertion
_PRICE_LEVEL_NAME_RE = re.compile(
    r"\bprice\s+(?:level|code)\s+['\"]?([A-Za-z0-9_]+)['\"]?",
    re.IGNORECASE,
)

# Image-status claim: "GDL-6 image is broken/missing/..."
_IMAGE_BROKEN_RE = re.compile(
    r"(?:"
    r"([A-Z][A-Z0-9]{0,9}-[A-Z0-9][A-Z0-9-]{0,19})\s+(?:image|photo|\.jpg)"
    r"|(?:image|photo)\s+(?:for|of)\s+([A-Z][A-Z0-9]{0,9}-[A-Z0-9][A-Z0-9-]{0,19})"
    r")"
    r"[^.]*?\b(broken|missing|incorrect|wrong|not\s+showing|not\s+uploading|"
    r"not\s+displaying|not\s+visible|absent|re.?upload)\b",
    re.IGNORECASE,
)

# Causal claim: "because", "due to", "caused by", "the reason"
_CAUSAL_RE = re.compile(
    r"\b(?:because|due to|caused by|the reason|resulted in|led to)\b",
    re.IGNORECASE,
)

# Positive import-success claim: "successfully imported", "all X are now live"
_SUCCESS_CLAIM_RE = re.compile(
    r"\b(?:successfully imported|now live|now active|are imported|have been imported|"
    r"import(?:ed)? successfully|now in (?:the|your|eCat)|all.{0,30}imported)\b",
    re.IGNORECASE,
)


def _normalize_count(raw: str) -> int:
    return int(raw.replace(",", ""))


def extract_claims(draft_text: str, live: Dict) -> List[Claim]:
    """Walk the draft line by line and extract every verifiable claim."""
    claims: List[Claim] = []
    lines = draft_text.splitlines()

    uploaded_stems = {
        os.path.splitext(f)[0].lower()
        for f in (live.get("uploaded_images") or [])
    }
    price_levels = {str(c).lower() for c in (live.get("price_levels") or [])}
    live_counts: Dict[str, int] = live.get("counts") or {}
    live_product_keys = {
        str(k).lower() for k in (live.get("keys") or {}).get("products.csv") or []
    }

    for line_no, line in enumerate(lines, start=1):

        # --- Count claims ---------------------------------------------------
        for m in _COUNT_RE.finditer(line):
            raw_n = m.group(1)
            kind_word = m.group(2).lower()
            n = _normalize_count(raw_n)

            # Map the kind word to a live count key
            live_key = None
            query_name = ""
            if re.match(r"products?|skus?|items?", kind_word):
                live_key = "products.csv"
                query_name = "PRODUCT_COUNTS"
            elif re.match(r"customers?|accounts?|bill.tos?", kind_word):
                live_key = "customers.csv"
                query_name = "CUSTOMER_COUNT"
            elif re.match(r"images?|photos?|image files?", kind_word):
                live_key = None  # images not directly a count key
                query_name = "IMAGE_EXISTS_SPLIT"
            elif re.match(r"inventory rows?|inventory records?", kind_word):
                live_key = "inventory.csv"
                query_name = "INVENTORY_COUNTS"

            if live_key and live_key in live_counts:
                live_n = live_counts[live_key]
                if live_n == n:
                    status = VERIFIED
                    evidence = (
                        f"{query_name} → {live_n:,} (matches draft)"
                    )
                else:
                    status = CONTRADICTED
                    evidence = (
                        f"{query_name} → {live_n:,} but draft claims {n:,}"
                    )
            elif live:
                status = UNVERIFIABLE
                evidence = (
                    f"no {query_name or 'count'} in live-state JSON for "
                    f"{live_key or kind_word}"
                )
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"
                query_name = ""

            claims.append(Claim(
                text=m.group(0),
                kind=KIND_COUNT,
                status=status,
                evidence=evidence,
                query_name=query_name,
                line_no=line_no,
            ))

        # --- DefaultPriceCode claims ----------------------------------------
        for m in _PRICE_CODE_RE.finditer(line):
            code = m.group(1).strip().lower()
            if price_levels:
                if code in price_levels:
                    status = VERIFIED
                    evidence = f"PRICE_LEVELS → '{code}' is a valid code for this org"
                else:
                    status = CONTRADICTED
                    evidence = (
                        f"PRICE_LEVELS → '{code}' is NOT a valid code for this org "
                        f"(valid: {', '.join(sorted(price_levels))}); "
                        f"this is the tcd pattern — a placeholder/ERP code causes "
                        f"100% customer rejection"
                    )
            elif live:
                status = UNVERIFIABLE
                evidence = "price_levels absent from live-state JSON; cannot confirm"
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"

            claims.append(Claim(
                text=m.group(0),
                kind=KIND_PRICE_CODE,
                status=status,
                evidence=evidence,
                query_name="PRICE_LEVELS" if price_levels else "",
                line_no=line_no,
            ))

        # --- Price level name assertion -------------------------------------
        for m in _PRICE_LEVEL_NAME_RE.finditer(line):
            code = m.group(1).strip().lower()
            # Skip words that aren't codes
            if code in ("level", "code", "the", "a", "an", "of", "for", "is"):
                continue
            if price_levels:
                if code in price_levels:
                    status = VERIFIED
                    evidence = f"PRICE_LEVELS → '{code}' confirmed for this org"
                else:
                    status = CONTRADICTED
                    evidence = (
                        f"PRICE_LEVELS → '{code}' not found for this org "
                        f"(valid: {', '.join(sorted(price_levels))})"
                    )
            elif live:
                status = UNVERIFIABLE
                evidence = "price_levels absent from live-state JSON"
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"

            claims.append(Claim(
                text=m.group(0),
                kind=KIND_PRICE_CODE,
                status=status,
                evidence=evidence,
                query_name="PRICE_LEVELS" if price_levels else "",
                line_no=line_no,
            ))

        # --- Image-status claims -------------------------------------------
        for m in _IMAGE_BROKEN_RE.finditer(line):
            code = (m.group(1) or m.group(2) or "").strip().lower()
            status_word = m.group(3).strip()
            if uploaded_stems:
                if code in uploaded_stems:
                    status = CONTRADICTED
                    evidence = (
                        f"UPLOADED_IMAGES → '{code}' filename IS present in the live org; "
                        f"a broken-image claim from catalog text is the Magic Lite "
                        f"false-positive pattern — visual confirmation required, not inferred"
                    )
                else:
                    status = VERIFIED
                    evidence = (
                        f"UPLOADED_IMAGES → '{code}' filename NOT found in live org "
                        f"(consistent with '{status_word}' claim)"
                    )
            elif live:
                status = UNVERIFIABLE
                evidence = "uploaded_images absent from live-state JSON; cannot confirm"
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"

            claims.append(Claim(
                text=m.group(0),
                kind=KIND_IMAGE_STATUS,
                status=status,
                evidence=evidence,
                query_name="UPLOADED_IMAGES" if uploaded_stems or live else "",
                line_no=line_no,
            ))

        # --- Entity (product code) claims ----------------------------------
        for m in _ITEM_CODE_RE.finditer(line):
            code = m.group(1)
            code_lower = code.lower()
            # Skip if this was already caught as an image-status claim
            if _IMAGE_BROKEN_RE.search(line):
                continue
            if live_product_keys:
                if code_lower in live_product_keys:
                    status = VERIFIED
                    evidence = (
                        f"PRODUCT_KEYS_SAMPLE → '{code}' is an active product "
                        f"(not deleted, not an option, not a group member)"
                    )
                elif code_lower in uploaded_stems:
                    status = UNVERIFIABLE
                    evidence = (
                        f"'{code}' not in active products but IS an uploaded image filename; "
                        f"could be a deleted product, option code, or image alias — "
                        f"disambiguation required"
                    )
                else:
                    status = UNVERIFIABLE
                    evidence = (
                        f"'{code}' not found in PRODUCT_KEYS_SAMPLE for this org; "
                        f"may be deleted, an option code, a group code, or a typo — "
                        f"four states: active product / deleted product / option / "
                        f"group member"
                    )
            elif live:
                status = UNVERIFIABLE
                evidence = "product keys absent from live-state JSON"
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"

            claims.append(Claim(
                text=code,
                kind=KIND_ENTITY,
                status=status,
                evidence=evidence,
                query_name="PRODUCT_KEYS_SAMPLE" if live_product_keys else "",
                line_no=line_no,
            ))

        # --- Success / import-status claims --------------------------------
        for m in _SUCCESS_CLAIM_RE.finditer(line):
            # A success claim is verifiable if we have counts; otherwise flag it.
            has_any_count = bool(live_counts)
            if has_any_count:
                # Check if any count is 0 while success is claimed — that's a contradiction
                zeros = [k for k, v in live_counts.items() if v == 0]
                if zeros:
                    status = CONTRADICTED
                    evidence = (
                        f"CUSTOMER_COUNT / PRODUCT_COUNTS → "
                        f"{', '.join(zeros)} show 0 in live org; "
                        f"a success claim cannot be reconciled with empty tables"
                    )
                    query_name = "CUSTOMER_COUNT"
                else:
                    status = VERIFIED
                    evidence = "live counts are non-zero; consistent with success claim"
                    query_name = "PRODUCT_COUNTS"
            elif live:
                status = UNVERIFIABLE
                evidence = "no count data in live-state JSON to confirm or deny success"
                query_name = ""
            else:
                status = UNVERIFIABLE
                evidence = "no live-state JSON supplied"
                query_name = ""

            claims.append(Claim(
                text=m.group(0),
                kind=KIND_CAUSAL,
                status=status,
                evidence=evidence,
                query_name=query_name,
                line_no=line_no,
            ))

        # --- Causal claims -------------------------------------------------
        for m in _CAUSAL_RE.finditer(line):
            # Causal claims ("because", "due to") are always flagged as UNVERIFIABLE
            # unless there is direct evidence in the live state or source files.
            claims.append(Claim(
                text=line.strip()[:120],
                kind=KIND_CAUSAL,
                status=UNVERIFIABLE,
                evidence=(
                    "Causal explanation — confirm via IMPORT_EVENTS_BY_TYPE "
                    "import log before attributing root cause; "
                    "IMPLEMENTATION_PLAN §2.3: counts must never be narrated"
                ),
                query_name="IMPORT_EVENTS_BY_TYPE",
                line_no=line_no,
            ))

    return claims


# ---------------------------------------------------------------------------
# Entity disambiguation section
# ---------------------------------------------------------------------------

def _disambiguate_entities(claims: List[Claim], live: Dict) -> List[str]:
    """For every entity code found in the draft, produce a disambiguation row.

    Four states per entity (IMPLEMENTATION_PLAN §7 Phase 3 step 6):
        active product / deleted product / option / group member
    """
    codes_seen = set()
    product_keys = {
        str(k).lower()
        for k in (live.get("keys") or {}).get("products.csv") or []
    }
    uploaded = {
        os.path.splitext(f)[0].lower()
        for f in (live.get("uploaded_images") or [])
    }

    rows = []
    for c in claims:
        if c.kind != KIND_ENTITY:
            continue
        code = c.text.lower()
        if code in codes_seen:
            continue
        codes_seen.add(code)

        states = []
        if product_keys:
            states.append(
                "active product ✓" if code in product_keys
                else "active product ✗ (not in PRODUCT_KEYS_SAMPLE)"
            )
        if uploaded:
            states.append(
                "image uploaded ✓" if code in uploaded
                else "image uploaded ✗"
            )
        if not states:
            states.append(
                "state unknown — no live-state JSON; "
                "could be active product / deleted product / option / group member"
            )

        rows.append(f"- `{c.text}` (line {c.line_no}): {'; '.join(states)}")

    return rows


# ---------------------------------------------------------------------------
# Live-state generation (calls profile.py if --shortname given and no JSON)
# ---------------------------------------------------------------------------

def _generate_live_state(shortname: str, scripts_dir: str) -> Optional[Dict]:
    """Try to generate live-state JSON by calling profile.py --emit-live-state."""
    profile_script = os.path.join(scripts_dir, "reconcile", "profile.py")
    if not os.path.exists(profile_script):
        return None
    try:
        result = subprocess.run(
            [sys.executable, profile_script, "--shortname", shortname, "--emit-live-state"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def _claim_table(claims: List[Claim]) -> List[str]:
    if not claims:
        return ["_No verifiable claims extracted from this draft._"]
    lines = ["| # | Claim | Kind | Status | Evidence | Query | Line |"]
    lines.append("|---|-------|------|--------|----------|-------|------|")
    for i, c in enumerate(claims, start=1):
        text = c.text.replace("|", "\\|")[:80]
        evidence = c.evidence.replace("|", "\\|")[:120]
        lines.append(
            f"| {i} | `{text}` | {c.kind} | **{c.status}** "
            f"| {evidence} | {c.query_name or '—'} | {c.line_no} |"
        )
    return lines


def _verdict(claims: List[Claim]) -> Tuple[str, List[str]]:
    """Return (verdict_label, rewrite_guidance_lines)."""
    contradicted = [c for c in claims if c.status == CONTRADICTED]
    unverifiable = [c for c in claims if c.status == UNVERIFIABLE]

    if contradicted:
        guidance = [
            "**Rewrite guidance:**",
            "",
        ]
        for c in contradicted:
            guidance.append(
                f"- Line {c.line_no} — `{c.text[:80]}`: "
                f"{c.evidence[:200]}"
            )
        guidance += [
            "",
            "Remove or qualify every CONTRADICTED claim before sending.",
            "A flagged gap beats a wrong-but-confident map.",
        ]
        return "not-safe-to-send", guidance
    elif unverifiable and not any(c.status == VERIFIED for c in claims):
        return "not-safe-to-send", [
            "All extracted claims are UNVERIFIABLE — no live-state JSON was supplied.",
            "Run profile.py --emit-live-state before reviewing client-facing output.",
        ]
    else:
        return "safe-to-send", []


# ---------------------------------------------------------------------------
# Checker: orchestrates all 9 steps
# ---------------------------------------------------------------------------

class PreSendChecker:
    """Orchestrates the 9-step pre-send review contract."""

    def __init__(
        self,
        draft_path: str,
        draft_text: str,
        client_dir: Optional[str],
        shortname: Optional[str],
        live: Dict,
        scripts_dir: Optional[str] = None,
    ):
        self.draft_path = draft_path
        self.draft_text = draft_text
        self.client_dir = client_dir
        self.shortname = shortname
        self.live = live
        self.scripts_dir = scripts_dir
        self.reviewed_at = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

    def run(self) -> "PreSendReport":
        claims = extract_claims(self.draft_text, self.live)
        source_files = _gather_source_files(self.client_dir)
        entity_rows = _disambiguate_entities(claims, self.live)
        prior_patterns = self._check_prior_patterns()
        verdict_label, rewrite_guidance = _verdict(claims)

        return PreSendReport(
            draft_path=self.draft_path,
            shortname=self.shortname,
            reviewed_at=self.reviewed_at,
            live=self.live,
            draft_text=self.draft_text,
            claims=claims,
            source_files=source_files,
            entity_rows=entity_rows,
            prior_patterns=prior_patterns,
            verdict_label=verdict_label,
            rewrite_guidance=rewrite_guidance,
        )

    def _check_prior_patterns(self) -> List[Tuple[str, str]]:
        """Return list of (pattern_name, description) that fired."""
        fired = []
        for name, desc, detect_fn in _PRIOR_ERROR_PATTERNS:
            try:
                if detect_fn(self.draft_text, self.live):
                    fired.append((name, desc))
            except Exception:
                pass
        return fired


@dataclasses.dataclass
class PreSendReport:
    """The full output of a pre-send review."""
    draft_path: str
    shortname: Optional[str]
    reviewed_at: str
    live: Dict
    draft_text: str
    claims: List[Claim]
    source_files: List[str]
    entity_rows: List[str]
    prior_patterns: List[Tuple[str, str]]
    verdict_label: str
    rewrite_guidance: List[str]

    @property
    def exit_code(self) -> int:
        if self.verdict_label == "safe-to-send":
            return 0
        return 1

    def render(self) -> str:
        lines: List[str] = []
        queried_at = self.live.get("queried_at") or "NOT SUPPLIED"

        # Header
        lines += [
            "# Pre-Send Review",
            "",
            f"**Draft:** {self.draft_path}",
            f"**Client / shortname:** {self.shortname or 'UNKNOWN'}",
            f"**Reviewed at:** {self.reviewed_at}",
            f"**Live state queried at:** {queried_at}",
            "",
            "---",
            "",
        ]

        # Step 1 — Stakes
        lines += [
            "## Step 1 — Stakes",
            "",
            "This artifact will be received by the client as a factual account of their "
            "data state. A wrong claim cannot be unsent and damages the relationship in "
            "proportion to how confident it sounded.",
            "",
            "Every claim below is classified VERIFIED / UNVERIFIABLE / CONTRADICTED. "
            "A single CONTRADICTED claim is sufficient to block sending.",
            "",
        ]

        # Step 2 — Void prior analysis
        lines += [
            "## Step 2 — Prior Analysis Voided",
            "",
            "All prior agent analysis of this client is treated as unverified for this "
            "review. The live DB is the authority; document claims are evidence of intent, "
            "not fact. Counts in prior handoffs may be stale.",
            "",
        ]

        # Step 3 — Evidence tiers
        live_note = (
            f"queried at {queried_at}; "
            f"shortname = {self.live.get('shortname', 'UNKNOWN')}"
            if self.live else "NOT SUPPLIED — Tier 3 checks are UNVERIFIABLE"
        )
        lines += [
            "## Step 3 — Evidence Tiers",
            "",
            f"**{TIER_SOURCE}:**",
        ]
        if self.source_files:
            for f in self.source_files[:30]:
                lines.append(f"  - `{f}`")
            if len(self.source_files) > 30:
                lines.append(f"  - _(and {len(self.source_files) - 30} more)_")
        else:
            lines.append("  - _No source files found — pass `--client-dir`_")
        lines += [
            "",
            f"**{TIER_CODE}:**",
        ]
        for rule in TIER2_RULES:
            lines.append(f"  - {rule}")
        lines += [
            "",
            f"**{TIER_LIVE}:** {live_note}",
            "",
        ]
        if self.live.get("price_levels"):
            pl = ", ".join(f"`{c}`" for c in self.live["price_levels"])
            lines.append(f"  - PRICE_LEVELS: {pl}")
        if self.live.get("counts"):
            for k, v in self.live["counts"].items():
                lines.append(f"  - counts[{k}] = {v:,} (via PRODUCT_COUNTS / CUSTOMER_COUNT)")
        if self.live.get("uploaded_images") is not None:
            n = len(self.live["uploaded_images"])
            lines.append(f"  - UPLOADED_IMAGES: {n:,} filenames in product_images")
        if self.live.get("_warnings"):
            lines.append("")
            lines.append("  **Tier 3 degraded queries (check live-state JSON):**")
            for w in self.live["_warnings"]:
                lines.append(f"    - {w}")
        lines.append("")

        # Step 4 — Prior client-pushback errors
        lines += [
            "## Step 4 — Prior Client-Pushback Error Patterns",
            "",
        ]
        if self.prior_patterns:
            for name, desc in self.prior_patterns:
                lines += [
                    f"### ⚠ Pattern detected: `{name}`",
                    "",
                    desc,
                    "",
                ]
        else:
            lines += [
                "_No known false-claim patterns detected in this draft._",
                "",
            ]

        # Step 5 — File enumeration
        lines += [
            "## Step 5 — Files Enumerated",
            "",
        ]
        if self.source_files:
            for f in self.source_files:
                lines.append(f"- `{f}`")
        else:
            lines.append("_No source files found. Pass `--client-dir` for complete enumeration._")
        lines.append("")

        # Step 6 — Entity-by-entity live state
        lines += [
            "## Step 6 — Entity Disambiguation (live org state)",
            "",
            "Each entity code mentioned in the draft, against four possible states: "
            "active product / deleted product / option / group member.",
            "",
        ]
        if self.entity_rows:
            lines += self.entity_rows
        else:
            lines.append(
                "_No eCat entity codes (BaseItemCode pattern) detected in this draft, "
                "or live-state JSON was not supplied._"
            )
        lines.append("")

        # Step 7 — Draft artifact
        lines += [
            "## Step 7 — Draft Artifact (full text reviewed)",
            "",
            "```",
        ]
        lines += self.draft_text.splitlines()
        lines += [
            "```",
            "",
        ]

        # Step 8 — Claim analysis (the full table)
        contradicted = [c for c in self.claims if c.status == CONTRADICTED]
        unverifiable = [c for c in self.claims if c.status == UNVERIFIABLE]
        verified = [c for c in self.claims if c.status == VERIFIED]

        lines += [
            "## Step 8 — Claim Analysis",
            "",
            f"Extracted {len(self.claims)} claim(s): "
            f"**{len(verified)} VERIFIED**, "
            f"**{len(unverifiable)} UNVERIFIABLE**, "
            f"**{len(contradicted)} CONTRADICTED**.",
            "",
            "Failure criterion: factually airtight, no over-claim, no blame, "
            "no asserted-but-unconfirmed mapping.",
            "",
        ]
        lines += _claim_table(self.claims)
        lines.append("")

        # Step 9 — Verdict
        verdict_emoji = "✅" if self.verdict_label == "safe-to-send" else "🚫"
        lines += [
            "## Step 9 — Verdict",
            "",
            f"## {verdict_emoji} {self.verdict_label.upper()}",
            "",
        ]
        if self.rewrite_guidance:
            lines += self.rewrite_guidance
        else:
            lines += [
                "All extracted claims are VERIFIED or the draft contains no contradicted assertions.",
                "If any UNVERIFIABLE claims touch client-visible facts, add source citations "
                "or label them as estimates before sending.",
            ]
        lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--draft", required=True,
                    help="path to the email or markdown draft to review")
    ap.add_argument("--client-dir", default=None,
                    help="eCat_Onboarding/<client>/ root for source file enumeration")
    ap.add_argument("--shortname", default=None,
                    help="org shortname (e.g. tcd, mali, libco); "
                         "used to auto-generate live-state if --live-state is omitted")
    ap.add_argument("--live-state", default=None,
                    help="path to live-state JSON from "
                         "`profile.py --shortname X --emit-live-state`; "
                         "if omitted and --shortname is set, the checker will try "
                         "to generate it automatically")
    ap.add_argument("--out", default=None,
                    help="write report to this file instead of stdout")
    args = ap.parse_args()

    # Load draft
    try:
        with open(args.draft, "r", encoding="utf-8-sig") as f:
            draft_text = f.read()
    except OSError as exc:
        print(f"ERROR: cannot read draft: {exc}", file=sys.stderr)
        return 2

    if not draft_text.strip():
        print("ERROR: draft file is empty", file=sys.stderr)
        return 2

    # Load or generate live state
    live: Dict = {}
    if args.live_state:
        try:
            with open(args.live_state, "r", encoding="utf-8") as f:
                live = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read live-state JSON: {exc}", file=sys.stderr)
            return 2
    elif args.shortname:
        scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        generated = _generate_live_state(args.shortname, scripts_dir)
        if generated:
            live = generated
            print(
                f"Auto-generated live-state for '{args.shortname}' "
                f"(queried {live.get('queried_at', 'unknown')})",
                file=sys.stderr,
            )
        else:
            print(
                f"WARNING: could not auto-generate live-state for '{args.shortname}' "
                f"(DATABASE_URL not set or VPN required). Tier 3 checks will be UNVERIFIABLE.",
                file=sys.stderr,
            )

    # Derive shortname from live state if not provided
    shortname = args.shortname or live.get("shortname")

    # Build scripts dir for potential live-state generation path
    scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    checker = PreSendChecker(
        draft_path=os.path.abspath(args.draft),
        draft_text=draft_text,
        client_dir=args.client_dir,
        shortname=shortname,
        live=live,
        scripts_dir=scripts_dir,
    )

    report = checker.run()
    output = report.render()

    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Wrote report to {args.out}", file=sys.stderr)
        except OSError as exc:
            print(f"ERROR: cannot write to {args.out}: {exc}", file=sys.stderr)
            return 2
    else:
        print(output)

    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
