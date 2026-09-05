#!/usr/bin/env python3
"""
Direct test of Fathom API with detailed debugging
"""

import urllib.request
import urllib.error
import json
import ssl

# Create SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

FATHOM_API_KEY = "igqF30s2AYp-UZskolVYMA.eTw97iS9AnIgsxdEsel4qQajIMcHGXVipSMeDNe7aCI"
FATHOM_BASE_URL = "https://fathom.video/external/v1"

def test_api():
    url = f"{FATHOM_BASE_URL}/meetings"
    
    headers = {
        "X-API-Key": FATHOM_API_KEY,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Testing URL: {url}")
    print(f"Headers: {headers}")
    
    request = urllib.request.Request(url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(request, context=ssl_context, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"\n✅ SUCCESS!")
            print(f"Response: {json.dumps(data, indent=2)[:500]}")
            return data
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.code}")
        print(f"Reason: {e.reason}")
        error_body = e.read().decode('utf-8') if e.fp else ""
        print(f"Error body: {error_body}")
        return None
    except Exception as e:
        print(f"\n❌ Exception: {type(e).__name__}: {e}")
        return None

if __name__ == "__main__":
    test_api()
