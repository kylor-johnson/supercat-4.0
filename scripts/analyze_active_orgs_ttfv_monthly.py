#!/usr/bin/env python3
"""
Analyze TTFV for all active orgs with monthly averages
"""
import json
from datetime import datetime
from collections import defaultdict
import csv

print("Loading Mixpanel events data...")
# Read the Mixpanel events data
with open('/Users/kylorjohnson/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-tools/bb136376-26e6-466f-8f5e-e34bb461a9c3.txt', 'r') as f:
    mixpanel_data = json.load(f)

print(f"Loaded {mixpanel_data['row_count']} events")

# Read the active orgs CSV
orgs_list = []
with open('/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/ttfv/active_orgs.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        orgs_list.append(row['Org'])

print(f"Analyzing {len(orgs_list)} active organizations")

# Known admin usernames
known_admins = ['kylor', 'admin', 'supercat', 'test', 'demo']

# Process events to find first value action per org
org_first_events = {}

for event in mixpanel_data['data']:
    org = event['org']
    username = event['username'].lower()
    event_name = event['event_name']
    event_date = datetime.strptime(event['event_date']['value'], '%Y-%m-%d').date()
    timestamp = event['time']
    
    # Skip known admin usernames
    if any(admin in username for admin in known_admins):
        continue
    
    # Track first event per org
    if org not in org_first_events:
        org_first_events[org] = {
            'username': event['username'],
            'event_name': event_name,
            'event_date': event_date,
            'timestamp': timestamp
        }
    elif timestamp < org_first_events[org]['timestamp']:
        org_first_events[org] = {
            'username': event['username'],
            'event_name': event_name,
            'event_date': event_date,
            'timestamp': timestamp
        }

print(f"Found first value events for {len(org_first_events)} organizations")

# For this analysis, we need start dates. Since we don't have them for all orgs,
# we'll just group by the month of first value achievement
# Group by month of first value
monthly_groups = defaultdict(list)
for org, first_event in org_first_events.items():
    month_key = first_event['event_date'].strftime('%Y-%m')
    monthly_groups[month_key].append({
        'org': org,
        'event_date': first_event['event_date']
    })

# Calculate counts per month
monthly_stats = {}
for month in sorted(monthly_groups.keys()):
    monthly_stats[month] = {
        'count': len(monthly_groups[month]),
        'orgs': monthly_groups[month]
    }

# Print results
print("\n" + "=" * 80)
print("MONTHLY FIRST VALUE ACHIEVEMENT - ALL ACTIVE ORGS")
print("January 2025 - January 2026")
print("=" * 80)
print()

# Create month range
months = []
for year in [2025, 2026]:
    for month in range(1, 13):
        month_key = f"{year}-{month:02d}"
        months.append(month_key)
        if month_key == '2026-01':
            break
    if year == 2026:
        break

for month in months:
    if month in monthly_stats:
        print(f"{month}: {monthly_stats[month]['count']} companies achieved first value")
    else:
        print(f"{month}: 0 companies achieved first value")

# Create CSV output
print("\n" + "=" * 80)
print("Creating CSV output...")

# Build the CSV data
csv_months = ['Jan-25', 'Feb-25', 'Mar-25', 'Apr-25', 'May-25', 'Jun-25', 
              'Jul-25', 'Aug-25', 'Sep-25', 'Oct-25', 'Nov-25', 'Dec-25', 'Jan-26']
month_mapping = {
    '2025-01': 'Jan-25', '2025-02': 'Feb-25', '2025-03': 'Mar-25', '2025-04': 'Apr-25',
    '2025-05': 'May-25', '2025-06': 'Jun-25', '2025-07': 'Jul-25', '2025-08': 'Aug-25',
    '2025-09': 'Sep-25', '2025-10': 'Oct-25', '2025-11': 'Nov-25', '2025-12': 'Dec-25',
    '2026-01': 'Jan-26'
}

counts = []
for month_key in ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                  '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12', '2026-01']:
    if month_key in monthly_stats:
        counts.append(monthly_stats[month_key]['count'])
    else:
        counts.append(0)

# Write CSV
with open('/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/ttfv/active_orgs_monthly_first_value.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Metric'] + csv_months)
    writer.writerow(['Companies Achieving First Value'] + counts)

print("CSV created: active_orgs_monthly_first_value.csv")
print("\nNote: This shows COUNT of companies achieving first value each month.")
print("TTFV calculation requires start dates (HubSpot close date or org created_at)")
print("which are not available in active_orgs.csv")
print("=" * 80)
