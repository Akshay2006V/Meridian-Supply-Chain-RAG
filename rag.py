import chromadb
import ollama


# --------------------------------------------------
# Configuration
# --------------------------------------------------

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "meridian_supply_chain"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "qwen3:4b"

TOP_K = 8


# --------------------------------------------------
# ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# --------------------------------------------------
# Embedding
# --------------------------------------------------

def embed_query(query: str):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )

    return response["embeddings"][0]


# --------------------------------------------------
# Retrieval
# --------------------------------------------------

def retrieve(query: str, top_k: int = TOP_K):

    query_embedding = embed_query(query)

    # Retrieve independently from both documents.
    # This prevents one document from dominating the results.

    review_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=4,
        where={
            "document_type": "performance_review"
        },
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    policy_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k // 2 + 1,
        where={
            "document_type": "procurement_policy"
        },
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved = []

    # Add review results
    for document, metadata, distance in zip(
        review_results["documents"][0],
        review_results["metadatas"][0],
        review_results["distances"][0]
    ):
        retrieved.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance
            }
        )

    # Add policy results
    for document, metadata, distance in zip(
        policy_results["documents"][0],
        policy_results["metadatas"][0],
        policy_results["distances"][0]
    ):
        retrieved.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance
            }
        )

    # Sort by semantic distance.
    retrieved.sort(
        key=lambda x: x["distance"]
    )

    return retrieved[:top_k]
# --------------------------------------------------
# Context builder
# --------------------------------------------------

def build_context(retrieved_chunks):

    context_parts = []

    for i, item in enumerate(
        retrieved_chunks,
        start=1
    ):

        metadata = item["metadata"]

        source = metadata["source"]
        page = metadata["page"]

        context_parts.append(
            f"""
SOURCE {i}
File: {source}
Page: {page}

{item["text"]}
"""
        )

    return "\n".join(context_parts)


# --------------------------------------------------
# LLM
# --------------------------------------------------

SYSTEM_PROMPT = """
You are Meridian Supply Chain Document Intelligence Assistant.

Your job is to answer questions using ONLY the supplied
Meridian Components documents in the retrieved context.

POLICY THRESHOLD INTERPRETATION:

When evaluating supplier performance against the Procurement
Policy Handbook, carefully check ALL applicable clauses.

Important:
- Clause 6.1 applies when on-time delivery is BELOW 90%.
- Clause 6.2 applies only when on-time delivery is BELOW 85%
  FOR TWO CONSECUTIVE QUARTERS.
- Clause 6.3 applies when defect rate is ABOVE 500 PPM.

Do not substitute the Clause 6.2 threshold (85%) for the
Clause 6.1 threshold (90%).

For a supplier with 88.1% OTD:
- Clause 6.1 IS applicable because 88.1% < 90%.
- Clause 6.2 is NOT applicable based on a single quarter,
  because 88.1% is not below 85% and the two-quarter
  requirement is not established.

For a supplier with 1,150 PPM defects:
- Clause 6.3 IS applicable because 1,150 > 500 PPM.

IMPORTANT INTERPRETATION RULE:

If a question asks what policy consequences "apply",
"would apply", "should apply", or what a supplier is
subject to based on stated performance metrics, compare
the supplied performance metrics against the policy
thresholds and explain the resulting policy consequences.

This is a document-grounded inference, NOT an invention.

For example:
- If the performance document says OTD = 88%
- and the policy says OTD below 90% triggers Clause 6.1,
then you may conclude that Clause 6.1 applies based on
the documented threshold.

Similarly:
- If defects = 1,150 PPM
- and the policy says defects above 500 PPM trigger
Clause 6.3,
then you may conclude that Clause 6.3 applies.

RULES:

1. Use ONLY information contained in the retrieved context.

2. Do not invent facts, numbers, supplier actions,
   dates, policies, clauses, or outcomes.

3. Distinguish between:
   a) what the documents explicitly state happened, and
   b) what policy consequence follows from comparing
      documented performance against a documented threshold.

4. For cross-document questions, actively combine
   information from BOTH the Supply Chain Performance
   Review and the Procurement Policy Handbook when
   relevant.

5. If the documents contain the necessary performance
   metric and the corresponding policy threshold,
   answer the question by applying that threshold.

6. If the required information is genuinely absent from
   the supplied documents, respond exactly:

   "I cannot answer that from the supplied documents."

7. Do NOT refuse merely because the documents do not
   explicitly say that the policy consequence was already
   executed. If the question asks what consequence applies
   based on a documented threshold, derive the applicability
   from the threshold.

8. Always cite the relevant source filename and page number.

9. Never use outside knowledge.

10. Keep answers concise but explain the reasoning when
    combining information across documents.
"""

def generate_answer(question, context):

    user_prompt = f"""
Retrieved context:

{context}

Question:

{question}

Answer using ONLY the retrieved context.
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response["message"]["content"]


# --------------------------------------------------
# Complete RAG query
# --------------------------------------------------

def ask(question: str):

    retrieved = retrieve(
        question,
        TOP_K
    )

    context = build_context(
        retrieved
    )

    answer = generate_answer(
        question,
        context
    )

    return answer, retrieved


# --------------------------------------------------
# CLI test
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("MERIDIAN SUPPLY CHAIN RAG")
    print("=" * 70)

    question = input(
        "\nEnter your question: "
    ).strip()

    if not question:
        print("No question entered.")
        raise SystemExit

    answer, retrieved = ask(question)

    print("\nANSWER")
    print("-" * 70)
    print(answer)

    print("\nRETRIEVED SOURCES")
    print("-" * 70)

    for i, item in enumerate(
        retrieved,
        start=1
    ):

        metadata = item["metadata"]

        print(
            f"{i}. "
            f"{metadata['source']} "
            f"(Page {metadata['page']}) "
            f"[distance={item['distance']:.4f}]"
        )