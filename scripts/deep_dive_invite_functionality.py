#!/usr/bin/env python3
"""
Deep dive analysis into invite/add user workflows to understand:
1. Current pain points in the process
2. Common workflows and use cases
3. Time to resolution
4. Multi-touch vs single-touch requests
"""

import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from collections import Counter, defaultdict
from datetime import datetime, timedelta

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

print("=" * 100)
print("🔍 DEEP DIVE: USER INVITE FUNCTIONALITY ANALYSIS")
print("=" * 100)

# Query 1: Get all new user/invite related tickets with full details
query_new_users = """
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
  ticket_closed_at,
  thread_count,
  (SELECT STRING_AGG(tag.tag_name, ', ')
   FROM UNNEST(ticket_tags) as tag) as all_tags
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  (LOWER(ticket_subject) LIKE '%new user%'
  OR LOWER(ticket_subject) LIKE '%invite%'
  OR LOWER(ticket_subject) LIKE '%add user%'
  OR LOWER(ticket_subject) LIKE '%create user%'
  OR LOWER(ticket_subject) LIKE '%set up user%'
  OR LOWER(ticket_subject) LIKE '%setup user%'
  OR LOWER(ticket_subject) LIKE '%needs username%'
  OR LOWER(ticket_subject) LIKE '%new rep%'
  OR LOWER(ticket_subject) LIKE '%new employee%'
  OR LOWER(ticket_preview) LIKE '%add a new user%'
  OR LOWER(ticket_preview) LIKE '%invite a user%'
  OR LOWER(ticket_preview) LIKE '%new rep%'
  OR LOWER(ticket_preview) LIKE '%new employee%')
  AND ticket_created_at >= '2025-01-01'
ORDER BY ticket_created_at DESC
"""

print("\n📊 PART 1: NEW USER/INVITE TICKET ANALYSIS\n")
print("-" * 100)

results = client.query(query_new_users).result()

tickets = []
for row in results:
    ticket = {
        'conversation_id': row.conversation_id,
        'ticket_number': row.ticket_number,
        'ticket_subject': row.ticket_subject,
        'ticket_status': row.ticket_status,
        'ticket_preview': row.ticket_preview,
        'conv_customer_organization': row.conv_customer_organization,
        'conv_customer_email': row.conv_customer_email,
        'agent_name': row.agent_name,
        'ticket_created_at': row.ticket_created_at,
        'ticket_closed_at': row.ticket_closed_at,
        'thread_count': row.thread_count,
        'all_tags': row.all_tags
    }
    tickets.append(ticket)

print(f"Total new user/invite tickets (2025+): {len(tickets)}\n")

# Analysis 1: Resolution time
print("\n⏱️  RESOLUTION TIME ANALYSIS\n")
print("-" * 100)

resolution_times = []
for ticket in tickets:
    if ticket['ticket_created_at'] and ticket['ticket_closed_at']:
        time_diff = ticket['ticket_closed_at'] - ticket['ticket_created_at']
        hours = time_diff.total_seconds() / 3600
        resolution_times.append({
            'ticket_number': ticket['ticket_number'],
            'hours': hours,
            'threads': ticket['thread_count'],
            'subject': ticket['ticket_subject']
        })

if resolution_times:
    avg_hours = sum(r['hours'] for r in resolution_times) / len(resolution_times)
    median_hours = sorted(r['hours'] for r in resolution_times)[len(resolution_times) // 2]
    
    print(f"Tickets with resolution time: {len(resolution_times)}")
    print(f"Average resolution time: {avg_hours:.1f} hours ({avg_hours/24:.1f} days)")
    print(f"Median resolution time: {median_hours:.1f} hours ({median_hours/24:.1f} days)")
    
    # Categorize by resolution speed
    fast = sum(1 for r in resolution_times if r['hours'] < 2)
    same_day = sum(1 for r in resolution_times if 2 <= r['hours'] < 24)
    next_day = sum(1 for r in resolution_times if 24 <= r['hours'] < 48)
    slow = sum(1 for r in resolution_times if r['hours'] >= 48)
    
    print(f"\nResolution Speed Distribution:")
    print(f"  • Fast (<2 hours): {fast} tickets ({fast/len(resolution_times)*100:.1f}%)")
    print(f"  • Same day (2-24 hours): {same_day} tickets ({same_day/len(resolution_times)*100:.1f}%)")
    print(f"  • Next day (24-48 hours): {next_day} tickets ({next_day/len(resolution_times)*100:.1f}%)")
    print(f"  • Slow (>48 hours): {slow} tickets ({slow/len(resolution_times)*100:.1f}%)")
    
    # Show slowest tickets
    print(f"\n🐌 Slowest Resolutions (Top 10):")
    for i, r in enumerate(sorted(resolution_times, key=lambda x: x['hours'], reverse=True)[:10], 1):
        print(f"  {i}. Ticket #{r['ticket_number']}: {r['hours']:.1f} hours ({r['hours']/24:.1f} days)")
        print(f"     Subject: {r['subject']}")
        print(f"     Threads: {r['threads']}")

# Analysis 2: Thread count (complexity indicator)
print("\n\n💬 THREAD COUNT ANALYSIS (Complexity Indicator)\n")
print("-" * 100)

thread_counts = [t['thread_count'] for t in tickets if t['thread_count']]
if thread_counts:
    avg_threads = sum(thread_counts) / len(thread_counts)
    print(f"Average threads per ticket: {avg_threads:.1f}")
    
    single_touch = sum(1 for t in thread_counts if t == 1)
    low_touch = sum(1 for t in thread_counts if 2 <= t <= 3)
    medium_touch = sum(1 for t in thread_counts if 4 <= t <= 6)
    high_touch = sum(1 for t in thread_counts if t > 6)
    
    print(f"\nComplexity Distribution:")
    print(f"  • Single-touch (1 thread): {single_touch} tickets ({single_touch/len(thread_counts)*100:.1f}%)")
    print(f"  • Low-touch (2-3 threads): {low_touch} tickets ({low_touch/len(thread_counts)*100:.1f}%)")
    print(f"  • Medium-touch (4-6 threads): {medium_touch} tickets ({medium_touch/len(thread_counts)*100:.1f}%)")
    print(f"  • High-touch (>6 threads): {high_touch} tickets ({high_touch/len(thread_counts)*100:.1f}%)")
    
    # Show high-touch tickets
    print(f"\n🔥 High-Touch Tickets (>6 threads):")
    high_touch_tickets = [t for t in tickets if t['thread_count'] and t['thread_count'] > 6]
    for i, t in enumerate(sorted(high_touch_tickets, key=lambda x: x['thread_count'], reverse=True)[:10], 1):
        print(f"  {i}. Ticket #{t['ticket_number']}: {t['thread_count']} threads")
        print(f"     Subject: {t['ticket_subject']}")
        print(f"     Customer: {t['conv_customer_organization'] or t['conv_customer_email'] or 'Unknown'}")

# Analysis 3: Common pain points in ticket content
print("\n\n🚨 COMMON PAIN POINTS\n")
print("-" * 100)

pain_points = Counter()
for ticket in tickets:
    subject = ticket['ticket_subject'].lower()
    preview = (ticket['ticket_preview'] or '').lower()
    full_text = f"{subject} {preview}"
    
    # Identify pain points
    if any(word in full_text for word in ['cannot', 'can\'t', 'unable', 'not working', 'issue', 'problem', 'error']):
        pain_points['Encountering errors/issues'] += 1
    if any(word in full_text for word in ['how do i', 'how to', 'how can i', 'help with']):
        pain_points['Needs guidance on process'] += 1
    if any(word in full_text for word in ['waiting', 'pending', 'not approved', 'not activated']):
        pain_points['Waiting for approval/activation'] += 1
    if any(word in full_text for word in ['forgot', 'lost', 'reset', 'password']):
        pain_points['Password/credential issues'] += 1
    if any(word in full_text for word in ['wrong', 'incorrect', 'misspelled', 'typo']):
        pain_points['Data entry errors'] += 1
    if any(word in full_text for word in ['not receiving', 'didn\'t get', 'no email']):
        pain_points['Email delivery issues'] += 1
    if any(word in full_text for word in ['permission', 'access denied', 'can\'t access']):
        pain_points['Permission/access issues'] += 1

for pain_point, count in pain_points.most_common():
    percentage = (count / len(tickets)) * 100
    print(f"  • {pain_point}: {count} tickets ({percentage:.1f}%)")

# Analysis 4: Workflow patterns
print("\n\n🔄 WORKFLOW PATTERNS\n")
print("-" * 100)

workflow_patterns = Counter()
for ticket in tickets:
    subject = ticket['ticket_subject'].lower()
    preview = (ticket['ticket_preview'] or '').lower()
    full_text = f"{subject} {preview}"
    
    # Identify workflow types
    if 'needs username' in full_text or 'username and password' in full_text:
        workflow_patterns['Admin requests credentials for new user'] += 1
    elif 'new user' in subject and 'add' not in full_text:
        workflow_patterns['Admin reports new user added (notification)'] += 1
    elif 'invite' in full_text:
        workflow_patterns['Admin wants to invite/send invite'] += 1
    elif 'add user' in full_text or 'create user' in full_text:
        workflow_patterns['Admin wants to add/create user'] += 1
    elif 'set up' in full_text or 'setup' in full_text:
        workflow_patterns['Admin needs help setting up user'] += 1
    elif 'new employee' in full_text or 'new rep' in full_text:
        workflow_patterns['Onboarding new employee/rep'] += 1

print("Most Common Workflows:")
for workflow, count in workflow_patterns.most_common():
    percentage = (count / len(tickets)) * 100
    print(f"  • {workflow}: {count} tickets ({percentage:.1f}%)")

# Analysis 5: Self-service potential
print("\n\n🎯 SELF-SERVICE POTENTIAL\n")
print("-" * 100)

self_service_candidates = 0
requires_support = 0

for ticket in tickets:
    subject = ticket['ticket_subject'].lower()
    preview = (ticket['ticket_preview'] or '').lower()
    full_text = f"{subject} {preview}"
    threads = ticket['thread_count'] or 0
    
    # Criteria for self-service potential:
    # - Simple request (low thread count)
    # - Standard workflow
    # - No errors or issues mentioned
    
    is_simple = threads <= 2
    is_standard = any(pattern in full_text for pattern in [
        'new user', 'add user', 'invite', 'username and password'
    ])
    has_issues = any(word in full_text for word in [
        'cannot', 'can\'t', 'unable', 'not working', 'issue', 'problem', 'error'
    ])
    
    if is_simple and is_standard and not has_issues:
        self_service_candidates += 1
    else:
        requires_support += 1

total = self_service_candidates + requires_support
print(f"Tickets that could be self-service: {self_service_candidates} ({self_service_candidates/total*100:.1f}%)")
print(f"Tickets requiring support: {requires_support} ({requires_support/total*100:.1f}%)")

print("\n💡 Interpretation:")
print(f"   Up to {self_service_candidates} tickets ({self_service_candidates/total*100:.1f}%) could potentially be")
print(f"   handled through self-service user invite functionality, reducing")
print(f"   support burden and improving time-to-value for customers.")

# Query 2: Get broader user management context
print("\n\n📊 PART 2: BROADER USER MANAGEMENT CONTEXT\n")
print("-" * 100)

query_all_user_mgmt = """
SELECT 
  (SELECT STRING_AGG(tag.tag_name, ', ') FROM UNNEST(ticket_tags) as tag) as all_tags,
  COUNT(*) as ticket_count
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
WHERE 
  LOWER((SELECT STRING_AGG(tag.tag_name, ', ') FROM UNNEST(ticket_tags) as tag)) LIKE '%user management%'
  AND ticket_created_at >= '2025-01-01'
GROUP BY all_tags
ORDER BY ticket_count DESC
LIMIT 50
"""

results = client.query(query_all_user_mgmt).result()

print("\nUser Management Tag Combinations (2025+):")
for row in results:
    if row.all_tags:
        print(f"  • {row.all_tags}: {row.ticket_count} tickets")

# Save comprehensive report
output = {
    'analysis_date': datetime.now().isoformat(),
    'total_tickets_analyzed': len(tickets),
    'resolution_time': {
        'average_hours': avg_hours if resolution_times else None,
        'median_hours': median_hours if resolution_times else None,
        'distribution': {
            'fast_under_2h': fast if resolution_times else 0,
            'same_day_2_24h': same_day if resolution_times else 0,
            'next_day_24_48h': next_day if resolution_times else 0,
            'slow_over_48h': slow if resolution_times else 0
        }
    },
    'complexity': {
        'average_threads': avg_threads if thread_counts else None,
        'distribution': {
            'single_touch': single_touch if thread_counts else 0,
            'low_touch': low_touch if thread_counts else 0,
            'medium_touch': medium_touch if thread_counts else 0,
            'high_touch': high_touch if thread_counts else 0
        }
    },
    'pain_points': dict(pain_points),
    'workflow_patterns': dict(workflow_patterns),
    'self_service_potential': {
        'candidates': self_service_candidates,
        'requires_support': requires_support,
        'percentage_self_serviceable': (self_service_candidates/total*100) if total > 0 else 0
    },
    'sample_tickets': [
        {
            'ticket_number': t['ticket_number'],
            'subject': t['ticket_subject'],
            'preview': t['ticket_preview'][:300] if t['ticket_preview'] else None,
            'customer': t['conv_customer_organization'] or t['conv_customer_email'],
            'threads': t['thread_count'],
            'created_at': t['ticket_created_at'].isoformat() if t['ticket_created_at'] else None,
            'closed_at': t['ticket_closed_at'].isoformat() if t['ticket_closed_at'] else None
        }
        for t in tickets[:50]
    ]
}

output_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports/invite_functionality_deep_dive.json"
)

with open(output_file, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\n\n✅ Detailed analysis saved to: {output_file}")

# Final recommendations
print("\n\n" + "=" * 100)
print("🎯 KEY RECOMMENDATIONS FOR INVITE FUNCTIONALITY")
print("=" * 100)

print("""
Based on the deep dive analysis, here are prioritized recommendations:

1. PRIORITY 1: AUTOMATED INVITE WORKFLOW
   • Enable admins to send invite emails directly from platform
   • Auto-generate secure credentials or allow user to set password
   • Include clear onboarding instructions in invite email
   • Estimated impact: Could reduce {0} tickets/year ({1:.1f}% of user mgmt tickets)

2. PRIORITY 2: BULK USER OPERATIONS
   • CSV upload for multiple user invites
   • Particularly valuable for high-volume customers (Capital Lighting, Wildwood, etc.)
   • Include validation and error handling
   • Estimated impact: Reduce high-touch tickets by {2}%

3. PRIORITY 3: IMPROVED EMAIL DELIVERY
   • Ensure invite emails are not blocked/filtered
   • Add "resend invite" functionality
   • Show invite status (pending, accepted, expired)
   • Estimated impact: Address {3:.1f}% of pain points

4. PRIORITY 4: ROLE-BASED QUICK SETUP
   • Pre-configured permission templates (Rep, Manager, Admin)
   • One-click user setup with standard permissions
   • Reduce configuration complexity
   • Estimated impact: Reduce resolution time by {4:.1f}%

5. PRIORITY 5: SELF-SERVICE KNOWLEDGE BASE
   • Step-by-step guides for common user management tasks
   • Video tutorials for user invite workflow
   • FAQ section for common issues
   • Estimated impact: Deflect {5:.1f}% of "how to" requests

METRICS TO TRACK POST-LAUNCH:
• Reduction in user management support tickets
• Time to first login for new users
• Admin satisfaction with invite process
• Percentage of successful self-service invites
""".format(
    self_service_candidates,
    (self_service_candidates/len(tickets)*100) if len(tickets) > 0 else 0,
    (high_touch/len(thread_counts)*100) if thread_counts else 0,
    (pain_points.get('Email delivery issues', 0)/len(tickets)*100) if len(tickets) > 0 else 0,
    ((same_day + next_day + slow) / len(resolution_times) * 100) if resolution_times else 0,
    (pain_points.get('Needs guidance on process', 0)/len(tickets)*100) if len(tickets) > 0 else 0
))

print("=" * 100)
print("✅ Deep dive analysis complete!")
print("=" * 100)
