"""
SuperCat Customer Segmentation v4.0 — Master Build Script
Combines Postgres-pulled data with v3.2 CSV to produce enriched classification.
"""
import csv
import json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent

# === ORG ID → SHORTNAME MAPPING (from Postgres organizations table) ===
ORG_MAP = {
    246:'am', 272:'tam', 107:'ihw', 126:'big', 2:'sbmh', 121:'jcusa', 131:'hmjc',
    111:'ta', 164:'ih', 32:'pf', 162:'rf', 167:'vce', 1:'sarreid', 268:'ol',
    225:'fsf', 72:'cl', 243:'hf', 133:'blh', 65:'jc', 83:'cfg', 236:'yw',
    161:'cci', 55:'gh', 23:'ap', 223:'all', 141:'vcg', 114:'tla', 108:'fms',
    182:'sbl', 241:'fal', 10:'cf', 78:'hh', 99:'kkc', 249:'ihm', 165:'hfg',
    18:'ufi', 146:'kal', 239:'dccl', 269:'arl', 171:'bcf', 88:'sccon', 147:'vl',
    120:'fc', 69:'sc', 152:'el', 14:'bsc', 245:'ril', 8:'wwjc', 231:'gcl',
    266:'luc', 64:'clm', 70:'tl', 71:'hvl', 255:'wag', 76:'jyc', 68:'eli',
    248:'rw', 250:'bp', 166:'kll', 252:'mlg', 221:'mlc', 62:'da', 124:'ah',
    181:'wac', 224:'lss', 58:'swc', 90:'sca', 187:'gl', 40:'clc', 41:'shl',
    229:'khi', 49:'kl', 139:'lpf', 149:'clli', 185:'afx', 232:'eglo_can',
    176:'vic', 286:'prog', 138:'et2', 168:'eglo', 237:'df', 220:'dals',
    227:'gc', 127:'ali', 155:'ml', 137:'mli', 184:'mh', 273:'leg', 48:'mfc',
    230:'soi', 22:'asi', 89:'mpc', 12:'gsa', 19:'rac', 222:'bri', 51:'pw',
    20:'ssi', 140:'etl', 136:'mah', 97:'st', 26:'heb', 94:'kii', 160:'uhc',
    132:'sp', 244:'krb', 86:'tel', 235:'abol', 234:'ilc', 87:'scw'
}

SHORTNAME_TO_ID = {v: k for k, v in ORG_MAP.items()}

# === PRODUCT STATS (from Postgres) ===
PRODUCT_STATS = {
    246: {'count':528,'avg':12916.18,'min':2400,'max':57550},
    272: {'count':7252,'avg':2853.20,'min':6,'max':59997},
    107: {'count':3340,'avg':2087.64,'min':20,'max':9840},
    126: {'count':1839,'avg':2440.45,'min':90,'max':41089},
    2: {'count':679,'avg':4456.09,'min':1086,'max':15894},
    121: {'count':1235,'avg':1640.60,'min':83,'max':18475},
    131: {'count':2915,'avg':1567.52,'min':33,'max':10999},
    111: {'count':8638,'avg':935.82,'min':15,'max':28499},
    164: {'count':832,'avg':877.86,'min':5,'max':5551},
    32: {'count':1479,'avg':3642.18,'min':139,'max':18526},
    162: {'count':1637,'avg':1197.24,'min':75,'max':9485},
    167: {'count':2849,'avg':1741.34,'min':20,'max':31199},
    1: {'count':5540,'avg':798.05,'min':1,'max':5995},
    268: {'count':824,'avg':1059.67,'min':30,'max':6680},
    225: {'count':4752,'avg':608.58,'min':10,'max':2050},
    72: {'count':724,'avg':1425.54,'min':25,'max':9379},
    243: {'count':3323,'avg':940.23,'min':89,'max':9175},
    133: {'count':486,'avg':1900.68,'min':48,'max':15678},
    65: {'count':17816,'avg':763.95,'min':0.01,'max':64149},
    83: {'count':630,'avg':840.51,'min':10,'max':6640},
    236: {'count':4292,'avg':877.41,'min':34,'max':3332},
    161: {'count':6112,'avg':1573.49,'min':14,'max':28330},
    55: {'count':5998,'avg':883.12,'min':5,'max':13750},
    23: {'count':794,'avg':817.77,'min':35,'max':4995},
    223: {'count':713,'avg':596.90,'min':5,'max':3786},
    141: {'count':17354,'avg':779.83,'min':1,'max':23914},
    114: {'count':17691,'avg':631.16,'min':1.5,'max':16795},
    108: {'count':9975,'avg':182.19,'min':2.15,'max':1750},
    182: {'count':1,'avg':14.00,'min':14,'max':14},
    249: {'count':259,'avg':2673.69,'min':67,'max':26061},
    165: {'count':1052,'avg':2531.95,'min':5,'max':39375},
    18: {'count':0,'avg':0,'min':0,'max':0},  # no products in DB (portal-only)
    146: {'count':2480,'avg':892.81,'min':46,'max':17847},
    239: {'count':395,'avg':821.31,'min':70,'max':2495},
    269: {'count':196,'avg':829.71,'min':99,'max':3499},
    171: {'count':2965,'avg':631.82,'min':3,'max':5825},
    88: {'count':10149,'avg':841.96,'min':5,'max':13750},
    147: {'count':458,'avg':1598.14,'min':124,'max':12936},
    120: {'count':1905,'avg':566.99,'min':7.7,'max':4295},
    69: {'count':17510,'avg':966.66,'min':1,'max':26260},
    152: {'count':2204,'avg':604.04,'min':15,'max':15445},
    14: {'count':1910,'avg':569.52,'min':56,'max':3796},
    245: {'count':1357,'avg':1058.69,'min':18.7,'max':7418},
    8: {'count':3860,'avg':550.24,'min':9,'max':5495},
    231: {'count':130,'avg':573.29,'min':17,'max':9598},
    266: {'count':603,'avg':354.16,'min':109,'max':2284},
    64: {'count':1962,'avg':648.72,'min':7,'max':21997},
    70: {'count':4184,'avg':315.71,'min':1,'max':21086},
    71: {'count':4925,'avg':435.09,'min':2,'max':7230},
    255: {'count':48056,'avg':444.91,'min':40,'max':10059},
    76: {'count':989,'avg':361.67,'min':35,'max':1800},
    68: {'count':11208,'avg':415.36,'min':0.5,'max':13468},
    248: {'count':1732,'avg':235.37,'min':4,'max':1679},
    250: {'count':1125,'avg':387.47,'min':5,'max':9450},
    166: {'count':0,'avg':0,'min':0,'max':0},  # no products in DB for kll
    252: {'count':3876,'avg':302.59,'min':2,'max':11967},
    221: {'count':2091,'avg':229.96,'min':21,'max':1960},
    62: {'count':2244,'avg':153.34,'min':3,'max':1059},
    124: {'count':2493,'avg':221.31,'min':0.45,'max':3295},
    181: {'count':0,'avg':0,'min':0,'max':0},  # wac - no products matched
    224: {'count':360,'avg':650.73,'min':109,'max':2999},
    58: {'count':560,'avg':460.47,'min':50,'max':1630},
    90: {'count':3304,'avg':368.54,'min':69.5,'max':2070},
    187: {'count':3131,'avg':170.57,'min':9,'max':9900},
    40: {'count':1793,'avg':180.71,'min':7,'max':1149},
    41: {'count':4983,'avg':181.54,'min':1.19,'max':6723},
    229: {'count':716,'avg':162.36,'min':40,'max':903},
    49: {'count':4414,'avg':181.91,'min':0.75,'max':2807},
    139: {'count':2032,'avg':78.80,'min':1,'max':644},
    149: {'count':2970,'avg':114.83,'min':1,'max':2399},
    185: {'count':2425,'avg':142.15,'min':2,'max':964},
    232: {'count':1563,'avg':172.45,'min':1.65,'max':2035},
    176: {'count':0,'avg':0,'min':0,'max':0},  # vic - check later
    286: {'count':3238,'avg':114.74,'min':1.85,'max':1130},
    138: {'count':3059,'avg':204.29,'min':0.01,'max':3749},
    168: {'count':2165,'avg':139.05,'min':1.5,'max':1960},
    237: {'count':1198,'avg':96.18,'min':1.95,'max':599},
    220: {'count':1117,'avg':82.31,'min':0.32,'max':2577},
    227: {'count':5580,'avg':159.72,'min':0.45,'max':3852},
    127: {'count':1537,'avg':72.88,'min':5,'max':351},
    155: {'count':3202,'avg':75.15,'min':1,'max':540},
    137: {'count':11508,'avg':168.73,'min':0.01,'max':13174},
    184: {'count':0,'avg':0,'min':0,'max':0},  # mh - check
    48: {'count':0,'avg':0,'min':0,'max':0},  # mfc
    22: {'count':9312,'avg':39.85,'min':0.01,'max':3000},
    89: {'count':4916,'avg':33.16,'min':0.01,'max':488},
    12: {'count':5670,'avg':31.69,'min':0.75,'max':1500},
    19: {'count':630,'avg':49.59,'min':5.75,'max':525},
    222: {'count':883,'avg':13.77,'min':0.39,'max':199},
    51: {'count':1258,'avg':12.34,'min':1.25,'max':60},
    20: {'count':284,'avg':15.33,'min':0.5,'max':130},
    140: {'count':4624,'avg':11.52,'min':1,'max':174},
    136: {'count':3048,'avg':10.57,'min':0.5,'max':880},
    97: {'count':14171,'avg':10.67,'min':2,'max':65},
    26: {'count':32499,'avg':14.83,'min':0.01,'max':700},
    94: {'count':31071,'avg':8.28,'min':0.1,'max':12499},
    160: {'count':4372,'avg':7.26,'min':0.14,'max':213},
    132: {'count':5613,'avg':614.37,'min':4.99,'max':25499},
    244: {'count':0,'avg':0,'min':0,'max':0},  # krb - check
    87: {'count':6941,'avg':944.17,'min':5,'max':12059},
    241: {'count':0,'avg':0,'min':0,'max':0},  # fal placeholder
    99: {'count':766,'avg':14600.39,'min':2304,'max':135172},
    # Round 3 audit (2026-07-09): ORG_MAP had these shortnames but PRODUCT_STATS
    # never got entries — CSV product_count was blank after SHORTNAME_CORRECTIONS.
    273: {'count':1012,'avg':100.00,'min':100,'max':100},   # leg — placeholder $100 net_price
    230: {'count':1106,'avg':0,'min':0,'max':0},            # soi — catalog loaded, no net_price
    86: {'count':2253,'avg':2184.74,'min':140,'max':14010}, # tel
    234: {'count':336,'avg':1592.83,'min':393.78,'max':3675}, # ilc
    235: {'count':542,'avg':675.67,'min':138.78,'max':1491.40}, # abol
}

# === CUSTOMER STATS ===
CUSTOMER_STATS = {
    246: {'customers':92,'territories':13,'price_codes':1},
    272: {'customers':262,'territories':1,'price_codes':1},
    107: {'customers':6106,'territories':32,'price_codes':5},
    126: {'customers':301,'territories':14,'price_codes':1},
    2: {'customers':6548,'territories':26,'price_codes':4},
    121: {'customers':5123,'territories':29,'price_codes':6},
    131: {'customers':1689,'territories':25,'price_codes':1},
    111: {'customers':7306,'territories':27,'price_codes':4},
    164: {'customers':20162,'territories':34,'price_codes':5},
    32: {'customers':17387,'territories':82,'price_codes':15},
    162: {'customers':4803,'territories':39,'price_codes':4},
    167: {'customers':1752,'territories':24,'price_codes':24},
    1: {'customers':4780,'territories':82,'price_codes':6},
    268: {'customers':13364,'territories':2,'price_codes':4},
    225: {'customers':776,'territories':29,'price_codes':3},
    72: {'customers':2272,'territories':62,'price_codes':4},
    243: {'customers':12543,'territories':105,'price_codes':7},
    133: {'customers':8527,'territories':7,'price_codes':2},
    65: {'customers':34,'territories':7,'price_codes':1},
    83: {'customers':2557,'territories':25,'price_codes':3},
    236: {'customers':227,'territories':20,'price_codes':2},
    161: {'customers':39056,'territories':56,'price_codes':6},
    55: {'customers':12012,'territories':21,'price_codes':12},
    23: {'customers':4763,'territories':22,'price_codes':3},
    223: {'customers':673,'territories':27,'price_codes':5},
    141: {'customers':5170,'territories':100,'price_codes':16},
    114: {'customers':4418,'territories':112,'price_codes':23},
    108: {'customers':5299,'territories':153,'price_codes':42},
    182: {'customers':1326,'territories':67,'price_codes':4},
    249: {'customers':121,'territories':13,'price_codes':1},
    165: {'customers':9067,'territories':62,'price_codes':8},
    18: {'customers':14663,'territories':45,'price_codes':1},
    146: {'customers':2262,'territories':46,'price_codes':3},
    239: {'customers':377,'territories':7,'price_codes':2},
    269: {'customers':33,'territories':3,'price_codes':1},
    171: {'customers':2058,'territories':32,'price_codes':6},
    88: {'customers':5375,'territories':18,'price_codes':6},
    147: {'customers':1857,'territories':32,'price_codes':6},
    120: {'customers':3746,'territories':26,'price_codes':4},
    69: {'customers':92470,'territories':17,'price_codes':1},
    152: {'customers':1991,'territories':93,'price_codes':4},
    14: {'customers':8351,'territories':83,'price_codes':18},
    245: {'customers':4450,'territories':71,'price_codes':15},
    8: {'customers':14022,'territories':74,'price_codes':7},
    231: {'customers':174,'territories':37,'price_codes':4},
    266: {'customers':877,'territories':44,'price_codes':1},
    64: {'customers':4848,'territories':64,'price_codes':5},
    70: {'customers':2272,'territories':62,'price_codes':4},
    71: {'customers':2289,'territories':69,'price_codes':4},
    255: {'customers':24660,'territories':88,'price_codes':1},
    76: {'customers':9496,'territories':145,'price_codes':4},
    68: {'customers':6010,'territories':47,'price_codes':1},
    248: {'customers':4900,'territories':77,'price_codes':5},
    250: {'customers':6847,'territories':131,'price_codes':41},
    166: {'customers':2845,'territories':34,'price_codes':11},
    252: {'customers':8609,'territories':33,'price_codes':26},
    221: {'customers':1211,'territories':36,'price_codes':2},
    62: {'customers':2010,'territories':103,'price_codes':6},
    124: {'customers':3753,'territories':50,'price_codes':1},
    181: {'customers':9618,'territories':316,'price_codes':26},
    224: {'customers':52,'territories':2,'price_codes':2},
    58: {'customers':0,'territories':0,'price_codes':0},
    90: {'customers':2782,'territories':34,'price_codes':1},
    187: {'customers':2347,'territories':29,'price_codes':6},
    40: {'customers':3246,'territories':3246,'price_codes':2},
    41: {'customers':1361,'territories':22,'price_codes':4},
    229: {'customers':2,'territories':2,'price_codes':1},
    49: {'customers':3193,'territories':1,'price_codes':7},
    139: {'customers':1978,'territories':65,'price_codes':2},
    149: {'customers':5189,'territories':118,'price_codes':3},
    185: {'customers':3554,'territories':76,'price_codes':3},
    232: {'customers':790,'territories':9,'price_codes':11},
    176: {'customers':1496,'territories':43,'price_codes':8},
    286: {'customers':6551,'territories':24,'price_codes':1},
    138: {'customers':7529,'territories':96,'price_codes':31},
    168: {'customers':1321,'territories':29,'price_codes':6},
    237: {'customers':778,'territories':25,'price_codes':1},
    220: {'customers':630,'territories':28,'price_codes':2},
    227: {'customers':1515,'territories':25,'price_codes':1},
    127: {'customers':2375,'territories':78,'price_codes':27},
    155: {'customers':0,'territories':0,'price_codes':0},
    137: {'customers':9387,'territories':124,'price_codes':35},
    184: {'customers':1572,'territories':36,'price_codes':3},
    22: {'customers':1763,'territories':48,'price_codes':2},
    89: {'customers':1764,'territories':10,'price_codes':1},
    12: {'customers':2017,'territories':44,'price_codes':1},
    19: {'customers':549,'territories':27,'price_codes':1},
    222: {'customers':3232,'territories':34,'price_codes':22},
    51: {'customers':102,'territories':17,'price_codes':1},
    20: {'customers':410,'territories':27,'price_codes':1},
    140: {'customers':595,'territories':7,'price_codes':3},
    136: {'customers':883,'territories':26,'price_codes':1},
    97: {'customers':787,'territories':52,'price_codes':1},
    26: {'customers':1627,'territories':73,'price_codes':1},
    94: {'customers':3636,'territories':55,'price_codes':1},
    160: {'customers':6617,'territories':105,'price_codes':2},
    132: {'customers':0,'territories':0,'price_codes':0},
    244: {'customers':2208,'territories':53,'price_codes':14},
    87: {'customers':8463,'territories':21,'price_codes':14},
    # Round 3 audit backfill (live Postgres 2026-07-09)
    273: {'customers':1,'territories':1,'price_codes':1},     # leg
    230: {'customers':0,'territories':0,'price_codes':0},     # soi
    86: {'customers':287,'territories':11,'price_codes':2},   # tel
    234: {'customers':0,'territories':0,'price_codes':0},     # ilc
    235: {'customers':605,'territories':10,'price_codes':1},  # abol
}

# === ORDER STATS ===
ORDER_STATS = {
    246: {'orders':126,'aov':12082,'recent':'2026-07'},
    272: {'orders':360,'aov':9818,'recent':'2026-07'},
    107: {'orders':13595,'aov':5295,'recent':'2026-07'},
    126: {'orders':130,'aov':25898,'recent':'2026-06'},
    2: {'orders':30696,'aov':2996,'recent':'2026-07'},
    121: {'orders':2297,'aov':6696,'recent':'2026-07'},
    131: {'orders':2,'aov':2407,'recent':'2019-04'},
    111: {'orders':8989,'aov':7644,'recent':'2026-07'},
    164: {'orders':13796,'aov':3431,'recent':'2026-07'},
    32: {'orders':41650,'aov':4501,'recent':'2026-07'},
    162: {'orders':1283,'aov':4707,'recent':'2026-07'},
    167: {'orders':126,'aov':3638,'recent':'2026-07'},
    1: {'orders':13431,'aov':3898,'recent':'2026-07'},
    268: {'orders':79,'aov':9742,'recent':'2026-04'},
    225: {'orders':11531,'aov':2076,'recent':'2026-07'},
    72: {'orders':283,'aov':8437,'recent':'2025-02'},
    243: {'orders':345,'aov':11976,'recent':'2026-05'},
    133: {'orders':3506,'aov':3096,'recent':'2026-01'},
    65: {'orders':138,'aov':81608,'recent':'2026-04'},
    83: {'orders':6666,'aov':3035,'recent':'2026-07'},
    236: {'orders':181,'aov':5472,'recent':'2026-07'},
    161: {'orders':13948,'aov':1977,'recent':'2026-07'},
    55: {'orders':175282,'aov':2366,'recent':'2026-07'},
    23: {'orders':1635,'aov':4788,'recent':'2026-07'},
    223: {'orders':94,'aov':3534,'recent':'2026-06'},
    141: {'orders':9496,'aov':2765,'recent':'2026-06'},
    114: {'orders':2595,'aov':11003,'recent':'2026-06'},
    108: {'orders':17067,'aov':92048,'recent':'2026-07'},
    182: {'orders':412,'aov':14255,'recent':'2026-06'},
    249: {'orders':18,'aov':2963,'recent':'2026-02'},
    165: {'orders':8907,'aov':9538,'recent':'2026-07'},
    18: {'orders':37526,'aov':7671,'recent':'2026-07'},
    146: {'orders':1352,'aov':8332,'recent':'2026-06'},
    239: {'orders':525,'aov':3391,'recent':'2026-07'},
    269: {'orders':349,'aov':2094,'recent':'2026-07'},
    171: {'orders':6817,'aov':2670,'recent':'2026-07'},
    88: {'orders':65941,'aov':17261,'recent':'2026-07'},
    147: {'orders':743,'aov':7366,'recent':'2026-06'},
    120: {'orders':31221,'aov':4144,'recent':'2026-07'},
    69: {'orders':333740,'aov':4421,'recent':'2026-07'},
    152: {'orders':1245,'aov':11248,'recent':'2026-06'},
    14: {'orders':8608,'aov':1849,'recent':'2026-07'},
    245: {'orders':1974,'aov':13671,'recent':'2026-07'},
    8: {'orders':43559,'aov':1715,'recent':'2026-07'},
    231: {'orders':470,'aov':2117,'recent':'2026-07'},
    266: {'orders':4,'aov':2230,'recent':'2025-05'},
    64: {'orders':1816,'aov':3790,'recent':'2026-07'},
    70: {'orders':548,'aov':3194,'recent':'2026-05'},
    71: {'orders':849,'aov':3926,'recent':'2026-01'},
    255: {'orders':4679,'aov':4783,'recent':'2026-07'},
    76: {'orders':82488,'aov':1043,'recent':'2026-07'},
    68: {'orders':21122,'aov':3279,'recent':'2026-07'},
    248: {'orders':10449,'aov':1200,'recent':'2026-07'},
    250: {'orders':28,'aov':3905,'recent':'2026-07'},
    166: {'orders':978,'aov':6498,'recent':'2026-07'},
    252: {'orders':170,'aov':10394,'recent':'2026-07'},
    221: {'orders':369,'aov':3823,'recent':'2026-07'},
    62: {'orders':22126,'aov':1663,'recent':'2026-07'},
    124: {'orders':9578,'aov':5652,'recent':'2026-07'},
    181: {'orders':4769,'aov':4338,'recent':'2026-07'},
    224: {'orders':161,'aov':2798,'recent':'2026-07'},
    58: {'orders':5,'aov':10825,'recent':'2015-11'},
    90: {'orders':3068,'aov':4178,'recent':'2026-07'},
    187: {'orders':533,'aov':925,'recent':'2026-07'},
    40: {'orders':287,'aov':4727,'recent':'2026-07'},
    41: {'orders':6751,'aov':75677,'recent':'2026-07'},
    229: {'orders':48,'aov':1343,'recent':'2024-08'},
    49: {'orders':875,'aov':7249,'recent':'2026-06'},
    139: {'orders':11856,'aov':2195,'recent':'2026-07'},
    149: {'orders':1351,'aov':4686,'recent':'2026-07'},
    185: {'orders':73,'aov':1929,'recent':'2026-06'},
    232: {'orders':151,'aov':6345,'recent':'2026-07'},
    176: {'orders':317,'aov':496,'recent':'2026-07'},
    286: {'orders':96,'aov':2994,'recent':'2026-06'},
    138: {'orders':53,'aov':2455,'recent':'2025-03'},
    168: {'orders':289,'aov':2642,'recent':'2026-06'},
    237: {'orders':27,'aov':749,'recent':'2026-05'},
    220: {'orders':55,'aov':2248,'recent':'2026-01'},
    227: {'orders':3759,'aov':1136,'recent':'2026-07'},
    127: {'orders':129,'aov':2091,'recent':'2025-08'},
    155: {'orders':118,'aov':2168,'recent':'2026-06'},
    137: {'orders':258,'aov':6780,'recent':'2026-07'},
    184: {'orders':1961,'aov':5224,'recent':'2026-07'},
    22: {'orders':78596,'aov':2129,'recent':'2026-07'},
    89: {'orders':74493,'aov':1916,'recent':'2026-07'},
    12: {'orders':4663,'aov':1383,'recent':'2026-06'},
    19: {'orders':6497,'aov':756,'recent':'2026-07'},
    222: {'orders':5996,'aov':979,'recent':'2026-07'},
    51: {'orders':461,'aov':513,'recent':'2023-06'},
    20: {'orders':567,'aov':1148,'recent':'2025-05'},
    140: {'orders':5509,'aov':3521,'recent':'2026-07'},
    136: {'orders':5522,'aov':968,'recent':'2026-07'},
    97: {'orders':429,'aov':908,'recent':'2025-04'},
    26: {'orders':16308,'aov':1783,'recent':'2026-07'},
    94: {'orders':32820,'aov':4847,'recent':'2026-07'},
    160: {'orders':19446,'aov':5864,'recent':'2026-07'},
    132: {'orders':1828,'aov':5901,'recent':'2026-07'},
    244: {'orders':2,'aov':191,'recent':'2025-08'},
    87: {'orders':119686,'aov':4823,'recent':'2026-07'},
    # Round 3 audit backfill (live Postgres 2026-07-09)
    273: {'orders':0,'aov':0,'recent':''},                   # leg
    230: {'orders':0,'aov':0,'recent':''},                   # soi
    86: {'orders':14,'aov':7688,'recent':'2022-03'},         # tel
    234: {'orders':0,'aov':0,'recent':''},                   # ilc
    235: {'orders':0,'aov':0,'recent':''},                   # abol
}

# === INVOICE STATS ===
INVOICE_STATS = {
    1: 62120797, 2: 27816980, 8: 50051963, 18: 252230369,
    22: 89742261, 26: 61171979, 32: 67377152, 40: 92288787,
    41: 97466062, 55: 60621588, 64: 74154162, 65: 30109375,
    69: 122735871, 76: 73935117, 85: 52143216, 87: 166138663,
    88: 74348177, 107: 7002166, 111: 301013857, 120: 27592517,
    121: 30590032, 127: 7295183, 139: 87451083, 146: 48017669,
    147: 12544262, 149: 326546428, 152: 45083087, 161: 185226777,
    164: 14919454, 165: 105351052, 166: 437596912960, # kll - seems data anomaly
    171: 37135938, 176: 18300167, 187: 2414670, 222: 45080079,
    225: 48587778, 239: 11343621, 245: 55544230, 248: 72226067,
    272: 558442, 288: 42972752,
}

# === IPAD ACTIVE USERS ===
IPAD_USERS = {
    246:20, 272:29, 107:46, 126:77, 2:43, 121:66, 131:120, 111:136,
    164:43, 32:160, 162:56, 167:33, 1:125, 268:15, 225:31, 72:184,
    243:56, 133:33, 65:43, 83:46, 236:24, 161:83, 55:103, 23:42,
    223:65, 141:138, 114:157, 108:169, 182:122, 249:24, 165:144,
    18:99, 146:84, 239:13, 269:60, 171:68, 88:47, 147:89, 120:56,
    69:135, 152:204, 14:22, 245:57, 8:115, 231:38, 266:17, 64:109,
    70:190, 71:163, 255:82, 76:102, 68:129, 248:82, 250:76, 166:83,
    252:98, 221:62, 62:40, 124:102, 181:139, 224:20, 58:28, 90:35,
    187:55, 40:111, 41:97, 229:14, 49:89, 139:162, 149:110, 185:57,
    232:20, 176:41, 286:64, 138:79, 168:38, 237:35, 220:40, 227:23,
    127:87, 155:87, 137:80, 184:98, 22:89, 89:38, 12:45, 19:42,
    222:99, 51:41, 20:42, 140:18, 136:34, 97:11, 26:84, 94:42,
    160:20, 132:14, 244:6, 87:105,
    # Round 3 audit backfill — last_ipad_login_at IS NOT NULL, disabled=false
    273:6, 230:9, 86:17, 234:9, 235:13,
}

# === CATEGORY/COLLECTION DIVERSITY ===
CAT_DIVERSITY = {
    246: {'cats':22,'colls':134,'trades':1},
    272: {'cats':110,'colls':127,'trades':4},
    107: {'cats':29,'colls':361,'trades':5},
    126: {'cats':106,'colls':46,'trades':3},
    2: {'cats':17,'colls':17,'trades':2},
    121: {'cats':35,'colls':29,'trades':7},
    131: {'cats':56,'colls':974,'trades':3},
    111: {'cats':64,'colls':130,'trades':4},
    164: {'cats':10,'colls':230,'trades':1},
    32: {'cats':35,'colls':33,'trades':3},
    162: {'cats':11,'colls':25,'trades':6},
    167: {'cats':32,'colls':34,'trades':2},
    1: {'cats':36,'colls':33,'trades':4},
    268: {'cats':68,'colls':13,'trades':1},
    225: {'cats':954,'colls':315,'trades':19},
    72: {'cats':10,'colls':291,'trades':1},
    243: {'cats':41,'colls':139,'trades':3},
    133: {'cats':25,'colls':20,'trades':1},
    65: {'cats':107,'colls':621,'trades':190},
    83: {'cats':35,'colls':113,'trades':3},
    236: {'cats':47,'colls':54,'trades':6},
    161: {'cats':40,'colls':12,'trades':2},
    55: {'cats':54,'colls':251,'trades':3},
    23: {'cats':36,'colls':25,'trades':7},
    223: {'cats':15,'colls':43,'trades':1},
    141: {'cats':25,'colls':38,'trades':1},
    114: {'cats':35,'colls':574,'trades':3},
    108: {'cats':30,'colls':1195,'trades':5},
    182: {'cats':15,'colls':266,'trades':4},
    249: {'cats':20,'colls':57,'trades':2},
    165: {'cats':17,'colls':267,'trades':1},
    18: {'cats':61,'colls':180,'trades':7},
    146: {'cats':31,'colls':647,'trades':4},
    239: {'cats':75,'colls':200,'trades':3},
    269: {'cats':6,'colls':32,'trades':1},
    171: {'cats':33,'colls':195,'trades':1},
    88: {'cats':146,'colls':394,'trades':4},
    147: {'cats':16,'colls':115,'trades':1},
    120: {'cats':23,'colls':2,'trades':4},
    69: {'cats':160,'colls':437,'trades':6},
    152: {'cats':18,'colls':258,'trades':4},
    14: {'cats':48,'colls':54,'trades':1},
    245: {'cats':35,'colls':133,'trades':6},
    8: {'cats':45,'colls':31,'trades':2},
    231: {'cats':17,'colls':29,'trades':3},
    266: {'cats':14,'colls':130,'trades':1},
    64: {'cats':10,'colls':228,'trades':1},
    70: {'cats':18,'colls':652,'trades':1},
    71: {'cats':15,'colls':1537,'trades':1},
    255: {'cats':40,'colls':170,'trades':4},
    76: {'cats':12,'colls':11,'trades':1},
    68: {'cats':74,'colls':573,'trades':9},
    248: {'cats':47,'colls':10,'trades':2},
    250: {'cats':83,'colls':9,'trades':8},
    166: {'cats':38,'colls':703,'trades':5},
    252: {'cats':4,'colls':879,'trades':6},
    221: {'cats':10,'colls':305,'trades':1},
    62: {'cats':355,'colls':30,'trades':11},
    124: {'cats':49,'colls':37,'trades':5},
    181: {'cats':129,'colls':1022,'trades':10},
    224: {'cats':11,'colls':155,'trades':6},
    58: {'cats':41,'colls':30,'trades':1},
    90: {'cats':2,'colls':19,'trades':1},
    187: {'cats':15,'colls':256,'trades':1},
    40: {'cats':17,'colls':359,'trades':3},
    41: {'cats':33,'colls':614,'trades':7},
    229: {'cats':24,'colls':24,'trades':2},
    49: {'cats':103,'colls':436,'trades':8},
    139: {'cats':73,'colls':407,'trades':4},
    149: {'cats':67,'colls':545,'trades':1},
    185: {'cats':11,'colls':270,'trades':2},
    232: {'cats':20,'colls':471,'trades':10},
    176: {'cats':24,'colls':403,'trades':3},
    286: {'cats':26,'colls':553,'trades':32},
    138: {'cats':47,'colls':422,'trades':1},
    168: {'cats':16,'colls':608,'trades':10},
    237: {'cats':56,'colls':284,'trades':2},
    220: {'cats':29,'colls':120,'trades':1},
    227: {'cats':37,'colls':277,'trades':13},
    127: {'cats':27,'colls':334,'trades':1},
    155: {'cats':65,'colls':526,'trades':2},
    137: {'cats':72,'colls':1260,'trades':3},
    184: {'cats':48,'colls':659,'trades':15},
    22: {'cats':59,'colls':22,'trades':9},
    89: {'cats':53,'colls':4,'trades':4},
    12: {'cats':30,'colls':126,'trades':2},
    19: {'cats':35,'colls':69,'trades':2},
    222: {'cats':32,'colls':6,'trades':1},
    51: {'cats':22,'colls':22,'trades':2},
    20: {'cats':22,'colls':17,'trades':2},
    140: {'cats':74,'colls':61,'trades':18},
    136: {'cats':69,'colls':293,'trades':4},
    97: {'cats':185,'colls':31,'trades':3},
    26: {'cats':285,'colls':561,'trades':6},
    94: {'cats':413,'colls':140,'trades':7},
    160: {'cats':1,'colls':1,'trades':1},
    132: {'cats':46,'colls':695,'trades':46},
    244: {'cats':2,'colls':28,'trades':4},
    87: {'cats':121,'colls':190,'trades':4},
    # Round 3 audit backfill (live Postgres 2026-07-09)
    273: {'cats':24,'colls':11,'trades':4},   # leg
    230: {'cats':52,'colls':0,'trades':2},    # soi
    86: {'cats':19,'colls':15,'trades':7},    # tel
    234: {'cats':39,'colls':63,'trades':3},   # ilc
    235: {'cats':36,'colls':77,'trades':3},   # abol
}


# === CLASSIFICATION LOGIC ===

def classify_what_they_sell(shortname, company, avg_price, cats, product_count):
    """Classify product type based on company name, category diversity, and known industry."""
    company_lower = company.lower()
    
    lighting_keywords = ['lighting', 'light', 'lamp', 'chandelier', 'sconce',
                         'luminaire', 'bulb', 'led', 'visual comfort', 'corbett',
                         'hudson valley', 'troy', 'savoy house', 'crystorama',
                         'kuzco', 'minka', 'maxim', 'eurofase', 'dainolite',
                         'et2', 'eglo', 'access light', 'millennium', 'golden light',
                         'capital light', 'craftmade', 'kalco', 'matteo', 'dals',
                         'hubbardton forge', 'wac', 'modern forms', 'schonbek',
                         'fine art', 'currey', 'accord', 'arabela', 'lucas mckearn',
                         'varaluz', 'buster & punch', 'designer\'s fountain',
                         'pageone', 'progress light']
    furniture_keywords = ['furniture', 'furnish', 'sofa', 'chair', 'table', 'bed',
                          'cabinet', 'desk', 'woodwork', 'upholster', 'braxton culler',
                          'charleston forge', 'palecek', 'interlude', 'baker',
                          'theodore alexander', 'somerset bay', 'jonathan charles',
                          'rowe', 'four seasons', 'yutzy', 'hooker', 'century',
                          'highland house', 'kindel', 'lifestyle solution',
                          'sauder', 'magnussen', 'linon', 'powell']
    outdoor_keywords = ['outdoor', 'patio', 'pool', 'summer classics', 'sunset west',
                        'ratana', 'alfresco', 'backyard', 'sabine pools']
    accessories_keywords = ['gift', 'silversmith', 'silver art', 'frame', 'sixtrees',
                            'philip whitney', 'home essentials', 'kennedy international',
                            'uniware', 'housewares', 'moda at home', 'popular bath',
                            'elico', 'pioneer morton', 'ricci argentieri',
                            'container marketing']
    decor_art_keywords = ['art', 'decor', 'wendover', 'shadow catcher', 'bliss studio',
                          'elegant furniture', 'jamie young', 'wildwood', 'chelsea house',
                          'made goods', 'gabby']
    rug_keywords = ['rug', 'carpet', 'broadloom', 'kaleen']
    
    # Check in priority order
    for kw in rug_keywords:
        if kw in company_lower:
            return 'Rugs'
    for kw in outdoor_keywords:
        if kw in company_lower:
            return 'Outdoor'
    for kw in lighting_keywords:
        if kw in company_lower:
            return 'Lighting'
    for kw in accessories_keywords:
        if kw in company_lower:
            return 'Accessories/Giftware'
    for kw in decor_art_keywords:
        if kw in company_lower:
            return 'Decor/Art'
    for kw in furniture_keywords:
        if kw in company_lower:
            return 'Furniture'
    
    # Fallback heuristics
    if shortname in ('am','tam','ihw','big','sbmh','jcusa','hmjc','ta','ih','pf',
                     'rf','ol','fsf','cfg','yw','hf','cf','hh','kkc','ihm','bcf',
                     'fc','lss','swc','mh','lpf','dccl','sp'):
        return 'Furniture'
    if shortname in ('vce','vcg','tla','fms','sbl','cl','all','hfg','kal','vl',
                     'el','clm','tl','hvl','kll','mlg','mlc','da','wac','gl',
                     'clc','shl','clli','afx','eglo_can','eglo','et2','dals',
                     'ali','ml','mli','prog','df','arl','luc','bp','gcl','fal'):
        return 'Lighting'
    if shortname in ('sc','sccon','ah','ril'):
        return 'Outdoor'
    if shortname in ('asi','mpc','gsa','rac','bri','pw','ssi','etl','mah','st',
                     'heb','kii','uhc'):
        return 'Accessories/Giftware'
    if shortname in ('wag','sca','jyc','wwjc','blh','eli','rw','gh','ap','sarreid','cci'):
        return 'Decor/Art'
    if shortname in ('krb',):
        return 'Rugs'
    
    # Final catch-all for known remaining accounts
    REMAINING_MAP = {
        'bsc': 'Furniture', 'khi': 'Furniture', 'kl': 'Lighting',
        'vic': 'Lighting', 'gc': 'Accessories/Giftware', 'mfc': 'Textiles',
    }
    if shortname in REMAINING_MAP:
        return REMAINING_MAP[shortname]
    
    # ?? shortnames — classify by company name
    if 'gabriella' in company_lower:
        return 'Outdoor'
    if 'legrand' in company_lower:
        return 'Lighting'
    if 'silver' in company_lower:
        return 'Accessories/Giftware'
    if 'tomlinson' in company_lower:
        return 'Furniture'
    if 'ideal' in company_lower:
        return 'Furniture'
    
    return 'Mixed/Unclassified'


def classify_how_they_sell(shortname, avg_price, aov, orders, price_codes, 
                           customers, territories):
    """
    Classify selling motion using v3.2-validated qualitative knowledge as anchor,
    with quantitative signals as confirmation/challenge. Per v3.2 finding:
    "price is a correlate, not a classifier."
    
    The selling motion axis is:
    - Specification: designer-driven, project-based (designers put it in a project)
    - Brand-building: dealers carry the line on brand reputation
    - Multi-channel: trade + retail + online distribution
    - Volume: commodity distribution, high volume, low touch
    """
    # Anchor on v3.2 validated selling motion (Kylor-stamped baseline)
    # Only move accounts where data STRONGLY contradicts v3.2 placement
    
    SPEC = ('am','tam','ihw','big','sbmh','jcusa','hmjc','ta','ih','pf',
            'rf','vce','sarreid','ol','fsf','cl','hf','blh','jc','cfg','yw',
            'cci','gh','ap','all','vcg','tla','fms','sbl','fal','cf','hh','kkc')
    
    BRAND = ('ihm','hfg','ufi','kal','dccl','arl','bcf','sccon','vl','fc','sc','scw',
             'el','bsc','ril','wwjc','gcl','luc','clm','tl','hvl','wag','jyc',
             'eli','rw','bp','kll','mlg','mlc','da','ah','wac',
             # Round 1/3 unmatched resolutions — keep Brand-Building; do not let the
             # avg_price>800 fallthrough reclassify them as Specification once stats are backfilled
             'leg','soi','tel','ilc','abol')
    
    MULTI = ('lss','swc','sca','gl','clc','shl','khi','kl','lpf','clli',
             'afx','eglo_can','vic','prog','et2','eglo','df','dals','gc',
             'ali','ml','mli','mh','mfc')
    
    VOLUME = ('asi','mpc','gsa','rac','bri','pw','ssi','etl','mah','st',
              'heb','kii','uhc')
    
    if shortname in SPEC:
        return 'Specification'
    if shortname in BRAND:
        return 'Brand-Building'
    if shortname in MULTI:
        return 'Multi-Channel'
    if shortname in VOLUME:
        return 'Volume Distribution'
    
    # Unmatched accounts (the ?? shortnames and specialty) - classify by signals
    if avg_price and avg_price < 30:
        return 'Volume Distribution'
    if avg_price and avg_price > 800:
        return 'Specification'
    if price_codes > 5 or territories > 50:
        return 'Multi-Channel'
    return 'Brand-Building'


def classify_who_they_sell_to(shortname, customers, territories, price_codes, 
                              avg_price, selling_motion):
    """
    Classify buyer type:
    - Trade-only: designers/architects (specification-based)
    - Wholesale: dealers/retailers
    - Mixed: trade + retail + online
    - Contract: hospitality/project buyers
    """
    # Specification sellers typically sell to trade (designers)
    if selling_motion == 'Specification':
        if shortname in ('sccon','ihm'):
            return 'Contract/Hospitality'
        return 'Trade (Designers/Architects)'
    
    # Volume distributors sell wholesale to retailers
    if selling_motion == 'Volume Distribution':
        return 'Wholesale (Retailers)'
    
    # Multi-channel = mixed by definition
    if selling_motion == 'Multi-Channel':
        if price_codes > 10:
            return 'Mixed (Trade + Retail)'
        return 'Wholesale (Dealers/Retailers)'
    
    # Brand-building: mostly wholesale to dealers
    if customers > 5000 and territories > 50:
        return 'Wholesale (Broad Dealer Network)'
    if price_codes > 10:
        return 'Mixed (Trade + Retail)'
    return 'Wholesale (Dealers)'


# === IDENTITY CORRECTIONS (found 2026-07-09, post-stamp) ===
# The v3.2 baseline (and every version built on it, incl. the first v4.0 pass) mapped
# "Summer Classics" to shortname 'sc'. Live Postgres organizations.company_website proves
# 'sc' is actually Gabriella White (www.GabriellaWhite.com) — the real-world PARENT LLC that
# owns the Summer Classics / Summer Classics Contract / Gabby / Wendy Jane brands. The real
# Summer Classics org is 'scw' (www.summerclassics.com) — which had data pulled into the dicts
# above but was never referenced by any roster row (orphaned). Both 'sc' and 'scw' are
# separately-billed, simultaneously-active accounts (each has orders posting same-day) — this
# is a parent/sibling-brand family (per VM-K6: no native parent key, never silently merge),
# not a duplicate. Gabriella White and the 4 other '??' accounts were unmatched only because
# the source CSV carried literal placeholder/wrong shortnames — see
# unmatched_accounts_validation_2026-07-09.md for the full trace.
SHORTNAME_CORRECTIONS = {
    ('Summer Classics', 'sc'): 'scw',
    ('Gabriella White', '??'): 'sc',
    ('Legrand US', '??'): 'leg',
    ('Silver One', '??'): 'soi',
    ('Tomlinson Companies', '??'): 'tel',
    ('Ideal Living', '??'): 'ilc',
}


# === BUILD THE MASTER TABLE ===
def build_master():
    """Read v3.2 CSV and enrich with all Postgres dimensions."""
    
    csv_path = BASE / 'SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv'
    rows = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    enriched = []
    for row in rows:
        shortname = row['org']
        company = row['Company']
        v3_segment = row['segment']
        
        shortname = SHORTNAME_CORRECTIONS.get((company, shortname), shortname)
        org_id = SHORTNAME_TO_ID.get(shortname)
        
        # Product stats
        ps = PRODUCT_STATS.get(org_id, {})
        product_count = ps.get('count', 0)
        avg_price = ps.get('avg', 0)
        
        # Customer stats
        cs = CUSTOMER_STATS.get(org_id, {})
        customer_count = cs.get('customers', 0)
        territory_count = cs.get('territories', 0)
        price_code_count = cs.get('price_codes', 0)
        
        # Order stats
        os_data = ORDER_STATS.get(org_id, {})
        order_count = os_data.get('orders', 0)
        aov = os_data.get('aov', 0)
        recent = os_data.get('recent', '')
        
        # Invoice revenue
        invoiced = INVOICE_STATS.get(org_id, 0)
        # Fix anomaly for kll (org 166) - clearly a data issue
        if org_id == 166 and invoiced > 1000000000:
            invoiced = 0
        
        # iPad users
        ipad_users = IPAD_USERS.get(org_id, 0)
        
        # Category diversity
        cd = CAT_DIVERSITY.get(org_id, {})
        distinct_cats = cd.get('cats', 0)
        distinct_colls = cd.get('colls', 0)
        
        # CSV fields
        csv_avg_price = row.get('v3_avg_price', '')
        csv_median = row.get('catalog_scrub_median', '')
        csv_realized = row.get('realized_mean_price', '')
        csv_best = row.get('best_price', '')
        csv_orders = row.get('total_orders', '')
        csv_aov = row.get('avg_order_value', '')
        csv_price_codes = row.get('distinct_price_codes', '')
        csv_products = row.get('n_products', '')
        
        # Use best available price
        # NOTE: rows touched by SHORTNAME_CORRECTIONS carry a v3.2 best_price/realized-price
        # computed against the WRONG org (e.g. "Summer Classics" originally had 'sc' — really
        # Gabriella White — baked into its v3.2 realized price). Don't trust those stale
        # v3.2 price columns on a corrected row; fall back to the freshly-pulled catalog avg.
        if (company, row['org']) in SHORTNAME_CORRECTIONS:
            best_price = avg_price if avg_price else 0
        else:
            best_price = float(csv_best) if csv_best else (avg_price if avg_price else 0)
        
        # Classifications
        what_sell = classify_what_they_sell(shortname, company, best_price, distinct_cats, product_count)
        how_sell = classify_how_they_sell(shortname, best_price, aov, order_count,
                                          price_code_count, customer_count, territory_count)
        who_sell = classify_who_they_sell_to(shortname, customer_count, territory_count,
                                             price_code_count, best_price, how_sell)
        
        # Derive v4 segment based on axes
        if how_sell == 'Specification':
            v4_segment = '1. Luxury Specification'
        elif how_sell == 'Brand-Building':
            v4_segment = '2. Premium Trade Brand'
        elif how_sell == 'Multi-Channel':
            v4_segment = '3. Mid-Market Multi-Channel'
        elif how_sell == 'Volume Distribution':
            v4_segment = '4. Volume Distribution'
        else:
            v4_segment = '5. Specialty/Non-Traditional'
        
        enriched.append({
            'Company': company,
            'org': shortname,
            'org_id': org_id or '',
            'v3_segment': v3_segment,
            'v4_segment': v4_segment,
            'segment_changed': 'YES' if v3_segment != v4_segment else '',
            'how_they_sell': how_sell,
            'what_they_sell': what_sell,
            'who_they_sell_to': who_sell,
            'best_price': best_price,
            'catalog_avg_price': f"{avg_price:.0f}" if avg_price else '',
            'catalog_scrub_median': csv_median,
            'realized_mean': csv_realized,
            'product_count': product_count or csv_products,
            'customer_count': customer_count,
            'territory_count': territory_count,
            'price_code_count': price_code_count,
            'order_count': order_count,
            'avg_order_value': aov,
            'most_recent_order': recent,
            'total_invoiced_net': invoiced,
            'ipad_active_users': ipad_users,
            'distinct_categories': distinct_cats,
            'distinct_collections': distinct_colls,
        })
    
    return enriched


def write_csv(enriched):
    """Write the master enriched CSV."""
    out_path = BASE / 'SuperCat_Customer_Segmentation_v4.0_MASTER.csv'
    fieldnames = [
        'Company','org','org_id','v3_segment','v4_segment','segment_changed',
        'how_they_sell','what_they_sell','who_they_sell_to',
        'best_price','catalog_avg_price','catalog_scrub_median','realized_mean',
        'product_count','customer_count','territory_count','price_code_count',
        'order_count','avg_order_value','most_recent_order','total_invoiced_net',
        'ipad_active_users','distinct_categories','distinct_collections'
    ]
    
    with open(out_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)
    
    print(f"Wrote {len(enriched)} rows to {out_path}")
    return out_path


def analyze_segments(enriched):
    """Produce segment analysis stats."""
    
    # Count by v3 vs v4
    v3_counts = defaultdict(int)
    v4_counts = defaultdict(int)
    changes = []
    
    for row in enriched:
        v3_counts[row['v3_segment']] += 1
        v4_counts[row['v4_segment']] += 1
        if row['segment_changed']:
            changes.append(row)
    
    # Axis distributions
    how_counts = defaultdict(int)
    what_counts = defaultdict(int)
    who_counts = defaultdict(int)
    
    for row in enriched:
        how_counts[row['how_they_sell']] += 1
        what_counts[row['what_they_sell']] += 1
        who_counts[row['who_they_sell_to']] += 1
    
    return {
        'v3_counts': dict(v3_counts),
        'v4_counts': dict(v4_counts),
        'changes': changes,
        'how_counts': dict(how_counts),
        'what_counts': dict(what_counts),
        'who_counts': dict(who_counts),
    }


def compute_enrichment_medians(enriched):
    """
    Correctly-computed per-segment medians for the enrichment dimensions (order count, AOV,
    iPad-active users, invoiced revenue, catalog complexity, customer structure).

    Added 2026-07-09 after discovering the original analysis doc's Section 3 tables reported
    single-org raw values mislabeled as medians (e.g. "median AOV $5,295" was literally org
    `ihw`'s AOV, not a real median). Uses statistics.median explicitly — never hand-picked.
    Zero-value rows (orgs with no product/order data in Postgres) are INCLUDED as 0, matching
    how they're written into the CSV (build_master() defaults missing dict lookups to 0, not
    blank) — this keeps the CSV and this stats function consistent with each other.
    """
    import statistics as stats_mod
    from collections import defaultdict

    by_seg = defaultdict(list)
    for row in enriched:
        by_seg[row['v4_segment']].append(row)

    def med(rows, key, exclude_zero=False):
        vals = []
        for r in rows:
            v = r.get(key)
            try:
                v = float(v)
            except (TypeError, ValueError):
                continue
            if exclude_zero and v == 0:
                continue
            vals.append(v)
        return stats_mod.median(vals) if vals else None

    out = {}
    for seg, rows in sorted(by_seg.items()):
        n = len(rows)
        invoiced_nonzero = [r for r in rows if float(r.get('total_invoiced_net') or 0) != 0]
        out[seg] = {
            'n': n,
            'median_ipad_users': med(rows, 'ipad_active_users'),
            'median_order_count': med(rows, 'order_count'),
            'median_aov': med(rows, 'avg_order_value'),
            'invoice_feed_n': len(invoiced_nonzero),
            'invoice_feed_pct': round(len(invoiced_nonzero) / n * 100) if n else None,
            'median_invoiced_nonzero': med(invoiced_nonzero, 'total_invoiced_net') if invoiced_nonzero else None,
            'median_product_count': med(rows, 'product_count'),
            'median_distinct_categories': med(rows, 'distinct_categories'),
            'median_distinct_collections': med(rows, 'distinct_collections'),
            'median_customer_count': med(rows, 'customer_count'),
            'median_territory_count': med(rows, 'territory_count'),
            'median_price_codes': med(rows, 'price_code_count'),
        }
    return out


if __name__ == '__main__':
    enriched = build_master()
    csv_path = write_csv(enriched)
    stats = analyze_segments(enriched)
    medians = compute_enrichment_medians(enriched)
    print("\n=== ENRICHMENT MEDIANS (correctly computed) ===")
    for seg, m in medians.items():
        print(f"  {seg}: {m}")
    
    print("\n=== V3 SEGMENT COUNTS ===")
    for seg, count in sorted(stats['v3_counts'].items()):
        print(f"  {seg}: {count}")
    
    print("\n=== V4 SEGMENT COUNTS ===")
    for seg, count in sorted(stats['v4_counts'].items()):
        print(f"  {seg}: {count}")
    
    print(f"\n=== SEGMENT CHANGES: {len(stats['changes'])} accounts moved ===")
    for ch in stats['changes']:
        print(f"  {ch['Company']} ({ch['org']}): {ch['v3_segment']} → {ch['v4_segment']}")
    
    print("\n=== HOW THEY SELL ===")
    for k, v in sorted(stats['how_counts'].items()):
        print(f"  {k}: {v}")
    
    print("\n=== WHAT THEY SELL ===")
    for k, v in sorted(stats['what_counts'].items()):
        print(f"  {k}: {v}")
    
    print("\n=== WHO THEY SELL TO ===")
    for k, v in sorted(stats['who_counts'].items()):
        print(f"  {k}: {v}")
