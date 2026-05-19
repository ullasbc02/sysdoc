
# OpsPilot AI

AI-powered Linux troubleshooting and developer productivity agent.

This repository has been reorganized into a small Python package layout. The main entrypoint is `src/main.py` and supporting code lives in `src/`, `llm/`, `utils/`, and `data/`.

Quick reference — recommended run commands:

Run the interactive CLI (preferred):

```bash
python3 -m src.main
```

Run the interactive CLI (alternative):

```bash
python3 src/main.py
```

Run in ReAct agent mode (step-by-step agent):

```bash
python3 -m src.main --react
```

Run demo mode:

```bash
python3 -m src.main --demo
```

Run via Makefile:

```bash
make run        # runs python3 -m src.main
make demo       # runs demo mode
```

Docker:

```bash
make docker-build
make docker-run
# inside container: python3 -m src.main
```

Project layout (important files only):

```
sysdoc/
  src/                 # main application code (entrypoint: src/main.py)
    agent_state.py
    analyzer.py
    executor.py
    history.py
    main.py
    planner.py
    reporter.py
    react_agent.py
  llm/                 # LLM integration helpers
  utils/               # helpers: safety, plan validation
  data/                # runtime data: reports/, sample_logs/, opspilot_history.log
  tests/               # example runners and tests
  tools.py             # thin tool adapter used by react agent
  Makefile
  Dockerfile
  README.md
```

Data and outputs:

- `data/reports/` — generated investigation reports
- `data/opspilot_history.log` — execution history log
- `data/sample_logs/` — sample application logs used by the `search_logs` tool

Local setup

```bash
git clone <repo-url>
cd sysdoc
python3 -m pip install -r requirements.txt
```

Running tests (basic script runners are in `tests/`):

```bash
python3 tests/test_react_agent.py
python3 -m tests.test_llm
```

Notes and recommendations

- Prefer `python3 -m src.main` so module imports resolve reliably.
- The Makefile targets call `python3 -m src.main` and `docker` for convenience.
- Reports and history now live under the `data/` directory.

If you'd like, I can also add a short `CONTRIBUTING.md` with development tips.

```text
df -h
du -sh *
```

Analysis:

```text
filesystem usage
largest directories
cleanup recommendations
```

---

## Log analysis

Input:

```text
check log errors
```

Output:

```text
grep -i ERROR sample_logs/app.log
```

Analysis:

```text
repeated database timeouts
auth failures
investigation recommendations
```

---

## Process inspection

Input:

```text
check running processes
```

Output:

```text
ps aux
```

---

## Large file search

Input:

```text
find large files
```

Output:

```text
find . -type f -size +100M
```

---

# Current Limitations

V1 intentionally uses rule-based planning.

Not yet included:

* LLM reasoning
* dynamic tool selection
* memory retrieval
* multi-step planning
* autonomous retries
* human approval
* multi-agent collaboration

---

# Roadmap

## V2 - LLM Planner

Replace static planner with OpenAI / Claude.

Flow:

```text
User request
-> LLM planner
-> command plan
```

Learn:

* prompt engineering
* tool calling
* structured outputs

---

## V3 - Agent Loop

Introduce ReAct:

```text
Reason
Act
Observe
Repeat
```

Dynamic troubleshooting.

---

## V4 - Memory

Add:

* SQLite session history
* vector semantic memory

Capabilities:

```text
similar incidents
past fixes
context recall
```

---

## V5 - LangChain

Introduce:

* prompt templates
* tools
* retrievers
* agent abstraction

---

## V6 - LangGraph

Production orchestration:

* planner node
* tool executor node
* validator node
* retries
* conditional routing
* human approval

---

## V7 - AutoGen Multi-Agent

Agents:

* planner
* Linux debugger
* bash script generator
* security reviewer
* report summarizer

---

# Interview Talking Points

This project demonstrates:

✅ Linux troubleshooting
✅ Bash automation
✅ Python systems programming
✅ safe command execution
✅ operational diagnostics
✅ AI agent architecture fundamentals
✅ production architecture thinking
✅ incremental framework adoption
✅ developer productivity tooling

---

# Future Production Extensions

Potential upgrades:

* FastAPI API service
* web dashboard
* Kubernetes deployment
* Slack bot integration
* GitHub Actions integration
* CI/CD failure investigation
* Claude Code integration
* shellcheck validation
* policy engine
* audit logging
* RBAC
* remote host diagnostics

---

# Long-Term Goal

OpsPilot evolves from:

```text
safe Linux assistant
```

into:

```text
production AI engineering operations agent
```

for:

* troubleshooting
* incident analysis
* deployment debugging
* automation generation
* developer workflow acceleration

This now looks like a serious production-oriented project, not a toy script.

