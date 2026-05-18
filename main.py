import sys

from planner import plan_commands
from safety import is_safe_command
from executor import execute_command
from analyzer import analyze_results
from history import save_history
from reporter import build_report, save_report


DEMO_REQUESTS = [
    "check disk usage",
    "check log errors",
    "find large files",
    "check running processes",
]


def print_header(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def handle_request(user_input: str) -> None:
    plans = plan_commands(user_input)
    results = []

    print_header("PLAN")

    for index, plan in enumerate(plans, start=1):
        command = plan["command"]
        safe, reason = is_safe_command(command)
        status = "SAFE" if safe else "BLOCKED"

        print(f"{index}. [{status}] [{plan['category']}] {command}")
        print(f"   Planner reason: {plan['reason']}")
        print(f"   Safety reason: {reason}")

    print_header("EXECUTION")

    for plan in plans:
        command = plan["command"]
        safe, reason = is_safe_command(command)

        if not safe:
            print(f"[BLOCKED] {command}")
            print(f"Reason: {reason}")
            continue

        print(f"\n$ {command}")
        result = execute_command(command)
        result["category"] = plan["category"]
        result["reason"] = plan["reason"]
        results.append(result)

        if result["success"]:
            print(result["stdout"] or "(no output)")
        else:
            print(f"ERROR: {result['stderr']}")

    print_header("ANALYSIS")
    analysis = analyze_results(user_input, results)
    report = build_report(user_input, results, analysis)
    print(report)

    save_history(user_input, results)

    report_path = save_report(report)
    print()
    print(f"Report saved to: {report_path}")

    print_header("DONE")


def run_demo() -> None:
    print_header("OpsPilot AI Demo Mode")

    for request in DEMO_REQUESTS:
        print_header(f"DEMO REQUEST: {request}")
        handle_request(request)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
        return

    print_header("OpsPilot AI - Safe Linux Troubleshooting Agent")
    print("Type 'exit' to quit")

    while True:
        user_input = input("\nAsk OpsPilot > ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        if not user_input:
            continue

        handle_request(user_input)


if __name__ == "__main__":
    main()