from langchain_planner import plan_with_langchain


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

    plans = plan_with_langchain(request)

    for plan in plans:
        print(plan)