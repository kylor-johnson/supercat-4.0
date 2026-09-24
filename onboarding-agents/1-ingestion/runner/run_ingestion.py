#!/usr/bin/env python3
"""Agent 1 — one command: a client folder in, eCat files + a report out.

    /opt/homebrew/bin/python3 runner/run_ingestion.py --client leg

Six phases, run in order, each one able to refuse:

    1 PREFLIGHT   interpreter, iCloud dataless placeholders, declared inputs
    2 PROFILE     what is actually in the source folder            (profiler/)
    3 RESOLVE     which mapping, and every required field mapped   (mapping/)
    4 BUILD       produce files in IMPORT ORDER, into a sandbox    (mapper.py)
    5 GATE        B6 + B7 + A1 together                   (preupload_check.py)
    6 VERIFY      regression bytes, then the client-tree guard

THE GATE IS THE POINT
---------------------
No upload proposal is emitted unless every phase was EVALUATED. Not "did not
complain" — evaluated. The recurring defect across this whole programme is a
check that had nothing to measure reporting a pass, so a phase that could not
run refuses the run and names itself, and the exit code says which phase.

Nothing uploads. Ever. This produces files and a report; a human uploads.

EXIT CODES — one meaning each, for a cron that reads them
---------------------------------------------------------
    0   PASS. Every phase evaluated. Upload proposal in the report.
    1   internal error (a bug here, not a finding about the client)
    2   usage or registry error — unknown client, no mapping directory
    3   PREFLIGHT failed  — environment or inputs
    4   PROFILE failed    — the source folder could not be read
    5   MAPPING refused   — cannot map, and it names what
    6   BUILD failed      — a mapping could not be evaluated
    7   GATE refused      — a FINDING. B6 blanking, B7 lossy, A1 wrong org.
                            Something is wrong with the FILE. Do not upload.
    8   REGRESSION failed — produced bytes != the trusted file
    9   CLIENT TREE MODIFIED — the worst case, and it overrides every other
                              code. Reported even when a phase already failed.
   10   GATE NOT EVALUATED — needs Postgres and had none. Nothing is known to
                            be wrong with the file; nothing is known to be
                            right either. An OPS problem, not a data one, and
                            it is a separate code because a cron that cannot
                            tell those apart will page the wrong person.

Every phase that CAN run does run, even after an earlier one refuses: the
regression check needs no database and no gate, and its answer is worth having
on a run the gate stopped. The exit code names the FIRST phase that refused;
the report lists all of them.

WHAT NEEDS THE DATABASE, AND WHAT DOES NOT
------------------------------------------
    phase 1 PREFLIGHT   no database
    phase 2 PROFILE     no database          (profiler/ never connects)
    phase 3 RESOLVE     no database          (ecatlib never connects)
    phase 4 BUILD        no database
    phase 5 GATE         B6 no · B7 YES · A1 YES
    phase 6 VERIFY       no database

So four of six phases and the whole file-production path are already
container-ready with no credential at all. Only the gate needs Postgres, and
it needs it for the two checks that matter most — B7 asks whether the file is
POORER than the live rows it replaces, A1 asks whether it is even the right
org. With `--use-db` and a read-only `DATABASE_URL` those now run in-process.
Without either, they EMIT SQL and the run exits 7: a gate that printed a query
nobody ran has not gated anything.

Read-only against Postgres throughout. Writes nothing to any client tree.
"""

import argparse
import datetime
import io
import os
import re
import shutil
import subprocess
import sys
import tomllib
import traceback
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)               # onboarding-agents/1-ingestion/
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'profiler'))
sys.path.insert(0, os.path.join(ROOT, 'mapping'))

import preflight                                              # noqa: E402
import sandbox as sbx                                         # noqa: E402

# The canonical implementation tree. A SIBLING of `SuperCat 4.0`, not inside
# it — which cost this session a wrong turn and has cost earlier ones more.
# Overridable with --implementation-root; never discovered by searching, and
# never relative to the current working directory, because a cron has no
# meaningful cwd.
DEFAULT_IMPL_ROOT = ('/Users/kylorjohnson/Library/Mobile Documents/'
                     'com~apple~CloudDocs/SuperCat_Simple_Final')

# MANDATORY. options.csv NULLS group membership, so option_groups is sent
# AGAIN after it. Three of the six HARD-delete. This order is a property of
# the importer, not a preference, so it is enforced here rather than left to
# the order someone happens to list targets in.
IMPORT_ORDER = ['options', 'option_groups', 'products', 'stories',
                'inventory', 'customers']

PHASES = ['PREFLIGHT', 'PROFILE', 'RESOLVE', 'BUILD', 'GATE', 'VERIFY']

EXIT = {'ok': 0, 'internal': 1, 'usage': 2, 'PREFLIGHT': 3, 'PROFILE': 4,
        'RESOLVE': 5, 'BUILD': 6, 'GATE': 7, 'REGRESSION': 8, 'TREE': 9,
        'GATE_UNEVALUATED': 10}

# Order of precedence when more than one phase refuses. The earliest real
# failure is the one an operator should act on first -- except TREE, which is
# an incident rather than a finding and outranks everything.
PRECEDENCE = ['TREE', 'internal', 'usage', 'PREFLIGHT', 'PROFILE', 'RESOLVE',
              'BUILD', 'GATE', 'REGRESSION', 'GATE_UNEVALUATED']


class Refused(Exception):
    """A phase refused. Carries the phase name and the reasons."""

    def __init__(self, phase, problems):
        self.phase = phase
        self.problems = problems if isinstance(problems, list) else [problems]
        super().__init__('%s refused: %s' % (phase, self.problems[0]))


class Report:
    """The one report file. Everything goes here; stdout gets phase lines only.

    A cron cannot read a terminal, and the 09-09 runner's ~13 minutes of work
    left no artifact anyone could inspect afterwards. So the report is the
    output, it is written incrementally, and it is written even when a phase
    refuses — a refusal report is the most useful one there is.
    """

    def __init__(self, path):
        self.path = path
        self.buf = []
        self.phase_results = []

    def h1(self, text):
        self.buf += ['', '=' * 78, text, '=' * 78]

    def h2(self, text):
        self.buf += ['', '-' * 78, text, '-' * 78]

    def line(self, text=''):
        if isinstance(text, list):
            self.buf += text
        else:
            self.buf.append(text)

    def phase(self, name, state, detail=''):
        self.phase_results.append((name, state, detail))
        print('  %-10s %-12s %s' % (name, state, detail), flush=True)

    def write(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)
        with open(self.path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(self.buf) + '\n')
        return self.path


# --- registry ---------------------------------------------------------------

def load_registry(path=None):
    path = path or os.path.join(HERE, 'clients.toml')
    if not os.path.exists(path):
        raise Refused('usage', 'client registry not found: %s' % path)
    with open(path, 'rb') as fh:
        return tomllib.load(fh).get('clients', {}), path


def find_mapping(mapping_root, target):
    """The mapping file for one target, preferring a `_v2` revision.

    tcs carries `customers.toml` and `customers_v2.toml`; PHASE2_COMPLETE
    names the `_v2` files as the ones that scored. Preferring the newer and
    SAYING which was chosen beats picking silently — a run that used the older
    mapping and reported a lower score would look like a data problem.
    """
    for name in ('%s_v2.toml' % target, '%s.toml' % target):
        p = os.path.join(mapping_root, name)
        if os.path.exists(p):
            return p, name
    return None, None


# --- phase 1 ----------------------------------------------------------------

def phase_preflight(rep, cfg, client_root, mappings, args):
    rep.h1('PHASE 1 — PREFLIGHT')
    problems = []

    declared_all = []
    needs_xlsx = False
    for target, (mpath, mapping) in mappings.items():
        d = preflight.collect_declared_paths(mapping, client_root)
        for rel, absolute in d:
            declared_all.append((rel, absolute))
        for spec in (mapping.get('inputs') or {}).values():
            if isinstance(spec, dict) and spec.get('format') in ('xlsx',):
                needs_xlsx = True

    rep.h2('1a — the interpreter')
    ok, lines, probs = preflight.check_interpreter(need_xlsx=needs_xlsx)
    rep.line(lines)
    rep.line('  xlsx inputs declared: %s' % ('yes' if needs_xlsx else 'no'))
    problems += probs

    rep.h2('1b — iCloud dataless placeholders (SF_DATALESS, not *.icloud)')
    ok2, lines2, probs2 = preflight.check_dataless(
        sorted({a for _, a in declared_all if os.path.exists(a)}),
        do_hydrate=args.hydrate)
    rep.line(lines2)
    problems += probs2

    rep.h2('1c — every declared input, absolute and present')
    ok3, lines3, probs3 = preflight.check_inputs(declared_all)
    rep.line(lines3)
    problems += probs3

    if problems:
        rep.line('')
        for p in problems:
            rep.line('  REFUSED: %s' % p)
        raise Refused('PREFLIGHT', problems)
    rep.line('')
    rep.line('  PREFLIGHT: evaluated 3 of 3 checks; all passed.')
    return declared_all


# --- phase 2 ----------------------------------------------------------------

def phase_profile(rep, client_root, cfg, args):
    rep.h1('PHASE 2 — PROFILE the source folder')
    src = os.path.join(client_root, cfg.get('source_dir', 'Source Data'))
    if not os.path.isdir(src):
        raise Refused('PROFILE',
                      'no source folder at %s. Three of six clients have none; '
                      'that is a finding about the client, not a bug here — but '
                      'it means nothing can be profiled.' % src)
    try:
        import folder_mode
        recs, exact, derived, near = folder_mode.profile_folder(src)
        buf = io.StringIO()
        folder_mode.report(src, recs, exact, derived, near, out=buf)
        rep.line(buf.getvalue().splitlines())
    except Refused:
        raise
    except Exception as exc:                                   # noqa: BLE001
        raise Refused('PROFILE', 'profiler failed on %s: %s' % (src, exc))
    rep.line('')
    rep.line('  PROFILE: %d files profiled. The profiler is READ-ONLY and '
             'touches no database.' % len(recs))
    return len(recs)


# --- phase 3 ----------------------------------------------------------------

def phase_resolve(rep, shortname, cfg, mappings):
    """Resolve the mapping, or refuse and NAME what cannot be mapped."""
    rep.h1('PHASE 3 — RESOLVE the mapping')
    sys.path.insert(0, os.path.join(ROOT, 'mapping'))
    import required_check

    problems = []
    rep.line('  client   : %s (%s)' % (shortname, cfg.get('name')))
    rep.line('  mode     : %s' % cfg.get('mode', 'unknown'))
    rep.line('  mappings : %s' % os.path.join(ROOT, 'mappings',
                                              cfg['mapping_dir']))
    rep.line('')

    declared_targets = list(cfg.get('targets') or [])
    ordered = [t for t in IMPORT_ORDER if t in declared_targets]
    unknown = [t for t in declared_targets if t not in IMPORT_ORDER]
    if unknown:
        problems.append('registry lists target(s) with no importer slot: %s'
                        % ', '.join(unknown))

    rep.line('  IMPORT ORDER for this client (mandatory, importer-imposed):')
    rep.line('     %s' % ' -> '.join(ordered))
    if 'options' in ordered and 'option_groups' in ordered:
        rep.line('     ... then RE-SEND option_groups. options.csv NULLS group '
                 'membership. That is A4.')
    missing_slots = [t for t in IMPORT_ORDER if t not in declared_targets]
    rep.line('  NOT PRODUCED for this client: %s' % (', '.join(missing_slots)
                                                     or 'nothing'))
    rep.line('     A slot with no mapping is NOT an empty file. Producing one '
             'would delete every live row it omits')
    rep.line('     (three of the six HARD-delete), so an absent mapping means '
             'an absent file, stated rather than assumed.')
    for key, note in (cfg.get('notes') or {}).items():
        rep.line('')
        rep.line('  NOTE (%s): %s' % (key, note.strip().replace('\n', '\n     ')))

    rep.h2('3a — required-field coverage, per mapping')
    for target in ordered:
        mpath, mapping = mappings[target]
        rep.line('')
        rep.line('  %s  <-  %s' % (target, os.path.basename(mpath)))
        # The mapping's own declared org must agree with the registry. Two
        # orgs are named "legrand" (live `leg` id 273; `lna` id 93 is a dead
        # 2015 org), and nothing inside a products.csv says which org it is
        # for. A mapping edited to the wrong org_id refuses here rather than
        # at the FTP.
        m_org = mapping.get('org_id')
        r_org = cfg.get('org_id') or 0
        if m_org and r_org and int(m_org) != int(r_org):
            problems.append('%s: mapping declares org_id %s, registry says %s. '
                            'Refusing — this is the 2026-08-18 shape.'
                            % (target, m_org, r_org))
        elif m_org and not r_org:
            rep.line('     org_id   : %s (mapping) — registry has none pinned, '
                     'so this is NOT cross-checked' % m_org)
        else:
            rep.line('     org_id   : %s (mapping and registry agree)' % m_org)
        rep.line('     target   : %s' % mapping.get('target', '(products.csv)'))
        rep.line('     dialect  : %s   input_class: %s'
                 % (mapping.get('dialect', '(none declared)'),
                    mapping.get('input_class', '(not declared)')))

        try:
            _m, tgt, rows = required_check.check(mpath)
        except Exception as exc:                               # noqa: BLE001
            problems.append('%s: mapping could not be parsed: %s' % (target, exc))
            continue
        if rows is None:
            problems.append('%s: %s declares no fields and no kind — it is a '
                            'lookup-table file, not a mapping' % (target, mpath))
            continue
        for name, state, why in rows:
            flag = '  ' if state == 'mapped' else '!!'
            rep.line('     %s %-22s %-16s %s' % (flag, name, state, why))
            if state != 'mapped':
                problems.append('%s: required field %r is %s — %s'
                                % (target, name, state, why))

    if problems:
        rep.line('')
        for p in problems:
            rep.line('  REFUSED: %s' % p)
        raise Refused('RESOLVE', problems)
    rep.line('')
    rep.line('  RESOLVE: evaluated %d of %d declared targets; every eCat '
             'required field has a source column.' % (len(ordered), len(ordered)))
    return ordered


# --- phase 4 ----------------------------------------------------------------

def phase_build(rep, shortname, cfg, mappings, ordered, staged_root, out_dir):
    rep.h1('PHASE 4 — BUILD, in import order, into the sandbox')
    rep.line('  Nothing here writes to a client tree. `mapper.py` takes its '
             'output path as an argument;')
    rep.line('  every input was COPIED into the sandbox read-only, so the '
             'client tree is not even referenced.')
    rep.line('  (build_ecat_files.py:31 sets OUTPUT_DIR from __file__ and takes '
             'no arguments at all. It is')
    rep.line('   not invoked, imported, patched or read by this runner.)')
    rep.line('')

    import mapper

    produced = {}
    problems = []
    for target in ordered:
        mpath, mapping = mappings[target]
        fname = mapping.get('target') or '%s.csv' % target
        rep.h2('4.%d — %s' % (ordered.index(target) + 1, fname))
        try:
            if mapping.get('kind') == 'option_stack':
                dest = os.path.join(out_dir, target)
                os.makedirs(dest, exist_ok=True)
            else:
                dest = os.path.join(out_dir, fname)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rows, eng = mapper.run(mpath, staged_root, dest)
            rep.line(buf.getvalue().splitlines())
            if mapping.get('kind') == 'option_stack':
                stack, paths = rows
                rep.line('  option stack -> %s' % dest)
                for p in paths:
                    rep.line('     %-44s %d bytes' % (os.path.basename(p),
                                                      os.path.getsize(p)))
                produced[target] = (dest, None)
            else:
                size = os.path.getsize(dest)
                rep.line('  rows: %d   bytes: %d   -> %s'
                         % (len(rows), size, dest))
                produced[target] = (dest, len(rows))
            if eng.report.counters:
                rep.line('  report:')
                rep.line(['     ' + l.strip() for l in eng.report.lines()])
            for w in eng.report.warnings:
                rep.line('  ! %s' % w)
        except Exception as exc:                               # noqa: BLE001
            rep.line('  BUILD FAILED: %s: %s' % (type(exc).__name__, exc))
            rep.line(['     ' + l for l in
                      traceback.format_exc().splitlines()[-6:]])
            problems.append('%s: %s' % (fname, exc))

    if problems:
        rep.line('')
        for p in problems:
            rep.line('  REFUSED: %s' % p)
        raise Refused('BUILD', problems)
    rep.line('')
    rep.line('  BUILD: produced %d of %d declared files.'
             % (len(produced), len(ordered)))
    return produced


# --- phase 5 ----------------------------------------------------------------

def phase_gate(rep, shortname, cfg, client_root, produced, mappings, ordered,
               args):
    """B6 + B7 + A1 TOGETHER, via preupload_check. Never individually."""
    rep.h1('PHASE 5 — THE GATE  (preupload_check: B6, B7, A1 together)')
    rep.line('  Invoked as one command by design. The three checks answer '
             'three different questions and')
    rep.line('  the coverage line only adds up if they are asked together: B6 '
             'diffs against the PREVIOUS FILE,')
    rep.line('  B7 against LIVE STATE, A1 against the ORG. B6 alone passes a '
             'file with every key present')
    rep.line('  and half its columns blanked.')
    rep.line('')

    gate_script = os.path.join(ROOT, 'mapping', 'preupload_check.py')
    build_dir = os.path.join(client_root, cfg.get('build_dir', 'Build'))
    problems = []        # something is WRONG with the file
    unevaluated = []     # nothing is known either way -- no credential
    ran = []

    for target in ordered:
        mpath, mapping = mappings[target]
        if mapping.get('kind') == 'option_stack':
            rep.h2('5 — %s: NOT GATED' % target)
            rep.line('  An option_stack emits two importer files plus an '
                     'intermediate. preupload_check keys on one')
            rep.line('  produced file, so this is NOT CHECKED rather than '
                     'passed.')
            unevaluated.append('%s: option stack not gated (NOT CHECKED)'
                               % target)
            continue

        fname = mapping.get('target') or '%s.csv' % target
        prod_path = produced[target][0]
        prev_path = os.path.join(build_dir, fname)
        rep.h2('5 — %s' % fname)

        if not os.path.exists(prev_path):
            rep.line('  previous file : NONE at %s' % prev_path)
            rep.line('  B6 has nothing to diff against. A first regeneration '
                     'is exactly the case B6 cannot see')
            rep.line('  and B7 exists for — and B7 needs the database. NOT '
                     'CHECKED, not passed.')
            unevaluated.append('%s: no previous file at %s, so B6 is NOT '
                               'CHECKED' % (fname, prev_path))
            continue

        cmd = [sys.executable, gate_script, prod_path, prev_path,
               '--org', shortname]
        if args.use_db:
            cmd.append('--use-db')
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        rep.line(r.stdout.splitlines())
        if r.stderr.strip():
            rep.line(['  stderr: ' + l for l in r.stderr.splitlines()])
        rep.line('  preupload_check exit: %d' % r.returncode)
        ran.append(fname)
        # preupload_check's exit codes, mapped onto the two kinds of refusal
        # this runner distinguishes. 4 means a check RAN and FOUND something,
        # which is a fact about the FILE; 2 and 3 mean a check did not measure,
        # which is a fact about the ENVIRONMENT. Collapsing them would page the
        # wrong person.
        if r.returncode == 0:
            continue
        if r.returncode == 4:
            problems.append(
                '%s: a gate check RAN and found a BLOCKING problem — B6 column '
                'blanking, B7 lossy regeneration, or A1 wrong org. Read the '
                'section above; do not upload.' % fname)
        elif r.returncode == 2:
            unevaluated.append(
                '%s: a gate check could not run at all (NOT CHECKED). A '
                'skipped check is not a passed check.' % fname)
        elif r.returncode == 3:
            unevaluated.append(
                '%s: B7 and/or A1 were EMITTED ONLY, not evaluated. They need '
                'Postgres. Re-run with --use-db and a read-only DATABASE_URL, '
                'or run the emitted SQL through the supercat-postgres-vpn MCP '
                'and feed it back with --from-results.' % fname)
        else:
            problems.append('%s: gate refused (exit %d) — see the section above'
                            % (fname, r.returncode))

    rep.line('')
    rep.line('  GATE COVERAGE: evaluated %d of %d produced files.'
             % (len(ran), len(ordered)))
    # A FINDING outranks a MISSING CREDENTIAL. If B6 found column blanking,
    # that is true regardless of whether B7 could reach the database, and it
    # is the more urgent thing to say.
    if problems:
        rep.line('')
        for p in problems:
            rep.line('  REFUSED: %s' % p)
        raise Refused('GATE', problems + unevaluated)
    if unevaluated:
        rep.line('')
        for p in unevaluated:
            rep.line('  NOT EVALUATED: %s' % p)
        rep.line('')
        rep.line('  This is not a finding about the file. It is the absence of '
                 'a measurement, which is')
        rep.line('  the one thing this harness refuses to let read as a pass.')
        raise Refused('GATE_UNEVALUATED', unevaluated)
    return ran


# --- phase 6 ----------------------------------------------------------------

def phase_verify(rep, cfg, produced, mappings, ordered):
    rep.h1('PHASE 6 — VERIFY the regression contract')
    expect = cfg.get('expect_bytes') or {}
    if not expect:
        rep.line('  no expect_bytes pinned for this client. NOT CHECKED — a '
                 'client with no trusted')
        rep.line('  reproducible build has nothing to regress against, and '
                 'saying so beats reporting a pass.')
        return None
    problems, lines, matched = [], [], []
    checked = 0
    for target in ordered:
        mpath, mapping = mappings[target]
        fname = mapping.get('target') or '%s.csv' % target
        if fname not in expect:
            lines.append('  %-16s NOT PINNED — not part of the regression '
                         'contract' % fname)
            continue
        want = int(expect[fname])
        got = os.path.getsize(produced[target][0])
        checked += 1
        if got == want:
            matched.append(fname)
            lines.append('  %-16s %8d bytes   BYTE-IDENTICAL to the trusted '
                         'file' % (fname, got))
        else:
            lines.append('  %-16s %8d bytes   EXPECTED %d  (delta %+d)'
                         % (fname, got, want, got - want))
            problems.append('%s: %d bytes, expected %d' % (fname, got, want))
    rep.line(lines)
    rep.line('')
    rep.line('  coverage: evaluated %d of %d pinned files.' % (checked, len(expect)))
    if not checked:
        # Every pinned name missed the produced set, so nothing was compared.
        # Returning a pass here would be the §3.4 defect in its purest form.
        rep.line('  NOT CHECKED — none of the pinned names matched a produced '
                 'file.')
        return None
    for key, note in (cfg.get('notes') or {}).items():
        if key == 'stories':
            rep.line('  ' + note.strip().replace('\n', '\n  '))
        if problems:
            rep.line('')
            for p in problems:
                rep.line('  REFUSED: %s' % p)
            raise Refused('REGRESSION', problems)
    return matched


# --- proposal ---------------------------------------------------------------

def write_proposal(rep, shortname, cfg, produced, mappings, ordered):
    rep.h1('UPLOAD PROPOSAL — for a human. NOTHING HAS BEEN UPLOADED.')
    rep.line('  org      : %s (%s), org_id %s'
             % (shortname, cfg.get('name'), cfg.get('org_id') or 'not pinned'))
    rep.line('')
    rep.line('  Send in THIS order. It is imposed by the importer, not chosen:')
    for i, target in enumerate(ordered, 1):
        mapping = mappings[target][1]
        fname = mapping.get('target') or '%s.csv' % target
        path = produced[target][0]
        rows = produced[target][1]
        rep.line('    %d. %-18s %-9s %s'
                 % (i, fname, ('%d rows' % rows) if rows else '', path))
    if 'options' in ordered and 'option_groups' in ordered:
        rep.line('    %d. option_groups.csv AGAIN — options.csv nulls group '
                 'membership (A4)' % (len(ordered) + 1))
    rep.line('')
    rep.line('  DELETE SEMANTICS on a warnings-only import:')
    rep.line('     products.csv                     SOFT-deletes omitted rows')
    rep.line('     inventory.csv / customers.csv    HARD-delete '
             '(customers takes ship-tos with it)')
    rep.line('     options.csv / option_groups.csv  HARD-delete')
    rep.line('     stories.csv                      sets story = NULL')
    rep.line('     A single Error row SUPPRESSES the deletes — "the delete did '
             'not happen" is usually an Error row nobody read.')
    rep.line('')
    rep.line('  CONFIRM THE TARGET ORG BEFORE UPLOADING. A1 ran against these '
             'files, and A1 is the only')
    rep.line('  check that would have stopped 2026-08-18, when Legrand\'s '
             '1,020-row products.csv went into')
    rep.line('  111Mercer and soft-deleted all 102 of its products. The file '
             'was valid; the import was clean.')


# --- main -------------------------------------------------------------------

def build_report_header(rep, args, shortname, cfg, client_root, registry_path):
    rep.h1('eCat INGESTION RUN — %s' % shortname)
    rep.line('  started      : %s' % datetime.datetime.now().isoformat(timespec='seconds'))
    rep.line('  client       : %s (%s)' % (shortname, cfg.get('name')))
    rep.line('  client root  : %s' % client_root)
    rep.line('  registry     : %s' % registry_path)
    rep.line('  interpreter  : %s' % sys.executable)
    rep.line('  sandbox      : %s' % args.sandbox)
    rep.line('  use-db       : %s' % ('yes' if args.use_db else
                                      'no — B7 and A1 will EMIT SQL only'))
    rep.line('  hydrate      : %s' % ('yes' if args.hydrate else 'no'))
    if args.break_phase:
        rep.line('  !! --break-phase %s : this run is DELIBERATELY SABOTAGED '
                 'to prove the gate refuses.' % args.break_phase)
    rep.line('')
    rep.line('  Read-only against Postgres. Writes nothing to any client tree.')


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--client', help='shortname from runner/clients.toml')
    ap.add_argument('--implementation-root', default=DEFAULT_IMPL_ROOT,
                    help='canonical 02_Implementation parent (absolute)')
    ap.add_argument('--registry', help='override runner/clients.toml')
    ap.add_argument('--sandbox', help='sandbox directory (absolute)')
    ap.add_argument('--report', help='report file path (absolute)')
    ap.add_argument('--hydrate', action='store_true',
                    help='ask iCloud to materialise dataless inputs and wait')
    ap.add_argument('--use-db', action='store_true',
                    help='run B7 and A1 against DATABASE_URL, read-only')
    ap.add_argument('--list', action='store_true', help='list registered clients')
    ap.add_argument('--break-phase', choices=('inputs', 'mapping', 'build',
                                              'gate', 'regression'),
                    help='deliberately sabotage one phase, to prove the gate '
                         'refuses and names it. Operates ONLY on sandbox and '
                         'temporary copies; never on a client tree.')
    args = ap.parse_args(argv)

    registry, registry_path = load_registry(args.registry)

    if args.list:
        print('registered clients (%s):' % registry_path)
        for sn, cfg in sorted(registry.items()):
            print('  %-8s %-24s %-12s targets: %s'
                  % (sn, cfg.get('name'), cfg.get('mode'),
                     ', '.join(cfg.get('targets') or [])))
        return EXIT['ok']

    if not args.client:
        print('need --client <shortname>, or --list. '
              'This is non-interactive by design.', file=sys.stderr)
        return EXIT['usage']

    shortname = args.client
    if shortname not in registry:
        print('unknown client %r. Registered: %s\n'
              'A client with no registry entry cannot be mapped, and a runner '
              'that guessed a folder name would be the wrong-directory failure '
              'that has already broken three sessions.'
              % (shortname, ', '.join(sorted(registry))), file=sys.stderr)
        return EXIT['usage']

    cfg = registry[shortname]
    impl = os.path.abspath(args.implementation_root)
    client_root = os.path.join(impl, cfg['client_dir'])
    mapping_root = os.path.join(ROOT, 'mappings', cfg['mapping_dir'])

    args.sandbox = os.path.abspath(
        args.sandbox or os.path.join(ROOT, 'runner', '_sandbox', shortname))
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    report_path = os.path.abspath(
        args.report or os.path.join(args.sandbox,
                                    'REPORT_%s_%s.txt' % (shortname, stamp)))

    rep = Report(report_path)
    guard = None
    refusals = []

    try:
        if not os.path.isdir(impl):
            raise Refused('usage', 'implementation root is not a directory: %s'
                          % impl)
        if not os.path.isdir(client_root):
            raise Refused('usage',
                          'client root is not a directory: %s\n'
                          '     If this looks missing, check the path before '
                          'concluding it does not exist — SuperCat_Simple_Final '
                          'is a SIBLING of "SuperCat 4.0", not inside it.'
                          % client_root)
        if not os.path.isdir(mapping_root):
            raise Refused('usage', 'no mapping directory: %s' % mapping_root)

        build_report_header(rep, args, shortname, cfg, client_root, registry_path)
        print('run_ingestion %s -> %s' % (shortname, report_path), flush=True)

        # load every declared mapping up front: a missing one is a usage
        # error, not a build failure, and it should surface before any work.
        mappings = {}
        import mapper
        for target in (cfg.get('targets') or []):
            mpath, chosen = find_mapping(mapping_root, target)
            if not mpath:
                raise Refused('RESOLVE',
                              'no mapping for target %r in %s. The layer '
                              'cannot map it, and that is named rather than '
                              'silently skipped.' % (target, mapping_root))
            m, _tables = mapper.load_mapping(mpath)
            mappings[target] = (mpath, m)

        # ---- guard the client tree BEFORE anything runs
        git_root = impl
        guard = sbx.TreeGuard(client_root, git_root)
        rep.h2('CLIENT-TREE GUARD — baseline')
        rep.line(guard.snapshot())

        # ---- phase 1
        declared = phase_preflight(rep, cfg, client_root, mappings, args)
        if args.break_phase == 'inputs':
            declared = declared + [('BROKEN/does-not-exist.csv',
                                    os.path.join(client_root, 'BROKEN',
                                                 'does-not-exist.csv'))]
            ok, lines, probs = preflight.check_inputs(declared)
            rep.h2('1d — SABOTAGE: a declared input that does not exist')
            rep.line(lines)
            raise Refused('PREFLIGHT', probs)
        rep.phase('PREFLIGHT', 'PASS', '%d inputs' % len(declared))

        # ---- phase 2
        nfiles = phase_profile(rep, client_root, cfg, args)
        rep.phase('PROFILE', 'PASS', '%d files' % nfiles)

        # ---- phase 3
        if args.break_phase == 'mapping':
            mappings, note = sabotage_mapping(args.sandbox, mappings)
            rep.h2('SABOTAGE: %s' % note)
        ordered = phase_resolve(rep, shortname, cfg, mappings)
        rep.phase('RESOLVE', 'PASS', ' -> '.join(ordered))

        # ---- stage the sandbox
        rep.h1('SANDBOX — inputs copied read-only; the client tree is not '
               'referenced')
        staged_root, out_dir, lines = sbx.stage(args.sandbox, client_root,
                                                declared)
        rep.line(lines)
        if args.break_phase == 'build':
            victim = declared[0][0]
            os.remove(os.path.join(staged_root, victim))
            rep.line('')
            rep.line('  SABOTAGE: removed the staged input %r, so the build '
                     'must fail loudly rather than' % victim)
            rep.line('  warn and continue with an empty table '
                     '(build_ecat_files.py:535 is the anti-pattern).')

        # ---- phase 4
        produced = phase_build(rep, shortname, cfg, mappings, ordered,
                               staged_root, out_dir)
        rep.phase('BUILD', 'PASS', '%d files' % len(produced))

        if args.break_phase == 'regression':
            victim = produced[ordered[0]][0]
            with open(victim, 'a', encoding='utf-8') as fh:
                fh.write('SABOTAGE,extra,row\n')
            rep.h2('SABOTAGE: appended a row to the produced %s in the SANDBOX'
                   % os.path.basename(victim))

        # ---- phase 5
        if args.break_phase == 'gate':
            victim = produced[ordered[0]][0]
            blank_a_column(victim)
            rep.h2('SABOTAGE: blanked a column in the produced %s in the '
                   'SANDBOX' % os.path.basename(victim))
            rep.line('  Blanking is the dangerous direction: the file still '
                     'imports CLEAN. This is how Legrand')
            rep.line('  lost 19 products\' live images.')
        # Phases 5 and 6 both consume `produced` and neither depends on the
        # other, so a refusal in one must not silence the other. The
        # regression check needs no database and no gate, and on the run that
        # first exercised this the gate refused for want of a credential and
        # took the byte-identity answer down with it -- the one measurement
        # that was actually available.
        try:
            gated = phase_gate(rep, shortname, cfg, client_root, produced,
                               mappings, ordered, args)
            rep.phase('GATE', 'PASS', '%d files gated' % len(gated))
        except Refused as exc:
            refusals.append(exc)
            rep.phase(exc.phase, 'REFUSED',
                      exc.problems[0].split('\n')[0][:60])

        # ---- phase 6
        try:
            verified = phase_verify(rep, cfg, produced, mappings, ordered)
            # `None` means nothing was compared. It must NOT read as a pass:
            # tcs and drf have no pinned bytes, and the first version of this
            # printed `VERIFY PASS  regression bytes match` for both — a
            # green line for a measurement that never happened, which is the
            # exact defect BUILD_SPEC §3.4 exists to forbid.
            if verified is None:
                rep.phase('VERIFY', 'NOT CHECKED',
                          'no trusted bytes pinned for this client')
            else:
                rep.phase('VERIFY', 'PASS',
                          '%d file(s) byte-identical to the trusted build'
                          % len(verified))
        except Refused as exc:
            refusals.append(exc)
            rep.phase(exc.phase, 'REFUSED',
                      exc.problems[0].split('\n')[0][:60])

        if not refusals:
            write_proposal(rep, shortname, cfg, produced, mappings, ordered)

    except Refused as exc:
        refusals.append(exc)
        rep.phase(exc.phase, 'REFUSED', exc.problems[0].split('\n')[0][:60])
    except Exception as exc:                                   # noqa: BLE001
        refusals.append(Refused('internal', '%s: %s'
                                % (type(exc).__name__, exc)))
        rep.h1('INTERNAL ERROR — a bug in the runner, not a finding about the '
               'client')
        rep.line(traceback.format_exc().splitlines())
        rep.phase('internal', 'ERROR', str(exc)[:60])

    # ---- the tree guard runs ALWAYS, and overrides every other verdict
    if guard is not None and guard.before is not None:
        rep.h1('CLIENT-TREE GUARD — verify')
        clean, lines, probs = guard.verify()
        rep.line(lines)
        if not clean:
            rep.line('')
            for p in probs:
                rep.line('  REFUSED: %s' % p)
            rep.phase('TREE', 'DIRTY', probs[0][:60])
            refusals.append(Refused('TREE', probs))
        else:
            rep.line('')
            rep.line('  CLEAN — the client tree is byte-for-byte as it was '
                     'before this run.')
            rep.phase('TREE', 'CLEAN', 'client tree unchanged')

    # ---- verdict
    # The exit code is ONE number and a cron acts on it, so when several
    # phases refuse it must be the one worth acting on first: PRECEDENCE
    # decides, and every refusal is still listed. A dirty client tree
    # outranks everything -- it is an incident, not a finding.
    if refusals:
        chosen = min(refusals,
                     key=lambda r: PRECEDENCE.index(r.phase)
                     if r.phase in PRECEDENCE else len(PRECEDENCE))
        code = EXIT.get(chosen.phase, EXIT['internal'])
    else:
        chosen = None
        code = EXIT['ok']

    rep.h1('VERDICT')
    for name, state, detail in rep.phase_results:
        rep.line('  %-10s %-9s %s' % (name, state, detail))
    rep.line('')
    if not refusals:
        rep.line('  PASS — every phase EVALUATED. Upload proposal above.')
        rep.line('  Nothing has been uploaded. A human decides.')
    else:
        rep.line('  REFUSED. exit %d — %s' % (code, chosen.phase))
        rep.line('  NO UPLOAD PROPOSAL IS EMITTED. A phase that could not be '
                 'evaluated is not a phase that passed.')
        rep.line('')
        rep.line('  %d phase(s) refused, most actionable first:' % len(refusals))
        for r in sorted(refusals,
                        key=lambda r: PRECEDENCE.index(r.phase)
                        if r.phase in PRECEDENCE else len(PRECEDENCE)):
            rep.line('')
            rep.line('   %s  (exit %d if it were alone)'
                     % (r.phase, EXIT.get(r.phase, 1)))
            for pr in r.problems:
                rep.line('     - %s' % pr)
    rep.line('')
    rep.line('  exit %d' % code)

    path = rep.write()
    print('  report -> %s' % path, flush=True)
    print('  exit %d' % code, flush=True)
    return code


# --- sabotage helpers (sandbox only) ----------------------------------------

def sabotage_mapping(sandbox, mappings):
    """Copy the WHOLE mapping directory into the sandbox, then delete the one
    required field from the real TOML on disk.

    The first version of this mutated only the in-memory dict and copied the
    file unchanged, so `required_check.check()` re-read a pristine mapping,
    RESOLVE passed, and the run failed later at BUILD because `tables.toml`
    was no longer beside it. The test refused for the wrong reason and
    reported the wrong phase, which is worse than not testing: it read as
    evidence that RESOLVE could not be broken.

    So the whole directory is copied (siblings and all) and the field is
    struck from the file itself. Sandbox only -- editing `mappings/` would
    leave the repository broken for the next run, and editing a client tree
    would be the incident this runner exists to prove cannot happen.
    """
    target = next(iter(mappings))
    mpath, m = mappings[target]
    dst_dir = os.path.join(sandbox, '_sabotage')
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(os.path.dirname(mpath), dst_dir)
    dst = os.path.join(dst_dir, os.path.basename(mpath))

    victim = 'BaseItemCode'
    src = open(dst, encoding='utf-8').read()
    # Strike the [[fields]] block whose name is the victim. Bounded by the
    # next [[ table header, so the surrounding mapping stays valid TOML -- the
    # point is a mapping that PARSES and is missing a required field, not one
    # that fails to parse.
    pat = re.compile(r'\[\[fields\]\]\s*\nname\s*=\s*"%s".*?(?=\n\[\[)'
                     % victim, re.S)
    src2, n = pat.subn('', src, count=1)
    if not n:
        raise Refused('usage', 'sabotage could not find a [[fields]] block for '
                               '%s in %s' % (victim, dst))
    open(dst, 'w', encoding='utf-8').write(src2)

    import mapper
    m2, _tables = mapper.load_mapping(dst)
    out = dict(mappings)
    out[target] = (dst, m2)
    return out, ('struck the %s [[fields]] block from a sandbox COPY of the '
                 'whole %s mapping directory — %s is the ONE field '
                 'products.csv requires'
                 % (victim, os.path.basename(os.path.dirname(mpath)), victim))


def blank_a_column(path):
    """Empty one populated column in a produced file, in place, in the sandbox."""
    import csv
    with open(path, newline='', encoding='utf-8') as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 2:
        return
    header = rows[0]
    # pick a column that is populated on most rows and is not the key
    best, bestn = None, 0
    for i, h in enumerate(header[1:], 1):
        n = sum(1 for r in rows[1:] if i < len(r) and r[i].strip())
        if n > bestn:
            best, bestn = i, n
    if best is None:
        return
    for r in rows[1:]:
        if best < len(r):
            r[best] = ''
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        csv.writer(fh, lineterminator='\r\n').writerows(rows)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(EXIT['internal'])
