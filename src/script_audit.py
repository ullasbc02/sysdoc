from datetime import datetime
from pathlib import Path


SCRIPT_AUDIT_DIR = Path("script_audits")


def save_script_audit(
    user_request: str,
    script_path: str,
    script: str,
    safe: bool,
    warnings: list[str],
    explanation: str,
) -> str:
    SCRIPT_AUDIT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_path = SCRIPT_AUDIT_DIR / f"script_audit_{timestamp}.log"

    lines = []

    lines.append("=" * 80)
    lines.append("OpsPilot Script Audit")
    lines.append("=" * 80)
    lines.append(f"Timestamp: {datetime.now().isoformat()}")
    lines.append(f"User request: {user_request}")
    lines.append(f"Script path: {script_path}")
    lines.append(f"Safety passed: {safe}")
    lines.append("")

    lines.append("Warnings:")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("Generated Script:")
    lines.append("-" * 80)
    lines.append(script)

    lines.append("")
    lines.append("Explanation:")
    lines.append("-" * 80)
    lines.append(explanation)

    audit_path.write_text("\n".join(lines), encoding="utf-8")

    return str(audit_path)