#!/usr/bin/env python3
"""
Coaster Furniture Customer File Cleaner
========================================
Fixes import validation errors identified in Jan 20, 2026 standup calls.

Issues Addressed:
1. International addresses (missing state, non-US locations)
2. Email field problems (multiple emails, N/A, line breaks)
3. Missing shipping locations (duplicate billing when missing)
4. Ship-to code preservation for multi-location customers

Usage:
    python clean_coaster_customers.py <input_file.csv> [output_file.csv]
"""

import csv
import re
import sys
from pathlib import Path


# Known international location patterns (city/address -> country code)
INTERNATIONAL_PATTERNS = {
    # Caribbean
    'WEST INDIES': 'INTL',
    'TRINIDAD': 'TT',
    'TOBAGO': 'TT',
    'NASSAU': 'BS',  # Bahamas
    'BAHAMAS': 'BS',
    'FREEPORT': 'BS',
    'ABACO': 'BS',
    'GRAND CAYMAN': 'KY',
    'CAYMAN': 'KY',
    'GEORGE TOWN': 'KY',
    'JAMAICA': 'JM',
    'KINGSTON': 'JM',
    'BARBADOS': 'BB',
    'BRIDGETOWN': 'BB',
    'ST. MICHAEL': 'BB',
    'ST MAARTEN': 'SX',
    'ST.MAARTEN': 'SX',
    'PHILIPSBURG': 'SX',
    'ANTIGUA': 'AG',
    'ST. KITTS': 'KN',
    'TORTOLA': 'VG',
    'ROADTOWN': 'VG',
    'GRENADA': 'GD',
    'ARUBA': 'AW',
    'ORANJESTAD': 'AW',
    'CURACAO': 'CW',
    'BERMUDA': 'BM',
    'HAMILTON BERMUDA': 'BM',
    'TURKS AND CAICOS': 'TC',
    'PROVIDENCIALES': 'TC',
    # Central America
    'PANAMA': 'PA',
    'COSTA RICA': 'CR',
    'SAN JOSE COSTA': 'CR',
    'GUATEMALA': 'GT',
    'HONDURAS': 'HN',
    'SAN PEDRO SULA': 'HN',
    'TEGUCIGALPA': 'HN',
    'LA CEIBA': 'HN',
    'NICARAGUA': 'NI',
    'MANAGUA': 'NI',
    'ESTELI': 'NI',
    'BELIZE': 'BZ',
    'EL SALVADOR': 'SV',
    # South America
    'SURINAME': 'SR',
    'PARAMARIBO': 'SR',
    'COCHABAMBA': 'BO',
    # Mexico (various patterns)
    'MEXICO': 'MX',
    'MEXICALI': 'MX',
    'TIJUANA': 'MX',
    'REYNOSA': 'MX',
    'YUCATAN': 'MX',
    'CHIHUAHUA': 'MX',
    'NAYARIT': 'MX',
    'TAMAULIPAS': 'MX',
    'BUCERIAS': 'MX',
    'MERIDA': 'MX',
    'SONORA': 'MX',
    'MONTERREY': 'MX',
    'NUEVO LEON': 'MX',
    'SALTILLO': 'MX',
    'COAH': 'MX',  # Coahuila
    'CULIACAN': 'MX',
    'SINALOA': 'MX',
    'HERMOSILLO': 'MX',
    'ENSENADA': 'MX',
    'CABO SAN LUCAS': 'MX',
    'LA PAZ, BCS': 'MX',
    'PUERTO PENASCO': 'MX',
    'OBREGON': 'MX',
    'NOGALES': 'MX',
    'QUERETARO': 'MX',
    'GUADALAJARA': 'MX',
    'JALISCO': 'MX',
    'AGUASCALIENTES': 'MX',
    'GUANAJUATO': 'MX',
    'LEON,GTO': 'MX',
    'PIEDRAS NEGRAS': 'MX',
    'DELICIAS': 'MX',
    'JUAREZ': 'MX',
    'ROSARITO': 'MX',
    'GUAMUCHIL': 'MX',
    'LOS MOCHIS': 'MX',
    'TAMPICO': 'MX',
    # Canada
    'CANADA': 'CA',
    'CALGARY': 'CA',
    'EDMONTON': 'CA',
    'ALBERTA': 'CA',
    # Dominican Republic
    'SANTO DOMINGO': 'DO',
    'PUERTO PLATA': 'DO',
    'D.R': 'DO',
    # Haiti
    'PORT-AU-PRINCE': 'HT',
    # Other
    'MONGOLIA': 'MN',
    'ULAANBAATAR': 'MN',
    'GUAM': 'GU',
    'HAGATNA': 'GU',
    'HUGATNA': 'GU',  # Misspelling in data
    # Costa Rica
    'ALAJUELA': 'CR',
    'SAN RAMON': 'CR',
    'PALAU': 'PW',
    'KOROR': 'PW',
    'JORDAN': 'JO',
    'AMMAN': 'JO',
}

# Canadian province codes (valid, but not US states)
CANADIAN_PROVINCES = {'AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT'}

# Mexican state codes (excluding codes that overlap with US states)
# Excluded: CO (Colorado), ME (Maine), MI (Michigan), MO (Missouri), NV (Nevada)
MEXICAN_STATES = {'BA', 'BC', 'BS', 'CH', 'CL', 'CM', 'CS', 'DF', 'DG', 'GR', 'GT', 'HG', 
                  'JA', 'NL', 'OA', 'PB', 'QE', 'QR', 'SI', 'SL', 
                  'SO', 'TB', 'TL', 'TM', 'VE', 'YU', 'ZA'}

# Valid US state codes (including territories) - these take priority over any international pattern matching
US_STATES = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
             'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
             'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
             'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC',
             'PR', 'GU', 'VI', 'AS', 'MP'}  # US territories: Puerto Rico, Guam, Virgin Islands, American Samoa, N. Mariana Islands

# Invalid email placeholders to clear
INVALID_EMAIL_PATTERNS = [
    r'^n/?a$',
    r'^no\s*email',
    r'^none$',
    r'^null$',
    r'^\s*$',
]


def clean_email(email_value):
    """
    Clean email field:
    - Keep only first email if multiple
    - Remove N/A, 'no email', etc.
    - Strip whitespace and newlines
    - Fix common typos (trailing dots, apostrophes)
    """
    if not email_value:
        return ''
    
    # Remove newlines and extra whitespace
    email_value = ' '.join(email_value.split())
    
    # Check for invalid placeholders
    for pattern in INVALID_EMAIL_PATTERNS:
        if re.match(pattern, email_value.strip(), re.IGNORECASE):
            return ''
    
    # Split on semicolon, comma, or space - keep first email only
    # Per eCat spec: "Must be valid email address" (single)
    if ';' in email_value:
        email_value = email_value.split(';')[0].strip()
    elif ',' in email_value and '@' in email_value.split(',')[0]:
        parts = email_value.split(',')
        if '@' in parts[0]:
            email_value = parts[0].strip()
    
    # Also handle space-separated emails (e.g., "email1@x.com email2@x.com")
    if ' ' in email_value and '@' in email_value:
        parts = email_value.split()
        for part in parts:
            if '@' in part and '.' in part:
                email_value = part.strip()
                break
    
    email_value = email_value.strip()
    
    # Fix common email issues:
    # 1. Remove trailing dots (e.g., "email@domain.com." -> "email@domain.com")
    while email_value.endswith('.'):
        email_value = email_value[:-1]
    
    # 2. Remove apostrophes (e.g., "gsaunder's@domain.net" -> "gsaunders@domain.net")
    email_value = email_value.replace("'", "")
    
    # 3. Normalize special characters (ñ -> n, etc.) for ASCII compatibility
    # This handles cases like "Aliña.navarro@domain.net"
    import unicodedata
    email_value = unicodedata.normalize('NFKD', email_value).encode('ASCII', 'ignore').decode('ASCII')
    
    # Final validation - clear if not valid email format
    # Per eCat spec: "Must be valid email address"
    if email_value and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_value):
        return ''  # Clear invalid emails
    
    return email_value


def is_us_zip(postcode):
    """Check if postcode looks like a valid US ZIP code."""
    if not postcode:
        return False
    postcode = postcode.strip()
    # US ZIP: 5 digits, or 5+4 format (12345 or 12345-6789)
    return bool(re.match(r'^\d{5}(-\d{4})?$', postcode))


# Mexico state abbreviations commonly found in city names (e.g., "SAN PEDRO GARZA, NL")
MEXICO_STATE_ABBREVS = {
    ', NL', ',NL', ' NL',  # Nuevo León
    'GARZA GARC',  # Short for García - common in Monterrey area
    'SAN PEDRO GARZA',  # San Pedro Garza García, NL
    ', QRO', ',QRO', 'TEQUISQUIAPAN',  # Querétaro
    'TAMPS', 'TAMAULIPAS', 'VICTORIA TAMPS',  # Tamaulipas
    ', COAH', ',COAH', 'COAHUILA',  # Coahuila
    'MIGUEL ALEMAN',  # Tamaulipas border town
    ', SON', ',SON',  # Sonora - but be careful with English words
    ', BC', ', B.C', 'BAJA',  # Baja California
    ', GTO', ',GTO',  # Guanajuato
    ', JAL', ',JAL',  # Jalisco
    ', SIN', ',SIN',  # Sinaloa
    ', CHIH', ',CHIH',  # Chihuahua
}

# US cities that might have blank state but valid US zip
US_CITY_PATTERNS = {
    'SAN DIEGO', 'LOS ANGELES', 'LAS VEGAS', 'N LAS VEGAS', 'EL PASO',
    'CORONA', 'TORRANCE', 'GARDENA', 'PARAMOUNT', 'WHITTIER', 
    'MISSION VIEJO', 'TRABUCO CANYON', 'PALM DESERT', 'ONTARIO',
    'ELIZABETH',  # NJ
}

# Puerto Rico / US Virgin Islands - these are US territories
# ZIP codes: PR = 006XX-009XX, VI = 008XX
def is_pr_vi_zip(postcode):
    """Check if ZIP is Puerto Rico or US Virgin Islands."""
    if not postcode:
        return False
    postcode = postcode.strip().replace(' ', '')
    # PR/VI zips: 006XX through 009XX (5 digits starting with 00)
    if re.match(r'^00[6-9]\d{2}(-\d{4})?$', postcode):
        return True
    return False


# Puerto Rico city names
PR_CITIES = {
    'CIDRA', 'PONCE', 'HATO REY', 'MOCA', 'COTO LAUREL', 'SAN SEBASTIAN',
    'MANATI', 'BAYAMON', 'CAGUAS', 'MAYAGUEZ', 'ARECIBO', 'GUAYNABO',
    'CAROLINA', 'TRUJILLO ALTO', 'HUMACAO', 'FAJARDO', 'AGUADILLA',
}

# US Virgin Islands
VI_CITIES = {'ST. THOMAS', 'ST THOMAS', 'ST. CROIX', 'ST CROIX', 'ST. JOHN'}


def detect_country(row, prefix='BillTo'):
    """
    Detect if an address is international and return country code.
    Returns 'US' for domestic, or appropriate country code for international.
    """
    city = row.get(f'{prefix}City', '').upper()
    state = row.get(f'{prefix}State', '').upper()
    postcode = row.get(f'{prefix}PostCode', '').upper().strip()
    address1 = row.get(f'{prefix}Address1', '').upper()
    address2 = row.get(f'{prefix}Address2', '').upper()
    country = row.get(f'{prefix}Country', '').upper()
    
    # If country already specified and not US
    if country and country not in ['', 'US', 'USA', 'UNITED STATES']:
        return country
    
    # PRIORITY: If state is a valid US state, assume US
    if state in US_STATES:
        return 'US'
    
    # PRIORITY: Check Puerto Rico / US Virgin Islands BEFORE international patterns
    # (because ST. THOMAS might match other international patterns)
    if is_pr_vi_zip(postcode):
        return 'US'
    for pr_city in PR_CITIES:
        if pr_city in city or ', PR' in city:
            return 'US'
    for vi_city in VI_CITIES:
        if vi_city in city:
            return 'US'
    
    # Check for Mexico state abbreviations in city field (e.g., "SAN PEDRO GARZA, NL")
    for mx_pattern in MEXICO_STATE_ABBREVS:
        if mx_pattern in city:
            return 'MX'
    
    # Check city field for international locations
    for pattern, country_code in INTERNATIONAL_PATTERNS.items():
        if pattern in city or pattern in address1 or pattern in address2 or pattern in postcode:
            return country_code
    
    # Check if state is a Canadian province
    if state in CANADIAN_PROVINCES:
        return 'CA'
    
    # Check if state is Mexican state code (only if not a US state)
    if state in MEXICAN_STATES:
        return 'MX'
    
    # Check postcode field for country names
    if 'MEXICO' in postcode:
        return 'MX'
    if 'BAHAMAS' in postcode:
        return 'BS'
    if 'JAMAICA' in postcode:
        return 'JM'
    if 'ANTIGUA' in postcode:
        return 'AG'
    if 'INDIES' in postcode:
        return 'INTL'
    if 'BARBADOS' in postcode:
        return 'BB'
    if 'GRENADA' in postcode:
        return 'GD'
    if 'PROVID' in postcode:  # NEW PROVIDENCE (Bahamas)
        return 'BS'
    
    # Check for Canadian postal codes (letter-number pattern like V1Z3S2 or A1A 1A1)
    if postcode and re.match(r'^[A-Z]\d[A-Z]\s*\d?[A-Z]?\d?$', postcode):
        return 'CA'
    
    # Check for Cayman postal codes (KY1-XXXX)
    if postcode and postcode.startswith('KY'):
        return 'KY'
    
    # Check for Barbados postal codes (BBXXXXX)
    if postcode and postcode.startswith('BB'):
        return 'BB'
    
    # Check for British Virgin Islands (VG)
    if postcode and postcode.startswith('VG'):
        return 'VG'
    
    # If state is blank, apply additional logic
    if not state or state.strip() == '':
        # Puerto Rico / US Virgin Islands - these are US territories
        if is_pr_vi_zip(postcode):
            return 'US'  # Will handle state separately
        
        # Check for Puerto Rico cities
        for pr_city in PR_CITIES:
            if pr_city in city or ', PR' in city:
                return 'US'  # Puerto Rico is US territory
        
        # Check for US Virgin Islands cities
        for vi_city in VI_CITIES:
            if vi_city in city:
                return 'US'  # US VI is US territory
        
        # Check if city is a known US city
        for us_city in US_CITY_PATTERNS:
            if us_city in city:
                return 'US'  # Valid US city with valid zip but missing state
        
        # Costa Rica patterns
        if 'ALAJUELA' in city or 'SAN RAMON' in city or 'SAN JOSE' in city:
            if postcode.startswith('20') or postcode.startswith('10'):  # Costa Rica zips
                return 'CR'
        
        if not is_us_zip(postcode):
            # State is blank and zip is not valid US format - likely international
            return 'INTL'
    
    return 'US'


def detect_us_territory_state(city, postcode):
    """
    Detect if an address is in a US territory and return the territory code.
    Returns None if not a US territory.
    """
    city_upper = city.upper()
    postcode_clean = postcode.strip().replace(' ', '') if postcode else ''
    
    # Check for Puerto Rico
    for pr_city in PR_CITIES:
        if pr_city in city_upper:
            return 'PR'
    if ', PR' in city_upper or is_pr_vi_zip(postcode_clean):
        # Check if it's a PR zip (006XX-009XX except 008XX which could be VI)
        if postcode_clean.startswith('006') or postcode_clean.startswith('007') or postcode_clean.startswith('009'):
            return 'PR'
    
    # Check for US Virgin Islands (008XX zips, or VI cities)
    for vi_city in VI_CITIES:
        if vi_city in city_upper:
            return 'VI'
    if postcode_clean.startswith('008'):
        return 'VI'
    
    # Check for Guam (969XX zips)
    if 'GUAM' in city_upper or 'HAGATNA' in city_upper or 'HUGATNA' in city_upper:
        return 'GU'
    if postcode_clean.startswith('969'):
        return 'GU'
    
    return None


def normalize_international_address(row, prefix='BillTo'):
    """
    Normalize international addresses:
    - Set country code
    - For international, set state to 'INTL' if blank (prevents validation error)
    - For international, set postcode to '00000' if blank (eCat requires a value)
    - For US territories with blank state, fill in PR/VI/GU
    """
    country = detect_country(row, prefix)
    
    if country != 'US':
        row[f'{prefix}Country'] = country
        
        # If state is blank or contains country name, normalize it
        state = row.get(f'{prefix}State', '').strip()
        if not state or state.upper() in ['MEXICO', 'CANADA', 'YUCATAN']:
            # Keep the original value but ensure it's not empty
            if not state:
                row[f'{prefix}State'] = 'INTL'
        
        # If postal code is blank, set placeholder (eCat requires a value even for international)
        postcode = row.get(f'{prefix}PostCode', '').strip()
        if not postcode:
            row[f'{prefix}PostCode'] = '00000'
    else:
        # Ensure US addresses have country set
        if not row.get(f'{prefix}Country'):
            row[f'{prefix}Country'] = 'US'
        
        # For US territories with blank state, fill in the territory code
        state = row.get(f'{prefix}State', '').strip()
        if not state:
            city = row.get(f'{prefix}City', '')
            postcode = row.get(f'{prefix}PostCode', '')
            territory = detect_us_territory_state(city, postcode)
            if territory:
                row[f'{prefix}State'] = territory
    
    return row


def copy_billing_to_shipping(row):
    """
    If shipping address is missing, copy from billing address.
    Preserves ShipToCode if it exists.
    """
    ship_fields = ['ShipToName', 'ShipToAddress1', 'ShipToAddress2', 
                   'ShipToCity', 'ShipToState', 'ShipToPostCode', 'ShipToCountry']
    bill_fields = ['BillToName', 'BillToAddress1', 'BillToAddress2',
                   'BillToCity', 'BillToState', 'BillToPostCode', 'BillToCountry']
    
    # Check if shipping is essentially empty
    shipping_empty = all(
        not row.get(f, '').strip() 
        for f in ['ShipToAddress1', 'ShipToCity']
    )
    
    if shipping_empty:
        for ship_field, bill_field in zip(ship_fields, bill_fields):
            if not row.get(ship_field, '').strip():
                row[ship_field] = row.get(bill_field, '')
        
        # Also copy email and phone if missing
        if not row.get('ShipToEmail', '').strip():
            row['ShipToEmail'] = row.get('BuyerEmail', '')
        if not row.get('ShipToPhone', '').strip():
            row['ShipToPhone'] = row.get('BuyerPhone', '')
    
    return row


def truncate_address(address, max_length=60):
    """
    Truncate address to max_length characters.
    eCat has a 60-character limit on address fields.
    """
    if not address:
        return address
    address = address.strip()
    if len(address) <= max_length:
        return address
    # Truncate and clean up (don't end mid-word if possible)
    truncated = address[:max_length]
    # Try to break at a space or semicolon
    last_space = truncated.rfind(' ')
    last_semi = truncated.rfind(';')
    break_point = max(last_space, last_semi)
    if break_point > max_length - 15:  # Only break at word if reasonable
        truncated = truncated[:break_point]
    return truncated.strip()


def clean_row(row):
    """Apply all cleaning operations to a single row."""
    
    # Remove any None keys (from malformed CSV rows)
    row = {k: v for k, v in row.items() if k is not None}
    
    # 1. Clean email fields
    if 'BuyerEmail' in row:
        row['BuyerEmail'] = clean_email(row['BuyerEmail'])
    if 'ShipToEmail' in row:
        row['ShipToEmail'] = clean_email(row['ShipToEmail'])
    
    # 2. Truncate address fields to 60 chars (eCat limit)
    for field in ['BillToAddress1', 'BillToAddress2', 'ShipToAddress1', 'ShipToAddress2']:
        if field in row:
            row[field] = truncate_address(row[field], 60)
    
    # 3. Normalize international addresses (BillTo)
    row = normalize_international_address(row, 'BillTo')
    
    # 4. Normalize international addresses (ShipTo)
    row = normalize_international_address(row, 'ShipTo')
    
    # 5. Copy billing to shipping if missing
    row = copy_billing_to_shipping(row)
    
    return row


def process_file(input_path, output_path):
    """Process the CSV file and output cleaned version."""
    
    stats = {
        'total_rows': 0,
        'emails_cleaned': 0,
        'international_addresses': 0,
        'shipping_copied': 0,
        'errors': []
    }
    
    # Read the input file - use csv module's built-in multiline handling
    with open(input_path, 'r', encoding='utf-8-sig', errors='replace', newline='') as infile:
        # Use csv.DictReader directly - it handles quoted multiline fields
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        rows = []
        for i, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            try:
                original_email = row.get('BuyerEmail', '')
                original_ship_addr = row.get('ShipToAddress1', '')
                original_country = row.get('BillToCountry', '')
                
                cleaned_row = clean_row(row)
                rows.append(cleaned_row)
                stats['total_rows'] += 1
                
                # Track what changed
                if cleaned_row.get('BuyerEmail', '') != original_email:
                    stats['emails_cleaned'] += 1
                if cleaned_row.get('BillToCountry', '') != original_country and cleaned_row.get('BillToCountry', '') != 'US':
                    stats['international_addresses'] += 1
                if cleaned_row.get('ShipToAddress1', '') != original_ship_addr and not original_ship_addr:
                    stats['shipping_copied'] += 1
                    
            except Exception as e:
                stats['errors'].append(f"Row {i}: {str(e)}")
    
    # Sort by BillToCode before writing (required by eCat spec)
    # Per KB: "The customer file must be sorted by BillToCode before importing"
    def sort_key(row):
        code = row.get('BillToCode', '')
        # Try numeric sort first, fall back to string
        try:
            return (0, int(code), row.get('ShipToCode', ''))
        except (ValueError, TypeError):
            return (1, code, row.get('ShipToCode', ''))
    
    rows.sort(key=sort_key)
    
    # Write the output file
    with open(output_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return stats


def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_coaster_customers.py <input_file.csv> [output_file.csv]")
        print("\nThis script cleans the Coaster customer import file by:")
        print("  1. Fixing international addresses (adds country code, normalizes state)")
        print("  2. Cleaning email fields (keeps first email, removes N/A)")
        print("  3. Copying billing to shipping when shipping is missing")
        print("  4. Preserving ship-to codes for multi-location customers")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"{input_path.stem}_CLEANED{input_path.suffix}"
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    print(f"Processing: {input_path}")
    print(f"Output to:  {output_path}")
    print("-" * 50)
    
    stats = process_file(input_path, output_path)
    
    print(f"\n✅ Processing Complete!")
    print(f"   Total rows processed: {stats['total_rows']}")
    print(f"   Emails cleaned:       {stats['emails_cleaned']}")
    print(f"   International addrs:  {stats['international_addresses']}")
    print(f"   Shipping copied:      {stats['shipping_copied']}")
    
    if stats['errors']:
        print(f"\n⚠️  Errors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:10]:
            print(f"   - {error}")
        if len(stats['errors']) > 10:
            print(f"   ... and {len(stats['errors']) - 10} more")
    
    print(f"\n📁 Cleaned file saved to: {output_path}")


if __name__ == '__main__':
    main()
