import streamlit as st
import time
import json
import requests
import os
from utils import extract_text_from_pdf, chunk_text, get_relevant_chunks

# Page configuration
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for better UI
st.markdown("""
<style>
.stTextInput>div>div>input {
    background-color: #f0f2f6;
}
.system-info {
    padding: 0.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    background-color: #f8f9fa;
    border-left: 3px solid #4CAF50;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []

# Default Ollama host
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Function to check if Ollama is running
def check_ollama_server():
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


# Function to send message to Ollama
def send_message(message, model="qwen2.5:0.5b"):
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "stream": True
            },
            stream=True,
            timeout=60
        )

        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        chunk = data.get("message", {}).get("content", "")
                        full_response += chunk
                    except json.JSONDecodeError:
                        continue  # Skip lines that are not valid JSON
            return full_response.strip() if full_response else "⚠️ No response received from model."
        else:
            return f"❌ Error: HTTP {response.status_code} - {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"🚫 Connection error: {str(e)}"

# Sidebar
with st.sidebar:
    st.title("Chatbot")

    # Server status
    st.subheader("Server Status")
    server_status = check_ollama_server()
    if server_status:
        st.success("✅ Connected to Ollama server")
    else:
        st.error("❌ Cannot connect to Ollama server")
        st.info("""
        Make sure Ollama is running. Start it with:
        ```
        ollama serve
        ```
        """)



    # PDF upload
    st.subheader("PDF Upload")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            full_text = extract_text_from_pdf(uploaded_file)
            st.session_state.pdf_chunks = chunk_text(full_text)
        st.success("✅ PDF processed and ready!")

    if st.button("Clear Chat History", key="clear"):
        st.session_state.messages = []
        st.session_state.pdf_chunks = []
        st.rerun()

# Main chat interface
st.title("Chatbot")

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Send a message...")

# Process user input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare prompt
    if st.session_state.pdf_chunks:
        relevant = get_relevant_chunks(prompt, st.session_state.pdf_chunks, top_k=4)
        context = "\n\n".join(relevant)
        full_prompt = f"You are a helpful assistant. Use the following PDF context if relevant.\n\nPDF Context:\n{context}\n\nUser Question: {prompt}"
    else:
        full_prompt = f"You are a helpful assistant. Answer the question below.\n\nUser Question: {prompt}"

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            selected_model = st.session_state.get("selected_model", "qwen2.5:0.5b")
            response = send_message(full_prompt, selected_model)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

if not st.session_state.messages:
    st.info("👋 Hello! I'm your assistant. Ask me anything!")
