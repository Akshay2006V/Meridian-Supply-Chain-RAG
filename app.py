import streamlit as st
from rag import ask


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Meridian Supply Chain AI",
    page_icon="📦",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       Hero
       -------------------------------------------------------- */

    .hero {
        padding: 28px 32px;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a5f 100%
        );
        margin-bottom: 28px;
    }

.hero-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 8px 0;
    color: white;
}

.hero-subtitle {
    font-size: 16px;
    color: #dbeafe;
    margin: 0;
    line-height: 1.5;
}

    /* --------------------------------------------------------
       Buttons
       -------------------------------------------------------- */

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }


    /* --------------------------------------------------------
       Metric cards
       -------------------------------------------------------- */

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background: rgba(128, 128, 128, 0.06);
    }

    .metric-number {
        font-size: 28px;
        font-weight: 700;
    }

    .metric-label {
        font-size: 14px;
        opacity: 0.75;
        margin-top: 4px;
    }


    /* --------------------------------------------------------
       Source cards
       -------------------------------------------------------- */

    .source-header {
        font-weight: 700;
        font-size: 16px;
    }

    .source-page {
        font-size: 14px;
        opacity: 0.75;
        margin-top: 4px;
    }


    /* --------------------------------------------------------
       Small UI polish
       -------------------------------------------------------- */

    .section-note {
        opacity: 0.75;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1 class="hero-title">📦 Meridian Supply Chain AI</h1>
        <p class="hero-subtitle">
            Grounded document intelligence for supply-chain
            performance and procurement policy analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("About")

    st.write(
        """
        This application uses Retrieval-Augmented
        Generation (RAG) to answer questions from
        Meridian Components' internal documents.
        """
    )

    st.divider()

    st.subheader("AI Stack")

    st.write("🧠 LLM: Qwen3 4B")
    st.write("🔎 Embeddings: Nomic Embed Text")
    st.write("🗄️ Vector DB: ChromaDB")
    st.write("📄 PDF Parser: PyPDF")
    st.write("🖥️ Interface: Streamlit")

    st.divider()

    st.subheader("Indexed Documents")

    st.write("📄 Supply Chain Performance Review")
    st.write("📄 Procurement Policy Handbook")

    st.divider()

    st.caption(
        "Answers are generated only from the "
        "indexed Meridian documents."
    )


# ============================================================
# MAIN
# ============================================================

st.subheader("Ask Meridian")

st.write(
    "Ask questions about supplier performance, "
    "procurement policy, spend, delivery, quality, "
    "and other information contained in the documents."
)


question = st.text_area(
    "Your question",
    placeholder=(
        "Example: Which suppliers had the lowest "
        "on-time delivery in Q1?"
    ),
    height=100,
    label_visibility="visible",
)


col1, col2, _ = st.columns([1, 1, 4])


with col1:

    ask_button = st.button(
        "🔍 Ask Meridian",
        type="primary",
        use_container_width=True,
    )


with col2:

    clear_button = st.button(
        "Clear",
        use_container_width=True,
    )


if clear_button:
    st.rerun()


# ============================================================
# QUERY
# ============================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                answer, retrieved = ask(
                    question.strip()
                )

            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )

                st.stop()


        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        st.divider()

        st.subheader("Answer")

        # Native Streamlit container automatically adapts
        # to light/dark mode and preserves Markdown.
        with st.container(border=True):

            st.markdown(answer)


        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        st.divider()

        st.subheader("Sources")

        displayed_sources = set()

        for item in retrieved:

            metadata = item["metadata"]

            source = metadata["source"]
            page = metadata["page"]

            source_key = (source, page)

            # Remove duplicate source/page combinations.
            if source_key in displayed_sources:
                continue

            displayed_sources.add(source_key)


            # Determine friendly document name.
            if "Review" in source:

                document_label = (
                    "Supply Chain Performance Review"
                )

            else:

                document_label = (
                    "Procurement Policy Handbook"
                )


            # Native Streamlit container.
            # No raw HTML source code is exposed.
            with st.container(border=True):

                st.markdown(
                    f"**📄 {document_label}**"
                )

                st.caption(
                    f"Source: {source}  •  Page {page}"
                )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.divider()

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">2</div>
                <div class="metric-label">
                    Indexed Documents
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">26</div>
                <div class="metric-label">
                    Indexed Chunks
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    with col3:

        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-number">✓</div>
                <div class="metric-label">
                    Grounded Document-only Answers
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.info(
        "Enter a question above to search the Meridian "
        "document collection."
    )