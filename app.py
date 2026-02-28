# importing libraries for env variables
import os
import dotenv
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
import streamlit as st


# loading the env variables
load_dotenv()

# loading variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# using Groq model
from langchain_groq import ChatGroq
model = ChatGroq(model = "llama-3.1-8b-instant")


# prompt template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
system_prompt = (
    "Act as an assistant. Answer each and every question with details. "
)

# setting up the chat template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}")
    ]
)

# parsing function for the output
output_parser = StrOutputParser()

# base chain
base_lcel_chain = prompt|model|output_parser

# initializing session store under streamlit
if "store" not in st.session_state:
    st.session_state.store={}               # basically --> store = {}

if "session_id" not in st.session_state:
    st.session_state.session_id = "chat_1"      # basically --> session_id = "chat_1"

# loops -> sessions -> refresh -> stored and closed

# function for storing chat history
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

# function for generating answer
def generate_response(input: str):
    # configuration of the session and chats
    config1 = {"configurable":{"session_id":st.session_state.session_id}}
    # wrapping the base chain with chat history
    chain_with_history = RunnableWithMessageHistory(
    base_lcel_chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"

    )

# getting the answer stored --> response
    answer = chain_with_history.invoke(
            {"input":input},
            config=config1

    )

    return answer

# ---------- App dev ------------

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Chat container */
    .chat-container {
        background: transparent;  /* or your page background color */
        border: 2px dashed #e5e7eb;  /* Optional: subtle border when empty */
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        min-height: 0;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* User message bubble */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: auto;
        max-width: 70%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        word-wrap: break-word;
    }
    
    /* Assistant message bubble */
    .assistant-message {
        background: white;
        color: #1f2937;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: auto;
        max-width: 70%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        word-wrap: break-word;
    }
    
    /* Input area styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        border: 2px solid #e5e7eb;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="CHITCHAT - AI Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h2 style='color: #667eea; margin-bottom: 1rem;'>💬 CHITCHAT</h2>
            <p style='color: #6b7280;'>Powered by Llama 3.1</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.markdown("""
        - **AI-Powered Conversations**
        - **Context-Aware Responses**
        - **Session Management**
        - **LangSmith Tracing**
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Session Info")
    st.info(f"Session ID: `{st.session_state.session_id}`")
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.session_id = f"chat_{len(st.session_state.store) + 1}"
        st.rerun()

# Main content
st.markdown("""
    <h1>💬 CHITCHAT</h1>
    <p class="subtitle">An Enhanced AI Chatbot Powered by Llama 3.1</p>
    <p class="subtitle">made by Trio Mit.</p>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.messages:
        st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #9ca3af;'>
                <h3>👋 Welcome to CHITCHAT!</h3>
                <p>Start a conversation by typing a message below.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message"><strong>Assistant:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_input(
        "Type your message here...",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Ask me anything..."
    )

with col2:
    send_button = st.button("Send 🚀", use_container_width=True, type="primary")

# Process user input
if send_button and user_input:
    if user_input.strip():
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            response = generate_response(user_input)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear input and rerun to update the chat display
        st.rerun()
