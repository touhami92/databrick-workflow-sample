from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "artifacts" / "curated" / "sales_summary.json"
    report_path = project_root / "artifacts" / "reports" / "daily_sales_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. Run transform_sales.py first."
        )

    with input_path.open("r", encoding="utf-8") as f:
        summary = json.load(f)

    lines = [
        "Daily Sales Report",
        f"Generated at: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Source records: {summary.get('source_record_count', 0)}",
        f"Grand total: {summary.get('grand_total', 0.0):.2f}",
        "",
        "Breakdown by country:",
    ]

    for item in summary.get("countries", []):
        lines.append(
            f"- {item['country']}: {item['orders']} orders / total {item['total_amount']:.2f}"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Built daily report -> {report_path}")


if __name__ == "__main__":
    main()
