#!/usr/bin/env python3
"""
Find positive sentiment about SuperCat features in Coaster calls
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))
from fathom_api import get_meetings, get_transcript

def find_coaster_standups():
    """Find all Coaster standup calls"""
    all_meetings = get_meetings(paginate=True)
    coaster_calls = []
    
    for meeting in all_meetings:
        title = meeting.get('meeting_title', '').lower()
        if any(term in title for term in ['ecat x coaster standup', 'coaster standup']):
            date_str = meeting.get('recording_start_time', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    if date_obj >= datetime(2024, 12, 16, tzinfo=date_obj.tzinfo):
                        coaster_calls.append(meeting)
                except:
                    pass
    
    coaster_calls.sort(key=lambda x: x.get('recording_start_time', ''))
    return coaster_calls

def find_positive_mentions(transcript):
    """Find positive sentiment mentions"""
    positive_keywords = [
        'love', 'great', 'perfect', 'awesome', 'excited', 'amazing',
        'really like', 'this is great', 'that\'s great', 'that\'s perfect',
        'wow', 'cool', 'nice', 'excellent', 'fantastic', 'wonderful',
        'better', 'easier', 'simpler', 'helpful', 'useful'
    ]
    
    positive_mentions = []
    
    for i, segment in enumerate(transcript):
        text = segment.get('text', '').lower()
        speaker = segment.get('speaker', {})
        speaker_name = speaker.get('display_name', 'Unknown') if isinstance(speaker, dict) else str(speaker)
        
        # Check if Coaster team member (not Brent/Kylor from SuperCat)
        is_coaster = 'brent' not in speaker_name.lower() and 'kylor' not in speaker_name.lower()
        
        if is_coaster and any(keyword in text for keyword in positive_keywords):
            # Get context
            context_segments = []
            start_idx = max(0, i - 2)
            end_idx = min(len(transcript), i + 3)
            
            for j in range(start_idx, end_idx):
                seg = transcript[j]
                seg_speaker = seg.get('speaker', {})
                seg_speaker_name = seg_speaker.get('display_name', 'Unknown') if isinstance(seg_speaker, dict) else str(seg_speaker)
                context_segments.append(f"{seg_speaker_name}: {seg.get('text', '')}")
            
            positive_mentions.append({
                'quote': segment.get('text', ''),
                'speaker': speaker_name,
                'context': '\n'.join(context_segments),
                'timestamp': segment.get('start_time', 0)
            })
    
    return positive_mentions

def format_timestamp(seconds):
    if isinstance(seconds, (int, float)):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    return "00:00"

def main():
    print("Finding positive SuperCat mentions from Coaster team...\n")
    
    coaster_calls = find_coaster_standups()
    all_positive = []
    
    for call in coaster_calls:
        recording_id = call.get('recording_id')
        date = call.get('recording_start_time', '')[:10]
        share_url = call.get('share_url', 'N/A')
        
        print(f"Analyzing: {date}")
        
        transcript = get_transcript(recording_id)
        if not transcript:
            continue
        
        positive = find_positive_mentions(transcript)
        
        for p in positive:
            p['date'] = date
            p['share_url'] = share_url
            p['recording_id'] = recording_id
        
        all_positive.extend(positive)
        print(f"  Found {len(positive)} positive mentions")
    
    # Output
    print(f"\n\nTotal positive mentions: {len(all_positive)}\n")
    print("="*80)
    
    for i, mention in enumerate(all_positive, 1):
        print(f"\n{i}. [{mention['date']}] {mention['speaker']}")
        print(f"   Quote: \"{mention['quote']}\"")
        print(f"   Link: {mention['share_url']} @ {format_timestamp(mention['timestamp'])}")
        print(f"   Context:")
        for line in mention['context'].split('\n'):
            print(f"      {line}")

if __name__ == "__main__":
    main()
