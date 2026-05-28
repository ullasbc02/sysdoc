from langchain_chain import run_basic_langchain_chain


requests = [
    "How do I check disk usage safely?",
    "How do I find high CPU processes?",
    "How do I inspect application logs?",
]

for request in requests:
    print()
    print("=" * 80)
    print(request)
    print("=" * 80)

    print(run_basic_langchain_chain(request))