#!/usr/bin/env python3
"""
Create a clean inventory CSV with one row per Item Number, 
showing inventory by location (ML, NSL, GA).
"""

import pandas as pd
import sys

def safe_float(value):
    """Safely convert value to float, handling commas and other issues."""
    if pd.isna(value):
        return 0.0
    try:
        # Remove commas and convert to float
        return float(str(value).replace(',', ''))
    except:
        return 0.0

def create_clean_inventory():
    # File path
    combined_file = "/Users/kylorjohnson/Downloads/Combined ML NSL INV LIST .csv"
    output_file = "/Users/kylorjohnson/Downloads/Clean_Inventory_By_Location.csv"
    
    try:
        # Read the file
        print("Reading Combined ML NSL INV LIST.csv...")
        df = pd.read_csv(combined_file)
        
        print(f"Total rows: {len(df)}")
        print(f"Unique Item Numbers: {df['Item Number'].nunique()}")
        
        # Create a clean dataset
        # Group by Item Number and create columns for each location
        print("\nProcessing inventory by location...")
        
        # First, let's identify the location for each row
        # The pattern shows that NSL/GA appear in the "QTY On Hand" column for those locations
        # ML location has numeric values in "QTY On Hand"
        
        clean_data = []
        
        for item_number in df['Item Number'].dropna().unique():
            item_rows = df[df['Item Number'] == item_number]
            
            # Get the description (should be same for all rows)
            description = item_rows.iloc[0]['Item Description']
            
            # Initialize location data
            ml_data = {'on_hand': 0, 'available': 0, 'allocated': 0, 'on_order': 0}
            nsl_data = {'on_hand': 0, 'available': 0, 'allocated': 0, 'on_order': 0}
            ga_data = {'on_hand': 0, 'available': 0, 'allocated': 0, 'on_order': 0}
            
            for idx, row in item_rows.iterrows():
                qty_on_hand = str(row['QTY On Hand'])
                
                # Determine location based on QTY On Hand column
                if qty_on_hand == 'NSL':
                    # This is NSL location data
                    nsl_data['on_hand'] = safe_float(row['QTY Available'])
                    nsl_data['available'] = safe_float(row['QTY Available'])
                    nsl_data['allocated'] = safe_float(row['QTY Allocated'])
                    nsl_data['on_order'] = 0  # On Order shows category for NSL rows
                elif qty_on_hand == 'GA':
                    # This is GA location data
                    ga_data['on_hand'] = safe_float(row['QTY Available'])
                    ga_data['available'] = safe_float(row['QTY Available'])
                    ga_data['allocated'] = safe_float(row['QTY Allocated'])
                    ga_data['on_order'] = 0
                else:
                    # This is ML location data (has numeric values)
                    ml_data['on_hand'] = safe_float(qty_on_hand)
                    ml_data['available'] = safe_float(row['QTY Available'])
                    ml_data['allocated'] = safe_float(row['QTY Allocated'])
                    ml_data['on_order'] = safe_float(row['QTY On Order'])
            
            # Create clean row
            clean_row = {
                'Item Number': item_number,
                'Item Description': description,
                'ML_QTY_On_Hand': ml_data['on_hand'],
                'ML_QTY_Available': ml_data['available'],
                'ML_QTY_Allocated': ml_data['allocated'],
                'ML_QTY_On_Order': ml_data['on_order'],
                'NSL_QTY_On_Hand': nsl_data['on_hand'],
                'NSL_QTY_Available': nsl_data['available'],
                'NSL_QTY_Allocated': nsl_data['allocated'],
                'NSL_QTY_On_Order': nsl_data['on_order'],
                'GA_QTY_On_Hand': ga_data['on_hand'],
                'GA_QTY_Available': ga_data['available'],
                'GA_QTY_Allocated': ga_data['allocated'],
                'GA_QTY_On_Order': ga_data['on_order'],
                'Total_QTY_On_Hand': ml_data['on_hand'] + nsl_data['on_hand'] + ga_data['on_hand'],
                'Total_QTY_Available': ml_data['available'] + nsl_data['available'] + ga_data['available'],
            }
            
            clean_data.append(clean_row)
        
        # Create DataFrame
        clean_df = pd.DataFrame(clean_data)
        
        # Sort by Item Number
        clean_df = clean_df.sort_values('Item Number')
        
        # Save to CSV
        clean_df.to_csv(output_file, index=False)
        
        print(f"\n{'='*80}")
        print("CLEAN INVENTORY FILE CREATED")
        print(f"{'='*80}")
        print(f"Output file: {output_file}")
        print(f"Total unique items: {len(clean_df)}")
        print(f"\nColumns created:")
        for col in clean_df.columns:
            print(f"  • {col}")
        
        # Summary statistics
        print(f"\n{'='*80}")
        print("INVENTORY SUMMARY")
        print(f"{'='*80}")
        
        items_in_ml = len(clean_df[clean_df['ML_QTY_On_Hand'] > 0])
        items_in_nsl = len(clean_df[clean_df['NSL_QTY_On_Hand'] > 0])
        items_in_ga = len(clean_df[clean_df['GA_QTY_On_Hand'] > 0])
        items_in_multiple = len(clean_df[
            ((clean_df['ML_QTY_On_Hand'] > 0) & (clean_df['NSL_QTY_On_Hand'] > 0)) |
            ((clean_df['ML_QTY_On_Hand'] > 0) & (clean_df['GA_QTY_On_Hand'] > 0)) |
            ((clean_df['NSL_QTY_On_Hand'] > 0) & (clean_df['GA_QTY_On_Hand'] > 0))
        ])
        
        print(f"Items with stock in ML: {items_in_ml}")
        print(f"Items with stock in NSL: {items_in_nsl}")
        print(f"Items with stock in GA: {items_in_ga}")
        print(f"Items stocked in multiple locations: {items_in_multiple}")
        
        # Show sample
        print(f"\n{'='*80}")
        print("SAMPLE DATA (first 10 items)")
        print(f"{'='*80}\n")
        print(clean_df.head(10).to_string(index=False))
        
        print(f"\n{'='*80}")
        print(f"✅ Clean inventory file created successfully!")
        print(f"{'='*80}\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_clean_inventory()
