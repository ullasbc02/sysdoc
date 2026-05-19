VALID_CATEGORIES = {
    "disk",
    "process",
    "logs",
    "files",
    "general",
}


def validate_plan_schema(plans: list[dict]) -> tuple[list[dict], list[str]]:
    valid_plans = []
    errors = []

    for index, plan in enumerate(plans, start=1):
        if not isinstance(plan, dict):
            errors.append(f"Plan {index} is not a dictionary.")
            continue

        category = plan.get("category")
        command = plan.get("command")
        reason = plan.get("reason")

        if category not in VALID_CATEGORIES:
            errors.append(f"Plan {index} has invalid category: {category}")
            category = "general"

        if not isinstance(command, str) or not command.strip():
            errors.append(f"Plan {index} has invalid command.")
            continue

        if not isinstance(reason, str) or not reason.strip():
            reason = "No reason provided."

        valid_plans.append(
            {
                "category": category,
                "command": command.strip(),
                "reason": reason.strip(),
            }
        )

    return valid_plans, errors