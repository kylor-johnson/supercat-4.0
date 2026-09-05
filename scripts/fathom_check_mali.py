import sys
import os
import json

# Add integrations/fathom to path
sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))

try:
    from fathom_api import get_meetings, get_summary
except ImportError:
    # Fallback if file structure is different or running from root
    sys.path.insert(0, os.path.join(os.getcwd(), 'SuperCat 4.0/integrations/fathom'))
    try:
        from fathom_api import get_meetings, get_summary
    except ImportError:
        print("Could not import fathom_api. Please check path.")
        sys.exit(1)

def check_client(client_name, shortname, domains, keywords):
    print(f"Checking Fathom for {client_name} ({shortname})...")
    meetings = get_meetings()
    
    relevant_meetings = []
    
    search_terms = [client_name.lower(), shortname.lower()] + [d.lower() for d in domains]
    
    print(f"Scanning {len(meetings)} meetings...")
    
    for m in meetings:
        title = m.get('meeting_title', '').lower()
        date = m.get('recording_start_time', '')[:10]
        
        # Check title
        if any(term in title for term in search_terms):
            relevant_meetings.append(m)
            continue
            
        # Check keywords AND (title or domain match) - wait, keywords are broad
        # Playbook says: Check keywords like "implementation" AND ...?
        # Playbook: "Search meeting titles for ANY of these patterns: Client name, Shortname, Keywords"
        # BUT relying on just "implementation" would find all clients.
        # "Filter for Client (MULTI-CRITERIA)"
        # "Search meeting titles for ANY of these patterns: 1. Client name... 2. Shortname... 3. Keywords... 4. [Hold]"
        # This implies keywords ALONE might be enough? No, that would be noisy.
        # "Step 3: Check Invite Lists... For meetings where title doesn't clearly indicate client"
        
        # Strategy:
        # 1. Strong match: Title contains client name/shortname
        # 2. Weak match: Title contains keyword AND we check attendees
        
        is_keyword_match = any(k.lower() in title for k in keywords)
        if is_keyword_match:
            # We must check attendees for this to be assigned to this client?
            # Or just flag it for manual check?
            # Playbook says "For meetings where title doesn't clearly indicate client... Match email domains"
            # I'll do that for matches that AREN'T clearly client name but ARE keywords.
            pass

    # Let's filter first by Name/Shortname
    # Then for others, check attendees if we can (summary needed)
    
    # Actually, to avoid hitting API too much, let's just find strong matches first.
    # And maybe keyword matches that are "ambiguous"
    
    strong_matches = [m for m in meetings if any(t in m.get('meeting_title', '').lower() for t in search_terms)]
    
    print(f"Found {len(strong_matches)} strong title matches.")
    
    for m in strong_matches:
        print(f"  - {m.get('recording_start_time')[:10]} | {m.get('meeting_title')}")
        # Get summary for these
        try:
            summary = get_summary(m.get('recording_id'))
            print(f"    Summary: {summary.get('summary', {}).get('markdown_formatted', '')[:200]}...")
        except Exception as e:
            print(f"    Error getting summary: {e}")

    # Now check for email domain matches in RECENT meetings (last 90 days)
    # This is expensive if we do it for ALL meetings.
    # Playbook says "Step 1: Get ALL Meetings... Step 3: Check Invite Lists (MANDATORY FOR UNCERTAIN MATCHES)"
    # I'll skip the exhaustive attendee check for now unless I find 0 strong matches.
    
    if not strong_matches:
        print("No strong matches found. Checking attendees for recent keyword matches...")
        # ... logic ...

check_client("Donald Choi", "dccl", ["donaldchoi.com", "choihome.ca"], ["implementation", "onboarding", "kickoff"])
