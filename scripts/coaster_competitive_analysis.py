#!/usr/bin/env python3
"""
Coaster Standup Competitive Analysis Script
Queries all [Hold] eCat x Coaster Standup calls and extracts competitive insights
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Any

# Add integrations/fathom to path
sys.path.insert(0, os.path.join(os.getcwd(), 'integrations/fathom'))

try:
    from fathom_api import get_meetings, get_transcript, get_summary, get_recording
except ImportError:
    print("Could not import fathom_api. Please check path.")
    sys.exit(1)

def find_coaster_standups() -> List[Dict]:
    """Find all [Hold] eCat x Coaster Standup meetings"""
    print("Fetching all meetings from Fathom API...")
    all_meetings = get_meetings(paginate=True)
    
    print(f"Total meetings retrieved: {len(all_meetings)}")
    
    # Filter for Coaster Standup calls
    coaster_calls = []
    search_terms = [
        "[hold] ecat x coaster standup",
        "ecat x coaster standup",
        "coaster standup",
        "ecat x coaster"
    ]
    
    for meeting in all_meetings:
        title = meeting.get('meeting_title', '').lower()
        
        # Check if title matches any search term
        if any(term in title for term in search_terms):
            # Parse date
            date_str = meeting.get('recording_start_time', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    # Filter for calls from Dec 16, 2024 onwards
                    if date_obj >= datetime(2024, 12, 16, tzinfo=date_obj.tzinfo):
                        coaster_calls.append(meeting)
                except:
                    # If date parsing fails, include it anyway
                    coaster_calls.append(meeting)
    
    # Sort by date (oldest first)
    coaster_calls.sort(key=lambda x: x.get('recording_start_time', ''))
    
    print(f"\nFound {len(coaster_calls)} Coaster Standup calls since Dec 16, 2024")
    return coaster_calls

def analyze_transcript_for_competitive_insights(transcript: List[Dict], recording_id: int, meeting_title: str, date: str) -> Dict[str, List[str]]:
    """
    Analyze transcript for competitive mentions (SuperCat vs Amp)
    
    Returns:
        Dict with 'supercat_better' and 'amp_better' lists
    """
    insights = {
        'supercat_better': [],
        'amp_better': []
    }
    
    if not transcript:
        return insights
    
    # Keywords to look for
    supercat_keywords = ['supercat', 'super cat', 'ecat', 'e-cat']
    amp_keywords = ['amp', 'ampd', 'ampd.ai']
    comparison_keywords = [
        'better', 'worse', 'prefer', 'like', 'love', 'hate',
        'easier', 'harder', 'simpler', 'complicated',
        'faster', 'slower', 'efficient', 'inefficient',
        'works', 'doesn\'t work', 'broken', 'fixed',
        'improvement', 'issue', 'problem', 'solution',
        'feature', 'missing', 'has', 'doesn\'t have',
        'wish', 'would be nice', 'frustrating', 'great',
        'compared to', 'versus', 'vs', 'instead of',
        'upgrade', 'downgrade', 'switch', 'migration'
    ]
    
    # Process transcript segments
    for i, segment in enumerate(transcript):
        text = segment.get('text', '').lower()
        speaker = segment.get('speaker', 'Unknown')
        timestamp = segment.get('start_time', 0)
        
        # Check if this segment mentions both products or comparison keywords
        has_supercat = any(kw in text for kw in supercat_keywords)
        has_amp = any(kw in text for kw in amp_keywords)
        has_comparison = any(kw in text for kw in comparison_keywords)
        
        if (has_supercat or has_amp) and has_comparison:
            # Get context (previous and next segments for full context)
            context_segments = []
            start_idx = max(0, i - 2)
            end_idx = min(len(transcript), i + 3)
            
            for j in range(start_idx, end_idx):
                seg = transcript[j]
                context_segments.append(f"{seg.get('speaker', 'Unknown')}: {seg.get('text', '')}")
            
            context = "\n".join(context_segments)
            
            # Determine sentiment
            positive_indicators = ['better', 'prefer', 'like', 'love', 'easier', 'simpler', 'faster', 'efficient', 'works', 'great', 'improvement', 'solution', 'has', 'upgrade']
            negative_indicators = ['worse', 'hate', 'harder', 'complicated', 'slower', 'inefficient', 'doesn\'t work', 'broken', 'issue', 'problem', 'missing', 'doesn\'t have', 'frustrating', 'downgrade']
            
            # Analyze sentiment direction
            if has_supercat and has_amp:
                # Both mentioned - need to determine which is better
                # Look for patterns like "SuperCat is better than Amp" or "Amp is worse than SuperCat"
                supercat_positive = False
                amp_positive = False
                
                # Simple heuristic: check proximity of product names to positive/negative words
                words = text.split()
                for idx, word in enumerate(words):
                    if any(kw in word for kw in supercat_keywords):
                        # Check surrounding words
                        window = words[max(0, idx-5):min(len(words), idx+6)]
                        window_text = ' '.join(window)
                        if any(pos in window_text for pos in positive_indicators):
                            supercat_positive = True
                        if any(neg in window_text for neg in negative_indicators):
                            amp_positive = True  # If SuperCat is negative, Amp is relatively positive
                    
                    if any(kw in word for kw in amp_keywords):
                        window = words[max(0, idx-5):min(len(words), idx+6)]
                        window_text = ' '.join(window)
                        if any(pos in window_text for pos in positive_indicators):
                            amp_positive = True
                        if any(neg in window_text for neg in negative_indicators):
                            supercat_positive = True  # If Amp is negative, SuperCat is relatively positive
                
                if supercat_positive:
                    insights['supercat_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
                if amp_positive:
                    insights['amp_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
            
            elif has_supercat and has_comparison:
                # Only SuperCat mentioned with comparison words
                if any(pos in text for pos in positive_indicators):
                    insights['supercat_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
                elif any(neg in text for neg in negative_indicators):
                    insights['amp_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
            
            elif has_amp and has_comparison:
                # Only Amp mentioned with comparison words
                if any(pos in text for pos in positive_indicators):
                    insights['amp_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
                elif any(neg in text for neg in negative_indicators):
                    insights['supercat_better'].append({
                        'context': context,
                        'speaker': speaker,
                        'timestamp': timestamp,
                        'key_segment': text
                    })
    
    return insights

def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def main():
    print("=" * 80)
    print("COASTER STANDUP COMPETITIVE ANALYSIS")
    print("SuperCat vs Amp - Competitive Intelligence Report")
    print("=" * 80)
    print()
    
    # Find all Coaster standup calls
    coaster_calls = find_coaster_standups()
    
    if not coaster_calls:
        print("No Coaster Standup calls found.")
        return
    
    # Display found calls
    print("\nCalls to analyze:")
    for i, call in enumerate(coaster_calls, 1):
        date = call.get('recording_start_time', '')[:10]
        title = call.get('meeting_title', 'Untitled')
        rec_id = call.get('recording_id', 'N/A')
        print(f"{i}. {date} - {title} (ID: {rec_id})")
    
    print("\n" + "=" * 80)
    print("ANALYZING TRANSCRIPTS FOR COMPETITIVE INSIGHTS")
    print("=" * 80)
    
    all_supercat_better = []
    all_amp_better = []
    
    # Analyze each call
    for i, call in enumerate(coaster_calls, 1):
        recording_id = call.get('recording_id')
        title = call.get('meeting_title', 'Untitled')
        date = call.get('recording_start_time', '')[:10]
        share_url = call.get('share_url', 'N/A')
        
        print(f"\n{'='*80}")
        print(f"Call #{i}: {date} - {title}")
        print(f"Recording ID: {recording_id}")
        print(f"Share URL: {share_url}")
        print(f"{'='*80}")
        
        # Get transcript
        print(f"Fetching transcript for recording {recording_id}...")
        transcript = get_transcript(recording_id)
        
        if not transcript:
            print("  ⚠️  No transcript available for this call")
            continue
        
        print(f"  ✓ Transcript retrieved ({len(transcript)} segments)")
        
        # Analyze for competitive insights
        print("  Analyzing for competitive mentions...")
        insights = analyze_transcript_for_competitive_insights(transcript, recording_id, title, date)
        
        # Add metadata to insights
        for insight in insights['supercat_better']:
            insight['call_date'] = date
            insight['call_title'] = title
            insight['recording_id'] = recording_id
            insight['share_url'] = share_url
        
        for insight in insights['amp_better']:
            insight['call_date'] = date
            insight['call_title'] = title
            insight['recording_id'] = recording_id
            insight['share_url'] = share_url
        
        all_supercat_better.extend(insights['supercat_better'])
        all_amp_better.extend(insights['amp_better'])
        
        print(f"  ✓ Found {len(insights['supercat_better'])} mentions where SuperCat is better")
        print(f"  ✓ Found {len(insights['amp_better'])} mentions where Amp is better")
    
    # Generate final report
    print("\n\n" + "=" * 80)
    print("COMPETITIVE INTELLIGENCE REPORT")
    print("=" * 80)
    
    print(f"\n📊 SUMMARY")
    print(f"Total Calls Analyzed: {len(coaster_calls)}")
    print(f"Total SuperCat Advantages Mentioned: {len(all_supercat_better)}")
    print(f"Total Amp Advantages Mentioned: {len(all_amp_better)}")
    
    # SuperCat Better
    print("\n\n" + "=" * 80)
    print("🟢 WHERE SUPERCAT IS BETTER THAN AMP")
    print("=" * 80)
    
    if all_supercat_better:
        for i, insight in enumerate(all_supercat_better, 1):
            print(f"\n--- Insight #{i} ---")
            print(f"Call: {insight['call_date']} - {insight['call_title']}")
            print(f"Speaker: {insight['speaker']}")
            print(f"Timestamp: {format_timestamp(insight['timestamp'])}")
            print(f"Recording: {insight['share_url']}")
            print(f"\nKey Quote:")
            print(f'  "{insight["key_segment"]}"')
            print(f"\nFull Context:")
            print(insight['context'])
            print()
    else:
        print("\nNo specific mentions found where SuperCat was explicitly stated as better than Amp.")
    
    # Amp Better
    print("\n\n" + "=" * 80)
    print("🔴 WHERE AMP IS BETTER THAN SUPERCAT (Areas for Improvement)")
    print("=" * 80)
    
    if all_amp_better:
        for i, insight in enumerate(all_amp_better, 1):
            print(f"\n--- Insight #{i} ---")
            print(f"Call: {insight['call_date']} - {insight['call_title']}")
            print(f"Speaker: {insight['speaker']}")
            print(f"Timestamp: {format_timestamp(insight['timestamp'])}")
            print(f"Recording: {insight['share_url']}")
            print(f"\nKey Quote:")
            print(f'  "{insight["key_segment"]}"')
            print(f"\nFull Context:")
            print(insight['context'])
            print()
    else:
        print("\nNo specific mentions found where Amp was explicitly stated as better than SuperCat.")
    
    # Save to file
    output_file = f"documentation/Coaster_Competitive_Analysis_{datetime.now().strftime('%Y%m%d')}.md"
    
    print("\n\n" + "=" * 80)
    print(f"Saving report to: {output_file}")
    print("=" * 80)
    
    with open(output_file, 'w') as f:
        f.write("# Coaster Standup Competitive Analysis\n")
        f.write("## SuperCat vs Amp - Competitive Intelligence Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Analysis Period:** December 16, 2024 - Present\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Calls Analyzed:** {len(coaster_calls)}\n")
        f.write(f"- **SuperCat Advantages Mentioned:** {len(all_supercat_better)}\n")
        f.write(f"- **Amp Advantages Mentioned:** {len(all_amp_better)}\n\n")
        
        f.write("## Calls Analyzed\n\n")
        for i, call in enumerate(coaster_calls, 1):
            date = call.get('recording_start_time', '')[:10]
            title = call.get('meeting_title', 'Untitled')
            rec_id = call.get('recording_id', 'N/A')
            share_url = call.get('share_url', 'N/A')
            f.write(f"{i}. **{date}** - {title}\n")
            f.write(f"   - Recording ID: {rec_id}\n")
            f.write(f"   - [View Recording]({share_url})\n\n")
        
        f.write("\n---\n\n")
        f.write("## 🟢 Where SuperCat is Better Than Amp\n\n")
        
        if all_supercat_better:
            for i, insight in enumerate(all_supercat_better, 1):
                f.write(f"### Insight #{i}\n\n")
                f.write(f"**Call:** {insight['call_date']} - {insight['call_title']}\n\n")
                f.write(f"**Speaker:** {insight['speaker']}\n\n")
                f.write(f"**Timestamp:** {format_timestamp(insight['timestamp'])}\n\n")
                f.write(f"**Recording:** [{insight['share_url']}]({insight['share_url']})\n\n")
                f.write(f"**Key Quote:**\n\n")
                f.write(f"> {insight['key_segment']}\n\n")
                f.write(f"**Full Context:**\n\n")
                f.write(f"```\n{insight['context']}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("No specific mentions found where SuperCat was explicitly stated as better than Amp.\n\n")
        
        f.write("\n---\n\n")
        f.write("## 🔴 Where Amp is Better Than SuperCat (Areas for Improvement)\n\n")
        
        if all_amp_better:
            for i, insight in enumerate(all_amp_better, 1):
                f.write(f"### Insight #{i}\n\n")
                f.write(f"**Call:** {insight['call_date']} - {insight['call_title']}\n\n")
                f.write(f"**Speaker:** {insight['speaker']}\n\n")
                f.write(f"**Timestamp:** {format_timestamp(insight['timestamp'])}\n\n")
                f.write(f"**Recording:** [{insight['share_url']}]({insight['share_url']})\n\n")
                f.write(f"**Key Quote:**\n\n")
                f.write(f"> {insight['key_segment']}\n\n")
                f.write(f"**Full Context:**\n\n")
                f.write(f"```\n{insight['context']}\n```\n\n")
                f.write("---\n\n")
        else:
            f.write("No specific mentions found where Amp was explicitly stated as better than SuperCat.\n\n")
        
        f.write("\n---\n\n")
        f.write("## Recommendations\n\n")
        f.write("### For Sales Team\n\n")
        f.write("- Use the 'SuperCat Better' insights as competitive ammunition in sales conversations\n")
        f.write("- Address the 'Amp Better' points proactively by highlighting SuperCat's roadmap or workarounds\n\n")
        f.write("### For Product Team\n\n")
        f.write("- Review 'Amp Better' insights to identify feature gaps and prioritize enhancements\n")
        f.write("- Consider the 'SuperCat Better' insights as validation of current product direction\n\n")
    
    print(f"\n✅ Report saved successfully!")
    print(f"\nYou can find the detailed report at: {output_file}")

if __name__ == "__main__":
    main()
