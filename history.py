from datetime import datetime


HISTORY_FILE = "opspilot_history.log"


def save_history(user_input: str, results: list[dict]) -> None:
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write("=" * 80 + "\n")
        file.write(f"Timestamp: {datetime.now().isoformat()}\n")
        file.write(f"User input: {user_input}\n")

        for result in results:
            file.write(f"\nCommand: {result['command']}\n")
            file.write(f"Success: {result['success']}\n")
            file.write(f"Return code: {result['returncode']}\n")
            file.write("STDOUT:\n")
            file.write(result["stdout"] + "\n")
            file.write("STDERR:\n")
            file.write(result["stderr"] + "\n")

        file.write("\n")