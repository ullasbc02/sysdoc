from langchain_core.prompts import ChatPromptTemplate

from langchain_llm import get_langchain_llm


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux operations and developer productivity assistant.

Your job:
Explain safe Linux troubleshooting steps clearly.

Rules:
- Be concise.
- Prefer safe read-only commands.
- Do not recommend destructive commands.
- Explain why each command is useful.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{user_request}"),
    ]
)


def run_basic_langchain_chain(user_request: str) -> str:
    llm = get_langchain_llm()

    chain = prompt | llm

    response = chain.invoke(
        {
            "user_request": user_request,
        }
    )

    return response.content