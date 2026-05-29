from langgraph_workflow import run_langgraph_agent


if __name__ == "__main__":
    state = run_langgraph_agent("check disk usage")

    print()
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(state["final_report"])

    print()
    print("=" * 80)
    print("OBSERVATIONS")
    print("=" * 80)

    for obs in state["observations"]:
        print(obs)