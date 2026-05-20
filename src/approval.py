from __future__ import annotations


def request_approval(action: str, command: str | None = None) -> bool:
    print()
    print("Human approval required")
    print("-" * 80)
    print(f"Action: {action}")

    if command:
        print(f"Command: {command}")

    response = input("Approve execution? (y/n): ").strip().lower()

    return response in {"y", "yes"}