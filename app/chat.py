import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from models import pdf_ragchain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

class Chat():
    store = {}
    def __init__(self, question, session_id, client, embeddings) -> None:
        # super().__init__()
        self.question = question
        # self.store = {}
        self.session_id = session_id
        self.client = client
        self.embeddings = embeddings
    
    def get_session_history(self) -> BaseChatMessageHistory:
        if self.session_id not in Chat.store:
            print(f"Creating new history for session: {self.session_id}")
            Chat.store[self.session_id] = ChatMessageHistory()
        else:
            print(f"Using existing history for session: {self.session_id}")
        return Chat.store[self.session_id]

    def process_question(self):
        chat_history = self.get_session_history()
        pdf_handler = pdf_ragchain.PDFHandler(self.client, self.embeddings)
        print('X')
        response = pdf_handler.pdf_response(self.question, chat_history.messages, self.session_id)
        # update chat history
        chat_history.add_message(HumanMessage(content=self.question))
        chat_history.add_message(AIMessage(content=response))

        print(chat_history)
        print(response)
        return response

