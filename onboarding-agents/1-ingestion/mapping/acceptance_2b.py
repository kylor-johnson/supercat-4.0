#!/usr/bin/env python3
"""Phase 2b acceptance -- the four remaining eCat file types, green AND red.

A test that cannot go red is not a test. `acceptance_mapping.py` proves that by
mutating eleven mapping entries and requiring every one to break the build; this
does the same for options, option_groups, customers and stories.

WHAT IS GATED, AND ON WHAT

  stories.csv    BYTE-IDENTICAL on every shared row. 379 of 379, both columns.
  customers.csv  13,693 of 13,699 cells. The six are named and each has a
                 reason it is not derivable from the folder -- an invented
                 postcode, an inconsistent province spelling in the build
                 itself, two multi-address cells the build shipped whole.
  options.csv    328 of 341 codes; 96.1% of cells over the four DERIVED columns.
                 ImageName and SortValue are not derived and are excluded from
                 the denominator BY NAME rather than quietly.
  option_groups  MEMBERSHIP, not code. 67.8% of the reference's 311 member sets
                 reproduced exactly. Code spelling is invented by whoever built
                 the file and scoring it measures nothing.

  and on every run: INTEGRITY -- every option code a group references exists,
  and every group an OptionSet references was emitted. 0 dangling. That is the
  A4 condition mali fails.

Thresholds are floors, recorded from a measured run. A mapping change that
raises them is a re-bless (`bless.py`), not an edit to a number in this file.

usage: acceptance_2b.py "<The CopperSmith dir>"
"""

import os
import shutil
import subprocess
import sys
import tempfile
import csv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import pins  # noqa: E402

MAPPINGS = os.path.join(ROOT, 'mappings', 'tcs')

# Floors, from the measured post-unblind run. Raising one is a deliberate act.
FLOOR = {
    'stories_cells':        1.00,    # byte-identical
    'customers_cells':      0.9995,
    'options_cells':        0.95,
    # Raised 0.65 -> 0.88 when the `LR` type override took recall from 67.8% to
    # 91.0%. The old floor was set from a measured run in which ONE
    # miscategorised catalogue row cost 22 points, and a floor that accommodates
    # a known systematic defect is a floor that protects nothing.
    'group_membership':     0.88,
    # PRECISION, separately from cells. `emit = "all"` adds 86 catalogue rows
    # nobody can order and the CELL metric does not move at all -- it only ever
    # looks at shared keys, so rows I invent are invisible to it. A metric that
    # cannot see over-production is half a metric, and this is the half.
    'options_precision':    0.95,
    # THE METRIC THAT ACTUALLY GATES A CLIENT, and it did not exist until the
    # 2b closeout asked what the residual was made of.
    #
    # `group_membership` counts DISTINCT member sets. Per-product groups make
    # that a poor proxy for what a rep sees: the Finish family is 2 of 311 sets
    # and it applies to 375 of 379 products. Membership read 91.0% while
    # per-product option availability was exact on ZERO products.
    #
    # These floors gate REGRESSION only. They are nowhere near client-ready and
    # the run says so in as many words.
    'offer_recall':         0.85,
    'offer_precision':      0.82,
}


def run_mapping(toml, client_root, out):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'mapper.py'),
                        toml, client_root, out],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def cells(produced, reference, key, columns):
    """Byte-exact cells over the NAMED columns and shared keys. Coverage stated."""
    def load(p):
        with open(p, newline='', encoding='utf-8-sig') as fh:
            return {(r.get(key) or '').strip(): r for r in csv.DictReader(fh)
                    if (r.get(key) or '').strip()}
    ref, mine = load(reference), load(produced)
    shared = sorted(set(ref) & set(mine))
    tot = ex = 0
    for k in shared:
        for c in columns:
            tot += 1
            if (ref[k].get(c) or '') == (mine[k].get(c) or ''):
                ex += 1
    return ex, tot, len(shared), len(ref), len(mine)


def member_sets(path, col='Options'):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        return {tuple(sorted(x for x in (r.get(col) or '').split(',') if x))
                for r in csv.DictReader(fh)}


def offer_check(out_dir, tcs, ref_groups_path):
    """Per product, the SET of option codes a rep can choose from.

    Resolves each side's OptionSet columns through its OWN option_groups, so
    invented group CODES do not matter and the comparison is what the rep sees.

    This is the only number here that answers "can this go to a client".
    """
    def groups(path):
        with open(path, newline='', encoding='utf-8-sig') as fh:
            return {r['Code']: [x for x in (r['Options'] or '').split(',') if x]
                    for r in csv.DictReader(fh)}

    def offered(row, g):
        out = set()
        for c in row:
            if not c.startswith('OptionSet') or c.endswith(('Required', 'Matrixed')):
                continue
            for code in (row.get(c) or '').split(','):
                code = code.strip()
                if code:
                    out.update(g.get(code, []))
        return out

    rg = groups(ref_groups_path)
    mg = groups(os.path.join(out_dir, 'option_groups.csv'))
    with open(os.path.join(tcs, 'CS_eCat_Rebuild', 'products.csv'),
              newline='', encoding='utf-8-sig') as fh:
        ref = {r['BaseItemCode']: offered(r, rg) for r in csv.DictReader(fh)}
    asn = os.path.join(out_dir, '_INTERMEDIATE_option_assignments.csv')
    with open(asn, newline='', encoding='utf-8-sig') as fh:
        mine = {r['SKU']: offered(r, mg) for r in csv.DictReader(fh)}

    sh = sorted(set(ref) & set(mine))
    exact = sum(1 for k in sh if ref[k] == mine[k])
    tp = sum(len(ref[k] & mine[k]) for k in sh)
    fn = sum(len(ref[k] - mine[k]) for k in sh)
    fp = sum(len(mine[k] - ref[k]) for k in sh)
    recall = tp / float(tp + fn) if tp + fn else 0.0
    prec = tp / float(tp + fp) if tp + fp else 0.0
    lines = [
        '  offers END-TO-END   %s  %d of %d products have IDENTICAL option '
        'availability (%.1f%%)' % ('PASS' if recall >= FLOOR['offer_recall']
                                   and prec >= FLOOR['offer_precision']
                                   else 'FAIL',
                                   exact, len(sh), 100 * exact / len(sh) if sh else 0),
        '    %d correct offers, %d MISSING (a rep cannot pick something the '
        'build offers), %d EXTRA (a rep CAN pick something the build does not)'
        % (tp, fn, fp),
        '    recall %.1f%%  precision %.1f%%' % (100 * recall, 100 * prec),
        '    COVERAGE — evaluated %d of %d reference products; %d are '
        'accessories/kits outside the two lantern sheets and contributed '
        'nothing.' % (len(sh), len(ref), len(ref) - len(sh)),
        '    NOT CLIENT-READY. These floors gate regression, not readiness.',
    ]
    return {'recall': recall, 'precision': prec, 'exact': exact,
            'shared': len(sh), 'lines': lines}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    tcs = sys.argv[1]
    key_dir = os.path.join(tcs, 'CS_eCat_Rebuild')
    om_dir = os.path.join(tcs, 'CS_OptionMapping_Rebuild')
    refs = {
        'options': os.path.join(key_dir, 'options.csv'),
        'option_groups': os.path.join(key_dir, 'option_groups.csv'),
        'customers': os.path.join(om_dir, 'customers.csv'),
        'stories': os.path.join(key_dir, 'stories.csv'),
    }

    print('=' * 72)
    print('COMPARISON TARGETS — all four must be pinned or this refuses')
    print('=' * 72)
    ok, lines = pins.require(list(refs.values()))
    for ln in lines:
        print(ln)
    if not ok:
        return 2

    tmp = tempfile.mkdtemp(prefix='acc2b-')
    fails = []
    try:
        print()
        print('=' * 72)
        print('GREEN — the mappings reproduce the build')
        print('=' * 72)

        # -- stories --
        out = os.path.join(tmp, 'stories.csv')
        rc, log = run_mapping(os.path.join(MAPPINGS, 'stories_v2.toml'), tcs, out)
        if rc:
            fails.append('stories build failed: %s' % log[-400:])
        else:
            ex, tot, sh, nref, nmine = cells(out, refs['stories'], 'BaseItemCode',
                                             ['BaseItemCode', 'ProductStory'])
            frac = ex / float(tot) if tot else 0
            status = 'PASS' if frac >= FLOOR['stories_cells'] else 'FAIL'
            print('  stories.csv         %s  %d of %d cells byte-exact (%.2f%%)'
                  % (status, ex, tot, 100 * frac))
            print('    COVERAGE — evaluated %d of %d reference rows; %d reference '
                  'rows have no counterpart (accessories and kits, whose prose '
                  'is not in this folder)' % (sh, nref, nref - sh))
            if status == 'FAIL':
                fails.append('stories below floor')

        # -- customers --
        out = os.path.join(tmp, 'customers.csv')
        rc, log = run_mapping(os.path.join(MAPPINGS, 'customers_v2.toml'), tcs, out)
        if rc:
            fails.append('customers build failed: %s' % log[-400:])
        else:
            with open(out, encoding='utf-8-sig') as fh:
                mycols = next(csv.reader(fh))
            ex, tot, sh, nref, nmine = cells(out, refs['customers'], 'BillToCode',
                                             mycols)
            frac = ex / float(tot) if tot else 0
            status = 'PASS' if frac >= FLOOR['customers_cells'] else 'FAIL'
            print('  customers.csv       %s  %d of %d cells byte-exact (%.2f%%)'
                  % (status, ex, tot, 100 * frac))
            print('    COVERAGE — evaluated %d of %d columns over %d of %d rows. '
                  'The 4 unevaluated columns (BillToShortname, ShipToCode, '
                  'ShipToName, ShipInstructions) are NOT produced and are named, '
                  'not hidden in a denominator.' % (len(mycols), 23, sh, nref))
            if status == 'FAIL':
                fails.append('customers below floor')

        # -- the option stack --
        out = os.path.join(tmp, 'opts')
        rc, log = run_mapping(os.path.join(MAPPINGS, 'options_v2.toml'), tcs, out)
        if rc:
            fails.append('option stack build failed: %s' % log[-400:])
        else:
            ex, tot, sh, nref, nmine = cells(
                os.path.join(out, 'options.csv'), refs['options'], 'Code',
                ['Code', 'Name', 'Description', 'PriceAddend'])
            frac = ex / float(tot) if tot else 0
            status = 'PASS' if frac >= FLOOR['options_cells'] else 'FAIL'
            print('  options.csv         %s  %d of %d cells byte-exact (%.1f%%)'
                  % (status, ex, tot, 100 * frac))
            print('    COVERAGE — evaluated 4 of 7 reference columns over %d of '
                  '%d codes. ImageName, SortValue and PriceFactor are NOT '
                  'derivable from this folder and are excluded BY NAME.'
                  % (sh, nref))
            prec = sh / float(nmine) if nmine else 0.0
            pstatus = 'PASS' if prec >= FLOOR['options_precision'] else 'FAIL'
            print('  options precision   %s  %d of %d produced codes exist in '
                  'the reference (%.1f%%)' % (pstatus, sh, nmine, 100 * prec))
            if pstatus == 'FAIL':
                fails.append('options precision below floor')

            rs = member_sets(refs['option_groups'])
            ms = member_sets(os.path.join(out, 'option_groups.csv'))
            recall = len(rs & ms) / float(len(rs))
            status = 'PASS' if recall >= FLOOR['group_membership'] else 'FAIL'
            print('  option_groups.csv   %s  %d of %d reference member sets '
                  'reproduced (%.1f%%)' % (status, len(rs & ms), len(rs),
                                           100 * recall))
            print('    COVERAGE — evaluated %d of %d reference sets and %d of %d '
                  'produced sets. Group CODE is not scored: it is invented by '
                  'whoever built the file.' % (len(rs), len(rs), len(ms), len(ms)))
            if status == 'FAIL':
                fails.append('group membership below floor')

            # -- END TO END: what a rep can actually choose from --
            e2e = offer_check(out, tcs, refs['option_groups'])
            for line in e2e['lines']:
                print(line)
            if e2e['recall'] < FLOOR['offer_recall']:
                fails.append('per-product offer recall below floor')
            if e2e['precision'] < FLOOR['offer_precision']:
                fails.append('per-product offer precision below floor')

            if 'INTEGRITY' in log:
                print('  integrity           FAIL  dangling reference(s) emitted')
                fails.append('integrity: dangling references')
            else:
                print('  integrity           PASS  0 dangling group-membership or '
                      'OptionSet references')

        # -- RED --
        print()
        print('=' * 72)
        print('RED — every mutation below MUST break the build')
        print('=' * 72)
        muts = [
            # THE READING. per_product -> per_column is the whole decision the
            # format refuses to default: a product carrying PF3 would see all
            # five post fitters. If this does not go red the format is not
            # actually expressing a choice.
            ('options_v2.toml', 'the reading (per_product -> per_column)',
             'grouping     = "per_product"\ngroup_code   = "CM{n}"',
             'grouping     = "per_column"\ngroup_code   = "CM{n}"',
             'group_membership'),
            # A weaker partition mutation was tried first -- GAS -> BULBS -- and
            # it moved membership by 1.9 points, under the floor's noise. Seven
            # options in a 341-option file cannot break a whole-file metric. The
            # partition mutation has to move the LARGEST axis to be a test.
            ('options_v2.toml', 'the axis partition (largest axis)',
             'option_types = ["WALL ACCESSORIES"]', 'option_types = ["BULBS"]',
             'group_membership'),
            # The override IS the finding. Without it recall is 67.8%, and the
            # summary read as a green row on a file type that hard-deletes.
            ('options_v2.toml', 'the LR type override',
             '"LR" = "CEILING MOUNT"', '"LR" = "POST & PIER MOUNT"',
             'group_membership'),
            ('options_v2.toml', 'the catalogue key',
             'code  = "Accessory SKU"', 'code  = "Accessory Name"',
             'options_cells'),
            # `null_tokens = []` was tried here and changed NOTHING, which is a
            # finding rather than a weak test: in the catalogue-driven reading
            # `----` is filtered by the catalogue lookup before the null check
            # ever runs, so the declaration is dead weight on this mapping. It
            # is load-bearing on `options.toml`, which has no catalogue. Kept in
            # the mapping for the mapping without one; not asserted here.
            ('options_v2.toml', 'the emit rule (referenced -> all)',
             'emit  = "referenced"', 'emit  = "all"', 'options_cells'),
            ('customers_v2.toml', 'DefaultPriceCode case',
             'value = "map"', 'value = "MAP"', 'customers_cells'),
            ('customers_v2.toml', 'the state table',
             'table = "state_code"', 'table = "country_iso"', 'customers_cells'),
            ('customers_v2.toml', 'the territory default',
             'default = "100"', 'default = ""', 'customers_cells'),
            ('stories_v2.toml', 'the bullet prefix',
             'prefix_each = "• "', 'prefix_each = "- "', 'stories_cells'),
            ('stories_v2.toml', 'skip_blank on the features list',
             'of = ["_f1", "_f2", "_f3", "_f4", "_f5", "_f6"]\njoin = "\\n"\nprefix_each = "• "\nskip_blank = true',
             'of = ["_f1", "_f2", "_f3", "_f4", "_f5", "_f6"]\njoin = "\\n"\nprefix_each = "• "\nskip_blank = false',
             'stories_cells'),
            ('stories_v2.toml', 'the story column',
             'column = "Marketing Copy"', 'column = "Long Description"',
             'stories_cells'),
        ]
        for fname, what, old, new, metric in muts:
            src = os.path.join(MAPPINGS, fname)
            text = open(src, encoding='utf-8').read()
            if old not in text:
                print('  %-38s SKIPPED  mutation text not found — the test '
                      'silently stopped testing' % what)
                fails.append('mutation %r no longer applies' % what)
                continue
            mdir = os.path.join(tmp, 'mut')
            shutil.rmtree(mdir, ignore_errors=True)
            shutil.copytree(MAPPINGS, mdir)
            open(os.path.join(mdir, fname), 'w', encoding='utf-8').write(
                text.replace(old, new, 1))
            mout = os.path.join(tmp, 'mutout')
            shutil.rmtree(mout, ignore_errors=True)
            rc, log = run_mapping(os.path.join(mdir, fname), tcs,
                                  mout if 'options' in fname else mout + '.csv')
            broke, detail = False, ''
            if rc:
                broke, detail = True, 'build refused'
            else:
                if fname.startswith('options'):
                    rs = member_sets(refs['option_groups'])
                    ms = member_sets(os.path.join(mout, 'option_groups.csv'))
                    r2 = len(rs & ms) / float(len(rs))
                    ex2, tot2, _, _, _ = cells(
                        os.path.join(mout, 'options.csv'), refs['options'], 'Code',
                        ['Code', 'Name', 'Description', 'PriceAddend'])
                    f2 = ex2 / float(tot2) if tot2 else 0.0
                    ex2, tot2, sh2, _, nm2 = cells(
                        os.path.join(mout, 'options.csv'), refs['options'], 'Code',
                        ['Code', 'Name', 'Description', 'PriceAddend'])
                    p2 = sh2 / float(nm2) if nm2 else 0.0
                    broke = (r2 < FLOOR['group_membership']
                             or f2 < FLOOR['options_cells']
                             or p2 < FLOOR['options_precision'])
                    detail = ('membership %.1f%%, cells %.1f%%, precision %.1f%%'
                              % (100 * r2, 100 * f2, 100 * p2))
                else:
                    ref = refs['customers'] if 'customers' in fname else refs['stories']
                    k = 'BillToCode' if 'customers' in fname else 'BaseItemCode'
                    with open(mout + '.csv', encoding='utf-8-sig') as fh:
                        cols = next(csv.reader(fh))
                    ex2, tot2, _, _, _ = cells(mout + '.csv', ref, k, cols)
                    f2 = ex2 / float(tot2) if tot2 else 0.0
                    broke = f2 < FLOOR[metric]
                    detail = '%d of %d cells (%.2f%%)' % (ex2, tot2, 100 * f2)
            print('  %-38s %s  %s' % (what, 'RED ' if broke else 'GREEN — BAD',
                                      detail))
            if not broke:
                fails.append('mutation %r did NOT break the build' % what)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print('=' * 72)
    if fails:
        print('ACCEPTANCE: FAIL — %d problem(s)' % len(fails))
        for f in fails:
            print('  - %s' % f)
        print('=' * 72)
        return 1
    print('ACCEPTANCE: PASS')
    print('  Four eCat file types reproduced from mappings alone, and red under')
    print('  %d mutated mapping entries.' % len(muts))
    print()
    print('  PASS means NO REGRESSION. It does NOT mean client-ready, and for')
    print('  the option stack it specifically does not:')
    print('    stories.csv       byte-identical            -> ready')
    print('    customers.csv     13,693 of 13,699 cells    -> ready, 6 named')
    print('    options.csv       328 of 341 codes          -> BLOCKED: 13 codes')
    print('                      have no source in the folder')
    print('    option_groups.csv 0 of 379 products have identical option')
    print('                      availability              -> BLOCKED')
    print('  See mappings/tcs/SCORE_2b.md § the residual.')
    print('=' * 72)
    return 0


if __name__ == '__main__':
    sys.exit(main())
