from typing import Literal
from pydantic import BaseModel, Field


class CommandPlan(BaseModel):
    category: Literal["disk", "process", "logs", "files", "general"] = Field(
        description="Troubleshooting category"
    )

    command: str = Field(
        description="Safe Linux diagnostic command"
    )

    reason: str = Field(
        description="Why this command is useful"
    )


class CommandPlanList(BaseModel):
    plans: list[CommandPlan] = Field(
        description="List of safe diagnostic command plans"
    )