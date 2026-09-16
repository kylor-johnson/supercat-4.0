#!/usr/bin/env python3
"""Convert a Python-literal (or JSON) list-of-dicts file to a CSV file.

Usage:
    _to_csv.py INPUT_FILE OUTPUT_CSV col1,col2,col3,...

Reads INPUT_FILE (Python repr or JSON text containing a list of dicts), then
writes OUTPUT_CSV with the provided column order. Datetime objects are
serialized as ISO-8601 strings.
"""
import ast
import csv
import datetime
import json
import sys
from decimal import Decimal


def parse(text: str):
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    try:
        return ast.literal_eval(text)
    except Exception:
        pass
    safe_globals = {
        "__builtins__": {},
        "datetime": datetime,
        "Decimal": Decimal,
        "True": True,
        "False": False,
        "None": None,
    }
    return eval(text, safe_globals, {})


def fmt(v):
    if v is None:
        return ""
    if isinstance(v, dict) and set(v.keys()) == {"value"}:
        return fmt(v["value"])
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return repr(v) if v and all(isinstance(x, str) for x in v) else json.dumps(v, default=str)
    return v


def main(argv):
    in_path, out_path, cols_csv = argv[1], argv[2], argv[3]
    cols = [c.strip() for c in cols_csv.split(",") if c.strip()]
    with open(in_path, "r", encoding="utf-8") as f:
        data = parse(f.read())
    if not isinstance(data, list):
        raise SystemExit(f"Expected list at top level of {in_path}, got {type(data).__name__}")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for row in data:
            w.writerow([fmt(row.get(c)) for c in cols])
    print(f"WROTE {out_path}: {len(data)} rows")


if __name__ == "__main__":
    main(sys.argv)
