#!/usr/bin/env python3
"""
Compare inventory files (NSL + ML) with the products CSV to identify discrepancies.
"""

import pandas as pd
import sys

def compare_inventories():
    # File paths
    nsl_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/NSL  INV LIST.xlsx"
    ml_file = "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat_Simple_Final/02_Implementation/Magic Lite/03_Data/ML  INV LIST.xlsx"
    products_file = "/Users/kylorjohnson/Downloads/products.csv.20260126-1148.csv"
    
    try:
        # Read all files
        print("Reading NSL INV LIST.xlsx...")
        nsl_df = pd.read_excel(nsl_file)
        
        print("Reading ML INV LIST.xlsx...")
        ml_df = pd.read_excel(ml_file)
        
        print("Reading products.csv...")
        products_df = pd.read_csv(products_file)
        
        print("\n" + "="*80)
        print("FILE OVERVIEW")
        print("="*80)
        
        # Get Item Numbers from inventory files
        nsl_items = set(nsl_df['Item Number'].dropna().astype(str))
        ml_items = set(ml_df['Item Number'].dropna().astype(str))
        
        # Combine and deduplicate inventory items
        combined_inventory = nsl_items.union(ml_items)
        
        print(f"NSL file: {len(nsl_items)} unique Item Numbers")
        print(f"ML file: {len(ml_items)} unique Item Numbers")
        print(f"Combined (deduplicated): {len(combined_inventory)} unique Item Numbers")
        
        # Get BaseItemCode from products file
        products_items = set(products_df['BaseItemCode'].dropna().astype(str))
        print(f"\nProducts CSV: {len(products_items)} unique BaseItemCodes")
        
        # Find items in inventory but NOT in products
        in_inventory_not_products = combined_inventory - products_items
        
        # Find items in products but NOT in inventory
        in_products_not_inventory = products_items - combined_inventory
        
        # Find items in both
        in_both = combined_inventory.intersection(products_items)
        
        print("\n" + "="*80)
        print("COMPARISON RESULTS")
        print("="*80)
        print(f"Items in BOTH inventory and products: {len(in_both)}")
        print(f"Items in inventory but NOT in products: {len(in_inventory_not_products)}")
        print(f"Items in products but NOT in inventory: {len(in_products_not_inventory)}")
        
        # Analyze items in inventory but not in products
        if in_inventory_not_products:
            print("\n" + "="*80)
            print(f"❌ {len(in_inventory_not_products)} ITEMS IN INVENTORY BUT NOT IN PRODUCTS CSV:")
            print("="*80)
            
            # Check which file(s) they come from
            only_nsl = in_inventory_not_products.intersection(nsl_items - ml_items)
            only_ml = in_inventory_not_products.intersection(ml_items - nsl_items)
            in_both_inv = in_inventory_not_products.intersection(nsl_items.intersection(ml_items))
            
            print(f"\nBreakdown by source:")
            print(f"  • Only in NSL: {len(only_nsl)}")
            print(f"  • Only in ML: {len(only_ml)}")
            print(f"  • In both NSL & ML: {len(in_both_inv)}")
            
            print(f"\nFirst 50 items (sorted):")
            for item in sorted(list(in_inventory_not_products))[:50]:
                source = []
                if item in nsl_items:
                    source.append("NSL")
                if item in ml_items:
                    source.append("ML")
                print(f"  • {item} [{', '.join(source)}]")
            
            if len(in_inventory_not_products) > 50:
                print(f"  ... and {len(in_inventory_not_products) - 50} more")
        
        # Analyze items in products but not in inventory
        if in_products_not_inventory:
            print("\n" + "="*80)
            print(f"⚠️  {len(in_products_not_inventory)} ITEMS IN PRODUCTS CSV BUT NOT IN INVENTORY:")
            print("="*80)
            print(f"\nFirst 50 items (sorted):")
            for item in sorted(list(in_products_not_inventory))[:50]:
                print(f"  • {item}")
            
            if len(in_products_not_inventory) > 50:
                print(f"  ... and {len(in_products_not_inventory) - 50} more")
        
        # Analysis and potential reasons
        print("\n" + "="*80)
        print("POTENTIAL REASONS FOR DISCREPANCIES")
        print("="*80)
        
        if len(in_inventory_not_products) > 0:
            print("\n✓ Inventory has MORE items than products CSV:")
            print("  Possible reasons:")
            print("  1. Products CSV is outdated (created Jan 26, 2026)")
            print("  2. New items added to inventory after products export")
            print("  3. Items in inventory are discontinued/inactive in products")
            print("  4. Different naming conventions or data sync issues")
            print("  5. Inventory includes items from different locations/warehouses")
        
        if len(in_products_not_inventory) > 0:
            print("\n✓ Products CSV has items NOT in inventory:")
            print("  Possible reasons:")
            print("  1. Zero-stock items (no inventory on hand)")
            print("  2. Items not stocked at NSL or ML locations")
            print("  3. Virtual/bundle items that don't have physical inventory")
            print("  4. Recently discontinued items still in product catalog")
        
        # Check for pattern analysis
        print("\n" + "="*80)
        print("PATTERN ANALYSIS")
        print("="*80)
        
        if in_inventory_not_products:
            # Analyze prefixes
            prefixes = {}
            for item in in_inventory_not_products:
                prefix = item.split('-')[0] if '-' in item else item[:3]
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
            
            print("\nTop 10 prefixes in inventory-only items:")
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
    compare_inventories()
