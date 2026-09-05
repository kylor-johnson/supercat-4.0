#!/usr/bin/env python3
"""
Comprehensive Client Validation
Searches ALL Fathom calls and HelpScout tickets for 6 specific clients
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import Fathom
sys.path.insert(0, os.path.join(parent_dir, 'integrations/fathom'))
from fathom_api import get_meetings, get_summary

# BigQuery setup
SERVICE_ACCOUNT_PATH = os.path.join(parent_dir, "integrations/bigquery/service-account/supercat-data-pipeline-dbfab43c27bb.json")
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=["https://www.googleapis.com/auth/bigquery"])
bq_client = bigquery.Client(credentials=credentials, project="supercat-data-pipeline")

# Client data with multiple name variations
CLIENTS = {
    'cst': {
        'names': ['Coaster Furniture', 'Coaster', 'CST'],
        'domains': ['coasterfurniture.com', 'coaster.com'],
        'full_name': 'Coaster Furniture'
    },
    'dccl': {
        'names': ['Donald Choi Canada', 'Donald Choi', 'DCCL'],
        'domains': ['donaldchoi.com'],
        'full_name': 'Donald Choi Canada'
    },
    'krb': {
        'names': ['Kaleen Rugs', 'Kaleen', 'KRB', 'Kaleen Rugs & Broadloom'],
        'domains': ['kaleenrugs.com', 'kaleen.com'],
        'full_name': 'Kaleen Rugs & Broadloom'
    },
    'mali': {
        'names': ['Magic Lite', 'MagicLite', 'MALI'],
        'domains': ['magiclite.com'],
        'full_name': 'Magic Lite'
    },
    'pebl': {
        'names': ['Pebl', 'PEBL', 'Pebble'],
        'domains': ['pebl.com', 'pebble.com'],
        'full_name': 'Pebl'
    },
    'tcd': {
        'names': ['Terracotta Designs', 'Terracotta', 'TCD'],
        'domains': ['terracottadesigns.com', 'terracotta.com'],
        'full_name': 'Terracotta Designs'
    }
}

def match_text_to_client(text):
    """Match text to client using name variations"""
    if not text:
        return []
    text_lower = text.lower()
    matches = []
    for shortname, client in CLIENTS.items():
        for name in client['names']:
            if name.lower() in text_lower:
                matches.append(shortname)
                break
    return list(set(matches))

def match_email_to_client(email):
    """Match email domain to client"""
    if not email:
        return []
    email_lower = email.lower()
    matches = []
    for shortname, client in CLIENTS.items():
        for domain in client['domains']:
            if domain.lower() in email_lower:
                matches.append(shortname)
                break
    return matches

print("="*100)
print("COMPREHENSIVE CLIENT VALIDATION - FATHOM + HELPSCOUT")
print("="*100)
print(f"Clients: {', '.join([c['full_name'] for c in CLIENTS.values()])}")
print()

# ============================================================================
# PART 1: FATHOM MEETINGS
# ============================================================================

print("\n" + "="*100)
print("PART 1: FATHOM MEETINGS (Last 14 Days)")
print("="*100)

meetings = get_meetings()
cutoff = (datetime.now() - timedelta(days=14)).isoformat()
recent_meetings = [m for m in meetings if m.get('recording_start_time', '') >= cutoff]

print(f"\nTotal meetings in API: {len(meetings)}")
print(f"Meetings in last 14 days: {len(recent_meetings)}\n")

# Match meetings to clients
client_fathom_matches = {shortname: [] for shortname in CLIENTS.keys()}

for meeting in sorted(recent_meetings, key=lambda x: x.get('recording_start_time', ''), reverse=True):
    title = meeting.get('meeting_title', '')
    rid = meeting.get('recording_id')
    start = meeting.get('recording_start_time', '')
    date = start[:10] if start else 'N/A'
    time = start[11:16] if len(start) > 11 else ''
    
    # Match by title
    matched_clients = match_text_to_client(title)
    
    if matched_clients:
        for shortname in matched_clients:
            client_fathom_matches[shortname].append({
                'id': rid,
                'title': title,
                'date': date,
                'time': time,
                'match_method': 'title'
            })
            print(f"✓ {shortname.upper()}: {date} {time} | {title}")

# Get summaries for matched meetings
print("\n" + "-"*100)
print("GETTING MEETING SUMMARIES...")
print("-"*100)

for shortname, meetings_list in client_fathom_matches.items():
    if meetings_list:
        print(f"\n--- {shortname.upper()} ({CLIENTS[shortname]['full_name']}) ---")
        for meeting in meetings_list[:3]:  # Get up to 3 most recent
            rid = meeting['id']
            print(f"\n  Meeting: {meeting['title']}")
            print(f"  Date: {meeting['date']} | ID: {rid}")
            
            try:
                summary = get_summary(rid)
                if summary:
                    # Extract summary text
                    summary_text = summary.get('summary', {})
                    if isinstance(summary_text, dict):
                        summary_text = summary_text.get('markdown_formatted', summary_text.get('text', ''))
                    
                    print(f"  Summary: {str(summary_text)[:300]}...")
                    
                    # Action items
                    action_items = summary.get('action_items', [])
                    if action_items:
                        print(f"  Action Items: {len(action_items)}")
                    
                    meeting['summary'] = summary
                    meeting['summary_text'] = str(summary_text)[:1000]
                    meeting['action_items'] = action_items
            except Exception as e:
                print(f"  Error getting summary: {e}")

# ============================================================================
# PART 2: HELPSCOUT TICKETS
# ============================================================================

print("\n\n" + "="*100)
print("PART 2: HELPSCOUT TICKETS (Last 180 Days)")
print("="*100)

client_helpscout_matches = {shortname: [] for shortname in CLIENTS.keys()}

# Search for each client
for shortname, client in CLIENTS.items():
    print(f"\nSearching for {shortname.upper()} ({client['full_name']})...")
    
    # Build search conditions for all name variations and domains
    name_conditions = " OR ".join([f"LOWER(conv_customer_organization) LIKE '%{name.lower()}%'" for name in client['names']])
    domain_conditions = " OR ".join([f"LOWER(conv_customer_email) LIKE '%@{domain.lower()}%'" for domain in client['domains']])
    subject_conditions = " OR ".join([f"LOWER(ticket_subject) LIKE '%{name.lower()}%'" for name in client['names']])
    
    query = f"""
    SELECT DISTINCT
        ticket_number,
        ticket_subject,
        ticket_status,
        ticket_created_at,
        conv_customer_organization,
        conv_customer_email,
        agent_name,
        mailbox_name,
        LEFT(ticket_preview, 500) as preview,
        thread_count,
        (SELECT STRING_AGG(tag.tag_name, ', ') FROM UNNEST(ticket_tags) as tag) as all_tags
    FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
    WHERE (
        {name_conditions}
        OR {domain_conditions}
        OR {subject_conditions}
    )
    AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 180 DAY)
    ORDER BY ticket_created_at DESC
    LIMIT 50
    """
    
    try:
        results = bq_client.query(query).result()
        
        for row in results:
            client_helpscout_matches[shortname].append({
                'ticket_number': row.ticket_number,
                'subject': row.ticket_subject,
                'status': row.ticket_status,
                'created_at': str(row.ticket_created_at),
                'organization': row.conv_customer_organization,
                'email': row.conv_customer_email,
                'agent': row.agent_name,
                'mailbox': row.mailbox_name,
                'preview': row.preview,
                'thread_count': row.thread_count,
                'tags': row.all_tags
            })
            
            print(f"  ✓ Ticket #{row.ticket_number}: {row.ticket_subject[:60]}... ({row.ticket_created_at.strftime('%Y-%m-%d')})")
        
        if not client_helpscout_matches[shortname]:
            print(f"  ❌ NO TICKETS FOUND")
    
    except Exception as e:
        print(f"  Error querying: {e}")

# ============================================================================
# SUMMARY OUTPUT
# ============================================================================

print("\n\n" + "="*100)
print("VALIDATION SUMMARY BY CLIENT")
print("="*100)

for shortname in ['cst', 'dccl', 'krb', 'mali', 'pebl', 'tcd']:
    client = CLIENTS[shortname]
    fathom_meetings = client_fathom_matches.get(shortname, [])
    helpscout_tickets = client_helpscout_matches.get(shortname, [])
    
    print(f"\n{shortname.upper()} - {client['full_name']}")
    print("-" * 60)
    
    # Fathom
    if fathom_meetings:
        most_recent = fathom_meetings[0]
        print(f"  📞 Fathom: {len(fathom_meetings)} meetings")
        print(f"     Most recent: {most_recent['date']} - {most_recent['title']}")
    else:
        print(f"  📞 Fathom: ❌ NO MEETINGS IN LAST 14 DAYS")
    
    # HelpScout
    if helpscout_tickets:
        most_recent = helpscout_tickets[0]
        open_tickets = [t for t in helpscout_tickets if t['status'] in ['active', 'pending']]
        print(f"  🎫 HelpScout: {len(helpscout_tickets)} tickets (180 days), {len(open_tickets)} open")
        print(f"     Most recent: {most_recent['created_at'][:10]} - {most_recent['subject'][:50]}")
    else:
        print(f"  🎫 HelpScout: ❌ NO TICKETS IN LAST 180 DAYS")

# Save detailed results
output = {
    'generated_at': datetime.now().isoformat(),
    'fathom_meetings': client_fathom_matches,
    'helpscout_tickets': client_helpscout_matches
}

output_file = os.path.join(parent_dir, 'reports', 'comprehensive_validation_data.json')
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\n✅ Detailed data saved to: {output_file}")
