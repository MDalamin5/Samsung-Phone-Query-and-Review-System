# /graph/builder.py
from langgraph.graph import StateGraph, END, START
from .nodes import (
    supervisor_node,
    data_extraction_node,
    review_generate_node,
    rag_node,
    llm_node
)
from core.state import AgentState

def router(state: AgentState):
    """Conditional router for the graph."""
    print("--Router--")
    next_path = state["path"]
    print(next_path)
    
    if next_path == "RAG_CALL":
        return "RAG_CALL"
    elif next_path == "REVIEW_CALL":
        return "REVIEW_CALL"
    else:
        return "LLM_CALL"

def build_graph():
    """Builds and compiles the multi-agent graph."""
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("Supervisor", supervisor_node)
    builder.add_node("Data_Gether", data_extraction_node)
    builder.add_node("Review_Writer", review_generate_node)
    builder.add_node("RAG", rag_node)
    builder.add_node("LLM", llm_node)

    # Define edges
    builder.add_edge(START, "Supervisor")
    builder.add_conditional_edges(
        "Supervisor",
        router,
        {
            "RAG_CALL": "RAG",
            "REVIEW_CALL": "Data_Gether",
            "LLM_CALL": "LLM"
        }
    )
    builder.add_edge("Data_Gether", "Review_Writer")
    
    # Endpoints
    builder.add_edge("Review_Writer", END)
    builder.add_edge("LLM", END)
    builder.add_edge("RAG", END)

    graph = builder.compile()
    return graph