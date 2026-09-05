import json
import urllib.request
import ssl

ACCESS_TOKEN = 'pat-na1-1601c430-0ab6-4d25-9116-63102b697536'
BASE_URL = "https://api.hubapi.com"

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def hubspot_post(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    req_data = json.dumps(data).encode('utf-8')
    request = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, context=ssl_context, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error querying HubSpot: {e}")
        return {"results": []}

# Get all companies in "Onboarding" lifecycle stage
# Internal HubSpot value: "evangelist" = "Onboarding" in UI
search_data = {
    'filterGroups': [{
        'filters': [{
            'propertyName': 'lifecyclestage',
            'operator': 'EQ',
            'value': 'evangelist'
        }]
    }],
    'properties': ['name', 'domain', 'hs_date_entered_evangelist'],
    'limit': 100
}

print("Querying HubSpot for companies in 'evangelist' (Onboarding) stage...")
result = hubspot_post('/crm/v3/objects/companies/search', search_data)
companies = result.get('results', [])

print(f"Found {len(companies)} companies in Onboarding:")
for c in companies:
    props = c.get('properties', {})
    print(f"  - {props.get('name')} | {props.get('domain')} | Entered: {props.get('hs_date_entered_evangelist', 'N/A')[:10] if props.get('hs_date_entered_evangelist') else 'N/A'}")
