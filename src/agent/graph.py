from langgraph.graph import StateGraph, START, END
from src.agent.state import ASKNOVA, INTENT
from src.agent.prompts import SYSTEM_CHAT_PROMPT
from langchain_core.prompts import PromptTemplate
from src.helper import get_llm, get_logger
from IPython.display import Image, display

llm = get_llm()
print("graph>>LLM Initialized")

async def chatbot(state: ASKNOVA) -> ASKNOVA:
    print("In Chatbot")
    try:
        messages = state.get("messages", [])
        print("chatbot>>messages extracted")
        if len(messages) == 0: raise Exception
        query = messages[-1].content
        prompt = PromptTemplate(
            template=SYSTEM_CHAT_PROMPT,
            input_variables=["query"],
        )
        print("chatbot>>prompt generated")
        chain = prompt | llm
        print("chatbot>>chain generated")
        response = chain.invoke({"query":query})
        print("chatbot>>response generated")
        return {
            "messages": [response]
        }

    except Exception as e:
        print(f"chatbot>> Error Ocurred with message: {e}")

async def build_graph():
    graph = StateGraph(ASKNOVA)

    graph.add_node("chatbot", chatbot)

    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot",END)
    workflow = graph.compile()
    png = workflow.get_graph().draw_mermaid_png()
    with open("workflow.png", "wb") as f:
        f.write(png)
    return workflow