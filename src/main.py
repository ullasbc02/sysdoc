import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` package imports work
# when running `python3 src/main.py` directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.planner import plan_commands as rule_based_plan_commands
from llm.llm_planner import plan_commands_with_llm
from utils.safety import is_safe_command
from src.executor import execute_command
from src.analyzer import analyze_results
from llm.llm_analyzer import analyze_results_with_llm
from src.history import save_history
from src.reporter import build_report, save_report
from utils.plan_validator import validate_plan_schema
from src.react_agent import run_react_agent
from src.react_reporter import build_react_report, save_react_report
from src.audit import save_agent_audit
from memory import save_investigation, list_recent_investigations

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


def use_llm_mode() -> bool:
    if "--rule" in sys.argv:
        return False

    if "--llm" in sys.argv:
        return True

    return True


def handle_react_request(user_input: str) -> None:
    print_header("REACT AGENT MODE")
    approval_required = "--approval" in sys.argv

    state = run_react_agent(user_input, approval_required=approval_required)

    print_header("AGENT TRACE")

    for step in state.steps:
        print()
        print(f"Iteration {step.iteration}")
        print("-" * 80)
        print(f"Thought: {step.thought}")
        print(f"Action: {step.action}")

        if step.command:
            print(f"Command: {step.command}")

        if step.observation:
            print("Observation:")
            print(step.observation)

    print_header("FINAL ANSWER")
    print(state.final_answer)

    report = build_react_report(state)
    report_path = save_react_report(report)
    audit_path = save_agent_audit(state)
    memory_id = save_investigation(state)
    print()
    print(f"ReAct report saved to: {report_path}")
    print(f"Audit log saved to: {audit_path}")
    print(f"Investigation saved to memory with id: {memory_id}")

def get_plans(user_input: str, llm_enabled: bool) -> tuple[list[dict], str, list[str]]:
    if llm_enabled:
        try:
            plans = plan_commands_with_llm(user_input)
            planner_mode = "LLM"
        except Exception as e:
            print(f"LLM planner failed. Falling back to rule-based planner. Error: {e}")
            plans = rule_based_plan_commands(user_input)
            planner_mode = "RULE_BASED_FALLBACK"
    else:
        plans = rule_based_plan_commands(user_input)
        planner_mode = "RULE_BASED"

    plans, validation_errors = validate_plan_schema(plans)

    return plans, planner_mode, validation_errors


def get_analysis(user_input: str, results: list[dict], llm_enabled: bool) -> tuple[str, str]:
    if llm_enabled:
        try:
            analysis = analyze_results_with_llm(user_input, results)
            return analysis, "LLM"
        except Exception as e:
            print(f"LLM analyzer failed. Falling back to rule-based analyzer. Error: {e}")

    return analyze_results(user_input, results), "RULE_BASED"


def handle_request(user_input: str, llm_enabled: bool) -> None:
    plans, planner_mode, validation_errors = get_plans(user_input, llm_enabled)
    results = []

    print_header("PLAN")
    print(f"Planner mode: {planner_mode}")

    if validation_errors:
        print()
        print("Plan validation warnings:")
        for error in validation_errors:
            print(f"- {error}")

    for index, plan in enumerate(plans, start=1):
        command = plan["command"]
        safe, reason = is_safe_command(command)
        status = "SAFE" if safe else "BLOCKED"

        print()
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
    analysis, analyzer_mode = get_analysis(user_input, results, llm_enabled)
    print(f"Analyzer mode: {analyzer_mode}")
    print()

    report = build_report(user_input, results, analysis)
    print(report)

    save_history(user_input, results)

    report_path = save_report(report)
    print()
    print(f"Report saved to: {report_path}")

    print_header("DONE")


def run_demo(llm_enabled: bool) -> None:
    print_header("OpsPilot AI Demo Mode")

    for request in DEMO_REQUESTS:
        print_header(f"DEMO REQUEST: {request}")
        handle_request(request, llm_enabled)


def main():
    llm_enabled = use_llm_mode()

    if "--demo" in sys.argv:
        run_demo(llm_enabled)
        return

    print_header("OpsPilot AI - Safe Linux Troubleshooting Agent")

    mode = "LLM" if llm_enabled else "RULE_BASED"
    print(f"Mode: {mode}")
    print("Type 'exit' to quit")

    while True:
        user_input = input("\nAsk OpsPilot > ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ["history", "recent"]:
            recent = list_recent_investigations()

            print_header("RECENT INVESTIGATIONS")

            if not recent:
                print("No previous investigations found.")
            else:
                for item in recent:
                    print(f"ID: {item['id']}")
                    print(f"Time: {item['timestamp']}")
                    print(f"Query: {item['user_query']}")
                    print(f"Steps: {item['steps_count']}")
                    print(f"Final: {item['final_answer']}")
                    print("-" * 80)

            continue

        if "--react" in sys.argv:
            handle_react_request(user_input)
        else:
            handle_request(user_input, llm_enabled)


if __name__ == "__main__":
    main()