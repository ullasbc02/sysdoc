from langgraph.graph import StateGraph, END

from graph_state import OpsPilotGraphState
from graph_nodes import (
    planner_node,
    tool_executor_node,
    analyzer_node,
)


def build_opspilot_graph():
    graph = StateGraph(OpsPilotGraphState)

    graph.add_node("planner", planner_node)
    graph.add_node("tool_executor", tool_executor_node)
    graph.add_node("analyzer", analyzer_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "tool_executor")
    graph.add_edge("tool_executor", "analyzer")
    graph.add_edge("analyzer", END)

    return graph.compile()


def run_langgraph_agent(user_query: str) -> dict:
    app = build_opspilot_graph()

    initial_state = {
        "user_query": user_query,
        "plan": [],
        "observations": [],
        "final_report": None,
        "next_action": None,
        "iteration": 0,
        "max_iterations": 5,
    }

    final_state = app.invoke(initial_state)

    return final_state