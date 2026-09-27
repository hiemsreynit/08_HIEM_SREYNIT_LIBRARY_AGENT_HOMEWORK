from pydantic import ValidationError

from schemas import (
    SearchBookInput,
    CheckAvailabilityInput,
    BorrowBookInput,
    DeleteBookInput,
)

from tools import (
    search_book,
    check_availability,
    borrow_book,
    delete_book,
)


MAX_TOOL_CALLS = 5


PERMISSIONS = {
    "student": {
        "search_book",
        "check_availability",
        "borrow_book",
    },
    "admin": {
        "search_book",
        "check_availability",
        "borrow_book",
        "delete_book",
    },
}

TOOL_REGISTRY = {
    "search_book": {
        "schema": SearchBookInput,
        "function": search_book,
    },
    "check_availability": {
        "schema": CheckAvailabilityInput,
        "function": check_availability,
    },
    "borrow_book": {
        "schema": BorrowBookInput,
        "function": borrow_book,
    },
    "delete_book": {
        "schema": DeleteBookInput,
        "function": delete_book,
    },
}


def execute_tool(
    tool_name: str,
    arguments: dict,
    role: str,
    tool_call_count: int,
):
    if tool_call_count >= MAX_TOOL_CALLS:
        return {
            "success": False,
            "error": "Tool-call limit reached.",
        }

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
        }

    if role not in PERMISSIONS:
        return {
            "success": False,
            "error": f"Unknown role: {role}",
        }

    if tool_name not in PERMISSIONS[role]:
        return {
            "success": False,
            "error": f"Role '{role}' is not allowed to use '{tool_name}'.",
        }

    tool = TOOL_REGISTRY[tool_name]

    try:
        validated_input = tool["schema"](**arguments)
    except ValidationError as error:
        return {
            "success": False,
            "error": "Invalid tool arguments.",
            "details": error.errors(),
        }

    try:
        result = tool["function"](validated_input)
        return result

    except Exception:
        return {
            "success": False,
            "error": "The tool failed while processing the request.",
        }