
# OpsPilot AI

AI-powered Linux troubleshooting and developer productivity agent.

OpsPilot converts natural language engineering troubleshooting requests into safe Linux investigation workflows, executes diagnostic commands, analyzes results, and generates operational reports.

This project is being built incrementally from first principles to understand how production AI agents work before introducing frameworks like LangChain, LangGraph, and AutoGen.

---

# Motivation

Modern engineering teams spend significant time on repetitive troubleshooting tasks:

- checking disk usage
- analyzing logs
- finding failing processes
- locating large files
- investigating infrastructure issues
- writing diagnostic shell commands manually

OpsPilot explores how AI agents can improve engineering productivity by safely automating these workflows.

---

# Why this project?

This project directly aligns with roles focused on:

- Linux systems troubleshooting
- Bash / Python automation
- engineering productivity
- AI-first developer workflows
- operational reliability
- safe automation
- agentic tooling

---

# V1 Scope

V1 is a safe Linux troubleshooting assistant.

Core workflow:

```text
User request
   |
Planner
   |
Safety Validator
   |
Command Executor
   |
Analyzer
   |
History Logger
   |
Report Generator
```

Example:

```text
User:
"My disk is full"

OpsPilot:
- plans investigation steps
- selects safe Linux commands
- executes diagnostics
- analyzes outputs
- generates recommendations
```

---

# Features (V1)

## CLI Interface

Interactive terminal agent:

```bash
python3 main.py
```

---

## Demo Mode

Quick demo for interviewers / reviewers:

```bash
python3 main.py --demo
```

---

## Rule-Based Planner

Maps user intent into investigation workflows.

Supported categories:

* disk usage
* processes / CPU / memory
* log errors
* large files

---

## Safety Guardrails

Allowed commands:

```text
df
du
ps
grep
find
ls
cat
head
tail
wc
echo
```

Blocked dangerous commands:

```text
rm
sudo
shutdown
reboot
kill
pkill
chmod
chown
mv
dd
mkfs
mount
umount
```

Blocked shell operators:

```text
&&
||
;
>
>>
<
$()
`
```

## Linux Command Execution

Commands are executed using:

```python
subprocess.run()
```

With:

* timeout protection
* stdout capture
* stderr capture
* return code handling

---

## Log Analysis

OpsPilot analyzes repeated application errors.

Example:

```text
payment-service database timeout
```

Frequency detection:

```text
3x repeated timeout
```

Helps identify likely root causes.

---

## Command History

Every session logs:

* timestamp
* user request
* category
* planner reason
* commands executed
* stdout
* stderr

Saved to:

```text
opspilot_history.log
```

---

## Report Generation

Each investigation generates a timestamped report:

```text
reports/report_YYYYMMDD_HHMMSS.txt
```

---

# Architecture

```text
+-------------------------+
| User CLI Input          |
+-------------------------+
                  |
                  v
+-------------------------+
| Planner                 |
| Intent -> Commands      |
+-------------------------+
                  |
                  v
+-------------------------+
| Safety Validator        |
| Allowlist / Blocking    |
+-------------------------+
                  |
                  v
+-------------------------+
| Command Executor        |
| subprocess.run()        |
+-------------------------+
                  |
                  v
+-------------------------+
| Analyzer                |
| Result interpretation   |
+-------------------------+
                  |
                  v
+-------------------------+
| History + Reports       |
+-------------------------+
```

---

# Project Structure

```text
opspilot-ai/
   main.py
   planner.py
   safety.py
   executor.py
   analyzer.py
   history.py
   reporter.py
   sample_logs/
      app.log
   reports/
   Dockerfile
   Makefile
   README.md
```

---

# Local Setup

## Clone

```bash
git clone <repo-url>
cd opspilot-ai
```

---

## Run

```bash
python3 main.py
```

---

## Demo

```bash
python3 main.py --demo
```

---

# Makefile Commands

Run:

```bash
make run
```

Demo:

```bash
make demo
```

Docker build:

```bash
make docker-build
```

Docker run:

```bash
make docker-run
```

Clean generated artifacts:

```bash
make clean
```

---

# Docker Linux Lab (Mac Friendly)

This project is developed on macOS but runs Linux diagnostics inside Docker.

Build:

```bash
docker build -t opspilot-ai .
```

Run:

```bash
docker run -it --rm -v $(pwd):/app opspilot-ai
```

Inside container:

```bash
python3 main.py
```

This provides:

* Ubuntu environment
* Linux utilities
* isolated troubleshooting lab

---

# Example Usage

## Disk troubleshooting

Input:

```text
check disk usage
```

Output:

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

