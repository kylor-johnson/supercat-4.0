#!/usr/bin/env python3
"""
Check GDL items specifically to understand the matching pattern.
"""

import pandas as pd
import sys
import re

def normalize_code(code):
    """Remove all dashes, hyphens, and spaces from item code."""
    if pd.isna(code):
        return ""
    return re.sub(r'[-\s]', '', str(code))

def check_gdl():
    # File paths
    nsl_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/NSL  INV LIST.xlsx"
    ml_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/ML  INV LIST.xlsx"
    products_file = "/Users/kylorjohnson/Downloads/products.csv.20260126-1148.csv"
    
    try:
        # Read all files
        print("Reading files...")
        nsl_df = pd.read_excel(nsl_file)
        ml_df = pd.read_excel(ml_file)
        products_df = pd.read_csv(products_file)
        
        # Get all GDL items from each source
        print("\n" + "="*80)
        print("GDL ITEMS IN INVENTORY FILES")
        print("="*80)
        
        nsl_gdl = nsl_df[nsl_df['Item Number'].str.startswith('GDL', na=False)]['Item Number'].tolist()
        ml_gdl = ml_df[ml_df['Item Number'].str.startswith('GDL', na=False)]['Item Number'].tolist()
        
        all_inv_gdl = sorted(set(nsl_gdl + ml_gdl))
        
        print(f"\nFound {len(all_inv_gdl)} unique GDL items in inventory:")
        for item in all_inv_gdl:
            source = []
            if item in nsl_gdl:
                source.append("NSL")
            if item in ml_gdl:
                source.append("ML")
            print(f"  • {item} [{', '.join(source)}]")
        
        # Get all GDL items from products
        print("\n" + "="*80)
        print("GDL ITEMS IN PRODUCTS CSV")
        print("="*80)
        
        products_gdl = products_df[products_df['BaseItemCode'].str.startswith('GDL', na=False)]['BaseItemCode'].tolist()
        products_gdl_sorted = sorted(set(products_gdl))
        
        print(f"\nFound {len(products_gdl_sorted)} unique GDL items in products CSV:")
        for item in products_gdl_sorted:
            print(f"  • {item}")
        
        # Compare
        print("\n" + "="*80)
        print("COMPARISON")
        print("="*80)
        
        inv_gdl_set = set(all_inv_gdl)
        prod_gdl_set = set(products_gdl_sorted)
        
        in_both = inv_gdl_set.intersection(prod_gdl_set)
        in_inv_not_prod = inv_gdl_set - prod_gdl_set
        in_prod_not_inv = prod_gdl_set - inv_gdl_set
        
        print(f"\nGDL items in BOTH: {len(in_both)}")
        if in_both:
            for item in sorted(in_both):
                print(f"  ✓ {item}")
        
        print(f"\nGDL items in INVENTORY but NOT in products: {len(in_inv_not_prod)}")
        if in_inv_not_prod:
            for item in sorted(in_inv_not_prod):
                print(f"  ✗ {item}")
        
        print(f"\nGDL items in PRODUCTS but NOT in inventory: {len(in_prod_not_inv)}")
        if in_prod_not_inv:
            for item in sorted(in_prod_not_inv):
                print(f"  ⚠ {item}")
        
        # Check with normalization
        print("\n" + "="*80)
        print("NORMALIZED COMPARISON (no dashes)")
        print("="*80)
        
        inv_gdl_norm = {normalize_code(x): x for x in all_inv_gdl}
        prod_gdl_norm = {normalize_code(x): x for x in products_gdl_sorted}
        
        inv_gdl_norm_set = set(inv_gdl_norm.keys())
        prod_gdl_norm_set = set(prod_gdl_norm.keys())
        
        in_both_norm = inv_gdl_norm_set.intersection(prod_gdl_norm_set)
        in_inv_not_prod_norm = inv_gdl_norm_set - prod_gdl_norm_set
        
        print(f"\nGDL items in BOTH (normalized): {len(in_both_norm)}")
        if in_both_norm:
            for norm in sorted(in_both_norm):
                print(f"  ✓ {inv_gdl_norm[norm]} → {prod_gdl_norm[norm]} (normalized: {norm})")
        
        print(f"\nGDL items in INVENTORY but NOT in products (normalized): {len(in_inv_not_prod_norm)}")
        if in_inv_not_prod_norm:
            for norm in sorted(in_inv_not_prod_norm):
                print(f"  ✗ {inv_gdl_norm[norm]} (normalized: {norm})")
        
        # Pattern analysis
        print("\n" + "="*80)
        print("PATTERN ANALYSIS")
        print("="*80)
        
        print("\nInventory GDL items NOT in products - looking for patterns:")
        for item in sorted(in_inv_not_prod):
            # Parse the item code
            parts = item.split('-')
            print(f"  {item}")
            print(f"    Parts: {parts}")
            
            # Check if similar items exist in products
            similar = [p for p in products_gdl_sorted if parts[0] == p.split('-')[0] and parts[1] == p.split('-')[1]]
            if similar:
                print(f"    Similar in products: {similar}")
        
        print("\n" + "="*80)
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    check_gdl()
