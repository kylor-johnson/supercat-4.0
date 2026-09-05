#!/usr/bin/env python3
"""
Comprehensive Validation Script
Collects ALL Fathom and HelpScout data for stage-gated validation
"""

import sys
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import Fathom integration
sys.path.insert(0, os.path.join(parent_dir, 'integrations/fathom'))
from fathom_api import get_meetings, get_summary

# Client data
CLIENTS = {
    'cst': {'name': 'Coaster Furniture', 'domain': 'coasterfurniture.com'},
    'dccl': {'name': 'Donald Choi Canada', 'domain': 'donaldchoi.com'},
    'krb': {'name': 'Kaleen Rugs', 'domain': 'kaleenrugs.com'},
    'mali': {'name': 'Magic Lite', 'domain': 'magiclite.com'},
    'pebl': {'name': 'Pebl', 'domain': 'pebl.com'},
    'tcd': {'name': 'Terracotta Designs', 'domain': 'terracottadesigns.com'}
}

def match_meeting_to_client(meeting, summary=None):
    """Match a meeting to a client using multiple signals"""
    title = meeting.get('meeting_title', '').lower()
    matched_clients = []
    
    # Check title for client names
    for shortname, client in CLIENTS.items():
        client_name = client['name'].lower()
        # Check for full name or shortname
        if client_name in title or shortname in title:
            matched_clients.append((shortname, 'title_match'))
    
    # Check attendees if we have summary
    if summary and 'attendees' in summary:
        for attendee in summary.get('attendees', []):
            if isinstance(attendee, dict):
                email = attendee.get('email', '').lower()
                for shortname, client in CLIENTS.items():
                    domain = client['domain'].lower()
                    if domain in email:
                        matched_clients.append((shortname, 'email_domain'))
    
    return matched_clients

def main():
    print("="*80)
    print("COMPREHENSIVE VALIDATION - FATHOM MEETINGS")
    print("="*80)
    
    # Get all meetings
    meetings = get_meetings()
    cutoff = (datetime.now() - timedelta(days=14)).isoformat()
    
    recent_meetings = [m for m in meetings if m.get('recording_start_time', '') >= cutoff]
    print(f"\nTotal meetings in last 14 days: {len(recent_meetings)}\n")
    
    # Track matches
    client_meetings = defaultdict(list)
    
    # First pass: match by title
    for meeting in sorted(recent_meetings, key=lambda x: x.get('recording_start_time', ''), reverse=True):
        title = meeting.get('meeting_title', '')
        rid = meeting.get('recording_id')
        start = meeting.get('recording_start_time', '')[:10]
        
        matches = match_meeting_to_client(meeting)
        
        if matches:
            for shortname, method in matches:
                client_meetings[shortname].append({
                    'id': rid,
                    'title': title,
                    'date': start,
                    'match_method': method
                })
                print(f"✓ MATCH: {shortname.upper()} | {start} | {title} | ({method})")
    
    print("\n" + "="*80)
    print("GETTING MEETING SUMMARIES")
    print("="*80 + "\n")
    
    # Get summaries for matched meetings
    for shortname, meetings_list in client_meetings.items():
        print(f"\n--- {shortname.upper()} ({CLIENTS[shortname]['name']}) ---")
        for meeting in meetings_list[:2]:  # Get summaries for up to 2 most recent
            rid = meeting['id']
            print(f"\nGetting summary for: {meeting['title']}")
            print(f"Recording ID: {rid}")
            
            try:
                summary = get_summary(rid)
                if summary:
                    # Extract key info
                    summary_text = summary.get('summary', {})
                    if isinstance(summary_text, dict):
                        summary_text = summary_text.get('markdown_formatted', summary_text.get('text', ''))
                    
                    print(f"Summary: {str(summary_text)[:500]}...")
                    
                    # Action items
                    action_items = summary.get('action_items', [])
                    if action_items:
                        print(f"Action Items: {len(action_items)}")
                        for item in action_items[:3]:
                            if isinstance(item, dict):
                                print(f"  - {item.get('content', item.get('text', str(item)))}")
                    
                    # Attendees
                    attendees = summary.get('attendees', [])
                    if attendees:
                        print(f"Attendees:")
                        for a in attendees[:5]:
                            if isinstance(a, dict):
                                print(f"  - {a.get('name', 'Unknown')} ({a.get('email', 'no email')})")
                    
                    meeting['summary'] = summary
            except Exception as e:
                print(f"Error getting summary: {e}")
    
    # Output results
    print("\n" + "="*80)
    print("SUMMARY BY CLIENT")
    print("="*80)
    
    for shortname in ['cst', 'dccl', 'krb', 'mali', 'pebl', 'tcd']:
        meetings_list = client_meetings.get(shortname, [])
        print(f"\n{shortname.upper()} ({CLIENTS[shortname]['name']})")
        print(f"  Meetings found: {len(meetings_list)}")
        if meetings_list:
            most_recent = meetings_list[0]
            print(f"  Most recent: {most_recent['date']} - {most_recent['title']}")
        else:
            print(f"  ❌ NO MEETINGS FOUND IN LAST 14 DAYS")
    
    # Save to JSON
    output_file = os.path.join(parent_dir, 'reports', 'fathom_validation_data.json')
    with open(output_file, 'w') as f:
        json.dump(dict(client_meetings), f, indent=2, default=str)
    
    print(f"\n✅ Data saved to: {output_file}")

if __name__ == '__main__':
    main()
