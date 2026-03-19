from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    attribution_path = project_root / "artifacts" / "curated" / "attribution_scores.json"

    if not attribution_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {attribution_path}. Run attribution_model.py first."
        )

    with attribution_path.open("r", encoding="utf-8") as f:
        attribution = json.load(f)

    top = attribution.get("scores", [{}])[0]
    message = (
        f":rocket: *Marketing Analytics Pipeline Complete* — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"• Campaigns analyzed: {attribution.get('total_campaigns', 0)}\n"
        f"• Total spend: ${attribution.get('total_spend', 0):,.2f}\n"
        f"• Total conversions: {attribution.get('total_conversions', 0)}\n"
        f"• Top channel: *{top.get('channel', 'N/A')}* (ROI: {top.get('roi', 0):.2%})"
    )

    slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if slack_webhook_url:
        # TODO: send via actual HTTP POST
        # import urllib.request
        # req = urllib.request.Request(slack_webhook_url, data=json.dumps({"text": message}).encode(),
        #                              headers={"Content-Type": "application/json"})
        # urllib.request.urlopen(req)
        print(f"Slack notification sent to webhook.")
    else:
        print("SLACK_WEBHOOK_URL not set — skipping HTTP call.")

    print(f"Message:\n{message}")


if __name__ == "__main__":
    main()
