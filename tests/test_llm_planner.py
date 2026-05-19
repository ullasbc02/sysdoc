import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.llm_planner import plan_commands_with_llm


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