#!/usr/bin/env python3
"""
Check if duplicate Item Numbers have matching or mismatched quantities.
"""

import pandas as pd
import sys

def check_duplicate_quantities():
    # File path
    combined_file = "/Users/kylorjohnson/Downloads/Combined ML NSL INV LIST .csv"
    
    try:
        # Read the file
        print("Reading Combined ML NSL INV LIST.csv...")
        df = pd.read_csv(combined_file)
        
        # Find duplicates based on Item Number
        item_numbers = df['Item Number'].dropna()
        duplicates = item_numbers[item_numbers.duplicated(keep=False)]
        duplicate_items = sorted(duplicates.unique())
        
        print("\n" + "="*80)
        print("DUPLICATE QUANTITY ANALYSIS")
        print("="*80)
        print(f"Analyzing {len(duplicate_items)} duplicate Item Numbers...\n")
        
        matching_quantities = 0
        mismatched_quantities = 0
        
        # Check first 30 examples
        print("Sample of duplicates (first 30):\n")
        
        for i, item in enumerate(duplicate_items[:30], 1):
            dup_rows = df[df['Item Number'] == item]
            
            # Get quantities
            qty_on_hand = dup_rows['QTY On Hand'].tolist()
            qty_available = dup_rows['QTY Available'].tolist()
            
            # Check if they match
            on_hand_match = len(set([str(x) for x in qty_on_hand])) == 1
            available_match = len(set([str(x) for x in qty_available])) == 1
            
            if on_hand_match and available_match:
                status = "✓ MATCH"
                matching_quantities += 1
            else:
                status = "✗ MISMATCH"
                mismatched_quantities += 1
            
            print(f"{i:3d}. {item} - {status}")
            for idx, row in dup_rows.iterrows():
                print(f"       Row {idx+2}: On Hand={row['QTY On Hand']}, Available={row['QTY Available']}, " +
                      f"Allocated={row['QTY Allocated']}, On Order={row['QTY On Order']}")
        
        # Analyze all duplicates
        print(f"\n{'='*80}")
        print("ANALYZING ALL DUPLICATES...")
        print(f"{'='*80}\n")
        
        matching_quantities = 0
        mismatched_quantities = 0
        
        for item in duplicate_items:
            dup_rows = df[df['Item Number'] == item]
            
            # Get quantities
            qty_on_hand = dup_rows['QTY On Hand'].tolist()
            qty_available = dup_rows['QTY Available'].tolist()
            
            # Check if they match (convert to string to handle any data type issues)
            on_hand_match = len(set([str(x) for x in qty_on_hand])) == 1
            available_match = len(set([str(x) for x in qty_available])) == 1
            
            if on_hand_match and available_match:
                matching_quantities += 1
            else:
                mismatched_quantities += 1
        
        print(f"Total duplicates analyzed: {len(duplicate_items)}")
        print(f"Duplicates with MATCHING quantities: {matching_quantities} ({matching_quantities/len(duplicate_items)*100:.1f}%)")
        print(f"Duplicates with MISMATCHED quantities: {mismatched_quantities} ({mismatched_quantities/len(duplicate_items)*100:.1f}%)")
        
        # Show some mismatch examples
        if mismatched_quantities > 0:
            print(f"\n{'='*80}")
            print("EXAMPLES OF MISMATCHED QUANTITIES (first 10):")
            print(f"{'='*80}\n")
            
            count = 0
            for item in duplicate_items:
                if count >= 10:
                    break
                    
                dup_rows = df[df['Item Number'] == item]
                qty_on_hand = dup_rows['QTY On Hand'].tolist()
                qty_available = dup_rows['QTY Available'].tolist()
                
                on_hand_match = len(set([str(x) for x in qty_on_hand])) == 1
                available_match = len(set([str(x) for x in qty_available])) == 1
                
                if not (on_hand_match and available_match):
                    count += 1
                    print(f"{count}. {item}:")
                    for idx, row in dup_rows.iterrows():
                        print(f"     Row {idx+2}: On Hand={row['QTY On Hand']}, Available={row['QTY Available']}")
        
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
    check_duplicate_quantities()
