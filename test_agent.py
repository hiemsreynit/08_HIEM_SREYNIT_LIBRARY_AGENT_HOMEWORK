from harness import execute_tool


result = execute_tool(
    tool_name="delete_book",
    arguments={"book_id": 1},
    role="admin",
    tool_call_count=0,
)

print(result)