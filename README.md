# azure_ragchain_chatbot

## Project Description

This project involves creating a chatbot that leverages data from multiple sources to provide information about products and related topics. The data sources include an SQL file, web-scraped data from a website, and a PDF document. The chatbot is built using OpenAI/Langchain, with a FAST API backend and a Streamlit frontend. 

## Features

- **Data Gathering**: Scrapes data from specified web pages, processes an SQL file, and extracts information from a PDF document.
- **Knowledge Base Creation**: Uses a vector database to create a searchable knowledge base.
- **Chatbot**: Implemented with OpenAI/Langchain for natural language processing.
- **Backend**: FAST API used for handling API requests.
- **Frontend**: Streamlit application for user interaction.

## Interface 
![Screenshot 2024-06-12 190323](https://github.com/khair-bs23/nikles_llm_chatbot/assets/167753101/a7705f4e-ec88-4ec6-8edd-0be6b3430d7b)
![Screenshot 2024-06-12 190338](https://github.com/khair-bs23/nikles_llm_chatbot/assets/167753101/07e55ec9-bdbd-4158-b757-507dc904b7ce)


## Setup Instructions

### Prerequisites

- Python 3.8+
- Git
- Virtual Environment (optional but recommended)

### Installation

1. **Clone the Repository**
   
   ```sh
   git clone https://github.com/yourusername/knowledge_base_chatbot.git
   cd knowledge_base_chatbot
   ```
3. **Create and Activate Virtual Environment**
   
    ```sh
    python -m venv venv
    venv/Scripts/activate  # On linux use `venv\bin\activate`
    ```
    
3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```
4. **Setup Environment Variables**
Create a .env file in the root directory and add necessary environment variables as per your setup.

    ```sh
    touch .env
    # Add your environment variables in the .env file
    ```
    
### Running the Application
1. Run the Backend (FAST API)
   
    ```sh
    Copy code
    uvicorn api.main:app --reload
    ```
    
3. Run the Frontend (Streamlit)
   
    ```sh
    streamlit run src/frontend/main.py
    ```

### Scraping Data
Before running the application, ensure to scrape the data from the required web pages and process the SQL and PDF data.

1. Scrape Web Data
   ```sh
   python utils/scrapper.py
   ```
2. Load PDF and SQL database in the data folder

### Environment Variables
Ensure to set up the following environment variables in your .env file:

DB_URI: URI for the vector database
OPENAI_API_KEY: API key for OpenAI

### Requirements
List of Python packages required for the project, as specified in requirements.txt.

### Gitignore
The .gitignore file is configured to exclude:
Virtual environment folders
Environment variable files (.env)
Compiled python files (__pycache__, .pyc, etc.)
Data files (SQL)



