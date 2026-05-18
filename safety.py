import shlex


BLOCKED_COMMANDS = {
    "rm",
    "sudo",
    "shutdown",
    "reboot",
    "kill",
    "pkill",
    "chmod",
    "chown",
    "mv",
    "dd",
    "mkfs",
    "mount",
    "umount",
}


ALLOWED_COMMANDS = {
    "df",
    "du",
    "ps",
    "grep",
    "find",
    "ls",
    "cat",
    "head",
    "tail",
    "wc",
    "echo",
}


def is_safe_command(command: str) -> tuple[bool, str]:
    try:
        parts = shlex.split(command)
    except ValueError as e:
        return False, f"Invalid command syntax: {e}"

    if not parts:
        return False, "Empty command"

    base_command = parts[0]

    if base_command in BLOCKED_COMMANDS:
        return False, f"Blocked dangerous command: {base_command}"

    if base_command not in ALLOWED_COMMANDS:
        return False, f"Command not in allowlist: {base_command}"

    dangerous_tokens = ["&&", "||", ";", "`", "$(", ">", ">>", "<"]

    for token in dangerous_tokens:
        if token in command:
            return False, f"Blocked dangerous shell operator: {token}"

    return True, "Command is safe"