from pathlib import Path

from src.executor import execute_command
from utils.safety import is_safe_command
from config import load_config

def get_default_log_file() -> str:
    config = load_config()
    return config["paths"]["default_log_file"]

TOOL_RISK_LEVELS = {
    "search_logs": "safe",
    "inspect_processes": "safe",
    "inspect_disk": "safe",
    "run_command": "review",
}
def get_tool_risk_level(action: str) -> str:
    return TOOL_RISK_LEVELS.get(action, "review")

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


def search_logs_tool(pattern: str, path: str | None = None) -> dict:
    if path is None:
        path = get_default_log_file()

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

def inspect_processes_tool(sort_by: str | None = None, limit: int | None = None) -> dict:
    config = load_config()

    sort_by = sort_by or config["tools"]["default_process_sort"]
    limit = limit or config["tools"]["default_process_limit"]

    if sort_by == "memory":
        command = "ps aux --sort=-%mem"
    else:
        command = "ps aux --sort=-%cpu"

    result = execute_command(command)

    if not result["success"]:
        return {
            "success": False,
            "observation": f"Command failed: {result['stderr']}",
            "command": command,
        }

    lines = result["stdout"].splitlines()

    if not lines:
        observation = "No process information found."
    else:
        header = lines[0]
        processes = lines[1 : limit + 1]
        observation = "\n".join([header] + processes)

    return {
        "success": True,
        "observation": observation,
        "command": f"inspect_processes(sort_by={sort_by}, limit={limit})",
    }

def inspect_disk_tool(path: str | None = None) -> dict:
    config = load_config()
    path = path or config["tools"]["default_disk_path"]
    commands = [
        "df -h",
        f"du -sh {path}",
        f"du -sh {path}/*",
    ]

    observations = []

    for command in commands:
        result = execute_command(command)

        observations.append(f"$ {command}")

        if result["success"]:
            observations.append(result["stdout"] or "(no output)")
        else:
            observations.append(f"ERROR: {result['stderr']}")

        observations.append("")

    return {
        "success": True,
        "observation": "\n".join(observations),
        "command": f"inspect_disk(path={path})",
    }

TOOLS = {
    "run_command": run_command_tool,
    "search_logs": search_logs_tool,
    "inspect_processes": inspect_processes_tool,
    "inspect_disk": inspect_disk_tool,
}


def execute_tool(
    action: str,
    command: str | None = None,
    pattern: str | None = None,
    path: str | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
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

        return tool(pattern, path)
    
    if action == "inspect_processes":
        return tool(
            sort_by=sort_by or "cpu",
            limit=limit or 5,
        )

    if action == "inspect_disk":
        return tool(path or ".")

    return {
        "success": False,
        "observation": f"No executor implemented for action: {action}",
        "command": command,
    }
