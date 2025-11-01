# Bank of Maharashtra RAG Assistant

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** system that answers user questions about various **Bank of Maharashtra loan products** (Home Loan, Car Loan, Gold Loan, Personal Loan, etc.) using information scraped from the bank’s official website.

The system combines **web scraping**, **semantic embeddings**, **FAISS vector search**, and **a generative transformer model** to accurately retrieve and respond to user queries.


# Project Overview

The RAG assistant is designed to:
- Scrape and store relevant information from official Bank of Maharashtra web pages.
- Preprocess and chunk the scraped text data.
- Generate **vector embeddings** using a transformer-based sentence encoder.
- Store the embeddings in a **FAISS vector index** for efficient similarity search.
- Retrieve context relevant to a user’s query and use a **Flan-T5 model** to generate natural, concise answers.

Example questions:
- “What is the interest rate for a Bank of Maharashtra home loan?”
- “What is the processing fee for a car loan?”
- “What is the maximum tenure for a home loan?”
- “Does the bank provide gold loans?”

---

#  Tech Stack
- Language - Python 3.10+ 
- Web Scraping - `requests`, `BeautifulSoup` 
- Text Embedding - `sentence-transformers (all-MiniLM-L6-v2)` 
- Vector Database - `FAISS` 
- Model for Q&A - `google/flan-t5-base` 
- Libraries - `transformers`, `torch`, `langchain`, `numpy`, `pandas` 

---

# Folder Structure

bank_rag_project/
│
├── data/
│ ├── raw_data/ # Contains scraped JSON data from official pages
│ └── processed_data/ # Cleaned and combined data
│
├── embeddings/
│ ├── faiss_index.bin # Saved FAISS vector index
│ └── texts.pkl # Text chunks used for embedding
│
├── scripts/
│ ├── data_scrapping.py # Scrapes content from all target URLs
│ ├── clean_data.py # Cleans and merges scraped content
│ ├── vector_db.py # Creates embeddings & builds FAISS index
│ └── chatbot.py # RAG assistant script for Q&A
│
├── requirements.txt # All Python dependencies
└── README.md # Project documentation


## Setup Instructions

# 1. Clone the Repository
    - Open command terminal and enter the below git command
    - git clone https://github.com/<your-username>/bank_rag_project.git
    - then change the directory by using below command
        cd bank_rag_project

# 2. Create and Activate a Virtual Environment
    - Open Anaconda Prompt and the below commands
        - conda create -n rag_env python=3.10 -y
        - conda activate rag_env

# 3. Install Dependencies
    - Run the below command in conda prompt     
        - pip install -r requirements.txt

# 4. Scrape the data
    - Run the below command in conda prompt
        - python scripts/data_scrapping.py

# 5. Clean and Combine the Data
    - Run the below command in conda prompt
        - python scripts/clean_data.py

# 6. Generate Embeddings & Build FAISS Index
    - Run the below command in conda prompt
        - python scripts/vector_db.py

# 7. Run the RAG Chatbot
    - Run the below command in conda prompt
        - python scripts/chatbot.py

# 8. Ask the Chatbot about Bank of Maharashtra
    - “What is the interest rate for a Bank of Maharashtra home loan?”
    - “What is the processing fee for a car loan?”
    - “What is the maximum tenure for a home loan?”
    - “Does the bank provide gold loans?”
