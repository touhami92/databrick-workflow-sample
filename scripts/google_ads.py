from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / "artifacts" / "raw" / "google_ads.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # TODO: replace with actual Google Ads API client
    # from google.ads.googleads.client import GoogleAdsClient
    # client = GoogleAdsClient.load_from_env()

    ad_spend_records = [
        {"campaign_id": "CAMP-001", "channel": "search", "spend": 1200.50, "clicks": 340, "impressions": 8200},
        {"campaign_id": "CAMP-002", "channel": "display", "spend": 450.00, "clicks": 95, "impressions": 22000},
        {"campaign_id": "CAMP-003", "channel": "youtube", "spend": 870.75, "clicks": 210, "impressions": 15500},
    ]

    payload = {
        "source": "google_ads",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(ad_spend_records),
        "records": ad_spend_records,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Extracted {len(ad_spend_records)} Google Ads records -> {output_path}")


if __name__ == "__main__":
    main()
