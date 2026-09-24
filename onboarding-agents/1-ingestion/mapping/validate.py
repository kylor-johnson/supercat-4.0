#!/usr/bin/env python3
"""Class-2 validation — CHECK a pre-mapped file, do not re-map it.

The rule (KICKOFF_mapping.md § three input classes): a file whose headers are
already `BaseItemCode` / `BillToCode` has had its mapping done by a human.
Re-mapping it overrides a decision someone already made, usually silently and
usually wrongly. **The job on a class-2 file is checking it** -- fill rates,
value shapes, required fields -- and reporting where the human's mapping
disagrees with what eCat will accept.

So this module never changes a value. It reports. Everything it emits is a
MEASUREMENT with a specimen; consequences are stated separately and marked when
they are conditional, because a measurement and its consequence are two claims
(SCORECARD §12 R1).

Checks, each tied to a real incident:

  unrecognised column     an unrecognised header is a FATAL import error, and a
                          BLANK header cannot be imported at all
  unregistered custom     populated + unregistered = data DISCARDED on every
                          import, silently (BUILD_SPEC §3 B1b)
  boolean shape           eCat boolean filters match Y/y/T/t/1-9. A registered
                          binary field carrying Yes/No cannot match -- leg
                          shipped 13 empty filter chips this way (B1)
  case-duplicate values   two spellings of one value ship as two filter facets
  float tail              '810117540005.0' is a spreadsheet artifact reaching a
                          text field; 5+ dp reaching a money field is the same
                          shape (profiler SKILL.md)
  length overrun          against preflight/limits_generated.py, never a typed
                          number -- several documented limits are wrong
  empty required          a required field with no value
"""

import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'profiler'))

import ecat_vocab as vocab      # noqa: E402
import inputclass               # noqa: E402

BOOL_TOKENS = {'yes', 'no', 'true', 'false'}
ECAT_BOOL_MATCHES = "Y/y/T/t and digits 1-9"


def _limits():
    try:
        from preflight import limits_generated
        return limits_generated.LIMITS.get('products.csv', {})
    except Exception:
        return getattr(vocab, 'LIMITS', {}).get('products.csv', {}) \
            if hasattr(vocab, 'LIMITS') else {}


def check(rows, headers, target='products.csv', source_name='',
          declared_custom_fields=None):
    """Return a list of finding dicts. Every finding carries a specimen."""
    findings = []
    n = len(rows)
    if not n:
        return [{'level': 'FATAL', 'check': 'empty',
                 'text': 'no data rows', 'specimen': None}]

    verdict = inputclass.classify(headers, target)
    limits = _limits()
    known = {h.lower() for h in vocab.PRODUCTS['distinctive']}
    declared = {c.lower() for c in (declared_custom_fields or [])}

    def col(h):
        return [(r.get(h) or '').strip() for r in rows]

    # -- structural --------------------------------------------------------
    if verdict['blank_headers']:
        findings.append({
            'level': 'FATAL', 'check': 'blank header',
            'text': '%d column(s) have a BLANK header. A blank header cannot be '
                    'imported and an unrecognised column is a FATAL import error.'
                    % verdict['blank_headers'],
            'specimen': '(unnamed column)'})

    for h in verdict['required_missing']:
        findings.append({'level': 'FATAL', 'check': 'required missing',
                         'text': 'required field %r has no column' % h,
                         'specimen': None})

    # -- per column --------------------------------------------------------
    for h in headers:
        h = (h or '').strip()
        if not h:
            continue
        values = col(h)
        filled = [v for v in values if v]
        fill_pct = round(100.0 * len(filled) / n, 1)

        if h.lower() not in known and not inputclass._patterned(h, target):
            level = 'BLOCKING' if filled else 'NOTE'
            registered = h.lower() in declared
            findings.append({
                'level': 'NOTE' if registered else level,
                'check': 'custom field',
                'text': '%r is not a built-in eCat field. %s Populated %d/%d '
                        '(%.1f%%). A column not registered in Admin is SILENTLY '
                        'DROPPED on every import.'
                        % (h, 'Declared for registration.' if registered
                           else 'NOT declared for registration.',
                           len(filled), n, fill_pct),
                'specimen': filled[0][:60] if filled else '(empty)'})

        if not filled:
            # A declared-but-empty column is the leg B1 shape: 13 fields warned
            # missing, went clean 61 minutes later, and remain empty across all
            # 1,020 products. An empty built-in field is worse than an absent
            # one when the field is the thing a rep reads.
            findings.append({
                'level': 'BLOCKING' if h.lower() in known else 'NOTE',
                'check': 'declared but empty',
                'text': '%r is present as a column and has NO value on any of '
                        'the %d rows.%s' % (h, n,
                        ' It is a built-in eCat field.' if h.lower() in known else ''),
                'specimen': '(0 of %d populated)' % n})
            continue

        distinct = collections.Counter(filled)

        # boolean shape
        low = {v.lower() for v in distinct}
        if low and low <= BOOL_TOKENS:
            findings.append({
                'level': 'BLOCKING', 'check': 'boolean shape',
                'text': '%r is binary (%s) but carries Yes/No. eCat boolean '
                        'filters match only %s, so IF this field is registered '
                        'as an iPad filter the chip cannot match. %d values.'
                        % (h, '/'.join(sorted(distinct)), ECAT_BOOL_MATCHES,
                           len(filled)),
                'specimen': '%s = %r' % (list(distinct)[0], distinct.most_common(1)[0][0])})

        # case-duplicate values
        folded = collections.defaultdict(set)
        for v in distinct:
            folded[v.lower()].add(v)
        dupes = {k: sorted(v) for k, v in folded.items() if len(v) > 1}
        if dupes:
            k0 = sorted(dupes)[0]
            findings.append({
                'level': 'BLOCKING', 'check': 'case-duplicate value',
                'text': '%r has %d value(s) differing only by case. Each spelling '
                        'ships as its own filter facet.' % (h, len(dupes)),
                'specimen': ' vs '.join(repr(x) for x in dupes[k0])})

        # float tails
        # NOT a percentage threshold. An earlier version required the tail on
        # >50% of rows and missed libco's ShipWeight, which carries it on 39%
        # (322 of 822) because only whole-number weights get one. A systematic
        # spreadsheet artifact does not become acceptable at 39% prevalence --
        # the tail is wrong on every row that has it.
        tails = [v for v in filled if re.match(r'^-?\d+\.0$', v)]
        if len(tails) >= 3:
            findings.append({
                'level': 'BLOCKING', 'check': 'float tail',
                'text': '%r carries a spreadsheet float tail on %d of %d rows '
                        '(%d populated). The importer takes the tail verbatim.'
                        % (h, len(tails), n, len(filled)),
                'specimen': tails[0]})
        long_tails = [v for v in filled if re.match(r'^-?\d+\.\d{5,}$', v)]
        if long_tails:
            findings.append({
                'level': 'BLOCKING', 'check': 'binary-float tail',
                'text': '%r has %d value(s) with 5+ decimal places — a rounding '
                        'artifact, not a value.' % (h, len(long_tails)),
                'specimen': long_tails[0]})

        # datetime reaching a text/date field
        dt = [v for v in filled if re.match(r'^\d{4}-\d{2}-\d{2} 00:00:00$', v)]
        if dt:
            findings.append({
                'level': 'BLOCKING', 'check': 'datetime not date',
                'text': '%r carries a datetime on %d/%d values where eCat wants '
                        'YYYY-MM-DD.' % (h, len(dt), n),
                'specimen': dt[0]})

        # length overrun, against the GENERATED limits
        spec = limits.get(h.lower())
        if spec and spec.get('limit'):
            over = [v for v in filled if len(v) > spec['limit']]
            if over:
                findings.append({
                    'level': 'BLOCKING' if spec.get('tier') == 'error' else 'NOTE',
                    'check': 'length overrun',
                    'text': '%r exceeds its %d-char limit (%s tier) on %d/%d rows.'
                            % (h, spec['limit'], spec.get('tier', '?'), len(over), n),
                    'specimen': over[0][:70]})

    return findings, verdict


def render(findings, verdict, source_name=''):
    out = ['=' * 74,
           'CLASS-2 VALIDATION — %s' % (source_name or 'file'),
           '=' * 74,
           inputclass.report(verdict, source_name),
           '']
    order = {'FATAL': 0, 'BLOCKING': 1, 'NOTE': 2}
    counts = collections.Counter(f['level'] for f in findings)
    out.append('findings: %s' % (', '.join('%d %s' % (counts[k], k)
                                           for k in sorted(counts, key=lambda x: order.get(x, 9)))
                                 or 'none'))
    out.append('')
    for f in sorted(findings, key=lambda f: (order.get(f['level'], 9), f['check'])):
        out.append('[%-8s] %-22s %s' % (f['level'], f['check'], f['text']))
        if f['specimen'] is not None:
            out.append('%s specimen: %s' % (' ' * 12, f['specimen']))
    out.append('')
    out.append('Every count above ships a specimen. Consequences marked "IF ..." are')
    out.append('conditional and have NOT been verified against this org\'s Admin config.')
    return '\n'.join(out)
