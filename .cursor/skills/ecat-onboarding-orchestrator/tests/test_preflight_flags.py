"""Tests for preflight/flags.py — the archetype and applicability declarations.

Two properties matter more than the parsing:

1. **An undeclared subsystem stays checked.** Defaulting to "skip" would turn every
   half-filled profile into a silent pass, which is the failure this module prevents.
2. **A skip always names its cause.** `SKIP (flag: options none)` is auditable; a missing
   line is not.
"""
import pytest

from preflight.flags import (ARCHETYPES, FLAG_DISABLES, IMAGE_MODES, PRODUCT_LINES,
                             Profile, parse_profile)

SECTION = """# Client — eCat Client Profile

## Identity
- **Org shortname:** `acme`

## Archetype & applicability
- **Archetype:** standard
- **Product line:** ecat-ipad
- **Flags:** `pricing: n/a`, `options: none`, sample-catalog
- **File owner mode:** csv
- **Image mode:** ftp
- **Source cutover date:** 2025-07-08
- **Sub-brands:** none

## Contacts
- **Client:** someone
"""


@pytest.fixture
def profile(tmp_path):
    def _write(text):
        path = tmp_path / "CLIENT_PROFILE.md"
        path.write_text(text, encoding="utf-8")
        return parse_profile(path)
    return _write


def test_parses_every_declared_field(profile):
    p = profile(SECTION)
    assert p.declared is True
    assert p.shortname == "acme"
    assert p.archetype == "standard"
    assert p.product_lines == ["ecat-ipad"]
    assert p.flags == {"pricing:n/a", "options:none", "sample-catalog"}
    assert p.file_owner == "csv"
    assert p.image_mode == "ftp"
    assert p.cutover_date == "2025-07-08"
    assert p.sub_brands == []


def test_flag_disables_its_subsystem_with_a_reason(profile):
    p = profile(SECTION)
    assert p.applies("pricing") is False
    assert p.skip_reason("pricing") == "flag: pricing n/a"
    assert p.applies("options") is False
    assert p.skip_reason("options") == "flag: options none"


def test_undeclared_subsystems_still_apply(profile):
    """drf declares no customers flag, so the customer checks must still run."""
    p = profile(SECTION)
    assert p.applies("customers") is True
    assert p.applies("core") is True
    assert p.skip_reason("core") is None


def test_a_note_flag_switches_nothing_off(profile):
    """sample-catalog changes how a human reads the output, not which checks run."""
    p = profile(SECTION)
    assert "sample-catalog" in p.flags
    assert "sample-catalog" not in FLAG_DISABLES
    assert p.applies("core") and p.applies("inventory")


def test_image_mode_picks_exactly_one_image_path(profile):
    ftp = profile(SECTION)
    assert ftp.applies("images-local") is True
    assert ftp.applies("images-url") is False
    assert ftp.skip_reason("images-url") == "flag: images ftp"

    cdn = profile(SECTION.replace("**Image mode:** ftp", "**Image mode:** cdn-url"))
    assert cdn.applies("images-url") is True
    assert cdn.applies("images-local") is False

    both = profile(SECTION.replace("**Image mode:** ftp", "**Image mode:** both"))
    assert both.applies("images-url") and both.applies("images-local")


def test_missing_section_means_everything_applies(profile):
    p = profile("# Client\n\n## Identity\n- **Org shortname:** `acme`\n")
    assert p.declared is False
    assert p.shortname == "acme"
    for subsystem in ("core", "pricing", "options", "inventory", "customers",
                      "images-local", "images-url"):
        assert p.applies(subsystem), subsystem
    assert any("no '## Archetype & applicability' section" in m
               for _hint, m in p.issues())


def test_unreadable_profile_degrades_instead_of_raising():
    p = parse_profile("/nonexistent/CLIENT_PROFILE.md")
    assert p.declared is False
    assert p.applies("pricing") is True


def test_undeclared_helper_applies_everything():
    p = Profile.undeclared()
    assert all(p.applies(s) for s in ("core", "pricing", "options", "images-url"))


def test_template_placeholders_never_disable_a_check(profile):
    """A copied-but-unfilled template must read as undeclared, not as five real flags.

    Left unhandled, the choice list on the Flags line parses as `pricing: n/a` and
    friends and silently switches off four subsystems.
    """
    p = profile("""## Archetype & applicability
- **Archetype:** standard | snowflake | churned
- **Product line:** ecat-ipad | eol | sales-portal
- **Flags:** {`pricing: n/a`, `options: none`, or "none"}
- **File owner mode:** generator | csv | mixed
- **Image mode:** ftp | cdn-url | both
- **Source cutover date:** {YYYY-MM-DD}
- **Sub-brands:** {e.g. ML,NSL — or "none"}
""")
    assert p.disabled_subsystems == set()
    assert p.archetype is None and p.product_lines == []
    assert p.flags == set()
    assert p.cutover_date is None


def test_the_real_template_and_real_clients_parse(client_profiles):
    """The shipped template must disable nothing, and every client must be declared.

    This runs against the actual profiles rather than a fixture, because the parser's
    only job is to read *those* files and they are hand-maintained.
    """
    if not client_profiles:
        pytest.skip("eCat_Onboarding profiles not present in this checkout")
    for path in client_profiles:
        p = parse_profile(path)
        if path.parent.name == "_Template":
            assert p.disabled_subsystems == set(), "the template must disable nothing"
            continue
        assert p.declared is True, f"{path.parent.name} has no archetype section"
        assert p.archetype in ARCHETYPES, path.parent.name
        assert p.product_lines, path.parent.name
        assert all(line in PRODUCT_LINES for line in p.product_lines), path.parent.name
        assert p.image_mode in IMAGE_MODES, path.parent.name
        assert all("unrecognized flag" not in m for _h, m in p.issues()), path.parent.name


def test_placeholder_cutover_date_reads_as_undeclared(profile):
    """"unknown" is not a date. It must warn, not be accepted as a declared value."""
    p = profile(SECTION.replace("**Source cutover date:** 2025-07-08",
                                "**Source cutover date:** unknown"))
    assert p.cutover_date is None
    assert any("cutover date" in m for _hint, m in p.issues())


def test_multiple_product_lines(profile):
    """Lib & Co runs the iPad build and eOL together; each line has its own gate set."""
    p = profile(SECTION.replace("**Product line:** ecat-ipad",
                                "**Product line:** ecat-ipad, eol"))
    assert p.product_lines == ["ecat-ipad", "eol"]
    assert p.issues() == [] or all("product line" not in m for _h, m in p.issues())


def test_sub_brands_parsed_for_mali_shape(profile):
    p = profile(SECTION.replace("**Sub-brands:** none", "**Sub-brands:** ML,NSL"))
    assert p.sub_brands == ["ML", "NSL"]
    assert "sub-brands=ML,NSL" in p.summary()


def test_snowflake_annotates_and_never_blocks(profile):
    """The whole design rule of Axis 1: an unusual client runs the same gates."""
    p = profile(SECTION
                .replace("**Archetype:** standard", "**Archetype:** snowflake")
                .replace("- **Flags:** `pricing: n/a`, `options: none`, sample-catalog",
                         "- **Flags:** churned, manual-review"))
    assert p.archetype == "snowflake"
    assert p.disabled_subsystems == {"images-url"}  # only the image-mode split
    assert all("unrecognized flag" not in m for _hint, m in p.issues())


def test_unrecognized_flag_is_reported_rather_than_silently_ignored(profile):
    p = profile(SECTION.replace("- **Flags:** `pricing: n/a`, `options: none`, sample-catalog",
                                "- **Flags:** `prcing: n/a`"))
    messages = [m for _hint, m in p.issues()]
    assert any("unrecognized flag" in m and "prcing:n/a" in m for m in messages)
    assert p.applies("pricing") is True  # a typo must not switch anything off


def test_bad_enum_values_warn(profile):
    p = profile(SECTION
                .replace("**Archetype:** standard", "**Archetype:** bespoke")
                .replace("**File owner mode:** csv", "**File owner mode:** both")
                .replace("**Image mode:** ftp", "**Image mode:** sftp"))
    messages = " ".join(m for _hint, m in p.issues())
    assert "archetype 'bespoke'" in messages
    assert "file owner 'both'" in messages
    assert "image mode 'sftp'" in messages


def test_normalization_is_forgiving_about_formatting(profile):
    p = profile(SECTION.replace("- **Flags:** `pricing: n/a`, `options: none`, sample-catalog",
                                "- **Flags:** Pricing:N/A; `OPTIONS : none`"))
    assert p.flags == {"pricing:n/a", "options:none"}


def test_summary_names_undeclared_fields_explicitly():
    assert "archetype=UNDECLARED" in Profile.undeclared().summary()


def test_vocabularies_are_the_ones_the_plan_defines():
    assert set(ARCHETYPES) == {"standard", "snowflake", "churned"}
    assert set(PRODUCT_LINES) == {"ecat-ipad", "eol", "sales-portal"}
    assert set(IMAGE_MODES) == {"ftp", "cdn-url", "both"}
