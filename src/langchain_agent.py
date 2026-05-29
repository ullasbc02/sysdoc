from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage

from langchain_llm import get_langchain_llm
from langchain_tools import LANGCHAIN_TOOLS

SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux operations and developer productivity agent.

You help engineers troubleshoot Linux/system issues using safe tools.

Rules:
- Use tools when investigation is needed.
- Prefer structured tools over raw commands.
- Do not suggest destructive actions.
- Be concise and practical.
- If enough evidence is available, provide a final diagnosis and next steps.
"""

def create_langchain_agent_executor():
    llm = get_langchain_llm()

    return create_agent(
        model=llm,
        tools=LANGCHAIN_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )

class LangChainAgentSession:
    def __init__(self):
        self.executor = create_langchain_agent_executor()
        self.chat_history = []

    def run(self, user_input: str) -> str:
        result = self.executor.invoke(
            {
                "messages": self.chat_history + [HumanMessage(content=user_input)],
            }
        )

        output = self._extract_output(result)

        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=output))

        return output

    def _extract_output(self, result) -> str:
        if isinstance(result, dict):
            messages = result.get("messages", [])

            if messages:
                last_message = messages[-1]
                content = getattr(last_message, "content", None)

                if content:
                    return content

            output = result.get("output")

            if isinstance(output, str) and output.strip():
                return output

        return str(result)
from langchain.agents import create_agent

from langchain_llm import get_langchain_llm
from langchain_tools import LANGCHAIN_TOOLS


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux operations and developer productivity agent.

You help engineers troubleshoot Linux/system issues using safe tools.

Rules:
- Use tools when investigation is needed.
- Prefer structured tools over raw commands.
- Do not suggest destructive actions.
- Be concise and practical.
- If enough evidence is available, provide a final diagnosis and next steps.
"""


def run_langchain_agent(user_input: str) -> str:
    llm = get_langchain_llm()

    agent = create_agent(
        model=llm,
        tools=LANGCHAIN_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
        }
    )

    messages = result.get("messages", []) if isinstance(result, dict) else []

    if messages:
        last_message = messages[-1]
        content = getattr(last_message, "content", None)

        if content:
            return content

    return str(result)