"""11. CSV IO.

Small, but it is where byte-identical output is won or lost. Every difference
below changes the bytes without changing the data, which is why it belongs in
one place rather than in sixty:

  newline=''      csv writes \\r\\n itself; without this Python adds another \\r
  encoding        utf-8-sig on READ (clients send BOMs), utf-8 on WRITE
  lineterminator  '\\r\\n' is csv's default; the live Legrand file uses it
  extrasaction    'ignore' hides a typo'd fieldname; 'raise' surfaces it
"""

import csv


def read_rows(path, encoding='utf-8-sig'):
    """Read a CSV into a list of dicts. utf-8-sig strips a BOM if present and is
    harmless if not, so it is the right default for anything a client sent."""
    with open(path, newline='', encoding=encoding) as fh:
        return list(csv.DictReader(fh))


def read_table(path, encoding='utf-8-sig'):
    """Read a CSV into (headers, rows-as-lists)."""
    with open(path, newline='', encoding=encoding) as fh:
        rows = list(csv.reader(fh))
    return (rows[0], rows[1:]) if rows else ([], [])


def write_rows(path, fieldnames, rows, encoding='utf-8', lineterminator='\r\n',
               extrasaction='raise'):
    """Write dict rows.

    `extrasaction='raise'` is deliberate. The csv default is to drop unknown
    keys silently, which turns a mistyped field name into a column that simply
    never appears - the same shape as leg's 13 registered-but-empty filter
    fields. Fail loudly instead.
    """
    with open(path, 'w', newline='', encoding=encoding) as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction=extrasaction,
                           lineterminator=lineterminator)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_table(path, header, rows, encoding='utf-8', lineterminator='\r\n'):
    with open(path, 'w', newline='', encoding=encoding) as fh:
        w = csv.writer(fh, lineterminator=lineterminator)
        if header:
            w.writerow(header)
        w.writerows(rows)


def sniff_bytes_equal(path_a, path_b):
    """True when two files are byte-identical. The Phase 1 acceptance test."""
    with open(path_a, 'rb') as a, open(path_b, 'rb') as b:
        return a.read() == b.read()
