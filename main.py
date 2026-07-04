import asyncio
from langchain_core.messages import HumanMessage
from src.agent.graph import build_graph


async def main():
    workflow = await build_graph()

    while True:
        query = input("Write Your Query: ")

        initial_state = {
            "messages": [HumanMessage(content=query)]
        }

        response = await workflow.ainvoke(initial_state)

        messages = response.get("messages", [])

        print(f"Human: {query}")
        print(f"AI: {messages[-1].content}")


if __name__ == "__main__":
    asyncio.run(main())