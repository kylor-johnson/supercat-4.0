#!/usr/bin/env python3
"""Read a client's archetype and applicability flags out of CLIENT_PROFILE.md.

IMPLEMENTATION_PLAN.md 2.4 splits client variation onto three independent axes:

  Axis 1  handling archetype   standard | snowflake | churned
  Axis 2  product line         ecat-ipad | eol | sales-portal
  Axis 3  applicability flags  pricing: n/a, options: none, ...

Axis 1 annotates and never gates — nothing in the corpus supports treating an unusual
client as un-automatable. Axis 3 *skips* checks, and a skipped check must print
`SKIP (flag: pricing n/a)` rather than passing silently, because an unexplained
absence is how a deliberate exclusion turns into next quarter's argument.

The profile is hand-maintained and drifts, so this parser only reads the *declared
policy* fields — never counts. Counts come from the live DB (Phase 2 reconciler).
"""
import re

SECTION = "Archetype & applicability"

ARCHETYPES = ("standard", "snowflake", "churned")
PRODUCT_LINES = ("ecat-ipad", "eol", "sales-portal")
# "mixed" is legitimate when different deliverables have different owners (Dorell's
# stories.csv is generator-owned while its products.csv is hand-edited). What is never
# legitimate is one deliverable with two owners — see IMPLEMENTATION_PLAN.md 5.2.
FILE_OWNERS = ("generator", "csv", "mixed")
IMAGE_MODES = ("ftp", "cdn-url", "both")

# Subsystems a check can belong to. A check in a disabled subsystem reports SKIP.
SUBSYSTEMS = (
    "core", "pricing", "inventory", "options", "customers", "stories",
    "images", "images-local", "images-url",
)

# Axis 3 flag -> subsystems it switches off. Verified sources for each in 2.4.
FLAG_DISABLES = {
    "pricing:n/a": {"pricing"},
    "inventory:n/a": {"inventory"},
    "options:none": {"options"},
    "customers:n/a": {"customers"},
    "stories:none": {"stories"},
}

# Image mode decides which of the two image paths is even meaningful.
IMAGE_MODE_DISABLES = {
    "ftp": {"images-url"},
    "cdn-url": {"images-local"},
    "both": set(),
}

# Flags that are notes rather than switches — they change how a human reads the
# output, not which checks run. `churned` and `manual-review` are deliberately inert:
# 2.4's design rule is that an unusual or departed client still runs the same gates,
# because the CopperSmith failures were ordinary bugs in an unusual costume.
NOTE_FLAGS = {"sample-catalog", "sub-brands", "churned", "manual-review"}


def _normalize(token):
    """`pricing: n/a` / `Pricing:N/A` / `` `options: none` `` -> `pricing:n/a`."""
    token = token.strip().strip("`").strip().lower()
    token = re.sub(r"\s*:\s*", ":", token)
    return re.sub(r"\s+", " ", token)


def _is_placeholder(value):
    """True for un-filled template text: a `a | b | c` choice list or a `{hint}`.

    Copying the template and not filling a line must read as *undeclared*, never as a
    declaration. Left unhandled, `_Template`'s own Flags line parses as four real
    applicability flags and silently switches off pricing, inventory, options, and
    stories — the exact silent-pass failure this module exists to prevent.
    """
    return "|" in value or "{" in value or "}" in value


class Profile:
    """Declared policy for one client. Never holds counts."""

    def __init__(self, shortname=None, archetype=None, product_lines=None, flags=None,
                 file_owner=None, image_mode=None, cutover_date=None, sub_brands=None,
                 path=None, declared=False):
        self.shortname = shortname
        self.archetype = archetype
        # A client can be on more than one product line at once — Lib & Co runs the eCat
        # iPad build and eOL together, and each line has its own gate set.
        self.product_lines = list(product_lines or ())
        self.flags = set(flags or ())
        self.file_owner = file_owner
        self.image_mode = image_mode
        self.cutover_date = cutover_date
        self.sub_brands = list(sub_brands or ())
        self.path = path
        self.declared = declared

    @classmethod
    def undeclared(cls, path=None):
        """Everything applicable. Used when no profile is supplied."""
        return cls(path=path, declared=False)

    @property
    def disabled_subsystems(self):
        out = set()
        for flag in self.flags:
            out |= FLAG_DISABLES.get(flag, set())
        if self.image_mode:
            out |= IMAGE_MODE_DISABLES.get(self.image_mode, set())
        return out

    def skip_reason(self, subsystem):
        """Human-readable reason this subsystem is skipped, or None if it applies."""
        if self.image_mode and subsystem in IMAGE_MODE_DISABLES.get(self.image_mode, set()):
            return f"flag: images {self.image_mode}"
        for flag in sorted(self.flags):
            if subsystem in FLAG_DISABLES.get(flag, set()):
                return f"flag: {flag.replace(':', ' ')}"
        return None

    def applies(self, subsystem):
        return self.skip_reason(subsystem) is None

    def summary(self):
        bits = [f"archetype={self.archetype or 'UNDECLARED'}"]
        bits.append(f"line={','.join(self.product_lines) or 'UNDECLARED'}")
        if self.flags:
            bits.append(f"flags={','.join(sorted(self.flags))}")
        if self.file_owner:
            bits.append(f"owner={self.file_owner}")
        if self.image_mode:
            bits.append(f"images={self.image_mode}")
        if self.cutover_date:
            bits.append(f"cutover={self.cutover_date}")
        if self.sub_brands:
            bits.append(f"sub-brands={','.join(self.sub_brands)}")
        return " | ".join(bits)

    def issues(self):
        """Problems with the declaration itself, as (severity_hint, message) pairs."""
        out = []
        if not self.declared:
            out.append((
                "warn",
                f"CLIENT_PROFILE.md has no '## {SECTION}' section — every check is "
                f"treated as applicable. Declare the archetype, product line, and "
                f"applicability flags so intentional exclusions read as SKIP rather "
                f"than as passes.",
            ))
            return out
        if self.archetype not in ARCHETYPES:
            out.append(("warn", f"archetype {self.archetype!r} not one of {ARCHETYPES}"))
        if not self.product_lines:
            out.append(("warn", f"no product line declared; expected one or more of "
                                f"{PRODUCT_LINES}"))
        for line in self.product_lines:
            if line not in PRODUCT_LINES:
                out.append((
                    "warn", f"product line {line!r} not one of {PRODUCT_LINES}"))
        if self.file_owner and self.file_owner not in FILE_OWNERS:
            out.append(("warn", f"file owner {self.file_owner!r} not one of {FILE_OWNERS}"))
        if self.image_mode and self.image_mode not in IMAGE_MODES:
            out.append(("warn", f"image mode {self.image_mode!r} not one of {IMAGE_MODES}"))
        if not self.cutover_date:
            out.append((
                "warn",
                "no source-data cutover date declared — pre-cutover POC rows keep "
                "re-entering analysis as if they were real (2.4, Open Decision 4)",
            ))
        unknown = {
            f for f in self.flags
            if f not in FLAG_DISABLES and f.split(":")[0] not in NOTE_FLAGS
        }
        if unknown:
            out.append((
                "warn",
                f"unrecognized flag(s) {sorted(unknown)} — they will not skip anything. "
                f"Known switches: {sorted(FLAG_DISABLES)}",
            ))
        return out


def _field(text, label):
    match = re.search(
        rf"^\s*[-*]\s*\*\*{re.escape(label)}:?\*\*\s*(.+)$", text, re.M | re.I)
    return match.group(1).strip() if match else None


def _section_text(text):
    match = re.search(
        rf"^##\s+{re.escape(SECTION)}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return match.group(1) if match else None


def parse_profile(path):
    """Parse CLIENT_PROFILE.md. A missing section yields an undeclared Profile."""
    try:
        text = open(path, "r", encoding="utf-8").read()
    except OSError:
        return Profile.undeclared(path=path)

    shortname = _field(text, "Org shortname")
    if shortname:
        shortname = shortname.strip("`").split()[0].strip("`")

    section = _section_text(text)
    if section is None:
        return Profile(shortname=shortname, path=path, declared=False)

    raw_flags = _field(section, "Flags") or ""
    if _is_placeholder(raw_flags):
        raw_flags = ""
    flags = {
        _normalize(tok) for tok in re.split(r"[,;]", raw_flags) if _normalize(tok)
    }
    flags.discard("none")
    flags.discard("n/a")

    sub_brands_raw = _field(section, "Sub-brands") or ""
    if _is_placeholder(sub_brands_raw):
        sub_brands_raw = ""
    sub_brands = [
        t.strip().strip("`") for t in re.split(r"[,;]", sub_brands_raw)
        if t.strip() and _normalize(t) not in ("none", "n/a")
    ]

    # "unknown"/"tbd" must read as undeclared, not as a declared value, so the profile
    # warns about them instead of quietly accepting a placeholder.
    nullish = ("", "none", "n/a", "unknown", "tbd", "todo")

    def norm_opt(label):
        value = _field(section, label)
        if value is None or _is_placeholder(value):
            return None
        value = _normalize(value)
        return None if value in nullish else value

    raw_lines = _field(section, "Product line") or ""
    if _is_placeholder(raw_lines):
        raw_lines = ""
    product_lines = [
        _normalize(tok) for tok in re.split(r"[,;+]", raw_lines) if _normalize(tok)
    ]

    return Profile(
        shortname=shortname,
        archetype=norm_opt("Archetype"),
        product_lines=[l for l in product_lines if l not in ("none", "n/a")],
        flags=flags,
        file_owner=norm_opt("File owner mode"),
        image_mode=norm_opt("Image mode"),
        cutover_date=norm_opt("Source cutover date"),
        sub_brands=sub_brands,
        path=path,
        declared=True,
    )
