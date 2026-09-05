"""12. Carry-forward, and 10. taxonomy rollup.

## Why carry-forward is the load-bearing one

It exists in exactly one of the sixty scripts and encodes a rule that applies to
all of them: **when regenerating a file, values the generator cannot derive must
be carried forward by key, or regeneration silently destroys them.**

The two that matter:
  - `Hideable` - set by hand in Admin; nothing in the source knows about it
  - `ImageFileName` - for images uploaded AFTER the last build

It has already cost Legrand 19 products' live images once. `products.csv`
soft-deletes omitted rows on a clean import, so a regeneration that blanks a
column looks like a successful import.
"""

import collections
import csv
import os


def load_carryforward(path, column, key_column='BaseItemCode', encoding='utf-8-sig'):
    """Read `column` from a known-good previous build, keyed by `key_column`.

    Empty values are dropped, so a blank in the old file never overwrites a
    freshly derived value.

    Returns {} and reports when the file or column is missing - callers must
    decide whether that is acceptable. It usually is not: a silent {} here is
    precisely how the 19 images were lost.

    NOTE the original passes a bare filename, which resolves against the
    CURRENT WORKING DIRECTORY, not the script's directory. Running the build
    from anywhere else silently carries nothing forward. Pass an absolute path.
    """
    if not os.path.exists(path):
        return {}, 'carry-forward source not found: %s - nothing carried forward' % path
    with open(path, newline='', encoding=encoding) as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return {}, 'carry-forward source %s is empty' % path
    if column not in rows[0]:
        return {}, 'carry-forward source %s has no %s column' % (path, column)
    out = {}
    for r in rows:
        k = (r.get(key_column) or '').strip()
        v = (r.get(column) or '').strip()
        if k and v:
            out[k] = v
    return out, None


def apply_carryforward(products, carried, column, key_column='BaseItemCode',
                       only_when_blank=True):
    """Apply carried values, and report what happened.

    `only_when_blank=True` means a derived value always wins and carry-forward
    fills gaps. Set False when the stored value is authoritative (`Hideable` is
    an Admin decision the generator can never re-derive).

    Returns (applied, missed) - `missed` is the keys present in the carried map
    that no longer exist in the build, which is a genuine signal: it means the
    product disappeared from source and is about to be soft-deleted.
    """
    applied = 0
    present = set()
    for p in products:
        k = (p.get(key_column) or '').strip()
        if not k:
            continue
        present.add(k)
        if k not in carried:
            continue
        if only_when_blank and (p.get(column) or '').strip():
            continue
        p[column] = carried[k]
        applied += 1
    missed = sorted(set(carried) - present)
    return applied, missed


def diff_against_previous(previous_rows, new_rows, key_column='BaseItemCode'):
    """Compare a regenerated file against the one that produced live state.

    BUILD_SPEC B6: 'the only differences should be intended'. This makes the
    differences enumerable instead of a matter of trust.

    Returns a dict with dropped / added keys and per-column change counts, plus
    `blanked`: columns that had a value before and are empty now. Blanking is
    the dangerous direction and is counted separately for that reason.
    """
    prev = {(r.get(key_column) or '').strip(): r for r in previous_rows}
    new = {(r.get(key_column) or '').strip(): r for r in new_rows}
    prev.pop('', None)
    new.pop('', None)

    dropped = sorted(set(prev) - set(new))
    added = sorted(set(new) - set(prev))
    changed = collections.Counter()
    blanked = collections.Counter()
    blanked_examples = collections.defaultdict(list)

    for k in sorted(set(prev) & set(new)):
        for col, old_val in prev[k].items():
            old_val = (old_val or '').strip()
            new_val = (new[k].get(col) or '').strip()
            if old_val == new_val:
                continue
            changed[col] += 1
            if old_val and not new_val:
                blanked[col] += 1
                if len(blanked_examples[col]) < 5:
                    blanked_examples[col].append(k)

    return {
        'dropped': dropped, 'added': added,
        'changed': dict(changed), 'blanked': dict(blanked),
        'blanked_examples': {k: v for k, v in blanked_examples.items()},
    }


# --- 10. taxonomy rollup ---------------------------------------------------

def rollup_taxonomy(products, category_column='CategoryCodes',
                    collection_column='CollectionCodes', group_map=None):
    """Count products per category and note which collections each spans.

    Categories and collections are comma lists, and whatever string appears
    becomes the iPad LABEL (auto-create), so a cryptic internal code ships to
    reps as-is. Groups never auto-create from a product import - they must
    exist first - which is why unmapped categories are returned separately.

    Returns (counts, collections_by_category, unmapped).
    """
    group_map = group_map or {}
    counts = collections.Counter()
    cols = collections.defaultdict(set)
    for p in products:
        collection = (p.get(collection_column) or '').strip()
        for cat in (p.get(category_column) or '').split(','):
            cat = cat.strip()
            if not cat:
                continue
            counts[cat] += 1
            if collection:
                cols[cat].add(collection)
    unmapped = sorted(c for c in counts if c not in group_map)
    return counts, {k: sorted(v) for k, v in cols.items()}, unmapped
