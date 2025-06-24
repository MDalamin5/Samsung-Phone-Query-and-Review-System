# /config.py
import os
from dotenv import load_dotenv

def load_environment():
    """Loads environment variables from .env file."""
    load_dotenv()
    
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Samsung Phone Assistant"
    
    print("LangSmith tracing is enabled for project: 'Samsung Phone Assistant'")

# Call it once at the start
load_environment()

# You can now import specific keys from here if you prefer
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")