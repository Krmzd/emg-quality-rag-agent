import uuid
import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000/chat")

st.title("EMG Quality & Research Assistant")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about EMG reporting, the dataset, or check a recording...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.spinner("Thinking..."):
        response = requests.post(
            API_URL,
            json={"message": question, "thread_id": st.session_state.thread_id},
            timeout=120,
        )
    answer = response.json()["answer"]

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)