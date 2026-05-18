def plan_commands(user_input: str) -> list[str]:
    text = user_input.lower()

    if "disk" in text or "storage" in text or "space" in text:
        return [
            "df -h",
            "du -sh *"
        ]

    if "process" in text or "cpu" in text or "memory" in text:
        return [
            "ps aux"
        ]

    if "log" in text or "error" in text or "failure" in text:
        return [
            "grep -i ERROR sample_logs/app.log"
        ]

    if "large file" in text or "big file" in text:
        return [
            "find . -type f -size +100M"
        ]

    return [
        "echo 'No matching troubleshooting plan found yet.'"
    ]