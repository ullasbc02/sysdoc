from pathlib import Path

from src.executor import execute_command
from utils.safety import is_safe_command


DEFAULT_LOG_FILE = "sample_logs/app.log"


def run_command_tool(command: str) -> dict:
    safe, reason = is_safe_command(command)

    if not safe:
        return {
            "success": False,
            "observation": f"Command blocked by safety validator: {reason}",
            "command": command,
        }

    result = execute_command(command)

    if result["success"]:
        observation = result["stdout"] or "(no output)"
    else:
        observation = f"Command failed: {result['stderr']}"

    return {
        "success": result["success"],
        "observation": observation,
        "command": command,
        "returncode": result["returncode"],
    }


def search_logs_tool(pattern: str, path: str = DEFAULT_LOG_FILE) -> dict:
    log_path = Path(path)

    if not log_path.exists():
        return {
            "success": False,
            "observation": f"Log file not found: {path}",
            "command": None,
        }

    matches = []

    with log_path.open("r", encoding="utf-8") as file:
        for line in file:
            if pattern.lower() in line.lower():
                matches.append(line.strip())

    if not matches:
        observation = f"No log lines matched pattern: {pattern}"
    else:
        observation = "\n".join(matches)

    return {
        "success": True,
        "observation": observation,
        "command": f"search_logs(pattern={pattern}, path={path})",
    }


TOOLS = {
    "run_command": run_command_tool,
    "search_logs": search_logs_tool,
}


def execute_tool(
    action: str,
    command: str | None = None,
    pattern: str | None = None,
    path: str | None = None,
) -> dict:
    tool = TOOLS.get(action)

    if not tool:
        return {
            "success": False,
            "observation": f"Unsupported tool/action: {action}",
            "command": command,
        }

    if action == "run_command":
        if not command:
            return {
                "success": False,
                "observation": "run_command requires a command.",
                "command": command,
            }

        return tool(command)

    if action == "search_logs":
        if not pattern:
            return {
                "success": False,
                "observation": "search_logs requires a pattern.",
                "command": None,
            }

        return tool(pattern, path or DEFAULT_LOG_FILE)

    return {
        "success": False,
        "observation": f"No executor implemented for action: {action}",
        "command": command,
    }
