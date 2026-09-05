#!/usr/bin/env python3
"""
Phase 1.1: surface inventory + navigation graph + reachability.

Screens are identified from three independent sources and unioned:
  (a) Objective-C  @interface X : *ViewController        (declared classes)
  (b) Swift        class X: *ViewController              (declared classes)
  (c) storyboard scenes / .xib documents with a customClass binding

Navigation edges come from two sources:
  (1) storyboard <segue destination=...> and navigation/split relationships,
      resolved from destination element id -> owning scene controller class
  (2) programmatic navigation: within a single method body that contains a
      navigation verb (push/present/show/setViewControllers/instantiate...),
      every OTHER known screen class named in that body becomes an out-edge.
      This is a deliberately mechanical rule; it over-connects rather than
      under-connects, so UNREACHABLE_CANDIDATE is a conservative claim.

Emits scripts/surface.json
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_loc_split as P  # reuse lexer / method ranges / unit map

ROOT = P.ROOT
HERE = os.path.dirname(os.path.abspath(__file__))
CLASSES = os.path.join(ROOT, "Classes")
FILE_TO_UNIT = P.FILE_TO_UNIT

VC_SUFFIX = re.compile(r'(ViewController|TableViewController|CollectionViewController)$')

# ------------------------------------------------- (a)(b) declared VC classes
declared = {}   # class -> {"files": set, "kind": objc|swift, "super": str}
OBJC_IFACE = re.compile(r'^@interface\s+(\w+)\s*:\s*(\w+)', re.M)
SWIFT_CLASS = re.compile(r'^\s*(?:@objc\w*\s+|public\s+|final\s+|internal\s+|open\s+)*class\s+(\w+)\s*:\s*([^\{\n]+)', re.M)

src_files = {}
for dp, _, fns in os.walk(CLASSES):
    for fn in sorted(fns):
        ext = os.path.splitext(fn)[1]
        if ext not in (".m", ".mm", ".h", ".swift"):
            continue
        path = os.path.join(dp, fn)
        raw = open(path, encoding="utf-8", errors="ignore").read()
        src_files[fn] = (path, raw, P.strip_noncode(raw, ext == ".swift"))

for fn, (path, raw, st) in src_files.items():
    swift = fn.endswith(".swift")
    if swift:
        for m in SWIFT_CLASS.finditer(st):
            cls, sup = m.group(1), m.group(2).strip()
            if VC_SUFFIX.search(sup.split(",")[0].strip()) or VC_SUFFIX.search(cls):
                d = declared.setdefault(cls, {"files": set(), "kind": "swift", "super": sup.split(",")[0].strip()})
                d["files"].add(fn)
    else:
        for m in OBJC_IFACE.finditer(st):
            cls, sup = m.group(1), m.group(2)
            if VC_SUFFIX.search(sup) or VC_SUFFIX.search(cls):
                d = declared.setdefault(cls, {"files": set(), "kind": "objc", "super": sup})
                d["files"].add(fn)

# subclasses of already-known screen classes (2 passes for depth)
for _ in range(3):
    for fn, (path, raw, st) in src_files.items():
        swift = fn.endswith(".swift")
        pat = SWIFT_CLASS if swift else OBJC_IFACE
        for m in pat.finditer(st):
            cls, sup = m.group(1), m.group(2).split(",")[0].strip()
            if sup in declared and cls not in declared:
                declared[cls] = {"files": {fn}, "kind": "swift" if swift else "objc", "super": sup}

# ------------------------------------------------- (c) IB documents
ib_scenes = defaultdict(list)     # class -> [ib file]
ib_files = {}
storyboard_edges = []             # (src_class, dst_class, kind, ibfile)
sb_initial = []                   # (ibfile, class) initial view controller

for dp, _, fns in os.walk(CLASSES):
    for fn in sorted(fns):
        if not fn.endswith((".storyboard", ".xib")):
            continue
        path = os.path.join(dp, fn)
        ib_files[fn] = path
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue
        root = tree.getroot()
        # map every element id in a controller's subtree -> controller class
        owner = {}
        controllers = []
        for scene in root.iter("scene"):
            objs = scene.find("objects")
            if objs is None:
                continue
            for child in objs:
                if child.get("sceneMemberID") == "viewController" or \
                   child.tag.endswith("ViewController") or child.tag in (
                       "viewController", "tableViewController", "collectionViewController",
                       "navigationController", "splitViewController", "tabBarController",
                       "pageViewController"):
                    cls = child.get("customClass") or ("UIKit:" + child.tag)
                    controllers.append((child, cls))
                    for el in child.iter():
                        if el.get("id"):
                            owner[el.get("id")] = cls
                    if child.get("customClass"):
                        ib_scenes[cls].append(fn)
        # xib documents have no <scene>; look for top-level objects
        if not controllers:
            for objs in root.iter("objects"):
                for child in objs:
                    cc = child.get("customClass")
                    if cc and VC_SUFFIX.search(cc):
                        ib_scenes[cc].append(fn)
                        for el in child.iter():
                            if el.get("id"):
                                owner[el.get("id")] = cc
        # segues
        for ctrl, cls in controllers:
            for sg in ctrl.iter("segue"):
                dst = sg.get("destination")
                if dst and dst in owner:
                    storyboard_edges.append((cls, owner[dst], sg.get("kind") or "segue", fn))
            for rel in ctrl.iter("relationship"):
                dst = rel.get("destination")
                if dst and dst in owner:
                    storyboard_edges.append((cls, owner[dst], "relationship", fn))
            # navigation/split/tab root controllers
            for key in ("rootViewController",):
                rv = ctrl.get(key)
                if rv and rv in owner:
                    storyboard_edges.append((cls, owner[rv], "root", fn))
        init = root.get("initialViewController")
        if init and init in owner:
            sb_initial.append((fn, owner[init]))

screens = set(declared) | {c for c in ib_scenes if not c.startswith("UIKit:")}

# ------------------------------------------------- programmatic edges
NAV_VERBS = ("pushviewcontroller", "presentviewcontroller", "presentmodalviewcontroller",
             "present(", "showdetailviewcontroller", "setviewcontrollers",
             "instantiateviewcontroller", "performsegue", "addchildviewcontroller",
             "show(", "popovercontroller", "presentpopover")
prog_edges = []
name_re = {c: re.compile(r'\b%s\b' % re.escape(c)) for c in screens}

for fn, (path, raw, st) in src_files.items():
    swift = fn.endswith(".swift")
    # which screen class does this file implement?
    owners = [c for c, d in declared.items() if fn in d["files"]]
    base = os.path.splitext(fn)[0]
    if not owners and base in screens:
        owners = [base]
    for s, e in P.method_ranges(st, swift):
        body = st[s:e]
        low = body.lower()
        if not any(v in low for v in NAV_VERBS):
            continue
        for c in screens:
            if c in owners:
                continue
            if name_re[c].search(body):
                for o in (owners or ["_unowned:" + fn]):
                    prog_edges.append((o, c, "programmatic", fn))

# also: storyboard identifier strings -> screens instantiated by name
edges = storyboard_edges + prog_edges
out_edges = defaultdict(set)
in_edges = defaultdict(set)
for a, b, kind, f in edges:
    if a.startswith("UIKit:") or b.startswith("UIKit:"):
        # keep UIKit container edges only for reachability of the destination
        if not b.startswith("UIKit:"):
            in_edges[b].add(a)
        continue
    out_edges[a].add(b)
    in_edges[b].add(a)

# entry points: storyboard initial VCs + Main.storyboard root
entry = {c for _, c in sb_initial if not c.startswith("UIKit:")}

# ------------------------------------------------- LOC per screen
loc_by_file = {r["file"].split("/")[-1]: r for r in P.file_rows} if hasattr(P, "file_rows") else {}
locsplit = json.load(open(os.path.join(HERE, "loc_split.json")))
loc_by_file = {}
for r in locsplit["files"]:
    loc_by_file[os.path.basename(r["file"])] = r

rows = []
for c in sorted(screens):
    files = set(declared.get(c, {}).get("files", set()))
    for cand in (c + ".m", c + ".h", c + ".swift"):
        if cand in src_files:
            files.add(cand)
    ibs = sorted(set(ib_scenes.get(c, [])))
    loc = sum(loc_by_file.get(f, {}).get("code_lines", 0) for f in files)
    split = defaultdict(int)
    for f in files:
        for k, v in loc_by_file.get(f, {}).get("split", {}).items():
            split[k] += v
    unit = next((FILE_TO_UNIT.get(f) for f in sorted(files) if FILE_TO_UNIT.get(f)), None)
    inb = sorted(in_edges.get(c, set()))
    reach = "ENTRY_POINT" if c in entry else ("UNREACHABLE_CANDIDATE" if not inb else "REACHABLE")
    rows.append({
        "screen_id": c,
        "display_name": c,
        "unit": unit,
        "files": sorted(files),
        "ib_documents": ibs,
        "loc_total": loc,
        "loc_ui": split.get("UI", 0),
        "loc_logic": split.get("LOGIC", 0),
        "loc_glue": split.get("GLUE", 0),
        "loc_unclassified": split.get("UNCLASSIFIED", 0),
        "declared_in": declared.get(c, {}).get("kind", "ib_only"),
        "superclass": declared.get(c, {}).get("super"),
        "reachable_from": inb,
        "navigation_out_edges": sorted(out_edges.get(c, set())),
        "in_degree": len(inb),
        "out_degree": len(out_edges.get(c, set())),
        "reachability": reach,
        "source": "pbxproj unit map + declared class scan + IB XML parse + programmatic nav scan",
    })

rows.sort(key=lambda r: (-r["loc_total"], r["screen_id"]))
summary = {
    "screens_total": len(rows),
    "declared_objc": sum(1 for r in rows if r["declared_in"] == "objc"),
    "declared_swift": sum(1 for r in rows if r["declared_in"] == "swift"),
    "ib_only": sum(1 for r in rows if r["declared_in"] == "ib_only"),
    "ib_documents_total": len(ib_files),
    "storyboard_edges": len(storyboard_edges),
    "programmatic_edges": len(prog_edges),
    "entry_points": sorted(entry),
    "reachable": sum(1 for r in rows if r["reachability"] == "REACHABLE"),
    "unreachable_candidates": sum(1 for r in rows if r["reachability"] == "UNREACHABLE_CANDIDATE"),
    "screens_with_ib": sum(1 for r in rows if r["ib_documents"]),
    "screens_without_ib": sum(1 for r in rows if not r["ib_documents"]),
}
json.dump({"summary": summary, "screens": rows,
           "storyboard_initial": sb_initial}, open(os.path.join(HERE, "surface.json"), "w"), indent=1)

print(json.dumps(summary, indent=1))
print()
print(f"{'screen':<46}{'unit':<26}{'loc':>6}{'in':>4}{'out':>4}  reach")
for r in rows[:45]:
    print(f"{r['screen_id']:<46}{str(r['unit'])[:25]:<26}{r['loc_total']:>6}"
          f"{r['in_degree']:>4}{r['out_degree']:>4}  {r['reachability']}")
print()
print("=== UNREACHABLE_CANDIDATEs ===")
for r in rows:
    if r["reachability"] == "UNREACHABLE_CANDIDATE":
        print(f"  {r['screen_id']:<46}{str(r['unit'])[:25]:<26}{r['loc_total']:>6}  ib={r['ib_documents']}")
