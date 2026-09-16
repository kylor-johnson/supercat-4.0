#!/usr/bin/env python3
"""Convert a Python-literal list-of-dicts file (as returned by MCP) into CSV.

Usage: python3 to_csv.py <input_file> <output_csv> [header1,header2,...]

If a header list is provided, columns are written in that order (and missing
keys are written as empty). Otherwise, columns come from the first row.
"""
import csv
import sys
import datetime
import decimal
from pathlib import Path


def stringify(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat(sep=" ") if isinstance(v, datetime.datetime) else v.isoformat()
    if isinstance(v, decimal.Decimal):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(stringify_list_item(x) for x in v) + "]"
    return v


def stringify_list_item(v):
    if isinstance(v, str):
        return "'" + v + "'"
    return str(v)


def main():
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2])
    columns = sys.argv[3].split(",") if len(sys.argv) >= 4 else None

    raw = inp.read_text(encoding="utf-8").strip()
    try:
        import json
        data = json.loads(raw)
    except (ValueError, json.JSONDecodeError):
        safe_globals = {
            "__builtins__": {},
            "datetime": datetime,
            "Decimal": decimal.Decimal,
            "True": True,
            "False": False,
            "None": None,
        }
        data = eval(raw, safe_globals, {})

    if not isinstance(data, list):
        raise SystemExit(f"Expected list, got {type(data).__name__}")

    if columns is None:
        if not data:
            raise SystemExit("Empty result and no columns specified")
        columns = list(data[0].keys())

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(columns)
        for row in data:
            w.writerow([stringify(row.get(c)) for c in columns])

    print(f"Wrote {len(data)} rows to {out}")


if __name__ == "__main__":
    main()
