from langchain_core.tools import tool

from tools import (
    search_logs_tool,
    inspect_processes_tool,
    inspect_disk_tool,
    run_command_tool,
)


@tool
def search_logs(pattern: str, path: str = "sample_logs/app.log") -> str:
    """
    Search application logs for a case-insensitive pattern.
    Use this when investigating application failures or log errors.
    """
    result = search_logs_tool(pattern=pattern, path=path)
    return result["observation"]


@tool
def inspect_processes(sort_by: str = "cpu", limit: int = 5) -> str:
    """
    Inspect running Linux processes sorted by CPU or memory.
    Use this when troubleshooting high CPU, high memory, or process issues.
    """
    result = inspect_processes_tool(sort_by=sort_by, limit=limit)
    return result["observation"]


@tool
def inspect_disk(path: str = ".") -> str:
    """
    Inspect disk usage and directory sizes for a given path.
    Use this when troubleshooting disk usage or storage issues.
    """
    result = inspect_disk_tool(path=path)
    return result["observation"]


@tool
def run_safe_command(command: str) -> str:
    """
    Run a safe read-only Linux diagnostic command.
    Use only when no structured tool fits.
    """
    result = run_command_tool(command)
    return result["observation"]


LANGCHAIN_TOOLS = [
    search_logs,
    inspect_processes,
    inspect_disk,
    run_safe_command,
]