import streamlit as st
from google import genai
from google.genai import types

st.title("My AI Assistant")

if "chat" not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    rules = "You are the AI assistant of Saipavan Gunti. Answer questions about him using only this profile. If something is not in the profile, say you don't know. You can also help with general questions. Profile: " + open("profile.txt").read()
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