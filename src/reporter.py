from datetime import datetime
from pathlib import Path

from src.config import load_config


def get_reports_dir() -> Path:
    config = load_config()
    return Path(config["paths"]["reports_dir"])


def build_report(user_input: str, results: list[dict], analysis: str) -> str:
    lines = []

    lines.append("OpsPilot Summary Report")
    lines.append("-" * 80)
    lines.append(f"User request: {user_input}")
    lines.append("")

    lines.append("Commands executed:")

    if not results:
        lines.append("- No commands executed.")
    else:
        for result in results:
            status = "SUCCESS" if result["success"] else "FAILED"
            category = result.get("category", "unknown")
            command = result["command"]

            lines.append(f"- [{status}] [{category}] {command}")

    lines.append("")
    lines.append(analysis)

    return "\n".join(lines)


def save_report(report: str) -> str:
    reports_dir = get_reports_dir()
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"report_{timestamp}.txt"

    report_path.write_text(report, encoding="utf-8")

    return str(report_path)