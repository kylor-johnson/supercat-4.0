"""111 Mercer's budgeted per-field escape hatches. 3 of 3 used.

At budget. A FOURTH transform is not permitted here -- the rule is that beyond
three, the library is missing a primitive: file it against `ecatlib` and the
next client gets it free. Two were filed and added while writing this mapping
(`values.parse_int`, `values.round_decimals`), which is the flywheel working.

All three below are string surgery over THIS client's SKU convention (a `-S`
suffix meaning "sample of the item without it"). None generalise as written.
"""

import re

SAMPLE_SUFFIX = '-S'


def image_filename_from_code(code):
    """`GL9190-S` -> `gl9190-s.jpg`.

    A CONVENTION WE CHOSE, not filenames the client supplied (BUILD_NOTES,
    still open with Ryan). If his files are named anything else, all 102 values
    are wrong and every image silently fails to match -- pebl ran 18 days of
    `.jpg.jpg` at clean import tier. Confirm before the bulk upload; a clean
    import will not catch it.
    """
    return '%s.jpg' % (code or '').strip().lower()


def sample_counterpart(code):
    """The other half of the bolt/sample pair: `GK9195` <-> `GK9195-S`.

    Returns the counterpart CODE only. Whether that code actually exists in the
    file is decided in the mapping by looking it up, because a RelatedItems
    value pointing at a SKU that is not in the catalogue is a dangling
    reference (BUILD_SPEC A3), not a related item.
    """
    code = (code or '').strip()
    if code.endswith(SAMPLE_SUFFIX):
        return code[:-len(SAMPLE_SUFFIX)]
    return code + SAMPLE_SUFFIX


def design_family_key(description, code):
    """Group SKUs that differ only by COLORWAY into one Related Items family.

    The family key is the design name, which is segment 2 of the description,
    with a trailing "MURAL" normalised away -- the source spells the same design
    both ways (`DEEP SEA` and `DEEP SEA MURAL`).

    Samples and full items are kept in SEPARATE families: a sample's peers are
    the other samples. The bolt<->sample link is `RelatedItems2`, a different
    relationship on a different tab.

    NOTE this normalisation is for GROUPING ONLY. The client's own `Design`
    DISPLAY value is inconsistent about it -- GK9194 drops "Mural", GC9193
    keeps it -- so `Design` is an editorial value that is carried forward, not
    derived. Grouping and labelling are two different questions.
    """
    segments = [s.strip() for s in (description or '').split(' - ')]
    design = segments[1] if len(segments) > 1 else ''
    design = re.sub(r'\s+MURAL$', '', design.upper()).strip()
    return '%s|%s' % (design, (code or '').strip().endswith(SAMPLE_SUFFIX))
