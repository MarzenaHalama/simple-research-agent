from src.agent import run_agent


def main():
    task_prompt = input("Enter your question for the agent: ")
    run_agent(task_prompt)


if __name__ == "__main__":
    main()
