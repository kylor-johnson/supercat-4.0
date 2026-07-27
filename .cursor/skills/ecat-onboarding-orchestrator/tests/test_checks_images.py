"""Tests for the three image checks: image_urls, images_live, blanks.

Each covers a delivery path the others cannot see, and the corpus has one expensive
failure per path:

* **image_urls** — 23 PNG URLs across 54 rows, live for eight weeks. PNG fails both
  CdnImageSync gates and logs at `:error`, which also suppresses every delete in the
  same import.
* **images_live** — 9 of Lib & Co's 832 products had no uploaded primary image, and eOL
  suppresses imageless products from search. The catalog was off the portal while the
  iPad looked fine.
* **blanks** — the client's standing rule is to leave a SKU blank rather than borrow a
  sibling's image. This is the only image check that asserts against the client's own
  file rather than our transform.

The network is never touched here: classification is by pattern, and the HEAD path is
exercised with a stubbed request.
"""
import json

import pytest

from preflight.checks import blanks, image_urls, images_live
from preflight.core import FAIL, WARNING

CDN = "https://cdn.example.com"


# --- URL census -----------------------------------------------------------------


def test_png_url_is_reported_with_both_gates_it_fails(rows_from, severities):
    rows, lookup = rows_from(
        f"BaseItemCode,ImageFileName\nCO18G,{CDN}/co18g.png\n")
    by = severities(image_urls.run(rows, lookup))
    assert FAIL in by
    message = next(m for m in by[FAIL] if "co18g.png" in m)
    assert "[png]" in message
    assert "BOTH CdnImageSync gates" in message
    # The second-order consequence is the part nobody knew.
    assert "suppresses every delete in the same import" in message
    assert "CO18G" in message  # which SKU to go fix


def test_share_link_can_never_resolve(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\n"
        "A-1,https://drive.google.com/file/d/abc/view\n")
    by = severities(image_urls.run(rows, lookup))
    assert any("[share-link]" in m and "HTML page" in m for m in by[FAIL])


@pytest.mark.parametrize("url", [
    "https://www.dropbox.com/s/abc/a.jpg",
    "https://docs.google.com/uc?id=abc",
    "https://mycompany.sharepoint.com/x/a.jpg",
])
def test_share_link_hosts(url, rows_from, severities):
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{url}\n")
    by = severities(image_urls.run(rows, lookup))
    assert FAIL in by


def test_non_http_scheme_is_not_fetchable(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,ftp://host/a.jpg\n")
    by = severities(image_urls.run(rows, lookup))
    assert any("[non-http]" in m for m in by[FAIL])


def test_jpg_url_is_unconfirmed_rather_than_passed_without_network(rows_from, severities):
    """A plausible pattern is not proof. Say what was not checked."""
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    by = severities(image_urls.run(rows, lookup))
    assert FAIL not in by
    assert "unchecked=1" in by[WARNING][0]
    assert "pass --check-urls" in by[WARNING][0]


def test_census_counts_are_deduplicated_by_url(rows_from, severities):
    """Two SKUs on one bad URL is one URL to fix, not two."""
    rows, lookup = rows_from(
        f"BaseItemCode,ImageFileName\nA-1,{CDN}/x.png\nA-2,{CDN}/x.png\n")
    by = severities(image_urls.run(rows, lookup))
    assert "over 1 distinct URL(s)" in by[WARNING][0]
    assert len([m for m in by[FAIL] if "x.png" in m]) == 1


def test_cache_reminder_is_emitted_for_fetchable_urls(rows_from, severities):
    """Replacing bytes at the same URL changes nothing until a re-import."""
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    by = severities(image_urls.run(rows, lookup))
    assert any("versioned filename (-v2)" in m for m in by[WARNING])


def test_no_urls_reports_the_undocumented_capability(rows_from, severities):
    """Nobody at SuperCat knew ImageFileName takes a URL until five weeks in."""
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nA-1,a.jpg\n")
    by = severities(image_urls.run(rows, lookup))
    assert FAIL not in by
    assert "also accepts a full HTTPS URL" in by[WARNING][0]


def test_head_confirms_content_type(monkeypatch, rows_from, severities):
    """A .jpg URL serving image/png still fails: the Content-Type gate is separate."""
    monkeypatch.setattr(image_urls, "head",
                        lambda url, timeout=10: (200, "image/png", None))
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    by = severities(image_urls.run(rows, lookup, check_network=True))
    assert any("[wrong-type]" in m and "image/png" in m for m in by[FAIL])


def test_head_catches_a_dead_link(monkeypatch, rows_from, severities):
    monkeypatch.setattr(image_urls, "head",
                        lambda url, timeout=10: (404, None, "HTTP 404"))
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/gone.jpg\n")
    by = severities(image_urls.run(rows, lookup, check_network=True))
    assert any("[dead]" in m and "points at nothing" in m for m in by[FAIL])


def test_head_success_is_a_pass(monkeypatch, rows_from, severities):
    monkeypatch.setattr(image_urls, "head",
                        lambda url, timeout=10: (200, "image/jpeg", None))
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    by = severities(image_urls.run(rows, lookup, check_network=True))
    assert FAIL not in by
    assert "jpg-ok=1" in by[WARNING][0]


def test_head_is_not_spent_on_urls_that_already_failed_a_gate(monkeypatch, rows_from):
    """A PNG is already disqualified by pattern; probing it would be a wasted request."""
    calls = []

    def _head(url, timeout=10):
        calls.append(url)
        return 200, "image/jpeg", None

    monkeypatch.setattr(image_urls, "head", _head)
    rows, lookup = rows_from(
        f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.png\nA-2,{CDN}/b.jpg\n")
    image_urls.run(rows, lookup, check_network=True)
    assert calls == [f"{CDN}/b.jpg"]


def test_cache_makes_a_rerun_free(monkeypatch, rows_from, tmp_path):
    cache = tmp_path / "urls.json"
    calls = []

    def _head(url, timeout=10):
        calls.append(url)
        return 200, "image/jpeg", None

    monkeypatch.setattr(image_urls, "head", _head)
    rows, lookup = rows_from(f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    image_urls.run(rows, lookup, check_network=True, cache_path=str(cache))
    assert len(calls) == 1
    assert json.loads(cache.read_text())[f"{CDN}/a.jpg"][0] == "jpg-ok"
    image_urls.run(rows, lookup, check_network=True, cache_path=str(cache))
    assert len(calls) == 1  # served from cache


def test_local_filenames_are_not_treated_as_urls(rows_from):
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nA-1,\"a.jpg,a-1.jpg\"\n")
    assert image_urls.extract_urls(rows, lookup) == {}


# --- primary-image set diff -----------------------------------------------------


def test_missing_primary_blocks_and_explains_the_portal_symptom(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName,Hideable\nLC-1,lc-1.jpg,N\n")
    by = severities(images_live.run(rows, lookup, live_images=["other.jpg"]))
    assert FAIL in by
    assert "image_exists=false" in by[FAIL][0]
    assert "eOL will suppress it from search" in by[FAIL][0]
    assert "browses fine on the iPad" in by[FAIL][0]


def test_an_uploaded_alternate_does_not_satisfy_image_exists(rows_from, severities):
    """Only the FIRST filename counts — the single most confusing bug shape in the corpus."""
    rows, lookup = rows_from(
        'BaseItemCode,ImageFileName\nLC-1,"lc-1.jpg,lc-1-alt.jpg"\n')
    by = severities(images_live.run(rows, lookup, live_images=["lc-1-alt.jpg"]))
    assert FAIL in by
    assert "an ALTERNATE for this SKU IS uploaded" in by[FAIL][0]
    assert "only the first filename counts" in by[FAIL][0]


def test_case_mismatch_counts_as_missing(rows_from, severities):
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nLC-1,LC-1.jpg\n")
    by = severities(images_live.run(rows, lookup, live_images=["lc-1.jpg"]))
    assert FAIL in by
    assert "by case only" in by[FAIL][0]
    assert "case-sensitive" in by[FAIL][0]


def test_missing_alternate_only_warns(rows_from, severities):
    rows, lookup = rows_from(
        'BaseItemCode,ImageFileName\nLC-1,"lc-1.jpg,lc-1-alt.jpg"\n')
    by = severities(images_live.run(rows, lookup, live_images=["lc-1.jpg"]))
    assert FAIL not in by
    assert any("does not affect image_exists" in m for m in by[WARNING])


def test_all_primaries_present_reports_the_ratio(rows_from, severities):
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nLC-1,lc-1.jpg\nLC-2,lc-2.jpg\n")
    by = severities(images_live.run(
        rows, lookup, live_images=["lc-1.jpg", "lc-2.jpg", "spare.jpg"]))
    assert FAIL not in by
    assert "2/2 products have their PRIMARY image uploaded" in by[WARNING][0]
    assert "3 filenames live" in by[WARNING][0]


def test_absent_live_list_says_local_disk_is_not_authoritative(rows_from, severities):
    """mali had 691 images live against 17 staged locally — a clean local audit proves little."""
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nLC-1,lc-1.jpg\n")
    by = severities(images_live.run(rows, lookup, live_images=None))
    assert FAIL not in by
    assert "local disk is not" in by[WARNING][0]


def test_url_only_catalog_is_redirected_to_the_census(rows_from, severities):
    rows, lookup = rows_from(
        f"BaseItemCode,ImageFileName\nA-1,{CDN}/a.jpg\n")
    by = severities(images_live.run(rows, lookup, live_images=[]))
    assert FAIL not in by
    assert "Use the image URL census instead" in by[WARNING][0]


def test_hidden_product_missing_its_image_is_less_urgent(rows_from, severities):
    """Still a FAIL, but it does not claim a portal outage that cannot happen."""
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName,Hideable\nLC-1,lc-1.jpg,Y\n")
    by = severities(images_live.run(rows, lookup, live_images=[]))
    assert FAIL in by
    assert "eOL will suppress" not in by[FAIL][0]


# --- blank-stays-blank ----------------------------------------------------------


def test_inventing_an_image_for_a_blank_source_sku_blocks(rows_from, severities,
                                                          tmp_path):
    source = tmp_path / "client_export.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n",
                      encoding="utf-8")
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,a-1.jpg\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert FAIL in by
    assert any("blank at source" in m and "A-2" in m for m in by[FAIL])
    assert any("rather than borrow a similar SKU's image" in m for m in by[FAIL])


def test_sibling_inheritance_is_caught_as_a_shared_filename(rows_from, severities,
                                                            tmp_path):
    source = tmp_path / "src.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,a-2.jpg\n",
                      encoding="utf-8")
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,a-1.jpg\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert any("sibling-image inheritance" in m for m in by[FAIL])


def test_a_genuinely_shared_hero_is_allowed_when_the_source_shares_it(rows_from,
                                                                     severities,
                                                                     tmp_path):
    source = tmp_path / "src.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,hero.jpg\nA-2,hero.jpg\n",
                      encoding="utf-8")
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,hero.jpg\nA-2,hero.jpg\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert FAIL not in by


def test_matching_the_source_exactly_is_stated_positively(rows_from, severities,
                                                          tmp_path):
    source = tmp_path / "src.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n",
                      encoding="utf-8")
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert FAIL not in by
    assert "match the source's blank/non-blank pattern" in by[WARNING][0]


def test_dropping_an_image_the_source_has_warns(rows_from, severities, tmp_path):
    source = tmp_path / "src.csv"
    source.write_text("BaseItemCode,ImageFileName\nA-1,a-1.jpg\n", encoding="utf-8")
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nA-1,\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert FAIL not in by
    assert any("image at source but none in the output" in m for m in by[WARNING])


def test_without_a_source_it_can_only_warn(rows_from, severities):
    """A shared hero is legitimate when the source shares it — so this cannot block."""
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,hero.jpg\nA-2,hero.jpg\n")
    by = severities(blanks.run(rows, lookup, source_path=None))
    assert FAIL not in by
    assert "no --source supplied" in by[WARNING][0]
    assert any("shared by 2 SKUs" in m for m in by[WARNING])


def test_differently_named_source_columns_can_be_mapped(rows_from, severities,
                                                        tmp_path):
    """A client export calls them SKU and Image, not BaseItemCode and ImageFileName."""
    source = tmp_path / "src.csv"
    source.write_text("SKU,Image\nA-1,a-1.jpg\nA-2,\n", encoding="utf-8")
    rows, lookup = rows_from(
        "BaseItemCode,ImageFileName\nA-1,a-1.jpg\nA-2,a-1.jpg\n")
    by = severities(blanks.run(rows, lookup, str(source),
                               source_key_field="SKU", source_image_field="Image"))
    assert any("blank at source" in m for m in by[FAIL])


def test_unmappable_source_says_which_flag_to_pass(rows_from, severities, tmp_path):
    source = tmp_path / "src.csv"
    source.write_text("SKU,Image\nA-1,a-1.jpg\n", encoding="utf-8")
    rows, lookup = rows_from("BaseItemCode,ImageFileName\nA-1,a-1.jpg\n")
    by = severities(blanks.run(rows, lookup, str(source)))
    assert FAIL not in by
    assert "--source-key" in by[WARNING][0]
