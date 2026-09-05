#!/usr/bin/env python3
"""
Diagnostic for the 1.2 split: (a) what is UNCLASSIFIED, (b) how much LOC matches
BOTH logic and UI terms (the entanglement number), (c) which files are _UNMAPPED.
Reuses p1_loc_split internals.
"""
import json
import os
import re
import sys
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_loc_split as P  # noqa: E402  (module runs its analysis on import)

ROOT = P.ROOT
CLASSES = os.path.join(ROOT, "Classes")

cooc = defaultdict(int)          # (logic,ui,glue) -> loc
uncl_names = Counter()
uncl_examples = []
unmapped = Counter()

OBJC_NAME = re.compile(r'^[-+]\s*\([^)]*\)\s*([A-Za-z_][\w:]*)')
SWIFT_NAME = re.compile(r'(?:func\s+(\w+)|(init)\b|(deinit)\b|var\s+(\w+)\s*:)')

for dirpath, _, filenames in os.walk(CLASSES):
    for fn in sorted(filenames):
        ext = os.path.splitext(fn)[1]
        if ext not in (".m", ".mm", ".h", ".swift"):
            continue
        if fn not in P.FILE_TO_UNIT:
            unmapped[fn] = 1
        path = os.path.join(dirpath, fn)
        swift = ext == ".swift"
        raw = open(path, encoding="utf-8", errors="ignore").read()
        st = P.strip_noncode(raw, swift)
        for s, e in P.method_ranges(st, swift):
            body = st[s:e].lower()
            cl = P.codelines(st[s:e])
            l1 = P.has_any(body, P.L1_LOGIC)
            l2 = P.has_any(body, P.L2_ENTITY) and P.has_any(body, P.L2_COMPUTE)
            logic, ui, glue = (l1 or l2), P.has_any(body, P.UI_TERMS), P.has_any(body, P.GLUE_TERMS)
            cooc[(logic, ui, glue)] += cl
            if not (logic or ui or glue):
                head = st[s:e].split("\n")[0].strip()[:110]
                m = (OBJC_NAME.search(head) if not swift else SWIFT_NAME.search(head))
                nm = next((g for g in (m.groups() if m else []) if g), "?") if m else "?"
                uncl_names[nm] += cl
                if len(uncl_examples) < 40 and cl >= 5:
                    uncl_examples.append((cl, fn, head))

tot = sum(cooc.values())
print("=== co-occurrence of term families, by code lines inside methods ===")
print(f"{'logic':>6}{'ui':>6}{'glue':>6}{'loc':>9}{'pct':>7}")
for k in sorted(cooc, key=lambda k: -cooc[k]):
    l, u, g = k
    print(f"{str(l):>6}{str(u):>6}{str(g):>6}{cooc[k]:>9}{100.0*cooc[k]/tot:>6.1f}%")
print(f"\ntotal in-method loc: {tot}")

ent = sum(v for k, v in cooc.items() if k[0] and k[1])
print(f"\nENTANGLED (matches BOTH logic and ui terms): {ent} loc "
      f"({100.0*ent/tot:.1f}% of in-method loc)")
print(f"logic-only: {sum(v for k,v in cooc.items() if k[0] and not k[1])}")
print(f"ui-only:    {sum(v for k,v in cooc.items() if k[1] and not k[0])}")

print(f"\n=== UNCLASSIFIED: top method names by loc ===")
for nm, cl in uncl_names.most_common(30):
    print(f"{cl:>7}  {nm}")

print(f"\n=== UNCLASSIFIED examples (loc >= 5) ===")
for cl, fn, head in sorted(uncl_examples, reverse=True)[:25]:
    print(f"{cl:>5}  {fn:<38} {head}")

print(f"\n=== _UNMAPPED files (in Classes/ but not in pbxproj map) ===")
print(len(unmapped), "files:", list(unmapped)[:30])

json.dump({"cooccurrence": {str(k): v for k, v in cooc.items()},
           "entangled_loc": ent,
           "unclassified_top": uncl_names.most_common(60),
           "unmapped_files": list(unmapped)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "loc_diag.json"), "w"),
          indent=1)
