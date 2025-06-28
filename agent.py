from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from datetime import datetime, timedelta
import calendar_integration  # Custom Google Calendar module

llm = ChatOpenAI(temperature=0)

# Define state
def run_agent(state):
    history = state["history"]
    last_user_message = history[-1].content

    # Very basic intent detection
    if "book" in last_user_message or "schedule" in last_user_message:
        response = calendar_integration.check_and_book_slot(last_user_message)
    else:
        response = llm.invoke(history)

    return {"history": history + [AIMessage(content=response)]}

# LangGraph build
builder = StateGraph()
builder.add_node("run_agent", run_agent)
builder.set_entry_point("run_agent")
builder.set_finish_point("run_agent")
graph = builder.compile()
