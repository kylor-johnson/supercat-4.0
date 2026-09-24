"""ecatlib — the twelve primitives BUILD_SPEC §2 found hiding in ~60 scripts.

Extracted from the three largest independent builds (Legrand 1,537 lines,
libco 1,277, tcs 656), which each reimplement the same twelve operations.

**The primitives are shared; the DIALECT is config.** The three builds disagree
on output format, not just on style, so every divergent primitive takes an
explicit dialect and `values.LEGRAND` is byte-exact with `build_ecat_files.py`.
See values.py for the divergence table and the two suspected live defects.

Field lengths and enums are NOT here - they are generated into
`preflight/limits_generated.py` from supercat_server. Callers pass limits in.

    1  money            values.parse_money
    2  weight           values.parse_weight_lb
    3  dimensions       values.build_dimensions
    4  booleans         values.to_boolean
    5  dates            values.normalize_date
    6  LongDesc trunc   desc.build_long_desc / build_short_desc
    7  text hygiene     values.clean_text / clean_na / clean_lookup / clean_country
    8  RelatedItems     related.build_related_items / merge_related
    9  variant grouping related.variant_key_by_name / variant_key_by_sku_suffix
   10  taxonomy         carryforward.rollup_taxonomy
   11  CSV IO           csvio.read_rows / write_rows
   12  carry-forward    carryforward.load_carryforward / apply_carryforward
"""

from . import values, desc, related, carryforward, csvio  # noqa: F401

from .values import (  # noqa: F401
    LEGRAND, LIBCO, TCS,
    clean_text, clean_na, clean_lookup, clean_country, split_first,
    parse_money, has_float_tail, parse_weight_lb, build_dimensions,
    to_boolean, normalize_date, clean_integer, parse_int, round_decimals, strip_float_tail,
)
from .desc import (  # noqa: F401
    truncate_word_boundary, find_token_span, build_long_desc, build_short_desc,
)
from .related import (  # noqa: F401
    variant_key_by_name, variant_key_by_sku_suffix, group_families,
    build_related_items, parse_related_items, merge_related,
)
from .carryforward import (  # noqa: F401
    load_carryforward, apply_carryforward, diff_against_previous, diff_key_for,
    rollup_taxonomy,
)
from .csvio import (  # noqa: F401
    read_rows, read_table, write_rows, write_table, sniff_bytes_equal,
)
