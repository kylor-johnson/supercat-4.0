#!/usr/bin/env python3
"""
Find key contacts at DCCL and KRB from HelpScout tickets and Fathom calls
"""

import os
import sys
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, timedelta

# Add integrations to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "integrations"))
from fathom.fathom_api import get_meetings, get_transcript, get_recording

# Service account path
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "integrations/bigquery/service-account/supercat-data-pipeline-dbfab43c27bb.json"
)

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Create BigQuery client
client = bigquery.Client(credentials=credentials, project="supercat-data-pipeline")

def query_helpscout_tickets(company_keywords):
    """Query HelpScout for tickets from specific companies"""
    
    # Build WHERE clause for company matching
    company_conditions = " OR ".join([
        f"LOWER(conv_customer_organization) LIKE '%{keyword.lower()}%'"
        for keyword in company_keywords
    ])
    
    query = f"""
    SELECT DISTINCT
      conversation_id,
      ticket_number,
      ticket_subject,
      ticket_status,
      ticket_preview,
      conv_customer_organization,
      conv_customer_email,
      conv_creator_name,
      agent_name,
      ticket_created_at,
      thread_count,
      thread_customer_name,
      thread_customer_email_value,
      (SELECT STRING_AGG(tag.tag_name, ', ')
       FROM UNNEST(ticket_tags) as tag) as all_tags
    FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
    WHERE ({company_conditions})
    ORDER BY ticket_created_at DESC
    LIMIT 100
    """
    
    print(f"🔍 Querying HelpScout tickets for: {', '.join(company_keywords)}\n")
    print("=" * 100)
    
    try:
        results = client.query(query).result()
        
        # Collect unique contacts
        contacts = {}
        tickets_by_contact = {}
        
        for row in results:
            # Try multiple email fields
            email = row.conv_customer_email or row.thread_customer_email_value
            name = row.conv_creator_name or row.thread_customer_name or "Unknown"
            org = row.conv_customer_organization or "Unknown"
            
            if email:
                if email not in contacts:
                    contacts[email] = {
                        "name": name,
                        "organization": org,
                        "tickets": [],
                        "first_seen": row.ticket_created_at,
                        "last_seen": row.ticket_created_at
                    }
                
                contacts[email]["tickets"].append({
                    "number": row.ticket_number,
                    "subject": row.ticket_subject,
                    "created": row.ticket_created_at,
                    "status": row.ticket_status,
                    "agent": row.agent_name,
                    "tags": row.all_tags
                })
                
                # Update last seen
                if row.ticket_created_at > contacts[email]["last_seen"]:
                    contacts[email]["last_seen"] = row.ticket_created_at
        
        return contacts, results.total_rows
        
    except Exception as e:
        print(f"❌ Error querying BigQuery: {e}")
        return {}, 0

def search_fathom_meetings(company_keywords):
    """Search Fathom meetings for specific companies"""
    
    print(f"\n🎥 Searching Fathom meetings for: {', '.join(company_keywords)}\n")
    print("=" * 100)
    
    try:
        # Get all meetings (with pagination)
        print("Fetching meetings from Fathom API...")
        meetings = get_meetings(limit=200, paginate=True)
        
        print(f"Retrieved {len(meetings)} meetings, filtering for relevant companies...\n")
        
        # Filter meetings by company keywords
        relevant_meetings = []
        contacts_from_meetings = {}
        
        for meeting in meetings:
            title = meeting.get("title", "").lower()
            
            # Check if any keyword appears in the title
            if any(keyword.lower() in title for keyword in company_keywords):
                relevant_meetings.append(meeting)
                
                # Extract attendees
                attendees = meeting.get("attendees", [])
                for attendee in attendees:
                    email = attendee.get("email")
                    name = attendee.get("name", "Unknown")
                    
                    if email:
                        if email not in contacts_from_meetings:
                            contacts_from_meetings[email] = {
                                "name": name,
                                "meetings": [],
                                "first_meeting": meeting.get("start_time"),
                                "last_meeting": meeting.get("start_time")
                            }
                        
                        contacts_from_meetings[email]["meetings"].append({
                            "title": meeting.get("title"),
                            "date": meeting.get("start_time"),
                            "recording_id": meeting.get("recording_id"),
                            "duration": meeting.get("duration_minutes")
                        })
        
        return contacts_from_meetings, relevant_meetings
        
    except Exception as e:
        print(f"❌ Error querying Fathom: {e}")
        return {}, []

def main():
    # Companies to search for
    companies = ["DCCL", "Donald Choi", "KRB", "Kaleen", "Kaleen Rugs"]
    
    print("🔎 FINDING KEY CONTACTS FOR DCCL AND KRB")
    print("=" * 100)
    print(f"Search terms: {', '.join(companies)}\n")
    
    # Query HelpScout
    helpscout_contacts, total_tickets = query_helpscout_tickets(companies)
    
    print(f"\n✅ Found {total_tickets} HelpScout tickets")
    print(f"✅ Identified {len(helpscout_contacts)} unique contacts from HelpScout\n")
    
    # Query Fathom
    fathom_contacts, fathom_meetings = search_fathom_meetings(companies)
    
    print(f"\n✅ Found {len(fathom_meetings)} relevant Fathom meetings")
    print(f"✅ Identified {len(fathom_contacts)} unique contacts from Fathom\n")
    
    # Combine and analyze
    print("\n" + "=" * 100)
    print("📊 CONTACT ANALYSIS")
    print("=" * 100)
    
    # Merge contacts
    all_contacts = {}
    
    # Add HelpScout contacts
    for email, data in helpscout_contacts.items():
        all_contacts[email] = {
            "email": email,
            "name": data["name"],
            "organization": data["organization"],
            "helpscout_tickets": len(data["tickets"]),
            "recent_tickets": sorted(data["tickets"], key=lambda x: x["created"], reverse=True)[:3],
            "fathom_meetings": 0,
            "recent_meetings": [],
            "first_interaction": data["first_seen"],
            "last_interaction": data["last_seen"]
        }
    
    # Add Fathom contacts
    for email, data in fathom_contacts.items():
        if email not in all_contacts:
            all_contacts[email] = {
                "email": email,
                "name": data["name"],
                "organization": "Unknown",
                "helpscout_tickets": 0,
                "recent_tickets": [],
                "fathom_meetings": 0,
                "recent_meetings": [],
                "first_interaction": data["first_meeting"],
                "last_interaction": data["last_meeting"]
            }
        
        all_contacts[email]["fathom_meetings"] = len(data["meetings"])
        all_contacts[email]["recent_meetings"] = sorted(data["meetings"], key=lambda x: x["date"], reverse=True)[:3]
        
        # Update last interaction if more recent
        if data["last_meeting"] and data["last_meeting"] > all_contacts[email]["last_interaction"]:
            all_contacts[email]["last_interaction"] = data["last_meeting"]
    
    # Sort by engagement (tickets + meetings) and recency
    sorted_contacts = sorted(
        all_contacts.values(),
        key=lambda x: (x["helpscout_tickets"] + x["fathom_meetings"], x["last_interaction"]),
        reverse=True
    )
    
    # Display results
    print("\n🎯 TOP CONTACTS TO EMAIL (Sorted by engagement and recency):\n")
    
    for i, contact in enumerate(sorted_contacts[:10], 1):
        print(f"\n{i}. {contact['name']} <{contact['email']}>")
        print(f"   Organization: {contact['organization']}")
        print(f"   Engagement: {contact['helpscout_tickets']} HelpScout tickets, {contact['fathom_meetings']} Fathom meetings")
        print(f"   Last interaction: {contact['last_interaction']}")
        
        if contact['recent_tickets']:
            print(f"\n   Recent HelpScout Tickets:")
            for ticket in contact['recent_tickets']:
                print(f"     • #{ticket['number']}: {ticket['subject'][:60]}")
                print(f"       {ticket['created']} | Status: {ticket['status']} | Agent: {ticket['agent']}")
        
        if contact['recent_meetings']:
            print(f"\n   Recent Fathom Meetings:")
            for meeting in contact['recent_meetings']:
                print(f"     • {meeting['title'][:60]}")
                print(f"       {meeting['date']} | {meeting['duration']} min")
        
        print("-" * 100)
    
    # Save to JSON
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "reports/dccl_krb_contacts.json"
    )
    
    with open(output_file, 'w') as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "companies_searched": companies,
            "total_helpscout_tickets": total_tickets,
            "total_fathom_meetings": len(fathom_meetings),
            "unique_contacts": len(all_contacts),
            "contacts": sorted_contacts
        }, f, indent=2, default=str)
    
    print(f"\n💾 Full report saved to: {output_file}")
    
    # Print summary recommendation
    print("\n" + "=" * 100)
    print("📧 RECOMMENDED EMAIL RECIPIENTS")
    print("=" * 100)
    print("\nBased on engagement and recency, you should email:\n")
    
    for i, contact in enumerate(sorted_contacts[:5], 1):
        print(f"{i}. {contact['name']} <{contact['email']}> - {contact['organization']}")
        print(f"   ({contact['helpscout_tickets']} tickets, {contact['fathom_meetings']} meetings, last: {contact['last_interaction']})\n")

if __name__ == "__main__":
    main()
