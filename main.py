from planner import plan_commands
from safety import is_safe_command
from executor import execute_command
from analyzer import analyze_results


def main():
    print("OpsPilot AI - Safe Linux Troubleshooting Agent")
    print("Type 'exit' to quit")
    print()

    while True:
        user_input = input("Ask OpsPilot > ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        if not user_input:
            continue

        commands = plan_commands(user_input)
        results = []

        print()
        print("Plan + Execution:")

        for command in commands:
            safe, reason = is_safe_command(command)

            if not safe:
                print(f"- [BLOCKED] {command} ({reason})")
                continue

            print(f"- [RUNNING] {command}")

            result = execute_command(command)
            results.append(result)

            if result["success"]:
                print(result["stdout"] or "(no output)")
            else:
                print(f"ERROR: {result['stderr']}")

            print()

        print(analyze_results(user_input, results))
        print()


if __name__ == "__main__":
    main()