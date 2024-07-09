from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import  create_history_aware_retriever, create_retrieval_chain
from langchain_community.embeddings import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import sys, os
import pickle
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app import main
from models import  prompt_template
print(os.path.abspath(__file__))

class PDFHandler(main.Chatbot):
    def __init__(self) -> None:
        super().__init__()
        api_key_path = "../.env" 
        load_dotenv(api_key_path) 

        self.embeddings = AzureOpenAIEmbeddings(
                openai_api_version= os.getenv("AZURE_OPENAI_API_VERSION"),
                openai_api_type= os.getenv("AZURE_OPENAI_API_TYPE"),
                openai_api_key= os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
                azure_deployment=os.getenv("EMBEDDINGS_MODEL"),
                # max_retries=max_retries,
                # retry_min_seconds=retry_min_seconds,
                # retry_max_seconds=retry_max_seconds,
                # chunk_size=embeddings_chunk_size,
                # timeout=timeout,
            )
        # self.all_pdf_data = self.pdf_loader("../data/nikles_data_report.pdf", "../data/Warranty.pdf")
        # self.processed_data_retriver = self.processing() 

        self.vectorstore_path = "../utils/vectorstore/" 
        if os.path.exists(self.vectorstore_path): 
            self.processed_data_retriever = self.load_vectorstore()  
        else: 
            self.all_pdf_data = self.pdf_loader("../data/nikles_data_report.pdf") 
            self.processed_data_retriever = self.processing() 
 
    def pdf_loader(self, file_path): 
        try:  
            loader = PyPDFLoader(file_path) 
            docs = loader.load() 

        except Exception as e: 
            logging.log(f"pdf file didn't load properly {e}") 
        return docs 

    def processing(self): 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
        splits = text_splitter.split_documents(self.all_pdf_data) 

        
        vectorstore = Chroma.from_documents(documents=splits, embedding = self.embeddings, persist_directory = self.vectorstore_path)
        vectorstore.persist()
        retriever = vectorstore.as_retriever()
        return retriever
    
    def load_vectorstore(self):
        vectorstore = Chroma(persist_directory=self.vectorstore_path, embedding_function=self.embeddings)
        retriever = vectorstore.as_retriever()
        return retriever

    def pdf_chain(self):
        question_answer_chain = create_stuff_documents_chain(self.client, prompt_template.pdf_generation_prompt)
        history_aware_retriever = create_history_aware_retriever(
                                    self.client, self.processed_data_retriever, 
                                    prompt_template.pdf_reformulated_question_generation_template
                                )
        pdf_rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        return pdf_rag_chain
    
    
    def pdf_response(self, question, chat_history, session_id):
        pdf_chain = self.pdf_chain()
        response = pdf_chain.invoke(
                {"input": question, "chat_history": chat_history},
                config={"configurable": {"session_id": session_id}}
            )["answer"]
        return response

