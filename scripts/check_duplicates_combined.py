#!/usr/bin/env python3
"""
Check for duplicate Item Numbers in the combined inventory file.
"""

import pandas as pd
import sys

def check_duplicates():
    # File path
    combined_file = "/Users/kylorjohnson/Downloads/Combined ML NSL INV LIST .csv"
    
    try:
        # Read the file
        print("Reading Combined ML NSL INV LIST.csv...")
        df = pd.read_csv(combined_file)
        
        print("\n" + "="*80)
        print("FILE OVERVIEW")
        print("="*80)
        print(f"Total rows in file: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Check for duplicates based on Item Number
        print("\n" + "="*80)
        print("DUPLICATE ANALYSIS")
        print("="*80)
        
        # Get Item Numbers (remove NaN)
        item_numbers = df['Item Number'].dropna()
        
        print(f"\nTotal Item Number entries: {len(item_numbers)}")
        print(f"Unique Item Numbers: {len(item_numbers.unique())}")
        
        # Find duplicates
        duplicates = item_numbers[item_numbers.duplicated(keep=False)]
        duplicate_items = duplicates.unique()
        
        print(f"\n{'='*80}")
        if len(duplicate_items) > 0:
            print(f"❌ FOUND {len(duplicate_items)} ITEM NUMBERS THAT APPEAR MORE THAN ONCE")
            print(f"{'='*80}")
            
            # Show each duplicate and how many times it appears
            print("\nDuplicate Item Numbers and their counts:")
            for item in sorted(duplicate_items):
                count = len(df[df['Item Number'] == item])
                print(f"  • {item}: appears {count} times")
                
                # Show the rows for this duplicate
                dup_rows = df[df['Item Number'] == item][['Item Number', 'Item Description', 'QTY On Hand', 'QTY Available']]
                for idx, row in dup_rows.iterrows():
                    print(f"      Row {idx + 2}: Qty On Hand={row['QTY On Hand']}, Qty Available={row['QTY Available']}")
            
            # Calculate total duplicate rows
            total_duplicate_rows = len(duplicates)
            unique_items_if_deduped = len(item_numbers.unique())
            rows_to_remove = total_duplicate_rows - len(duplicate_items)
            
            print(f"\n{'='*80}")
            print("SUMMARY")
            print(f"{'='*80}")
            print(f"Total rows with Item Numbers: {len(item_numbers)}")
            print(f"Duplicate rows (all occurrences): {total_duplicate_rows}")
            print(f"Unique Item Numbers: {unique_items_if_deduped}")
            print(f"Rows that could be removed: {rows_to_remove}")
            
        else:
            print("✅ NO DUPLICATES FOUND")
            print("All Item Numbers are unique in this file.")
        
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
