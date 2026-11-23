import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

st.set_page_config(page_title="Saipavan's AI Assistant", page_icon="🤖")
st.title("🤖 Saipavan's AI Assistant")
st.caption("Ask me about Saipavan's skills and projects, or upload a PDF on the left.")
if not st.user.is_logged_in:
    st.info("Please sign in to use the assistant.")
    st.button("Sign in with Google", on_click=st.login)
    st.stop()
print("VISITOR:", st.user.email, st.user.name, flush=True)

pdf_text = ""
f = st.sidebar.file_uploader("Upload a PDF (optional)", type="pdf")
if f:
    pdf_text = "\n".join((p.extract_text() or "") for p in PdfReader(f).pages)[:20000]
    st.sidebar.success("PDF loaded")

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
    msg = q
    if pdf_text:
        msg = "Answer using this uploaded document.\nDocument:\n" + pdf_text + "\n\nQuestion: " + q
    import time
    a = None
    for i in range(8):
        try:
            a = st.session_state.chat.send_message(msg).text
            break
        except Exception as e:
            time.sleep(2)
    if not a:
        a = "The AI is busy right now. Please try again in a minute."
    st.chat_message("assistant").write(a)
    st.session_state.msgs.append({"role": "user", "text": q})
    st.session_state.msgs.append({"role": "assistant", "text": a})