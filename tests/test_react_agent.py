import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.react_agent import run_react_agent


def print_agent_trace(state):
    print()
    print("=" * 80)
    print("AGENT TRACE")
    print("=" * 80)

    print(f"User query: {state.user_query}")

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

    print()
    print("=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)
    print(state.final_answer)


if __name__ == "__main__":
    query = "check why the app is failing from logs"
    state = run_react_agent(query)
    print_agent_trace(state)