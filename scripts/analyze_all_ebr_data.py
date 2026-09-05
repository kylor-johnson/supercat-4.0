
import json
import csv
import os
from collections import defaultdict

DATA_DIR = "/Users/kylorjohnson/Downloads"
CSVS = {
    "gh": "gh_2025-02-24_2026-02-24.csv",
    "scw": "scw_2025-02-24_2026-02-24.csv",
    "sccon": "sccon_2025-02-24_2026-02-24.csv",
    "sc": "sc_2025-02-24_2026-02-24.csv"
}

def analyze_csv(filepath):
    metrics = {
        "total_users": 0,
        "active_users": 0,
        "total_logins": 0,
        "total_orders": 0,
        "total_searches": 0,
        "total_lists_created": 0,
        "total_catalog_views": 0, # Assuming 'Search Collections' or similar
        "users_with_orders": 0
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                metrics["total_users"] += 1
                logins = int(row.get("Logins", 0) or 0)
                orders = int(row.get("Submit Order", 0) or 0)
                searches = int(row.get("Search Products", 0) or 0)
                lists = int(row.get("Create 'My List'", 0) or 0)
                
                metrics["total_logins"] += logins
                metrics["total_orders"] += orders
                metrics["total_searches"] += searches
                metrics["total_lists_created"] += lists
                
                if logins > 0:
                    metrics["active_users"] += 1
                if orders > 0:
                    metrics["users_with_orders"] += 1
                    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        
    return metrics

def analyze_json():
    with open("scripts/ebr_data_output.json", "r") as f:
        data = json.load(f)
        
    # Help Scout Analysis
    hs_tickets = len(data.get("helpscout", []))
    hs_by_org = defaultdict(int)
    for ticket in data.get("helpscout", []):
        org = ticket.get("conv_customer_organization")
        if org:
            hs_by_org[org] += 1
            
    # Fathom Analysis
    fathom_meetings = len(data.get("fathom", []))
    
    # Mixpanel Analysis
    mp_mau = defaultdict(dict)
    for row in data.get("mixpanel", []):
        brand = row.get("organization_shortname")
        month = row.get("month")
        active_users = row.get("active_users")
        mp_mau[brand][month] = active_users

    return {
        "helpscout_total": hs_tickets,
        "helpscout_by_org": dict(hs_by_org),
        "fathom_total": fathom_meetings,
        "mixpanel_mau": dict(mp_mau)
    }

def main():
    print("--- CSV Analysis ---")
    all_csv_metrics = {}
    for brand, filename in CSVS.items():
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            metrics = analyze_csv(filepath)
            all_csv_metrics[brand] = metrics
            print(f"\nBrand: {brand.upper()}")
            print(f"Total Users: {metrics['total_users']}")
            print(f"Active Users: {metrics['active_users']} ({metrics['active_users']/metrics['total_users']*100:.1f}%)" if metrics['total_users'] else "Active Users: 0")
            print(f"Total Logins: {metrics['total_logins']}")
            print(f"Total Orders: {metrics['total_orders']}")
            print(f"Users with Orders: {metrics['users_with_orders']}")
            print(f"Total Searches: {metrics['total_searches']}")
        else:
            print(f"\nBrand: {brand.upper()} - File not found: {filepath}")

    print("\n--- BigQuery Analysis ---")
    bq_metrics = analyze_json()
    print(f"Help Scout Tickets (Last Year): {bq_metrics['helpscout_total']}")
    print("Help Scout by Org:")
    for org, count in bq_metrics['helpscout_by_org'].items():
        print(f"  {org}: {count}")
        
    print(f"\nFathom Meetings (Last Year): {bq_metrics['fathom_total']}")
    
    print("\nMixpanel MAU Trend (Last 12 Months):")
    for brand, monthly_data in bq_metrics['mixpanel_mau'].items():
        print(f"  {brand}: {sorted(monthly_data.items())}")

if __name__ == "__main__":
    main()
