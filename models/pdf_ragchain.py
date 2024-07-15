from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import  create_history_aware_retriever, create_retrieval_chain
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import sys, os
import pickle
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app import main
from models import  prompt_template
print(os.path.abspath(__file__))

class PDFHandler():
    def __init__(self, client, embeddings) -> None:
        # super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.join(script_dir, '../')
        load_dotenv(root_path+'.env')
        self.client = client
        self.embeddings = embeddings     
    
        # self.all_pdf_data = self.pdf_loader("../data/nikles_data_report.pdf", "../data/Warranty.pdf")
        # self.processed_data_retriver = self.processing() 

        self.vectorstore_path = root_path+"utils/vectorstore/" 
        # if os.path.exists(self.vectorstore_path): 
        #     self.processed_data_retriever = self.load_vectorstore()  
        # else: 
        self.all_pdf_data = self.pdf_loader(root_path+"data/nikles_data_report.pdf") 
        self.processed_data_retriever = self.processing() 


    def pdf_loader(self, file_path): 
        try:  
            loader = PyPDFLoader(file_path) 
            docs = loader.load() 

        except Exception as e: 
            logging.log(msg=f"pdf file didn't load properly {e}", level=2) 
        return docs 

    def processing(self): 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
        splits = text_splitter.split_documents(self.all_pdf_data) 
        
        vectorstore = Chroma.from_documents(documents=splits, embedding = self.embeddings)
        # vectorstore.persist() 
        retriever = vectorstore.as_retriever()
        return retriever

    def load_vectorstore(self):
        vectorstore = Chroma(persist_directory=self.vectorstore_path, embedding_function=self.embeddings)
        retriever = vectorstore.as_retriever()
        return retriever

    def validate_retriever(self, question, chat_history):
    # Use the history-aware retriever directly to fetch relevant documents
        print("Validaing Retriever.....")
        history_aware_retriever = create_history_aware_retriever(
            self.client,
            self.processed_data_retriever,
            prompt_template.pdf_reformulated_question_generation_template
        )
  
        # Retrieve relevant documents for the given question
     
        retrieved_docs = history_aware_retriever.invoke({"input": question, "chat_history": chat_history}) 
        # for idx, doc in enumerate(retrieved_docs): 
        #     print(f"Document {idx + 1}:\n{doc['content']}\n") 
        for doc in retrieved_docs:
            print(doc.page_content)
            print('\n \n')
                
   
        
        # Inspect the retrieved documents
        
        # print("History")
    def pdf_chain(self):


    
        try:
            history_aware_retriever = create_history_aware_retriever( 
                                    self.client, self.processed_data_retriever, 
                                    prompt_template.pdf_reformulated_question_generation_template 
                                ) 
        
            question_answer_chain = create_stuff_documents_chain(self.client, prompt_template.pdf_generation_prompt)
            # question_answer_chain.invoke({"context":history_aware_retriever})
            # print(prompt_template.pdf_generation_prompt)
            pdf_rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        except Exception as e:
            print("chain completion error", e)

        return pdf_rag_chain


    def pdf_response(self, question, chat_history, session_id): 
        pdf_chain = self.pdf_chain()
        print("Validating Retriever:")
        # self.validate_retriever(question, chat_history)

        
        try:
            response = pdf_chain.invoke(
                {"input": question, "chat_history": chat_history},
                config={"configurable": {"session_id": session_id}}
            )["answer"]
        except Exception as e:
            logging.error(f"Error during PDF chain invocation: {e}")
            raise
    
        return response
      

