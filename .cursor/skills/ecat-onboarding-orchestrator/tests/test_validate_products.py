"""Regression tests for validate_products.py.

Each assertion in test_dirty_file_flags_every_lessons_learned_case maps to a real
failure documented in LESSONS_LEARNED.md. Add a row + assertion here whenever a new
snowflake bites — that is how nuance gets locked in permanently.
"""


def test_clean_file_passes(run_script, fixtures):
    rc, out = run_script("validate_products.py", str(fixtures / "products_clean.csv"))
    assert rc == 0
    assert "PASS" in out


def test_clean_file_inventories_codes(run_script, fixtures):
    rc, out = run_script("validate_products.py", str(fixtures / "products_clean.csv"))
    # Collection/Category codes must be surfaced so they can be verified in Admin.
    assert "CollectionCodes" in out
    assert "CategoryCodes" in out
    assert "'SL'" in out
    assert "'DRVRS'" in out


def test_dirty_file_fails(run_script, fixtures):
    rc, out = run_script("validate_products.py", str(fixtures / "products_dirty.csv"))
    assert rc == 1
    assert "FAIL" in out


def test_dirty_file_flags_every_lessons_learned_case(run_script, fixtures):
    _, out = run_script("validate_products.py", str(fixtures / "products_dirty.csv"))
    assert "DUPLICATE BaseItemCode 'ML-001'" in out      # one row per BaseItemCode
    assert "blank LongDesc" in out                       # required field present-but-empty
    assert "blank CollectionCodes" in out                # required taxonomy field
    assert "invalid Hideable 'X'" in out                 # Hideable must be Y/N
    # Long BaseItemCode is detected but as an advisory WARNING, not a hard fail
    # (mali shipped live 21-char codes — verified against the production DB).
    assert "advisory" in out


def test_long_baseitemcode_is_warning_not_failure(run_script, write_csv):
    # 21-char code, everything else valid → PASS with a warning, exit 0.
    csv = write_csv(
        "BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes,Hideable\n"
        "LV-HS-PD20-24V-100-WW,Long but valid,ML,LL,LIGHT,N\n"
    )
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "WARNINGS" in out
    assert "PASS" in out


def test_missing_required_column_is_reported(run_script, write_csv):
    csv = write_csv("BaseItemCode,LongDesc\nML-9,Only two columns\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 1
    assert "MISSING REQUIRED COLUMNS" in out


def test_standard_taxonomy_note(run_script, fixtures):
    # Short codes (LL, LIGHT, SL) => Standard method messaging.
    _, out = run_script("validate_products.py", str(fixtures / "products_clean.csv"))
    assert "Standard taxonomy" in out


def test_auto_create_taxonomy_detected(run_script, write_csv):
    # A code containing a space => Auto-Create messaging, not the Standard pre-create note.
    csv = write_csv(
        "BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes,Hideable\n"
        "P-1,Lounge Chair,PB,HAVEN ALU.,SUNLOUNGER,N\n"
    )
    _, out = run_script("validate_products.py", str(csv))
    assert "Auto-Create taxonomy" in out
    assert "Standard taxonomy" not in out


def test_long_single_token_code_is_not_auto_create(run_script, write_csv):
    # mali ships "ACCESSORIES"/"STRING" (>5 chars, no spaces) yet is Standard.
    csv = write_csv(
        "BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes,Hideable\n"
        "ML-1,Strip Light,ML,LL,ACCESSORIES,N\n"
    )
    _, out = run_script("validate_products.py", str(csv))
    assert "Standard taxonomy" in out
    assert "Auto-Create" not in out


def test_absent_hideable_column_is_noted(run_script, write_csv):
    # Pebl-style file with no Hideable column must not imply "0 visible".
    csv = write_csv(
        "BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes\n"
        "P-1,Lounge Chair,PB,BISTRO,CHAIR\n"
    )
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "Hideable column ABSENT" in out


def test_headers_are_case_insensitive(run_script, write_csv):
    # The importer downcases headers; the validator must too.
    csv = write_csv(
        "baseitemcode,longdesc,tradenamecode,collectioncodes,categorycodes,hideable\n"
        "ML-1,Lower Header Lamp,ML,LL,LIGHT,N\n"
    )
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "PASS" in out


# --- Phase 1 additions ----------------------------------------------------------
# The checks below came in with the pre-import gate. They run inside this validator so
# an operator checking one file still gets them, without having to know the gate exists.


BASE_HEADER = ("BaseItemCode,LongDesc,TradeNameCode,CollectionCodes,CategoryCodes,"
               "Hideable\n")


def test_bom_is_caught_here_too(run_script, tmp_path):
    """Excel's "CSV UTF-8" is the default a client reaches for, so this recurs."""
    path = tmp_path / "products.csv"
    path.write_bytes(b"\xef\xbb\xbf" + (BASE_HEADER + "ML-1,Lamp,ML,LL,LIGHT,N\n")
                     .encode("utf-8"))
    rc, out = run_script("validate_products.py", str(path))
    assert rc == 1
    assert "UTF-8 BOM" in out
    assert "a column that IS present" in out


def test_long_desc_over_255_warns_and_says_it_truncates(run_script, write_csv):
    """255, not the 50 in ecat-core-files — and the row imports mangled rather than failing."""
    csv = write_csv(BASE_HEADER + f"ML-1,{'x' * 260},ML,LL,LIGHT,N\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "260>255" in out
    assert "TRUNCATES" in out


def test_length_findings_cite_the_ruby_attribute(run_script, write_csv):
    csv = write_csv(BASE_HEADER + f"ML-1,Lamp,ML,LL,LIGHT,N\nML-2,{'x' * 300},ML,LL,LIGHT,N\n")
    _, out = run_script("validate_products.py", str(csv))
    assert "Product::ATTR_LENGTHS[:long_description]" in out
    assert "supercat_server @" in out


def test_baseitemcode_over_40_blocks(run_script, write_csv):
    """The real limit is 40 and it IS enforced; mali's 21-char codes pass because 21 < 40."""
    csv = write_csv(BASE_HEADER + f"{'A' * 41},Lamp,ML,LL,LIGHT,N\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 1
    assert "41>40" in out


def test_duplicate_upc_warns_without_blocking(run_script, write_csv):
    """upc_value has no uniqueness constraint, so it imports — but it is usually a typo."""
    csv = write_csv(
        BASE_HEADER.rstrip("\n") + ",UPCValue\n"
        "ML-1,Lamp,ML,LL,LIGHT,N,0001\n"
        "ML-2,Sconce,ML,LL,LIGHT,N,0001\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "UPCValue '0001' repeats" in out


def test_unregistered_column_blocks_when_the_list_is_supplied(run_script, write_csv):
    """Legrand's live case: carton1_h / carton1_l / carton1_w are dropped silently."""
    csv = write_csv(
        BASE_HEADER.rstrip("\n") + ",carton1_h\nML-1,Lamp,ML,LL,LIGHT,N,10\n")
    rc, out = run_script("validate_products.py", str(csv), "--custom-fields", "Color")
    assert rc == 1
    assert "carton1_h is unknown" in out
    assert "DROP the data" in out


def test_registered_field_absent_from_the_file_only_warns(run_script, write_csv):
    csv = write_csv(BASE_HEADER + "ML-1,Lamp,ML,LL,LIGHT,N\n")
    rc, out = run_script("validate_products.py", str(csv),
                         "--custom-fields", "rohscompliant,Color,voltage")
    assert rc == 0
    assert "rohscompliant" in out
    assert "omitting it does NOT clear it" in out


def test_without_the_custom_field_list_it_says_what_it_could_not_check(run_script,
                                                                      write_csv):
    csv = write_csv(BASE_HEADER + "ML-1,Lamp,ML,LL,LIGHT,N\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "no --custom-fields list supplied" in out


def test_taxonomy_code_missing_from_admin_blocks(run_script, write_csv):
    csv = write_csv(BASE_HEADER + "ML-1,Lamp,ML,LL,GHOSTCAT,N\n")
    rc, out = run_script("validate_products.py", str(csv),
                         "--admin-taxonomy", "ML,LL", "--admin-groups", "MAIN")
    assert rc == 1
    assert "GHOSTCAT" in out
    assert "pre-create it" in out


def test_zero_admin_groups_blocks_because_groups_never_auto_create(run_script,
                                                                  write_csv):
    """The one taxonomy layer a product import cannot bootstrap — a real mali fatal."""
    csv = write_csv(BASE_HEADER + "ML-1,Lamp,ML,LL,LIGHT,N\n")
    rc, out = run_script("validate_products.py", str(csv),
                         "--admin-taxonomy", "ML,LL,LIGHT", "--admin-groups", "")
    assert rc == 1
    assert "never auto-create" in out


def test_dangling_related_item_warns(run_script, write_csv):
    csv = write_csv(
        BASE_HEADER.rstrip("\n") + ",RelatedItems\n"
        "ML-1,Lamp,ML,LL,LIGHT,N,\"ML-2,GHOST\"\n"
        "ML-2,Sconce,ML,LL,LIGHT,N,\n")
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "GHOST" in out
    assert "the product still imports" in out


def test_a_very_long_related_items_cell_is_fine(run_script, write_csv):
    """related_items is an unbounded text column: the 255 limit in the docs is fiction.

    A 207-SKU collection needs roughly 2,690 characters, and the claim that this makes
    related-by-collection impossible rests on a limit that does not exist.
    """
    codes = [f"ML-{i:03d}" for i in range(1, 208)]
    body = "".join(
        f"{code},Lamp,ML,LL,LIGHT,N,\"{','.join(c for c in codes if c != code)}\"\n"
        for code in codes[:2])
    rest = "".join(f"{code},Lamp,ML,LL,LIGHT,N,\n" for code in codes[2:])
    csv = write_csv(BASE_HEADER.rstrip("\n") + ",RelatedItems\n" + body + rest)
    rc, out = run_script("validate_products.py", str(csv))
    assert rc == 0
    assert "RelatedItems" not in out.split("WARNINGS")[0]
