from langgraph.graph import StateGraph, START, END
from src.agent.state import ASKNOVA
from src.agent.prompts import SYSTEM_CHAT_PROMPT, INTENT_FINDER
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from src.helper import get_llm, get_logger
from IPython.display import Image, display
import json

llm = get_llm()
print("graph>>LLM Initialized")

async def intent_finder(state: ASKNOVA) -> ASKNOVA:
    print("In Intent Finder")
    try:
        msg = state.get("messages")
        user_query = msg[-1]
        print("intent_finder>> user query")
        prompt = PromptTemplate(
            template=INTENT_FINDER,
            input_variables=["query"],
        )
        chain = prompt | llm
        response = await chain.ainvoke({"query": user_query})
        print(f"intent_finder>> RESPONSE: {response}")
        data = json.loads(response.content)
        tone = data["tone"]
        print(f"intent_finder>> Tone Extracted: {tone}")

        return {
            "tone": tone
        }
    except Exception as e:
        print(f"chatbot>> Error Ocurred with message: {e}")

    return {
        "tone": "normal"
    }


async def chatbot(state: ASKNOVA) -> ASKNOVA:
    print("In Chatbot")
    try:
        messages = state.get("messages", [])
        tone = state.get("tone", "")
        print("chatbot>>messages extracted")
        print(f"chatbot>>tone extracted from the state: {tone}")
        if len(messages) == 0: raise Exception
        query = messages[-1].content
        prompt = PromptTemplate(
            template=SYSTEM_CHAT_PROMPT,
            input_variables=["tone","query"],
        )
        print("chatbot>>prompt generated")
        chain = prompt | llm
        print("chatbot>>chain generated")
        response = await chain.ainvoke({"tone":tone,"query":query})
        print("chatbot>>response generated")
        return {
            "messages": [response]
        }

    except Exception as e:
        print(f"chatbot>> Error Ocurred with message: {e}")

    return {
        "messages": AIMessage(content="Network Error. Please send your Query again.")
    }

async def build_graph():
    graph = StateGraph(ASKNOVA)

    graph.add_node("intent_finder",intent_finder)
    graph.add_node("chatbot", chatbot)

    graph.add_edge(START, "intent_finder")
    graph.add_edge("intent_finder","chatbot")
    graph.add_edge("chatbot",END)
    workflow = graph.compile()
    png = workflow.get_graph().draw_mermaid_png()
    with open("workflow.png", "wb") as f:
        f.write(png)
    return workflow