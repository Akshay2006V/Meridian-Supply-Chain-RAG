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

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New conversation"


# ============================================================
# THEME
# ============================================================

if st.session_state.theme == "Dark":

    COLORS = {
        "bg": "#000000",
        "surface": "#1F150C",
        "surface2": "#412D15",
        "card": "#1F150C",
        "input": "#1F150C",
        "text": "#E1DCC9",
        "muted": "#B7AF9E",
        "accent": "#E1DCC9",
        "accent_text": "#000000",
        "border": "rgba(225,220,201,0.16)",
        "sidebar": "#1F150C",
        "shadow": "rgba(0,0,0,0.35)",
        "gradient1": "rgba(56,73,150,0.22)",
        "gradient2": "rgba(128,76,126,0.12)",
    }

else:

    COLORS = {
        "bg": "#FFFAF3",
        "surface": "#FFF2DB",
        "surface2": "#FFE5BF",
        "card": "#FFFFFF",
        "input": "#FFFFFF",
        "text": "#1F150C",
        "muted": "#6F6255",
        "accent": "#F62440",
        "accent_text": "#FFFFFF",
        "border": "rgba(31,21,12,0.12)",
        "sidebar": "#FFF2DB",
        "shadow": "rgba(31,21,12,0.10)",
        "gradient1": "rgba(246,36,64,0.08)",
        "gradient2": "rgba(255,229,191,0.65)",
    }


# ============================================================
# CSS
# ============================================================

css = f"""
<style>

:root {{
    --bg: {COLORS["bg"]};
    --surface: {COLORS["surface"]};
    --surface2: {COLORS["surface2"]};
    --card: {COLORS["card"]};
    --input: {COLORS["input"]};
    --text: {COLORS["text"]};
    --muted: {COLORS["muted"]};
    --accent: {COLORS["accent"]};
    --accent-text: {COLORS["accent_text"]};
    --border: {COLORS["border"]};
    --sidebar: {COLORS["sidebar"]};
    --shadow: {COLORS["shadow"]};
}}


/* ============================================================
   BASE
   ============================================================ */

.stApp {{
    min-height: 100vh;

    background:
        radial-gradient(
            circle at 82% 100%,
            {COLORS["gradient1"]},
            transparent 30%
        ),
        radial-gradient(
            circle at 15% 8%,
            {COLORS["gradient2"]},
            transparent 30%
        ),
        var(--bg);

    color: var(--text);
}}


/* ============================================================
   REMOVE STREAMLIT DEPLOY DECORATION
   ============================================================ */

[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton {{
    display: none !important;
}}


/* ============================================================
   HEADER
   ============================================================ */

header[data-testid="stHeader"] {{
    background: transparent !important;
}}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {{
    max-width: 920px !important;
    padding-top: 0.5rem !important;
    padding-bottom: 6rem !important;
}}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {{
    width: 235px !important;
    min-width: 235px !important;
    max-width: 235px !important;

    background: var(--sidebar) !important;

    border-right:
        1px solid var(--border);
}}

section[data-testid="stSidebar"] > div {{
    width: 235px !important;
    max-width: 235px !important;
}}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1 {{
    color: var(--text) !important;

    font-size: 30px !important;

    font-weight: 780 !important;

    letter-spacing:
        -0.035em !important;

    margin-bottom:
        0.1rem !important;
}}

h2 {{
    color: var(--text) !important;
}}

h3 {{
    color: var(--text) !important;
}}

p,
label,
span {{
    color: var(--text);
}}

[data-testid="stCaptionContainer"] {{
    color: var(--muted) !important;
}}


/* ============================================================
   TOP RIGHT SETTINGS BUTTON
   ============================================================ */

[data-testid="stPopover"] > button {{
    width: 38px !important;
    min-width: 38px !important;

    height: 38px !important;
    min-height: 38px !important;

    padding: 0 !important;

    border-radius: 50% !important;

    background: var(--surface) !important;

    color: var(--text) !important;

    border:
        1px solid var(--border) !important;

    font-size: 20px !important;

    box-shadow:
        none !important;
}}

[data-testid="stPopover"] > button svg {{
    display: none !important;
}}


/* ============================================================
   POPOVER
   ============================================================ */

[data-testid="stPopoverBody"] {{
    background: var(--card) !important;

    color: var(--text) !important;

    border:
        1px solid var(--border) !important;

    border-radius:
        16px !important;
}}

div[data-baseweb="popover"] > div {{
    background: var(--card) !important;

    color: var(--text) !important;

    border:
        1px solid var(--border) !important;
}}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {{
    border:
        none !important;

    height:
        1px !important;

    background:
        var(--border) !important;

    margin:
        15px 0 !important;
}}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {{
    background:
        linear-gradient(
            145deg,
            var(--card),
            var(--surface)
        ) !important;

    border:
        1px solid var(--border) !important;

    border-radius:
        14px !important;

    padding:
        10px 12px !important;

    box-shadow:
        0 7px 24px var(--shadow) !important;
}}

[data-testid="stMetricValue"] {{
    color:
        var(--text) !important;

    font-weight:
        800 !important;
}}

[data-testid="stMetricLabel"] {{
    color:
        var(--muted) !important;
}}


/* ============================================================
   SUGGESTION BUTTONS
   ============================================================ */

div.stButton > button {{
    border-radius:
        999px !important;

    min-height:
        40px !important;

    background:
        rgba(255,255,255,0.025) !important;

    border:
        1px solid var(--border) !important;

    color:
        var(--text) !important;

    font-size:
        13px !important;

    font-weight:
        600 !important;

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        background 0.18s ease;
}}

div.stButton > button:hover {{
    transform:
        translateY(-1px);

    background:
        var(--surface) !important;

    border-color:
        var(--accent) !important;
}}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

button[kind="primary"] {{
    background:
        var(--accent) !important;

    color:
        var(--accent-text) !important;

    border-color:
        var(--accent) !important;
}}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {{
    background:
        var(--surface) !important;

    border:
        1px solid var(--border) !important;

    border-radius:
        13px !important;
}}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {{
    padding:
        4px 0 !important;
}}

[data-testid="stChatMessageContent"] {{
    max-width:
        760px !important;

    color:
        var(--text) !important;

    font-size:
        14px !important;

    line-height:
        1.62 !important;
}}


/* ============================================================
   CHAT INPUT
   IMPORTANT:
   Do NOT position stBottom manually.
   Streamlit handles fixed positioning natively.
   ============================================================ */

[data-testid="stChatInput"] {{
    max-width:
        780px !important;

    margin:
        0 auto !important;

    padding:
        0 !important;
}}

[data-testid="stChatInput"] > div {{
    min-height:
        54px !important;

    border-radius:
        999px !important;

    background:
        var(--input) !important;

    border:
        1px solid var(--border) !important;

    box-shadow:
        0 8px 28px var(--shadow) !important;
}}

[data-testid="stChatInput"] textarea {{
    min-height:
        50px !important;

    max-height:
        50px !important;

    padding:
        14px 55px 14px 58px !important;

    background:
        transparent !important;

    color:
        var(--text) !important;

    border:
        none !important;

    resize:
        none !important;

    font-size:
        14px !important;
}}

[data-testid="stChatInput"] textarea::placeholder {{
    color:
        transparent !important;

    opacity:
        0 !important;
}}


/* ============================================================
   MERIDIAN CHAT MARK
   ============================================================ */

[data-testid="stChatInput"] > div::before {{
    content: "✦";

    position:
        absolute;

    left:
        15px;

    top:
        50%;

    transform:
        translateY(-50%);

    width:
        29px;

    height:
        29px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        50%;

    font-size:
        17px;

    font-weight:
        800;

    color:
        #1F150C;

    background:
        radial-gradient(
            circle at 35% 30%,
            #FFF7D6 0%,
            #F4C66B 25%,
            #CA7137 58%,
            #6C3621 100%
        );

    box-shadow:
        0 0 10px rgba(225,220,201,0.18);

    pointer-events:
        none;
}}


/* ============================================================
   SEND BUTTON
   ============================================================ */

[data-testid="stChatInput"] button {{
    width:
        34px !important;

    min-width:
        34px !important;

    height:
        34px !important;

    min-height:
        34px !important;

    border-radius:
        50% !important;

    background:
        var(--accent) !important;

    color:
        var(--accent-text) !important;

    border:
        none !important;
}}


/* ============================================================
   SOURCES
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {{
    background:
        var(--surface) !important;

    border:
        1px solid var(--border) !important;

    border-radius:
        11px !important;
}}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 850px) {{

    .block-container {{
        max-width:
            calc(100vw - 26px) !important;

        padding-left:
            13px !important;

        padding-right:
            13px !important;

        padding-bottom:
            6rem !important;
    }}

    h1 {{
        font-size:
            27px !important;
    }}

    section[data-testid="stSidebar"] {{
        width:
            250px !important;
        max-width:
            250px !important;
    }}
}}

</style>
"""

st.markdown(
    css,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def indexed_document_count():
    try:
        result = collection.get(
            include=["metadatas"]
        )

        metadatas = result.get(
            "metadatas",
            []
        )

        sources = {
            item.get("source")
            for item in metadatas
            if item and item.get("source")
        }

        return len(sources)

    except Exception:
        return 0


def document_label(source):
    if "Review" in source:
        return "Supply Chain Performance Review"

    if "Policy" in source:
        return "Procurement Policy Handbook"

    return "Meridian Document"


def extract_sources(retrieved):
    sources = []
    seen = set()

    for item in retrieved:

        metadata = item["metadata"]

        source = metadata.get(
            "source",
            "Unknown document",
        )

        page = metadata.get(
            "page",
            "?",
        )

        key = (
            source,
            page,
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "label": document_label(source),
                "source": source,
                "page": page,
            }
        )

    return sources


def new_chat():
    st.session_state.messages = []
    st.session_state.chat_title = "New conversation"


def process_question(question):

    answer, retrieved, timing = ask(
        question
    )

    return (
        answer,
        extract_sources(retrieved),
        timing,
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
    # Knowledge Base
    # --------------------------------------------------------

    st.subheader(
        "Knowledge Base"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Chunks",
            collection.count(),
        )

    with c2:
        st.metric(
            "PDFs",
            indexed_document_count(),
        )

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if st.button(
        "Index Documents",
        type="primary",
        use_container_width=True,
    ):

        if not uploaded_files:

            st.warning(
                "Upload at least one PDF first."
            )

        else:

            data_dir = Path("data")

            data_dir.mkdir(
                parents=True,
                exist_ok=True,
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

                if stats["new_chunks"]:

                    st.success(
                        f"{stats['new_chunks']} new chunks added."
                    )

                else:

                    st.info(
                        f"No new chunks. "
                        f"{stats['total_chunks']} chunks already indexed."
                    )

            except Exception as exc:

                st.error(
                    f"Indexing failed: {exc}"
                )

    st.divider()

    # --------------------------------------------------------
    # AI Stack
    # --------------------------------------------------------

    st.subheader(
        "AI Stack"
    )

    st.caption("Qwen3 4B")
    st.caption("Nomic Embed Text")
    st.caption("ChromaDB")
    st.caption("PyPDF")
    st.caption("Streamlit")

    st.divider()

    # --------------------------------------------------------
    # Chat History
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
            "Your conversations will appear here."
        )

    if st.button(
        "New chat",
        use_container_width=True,
    ):

        new_chat()

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

header_left, header_right = st.columns(
    [12, 1],
    vertical_alignment="center",
)

with header_left:

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )

    st.markdown(
        f"""
        <div style="
            text-align:right;
            font-size:11px;
            font-weight:500;
            letter-spacing:0.04em;
            opacity:0.65;
            margin-bottom:-4px;
        ">
            {current_time}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title(
        "Meridian Supply Chain AI"
    )

    st.caption(
        "A local Retrieval-Augmented Generation assistant that answers "
        "supply-chain and procurement questions using evidence from "
        "indexed Meridian Components documents."
    )


with header_right:

    with st.popover(
        "⋮",
        use_container_width=False,
    ):

        st.subheader(
            "Settings"
        )

        st.markdown(
            "**Appearance**"
        )

        selected_theme = st.radio(
            "Theme",
            [
                "Dark",
                "Light",
            ],
            index=(
                0
                if st.session_state.theme == "Dark"
                else 1
            ),
            label_visibility="collapsed",
        )

        if selected_theme != st.session_state.theme:

            st.session_state.theme = (
                selected_theme
            )

            st.rerun()

        st.divider()

        if st.button(
            "Clear conversation",
            use_container_width=True,
        ):

            new_chat()

            st.rerun()


st.divider()


# ============================================================
# KNOWLEDGE BASE
# ============================================================

st.subheader(
    "Knowledge Base"
)

st.caption(
    "Persistent semantic retrieval across the indexed Meridian document collection."
)

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "Source documents",
        indexed_document_count(),
    )

with m2:

    st.metric(
        "Indexed chunks",
        collection.count(),
    )

with m3:

    st.metric(
        "Grounding",
        "100%",
    )


# ============================================================
# WELCOME
# ============================================================

if not st.session_state.messages:

    st.divider()

    st.subheader(
        "What can I help you find?"
    )

    st.caption(
        "Ask about supplier performance, procurement policy, "
        "spend, delivery, quality, or inventory."
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

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.chat_title = (
                "Highest Q1 supplier spend"
            )

            answer, sources, timing = process_question(
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

            st.session_state.chat_history.append(
                st.session_state.chat_title
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

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.chat_title = (
                "Q1 line stoppages"
            )

            answer, sources, timing = process_question(
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

            st.session_state.chat_history.append(
                st.session_state.chat_title
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

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.chat_title = (
                "₹1.4 crore PO authority"
            )

            answer, sources, timing = process_question(
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

            st.session_state.chat_history.append(
                st.session_state.chat_title
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

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            st.session_state.chat_title = (
                "Safety-stock requirement"
            )

            answer, sources, timing = process_question(
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

            st.session_state.chat_history.append(
                st.session_state.chat_title
            )

            st.rerun()


# ============================================================
# CHAT HISTORY / MESSAGES
# ============================================================

for message in st.session_state.messages:

    avatar = (
        "👤"
        if message["role"] == "user"
        else "✦"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown(
                "**Sources**"
            )

            for source in message["sources"]:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"📄 **{source['label']}**"
                    )

                    st.caption(
                        f"{source['source']} • Page {source['page']}"
                    )


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input()

if prompt:

    question = prompt.strip()

    if question:

        if (
            st.session_state.chat_title
            == "New conversation"
        ):

            words = question.split()

            title = " ".join(
                words[:6]
            )

            if len(words) > 6:
                title += "..."

            st.session_state.chat_title = title

            st.session_state.chat_history.append(
                title
            )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        try:

            with st.spinner(
                "Searching the Meridian knowledge base..."
            ):

                answer, sources, timing = process_question(
                    question
                )

        except Exception as exc:

            answer = (
                "I couldn't process that request because "
                f"an internal error occurred: {exc}"
            )

            sources = []
            timing = {}

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
                "timing": timing,
            }
        )

        st.rerun()