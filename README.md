
# OpsPilot AI

AI-powered Linux troubleshooting and developer productivity agent.

This repository is organized around a Python package layout. The main entrypoint is `src/main.py`, and application code lives under `src/`, `llm/`, and `utils/`.

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
```

Docker workflow notes:

- If you run `python3 -m pip install ...` inside a live container, the install only lasts for that container instance.
- To make packages stay installed for future containers, add them to `requirements.txt` and rebuild the image with `make docker-build`.
- The Dockerfile installs dependencies from `requirements.txt` during image build, so that layer is what should hold `faiss-cpu`, `numpy`, and `sentence-transformers`.
- The usual flow is: build once, then start as many containers as you want from that image.
- If you are already inside a running container and want a quick temporary fix, you can still run `python3 -m pip install ...` there, but you will need a rebuild to persist it.

Project layout (important files only):

```
sysdoc/
  src/                 # main application code (entrypoint: src/main.py)
    agent_state.py
    analyzer.py
    approval.py
    audit.py
    config.py
    executor.py
    history.py
    main.py
    memory.py
    planner.py
    reporter.py
    react_agent.py
    react_reporter.py
    script_audit.py
    script_executor.py
    script_generator.py
    script_safety.py
    tools.py
    vector_memory.py
  llm/                 # LLM integration helpers
  utils/               # helpers: safety, plan validation
  data/                # runtime data: reports/, sample_logs/, opspilot_history.log
  tests/               # example runners and tests
  Makefile
  Dockerfile
  README.md
```

Data and outputs:

- `ops_reports/` — generated investigation reports
- `ops_audit_logs/` — ReAct audit logs
- `generated_scripts/` — saved Bash scripts from script mode
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
- The Makefile targets call `python3 -m src.main` and Docker for convenience.
- Reports now live in `ops_reports/`, audit logs in `ops_audit_logs/`, and script output in `generated_scripts/`.
- `data/` is kept for sample logs and the history log file.
- ReAct and semantic memory depend on `faiss-cpu`, `numpy`, and `sentence-transformers` being installed in the container image.

LLM provider switching

- Use `.env` to control LLM provider and model selection.
- Use `openrouter` or `ollama` as the provider value in `LLM_PROVIDER`.
- Set `OPENROUTER_MODEL` to choose the OpenRouter model.
- Set `OLLAMA_MODEL` to choose the Ollama model.
- Set `OLLAMA_BASE_URL` to point at your Ollama server.
- The Docker default for Ollama is `http://host.docker.internal:11434/v1`.
- Keep one provider block active in `.env` and comment out the other.

Example `.env` values:

```bash
# OpenRouter
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=openrouter/free

# Ollama
#LLM_PROVIDER=ollama
#OLLAMA_MODEL=llama3.1
#OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
```

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

