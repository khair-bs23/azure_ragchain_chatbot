from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os 

pdf_reformulated_question_generation_template = ChatPromptTemplate.from_messages(
      [
        ("system", (
              "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question which can be understood "
                "without the chat history. Do NOT answer the question, "
                "just reformulate it if needed and otherwise return it as is."
        )),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


pdf_generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", (
                    """
                        You are an assistant for answering the questions from the retrived context.
                        Use the following pieces of retrieved context to answer 
                        the question. If you don't know the answer, say that you
                        don't know. Please don't make up anything on your own knowledgebase.
                        Use six sentences maximum and keep the 
                        answer concise.
                        \n\n
                        {context}
                    """
                )
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

    