from typing import TypedDict, Optional


class OpsPilotGraphState(TypedDict):
    user_query: str
    plan: list[dict]
    observations: list[dict]
    final_report: Optional[str]
    next_action: Optional[str]
    iteration: int
    max_iterations: int