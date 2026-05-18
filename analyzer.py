def analyze_results(user_input: str, results: list[dict]) -> str:
    lines = []

    lines.append("Diagnosis:")

    if not results:
        return "No command results to analyze."

    for result in results:
        command = result["command"]

        if not result["success"]:
            lines.append(f"- Command failed: {command}")
            lines.append(f"  Error: {result['stderr']}")
            continue

        output = result["stdout"]

        if command.startswith("df"):
            lines.append("- Checked filesystem disk usage.")
            lines.append("  Look for filesystems with high Use% such as 80% or above.")

        elif command.startswith("du"):
            lines.append("- Checked directory sizes in the current folder.")
            lines.append("  Larger directories may be good candidates for cleanup or archiving.")

        elif command.startswith("ps"):
            lines.append("- Checked running processes.")
            lines.append("  Look for processes with high CPU or memory usage.")

        elif command.startswith("grep"):
            if output:
                lines.append("- Found matching log errors.")
                lines.append("  Review repeated errors first because they may indicate root cause.")
            else:
                lines.append("- No matching log errors found.")

        elif command.startswith("find"):
            if output:
                lines.append("- Found large files.")
                lines.append("  Review these files before deleting or archiving.")
            else:
                lines.append("- No large files found for the current threshold.")

        else:
            lines.append(f"- Ran command: {command}")

    lines.append("")
    lines.append("Recommended next step:")
    lines.append("- Review the command output above and avoid destructive cleanup until confirmed.")

    return "\n".join(lines)