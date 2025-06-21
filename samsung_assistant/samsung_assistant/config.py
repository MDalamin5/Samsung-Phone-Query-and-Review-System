# /config.py
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