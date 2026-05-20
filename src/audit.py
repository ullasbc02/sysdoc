from datetime import datetime
from pathlib import Path
from config import load_config
from src.agent_state import AgentState


def get_audit_dir() -> Path:
    config = load_config()
    return Path(config["paths"]["audit_dir"])


def save_agent_audit(state: AgentState) -> str:
    audit_dir = get_audit_dir()
    audit_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_path = audit_dir / f"agent_audit_{timestamp}.log"

    lines = []

    lines.append("=" * 80)
    lines.append("OpsPilot Agent Audit Log")
    lines.append("=" * 80)
    lines.append(f"Timestamp: {datetime.now().isoformat()}")
    lines.append(f"User query: {state.user_query}")
    lines.append(f"Done: {state.done}")
    lines.append("")

    for step in state.steps:
        lines.append("-" * 80)
        lines.append(f"Iteration: {step.iteration}")
        lines.append(f"Thought: {step.thought}")
        lines.append(f"Action: {step.action}")

        if step.command:
            lines.append(f"Command/Tool: {step.command}")

        if step.observation:
            lines.append("Observation:")
            lines.append(step.observation)

        lines.append("")

    lines.append("=" * 80)
    lines.append("Final Answer")
    lines.append("=" * 80)
    lines.append(state.final_answer or "No final answer provided.")

    audit_path.write_text("\n".join(lines), encoding="utf-8")

    return str(audit_path)