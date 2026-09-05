#!/usr/bin/env python3
"""
Analyze HelpScout tickets related to user management and inviting new reps
to inform new user functionality development
"""

import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from collections import Counter, defaultdict
from datetime import datetime

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

# Query for user management related tickets
query = """
SELECT DISTINCT
  conversation_id,
  ticket_number,
  ticket_subject,
  ticket_status,
  ticket_preview,
  conv_customer_organization,
  conv_customer_email,
  agent_name,
  ticket_created_at,
  thread_count,
  (SELECT STRING_AGG(tag.tag_name, ', ')
   FROM UNNEST(ticket_tags) as tag) as all_tags
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  LOWER((SELECT STRING_AGG(tag.tag_name, ', ') FROM UNNEST(ticket_tags) as tag)) LIKE '%user management%'
  OR LOWER(ticket_subject) LIKE '%new user%'
  OR LOWER(ticket_subject) LIKE '%invite%'
  OR LOWER(ticket_subject) LIKE '%add user%'
  OR LOWER(ticket_subject) LIKE '%username%'
  OR LOWER(ticket_subject) LIKE '%credentials%'
  OR LOWER(ticket_subject) LIKE '%new rep%'
  OR LOWER(ticket_subject) LIKE '%new employee%'
  OR LOWER(ticket_subject) LIKE '%user access%'
  OR LOWER(ticket_subject) LIKE '%create user%'
  OR LOWER(ticket_subject) LIKE '%set up user%'
  OR LOWER(ticket_subject) LIKE '%setup user%'
  OR LOWER(ticket_preview) LIKE '%new rep%'
  OR LOWER(ticket_preview) LIKE '%new user%'
  OR LOWER(ticket_preview) LIKE '%add a user%'
  OR LOWER(ticket_preview) LIKE '%invite user%'
ORDER BY ticket_created_at DESC
LIMIT 500
"""

print("🔍 Querying BigQuery for user management related tickets...\n")
print("=" * 100)

try:
    results = client.query(query).result()
    
    # Convert to list for analysis
    tickets = []
    for row in results:
        tickets.append({
            'conversation_id': row.conversation_id,
            'ticket_number': row.ticket_number,
            'ticket_subject': row.ticket_subject,
            'ticket_status': row.ticket_status,
            'ticket_preview': row.ticket_preview,
            'conv_customer_organization': row.conv_customer_organization,
            'conv_customer_email': row.conv_customer_email,
            'agent_name': row.agent_name,
            'ticket_created_at': row.ticket_created_at,
            'thread_count': row.thread_count,
            'all_tags': row.all_tags
        })
    
    print(f"\n✅ Retrieved {len(tickets)} user management related tickets\n")
    print("=" * 100)
    
    # Analysis 1: Categorize by request type
    print("\n📊 REQUEST TYPE BREAKDOWN\n")
    print("-" * 100)
    
    request_types = Counter()
    examples_by_type = defaultdict(list)
    
    for ticket in tickets:
        subject = ticket['ticket_subject'].lower()
        preview = (ticket['ticket_preview'] or '').lower()
        tags = (ticket['all_tags'] or '').lower()
        
        # Categorize
        if 'voice message' in subject or 'password reset' in subject:
            request_types['Password Reset'] += 1
            examples_by_type['Password Reset'].append(ticket)
        elif any(word in subject for word in ['new user', 'new ecat user', 'needs username']):
            request_types['New User Account Setup'] += 1
            examples_by_type['New User Account Setup'].append(ticket)
        elif any(word in subject for word in ['invite', 'add user', 'create user', 'set up user', 'setup user']):
            request_types['Add/Invite User'] += 1
            examples_by_type['Add/Invite User'].append(ticket)
        elif any(word in subject for word in ['change', 'update']) and ('email' in subject or 'username' in subject):
            request_types['Email/Username Change'] += 1
            examples_by_type['Email/Username Change'].append(ticket)
        elif 'credentials' in subject or ('username' in subject and 'password' in subject):
            request_types['Credentials Request'] += 1
            examples_by_type['Credentials Request'].append(ticket)
        elif 'access' in subject or 'permission' in subject:
            request_types['Access/Permission Issue'] += 1
            examples_by_type['Access/Permission Issue'].append(ticket)
        elif 'remove' in subject or 'delete' in subject or 'deactivate' in subject:
            request_types['Remove/Deactivate User'] += 1
            examples_by_type['Remove/Deactivate User'].append(ticket)
        else:
            request_types['Other User Management'] += 1
            examples_by_type['Other User Management'].append(ticket)
    
    for req_type, count in request_types.most_common():
        percentage = (count / len(tickets)) * 100
        print(f"{req_type}: {count} tickets ({percentage:.1f}%)")
    
    # Analysis 2: Common pain points and patterns
    print("\n\n🔍 DETAILED ANALYSIS BY CATEGORY\n")
    print("=" * 100)
    
    for req_type, ticket_list in sorted(examples_by_type.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n\n### {req_type.upper()} ({len(ticket_list)} tickets)\n")
        print("-" * 100)
        
        # Show first 5 examples
        for i, ticket in enumerate(ticket_list[:5], 1):
            print(f"\n{i}. Ticket #{ticket['ticket_number']}")
            print(f"   Subject: {ticket['ticket_subject']}")
            print(f"   Customer: {ticket['conv_customer_organization'] or ticket['conv_customer_email'] or 'Unknown'}")
            print(f"   Status: {ticket['ticket_status']}")
            print(f"   Created: {ticket['ticket_created_at']}")
            print(f"   Threads: {ticket['thread_count']}")
            if ticket['all_tags']:
                print(f"   Tags: {ticket['all_tags']}")
            if ticket['ticket_preview']:
                preview = ticket['ticket_preview'][:200] + "..." if len(ticket['ticket_preview']) > 200 else ticket['ticket_preview']
                print(f"   Preview: {preview}")
        
        if len(ticket_list) > 5:
            print(f"\n   ... and {len(ticket_list) - 5} more tickets in this category")
    
    # Analysis 3: Time-based patterns
    print("\n\n📅 TEMPORAL PATTERNS\n")
    print("=" * 100)
    
    # Group by month
    monthly_counts = Counter()
    for ticket in tickets:
        if ticket['ticket_created_at']:
            month = ticket['ticket_created_at'].strftime('%Y-%m')
            monthly_counts[month] += 1
    
    print("\nTickets by Month:")
    for month, count in sorted(monthly_counts.items(), reverse=True)[:12]:
        print(f"  {month}: {count} tickets")
    
    # Analysis 4: Customer patterns
    print("\n\n👥 TOP CUSTOMERS WITH USER MANAGEMENT REQUESTS\n")
    print("=" * 100)
    
    customer_counts = Counter()
    for ticket in tickets:
        customer = ticket['conv_customer_organization'] or ticket['conv_customer_email'] or 'Unknown'
        customer_counts[customer] += 1
    
    print("\nTop 15 Customers:")
    for customer, count in customer_counts.most_common(15):
        print(f"  {customer}: {count} tickets")
    
    # Analysis 5: Key insights for product development
    print("\n\n💡 KEY INSIGHTS FOR NEW USER INVITE FUNCTIONALITY\n")
    print("=" * 100)
    
    # Analyze specific patterns in new user requests
    new_user_tickets = examples_by_type['New User Account Setup'] + examples_by_type['Add/Invite User'] + examples_by_type['Credentials Request']
    
    print(f"\nTotal New User/Invite Related Tickets: {len(new_user_tickets)}")
    print(f"Percentage of all user management tickets: {(len(new_user_tickets) / len(tickets)) * 100:.1f}%")
    
    # Common phrases in these tickets
    print("\n\nCommon Request Patterns:")
    common_phrases = Counter()
    for ticket in new_user_tickets:
        subject = ticket['ticket_subject'].lower()
        preview = (ticket['ticket_preview'] or '').lower()
        full_text = f"{subject} {preview}"
        
        if 'new user' in full_text:
            common_phrases['Requesting new user account'] += 1
        if 'username and password' in full_text or 'credentials' in full_text:
            common_phrases['Requesting credentials/login info'] += 1
        if 'invite' in full_text:
            common_phrases['Wants to invite someone'] += 1
        if 'add' in full_text and 'user' in full_text:
            common_phrases['Wants to add a user'] += 1
        if 'new employee' in full_text or 'new rep' in full_text:
            common_phrases['New employee/rep onboarding'] += 1
        if 'access' in full_text:
            common_phrases['Needs access granted'] += 1
        if 'set up' in full_text or 'setup' in full_text:
            common_phrases['Needs help setting up user'] += 1
    
    for phrase, count in common_phrases.most_common():
        percentage = (count / len(new_user_tickets)) * 100
        print(f"  • {phrase}: {count} ({percentage:.1f}%)")
    
    # Save detailed results to file
    output_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "reports/user_management_analysis.json"
    )
    
    with open(output_file, 'w') as f:
        json.dump({
            'total_tickets': len(tickets),
            'request_types': dict(request_types),
            'monthly_counts': dict(monthly_counts),
            'top_customers': dict(customer_counts.most_common(20)),
            'new_user_patterns': dict(common_phrases),
            'sample_tickets': {
                req_type: [
                    {
                        'ticket_number': t['ticket_number'],
                        'subject': t['ticket_subject'],
                        'preview': t['ticket_preview'][:300] if t['ticket_preview'] else None,
                        'customer': t['conv_customer_organization'] or t['conv_customer_email'],
                        'created_at': t['ticket_created_at'].isoformat() if t['ticket_created_at'] else None
                    }
                    for t in ticket_list[:10]
                ]
                for req_type, ticket_list in examples_by_type.items()
            }
        }, f, indent=2, default=str)
    
    print(f"\n\n✅ Detailed analysis saved to: {output_file}")
    
    # Print recommendations
    print("\n\n🎯 PRODUCT RECOMMENDATIONS\n")
    print("=" * 100)
    print("""
Based on the analysis of user management tickets, here are key recommendations for 
new user invite functionality:

1. SELF-SERVICE USER INVITES
   • Allow admins to invite new users directly from the platform
   • Reduce dependency on support for basic user additions
   • Provide clear role/permission selection during invite

2. AUTOMATED CREDENTIAL DELIVERY
   • Send automated welcome emails with login instructions
   • Reduce "username and password" support requests
   • Include password reset link in welcome email

3. BULK USER IMPORT
   • Enable CSV upload for multiple user additions
   • Useful for customers with frequent new employee onboarding
   • Reduce repetitive support tickets from high-volume customers

4. USER MANAGEMENT DASHBOARD
   • Clear view of all users and their status
   • Easy enable/disable user access
   • Track pending invites and resend if needed

5. ROLE-BASED TEMPLATES
   • Pre-defined permission sets for common roles (rep, manager, admin)
   • Simplify the user setup process
   • Reduce configuration errors

6. ONBOARDING WORKFLOW
   • Step-by-step guide for new users after first login
   • Reduce "how do I..." training requests
   • Include video tutorials or interactive walkthroughs
""")
    
    print("\n" + "=" * 100)
    print("✅ Analysis complete!")
    
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}")
    import traceback
    traceback.print_exc()
