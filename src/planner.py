def plan_commands(user_input: str) -> list[dict]:
    text = user_input.lower()

    if "disk" in text or "storage" in text or "space" in text:
        return [
            {
                "category": "disk",
                "command": "df -h",
                "reason": "Check overall filesystem disk usage."
            },
            {
                "category": "disk",
                "command": "du -sh *",
                "reason": "Find large directories in the current path."
            }
        ]

    if "process" in text or "cpu" in text or "memory" in text:
        return [
            {
                "category": "process",
                "command": "ps aux",
                "reason": "Inspect running processes and resource usage."
            }
        ]

    if "log" in text or "error" in text or "failure" in text:
        return [
            {
                "category": "logs",
                "command": "grep -i ERROR data/sample_logs/app.log",
                "reason": "Search application logs for error entries."
            }
        ]

    if "large file" in text or "big file" in text:
        return [
            {
                "category": "files",
                "command": "find . -type f -size +100M",
                "reason": "Find files larger than 100 MB."
            }
        ]

    return [
        {
            "category": "general",
            "command": "echo 'No matching troubleshooting plan found yet.'",
            "reason": "Fallback response for unsupported requests."
        }
    ]