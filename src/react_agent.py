from __future__ import annotations

import json
import re

from src.agent_state import AgentState
from src.tools import execute_tool
from llm.openrouter_client import call_llm
from src.approval import request_approval
from src.tools import get_tool_risk_level
from src.config import load_config

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
3. inspect_processes
4. inspect_disk
5. final_answer

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
    "path": "data/sample_logs/app.log"
}
JSON format for process inspection:
{
  "thought": "reasoning for the next step",
  "action": "inspect_processes",
  "sort_by": "cpu | memory",
  "limit": 5
}
JSON format for disk inspection:
{
  "thought": "reasoning for the next step",
  "action": "inspect_disk",
  "path": "."
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


def extract_json(text: str | None) -> dict:
    if text is None or not text.strip():
        raise ValueError("LLM returned empty response.")

    text = text.strip()

    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    decoder = json.JSONDecoder()

    for match in re.finditer(r"\{", text):
        try:
            parsed, _ = decoder.raw_decode(text[match.start():])
            return parsed
        except json.JSONDecodeError:
            continue

    raise ValueError("No JSON object found in LLM response.")


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


def run_react_agent(user_query: str, approval_required: bool = False) -> AgentState:
    state = AgentState(user_query=user_query)

    config = load_config()
    state.max_iterations = config["agent"]["max_iterations"]

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

        if action not in {"run_command", "search_logs", "inspect_processes", "inspect_disk"}:
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

        sort_by = decision.get("sort_by", "cpu")
        limit = decision.get("limit", 5)

        # Create a stable signature for the requested tool call so we can
        # detect repeated actions across iterations (including different
        # tool types like `search_logs`).
        if action == "run_command":
            tool_signature = command
        elif action == "search_logs":
            tool_signature = f"search_logs:{pattern}:{path}"
        elif action == "inspect_processes":
            tool_signature = f"inspect_processes:{sort_by}:{limit}"
        elif action == "inspect_disk":
            tool_signature = f"inspect_disk:{path or '.'}"
        else:
            tool_signature = action

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

        # Request human approval if required.
        risk_level = get_tool_risk_level(action)

        if risk_level == "blocked":
            observation = f"Tool action is blocked by policy: {action}"

            state.add_step(
                thought=thought,
                action=action,
                command=tool_signature,
                observation=observation,
            )

            continue

        if approval_required and risk_level != "safe":
            approved = request_approval(action, tool_signature)

            if not approved:
                observation = f"Human rejected action: {tool_signature}"

                state.add_step(
                    thought=thought,
                    action=action,
                    command=tool_signature,
                    observation=observation,
                )

                state.final_answer = "Investigation stopped because human approval was denied."
                state.done = True
                break

        # Execute the requested tool with explicit keyword arguments.
        tool_result = execute_tool(
            action=action,
            command=command,
            pattern=pattern,
            path=path,
            sort_by=sort_by,
            limit=limit,
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