#!/usr/bin/env python3
"""
Check if discontinued items (marked with "Disc" in description) explain the discrepancy.
"""

import pandas as pd
import sys
import re

def normalize_code(code):
    """Remove all dashes, hyphens, and spaces from item code."""
    if pd.isna(code):
        return ""
    return re.sub(r'[-\s]', '', str(code))

def check_discontinued():
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
        
        # Combine inventory files
        inventory_df = pd.concat([nsl_df, ml_df], ignore_index=True)
        
        # Check for discontinued items
        print("\n" + "="*80)
        print("DISCONTINUED ITEMS ANALYSIS")
        print("="*80)
        
        # Find items with "Disc" at the start of description
        disc_items = inventory_df[
            inventory_df['Item Description'].str.startswith('Disc', na=False)
        ].copy()
        
        print(f"\nFound {len(disc_items)} rows with 'Disc' at start of Item Description")
        
        # Get unique discontinued item numbers
        disc_item_numbers = disc_items['Item Number'].dropna().unique()
        print(f"Unique discontinued Item Numbers: {len(disc_item_numbers)}")
        
        # Show sample
        print("\nSample of discontinued items:")
        for i, row in disc_items.head(20).iterrows():
            print(f"  • {row['Item Number']}: {row['Item Description']}")
        
        if len(disc_items) > 20:
            print(f"  ... and {len(disc_items) - 20} more rows")
        
        # Now check: of the 134 items in inventory but not in products (normalized), 
        # how many are discontinued?
        
        # Get normalized sets
        nsl_df['Item_Normalized'] = nsl_df['Item Number'].apply(normalize_code)
        ml_df['Item_Normalized'] = ml_df['Item Number'].apply(normalize_code)
        products_df['BaseItemCode_Normalized'] = products_df['BaseItemCode'].apply(normalize_code)
        
        nsl_items_norm = set(nsl_df['Item_Normalized'].dropna())
        ml_items_norm = set(ml_df['Item_Normalized'].dropna())
        combined_inventory_norm = nsl_items_norm.union(ml_items_norm)
        products_items_norm = set(products_df['BaseItemCode_Normalized'].dropna())
        
        # Remove empty strings
        combined_inventory_norm.discard('')
        products_items_norm.discard('')
        
        in_inv_not_prod_norm = combined_inventory_norm - products_items_norm
        
        # Get normalized discontinued items
        disc_items_norm = set(disc_items['Item Number'].apply(normalize_code).dropna())
        disc_items_norm.discard('')
        
        # Find overlap
        disc_in_discrepancy = in_inv_not_prod_norm.intersection(disc_items_norm)
        non_disc_in_discrepancy = in_inv_not_prod_norm - disc_items_norm
        
        print("\n" + "="*80)
        print("EXPLAINING THE 134 ITEM DISCREPANCY (normalized)")
        print("="*80)
        print(f"Items in inventory but NOT in products CSV: {len(in_inv_not_prod_norm)}")
        print(f"  • Discontinued items: {len(disc_in_discrepancy)} ({len(disc_in_discrepancy)/len(in_inv_not_prod_norm)*100:.1f}%)")
        print(f"  • Non-discontinued items: {len(non_disc_in_discrepancy)} ({len(non_disc_in_discrepancy)/len(in_inv_not_prod_norm)*100:.1f}%)")
        
        if len(disc_in_discrepancy) > 0:
            print(f"\n✅ HYPOTHESIS CONFIRMED!")
            print(f"   {len(disc_in_discrepancy)} of the 134 discrepancy items are DISCONTINUED")
            print(f"   These items are still in physical inventory but no longer in the product catalog")
        
        # Show the discontinued items in discrepancy
        if disc_in_discrepancy:
            print(f"\nDiscontinued items in inventory but NOT in products CSV:")
            
            # Create reverse mapping
            norm_to_orig = {}
            for idx, row in inventory_df.iterrows():
                norm = normalize_code(row['Item Number'])
                if norm and norm not in norm_to_orig:
                    norm_to_orig[norm] = row['Item Number']
            
            for i, norm_code in enumerate(sorted(disc_in_discrepancy), 1):
                orig_code = norm_to_orig.get(norm_code, norm_code)
                # Get description
                desc_rows = disc_items[disc_items['Item Number'] == orig_code]
                if len(desc_rows) > 0:
                    desc = desc_rows.iloc[0]['Item Description']
                    print(f"{i:3d}. {orig_code}: {desc}")
                else:
                    print(f"{i:3d}. {orig_code}")
        
        # Show non-discontinued items still in discrepancy
        if non_disc_in_discrepancy:
            print(f"\n" + "="*80)
            print(f"REMAINING {len(non_disc_in_discrepancy)} NON-DISCONTINUED ITEMS NOT IN PRODUCTS")
            print("="*80)
            
            # Create reverse mapping
            norm_to_orig_all = {}
            for idx, row in pd.concat([nsl_df, ml_df]).iterrows():
                norm = normalize_code(row['Item Number'])
                if norm and norm not in norm_to_orig_all:
                    norm_to_orig_all[norm] = row['Item Number']
            
            print(f"\nFirst 30 items:")
            for i, norm_code in enumerate(sorted(list(non_disc_in_discrepancy))[:30], 1):
                orig_code = norm_to_orig_all.get(norm_code, norm_code)
                
                # Get description if available
                desc_rows = inventory_df[inventory_df['Item Number'] == orig_code]
                if len(desc_rows) > 0:
                    desc = desc_rows.iloc[0]['Item Description']
                    print(f"{i:3d}. {orig_code}: {desc[:60]}...")
                else:
                    print(f"{i:3d}. {orig_code}")
            
            if len(non_disc_in_discrepancy) > 30:
                print(f"     ... and {len(non_disc_in_discrepancy) - 30} more")
        
        # Pattern analysis of non-discontinued items
        print("\n" + "="*80)
        print("PATTERN ANALYSIS OF REMAINING NON-DISCONTINUED ITEMS")
        print("="*80)
        
        prefixes = {}
        for norm_code in non_disc_in_discrepancy:
            orig_code = norm_to_orig_all.get(norm_code, norm_code)
            prefix = orig_code.split('-')[0] if '-' in orig_code else orig_code[:3]
            prefixes[prefix] = prefixes.get(prefix, 0) + 1
        
        print("\nTop 10 prefixes:")
        for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {prefix}: {count} items")
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"\nOriginal discrepancy: 159 items")
        print(f"After normalization: 134 items")
        print(f"Discontinued items: {len(disc_in_discrepancy)} items")
        print(f"Remaining unexplained: {len(non_disc_in_discrepancy)} items")
        print(f"\nPercentage explained by discontinued items: {len(disc_in_discrepancy)/134*100:.1f}%")
        
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
    check_discontinued()
