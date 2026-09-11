#!/usr/bin/env python3
"""Prove the --use-db wiring works, on a machine with no psycopg2 and no DSN.

There is no `DATABASE_URL` here and psycopg2 is installed on neither
interpreter (measured 2026-09-09). So the DATABASE_URL path in the four
acceptance modules is, on this machine, code that has never executed -- and
untested plumbing inside an upload gate is precisely the failure this whole
programme exists to stop. "It will work when the credential arrives" is a
capability claim, and a capability claim needs its own evidence.

So: substitute a fake driver, run the real code paths, and assert on what they
did. What this establishes, and it is worth being exact about the scope:

  1. every statement the four modules send is a READ, per dbexec's guard
  2. the session is opened read-only and closed
  3. --use-db assembles the SAME dict shape --from-results loads, and the
     downstream report path consumes it without special-casing
  4. statement KEYS agree between --emit-sql's banner and --use-db's dict --
     the F6 `_key()` defect (73 windows at WARN while looking evaluated) was a
     mismatch of exactly this kind

What it does NOT establish: that the SQL is correct against the real schema,
that psycopg2 accepts these strings, or that a replica DSN has the privileges.
Those need the credential. This is the half that can be known now.

usage: test_dbexec_wiring.py
"""

import io
import json
import os
import re
import sys
import types
import contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


# --- the fake driver --------------------------------------------------------

class _FakeCursor:
    def __init__(self, conn, dictrows):
        self.conn = conn
        self.dictrows = dictrows
        self.description = None
        self._rows = []

    def execute(self, sql, params=None):
        self.conn.sent.append(sql)
        if re.match(r'^\s*SET\b', sql, re.I):
            self.description = None
            self._rows = []
            return
        self._rows = self.conn.answer(sql)
        self.description = [('c',)] if self._rows is not None else None

    def fetchall(self):
        return list(self._rows or [])

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class _FakeConn:
    def __init__(self, answer):
        self.sent = []
        self.session = None
        self.closed = False
        self.answer = answer

    def cursor(self, cursor_factory=None):
        return _FakeCursor(self, cursor_factory is not None)

    def set_session(self, readonly=None, autocommit=None):
        self.session = {'readonly': readonly, 'autocommit': autocommit}

    def close(self):
        self.closed = True


def install_fake(answer):
    """Put a fake psycopg2 in sys.modules and return the connection holder."""
    holder = {}

    def connect(url):
        holder['conn'] = _FakeConn(answer)
        holder['url'] = url
        return holder['conn']

    pg = types.ModuleType('psycopg2')
    pg.connect = connect
    extras = types.ModuleType('psycopg2.extras')
    extras.RealDictCursor = object
    pg.extras = extras
    sys.modules['psycopg2'] = pg
    sys.modules['psycopg2.extras'] = extras
    import dbexec
    dbexec._DRIVER = None            # force re-resolution through the fake
    os.environ['DATABASE_URL'] = 'postgres://fake/readonly'
    return holder


# --- canned answers ---------------------------------------------------------

A1_SUMMARY = [{
    'target_shortname': 'leg', 'target_org_id': 273,
    'file_keys': 3, 'org_live_keys': 3, 'matched': 3,
    'new_to_org': 0, 'would_be_deleted': 0,
}]
A1_RIVALS = [{'shortname': 'leg', 'name': 'Legrand',
              'matched_keys': 3, 'pct_of_file': 100.0}]


def a1_answer(sql):
    return A1_RIVALS if 'rival orgs' in sql else A1_SUMMARY


def b7_answer(sql):
    if 'B7 stage 1' in sql:
        return [{'live_rows': 3, 'c_shortdesc': 3, 'c_longdesc': 3,
                 'c_netprice': 3}]
    if 'B7 stage 2' in sql:
        return [{'__key': 'A1', 'c_shortdesc': 'Widget',
                 'c_longdesc': 'Widget, Graphite', 'c_netprice': '1.00'}]
    return []


def generic_answer(sql):
    return []


# --- fixtures ---------------------------------------------------------------

PRODUCTS_CSV = (
    'BaseItemCode,ShortDesc,LongDesc,NetPrice\r\n'
    'A1,Widget,"Widget, Graphite",1.00\r\n'
    'A2,Widget,"Widget, White",2.00\r\n'
    'A3,Gadget,"Gadget, Black",3.00\r\n'
)


def write_fixture(tmp):
    p = os.path.join(tmp, 'products.csv')
    with open(p, 'w', newline='', encoding='utf-8') as fh:
        fh.write(PRODUCTS_CSV)
    return p


# --- the checks -------------------------------------------------------------

RESULTS = []


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    print('  %-6s %-52s %s' % ('ok' if ok else 'FAIL', name, detail))


def guard_all_reads(conn, label):
    import dbexec
    bad = []
    for sql in conn.sent:
        if re.match(r'^\s*SET\s+default_transaction_read_only', sql, re.I):
            continue
        try:
            dbexec.assert_read_only(sql)
        except dbexec.DbUnavailable as e:
            bad.append((sql.splitlines()[0][:60], str(e)))
    check('%s: every statement is a read' % label, not bad,
          '%d statement(s) sent' % len(conn.sent) if not bad else str(bad[:2]))


def test_a1(tmp):
    holder = install_fake(a1_answer)
    import a1_fingerprint as a1
    f = write_fixture(tmp)
    ftype, keycol, keys, blank, note = a1.read_keys(f)
    sql, err = a1.emit_sql(ftype, keys, 'leg')
    res = a1._results_from_db(sql)
    conn = holder['conn']
    check('A1: summary + rivals both fetched',
          'summary' in res and 'rivals' in res,
          'keys=%s' % sorted(res))
    check('A1: shape matches --from-results',
          isinstance(res['summary'], list) and 'would_be_deleted' in res['summary'][0])
    check('A1: session opened read-only',
          conn.session == {'readonly': True, 'autocommit': True},
          str(conn.session))
    check('A1: connection closed', conn.closed)
    guard_all_reads(conn, 'A1')
    # the reporting path must consume it unchanged
    lines, fatal, warn = a1.verdict(res['summary'][0], ftype, res['rivals'])
    check('A1: verdict runs on the --use-db dict', bool(lines) and not fatal,
          '%d lines, %d blocking' % (len(lines), len(fatal)))
    # and the two statements must not be one
    check('A1: rivals split off, not sent as one statement',
          len(conn.sent) >= 3, '%d sent (1 SET + 2 reads)' % len(conn.sent))


def test_b7(tmp):
    holder = install_fake(b7_answer)
    import b7_lossy as b7
    f = write_fixture(tmp)
    headers, body = b7.read_file(f)
    ftype, note = b7.detect_file_type(f, headers)
    meta, stmts = b7.emit_sql(f, ftype, headers, body, 'leg', 50)
    res = b7._results_from_db(meta, stmts)
    conn = holder['conn']
    check('B7: file type detected', ftype == 'products.csv', ftype or 'none')
    check('B7: density keyed BY LIVE TABLE',
          list(res['density']) == ['products'], str(list(res['density'])))
    check('B7: spotcheck rows returned', bool(res['spotcheck']),
          '%d row(s)' % len(res['spotcheck']))
    check('B7: shape matches --from-results',
          set(res) == {'meta', 'density', 'spotcheck'}, str(sorted(res)))
    check('B7: session read-only', conn.session == {'readonly': True, 'autocommit': True})
    guard_all_reads(conn, 'B7')
    out, blocking, warn, notchecked, spot, evaluated, compared = b7.report(
        meta, res, 10.0, 20.0)
    check('B7: report runs on the --use-db dict', evaluated > 0,
          'evaluated %d columns, %d blocking' % (evaluated, len(blocking)))
    # An unrecognised statement must raise, not be silently skipped: a
    # statement nobody ran must never look like a statement that returned zero.
    try:
        b7._results_from_db(meta, ['-- B7 stage 9: nonsense\nSELECT 1'])
        raised = False
    except RuntimeError:
        raised = True
    check('B7: unknown statement refuses rather than skips', raised)


def test_state_checks():
    holder = install_fake(generic_answer)
    import state_checks as sc
    names = sorted(sc.CHECKS)
    stmts = sc._statements('leg', names)
    keys = [k for k, _ in stmts]
    check('state_checks: header first, then checks',
          keys == ['header'] + names, str(keys))
    # --emit-sql banners must name the same keys, upper-cased
    buf = io.StringIO()
    argv = sys.argv
    sys.argv = ['state_checks.py', '--org', 'leg', '--emit-sql']
    try:
        with contextlib.redirect_stdout(buf):
            sc.main()
    finally:
        sys.argv = argv
    banners = re.findall(r'^-- ===== (\S+) =====$', buf.getvalue(), re.M)
    check('state_checks: --emit-sql banners == --use-db keys',
          banners == [k.upper() for k in keys], str(banners))
    import dbexec
    with dbexec.ReadOnlySession() as s:
        for _, sql in stmts:
            s.rows(sql)
    guard_all_reads(holder['conn'], 'state_checks')


def test_import_log():
    holder = install_fake(generic_answer)
    import import_log as il

    class A:
        mode = 'events'
        since = None
        limit = 60
    filt = il.org_filter('leg', None)
    seen = {}
    for mode in ('events', 'taxonomy', 'signatures', 'feed_pairs'):
        A.mode = mode
        seen[mode] = il._statement(A, filt)
    check('import_log: a statement per mode', len(set(seen.values())) == 4,
          '%d distinct' % len(set(seen.values())))
    import dbexec
    with dbexec.ReadOnlySession() as s:
        for sql in seen.values():
            s.rows(sql)
    guard_all_reads(holder['conn'], 'import_log')


def test_refuses_without_dsn():
    import dbexec
    saved = os.environ.pop('DATABASE_URL', None)
    try:
        try:
            dbexec.ReadOnlySession()
            ok = False
            detail = 'opened a session with no DSN'
        except dbexec.DbUnavailable as e:
            ok = 'DATABASE_URL is not set' in str(e)
            detail = str(e).splitlines()[0]
    finally:
        if saved:
            os.environ['DATABASE_URL'] = saved
    check('no DSN: refuses loudly, names what is missing', ok, detail)


def main():
    tmp = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'dbexec_wiring')
    os.makedirs(tmp, exist_ok=True)
    print('=' * 72)
    print('--use-db WIRING TEST  (fake driver; no database is contacted)')
    print('=' * 72)
    print()
    test_a1(tmp)
    print()
    test_b7(tmp)
    print()
    test_state_checks()
    print()
    test_import_log()
    print()
    test_refuses_without_dsn()
    print()
    failed = [n for n, ok, _ in RESULTS if not ok]
    print('-' * 72)
    print('evaluated %d of %d assertions; %d failed'
          % (len(RESULTS), len(RESULTS), len(failed)))
    print('NOT CHECKED: SQL correctness against the live schema, psycopg2 '
          'acceptance of these\n             strings, and replica privileges — '
          'all three need the credential.')
    print('-' * 72)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
