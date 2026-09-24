"""6. LongDesc / ShortDesc truncation.

Field lengths are NOT defined here. They come from `preflight/limits_generated.py`,
generated from `Product::ATTR_LENGTHS` in supercat_server. Several documented
numbers are wrong (LongDesc 50, ShortDesc 15, TradeNameCode 5, BaseItemCode 20
were all wrong and caused real data loss), so a limit typed into this file would
be a build error, not a style choice. Callers pass the limit in.
"""

import re


def truncate_word_boundary(s, limit):
    """Truncate to `limit` without cutting a word in half.

    Breaks on a space or a hyphen, KEEPING the hyphen ("Tamper-" not "Tamper"),
    because the hyphen signals the word was cut. Falls back to a hard cut only
    when the boundary would discard more than half the string.
    """
    if len(s) <= limit:
        return s
    truncated = s[:limit].rstrip()
    last_space = truncated.rfind(' ')
    last_hyphen = truncated.rfind('-')
    if last_hyphen > last_space:
        cut = last_hyphen + 1
    else:
        cut = last_space
    if cut > limit * 0.5:
        return truncated[:cut].rstrip(', ;')
    return truncated.rstrip(',; -')


def find_token_span(s, token):
    """Locate `token` in `s` treating '-' and ' ' as equivalent.

    Both substitutions are single-char-for-single-char, so the span indexes
    directly into the ORIGINAL string and the caller can slice it without
    re-deriving offsets.
    """
    idx = s.replace('-', ' ').lower().find(token.replace('-', ' ').lower())
    return None if idx == -1 else (idx, idx + len(token))


def build_long_desc(product_name, brand, finish, limit,
                    strip_suffix_re=r',?\s*with Microban\.?\s*$',
                    null_tokens=('#N/A', '0')):
    """Build a LongDesc that fits `limit` without truncating the Finish off it.

    Finish is the one part of the name that distinguishes finish-variant SKUs
    from each other in a list view, so it is moved to the end and protected:
    the CORE is truncated, never the suffix.

    Returns (long_desc, was_truncated, finish_mismatch).

    `finish_mismatch` means the Finish column's value does not appear anywhere
    in Product Name. That is a source-quality contradiction between two columns,
    and the name is left untouched rather than having an unverified colour word
    forced into it. Report it; do not paper over it.
    """
    s = product_name.replace('®', '').replace('™', '')
    s = re.sub(r'^\s*%s\s*' % re.escape(brand), '', s, flags=re.IGNORECASE)
    if strip_suffix_re:
        s = re.sub(strip_suffix_re, '', s, flags=re.IGNORECASE)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r',\s*,', ',', s)
    s = s.strip().strip(',').strip()

    finish = (finish or '').strip()
    core, suffix, mismatch = s, '', False
    if finish and finish not in null_tokens:
        span = find_token_span(s, finish)
        if span:
            start, end = span
            core = (s[:start] + s[end:]).strip()
            core = re.sub(r'\s{2,}', ' ', core).strip(' ,-')
            suffix = ', %s' % s[start:end]
        else:
            mismatch = True

    if len(core) + len(suffix) <= limit:
        return (core + suffix).strip(', '), False, mismatch

    core_trunc = truncate_word_boundary(core, limit - len(suffix))
    return (core_trunc + suffix).strip(', '), True, mismatch


def build_short_desc(long_desc, limit):
    """Compact label for order-form and admin grid views.

    ShortDesc falls back to LongDesc when blank, so this is an improvement not
    a requirement - but a word-boundary label reads far better in a narrow
    column than a mid-word-truncated LongDesc.
    """
    return truncate_word_boundary(long_desc, limit)
