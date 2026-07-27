# Pre-Import Baseline — tcs (org 291)

Captured **2026-06-25** after June source-truth sync, **before FTP upload**. Live org
still reflects the June 18 import — local CSVs are synced and validated.

## Local CSV status

```bash
python3 validate_source_truth.py   # VALIDATION PASSED
python3 verify_post_import.py --expect
```

753 changes logged in [SOURCE_SYNC_CHANGELOG.md](SOURCE_SYNC_CHANGELOG.md).
Field mapping for Jordan: [FIELD_MAPPING.md](FIELD_MAPPING.md).

## Live DB — products (images_json primary)

| SKU | Live (wrong) | Expected after import |
|-----|--------------|----------------------|
| VNG | CS-Double-Burner-2.jpg | VNG.png |
| VNG50FH | CS-Double-Burner-2.jpg | *(blank)* |
| GH1-GPF | CS_GH_12_11-4.jpg | GH1-GPF.png |
| GH2-GPF | CS_GH_17_11-4.jpg | GH2-GPF.png |
| HSI1 | HSI.jpg | HSI1.png |
| HSI2 | HSI.jpg | HSI2.png |
| CSHI | CHSI.jpg | *(gone — replaced by CHSI)* |
| LL-TUBE6 | *(blank)* | *(gone — replaced by LL-TUBE6A)* |
| LL-TUBE8 | *(blank)* | *(gone — replaced by LL-TUBE8A)* |
| BMHCHM | *(blank)* | BMDSM.jpg |
| SP36 | *(blank)* | SP.jpg |
| WY36 | *(blank)* | WY36.png |
| VR25E | VR25E.jpg | VR25E.png |
| VR25G | VR25G.jpg | VR25G.png |
| GLC | GLC.jpg | GLC.png |
| GN14 | GNP.jpg | GN14.png |
| GN17 | GNP.jpg | GN17.png |
| GTTL | GTTL.jpg | GTTL.jpg (CDN) |
| PM36 | PMG.jpg | PM36.png |
| SA14 | SA14.jpg | SA14.png |
| SA17 | SA17.jpg | SA17.png |

## Live DB — options (image_name)

| Code | Live (wrong) | Expected after import |
|------|--------------|----------------------|
| CSHI | CHSI.jpg | *(gone — CHSI)* |
| BMPM | BMDSM.jpg | *(blank)* |
| CHB | CHB.jpg | *(blank)* |
| CSP8 | CSP8.jpg | *(blank)* |
| FT | FT.jpg | *(blank)* |
| PFA | PFP.jpg | *(blank)* |
| HSI1 | HSI.jpg | HSI1.png |
| HSI2 | HSI.jpg | HSI2.png |
| HSCM | *(blank)* | HSCM.png |
| WY | *(blank)* | WY.png |
| PF1–PF7 | PFP.jpg | PF.png |
| BLK | Finishes_BLK_750px.jpg | Finishes_BLK.jpg (CDN) |

**Note:** `CHSI` product row exists in local CSV but not yet in live DB; live still has `CSHI`.

## Last catalog import events

| When | Type | Status |
|------|------|--------|
| 2026-06-18 05:07 | Images | thumbnail error (unrelated corrupt JPG) |
| 2026-06-18 04:26 | Products | warnings only (UPCValue) |
| 2026-06-18 04:23 | Option Groups | clean |
| 2026-06-18 04:18 | Options | clean |

No import events after source-truth sync — **FTP upload still required**.

## Your upload step

```bash
cd CS_OptionMapping_Rebuild
FTP_PASS='...' ./upload_image_fixes.sh
```

Then re-run the Postgres queries in [IMAGE_IMPORT_CHECKLIST.md](IMAGE_IMPORT_CHECKLIST.md)
or `python3 verify_post_import.py` for expected values. iPad spot-check after full sync.
