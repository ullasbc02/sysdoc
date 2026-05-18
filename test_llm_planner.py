from llm_planner import plan_commands_with_llm


requests = [
    "check disk usage",
    "find high CPU processes",
    "check app log errors",
    "find large files",
]

for request in requests:
    print()
    print("=" * 80)
    print(request)
    print("=" * 80)

    plans = plan_commands_with_llm(request)

    for plan in plans:
        print(plan)