import json
from datetime import datetime, timezone

def mock_lead_capture(name, email, platform, plan):
    lead = {
        "name": name,
        "email": email,
        "platform": platform,
        "plan": plan,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with open("leads.json", "a") as f:
        f.write(json.dumps(lead) + "\n")

    print("Lead captured successfully:", lead)
