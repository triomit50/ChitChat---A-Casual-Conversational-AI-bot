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

## #Title of the app
st.title("CHITCHAT- A chatbot based on Llama 3.1")


## MAin interface for user input
st.write("Go ahead and engage in a chit-chat :)")
user_input=st.text_input("Your input:")



if user_input :
    response=generate_response(user_input)
    st.write(response)
else:
    st.write("Please provide the user input")


