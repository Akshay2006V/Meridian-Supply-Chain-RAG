\# Meridian Supply Chain RAG



A local Retrieval-Augmented Generation (RAG) application for querying Meridian Components' supply-chain and procurement documents.



\## Overview



Meridian Supply Chain RAG provides grounded answers to questions about supplier performance, procurement policy, purchasing, quality, delivery, inventory, and related information contained in the indexed Meridian documents.



The system runs locally using Ollama and does not require an OpenAI API key.



\## Features



\- Retrieval-Augmented Generation (RAG)

\- Local Qwen3 4B language model

\- Nomic Embed Text embeddings

\- ChromaDB vector database

\- PDF document parsing with PyPDF

\- Streamlit web interface

\- Grounded document-only answers

\- Deterministic answers for common factual queries

\- Explicit refusal for unsupported questions

\- Automated RAG test suite



\## Technology Stack



\- Python

\- Ollama

\- Qwen3 4B

\- Nomic Embed Text

\- ChromaDB

\- PyPDF

\- LangChain Text Splitters

\- Streamlit



\## Project Structure



```text

supplychain-rag/

├── app.py

├── rag.py

├── ingest.py

├── test\_rag.py

├── requirements.txt

├── README.md

├── .env.example

├── .gitignore

└── data/

&#x20;   ├── Meridian\_Procurement\_Policy\_Handbook\_v4.2.pdf

&#x20;   └── Meridian\_Supply\_Chain\_Review\_Q1\_FY2025-26.pdf

```



\## Setup



\### 1. Create the virtual environment



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 2. Install dependencies



```powershell

pip install -r requirements.txt

```



\### 3. Install the Ollama models



```powershell

ollama pull qwen3:4b

ollama pull nomic-embed-text

```



\### 4. Build the document index



```powershell

python ingest.py

```



\### 5. Start the application



```powershell

streamlit run app.py

```



Open:



```text

http://localhost:8501

```



\## Automated Testing



Run:



```powershell

python test\_rag.py

```



The test suite validates:



1\. Highest-spend supplier identification

2\. Line stoppages and downtime

3\. Purchase-order approval authority

4\. Supplier classification

5\. Safety-stock calculation

6\. Unsupported-question handling



The validated test suite currently passes all six tests.



\## Example Questions



\### Supplier Performance



> Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?



\### Line Stoppages



> How many line stoppages happened in Q1, what was the total downtime, and what caused them?



\### Procurement Approval



> What is the approval authority for a purchase order worth ₹1.4 crore?



\### Supplier Classification



> What are the four supplier classification categories, and what qualifies a supplier as Critical?



\### Safety Stock



> Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?



\### Unsupported Information



> What is the annual salary of the Head of Procurement?



The final question demonstrates grounded-answer behavior: when the supplied documents do not contain the requested information, the system refuses to invent an answer.



\## Local Operation



The project is designed to run locally with Ollama and does not require an external OpenAI API key.



\## Notes



\- `.venv/` is excluded from version control.

\- `chroma\_db/` is generated locally and excluded from version control.

\- `.env` is excluded from version control.

\- The documents in `data/` form the knowledge base for the RAG system.



\## Assignment



This project was developed as part of the HCLTech × Economic Times AI Masterclass assignment.

