"""Public hackathon demo UI for CortexFlow AI.

Local usage from the CortexFlow repository root:
    streamlit run frontend/streamlit_app.py
"""

import os
from typing import Any

import requests
import streamlit as st


API_URL = os.getenv("CORTEXFLOW_API_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="CortexFlow AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


def ask_cortexflow(question: str) -> dict[str, Any]:
    """Submit a question to the existing FastAPI chat endpoint."""
    response = requests.post(
        f"{API_URL}/chat/",
        json={"message": question},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return {
    "answer": payload.get("response", "No response received."),
    "sources": payload.get("sources", []),
    "intent": payload.get("intent"),
    "generated_sql": payload.get("generated_sql"),}


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("# ✦ CortexFlow AI")
    st.caption("Enterprise Intelligence Workspace")
    st.divider()
    st.markdown("**Demo workspace**")
    st.success("Acme Corporation")
    st.markdown("**Connected sources**")
    st.markdown("- Snowflake employee records\n- Leave balances\n- Cortex Search policy knowledge")
    st.divider()
    st.markdown("**How it works**")
    st.caption("A LangGraph workflow routes each question to enterprise policy knowledge, structured data, or both.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("CortexFlow AI")
st.caption("Enterprise AI Assistant powered by Snowflake Cortex")

col1, col2, col3 = st.columns(3)
col1.metric("Knowledge sources", "4", "Policy documents")
col2.metric("Structured sources", "2", "Snowflake tables")
col3.metric("Orchestration", "LangGraph", "RAG + SQL")

st.markdown("#### Try a demo question")
examples = [
    "Hello!",
    "How many employees are there?",
    "What is the leave policy?",
    "How many leave days does Alice have and what is the carry forward policy?",
]
example_columns = st.columns(2)
for index, example in enumerate(examples):
    if example_columns[index % 2].button(example, key=f"example_{index}", use_container_width=True):
        st.session_state.pending_question = example

st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("intent"):
            st.caption(f"🧠 Route: {message['intent']}")

        if message.get("generated_sql"):
            with st.expander("🗄 Generated SQL"):
                st.code(message["generated_sql"], language="sql")

        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.write(source)

question = st.chat_input("Ask about policies, employees, leave, or travel expenses")
if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Consulting Snowflake Cortex..."):
            try:
                result = ask_cortexflow(question)
                st.markdown(result["answer"])

                # Show which LangGraph path was taken
                if result.get("intent"):
                    st.caption(f"🧠 Route: {result['intent']}")

                # Show generated SQL if available
                if result.get("generated_sql"):
                    with st.expander("🗄 Generated SQL"):
                        st.code(result["generated_sql"], language="sql")

                # Show retrieved documents
                if result["sources"]:
                    with st.expander("📄 Sources"):
                        for source in result["sources"]:
                            st.write(source)
                st.session_state.messages.append({"role": "assistant", "content": result["answer"], "sources": result["sources"],
                                            "intent": result.get("intent"), "generated_sql": result.get("generated_sql"),})
            except requests.RequestException as exc:
                st.error("Backend unavailable.")
                st.info("Please start the FastAPI server or configure " "CORTEXFLOW_API_URL.")
                st.caption(f"Connection detail: {exc}")
