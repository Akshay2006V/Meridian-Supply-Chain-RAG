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

# 🎯 Problem Statement

Supply-chain and procurement teams frequently work with operational documents containing:

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

# 💡 Solution

The application combines:

```text
PDF ingestion
      ↓
Text extraction
      ↓
Recursive chunking
      ↓
Embedding generation
      ↓
ChromaDB semantic retrieval
      ↓
Relevant evidence
      ↓
Grounded answer extraction
      ↓
Qwen3 4B fallback when synthesis is required
```

The result is a lightweight local AI assistant that can answer supply-chain questions without requiring an external OpenAI API key.

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

## 1. Document Ingestion

The supplied Meridian PDF documents are processed using `PyPDF`.

## 2. Text Extraction

Text is extracted page-by-page while preserving the source document and page metadata.

## 3. Recursive Chunking

The project uses LangChain's recursive text splitter.

```text
Chunk size  : 1000 characters
Overlap     : 150 characters
```

The chunk size keeps policy clauses, supplier metrics, and related evidence together, while the overlap preserves context across adjacent chunks.

## 4. Embedding Generation

Each chunk is converted into a vector representation using:

```text
nomic-embed-text
```

## 5. Vector Storage

Embeddings and their metadata are stored in a persistent:

```text
ChromaDB
```

collection.

## 6. Query Retrieval

A user question follows this pipeline:

```text
Question
   ↓
Query embedding
   ↓
ChromaDB semantic search
   ↓
Relevant document chunks
```

## 7. Grounded Answer Generation

The application uses retrieved context as the factual source for the answer.

For questions that require additional synthesis, the system can use:

```text
Qwen3 4B
```

## 8. Unsupported Information Handling

When the requested information is not supported by the available documents, the system refuses to fabricate an answer.

Example:

```text
User:
What is the annual salary of the Head of Procurement?

System:
I cannot answer that from the supplied documents.
```

This is a deliberate hallucination-control mechanism.

---

# ⭐ Key Features

## 📄 PDF-Based Knowledge Base

The current knowledge base contains:

```text
Meridian_Procurement_Policy_Handbook_v4.2.pdf
Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
```

## 🔎 Semantic Search

Questions are converted into embeddings and matched against indexed document chunks using ChromaDB.

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

## 🧾 Procurement Policy Reasoning

The system can combine supplier-performance evidence with procurement-policy thresholds.

```text
Supplier Performance
        +
Procurement Policy
        ↓
Applicable Policy Consequence
```

## 🚫 Hallucination Resistance

The system is intentionally designed to prefer:

```text
"I cannot answer that from the supplied documents."
```

over unsupported or fabricated information.

## ⚡ Local Execution

The core AI workflow operates locally through Ollama, avoiding dependence on an external LLM API.

---

# 🧪 Automated Validation

The project includes:

```text
test_rag.py
```

The automated suite validates six representative scenarios:

| Test | Scenario |
|---|---|
| 1 | Highest-spend supplier |
| 2 | Line stoppages and downtime |
| 3 | Purchase-order approval |
| 4 | Critical supplier classification |
| 5 | Safety-stock calculation |
| 6 | Unsupported question handling |

### Final Automated Result

```text
============================================================
MERIDIAN RAG AUTOMATED TESTS
============================================================

Passed: 6
Failed: 0
Total : 6

RESULT: ALL TESTS PASSED
```

These automated tests were used as a repeatable validation layer during development.

---

# 💬 Example Questions

## 1. Highest-Spend Supplier

> Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?

### Answer

**Shenzhen Rui Electronics** had the highest Q1 spend at **₹21.9 crore**, with **79.5% on-time delivery**.

---

## 2. Line Stoppages

> How many line stoppages happened in Q1, what was the total downtime, and what caused them?

### Answer

There were **7 line-stoppage events**, resulting in **41 hours of downtime**.

The causes included:

- Four microcontroller shortages involving Shenzhen Rui Electronics
- Two PCB lots rejected at incoming inspection involving Trident Circuit Boards
- One transporter strike in the Coimbatore–Pune corridor

---

## 3. Purchase-Order Approval

> What is the approval authority for a purchase order worth ₹1.4 crore?

### Answer

A purchase order worth **₹1.4 crore** requires approval from the **Chief Operating Officer**.

---

## 4. Supplier Classification

> What are the four supplier classification categories, and what qualifies a supplier as Critical?

### Answer

The four categories are:

- Critical
- Strategic
- Standard
- Tail

A supplier is classified as Critical when it is:

- Single-source for any part
- Above ₹10 crore annual spend
- Supplying a safety-related component

---

## 5. Kaveri Metals Policy Consequences

> Kaveri Metals had 88.1% on-time delivery and 1,150 PPM defects in Q1. What procurement policy consequences apply to this supplier?

### Answer

Kaveri Metals' **1,150 PPM defect rate** exceeds the **500 PPM** policy threshold, so Clause 6.3 applies.

The consequence is:

- Supplier bears rework cost at **₹120 per affected unit**
- **100% incoming inspection** is imposed at the supplier's cost until three consecutive lots are accepted without defect

Its 88.1% on-time delivery does not trigger the below-85% delivery clause.

---

## 6. Single-Source Microcontroller Supplier

> The microcontroller supplier is single-source. What does the sourcing policy require in this situation, and what is the company already doing about it?

### Answer

A qualified second source must be established **within 12 months** of Critical classification.

As a temporary mitigation, the company is shifting **30% of Shenzhen microcontroller volume to air freight** while qualification of an alternate supplier is underway.

---

## 7. Safety Stock

> Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?

### Answer

The calculated safety stock is:

```text
46 × 0.25 = 11.5 days
```

The applicable minimum safety-stock floor is **30 days**.

Therefore:

**Required safety stock = 30 days**

---

## 8. Trident Circuit Boards

> Trident Circuit Boards had a defect rate of 640 PPM. What is the cost consequence under the policy?

### Answer

640 PPM exceeds the policy threshold of 500 PPM.

Therefore:

- Supplier bears rework cost at **₹120 per affected unit**
- **100% incoming inspection** is imposed at the supplier's cost until three consecutive lots are accepted without defect

---

## 9. B-Rating Band and Escalation

> Which suppliers would fall below the B rating band on on-time delivery alone, and what is the escalation path for them?

### Answer

No supplier in the available Q1 dataset falls below the **75% B-band threshold** on on-time delivery alone.

The escalation path for delivery-related issues is:

| Level | Owner | Response Time | Typical Trigger |
|---|---|---|---|
| 1 | Buyer | 24 hours | Delivery slippage up to 3 days |
| 2 | Category Manager | 48 hours | Slippage beyond 3 days or rejected lot |
| 3 | Head of Procurement | 72 hours | Risk of line stoppage within 7 days |
| 4 | Chief Operating Officer | 5 working days | Actual line stoppage or supplier insolvency signal |

---

## 10. Unsupported Information

> What is the annual salary of the Head of Procurement?

### Answer

```text
I cannot answer that from the supplied documents.
```

This demonstrates the system's ability to reject unsupported requests rather than hallucinating information.

---

# 🖥️ Application Interface

The Streamlit interface provides three primary areas:

### Ask Meridian

Natural-language questions can be entered directly into the application.

### Answer

The generated response is presented in a clean response area.

### Sources

Retrieved source documents and page information are displayed below the answer.

---

# 📸 Screenshots

## Streamlit Application

![Meridian Supply Chain AI](<img width="1920" height="1080" alt="Screenshot 2026-08-16 203541" src="https://github.com/user-attachments/assets/044a5399-bc9b-4e83-8f7a-1fa50d55d46d" />
)

*Main application interface showing the Meridian Supply Chain AI assistant, indexed documents, technology stack, and query interface.*

## GitHub Repository

![Meridian Supply Chain GitHub Repository](<img width="1920" height="1080" alt="Screenshot 2026-08-16 203948" src="https://github.com/user-attachments/assets/f183a225-d596-4aef-9e14-3afb1bf20572" />
)

*Public GitHub repository showing the project structure, README, source files, and documentation.*

---

# 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.14 |
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
├── .streamlit/
│   └── Streamlit configuration
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

Activate on Windows:

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

The ingestion pipeline follows:

```text
PDF
 ↓
Text Extraction
 ↓
Recursive Chunking
 ↓
Embedding
 ↓
Persistent ChromaDB
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

Expected final benchmark:

```text
Passed: 6
Failed: 0
Total : 6
```

---

# 🔐 Privacy & Local Execution

The project is designed for local execution.

The core workflow is:

```text
Ollama
   ↓
Local LLM
   +
Local Embeddings
   ↓
ChromaDB
```

No OpenAI API key is required.

The following are excluded from version control:

```text
.venv/
.env
__pycache__/
*.pyc
chroma_db/
```

---

# 📐 Design Principles

## 1. Grounded Answers

The system answers from the supplied documents rather than relying on unsupported general knowledge.

## 2. Evidence Before Generation

Relevant document content is retrieved before an answer is generated.

## 3. Exact Information Preservation

Important names, numerical values, units, supplier names, and policy thresholds should be preserved.

## 4. Unsupported Questions Should Be Rejected

When evidence is unavailable, the system should prefer:

```text
I cannot answer that from the supplied documents.
```

over an invented answer.

## 5. Local-First AI

The project demonstrates that practical document intelligence can be implemented using local models, local embeddings, and a local vector database.

---

# 📊 Assignment Validation — All 10 Required Questions

The application was evaluated against the ten required assignment questions.

| # | Question | Validation |
|---|---|---|
| 1 | Highest-spend supplier and on-time delivery | ✅ |
| 2 | Line stoppages, downtime, and causes | ✅ |
| 3 | ₹1.4 crore purchase-order approval authority | ✅ |
| 4 | Supplier categories and Critical criteria | ✅ |
| 5 | Kaveri Metals policy consequences | ✅ |
| 6 | Single-source microcontroller sourcing requirement | ✅ |
| 7 | Microcontroller safety stock | ✅ |
| 8 | Trident Circuit Boards policy consequence | ✅ |
| 9 | B-rating threshold and escalation path | ✅ |
| 10 | Unsupported salary question | ✅ Correct refusal |

The ten questions are documented above together with the answers produced by the final implementation.

---

# ⚠️ Honest Validation Note

During development, several questions initially exposed weaknesses in retrieval coverage and answer generation.

Examples included:

- A line-stoppage answer that did not preserve every supplier name
- An unsupported-question response that initially narrated its analysis instead of returning the required refusal
- Cross-document policy questions that initially produced incomplete conclusions

These issues were addressed through changes to the retrieval balance, answer-generation constraints, unsupported-topic handling, and validation logic.

The repeatable automated benchmark ultimately reached:

```text
Passed: 6
Failed: 0
Total : 6

RESULT: ALL TESTS PASSED
```

This distinction is intentional: development-stage failures are acknowledged rather than hidden, while the final automated benchmark represents the validated state of the implementation.

---

# 📈 Why This Project Matters

Supply-chain decisions often require connecting multiple dimensions:

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

This project demonstrates how RAG can act as an interface between operational documents and the person making the decision.

Instead of manually searching through pages of reports and policies, users can ask direct questions in natural language and retrieve evidence-backed information.

---

# 🎓 Learning Outcomes

The project provided hands-on experience with:

- Retrieval-Augmented Generation
- Semantic search
- Vector databases
- Embeddings
- Local LLM inference
- PDF processing
- Recursive chunking
- Prompt design
- Grounding and hallucination control
- Automated testing
- Streamlit application development
- Git and GitHub workflow

Most importantly, it demonstrates the difference between:

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

Current limitations include:

- The knowledge base contains two source documents.
- Answers are limited to information contained in those documents.
- Qwen3 4B is a compact local model and has less general reasoning capacity than larger frontier models.
- The system is optimized for grounded document QA rather than unrestricted general-purpose conversation.
- The current interface is designed for local use.

---

# 🔮 Future Improvements

Potential extensions include:

- Multi-quarter supply-chain analysis
- Supplier trend dashboards
- Automated supplier-risk scoring
- Document upload directly from the UI
- Automatic re-indexing
- Hybrid retrieval
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

# 🎯 Conclusion

Meridian Supply Chain RAG demonstrates how Retrieval-Augmented Generation can transform operational documents into a practical supply-chain intelligence interface.

The project combines:

```text
Document Processing
        +
Semantic Retrieval
        +
Persistent Vector Storage
        +
Grounded Answering
        +
Unsupported-Question Detection
        ↓
Supply-Chain Decision Support
```

The most important outcome is not simply generating answers.

It is generating answers that are **supported by evidence from the supplied documents** while explicitly refusing to invent information when that evidence does not exist.

The project therefore focuses on a practical principle for enterprise AI:

> **Retrieve → Ground → Generate → Verify**

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

### Project

> **Meridian Supply Chain RAG**

A grounded AI assistant for supply-chain and procurement document intelligence.

---

## ⭐ Final Takeaway

> **The objective of an enterprise AI assistant is not to answer every question.**
>
> **It is to retrieve the right evidence, answer from that evidence, and clearly say when the evidence is not available.**
