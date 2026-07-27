#!/usr/bin/env python3
"""Generate preflight/limits_generated.py from the supercat_server source tree.

Why this exists (IMPLEMENTATION_PLAN.md 4.1): every document that transcribed eCat's
field limits got them wrong, and at one client an agent wrote the *documented* limits
into a sync script as `[:15]` / `[:50]`, mangling 355 product names — then wrote a
validator asserting the transform's own rules, which certified the damage as passing.

So the limit table is never typed. It is derived from:

  * `<model>::ATTR_LENGTHS`          -> the real maximum for each db attribute
  * `Product::ATTRS_TO_TRUNCATE`     -> which overflows warn-and-truncate vs hard-error
  * the importers' field declarations -> which CSV header maps to which attribute

The CSV header for a `field_for :attr` with no `name:` option is derived exactly the
way `Importer::Transformer.field_for` derives it:

    field_name = opts[:name]&.to_s || attr.to_s.downcase.remove('_')

Usage:
    python gen_limits.py --server-root ~/supercat-code/supercat_server
    python gen_limits.py --check      # exit 1 if the committed table is stale

`--check` is what CI/tests call. It re-derives the table and diffs it against the
committed file, so a limit change in supercat_server surfaces as a failing test
rather than as silent drift.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SERVER_ROOT = Path("~/supercat-code/supercat_server").expanduser()
OUT_PATH = Path(__file__).resolve().parent.parent / "preflight" / "limits_generated.py"

# --- source files we parse -------------------------------------------------------

MODEL_FILES = {
    "Product": "app/models/product.rb",
    "Customer": "app/models/customer.rb",
    "ShippingLocation": "app/models/shipping_location.rb",
    "Option": "app/models/option.rb",
    "OptionGroup": "app/models/option_group.rb",
    "Inventory": "app/models/inventory.rb",
    "Taxonomy": "app/models/taxonomy.rb",
}

IMPORTER_FILES = {
    "product": "app/services/importer/product_importer.rb",
    "inventory": "app/services/importer/inventory_importer.rb",
    "option": "app/services/importer/option_importer.rb",
    "option_group": "app/models/importer/option_group_importer.rb",
    "customer": "app/models/importer/customer_importer.rb",
    "shipping_location": "app/models/importer/shipping_location_importer.rb",
}

OTHER_FILES = {
    "cdn_image_sync": "app/services/importer/product_importer_lib/cdn_image_sync.rb",
    "line_data_validator": "app/services/importer/line_data_validator.rb",
    "file_reader": "app/models/file_reader.rb",
}

# Ruby constants used as hash keys/values in the importers. Resolved here because a
# regex cannot follow a constant reference; each is asserted against source below, so
# a rename breaks generation instead of producing a bogus header name.
RUBY_CONSTANTS = {"CUSTOMER_CODE": "code", "OPTIONS_KEY": "options"}
CONSTANT_ASSERTIONS = {
    "CUSTOMER_CODE": ("customer", "CUSTOMER_CODE"),
    "OPTIONS_KEY": ("option_group", "OPTIONS_KEY = 'options'"),
}

# Thresholds that live in importer *logic* rather than in ATTR_LENGTHS. Each carries a
# snippet asserted to still exist in the named file — if the importer stops emitting it,
# generation fails instead of silently shipping a stale advisory tier.
ADVISORY_SPECS = [
    {
        "file": "customers.csv",
        "header": "billtocode",
        "limit": 15,
        "source": "customer",
        "assert_contains": "is greater than 15 characters",
        "note": "importer logs :warning above 15; Customer::ATTR_LENGTHS errors above 20",
    },
]

# The BOM story (4.8), pinned to the two code paths that disagree about it.
BOM_SPECS = {
    "header_read": {
        "source": "line_data_validator",
        "assert_contains": "CSV.open(path, 'r', &:first)",
        "note": "header validation reads WITHOUT the bom| prefix, so a BOM survives",
    },
    "row_read": {
        "source": "file_reader",
        "assert_contains": "encoding: 'bom|utf-8'",
        "note": "row parsing DOES strip the BOM — which is why the failure looks absurd",
    },
    "message": {
        "source": "line_data_validator",
        "assert_contains": "Column #{column} is missing and is required",
        "note": "the fatal a BOM produces, naming a column that is plainly present",
    },
}


def read(server_root, key, table):
    path = Path(server_root) / table[key]
    if not path.exists():
        raise SystemExit(f"ERROR: expected source file not found: {path}")
    return path.read_text(encoding="utf-8"), table[key]


def braced_block(text, start_marker):
    """Return the text between the braces of `start_marker = {` ... `}`."""
    idx = text.find(start_marker)
    if idx == -1:
        return None
    open_idx = text.find("{", idx)
    if open_idx == -1:
        return None
    depth = 0
    for i in range(open_idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1:i]
    return None


def parse_attr_lengths(text):
    """Parse `ATTR_LENGTHS = { key: 255, :other => 60 }` in either Ruby hash style."""
    block = braced_block(text, "ATTR_LENGTHS")
    if block is None:
        return {}
    out = {}
    for match in re.finditer(
        r"(?::(\w+)\s*=>|(\w+)\s*:)\s*(\d+)", block
    ):
        attr = match.group(1) or match.group(2)
        out[attr] = int(match.group(3))
    return out


def parse_attrs_to_truncate(text):
    match = re.search(r"ATTRS_TO_TRUNCATE\s*=\s*%i\[(.*?)\]", text, re.S)
    if not match:
        return set()
    return {tok for tok in match.group(1).split()}


def parse_field_for(text):
    """Parse `field_for :attr, name: 'header'` declarations -> {attr: (header, required)}.

    Mirrors Importer::Transformer.field_for:
        field_name = opts[:name]&.to_s || attr.to_s.downcase.remove('_')
    """
    out = {}
    for match in re.finditer(r"^\s*field_for\s+:(\w+)(.*)$", text, re.M):
        attr, opts = match.group(1), match.group(2)
        name = re.search(r"name:\s*['\":]?([\w.]+)['\"]?", opts)
        header = name.group(1) if name else attr.lower().replace("_", "")
        required = bool(re.search(r"required:\s*:fatal", opts))
        out[attr] = (header.lower(), required)
    return out


def parse_percent_w_fields(text, method_name):
    """Parse `'header' => %w[attr S]` / `'header' => [CONST, 'S']` hashes."""
    block = braced_block(text, f"def self.{method_name}")
    if block is None:
        return {}
    out = {}
    for match in re.finditer(
        r"['\"]([\w]+)['\"]\s*=>\s*(?:%w\[\s*(\w+)|(?:\[\s*(\w+)))", block
    ):
        header = match.group(1).lower()
        attr = match.group(2) or match.group(3)
        out[header] = RUBY_CONSTANTS.get(attr, attr)
    return out


def parse_generic_fields(text, method_name):
    """Parse `'header' => { :type => 'S', :required => true, :field => 'attr' }`.

    A bare-word key is a Ruby constant reference (e.g. OPTIONS_KEY), so resolve it
    through RUBY_CONSTANTS rather than downcasing the constant name into a header.
    """
    block = braced_block(text, f"def self.{method_name}")
    if block is None:
        return {}
    out = {}
    for match in re.finditer(
        r"(?:['\"](\w+)['\"]|(\w+))\s*=>\s*\{([^}]*)\}", block
    ):
        if match.group(2):
            const = match.group(2)
            if const not in RUBY_CONSTANTS:
                raise SystemExit(
                    f"ERROR: unresolved Ruby constant {const!r} used as a field key in "
                    f"{method_name}; add it to RUBY_CONSTANTS with an assertion."
                )
            header = RUBY_CONSTANTS[const]
        else:
            header = match.group(1).lower()
        body = match.group(3)
        field = re.search(r":field\s*=>\s*['\"](\w+)['\"]", body)
        required = bool(re.search(r":required\s*=>\s*true", body))
        out[header] = (field.group(1) if field else None, required)
    return out


def parse_requirement_hash(text, method_name):
    block = braced_block(text, f"def self.{method_name}")
    if block is None:
        return set()
    return {
        m.group(1).lower()
        for m in re.finditer(r"['\"](\w+)['\"]\s*=>\s*\{\s*type:\s*:fatal", block)
    }


def parse_valid_content_types(text):
    match = re.search(r"valid_content_types\s*=\s*%w\[(.*?)\]", text, re.S)
    return sorted(match.group(1).split()) if match else []


def parse_valid_extnames(text):
    match = re.search(r"valid_extnames\s*=\s*%w\[(.*?)\]", text, re.S)
    return sorted(match.group(1).split()) if match else []


def parse_image_regex(text):
    """Product::VALID_IMAGE_REGEX, translated from Ruby anchors to Python ones."""
    match = re.search(r"VALID_IMAGE_REGEX\s*=\s*%r\{(.*?)\}", text)
    if not match:
        return None
    return match.group(1).replace(r"\A", "^").replace(r"\z", "$")


def git_sha(server_root):
    try:
        out = subprocess.run(
            ["git", "-C", str(server_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def sha1(path):
    return hashlib.sha1(Path(path).read_bytes()).hexdigest()[:12]


def build(server_root):
    """Derive the whole table. Returns a dict ready to render."""
    server_root = Path(server_root)
    models, model_text, sources = {}, {}, {}

    for name, rel in MODEL_FILES.items():
        text, rel = read(server_root, name, MODEL_FILES)
        model_text[name] = text
        models[name] = {
            "lengths": parse_attr_lengths(text),
            "truncate": parse_attrs_to_truncate(text),
        }
        sources[rel] = sha1(server_root / rel)
        if not models[name]["lengths"]:
            raise SystemExit(f"ERROR: no ATTR_LENGTHS parsed from {rel}")

    importer_text = {}
    for name, rel in IMPORTER_FILES.items():
        text, rel = read(server_root, name, IMPORTER_FILES)
        importer_text[name] = text
        sources[rel] = sha1(server_root / rel)

    for name, rel in OTHER_FILES.items():
        text, rel = read(server_root, name, OTHER_FILES)
        importer_text[name] = text
        sources[rel] = sha1(server_root / rel)

    def entries(model, header_to_attr, truncate_attrs):
        """header -> {limit, tier, attr, model}, for headers whose attr has a limit."""
        lengths = models[model]["lengths"]
        out = {}
        for header, attr in sorted(header_to_attr.items()):
            if attr is None or attr not in lengths:
                continue
            out[header] = {
                "limit": lengths[attr],
                "tier": "truncate" if attr in truncate_attrs else "error",
                "attr": attr,
                "model": model,
            }
        return out

    # products.csv
    product_fields = parse_field_for(importer_text["product"])
    product_headers = {h: a for a, (h, _r) in product_fields.items()}
    products = entries("Product", product_headers, models["Product"]["truncate"])

    # inventory.csv
    inv_fields = parse_field_for(importer_text["inventory"])
    inventory = entries(
        "Inventory", {h: a for a, (h, _r) in inv_fields.items()}, set()
    )

    # options.csv
    opt_fields = parse_field_for(importer_text["option"])
    options = entries("Option", {h: a for a, (h, _r) in opt_fields.items()}, set())

    # option_groups.csv
    og_fields = parse_generic_fields(importer_text["option_group"], "fields")
    option_groups = entries(
        "OptionGroup", {h: a for h, (a, _r) in og_fields.items()}, set()
    )

    # customers.csv — bill-to columns plus the ship-to continuation columns, which
    # are a different model (ShippingLocation) in the same physical file.
    cust_headers = parse_percent_w_fields(importer_text["customer"], "customer_fields")
    ship_headers = parse_percent_w_fields(importer_text["shipping_location"], "fields")
    customers = entries("Customer", cust_headers, set())
    customers.update(entries("ShippingLocation", ship_headers, set()))

    limits = {
        "products.csv": products,
        "customers.csv": customers,
        "inventory.csv": inventory,
        "options.csv": options,
        "option_groups.csv": option_groups,
    }

    required = {
        "products.csv": sorted(h for _a, (h, r) in product_fields.items() if r),
        "inventory.csv": sorted(h for _a, (h, r) in inv_fields.items() if r),
        "options.csv": sorted(h for _a, (h, r) in opt_fields.items() if r),
        "option_groups.csv": sorted(h for h, (_a, r) in og_fields.items() if r),
        "customers.csv": sorted(
            parse_requirement_hash(importer_text["customer"], "fields_by_requirement")
        ),
        "customers.csv:shipto": sorted(
            parse_requirement_hash(
                importer_text["shipping_location"], "fields_by_requirement"
            )
        ),
    }

    advisory = {}
    for spec in ADVISORY_SPECS:
        text = importer_text[spec["source"]]
        if spec["assert_contains"] not in text:
            raise SystemExit(
                f"ERROR: advisory limit for {spec['file']}:{spec['header']} no longer "
                f"traceable — {spec['assert_contains']!r} absent from "
                f"{IMPORTER_FILES[spec['source']]}. Re-read the importer before editing "
                f"this number."
            )
        advisory.setdefault(spec["file"], {})[spec["header"]] = {
            "limit": spec["limit"],
            "note": spec["note"],
            "source": IMPORTER_FILES[spec["source"]],
        }

    for key, spec in BOM_SPECS.items():
        src = OTHER_FILES.get(spec["source"], IMPORTER_FILES.get(spec["source"]))
        text = importer_text[spec["source"]]
        if spec["assert_contains"] not in text:
            raise SystemExit(
                f"ERROR: BOM premise '{key}' no longer holds — "
                f"{spec['assert_contains']!r} absent from {src}. The BOM check may be "
                f"obsolete; re-read the code before regenerating."
            )

    for const, (source, snippet) in CONSTANT_ASSERTIONS.items():
        if snippet not in importer_text[source]:
            raise SystemExit(
                f"ERROR: Ruby constant {const} no longer defined as expected in "
                f"{IMPORTER_FILES[source]} (looked for {snippet!r})."
            )

    cdn = importer_text["cdn_image_sync"]
    image_rules = {
        "content_types": parse_valid_content_types(cdn),
        "extensions": parse_valid_extnames(cdn),
        "filename_regex": parse_image_regex(model_text["Product"]),
    }
    if not all(image_rules.values()):
        raise SystemExit(f"ERROR: could not parse image rules: {image_rules}")

    bom_message = re.search(
        r"fatal:\s*->\(column\)\s*\{\s*\"(.*?)\"", importer_text["line_data_validator"]
    )

    return {
        "limits": limits,
        "required": required,
        "advisory": advisory,
        "image_rules": image_rules,
        "bom_fatal_message": (
            bom_message.group(1).replace("#{column}", "{column}")
            if bom_message else None
        ),
        "sources": dict(sorted(sources.items())),
        "git_sha": git_sha(server_root),
    }


def render(spec, server_root):
    def pyrepr(obj, indent=4):
        pad = " " * indent
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            inner = ",\n".join(
                f"{pad}{k!r}: {pyrepr(v, indent + 4)}" for k, v in obj.items()
            )
            return "{\n" + inner + ",\n" + " " * (indent - 4) + "}"
        if isinstance(obj, list):
            return repr(obj)
        return repr(obj)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        '"""AUTO-GENERATED by scripts/tools/gen_limits.py — DO NOT EDIT BY HAND.',
        "",
        "Every number here was read out of supercat_server, not out of a document.",
        "Regenerate with:",
        "",
        "    python scripts/tools/gen_limits.py --server-root <path-to-supercat_server>",
        "",
        "and verify with `--check`, which the test suite runs whenever the source tree",
        "is available. See IMPLEMENTATION_PLAN.md 4.1 for why transcribing these is",
        "a build error rather than a style choice.",
        '"""',
        "",
        f"GENERATED_AT = {now!r}",
        f"SOURCE_REPO = 'supercat_server'",
        f"SOURCE_GIT_SHA = {spec['git_sha']!r}",
        "",
        "# path within supercat_server -> short content hash at generation time",
        f"SOURCE_FILES = {pyrepr(spec['sources'])}",
        "",
        "# file -> csv header (lowercase) -> limit metadata.",
        "#   tier 'error'    -> the importer raises a validation error; the row is rejected",
        "#   tier 'truncate' -> the importer warns and silently truncates (ATTRS_TO_TRUNCATE)",
        f"LIMITS = {pyrepr(spec['limits'])}",
        "",
        "# Headers the importer treats as fatal-if-absent.",
        f"REQUIRED_HEADERS = {pyrepr(spec['required'])}",
        "",
        "# Thresholds that live in importer logic rather than ATTR_LENGTHS. These warn.",
        f"ADVISORY_LIMITS = {pyrepr(spec['advisory'])}",
        "",
        "# CdnImageSync accepts a URL only if BOTH gates pass (4.7).",
        f"IMAGE_RULES = {pyrepr(spec['image_rules'])}",
        "",
        "# The fatal a UTF-8 BOM produces via LineDataValidator#validate_header (4.8),",
        "# which reads the header with CSV.open and no 'bom|' prefix while row parsing",
        "# uses FileReader.each_line with encoding 'bom|utf-8' and strips it.",
        f"BOM_FATAL_MESSAGE = {spec['bom_fatal_message']!r}",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--server-root", default=os.environ.get(
        "SUPERCAT_SERVER_ROOT", str(DEFAULT_SERVER_ROOT)))
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed table differs from the source")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    root = Path(args.server_root).expanduser()
    if not root.exists():
        print(f"ERROR: supercat_server not found at {root}")
        print("Pass --server-root or set SUPERCAT_SERVER_ROOT.")
        return 2

    spec = build(root)
    rendered = render(spec, root)
    out = Path(args.out)

    if args.check:
        if not out.exists():
            print(f"FAIL: {out} does not exist — run without --check to generate it")
            return 1
        # Compare everything except the volatile generation timestamp.
        def strip_ts(text):
            return "\n".join(
                l for l in text.splitlines() if not l.startswith("GENERATED_AT")
            )
        if strip_ts(out.read_text(encoding="utf-8")) == strip_ts(rendered):
            print(f"PASS: {out.name} matches supercat_server @ {spec['git_sha'][:8]}")
            return 0
        print(f"FAIL: {out.name} is STALE against supercat_server "
              f"@ {spec['git_sha'][:8]} — regenerate with gen_limits.py")
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    total = sum(len(v) for v in spec["limits"].values())
    print(f"Wrote {out}")
    print(f"  {total} header limits across {len(spec['limits'])} files "
          f"from supercat_server @ {spec['git_sha'][:8]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
