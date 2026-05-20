from datetime import datetime
from pathlib import Path

from config import load_config
from src.agent_state import AgentState


def get_reports_dir() -> Path:
    config = load_config()
    return Path(config["paths"]["reports_dir"])


def build_react_report(state: AgentState) -> str:
    lines = []

    lines.append("OpsPilot ReAct Agent Report")
    lines.append("-" * 80)
    lines.append(f"User request: {state.user_query}")
    lines.append("")

    lines.append("Agent trace:")

    for step in state.steps:
        lines.append("")
        lines.append(f"Iteration {step.iteration}")
        lines.append("-" * 80)
        lines.append(f"Thought: {step.thought}")
        lines.append(f"Action: {step.action}")

        if step.command:
            lines.append(f"Command: {step.command}")

        if step.observation:
            lines.append("Observation:")
            lines.append(step.observation)

    lines.append("")
    lines.append("Final answer:")
    lines.append(state.final_answer or "No final answer provided.")

    return "\n".join(lines)


def save_react_report(report: str) -> str:
    reports_dir = get_reports_dir()
    reports_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"react_report_{timestamp}.txt"

    report_path.write_text(report, encoding="utf-8")

    return str(report_path)
