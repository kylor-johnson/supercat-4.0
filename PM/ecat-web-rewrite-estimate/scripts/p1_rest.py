#!/usr/bin/env python3
"""
Phase 1.3 - 1.8. Emits scripts/rest.json

1.3 data model (19 xcdatamodel versions)
1.4 sync/offline engine
1.5 integration surface (iOS endpoint strings x server routes)
1.6 platform-native port hazards
1.7 confidence signals
1.8 dead code
"""
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
IOS = "/tmp/ecat-audit/ios-master/eCatalog"
SERVER = "/tmp/ecat-audit/server-master"
CLASSES = os.path.join(IOS, "Classes")
UNITS = json.load(open(os.path.join(HERE, "units.json")))
LOC = json.load(open(os.path.join(HERE, "loc_split.json")))
FILE_TO_UNIT = UNITS["file_to_unit"]
LOC_BY_FILE = {os.path.basename(r["file"]): r for r in LOC["files"]}
out = {}


def rg_count(pattern, path=CLASSES, globs=("*.m", "*.h", "*.swift"), flags="-ci"):
    """Total match count via ripgrep. Returns (count, files_touched)."""
    cmd = ["rg", flags, pattern]
    for g in globs:
        cmd += ["--glob", g]
    cmd.append(path)
    r = subprocess.run(cmd, capture_output=True, text=True)
    n, files = 0, 0
    for line in r.stdout.strip().split("\n"):
        if ":" in line:
            try:
                n += int(line.rsplit(":", 1)[1])
                files += 1
            except ValueError:
                pass
    return n, files


def rg_files(pattern, path=CLASSES, globs=("*.m", "*.h", "*.swift")):
    cmd = ["rg", "-li", pattern]
    for g in globs:
        cmd += ["--glob", g]
    cmd.append(path)
    r = subprocess.run(cmd, capture_output=True, text=True)
    return sorted(os.path.basename(x) for x in r.stdout.strip().split("\n") if x)


# ============================================================ 1.3 data model
mdir = os.path.join(IOS, "eCat.xcdatamodeld")
versions = []
for name in sorted(os.listdir(mdir)):
    if not name.endswith(".xcdatamodel"):
        continue
    cpath = os.path.join(mdir, name, "contents")
    if not os.path.exists(cpath):
        continue
    root = ET.parse(cpath).getroot()
    ents = {}
    for e in root.iter("entity"):
        ents[e.get("name")] = {
            "attributes": len(e.findall("attribute")),
            "relationships": len(e.findall("relationship")),
            "parent": e.get("parentEntity"),
        }
    versions.append({
        "version": name.replace(".xcdatamodel", ""),
        "entities": len(ents),
        "attributes": sum(v["attributes"] for v in ents.values()),
        "relationships": sum(v["relationships"] for v in ents.values()),
        "entity_detail": ents,
        "source": os.path.relpath(cpath, IOS),
    })

# The CURRENT model is declared in .xccurrentversion, NOT the last one
# alphabetically. Reading the wrong one reports 25 entities instead of 3 and
# misrepresents the entire local-persistence architecture.
curname = None
xccv = os.path.join(mdir, ".xccurrentversion")
if os.path.exists(xccv):
    m = re.search(r'<string>([^<]+)\.xcdatamodel</string>',
                  open(xccv, encoding="utf-8", errors="ignore").read())
    curname = m.group(1) if m else None
cur = next((v for v in versions if v["version"] == curname), None) or \
      (versions[-1] if versions else {"entity_detail": {}})
# entity shape churn across adjacent versions
churn = []
for a, b in zip(versions, versions[1:]):
    ea, eb = a["entity_detail"], b["entity_detail"]
    added = sorted(set(eb) - set(ea))
    removed = sorted(set(ea) - set(eb))
    changed = sorted(n for n in set(ea) & set(eb)
                     if ea[n]["attributes"] != eb[n]["attributes"]
                     or ea[n]["relationships"] != eb[n]["relationships"])
    churn.append({"from": a["version"], "to": b["version"],
                  "entities_added": added, "entities_removed": removed,
                  "entities_changed_shape": changed})

# which entities participate in sync (named in Sync-unit source)
sync_files = [f for f in UNITS["units"].get("Sync", {}).get("files", [])
              if f.endswith((".m", ".h", ".swift"))]
sync_text = ""
for f in sync_files:
    p = os.path.join(CLASSES, f)
    if os.path.exists(p):
        sync_text += open(p, encoding="utf-8", errors="ignore").read()
entities_in_sync = sorted(e for e in cur["entity_detail"]
                          if re.search(r'\b%s\b' % re.escape(e), sync_text))

# ---- second persistence stack: raw SQLite schema migrations (FMDB) ----
sqldir = os.path.join(IOS, "Database")
sqlfiles = sorted(f for f in os.listdir(sqldir) if f.endswith(".sql")) \
    if os.path.isdir(sqldir) else []
sql_lines = sum(sum(1 for _ in open(os.path.join(sqldir, f), encoding="utf-8",
                                    errors="ignore")) for f in sqlfiles)
base_sql = os.path.join(sqldir, "0_base_migration.sql")
sql_tables, sql_views, sql_indices = [], [], []
if os.path.exists(base_sql):
    bt = open(base_sql, encoding="utf-8", errors="ignore").read()
    sql_tables = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)',
                            bt, re.I)
    sql_views = re.findall(r'CREATE\s+VIEW\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)', bt, re.I)
    sql_indices = re.findall(r'CREATE\s+(?:UNIQUE\s+)?INDEX', bt, re.I)
# tables created by later migrations too
all_sql = "".join(open(os.path.join(sqldir, f), encoding="utf-8",
                       errors="ignore").read() for f in sqlfiles)
sql_tables_all = sorted(set(re.findall(
    r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)', all_sql, re.I)))
sql_views_all = sorted(set(re.findall(
    r'CREATE\s+VIEW\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\[]?(\w+)', all_sql, re.I)))

out["data_model"] = {
    "ARCHITECTURE_NOTE": (
        "Local persistence is TWO independent stacks with TWO independent "
        "migration histories: (1) raw SQLite via FMDB holds the catalog "
        "(products, customers, inventory, options, pricing); (2) Core Data holds "
        "ONLY locally-created orders. The Core Data model shrank from 25 entities "
        "to 3 at version 'eCat 20150407', when the catalog moved to SQLite. Any "
        "rewrite must replace both, not one."),
    "core_data": {
        "model_versions": len(versions),
        "migrations_between_adjacent_versions": len(churn),
        "current_version_declared_in_xccurrentversion": curname,
        "current_version_used": cur.get("version"),
        "current_entities": cur.get("entities"),
        "current_attributes": cur.get("attributes"),
        "current_relationships": cur.get("relationships"),
        "current_entity_names": sorted(cur.get("entity_detail", {})),
        "entities_participating_in_sync": len(entities_in_sync),
        "entities_participating_in_sync_list": entities_in_sync,
        "versions": [{k: v for k, v in ver.items() if k != "entity_detail"}
                     for ver in versions],
        "version_churn": churn,
        "entities_current_detail": cur.get("entity_detail"),
        "source": ("eCat.xcdatamodeld/.xccurrentversion for current version; "
                   "eCat.xcdatamodeld/*/contents parsed with ElementTree"),
    },
    "sqlite_fmdb": {
        "migration_files": len(sqlfiles),
        "migration_sql_lines": sql_lines,
        "base_migration_tables": len(set(sql_tables)),
        "base_migration_views": len(set(sql_views)),
        "base_migration_index_statements": len(sql_indices),
        "tables_created_across_all_migrations": len(sql_tables_all),
        "views_created_across_all_migrations": len(sql_views_all),
        "table_names": sql_tables_all,
        "view_names": sql_views_all,
        "source": "eCatalog/Database/*.sql regex scan for CREATE TABLE/VIEW/INDEX",
    },
}

# ============================================================ 1.4 sync engine
sync_loc = LOC["units"].get("Sync", {})
conflict_probe = {}
for term in ["conflict", "lastwritewins", "last_write", "tombstone", "etag",
             "if-modified-since", "vector clock", "merge", "resolve",
             "overwrite", "stale", "dirty", "pending", "retry", "backoff",
             "reachab", "timeout", "cancel", "purge", "rollback", "transaction"]:
    n, f = rg_count(term)
    conflict_probe[term] = {"matches": n, "files": f}

# NSMergePolicy is the Core Data conflict mechanism; count explicit policies
merge_policy_files = rg_files(r'NSMergePolicy|mergePolicy|NSMergeByProperty|NSOverwriteMergePolicy|NSRollbackMergePolicy')
retry_files = rg_files(r'\bretry|backoff|attemptCount|maxAttempts|reachabilityChanged')
sync_methods = []
for f in sync_files:
    p = os.path.join(CLASSES, f)
    if f.endswith(".m") and os.path.exists(p):
        txt = open(p, encoding="utf-8", errors="ignore").read()
        sync_methods += re.findall(r'^[-+]\s*\([^)]*\)\s*([A-Za-z_][\w:]*)', txt, re.M)

# Sync spans BOTH persistence stacks. Counting only Core Data entities named in
# the Sync unit understates it (Core Data now holds only 3 order entities).
sqlite_tables_in_sync = sorted(t for t in sql_tables_all
                               if re.search(r'\b%s\b' % re.escape(t), sync_text))
# the sync engine also drives DataStore/BuildsDataObjects, so widen the corpus
wider = sync_text
for f in ("DataStore.m", "BuildsDataObjects.m", "DataObject.m", "ProductQuery.m"):
    p = os.path.join(CLASSES, f)
    if os.path.exists(p):
        wider += open(p, encoding="utf-8", errors="ignore").read()
sqlite_tables_in_sync_wide = sorted(t for t in sql_tables_all
                                    if re.search(r'\b%s\b' % re.escape(t), wider))

out["sync_engine"] = {
    "unit": "Sync",
    "files": len(sync_files),
    "core_data_entities_named_in_sync": len(entities_in_sync),
    "core_data_entities_named_in_sync_list": entities_in_sync,
    "sqlite_tables_named_in_sync_unit": len(sqlite_tables_in_sync),
    "sqlite_tables_named_in_sync_unit_list": sqlite_tables_in_sync,
    "sqlite_tables_named_in_sync_plus_datastore": len(sqlite_tables_in_sync_wide),
    "sqlite_tables_named_in_sync_plus_datastore_list": sqlite_tables_in_sync_wide,
    "entity_types_participating_total_both_stacks":
        len(entities_in_sync) + len(sqlite_tables_in_sync_wide),
    "loc_total": sync_loc.get("loc_total"),
    "loc_ui": sync_loc.get("loc_ui"),
    "loc_logic": sync_loc.get("loc_logic"),
    "loc_glue": sync_loc.get("loc_glue"),
    "methods_objc_in_sync_unit": len(sync_methods),
    "entity_types_participating_in_sync": len(entities_in_sync),
    "conflict_resolution_branches": 0,
    "conflict_resolution_branches_basis": (
        "zero matches for 'conflict', 'lastwritewins', 'last_write', 'tombstone', "
        "'etag', 'vector clock' across all .m/.h/.swift in Classes/; no NSMergePolicy "
        "declaration found. There is no conflict-resolution engine to port."),
    "lww_paths": 0,
    "merge_resolved_paths": 0,
    "nsmergepolicy_files": merge_policy_files,
    "retry_backoff_files": retry_files,
    "vocabulary_probe": conflict_probe,
    "sync_method_names": sorted(set(sync_methods)),
    "source": "units.json Sync unit + loc_split.json + ripgrep counts (see vocabulary_probe)",
}

# ============================================================ 1.5 integration
# iOS endpoints are NOT bare "/path" literals. All URL construction funnels
# through MakesURLs, which appends a `resource` string to an org base URL or to
# {loginHost}/api/v1/. Scanning for "/..." literals found only 11 paths and was
# effectively a tooling failure; extract the resource arguments instead.
RESOURCE_CALLS = re.compile(
    r'(?:baseAPIURLForResource|URLForResource|APIURLForResource'
    r'|urlForResource|apiURLForResource)\s*:?\s*\(?\s*@?"([^"]+)"')
FMT_RESOURCE = re.compile(
    r'(?:baseAPIURLForResource|URLForResource|APIURLForResource'
    r'|urlForResource|apiURLForResource)\s*:?\s*\(?\s*\[?\s*NSString\s+stringWithFormat\s*:\s*@"([^"]+)"')
APPEND_PATH = re.compile(r'URLByAppendingPathComponent\s*:?\s*\(?\s*@?"([^"]+)"')

ios_paths = Counter()
ios_path_files = defaultdict(set)
parameterized = Counter()
makesurls_sites = 0
for dp, _, fns in os.walk(CLASSES):
    for fn in fns:
        if not fn.endswith((".m", ".h", ".swift")):
            continue
        txt = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        makesurls_sites += len(re.findall(r'MakesURLs', txt))
        for rx in (RESOURCE_CALLS, APPEND_PATH):
            for m in rx.finditer(txt):
                p = m.group(1)
                if p.startswith("http") or p.endswith((".png", ".jpg", ".zip")):
                    continue
                ios_paths[p] += 1
                ios_path_files[p].add(fn)
        for m in FMT_RESOURCE.finditer(txt):
            parameterized[m.group(1)] += 1
            ios_path_files[m.group(1)].add(fn)

# resource strings declared inside MakesURLs.m itself (explicit endpoints)
mk = os.path.join(CLASSES, "MakesURLs.m")
mk_txt = open(mk, encoding="utf-8", errors="ignore").read() if os.path.exists(mk) else ""
for m in re.finditer(r'@"([a-z_][a-z_0-9/]*\.(?:json|plist))"', mk_txt, re.I):
    ios_paths[m.group(1)] += 1
    ios_path_files[m.group(1)].add("MakesURLs.m")
for m in re.finditer(r'@"(api/v1/[^"]*|users/[^"]*|passwordless_sessions/[^"]*|organizations[^"]*)"',
                     mk_txt):
    ios_paths[m.group(1)] += 1
    ios_path_files[m.group(1)].add("MakesURLs.m")
hosts = re.findall(r'#define\s+\w*HOST\s+@"([^"]+)"', mk_txt)

# server routes
routes_path = os.path.join(SERVER, "config/routes.rb")
routes_txt = open(routes_path, encoding="utf-8", errors="ignore").read()
api_controllers = []
for dp, _, fns in os.walk(os.path.join(SERVER, "app/controllers/api")):
    for fn in fns:
        if fn.endswith(".rb"):
            rel = os.path.relpath(os.path.join(dp, fn), SERVER)
            txt = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
            actions = re.findall(r'^\s*def\s+(\w+)', txt, re.M)
            api_controllers.append({"file": rel, "public_actions": len(actions),
                                    "actions": actions})

# which ecat_* (web) controllers exist -> shared-surface evidence
web_ecat_controllers = sorted(
    f for f in os.listdir(os.path.join(SERVER, "app/controllers"))
    if f.startswith("ecat") and f.endswith(".rb"))

out["integration_surface"] = {
    "url_construction_chokepoint": "Classes/MakesURLs.m",
    "makesurls_call_sites": makesurls_sites,
    "hosts_hardcoded": hosts,
    "ios_endpoint_resources_distinct": len(ios_paths),
    "ios_endpoint_resources": [{"resource": p, "call_sites": c,
                                "files": sorted(ios_path_files[p])[:8]}
                               for p, c in ios_paths.most_common(100)],
    "ios_endpoint_parameterized": [{"format": p, "call_sites": c}
                                   for p, c in parameterized.most_common(40)],
    "server_api_controllers": len(api_controllers),
    "server_api_actions_total": sum(c["public_actions"] for c in api_controllers),
    "server_api_controller_detail": api_controllers,
    "server_web_ecat_controllers": web_ecat_controllers,
    "routes_file_lines": routes_txt.count("\n") + 1,
    "ipad_only_vs_shared": "UNKNOWN",
    "ipad_only_vs_shared_note": (
        "Cannot be resolved mechanically. The iPad consumes /api/v1/* which is also "
        "reachable by any client; the server has 13 ecat_* web controllers that render "
        "HTML rather than call /api/v1. Determining per-endpoint exclusivity requires "
        "server-side request-log attribution, which is not available through the "
        "read-only Postgres MCP. Left UNKNOWN rather than guessed."),
    "source": ("iOS: resource-argument extraction at MakesURLs call sites across "
               "Classes/**/*.{m,h,swift}; server: app/controllers/api/**/*.rb def-scan "
               "+ config/routes.rb"),
    "caveat": ("Resource strings assembled by stringWithFormat are reported separately "
               "as parameterized and are not expanded."),
}

# ============================================================ 1.6 port hazards
HAZARDS = [
    ("core_data_local_persistence", r'NSManagedObject|NSPersistentStore|NSFetchRequest|NSManagedObjectContext', "REQUIRES_PRODUCT_DECISION"),
    ("fmdb_sqlite_direct", r'FMDatabase|FMResultSet|sqlite3_', "POLYFILLABLE"),
    ("sqlite_vec_vector_search", r'sqlite_vec|sqlite3_vec|vec0', "REQUIRES_PRODUCT_DECISION"),
    ("coreml_on_device_embeddings", r'MLModel|CoreML|MLMultiArray', "REQUIRES_PRODUCT_DECISION"),
    ("camera_barcode_scanning", r'AVCaptureSession|AVCaptureMetadataOutput|ZXing|AVCaptureDevice', "POLYFILLABLE"),
    ("pencilkit_handwriting", r'PencilKit|PKCanvas|PKDrawing', "NONE"),
    ("drag_and_drop", r'UIDragInteraction|UIDropInteraction|UIPasteConfiguration|dragInteraction', "POLYFILLABLE"),
    ("local_filesystem", r'NSFileManager|NSSearchPathForDirectoriesInDomains|contentsOfDirectoryAtPath', "REQUIRES_PRODUCT_DECISION"),
    ("zip_archive", r'SSZipArchive|ZipArchive|unzipOpenFile', "POLYFILLABLE"),
    ("background_tasks", r'beginBackgroundTaskWithExpirationHandler|BGTaskScheduler|backgroundTimeRemaining', "REQUIRES_PRODUCT_DECISION"),
    ("push_local_notifications", r'UNUserNotificationCenter|UILocalNotification|registerForRemoteNotifications', "POLYFILLABLE"),
    ("printing", r'UIPrintInteractionController|UIPrintInfo', "POLYFILLABLE"),
    ("pdf_generation_or_render", r'UIGraphicsPDF|PDFKit|PSPDFKit|CGPDFDocument|renderInContext', "POLYFILLABLE"),
    ("webview_bridge", r'WKWebView|UIWebView|evaluateJavaScript|WKScriptMessage', "NATIVE_EQUIVALENT"),
    ("keychain", r'SecItemAdd|SecItemCopyMatching|kSecClass', "POLYFILLABLE"),
    ("biometric_auth", r'LAContext|LocalAuthentication|biometry', "POLYFILLABLE"),
    ("mailcompose_native_share", r'MFMailComposeViewController|UIActivityViewController|MFMessageCompose', "POLYFILLABLE"),
    ("split_view_ipad_multitasking", r'UISplitViewController|UIUserInterfaceSizeClass|traitCollection', "REQUIRES_PRODUCT_DECISION"),
    ("popover_presentation", r'UIPopoverPresentationController|UIPopoverController|popoverPresentation', "REQUIRES_PRODUCT_DECISION"),
    ("keyboard_hardware_input", r'UIKeyCommand|pressesBegan|GCKeyboard', "POLYFILLABLE"),
    ("device_orientation", r'UIDeviceOrientation|shouldAutorotate|supportedInterfaceOrientations', "REQUIRES_PRODUCT_DECISION"),
    ("firebase_crashlytics_analytics", r'Crashlytics|FIRApp|Firebase', "NATIVE_EQUIVALENT"),
    ("mixpanel_telemetry", r'Mixpanel', "NATIVE_EQUIVALENT"),
]
surface = json.load(open(os.path.join(HERE, "surface.json")))
screen_files = {}
for s in surface["screens"]:
    for f in s["files"]:
        screen_files.setdefault(f, []).append(s["screen_id"])

hz = []
for name, pat, web in HAZARDS:
    files = rg_files(pat)
    n, _ = rg_count(pat)
    screens_hit = sorted({sid for f in files for sid in screen_files.get(f, [])})
    loc = sum(LOC_BY_FILE.get(f, {}).get("code_lines", 0) for f in files)
    hz.append({"hazard": name, "pattern": pat, "web_equivalent": web,
               "call_sites": n, "files": len(files), "file_list": files[:25],
               "loc_in_touched_files": loc,
               "screens_affected_count": len(screens_hit),
               "screens_affected": screens_hit[:25],
               "source": f"rg -ci '{pat}' over Classes/**/*.{{m,h,swift}}"})
hz.sort(key=lambda h: -h["call_sites"])

# Some native capabilities ship as ASSETS/LIBRARIES with little or no source in
# Classes/. Reporting 0 call sites alone would misrepresent them as absent.
shipped_assets = []
for label, relpath in (("sqlite_vec_static_library", "sqlite-vec"),
                       ("coreml_sentence_transformer", "CoreMLModels"),
                       ("sqlite_vec_xcframework", "sqlite_vec.xcframework")):
    p = os.path.join(IOS, relpath)
    if os.path.exists(p):
        entries = sorted(os.listdir(p)) if os.path.isdir(p) else [relpath]
        shipped_assets.append({"asset": label, "path": relpath, "entries": entries})
r = subprocess.run(["rg", "-n", "sqlite_vec|sqlite-vec|vec0|SentenceTransformer",
                    "--glob", "*.m", "--glob", "*.h", "--glob", "*.swift", CLASSES],
                   capture_output=True, text=True)
out["port_hazards"] = hz
out["port_hazards_shipped_assets_without_source"] = {
    "assets": shipped_assets,
    "source_references_in_Classes": [x for x in r.stdout.strip().split("\n") if x],
    "finding": ("sqlite-vec static libraries, an xcframework, and a CoreML "
                "SentenceTransformer model are vendored in the repo, but the only "
                "reference in Classes/ is a comment ('// sqlite-vec testing' in "
                "DataStore.h). The SemanticSearch unit's Swift files import only "
                "Foundation. Semantic/vector search is shipped-but-dormant."),
}

# ============================================================ 1.7 confidence
test_dirs = [("SuperCatTest", os.path.join(IOS, "SuperCatTest")),
             ("test", os.path.join(IOS, "test"))]
tests = []
for label, d in test_dirs:
    if not os.path.isdir(d):
        continue
    files, lines = 0, 0
    for dp, _, fns in os.walk(d):
        for fn in fns:
            if fn.endswith((".m", ".h", ".swift")):
                files += 1
                lines += sum(1 for _ in open(os.path.join(dp, fn),
                                             encoding="utf-8", errors="ignore"))
    tests.append({"dir": label, "test_files": files, "test_lines": lines})

# which units are named by test files (crude coverage-by-reference)
test_text = ""
for label, d in test_dirs:
    for dp, _, fns in os.walk(d) if os.path.isdir(d) else []:
        for fn in fns:
            if fn.endswith((".m", ".h", ".swift")):
                test_text += open(os.path.join(dp, fn), encoding="utf-8",
                                  errors="ignore").read()
unit_test_refs = {}
for u, d in UNITS["units"].items():
    hits = 0
    for f in d["files"]:
        base = os.path.splitext(f)[0]
        if len(base) > 4 and re.search(r'\b%s\b' % re.escape(base), test_text):
            hits += 1
    unit_test_refs[u] = hits

marker = {}
for m in ("TODO", "FIXME", "HACK", "XXX", "@deprecated", "DEPRECATED", "WORKAROUND"):
    n, f = rg_count(m, flags="-c")
    marker[m] = {"matches": n, "files": f}

# scc complexity per unit (scc reports per-file; aggregate by unit)
sccout = subprocess.run(
    ["scc", "--by-file", "--format", "json", "--no-cocomo", CLASSES],
    capture_output=True, text=True)
unit_cx = defaultdict(lambda: {"complexity": 0, "code": 0, "files": 0})
try:
    for lang in json.loads(sccout.stdout):
        for fl in lang.get("Files", []):
            base = os.path.basename(fl["Location"])
            u = FILE_TO_UNIT.get(base, "_UNMAPPED")
            unit_cx[u]["complexity"] += fl.get("Complexity", 0)
            unit_cx[u]["code"] += fl.get("Code", 0)
            unit_cx[u]["files"] += 1
    scc_ok = True
except Exception as ex:  # noqa: BLE001
    scc_ok = False
    unit_cx = {"TOOLING_FAILED": str(ex)}

out["confidence_signals"] = {
    "test_dirs": tests,
    "unit_files_referenced_by_tests": unit_test_refs,
    "markers": marker,
    "scc_by_file_ok": scc_ok,
    "complexity_by_unit": {k: dict(v) for k, v in unit_cx.items()} if scc_ok else unit_cx,
    "coverage": "TOOLING_FAILED_NOT_ATTEMPTED",
    "coverage_note": ("Xcode code coverage requires building and running the test "
                      "target against a provisioned simulator. Not attempted; "
                      "reported as unavailable rather than estimated."),
    "source": "filesystem walk + rg -c + scc --by-file --format json",
}

# ============================================================ 1.8 dead code
dead = {
    "source_files_on_disk_not_in_project": UNITS["on_disk_not_in_project"],
    "unreachable_screen_candidates": [
        {"screen_id": s["screen_id"], "unit": s["unit"], "loc_total": s["loc_total"],
         "ib_documents": s["ib_documents"]}
        for s in surface["screens"] if s["reachability"] == "UNREACHABLE_CANDIDATE"],
}

# Orphan IB documents. An earlier version compared every IB file against files
# referenced by SCREENS, which wrongly flagged 64 cell/view xibs as dead. A doc
# is orphan only if NONE of its customClass values is declared anywhere in source.
declared_syms = set()
for dp, _, fns in os.walk(CLASSES):
    for fn in fns:
        if fn.endswith((".m", ".h", ".swift")):
            t = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
            declared_syms.update(re.findall(r'^@interface\s+(\w+)', t, re.M))
            declared_syms.update(re.findall(r'^\s*(?:@objc\w*\s+|public\s+|final\s+|open\s+|internal\s+)*class\s+(\w+)', t, re.M))

orphan_ib, ib_detail = [], []
for dp, _, fns in os.walk(CLASSES):
    for fn in sorted(fns):
        if not fn.endswith((".storyboard", ".xib")):
            continue
        t = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        ccs = sorted(set(re.findall(r'customClass="([^"]+)"', t)))
        known = [c for c in ccs if c in declared_syms]
        ib_detail.append({"ib": fn, "custom_classes": len(ccs), "declared_in_source": len(known)})
        if ccs and not known:
            orphan_ib.append({"ib": fn, "custom_classes": ccs})
        elif not ccs:
            orphan_ib.append({"ib": fn, "custom_classes": [], "note": "no customClass bindings at all"})
dead["ib_documents_orphan"] = orphan_ib
dead["ib_documents_total"] = len(ib_detail)

# headers declaring a class never referenced elsewhere
unref = []
for dp, _, fns in os.walk(CLASSES):
    for fn in sorted(fns):
        if not fn.endswith(".h"):
            continue
        txt = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read()
        for cls in re.findall(r'^@interface\s+(\w+)\s*:', txt, re.M):
            r = subprocess.run(["rg", "-l", r'\b%s\b' % cls, "--glob", "*.m",
                                "--glob", "*.swift", "--glob", "*.h", CLASSES],
                               capture_output=True, text=True)
            hits = [os.path.basename(x) for x in r.stdout.strip().split("\n") if x]
            others = [h for h in hits if os.path.splitext(h)[0] != os.path.splitext(fn)[0]]
            if not others:
                unref.append({"class": cls, "header": fn,
                              "unit": FILE_TO_UNIT.get(fn),
                              "loc_header": LOC_BY_FILE.get(fn, {}).get("code_lines", 0),
                              "loc_impl": LOC_BY_FILE.get(
                                  os.path.splitext(fn)[0] + ".m", {}).get("code_lines", 0)})
dead["classes_declared_but_referenced_only_in_own_pair"] = unref
dead["source"] = ("units.json on_disk_not_in_project; surface.json reachability; "
                  "rg -l per @interface class name across Classes/**")
out["dead_code"] = dead

json.dump(out, open(os.path.join(HERE, "rest.json"), "w"), indent=1)

# ------------------------------------------------------------------ console
print("=== 1.3 DATA MODEL (TWO STACKS) ===")
cd = out["data_model"]["core_data"]; sq = out["data_model"]["sqlite_fmdb"]
print("CORE DATA (orders only):")
print(f"  model versions {cd['model_versions']}  migrations {cd['migrations_between_adjacent_versions']}")
print(f"  current (.xccurrentversion) = {cd['current_version_declared_in_xccurrentversion']}")
print(f"  entities={cd['current_entities']} attrs={cd['current_attributes']} rels={cd['current_relationships']}")
print(f"  entity names: {cd['current_entity_names']}")
print(f"  entities named in Sync unit: {cd['entities_participating_in_sync']}")
print("SQLITE / FMDB (catalog):")
print(f"  migration files {sq['migration_files']}  sql lines {sq['migration_sql_lines']}")
print(f"  tables across migrations {sq['tables_created_across_all_migrations']}  views {sq['views_created_across_all_migrations']}")
print("\nCore Data version trajectory:")
for v in cd["versions"]:
    print(f"  {v['version']:<22} ent={v['entities']:>3} attr={v['attributes']:>4} rel={v['relationships']:>3}")

print("\n=== 1.4 SYNC ENGINE ===")
se = out["sync_engine"]
for k in ("files", "loc_total", "loc_logic", "loc_glue", "methods_objc_in_sync_unit",
          "entity_types_participating_in_sync", "conflict_resolution_branches",
          "lww_paths", "merge_resolved_paths"):
    print(f"  {k:<40} {se[k]}")
print(f"  NSMergePolicy files: {se['nsmergepolicy_files']}")
print(f"  retry/backoff files: {se['retry_backoff_files']}")
print("  vocabulary probe (matches, files):")
for t, d in se["vocabulary_probe"].items():
    print(f"     {t:<20} {d['matches']:>5}  {d['files']:>4}")

print("\n=== 1.5 INTEGRATION ===")
isf = out["integration_surface"]
print(f"  URL chokepoint: {isf['url_construction_chokepoint']}  call sites: {isf['makesurls_call_sites']}")
print(f"  hosts: {isf['hosts_hardcoded']}")
print(f"  iOS distinct endpoint resources: {isf['ios_endpoint_resources_distinct']}")
for e in isf['ios_endpoint_resources'][:30]:
    print(f"     {e['call_sites']:>3}  {e['resource']}")
print(f"  parameterized: {len(isf['ios_endpoint_parameterized'])}")
for e in isf['ios_endpoint_parameterized'][:12]:
    print(f"     {e['call_sites']:>3}  {e['format']}")
print(f"  server api controllers: {isf['server_api_controllers']}  actions: {isf['server_api_actions_total']}")
print(f"  server ecat_* web controllers: {len(isf['server_web_ecat_controllers'])}")

print("\n=== 1.6 PORT HAZARDS (by call sites) ===")
print(f"{'hazard':<36}{'sites':>7}{'files':>7}{'screens':>8}  web_equivalent")
for h in out["port_hazards"]:
    print(f"{h['hazard']:<36}{h['call_sites']:>7}{h['files']:>7}"
          f"{h['screens_affected_count']:>8}  {h['web_equivalent']}")

print("\n=== 1.7 CONFIDENCE ===")
cs = out["confidence_signals"]
print("  tests:", cs["test_dirs"])
print("  markers:", {k: v["matches"] for k, v in cs["markers"].items()})
print("  coverage:", cs["coverage"])

print("\n=== 1.8 DEAD CODE ===")
dc = out["dead_code"]
print(f"  on disk not in project: {dc['source_files_on_disk_not_in_project']}")
print(f"  unreachable screens: {len(dc['unreachable_screen_candidates'])}")
print(f"  IB docs total: {dc['ib_documents_total']}  orphan: {len(dc['ib_documents_orphan'])}")
for o in dc['ib_documents_orphan'][:15]: print(f"     {o}")
print(f"  classes referenced only in own .h/.m pair: {len(dc['classes_declared_but_referenced_only_in_own_pair'])}")
for c in dc["classes_declared_but_referenced_only_in_own_pair"][:20]:
    print(f"     {c['class']:<40} {c['header']:<36} loc={c['loc_header']}+{c['loc_impl']}")
