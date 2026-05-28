from langchain_core.prompts import ChatPromptTemplate

from langchain_llm import get_langchain_llm
from langchain_schema import CommandPlanList


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux troubleshooting planner.

Your job:
Convert a user request into safe Linux diagnostic command plans.

Rules:
- Only suggest read-only diagnostic commands.
- Do not use sudo.
- Do not use destructive commands.
- Do not use shell operators like &&, ||, ;, >, >>, <, `, or $().
- Prefer commands that work inside Ubuntu Docker containers.

Allowed command families:
df, du, ps, grep, find, ls, cat, head, tail, wc, echo
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{user_request}"),
    ]
)


def plan_with_langchain(user_request: str) -> list[dict]:
    llm = get_langchain_llm()

    structured_llm = llm.with_structured_output(CommandPlanList)

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "user_request": user_request,
        }
    )

    return [
        {
            "category": plan.category,
            "command": plan.command,
            "reason": plan.reason,
        }
        for plan in result.plans
    ]