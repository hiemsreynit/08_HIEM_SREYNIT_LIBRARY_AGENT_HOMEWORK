import json
import ollama

from harness import execute_tool, MAX_TOOL_CALLS


MODEL_NAME = "qwen2.5:0.5b-instruct"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_book",
            "description": "Search for books by title or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_name": {
                        "type": "string",
                        "description": "The book title or keyword to search for.",
                    }
                },
                "required": ["book_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check whether a specific book is currently available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book.",
                    }
                },
                "required": ["book_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "borrow_book",
            "description": "Borrow a book if it is currently available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book to borrow.",
                    }
                },
                "required": ["book_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_book",
            "description": "Delete a book from the library. Admin permission is required.",
            "parameters": {
                "type": "object",
                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book.",
                    }
                },
                "required": ["book_id"],
            },
        },
    },
]


SYSTEM_PROMPT = """
You are a library assistant.

You can use tools to search books, check availability,
borrow books, and delete books.

Rules:
- When the user asks to find a book, use search_book first.
- If you need to check availability, first search for the book.
- Use the book ID returned by search_book when calling check_availability.
- Do not use book_name with check_availability.
- Use the result of one tool to decide whether another tool is needed.
- Do not invent book information.
- If a tool returns an error, explain the problem to the user.
- When you have enough information, give a concise final answer.
"""


def run_agent(user_request: str, role: str = "student"):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    tool_call_count = 0

    while tool_call_count < MAX_TOOL_CALLS:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
        )

        assistant_message = response["message"]
        messages.append(assistant_message)

        if not assistant_message.get("tool_calls"):
            return assistant_message.get(
                "content",
                "I could not generate a final answer.",
            )

        for tool_call in assistant_message["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]

            print(f"\n[Agent requested tool: {tool_name}]")
            print(f"[Arguments: {arguments}]")

            result = execute_tool(
                tool_name=tool_name,
                arguments=arguments,
                role=role,
                tool_call_count=tool_call_count,
            )

            tool_call_count += 1

            print(f"[Tool result: {result}]")

            messages.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                }
            )

            if tool_call_count >= MAX_TOOL_CALLS:
                break

    return "The agent stopped because the maximum tool-call limit was reached."