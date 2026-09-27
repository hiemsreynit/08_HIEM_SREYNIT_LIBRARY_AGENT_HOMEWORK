from agent import run_agent


def main():
    role = input("Role (student/admin): ").strip().lower()
    user_request = input("What do you need? ").strip()

    answer = run_agent(
        user_request,
        role=role,
    )

    print("\nAssistant:")
    print(answer)


if __name__ == "__main__":
    main()