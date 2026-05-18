
# OpsPilot AI

OpsPilot AI is a safe Linux troubleshooting and automation assistant.

It converts natural language operations questions into safe Linux investigation commands, executes them, analyzes the output, and stores command history.

## Why this project?

This project is designed for AI-first engineering workflows:

- Linux troubleshooting
- Bash/Python automation
- developer productivity
- safe command execution
- system reliability analysis
- agent-style tool usage

## V1 Features

- CLI interface
- rule-based planner
- safe command allowlist
- dangerous command blocking
- Linux command execution
- log error analysis
- command history

## Architecture

```text
User request
   ↓
Planner
   ↓
Safety Validator
   ↓
Command Executor
   ↓
Analyzer
   ↓
History Logger
   ↓
Final Diagnosis
````

## Supported intents

```text
disk usage
process / CPU / memory
log errors
large files
```

## Example

```bash
python3 main.py
```

```text
Ask OpsPilot > check log errors
```

Output:

```text
Plan + Execution:
- [RUNNING] grep -i ERROR sample_logs/app.log

Diagnosis:
- Found log errors.
- Most frequent errors:
  - 3x ERROR payment-service database timeout after 3000ms
  - 1x ERROR auth-service invalid token signature

Recommended next step:
- Investigate the most repeated error first, then check related service configuration.
```

## Safety

OpsPilot blocks dangerous commands such as:

```text
rm
sudo
shutdown
reboot
kill
chmod
chown
dd
mkfs
```

Only read-only diagnostic commands are allowed in V1.

## Roadmap

### V1

Rule-based safe Linux troubleshooting agent.

### V2

LLM-powered planner using OpenAI/Claude APIs.

### V3

Memory with SQLite and vector search.

### V4

LangChain integration.

### V5

LangGraph production workflow with nodes, routing, retries, and approval.

### V6

Multi-agent AutoGen version with planner, Linux debugger, script writer, and safety reviewer.


## Setup Docker Container

Create and run Ubuntu 22.04 container:
```bash
docker run -it --name opspilot-lab ubuntu:22.04 bash
```

## Access Existing Container

To open a shell in the running container:
```bash
docker exec -it opspilot-lab bash
```
