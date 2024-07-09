import streamlit as st
import requests
import os, sys

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from utils import frontend_utils

# Set the page config
st.set_page_config(
    page_title="Nickles",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="auto",
)

frontend = frontend_utils.FrontEnd()

frontend.load_css(os.path.join(os.path.dirname(__file__), "static", "style.css"))

frontend.initialize_chat_history()

st.title("Nikles Chatbot")

frontend.display_chat_history()

prompt = st.chat_input("Ask me anything...")
if prompt:
    frontend.handle_user_input(prompt)

