# TCS Option Mapping Deployment Runbook

**Org:** The CopperSmith | **ID:** 291 | **Shortname:** tcs

---

## Pre-Flight State (Verified 2026-06-16, updated after full API reconciliation)

- Options: 341 → will become **366** (23 new codes added from API)
- Groups: 764 → will become **863** (includes new mount type + electric groups)
- Products: 424 active (file has 425 rows)
- Option Mappings: 0 records → will become 1
- Current labels: Finish (Required), Wall Mount, Wall Mount Accessories, Ceiling Mount, Post & Pier Mount, Decorative, Electric, Gas
- **API Validation: ZERO GAPS** — all 379 API products verified, every accessory code present

---

## PHASE 1: Update Option Type Labels

### Option A: Admin Console (you do this)

1. Go to Admin Console → Company Settings (gear icon) → scroll to "Define option types"
2. Change the 8 text fields:

| # | Type to: |
|---|---|
| 1 | `Finish` |
| 2 | `Mount Type` |
| 3 | `Mount Hardware` |
| 4 | `Wall Accessories` |
| 5 | `Decorative` |
| 6 | `Electric` |
| 7 | `Gas` |
| 8 | *(leave blank)* |

3. Save

### Option B: SQL (for Support to run)

```sql
UPDATE organizations
SET option_type_labels = '---
- Finish
- Mount Type
- Mount Hardware
- Wall Accessories
- Decorative
- Electric
- Gas
'
WHERE id = 291;
```

### Verify:

```sql
SELECT option_type_labels FROM organizations WHERE id = 291;
```

---

## PHASE 2: FTP File Import

Upload files from this directory to FTP `/data/` **in this exact order**:

1. `options.csv` (wait for processing, verify clean import)
2. `option_groups.csv` (wait for processing, verify clean import)
3. `products.csv` (wait 30-45 min for processing, verify clean import)

**Check after each:** Admin Console → Tools → Admin Reports → File Import Status

### Verify:

```sql
-- Should be 366
SELECT COUNT(*) FROM options WHERE organization_id = 291;

-- Should be 863
SELECT COUNT(*) FROM option_groups WHERE organization_id = 291;

-- Should be 425
SELECT COUNT(*) FROM products WHERE organization_id = 291 AND deleted = false;

-- Confirm new mount type options exist
SELECT code, name FROM options
WHERE organization_id = 291 AND code IN ('WALL', 'CEIL', 'POST');

-- Confirm new mount type groups exist
SELECT code, name FROM option_groups
WHERE organization_id = 291 AND code IN ('MT_WALL', 'MT_CEIL', 'MT_POST');
```

---

## PHASE 3: Create Option Mapping Record

### Option A: Admin Console UI

1. Go to Admin Console → Products → Option Mappings → "New Option Mapping"
2. Select Option Type: **OptionSet2**
3. Add connections (4 total — 638 group references):
   - MT_WALL → OptionSet3: all WM### groups
   - MT_WALL → OptionSet4: all W###/WA### groups
   - MT_CEIL → OptionSet3: all CM### groups
   - MT_POST → OptionSet3: all PP### groups

(This is impractical via UI — use Option B)

### Option B: SQL INSERT (for Support to run)

```sql
INSERT INTO option_mappings (organization_id, option_type_code, mapping, created_at, updated_at)
VALUES (
  291,
  'OptionSet2',
  '{"MT_WALL":{"OptionSet3":["WM001","WM002","WM003","WM004","WM005","WM006","WM007","WM008","WM009","WM010","WM011","WM012","WM013","WM014","WM015","WM016","WM017","WM018","WM019","WM020","WM021","WM022","WM023","WM024","WM025","WM026","WM027","WM028","WM029","WM030","WM031","WM032","WM033","WM034","WM035","WM036","WM037","WM038","WM039","WM040","WM041","WM042","WM043","WM044","WM045","WM046","WM047","WM048","WM049","WM050","WM051","WM052","WM053","WM054","WM055","WM056","WM057","WM058","WM059","WM060","WM061","WM062","WM063","WM064","WM065","WM066","WM067","WM068","WM069","WM076","WM077","WM078","WM079","WM080","WM081","WM082","WM083","WM084","WM085","WM086","WM087","WM088","WM089","WM090","WM091","WM092","WM093","WM094","WM095","WM096","WM097","WM098","WM099","WM100","WM101","WM102","WM103","WM104","WM105","WM106","WM107","WM108","WM109","WM110","WM111","WM112","WM113","WM114","WM115","WM116","WM117","WM118","WM119","WM120","WM121","WM122","WM123","WM124","WM125","WM126","WM127","WM128","WM129","WM130","WM131","WM132","WM133","WM134","WM135","WM136","WM137","WM138","WM139","WM140","WM141","WM142","WM143","WM144","WM145","WM146","WM147","WM148","WM149","WM150","WM151","WM152","WM153","WM154","WM155","WM156","WM157","WM158","WM159","WM160","WM161","WM162","WM163","WM164"],"OptionSet4":["W028","W029","W030","W031","W032","W033","W034","W035","W039","W040","W041","W042","W043","W044","W045","W046","W047","W048","W049","W050","W051","W052","W053","W054","W055","W056","W057","W058","W059","W060","W065","W066","W067","W068","W069","W076","W077","W078","W079","W080","W081","W082","W083","W090","W091","W092","W093","W094","W095","W096","W097","W098","W099","W100","W101","W102","W103","W104","W106","W107","W108","W109","W110","W111","W112","W113","W114","W115","W116","W117","W118","W119","W120","W121","W122","W123","W124","W125","W126","W127","W134","W135","W136","W137","W138","W139","W146","W147","W148","W149","W150","W151","W152","W153","W154","W155","W156","WA001","WA002","WA003","WA004","WA005","WA006","WA007","WA008","WA009","WA010","WA011","WA012","WA013","WA014","WA015","WA016","WA017","WA018","WA019","WA020","WA021","WA022","WA023","WA024","WA025","WA029","WA030","WA031","WA032","WA033","WA034","WA035","WA036","WA037","WA038","WA039","WA040","WA041","WA042","WA043","WA044","WA047","WA048","WA049","WA050","WA051","WA052","WA053","WA054","WA055","WA056","WA057","WA058","WA059","WA060","WA061","WA062","WA_HL30"]},"MT_CEIL":{"OptionSet3":["CM001","CM002","CM003","CM004","CM005","CM006","CM007","CM008","CM009","CM010","CM011","CM012","CM013","CM014","CM015","CM016","CM017","CM018","CM019","CM020","CM021","CM022","CM023","CM024","CM025","CM026","CM027","CM028","CM029","CM030","CM031","CM032","CM033","CM034","CM035","CM036","CM037","CM038","CM039","CM040","CM041","CM042","CM043","CM044","CM045","CM046","CM047","CM048","CM049","CM050","CM051","CM052","CM053","CM054","CM055","CM056","CM057","CM058","CM059","CM060","CM061","CM062","CM063","CM064","CM065","CM066","CM067","CM068","CM069","CM070","CM071","CM072","CM073","CM074","CM075","CM076","CM077","CM078","CM079","CM080","CM081","CM082","CM083","CM084","CM085","CM086","CM087","CM088","CM089","CM090","CM091","CM092","CM093","CM094","CM095","CM096","CM097","CM098","CM099","CM100","CM101","CM102","CM103","CM104","CM105","CM106","CM107","CM108","CM109","CM110","CM111","CM112","CM113","CM114","CM115","CM116","CM117","CM118","CM119","CM120","CM121","CM122","CM123","CM124","CM125","CM126","CM127","CM128","CM129","CM130","CM131","CM132","CM133","CM134","CM135","CM136","CM137","CM138","CM139","CM140","CM141","CM142","CM143","CM144","CM145","CM146","CM147","CM148","CM149","CM150","CM151","CM152","CM153","CM154","CM155","CM156","CM157","CM158","CM159","CM160","CM161","CM162","CM163","CM164"],"OptionSet4":[]},"MT_POST":{"OptionSet3":["PP001","PP002","PP003","PP004","PP005","PP006","PP007","PP008","PP009","PP010","PP011","PP012","PP013","PP014","PP015","PP016","PP017","PP018","PP019","PP020","PP021","PP022","PP023","PP024","PP025","PP026","PP027","PP028","PP029","PP030","PP031","PP032","PP033","PP034","PP035","PP036","PP037","PP038","PP039","PP040","PP041","PP042","PP043","PP044","PP045","PP046","PP047","PP048","PP049","PP050","PP051","PP052","PP053","PP054","PP055","PP056","PP057","PP058","PP059","PP060","PP061","PP062","PP063","PP064","PP065","PP066","PP067","PP068","PP069","PP076","PP077","PP078","PP079","PP080","PP081","PP082","PP083","PP084","PP085","PP086","PP087","PP088","PP089","PP090","PP091","PP092","PP093","PP094","PP095","PP096","PP097","PP098","PP099","PP100","PP101","PP102","PP103","PP104","PP105","PP106","PP107","PP108","PP109","PP110","PP111","PP112","PP113","PP114","PP115","PP116","PP117","PP118","PP119","PP120","PP121","PP122","PP123","PP124","PP125","PP126","PP127","PP128","PP129","PP130","PP131","PP132","PP133","PP134","PP135","PP136","PP137","PP138","PP139","PP146","PP147","PP148","PP149","PP150","PP151","PP152","PP153","PP154","PP155","PP156","PP157","PP158","PP159","PP160","PP161","PP162","PP163","PP164"],"OptionSet4":[]}}',
  NOW(),
  NOW()
);
```

### Verify:

```sql
SELECT id, option_type_code, jsonb_object_keys(mapping) as trigger_groups
FROM option_mappings WHERE organization_id = 291;
```

---

## PHASE 4: Update Order Item Number Construction

### Current JS (backup):

```javascript
// The CopperSmith (org: tcs) — Smart SKU builder
// Build order: Base + Finish + Mount + Decorative + Electric/Gas
// OptionSet1=Finish  OptionSet2=Mount  OptionSet3=Decorative  OptionSet4=Electric/Gas
// Default finish (Antique Copper = COPPER) emits no suffix. AOB families have no finish set.
function main(orderItem) {
  var DEFAULT_FINISH = "COPPER";
  function setIndex(o) {
    var m = /(\d+)$/.exec(o.optionTypeCode || "");
    return m ? parseInt(m[1], 10) : 999;
  }
  var opts = (orderItem.options || []).slice().sort(function(a, b) {
    return setIndex(a) - setIndex(b);
  });
  var suffixes = [];
  for (var i = 0; i < opts.length; i++) {
    var code = opts[i].code;
    if (!code) continue;
    if (code === DEFAULT_FINISH) continue;
    suffixes.push(code);
  }
  return [orderItem.itemNumber].concat(suffixes).join("-");
}
```

### New JS (to replace it):

```javascript
// The CopperSmith (org: tcs) — Smart SKU builder v2 (Option Mapping)
// OS1=Finish  OS2=Mount Type (routing only)  OS3=Mount Hardware
// OS4=Wall Accessories  OS5=Decorative  OS6=Electric  OS7=Gas
// Default finish (Antique Copper = COPPER) emits no suffix.
// Mount Type codes (WALL/CEIL/POST) are routing selectors, excluded from SKU.
function main(orderItem) {
  var DEFAULT_FINISH = "COPPER";
  var SKIP_CODES = {"WALL": true, "CEIL": true, "POST": true};
  function setIndex(o) {
    var m = /(\d+)$/.exec(o.optionTypeCode || "");
    return m ? parseInt(m[1], 10) : 999;
  }
  var opts = (orderItem.options || []).slice().sort(function(a, b) {
    return setIndex(a) - setIndex(b);
  });
  var suffixes = [];
  for (var i = 0; i < opts.length; i++) {
    var code = opts[i].code;
    if (!code) continue;
    if (code === DEFAULT_FINISH) continue;
    if (SKIP_CODES[code]) continue;
    suffixes.push(code);
  }
  return [orderItem.itemNumber].concat(suffixes).join("-");
}
```

### How to apply:

**Option A:** Admin Console → org edit (super_user only) → "Order Item Number Construction" field → paste the new JS → Save

**Option B:** SQL (for Support):

```sql
UPDATE organizations
SET properties = jsonb_set(
  properties,
  '{configured_item_number_builder}',
  '"// The CopperSmith (org: tcs) — Smart SKU builder v2 (Option Mapping)\n// OS1=Finish  OS2=Mount Type (routing only)  OS3=Mount Hardware\n// OS4=Wall Accessories  OS5=Decorative  OS6=Electric  OS7=Gas\n// Default finish (Antique Copper = COPPER) emits no suffix.\n// Mount Type codes (WALL/CEIL/POST) are routing selectors, excluded from SKU.\nfunction main(orderItem) {\n  var DEFAULT_FINISH = \"COPPER\";\n  var SKIP_CODES = {\"WALL\": true, \"CEIL\": true, \"POST\": true};\n  function setIndex(o) {\n    var m = /(\\d+)$/.exec(o.optionTypeCode || \"\");\n    return m ? parseInt(m[1], 10) : 999;\n  }\n  var opts = (orderItem.options || []).slice().sort(function(a, b) {\n    return setIndex(a) - setIndex(b);\n  });\n  var suffixes = [];\n  for (var i = 0; i < opts.length; i++) {\n    var code = opts[i].code;\n    if (!code) continue;\n    if (code === DEFAULT_FINISH) continue;\n    if (SKIP_CODES[code]) continue;\n    suffixes.push(code);\n  }\n  return [orderItem.itemNumber].concat(suffixes).join(\"-\");\n}\n"'
)
WHERE id = 291;
```

### Verify:

```sql
SELECT properties->>'configured_item_number_builder' FROM organizations WHERE id = 291;
```

---

## PHASE 5: Upload Mount Type Option Images

1. Create 3 images (300x300px, square, `.jpg`):
   - `WALL.jpg` — Wall mount icon/photo
   - `CEIL.jpg` — Ceiling mount icon/photo
   - `POST.jpg` — Post mount icon/photo

2. Upload to FTP `/option_images/`

3. Admin Console → Tools → Import Images → Option Photo

### Verify:

```sql
SELECT code, name, image_name FROM options
WHERE organization_id = 291 AND code IN ('WALL', 'CEIL', 'POST');
```

---

## PHASE 6: iPad Verification Checklist

After a full sync completes:

- [ ] **AS41E** (all 3 mount types):
  - OS2 shows Wall Mount, Ceiling Mount, Post & Pier Mount
  - Select Wall → OS3 shows wall brackets, OS4 shows scrolls/hooks
  - Select Ceiling → OS3 shows yokes/chains, OS4 hidden
  - Select Post → OS3 shows fitters/posts, OS4 hidden
- [ ] **AC15W** (flush mount, no mounts):
  - Only OS1 (Finish) and OS5 (Decorative) visible
  - No mount type selector
- [ ] **EB27E** (ceiling-only + decorative scrolls):
  - OS2 shows only Ceiling Mount
  - OS5 (Decorative) shows Top Scroll group
  - OS4 is hidden
- [ ] **SKU Construction** (add AS41E to cart):
  - Select BLK finish + WY wall yoke + TS3 top scroll
  - Item number displays: `AS41E-BLK-WY-TS3` (no "WALL" in SKU)
- [ ] **Default copper** (add AS41E with no finish change):
  - Item number displays: `AS41E-WY` (no "COPPER" suffix)

---

## Rollback (if needed)

```sql
-- Revert labels
UPDATE organizations
SET option_type_labels = '---
- Finish (Required)
- Wall Mount
- Wall Mount Accessories
- Ceiling Mount
- Post & Pier Mount
- Decorative
- Electric
- Gas
'
WHERE id = 291;

-- Delete option mapping
DELETE FROM option_mappings WHERE organization_id = 291 AND option_type_code = 'OptionSet2';

-- Revert item number builder
UPDATE organizations
SET properties = jsonb_set(
  properties,
  '{configured_item_number_builder}',
  '"// The CopperSmith (org: tcs) — Smart SKU builder\n// Build order: Base + Finish + Mount + Decorative + Electric/Gas\n// OptionSet1=Finish  OptionSet2=Mount  OptionSet3=Decorative  OptionSet4=Electric/Gas\n// Default finish (Antique Copper = COPPER) emits no suffix. AOB families have no finish set.\nfunction main(orderItem) {\n  var DEFAULT_FINISH = \"COPPER\";\n  function setIndex(o) {\n    var m = /(\\d+)$/.exec(o.optionTypeCode || \"\");\n    return m ? parseInt(m[1], 10) : 999;\n  }\n  var opts = (orderItem.options || []).slice().sort(function(a, b) {\n    return setIndex(a) - setIndex(b);\n  });\n  var suffixes = [];\n  for (var i = 0; i < opts.length; i++) {\n    var code = opts[i].code;\n    if (!code) continue;\n    if (code === DEFAULT_FINISH) continue;\n    suffixes.push(code);\n  }\n  return [orderItem.itemNumber].concat(suffixes).join(\"-\");\n}\n"'
)
WHERE id = 291;
```

Then re-upload original files from `CS_eCat_Rebuild/`:
1. `options.csv`
2. `option_groups.csv`
3. `products.csv`

---

## Post-Deploy Monitoring

After go-live, run these queries periodically:

```sql
-- Confirm mapping is intact
SELECT id, option_type_code,
  jsonb_array_length(mapping->'MT_WALL'->'OptionSet3') as wall_mount_groups,
  jsonb_array_length(mapping->'MT_WALL'->'OptionSet4') as wall_acc_groups,
  jsonb_array_length(mapping->'MT_CEIL'->'OptionSet3') as ceil_mount_groups,
  jsonb_array_length(mapping->'MT_POST'->'OptionSet3') as post_mount_groups
FROM option_mappings WHERE organization_id = 291;

-- Check for any import errors since deployment
SELECT created_at, filename, status, error_count, warning_count
FROM import_events
WHERE organization_id = 291
ORDER BY created_at DESC LIMIT 10;
```
