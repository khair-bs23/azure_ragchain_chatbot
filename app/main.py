import os 
import sys
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI
from langchain_community.embeddings import AzureOpenAIEmbeddings
import chat
import uvicorn

class Chatbot:
    def __init__(self) -> None:
        api_key_path = "../.env"
        load_dotenv(api_key_path)
        self.client = self.connect_api()

    def connect_api(self):
        # client = AzureChatOpenAI(
        #         api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        #         api_version = os.getenv("AZURE_OPENAI_API_VERSION"), 
        #         azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE")
        #         )
        client = AzureChatOpenAI(model=os.getenv('DEPLOYMENT_MODEL'),
                       api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
                       azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE"))
        return client

    def get_llm(self):
        return self.client

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str
    session_id: str



@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        chatting_instance = chat.Chat(request.question, session_id=request.session_id)
        response = chatting_instance.process_question()
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app using uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)