# /core/models.py
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv

def load_environment():
    """Loads environment variables from .env file."""
    load_dotenv()

# Call it once at the start
load_environment()

# You can now import specific keys from here if you prefer
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

def get_llm():
    """Initializes and returns the ChatGroq LLM."""
    return ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

def get_embedding_model():
    """Initializes and returns the HuggingFace embedding model."""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Create singleton instances to be imported by other modules
llm = get_llm()
embeddings = get_embedding_model()