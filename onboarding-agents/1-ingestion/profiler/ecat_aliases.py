"""Source-column -> eCat-field aliases, with a stated confidence per rule.

Confidence is part of the mapping, not decoration. A proposal a human has to
check is worth more than a guess presented as an answer, and the whole point of
Phase 2 is that the agent proposes and flags - it does not write the transform.

  certain  - the header IS the eCat field name
  high     - a well-known synonym seen across multiple real client exports
  moderate - a plausible synonym; a human should confirm
  low      - shape/keyword match only; treat as a question, not a proposal
"""

import re

# (regex over the lowercased raw header, eCat field, confidence, why)
ALIASES = [
    # --- keys
    (r'^(base\s*item\s*code)$', 'BaseItemCode', 'certain', 'exact eCat field'),
    (r'^(item|item\s*#|item\s*no\.?|item\s*num(ber)?|item\s*id)$', 'BaseItemCode',
     'high', 'item identifier is the eCat master key'),
    (r'^(sku|part\s*(no\.?|num(ber)?|#)|model(\s*(no\.?|#))?)$', 'BaseItemCode',
     'high', 'SKU/part number is the item key'),
    (r'^(internal\s*id)$', 'BaseItemCode', 'low',
     'ERP surrogate id - usually NOT the code reps search by; confirm against the '
     'client-facing item number before using'),

    # --- product descriptive
    (r'^(long\s*desc)$', 'LongDesc', 'certain', 'exact eCat field'),
    (r'^(product\s*name|item\s*description|description|display\s*name)$', 'LongDesc',
     'high', 'primary catalog name'),
    (r'^(short\s*desc)$', 'ShortDesc', 'certain', 'exact eCat field'),
    (r'^(medium\s*desc)$', 'MediumDesc', 'certain', 'exact eCat field'),
    (r'^(purchase\s*description)$', 'MediumDesc', 'low',
     'a purchasing-side description; may not be customer-facing'),
    (r'^(dimensions?)$', 'Dimensions', 'high', 'dimension string'),
    (r'^(materials?)$', 'Materials', 'high', 'materials list'),
    (r'^(features?)$', 'Features', 'high', 'features list'),
    (r'^(finish|color|colour)$', 'Finish', 'low',
     'client-domain attribute - eCat has no Finish field; becomes a custom field '
     'or an option set, decide which'),
    (r'^(collection|collections?\s*codes?)$', 'CollectionCodes', 'high',
     'taxonomy: whatever string is here becomes the iPad label'),
    (r'^(category|categor(y|ies)\s*codes?|class\s*id|item\s*class\s*code)$',
     'CategoryCodes', 'high', 'taxonomy: value becomes the iPad label'),
    (r'^(brand|trade\s*name(\s*code)?|product\s*line)$', 'TradeNameCode', 'high',
     'brand/trade name'),
    (r'^(upc|upc\s*value|ml_upc|nsl_upc)$', 'UPCValue', 'high', 'UPC'),
    (r'^(ship\s*weight|weight|wt)$', 'ShipWeight', 'high', 'shipping weight'),
    (r'^(packed\s*volume|cube|volume)$', 'PackedVolume', 'moderate',
     'required float; 0 if no cube data'),
    (r'^(pack\s*(qty|quantity))$', 'PackQuantity', 'high', 'integer, <=0 coerces to 1'),
    (r'^(min(imum)?\s*(qty|quantity|order))$', 'MinimumQuantity', 'high',
     'integer, <=0 coerces to 1'),
    (r'^(image(\s*file)?\s*name|image|photo)$', 'ImageFileName', 'high',
     'must match FTP filenames exactly; no slashes or parentheses'),
    (r'^(related\s*items?)$', 'RelatedItems', 'high', 'comma list of in-file codes'),
    (r'^(new\s*item)$', 'NewItem', 'high', 'Y/blank'),
    (r'^(hideable)$', 'Hideable', 'certain', 'exact eCat field'),
    (r'^(discontinued|item\s*discontinued|hide/?discontinue\??)$', 'Hideable',
     'moderate', 'discontinued flag most often drives Hideable; confirm the '
     'client wants them hidden rather than deleted'),

    # --- pricing
    (r'^(net\s*price)$', 'NetPrice', 'certain', 'exact eCat field'),
    (r'^(price|list\s*price|list|msrp|showroom\s*net(\s*(cdn|cad|usd))?)$',
     'NetPrice or Price_<code>', 'moderate',
     'MULTIPLE price columns usually mean multiple price LEVELS, not one NetPrice '
     '- decide the level codes before mapping'),
    (r'^(promo(tion)?\s*price)$', 'PromotionPrice', 'high', 'promo price'),
    (r'^(imap|map)$', 'Price_<code>', 'moderate',
     'IMAP/MAP is a distinct price level, not NetPrice'),
    (r'^(dn|discount|net)$', 'Price_<code>', 'moderate',
     'a discount level; needs its own price level code'),

    # --- customers
    (r'^(bill\s*to\s*code)$', 'BillToCode', 'certain', 'exact eCat field'),
    (r'^(customer\s*(#|no\.?|num(ber)?|code|id))$', 'BillToCode', 'high',
     'customer identifier'),
    (r'^(bill\s*to\s*name)$', 'BillToName', 'certain', 'exact eCat field'),
    (r'^(customer(\s*name)?|account(\s*name)?|name)$', 'BillToName', 'high',
     'customer name'),
    (r'^(address\s*1|bill\s*to\s*address\s*1|street)$', 'BillToAddress1', 'high', ''),
    (r'^(address\s*2)$', 'BillToAddress2', 'high', ''),
    (r'^(address\s*3)$', 'BillToAddress3', 'high', ''),
    (r'^(city)$', 'BillToCity', 'high', ''),
    (r'^(state|province|state/?province)$', 'BillToState', 'high', ''),
    (r'^(zip|postal(\s*code)?|post\s*code)$', 'BillToPostCode', 'high', ''),
    (r'^(country)$', 'BillToCountry', 'high', ''),
    (r'^(telephone#?|phone(\s*1)?|tel)$', 'BuyerPhone', 'high', ''),
    (r'^(e-?mail(\s*address)?)$', 'BuyerEmail', 'high', ''),
    (r'^(fax)$', 'BuyerFax', 'high', ''),
    (r'^(terms|payment\s*terms)$', 'Terms', 'high', ''),
    (r'^(carrier|ship\s*via|shipped\s*via)$', 'Carrier', 'moderate', ''),
    (r'^(territory(\s*codes?)?|salesperson(\s*(id|code))?|sales\s*rep|rep(\s*code)?|'
     r'am\s*#|account\s*manager)$', 'TerritoryCodes',
     'high', 'drives rep<->customer filtering; empty stores as the literal "[]"'),
    (r'^(default\s*price\s*code|price\s*level|price\s*code)$', 'DefaultPriceCode',
     'high', 'must resolve to a real Admin price level code'),

    # --- inventory
    (r'^(qty\s*on\s*hand|quantity\s*on\s*hand|on\s*hand)$', 'QtyOnHand', 'high', ''),
    (r'^(qty\s*available|quantity\s*available|available)$', 'QtyAvailable', 'high', ''),
    (r'^(qty\s*allocated|allocated|qty\s*reserved|reserved)$', 'QtyReserved',
     'moderate', 'allocated and reserved are not always the same concept'),
    (r'^(qty\s*(back\s*ordered|on\s*backorder)|back\s*order(ed)?)$',
     'QtyOnBackorder', 'high', ''),
    (r'^(qty\s*(on\s*order|on\s*p\s*order)|on\s*order)$', 'QtyOnPOrder', 'high', ''),
    (r'^(qty\s*in\s*transit|in\s*transit)$', 'QtyInTransit', 'high', ''),
    (r'^(next\s*(scheduled\s*)?(receipt|availability)\s*date|'
     r'item\s*next\s*availability\s*date|eta)$', 'NextReceiptDate', 'high',
     'must be a real date; prose like "Discontinued" fails the import'),
    (r'^(next\s*receipt\s*qty)$', 'NextReceiptQty', 'high', ''),

    # --- stories
    (r'^(product\s*story|story|romance(\s*copy)?|marketing\s*(copy|description))$',
     'ProductStory', 'high', 'stories.csv, not products.csv'),
]

COMPILED = [(re.compile(p, re.I), f, c, w) for p, f, c, w in ALIASES]


# Tokens that carry meaning on their own, for headers an exact rule cannot reach
# ("Accessory Name/Desciption" - note the client's typo). These are LOW confidence
# by construction: a token match is a question to ask, not a mapping to trust.
TOKEN_HINTS = [
    (r'\bsku\b', 'BaseItemCode'),
    (r'\bgtin\b|\bupc\b|\bean\b', 'UPCValue'),
    (r'\bdesc\w*|\bname\b', 'LongDesc'),
    (r'\bmsrp\b|\bmap\b|\bnet\b|\bprice\b|\bcost\b', 'NetPrice or Price_<code>'),
    (r'\bimage\b|\bphoto\b', 'ImageFileName'),
    (r'\bcategor\w*|\bclass\b', 'CategoryCodes'),
    (r'\bcollection\b|\bseries\b', 'CollectionCodes'),
    (r'\bbrand\b', 'TradeNameCode'),
    (r'\bweight\b', 'ShipWeight'),
    (r'\bqty\b|\bquantity\b', 'a Qty* field'),
    (r'\bterritor\w*|\bsales\s*rep\b', 'TerritoryCodes'),
]
TOKEN_COMPILED = [(re.compile(p, re.I), f) for p, f in TOKEN_HINTS]

# Leading words that qualify a header without changing what it means. Client
# exports prefix everything ("Accessory SKU", "Item Ship Weight").
PREFIXES = re.compile(
    r'^(accessory|item|product|part|customer|bill\s*to|ship\s*to|master|primary|'
    r'default|main|base)\s+', re.I)


def propose(raw_header):
    """Return (ecat_field, confidence, why) or None.

    Tries the whole header, then the header with a qualifying prefix stripped,
    then single-token hints at LOW confidence. Confidence only ever goes down as
    the evidence gets weaker - a prefix-stripped match is never 'certain'.
    """
    h = ' '.join(str(raw_header).strip().split()).lower()
    if not h:
        return None
    for rx, field, conf, why in COMPILED:
        if rx.match(h):
            return field, conf, why

    stripped, n = PREFIXES.subn('', h)
    if n:
        for rx, field, conf, why in COMPILED:
            if rx.match(stripped):
                weaker = {'certain': 'high', 'high': 'moderate'}.get(conf, conf)
                extra = 'matched after dropping the %r prefix' % h[:len(h) - len(stripped)].strip()
                return field, weaker, (why + '; ' + extra) if why else extra
    for rx, field in TOKEN_COMPILED:
        if rx.search(h):
            return field, 'low', ('keyword in the header only - confirm with the '
                                  'client before mapping')
    return None
