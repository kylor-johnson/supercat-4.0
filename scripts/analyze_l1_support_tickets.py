#!/usr/bin/env python3
"""
Analyze L1/First-Touch Support Tickets to identify common request types
"""

import json
import re
from collections import Counter, defaultdict

# Read the data file
with open('/Users/kylorjohnson/.cursor/projects/Users-kylorjohnson-Library-Mobile-Documents-com-apple-CloudDocs-SuperCat-4-0/agent-tools/41fb72df-b08d-4dba-bb9e-05ef003e2407.txt', 'r') as f:
    data = json.load(f)

print(f"Total L1/First-Touch Tickets: {len(data)}\n")
print("=" * 80)

# Categorize by tags
tag_categories = defaultdict(list)
for ticket in data:
    tags = ticket.get('all_tags', '') or ''
    ticket_num = ticket['ticket_number']
    subject = ticket['ticket_subject']
    preview = ticket['ticket_preview'] or ''
    
    # Extract type tags
    if 'type: user management' in tags.lower():
        tag_categories['User Management'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: training' in tags.lower():
        tag_categories['Training/How-To'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: data-sync' in tags.lower():
        tag_categories['Data Sync/Imports'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: image asset' in tags.lower():
        tag_categories['Image Assets'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: sales and finance' in tags.lower():
        tag_categories['Sales/Finance'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: feature request' in tags.lower():
        tag_categories['Feature Requests'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: config issue' in tags.lower():
        tag_categories['Configuration'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'type: orders invoices' in tags.lower():
        tag_categories['Orders/Invoices'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })
    if 'password reset email' in tags.lower():
        tag_categories['Password Reset'].append({
            'num': ticket_num,
            'subject': subject,
            'preview': preview[:150]
        })

# Print summary
print("\n📊 CATEGORY BREAKDOWN\n")
for category, tickets in sorted(tag_categories.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"{category}: {len(tickets)} tickets")

# Analyze subjects for patterns
print("\n\n🔍 SUBJECT LINE ANALYSIS\n")
print("=" * 80)

subject_patterns = Counter()
for ticket in data:
    subject = ticket['ticket_subject'].lower()
    
    # Password/login related
    if any(word in subject for word in ['password', 'login', 'voice message', 'username']):
        subject_patterns['Password/Login Issues'] += 1
    # New user
    elif any(word in subject for word in ['new user', 'new ecat user', 'credentials']):
        subject_patterns['New User Setup'] += 1
    # Email/username changes
    elif any(word in subject for word in ['change', 'email address', 'update']):
        subject_patterns['Email/Username Updates'] += 1
    # Questions
    elif any(word in subject for word in ['question', 'how', 'help please']):
        subject_patterns['General Questions'] += 1
    # Image/logo
    elif any(word in subject for word in ['image', 'logo', 'photo']):
        subject_patterns['Image/Logo Issues'] += 1
    # Report
    elif any(word in subject for word in ['report', 'export']):
        subject_patterns['Report Requests'] += 1
    # Order
    elif any(word in subject for word in ['order', 'invoice']):
        subject_patterns['Order/Invoice Issues'] += 1
    # Pricing
    elif any(word in subject for word in ['price', 'pricing']):
        subject_patterns['Pricing Questions'] += 1
    # Enrollment
    elif any(word in subject for word in ['enrollment', 'register', 'account']):
        subject_patterns['Account/Enrollment'] += 1
    # Import/sync
    elif any(word in subject for word in ['import', 'sync', 'upload']):
        subject_patterns['Import/Sync Issues'] += 1
    # Scan
    elif any(word in subject for word in ['scan', 'barcode']):
        subject_patterns['Scanning Issues'] += 1
    else:
        subject_patterns['Other'] += 1

for pattern, count in subject_patterns.most_common(15):
    print(f"{pattern}: {count} tickets")

print("\n\n📝 TOP 10 MOST COMMON SPECIFIC REQUESTS\n")
print("=" * 80)

# Analyze specific request types
specific_requests = Counter()
for ticket in data:
    subject = ticket['ticket_subject'].lower()
    preview = (ticket['ticket_preview'] or '').lower()
    
    # Be very specific
    if 'voice message' in subject:
        specific_requests['Voice Message (Password Reset)'] += 1
    elif 'password' in subject and 'reset' in subject:
        specific_requests['Password Reset Request'] += 1
    elif 'username and password' in subject or 'needs username' in subject:
        specific_requests['New User Credentials Request'] += 1
    elif 'change' in subject and ('login' in subject or 'email' in subject):
        specific_requests['Email/Username Change'] += 1
    elif 'new user' in subject or 'new ecat user' in subject:
        specific_requests['New User Account Setup'] += 1
    elif 'question' in subject:
        specific_requests['General How-To Question'] += 1
    elif 'image' in subject or 'logo' in subject:
        specific_requests['Image/Logo Update'] += 1
    elif 'report' in subject:
        specific_requests['Report Generation Question'] += 1
    elif 'verify' in subject and 'company' in subject:
        specific_requests['Company Info Verification'] += 1
    elif 'price' in subject or 'pricing' in subject:
        specific_requests['Pricing Configuration Question'] += 1
    elif 'enrollment' in subject or 'register' in subject:
        specific_requests['Account Enrollment Issue'] += 1
    elif 'import' in subject or 'upload' in subject:
        specific_requests['File Import Question'] += 1
    elif 'scan' in subject or 'barcode' in subject:
        specific_requests['Scanning/Barcode Question'] += 1
    elif 'order' in subject:
        specific_requests['Order-Related Question'] += 1
    elif 'catalog' in subject or 'link' in subject:
        specific_requests['Catalog Link Request'] += 1

for request, count in specific_requests.most_common(20):
    print(f"{request}: {count} tickets")

print("\n\n✅ Analysis complete!")
print(f"Total tickets analyzed: {len(data)}")
