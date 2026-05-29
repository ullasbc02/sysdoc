from datetime import datetime
from pathlib import Path

from config import load_config


def get_reports_dir() -> Path:
    config = load_config()
    return Path(config["paths"]["reports_dir"])


def build_langchain_agent_report(user_input: str, final_answer: str) -> str:
    lines = []

    lines.append("OpsPilot LangChain Agent Report")
    lines.append("-" * 80)
    lines.append(f"User request: {user_input}")
    lines.append("")
    lines.append("Final answer:")
    lines.append(final_answer)

    return "\n".join(lines)


def save_langchain_agent_report(report: str) -> str:
    reports_dir = get_reports_dir()
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"langchain_agent_report_{timestamp}.txt"

    report_path.write_text(report, encoding="utf-8")

    return str(report_path)