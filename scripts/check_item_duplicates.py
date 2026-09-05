#!/usr/bin/env python3
"""
Check for duplicate Item Numbers between two Excel inventory files.
"""

import pandas as pd
import sys

def check_duplicates():
    # File paths
    nsl_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/NSL  INV LIST.xlsx"
    ml_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/ML  INV LIST.xlsx"
    
    try:
        # Read both Excel files
        print("Reading NSL INV LIST.xlsx...")
        nsl_df = pd.read_excel(nsl_file)
        
        print("Reading ML INV LIST.xlsx...")
        ml_df = pd.read_excel(ml_file)
        
        # Display column names to identify the Item Number column
        print("\n" + "="*80)
        print("NSL INV LIST columns:")
        print(nsl_df.columns.tolist())
        
        print("\n" + "="*80)
        print("ML INV LIST columns:")
        print(ml_df.columns.tolist())
        
        # Try to find Item Number column (case-insensitive)
        nsl_item_col = None
        ml_item_col = None
        
        for col in nsl_df.columns:
            if 'item' in str(col).lower() and 'number' in str(col).lower():
                nsl_item_col = col
                break
        
        for col in ml_df.columns:
            if 'item' in str(col).lower() and 'number' in str(col).lower():
                ml_item_col = col
                break
        
        if not nsl_item_col:
            print("\n⚠️  Could not find 'Item Number' column in NSL file")
            print("Available columns:", nsl_df.columns.tolist())
            return
        
        if not ml_item_col:
            print("\n⚠️  Could not find 'Item Number' column in ML file")
            print("Available columns:", ml_df.columns.tolist())
            return
        
        print(f"\n" + "="*80)
        print(f"Using column '{nsl_item_col}' from NSL file")
        print(f"Using column '{ml_item_col}' from ML file")
        
        # Get Item Numbers from both files (remove NaN values)
        nsl_items = set(nsl_df[nsl_item_col].dropna().astype(str))
        ml_items = set(ml_df[ml_item_col].dropna().astype(str))
        
        print(f"\n" + "="*80)
        print(f"NSL file: {len(nsl_items)} unique Item Numbers")
        print(f"ML file: {len(ml_items)} unique Item Numbers")
        
        # Find duplicates (items that appear in both files)
        duplicates = nsl_items.intersection(ml_items)
        
        print(f"\n" + "="*80)
        if duplicates:
            print(f"❌ FOUND {len(duplicates)} DUPLICATE ITEM NUMBERS:")
            print("="*80)
            for item in sorted(duplicates):
                print(f"  • {item}")
        else:
            print("✅ NO DUPLICATES FOUND")
            print("All Item Numbers are unique between the two files.")
        
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
    check_duplicates()
