from langchain_agent import run_langchain_agent


queries = [
    "check disk usage",
    "check why the app is failing from logs",
    "find high CPU processes",
]

for query in queries:
    print()
    print("=" * 80)
    print(query)
    print("=" * 80)

    result = run_langchain_agent(query)
    print(result)