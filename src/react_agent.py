import json
import re

from src.agent_state import AgentState
from src.tools import execute_tool
from llm.openrouter_client import call_llm


SYSTEM_PROMPT = """
You are OpsPilot AI, a Linux troubleshooting agent.

You operate using a ReAct loop:
Reason -> Act -> Observe -> Repeat.

Your job:
Investigate the user's Linux/system troubleshooting request step by step.

You can use only one action per iteration.

Allowed actions:
1. run_command
2. search_logs
3. final_answer

Rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside JSON.
- Use only safe read-only diagnostic Linux commands.
- Do not use sudo.
- Do not use destructive commands.
- Do not use shell operators like &&, ||, ;, >, >>, <, `, or $().
- Prefer commands that work inside Ubuntu Docker containers.
- If you have enough evidence, use final_answer.
- Do not repeat the same command unless necessary.

Allowed command families:
df, du, ps, grep, find, ls, cat, head, tail, wc, echo

JSON format for command:
{
  "thought": "reasoning for the next step",
  "action": "run_command",
  "command": "linux command here"
}

JSON format for final answer:
{
  "thought": "why investigation is complete",
  "action": "final_answer",
  "final_answer": "clear diagnosis and recommended next steps"
}
JSON format for log search:
{
  "thought": "reasoning for the next step",
  "action": "search_logs",
  "pattern": "ERROR",
  "path": "sample_logs/app.log"
}
"""

def build_max_iteration_summary(state: AgentState) -> str:
    lines = []

    lines.append("Reached maximum investigation steps.")
    lines.append("")
    lines.append("Observations collected:")

    if not state.steps:
        lines.append("- No observations collected.")
        return "\n".join(lines)

    for step in state.steps:
        lines.append(f"- Iteration {step.iteration}:")
        lines.append(f"  Thought: {step.thought}")

        if step.command:
            lines.append(f"  Command: {step.command}")

        if step.observation:
            short_observation = step.observation[:500]
            lines.append(f"  Observation: {short_observation}")

    lines.append("")
    lines.append("Recommended next step:")
    lines.append("- Review the observations above and continue with a more specific troubleshooting question.")

    return "\n".join(lines)


def extract_json(text: str) -> dict:
    text = text.strip()

    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in LLM response.")

    return json.loads(match.group(0))


def decide_next_step(state: AgentState) -> dict:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""
                User request:
                {state.user_query}

                Previous investigation history:
                {state.format_history()}

                Decide the next best step.
            """,
        },
    ]

    response = call_llm(messages, temperature=0.0)
    return extract_json(response)


def run_react_agent(user_query: str) -> AgentState:
    state = AgentState(user_query=user_query)

    while not state.done and len(state.steps) < state.max_iterations:
        try:
            decision = decide_next_step(state)
        except Exception as e:
            state.final_answer = f"Agent failed to produce a valid decision: {e}"
            state.done = True
            break

        thought = decision.get("thought", "")
        action = decision.get("action", "")

        if action == "final_answer":
            state.final_answer = decision.get("final_answer", "No final answer provided.")
            state.done = True
            state.add_step(
                thought=thought,
                action=action,
                command=None,
                observation=state.final_answer,
            )
            break

        if action not in {"run_command", "search_logs"}:
            state.add_step(
                thought=thought,
                action=action,
                command=None,
                observation=f"Unsupported action: {action}",
            )
            continue

        command = decision.get("command", "").strip() if decision.get("command") else None
        pattern = decision.get("pattern")
        path = decision.get("path")

        # Create a stable signature for the requested tool call so we can
        # detect repeated actions across iterations (including different
        # tool types like `search_logs`).
        tool_signature = (
            command if action == "run_command" else f"search_logs:{pattern}:{path}"
        )

        previous_actions = {
            step.command
            for step in state.steps
            if step.command
        }

        if tool_signature in previous_actions:
            observation = (
                f"Tool call was already executed before: {tool_signature}. "
                "Choose a different diagnostic step or provide final_answer."
            )

            state.add_step(
                thought=thought,
                action=action,
                command=tool_signature,
                observation=observation,
            )

            continue

        # Execute the requested tool with explicit keyword arguments.
        tool_result = execute_tool(
            action=action,
            command=command,
            pattern=pattern,
            path=path,
        )

        observation = tool_result.get("observation")
        recorded_command = tool_result.get("command") or tool_signature

        state.add_step(
            thought=thought,
            action=action,
            command=recorded_command,
            observation=observation,
        )

    if not state.done:
        state.final_answer = build_max_iteration_summary(state)
        state.done = True

    return state