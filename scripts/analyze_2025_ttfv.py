#!/usr/bin/env python3
"""
Analyze TTFV for 2025 clients with monthly averages
"""
import json
from datetime import datetime
from collections import defaultdict
import csv

# Read the Mixpanel events data (updated with all events, no date filter)
with open('/Users/kylorjohnson/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-tools/d01d501f-6c81-46d5-8082-74f7c1e99da3.txt', 'r') as f:
    mixpanel_data = json.load(f)

# Read the 2025 clients CSV
clients = {}
with open('/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/ttfv/2025_clients.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        clients[row['Org']] = {
            'name': row['OrgName'],
            'close_date': datetime.strptime(row['CloseDate'], '%Y-%m-%d').date() if row['CloseDate'] else None
        }

# Known admin usernames (common SuperCat admins - we'll need to filter these)
# This is a simplified approach since Postgres is timing out
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

# Calculate TTFV for each org
results = []
for org, client_info in clients.items():
    if org in org_first_events:
        first_event = org_first_events[org]
        close_date = client_info['close_date']
        
        if close_date:
            ttfv_days = (first_event['event_date'] - close_date).days
            
            # Map event name to action type
            if first_event['event_name'] == 'item_added_via_magic_button':
                action_type = 'Presentation (Stack)'
            else:
                action_type = 'Email Draft'
            
            results.append({
                'org': org,
                'org_name': client_info['name'],
                'close_date': close_date,
                'first_value_date': first_event['event_date'],
                'first_value_action': action_type,
                'ttfv_days': ttfv_days,
                'username': first_event['username']
            })

# Sort by first value date
results.sort(key=lambda x: x['first_value_date'])

# Group by month of first value
monthly_groups = defaultdict(list)
for result in results:
    month_key = result['first_value_date'].strftime('%Y-%m')
    monthly_groups[month_key].append(result)

# Print results
print("=" * 100)
print("TTFV ANALYSIS - 2025 CLIENTS")
print("Monthly Averages: January 2025 - January 2026")
print("=" * 100)
print()

# Print monthly breakdown
for month in sorted(monthly_groups.keys()):
    month_data = monthly_groups[month]
    avg_ttfv = sum(r['ttfv_days'] for r in month_data) / len(month_data)
    
    month_name = datetime.strptime(month, '%Y-%m').strftime('%B %Y')
    print(f"\n{'='*100}")
    print(f"MONTH: {month_name}")
    print(f"{'='*100}")
    print(f"Companies achieving first value: {len(month_data)}")
    print(f"Average TTFV: {avg_ttfv:.1f} days")
    print()
    print(f"{'Organization':<30} {'Close Date':<15} {'First Value':<15} {'Action Type':<25} {'TTFV Days':<10}")
    print("-" * 100)
    
    for r in month_data:
        print(f"{r['org_name']:<30} {str(r['close_date']):<15} {str(r['first_value_date']):<15} {r['first_value_action']:<25} {r['ttfv_days']:<10}")
    print()

# Print summary
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
total_orgs = len(results)
total_avg = sum(r['ttfv_days'] for r in results) / len(results) if results else 0
print(f"Total organizations analyzed: {total_orgs}")
print(f"Overall average TTFV: {total_avg:.1f} days")
print()

# Best and worst performers
if results:
    best = min(results, key=lambda x: x['ttfv_days'])
    worst = max(results, key=lambda x: x['ttfv_days'])
    print(f"Best TTFV: {best['org_name']} - {best['ttfv_days']} days")
    print(f"Slowest TTFV: {worst['org_name']} - {worst['ttfv_days']} days")

# Orgs without TTFV
orgs_without_ttfv = [org for org in clients.keys() if org not in org_first_events]
if orgs_without_ttfv:
    print(f"\nOrganizations without valid TTFV events: {len(orgs_without_ttfv)}")
    for org in orgs_without_ttfv:
        print(f"  - {clients[org]['name']}")

print("\n" + "=" * 100)
