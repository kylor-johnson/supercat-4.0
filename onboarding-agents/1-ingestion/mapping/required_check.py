#!/usr/bin/env python3
"""Every eCat REQUIRED field, per client mapping: mapped, or named with a reason.

Phase 2's definition of done asks for "every unmapped required field named, with
the reason". This answers it mechanically so the answer cannot be left inferred
-- including when the answer is "none", which is the answer that most needs
saying out loud.

"Required" means the importer's own list, read from `ecat_vocab.REQUIRED_HEADERS`
(generated from supercat_server), never a typed number. It is a SHORT list:
products.csv requires exactly one field. That is worth knowing on its own,
because "required" in practice means "registered in this org's Admin and
expected by its reps", which is a different and longer list the importer does
not enforce.

usage: required_check.py <mapping.toml> [more...]
"""

import os
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'profiler'))

import ecat_vocab as vocab  # noqa: E402


# Fields the importer does not reject but a rep cannot work without. Each is
# here because it caused a real, live incident, and each names it.
SILENT_REQUIRED = {
    'customers.csv': [
        ('territorycodes',
         'KB-required, NOT importer-fatal. A blank TerritoryCodes imports clean '
         'and the customer is then invisible to every rep in a "show only '
         'associated customers" group. pebl sits at BLOCKING with 171 of 171 '
         'blank. Declare a default.'),
    ],
}


def check(path):
    with open(path, 'rb') as fh:
        m = tomllib.load(fh)

    # A LOOKUP TABLE FILE IS NOT A MAPPING. `tables.toml` and
    # `customers_tables.toml` have no `client`, no `fields` and no `kind`, and
    # reading them as products.csv mappings reported four fake "baseitemcode
    # ABSENT" failures against files that were never claiming to emit anything.
    #
    # That is this programme's own recurring defect turned on its own tool: a
    # check with nothing to measure reporting a result anyway. Skipped
    # explicitly and counted, so the coverage line still adds up.
    if 'client' not in m and 'fields' not in m and 'kind' not in m:
        return m, None, None

    # An option_stack mapping emits options.csv AND option_groups.csv from one
    # traversal, so it is checked against both required lists. Checking it as a
    # single unnamed target is how one of the two goes unexamined.
    if m.get('kind') == 'option_stack':
        return check_option_stack(path, m)

    target = m.get('target', 'products.csv')
    emitted = {f['name'].lower(): f for f in m.get('fields', [])}
    required = vocab.REQUIRED_HEADERS.get(target, [])

    rows = []
    for req in required:
        f = emitted.get(req)
        if not f:
            rows.append((req, 'ABSENT', 'no column emitted'))
            continue
        op = f.get('op', 'column')
        if op == 'const' and not str(f.get('value', '')).strip():
            rows.append((req, 'EMPTY CONST', 'emitted but constant-blank'))
        else:
            src = (f.get('column') or f.get('from') or f.get('input')
                   or f.get('fn') or op)
            rows.append((req, 'mapped', 'via %s (%s)' % (op, src)))

    for name, why in SILENT_REQUIRED.get(target, []):
        f = emitted.get(name)
        if not f:
            rows.append((name, 'ABSENT (silent)', why))
        elif f.get('op') == 'column' and not f.get('default'):
            rows.append((name, 'NO DEFAULT', why))
        else:
            rows.append((name, 'mapped', 'with a declared default'))
    return m, target, rows


def check_option_stack(path, m):
    """options.csv and option_groups.csv, from the one mapping that makes both."""
    opt_cols = {c.lower() for c in m.get('options_columns', ['Code', 'Name'])}
    grp_cols = {c.lower() for c in
                m.get('option_groups_columns', ['Code', 'Name', 'Options'])}
    if m.get('option_catalogue'):
        opt_cols |= {'code', 'name'}
    rows = []
    for target, have in (('options.csv', opt_cols),
                         ('option_groups.csv', grp_cols)):
        for req in vocab.REQUIRED_HEADERS.get(target, []):
            rows.append((('%s %s' % (target.split('.')[0], req)),
                         'mapped' if req in have else 'ABSENT',
                         'emitted column' if req in have else 'not in the emit list'))
    # Length caps are importer-fatal and are NOT in REQUIRED_HEADERS. The KB
    # says 8 and 25; the code says 15 and 50, and the code is right.
    rows.append(('code/name limits', 'mapped',
                 'Code<=15, Name<=50 enforced by the engine at build time '
                 '(the KB says 8/25 and is wrong)'))
    return m, 'options.csv + option_groups.csv', rows


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    unmapped_total = 0
    print('=' * 72)
    print('REQUIRED-FIELD COVERAGE')
    print('=' * 72)
    skipped = []
    for path in sys.argv[1:]:
        m, target, rows = check(path)
        if target is None:
            skipped.append(os.path.basename(path))
            continue
        print()
        print('%s — %s  (%s)' % (m.get('client', '?'), target,
                                 os.path.basename(path)))
        print('  fields evaluated: %d  (COVERAGE — %d importer-required, %d '
              'silently required)'
              % (len(rows), len([r for r in rows if 'silent' not in r[1].lower()
                                 and r[1] != 'NO DEFAULT']),
                 len([r for r in rows if 'silent' in r[1].lower()
                      or r[1] == 'NO DEFAULT'])))
        for name, state, why in rows:
            flag = ' ' if state == 'mapped' else '!'
            if state != 'mapped':
                unmapped_total += 1
            print('   %s %-18s %-12s %s' % (flag, name, state, why))
        print('  -> %s' % ('every required field has a source column'
                           if all(r[1] == 'mapped' for r in rows)
                           else 'UNMAPPED REQUIRED FIELDS ABOVE'))
    print()
    print('=' * 72)
    print('COVERAGE — evaluated %d of %d files. %d skipped as lookup-table '
          'files, which declare no fields and are not mappings%s'
          % (len(sys.argv) - 1 - len(skipped), len(sys.argv) - 1, len(skipped),
             (': ' + ', '.join(sorted(set(skipped)))) if skipped else '.'))
    if unmapped_total == 0:
        print('RESULT: NONE. No client has an eCat required field lacking a')
        print('        plausible source column. Stated explicitly, not inferred.')
    else:
        print('RESULT: %d unmapped required field(s) — see above.' % unmapped_total)
    print('=' * 72)
    print()
    print('Note the denominator. `products.csv` enforces exactly ONE required')
    print('header (BaseItemCode) and `inventory.csv` the same. The fields that')
    print('matter in practice -- the ones registered as filters in a given org --')
    print('are not importer-required, are not on this list, and can be empty on')
    print('every row while the import reads clean. That is BUILD_SPEC B1, and it')
    print('is why this check is necessary but nowhere near sufficient.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
