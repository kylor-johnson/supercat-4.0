#!/usr/bin/env python3
"""Convert MCP large-output Python repr text files to UTF-8 CSV.

Usage: python3 mcp_to_csv.py <input_txt> <output_csv> [col1,col2,...]
If columns are omitted, uses keys of the first row.
"""
import ast
import csv
import sys
import datetime as _dt
from datetime import datetime, date, timezone, timedelta
from decimal import Decimal


def safe_eval(text):
    """ast.literal_eval, but also accept datetime.datetime(...) / datetime.date(...) calls.

    The Postgres MCP returns python repr that includes datetime.datetime(...). We walk
    the AST and convert those Call nodes to constant datetime objects, then literal_eval.
    """
    tree = ast.parse(text, mode="eval")
    allowed_callables = {
        ("datetime", "datetime"): _dt.datetime,
        ("datetime", "date"): _dt.date,
        ("datetime", "time"): _dt.time,
        ("datetime", "timedelta"): _dt.timedelta,
        ("datetime", "timezone"): _dt.timezone,
    }

    def evalnode(node):
        if isinstance(node, ast.Expression):
            return evalnode(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            v = evalnode(node.operand)
            return -v if isinstance(node.op, ast.USub) else +v
        if isinstance(node, ast.List):
            return [evalnode(e) for e in node.elts]
        if isinstance(node, ast.Tuple):
            return tuple(evalnode(e) for e in node.elts)
        if isinstance(node, ast.Dict):
            return {evalnode(k): evalnode(v) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.Set):
            return {evalnode(e) for e in node.elts}
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                key = (func.value.id, func.attr)
                if key in allowed_callables:
                    args = [evalnode(a) for a in node.args]
                    kwargs = {kw.arg: evalnode(kw.value) for kw in node.keywords}
                    return allowed_callables[key](*args, **kwargs)
            if isinstance(func, ast.Name) and func.id in {"datetime", "date", "time", "timedelta", "Decimal"}:
                args = [evalnode(a) for a in node.args]
                kwargs = {kw.arg: evalnode(kw.value) for kw in node.keywords}
                if func.id == "Decimal":
                    return Decimal(*args)
                return getattr(_dt, func.id)(*args, **kwargs)
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Attribute):
                if (
                    isinstance(func.value.value, ast.Name)
                    and func.value.value.id == "datetime"
                    and func.value.attr == "timezone"
                    and func.attr == "utc"
                ):
                    return timezone.utc
            raise ValueError(f"Unsupported call: {ast.dump(func)}")
        if isinstance(node, ast.Attribute):
            if (
                isinstance(node.value, ast.Name)
                and node.value.id == "datetime"
                and node.attr == "timezone"
            ):
                return _dt.timezone
            if (
                isinstance(node.value, ast.Attribute)
                and isinstance(node.value.value, ast.Name)
                and node.value.value.id == "datetime"
                and node.value.attr == "timezone"
                and node.attr == "utc"
            ):
                return timezone.utc
            raise ValueError(f"Unsupported attribute: {ast.dump(node)}")
        if isinstance(node, ast.Name):
            mapping = {"None": None, "True": True, "False": False}
            if node.id in mapping:
                return mapping[node.id]
            raise ValueError(f"Unsupported name: {node.id}")
        raise ValueError(f"Unsupported node: {ast.dump(node)}")

    return evalnode(tree)


def stringify(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, Decimal):
        return format(v, "f")
    if isinstance(v, (list, tuple)):
        return "|".join(stringify(x) for x in v)
    return str(v)


def main():
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    cols = sys.argv[3].split(",") if len(sys.argv) > 3 else None

    with open(in_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    data = safe_eval(text)
    if not isinstance(data, list):
        raise SystemExit(f"Expected list, got {type(data).__name__}")

    if not data:
        if not cols:
            raise SystemExit("Empty data and no columns supplied")
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
        print(f"wrote {out_path} (0 rows)")
        return

    if cols is None:
        cols = list(data[0].keys())

    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for row in data:
            w.writerow([stringify(row.get(c)) for c in cols])

    print(f"wrote {out_path} ({len(data)} rows)")


if __name__ == "__main__":
    main()
