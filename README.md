# 🚀 Meridian Supply Chain RAG

<p align="center">
  <strong>Grounded AI for Supply-Chain & Procurement Intelligence</strong>
</p>

<p align="center">
  A local Retrieval-Augmented Generation (RAG) assistant that transforms enterprise supply-chain documents into fast, evidence-based answers.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-black?style=for-the-badge)
![Qwen](https://img.shields.io/badge/Qwen3-4B-7C3AED?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-FF6F00?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

</p>

---

## 📌 Project Overview

**Meridian Supply Chain RAG** is a locally running AI-powered document intelligence system designed to answer questions about supplier performance, procurement policy, delivery, quality, inventory, purchasing, and supply-chain operations.

Instead of searching through lengthy PDF documents manually, users can ask natural-language questions and receive concise, grounded answers derived from the indexed Meridian Components documents.

The system is intentionally designed around one principle:

> **Retrieve the evidence first. Answer only from the evidence. Never invent information that is not present in the supplied documents.**

---

## 🎯 Problem Statement

Supply-chain and procurement teams frequently work with large collections of operational documents containing:

- Supplier performance metrics
- Procurement policies
- Purchase-order approval rules
- Delivery performance
- Quality and defect information
- Safety-stock requirements
- Production interruptions
- Supplier risks
- Operational events

Traditional document search makes it difficult to connect information across different documents.

For example:

> **Kaveri Metals reported 88.1% on-time delivery and 1,150 PPM defects. What procurement-policy consequences apply?**

Answering this requires combining:

1. Supplier performance information from the supply-chain review
2. Thresholds and consequences from the procurement policy

This project demonstrates how RAG can convert those documents into an interactive enterprise knowledge system.

---

## 💡 Solution

The application combines:

**PDF ingestion → text extraction → chunking → embeddings → semantic retrieval → grounded answer extraction → LLM fallback**

The result is a lightweight local AI assistant that can answer supply-chain questions without sending the documents to an external AI API.

---

# 🧠 System Architecture

```text
                    ┌───────────────────────────┐
                    │       User Question       │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │     Query Embedding       │
                    │   Nomic Embed Text        │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │        ChromaDB            │
                    │   Semantic Vector Search   │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │   Retrieved PDF Chunks    │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌─────────────────────┐    ┌─────────────────────┐
          │ Deterministic       │    │ Qwen3 4B            │
          │ Answer Extraction   │    │ LLM Fallback        │
          └──────────┬──────────┘    └──────────┬──────────┘
                     │                          │
                     └────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       Grounded Answer     │
                    └───────────────────────────┘
```

---

# 🔄 RAG Workflow

### 1. Document Ingestion

The project processes the supplied Meridian PDF documents using `PyPDF`.

### 2. Text Chunking

Extracted document text is split into smaller chunks using LangChain text splitters.

### 3. Embedding Generation

Each chunk is converted into a vector representation using:

```text
nomic-embed-text
```

### 4. Vector Storage

Embeddings and their metadata are stored in:

```text
ChromaDB
```

The vector database is persisted locally.

### 5. Query Retrieval

When a user enters a question:

```text
Question
   ↓
Embedding
   ↓
ChromaDB semantic search
   ↓
Relevant document chunks
```

### 6. Grounded Answer Generation

The system first uses deterministic extraction for common factual questions.

For questions that require additional synthesis, the system can fall back to:

```text
Qwen3 4B
```

### 7. Unsupported Information Handling

If the requested information is not available in the supplied documents, the system refuses to fabricate an answer.

Example:

```text
User:
What is the annual salary of the Head of Procurement?

System:
I cannot answer that from the supplied documents.
```

This is a deliberate design choice to reduce hallucination.

---

# ⭐ Key Features

## 📄 PDF-Based Knowledge Base

The current knowledge base contains:

```text
Meridian_Procurement_Policy_Handbook_v4.2.pdf
Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
```

---

## 🔎 Semantic Search

Questions are converted into embeddings and matched against the indexed document chunks using ChromaDB.

This allows the system to understand semantic similarity rather than relying only on exact keyword matching.

---

## 🏭 Supply-Chain Intelligence

The assistant can answer questions involving:

- Supplier performance
- Supplier spend
- Delivery performance
- Quality metrics
- Defect rates
- Procurement rules
- Approval authority
- Safety stock
- Line stoppages
- Supplier classification
- Supply-chain risks

---

## 🧾 Procurement Policy Reasoning

The system can connect operational performance with procurement-policy rules.

For example:

```text
Supplier performance
        +
Procurement policy
        ↓
Applicable policy consequence
```

This allows questions that require information from multiple document sections.

---

## 🚫 Hallucination Resistance

The application intentionally avoids making unsupported claims.

For example:

```text
Question:
What is the annual salary of the Head of Procurement?

Answer:
I cannot answer that from the supplied documents.
```

The goal is not to answer every question.

The goal is to answer **only answerable questions reliably**.

---

## ⚡ Fast Local Execution

The application is designed to operate locally using Ollama.

This removes the dependency on external paid LLM APIs for the core workflow.

---

# 🧪 Automated Validation

The project includes an automated test suite:

```text
test_rag.py
```

The test suite validates six representative scenarios.

| Test | Scenario |
|---|---|
| 1 | Highest-spend supplier |
| 2 | Line stoppages and downtime |
| 3 | Purchase-order approval |
| 4 | Critical supplier classification |
| 5 | Safety-stock calculation |
| 6 | Unsupported question handling |

### Validation Result

```text
============================================================
MERIDIAN RAG AUTOMATED TESTS
============================================================

Passed: 6
Failed: 0
Total : 6

RESULT: ALL TESTS PASSED
```

The test suite was used during development to verify retrieval, grounded answers, policy reasoning, and unsupported-question handling.

---

# 💬 Example Questions

## Supplier Performance

> Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?

### Expected Answer

```text
Shenzhen Rui Electronics had the highest Q1 spend at
₹21.9 crore, with 79.5% on-time delivery.
```

---

## Line Stoppages

> How many line stoppages happened in Q1, what was the total downtime, and what caused them?

### Expected Answer

```text
Seven line-stoppage events occurred in Q1, totaling
41 hours of downtime.

The causes included:
• Four microcontroller shortages involving
  Shenzhen Rui Electronics
• Two PCB lots rejected at incoming inspection
  from Trident Circuit Boards
• One transporter strike in the Coimbatore–Pune corridor
```

---

## Procurement Approval

> What is the approval authority for a purchase order worth ₹1.4 crore?

### Expected Answer

```text
The approval authority is the Chief Operating Officer.
```

---

## Supplier Classification

> What are the four supplier classification categories, and what qualifies a supplier as Critical?

### Expected Answer

```text
The four categories are:

• Critical
• Strategic
• Standard
• Tail

A supplier is classified as Critical if it is:
• Single-source for any part
• Above ₹10 crore annual spend
• Supplying a safety-related component
```

---

## Safety Stock

> Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?

### Expected Answer

```text
The required safety stock is 30 days.
```

---

## Unsupported Information

> What is the annual salary of the Head of Procurement?

### Expected Behavior

```text
I cannot answer that from the supplied documents.
```

---

# 🖥️ Application Interface

The project provides a Streamlit-based interface designed around three primary areas:

### Ask Meridian

Natural-language questions can be entered directly into the interface.

### Answer

The generated answer is presented in a clean, readable response area.

### Sources

The application displays the retrieved document and page information used by the RAG pipeline.

---

# 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM Runtime | Ollama |
| Language Model | Qwen3 4B |
| Embedding Model | Nomic Embed Text |
| Vector Database | ChromaDB |
| PDF Parser | PyPDF |
| Text Splitting | LangChain Text Splitters |
| Web Interface | Streamlit |
| Version Control | Git + GitHub |

---

# 📁 Project Structure

```text
supplychain-rag/
│
├── app.py
│   └── Streamlit user interface
│
├── rag.py
│   └── Retrieval and answer-generation pipeline
│
├── ingest.py
│   └── PDF ingestion and ChromaDB indexing
│
├── test_rag.py
│   └── Automated RAG validation tests
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
├── .env.example
│   └── Example local configuration
│
├── .gitignore
│   └── Git exclusions
│
└── data/
    ├── Meridian_Procurement_Policy_Handbook_v4.2.pdf
    └── Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
```

---

# ⚙️ Installation & Setup

## Prerequisites

Install:

- Python
- Git
- Ollama

Verify:

```powershell
python --version
git --version
ollama --version
```

---

## 1. Clone the Repository

```powershell
git clone https://github.com/Akshay2006V/Meridian-Supply-Chain-RAG.git
cd Meridian-Supply-Chain-RAG
```

---

## 2. Create the Virtual Environment

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Install Ollama Models

```powershell
ollama pull qwen3:4b
ollama pull nomic-embed-text
```

Verify:

```powershell
ollama list
```

---

## 5. Ingest Documents

Build the local ChromaDB index:

```powershell
python ingest.py
```

The ingestion process:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding
 ↓
ChromaDB
```

---

## 6. Run the CLI RAG

```powershell
python rag.py
```

Example:

```text
Enter your question:
What is the approval authority for a purchase order worth ₹1.4 crore?
```

---

## 7. Run the Streamlit Application

```powershell
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 🧪 Running the Tests

Run the complete automated validation suite:

```powershell
python test_rag.py
```

Successful validation:

```text
Passed: 6
Failed: 0
Total : 6
```

---

# 🔐 Privacy & Local Execution

The project is designed for local execution.

The core AI workflow uses:

```text
Ollama
↓
Local models
↓
Local embeddings
↓
Local ChromaDB
```

No OpenAI API key is required.

The `.env` file is excluded from Git version control.

The generated ChromaDB directory is also excluded from version control.

---

# 🧠 Design Principles

## 1. Grounded Answers

The system should answer from the supplied documents rather than general world knowledge.

## 2. Evidence Before Generation

Relevant document content is retrieved before an answer is produced.

## 3. Exact Information Preservation

Important names, numbers, units, suppliers, and policy thresholds should be preserved.

## 4. Unsupported Questions Should Be Rejected

A confident answer is worse than an explicit:

```text
I cannot answer that from the supplied documents.
```

when the evidence is unavailable.

## 5. Local-First AI

The project demonstrates that useful enterprise document intelligence can be implemented using local models and local vector storage.

---

# 📈 Why This Project Matters

Supply-chain decisions often depend on connecting multiple pieces of information:

```text
Supplier Performance
        +
Procurement Policy
        +
Quality
        +
Delivery
        +
Inventory Risk
        ↓
Operational Decision
```

This project demonstrates how RAG can act as an interface between those documents and the person making the decision.

Instead of manually searching through pages of operational reports and policy documents, users can ask direct questions in natural language.

---

# 🎓 Learning Outcomes

This project provided hands-on experience with:

- Retrieval-Augmented Generation
- Semantic search
- Vector databases
- Embeddings
- Local LLM deployment
- PDF document processing
- Prompt design
- Grounding and hallucination control
- Automated testing
- Streamlit application development
- Git and GitHub workflow

Most importantly, the project demonstrates the difference between:

```text
Generating an answer
```

and:

```text
Generating an answer supported by evidence
```

---

# 🚧 Current Limitations

The current implementation is intentionally focused on the supplied Meridian document set.

Limitations include:

- The knowledge base currently contains two source documents.
- Answers are limited to information contained in those documents.
- The local Qwen3 4B model is smaller than many cloud-based frontier models.
- The system is optimized for document-grounded enterprise QA rather than general-purpose conversation.
- The current interface is designed for local use.

---

# 🔮 Future Improvements

Potential future extensions include:

- Multi-quarter supply-chain analysis
- Supplier trend dashboards
- Automated supplier risk scoring
- Document upload from the UI
- Automatic re-indexing of new documents
- More advanced hybrid retrieval
- Reranking models
- Conversation history
- REST API integration
- Authentication and role-based access
- Production deployment
- Advanced analytics and visualization
- Supplier comparison dashboards
- Automated procurement recommendations

---

# 📚 Source Documents

The current knowledge base contains:

1. **Meridian Procurement Policy Handbook v4.2**
2. **Meridian Supply Chain Review Q1 FY2025-26**

These documents form the source of truth for the current RAG system.

---

# 👨‍💻 Author

**Akshay Vankayala**

Mechanical Engineering Student  
Vishnu Institute of Technology

GitHub:  
https://github.com/Akshay2006V

Project Repository:  
https://github.com/Akshay2006V/Meridian-Supply-Chain-RAG

---

# 🏆 Project Submission

**HCLTech × Economic Times AI Masterclass**

Project:

> **Meridian Supply Chain RAG**

A grounded AI assistant for supply-chain and procurement document intelligence.

---

## ⭐ Final Takeaway

> **The objective of an enterprise AI assistant is not to answer every question.**
>
> **It is to retrieve the right evidence, answer from that evidence, and clearly say when the evidence is not available.**
