# Library Agent

A small agentic application that helps users interact with a library using an LLM and tools.

The agent receives a user's request, decides which tool to use, executes the tool through a safety layer, observes the result, and continues until it can provide a final answer.

## Project Overview

This project demonstrates a basic **Agentic AI workflow**:

```text
User Request
     ↓
Agent / LLM
     ↓
Tool Call
     ↓
Safety & Control Layer
     ↓
Tool Execution
     ↓
Tool Result
     ↓
Agent decides again
     ↺
Final Answer
```

The project uses a local Ollama model and does not use LangChain or LangGraph.

## Tools

The Library Agent has four tools:

| Tool | Description | Risk |
|---|---|---|
| `search_book` | Search for books by title or keyword | Green |
| `check_availability` | Check whether a book is available | Green |
| `borrow_book` | Borrow an available book | Yellow |
| `delete_book` | Delete a book from the library | Red |

## Permission Rules

The application controls which tools each role can use.

| Role | Allowed Tools |
|---|---|
| Student | `search_book`, `check_availability`, `borrow_book` |
| Admin | All four tools |

For example, a student cannot use `delete_book`.

The permission check is performed by the application, not by the LLM.

## Safety Features

### 1. Input Validation

Tool arguments are validated using Pydantic schemas before a tool is executed.

For example:

```text
book_id must be an integer greater than 0
book_name cannot be empty
```

Invalid arguments are rejected by the application.

### 2. Allowlist

Only tools registered in `TOOL_REGISTRY` are allowed to execute.

If the agent requests an unknown tool, the application rejects it.

```text
Agent requests tool
       ↓
Is tool registered?
   ┌───┴───┐
  Yes      No
   ↓        ↓
Execute   Reject
```

### 3. Risk Classification

Each tool is assigned a risk level:

```text
Green  → Low risk
Yellow → More sensitive
Red    → High risk
```

The application uses these levels to apply different execution policies.

For this project:

- Green tools can execute normally.
- Yellow tools are treated as more sensitive operations.
- Red tools require human approval.

### 4. Human-in-the-Loop (HITL)

High-risk actions require human approval before execution.

For example:

```text
Agent requests delete_book
          ↓
Permission check
          ↓
Risk = Red
          ↓
Human approval required
          ↓
Continue? (yes/no)
          ↓
       Execute
```

If the user rejects the action, the tool is not executed.

### 5. Maximum Tool-Call Limit

The agent has a maximum number of tool calls:

```text
MAX_TOOL_CALLS = 5
```

This prevents the agent from continuing tool calls indefinitely.

### 6. Controlled Failure Handling

The application catches validation errors, permission errors, unknown tools, and tool execution failures.

Instead of allowing the application to crash, the harness returns a controlled error.

## Agent Loop

The agent follows an iterative loop:

```text
User Request
     ↓
LLM decides what to do
     ↓
Tool call requested
     ↓
Harness validates and checks permissions
     ↓
Risk policy is applied
     ↓
Tool executes
     ↓
Result returned to LLM
     ↓
LLM decides whether another action is needed
     ↓
Final Answer
```

For example:

```text
User:
"Find me a Python book that is currently available."

       ↓

search_book("Python")
       ↓

Python Crash Course → ID: 1
       ↓

check_availability(book_id=1)
       ↓

Available
       ↓

Final Answer
```

## Project Structure

```text
my_agent/
├── agent.py
├── harness.py
├── schemas.py
├── tools.py
├── main.py
├── test_agent.py
├── requirements.txt
├── README.md
└── .gitignore
```

### File Responsibilities

| File | Purpose |
|---|---|
| `main.py` | Application entry point |
| `agent.py` | LLM interaction and agent loop |
| `harness.py` | Tool validation, permissions, risk control, HITL, and execution limits |
| `tools.py` | Library tool implementations |
| `schemas.py` | Pydantic input schemas |
| `test_agent.py` | Tests and demonstrations of safety features |
| `requirements.txt` | Python dependencies |

## Requirements

- Python 3.14
- Ollama
- `qwen2.5:0.5b-instruct`
- Pydantic
- ollama
- python-dotenv

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Git Bash:

```bash
source venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running and the model is available:

```bash
ollama pull qwen2.5:0.5b-instruct
```

## Run the Application

Start the Library Agent:

```bash
python main.py
```

Example:

```text
Role (student/admin): student
What do you need? Find me a Python book that is currently available.
```

The agent will decide which tools to use and return a final answer.

## Test Safety Features

`test_agent.py` can be used to test individual safety mechanisms without depending on the LLM to choose a particular tool.

For example, it can demonstrate:

- Permission control
- Risk Classification
- Human-in-the-Loop
- Input validation
- Tool-call limits
- Controlled errors

Run:

```bash
python test_agent.py
```

## Example HITL Test

When an admin attempts to delete a book:

```text
This is a high-risk action. Continue? (yes/no):
```

If the human enters:

```text
no
```

the action is cancelled.

If the human enters:

```text
yes
```

the tool is allowed to execute.

## Purpose of the Project

The main purpose of this project is to demonstrate how an agentic application can combine:

- LLM reasoning
- Tool calling
- Tool schemas
- Application-level permissions
- Risk classification
- Human approval
- Input validation
- Failure handling
- Execution limits

The LLM can propose an action, but the **application controls whether that action is allowed to execute**.