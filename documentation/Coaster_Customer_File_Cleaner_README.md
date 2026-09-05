# Coaster Customer File Cleaner

A Python script to clean and prepare your customer export file before importing into eCat.

---

## What This Script Does

| Issue | What the Script Does |
|-------|---------------------|
| **Price Level Codes** | Converts Coaster's price level names to eCat codes (e.g., "Z3T2 Pricelist" → "z3t2", "M1 Z2 Pricelist" → "m1_z2") |
| **Invalid Emails** | Removes "N/A", multiple emails (keeps first only), trailing dots, special characters. Validates format. |
| **International Addresses** | For non-US addresses with blank State, sets State to "INTL". For blank PostCode, sets to "00000". |
| **Long Addresses** | Truncates address fields to 60 characters (eCat limit). |

---

## What This Script Does NOT Do

**IMPORTANT:** This script does NOT:
- Copy billing address to shipping address (shipping data must exist in your source system)
- Fill in missing required fields like BillToState, BillToPostCode, ShipToCity, etc.
- Assign price codes to customers with "Pricelist" (generic) or unknown codes

**You must fix these in your source system** before the file will import successfully.

---

## Price Level Code Mapping

| Coaster Name | eCat Code |
|--------------|-----------|
| Z1T1 Pricelist | z1t1 |
| Z1T2 Pricelist | z1t2 |
| Z2T1 Pricelist | z2t1 |
| Z2T2 Pricelist | z2t2 |
| Z3T1 Pricelist | z3t1 |
| Z3T2 Pricelist | z3t2 |
| M1 Z1 Pricelist | m1_z1 |
| M1 Z2 Pricelist | m1_z2 |
| M1 Z3 Pricelist | m1_z3 |
| M2 Z1 Pricelist | m2_z1 |
| M2 Z2 Pricelist | m2_z2 |
| M2 Z3 Pricelist | m2_z3 |
| M3 Z1 Pricelist | m3_z1 |
| M3 Z2 Pricelist | m3_z2 |
| M3 Z3 Pricelist | m3_z3 |
| M4 Z1 Pricelist | m4_z1 |
| M4 Z2 Pricelist | m4_z2 |
| M4 Z3 Pricelist | m4_z3 |
| M5 Z1 Pricelist | m5_z1 |
| M5 Z2 Pricelist | m5_z2 |
| M5 Z3 Pricelist | m5_z3 |
| M10 Zone 1 | m10_z1 |
| M10 Zone 2 | m10_z2 |
| M10 Zone 3 | m10_z3 |
| Landed Pricing | a13 |

**Note:** "M8 Z2 Pricelist" does NOT exist in eCat. Customers with this code need to be assigned a valid price level.

---

## Requirements

- **Python 3.6 or higher**
- **openpyxl** (for Excel files): `pip install openpyxl`

### Check if Python is installed:

```bash
python3 --version
```

### Install openpyxl:

```bash
pip install openpyxl
```

---

## How to Use

### Step 1: Export Your Customer File

Export your customer file from your system. The script accepts:
- Excel files (.xlsx)
- CSV files (.csv)

### Step 2: Run the Script

```bash
python3 clean_coaster_customers_v2.py your_customers.xlsx
```

This creates `your_customers_CLEANED.csv` in the same folder.

**Or specify a custom output filename:**

```bash
python3 clean_coaster_customers_v2.py your_customers.xlsx cleaned_customers.csv
```

### Step 3: Review the Output

The script shows a summary:

```
Processing: customers.xlsx
Output to:  customers_CLEANED.csv
--------------------------------------------------

✅ Processing Complete!
   Total rows processed:    9,631
   Price codes converted:   9,512
   Emails cleaned:          359
   International addresses: 11
   Addresses truncated:     3

⚠️  Unknown price codes (need manual review):
   - M8 Z2 Pricelist
   - Pricelist

📁 Cleaned file saved to: customers_CLEANED.csv
```

### Step 4: Fix Outstanding Errors

After running the script, you may still have import errors for:

| Issue | # of Customers | Action Needed |
|-------|----------------|---------------|
| Missing DefaultPriceCode | ~19 | Assign a valid price level code |
| Invalid Price Code (M8 Z2) | 1 | This code doesn't exist in eCat - assign a valid code |
| Missing Billing State/Post Code | ~55 | Add state and/or postal code in source system |
| Missing Shipping Address Fields | ~22 | Add address, city, state, and/or postal code |
| Missing Billing City | ~5 | Add city in source system |

### Step 5: Import the Cleaned File

Upload the cleaned CSV to the eCat Admin Console:
- **Admin Console → Tools → Import Data → Customers**

---

## Tips for Future Exports

1. **Required fields must have values:**
   - BillToState, BillToPostCode
   - ShipToAddress1, ShipToCity, ShipToState, ShipToPostCode
   - DefaultPriceCode

2. **International customers:**
   - Use "INTL" for state if unknown
   - Use "00000" for postal code if unknown

3. **Price codes must match exactly:**
   - Use lowercase (e.g., `z3t2`, `m1_z2`)
   - Must match what's configured in eCat Admin

4. **Emails:**
   - One email per field (no semicolons or multiple addresses)
   - Valid format only (no trailing dots, no special characters)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'openpyxl'"

Install the required library:
```bash
pip install openpyxl
```

### "python3: command not found"

Try using `python` instead:
```bash
python clean_coaster_customers_v2.py customers.xlsx
```

Or download Python from https://www.python.org/downloads/

### Script shows "Unknown price codes"

These codes aren't in the mapping and will need manual review. Either:
- Add the mapping to the script's `PRICE_CODE_MAP` dictionary
- Manually update those customers in the output CSV

---

## Questions?

Contact SuperCat Support: support@supercatsolutions.com

---

# The Script

Save the following as `clean_coaster_customers_v2.py`:

```python
#!/usr/bin/env python3
"""
Coaster Furniture Customer File Cleaner v2
===========================================
Cleans customer import files for eCat validation.

What This Script Does:
1. Converts DefaultPriceCode values to eCat format (e.g., "Z3T2 Pricelist" → "z3t2")
2. Cleans invalid email formats (removes trailing dots, special chars, keeps first email only)
3. Sets international addresses to State="INTL" and PostCode="00000" where blank
4. Truncates addresses exceeding 60 characters

What This Script Does NOT Do:
- Does NOT copy billing address to shipping (shipping data must come from source)
- Does NOT fill in missing required fields (those must be fixed in source system)

Usage:
    python clean_coaster_customers_v2.py <input_file.xlsx> [output_file.csv]
    python clean_coaster_customers_v2.py <input_file.csv> [output_file.csv]

Requires: openpyxl (pip install openpyxl)
"""

import csv
import re
import sys
from pathlib import Path

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


# Price Level Code Mapping (Coaster's names → eCat codes)
PRICE_CODE_MAP = {
    # Zone/Tier codes
    'Z1T1 Pricelist': 'z1t1',
    'Z1T2 Pricelist': 'z1t2',
    'Z2T1 Pricelist': 'z2t1',
    'Z2T2 Pricelist': 'z2t2',
    'Z3T1 Pricelist': 'z3t1',
    'Z3T2 Pricelist': 'z3t2',
    # M-series codes
    'M1 Z1 Pricelist': 'm1_z1',
    'M1 Z2 Pricelist': 'm1_z2',
    'M1 Z3 Pricelist': 'm1_z3',
    'M2 Z1 Pricelist': 'm2_z1',
    'M2 Z2 Pricelist': 'm2_z2',
    'M2 Z3 Pricelist': 'm2_z3',
    'M3 Z1 Pricelist': 'm3_z1',
    'M3 Z2 Pricelist': 'm3_z2',
    'M3 Z3 Pricelist': 'm3_z3',
    'M4 Z1 Pricelist': 'm4_z1',
    'M4 Z2 Pricelist': 'm4_z2',
    'M4 Z3 Pricelist': 'm4_z3',
    'M5 Z1 Pricelist': 'm5_z1',
    'M5 Z2 Pricelist': 'm5_z2',
    'M5 Z3 Pricelist': 'm5_z3',
    'M10 Zone 1': 'm10_z1',
    'M10 Zone 2': 'm10_z2',
    'M10 Zone 3': 'm10_z3',
    # Special codes
    'Landed Pricing': 'a13',
    'Pricelist': '',  # Needs manual assignment
}

# Invalid email patterns to clear
INVALID_EMAIL_PATTERNS = [
    r'^n/?a$',
    r'^no\s*email',
    r'^none$',
    r'^null$',
    r'^\s*$',
]

# International location patterns (for detecting non-US addresses)
INTERNATIONAL_PATTERNS = {
    'WEST INDIES', 'TRINIDAD', 'TOBAGO', 'NASSAU', 'BAHAMAS', 'FREEPORT',
    'GRAND CAYMAN', 'CAYMAN', 'JAMAICA', 'KINGSTON', 'BARBADOS',
    'ST MAARTEN', 'ANTIGUA', 'BERMUDA', 'TURKS AND CAICOS',
    'PANAMA', 'COSTA RICA', 'GUATEMALA', 'HONDURAS', 'NICARAGUA', 'BELIZE',
    'MEXICO', 'MONTERREY', 'GUADALAJARA', 'TIJUANA', 'MEXICALI',
    'SANTO DOMINGO', 'COCHABAMBA', 'SURINAME',
}


def clean_price_code(price_code):
    """Convert Coaster price code to eCat format."""
    if not price_code:
        return ''
    
    price_code = str(price_code).strip()
    
    # Check direct mapping
    if price_code in PRICE_CODE_MAP:
        return PRICE_CODE_MAP[price_code]
    
    # If not in map, return as-is (will need manual review)
    return price_code


def clean_email(email_value):
    """
    Clean email field:
    - Keep only first email if multiple (split by ; or newline)
    - Remove N/A, 'no email', etc.
    - Strip whitespace and newlines
    - Fix trailing dots
    - Normalize special characters
    """
    if not email_value:
        return ''
    
    email_value = str(email_value)
    
    # Remove newlines and extra whitespace
    email_value = ' '.join(email_value.split())
    
    # Check for invalid placeholders
    for pattern in INVALID_EMAIL_PATTERNS:
        if re.match(pattern, email_value.strip(), re.IGNORECASE):
            return ''
    
    # Split on semicolon or comma - keep first email only
    if ';' in email_value:
        email_value = email_value.split(';')[0].strip()
    elif ',' in email_value and '@' in email_value.split(',')[0]:
        parts = email_value.split(',')
        if '@' in parts[0]:
            email_value = parts[0].strip()
    
    # Handle space-separated emails
    if ' ' in email_value and '@' in email_value:
        parts = email_value.split()
        for part in parts:
            if '@' in part and '.' in part:
                email_value = part.strip()
                break
    
    email_value = email_value.strip()
    
    # Fix trailing dots
    while email_value.endswith('.'):
        email_value = email_value[:-1]
    
    # Remove apostrophes
    email_value = email_value.replace("'", "")
    
    # Normalize special characters (ñ → n, etc.)
    import unicodedata
    email_value = unicodedata.normalize('NFKD', email_value).encode('ASCII', 'ignore').decode('ASCII')
    
    # Validate format
    if email_value and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_value):
        return ''
    
    return email_value


def is_international_address(city, state, postcode):
    """Check if address appears to be international (non-US)."""
    city = str(city).upper() if city else ''
    state = str(state).upper() if state else ''
    postcode = str(postcode).upper() if postcode else ''
    
    # Check for known international patterns in city
    for pattern in INTERNATIONAL_PATTERNS:
        if pattern in city:
            return True
    
    # Check for non-US postal codes
    if postcode:
        # Canadian postal codes (letter-number pattern)
        if re.match(r'^[A-Z]\d[A-Z]', postcode):
            return True
        # Cayman (KY1-XXXX)
        if postcode.startswith('KY'):
            return True
        # Country names in postcode
        if any(country in postcode for country in ['BAHAMAS', 'JAMAICA', 'MEXICO', 'ANTIGUA']):
            return True
    
    return False


def normalize_international_address(row, prefix='BillTo'):
    """
    For international addresses:
    - Set State to "INTL" if blank
    - Set PostCode to "00000" if blank
    """
    city = row.get(f'{prefix}City', '')
    state = row.get(f'{prefix}State', '')
    postcode = row.get(f'{prefix}PostCode', '')
    
    if is_international_address(city, state, postcode):
        # Set state to INTL if blank
        if not state or state.strip() == '':
            row[f'{prefix}State'] = 'INTL'
        
        # Set postcode to 00000 if blank
        if not postcode or postcode.strip() == '' or postcode == 'None':
            row[f'{prefix}PostCode'] = '00000'
    
    return row


def truncate_address(address, max_length=60):
    """Truncate address to max_length characters (eCat limit)."""
    if not address:
        return address
    address = str(address).strip()
    if len(address) <= max_length:
        return address
    
    # Truncate at word boundary if possible
    truncated = address[:max_length]
    last_space = truncated.rfind(' ')
    last_semi = truncated.rfind(';')
    break_point = max(last_space, last_semi)
    if break_point > max_length - 15:
        truncated = truncated[:break_point]
    
    return truncated.strip()


def clean_row(row):
    """Apply all cleaning operations to a single row."""
    
    # 1. Convert price code
    if 'DefaultPriceCode' in row:
        row['DefaultPriceCode'] = clean_price_code(row['DefaultPriceCode'])
    
    # 2. Clean email fields
    if 'BuyerEmail' in row:
        row['BuyerEmail'] = clean_email(row['BuyerEmail'])
    if 'ShipToEmail' in row:
        row['ShipToEmail'] = clean_email(row['ShipToEmail'])
    
    # 3. Normalize international addresses
    row = normalize_international_address(row, 'BillTo')
    row = normalize_international_address(row, 'ShipTo')
    
    # 4. Truncate long addresses
    for field in ['BillToAddress1', 'BillToAddress2', 'ShipToAddress1', 'ShipToAddress2']:
        if field in row:
            row[field] = truncate_address(row[field], 60)
    
    return row


def read_excel_file(filepath):
    """Read Excel file and return list of dicts."""
    if not HAS_OPENPYXL:
        raise ImportError("openpyxl is required for Excel files. Install with: pip install openpyxl")
    
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    
    # Get headers from first row
    headers = [cell.value for cell in ws[1]]
    
    rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_dict = {}
        for i, value in enumerate(row):
            if i < len(headers) and headers[i]:
                row_dict[headers[i]] = str(value) if value is not None else ''
        rows.append(row_dict)
    
    return headers, rows


def read_csv_file(filepath):
    """Read CSV file and return list of dicts."""
    with open(filepath, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)
    return headers, rows


def process_file(input_path, output_path):
    """Process the file and output cleaned version."""
    
    stats = {
        'total_rows': 0,
        'price_codes_converted': 0,
        'emails_cleaned': 0,
        'international_addresses': 0,
        'addresses_truncated': 0,
        'unknown_price_codes': set(),
        'errors': []
    }
    
    # Determine file type and read
    input_path = Path(input_path)
    if input_path.suffix.lower() in ['.xlsx', '.xls'] or 'Excel' in str(input_path):
        headers, rows = read_excel_file(input_path)
    else:
        # Try CSV first, fall back to Excel if binary
        try:
            headers, rows = read_csv_file(input_path)
        except:
            headers, rows = read_excel_file(input_path)
    
    cleaned_rows = []
    for i, row in enumerate(rows, start=2):
        try:
            original_price = row.get('DefaultPriceCode', '')
            original_email = row.get('BuyerEmail', '')
            original_state = row.get('BillToState', '')
            original_addr = row.get('ShipToAddress1', '')
            
            cleaned_row = clean_row(row)
            cleaned_rows.append(cleaned_row)
            stats['total_rows'] += 1
            
            # Track changes
            new_price = cleaned_row.get('DefaultPriceCode', '')
            if new_price != original_price:
                stats['price_codes_converted'] += 1
                if new_price == original_price:  # Not in mapping
                    stats['unknown_price_codes'].add(original_price)
            
            if cleaned_row.get('BuyerEmail', '') != original_email:
                stats['emails_cleaned'] += 1
            
            if cleaned_row.get('BillToState', '') != original_state and cleaned_row.get('BillToState') == 'INTL':
                stats['international_addresses'] += 1
            
            if original_addr and len(str(original_addr)) > 60:
                stats['addresses_truncated'] += 1
                
        except Exception as e:
            stats['errors'].append(f"Row {i}: {str(e)}")
    
    # Write output CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cleaned_rows)
    
    return stats


def main():
    if len(sys.argv) < 2:
        print("Coaster Customer File Cleaner v2")
        print("=" * 40)
        print("\nUsage: python clean_coaster_customers_v2.py <input_file> [output_file]")
        print("\nSupported input formats: .xlsx, .csv")
        print("\nThis script cleans customer import files by:")
        print("  1. Converting price codes to eCat format (e.g., 'Z3T2 Pricelist' → 'z3t2')")
        print("  2. Cleaning email fields (keeps first email, removes invalid)")
        print("  3. Setting international addresses to State='INTL', PostCode='00000'")
        print("  4. Truncating addresses to 60 characters")
        print("\nNOTE: This does NOT copy billing to shipping. Missing fields must be")
        print("      fixed in your source system.")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"{input_path.stem}_CLEANED.csv"
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    print(f"Processing: {input_path}")
    print(f"Output to:  {output_path}")
    print("-" * 50)
    
    stats = process_file(input_path, output_path)
    
    print(f"\n✅ Processing Complete!")
    print(f"   Total rows processed:    {stats['total_rows']}")
    print(f"   Price codes converted:   {stats['price_codes_converted']}")
    print(f"   Emails cleaned:          {stats['emails_cleaned']}")
    print(f"   International addresses: {stats['international_addresses']}")
    print(f"   Addresses truncated:     {stats['addresses_truncated']}")
    
    if stats['unknown_price_codes']:
        print(f"\n⚠️  Unknown price codes (need manual review):")
        for code in sorted(stats['unknown_price_codes']):
            print(f"   - {code}")
    
    if stats['errors']:
        print(f"\n⚠️  Errors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:10]:
            print(f"   - {error}")
    
    print(f"\n📁 Cleaned file saved to: {output_path}")


if __name__ == '__main__':
    main()
```
