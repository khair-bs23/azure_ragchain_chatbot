import requests
import streamlit as st
import os



class FrontEnd:
    def __init__(self) -> None:
        self.API_URL = "http://localhost:8000/ask"


    def load_css(self, file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def initialize_chat_history(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "bot", "content": "Hello, how can I help you today?"}]

    def display_chat_history(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(f'<span style="color:white">{message["content"]}</span>', unsafe_allow_html=True)

    def handle_user_input(self, prompt, session_id="123"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<span style="color:white">{prompt}</span>', unsafe_allow_html=True)

        payload = {
            "question": prompt,
            "session_id": session_id
        }
        response = requests.post(self.API_URL, json=payload)
        
        if response.status_code == 200:
            bot_response = response.json().get("response")
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            with st.chat_message("bot"):
                st.markdown(f'<span style="color:white">{bot_response}</span>', unsafe_allow_html=True)
        else:
            st.session_state.messages.append({"role": "bot", "content": f"Error: {response.status_code}"})
            with st.chat_message("bot"):
                st.markdown(f'<span style="color:white">Error: {response.status_code}</span>', unsafe_allow_html=True)
