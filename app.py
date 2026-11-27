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
    rules = "You are the AI assistant of Saipavan Gunti. Answer questions about him using this profile. Also answer any other questions helpfully. Profile: " + open("profile.txt").read()
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-3.5-flash-lite", config=types.GenerateContentConfig(system_instruction=rules))
    st.session_state.msgs = []

for m in st.session_state.msgs:
    st.chat_message(m["role"]).write(m["text"])

st.sidebar.markdown("---")
st.sidebar.markdown("*Try asking:*")
if st.sidebar.button("What are Saipavan's projects?"):
    st.session_state.picked = "What are Saipavan's projects?"
if st.sidebar.button("What skills does he have?"):
    st.session_state.picked = "What skills does he have?"
if st.sidebar.button("Tell me about his published paper"):
    st.session_state.picked = "Tell me about his published paper"

q = st.chat_input("Ask me anything")
if not q and "picked" in st.session_state:
    q = st.session_state["picked"]
    del st.session_state["picked"]
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
        a = "Please send your question again"
    st.chat_message("assistant").write(a)
    st.session_state.msgs.append({"role": "user", "text": q})
    st.session_state.msgs.append({"role": "assistant", "text": a})
    st.sidebar.markdown("---")
    st.sidebar.markdown("*Connect with me*")
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/saipavan-gunti-698310367/)")
    st.sidebar.markdown("[GitHub](https://github.com/Saipavan0409)")
    st.sidebar.markdown("Email: saipavangunti0409@gmail.com")