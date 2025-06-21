# /app.py

import streamlit as st
import requests
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Samsung Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- API Configuration ---
# This should be the URL where your FastAPI backend is running.
# If you are running both on your local machine, this is the correct URL.
API_URL = "http://127.0.0.1:8000/chat"

# --- Page Title and Description ---
st.title("🤖 Samsung Phone Assistant")
st.caption("Your intelligent expert for Samsung phone specs and reviews.")

# --- Session State Initialization ---
# This is crucial for maintaining the chat history.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you with Samsung phones today?"}
    ]

# --- Display Chat History ---
# This loop will display all the messages stored in the session state.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Function to Query the Backend ---
def get_assistant_response(user_input: str):
    """
    Sends the user's input to the FastAPI backend and gets the response.
    """
    try:
        response = requests.post(API_URL, json={"question": user_input})
        
        # Check for a successful response
        if response.status_code == 200:
            return response.json().get("response", "Sorry, I received an empty response.")
        else:
            # Handle API errors gracefully
            error_details = response.json().get('detail', 'Unknown error')
            st.error(f"Error from API: {response.status_code} - {error_details}")
            return None
            
    except requests.exceptions.RequestException as e:
        # Handle connection errors
        st.error(f"Could not connect to the assistant API: {e}")
        return None

# --- Chat Input Handling ---
# The `st.chat_input` widget provides the text input box at the bottom of the screen.
if prompt := st.chat_input("Ask me about a Samsung phone..."):
    
    # 1. Add user's message to the session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get the assistant's response
    with st.chat_message("assistant"):
        # Use a spinner to show that the assistant is "thinking"
        with st.spinner("Thinking..."):
            response = get_assistant_response(prompt)
        
        # If a response was successfully received, display it
        if response:
            # A small delay can make the interaction feel more natural
            time.sleep(0.5)
            st.markdown(response)
            # Add the assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- Sidebar (Optional, but professional) ---
with st.sidebar:
    st.header("About")
    st.markdown(
        "This chatbot is powered by a multi-agent system built with LangGraph. "
        "It can answer specific questions about Samsung phone specifications (RAG) "
        "or generate detailed product reviews."
    )
    st.markdown("---")
    st.subheader("Example Questions")
    st.markdown("- What is the battery capacity of the Samsung Galaxy S25 Ultra?")
    st.markdown("- Please write a review for the Samsung Galaxy A06 5G.")
    st.markdown("- hi how are you")