# Library Agent

## Requirements

- Python 3.10+
- Ollama
- Qwen 2.5 0.5B Instruct model

## 1. Project Overview

Library Agent is a small agentic application that helps users interact with a library.

The agent receives a user's request, decides which tool to use, executes the tool through the application, observes the result, and continues until it can provide a final answer.

The project uses a local LLM through Ollama and includes permission control and basic safety checks.

### Main Features

- Search for books
- Check book availability
- Borrow available books
- Delete books with admin permission
- Validate tool inputs
- Control tool permissions by user role
- Limit the maximum number of tool calls
- Handle tool errors safely

---

## 2. Available Tools

| Tool | Description | Permission |
|---|---|---|
| `search_book` | Searches for books by title or keyword. | Student, Admin |
| `check_availability` | Checks whether a specific book is available. | Student, Admin |
| `borrow_book` | Borrows a book if it is available. | Student, Admin |
| `delete_book` | Deletes a book from the library. | Admin only |

Each tool has a defined input schema using Pydantic.

For example, `check_availability` requires:

```text
book_id: integer
```

The application validates the arguments before executing the tool.

---

## 3. Agent Loop

The application follows a simple agent loop:

```text
User Request
     ↓
Agent / LLM
     ↓
Tool Call
     ↓
Application / Harness
     ↓
Permission + Validation
     ↓
Tool Execution
     ↓
Tool Result
     ↓
Agent / LLM
     ↓
Decide Again
     ↺
Final Answer
```

The agent can use the result of one tool to decide whether another tool is needed.

### Example

User:

```text
Find me a Python book that is currently available.
```

The agent can request:

```text
check_availability(book_id=1)
```

The tool returns:

```text
{
    "success": true,
    "book_id": 1,
    "title": "Python Crash Course",
    "available": true
}
```

The agent then uses this result to generate the final response.

---

## 4. Permission Rule

The application controls which tools each role can use.

### Student

A student can:

```text
search_book
check_availability
borrow_book
```

A student cannot:

```text
delete_book
```

### Admin

An admin can use all available tools:

```text
search_book
check_availability
borrow_book
delete_book
```

The permission check is performed by the application before the tool is executed.

For example:

```text
Student → delete_book
       ↓
Permission Check
       ↓
DENIED
```

The LLM can request a tool, but it cannot bypass the application's permission rules.

---

## 5. Safety

The project includes several basic safety mechanisms.

### Input Validation

Tool arguments are validated using Pydantic schemas.

For example:

```text
book_id > 0
```

If an invalid value is provided, the tool is not executed.

Example:

```text
book_id = -1
```

Result:

```text
Invalid tool arguments.
```

### Permission Control

The application checks the user's role before executing a tool.

For example:

```text
Student → delete_book → DENIED
Admin   → delete_book → ALLOWED
```

### Controlled Errors

The application does not expose raw exceptions to the user.

Instead, it returns controlled error messages such as:

```text
Unknown tool
Invalid tool arguments
Role is not allowed to use this tool
The tool failed while processing the request
```

### Tool-Call Limit

The agent has a maximum tool-call limit:

```text
MAX_TOOL_CALLS = 5
```

This prevents the agent from continuing to call tools indefinitely.

If the limit is reached, the agent stops and returns:

```text
The agent stopped because the maximum tool-call limit was reached.
```

---

## 6. Example Run

### Input

Role (student/admin): student

What do you need?
Find me a Python book that is currently available.

### Agent Execution

[Agent requested tool: check_availability]
[Arguments: {'book_id': 1}]

[Tool result: {
    'success': True,
    'book_id': 1,
    'title': 'Python Crash Course',
    'available': True
}]

### Final Answer

I found a Python book that is currently available.
The title of the book is "Python Crash Course".

### Permission Example

If a student attempts to delete a book:

```text
Tool: delete_book
Role: student
```

The application returns:

```text
{
    'success': False,
    'error': "Role 'student' is not allowed to use 'delete_book'."
}
```

This demonstrates that the application, rather than the LLM, controls whether a requested action is allowed.

---

## Project Structure

```text
my_agent/
│
├── agent.py
├── harness.py
├── schemas.py
├── tools.py
├── main.py
├── test_agent.py
└── README.md
```

### File Responsibilities

- `main.py` — Starts the application and receives user input.
- `agent.py` — Contains the LLM, tool definitions, and agent loop.
- `tools.py` — Contains the actual library tool implementations.
- `schemas.py` — Defines and validates tool input schemas.
- `harness.py` — Handles permissions, validation, errors, and tool-call limits.
- `test_agent.py` — Used to test the agent and safety mechanisms.
- `README.md` — Project documentation.