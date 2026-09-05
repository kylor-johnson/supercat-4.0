#!/usr/bin/env python3
"""
Phase 1 step A: derive unit boundaries from project.pbxproj PBXGroup tree.

Approved methodology (Phase 0 §1.3): Xcode PBXGroup entries are the
unit-boundary source, because Classes/ is flat on disk.

Parsing is section-scoped and line-anchored. An earlier regex using re.S with a
non-greedy comment group silently matched IDs from unrelated entries thousands
of lines away, producing wrong group IDs and dropping whole units. Do not
reintroduce a dot-matches-newline comment group here.

Emits scripts/units.json
"""
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ecat-audit/ios-master/eCatalog"
PBX = os.path.join(ROOT, "eCatalog.xcodeproj/project.pbxproj")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")

src = open(PBX, encoding="utf-8", errors="ignore").read()


def section(name):
    """Return the text between /* Begin <name> section */ and /* End ... */."""
    m = re.search(r'/\* Begin %s section \*/(.*?)/\* End %s section \*/' % (name, name),
                  src, re.S)
    return m.group(1) if m else ""


ENTRY_HEAD = re.compile(r'^\t\t([0-9A-F]{24})(?: /\* ([^\n]*?) \*/)? = \{')


def blocks(text):
    """Yield (id, comment, body) for each top-level object entry in a section."""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = ENTRY_HEAD.match(lines[i])
        if not m:
            i += 1
            continue
        oid, comment = m.group(1), (m.group(2) or "")
        # single-line entry
        if lines[i].rstrip().endswith("};"):
            yield oid, comment, lines[i]
            i += 1
            continue
        body, j = [lines[i]], i + 1
        while j < len(lines) and lines[j] != "\t\t};":
            body.append(lines[j])
            j += 1
        yield oid, comment, "\n".join(body)
        i = j + 1


def name_of(body, comment):
    nm = re.search(r'\bname = "?([^";]+)"?;', body)
    if nm:
        return nm.group(1)
    pm = re.search(r'\bpath = "?([^";]+)"?;', body)
    if pm:
        return pm.group(1)
    return comment


# --- file references: id -> filename -------------------------------------
fileref = {}
for oid, comment, body in blocks(section("PBXFileReference")):
    fileref[oid] = name_of(body, comment)

# --- variant groups (localized .storyboard/.xib) treated as files --------
for oid, comment, body in blocks(section("PBXVariantGroup")):
    fileref.setdefault(oid, name_of(body, comment))

# --- groups: id -> {name, children} --------------------------------------
groups = {}
for oid, comment, body in blocks(section("PBXGroup")):
    ch = re.search(r'children = \((.*?)\);', body, re.S)
    children = re.findall(r'([0-9A-F]{24})', ch.group(1)) if ch else []
    groups[oid] = {"name": name_of(body, comment), "children": children}

# Traverse from the project's mainGroup so every referenced file is placed. An
# earlier version walked only the Classes group plus a hardcoded list, which
# silently dropped files whose PBXGroup sits elsewhere in the tree (e.g.
# NetworkStatusMonitor.{h,m}) and made them look like dead code. Traverse
# everything; only files absent from the project are dead-code candidates.
mainm = re.search(r'mainGroup = ([0-9A-F]{24})', src)
root_gid = mainm.group(1) if mainm else None
if not root_gid or root_gid not in groups:
    root_gid = next((g for g, d in groups.items() if d["name"] == "Classes"), None)
if not root_gid:
    sys.exit("FATAL: no root PBXGroup found")

units, file_to_unit, unplaced = {}, {}, []


def unit_for(path):
    """Unit = the group directly under Classes; else the top-level group name."""
    if "Classes" in path:
        i = path.index("Classes")
        if i + 1 < len(path):
            return path[i + 1]
        return "_Classes_root"
    return "_" + (path[1] if len(path) > 1 else "root")


def walk(gid, path, seen):
    if gid in seen:
        return
    seen.add(gid)
    for cid in groups.get(gid, {}).get("children", []):
        if cid in groups:
            walk(cid, path + [groups[cid]["name"]], seen)
        elif cid in fileref:
            fname = fileref[cid]
            unit = unit_for(path)
            units.setdefault(unit, {"group_path": path[:3], "files": []})
            units[unit]["files"].append(fname)
            file_to_unit.setdefault(fname, unit)
        else:
            unplaced.append(cid)


walk(root_gid, ["<root>"], set())

# Files present on disk under Classes/ but absent from the project entirely.
# These are not compiled -> genuine dead-code candidates for 1.8.
disk_files, on_disk_unreferenced = set(), []
classes_dir = os.path.join(ROOT, "Classes")
for dp, _, fns in os.walk(classes_dir):
    for fn in fns:
        if os.path.splitext(fn)[1] in (".m", ".mm", ".h", ".swift"):
            disk_files.add(fn)
            if fn not in file_to_unit:
                on_disk_unreferenced.append(os.path.relpath(os.path.join(dp, fn), ROOT))

json.dump({
    "pbxproj": PBX,
    "group_count_total": len(groups),
    "fileref_count": len(fileref),
    "unit_count": len(units),
    "file_count_mapped": len(file_to_unit),
    "unresolved_child_refs": len(unplaced),
    "source_files_on_disk_in_Classes": len(disk_files),
    "on_disk_not_in_project": sorted(on_disk_unreferenced),
    "units": units,
    "file_to_unit": file_to_unit,
}, open(OUT, "w"), indent=1)

print(f"groups parsed:        {len(groups)}")
print(f"filerefs parsed:      {len(fileref)}")
print(f"units derived:        {len(units)}")
print(f"files mapped:         {len(file_to_unit)}")
print(f"unresolved child ids: {len(unplaced)}")
print(f"Classes/ src on disk: {len(disk_files)}")
print(f"on disk, NOT in project (dead-code candidates): {len(on_disk_unreferenced)}")
for f in sorted(on_disk_unreferenced):
    print(f"   {f}")
print()
print(f"{'files':>6}  unit")
for u, d in sorted(units.items(), key=lambda kv: -len(kv[1]["files"])):
    print(f"{len(d['files']):>6}  {u}")
