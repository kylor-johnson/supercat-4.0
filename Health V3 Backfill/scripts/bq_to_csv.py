#!/usr/bin/env python3
"""Convert BigQuery JSON result (with 'data' array) to UTF-8 CSV.

Usage: python3 bq_to_csv.py <input_json> <output_csv> col1,col2,...
"""
import csv
import json
import sys


def stringify(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "|".join(stringify(x) for x in v)
    return str(v)


def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    cols = sys.argv[3].split(",")

    with open(in_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    rows = payload.get("data", [])

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for row in rows:
            w.writerow([stringify(row.get(c)) for c in cols])

    print(f"wrote {out_path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
