#!/usr/bin/env python3
"""ecat-source-profile — FOLDER MODE.

Answers, before any column is parsed:

  1. Which files are catalog source vs Library content vs noise
  2. Which files are near-duplicates, and which of those is authoritative
  3. Which files are DERIVED COPIES of another file in the same folder
     (same content, different format) - a different mechanism from (2)
  4. Which eCat file each candidate is trying to be
  5. What is missing entirely

Read-only. Opens files, writes nothing but its own report.

Two rules it is built around:
  - Never print a zero that was not verified. Anything undetermined prints as
    "undetermined" with the reason, never as 0 or "none".
  - A measurement and its consequence are separate claims. This tool emits
    measurements and clearly-labelled inferences. It does not emit consequences.
"""

import csv
import hashlib
import io
import json
import os
import re
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ecat_vocab import (  # noqa: E402
    TARGETS, REQUIRED_HEADERS, norm, is_ecat_header, patterned_match,
    semantic_scores, key_expectation,
)

# --- file class constants --------------------------------------------------

TABULAR_EXT = {'.csv', '.tsv', '.txt', '.xlsx', '.xls', '.xlsm'}
LIBRARY_EXT = {
    '.pdf', '.mp4', '.mov', '.m4v', '.pptx', '.ppt', '.docx', '.doc',
    '.jpg', '.jpeg', '.png', '.gif', '.tif', '.tiff', '.webp', '.eps', '.ai',
    '.zip', '.md', '.html', '.htm',
}
# Tabular *intent*, but not machine-readable without a conversion step.
OPAQUE_EXT = {'.numbers', '.pages', '.key', '.accdb', '.mdb'}
NOISE_NAMES = {'.ds_store', 'thumbs.db', 'desktop.ini', 'icon\r'}
NOISE_PREFIX = ('~$', '._')
NOISE_EXT = {'.icloud', '.tmp', '.bak', '.lock'}

DERIVED_DIR_HINT = re.compile(
    r'(^|/)(_converted|converted|_derived|_generated|_backup|_old|_archive|archive|'
    r'_superseded|old|backup)(/|$)', re.I)

ENCODINGS = ['utf-8-sig', 'utf-8', 'cp1252', 'mac_roman', 'latin-1']


# --- helpers ---------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sniff_magic(path):
    """What the file ACTUALLY is, from its leading bytes.

    Never trust the extension. Legrand ships XLSX workbooks named .csv; routing
    those to a text decoder produces a bogus "encoding problem" and hides the
    fact that the file is a ZIP container.
    """
    try:
        with open(path, 'rb') as f:
            head = f.read(8)
    except OSError:
        return None
    if head[:4] == b'PK\x03\x04':
        try:
            import zipfile
            names = set(zipfile.ZipFile(path).namelist())
            if 'xl/workbook.xml' in names:
                return 'xlsx'
            if 'word/document.xml' in names:
                return 'docx'
            if 'ppt/presentation.xml' in names:
                return 'pptx'
        except Exception:
            pass
        return 'zip'
    if head[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
        return 'ole2'          # legacy .xls / .doc
    if head[:4] == b'%PDF':
        return 'pdf'
    if head[:3] == b'\xff\xd8\xff':
        return 'jpg'
    if head[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'
    return 'text'


def classify_path(path, root):
    base = os.path.basename(path)
    low = base.lower()
    ext = os.path.splitext(low)[1]
    if low in NOISE_NAMES or low.startswith(NOISE_PREFIX) or ext in NOISE_EXT:
        return 'noise', 'OS/editor artifact, not client content'
    if ext in OPAQUE_EXT:
        return 'opaque', 'tabular intent but not machine-readable (%s)' % ext
    if ext in TABULAR_EXT:
        return 'tabular', ''
    if ext in LIBRARY_EXT:
        return 'library', 'Library content (%s)' % ext.lstrip('.')
    return 'unknown', 'unrecognised extension %r' % ext


def decode_bytes(raw):
    """Return (text, encoding, note). Never raises."""
    first_bad = None
    for enc in ENCODINGS:
        try:
            txt = raw.decode(enc)
        except UnicodeDecodeError as e:
            if enc in ('utf-8', 'utf-8-sig') and first_bad is None:
                first_bad = e.start
            continue
        if enc in ('latin-1', 'mac_roman'):
            note = ('NOT valid UTF-8 (first bad byte at offset %s); decoded with %s '
                    'as a fallback - byte-for-byte lossless but the character '
                    'mapping is a guess, needs a human eye' % (first_bad, enc))
        elif first_bad is not None:
            note = 'decoded as %s; not valid UTF-8 (first bad byte at %s)' % (enc, first_bad)
        else:
            note = ''
        return txt, enc, note
    return None, None, 'undecodable by any of: %s' % ', '.join(ENCODINGS)


def sniff_delimiter(sample):
    try:
        return csv.Sniffer().sniff(sample, delimiters=',;\t|').delimiter
    except Exception:
        counts = {d: sample.count(d) for d in [',', ';', '\t', '|']}
        best = max(counts, key=counts.get)
        return best if counts[best] else ','


def read_tabular(path, ext, actual=None):
    """Return dict with rows (list of list), encoding, delimiter, notes, error.

    `actual` is the magic-byte type and OVERRIDES the extension when they disagree.
    """
    out = {'encoding': None, 'delimiter': None, 'notes': [], 'error': None,
           'rows': None, 'sheet': None}
    if ext in ('.xlsx', '.xlsm') or actual == 'xlsx':
        try:
            import openpyxl
            # Pass a handle, not a path: openpyxl refuses on file EXTENSION,
            # which would reject the very files whose extension is the lie.
            with open(path, 'rb') as _fh:
                _buf = io.BytesIO(_fh.read())
            wb = openpyxl.load_workbook(_buf, read_only=True, data_only=True)
            # Take the sheet with the most populated cells, not sheet 1. A cover
            # or notes sheet in position 1 otherwise masks the real data, and
            # multi-sheet workbooks are common (tcs ships six).
            best, best_rows, sizes = None, None, []
            for nm in wb.sheetnames:
                ws = wb[nm]
                rows = [['' if c is None else str(c) for c in r]
                        for r in ws.iter_rows(values_only=True)]
                filled = sum(1 for r in rows for c in r if str(c).strip())
                sizes.append((nm, len(rows), filled))
                if best_rows is None or filled > best[2]:
                    best, best_rows = (nm, len(rows), filled), rows
            wb.close()
            out['rows'] = best_rows
            out['encoding'] = 'n/a (xlsx)'
            out['delimiter'] = 'n/a (xlsx)'
            out['sheet'] = best[0]
            out['sheets'] = sizes
            if len(sizes) > 1:
                others = ', '.join('%r (%d rows)' % (n, r) for n, r, _ in sizes if n != best[0])
                out['notes'].append(
                    'workbook has %d sheets; profiled %r as the most populated. '
                    'NOT profiled: %s - each may be a separate source file'
                    % (len(sizes), best[0], others))
        except Exception as e:
            out['error'] = 'openpyxl failed: %s' % e
        return out
    if ext == '.xls' or actual == 'ole2':
        try:
            import xlrd
            bk = xlrd.open_workbook(path) if ext == '.xls' else xlrd.open_workbook(
                file_contents=open(path, 'rb').read())
            sh = bk.sheet_by_index(0)
            out['rows'] = [[('' if c is None else str(c)) for c in sh.row_values(i)]
                           for i in range(sh.nrows)]
            out['encoding'] = 'n/a (xls)'
            out['delimiter'] = 'n/a (xls)'
            out['sheet'] = '%s (of %d sheet(s))' % (sh.name, bk.nsheets)
        except Exception as e:
            out['error'] = 'xlrd failed: %s' % e
        return out

    with open(path, 'rb') as f:
        raw = f.read()
    if not raw.strip():
        out['error'] = 'file is empty (0 bytes of content)'
        return out
    # Embedded control characters. These are why file(1) reports "data" and why a
    # file gets called "binary" when it is in fact plain ASCII with an ERP marker
    # in it. Report the character and where it is; do not call it an encoding fault.
    ctrl = {}
    for b in set(raw):
        if b < 32 and b not in (9, 10, 13):
            ctrl[b] = raw.count(bytes([b]))
    txt, enc, note = decode_bytes(raw)
    if txt is None:
        out['error'] = note
        return out
    out['encoding'] = enc
    if note:
        out['notes'].append(note)
    if ctrl:
        names = {0x1a: 'SUB/EOF (CP/M-DOS)', 0x1c: 'FS file-separator (mainframe/AS400 EOF)',
                 0x1d: 'GS group-separator', 0x1e: 'RS record-separator',
                 0x0c: 'FF form-feed', 0x00: 'NUL'}
        bits = []
        for b, c in sorted(ctrl.items()):
            off = raw.find(bytes([b]))
            pct = 100.0 * off / max(1, len(raw))
            bits.append('0x%02X %s x%d, first at byte %d (%.0f%% through the file)'
                        % (b, names.get(b, 'control char'), c, off, pct))
        out['notes'].append(
            'contains embedded control characters - this is why file(1) calls it '
            '"data"; the text itself is %s. %s' % (enc, '; '.join(bits)))
        out['control_chars'] = {'0x%02X' % b: c for b, c in ctrl.items()}
    delim = sniff_delimiter(txt[:65536])
    out['delimiter'] = delim
    try:
        out['rows'] = list(csv.reader(io.StringIO(txt), delimiter=delim))
    except Exception as e:
        out['error'] = 'csv parse failed: %s' % e
    return out


def find_header_row(rows, scan=25):
    """Locate the header row. Returns (index, reason).

    Scores each candidate row on: how many cells are non-empty, how many are
    distinct, how many are recognised eCat field names, and penalises rows that
    look like prose instructions to a human rather than column names.
    """
    best, best_score, reason = None, -1.0, ''
    for i, row in enumerate(rows[:scan]):
        cells = [str(c).strip() for c in row]
        nonempty = [c for c in cells if c]
        if len(nonempty) < 2:
            continue
        distinct = len(set(c.lower() for c in nonempty))
        ecat_hits = sum(1 for c in nonempty if is_ecat_header(norm(c)))
        longish = sum(1 for c in nonempty if len(c) > 60)
        shouty = sum(1 for c in nonempty if c.startswith('*') or c.endswith('!'))
        numeric = sum(1 for c in nonempty if re.fullmatch(r'-?[\d.,$%]+', c))
        score = (len(nonempty) * 1.0
                 + distinct * 1.0
                 + ecat_hits * 6.0
                 - longish * 4.0
                 - shouty * 6.0
                 - numeric * 2.0
                 - i * 0.6)
        if score > best_score:
            best, best_score = i, score
            bits = ['%d non-empty cells' % len(nonempty), '%d distinct' % distinct]
            if ecat_hits:
                bits.append('%d recognised eCat field names' % ecat_hits)
            if shouty:
                bits.append('%d cells look like instructions, penalised' % shouty)
            reason = ', '.join(bits)
    if best is None:
        return None, 'no row in the first %d had 2+ non-empty cells' % scan
    return best, reason


def score_target(headers_norm, raw_headers):
    """Score the header set against each eCat target. Returns ordered list."""
    scores = []
    patt_by_target = {}
    for h in headers_norm:
        pm = patterned_match(h)
        if pm:
            patt_by_target.setdefault(pm[0], []).append(h)
    for name, spec in TARGETS.items():
        dist = spec['distinctive']
        hit = headers_norm & dist
        n_patt = len(patt_by_target.get(name, []))
        has_key = spec['key'] in headers_norm
        # fraction of the target's distinctive vocabulary present
        cover = len(hit) / float(len(dist)) if dist else 0.0
        score = len(hit) + n_patt * 0.5 + (2.0 if has_key else 0.0)
        scores.append({
            'target': name, 'score': round(score, 2), 'coverage': round(cover, 3),
            'matched': sorted(hit), 'patterned': sorted(patt_by_target.get(name, [])),
            'has_key': has_key, 'key': spec['key'],
        })
    scores.sort(key=lambda d: (-d['score'], d['target']))
    return scores


def classify_input(headers_norm, raw_headers):
    """Three input classes from the kickoff, plus hybrid."""
    n = len(headers_norm)
    if not n:
        return 'undetermined', 'no headers parsed', 0.0
    ecat = {h for h in headers_norm if is_ecat_header(h)}
    frac = len(ecat) / float(n)
    non_ecat = n - len(ecat)
    if frac >= 0.75:
        return ('pre-mapped',
                '%d of %d headers are eCat field names (%.0f%%) - VALIDATE, do not re-map'
                % (len(ecat), n, frac * 100), frac)
    if frac >= 0.25:
        return ('hybrid',
                '%d of %d headers are eCat field names (%.0f%%), %d are client-domain '
                'columns carried alongside' % (len(ecat), n, frac * 100, non_ecat), frac)
    if frac > 0:
        return ('raw (with incidental eCat-shaped names)',
                '%d of %d headers match eCat names (%.0f%%) - too few to be a mapping'
                % (len(ecat), n, frac * 100), frac)
    return ('raw', 'no header matches an eCat field name - needs mapping', 0.0)


def detect_transposed_options(rows, hi, headers):
    """Find an option stack TRANSPOSED sideways into a product sheet.

    THE PHASE 0 FALSE NEGATIVE THIS FIXES. Folder mode reported `options.csv`
    and `option_groups.csv` MISSING for tcs. They are not missing. 72 columns of
    its Master sheet, between `Propane Tip` and `Seeded Replacement Glass - SRG`,
    ARE the option stack: each header is an option NAME and each cell is an
    option CODE where that SKU can take it. The build emits OptionSet1-8 from
    them.

    A check whose whole job is saying what a source folder contains, reporting
    ABSENT when the thing is present, is the worst shape of failure available to
    it -- it does not merely fail to help, it actively tells you to go and ask
    the client for a file they already sent.

    THE SIGNATURE, and each clause is there because dropping it produced a false
    positive on one of the five client folders:

      * the header is NOT an eCat field name and NOT itself code-shaped
        (a header that is a code is a pivot table, not an option block)
      * every non-blank cell is <= 15 chars -- the option Code limit, which is
        what makes a column of codes different from a column of prose
      * few distinct values: <= 25, or exactly 1 (a pure availability flag)
      * SPARSE: fill < 95%. An option column says which products CAN take it,
        so a fully-populated column is an attribute, not an availability flag
      * and it runs CONTIGUOUSLY for >= 8 columns. One such column is a code
        field; eight in a row is a matrix

    Returns None or a dict. Conservative by construction: it would rather say
    nothing than mis-call a product sheet.
    """
    if hi is None or not headers:
        return None
    body = rows[hi + 1:]
    if len(body) < 5:
        return None
    n = len(body)
    CODE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9 ._/#?-]{0,14}$')

    def code_shaped(v):
        """A CODE, not a word.

        `Country of Origin` holds `China` and `Weiyan` holds `Yes`. Both are <=
        15 chars, both are sparse, both have one distinct value -- and neither
        is an option code. What separates them from `BLK`, `GPR`, `CSP10` and
        `FH?` is that a code is not an ordinary word: it carries a digit, or it
        is all upper case, or it has a separator.

        Dropping this clause pulled `Country of Origin` and `Replacement SKU`
        into the front of tcs's block and put a country in the option stack.
        """
        if not CODE.match(v):
            return False
        if not any(ch.isalpha() for ch in v):
            # A NUMBER is not a code. mer's item export has nine consecutive
            # price-list columns (`5. All Pro Stock`, `7. Distributor`,
            # `Amazon`) holding 239.4, 68.4, 6.95 -- sparse, few distinct, under
            # 15 chars, and a clean false positive until this line. A price is
            # the single most common thing to find in a sparse numeric column on
            # a product sheet, so the detector has to say so out loud.
            return False
        if any(ch.isdigit() for ch in v):
            return True
        if any(ch in '._/#?-' for ch in v):
            return True
        return v.isupper()
    NULLS = {'----', '---', '--', '-', 'n/a', 'na', 'none'}

    flags = []       # True = option-shaped, False = breaks a run, None = neutral
    percol = []
    for ci, h in enumerate(headers):
        hn = norm(h)
        vals = [str(r[ci]).strip() for r in body if ci < len(r)]
        nb = [v for v in vals if v and v.lower() not in NULLS]
        distinct = set(nb)
        if bool(h.strip()) and not nb and not is_ecat_header(hn):
            # An ENTIRELY EMPTY column is neutral: it neither is nor is not an
            # option column, and it must not break a run. tcs has six of them
            # sitting inside the block (`Weiyan` and `Single 12-V Base` are
            # empty in Master, populated in Weiyan LED). Treating them as breaks
            # cut a 72-column stack into a 21-column one and under-reported the
            # finding by two thirds.
            flags.append(None)
            percol.append({'header': h, 'filled': 0, 'distinct': 0, 'values': []})
            continue
        ok = bool(h.strip()) and bool(nb) and not is_ecat_header(hn)
        if ok:
            # >= 90%, not all. `Farm House Hook` carries the literal value `FH?`
            # -- a human's question mark left in the data -- and one such cell
            # broke a 72-column run into 35. A block is code-shaped in aggregate;
            # requiring purity makes the detector fail on exactly the messy
            # sheets it exists for. The stragglers are reported, not ignored.
            conform = sum(1 for v in nb if code_shaped(v)) / float(len(nb))
            ok = conform >= 0.9
        if ok:
            ok = len(distinct) <= 40
        if ok:
            ok = (len(nb) / float(n)) < 0.95 or len(distinct) == 1
        if ok:
            # A header that is itself short and code-shaped is a pivot column,
            # not an option name. Option names are words.
            # ALL-CAPS and short: `BLK`, `WGS`. That is a pivot column whose
            # header is itself a code. An option NAME is a word, and words are
            # not excluded by this — `e-lyte` is lowercase and hyphenated and
            # was being thrown out, which cut three columns off the front of
            # tcs's block.
            ok = not (re.match(r'^[A-Z0-9][A-Z0-9._/-]*$', h.strip())
                      and len(h.strip()) <= 8 and ' ' not in h.strip())
        flags.append(ok)
        percol.append({'header': h, 'filled': len(nb), 'distinct': len(distinct),
                       'values': sorted(distinct)[:6]})

    best = (0, 0, 0)
    i = 0
    while i < len(flags):
        if flags[i] is not True:
            i += 1
            continue
        j = i
        while j < len(flags) and flags[j] is not False:
            j += 1
        while j > i and flags[j - 1] is not True:   # do not end on a neutral
            j -= 1
        real = sum(1 for k in range(i, j) if flags[k] is True)
        if real > best[0]:
            best = (real, i, j)
        i = j
    run, a, b = best
    if run < 8:
        return None

    vocab = set()
    for ci in range(a, b):
        vocab |= set(percol[ci]['values'])
    return {
        'first_column': headers[a], 'last_column': headers[b - 1],
        'first_index': a, 'last_index': b - 1, 'columns': run,
        'span': b - a,
        'empty_inside': sum(1 for k in range(a, b) if flags[k] is None),
        'rows': n,
        'distinct_codes': sum(percol[ci]['distinct'] for ci in range(a, b)),
        'specimens': [(percol[ci]['header'], percol[ci]['values'][:3])
                      for ci in range(a, b) if flags[ci] is True][:3],
        'vocab': vocab,
    }


def key_candidates(rows, header_i, headers, limit=4):
    """Columns that look like a key: high uniqueness, high fill, code-shaped."""
    data = rows[header_i + 1:]
    if not data:
        return []
    out = []
    for ci, h in enumerate(headers):
        vals = []
        for r in data:
            if ci < len(r):
                v = str(r[ci]).strip()
                if v:
                    vals.append(v)
        if not vals:
            continue
        fill = len(vals) / float(len(data))
        uniq = len(set(vals)) / float(len(vals))
        codeish = sum(1 for v in vals[:400] if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._\-/]{1,39}', v))
        codefrac = codeish / float(min(len(vals), 400))
        score = uniq * 2 + fill + codefrac
        out.append({'column': h, 'index': ci, 'fill': round(fill, 3),
                    'uniqueness': round(uniq, 3), 'code_shaped': round(codefrac, 3),
                    'score': round(score, 3), 'values': set(vals)})
    out.sort(key=lambda d: -d['score'])
    return out[:limit]


# --- profiling one file ----------------------------------------------------

def profile_file(path, root):
    rel = os.path.relpath(path, root)
    st = os.stat(path)
    ext = os.path.splitext(path)[1].lower()
    cls, why = classify_path(path, root)
    rec = OrderedDict()
    rec['rel'] = rel
    rec['bytes'] = st.st_size
    rec['mtime'] = __import__('datetime').datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d')
    rec['class'] = cls
    rec['class_reason'] = why
    rec['in_derived_dir'] = bool(DERIVED_DIR_HINT.search(rel.replace(os.sep, '/')))
    rec['sha256'] = None
    rec['error'] = None

    if cls in ('noise',):
        return rec
    rec['sha256'] = sha256(path)

    # Content type from magic bytes. When it disagrees with the extension the
    # content wins, and the disagreement is itself a finding: a workbook named
    # .csv reads as an "encoding problem" to anything that trusts the name.
    actual = sniff_magic(path)
    rec['actual_format'] = actual
    EXT_EXPECT = {'.csv': 'text', '.tsv': 'text', '.txt': 'text',
                  '.xlsx': 'xlsx', '.xlsm': 'xlsx', '.xls': 'ole2',
                  '.pdf': 'pdf', '.jpg': 'jpg', '.jpeg': 'jpg', '.png': 'png'}
    expect = EXT_EXPECT.get(ext)
    if expect and actual and actual != expect:
        rec['format_mismatch'] = '%s named %s' % (actual, ext)
        if actual in ('xlsx', 'ole2') and cls != 'tabular':
            cls = 'tabular'
            rec['class'] = cls
        elif actual in ('pdf', 'jpg', 'png', 'docx', 'pptx') and cls == 'tabular':
            cls = 'library'
            rec['class'] = cls
            rec['class_reason'] = 'Library content (%s content named %s)' % (actual, ext)

    if cls in ('library', 'opaque', 'unknown'):
        return rec

    t = read_tabular(path, ext, rec.get('actual_format'))
    rec['encoding'] = t['encoding']
    rec['delimiter'] = t['delimiter']
    rec['sheet'] = t['sheet']
    rec['notes'] = t['notes']
    if t['error']:
        rec['error'] = t['error']
        return rec
    rows = t['rows']
    if not rows:
        rec['error'] = 'parsed but contains no rows'
        return rec

    hi, hreason = find_header_row(rows)
    rec['header_row'] = (hi + 1) if hi is not None else None   # 1-indexed, human
    rec['header_reason'] = hreason
    if hi is None:
        rec['error'] = 'could not locate a header row'
        return rec
    if hi > 0:
        rec['notes'].append(
            'header is on row %d, not row 1; rows 1-%d hold: %s'
            % (hi + 1, hi, ' | '.join(
                (' '.join(str(c) for c in rows[j] if str(c).strip())[:70] or '(blank)')
                for j in range(hi))))

    headers = [str(c).strip() for c in rows[hi]]
    headers = [h for h in headers]
    rec['columns'] = len(headers)

    # Trailing rows that carry no values are export artifacts, not records.
    # Counting them inflates a row count and can make a file look like it holds
    # one more entity than it does - which then corrupts every duplicate
    # comparison downstream.
    body = rows[hi + 1:]
    trailing = 0
    while body and not any(str(c).strip() for c in body[-1]):
        body.pop()
        trailing += 1
    rec['data_rows'] = len(body)
    rec['trailing_blank_rows'] = trailing
    if trailing:
        rec['notes'].append(
            '%d trailing row(s) with no values excluded from the row count '
            '(export terminator, not a record)' % trailing)
    rows = rows[:hi + 1] + body
    rec['headers_sample'] = headers[:12]
    hn = {norm(h) for h in headers if h}
    rec['headers_norm'] = sorted(hn)

    cls_in, cls_why, frac = classify_input(hn, headers)
    rec['input_class'] = cls_in
    rec['input_class_reason'] = cls_why
    rec['ecat_header_fraction'] = round(frac, 3)

    ts = score_target(hn, headers)
    rec['target_scores'] = ts
    top = ts[0]
    if top['score'] >= 3:
        rec['target'] = top['target']
        rec['target_basis'] = 'eCat header match (score %.1f, %d distinctive fields%s)' % (
            top['score'], len(top['matched']),
            ', key %s present' % top['key'] if top['has_key'] else ', KEY ABSENT')
        rec['target_confidence'] = 'high' if top['score'] >= 6 else 'moderate'
    else:
        sem = semantic_scores(headers)
        best = max(sem, key=sem.get)
        if sem[best] >= 4:
            rec['target'] = best
            rec['target_basis'] = ('SEMANTIC GUESS from client-domain header words '
                                   '(%d keyword families), NOT eCat header evidence'
                                   % sem[best])
            rec['target_confidence'] = 'low - inference'
        else:
            rec['target'] = None
            rec['target_basis'] = ('undetermined: %d eCat header matches, best semantic '
                                   'family count %d (%s)' % (top['score'], sem[best], best))
            rec['target_confidence'] = 'undetermined'
        rec['semantic'] = sem

    rec['transposed_options'] = detect_transposed_options(rows, hi, headers)

    kc = key_candidates(rows, hi, headers)
    rec['key_candidates'] = [
        {k: v for k, v in d.items() if k != 'values'} for d in kc]
    # Key selection is driven by the eCat file this claims to be, not by raw
    # uniqueness. customers.csv repeats BillToCode across ship-to rows by design,
    # so a uniqueness gate rejects the real key and reports "undetermined".
    keycol, expect_unique, shape = key_expectation(rec.get('target'), hn)
    rec['key_semantics'] = None
    keysets = {}
    if keycol and keycol in hn:
        for ci, h in enumerate(headers):
            if norm(h) != keycol:
                continue
            vals = [str(r[ci]).strip() for r in rows[hi + 1:]
                    if ci < len(r) and str(r[ci]).strip()]
            if not vals:
                break
            uniq = len(set(vals)) / float(len(vals))
            keysets[h] = set(vals)
            ok = (uniq > 0.999) if expect_unique else True
            rec['key_semantics'] = {
                'column': h, 'rows': len(vals), 'distinct': len(set(vals)),
                'expected_shape': shape, 'matches_expectation': ok,
                'note': ('%d rows over %d distinct %s - %s'
                         % (len(vals), len(set(vals)), h,
                            'as expected for %s' % rec['target'] if ok
                            else 'UNEXPECTED: %s wants %s' % (rec['target'], shape))),
            }
            break
    if not keysets:
        # Target unknown: fall back to the uniqueness heuristic, and only trust
        # genuinely key-shaped columns for cross-file comparison.
        keysets = {d['column']: d['values'] for d in kc[:2]
                   if d['uniqueness'] >= 0.9 and d['fill'] >= 0.5}
    rec['_keysets'] = keysets
    return rec


# --- cross-file relations --------------------------------------------------

def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def relate(recs):
    """Find exact duplicates, derived copies, and near-duplicates."""
    tab = [r for r in recs if r.get('class') == 'tabular' and not r.get('error')]
    exact, derived, near = [], [], []

    by_hash = {}
    for r in recs:
        if r.get('sha256'):
            by_hash.setdefault(r['sha256'], []).append(r['rel'])
    for h, group in by_hash.items():
        if len(group) > 1:
            exact.append({'sha256': h[:12], 'files': sorted(group)})

    for i in range(len(tab)):
        for j in range(i + 1, len(tab)):
            a, b = tab[i], tab[j]
            ha, hb = set(a['headers_norm']), set(b['headers_norm'])
            hj = jaccard(ha, hb)
            ea = os.path.splitext(a['rel'])[1].lower()
            eb = os.path.splitext(b['rel'])[1].lower()
            same_rows = a['data_rows'] == b['data_rows']
            diff_format = (ea in ('.xlsx', '.xls', '.xlsm')) != (eb in ('.xlsx', '.xls', '.xlsm'))

            if diff_format and hj >= 0.85 and same_rows:
                # DIRECTION is a separate claim from RELATEDNESS. Byte-identity
                # settles relatedness; nothing here settles which came first.
                # mtime is worthless in this tree (a 2026-09-03 bulk merge stamped
                # nearly every file) and a directory called _converted is a
                # filename, not evidence. Say undetermined.
                identical = a['sha256'] == b['sha256']
                derived.append({
                    'a': a['rel'], 'b': b['rel'], 'identical': identical,
                    'evidence': 'same %d data rows, header overlap %.0f%%, different '
                                'declared format%s' % (
                                    a['data_rows'], hj * 100,
                                    '; BYTE-IDENTICAL (sha256 %s) so one is a pure '
                                    'rename of the other and either may be dropped'
                                    % a['sha256'][:12] if identical else
                                    '; contents differ, so this is a real conversion'),
                    'direction': ('moot - byte-identical' if identical
                                  else 'UNDETERMINED - no evidence in the folder says '
                                       'which was produced from which'),
                })
                continue

            keyov, contain = None, None
            ka = a.get('_keysets') or {}
            kb = b.get('_keysets') or {}
            if ka and kb:
                best, best_contain = 0.0, 0.0
                for va in ka.values():
                    for vb in kb.values():
                        j = jaccard(va, vb)
                        if j > best:
                            best = j
                        # Containment, not Jaccard: a 421-row file whose keys all
                        # appear in a 3,517-row file is SUPERSEDED by it, not a
                        # complementary slice of it. Jaccard alone reads 12% and
                        # says "union them" - the opposite of the right answer.
                        small, large = (va, vb) if len(va) <= len(vb) else (vb, va)
                        if small:
                            best_contain = max(best_contain,
                                               len(small & large) / float(len(small)))
                keyov, contain = best, best_contain

            if hj >= 0.6 or (keyov is not None and keyov >= 0.5):
                kind, verdict = classify_relation(a, b, hj, keyov, contain)
                near.append({
                    'kind': kind, 'verdict': verdict,
                    'a': a['rel'], 'b': b['rel'],
                    'a_rows': a['data_rows'], 'b_rows': b['data_rows'],
                    'a_class': a.get('input_class'), 'b_class': b.get('input_class'),
                    'a_target': a.get('target'), 'b_target': b.get('target'),
                    'header_overlap': round(hj, 3),
                    'key_overlap': round(keyov, 3) if keyov is not None else None,
                })
    return exact, derived, near


def division_token(rel_a, rel_b):
    """If two paths differ by exactly one alphanumeric token, return that pair.

    Evidence comes from the folder itself - no hard-coded brand names.
    """
    split = lambda s: [t for t in re.split(r'[^A-Za-z0-9]+', os.path.basename(s)) if t]
    ta, tb = split(rel_a), split(rel_b)
    if len(ta) != len(tb):
        return None
    diffs = [(x, y) for x, y in zip(ta, tb) if x.lower() != y.lower()]
    if len(diffs) != 1:
        return None
    x, y = diffs[0]
    # A version bump ("2.0" vs "3.0") is not a division.
    if re.fullmatch(r'[\d.]+', x) or re.fullmatch(r'[\d.]+', y):
        return None
    if len(x) > 6 or len(y) > 6:
        return None
    return diffs[0]


def classify_relation(a, b, hj, keyov, contain=None):
    """Name the relationship between two files, and say what to DO about it.

    The four outcomes are genuinely different actions, and conflating them is
    how folders get pruned wrongly:

      rival-version          -> choose one; the other is stale
      complementary-partition-> UNION them; choosing one silently drops records
      mapping-pair           -> keep both; one is the source of the other
      key-linked             -> expected cross-file join (products <-> inventory)
    """
    ta, tb = a.get('target'), b.get('target')
    same_target = ta is not None and ta == tb

    # Per-division files. Two files of the same shape whose names differ by exactly
    # one token are usually one dataset split by brand/warehouse. eCat merges those
    # into a single file with per-division columns (Price_<div>_<code>,
    # <DIV>_QtyOnHand) - it does not choose between them. Calling this a rival
    # version would delete a division's data.
    div = division_token(a['rel'], b['rel'])
    if div and hj >= 0.6:
        return ('division-variant',
                'same shape (%.0f%% headers); the filenames differ by exactly one token '
                '(%s vs %s). This is one dataset split by division, not two versions. '
                'eCat merges divisions into ONE file with per-division columns; choosing '
                'between them drops a division.' % (hj * 100, div[0], div[1]))
    classes = [a.get('input_class', ''), b.get('input_class', '')]
    mapped_side = any(c.startswith(('pre-mapped', 'hybrid')) for c in classes)
    raw_side = any(c.startswith('raw') for c in classes)
    ko = keyov if keyov is not None else -1.0

    # One file's keys wholly inside the other's: superseded, not complementary.
    if (contain is not None and contain >= 0.95 and hj >= 0.6
            and a['data_rows'] != b['data_rows']):
        big, small = (a, b) if a['data_rows'] > b['data_rows'] else (b, a)
        return ('superseded',
                'every key in %s (%d rows) also appears in %s (%d rows) - the smaller '
                'is a strict SUBSET, superseded by the larger. Build from the larger; '
                'the smaller adds nothing.'
                % (os.path.basename(small['rel']), small['data_rows'],
                   os.path.basename(big['rel']), big['data_rows']))

    # Same shape, disjoint keys: two slices of one dataset, not two versions of it.
    if hj >= 0.85 and 0 <= ko <= 0.15:
        return ('complementary-partition',
                'identical column shape but the key sets barely intersect (%.0f%%) - '
                'these are two SLICES of one dataset, not two versions of it. '
                'UNION them. Picking one silently drops the other slice.' % (ko * 100))

    # Same entities, different vocabulary: one is the mapped form of the other.
    if ko >= 0.5 and hj < 0.3 and mapped_side and raw_side and (same_target or ta is None or tb is None):
        return ('mapping-pair',
                'key overlap %.0f%% with header overlap only %.0f%% - the same records '
                'expressed twice, one raw and one mapped. Keep both; reconcile the '
                'mapping against the raw file.' % (ko * 100, hj * 100))

    # Different eCat targets sharing a key: that is the schema working as designed.
    if ta and tb and not same_target and ko >= 0.5:
        return ('key-linked',
                'different eCat targets (%s / %s) sharing %.0f%% of their keys - this is '
                'the expected products<->inventory<->stories join, not a duplicate.'
                % (ta, tb, ko * 100))

    if hj >= 0.6 and ko >= 0.5:
        return ('rival-version',
                'same shape (%.0f%% headers) and same records (%.0f%% keys) at different '
                'row counts - one supersedes the other. AUTHORITY NOT DECIDABLE FROM THE '
                'FOLDER: reconcile row counts against the live org.' % (hj * 100, ko * 100))

    return ('unresolved',
            'header overlap %.0f%%, key overlap %s - related but the relationship does '
            'not fit a known pattern. Needs a human look.'
            % (hj * 100, ('%.0f%%' % (ko * 100)) if ko >= 0 else 'undetermined'))


# --- report ----------------------------------------------------------------

def human_bytes(n):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if n < 1024 or unit == 'GB':
            return '%.1f %s' % (n, unit) if unit != 'B' else '%d B' % n
        n /= 1024.0


def report(root, recs, exact, derived, near, out=sys.stdout):
    w = out.write
    w('\n' + '=' * 78 + '\n')
    w('FOLDER: %s\n' % root)
    w('=' * 78 + '\n')

    buckets = OrderedDict([('tabular', []), ('library', []), ('opaque', []),
                           ('noise', []), ('unknown', [])])
    for r in recs:
        buckets[r['class']].append(r)

    total_bytes = sum(r['bytes'] for r in recs)
    w('%d files, %s total\n' % (len(recs), human_bytes(total_bytes)))
    for k, v in buckets.items():
        if v:
            w('  %-8s %3d files  %10s\n'
              % (k, len(v), human_bytes(sum(r['bytes'] for r in v))))

    derived_set = set()
    for d in derived:
        if d['identical']:
            derived_set.add(sorted([d['a'], d['b']])[1])

    w('\n-- CATALOG SOURCE CANDIDATES ' + '-' * 48 + '\n')
    cands = [r for r in buckets['tabular'] if r['rel'] not in derived_set]
    if not cands:
        w('  none parsed\n')
    for r in cands:
        w('\n  %s\n' % r['rel'])
        w('    %s | %s | modified %s\n'
          % (human_bytes(r['bytes']), r.get('encoding') or '?', r['mtime']))
        if r.get('error'):
            w('    !! COULD NOT PROFILE: %s\n' % r['error'])
            continue
        w('    %s rows x %s cols | delimiter %r | header on row %s (%s)\n'
          % (r['data_rows'], r['columns'], r.get('delimiter'),
             r.get('header_row'), r.get('header_reason')))
        for n in r.get('notes', []):
            w('    NOTE: %s\n' % n)
        w('    input class : %s - %s\n' % (r['input_class'], r['input_class_reason']))
        if r.get('target'):
            w('    trying to be: %s [%s]\n' % (r['target'], r['target_confidence']))
            w('                  basis: %s\n' % r['target_basis'])
        else:
            w('    trying to be: UNDETERMINED - %s\n' % r['target_basis'])
        kcs = r.get('key_candidates') or []
        if kcs:
            k = kcs[0]
            w('    key candidate: %r (uniqueness %.0f%%, fill %.0f%%)\n'
              % (k['column'], k['uniqueness'] * 100, k['fill'] * 100))
        w('    headers: %s%s\n' % (', '.join(r['headers_sample']),
                                   ' ...' if r['columns'] > 12 else ''))

    if buckets['library']:
        w('\n-- LIBRARY CONTENT ' + '-' * 58 + '\n')
        ext_c = {}
        for r in buckets['library']:
            e = os.path.splitext(r['rel'])[1].lower()
            ext_c.setdefault(e, [0, 0])
            ext_c[e][0] += 1
            ext_c[e][1] += r['bytes']
        for e, (c, b) in sorted(ext_c.items(), key=lambda kv: -kv[1][1]):
            w('  %-6s %3d files  %10s\n' % (e, c, human_bytes(b)))

    if buckets['opaque']:
        w('\n-- TABULAR BUT UNREADABLE ' + '-' * 51 + '\n')
        for r in buckets['opaque']:
            w('  %s  (%s) - %s\n' % (r['rel'], human_bytes(r['bytes']), r['class_reason']))

    if buckets['noise']:
        w('\n-- NOISE ' + '-' * 68 + '\n')
        for r in buckets['noise']:
            w('  %s - %s\n' % (r['rel'], r['class_reason']))

    if derived:
        w('\n-- FORMAT TWINS (same content, different declared format) ' + '-' * 20 + '\n')
        for d in derived:
            w('  %s\n  %s\n    evidence: %s\n    which came first: %s\n'
              % (d['a'], d['b'], d['evidence'], d['direction']))

    if exact:
        w('\n-- BYTE-IDENTICAL DUPLICATES ' + '-' * 48 + '\n')
        for e in exact:
            w('  sha %s: %s\n' % (e['sha256'], ', '.join(e['files'])))

    titles = OrderedDict([
        ('superseded', 'SUPERSEDED  -> the smaller is a strict subset, drop it'),
        ('rival-version', 'RIVAL VERSIONS  -> choose one, the other is stale'),
        ('division-variant', 'DIVISION VARIANTS  -> merge into one file, do NOT choose'),
        ('complementary-partition', 'COMPLEMENTARY PARTITIONS  -> union them, do NOT choose'),
        ('mapping-pair', 'MAPPING PAIRS  -> keep both, one is the source of the other'),
        ('key-linked', 'KEY-LINKED  -> expected cross-file join, not a duplicate'),
        ('unresolved', 'UNRESOLVED RELATIONS  -> needs a human'),
    ])
    for kind, title in titles.items():
        group = [n for n in near if n['kind'] == kind]
        if not group:
            continue
        w('\n-- %s %s\n' % (title, '-' * max(2, 74 - len(title))))
        for n in sorted(group, key=lambda d: -(d['header_overlap'])):
            w('  %s (%s rows)\n  %s (%s rows)\n'
              % (n['a'], n['a_rows'], n['b'], n['b_rows']))
            w('    %s\n' % n['verdict'])

    w('\n-- eCAT TARGET COVERAGE ' + '-' * 53 + '\n')
    found = {}
    for r in cands:
        if r.get('target'):
            found.setdefault(r['target'], []).append(
                (r['rel'], r.get('target_confidence')))

    # TRANSPOSED OPTION STACKS. `options.csv` is not missing from tcs's folder;
    # it is sideways, 72 columns inside the Master sheet. Reporting MISSING sent
    # a reader to ask the client for a file they had already supplied. A check
    # that says what a folder contains must not answer "absent" for "present in
    # a shape I did not look for".
    sideways = [r for r in recs if r.get('transposed_options')]
    catalogues = []
    if sideways:
        vocab = set()
        for r in sideways:
            vocab |= r['transposed_options'].pop('vocab', set())
        # The codes have to BE something. If another file's key column contains
        # most of them, that file is the option CATALOGUE -- what the options
        # are -- and the sideways block is the availability MATRIX -- who can
        # have which. Two sources, two questions. Missing this on tcs cost the
        # blind run its option names, descriptions, prices and type partition:
        # 338 of 341 options were rows of a sheet already in the folder.
        for r in recs:
            if r.get('transposed_options') or not r.get('_keysets'):
                continue
            for col, vals in r['_keysets'].items():
                if not vals or not vocab:
                    continue
                cover = len(vocab & set(vals)) / float(len(vocab))
                if cover >= 0.5:
                    catalogues.append((r['rel'], col, cover, len(vals)))
        catalogues.sort(key=lambda t: -t[2])

    for t in REQUIRED_HEADERS:
        if t in found:
            for rel, conf in found[t]:
                w('  %-18s CANDIDATE  %s [%s]\n' % (t, rel, conf))
        elif t == 'option_groups.csv' and sideways:
            w('  %-18s PRESENT, TRANSPOSED  same block as options.csv above — '
              'the\n' % t)
            w('  %-18s   groups are the per-product COMBINATIONS of those '
              'codes.\n' % '')
        elif t == 'options.csv' and sideways:
            for r in sideways:
                d = r['transposed_options']
                w('  %-18s PRESENT, TRANSPOSED  inside %s\n' % (t, r['rel']))
                w('  %-18s   %d contiguous columns, %s .. %s (index %d-%d), '
                  '%d distinct codes over %d rows\n'
                  % ('', d['columns'], d['first_column'], d['last_column'],
                     d['first_index'], d['last_index'], d['distinct_codes'],
                     d['rows']))
                for hdr, vals in d['specimens']:
                    w('  %-18s   e.g. %-32s -> %s\n'
                      % ('', hdr, ', '.join(vals) or '(blank)'))
            w('  %-18s   the header is the option NAME, the cell is the option '
              'CODE.\n' % '')
            w('  %-18s   NOT missing. Do not ask the client for it.\n' % '')
        else:
            w('  %-18s MISSING    no file in this folder resolves to it\n' % t)

    if catalogues:
        w('\n  OPTION CATALOGUE — the codes in that block resolve against:\n')
        for rel, col, cover, nvals in catalogues[:3]:
            w('    %s  column %r  contains %.0f%% of the codes (%d keys)\n'
              % (rel, col, 100 * cover, nvals))
        w('    That file is WHAT the options are (name, price, type); the\n')
        w('    sideways block is WHO can have which. Map both.\n')
    elif sideways:
        w('\n  No file in this folder carries those codes as a key. The option\n')
        w('  NAMES are the column headers and there is no price or type source.\n')

    # BUILD_SPEC §3.4 — every check states its coverage.
    scanned = [r for r in recs if r.get('header_row')]
    w('\n  COVERAGE — evaluated %d of %d files for a target (%d parsed a header '
      'row; %d were binary, noise or unparseable). Transposed-stack detection '
      'ran on those same %d and fired on %d.\n'
      % (len(scanned), len(recs), len(scanned), len(recs) - len(scanned),
         len(scanned), len(sideways)))
    w('\n')


def profile_folder(root):
    recs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in sorted(filenames):
            recs.append(profile_file(os.path.join(dirpath, fn), root))
    recs.sort(key=lambda r: r['rel'])
    exact, derived, near = relate(recs)
    return recs, exact, derived, near


def main():
    args = sys.argv[1:]
    json_out = None
    if '--json' in args:
        i = args.index('--json')
        json_out = args[i + 1]
        del args[i:i + 2]
    all_json = {}
    for root in args:
        root = root.rstrip('/')
        if not os.path.isdir(root):
            sys.stderr.write('NOT A DIRECTORY: %s\n' % root)
            continue
        recs, exact, derived, near = profile_folder(root)
        report(root, recs, exact, derived, near)
        all_json[root] = {
            'files': [{k: v for k, v in r.items() if not k.startswith('_')} for r in recs],
            'exact_duplicates': exact, 'derived_copies': derived,
            'near_duplicates': near,
        }
    if json_out:
        with open(json_out, 'w') as f:
            json.dump(all_json, f, indent=2, default=str)
        sys.stderr.write('json -> %s\n' % json_out)


if __name__ == '__main__':
    main()
