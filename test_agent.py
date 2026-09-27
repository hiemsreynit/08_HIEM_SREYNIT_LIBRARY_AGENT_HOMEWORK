from agent import run_agent


result = run_agent(
    "Find me a Python book that is currently available.",
    role="student",
)

print("\nFinal answer:")
print(result)