#!/usr/bin/env python3
"""Phase 2 acceptance — regenerate live eCat files FROM THE MAPPING, script gone.

Phase 1 earned trust by reproducing a build that was already trusted, with the
1,537-line script still driving and only the twelve primitives delegated.
Phase 2 must do the same thing one level up:

    Discard build_ecat_files.py entirely. Express what it does as a declarative
    mapping. Regenerate through ecatlib driven by that mapping ALONE. Diff
    against the live file. Byte-identical, or every difference explained.

No client script is imported, patched, or read. `mapping/mapper.py` plus
`mappings/<client>/*.toml` are the whole input.

GREEN and RED both run, and the RED half is not decoration. A green test that
cannot go red proves nothing -- the same vacuity as a partition computed by
subtraction instead of counted (OPEN_ITEMS §F7). Each mutation changes exactly
one thing a human could plausibly get wrong while editing a mapping, and each
targets a different layer of the format.

usage: acceptance_mapping.py <Legrand dir> <111Mercer dir> [--keep]
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASELINES = os.path.join(HERE, 'baselines.toml')

# Exit codes are distinct on purpose. A CI job must be able to treat "the
# client's build legitimately changed" differently from "the mapping broke" --
# collapsing them into one FAIL is how a gate earns a reputation for
# false-alarming and gets switched off (OPEN_ITEMS G3, B1b).
EXIT_PASS, EXIT_MAPPING_BROKE, EXIT_BASELINE_MOVED = 0, 1, 3

# client -> (mapping dir, [(mapping toml, live file relative to client root)])
CLIENTS = {
    'leg': ('legrand', [('products.toml',  'Build/products.csv'),
                        ('inventory.toml', 'Build/inventory.csv')]),
    'mer': ('mercer',  [('products.toml',  'Import Files/products.csv')]),
}

# client -> [(label, what it proves, file, old text, new text)]
MUTATIONS = {
    'leg': [
        ('dialect', 'the DIALECT is load-bearing, not decorative',
         'products.toml', 'dialect     = "legrand"', 'dialect     = "libco"'),
        # NB: the same swap on ca_adorne is a genuine NO-OP -- its columns 6 and
        # 7 hold identical values on all 448 rows (one CA price level wearing
        # two names). ca_radiant's differ on all 631, so the swap is observable.
        ('column assignment', 'a swapped price column index',
         'products.toml',
         'columns = { net_cad = 5, imap_cad = 6, msrp_cad = 7 }',
         'columns = { net_cad = 5, imap_cad = 7, msrp_cad = 6 }'),
        ('source column name', 'a mistyped source header',
         'products.toml', 'column = "Country of Origin"', 'column = "Country Of Origin"'),
        ('carry-forward removed', 'the 19 live images depend on it',
         'products.toml', 'carry_forward = { when = "blank" }', ''),
        ('escape-hatch constant', 'the budgeted transform is exercised',
         'custom.py', "return str(volume) if volume > 0 else '0.01'",
         "return str(volume) if volume > 0 else '0.02'"),
        ('field order', 'column ORDER is part of the contract',
         'products.toml',
         '[[fields]]\nname = "PromotionPrice"\nop = "const"\nvalue = ""\n\n'
         '[[fields]]\nname = "Price_dn"\nop = "ref"\nfrom = "net_price"\n',
         '[[fields]]\nname = "Price_dn"\nop = "ref"\nfrom = "net_price"\n\n'
         '[[fields]]\nname = "PromotionPrice"\nop = "const"\nvalue = ""\n'),
    ],
    'mer': [
        ('dialect', 'mer is PASSTHROUGH money; legrand would pad 137 values to 2dp',
         'products.toml', 'dialect       = "tcs"', 'dialect       = "legrand"'),
        ('line terminator', "mer's file is LF; leg's is CRLF",
         'products.toml', 'line_terminator = "lf"', 'line_terminator = "crlf"'),
        ('row order', 'row order is carried, not derivable from the source',
         'products.toml', 'row_order = "carry_forward"', 'row_order = "source"'),
        ('escape hatch', 'the image-filename convention is exercised',
         'custom.py', "return '%s.jpg' % (code or '').strip().lower()",
         "return '%s.jpeg' % (code or '').strip().lower()"),
        # Mutate a table VALUE, not a comment. (An earlier version of this
        # mutation hit the word "Samples" inside a comment and stayed green --
        # which is exactly what the STILL-GREEN detector below is for.)
        ('taxonomy table', 'a taxonomy entry becomes the iPad LABEL',
         'tables.toml', '= "Unpasted Wallpaper"', '= "Unpasted Wallpapers"'),
    ],
}


def build(mapping_dir, client_root, toml_name, out_path):
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, 'mapper.py'),
         os.path.join(mapping_dir, toml_name), client_root, out_path],
        capture_output=True, text=True)
    if r.returncode != 0:
        return False, (r.stdout + r.stderr)[-1200:]
    with open(out_path, 'rb') as fh:
        return True, fh.read()


def load_pins():
    """Pinned baselines, keyed (client, key). A pin records what the baseline
    was WHEN THE TEST LAST PASSED, which is the only way to tell a moved
    baseline from a broken mapping."""
    if not os.path.exists(BASELINES):
        return {}
    with open(BASELINES, 'rb') as fh:
        doc = tomllib.load(fh)
    return {(b['client'], b['key']): b for b in doc.get('baseline', [])}


def nlines_differ(a, b):
    la, lb = a.splitlines(), b.splitlines()
    return sum(1 for x, y in zip(la, lb) if x != y) + abs(len(la) - len(lb))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    roots = {'leg': os.path.abspath(sys.argv[1]), 'mer': os.path.abspath(sys.argv[2])}
    sandbox = tempfile.mkdtemp(prefix='p2_accept_')
    failures, moved, unpinned = [], [], []
    try:
        print('=' * 72)
        print('GREEN — reproduce the pinned baselines from the mapping alone')
        print('=' * 72)
        print('  engine : mapping/mapper.py         client-agnostic, stdlib + ecatlib')
        print('  input  : mappings/<client>/*.toml  data')
        print('  script : the client build scripts  NOT READ\n')
        pins = load_pins()
        expected = {}
        for client, (mdir, targets) in CLIENTS.items():
            src = os.path.join(ROOT, 'mappings', mdir)
            work = os.path.join(sandbox, 'green_' + client)
            shutil.copytree(src, work)
            for toml_name, live_rel in targets:
                key = toml_name[:-5]                     # products.toml -> products
                live = os.path.join(roots[client], live_rel)
                with open(live, 'rb') as fh:
                    want = fh.read()
                expected[(client, toml_name)] = want
                ok, got = build(work, roots[client], toml_name,
                                os.path.join(sandbox, '%s_%s.csv' % (client, toml_name)))
                name = '%s %s' % (client, os.path.basename(live_rel))

                pin = pins.get((client, key))
                live_hash = hashlib.sha256(want).hexdigest()
                pinned = pin and pin['sha256'] == live_hash

                if not ok:
                    print('  %-26s BUILD FAILED\n%s' % (name, got))
                    failures.append(name)
                    continue

                if pin is None:
                    print('  %-26s UNPINNED — run mapping/bless.py' % name)
                    unpinned.append(name)
                    if got != want:
                        failures.append(name)
                    continue

                if pinned and got == want:
                    print('  %-26s PASS — byte-identical (%d bytes)' % (name, len(want)))
                elif pinned:
                    # The baseline is exactly what it was when this last passed,
                    # so the file did not move. The mapping did.
                    print('  %-26s FAIL — MAPPING REGRESSION' % name)
                    print('  %-26s   baseline unchanged since %s (%d bytes)'
                          % ('', pin['pinned_on'], pin['bytes']))
                    print('  %-26s   produced %d bytes, %d lines differ'
                          % ('', len(got), nlines_differ(want, got)))
                    failures.append(name)
                elif got == want:
                    # The live file moved AND the mapping already produces the
                    # new one. Not a defect -- a decision.
                    print('  %-26s BASELINE MOVED — mapping already tracks it' % name)
                    print('  %-26s   pinned %s at %d bytes; live file is now %d'
                          % ('', pin['pinned_on'], pin['bytes'], len(want)))
                    print('  %-26s   pinned build: %s' % ('', pin['produced_by']))
                    print('  %-26s   -> RE-BLESS (deliberate, recorded):' % '')
                    print('  %-26s      python3 mapping/bless.py %s %s --reason "..."'
                          % ('', client, key))
                    moved.append(name)
                else:
                    print('  %-26s BASELINE MOVED — and the mapping does NOT' % name)
                    print('  %-26s   reproduce the new baseline. INVESTIGATE.' % '')
                    print('  %-26s   pinned %s at %d bytes; live file is now %d;'
                          % ('', pin['pinned_on'], pin['bytes'], len(want)))
                    print('  %-26s   mapping produced %d (%d lines differ from live)'
                          % ('', len(got), nlines_differ(want, got)))
                    print('  %-26s   pinned build: %s' % ('', pin['produced_by']))
                    moved.append(name)
                    failures.append(name)

        if moved and not failures:
            print()
            print('=' * 72)
            print('ACCEPTANCE: BASELINE MOVED — a human decides, this is not a defect')
            print('  moved: %s' % ', '.join(moved))
            print('  The mapping reproduces the new file. Re-bless to accept it.')
            print('=' * 72)
            return EXIT_BASELINE_MOVED
        if failures:
            print()
            print('=' * 72)
            print('ACCEPTANCE: FAIL — green did not reproduce: %s' % ', '.join(failures))
            print('=' * 72)
            return EXIT_MAPPING_BROKE

        print()
        print('=' * 72)
        print('RED — every mutated mapping entry must break the reproduction')
        print('=' * 72)
        for client, (mdir, targets) in CLIENTS.items():
            toml_name, live_rel = targets[0]
            want = expected[(client, toml_name)]
            print('  %s:' % client)
            for i, (label, why, fname, old, new) in enumerate(MUTATIONS[client]):
                work = os.path.join(sandbox, 'red_%s_%d' % (client, i))
                shutil.copytree(os.path.join(ROOT, 'mappings', mdir), work)
                fpath = os.path.join(work, fname)
                with open(fpath, encoding='utf-8') as fh:
                    src = fh.read()
                if old not in src:
                    print('    %-22s SKIP — mutation text not found in %s' % (label, fname))
                    failures.append('%s:%s' % (client, label))
                    continue
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(src.replace(old, new, 1))
                ok, got = build(work, roots[client], toml_name,
                                os.path.join(sandbox, 'red_%s_%d.csv' % (client, i)))
                if not ok:
                    print('    %-22s RED (build refused)      <- %s' % (label, why))
                elif got == want:
                    print('    %-22s *** STILL GREEN *** mutation had no effect' % label)
                    print('        %s is NOT proven by this test.' % why)
                    failures.append('%s:%s' % (client, label))
                else:
                    nd = nlines_differ(want, got)
                    how = ('%d lines differ' % nd) if nd else \
                          ('same lines, %+d bytes' % (len(got) - len(want)))
                    print('    %-22s RED (%s)  <- %s' % (label, how, why))

        print()
        print('=' * 72)
        if failures:
            print('ACCEPTANCE: FAIL — did not go red: %s' % ', '.join(failures))
            print('=' * 72)
            return EXIT_MAPPING_BROKE
        n = sum(len(v) for v in MUTATIONS.values())
        print('ACCEPTANCE: PASS')
        print('  3 live files byte-identical from mappings alone, and red under')
        print('  %d mutated mapping entries across %d structurally different clients.'
              % (n, len(CLIENTS)))
        if unpinned:
            print('  NOTE: unpinned baselines: %s' % ', '.join(unpinned))
        print('=' * 72)
        return EXIT_PASS
    finally:
        if '--keep' in sys.argv:
            print('sandbox kept: %s' % sandbox)
        else:
            shutil.rmtree(sandbox, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
