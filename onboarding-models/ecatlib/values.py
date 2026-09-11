"""Value primitives: money, weight, dimensions, booleans, dates, text hygiene.

## Why every function takes a dialect

BUILD_SPEC §2 lists twelve primitives that Legrand, libco and tcs each reimplement,
and reads as though extraction were mechanical. It is not. The three
implementations **disagree on output**, not just on style:

    money    leg  "4058.00"   always 2dp
             lib  "4058"      integer dollars drop the .00
             tcs  "4058.00"   passthrough after stripping $ and ,

    boolean  leg  "Y" / ""    eCat boolean FILTERS only match Y/y/T/t/1-9
             lib  "Yes"/"No"  passthrough

    weight   leg  unit-aware  "500 g" -> "1.102311"
             lib  first number "500 g" -> "500"        (453x wrong if g appears)

Merging those into one function silently rewrites three clients' files. So the
divergence is preserved as an explicit, named `dialect`, chosen per client in
config — never guessed. `LEGRAND` is byte-exact with `build_ecat_files.py`, which
is what makes the acceptance test possible.

Two of the divergences look like live defects rather than legitimate variation;
they are flagged in the docstrings and must be raised with the client, not
"fixed" here.
"""

import re

LEGRAND = 'legrand'
LIBCO = 'libco'
TCS = 'tcs'

# Source null tokens. Legrand's files use these interchangeably with blank.
NULL_TOKENS = ('', '#N/A', 'N/A', '0')

_WHITESPACE_RE = re.compile(r'\s+')
_NUMERIC_CLEAN_RE = re.compile(r'[^0-9.\-]')


# --- 7. text hygiene -------------------------------------------------------

def clean_text(v):
    """Collapse all whitespace to single spaces and trim.

    The KB bans LF/CR inside product-file data; an embedded newline breaks the
    row. Collapsing defensively is cheaper than diagnosing it after import.
    """
    if v is None:
        return ''
    return _WHITESPACE_RE.sub(' ', str(v)).strip()


def clean_na(v, null_tokens=NULL_TOKENS):
    """Trim, and map the source's null tokens to empty.

    NOTE `'0'` is treated as null. That is right for Legrand's source, where 0
    means "not supplied" in text columns — and WRONG for any column where zero
    is a real value (a quantity, a price of zero). Never route a numeric column
    through this.
    """
    v = (v or '').strip()
    return '' if v in null_tokens else v


def clean_lookup(v, fixes, null_tokens=NULL_TOKENS):
    """Trim, null-map, then apply an explicit spelling-fix table.

    Generalises Legrand's `clean_category` / `normalize_finish`, which are the
    same function over different tables. The table stays per-client config: the
    fixes encode client decisions ("Night Lighs" -> "Night Lights"), not a rule.

    These values become iPad filter facets, so an unmerged typo ships as a
    duplicate chip.
    """
    v = clean_na(v, null_tokens)
    return fixes.get(v, v)


def clean_country(v, null_tokens=('0', '#N/A', '')):
    """Country of Origin: trim and null-map. Legrand keeps 'N/A' as a value
    here, so the default null set differs from `clean_na`'s - that asymmetry is
    deliberate and is preserved."""
    v = (v or '').strip()
    return '' if v in null_tokens else v


# --- 1. money --------------------------------------------------------------

def parse_money(v, dialect=LEGRAND):
    """Strip currency decoration and normalise to the dialect's number format.

    Returns a STRING, not a float: the output format is part of the contract
    and float formatting is exactly where the three builds diverge.
    """
    if dialect == LEGRAND:
        # Blank, the null tokens, AND literal "0" all mean "no price".
        if not v or v.strip() in NULL_TOKENS:
            return ''
        s = v.strip().replace('$', '').replace(',', '')
        try:
            return '%.2f' % float(s)
        except ValueError:
            return ''

    if dialect == LIBCO:
        s = clean_text(v)
        if not s:
            return ''
        cleaned = _NUMERIC_CLEAN_RE.sub('', s)
        if not cleaned:
            return ''
        try:
            f = float(cleaned)
        except ValueError:
            # libco returns the cleaned digits rather than dropping the value.
            return cleaned
        return str(int(f)) if f.is_integer() else '%.2f' % f

    if dialect == TCS:
        # No numeric validation at all: whatever is left after stripping $ and ,
        # goes into the file. A stray "TBD" reaches the importer intact.
        return (v or '').replace('$', '').replace(',', '').strip()

    raise ValueError('unknown money dialect: %r' % dialect)


def has_float_tail(v, places=5):
    """True if a value carries a binary-float tail (5.8740000000000006).

    Spreadsheet artifact, not a price. 143 of these sit in one Legrand price
    column. Round before the value reaches a money field.
    """
    return bool(re.match(r'^-?\d+\.\d{%d,}$' % places, (v or '').strip()))


# --- 2. weight -------------------------------------------------------------

def parse_weight_lb(v, dialect=LEGRAND):
    """Parse a source weight into pounds.

    `LEGRAND` is unit-aware (lb/lbs/g/kg) and converts. `LIBCO` takes the first
    number and ignores the unit entirely.

    **libco's behaviour is a latent defect, not a dialect choice**: a source
    value of "500 g" becomes "500" — off by a factor of 453. It is preserved
    here only so libco's output can be reproduced; raise it before reusing it.
    """
    if dialect == LIBCO:
        s = clean_text(v)
        if not s:
            return ''
        m = re.search(r'(\d+(?:\.\d+)?)', s)
        return m.group(1) if m else ''

    if dialect != LEGRAND:
        raise ValueError('unknown weight dialect: %r' % dialect)

    if not v or v.strip() in ('', '0', '#N/A', 'N/A'):
        return ''
    m = re.match(r'^\s*([\d.]+)\s*(lb|lbs|g|kg)?\s*$', v.strip(), re.IGNORECASE)
    if not m:
        return ''
    num = float(m.group(1))
    unit = (m.group(2) or 'lb').lower()
    if unit == 'g':
        num = num / 453.59237
    elif unit == 'kg':
        num = num * 2.20462262
    return ('%.6f' % num).rstrip('0').rstrip('.')


# --- 3. dimensions ---------------------------------------------------------

def build_dimensions(height, width, length, dialect=LEGRAND):
    """Assemble H/W/L into the single `Dimensions` string.

    The two dialects produce different strings and BOTH are live:
      LEGRAND  '3.5 in H x 2 in W x 1 in L', 'N/A' when nothing is supplied,
               and a missing axis becomes the literal '0 in' rather than being
               dropped - so the string always names three axes.
      TCS      '18.75"H x 10.5"W x 10.5"D', missing axes omitted, '' when empty.

    Dimensions truncates at 50 chars with a warning, so a long assembly is
    silently shortened rather than rejected.
    """
    if dialect == LEGRAND:
        parts = []
        for val in (height, width, length):
            val = val.strip() if val else ''
            parts.append(val if (val and val != '0') else '0 in')
        if not any(p != '0 in' for p in parts):
            return 'N/A'
        return '%s H x %s W x %s L' % (parts[0], parts[1], parts[2])

    if dialect == TCS:
        parts = []
        for val, axis in ((height, 'H'), (width, 'W'), (length, 'D')):
            if not val:
                continue
            v = val.replace('"', '')
            parts.append('%s"%s' % (v, axis))
        return ' x '.join(parts)

    raise ValueError('unknown dimension dialect: %r' % dialect)


# --- 4. booleans -----------------------------------------------------------

def to_boolean(v, dialect=LEGRAND):
    """Normalise a truthy source value for an eCat boolean column.

    LEGRAND returns 'Y' or ''. This is the correct behaviour for any field used
    as an iPad FILTER: eCat matches only 'Y'/'y'/'T'/'t'/digits 1-9, so a raw
    'Yes' does not match and the filter chip returns nothing.

    LIBCO returns 'Yes'/'No' verbatim. **If any libco field normalised this way
    is registered as an iPad filter, that filter cannot match** - the same shape
    as leg's 13 empty filter fields (BUILD_SPEC B1). Verify before reuse.
    """
    if dialect == LIBCO:
        s = clean_text(v)
        if s.lower() == 'yes':
            return 'Yes'
        if s.lower() == 'no':
            return 'No'
        return s

    if dialect != LEGRAND:
        raise ValueError('unknown boolean dialect: %r' % dialect)

    return 'Y' if clean_na(v).lower() in ('yes', 'y', 'true', 't', '1') else ''


# --- 5. dates --------------------------------------------------------------

_MONTHS = ('january february march april may june july august september '
           'october november december').split()

_LONG_DATE_RE = re.compile(
    r'^(%s)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})$' % '|'.join(_MONTHS),
    re.IGNORECASE)


def normalize_date(v, dialect=LEGRAND):
    """Normalise a source date to eCat's `YYYY-MM-DD`.

    Returns '' for anything that is not a date. That matters more than it
    looks: `NextReceiptDate` rejects prose, so 'to be sched' must become blank
    rather than reach the importer. Legrand's source carries 101 of those.

    Returning '' for unparseable input is deliberate - a date field is one of
    the few places where dropping a value is safer than passing it through.
    """
    v = (v or '').strip()
    if not v:
        return ''
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{2})$', v)
    if m:
        month, day, yy = m.groups()
        return '%04d-%02d-%02d' % (2000 + int(yy), int(month), int(day))
    m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', v)
    if m:
        month, day, yyyy = m.groups()
        return '%s-%02d-%02d' % (yyyy, int(month), int(day))
    if re.match(r'^\d{4}-\d{2}-\d{2}$', v):
        return v
    # xlsx date cells arrive as datetimes. Returning '' here would silently
    # blank a populated date column.
    m = re.match(r'^(\d{4}-\d{2}-\d{2})[ T]\d{2}:\d{2}:\d{2}', v)
    if m:
        return m.group(1)
    m = _LONG_DATE_RE.match(v)
    if m:
        mon, day, year = m.groups()
        return '%s-%02d-%02d' % (year, _MONTHS.index(mon.lower()) + 1, int(day))
    return ''


def parse_int(v, default='0'):
    """Coerce to an integer string with NO floor and NO null-mapping.

    Distinct from `clean_integer`, and the difference is load-bearing.
    `clean_integer` exists for `PackQuantity`/`MinimumQuantity`, where <=0 is
    invalid and is clamped to 1. A stock quantity is a SIGNED count where 0 and
    negative are both real values - leg carries 23 negative on-hand rows, one at
    -12,643. Clamping a quantity would silently invent stock, and "no stock
    value" versus "a stock value of zero" is a difference a rep experiences.

    Added 2026-09-04 for the Legrand inventory mapping. A mapping that needed a
    transform the library could not express is evidence of a MISSING PRIMITIVE,
    so it lands here and the next client gets it free.
    """
    v = (v or '').strip()
    try:
        return str(int(v))
    except (TypeError, ValueError):
        return default


def round_decimals(v, places=2, default=''):
    """Round a numeric string to `places` and drop trailing zeros.

    Distinct from `parse_money`, which PADS to a fixed width because a price
    column's format is part of its contract. A weight is a measurement: mer's
    source carries 0.008 lb and the build ships 0.01, while 6.5 stays 6.5 and
    must not become 6.50.

    Also the defence against binary-float tails - `5.8740000000000006` is a
    spreadsheet artifact, not a value, and 143 sit in one Legrand price column.

    Added 2026-09-04 by the 111Mercer mapping. Found by a mapping that could not
    express a transform, which is the signal to add a primitive HERE rather than
    fork one into a client file.
    """
    v = (v or '').strip()
    if not v:
        return default
    try:
        return '%g' % round(float(v), places)
    except (TypeError, ValueError):
        return default


def strip_float_tail(v):
    """Drop a spreadsheet's integer float tail: '810117540005.0' -> '810117540005'.

    openpyxl returns every numeric cell as a float, so an integer identifier read
    out of an xlsx arrives with `.0` welded on. `UPCValue` is the dangerous case:
    it is a TEXT field, so the importer takes '810117540005.0' verbatim and the
    barcode is wrong in a way nothing validates.

    Deliberately NOT `round_decimals`, which formats with %g and would render a
    12-digit UPC as '8.10118e+11'. Deliberately NOT `parse_int`, which cannot
    parse '...0.0' at all and would return the default, silently zeroing the
    column.

    Only an all-zero fraction is stripped. '1.5' is a real value and is returned
    untouched.
    """
    v = (v or '').strip()
    m = re.match(r'^(-?\d+)\.0+$', v)
    return m.group(1) if m else v


def clean_integer(v, default='1', minimum=1):
    """Coerce to an integer string, falling back to `default`.

    Legrand's `clean_order_min`. The floor matters: `PackQuantity` and
    `MinimumQuantity` coerce <=0 to 1 WITH A WARNING at import, so clamping
    here keeps the import clean rather than merely correct.

    A decimal in an integer eCat field is a HARD validation error - the row is
    rejected, not truncated - so this truncates via int(float(v)) rather than
    passing a decimal through.
    """
    v = (v or '').strip()
    if v in ('#N/A', '', '0'):
        return default
    try:
        return str(max(int(float(v)), minimum))
    except ValueError:
        return default

def split_first(v, sep=';'):
    """First value from a multi-valued cell, trimmed.

    A contact column holding several addresses is not a tcs quirk -- an ERP
    export of `Email` or `Phone` collects everything anyone ever entered, and
    eCat's BuyerEmail is ONE address. tcs ships 128 of 721 dealers with
    `kim@a-s-electric.com; evan@a-s-electric.com` in one cell.

    Sending the whole cell is worse than sending the first: the field imports
    clean, the address is invalid, and every order confirmation to that dealer
    bounces silently. Which of the several is "the" contact is a client
    decision; FIRST is the only one derivable, and the mapping says so.

    `sep` is a SET of delimiter characters, not one string, so a column that
    mixes them can be handled -- but the DEFAULT is `;` alone, and that is a
    measured choice rather than a guess. tcs's live file splits on `;` only:
    adding `,` fixed one row (`mlopez@designco.co,` loses its trailing comma)
    and broke another (`purchasing@galaxy-brands.com,jcgalaxie...` is shipped
    whole). Net zero against the live file, and `;` is what the client's own
    build does.

    Both of those rows are defects the live file carries -- a trailing comma and
    a two-address cell in a single-address field. Reproducing them is correct
    here and they are worth telling the client about separately.
    """
    if v is None:
        return ''
    out = str(v)
    for ch in sep:
        out = out.split(ch)[0]
    return out.strip()
