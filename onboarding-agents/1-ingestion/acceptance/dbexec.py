#!/usr/bin/env python3
"""Read-only DATABASE_URL execution for the acceptance modules.

`collector.py:197-217` and `rawstate.py:216-227` already had this; the four
modules that gate an upload did not. They offered `--emit-sql` and
`--from-results` only, which means **a human has to carry rows between two
commands**. That is fine at a desk and fatal on a cron: the gate cannot run in
a container, so the container can produce files it is structurally unable to
check. A replica credential alone would not have fixed it -- the credential had
nowhere to be used.

So this is the third copy of those ten lines, written once instead of four
times. Each module keeps its own `--from-results` shape and assembles that
shape itself; this file only knows how to open a read-only session, refuse a
statement that is not a read, and hand back rows.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not become the default. `--emit-sql` / `--from-results` stays the
documented path, because on this machine there is no `DATABASE_URL` and no
`psycopg2` (verified 2026-09-09 on both `/usr/bin/python3` and
`/opt/homebrew/bin/python3`), and the only reachable database is the
`supercat-postgres-vpn` MCP. `--use-db` is the path a container takes once a
read-only replica DSN exists. Until then it must fail LOUDLY and say exactly
what is missing -- never fall back to something that looks like an answer.

READ-ONLY IS ENFORCED THREE TIMES, not asserted once
----------------------------------------------------
1. `set_session(readonly=True)` on the connection,
2. `SET default_transaction_read_only = on` on the session,
3. `assert_read_only()` on every statement text before it is sent.

Three because the first two are promises made to the driver about a DSN whose
privileges nobody here can inspect, and the third is the only one that holds if
the DSN turns out to be a superuser against production. The acceptance harness
exists because "it ran clean" is not evidence of correctness; the same
scepticism applies to its own database access.
"""

import os
import re
import sys

# Indirected so a test can substitute a fake driver. Without this the
# read-only guard and the statement splitters are unreachable on any machine
# that lacks psycopg2 -- which is every machine this has run on so far, and
# untested plumbing in an upload gate is the whole failure mode being fixed.
_DRIVER = None


class DbUnavailable(RuntimeError):
    """No usable read-only database path. Always names what is missing."""


# A statement this module will send. Anything else is refused -- including
# anything with a second statement hidden after a semicolon, which is why the
# callers split on their own markers and pass one statement at a time.
_READ_START = re.compile(r'^\s*(?:--[^\n]*\n|\s)*(WITH|SELECT|EXPLAIN|SHOW)\b',
                         re.I)
_FORBIDDEN = re.compile(
    r'\b(INSERT|UPDATE|DELETE|TRUNCATE|DROP|CREATE|ALTER|GRANT|REVOKE|COPY|'
    r'VACUUM|REINDEX|CLUSTER|REFRESH|CALL|DO|SET|RESET|LOCK)\b', re.I)


def dsn():
    """The DSN, or None. Never invents one."""
    return os.environ.get('DATABASE_URL') or None


def available():
    return dsn() is not None


def strip_sql_comments(sql):
    """Remove line and block comments so the guard reads the real statement.

    Without this, `-- B7 stage 1: live density, products` trips the FORBIDDEN
    scan on nothing at all, and a comment mentioning DELETE semantics -- which
    these modules' comments do, constantly, because delete semantics are the
    subject -- would refuse a plain SELECT.
    """
    sql = re.sub(r'/\*.*?\*/', ' ', sql, flags=re.S)
    sql = re.sub(r'--[^\n]*', ' ', sql)
    return sql


def assert_read_only(sql):
    """Refuse anything that is not a single read. Raises DbUnavailable."""
    bare = strip_sql_comments(sql).strip().rstrip(';')
    if not bare:
        raise DbUnavailable('empty statement')
    if ';' in bare:
        raise DbUnavailable(
            'statement contains a semicolon after stripping comments, so it is '
            'more than one statement. Split it and send one at a time:\n  %s'
            % bare[:200])
    if not _READ_START.match(bare):
        raise DbUnavailable('not a read: statement starts %r' % bare[:60])
    hit = _FORBIDDEN.search(bare)
    if hit:
        raise DbUnavailable('refusing to send a statement containing %s'
                            % hit.group(1).upper())
    return True


def _driver():
    global _DRIVER
    if _DRIVER is not None:
        return _DRIVER
    try:
        import psycopg2
        import psycopg2.extras  # noqa: F401
    except ImportError:
        raise DbUnavailable(
            'psycopg2 is not installed on %s.\n'
            '  pip install psycopg2-binary\n'
            'Or drop --use-db and go through the MCP with '
            '--emit-sql / --from-results.' % sys.executable)
    _DRIVER = psycopg2
    return _DRIVER


class ReadOnlySession:
    """A read-only psycopg2 session that returns dict rows."""

    def __init__(self, url=None):
        url = url or dsn()
        if not url:
            raise DbUnavailable(
                'DATABASE_URL is not set.\n'
                '  There is no direct Postgres credential on this machine '
                '(SESSION_HANDOFF constraint 2); the only DB access is the\n'
                '  supercat-postgres-vpn MCP. Use --emit-sql, run the SQL '
                'read-only through the MCP, then --from-results.')
        drv = _driver()
        self._drv = drv
        self.conn = drv.connect(url)
        self.conn.set_session(readonly=True, autocommit=True)
        # Belt to the set_session braces: if this DSN's role can write, the
        # transaction still cannot.
        with self.conn.cursor() as cur:
            cur.execute('SET default_transaction_read_only = on')

    def rows(self, sql):
        """Run ONE read statement, return a list of dicts."""
        assert_read_only(sql)
        import psycopg2.extras
        with self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            if cur.description is None:
                return []
            return [dict(r) for r in cur.fetchall()]

    def close(self):
        try:
            self.conn.close()
        except Exception:                                     # noqa: BLE001
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


# --- statement splitters ----------------------------------------------------
# Each acceptance module emits its statements in its own shape, and the shape
# is load-bearing: the operator has been feeding these back by hand into a
# named key. Parsing the SAME emitted text the operator would have run keeps
# --use-db and --from-results on one code path, so the two cannot drift into
# disagreeing about what was measured.

def split_marked(text, pattern, flags=re.M):
    """Split emitted SQL on a marker regex whose group(1) names the statement.

    Returns [(name, sql), ...] in emitted order.
    """
    rx = re.compile(pattern, flags)
    hits = list(rx.finditer(text))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.start():end].strip().rstrip(';').strip()
        out.append((m.group(1).strip(), body))
    return out


def main():
    """Self-check: prove the guard rejects what it claims to reject.

    Runs without a database on purpose. The guard is the part that has to be
    right when a DSN finally appears, and it is the part nobody would notice
    was wrong.
    """
    cases = [
        ('SELECT 1', True),
        ('WITH a AS (SELECT 1) SELECT * FROM a', True),
        ('-- a comment mentioning DELETE and TRUNCATE\nSELECT 1', True),
        ('/* block DROP */ SELECT 1', True),
        ('SELECT 1;', True),
        ('DELETE FROM products', False),
        ('SELECT 1; DROP TABLE products', False),
        ('UPDATE organizations SET shortname = %s', False),
        ('SET default_transaction_read_only = off', False),
        ('', False),
        ('SELECT 1 -- ; DROP TABLE t', True),
    ]
    bad = 0
    for sql, want in cases:
        try:
            assert_read_only(sql)
            got = True
        except DbUnavailable:
            got = False
        ok = got == want
        bad += 0 if ok else 1
        print('  %-4s %-8s %s' % ('ok' if ok else 'FAIL',
                                  'allow' if want else 'refuse',
                                  sql.replace('\n', '\\n')[:56]))
    print()
    print('  evaluated %d of %d guard cases; %d wrong' % (len(cases), len(cases), bad))
    print('  DATABASE_URL : %s' % ('set' if available() else 'NOT SET'))
    try:
        _driver()
        drv = 'psycopg2 present'
    except DbUnavailable as e:
        drv = str(e).splitlines()[0]
    print('  driver       : %s' % drv)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
