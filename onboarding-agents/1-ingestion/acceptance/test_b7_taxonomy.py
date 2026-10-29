#!/usr/bin/env python3
"""B7 taxonomy columns agree on code OR name.

A standard org's products.csv carries the taxonomy CODE (`KAL`, as stored); a
FurnishWeb-method org's carries the NAME (`adorne`, stored as `TN2`). Before
2026-10-29, B7 resolved every stored code to its name and compared that, so a
byte-identical file from a standard org would have shown 100% disagreement on
TradeNameCode -- the cried-wolf failure the TradeName fix was written to stop,
moved to the other half of the fleet. Collection and category had no
resolution at all, so a FurnishWeb-method org cried wolf there.

Run: python3 -I test_b7_taxonomy.py   (exit 0 = pass). No database needed.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b7_lossy as b7  # noqa: E402

S = b7.TAXO_SEP
CASES = [
    # (what, file value, live value from stage 2, expected agreement)
    ('standard org, file carries the code', 'KAL', 'KAL' + S + 'Kaleen Broadloom', True),
    ('FurnishWeb org, file carries the name', 'adorne', 'TN2' + S + 'adorne', True),
    ('case and spacing do not matter', ' kal ', 'KAL' + S + 'Kaleen  Broadloom', True),
    ('different brand, by code', 'HAB', 'KAL' + S + 'Kaleen Broadloom', False),
    ('different brand, by name', 'Hook and Beam', 'KAL' + S + 'Kaleen Broadloom', False),
    ('orphaned code still agrees with that code', 'XYZ', 'XYZ' + S, True),
    ('orphaned code does not agree with a blank name', '', 'XYZ' + S, False),
]


def main():
    failed = 0
    for what, fv, lv, want in CASES:
        got = b7.values_agree(fv, lv, b7.TAXO)
        ok = got == want
        failed += not ok
        print('%s  %s' % ('ok  ' if ok else 'FAIL', what))
    for col in ('CollectionCode', 'CategoryCode', 'TradeNameCode'):
        kind = b7.PRODUCTS[col][1]
        ok = kind == b7.TAXO
        failed += not ok
        print('%s  products %s is compared as taxonomy' % ('ok  ' if ok else 'FAIL', col))
    sql = b7.value_expr('collection_code@Collection', b7.TAXO)
    ok = "'|||'" in sql and "tx.type = 'Collection'" in sql
    failed += not ok
    print('%s  stage-2 SQL returns code and name for Collection' % ('ok  ' if ok else 'FAIL'))
    print('B7 TAXONOMY: %s (%d failed)' % ('PASS' if not failed else 'FAIL', failed))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
