# Lib & Co — class-2 validation of the client's pre-mapped file

Produced BLIND, from the source alone (see `BLIND_BOUNDARY.md`).

The job on a class-2 file is **checking** the human's mapping, not redoing
it. Nothing here changes a value; every finding is a measurement with a
specimen, and consequences that depend on Admin config are marked `IF`.

```
==========================================================================
CLASS-2 VALIDATION — LIB_Co_Upload_Fixed_Prices.xlsx
==========================================================================
input class: hybrid — validate the eCat half, map the client half
  LIB_Co_Upload_Fixed_Prices.xlsx
  62 headers, 62 named, 0 BLANK
  20 of 62 named headers are eCat fields for products.csv (32.3%)
  client-domain columns (42): Subcategory, Feature1, Feature2, Feature3, Feature4, Feature5, MaxHeight, MinHeight, ChainLength, WireLength, ExtensionRods, BackplateDimension ...

findings: 29 BLOCKING, 43 NOTE

[BLOCKING] boolean shape          'Dimmable' is binary (No/Yes) but carries Yes/No. eCat boolean filters match only Y/y/T/t and digits 1-9, so IF this field is registered as an iPad filter the chip cannot match. 870 values.
             specimen: Yes = 'Yes'
[BLOCKING] boolean shape          'ADA' is binary (Yes) but carries Yes/No. eCat boolean filters match only Y/y/T/t and digits 1-9, so IF this field is registered as an iPad filter the chip cannot match. 20 values.
             specimen: Yes = 'Yes'
[BLOCKING] boolean shape          'BulbIncluded' is binary (NO/No/Yes) but carries Yes/No. eCat boolean filters match only Y/y/T/t and digits 1-9, so IF this field is registered as an iPad filter the chip cannot match. 559 values.
             specimen: Yes = 'Yes'
[BLOCKING] boolean shape          'SlopeCeilingCompatible' is binary (No/Yes) but carries Yes/No. eCat boolean filters match only Y/y/T/t and digits 1-9, so IF this field is registered as an iPad filter the chip cannot match. 779 values.
             specimen: Yes = 'Yes'
[BLOCKING] boolean shape          'MotionSensor' is binary (No/Yes) but carries Yes/No. eCat boolean filters match only Y/y/T/t and digits 1-9, so IF this field is registered as an iPad filter the chip cannot match. 152 values.
             specimen: No = 'No'
[BLOCKING] case-duplicate value   'Feature4' has 1 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'Adjustable Color Temperature for LED light sourcing' vs 'adjustable Color Temperature for LED light sourcing'
[BLOCKING] case-duplicate value   'FinishCode' has 15 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'Aged Brass' vs 'Aged brass'
[BLOCKING] case-duplicate value   'ShadeMaterial' has 1 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'Natural Alabaster' vs 'Natural alabaster'
[BLOCKING] case-duplicate value   'ShadeColor' has 1 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'Clear & White' vs 'Clear & white'
[BLOCKING] case-duplicate value   'BulbIncluded' has 1 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'NO' vs 'No'
[BLOCKING] case-duplicate value   'Materials' has 1 value(s) differing only by case. Each spelling ships as its own filter facet.
             specimen: 'Aluminum and Acrylic' vs 'Aluminum and acrylic'
[BLOCKING] datetime not date      'IntroDate' carries a datetime on 853/897 values where eCat wants YYYY-MM-DD.
             specimen: 2024-01-01 00:00:00
[BLOCKING] declared but empty     'LongDesc' is present as a column and has NO value on any of the 897 rows. It is a built-in eCat field.
             specimen: (0 of 897 populated)
[BLOCKING] declared but empty     'PromotionPrice' is present as a column and has NO value on any of the 897 rows. It is a built-in eCat field.
             specimen: (0 of 897 populated)
[BLOCKING] float tail             'UPCValue' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 810117543631.0
[BLOCKING] float tail             'NumberOfShades' carries a spreadsheet float tail on 807 of 897 rows (807 populated). The importer takes the tail verbatim.
             specimen: 1.0
[BLOCKING] float tail             'ShipWeight' carries a spreadsheet float tail on 369 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 70.0
[BLOCKING] float tail             'NbrBulbs' carries a spreadsheet float tail on 809 of 897 rows (809 populated). The importer takes the tail verbatim.
             specimen: 1.0
[BLOCKING] float tail             'TotalLumen' carries a spreadsheet float tail on 825 of 897 rows (825 populated). The importer takes the tail verbatim.
             specimen: 500.0
[BLOCKING] float tail             'CRI' carries a spreadsheet float tail on 839 of 897 rows (839 populated). The importer takes the tail verbatim.
             specimen: 90.0
[BLOCKING] float tail             'IPRating' carries a spreadsheet float tail on 674 of 897 rows (674 populated). The importer takes the tail verbatim.
             specimen: 20.0
[BLOCKING] float tail             'LEDHours' carries a spreadsheet float tail on 824 of 897 rows (824 populated). The importer takes the tail verbatim.
             specimen: 20000.0
[BLOCKING] float tail             'Price_cad' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 204.0
[BLOCKING] float tail             'Price_imapcad' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 510.0
[BLOCKING] float tail             'netprice' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 194.0
[BLOCKING] float tail             'Price_imapusd' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 485.0
[BLOCKING] float tail             'PackedVolume' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 1.0
[BLOCKING] float tail             'PackQuantity' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 1.0
[BLOCKING] float tail             'MinimumQuantity' carries a spreadsheet float tail on 897 of 897 rows (897 populated). The importer takes the tail verbatim.
             specimen: 1.0
[NOTE    ] custom field           'BaseItemCode' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 10193-030
[NOTE    ] custom field           'Subcategory' is not a built-in eCat field. Declared for registration. Populated 672/897 (74.9%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Chandelier
[NOTE    ] custom field           'Feature1' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Encapsulated clouds emit a soft and shimmering cascade of li
[NOTE    ] custom field           'Feature2' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Choice of painted antique brass or matte black canopy with g
[NOTE    ] custom field           'Feature3' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Sleek and stylish design is perfect for any room, providing 
[NOTE    ] custom field           'Feature4' is not a built-in eCat field. Declared for registration. Populated 850/897 (94.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Adjustable to accommodate any space with easy height strain 
[NOTE    ] custom field           'Feature5' is not a built-in eCat field. Declared for registration. Populated 628/897 (70.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Integrated dimmable LED light source
[NOTE    ] custom field           'MaxHeight' is not a built-in eCat field. Declared for registration. Populated 779/897 (86.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 106.5"
[NOTE    ] custom field           'MinHeight' is not a built-in eCat field. Declared for registration. Populated 678/897 (75.6%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 12"
[NOTE    ] custom field           'ChainLength' is not a built-in eCat field. Declared for registration. Populated 27/897 (3.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 180“
[NOTE    ] custom field           'WireLength' is not a built-in eCat field. Declared for registration. Populated 692/897 (77.1%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 96"
[NOTE    ] custom field           'ExtensionRods' is not a built-in eCat field. Declared for registration. Populated 91/897 (10.1%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Illuminated extension tubes (12", 24" , 48") available. Up t
[NOTE    ] custom field           'BackplateDimension' is not a built-in eCat field. Declared for registration. Populated 159/897 (17.7%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 6.75" L x 5.5" W
[NOTE    ] custom field           'CanopyDimension' is not a built-in eCat field. Declared for registration. Populated 790/897 (88.1%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 2" H x 5.5" D
[NOTE    ] custom field           'FinishCode' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Antique Brass
[NOTE    ] custom field           'ShadeMaterial' is not a built-in eCat field. Declared for registration. Populated 859/897 (95.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Glass
[NOTE    ] custom field           'ShadeColor' is not a built-in eCat field. Declared for registration. Populated 846/897 (94.3%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: White
[NOTE    ] custom field           'NumberOfShades' is not a built-in eCat field. Declared for registration. Populated 807/897 (90.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 1.0
[NOTE    ] custom field           'ShadeDimension' is not a built-in eCat field. Declared for registration. Populated 785/897 (87.5%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 3.5" H x 6.25"
[NOTE    ] custom field           'ShipLBS' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 2.54 lbs.
[NOTE    ] custom field           'Disclaimer' is not a built-in eCat field. Declared for registration. Populated 463/897 (51.6%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Fixtures weighing 35 lbs. or more must be supported and inst
[NOTE    ] custom field           'BulbType' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: LED Integrated
[NOTE    ] custom field           'NbrBulbs' is not a built-in eCat field. Declared for registration. Populated 809/897 (90.2%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 1.0
[NOTE    ] custom field           'TotalWattage' is not a built-in eCat field. Declared for registration. Populated 711/897 (79.3%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 7.5W
[NOTE    ] custom field           'BulbWattage' is not a built-in eCat field. Declared for registration. Populated 421/897 (46.9%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 7W
[NOTE    ] custom field           'TotalLumen' is not a built-in eCat field. Declared for registration. Populated 825/897 (92.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 500.0
[NOTE    ] custom field           'Kelvin' is not a built-in eCat field. Declared for registration. Populated 825/897 (92.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 3000K
[NOTE    ] custom field           'CRI' is not a built-in eCat field. Declared for registration. Populated 839/897 (93.5%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 90.0
[NOTE    ] custom field           'Dimmable' is not a built-in eCat field. Declared for registration. Populated 870/897 (97.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Yes
[NOTE    ] custom field           'Voltage' is not a built-in eCat field. Declared for registration. Populated 896/897 (99.9%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 120-277V
[NOTE    ] custom field           'Certifications' is not a built-in eCat field. Declared for registration. Populated 897/897 (100.0%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: cETLus
[NOTE    ] custom field           'IPRating' is not a built-in eCat field. Declared for registration. Populated 674/897 (75.1%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 20.0
[NOTE    ] custom field           'Rating' is not a built-in eCat field. Declared for registration. Populated 895/897 (99.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Damp
[NOTE    ] custom field           'ADA' is not a built-in eCat field. Declared for registration. Populated 20/897 (2.2%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Yes
[NOTE    ] custom field           'LEDHours' is not a built-in eCat field. Declared for registration. Populated 824/897 (91.9%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 20000.0
[NOTE    ] custom field           'BulbShape' is not a built-in eCat field. Declared for registration. Populated 16/897 (1.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: B10
[NOTE    ] custom field           'BulbSocket' is not a built-in eCat field. Declared for registration. Populated 238/897 (26.5%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: E26
[NOTE    ] custom field           'BulbIncluded' is not a built-in eCat field. Declared for registration. Populated 559/897 (62.3%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Yes
[NOTE    ] custom field           'SlopeCeilingCompatible' is not a built-in eCat field. Declared for registration. Populated 779/897 (86.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Yes
[NOTE    ] custom field           'IntroDate' is not a built-in eCat field. Declared for registration. Populated 859/897 (95.8%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: 2024-01-01 00:00:00
[NOTE    ] custom field           'Direction' is not a built-in eCat field. Declared for registration. Populated 85/897 (9.5%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: Multi
[NOTE    ] custom field           'MotionSensor' is not a built-in eCat field. Declared for registration. Populated 152/897 (16.9%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: No
[NOTE    ] custom field           'Video' is not a built-in eCat field. Declared for registration. Populated 83/897 (9.3%). A column not registered in Admin is SILENTLY DROPPED on every import.
             specimen: https://drive.google.com/file/d/1HGyuPsn7l_VgL3lbw5ftl3XMLq0

Every count above ships a specimen. Consequences marked "IF ..." are
conditional and have NOT been verified against this org's Admin config.
```
