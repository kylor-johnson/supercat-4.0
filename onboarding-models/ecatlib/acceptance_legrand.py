#!/usr/bin/env python3
"""Phase 1 acceptance test — rebuild Legrand's products.csv using ecatlib.

The test BUILD_SPEC demands: the library must reproduce a build that is already
trusted. Legrand's `products.csv` is 1,020 rows, live in production, produced by
a 1,537-line script.

Method: take `build_ecat_files.py` verbatim and replace ONLY the twelve
primitives with delegations to ecatlib, leaving the client-specific price
loaders and main() untouched (those are correctly client-specific, per
BUILD_SPEC §2). Run it. Diff the bytes.

Done = byte-identical, or every difference explained and accepted.

Anything less and the library is not trustworthy enough to point at a new
client - it is just script #61 with better naming.
"""

import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PARENT = os.path.dirname(HERE)

# Each entry replaces one function DEFINITION in build_ecat_files.py with a
# delegation. The signature is preserved exactly so the call sites are untouched
# - if a call site relied on a behaviour the library does not reproduce, the
# byte diff is what says so.
DELEGATIONS = {
    'strip_currency': '''def strip_currency(val):
    return _lib.parse_money(val, _lib.LEGRAND)
''',
    'parse_ship_weight_lb': '''def parse_ship_weight_lb(val):
    return _lib.parse_weight_lb(val, _lib.LEGRAND)
''',
    'build_dimensions': '''def build_dimensions(height, width, length):
    return _lib.build_dimensions(height, width, length, _lib.LEGRAND)
''',
    'to_boolean_y': '''def to_boolean_y(val):
    return _lib.to_boolean(val, _lib.LEGRAND)
''',
    'normalize_receipt_date': '''def normalize_receipt_date(val):
    return _lib.normalize_date(val, _lib.LEGRAND)
''',
    '_truncate_word_boundary': '''def _truncate_word_boundary(s, limit):
    return _lib.truncate_word_boundary(s, limit)
''',
    '_find_finish_span': '''def _find_finish_span(s, finish):
    return _lib.find_token_span(s, finish)
''',
    'build_long_desc': '''def build_long_desc(product_name, brand, finish, limit=LONGDESC_LIMIT):
    return _lib.build_long_desc(product_name, brand, finish, limit)
''',
    'build_short_desc': '''def build_short_desc(long_desc, limit=SHORTDESC_LIMIT):
    return _lib.build_short_desc(long_desc, limit)
''',
    'clean_na': '''def clean_na(val):
    return _lib.clean_na(val)
''',
    'clean_country': '''def clean_country(val):
    return _lib.clean_country(val)
''',
    # Legrand's clean_category does NOT null-map: a literal "0" category stays
    # "0". normalize_finish DOES null-map first. Same primitive, different
    # null policy - which is exactly why clean_lookup takes null_tokens.
    'clean_category': '''def clean_category(cat):
    return _lib.clean_lookup(cat, CATEGORY_FIXES, null_tokens=())
''',
    'normalize_finish': '''def normalize_finish(val):
    return _lib.clean_lookup(val, FINISH_FIXES)
''',
    'clean_order_min': '''def clean_order_min(val):
    return _lib.clean_integer(val, default="1", minimum=1)
''',
    '_normalize_variant_key': '''def _normalize_variant_key(name, finish):
    return _lib.variant_key_by_name(name, finish)
''',
    'build_related_items': '''def build_related_items(source_rows):
    return _lib.build_related_items(
        source_rows,
        key_fn=lambda row: _lib.variant_key_by_name(
            get_product_name(row), get_finish(row)),
        code_fn=lambda row: row["Item ID"].strip(),
    )
''',
    'load_carryforward': '''def load_carryforward(column, path=HIDEABLE_CARRYFORWARD_FILE):
    carried, warning = _lib.load_carryforward(path, column)
    if warning:
        print("  ! " + warning)
    return carried
''',
}


def find_def_span(src, name):
    """Return (start, end) of a top-level `def name(...)` block."""
    m = re.search(r'^def %s\(' % re.escape(name), src, re.M)
    if not m:
        return None
    start = m.start()
    nxt = re.search(r'^(?:def |class |# ---|[A-Z_]+ = )', src[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(src)
    return start, end


def patch(src):
    replaced, missing = [], []
    for name, body in DELEGATIONS.items():
        span = find_def_span(src, name)
        if not span:
            missing.append(name)
            continue
        start, end = span
        trailing = '\n' if not src[start:end].endswith('\n\n') else '\n\n'
        src = src[:start] + body.rstrip('\n') + trailing + src[end:]
        replaced.append(name)
    header = (
        'import sys as _sys\n'
        '_sys.path.insert(0, %r)\n'
        'import ecatlib as _lib\n' % LIB_PARENT)
    src = re.sub(r'^(import os\n)', r'\1' + header, src, count=1, flags=re.M)
    if '_lib' not in src.split('def ')[0]:
        src = header + src
    return src, replaced, missing


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print('usage: acceptance_legrand.py <Legrand dir> <sandbox dir> <target products.csv>')
        return 2
    legrand_dir, sandbox, target = sys.argv[1], sys.argv[2], sys.argv[3]
    build_dir = os.path.join(sandbox, 'Build')
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    os.makedirs(build_dir)

    # Only the inputs the build reads. Copying the whole Build directory pulls
    # in a 1GB image library for nothing.
    for fn in ('build_ecat_files.py', 'products.aug06-live.csv',
               'image_filename_map.csv'):
        srcf = os.path.join(legrand_dir, 'Build', fn)
        if os.path.exists(srcf):
            shutil.copy2(srcf, build_dir)
    os.symlink(os.path.join(legrand_dir, 'Source Data'),
               os.path.join(sandbox, 'Source Data'))

    script = os.path.join(build_dir, 'build_ecat_files.py')
    with open(script, encoding='utf-8') as fh:
        src = fh.read()
    patched, replaced, missing = patch(src)
    with open(script, 'w', encoding='utf-8') as fh:
        fh.write(patched)

    print('primitives delegated to ecatlib: %d' % len(replaced))
    for n in replaced:
        print('   %s' % n)
    if missing:
        print('NOT FOUND (library not exercised for these): %s' % ', '.join(missing))

    r = subprocess.run([sys.executable, '-u', 'build_ecat_files.py'],
                       cwd=build_dir, capture_output=True, text=True)
    if r.returncode != 0:
        print('\nBUILD FAILED (exit %d)\n%s' % (r.returncode, r.stdout[-3000:] + r.stderr[-3000:]))
        return 1

    produced = os.path.join(build_dir, 'products.csv')
    with open(target, 'rb') as a, open(produced, 'rb') as b:
        ba, bb = a.read(), b.read()

    print('\n%s' % ('=' * 66))
    if ba == bb:
        print('ACCEPTANCE: PASS - byte-identical (%d bytes)' % len(ba))
        print('%s' % ('=' * 66))
        return 0
    print('ACCEPTANCE: FAIL - %d bytes vs %d' % (len(ba), len(bb)))
    la, lb = ba.decode('utf-8').splitlines(), bb.decode('utf-8').splitlines()
    print('lines: target %d, produced %d' % (len(la), len(lb)))
    shown = 0
    for i, (x, y) in enumerate(zip(la, lb)):
        if x != y:
            print('\nline %d\n  target  : %s\n  produced: %s' % (i + 1, x[:200], y[:200]))
            shown += 1
            if shown >= 10:
                break
    print('%s' % ('=' * 66))
    return 1


if __name__ == '__main__':
    sys.exit(main())
