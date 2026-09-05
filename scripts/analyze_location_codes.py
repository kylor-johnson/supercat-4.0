#!/usr/bin/env python3
"""
Analyze Location Code column in inventory files to check for GA products.
"""

import pandas as pd
import sys

def analyze_locations():
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
        print("LOCATION CODE ANALYSIS")
        print("="*80)
        
        # Check Location Code column in NSL
        print("\nNSL Inventory - Location Code values:")
        nsl_locations = nsl_df['Location Code'].value_counts()
        for loc, count in nsl_locations.items():
            print(f"  • {loc}: {count} items")
        
        # Check Location Code column in ML
        print("\nML Inventory - Location Code values:")
        ml_locations = ml_df['Location Code'].value_counts()
        for loc, count in ml_locations.items():
            print(f"  • {loc}: {count} items")
        
        # Get items by location
        nsl_ga_items = set(nsl_df[nsl_df['Location Code'] == 'GA']['Item Number'].dropna().astype(str))
        ml_ga_items = set(ml_df[ml_df['Location Code'] == 'GA']['Item Number'].dropna().astype(str))
        
        nsl_non_ga_items = set(nsl_df[nsl_df['Location Code'] != 'GA']['Item Number'].dropna().astype(str))
        ml_non_ga_items = set(ml_df[ml_df['Location Code'] != 'GA']['Item Number'].dropna().astype(str))
        
        all_ga_items = nsl_ga_items.union(ml_ga_items)
        all_non_ga_items = nsl_non_ga_items.union(ml_non_ga_items)
        
        print("\n" + "="*80)
        print("GA vs NON-GA BREAKDOWN")
        print("="*80)
        print(f"Total unique GA items (across both files): {len(all_ga_items)}")
        print(f"Total unique non-GA items (across both files): {len(all_non_ga_items)}")
        
        # Get products items
        products_items = set(products_df['BaseItemCode'].dropna().astype(str))
        
        # Check if products CSV has TradeNameCode column
        if 'TradeNameCode' in products_df.columns:
            print("\nProducts CSV - TradeNameCode values:")
            trade_codes = products_df['TradeNameCode'].value_counts()
            for code, count in trade_codes.items():
                print(f"  • {code}: {count} items")
            
            # Check for GA in products
            ga_in_products = products_df[products_df['TradeNameCode'] == 'GA']
            print(f"\nGA items in products CSV: {len(ga_in_products)}")
        
        # Compare GA items to products
        ga_in_products_set = all_ga_items.intersection(products_items)
        ga_not_in_products = all_ga_items - products_items
        
        print("\n" + "="*80)
        print("GA ITEMS vs PRODUCTS CSV")
        print("="*80)
        print(f"GA items that ARE in products CSV: {len(ga_in_products_set)}")
        print(f"GA items that are NOT in products CSV: {len(ga_not_in_products)}")
        
        if ga_not_in_products:
            print(f"\nFirst 30 GA items NOT in products CSV:")
            for item in sorted(list(ga_not_in_products))[:30]:
                source = []
                if item in nsl_ga_items:
                    source.append("NSL")
                if item in ml_ga_items:
                    source.append("ML")
                print(f"  • {item} [{', '.join(source)}]")
            
            if len(ga_not_in_products) > 30:
                print(f"  ... and {len(ga_not_in_products) - 30} more")
        
        # Now check: of the 159 items in inventory but not in products, how many are GA?
        combined_inventory = nsl_df['Item Number'].dropna().astype(str).tolist() + ml_df['Item Number'].dropna().astype(str).tolist()
        combined_inventory_set = set(combined_inventory)
        
        in_inventory_not_products = combined_inventory_set - products_items
        
        ga_items_in_discrepancy = in_inventory_not_products.intersection(all_ga_items)
        non_ga_items_in_discrepancy = in_inventory_not_products - all_ga_items
        
        print("\n" + "="*80)
        print("EXPLAINING THE 159 ITEM DISCREPANCY")
        print("="*80)
        print(f"Items in inventory but NOT in products CSV: {len(in_inventory_not_products)}")
        print(f"  • GA items: {len(ga_items_in_discrepancy)} ({len(ga_items_in_discrepancy)/len(in_inventory_not_products)*100:.1f}%)")
        print(f"  • Non-GA items: {len(non_ga_items_in_discrepancy)} ({len(non_ga_items_in_discrepancy)/len(in_inventory_not_products)*100:.1f}%)")
        
        if len(ga_items_in_discrepancy) > 0:
            print(f"\n✅ HYPOTHESIS CONFIRMED!")
            print(f"   {len(ga_items_in_discrepancy)} of the 159 discrepancy items are GA products")
            print(f"   which are likely not included in the products CSV")
        
        if non_ga_items_in_discrepancy:
            print(f"\nRemaining {len(non_ga_items_in_discrepancy)} non-GA items in inventory but not in products:")
            for item in sorted(list(non_ga_items_in_discrepancy))[:20]:
                # Find which location(s) this item is in
                nsl_loc = nsl_df[nsl_df['Item Number'] == item]['Location Code'].values
                ml_loc = ml_df[ml_df['Item Number'] == item]['Location Code'].values
                
                locations = []
                if len(nsl_loc) > 0:
                    locations.append(f"NSL:{nsl_loc[0]}")
                if len(ml_loc) > 0:
                    locations.append(f"ML:{ml_loc[0]}")
                
                print(f"  • {item} [{', '.join(locations)}]")
            
            if len(non_ga_items_in_discrepancy) > 20:
                print(f"  ... and {len(non_ga_items_in_discrepancy) - 20} more")
        
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
    analyze_locations()
