from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    ads_path = project_root / "artifacts" / "raw" / "google_ads.json"
    leads_path = project_root / "artifacts" / "raw" / "salesforce_leads.json"
    output_path = project_root / "artifacts" / "curated" / "merged_marketing.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for path in (ads_path, leads_path):
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}. Run ingestion tasks first.")

    with ads_path.open("r", encoding="utf-8") as f:
        ads_data = json.load(f)

    with leads_path.open("r", encoding="utf-8") as f:
        leads_data = json.load(f)

    # Validate and cleanse ad records
    clean_ads = [
        r for r in ads_data.get("records", [])
        if r.get("campaign_id") and r.get("spend", 0) >= 0
    ]

    # Validate and cleanse lead records
    clean_leads = [
        r for r in leads_data.get("records", [])
        if r.get("lead_id") and r.get("status") in ("new", "qualified", "converted")
    ]

    merged = {
        "ads_record_count": len(clean_ads),
        "leads_record_count": len(clean_leads),
        "ads": clean_ads,
        "leads": clean_leads,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    print(
        f"Cleansed and merged {len(clean_ads)} ad records + {len(clean_leads)} lead records -> {output_path}"
    )


if __name__ == "__main__":
    main()
