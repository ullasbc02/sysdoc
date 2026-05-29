import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_planner import plan_with_langchain
from utils.plan_validator import validate_plan_schema
from config import load_config
from tools import run_command_tool
from llm.llm_analyzer import analyze_results_with_llm
from analyzer import analyze_results

def planner_node(state: dict) -> dict:
    user_query = state["user_query"]

    try:
        plans = plan_with_langchain(user_query)
        planner_error = None
    except Exception as e:
        plans = [
            {
                "category": "general",
                "command": "echo 'Planner failed.'",
                "reason": f"Planner error: {e}",
            }
        ]
        planner_error = str(e)

    valid_plans, validation_errors = validate_plan_schema(plans)

    return {
        **state,
        "plan": valid_plans,
        "observations": [],
        "final_report": None,
        "next_action": "execute_tools",
        "iteration": 0,
        "planner_error": planner_error,
        "validation_errors": validation_errors,
        "max_iterations": load_config()["agent"]["max_iterations"],
    }


def tool_executor_node(state: dict) -> dict:
    observations = state.get("observations", [])
    plan = state.get("plan", [])

    for item in plan:
        command = item["command"]

        result = run_command_tool(command)

        observations.append(
            {
                "category": item.get("category", "general"),
                "command": command,
                "reason": item.get("reason", ""),
                "success": result["success"],
                "observation": result["observation"],
            }
        )

    return {
        **state,
        "observations": observations,
        "iteration": state.get("iteration", 0) + 1,
        "next_action": "analyze",
    }

def analyzer_node(state: dict) -> dict:
    user_query = state["user_query"]
    observations = state.get("observations", [])

    # Convert graph observations into the format used by existing analyzers
    results = []

    for obs in observations:
        results.append(
            {
                "command": obs["command"],
                "success": obs["success"],
                "stdout": obs["observation"] if obs["success"] else "",
                "stderr": "" if obs["success"] else obs["observation"],
                "returncode": 0 if obs["success"] else 1,
                "category": obs.get("category", "general"),
                "reason": obs.get("reason", ""),
            }
        )

    try:
        report = analyze_results_with_llm(user_query, results)
    except Exception:
        report = analyze_results(user_query, results)

    return {
        **state,
        "final_report": report,
        "next_action": "finish",
    }