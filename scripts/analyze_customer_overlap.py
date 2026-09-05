import pandas as pd

# File paths
old_file_path = "/Users/kylorjohnson/Downloads/customers.csv.20260119-1946.csv"
new_file_path = "/Users/kylorjohnson/Downloads/customers.csv.20260224-0203.csv"

try:
    # Read files
    # Using 'utf-8' encoding, or 'latin1' if that fails as common with some exports
    try:
        df_old = pd.read_csv(old_file_path, encoding='utf-8', dtype=str)
    except UnicodeDecodeError:
        df_old = pd.read_csv(old_file_path, encoding='latin1', dtype=str)

    try:
        df_new = pd.read_csv(new_file_path, encoding='utf-8', dtype=str)
    except UnicodeDecodeError:
        df_new = pd.read_csv(new_file_path, encoding='latin1', dtype=str)

    # Clean column names (strip whitespace)
    df_old.columns = df_old.columns.str.strip()
    df_new.columns = df_new.columns.str.strip()

    # Identify key column
    key_col = 'BillToCode'

    if key_col not in df_old.columns or key_col not in df_new.columns:
        print(f"Error: '{key_col}' column not found in one of the files.")
        print("Old columns:", df_old.columns.tolist())
        print("New columns:", df_new.columns.tolist())
        exit(1)

    # Get unique customers
    old_customers = set(df_old[key_col].unique())
    new_customers = set(df_new[key_col].unique())

    # Calculate overlap
    overlap = old_customers.intersection(new_customers)
    only_in_old = old_customers - new_customers
    only_in_new = new_customers - old_customers

    print(f"Total customers in old file: {len(old_customers)}")
    print(f"Total customers in new file: {len(new_customers)}")
    print(f"Overlapping customers: {len(overlap)}")
    print(f"Customers only in old file: {len(only_in_old)}")
    print(f"Customers only in new file: {len(only_in_new)}")

    # Merge DataFrames for overlapping customers
    # Ensure key column is string
    df_old[key_col] = df_old[key_col].astype(str)
    df_new[key_col] = df_new[key_col].astype(str)
    
    # Check for duplicates in key column
    if df_old[key_col].duplicated().any():
        print(f"Warning: Duplicate {key_col} found in old file. Taking first occurrence.")
        df_old = df_old.drop_duplicates(subset=[key_col])
    
    if df_new[key_col].duplicated().any():
        print(f"Warning: Duplicate {key_col} found in new file. Taking first occurrence.")
        df_new = df_new.drop_duplicates(subset=[key_col])

    # Merge
    merged_df = pd.merge(df_old[[key_col, 'billto_warehouse']], 
                         df_new[[key_col, 'DistributionSource']], 
                         on=key_col, 
                         how='inner',
                         suffixes=('_old', '_new'))
    
    # Comparison
    col_old = 'billto_warehouse'
    col_new = 'DistributionSource'
    
    # Fill NaN with empty string and strip whitespace
    merged_df[col_old] = merged_df[col_old].fillna('').astype(str).str.strip()
    merged_df[col_new] = merged_df[col_new].fillna('').astype(str).str.strip()
    
    mismatches = merged_df[merged_df[col_old] != merged_df[col_new]]
    num_mismatches = len(mismatches)
    
    overlap_count = len(merged_df)
    
    print(f"\nOverlapping customers count (after deduplication): {overlap_count}")

    print(f"\nComparison of '{col_old}' (old) vs '{col_new}' (new):")
    if num_mismatches == 0:
        print("SUCCESS: All overlapping customers have matching values!")
    else:
        print(f"WARNING: {num_mismatches} mismatches found out of {overlap_count} overlapping customers.")
        print(f"Mismatch Rate: {(num_mismatches/overlap_count)*100:.2f}%")
        print("\nSample mismatches (first 5):")
        print(mismatches[[key_col, col_old, col_new]].head().to_string(index=False))

except Exception as e:
    import traceback
    traceback.print_exc()
