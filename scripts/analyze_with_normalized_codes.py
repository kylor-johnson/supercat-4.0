#!/usr/bin/env python3
"""
Analyze inventory vs products with normalized item codes (removing dashes/hyphens).
"""

import pandas as pd
import sys
import re

def normalize_code(code):
    """Remove all dashes, hyphens, and spaces from item code."""
    if pd.isna(code):
        return ""
    return re.sub(r'[-\s]', '', str(code))

def analyze_normalized():
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
        
        print("\n" + "="*80)
        print("ORIGINAL (WITH DASHES) ANALYSIS")
        print("="*80)
        
        # Original analysis
        nsl_items_orig = set(nsl_df['Item Number'].dropna().astype(str))
        ml_items_orig = set(ml_df['Item Number'].dropna().astype(str))
        combined_inventory_orig = nsl_items_orig.union(ml_items_orig)
        products_items_orig = set(products_df['BaseItemCode'].dropna().astype(str))
        
        in_both_orig = combined_inventory_orig.intersection(products_items_orig)
        in_inv_not_prod_orig = combined_inventory_orig - products_items_orig
        
        print(f"NSL unique items: {len(nsl_items_orig)}")
        print(f"ML unique items: {len(ml_items_orig)}")
        print(f"Combined inventory (deduplicated): {len(combined_inventory_orig)}")
        print(f"Products CSV: {len(products_items_orig)}")
        print(f"Items in BOTH: {len(in_both_orig)}")
        print(f"Items in inventory but NOT in products: {len(in_inv_not_prod_orig)}")
        
        # Normalized analysis
        print("\n" + "="*80)
        print("NORMALIZED (NO DASHES) ANALYSIS")
        print("="*80)
        
        # Create normalized versions
        nsl_df['Item_Normalized'] = nsl_df['Item Number'].apply(normalize_code)
        ml_df['Item_Normalized'] = ml_df['Item Number'].apply(normalize_code)
        products_df['BaseItemCode_Normalized'] = products_df['BaseItemCode'].apply(normalize_code)
        
        # Create mapping dictionaries
        nsl_norm_to_orig = dict(zip(nsl_df['Item_Normalized'], nsl_df['Item Number']))
        ml_norm_to_orig = dict(zip(ml_df['Item_Normalized'], ml_df['Item Number']))
        products_norm_to_orig = dict(zip(products_df['BaseItemCode_Normalized'], products_df['BaseItemCode']))
        
        nsl_items_norm = set(nsl_df['Item_Normalized'].dropna())
        ml_items_norm = set(ml_df['Item_Normalized'].dropna())
        combined_inventory_norm = nsl_items_norm.union(ml_items_norm)
        products_items_norm = set(products_df['BaseItemCode_Normalized'].dropna())
        
        # Remove empty strings
        combined_inventory_norm.discard('')
        products_items_norm.discard('')
        
        in_both_norm = combined_inventory_norm.intersection(products_items_norm)
        in_inv_not_prod_norm = combined_inventory_norm - products_items_norm
        
        print(f"Combined inventory (normalized, deduplicated): {len(combined_inventory_norm)}")
        print(f"Products CSV (normalized): {len(products_items_norm)}")
        print(f"Items in BOTH: {len(in_both_norm)}")
        print(f"Items in inventory but NOT in products: {len(in_inv_not_prod_norm)}")
        
        # Calculate improvement
        print("\n" + "="*80)
        print("IMPROVEMENT FROM NORMALIZATION")
        print("="*80)
        
        additional_matches = len(in_both_norm) - len(in_both_orig)
        reduction_in_discrepancy = len(in_inv_not_prod_orig) - len(in_inv_not_prod_norm)
        
        print(f"Additional matches found: {additional_matches}")
        print(f"Reduction in discrepancy: {reduction_in_discrepancy}")
        print(f"Original discrepancy: {len(in_inv_not_prod_orig)} items")
        print(f"New discrepancy: {len(in_inv_not_prod_norm)} items")
        print(f"Improvement: {reduction_in_discrepancy / len(in_inv_not_prod_orig) * 100:.1f}%")
        
        # Show examples of items that now match
        if additional_matches > 0:
            print("\n" + "="*80)
            print("EXAMPLES OF NEWLY MATCHED ITEMS (due to normalization)")
            print("="*80)
            
            # Find items that match now but didn't before
            newly_matched_norm = in_both_norm - set([normalize_code(x) for x in in_both_orig])
            
            print(f"\nShowing first 30 of {len(newly_matched_norm)} newly matched items:")
            for i, norm_code in enumerate(sorted(list(newly_matched_norm))[:30], 1):
                # Find original codes
                inv_orig = nsl_norm_to_orig.get(norm_code) or ml_norm_to_orig.get(norm_code)
                prod_orig = products_norm_to_orig.get(norm_code)
                
                print(f"{i:3d}. Inventory: '{inv_orig}' → Products: '{prod_orig}' (normalized: '{norm_code}')")
        
        # Show remaining discrepancies
        if in_inv_not_prod_norm:
            print("\n" + "="*80)
            print(f"REMAINING {len(in_inv_not_prod_norm)} ITEMS STILL NOT IN PRODUCTS (after normalization)")
            print("="*80)
            
            print(f"\nFirst 30 items:")
            for i, norm_code in enumerate(sorted(list(in_inv_not_prod_norm))[:30], 1):
                # Find original code
                inv_orig = nsl_norm_to_orig.get(norm_code) or ml_norm_to_orig.get(norm_code)
                
                # Check which file(s)
                source = []
                if norm_code in nsl_items_norm:
                    source.append("NSL")
                if norm_code in ml_items_norm:
                    source.append("ML")
                
                print(f"{i:3d}. {inv_orig} (normalized: {norm_code}) [{', '.join(source)}]")
            
            if len(in_inv_not_prod_norm) > 30:
                print(f"     ... and {len(in_inv_not_prod_norm) - 30} more")
        
        # Analyze patterns in remaining discrepancies
        print("\n" + "="*80)
        print("PATTERN ANALYSIS OF REMAINING DISCREPANCIES")
        print("="*80)
        
        prefixes = {}
        for norm_code in in_inv_not_prod_norm:
            inv_orig = nsl_norm_to_orig.get(norm_code) or ml_norm_to_orig.get(norm_code)
            if inv_orig:
                prefix = inv_orig.split('-')[0] if '-' in inv_orig else inv_orig[:3]
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
        
        print("\nTop 10 prefixes in remaining discrepancies:")
        for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  • {prefix}: {count} items")
        
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
    analyze_normalized()
