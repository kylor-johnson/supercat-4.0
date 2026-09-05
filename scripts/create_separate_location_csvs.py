#!/usr/bin/env python3
"""
Create separate CSV files for ML and NSL inventory from the original Excel files.
Filter by Location Code to get only the correct site inventory.
"""

import pandas as pd
import sys

def create_location_csvs():
    # File paths
    nsl_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/NSL  INV LIST.xlsx"
    ml_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/ML  INV LIST.xlsx"
    
    output_nsl = "/Users/kylorjohnson/Downloads/NSL_Inventory_Clean.csv"
    output_ml = "/Users/kylorjohnson/Downloads/ML_Inventory_Clean.csv"
    
    try:
        print("="*80)
        print("READING EXCEL FILES")
        print("="*80)
        
        # Read NSL file
        print("\nReading NSL INV LIST.xlsx...")
        nsl_df = pd.read_excel(nsl_file)
        print(f"Total rows: {len(nsl_df)}")
        print(f"Columns: {nsl_df.columns.tolist()}")
        
        # Read ML file
        print("\nReading ML INV LIST.xlsx...")
        ml_df = pd.read_excel(ml_file)
        print(f"Total rows: {len(ml_df)}")
        print(f"Columns: {ml_df.columns.tolist()}")
        
        print("\n" + "="*80)
        print("FILTERING BY LOCATION CODE")
        print("="*80)
        
        # Check Location Code values in NSL file
        print("\nNSL file - Location Code values:")
        nsl_locations = nsl_df['Location Code'].value_counts()
        for loc, count in nsl_locations.items():
            print(f"  • {loc}: {count} items")
        
        # Check Location Code values in ML file
        print("\nML file - Location Code values:")
        ml_locations = ml_df['Location Code'].value_counts()
        for loc, count in ml_locations.items():
            print(f"  • {loc}: {count} items")
        
        # Filter NSL file to only NSL location
        nsl_filtered = nsl_df[nsl_df['Location Code'] == 'NSL'].copy()
        print(f"\nNSL file filtered to NSL location only: {len(nsl_filtered)} items")
        
        # Filter ML file to only ML location
        ml_filtered = ml_df[ml_df['Location Code'] == 'ML'].copy()
        print(f"ML file filtered to ML location only: {len(ml_filtered)} items")
        
        # Save to CSV
        print("\n" + "="*80)
        print("SAVING CSV FILES")
        print("="*80)
        
        nsl_filtered.to_csv(output_nsl, index=False)
        print(f"\n✅ NSL Inventory saved to: {output_nsl}")
        print(f"   Rows: {len(nsl_filtered)}")
        print(f"   Unique Item Numbers: {nsl_filtered['Item Number'].nunique()}")
        
        ml_filtered.to_csv(output_ml, index=False)
        print(f"\n✅ ML Inventory saved to: {output_ml}")
        print(f"   Rows: {len(ml_filtered)}")
        print(f"   Unique Item Numbers: {ml_filtered['Item Number'].nunique()}")
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        # Check for duplicates in each filtered file
        nsl_duplicates = nsl_filtered['Item Number'].duplicated().sum()
        ml_duplicates = ml_filtered['Item Number'].duplicated().sum()
        
        print(f"\nNSL Inventory (NSL location only):")
        print(f"  • Total items: {len(nsl_filtered)}")
        print(f"  • Unique Item Numbers: {nsl_filtered['Item Number'].nunique()}")
        print(f"  • Duplicates: {nsl_duplicates}")
        
        print(f"\nML Inventory (ML location only):")
        print(f"  • Total items: {len(ml_filtered)}")
        print(f"  • Unique Item Numbers: {ml_filtered['Item Number'].nunique()}")
        print(f"  • Duplicates: {ml_duplicates}")
        
        # Show sample from each
        print("\n" + "="*80)
        print("SAMPLE DATA - NSL Inventory (first 10 items)")
        print("="*80)
        print(nsl_filtered[['Item Number', 'Item Description', 'Location Code', 'QTY On Hand', 'QTY Available']].head(10).to_string(index=False))
        
        print("\n" + "="*80)
        print("SAMPLE DATA - ML Inventory (first 10 items)")
        print("="*80)
        print(ml_filtered[['Item Number', 'Item Description', 'Location Code', 'QTY On Hand', 'QTY Available']].head(10).to_string(index=False))
        
        print("\n" + "="*80)
        print("✅ COMPLETE - Two clean CSV files created!")
        print("="*80)
        print(f"\nNSL Inventory: {output_nsl}")
        print(f"ML Inventory: {output_ml}")
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
    create_location_csvs()
