#!/usr/bin/env python3
"""
Phase 1.2: three-way UI / LOGIC / GLUE LOC split, per method, rolled up per unit.

Approved rule (Phase 0 §5.2):
  - classify per function/method, not per file
  - precedence LOGIC > GLUE > UI
  - anything matching none of the three -> UNCLASSIFIED (its own bucket)
  - storyboard/xib XML is NEVER folded into ui_loc (counted separately as IB_XML)

Documented refinement to the approved rule (reported in 01_CODE_CENSUS.md):
  LOGIC is evaluated in two tiers.
    L1 = domain-computation identifiers -> LOGIC unconditionally.
    L2 = bare Core Data entity nouns -> LOGIC only if the method ALSO contains an
         arithmetic/comparison/aggregation/validation token.
  Reason: bare entity nouns ("Customer", "Order") appear constantly in pure
  presentation code (CustomerCell, OrderTableView). Tier-1-only matching would
  have inflated LOGIC by absorbing cell-rendering methods, and under
  LOGIC-precedence that error is unrecoverable. Both tiers are published below.

Also emits a precedence sensitivity check (UI-first vs LOGIC-first) so the
leverage of the precedence choice is visible rather than hidden.

Emits scripts/loc_split.json
"""
import json
import os
import re
import sys
from collections import defaultdict

ROOT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ecat-audit/ios-master/eCatalog"
HERE = os.path.dirname(os.path.abspath(__file__))
UNITS = json.load(open(os.path.join(HERE, "units.json")))
FILE_TO_UNIT = UNITS["file_to_unit"]

# ----------------------------------------------------------------- keyword sets
L1_LOGIC = [
    # pricing / money
    "calculateprice", "pricefor", "unitprice", "extendedprice", "listprice",
    "netprice", "promoprice", "promotionprice", "contractprice", "matrixprice",
    "riserprice", "pricelevel", "pricecode", "discount", "surcharge", "markup",
    "margin", "taxamount", "computetotal", "ordertotal", "linetotal", "subtotal",
    "grandtotal", "extendedamount", "applydiscount", "pricebreak", "quantitybreak",
    # order construction
    "orderitem", "additemtoorder", "addtoorder", "removeorderitem", "lineitem",
    "ordersubmit", "submitorder", "orderstatus", "orderdraft", "cartitem",
    # cpq / options / kits
    "optiongroup", "optionmapping", "optionset", "optionform", "configureoption",
    "configureditem", "kititem", "explodekit", "kitcomponent", "componentqty",
    "matrixoption", "optionprice", "optioncode", "validateoption", "requiredoption",
    # inventory / availability
    "qtyavailable", "qtyonhand", "qtyreserved", "backorder", "availability",
    "nextreceipt", "inventoryfor",
    # sync / conflict
    "conflict", "lastwritewins", "resolveconflict", "mergechanges", "syncstate",
    "dirtyflag", "pendingchanges", "datasync", "deltasync", "syncversion",
    # catalog logic
    "filterpredicate", "searchrank", "relevancescore", "sortdescriptor",
    "buildpredicate", "nspredicate", "applyfilter", "matchesfilter",
    # validation
    "validate", "isvalid", "validation",
    # territory / entitlement
    "territorycode", "billtocode", "shiptocode", "defaultpricecode",
]

L2_ENTITY = [
    # the 25 Core Data entity names + close domain nouns (weak signal)
    "address", "customer", "inventory", "list", "listitem", "localuser",
    "maybelist", "option", "optiongroupoption", "order", "product",
    "pricing", "price", "kit", "quote", "commitment", "placement", "stack",
    "favorite", "territory", "taxonomy", "collection", "category", "tradename",
    "surchargetype", "rma", "invoice", "shipping", "showroom", "smartstack",
]

L2_COMPUTE = [
    "+", "-", "*", "/", "<", ">", "==", "!=", ">=", "<=",
    "sum", "count", "total", "round", "floor", "ceil", "decimal", "nsdecimal",
    "compare", "sortusing", "predicate", "filter", "reduce", "aggregate",
    "if ", "while ", "for ", "switch ",
]

UI_TERMS = [
    "nslayoutconstraint", "layoutsubviews", "setneedslayout", "layoutifneeded",
    "uicolor", "uifont", "uiimage", "drawrect", "animatewithduration", "uiview",
    "addsubview", "removefromsuperview", "backgroundcolor", "tintcolor",
    "cornerradius", "cgrect", "cgpoint", "cgsize", "cgaffine", "prepareforsegue",
    "performsegue", "pushviewcontroller", "presentviewcontroller",
    "dismissviewcontroller", "showdetailviewcontroller", "tableview",
    "collectionview", "cellforrow", "numberofrows", "numberofsections",
    "didselectrow", "reloaddata", "uitableviewcell", "uicollectionviewcell",
    "uibutton", "uilabel", "uitextfield", "uitextview", "uialertcontroller",
    "uibarbuttonitem", "navigationitem", "navigationcontroller", "viewdidload",
    "viewwillappear", "viewdidappear", "viewwilldisappear", "uistoryboard",
    "iboutlet", "ibaction", "contentsize", "uiscrollview", "scrollview",
    "becomefirstresponder", "resignfirstresponder", "gesturerecognizer",
    "uistackview", "safearea", "traitcollection", "uipopover", "sizetofit",
    "nsattributedstring", "uiactivityindicator", "uirefreshcontrol", "uiswitch",
    "uisegmentedcontrol", "uipickerview", "uidatepicker", "uinib", "dequeuereusable",
    "setneedsdisplay", "uiedgeinsets", "uibezierpath", "calayer", "uiwindow",
    "uitabbar", "uisearchbar", "uiimageview", "uiprogressview", "uislider",
    "titleforheader", "heightforrow", "willdisplaycell", "indexpath",
    "uisplitviewcontroller", "uinavigationbar", "appearance", "uitoolbar",
    # added after the diagnostic pass (see 01_CODE_CENSUS.md "rule additions"):
    # unambiguous UIKit lifecycle / appearance symbols that were simply missing.
    "awakefromnib", "preferredstatusbarstyle", "updateui", "theme", "fontsize",
    "textcolor", "setimage", "placeholder", "addtarget", "sendaction",
    "uiactionsheet", "uimenu", "badge", "segmentindex", "requiredheight",
    "preferredcontentsize", "intrinsiccontentsize", "setframe", "statusbar",
]

GLUE_TERMS = [
    "nsmanagedobjectcontext", "nspersistentstore", "nsmanagedobjectmodel",
    "nsfetchrequest", "persistentcontainer", "managedobjectcontext", "fmdatabase",
    "fmdbqueue", "sqlite3", "appdelegate", "applicationdidbecome",
    "applicationwillterminate", "applicationdidenterbackground", "didfinishlaunching",
    "dispatch_async", "dispatch_sync", "dispatch_after", "dispatch_once",
    "dispatchqueue", "nsoperationqueue", "nsthread", "performselector",
    "nslock", "semaphore", "secitemadd", "secitemcopy", "keychain",
    "nsfilemanager", "nssearchpathfordirectories", "documentsdirectory",
    "nsuserdefaults", "userdefaults", "nsbundle", "afhttpsessionmanager",
    "nsurlsession", "nsurlrequest", "nsurlconnection", "nsjsonserialization",
    "sbjson", "ssziparchive", "ziparchive", "nsnotificationcenter",
    "addobserver", "removeobserver", "nslog", "os_log", "crashlytics",
    "firebase", "mixpanel", "nscoder", "encodewithcoder", "initwithcoder",
    "reachability", "nstimer", "nsdateformatter", "nsnumberformatter",
    "objc_", "swizzl", "dlopen", "sharedinstance", "singleton",
    # added after the diagnostic pass: KVO plumbing, Core Data/SQLite schema
    # plumbing, encoding helpers, and WebView bridging were all missing.
    "observevalueforkeypath", "observedkeypaths", "keypath", "willchangevalue",
    "didchangevalue", "base64", "entityname", "tablename", "attributenames",
    "availablemigrations", "migration", "wkwebview", "webview",
]

# Structural fallback: object-construction / teardown members that match no
# term family are platform plumbing, not domain behavior.
GLUE_MEMBER_NAMES = ("init", "initwith", "deinit", "dealloc", "copywithzone",
                     "encodewithcoder", "description", "hash", "isequal")

# ----------------------------------------------------------------- lexing
def strip_noncode(text, swift):
    """Blank out comments and string literals, preserving line structure."""
    out = []
    i, n = 0, len(text)
    in_line, in_block, in_str, in_mstr = False, False, False, False
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if in_line:
            if c == "\n":
                in_line = False
                out.append(c)
            else:
                out.append(" ")
            i += 1
        elif in_block:
            if c == "*" and nxt == "/":
                in_block = False
                out.append("  ")
                i += 2
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
        elif in_mstr:
            if text[i:i + 3] == '"""':
                in_mstr = False
                out.append("   ")
                i += 3
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
        elif in_str:
            if c == "\\":
                out.append("  ")
                i += 2
            elif c == '"':
                in_str = False
                out.append(" ")
                i += 1
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
        else:
            if c == "/" and nxt == "/":
                in_line = True
                out.append("  ")
                i += 2
            elif c == "/" and nxt == "*":
                in_block = True
                out.append("  ")
                i += 2
            elif swift and text[i:i + 3] == '"""':
                in_mstr = True
                out.append("   ")
                i += 3
            elif c == '"':
                in_str = True
                out.append(" ")
                i += 1
            else:
                out.append(c)
                i += 1
    return "".join(out)


OBJC_METHOD = re.compile(r'^[-+]\s*\([^)]*\)[^;{]*\{', re.M)
SWIFT_FUNC = re.compile(
    r'^[ \t]*(?:@\w+\s+)*(?:public |private |internal |fileprivate |open |static |class |final |override |convenience |required |mutating |@objc |lazy |weak |nonisolated )*'
    r'(?:func\s+\w+|init\b|deinit\b|subscript\b|var\s+\w+\s*:\s*[^={\n]+\{)', re.M)


def method_ranges(stripped, swift):
    """Return list of (start_off, end_off) for each method/function body."""
    pat = SWIFT_FUNC if swift else OBJC_METHOD
    ranges = []
    for m in pat.finditer(stripped):
        b = stripped.find("{", m.start())
        if b == -1:
            continue
        depth, j, n = 0, b, len(stripped)
        while j < n:
            if stripped[j] == "{":
                depth += 1
            elif stripped[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j < n:
            ranges.append((m.start(), j + 1))
    # drop ranges nested inside an earlier range (closures picked up by SWIFT_FUNC)
    ranges.sort()
    merged = []
    for s, e in ranges:
        if merged and s < merged[-1][1]:
            continue
        merged.append((s, e))
    return merged


def has_any(body, terms):
    return any(t in body for t in terms)


def classify(body, head=""):
    """Return (label_logic_first, label_ui_first) for a method body (lowercased)."""
    l1 = has_any(body, L1_LOGIC)
    l2 = has_any(body, L2_ENTITY) and has_any(body, L2_COMPUTE)
    logic = l1 or l2
    ui = has_any(body, UI_TERMS)
    glue = has_any(body, GLUE_TERMS)
    if not (logic or ui or glue) and head:
        h = head.lower()
        if any(re.search(r'\b%s\b' % n, h) for n in GLUE_MEMBER_NAMES):
            glue = True
    # approved precedence
    if logic:
        a = "LOGIC"
    elif glue:
        a = "GLUE"
    elif ui:
        a = "UI"
    else:
        a = "UNCLASSIFIED"
    # sensitivity: UI-first
    if ui:
        b = "UI"
    elif logic:
        b = "LOGIC"
    elif glue:
        b = "GLUE"
    else:
        b = "UNCLASSIFIED"
    return a, b


def codelines(stripped_slice):
    return sum(1 for ln in stripped_slice.split("\n") if ln.strip())


# ----------------------------------------------------------------- main
CLASSES = os.path.join(ROOT, "Classes")
unit_loc = defaultdict(lambda: defaultdict(int))
unit_loc_uifirst = defaultdict(lambda: defaultdict(int))
unit_files = defaultdict(set)
unit_methods = defaultdict(int)
mixed_files = 0
residue_total = 0
file_rows = []
uncl_trivial = [0, 0]   # [loc, method_count] for UNCLASSIFIED methods <= 3 loc
uncl_subst = [0, 0]     # [loc, method_count] for UNCLASSIFIED methods > 3 loc

for dirpath, _, filenames in os.walk(CLASSES):
    for fn in sorted(filenames):
        ext = os.path.splitext(fn)[1]
        if ext not in (".m", ".mm", ".h", ".swift"):
            continue
        path = os.path.join(dirpath, fn)
        rel = os.path.relpath(path, ROOT)
        unit = FILE_TO_UNIT.get(fn, "_UNMAPPED")
        swift = ext == ".swift"
        raw = open(path, encoding="utf-8", errors="ignore").read()
        stripped = strip_noncode(raw, swift)
        total_cl = codelines(stripped)
        ranges = method_ranges(stripped, swift)

        seen = set()
        counts = defaultdict(int)
        counts_b = defaultdict(int)
        covered = 0
        for s, e in ranges:
            body = stripped[s:e].lower()
            head = stripped[s:e].split("\n")[0]
            a, b = classify(body, head)
            cl = codelines(stripped[s:e])
            counts[a] += cl
            counts_b[b] += cl
            covered += cl
            seen.add(a)
            unit_methods[unit] += 1
            if a == "UNCLASSIFIED":
                if cl <= 3:
                    uncl_trivial[0] += cl
                    uncl_trivial[1] += 1
                else:
                    uncl_subst[0] += cl
                    uncl_subst[1] += 1

        # residue = lines outside any method body (imports, ivars, @property,
        # @interface/@implementation, type decls). Assigned to the file's
        # dominant method class; if the file has no methods, UNCLASSIFIED.
        residue = max(0, total_cl - covered)
        residue_total += residue
        if residue:
            dom = max(counts.items(), key=lambda kv: kv[1])[0] if counts else "UNCLASSIFIED"
            dom_b = max(counts_b.items(), key=lambda kv: kv[1])[0] if counts_b else "UNCLASSIFIED"
            counts[dom] += residue
            counts_b[dom_b] += residue

        if len(seen) > 1:
            mixed_files += 1
        for k, v in counts.items():
            unit_loc[unit][k] += v
        for k, v in counts_b.items():
            unit_loc_uifirst[unit][k] += v
        unit_files[unit].add(fn)
        file_rows.append({
            "file": rel, "unit": unit, "ext": ext, "code_lines": total_cl,
            "methods": len(ranges), "residue": residue,
            "split": dict(counts),
        })

# ---- storyboards / xibs counted separately, never folded into ui_loc
ib = {"files": 0, "lines": 0}
for dirpath, _, filenames in os.walk(CLASSES):
    for fn in filenames:
        if os.path.splitext(fn)[1] in (".storyboard", ".xib"):
            ib["files"] += 1
            ib["lines"] += sum(1 for _ in open(os.path.join(dirpath, fn),
                                               encoding="utf-8", errors="ignore"))

rollup = {}
for u in sorted(unit_loc, key=lambda x: -sum(unit_loc[x].values())):
    d = unit_loc[u]
    tot = sum(d.values())
    rollup[u] = {
        "files": len(unit_files[u]),
        "methods": unit_methods[u],
        "loc_total": tot,
        "loc_ui": d.get("UI", 0),
        "loc_logic": d.get("LOGIC", 0),
        "loc_glue": d.get("GLUE", 0),
        "loc_unclassified": d.get("UNCLASSIFIED", 0),
        "pct_logic": round(100.0 * d.get("LOGIC", 0) / tot, 1) if tot else 0.0,
    }

grand = defaultdict(int)
for u in unit_loc:
    for k, v in unit_loc[u].items():
        grand[k] += v
grand_b = defaultdict(int)
for u in unit_loc_uifirst:
    for k, v in unit_loc_uifirst[u].items():
        grand_b[k] += v

out = {
    "root": ROOT,
    "rule": {
        "precedence": "LOGIC > GLUE > UI",
        "L1_LOGIC": L1_LOGIC, "L2_ENTITY": L2_ENTITY, "L2_COMPUTE": L2_COMPUTE,
        "UI_TERMS": UI_TERMS, "GLUE_TERMS": GLUE_TERMS,
    },
    "totals_approved_rule": dict(grand),
    "totals_sensitivity_ui_first": dict(grand_b),
    "mixed_files": mixed_files,
    "residue_lines": residue_total,
    "unclassified_trivial_le3loc": {"loc": uncl_trivial[0], "methods": uncl_trivial[1]},
    "unclassified_substantive_gt3loc": {"loc": uncl_subst[0], "methods": uncl_subst[1]},
    "ib_xml": ib,
    "units": rollup,
    "files": file_rows,
}
json.dump(out, open(os.path.join(HERE, "loc_split.json"), "w"), indent=1)

T = sum(grand.values())
print(f"total code lines classified: {T}")
for k in ("UI", "LOGIC", "GLUE", "UNCLASSIFIED"):
    print(f"  {k:<14} {grand[k]:>7}  {100.0*grand[k]/T:5.1f}%")
print(f"\nUNCLASSIFIED breakdown: trivial(<=3loc) {uncl_trivial[0]} loc in "
      f"{uncl_trivial[1]} methods | substantive(>3loc) {uncl_subst[0]} loc in "
      f"{uncl_subst[1]} methods")
print(f"mixed-class files: {mixed_files}   residue lines: {residue_total}")
print(f"IB_XML (separate): {ib['files']} files, {ib['lines']} xml lines")
print("\nsensitivity, UI-first precedence:")
for k in ("UI", "LOGIC", "GLUE", "UNCLASSIFIED"):
    print(f"  {k:<14} {grand_b[k]:>7}  {100.0*grand_b[k]/T:5.1f}%")
print(f"\n{'unit':<34}{'tot':>7}{'UI':>7}{'LOGIC':>7}{'GLUE':>7}{'UNCL':>7}{'%log':>7}")
for u, d in rollup.items():
    print(f"{u:<34}{d['loc_total']:>7}{d['loc_ui']:>7}{d['loc_logic']:>7}"
          f"{d['loc_glue']:>7}{d['loc_unclassified']:>7}{d['pct_logic']:>7}")
