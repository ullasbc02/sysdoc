from datetime import datetime
from pathlib import Path


REPORTS_DIR = Path(__file__).parent.parent / "data" / "reports"


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
    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"report_{timestamp}.txt"

    report_path.write_text(report, encoding="utf-8")

    return str(report_path)