from collections import Counter


def analyze_log_errors(output: str) -> list[str]:
    lines = output.splitlines()

    if not lines:
        return ["- No matching log errors found."]

    messages = []

    for line in lines:
        if "ERROR" in line:
            # Remove timestamp roughly: first two fields
            parts = line.split(" ", 2)
            if len(parts) == 3:
                messages.append(parts[2])
            else:
                messages.append(line)

    counter = Counter(messages)

    result = []
    result.append("- Found log errors.")

    most_common = counter.most_common(3)

    result.append("- Most frequent errors:")

    for message, count in most_common:
        result.append(f"  - {count}x {message}")

    return result


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
            lines.extend(analyze_log_errors(output))

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
    lines.append("- Investigate the most repeated error first, then check related service configuration.")

    return "\n".join(lines)