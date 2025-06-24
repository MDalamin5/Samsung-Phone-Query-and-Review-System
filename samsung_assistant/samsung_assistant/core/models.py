# /core/models.py
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

def get_llm():
    """Initializes and returns the ChatGroq LLM."""
    return ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

def get_embedding_model():
    """Initializes and returns the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Create singleton instances to be imported by other modules
llm = get_llm()
embeddings = get_embedding_model()