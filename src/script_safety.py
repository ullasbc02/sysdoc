DANGEROUS_PATTERNS = [
    "rm -rf /",
    "rm -rf *",
    "sudo ",
    "mkfs",
    "dd if=",
    ":(){",
    "chmod -R 777",
    "chown -R",
    "shutdown",
    "reboot",
]


def validate_script(script: str) -> tuple[bool, list[str]]:
    warnings = []

    lower_script = script.lower()

    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in lower_script:
            warnings.append(f"Dangerous pattern found: {pattern}")

    if "set -euo pipefail" not in script:
        warnings.append("Script missing: set -euo pipefail")

    if "rm " in lower_script and "dry" not in lower_script:
        warnings.append("Script uses rm without obvious dry-run behavior.")

    return len(warnings) == 0, warnings
