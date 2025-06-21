# /main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

import config  # This will run the environment loading at the start
from graph.builder import build_graph
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Define the Pydantic model for the request body ---
# It's better to keep this in main.py or a dedicated api_schemas.py
# if it's specific to the API layer.
class ChatRequest(BaseModel):
    """Request model for the /chat endpoint."""
    question: Annotated[str, Field(
        ...,
        description="The user's question for the assistant.",
        examples=["What is the camera of the Samsung S25 Ultra?"]
    )]

# --- 2. Create the graph and FastAPI app instances at the top level ---
print("Building LangGraph application...")
# This can take a few seconds, so it's good to do it once on startup.
graph = build_graph()
print("Graph built successfully. Starting FastAPI server...")

app = FastAPI(
    title="Samsung Phone Assistant API",
    description="An API for interacting with a multi-agent Q&A and Review system for Samsung phones.",
    version="1.0.0"
)

# --- 3. Define the API routes ---
@app.get("/", tags=["General"])
def read_root():
    """Welcome endpoint for the API."""
    return {"message": "Welcome to the Samsung Phone Assistant API!"}

@app.get("/health", tags=["General"])
def health_check():
    """Health check endpoint to verify the service is running."""
    return {
        "status": "OK",
        "graph_loaded": graph is not None
    }

@app.post("/chat", tags=["Chat"])
def chat_with_assistant(request: ChatRequest):
    """
    Main endpoint to send a question to the assistant and get a response.
    """
    user_input = request.question
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # Prepare the input for the LangGraph state
        inputs = {"messages": [HumanMessage(content=user_input)]}
        
        # Invoke the graph
        response_state = graph.invoke(inputs)
        
        # The final message is the last one in the list
        # It's an AIMessage object, we need its content
        final_message = response_state["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            response_content = final_message.content
        else:
            # Fallback in case the last message isn't an AIMessage
            response_content = str(final_message)

        return {"response": response_content}

    except Exception as e:
        print(f"An error occurred: {e}")
        # Re-raise as an HTTPException for a proper API error response
        raise HTTPException(status_code=500, detail=str(e))

# --- 4. Add a section to run the server with uvicorn ---
# This allows running the file directly with `python main.py` for development
if __name__ == "__main__":
    import uvicorn
    # The string 'main:app' tells uvicorn to look for the 'app' object
    # in the 'main.py' file. reload=True is great for development.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)