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
