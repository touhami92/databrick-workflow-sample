from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = project_root / "artifacts" / "curated" / "attribution_scores.json"
    output_path = project_root / "artifacts" / "reports" / "marketing_dashboard.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run attribution_model.py first."
        )

    with input_path.open("r", encoding="utf-8") as f:
        attribution = json.load(f)

    # TODO: replace with actual Tableau Server Client calls
    # import tableauserverclient as TSC
    # server = TSC.Server(os.environ["TABLEAU_SERVER_URL"])
    # server.auth.sign_in(TSC.TableauAuth(os.environ["TABLEAU_USERNAME"], os.environ["TABLEAU_PASSWORD"]))
    # datasource = server.datasources.get_by_id(os.environ["TABLEAU_DATASOURCE_ID"])
    # server.datasources.refresh(datasource)

    dashboard_payload = {
        "refreshed_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_campaigns": attribution.get("total_campaigns"),
            "total_spend": attribution.get("total_spend"),
            "total_conversions": attribution.get("total_conversions"),
        },
        "top_channels": attribution.get("scores", [])[:3],
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(dashboard_payload, f, indent=2)

    print(f"Marketing dashboard refreshed -> {output_path}")


if __name__ == "__main__":
    main()
