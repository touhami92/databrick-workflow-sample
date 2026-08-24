from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "artifacts" / "raw" / "salesforce_leads.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # TODO: replace with actual Salesforce client
    # from simple_salesforce import Salesforce
    # sf = Salesforce(username=os.environ["SF_USER"], password=os.environ["SF_PASSWORD"],
    #                 security_token=os.environ["SF_TOKEN"])

    lead_records = [
        {"lead_id": "LEAD-501", "source": "google_ads", "campaign_id": "CAMP-001", "status": "new", "country": "FR"},
        {"lead_id": "LEAD-502", "source": "google_ads", "campaign_id": "CAMP-003", "status": "qualified", "country": "DE"},
        {"lead_id": "LEAD-503", "source": "organic", "campaign_id": None, "status": "new", "country": "ES"},
        {"lead_id": "LEAD-504", "source": "google_ads", "campaign_id": "CAMP-002", "status": "converted", "country": "FR"},
    ]

    payload = {
        "source": "salesforce_crm",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(lead_records),
        "records": lead_records,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Extracted {len(lead_records)} Salesforce leads -> {output_path}")


if __name__ == "__main__":
    main()
