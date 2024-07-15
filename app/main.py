import os 
import sys
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import AzureChatOpenAI, AzureOpenAI

from langchain_community.embeddings import AzureOpenAIEmbeddings
from app import chat
import uvicorn

class Chatbot:
    def __init__(self) -> None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_key_path = os.path.join(script_dir, '../.env')
        load_dotenv(api_key_path)

    def connect_api(self):
        # client = AzureChatOpenAI(
        #         api_key = os.getenv("AZURE_OPENAI_API_KEY"), 
        #         api_version = os.getenv("AZURE_OPENAI_API_VERSION"), 
        #         azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE") 
        #         )
        try: 
            client = AzureChatOpenAI(model=os.getenv('DEPLOYMENT_MODEL'), 
                       api_version=os.getenv('AZURE_OPENAI_API_VERSION'), 
                       azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE"), 
                       temperature = 0
                       
                    #    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
                       )
        except Exception as e:
            print("Client Error ")
            print(e)
        return client

    def connect_embeddings(self):
        try:
            embeddings = AzureOpenAIEmbeddings(
                openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
                openai_api_type=os.getenv("AZURE_OPENAI_API_TYPE"),
                openai_api_key= os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
                azure_deployment=os.getenv("EMBEDDINGS_MODEL"),
                # max_retries=max_retries,
                # retry_min_seconds=retry_min_seconds,
                # retry_max_seconds=retry_max_seconds,
                # chunk_size=embeddings_chunk_size,
                # timeout=timeout,
            )
        except Exception as e:
            print(e)
        return embeddings

    def get_llm(self):
        return self.client

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str
    session_id: str


@app.post("/ask")   
def ask_question(request: QuestionRequest): 
    try: 
        connection = Chatbot() 
        embeddings = connection.connect_embeddings() 
        client = connection.connect_api() 

        chatting_instance = chat.Chat(request.question, session_id=request.session_id, client=client, embeddings=embeddings) 
        response = chatting_instance.process_question() 
        return {"response": response} 
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e)) 

# Run the app using uvicorn 
if __name__ == '__main__': 
    uvicorn.run(app, host="0.0.0.0", port=8000) 