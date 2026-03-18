from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "artifacts" / "raw" / "sales.json"
    output_path = project_root / "artifacts" / "curated" / "sales_summary.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run extract_sales.py first."
        )

    with input_path.open("r", encoding="utf-8") as f:
        raw_payload = json.load(f)

    totals_by_country: dict[str, float] = {}
    orders_by_country: dict[str, int] = {}

    for event in raw_payload.get("events", []):
        country = event["country"]
        amount = float(event["amount"])
        totals_by_country[country] = totals_by_country.get(country, 0.0) + amount
        orders_by_country[country] = orders_by_country.get(country, 0) + 1

    summary = {
        "source_record_count": raw_payload.get("record_count", 0),
        "countries": [
            {
                "country": country,
                "orders": orders_by_country[country],
                "total_amount": round(totals_by_country[country], 2),
            }
            for country in sorted(totals_by_country.keys())
        ],
        "grand_total": round(sum(totals_by_country.values()), 2),
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Transformed raw sales -> {output_path}")


if __name__ == "__main__":
    main()
