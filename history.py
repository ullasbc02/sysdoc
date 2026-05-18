from datetime import datetime


HISTORY_FILE = "opspilot_history.log"


def save_history(user_input: str, results: list[dict]) -> None:
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write("=" * 80 + "\n")
        file.write(f"Timestamp: {datetime.now().isoformat()}\n")
        file.write(f"User input: {user_input}\n")

        for result in results:
            file.write("\n")
            file.write(f"Category: {result.get('category', 'unknown')}\n")
            file.write(f"Planner reason: {result.get('reason', 'N/A')}\n")
            file.write(f"Command: {result['command']}\n")
            file.write(f"Success: {result['success']}\n")
            file.write(f"Return code: {result['returncode']}\n")
            file.write("STDOUT:\n")
            file.write(result["stdout"] + "\n")
            file.write("STDERR:\n")
            file.write(result["stderr"] + "\n")

        file.write("\n")