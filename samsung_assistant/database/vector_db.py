# /database/vector_db.py
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from config import PINECONE_API_KEY # Import the key
from core.models import embeddings # Import the embedding model

def get_pinecone_retriever(embedding_model):
    """
    Connects to Pinecone and returns a vector store retriever.
    """
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    index_name = "samsung-db"
    index = pc.Index(index_name)

    vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    return retriever

# Create a singleton instance
pinecone_retriever = get_pinecone_retriever(embeddings)