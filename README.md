# Samsung Phone Assistant: A Multi-Agent Q&A and Review System

![Samsung Assistant Demo](https://img.shields.io/badge/Samsung%20Assistant-Live-blue?style=for-the-badge&logo=samsung)

This project implements a sophisticated, multi-agent chatbot designed to be an expert on Samsung mobile phones. It leverages modern AI and database technologies to provide users with precise answers to technical questions and generate detailed, human-like product reviews.

The system is built using **LangGraph** to orchestrate multiple specialized agents, a **RAG (Retrieval-Augmented Generation)** pipeline for factual Q&A, and a connection to a SQL database for generating dynamic content.

## ✨ Features

-   **Dual-Agent System**:
    -   **RAG Agent**: Answers specific questions about phone specs (e.g., "What is the battery capacity?") by retrieving information from a Pinecone vector database.
    -   **Review Agent**: Generates detailed, professional-style reviews for any phone in the database by querying a MySQL database for full specifications.
-   **Intelligent Routing**: A supervisor agent analyzes the user's query to intelligently route the request to the appropriate agent (RAG, Review, or a general LLM for chit-chat).
-   **Vector Database for Q&A**: Uses Pinecone and Hugging Face embeddings for fast and accurate similarity searches on phone specifications.
-   **SQL Integration for Reviews**: Dynamically pulls comprehensive phone data from a MySQL database to generate rich, context-aware reviews.
-   **Interactive Interfaces**:
    -   A robust **FastAPI** backend serves the agent's logic.
    -   A user-friendly **Streamlit** frontend provides an interactive chatbot experience.
-   **Full Observability**: Integrated with **LangSmith** for end-to-end tracing and debugging of agent interactions.

## 🏛️ System Architecture

The project is built on a modular, multi-agent architecture orchestrated by LangGraph. This design separates concerns and allows for scalable and maintainable code.

<!-- It's highly recommended to create a simple diagram (e.g., using draw.io or Excalidraw) and link it here -->

1.  **User Interface (Streamlit)**: The user interacts with the system through a web-based chat interface.
2.  **API Backend (FastAPI)**: The Streamlit UI sends requests to the FastAPI server, which exposes the chatbot's logic.
3.  **Supervisor Agent (LangGraph)**: The entry point. This agent classifies the user's intent and determines which specialized agent should handle the request.
4.  **RAG Agent**:
    -   **Retriever**: Queries the **Pinecone** vector database to find documents relevant to the user's question.
    -   **Generator**: Uses the retrieved context and a powerful LLM (Groq Llama 4 Scout) to generate a precise answer.
5.  **Review Agent**:
    -   **Data Extractor**: Queries the **MySQL** database for the complete specifications of the requested phone.
    -   **Review Writer**: Uses the structured data from MySQL and the LLM to write a comprehensive, narrative-style review.

## 🛠️ Tech Stack

-   **Backend Framework**: FastAPI
-   **Frontend Framework**: Streamlit
-   **Orchestration**: LangGraph
-   **LLM Provider**: Groq (Llama 4 Scout 17B)
-   **Vector Database**: Pinecone
-   **Relational Database**: MySQL
-   **Embeddings**: Hugging Face (`sentence-transformers/all-mpnet-base-v2`)
-   **Observability**: LangSmith
-   **Containerization (Optional)**: Docker, Docker Compose

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

-   Python 3.10+
-   MySQL Server
-   Access to Pinecone, Groq, and LangSmith APIs.

### 2. Clone the Repository

```bash
git clone https://github.com/MDalamin5/Samsung-Phone-Query-and-Review-System.git
cd samsung_assistant/
```

### 3. Set Up the Environment
- a. Create a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
- c. Configure Environment Variables

Create a .env file in the project root directory and add your API keys and database credentials.

# .env

# API Keys
GROQ_API_KEY="gsk_..."
PINECONE_API_KEY="..."
HF_TOKEN="..."

# LangSmith Tracing
LANGCHAIN_API_KEY="ls__..."
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_PROJECT="Samsung Phone Assistant"

# MySQL Database (Optional - can be hardcoded in sql_db.py)
DB_USER="root"
DB_PASSWORD=""
DB_HOST="localhost"
DB_NAME="device_specs_db"


### 4. Database Setup
#### a. MySQL Database

1. Ensure your MySQL server is running.
2. Create a database named device_specs_db.
3. Import the provided SQL schema and data into the database. You can use a tool like MySQL 
4. Workbench or the command line.

```bash
-- Example table structure
CREATE TABLE samsung_phone (
    phone_name VARCHAR(255) PRIMARY KEY,
    network_technology VARCHAR(255),
    -- ... other columns for phone specs
);
```
- b. Pinecone Vector Database

Create a Pinecone index (e.g., samsung-db) with the correct dimension for the embedding model (768 for all-mpnet-base-v2).

Run the data ingestion script (if provided) to populate the vector database with phone spec embeddings. or for embedding checkout the `02-RAG-QnA` directory.

### 5. Running the Application
You need to run the backend and frontend in two separate terminals.

* **Terminal 1: Start the FastAPI Backend**

* Navigate to the project root and run:

```bash
python main.py
```

The backend server will be running on http://127.0.0.1:8000.


- Terminal 2: Start the Streamlit Frontend
- In a new terminal, navigate to the project root and run:

```bash
streamlit run app.py
```
- This will open the chatbot interface in your web browser, typically at http://localhost:8501.

### 🧪 Usage Examples

Once the application is running, you can interact with the chatbot. Here are some examples:

- Ask a specific question (RAG Agent):
    - "What are the camera specs of the Samsung Galaxy S23 Ultra?"
- Request a review (Review Agent):
    - "Please write a detailed review for the Samsung Galaxy S25 Ultra"
- Have a general conversation (LLM Agent):
    - "Hi, how are you today?"

### 📁 Project Structure
```bash
samsung-assistant/
├── app.py                 # Streamlit frontend application
├── README.md              # This file
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (local)
└── samsung_assistant/
    ├── __init__.py
    ├── main.py            # FastAPI backend application
    ├── config.py          # Environment loading and LangSmith setup
    ├── core/              # Core components like state and models
    │   ├── models.py
    │   └── state.py
    ├── database/          # Database connection modules
    │   ├── sql_db.py
    │   └── vector_db.py
    └── graph/             # LangGraph agent definitions
        ├── builder.py
        ├── nodes.py
        ├── prompts.py
        └── schemas.py

```