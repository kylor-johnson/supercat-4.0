"""Phase 3: the unit ledger.

UNIT BOUNDARY (justified once): a unit is one Xcode PBXGroup-derived code unit
from Phase 0 section 1.3, as approved. That choice is kept here for one reason
that matters to the ledger's arithmetic: PBXGroup units form a PARTITION of the
source, so loc_ui + loc_logic + loc_glue summed over units equals the Phase 1.2
totals exactly, with no double counting. Capability clusters and engines are not
introduced as separate rows -- where an engine exists it already IS a unit (Sync,
Pricing, Kit/Options related, Query), and that mapping is recorded per row in
`engine_role`.

Pure-infrastructure pseudo-units (_Pods, _Frameworks, _Products, _Resources,
_root, _Classes_root, _Test) carry no first-party source and are excluded; the
excluded set and its LOC are reported so the partition still reconciles.

Every classification below carries `rationale` and `source`. Fields that the
evidence does not determine are the literal string "UNKNOWN" and are escalated
to Phase 4 -- that is the designed outcome, not a gap.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HERE, "..", "03_UNIT_LEDGER.json")

census = json.load(open(os.path.join(HERE, "..", "01_CODE_CENSUS.json")))
tenants = json.load(open(os.path.join(HERE, "..", "02_TENANT_CENSUS.json")))
coupling = json.load(open(os.path.join(HERE, "coupling.json")))
swift = {r["unit"]: r for r in
         json.load(open(os.path.join(HERE, "swiftshare.json")))["units"]}

LOC = census["1_2_loc_split"]["units"]
TESTS = census["1_7_confidence_signals"]["unit_files_referenced_by_tests"]
CPLX = census["1_7_confidence_signals"]["complexity_by_unit"]
HAZ = census["1_6_port_hazards"]["hazards"]
SCREENS = census["1_1_surface_inventory"]["screens"]

EXCLUDED = ["_Pods", "_Frameworks", "_Products", "_Resources", "_root",
            "_Classes_root", "_Test", "_SuperCatTest", "_UNMAPPED",
            "_Other Sources"]

# Hazards attributed to units by the files each hazard touches.
haz_files = {h["hazard"]: set(h.get("file_list", [])) for h in HAZ}
haz_kind = {h["hazard"]: h["web_equivalent"] for h in HAZ}
file_unit = {os.path.basename(k): v for k, v in
             json.load(open(os.path.join(HERE, "units.json")))["file_to_unit"].items()}


def hazards_for(unit):
    found = []
    for hz, files in haz_files.items():
        if any(file_unit.get(os.path.basename(f)) == unit for f in files):
            found.append(f"{hz}:{haz_kind[hz]}")
    return sorted(found)


# ---------------------------------------------------------------------------
# Tenant reach per unit. Each entry names the measured Phase 2 quantity used,
# so tenants_touched is never a guess.
# ---------------------------------------------------------------------------
# ==========================================================================
# AMENDMENT 1 -- spike_status (the field approved in Phase 0 section 2.1 and
# omitted from the first Phase 3 pass).
#
# Measured, not asserted: scripts/spike.json counts lines added per unit on
# supercat_server origin/spike/ecat-web vs its merge-base. Threshold rule,
# applied mechanically:
#   PARTIALLY_BUILT     >= 50 added lines of unit-specific application code
#   PATTERN_ESTABLISHED  1-49 added lines (touched; no working surface)
#   NOT_STARTED           0 added lines
# ==========================================================================
_spike = json.load(open(os.path.join(HERE, "spike.json")))["per_unit"]


def spike_status(unit):
    v = _spike.get(unit)
    if not v or v["added"] == 0:
        return "NOT_STARTED", 0, 0
    added, files = v["added"], v["files"]
    lvl = "PARTIALLY_BUILT" if added >= 50 else "PATTERN_ESTABLISHED"
    return lvl, added, files


# ==========================================================================
# AMENDMENT 2 -- the eCat component registry.
#
# 22 files / 19,329 lines on supercat_server origin/master documenting the
# iPad app, dated 2026-04-03. Phase 1 MISSED this because it searched the iOS
# repo only. Its existence overturns behavior_specification=CODE_ONLY for the
# units it covers.
#
# registry_coverage levels (measured, scripts/registry.json):
#   DEDICATED_SPEC -- a registry component or workflow file whose SUBJECT is
#                     this unit exists (mapping below, one line per claim)
#   REFERENCED     -- unit's iOS files are named in the registry, but no file
#                     is dedicated to it
#   NONE           -- zero references anywhere in the registry
# ==========================================================================
_reg = json.load(open(os.path.join(HERE, "registry.json")))

# Which registry file is ABOUT which unit. Each entry is a checkable claim.
DEDICATED = {
    "Grid view related": ["components/catalog-browsing.yaml"],
    "Left Nav": ["components/left-navigation.yaml"],
    "SingleItemView related": ["components/product-detail.yaml"],
    "Query": ["components/smart-stacks.yaml", "workflows/stack-management.yaml"],
    "Order related": ["components/order-flow.yaml",
                      "workflows/order-creation.yaml"],
    "Customer": ["components/customer-flow.yaml"],
    "Kit/Options related": ["components/options-configuration.yaml"],
    "Reporting and Email Generation": [
        "components/presentations.yaml",
        "workflows/presentation-generation.yaml"],
    "Settings": ["components/settings-auth-sync.yaml", "_config-bindings.yaml"],
    "Login": ["components/settings-auth-sync.yaml",
              "workflows/authentication.yaml"],
    "Sync": ["_sync-protocol.yaml", "workflows/sync-cycle.yaml",
             "components/settings-auth-sync.yaml"],
    "SuperCat Notices": ["components/notices-territory.yaml"],
    "Data objects": ["_data-model.yaml"],
    "Global classes": ["_overview.yaml"],
}


def registry_for(unit):
    r = _reg["per_unit"].get(unit)
    if unit in DEDICATED:
        lvl = "DEDICATED_SPEC"
    elif r:
        lvl = "REFERENCED"
    else:
        lvl = "NONE"
    return {
        "registry_coverage": lvl,
        "registry_dedicated_docs": DEDICATED.get(unit, []),
        "registry_ios_files_documented": (
            r["distinct_ios_files_documented"] if r else 0),
        # denominator is the unit's file count in scripts/units.json (all
        # project-mapped files incl. headers), NOT the scc source-file count
        "registry_unit_files_total": (r["unit_total_files"] if r else None),
        "registry_pct_unit_files_documented": (
            r["pct_files_documented"] if r else 0.0),
    }


# behavior_specification is RECOMPUTED from registry coverage. CONTESTED wins
# over SPECIFIED: a doc that disagrees with the code is worse than no doc.
CONTESTED_UNITS = {
    "Data objects": ("registry _data-model.yaml documents 40 SQLite tables and "
                     "4 Core Data entities as a fixed shape; 240 tenants carry "
                     "product custom fields (max 185, median 33.5) so no fixed "
                     "shape exists in production"),
    "Grid view related": ("KB documents 6 product images; the paid "
                          "enable_twelve_product_images flag allows 12"),
    "Pricing": ("KB describes per-browser My Account markup rules that belong "
                "to eCat Online, not the iPad; iPad visibility is governed by "
                "user group. Registry names only 1 of 18 Pricing files"),
    "Query": ("KB documents SmartList item lists as comma-separated; the "
              "importer and app expect newline-separated"),
}


def behavior_spec(unit, original):
    if unit in CONTESTED_UNITS:
        return "CONTESTED"
    if original == "SPECIFIED":          # Categories, _Third Party
        return "SPECIFIED"
    if unit in DEDICATED:
        return "SPECIFIED"
    return "CODE_ONLY"


REACH = {
    "Sync": (255, "all tenants; data_versions tracks 22 live entity types for "
                  "235-253 orgs each (02 sync_entity_types)"),
    "Order related": (117, "submit_order telemetry reach 117 of 192; PG orders "
                           "table has rows for 190 orgs"),
    "Global classes": (255, "spine; fan_in 24 units, the highest measured"),
    "Data objects": (255, "spine; fan_in 20 units"),
    "Grid view related": (157, "search_products reach 157; filter_products 150"),
    "Reporting and Email Generation": (
        124, "create_pdf_catalog 124; export_data_to_excel 61; "
             "export_data_to_csv 61; ipad_reports table 227 orgs"),
    "SingleItemView related": (157, "product detail is reached from the grid; "
                                    "bounded by search_products 157"),
    "Customer": (150, "select_a_customer 150; customers table 208 orgs"),
    "Left Nav": (123, "search_collections 123; drilldown_leftnav_collections "
                      "true for 57 of 223"),
    "Kit/Options related": (43, "order_configured_item 43 (max of: view_kit 24, "
                                "order_kit 20, options table 91, kit_items 49, "
                                "matrix_options 53)"),
    "Settings": (255, "settings screens are unconditional"),
    "Categories": (123, "search_collections 123; taxonomies table 240 orgs"),
    "Login": (255, "unconditional"),
    "Documents Related": (151, "view_library_entry 151; shared_resources table "
                               "168 orgs"),
    "RepActivity": (7, "enable_rep_activity boolean true for 7 of 255"),
    "Custom UI controls": (255, "shared control layer, fan_in 11"),
    "ShowroomCart": (2, "enable_showroom_carts json flag true for 2; "
                        "showroom_locations table has 1 org, 2 rows"),
    "Organization chooser": (191, "selected_org telemetry reach 191"),
    "Pricing": (235, "price_levels table 235 orgs; matrix_options 53; "
                     "contract_prices 19"),
    "Scan Groups": (91, "scan_item_with_camera 91; enable_camera_scanning "
                        "boolean true for 142"),
    "Commitments": (5, "view_commitments telemetry 5; commitment_reports table "
                       "7 orgs"),
    "Flipbook": (11, "view_flipbook 11; enable_flipbook_support true for 26 of "
                     "197; order_from_flipbook 5; add_to_list_from_flipbook 4"),
    "ActionPopover": (255, "shared presentation layer, fan_in 4"),
    "SemanticSearch": (13, "smart_search_embeddings_generated 13 orgs, "
                           "smart_search_toggled 11; last event 2026-04-27"),
    "Placements": (41, "view_placements 41; placement_reports table 24 orgs"),
    "Spreadsheet Import": ("UNKNOWN", "no telemetry event and no PG table maps "
                                      "to this unit"),
    "Select List": (255, "generic picker used by other units, fan_in 5"),
    "SuperCat Notices": (114, "view_notifications 114, first seen 2026-02-02"),
    "Database Migration": (255, "63 SQLite migration files run on every device"),
    "Query": (190, "smart_stacks table 190 orgs; view_smart_stack telemetry 102"),
    "Notifications": ("UNKNOWN", "no telemetry event and no PG table maps to "
                                 "push/local notification delivery; "
                                 "view_notifications (114 orgs) belongs to the "
                                 "SuperCat Notices unit, not this one"),
    "Core Data Support": (255, "Core Data stack initialisation"),
    "External code": (255, "third-party glue compiled into every build"),
    "_Third Party": (255, "vendored dependencies compiled into every build"),
}

# ---------------------------------------------------------------------------
# Classifications. `A` and `B` hold port_class where the two scenarios differ.
# ---------------------------------------------------------------------------
U = "UNKNOWN"
LEDGER = {
 "Sync": dict(
    engine_role="sync engine",
    A="INVENTION", B="INVENTION",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "INVENTION in BOTH scenarios, and this is the single most consequential "
        "row in the ledger. Phase 1.4 found ZERO conflict-resolution branches: "
        "no 'conflict', 'lastwritewins', 'tombstone', 'etag', 'vector clock' "
        "vocabulary anywhere in the 3,935-LOC unit. The existing design is "
        "purge-and-replace -- the server is authoritative, the device discards "
        "and reloads. Scenario A cannot transcribe a conflict resolver that does "
        "not exist, so offline parity requires inventing merge semantics that "
        "the product has never specified. Scenario B is ALSO invention, not "
        "removal: 22 server-side entity types are versioned through "
        "data_versions and something must still decide freshness, cache "
        "invalidation and reload granularity for a connected web client. "
        "Classifying this RESPECIFICATION would be the error the brief warns "
        "about. 0 test files reference this unit."),
    scenario_delta=(
        "Identical class, different content. A must invent bidirectional merge "
        "and conflict semantics for 31 participating entity types across two "
        "local stacks. B must invent a freshness/invalidation policy for 22 "
        "server-versioned entity types. Neither is determined by existing code.")),

 "Order related": dict(
    engine_role="order construction",
    A="INVENTION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="BEHAVIOR_PARITY",
    rationale=(
        "Largest unit at 13,531 LOC and 73% LOGIC (9,902), which is order "
        "construction, validation, discounting and submission -- exactly the "
        "code that produces a wrong business answer if reimplemented naively. "
        "B is RESPECIFICATION: behaviour is determined by code plus a server "
        "contract, but the interaction model must be redesigned for web. A is "
        "INVENTION because local order construction depends on the "
        "purge-and-replace store having no merge story, and because "
        "require_online_order_submission is true for 185 of 218 tenants -- so "
        "'offline order construction' contradicts the currently configured "
        "product for most tenants and cannot be settled by reading code. "
        "7 test files reference the unit, so acceptance is partly anchored."),
    scenario_delta=(
        "B redesigns a determined behaviour. A additionally requires deciding "
        "whether offline submission is permitted at all, against 185 tenants "
        "configured to forbid it.")),

 "Global classes": dict(
    engine_role="application spine / shared services",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "Highest measured coupling in the codebase: fan_in 24 units, 453 "
        "imports received. 11,302 LOC of which 6,071 LOGIC and 1,508 UI. "
        "Contains MakesURLs.m, the single URL-construction chokepoint for all "
        "123 API call sites. SPINE by measurement, not by assertion. Not "
        "MECHANICAL because the unit mixes iOS lifecycle assumptions into "
        "shared services, so a web target must re-specify the boundary. 22 "
        "test files reference it."),
    scenario_delta="No measured difference between scenarios."),

 "Data objects": dict(
    engine_role="domain model / entity layer",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CONTESTED",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "10,955 LOC, fan_in 20, 63% LOGIC. CONTESTED rather than CODE_ONLY "
        "because the product entity demonstrably has no fixed shape: Phase 2.4 "
        "measured 240 of 255 tenants carrying product custom fields, one with "
        "185 of them. Any reimplementation must decide what the canonical "
        "entity is, and tenants disagree by construction. 9 test files."),
    scenario_delta="No measured difference between scenarios."),

 "Grid view related": dict(
    engine_role="catalog browse and search",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CONTESTED",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="UNDECIDED",
    rationale=(
        "10,461 LOC, the highest-reach feature surface (search_products 157 "
        "tenants, 3,397,018 events -- the most-fired event in the product). "
        "CONTESTED because documented behaviour and code disagree on image "
        "count: 6 images by default, 12 only with enable_twelve_product_images, "
        "true for 44 of 254 tenants. fidelity_bar UNDECIDED because the grid is "
        "where the 1024x768-to-1366x1024 device spread bites and no responsive "
        "target has been chosen. 10 test files."),
    scenario_delta=(
        "A must additionally serve this grid from a local store at the measured "
        "catalog ceiling: 50,614 active SKUs and 131,596 product images for the "
        "largest tenants.")),

 "Reporting and Email Generation": dict(
    engine_role="PDF/CSV/XLSX generation and share",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="HUMAN_JUDGMENT_ONLY",
    fidelity_bar="PIXEL_PARITY",
    rationale=(
        "6,548 LOC, 87.8% Swift. Generates customer-facing PDF catalogues "
        "(create_pdf_catalog, 124 tenants, 96,597 events) plus CSV and XLSX "
        "export. fidelity_bar PIXEL_PARITY is forced by the artifact, not "
        "chosen: the output is a document a rep hands to a buyer, so "
        "correctness is judged by appearance. acceptance HUMAN_JUDGMENT_ONLY "
        "for the same reason -- 2 test files exist but a rendered document is "
        "not assertable without visual comparison. Carries the pdf_generation "
        "and mailcompose hazards, both POLYFILLABLE."),
    scenario_delta=(
        "A must generate documents on-device with no server round trip; B may "
        "render server-side, which removes the hazard entirely.")),

 "SingleItemView related": dict(
    engine_role="product detail",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="HUMAN_JUDGMENT_ONLY",
    fidelity_bar="UNDECIDED",
    rationale=(
        "3,303 LOC, 0% Swift, 0 test files, fan_out 10. Pure presentation of a "
        "product record whose shape varies per tenant (up to 185 custom "
        "fields). RESPECIFICATION because the layout must be re-derived for "
        "responsive breakpoints; the data it shows is determined."),
    scenario_delta="No measured difference between scenarios."),

 "Customer": dict(
    engine_role="customer selection and context",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="BEHAVIOR_PARITY",
    rationale=(
        "3,018 LOC, 81% LOGIC, 53.8% Swift so coupling is PARTIAL_SWIFT_OPAQUE. "
        "Customer selection sets the price level for everything downstream "
        "(select_a_customer, 150 tenants, 690,621 events), which is why "
        "blast_radius is MULTI_SURFACE rather than ISOLATED. Largest tenant "
        "holds 92,669 customers. 1 test file."),
    scenario_delta=(
        "A must hold up to 92,669 customer records plus ship-tos locally.")),

 "Left Nav": dict(
    engine_role="taxonomy navigation",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "2,991 LOC, 65% LOGIC, 0 test files. Drives collection/category "
        "drilldown, and its behaviour is flag-dependent per tenant: "
        "drilldown_leftnav_collections true for 57 of 223, "
        "drilldown_leftnav_categories 50 of 223, drilldown_library_items 50 of "
        "201. RESPECIFICATION because a persistent left rail is a tablet "
        "idiom that must be re-decided for narrow viewports."),
    scenario_delta="No measured difference between scenarios."),

 "Kit/Options related": dict(
    engine_role="CPQ / configurable products / kits / matrix pricing",
    A="INVENTION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "2,982 LOC, 77% LOGIC, and ZERO test files reference it -- the "
        "highest-risk combination in the ledger: pure business logic with no "
        "acceptance anchor. This is the CPQ engine (configurable items, kits, "
        "matrix option pricing). Reach is concentrated, not broad: "
        "order_configured_item 43 tenants but 134,377 events; view_kit 24 "
        "tenants, 169,619 events. A is INVENTION because of scale, not "
        "behaviour: matrix_options reaches 1,669,094 rows for tenant 5 and "
        "770,494 for tenant 109, and whether that priced configuration space "
        "can live in a browser store is an unmade product decision. B is "
        "RESPECIFICATION -- server-side evaluation is determined."),
    scenario_delta=(
        "B evaluates configurations server-side. A must decide how 1.67M "
        "matrix rows reach a browser, or that they do not.")),

 "Settings": dict(
    engine_role="user and app configuration",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "2,507 LOC, 71% LOGIC, 0 test files. Surfaces a per-tenant flag space "
        "that Phase 2.2 measured as 239 distinct actual boolean configurations "
        "across 255 tenants out of a 105-flag declared surface. Contains one "
        "unreachable screen (SettingsAboutController, 15 LOC)."),
    scenario_delta="No measured difference between scenarios."),

 "Categories": dict(
    engine_role="taxonomy",
    A="RESPECIFICATION", B="MECHANICAL",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="SPECIFIED",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "2,138 LOC, fan_in 19 (third-highest). SPECIFIED because taxonomy "
        "semantics are documented in the eCat authority material "
        "(CollectionCodes / CategoryCodes / TradeNameCode become the iPad "
        "label; groups never auto-create) and 8 test files reference the unit. "
        "B is MECHANICAL: a documented tree with tests, rendered as a tree. "
        "A is RESPECIFICATION because the tree must be materialised locally at "
        "up to 4,109 taxonomy nodes per tenant."),
    scenario_delta="B transcribes; A must decide local materialisation."),

 "Login": dict(
    engine_role="authentication and session",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "1,606 LOC. SPINE and CUTOVER_ONLY because every other unit sits "
        "behind it; there is no flag that runs old and new auth side by side. "
        "Carries the keychain and biometric_auth hazards (both POLYFILLABLE, "
        "but browser credential storage is not keychain-equivalent). 2 test "
        "files."),
    scenario_delta=(
        "A requires authenticating with no network, which the current design "
        "does via locally cached credentials; browsers offer no keychain "
        "equivalent, so A inherits a REQUIRES_PRODUCT_DECISION.")),

 "Documents Related": dict(
    engine_role="library / shared resources",
    A="RESPECIFICATION", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "1,300 LOC and the second-broadest feature reach in telemetry "
        "(view_library_entry, 151 tenants, 571,679 events; shared_resources "
        "table 168 tenants, max 740 documents). B is MECHANICAL -- serving and "
        "viewing documents has a direct web equivalent. A is RESPECIFICATION "
        "because offline document availability requires deciding what is "
        "cached, and carries the local_filesystem hazard "
        "(REQUIRES_PRODUCT_DECISION). 0 test files."),
    scenario_delta="B serves documents; A must decide the caching policy."),

 "RepActivity": dict(
    engine_role="rep activity logging",
    A="RESPECIFICATION", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "1,166 LOC, 100% Swift so coupling is UNKNOWN_SWIFT_OPAQUE (measured "
        "fan_in 0 is a limitation of file-level import analysis, not evidence "
        "of isolation). enable_rep_activity is true for only 7 of 255 tenants, "
        "and rep_activity_log_label is set for 34. Low reach makes it a Phase 5 "
        "candidate. 0 test files."),
    scenario_delta="B is a form and a list; A must queue entries locally."),

 "Custom UI controls": dict(
    engine_role="shared control layer",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="HUMAN_JUDGMENT_ONLY",
    fidelity_bar="UNDECIDED",
    rationale=(
        "1,024 LOC, fan_in 11. A bespoke UIKit control set; there is no web "
        "equivalent to transcribe, so every control is a design decision "
        "against the chosen web framework. SPINE because 11 units depend on "
        "it. 0 test files and appearance-judged, hence "
        "HUMAN_JUDGMENT_ONLY."),
    scenario_delta="No measured difference between scenarios."),

 "ShowroomCart": dict(
    engine_role="showroom cart",
    A="REQUIRES_PRODUCT_DECISION", B="REQUIRES_PRODUCT_DECISION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="UNDECIDED",
    rationale=(
        "1,014 LOC, 100% Swift. The narrowest reach measured anywhere in the "
        "product: enable_showroom_carts is true for 2 tenants and "
        "showroom_locations holds 2 rows for exactly 1 tenant (org 6, "
        "shortname 'demo'). Whether this is rewritten at all is a product "
        "decision, so it is escalated rather than classified. 1 test file."),
    scenario_delta="Undetermined in both until the keep/kill decision is made."),

 "Organization chooser": dict(
    engine_role="multi-org switching",
    A="MECHANICAL", B="MECHANICAL",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "987 LOC, 0% Swift, 0 test files. A list of organizations and a "
        "selection that sets context (selected_org, 191 tenants, 1,675,664 "
        "events -- the second-most-fired event). MECHANICAL because the "
        "behaviour is a picker with a known web equivalent and no unmade "
        "decision sits under it."),
    scenario_delta="No measured difference between scenarios."),

 "Pricing": dict(
    engine_role="pricing engine",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CONTESTED",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "880 LOC and 87% LOGIC with ZERO UI -- the purest business-logic unit "
        "in the codebase, and the one where a naive reimplementation produces "
        "a wrong number a customer is invoiced for. fan_in 10. CONTESTED: "
        "documented pricing behaviour and implementation disagree (per-browser "
        "'My Account' markup applies to eCat Online, not iPad; price "
        "visibility is governed by user group rather than price level), and "
        "tenants differ sharply -- 235 tenants have price levels (max 326), 53 "
        "use matrix pricing, 19 use contract prices, 52 use surcharges. 8 test "
        "files, the best-anchored logic unit."),
    scenario_delta=(
        "Same class. A must additionally evaluate price locally across up to "
        "326 price levels plus 1.67M matrix rows for the largest tenant.")),

 "Scan Groups": dict(
    engine_role="barcode scanning",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "556 LOC, 100% Swift, 0 test files. scan_item_with_camera reaches 91 "
        "tenants with 285,756 events, and item_scan_failed 88 tenants -- real "
        "use, not vestigial. Carries the camera_barcode_scanning hazard, "
        "POLYFILLABLE via getUserMedia plus BarcodeDetector, but the supported "
        "symbology set is tenant-configured "
        "(supported_camera_scan_symbologies), so parity is not automatic."),
    scenario_delta="No measured difference between scenarios."),

 "Commitments": dict(
    engine_role="commitment reporting",
    A="REQUIRES_PRODUCT_DECISION", B="REQUIRES_PRODUCT_DECISION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "510 LOC, 100% Swift, 0 test files. view_commitments reaches 5 tenants "
        "(3,593 events) and commitment_reports holds rows for 7. "
        "commitments_market_code is set for 14. Escalated rather than "
        "classified: at 5 tenants the keep/kill decision precedes any port "
        "classification."),
    scenario_delta="Undetermined in both until the keep/kill decision is made."),

 "Flipbook": dict(
    engine_role="flipbook catalog",
    A="REQUIRES_PRODUCT_DECISION", B="REQUIRES_PRODUCT_DECISION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "510 LOC, 94.7% Swift, 0 test files. enable_flipbook_support is true "
        "for 26 of 197 tenants but actual use is far narrower: view_flipbook 11 "
        "tenants, order_from_flipbook 5 (68 events), add_to_list_from_flipbook "
        "4 (35 events). The gap between 26 enabled and 4-11 using is itself "
        "the finding. Escalated."),
    scenario_delta="Undetermined in both until the keep/kill decision is made."),

 "ActionPopover": dict(
    engine_role="shared presentation",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="HUMAN_JUDGMENT_ONLY",
    fidelity_bar="UNDECIDED",
    rationale=(
        "498 LOC, 0% Swift, 1 test file. Popover presentation is an iPad idiom "
        "with no responsive equivalent -- the popover_presentation hazard is "
        "REQUIRES_PRODUCT_DECISION across 32 call sites and 8 screens. What "
        "replaces a popover on a narrow viewport is a design decision, so "
        "RESPECIFICATION rather than MECHANICAL."),
    scenario_delta="No measured difference between scenarios."),

 "SemanticSearch": dict(
    engine_role="on-device semantic search",
    A="REQUIRES_PRODUCT_DECISION", B="REQUIRES_PRODUCT_DECISION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "456 LOC, 0 test files. Telemetry shows this was switched on and then "
        "stopped: smart_search_embeddings_generated fired 37 times across 13 "
        "tenants and its last event is 2026-04-27, while every other live event "
        "runs to 2026-08-07. smart_search_toggled: 11 tenants, 37 events. "
        "Phase 1.6 additionally found sqlite-vec static libraries and a CoreML "
        "SentenceTransformer model shipped in the bundle with zero referencing "
        "source. Both hazards are REQUIRES_PRODUCT_DECISION with 0 call sites. "
        "This is either an abandoned experiment or an unlaunched feature; the "
        "codebase cannot distinguish the two and neither can telemetry."),
    scenario_delta="Undetermined in both until the keep/kill decision is made."),

 "Placements": dict(
    engine_role="placement reporting",
    A="RESPECIFICATION", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "435 LOC, 100% Swift, 0 test files. view_placements reaches 41 tenants "
        "(10,340 events); placement_reports holds rows for 24, concentrated "
        "(org 18 has 9,542). Four flags govern behaviour: "
        "enable_historical_placements (62 of 234), "
        "enable_placement_reports_for_all_shipping_locations (57), "
        "display_placement_report_quantities (49), "
        "enable_placements_gallery_audit (39). B is MECHANICAL as a "
        "report view; A must decide local capture."),
    scenario_delta="B renders a report; A must queue captures offline."),

 "Spreadsheet Import": dict(
    engine_role="spreadsheet import",
    A=U, B=U,
    blast_radius="UNKNOWN",
    reversibility="UNKNOWN",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="UNDECIDED",
    rationale=(
        "327 LOC, 100% Swift, 0 test files, coupling UNKNOWN_SWIFT_OPAQUE. "
        "port_class is UNKNOWN because no telemetry event and no Postgres table "
        "maps to this unit, so tenants_touched cannot be measured and reach "
        "cannot be bounded. Filling this in would be a guess. Escalated to "
        "Phase 4 as an evidence gap rather than a product decision."),
    scenario_delta="UNKNOWN in both; reach is unmeasured."),

 "Select List": dict(
    engine_role="generic picker",
    A="MECHANICAL", B="MECHANICAL",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "292 LOC, 0% Swift, 86% LOGIC, fan_in 5. A reusable selection list. "
        "MECHANICAL: fully determined by existing code with an obvious web "
        "equivalent and no product decision underneath. 0 test files."),
    scenario_delta="No measured difference between scenarios."),

 "SuperCat Notices": dict(
    engine_role="in-app notices",
    A="MECHANICAL", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "180 LOC, 100% Swift, 0 test files. view_notifications reaches 114 "
        "tenants but only from 2026-02-02, so this is the newest surface in the "
        "product. enable_billing_notices is true for 62 of 67 carrying the key. "
        "MECHANICAL -- a notice list has a direct web equivalent."),
    scenario_delta="No measured difference between scenarios."),

 "Database Migration": dict(
    engine_role="local schema migration",
    A="INVENTION", B="MECHANICAL",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "Only 177 LOC of driver code, but it executes 63 SQLite migration files "
        "totalling 1,577 SQL lines that build 47 tables, alongside a SEPARATE "
        "Core Data stack with 19 model versions and 18 inter-version "
        "migrations. B is MECHANICAL because a connected web client needs no "
        "local schema at all -- this unit largely disappears. A is INVENTION: "
        "browser storage has no Core Data and no FMDB, so two independent local "
        "migration histories must be re-founded on a browser storage engine "
        "whose choice has not been made. LOC is a severe understatement of "
        "scope here and the 63 migration files are the real quantity."),
    scenario_delta=(
        "The largest single asymmetry in the ledger: B deletes two local "
        "persistence stacks and their migration histories; A must reinvent "
        "both on an unchosen browser storage engine.")),

 "Query": dict(
    engine_role="SmartList query engine",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="MULTI_SURFACE",
    reversibility="FLAGGABLE",
    behavior_specification="CONTESTED",
    acceptance_determinism="TEST_EXISTS",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "Only 160 LOC but 100% LOGIC and 0% UI, and it evaluates tenant-authored "
        "queries: smart_stacks holds rows for 190 tenants (max 256 for org 26), "
        "view_smart_stack reaches 102. CONTESTED because documented and actual "
        "behaviour disagree on a load-bearing detail -- SmartList item lists are "
        "documented as comma-separated but the implementation expects "
        "newline-separated, and a comma-separated list is parsed as one invalid "
        "item number. Reimplementing the evaluator without that knowledge "
        "silently breaks 190 tenants' saved lists. 1 test file."),
    scenario_delta=(
        "A must evaluate tenant-authored queries against a local store; B "
        "evaluates server-side.")),

 "Core Data Support": dict(
    engine_role="Core Data stack",
    A="INVENTION", B="MECHANICAL",
    blast_radius="SPINE",
    reversibility="CUTOVER_ONLY",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "43 LOC of stack setup, but it anchors the core_data_local_persistence "
        "hazard: 221 call sites across 49 files and 7 screens, classified "
        "REQUIRES_PRODUCT_DECISION. B is MECHANICAL because a connected client "
        "does not need it. A is INVENTION for the same reason as Database "
        "Migration -- there is no Core Data in a browser and no replacement has "
        "been chosen. 0 test files."),
    scenario_delta="B removes the stack; A must replace it."),

 "External code": dict(
    engine_role="third-party glue",
    A="MECHANICAL", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "205 LOC, 75% GLUE, 0 LOGIC. Adapter code around vendored libraries; "
        "replaced wholesale by web equivalents rather than ported. 0 test "
        "files."),
    scenario_delta="No measured difference between scenarios."),

 "Notifications": dict(
    engine_role="push / local notifications",
    A="RESPECIFICATION", B="RESPECIFICATION",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="CODE_ONLY",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "109 LOC, the smallest classified unit, 63% UI, 0 test files. Carries "
        "the push_local_notifications hazard (2 call sites, POLYFILLABLE). "
        "RESPECIFICATION rather than MECHANICAL because web push requires an "
        "explicit user permission grant and a service worker, and on iOS Safari "
        "it additionally requires the site be installed to the home screen -- "
        "so the delivery model is not equivalent and must be re-specified."),
    scenario_delta="No measured difference between scenarios."),

 "_Third Party": dict(
    engine_role="vendored dependencies",
    A="MECHANICAL", B="MECHANICAL",
    blast_radius="ISOLATED",
    reversibility="FLAGGABLE",
    behavior_specification="SPECIFIED",
    acceptance_determinism="TESTABLE_NOT_TESTED",
    fidelity_bar="OUTCOME_EQUIVALENT",
    rationale=(
        "357 LOC, 78% GLUE. Vendored third-party source (including "
        "NetworkStatusMonitor). SPECIFIED because the behaviour is defined by "
        "the upstream libraries' own documentation, not by this codebase. "
        "Replaced by web-native equivalents. 0 test files."),
    scenario_delta="No measured difference between scenarios."),
}


def build():
    rows, problems, amended = [], [], []
    for unit, c in LEDGER.items():
        loc = LOC.get(unit)
        if not loc:
            problems.append(f"{unit}: no LOC record")
            continue
        cp = coupling["units"].get(unit, {})
        sw = swift.get(unit, {})
        reach, reach_src = REACH.get(unit, ("UNKNOWN", "not mapped"))
        cx = CPLX.get(unit, {})
        unit_screens = [s["screen_id"] for s in SCREENS if s.get("unit") == unit]
        sp_lvl, sp_added, sp_files = spike_status(unit)
        reg = registry_for(unit)
        bspec = behavior_spec(unit, c["behavior_specification"])
        if bspec != c["behavior_specification"]:
            amended.append(
                f"{unit}: behavior_specification "
                f"{c['behavior_specification']} -> {bspec}")

        for scen in ("A", "B"):
            rows.append({
                "unit_id": unit,
                "scenario": scen,
                "engine_role": c["engine_role"],
                "port_class": c[scen],
                "blast_radius": c["blast_radius"],
                "tenants_touched": reach,
                "tenants_touched_basis": reach_src,
                "reversibility": c["reversibility"],
                "behavior_specification": bspec,
                "behavior_specification_first_pass": c["behavior_specification"],
                "contested_because": CONTESTED_UNITS.get(unit),
                "spike_status": sp_lvl,
                "spike_lines_added": sp_added,
                "spike_files_touched": sp_files,
                **reg,
                "acceptance_determinism": c["acceptance_determinism"],
                "fidelity_bar": c["fidelity_bar"],
                "coupling_fan_in": cp.get("coupling_fan_in", 0),
                "coupling_fan_out": cp.get("coupling_fan_out", 0),
                "coupling_confidence": sw.get("coupling_confidence", "UNKNOWN"),
                "swift_pct": sw.get("swift_pct"),
                "port_hazards": hazards_for(unit),
                "loc_ui": loc["loc_ui"],
                "loc_logic": loc["loc_logic"],
                "loc_glue": loc["loc_glue"],
                "loc_unclassified": loc["loc_unclassified"],
                "loc_total": loc["loc_total"],
                "files": loc["files"],
                "methods": loc["methods"],
                "test_files_referencing_unit": TESTS.get(unit, 0),
                "complexity": cx,
                "screens_in_unit": len(unit_screens),
                "rationale": c["rationale"],
                "scenario_delta": c["scenario_delta"],
                "source": ("01_CODE_CENSUS.json 1_2_loc_split.units + "
                           "1_7_confidence_signals; scripts/coupling.json; "
                           "scripts/swiftshare.json; 02_TENANT_CENSUS.json; "
                           "scripts/spike.json; scripts/registry.json"),
            })

    covered = sum(LOC[u]["loc_total"] for u in LEDGER if u in LOC)
    excluded = {u: LOC[u]["loc_total"] for u in EXCLUDED if u in LOC}
    total = sum(v["loc_total"] for v in LOC.values())
    if covered + sum(excluded.values()) != total:
        problems.append(f"LOC partition mismatch: {covered}+"
                        f"{sum(excluded.values())} != {total}")

    return rows, problems, amended, covered, excluded, total


rows, problems, amended, covered, excluded, total = build()

out = {
    "phase": 3,
    "generated": "2026-08-08",
    "unit_boundary": {
        "method": "Xcode PBXGroup-derived code units (Phase 0 section 1.3, approved)",
        "justification": (
            "PBXGroup units PARTITION the source, so LOC sums over units equal "
            "the Phase 1.2 totals with no double counting. Engines are not "
            "separate rows because each already IS a unit; the mapping is in "
            "engine_role."),
        "units_classified": len(LEDGER),
        "loc_classified": covered,
        "loc_excluded_infrastructure": excluded,
        "loc_total_phase1": total,
        "partition_reconciles": covered + sum(excluded.values()) == total,
    },
    "axis_definitions_used": {
        "MECHANICAL": "target behaviour fully determined by existing code; "
                      "reimplementable by transcription against a known web "
                      "equivalent",
        "RESPECIFICATION": "behaviour determined, interaction model must be "
                           "redesigned for web/responsive form factors",
        "INVENTION": "no amount of code reading determines the work; an unmade "
                     "product decision sits underneath",
        "REQUIRES_PRODUCT_DECISION": "used as a port_class here for units whose "
                                     "keep/kill decision precedes any port "
                                     "classification; escalated to Phase 4",
    "CODE_ONLY": "behaviour exists nowhere but the implementation; no doc, "
                 "no test, no ticket explains why",
        "CONTESTED": "documented behaviour and implemented behaviour disagree, "
                     "with the disagreement evidenced",
        "spike_status": {
            "PARTIALLY_BUILT": ">=50 lines of unit-specific application code "
                               "added on supercat_server "
                               "origin/spike/ecat-web",
            "PATTERN_ESTABLISHED": "1-49 lines added; touched, no working "
                                   "surface",
            "NOT_STARTED": "0 lines added",
            "note": "categorical, measured from git diff --numstat; contains "
                    "no time quantity",
        },
        "registry_coverage": {
            "DEDICATED_SPEC": "a registry component or workflow file whose "
                              "subject is this unit exists",
            "REFERENCED": "unit's iOS files are named in the registry but no "
                          "file is dedicated to it",
            "NONE": "zero references anywhere in the registry",
        },
    },
    "amendments_to_first_pass": {
        "1_spike_status_added": (
            "The spike_status field was approved in Phase 0 section 2.1 and "
            "omitted from the first Phase 3 pass. Added and measured from "
            "scripts/spike.json."),
        "2_component_registry_found": (
            "docs/design/ecat-component-registry/ (22 files, 19,329 lines, "
            "dated 2026-04-03) exists on supercat_server origin/master and "
            "documents the iPad app: 84 components, 5 workflows, 40 SQLite "
            "tables, 4 Core Data entities, 236 config settings. Phase 1 "
            "missed it because it searched the iOS repo only. "
            "behavior_specification was recomputed against it; the CODE_ONLY "
            "population drops accordingly. Each unit now carries "
            "behavior_specification_first_pass so the change is auditable."),
    },
    "registry": {
        "path": _reg["registry_path"],
        "files": _reg["registry_files"],
        "lines": _reg["registry_total_lines"],
        "dated": _reg["registry_dated"],
        "self_reported_status": "needs_attention (10 broken dependency "
                                "cross-references, 3 unregistered components: "
                                "action-popover, order-list, commitments-view)",
        "source": "supercat_server origin/master; scripts/p3_registry.py",
    },
    "spike": {
        "branch": "supercat_server origin/spike/ecat-web",
        "merge_base": json.load(open(os.path.join(HERE, "spike.json")))[
            "merge_base"],
        "commits_ahead": json.load(open(os.path.join(HERE, "spike.json")))[
            "commits_ahead"],
        "total_lines_added": json.load(open(os.path.join(HERE, "spike.json")))[
            "total_lines_added"],
        "source": "scripts/p3_spike.py",
    },
    "problems_found": problems,
    "amendments_applied": amended,
    "rows": rows,
}
with open(DEST, "w") as fh:
    json.dump(out, fh, indent=2)

# ---- rollups -------------------------------------------------------------
def roll(scen, key):
    d = {}
    for r in rows:
        if r["scenario"] != scen:
            continue
        d[r[key]] = d.get(r[key], 0) + 1
    return dict(sorted(d.items(), key=lambda kv: -kv[1]))


def loc_by(scen, key):
    d = {}
    for r in rows:
        if r["scenario"] != scen:
            continue
        d[r[key]] = d.get(r[key], 0) + r["loc_total"]
    return dict(sorted(d.items(), key=lambda kv: -kv[1]))


print(f"units={len(LEDGER)} rows={len(rows)} problems={problems}")
print(f"amendments applied: {len(amended)}")
for a in amended:
    print(f"   {a}")
print(f"LOC classified={covered} excluded={sum(excluded.values())} "
      f"total={total} reconciles={covered + sum(excluded.values()) == total}")
for scen in ("A", "B"):
    print(f"\n=== Scenario {scen} port_class (units | LOC)")
    u, l = roll(scen, "port_class"), loc_by(scen, "port_class")
    for k in u:
        print(f"  {k:<28}{u[k]:>4} units {l[k]:>8} LOC")
print(f"\n=== blast_radius (scenario-invariant)")
for k, v in roll("A", "blast_radius").items():
    print(f"  {k:<20}{v:>4} units {loc_by('A','blast_radius')[k]:>8} LOC")
print(f"\n=== behavior_specification")
for k, v in roll("A", "behavior_specification").items():
    print(f"  {k:<20}{v:>4} units {loc_by('A','behavior_specification')[k]:>8} LOC")
print(f"\n=== acceptance_determinism")
for k, v in roll("A", "acceptance_determinism").items():
    print(f"  {k:<24}{v:>4} units")
print(f"\n=== fidelity_bar")
for k, v in roll("A", "fidelity_bar").items():
    print(f"  {k:<22}{v:>4} units")
print(f"\n=== spike_status (measured, supercat_server origin/spike/ecat-web)")
for k, v in roll("A", "spike_status").items():
    print(f"  {k:<22}{v:>4} units {loc_by('A','spike_status')[k]:>8} LOC")
print(f"\n=== registry_coverage (measured, ecat-component-registry)")
for k, v in roll("A", "registry_coverage").items():
    print(f"  {k:<22}{v:>4} units {loc_by('A','registry_coverage')[k]:>8} LOC")
print(f"\n=== behavior_specification: first pass vs amended")
fp, am = roll("A", "behavior_specification_first_pass"), \
    roll("A", "behavior_specification")
for k in sorted(set(fp) | set(am)):
    lf = loc_by("A", "behavior_specification_first_pass").get(k, 0)
    la = loc_by("A", "behavior_specification").get(k, 0)
    print(f"  {k:<14} first_pass={fp.get(k,0):>3}u/{lf:>6}LOC   "
          f"amended={am.get(k,0):>3}u/{la:>6}LOC")

print(f"\n=== units whose port_class differs between scenarios")
byu = {}
for r in rows:
    byu.setdefault(r["unit_id"], {})[r["scenario"]] = r["port_class"]
diff = {u: v for u, v in byu.items() if v["A"] != v["B"]}
for u, v in diff.items():
    print(f"  {u:<32} A={v['A']:<28} B={v['B']}")
print(f"  ({len(diff)} of {len(byu)} units differ)")
print(f"\nwrote {DEST}")
