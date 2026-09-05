"""8. RelatedItems and 9. variant grouping.

Two primitives that only make sense together: variant grouping decides WHICH
SKUs form a family, RelatedItems decides how that family is written into the
file.

The three builds derive families three different ways, and the difference is
genuinely per-client because it depends on how the client's SKUs are shaped:

    leg   strip the Finish word out of the product NAME; SKUs whose remaining
          name matches are variants of each other
    lib   split the SKU on a trailing "-<digits>"  (ABC-1, ABC-2 -> root ABC)
    tcs   sort key over size, families assembled during the staged rebuild

So the GROUPING FUNCTION is config; the family-to-string assembly below is not.
"""

import collections
import re

RELATED_ITEMS_LIMIT_DEFAULT = 255


# --- 9. variant grouping ---------------------------------------------------

def variant_key_by_name(name, token, null_tokens=('#N/A', '0')):
    """Legrand: collapse a product name to a token-independent key.

    Removes the Finish word from the name so that SKUs differing only by finish
    land on the same key. Punctuation and case are normalised away.
    """
    key = name
    token = (token or '').strip()
    if token and token not in null_tokens:
        key = re.sub(re.escape(token), '', key, flags=re.IGNORECASE)
    key = key.replace(',', ' ')
    return re.sub(r'\s+', ' ', key).strip().lower()


def variant_key_by_sku_suffix(sku, pattern=r'^(.+)-(\d+)$'):
    """libco: the SKU root before a trailing -<digits>. None when it does not
    match, meaning the SKU is not part of a numbered variant family."""
    m = re.match(pattern, sku or '')
    return m.group(1) if m else None


# --- 8. RelatedItems -------------------------------------------------------

def group_families(rows, key_fn, code_fn):
    """Bucket rows into families. Insertion-ordered, so the output preserves
    SOURCE FILE ORDER - which is what makes the result reproducible run to run.

    Returns OrderedDict of key -> [code, ...].
    """
    groups = collections.OrderedDict()
    for row in rows:
        groups.setdefault(key_fn(row), []).append(code_fn(row))
    return groups


def build_related_items(rows, key_fn, code_fn, min_family=2):
    """Map each code in a multi-member family to the comma-joined family.

    The family list INCLUDES the item itself, per eCat Related Items practice.
    Singletons are omitted entirely rather than mapped to themselves.

    Returns (related_map, families).
    """
    groups = group_families(rows, key_fn, code_fn)
    related_map, families = {}, []
    for items in groups.values():
        if len(items) >= min_family:
            joined = ','.join(items)
            for item in items:
                related_map[item] = joined
            families.append(items)
    return related_map, families


def parse_related_items(val):
    return [x.strip() for x in (val or '').split(',') if x.strip()]


def merge_related(existing, add, limit=None):
    """Union two related-item lists, preserving order and dropping duplicates.

    tcs's `merge_related`, generalised. `limit` truncates to fit RelatedItems'
    length cap WITHOUT cutting a code in half - a half-code is a dangling
    reference, which is exactly the class of defect BUILD_SPEC A3 exists for.
    """
    seen = []
    for code in parse_related_items(existing) + list(add or []):
        if code and code not in seen:
            seen.append(code)
    if limit is None:
        return ','.join(seen)
    out = []
    for code in seen:
        candidate = ','.join(out + [code])
        if len(candidate) > limit:
            break
        out.append(code)
    return ','.join(out)
