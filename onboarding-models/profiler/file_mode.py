#!/usr/bin/env python3
"""ecat-source-profile — FILE MODE.

Answers the kickoff's six questions about ONE file:

  1. What is this?        rows, columns, encoding, delimiter, where the header is
  2. What's populated?    fill rate per column - a 3%-populated column is not a field
  3. What looks like a key?
  4. What maps to eCat?   proposed source-column -> eCat-field, WITH confidence
  5. What's missing?      required eCat fields with no plausible source column
  6. What doesn't add up?  internal contradictions

No transformation. No writes. It reads and reports.

It proposes a mapping and flags what it cannot map. It does not write transform
code, and it does not state a consequence it has not proved.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ecat_vocab import (  # noqa: E402
    TARGETS, REQUIRED_HEADERS, norm, is_ecat_header, patterned_match,
    semantic_scores, key_expectation,
)
from ecat_aliases import propose  # noqa: E402
from folder_mode import (  # noqa: E402
    read_tabular, find_header_row, sniff_magic, score_target, classify_input,
    human_bytes,
)

MONEYISH = re.compile(r'^\s*[-(]?\s*[$€£]?\s*[\d,]+(\.\d+)?\s*\)?\s*$')
INTISH = re.compile(r'^\s*-?\d+\s*$')
DECIMALISH = re.compile(r'^\s*-?\d+\.\d+\s*$')
DATEISH = re.compile(r'^\s*(\d{1,4}[-/]\d{1,2}[-/]\d{1,4})')

# Integer-typed eCat fields. A decimal here is a HARD validation error - the row
# is rejected, not truncated. (ecat-core-files, "Common build gotchas".)
INT_FIELDS = {
    'QtyOnHand', 'QtyAvailable', 'QtyReserved', 'QtyInTransit', 'QtyOnBackorder',
    'QtyOnPOrder', 'QtyOverseas', 'QtyInShowroom', 'NextReceiptQty',
    'PackQuantity', 'MinimumQuantity',
}


def column_stats(rows, hi, headers):
    data = rows[hi + 1:]
    n = len(data)
    stats = []
    for ci, h in enumerate(headers):
        vals = []
        for r in data:
            if ci < len(r):
                v = str(r[ci]).strip()
                if v:
                    vals.append(v)
        filled = len(vals)
        distinct = len(set(vals))
        sample = []
        seen = set()
        for v in vals:
            if v not in seen:
                seen.add(v)
                sample.append(v)
            if len(sample) == 3:
                break
        kinds = {'int': 0, 'decimal': 0, 'money': 0, 'date': 0, 'text': 0}
        for v in vals[:500]:
            if INTISH.match(v):
                kinds['int'] += 1
            elif DECIMALISH.match(v):
                kinds['decimal'] += 1
            elif MONEYISH.match(v):
                kinds['money'] += 1
            elif DATEISH.match(v):
                kinds['date'] += 1
            else:
                kinds['text'] += 1
        stats.append({
            'index': ci, 'header': h,
            'fill': (filled / float(n)) if n else None,
            'filled': filled, 'rows': n, 'distinct': distinct,
            'sample': sample, 'kinds': kinds,
            'maxlen': max((len(v) for v in vals), default=0),
            'values': set(vals),
        })
    return stats


def profile(path):
    rep = {'path': path}
    if not os.path.isfile(path):
        rep['error'] = 'not a file'
        return rep
    st = os.stat(path)
    ext = os.path.splitext(path)[1].lower()
    actual = sniff_magic(path)
    rep['bytes'] = st.st_size
    rep['declared'] = ext
    rep['actual'] = actual
    t = read_tabular(path, ext, actual)
    rep.update({k: t.get(k) for k in
                ('encoding', 'delimiter', 'sheet', 'sheets', 'notes', 'error')})
    if t['error']:
        return rep
    rows = t['rows']
    hi, hreason = find_header_row(rows)
    if hi is None:
        rep['error'] = 'could not locate a header row: %s' % hreason
        return rep
    rep['header_row'] = hi + 1
    rep['header_reason'] = hreason
    rep['preamble'] = [
        ' | '.join(c for c in (str(x).strip() for x in rows[j]) if c)
        for j in range(hi)]

    body = rows[hi + 1:]
    trailing = 0
    while body and not any(str(c).strip() for c in body[-1]):
        body.pop()
        trailing += 1
    rep['trailing_blank'] = trailing
    rows = rows[:hi + 1] + body

    headers = [str(c).strip() for c in rows[hi]]
    rep['columns'] = len(headers)
    rep['data_rows'] = len(body)
    rep['blank_headers'] = sum(1 for h in headers if not h)
    hn = {norm(h) for h in headers if h}

    ts = score_target(hn, headers)
    top = ts[0]
    if top['score'] >= 3:
        rep['target'], rep['target_conf'] = top['target'], (
            'high' if top['score'] >= 6 else 'moderate')
        rep['target_basis'] = 'eCat header match (%d distinctive fields%s)' % (
            len(top['matched']), ', key present' if top['has_key'] else ', KEY ABSENT')
    else:
        sem = semantic_scores(headers)
        best = max(sem, key=sem.get)
        if sem[best] >= 4:
            rep['target'], rep['target_conf'] = best, 'low - inference'
            rep['target_basis'] = ('client-domain keyword families only (%d), NOT eCat '
                                   'header evidence' % sem[best])
        else:
            rep['target'], rep['target_conf'] = None, 'undetermined'
            rep['target_basis'] = 'no eCat headers and too few domain keywords'
    rep['input_class'], rep['input_reason'], _ = classify_input(hn, headers)
    rep['stats'] = column_stats(rows, hi, headers)

    # --- 4. mapping proposal
    tgt_vocab = set()
    if rep['target'] and rep['target'] in TARGETS:
        tgt_vocab = set(TARGETS[rep['target']]['distinctive'])
        tgt_vocab.add(TARGETS[rep['target']]['key'])
    mapping, unmapped = [], []
    for s in rep['stats']:
        h = s['header']
        if not h:
            continue
        n = norm(h)
        pm = patterned_match(n)
        if n in tgt_vocab or (pm and pm[0] == rep['target']):
            mapping.append({'source': h, 'field': h, 'confidence': 'certain',
                            'why': 'already an eCat field name for %s' % rep['target']
                                   + (' (%s)' % pm[1] if pm else '')})
            continue
        if is_ecat_header(n):
            # Real eCat field name, but for a DIFFERENT file than this one.
            owner = next((t for t, v in TARGETS.items()
                          if n in v['distinctive'] or n == v['key']), None)
            mapping.append({
                'source': h, 'field': h, 'confidence': 'moderate',
                'why': 'is an eCat field name, but for %s - not for %s. In this file '
                       'it may hold something else entirely; check the values before '
                       'trusting the name' % (owner or 'another file', rep['target'])})
            continue
        p = propose(h)
        if p:
            mapping.append({'source': h, 'field': p[0], 'confidence': p[1], 'why': p[2]})
        else:
            unmapped.append(s)
    rep['mapping'] = mapping
    rep['unmapped_source'] = unmapped

    # --- 5. required eCat fields with no source
    tgt = rep['target']
    missing = []
    if tgt:
        have = {m['field'] for m in mapping}
        have_norm = {norm(f) for f in have}
        for req in REQUIRED_HEADERS.get(tgt, []):
            if req in hn or req in have_norm:
                continue
            near = [s['header'] for s in unmapped
                    if req[:4] in norm(s['header'])][:2]
            missing.append({
                'field': req,
                'reason': ('no source column maps to it'
                           + ('; closest unmapped headers: %s' % ', '.join(near)
                              if near else '; nothing in this file resembles it')),
            })
    rep['missing_required'] = missing

    # --- 6. what doesn't add up
    adds_up = []
    keycol, expect_unique, shape = key_expectation(tgt, hn)
    keystat = None
    for s in rep['stats']:
        if keycol and norm(s['header']) == keycol:
            keystat = s
            break
    rep['key_rivals'] = []
    if keystat is None:
        cands = [s for s in rep['stats']
                 if s['header'] and s['filled']
                 and s['distinct'] / float(s['filled']) > 0.95
                 and s['fill'] and s['fill'] > 0.9]
        # A purely numeric column that is unique is usually an ERP surrogate id,
        # not the code a rep searches by. Prefer code-shaped values, and keep the
        # rivals visible rather than silently picking one.
        def keyscore(s_):
            vals = list(s_['values'])[:300]
            if not vals:
                return -1
            numeric = sum(1 for v in vals if INTISH.match(v)) / float(len(vals))
            alnum = sum(1 for v in vals
                        if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]{1,39}', v)
                        and not INTISH.match(v)) / float(len(vals))
            return alnum * 2 - numeric
        cands.sort(key=keyscore, reverse=True)
        keystat = cands[0] if cands else None
        rep['key_rivals'] = cands[1:4]
    rep['key'] = keystat
    if keystat and expect_unique is not None:
        uniq = keystat['distinct'] / float(keystat['filled'] or 1)
        if expect_unique and uniq < 0.999:
            adds_up.append(
                'key %r has %d rows over %d distinct values; %s expects %s'
                % (keystat['header'], keystat['filled'], keystat['distinct'],
                   tgt, shape))
        elif not expect_unique:
            rep['key_note'] = (
                '%d rows over %d distinct %r - expected for %s (%s), NOT a key defect'
                % (keystat['filled'], keystat['distinct'], keystat['header'],
                   tgt, shape))

    for s in rep['stats']:
        if s['fill'] is None:
            continue
        if s['header'] and s['filled'] == 0:
            adds_up.append('column %r is present but has no values in any row - it is '
                           'a header, not a field' % s['header'])
        elif s['header'] and 0 < s['fill'] < 0.05:
            adds_up.append('column %r is %.1f%% populated (%d of %d) - too sparse to '
                           'treat as a field'
                           % (s['header'], s['fill'] * 100, s['filled'], s['rows']))
    if rep['blank_headers']:
        adds_up.append('%d column(s) have an empty header - they cannot be imported '
                       'and an unrecognised column is a FATAL import error'
                       % rep['blank_headers'])

    # A2: a price column that is one constant across the catalogue.
    for m in mapping:
        if 'Price' not in m['field'] and m['field'] != 'NetPrice':
            continue
        s = next((x for x in rep['stats'] if x['header'] == m['source']), None)
        if s and s['filled'] > 20 and s['distinct'] == 1:
            adds_up.append(
                'price column %r holds ONE distinct value (%s) across %d rows - '
                'the drf placeholder shape (BUILD_SPEC A2)'
                % (s['header'], s['sample'][0], s['filled']))

    # Decimals in integer-typed fields are a hard row rejection.
    for m in mapping:
        if m['field'] not in INT_FIELDS:
            continue
        s = next((x for x in rep['stats'] if x['header'] == m['source']), None)
        if s and s['kinds']['decimal']:
            adds_up.append(
                'column %r -> %s carries %d decimal value(s) in the first 500 rows; a '
                'decimal in an integer field is a HARD validation error and the row is '
                'rejected' % (s['header'], m['field'], s['kinds']['decimal']))

    # BaseItemCode length: 40 is the importer cap (limits_generated, tier 'error').
    if keystat and tgt in ('products.csv', 'inventory.csv', 'stories.csv'):
        over = [v for v in keystat['values'] if len(v) > 40]
        if over:
            adds_up.append('%d key value(s) exceed 40 chars - BaseItemCode over 40 is a '
                           'validation error and the row is rejected (e.g. %r)'
                           % (len(over), sorted(over, key=len)[-1][:50]))

    # Dates that are not dates.
    for m in mapping:
        if m['field'] != 'NextReceiptDate':
            continue
        s = next((x for x in rep['stats'] if x['header'] == m['source']), None)
        if s and s['kinds']['text']:
            bad = [v for v in list(s['values'])[:200] if not DATEISH.match(v)][:3]
            if bad:
                adds_up.append(
                    'column %r -> NextReceiptDate has non-date values (e.g. %s); prose '
                    'in a date field fails the import'
                    % (s['header'], ', '.join(repr(b) for b in bad)))
    # Two columns holding identical values are one field wearing two names -
    # and for price columns that decides how many price LEVELS the org needs.
    seen = {}
    for s_ in rep['stats']:
        if not s_['header'] or s_['filled'] < 10:
            continue
        sig = (s_['filled'], s_['distinct'], tuple(sorted(s_['values']))[:200])
        if sig in seen:
            adds_up.append(
                'columns %r and %r hold identical values (%d rows, %d distinct) - '
                'one field under two names, not two fields'
                % (seen[sig], s_['header'], s_['filled'], s_['distinct']))
        else:
            seen[sig] = s_['header']

    # Spreadsheet float artifacts. 96.95400000000001 is a binary-float rounding
    # tail, not a price; it must be rounded before it reaches a money column.
    for m in mapping:
        if 'Price' not in m['field'] and m['field'] not in (
                'NetPrice', 'PromotionPrice'):
            continue
        s_ = next((x for x in rep['stats'] if x['header'] == m['source']), None)
        if not s_:
            continue
        tails = [v for v in list(s_['values'])[:400]
                 if re.match(r'^-?\d+\.\d{5,}$', v)]
        if tails:
            adds_up.append(
                'column %r -> %s has %d value(s) with 5+ decimal places (e.g. %s) - '
                'spreadsheet float artifacts; round before import'
                % (s_['header'], m['field'], len(tails), tails[0]))

    rep['adds_up'] = adds_up
    return rep


# --- report ----------------------------------------------------------------

def show(rep, out=sys.stdout):
    w = out.write
    w('\n' + '=' * 78 + '\n')
    w('FILE: %s\n' % rep['path'])
    w('=' * 78 + '\n')
    if rep.get('error'):
        w('\n!! COULD NOT PROFILE: %s\n' % rep['error'])
        return

    w('\n1. WHAT IS THIS\n')
    w('   %s on disk\n' % human_bytes(rep['bytes']))
    if rep['actual'] and rep['declared'] and rep['actual'] not in (
            'text',) and rep['declared'] not in ('.xlsx', '.xlsm', '.xls'):
        w('   !! FORMAT MISMATCH: named %s, content is %s. Parsed as %s.\n'
          % (rep['declared'], rep['actual'], rep['actual']))
    else:
        w('   format      : %s (content agrees with the extension)\n' % rep['declared'])
    w('   encoding    : %s\n' % rep['encoding'])
    w('   delimiter   : %r\n' % rep['delimiter'])
    if rep.get('sheet'):
        w('   sheet       : %s\n' % rep['sheet'])
    for n in rep.get('notes') or []:
        w('   NOTE: %s\n' % n)
    w('   header row  : %d (%s)\n' % (rep['header_row'], rep['header_reason']))
    for i, line in enumerate(rep.get('preamble') or []):
        w('     row %d before it: %s\n' % (i + 1, line[:100] or '(blank)'))
    if rep['trailing_blank']:
        w('   %d trailing valueless row(s) excluded from the count\n'
          % rep['trailing_blank'])
    w('   %d data rows x %d columns\n' % (rep['data_rows'], rep['columns']))
    w('   input class : %s - %s\n' % (rep['input_class'], rep['input_reason']))
    w('   trying to be: %s [%s] - %s\n'
      % (rep['target'] or 'UNDETERMINED', rep['target_conf'], rep['target_basis']))

    w('\n2. WHAT\'S POPULATED\n')
    stats = sorted(rep['stats'], key=lambda s: (s['fill'] is None, -(s['fill'] or 0)))
    empty = [s for s in stats if s['filled'] == 0]
    sparse = [s for s in stats if 0 < (s['fill'] or 0) < 0.05]
    full = [s for s in stats if (s['fill'] or 0) >= 0.05]
    w('   %d columns: %d populated >=5%%, %d sparse (<5%%), %d entirely empty\n'
      % (len(stats), len(full), len(sparse), len(empty)))
    w('   %-34s %6s %8s  %s\n' % ('column', 'fill', 'distinct', 'sample'))
    for s in full[:40]:
        w('   %-34s %5.0f%% %8d  %s\n'
          % (s['header'][:34] or '(blank header)', s['fill'] * 100, s['distinct'],
             ', '.join(v[:18] for v in s['sample'])[:44]))
    if len(full) > 40:
        w('   ... %d more populated columns (see --all)\n' % (len(full) - 40))
    if sparse:
        w('   SPARSE (<5%%, not fields): %s\n'
          % ', '.join('%s %.1f%%' % (s['header'][:24], s['fill'] * 100)
                      for s in sparse[:12]))
    if empty:
        w('   EMPTY (0 values): %s\n'
          % ', '.join((s['header'][:24] or '(blank header)') for s in empty[:12]))

    w('\n3. WHAT LOOKS LIKE A KEY\n')
    k = rep.get('key')
    if not k:
        w('   UNDETERMINED - no column is both near-unique and near-fully populated.\n')
        w('   What would settle it: the client naming the item/customer identifier.\n')
    else:
        w('   %r - %d values, %d distinct, %.0f%% filled, max length %d\n'
          % (k['header'], k['filled'], k['distinct'], (k['fill'] or 0) * 100,
             k['maxlen']))
        if rep.get('key_note'):
            w('   %s\n' % rep['key_note'])
        for r in rep.get('key_rivals') or []:
            w('   also unique: %r (%d distinct, e.g. %s)\n'
              % (r['header'], r['distinct'], ', '.join(r['sample'][:2])))
        if rep.get('key_rivals'):
            w('   -> more than one column is unique. Which one the CLIENT calls the\n'
              '      item/customer code is not decidable from the file; ask.\n')

    w('\n4. WHAT MAPS TO eCAT\n')
    order = {'certain': 0, 'high': 1, 'moderate': 2, 'low': 3}
    for m in sorted(rep['mapping'], key=lambda m: order.get(m['confidence'], 9)):
        w('   %-32s -> %-26s [%s]\n'
          % (m['source'][:32], m['field'], m['confidence']))
        if m['why']:
            w('       %s\n' % m['why'])
    if not rep['mapping']:
        w('   nothing mapped\n')
    if rep['unmapped_source']:
        w('\n   UNMAPPED SOURCE COLUMNS (%d) - client-domain data with no eCat home:\n'
          % len(rep['unmapped_source']))
        for s in rep['unmapped_source'][:25]:
            w('     %-34s %s populated, e.g. %s\n'
              % ((s['header'][:34] or '(blank header)'),
                 ('%.0f%%' % (s['fill'] * 100)) if s['fill'] is not None else '?',
                 ', '.join(v[:16] for v in s['sample'])[:38]))
        if len(rep['unmapped_source']) > 25:
            w('     ... %d more\n' % (len(rep['unmapped_source']) - 25))
        w('     -> these become custom fields, option sets, or are dropped. That is a\n'
          '        decision for the client, not a default.\n')

    w('\n5. WHAT\'S MISSING\n')
    if rep['target'] is None:
        w('   Cannot list required fields: the target eCat file is undetermined.\n')
    elif not rep['missing_required']:
        w('   Every importer-required field for %s has a source column.\n' % rep['target'])
    else:
        for m in rep['missing_required']:
            w('   %-20s %s\n' % (m['field'], m['reason']))

    w('\n6. WHAT DOESN\'T ADD UP\n')
    if not rep['adds_up']:
        w('   No internal contradiction found by the checks this tool runs.\n')
        w('   That is not the same as "the file is correct" - cross-file and\n')
        w('   against-the-live-org checks are separate.\n')
    for a in rep['adds_up']:
        w('   - %s\n' % a)
    w('\n')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for p in args:
        show(profile(p))


if __name__ == '__main__':
    main()
