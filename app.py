import streamlit as st
from google import genai
from google.genai import types

st.title("My AI Assistant")

if "chat" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    rules = "You are a helpful assistant. You are chatting with a visitor. Be friendly and clear."
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-3.5-flash-lite", config=types.GenerateContentConfig(system_instruction=rules))
    st.session_state.msgs = []

for m in st.session_state.msgs:
    st.chat_message(m["role"]).write(m["text"])

q = st.chat_input("Ask me anything")
if q:
    st.chat_message("user").write(q)
    a = st.session_state.chat.send_message(q).text
    st.chat_message("assistant").write(a)
    st.session_state.msgs.append({"role": "user", "text": q})
    st.session_state.msgs.append({"role": "assistant", "text": a})