from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / "artifacts" / "raw" / "sales.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sales_events = [
        {"order_id": "ORD-1001", "country": "FR", "amount": 120.5},
        {"order_id": "ORD-1002", "country": "FR", "amount": 80.0},
        {"order_id": "ORD-1003", "country": "DE", "amount": 150.0},
        {"order_id": "ORD-1004", "country": "ES", "amount": 65.25},
        {"order_id": "ORD-1005", "country": "DE", "amount": 99.9},
    ]

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(sales_events),
        "events": sales_events,
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Extracted {len(sales_events)} sales events -> {output_path}")


if __name__ == "__main__":
    main()
