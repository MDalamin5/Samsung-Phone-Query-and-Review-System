# /graph/nodes.py
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough

from core.state import AgentState
from core.models import llm
from database.sql_db import sql_engine, fetch_phone_data
from database.vector_db import pinecone_retriever
from .prompts import (
    phone_name_prompt, phone_name_parser, review_prompt, 
    rag_prompt, llm_prompt, supervisor_prompt, path_parser # Renamed path_prompt
)

# Helper function from the RAG chain
def format_docs(retriever_docs):
    context_text = ""
    for doc in retriever_docs:
        phone_name = doc.metadata.get("phone_name", "unknown")
        context_text += f"Phone name (metadata): {phone_name}\n"
        context_text += f"{doc.page_content}\n\n"
    # print(context_text)
    return context_text.strip()

# --- Node for Phone Name Extraction (used by review agent) ---
def get_phone_name_from_query(question: str) -> str:
    """Extracts a structured phone name from a user query."""
    ph_name_extract_chain = phone_name_prompt | llm | phone_name_parser
    response = ph_name_extract_chain.invoke({"question": question})
    return response.phone_name

# --- Supervisor Node ---
def supervisor_node(state: AgentState):
    """This node is responsible for to select the correct path based on the user query."""
    question = state['messages'][-1].content
    print(question)
    chain = supervisor_prompt | llm | path_parser
    response = chain.invoke(question)
    print(response.path, response.reason)
    
    return {
        "path": response.path
    }
    
# --- Review Agent Nodes ---
def data_extraction_node(state: AgentState):
    print("--Data extraction--")
    question = state["messages"][-1].content
    
    phone_name = get_phone_name_from_query(question)
    
    if not phone_name:
        context_str = ""
    else:
        context_str = fetch_phone_data(sql_engine, phone_name)
    
    print("---Data extraction done---")
    return {"ph_raw_data": context_str}

# --Review Generate Node----
from langchain_core.output_parsers import StrOutputParser

def review_generate_node(state: AgentState):
    print("--Review generate--")
    question = state['messages'][-1].content
    phone_context = state["ph_raw_data"]
    print(question)
    # print(phone_context)
    
    review_chain = review_prompt | llm | StrOutputParser()
    # response = llm.invoke(question)
    
    response = review_chain.invoke(
        {
            "question": question,
            "context": phone_context
        }
    )
    
    return {
        "messages": [response]
    }

# --- RAG Node ---
def rag_node(state: AgentState):
    print("--Rag call--")
    question = state['messages'][-1].content
    print(question)
    
    
    print("im hare-1")
    rag_chain = (
        {
            "context": pinecone_retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    print("im hare-2")
    response = rag_chain.invoke(question)
    print("rag-response", response)
    
    return {
        "messages": [response]
    }

# --- General LLM Node ---
def llm_node(state: AgentState):
    print("--LLM Call--")
    question = state['messages'][0].content
    chain = llm_prompt | llm | StrOutputParser()
    response = chain.invoke(
        {
            "question": question
        }
    )
    print(response)
    return {
        "messages": [response]
    }