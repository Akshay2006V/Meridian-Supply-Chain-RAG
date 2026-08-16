from pathlib import Path
import hashlib

import chromadb
import ollama
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -----------------------------
# Configuration
# -----------------------------

DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")

COLLECTION_NAME = "meridian_supply_chain"

EMBEDDING_MODEL = "nomic-embed-text"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


# -----------------------------
# ChromaDB
# -----------------------------

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# -----------------------------
# Text splitter
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)


def make_id(filename: str, page: int, chunk: str) -> str:
    """
    Create a deterministic ID so the same chunk
    is not inserted repeatedly.
    """
    raw = f"{filename}|{page}|{chunk}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def embed_text(text: str):
    """
    Generate an embedding using Ollama.
    """
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response["embeddings"][0]


def process_pdf(pdf_path: Path):
    """
    Extract text page-by-page and create chunks
    while preserving source metadata.
    """

    print(f"\nProcessing: {pdf_path.name}")

    reader = PdfReader(str(pdf_path))

    documents = []
    metadatas = []
    ids = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        chunks = splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):

            chunk = chunk.strip()

            if not chunk:
                continue

            chunk_id = make_id(
                pdf_path.name,
                page_number,
                chunk
            )

            documents.append(chunk)

            metadatas.append(
                {
                    "source": pdf_path.name,
                    "page": page_number,
                    "document_type": (
                        "performance_review"
                        if "Review" in pdf_path.name
                        else "procurement_policy"
                    ),
                    "chunk_index": chunk_index,
                }
            )

            ids.append(chunk_id)

    return documents, metadatas, ids


def ingest():

    pdf_files = sorted(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("ERROR: No PDF files found in data/")
        return

    total_added = 0

    for pdf_path in pdf_files:

        documents, metadatas, ids = process_pdf(pdf_path)

        print(f"Chunks generated: {len(documents)}")

        # Check which IDs already exist
        existing = collection.get(
            ids=ids,
            include=[]
        )

        existing_ids = set(existing["ids"])

        new_documents = []
        new_metadatas = []
        new_ids = []

        for doc, metadata, doc_id in zip(
            documents,
            metadatas,
            ids
        ):

            if doc_id not in existing_ids:

                new_documents.append(doc)
                new_metadatas.append(metadata)
                new_ids.append(doc_id)

        if not new_documents:

            print("All chunks already exist. Skipping.")

            continue

        print(
            f"Generating embeddings for "
            f"{len(new_documents)} new chunks..."
        )

        embeddings = []

        for i, document in enumerate(new_documents, start=1):

            print(
                f"Embedding {i}/{len(new_documents)}",
                end="\r"
            )

            embeddings.append(
                embed_text(document)
            )

        print()

        collection.add(
            ids=new_ids,
            documents=new_documents,
            metadatas=new_metadatas,
            embeddings=embeddings,
        )

        total_added += len(new_documents)

        print(
            f"Added {len(new_documents)} chunks "
            f"from {pdf_path.name}"
        )

    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)

    print(f"New chunks added: {total_added}")
    print(f"Total chunks in ChromaDB: {collection.count()}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Database: {CHROMA_DIR.resolve()}")


if __name__ == "__main__":
    ingest()