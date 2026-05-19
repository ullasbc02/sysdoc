from dataclasses import dataclass, field


@dataclass
class AgentStep:
    iteration: int
    thought: str
    action: str
    command: str | None
    observation: str | None = None


@dataclass
class AgentState:
    user_query: str
    steps: list[AgentStep] = field(default_factory=list)
    final_answer: str | None = None
    done: bool = False
    max_iterations: int = 5

    def add_step(
        self,
        thought: str,
        action: str,
        command: str | None,
        observation: str | None = None,
    ) -> None:
        step = AgentStep(
            iteration=len(self.steps) + 1,
            thought=thought,
            action=action,
            command=command,
            observation=observation,
        )

        self.steps.append(step)

    def format_history(self) -> str:
        if not self.steps:
            return "No previous steps."

        lines = []

        for step in self.steps:
            lines.append(f"Iteration {step.iteration}")
            lines.append(f"Thought: {step.thought}")
            lines.append(f"Action: {step.action}")

            if step.command:
                lines.append(f"Command: {step.command}")

            if step.observation:
                lines.append(f"Observation:\n{step.observation}")

            lines.append("")

        return "\n".join(lines)