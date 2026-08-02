# ✦ CortexFlow AI

An enterprise AI assistant powered by **Snowflake Cortex**, **LangGraph**, and **Streamlit** that answers questions over both **structured enterprise data** and **unstructured policy documents** using intelligent query routing.

---

## Overview

CortexFlow AI enables employees to ask natural language questions such as:

- "How many leave days does Alice have left?"
- "What is the company's carry-forward leave policy?"
- "How many employees are in the organization?"
- "What is the travel reimbursement policy?"

The system automatically determines whether the question requires:

- 📄 Retrieval-Augmented Generation (RAG)
- 🗄️ SQL over structured enterprise data
- 🔀 A hybrid workflow combining both
- 💬 General conversational responses

---

## Architecture

```
                    User Query
                         │
                         ▼
                Intent Router (LLM)
                         │
      ┌───────────┬─────────────┬────────────┐
      ▼           ▼             ▼            ▼
    CHAT         RAG           SQL        HYBRID
      │           │             │            │
      │      Cortex Search   Snowflake      │
      │           │          SQL Query      │
      └───────────┴─────────────┬───────────┘
                                ▼
                         Response Synthesizer
                                │
                                ▼
                           Final Response
```

---

## Features

- Intelligent intent routing using LangGraph
- Snowflake Cortex LLM integration
- Cortex Search for enterprise document retrieval
- Automatic Text-to-SQL generation
- Hybrid reasoning over structured and unstructured data
- Secure read-only SQL execution
- Interactive Streamlit interface
- FastAPI backend

---

## Tech Stack

### Backend

- FastAPI
- LangGraph
- LangChain
- Snowflake Cortex
- Snowflake Cortex Search
- Snowflake Python Connector

### Frontend

- Streamlit

### Database

- Snowflake

---

## Project Structure

```
CortexFlow AI/
│
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   └── streamlit_app.py
│
├── docker/
├── tests/
├── .github/
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Clone the repository

```bash
git clone <repository-url>
cd CortexFlow-AI
```

### Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate     # macOS/Linux
# .venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Create a `.env` file:

```env
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_TOKEN=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_ROLE=
SNOWFLAKE_SEARCH_SCHEMA=
SNOWFLAKE_SEARCH_SERVICE=
SNOWFLAKE_CORTEX_MODEL=
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

---

### Frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## Example Questions

### SQL

- How many employees are there?
- How many leave days does Alice have left?

### RAG

- What is the leave carry-forward policy?
- What is the travel reimbursement policy?

### Hybrid

- How many leave days does Alice have left and what is the carry-forward policy?
- Does Bob have enough leave to take a two-week vacation according to company policy?

---

## Workflow

1. User submits a question
2. LangGraph routes it to the appropriate workflow
3. Snowflake Cortex Search retrieves policy documents (if required)
4. Snowflake SQL retrieves structured data (if required)
5. The synthesizer combines the results into a single response
6. Streamlit displays the answer along with the generated SQL and document sources

---

## Security

- Read-only SQL execution
- PAT-based authentication
- Environment-variable based configuration
- No hardcoded credentials

---

## License

This project is licensed under the MIT License.
