from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "artifacts" / "curated" / "merged_marketing.json"
    output_path = project_root / "artifacts" / "curated" / "attribution_scores.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run cleanse.py first."
        )

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    ads = {r["campaign_id"]: r for r in data.get("ads", [])}
    leads = data.get("leads", [])

    # Last-touch attribution: assign full credit to the last campaign seen per lead
    conversions_by_campaign: dict[str, int] = {}
    for lead in leads:
        campaign_id = lead.get("campaign_id")
        if campaign_id and lead.get("status") == "converted":
            conversions_by_campaign[campaign_id] = conversions_by_campaign.get(campaign_id, 0) + 1

    attribution_scores = []
    for campaign_id, ad in ads.items():
        spend = ad.get("spend", 0.0)
        conversions = conversions_by_campaign.get(campaign_id, 0)
        roi = round((conversions * 500 - spend) / spend, 4) if spend > 0 else 0.0
        attribution_scores.append({
            "campaign_id": campaign_id,
            "channel": ad.get("channel"),
            "spend": spend,
            "conversions": conversions,
            "roi": roi,
        })

    result = {
        "total_campaigns": len(attribution_scores),
        "total_spend": round(sum(a["spend"] for a in attribution_scores), 2),
        "total_conversions": sum(a["conversions"] for a in attribution_scores),
        "scores": sorted(attribution_scores, key=lambda x: x["roi"], reverse=True),
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Computed attribution for {len(attribution_scores)} campaigns -> {output_path}")


if __name__ == "__main__":
    main()
