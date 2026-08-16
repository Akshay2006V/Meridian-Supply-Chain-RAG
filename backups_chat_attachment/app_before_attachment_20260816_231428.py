from pathlib import Path
from datetime import datetime

import streamlit as st

from ingest import ingest_paths
from rag import ask, collection


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Meridian Supply Chain AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New conversation"


# ============================================================
# HELPERS
# ============================================================

def get_document_count():
    """Return the number of unique indexed source documents."""

    try:
        data = collection.get(
            include=["metadatas"]
        )

        metadatas = data.get(
            "metadatas",
            []
        )

        documents = set()

        for metadata in metadatas:
            if metadata and metadata.get("source"):
                documents.add(
                    metadata["source"]
                )

        return len(documents)

    except Exception:
        return 0


def make_chat_title(question):
    """Create a compact title for chat history."""

    words = question.strip().split()

    if not words:
        return "New conversation"

    title = " ".join(
        words[:7]
    )

    if len(words) > 7:
        title += "..."

    return title


def get_sources(retrieved):
    """Extract unique source/page references."""

    sources = []
    seen = set()

    for item in retrieved:

        metadata = item.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "Unknown document"
        )

        page = metadata.get(
            "page",
            "?"
        )

        key = (
            source,
            page
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "source": source,
                "page": page,
            }
        )

    return sources


def ask_meridian(question):
    """Run the existing RAG pipeline."""

    answer, retrieved, timing = ask(
        question
    )

    return (
        answer,
        get_sources(retrieved),
        timing,
    )


def start_new_chat():
    st.session_state.messages = []
    st.session_state.chat_title = (
        "New conversation"
    )


def add_history_title(title):

    if title not in st.session_state.chat_history:

        st.session_state.chat_history.append(
            title
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "Meridian"
    )

    st.caption(
        "Supply-chain & procurement intelligence"
    )

    st.divider()

    # --------------------------------------------------------
    # DOCUMENT KNOWLEDGE BASE
    # --------------------------------------------------------

    st.subheader(
        "Knowledge Base"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Chunks",
            collection.count()
        )

    with col2:
        st.metric(
            "PDFs",
            get_document_count()
        )

    st.write("")

    st.subheader(
        "Add PDF documents"
    )

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Select one or more PDF files to add to the local knowledge base.",
    )

    if uploaded_files:

        st.caption(
            f"{len(uploaded_files)} file(s) selected."
        )

    if st.button(
        "Index Documents",
        type="primary",
        use_container_width=True,
    ):

        if not uploaded_files:

            st.warning(
                "Please upload at least one PDF."
            )

        else:

            data_dir = Path("data")

            data_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            paths = []

            try:

                with st.spinner(
                    "Indexing documents..."
                ):

                    for uploaded_file in uploaded_files:

                        destination = (
                            data_dir
                            / uploaded_file.name
                        )

                        destination.write_bytes(
                            uploaded_file.getbuffer()
                        )

                        paths.append(
                            destination
                        )

                    stats = ingest_paths(
                        paths
                    )

                if stats["new_chunks"] > 0:

                    st.success(
                        f"{stats['new_chunks']} new chunks added."
                    )

                else:

                    st.info(
                        f"No new chunks. "
                        f"{stats['total_chunks']} chunks already indexed."
                    )

                st.rerun()

            except Exception as exc:

                st.error(
                    f"Indexing failed: {exc}"
                )

    st.divider()

    # --------------------------------------------------------
    # AI STACK
    # --------------------------------------------------------

    st.subheader(
        "AI Stack"
    )

    st.write(
        "🧠 Qwen3 4B"
    )

    st.write(
        "🔎 Nomic Embed Text"
    )

    st.write(
        "🗄️ ChromaDB"
    )

    st.write(
        "📄 PyPDF"
    )

    st.write(
        "🖥️ Streamlit"
    )

    st.divider()

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    st.subheader(
        "Chat History"
    )

    if st.session_state.chat_history:

        for index, title in enumerate(
            reversed(
                st.session_state.chat_history
            ),
            start=1,
        ):

            st.caption(
                f"{index}. {title}"
            )

    else:

        st.caption(
            "No conversations yet."
        )

    if st.button(
        "New chat",
        use_container_width=True,
    ):

        start_new_chat()

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

header_left, header_right = st.columns(
    [12, 1]
)

with header_left:

    st.caption(
        datetime.now().strftime(
            "%I:%M %p"
        )
    )

    st.title(
        "Meridian Supply Chain AI"
    )

    st.caption(
        "A local Retrieval-Augmented Generation assistant "
        "for supplier performance, procurement policy, "
        "delivery, quality, inventory, and operational analysis."
    )


with header_right:

    # Native Streamlit popover.
    # This is intentionally kept minimal.
    with st.popover(
        "⋮"
    ):

        st.subheader(
            "Session"
        )

        st.write(
            f"Indexed documents: "
            f"{get_document_count()}"
        )

        st.write(
            f"Indexed chunks: "
            f"{collection.count()}"
        )

        st.divider()

        if st.button(
            "Clear conversation",
            use_container_width=True,
        ):

            start_new_chat()

            st.rerun()


st.divider()


# ============================================================
# KNOWLEDGE BASE SUMMARY
# ============================================================

st.header(
    "Knowledge Base"
)

st.write(
    "Persistent semantic retrieval across the indexed "
    "Meridian document collection."
)

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "Source documents",
        get_document_count()
    )

with m2:

    st.metric(
        "Indexed chunks",
        collection.count()
    )

with m3:

    st.metric(
        "Grounding",
        "100%"
    )


# ============================================================
# WELCOME / QUICK QUESTIONS
# ============================================================

if not st.session_state.messages:

    st.divider()

    st.header(
        "What can I help you find?"
    )

    st.write(
        "Ask a natural-language question about supplier "
        "performance, procurement policy, spend, delivery, "
        "quality, or inventory."
    )

    st.write("")

    q1, q2 = st.columns(2)

    with q1:

        if st.button(
            "Highest Q1 supplier spend",
            use_container_width=True,
        ):

            question = (
                "Which supplier had the highest spend in Q1, "
                "and what was its on-time delivery percentage?"
            )

            st.session_state.chat_title = (
                "Highest Q1 supplier spend"
            )

            add_history_title(
                st.session_state.chat_title
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.spinner(
                "Searching Meridian documents..."
            ):

                answer, sources, timing = ask_meridian(
                    question
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timing": timing,
                }
            )

            st.rerun()

    with q2:

        if st.button(
            "Q1 line stoppages",
            use_container_width=True,
        ):

            question = (
                "How many line stoppages happened in Q1, "
                "what was the total downtime, and what caused them?"
            )

            st.session_state.chat_title = (
                "Q1 line stoppages"
            )

            add_history_title(
                st.session_state.chat_title
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.spinner(
                "Searching Meridian documents..."
            ):

                answer, sources, timing = ask_meridian(
                    question
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timing": timing,
                }
            )

            st.rerun()

    q3, q4 = st.columns(2)

    with q3:

        if st.button(
            "₹1.4 crore PO authority",
            use_container_width=True,
        ):

            question = (
                "What is the approval authority for a "
                "purchase order worth ₹1.4 crore?"
            )

            st.session_state.chat_title = (
                "₹1.4 crore PO authority"
            )

            add_history_title(
                st.session_state.chat_title
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.spinner(
                "Searching Meridian documents..."
            ):

                answer, sources, timing = ask_meridian(
                    question
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timing": timing,
                }
            )

            st.rerun()

    with q4:

        if st.button(
            "Safety-stock requirement",
            use_container_width=True,
        ):

            question = (
                "Microcontrollers are imported with a "
                "46-day lead time. Using the safety-stock policy, "
                "how many days of stock should be held for this part?"
            )

            st.session_state.chat_title = (
                "Safety-stock requirement"
            )

            add_history_title(
                st.session_state.chat_title
            )

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.spinner(
                "Searching Meridian documents..."
            ):

                answer, sources, timing = ask_meridian(
                    question
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "timing": timing,
                }
            )

            st.rerun()


# ============================================================
# CONVERSATION
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.write(
                "Sources"
            )

            for source in message["sources"]:

                st.caption(
                    f"📄 {source['source']} "
                    f"• Page {source['page']}"
                )


# ============================================================
# NATIVE CHAT INPUT + FILE ATTACHMENTS
# ============================================================

submission = st.chat_input(
    "Ask Meridian...",
    accept_file="multiple",
    file_type=["pdf"],
    max_upload_size=200,
)


if submission:

    question = submission["text"].strip()

    uploaded_files = submission["files"]


    # --------------------------------------------------------
    # Process PDF attachments
    # --------------------------------------------------------

    if uploaded_files:

        data_dir = Path("data")
        data_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        saved_paths = []

        try:

            with st.spinner(
                "Adding documents to the Meridian knowledge base..."
            ):

                for uploaded_file in uploaded_files:

                    destination = (
                        data_dir
                        / uploaded_file.name
                    )

                    destination.write_bytes(
                        uploaded_file.getbuffer()
                    )

                    saved_paths.append(
                        destination
                    )

                stats = ingest_paths(
                    saved_paths
                )

            if stats["new_chunks"] > 0:

                st.toast(
                    f"Added {stats['new_chunks']} new chunks.",
                    icon="??",
                )

            else:

                st.toast(
                    "Documents were already indexed.",
                    icon="??",
                )

        except Exception as exc:

            st.error(
                f"Document indexing failed: {exc}"
            )


    # --------------------------------------------------------
    # Process normal question
    # --------------------------------------------------------

    if question:

        if (
            st.session_state.chat_title
            == "New conversation"
        ):

            st.session_state.chat_title = (
                make_chat_title(question)
            )

            add_history_title(
                st.session_state.chat_title
            )


        # User message

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )


        # RAG response

        try:

            with st.spinner(
                "Searching Meridian documents..."
            ):

                answer, sources, timing = (
                    ask_meridian(question)
                )

        except Exception as exc:

            answer = (
                "I couldn't process that request because "
                f"an internal error occurred: {exc}"
            )

            sources = []
            timing = {}


        # Assistant message

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "timing": timing,
            }
        )


    # --------------------------------------------------------
    # Attachment-only submission
    # --------------------------------------------------------

    elif uploaded_files:

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    f"Added {len(uploaded_files)} PDF "
                    f"document(s) to the Meridian knowledge base."
                ),
                "sources": [],
                "timing": {},
            }
        )


    st.rerun()

