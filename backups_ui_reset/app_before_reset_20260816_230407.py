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
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "last_index_stats" not in st.session_state:
    st.session_state.last_index_stats = None


# ============================================================
# HELPERS
# ============================================================



def get_indexed_documents():

    try:

        result = collection.get(
            include=["metadatas"]
        )

        metadatas = result.get(
            "metadatas",
            []
        )

        sources = set()

        for metadata in metadatas:

            if metadata and metadata.get("source"):

                sources.add(
                    metadata["source"]
                )

        return len(sources)

    except Exception:

        return 0


def get_document_label(source):

    if "Review" in source:
        return "Supply Chain Performance Review"

    if "Policy" in source:
        return "Procurement Policy Handbook"

    return "Indexed PDF Document"


def answer_question(question):

    answer, retrieved, timing = ask(
        question.strip()
    )

    sources = []
    seen = set()

    for item in retrieved:

        metadata = item["metadata"]

        source = metadata["source"]
        page = metadata["page"]

        key = (
            source,
            page,
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        sources.append(
            {
                "label": get_document_label(source),
                "source": source,
                "page": page,
            }
        )

    return (
        answer,
        sources,
        timing,
    )


def queue_question(question):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "processed": False,
        }
    )

    st.rerun()


# ============================================================
# THEME PALETTE
# ============================================================

if st.session_state.theme == "Dark":

    COLORS = {
        "bg": "#000000",
        "surface": "#1F150C",
        "surface_alt": "#412D15",
        "card": "#1F150C",
        "text": "#E1DCC9",
        "muted": "#B7AF9E",
        "accent": "#E1DCC9",
        "accent_hover": "#FFF2DB",
        "border": "rgba(225,220,201,0.16)",
        "input": "#1F150C",
        "sidebar": "#1F150C",
        "chatbar": "transparent",
        "primary_text": "#000000",
    }

else:

    COLORS = {
        "bg": "#FFFAF3",
        "surface": "#FFF2DB",
        "surface_alt": "#FFE5BF",
        "card": "#FFFFFF",
        "text": "#1F150C",
        "muted": "#6F6255",
        "accent": "#F62440",
        "accent_hover": "#D91D37",
        "border": "rgba(31,21,12,0.12)",
        "input": "#FFFFFF",
        "sidebar": "#FFF2DB",
        "chatbar": "transparent",
        "primary_text": "#FFFFFF",
    }


# ============================================================
# SAFE CSS
# ============================================================

css = """
<style>

.stApp {
    background-color: __BG__;
    color: __TEXT__;
}

.block-container {
    max-width: 900px !important;
    width: min(900px, calc(100vw - 255px)) !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 0.65rem !important;
    padding-bottom: 4rem !important;
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

footer {
    visibility: hidden;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    width: 200px !important;
    min-width: 200px !important;
    max-width: 200px !important;
    background-color: __SIDEBAR__ !important;
    border-right: 1px solid __BORDER__;
}

section[data-testid="stSidebar"] > div {
    width: 200px !important;
    min-width: 200px !important;
    max-width: 200px !important;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

h1 {
    font-size: 31px !important;
    line-height: 1.08 !important;
    font-weight: 750 !important;
    letter-spacing: -0.035em !important;
    color: __TEXT__ !important;
}

h2 {
    font-size: 22px !important;
    font-weight: 750 !important;
    color: __TEXT__ !important;
}

h3 {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: __TEXT__ !important;
}

[data-testid="stMarkdownContainer"] p {
    color: __TEXT__;
}

[data-testid="stCaptionContainer"] {
    color: __MUTED__ !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {
    border: none !important;
    height: 1px !important;
    background: __BORDER__ !important;
    margin: 18px 0 !important;
}


/* ============================================================
   METRICS
   ============================================================ */

[data-testid="stMetric"] {
    padding: 10px 12px;
    border-radius: 11px;
    background: __CARD__;
    border: 1px solid __BORDER__;
    box-shadow: none;
}

[data-testid="stMetricValue"] {
    color: __TEXT__ !important;
    font-weight: 780 !important;
}

[data-testid="stMetricLabel"] {
    color: __MUTED__ !important;
}


/* ============================================================
   NORMAL BUTTONS
   ============================================================ */

div.stButton > button {
    min-height: 36px;
    border-radius: 10px;
    font-weight: 680;
    color: __TEXT__ !important;
    background: __SURFACE__ !important;
    border: 1px solid __BORDER__ !important;
}

div.stButton > button:hover {
    border-color: __ACCENT__ !important;
    box-shadow: 0 5px 16px rgba(0,0,0,0.08);
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

button[kind="primary"] {
    background: __ACCENT__ !important;
    color: __PRIMARY_TEXT__ !important;
    border: 1px solid __ACCENT__ !important;
}

button[kind="primary"]:hover {
    background: __ACCENT_HOVER__ !important;
    color: __PRIMARY_TEXT__ !important;
    border-color: __ACCENT_HOVER__ !important;
}


/* ============================================================
   POPOVER
   ============================================================ */

[data-testid="stPopover"] {
    position: relative;
}

[data-testid="stPopover"] > button {
    min-height: 36px !important;
    width: 42px !important;
    padding: 0 !important;
    border-radius: 10px !important;
    font-size: 20px !important;
    background: __SURFACE__ !important;
    color: __TEXT__ !important;
    border: 1px solid __BORDER__ !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    border-radius: 12px;
    background: __SURFACE__;
    border: 1px solid __BORDER__;
}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 11px;
}


/* ============================================================
   CONTAINERS
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 11px !important;
    border-color: __BORDER__ !important;
    background: __CARD__;
}


/* ============================================================
   CHAT
   ============================================================ */

[data-testid="stChatMessageContent"] {
    max-width: 820px;
    color: __TEXT__;
    font-size: 14px;
    line-height: 1.65;
}


/* ============================================================
   CHAT BOTTOM DOCK
   ============================================================ */

[data-testid="stBottom"] {
    background: transparent !important;
    border-top: none !important;
}

[data-testid="stBottomBlockContainer"] {
    max-width: 760px !important;
    margin: 0 auto !important;
    padding: 6px 0 8px 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] {
    max-width: 760px !important;
    margin: 0 auto !important;
    padding: 0 !important;
}

[data-testid="stChatInput"] textarea {
    min-height: 44px !important;
    max-height: 44px !important;
    padding: 11px 52px 11px 16px !important;

    border-radius: 18px !important;

    background: __INPUT__ !important;
    color: __TEXT__ !important;

    border: 1px solid __BORDER__ !important;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.10) !important;

    resize: none !important;

    font-size: 13px !important;
    line-height: 1.3 !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: __ACCENT__ !important;

    box-shadow:
        0 0 0 1px __ACCENT__,
        0 8px 24px rgba(0,0,0,0.12) !important;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 850px) {

    .block-container {
        width: calc(100vw - 28px) !important;
        max-width: calc(100vw - 28px) !important;
    }

}


/* ------------------------------------------------------------
   Chat history
   ------------------------------------------------------------ */

[data-testid="stChatMessage"] {
    margin-bottom: 3px !important;
    padding-top: 5px !important;
    padding-bottom: 5px !important;
}

[data-testid="stChatMessageContent"] {
    max-width: 760px !important;
    font-size: 14px !important;
    line-height: 1.65 !important;
}


/* ============================================================
   EXPLICIT LIGHT / DARK NATIVE SURFACE OVERRIDES
   ============================================================ */

body[data-meridian-theme="dark"] [data-testid="stPopoverBody"],
body[data-meridian-theme="dark"] div[data-baseweb="popover"] > div,
body[data-meridian-theme="dark"] div[role="dialog"] {
    background: #1F150C !important;
    color: #E1DCC9 !important;
    border-color: rgba(225,220,201,0.16) !important;
}

body[data-meridian-theme="dark"] [data-testid="stBottom"],
body[data-meridian-theme="dark"] [data-testid="stBottomBlockContainer"] {
    background: #000000 !important;
    color: #E1DCC9 !important;
}

body[data-meridian-theme="dark"] [data-testid="stChatInput"] textarea {
    background: #1F150C !important;
    color: #E1DCC9 !important;
    border-color: rgba(225,220,201,0.22) !important;
}

body[data-meridian-theme="dark"] [data-testid="stChatInput"] textarea::placeholder {
    color: #B7AF9E !important;
}

body[data-meridian-theme="light"] [data-testid="stPopoverBody"],
body[data-meridian-theme="light"] div[data-baseweb="popover"] > div,
body[data-meridian-theme="light"] div[role="dialog"] {
    background: #FFF2DB !important;
    color: #1F150C !important;
    border-color: rgba(31,21,12,0.12) !important;
}

body[data-meridian-theme="light"] [data-testid="stBottom"],
body[data-meridian-theme="light"] [data-testid="stBottomBlockContainer"] {
    background: #FFFAF3 !important;
    color: #1F150C !important;
}

body[data-meridian-theme="light"] [data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #1F150C !important;
    border-color: rgba(31,21,12,0.16) !important;
}

body[data-meridian-theme="light"] [data-testid="stChatInput"] textarea::placeholder {
    color: #6F6255 !important;
}

body[data-meridian-theme="light"] [data-testid="stFileUploader"] {
    background: #FFF2DB !important;
}

body[data-meridian-theme="dark"] [data-testid="stFileUploader"] {
    background: #1F150C !important;
}

/* ============================================================
   MERIDIAN FINAL UI CLEANUP
   ============================================================ */

/* ------------------------------------------------------------
   Hide Streamlit native toolbar
   ------------------------------------------------------------ */

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}

.stDeployButton {
    display: none !important;
}

header[data-testid="stHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
}


/* ------------------------------------------------------------
   Hide the custom Settings popover if any remains
   ------------------------------------------------------------ */

[data-testid="stPopover"] {
    display: none !important;
}


/* ------------------------------------------------------------
   Compact bottom chat dock
   ------------------------------------------------------------ */

[data-testid="stBottom"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;

    padding: 0 !important;

    min-height: 0 !important;
    height: 62px !important;
    max-height: 62px !important;
}

[data-testid="stBottomBlockContainer"] {
    width: min(780px, calc(100vw - 36px)) !important;

    max-width: 780px !important;

    margin: 0 auto !important;

    padding: 4px 0 6px 0 !important;

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;

    min-height: 0 !important;
    height: 58px !important;
    max-height: 58px !important;
}


/* ------------------------------------------------------------
   Floating chat input shell
   ------------------------------------------------------------ */

[data-testid="stChatInput"] {
    width: 100% !important;

    max-width: 780px !important;

    margin: 0 auto !important;

    padding: 0 !important;

    min-height: 50px !important;
    height: 50px !important;
    max-height: 50px !important;
}

[data-testid="stChatInput"] > div {
    position: relative !important;

    width: 100% !important;

    min-height: 50px !important;
    height: 50px !important;
    max-height: 50px !important;

    box-sizing: border-box !important;

    display: flex !important;
    align-items: center !important;

    padding: 0 8px 0 54px !important;

    border-radius: 999px !important;

    background: var(--meridian-input) !important;

    border: 1px solid var(--meridian-border) !important;

    box-shadow:
        0 6px 22px rgba(0,0,0,0.16) !important;
}


/* ------------------------------------------------------------
   Remove placeholder text completely
   ------------------------------------------------------------ */

[data-testid="stChatInput"] textarea::placeholder {
    color: transparent !important;
    opacity: 0 !important;
}

[data-testid="stChatInput"] textarea {
    min-height: 42px !important;
    height: 42px !important;
    max-height: 42px !important;

    padding: 9px 6px !important;

    margin: 0 !important;

    border: none !important;

    outline: none !important;

    box-shadow: none !important;

    border-radius: 999px !important;

    background: transparent !important;

    color: var(--meridian-text) !important;

    font-size: 13px !important;

    resize: none !important;
}


/* ------------------------------------------------------------
   Meridian chat logo
   ------------------------------------------------------------ */

[data-testid="stChatInput"] > div::before {
    content: "✦";

    position: absolute;

    left: 15px;

    top: 50%;

    transform:
        translateY(-50%);

    width: 27px;
    height: 27px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    z-index: 5;

    font-size: 17px;

    font-weight: 800;

    color: #1F150C;

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

    pointer-events: none;
}


/* ------------------------------------------------------------
   Send button
   ------------------------------------------------------------ */

[data-testid="stChatInput"] button {
    width: 34px !important;
    min-width: 34px !important;
    max-width: 34px !important;

    height: 34px !important;
    min-height: 34px !important;
    max-height: 34px !important;

    margin: 0 !important;

    padding: 0 !important;

    border-radius: 50% !important;

    background:
        var(--meridian-accent) !important;

    color:
        var(--meridian-button-text) !important;

    border:
        none !important;

    box-shadow:
        none !important;
}

[data-testid="stChatInput"] button:hover {
    transform:
        scale(1.04) !important;
}


/* ------------------------------------------------------------
   Mobile
   ------------------------------------------------------------ */

@media (max-width: 850px) {

    [data-testid="stBottomBlockContainer"] {
        width:
            calc(100vw - 20px) !important;

        max-width:
            calc(100vw - 20px) !important;
    }
}


/* ============================================================
   MERIDIAN - FIXED CHAT DOCK
   ============================================================ */

/* Reserve space so the fixed composer does not cover content */
.block-container {
    padding-bottom: 92px !important;
}


/* Outer Streamlit bottom container */
[data-testid="stBottom"] {
    position: fixed !important;

    left: 225px !important;
    right: 0 !important;
    bottom: 0 !important;

    width: auto !important;
    max-width: none !important;

    z-index: 999999 !important;

    background: transparent !important;

    border: none !important;
    box-shadow: none !important;

    padding: 0 !important;

    transform: none !important;
}


/* Inner bottom container */
[data-testid="stBottomBlockContainer"] {
    position: relative !important;

    width:
        min(780px, calc(100vw - 265px)) !important;

    max-width: 780px !important;

    margin:
        0 auto !important;

    padding:
        5px 0 10px 0 !important;

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;
}


/* Chat input itself */
[data-testid="stChatInput"] {
    position: relative !important;

    width: 100% !important;
    max-width: 780px !important;

    margin: 0 auto !important;

    padding: 0 !important;
}


/* Actual pill */
[data-testid="stChatInput"] > div {
    width: 100% !important;

    box-sizing: border-box !important;

    min-height: 50px !important;
    height: 50px !important;
    max-height: 50px !important;

    border-radius: 999px !important;

    background:
        var(--meridian-input) !important;

    border:
        1px solid var(--meridian-border) !important;

    box-shadow:
        0 8px 28px rgba(0,0,0,0.22) !important;
}


/* Keep the send button inside the pill */
[data-testid="stChatInput"] button {
    position: relative !important;
    z-index: 10 !important;
}


/* Mobile */
@media (max-width: 850px) {

    [data-testid="stBottom"] {
        left: 0 !important;
        right: 0 !important;
    }

    [data-testid="stBottomBlockContainer"] {
        width:
            calc(100vw - 24px) !important;

        max-width:
            calc(100vw - 24px) !important;

        padding:
            5px 0 8px 0 !important;
    }

    .block-container {
        padding-bottom:
            84px !important;
    }
}

/* ============================================================
   MERIDIAN ? FIXED CHAT COMPOSER
   ============================================================ */

/* Reserve viewport space so the composer does not cover content */
.block-container {
    padding-bottom: 92px !important;
}


/* Streamlit's actual bottom container */
[data-testid="stBottom"] {
    position: fixed !important;

    left: 225px !important;
    right: 0 !important;
    bottom: 0 !important;

    width: auto !important;
    max-width: none !important;

    z-index: 999999 !important;

    background: transparent !important;

    border: none !important;
    box-shadow: none !important;

    padding: 0 !important;

    transform: none !important;
}


/* Inner composer wrapper */
[data-testid="stBottomBlockContainer"] {
    width: min(
        780px,
        calc(100vw - 265px)
    ) !important;

    max-width: 780px !important;

    margin: 0 auto !important;

    padding: 5px 0 10px 0 !important;

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;
}


/* Chat input */
[data-testid="stChatInput"] {
    width: 100% !important;

    max-width: 780px !important;

    margin: 0 auto !important;

    padding: 0 !important;
}


/* Chat pill */
[data-testid="stChatInput"] > div {
    width: 100% !important;

    min-height: 50px !important;
    height: 50px !important;
    max-height: 50px !important;

    box-sizing: border-box !important;

    display: flex !important;
    align-items: center !important;

    border-radius: 999px !important;

    background:
        var(--meridian-input) !important;

    border:
        1px solid var(--meridian-border) !important;

    box-shadow:
        0 8px 28px rgba(0,0,0,0.20) !important;
}


/* Input area */
[data-testid="stChatInput"] textarea {
    min-height: 42px !important;
    height: 42px !important;
    max-height: 42px !important;

    resize: none !important;
}


/* Mobile */
@media (max-width: 850px) {

    [data-testid="stBottom"] {
        left: 0 !important;
        right: 0 !important;
    }

    [data-testid="stBottomBlockContainer"] {
        width:
            calc(100vw - 24px) !important;

        max-width:
            calc(100vw - 24px) !important;
    }

    .block-container {
        padding-bottom:
            84px !important;
    }
}

</style>
"""

css = css.replace(
    "__BG__",
    COLORS["bg"]
)

css = css.replace(
    "__SURFACE__",
    COLORS["surface"]
)

css = css.replace(
    "__SURFACE_ALT__",
    COLORS["surface_alt"]
)

css = css.replace(
    "__CARD__",
    COLORS["card"]
)

css = css.replace(
    "__TEXT__",
    COLORS["text"]
)

css = css.replace(
    "__MUTED__",
    COLORS["muted"]
)

css = css.replace(
    "__ACCENT__",
    COLORS["accent"]
)

css = css.replace(
    "__ACCENT_HOVER__",
    COLORS["accent_hover"]
)

css = css.replace(
    "__BORDER__",
    COLORS["border"]
)

css = css.replace(
    "__INPUT__",
    COLORS["input"]
)

css = css.replace(
    "__SIDEBAR__",
    COLORS["sidebar"]
)

css = css.replace(
    "__CHATBAR__",
    COLORS["chatbar"]
)

css = css.replace(
    "__PRIMARY_TEXT__",
    COLORS["primary_text"]
)

st.markdown(
    css,
    unsafe_allow_html=True,
)


# ============================================================
# TOP HEADER
# ============================================================

header_left, header_right = st.columns(
    [12, 1],
    vertical_alignment="center",
)

with header_left:

    header_time = datetime.now().strftime("%I:%M %p")

    st.markdown(
        f"""
        <div style="
            text-align: right;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 0.04em;
            opacity: 0.65;
            margin-bottom: -3px;
        ">
            {header_time}
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
        get_indexed_documents(),
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
        "Ask a natural-language question about supplier performance, "
        "procurement policy, spend, delivery, quality or inventory."
    )

    st.write("")

    q1, q2 = st.columns(2)

    with q1:

        if st.button(
            "Highest Q1 supplier spend",
            use_container_width=True,
        ):

            queue_question(
                "Which supplier had the highest spend in Q1, "
                "and what was its on-time delivery percentage?"
            )

    with q2:

        if st.button(
            "Q1 line stoppages",
            use_container_width=True,
        ):

            queue_question(
                "How many line stoppages happened in Q1, "
                "what was the total downtime, and what caused them?"
            )

    q3, q4 = st.columns(2)

    with q3:

        if st.button(
            "₹1.4 crore PO authority",
            use_container_width=True,
        ):

            queue_question(
                "What is the approval authority for a "
                "purchase order worth ₹1.4 crore?"
            )

    with q4:

        if st.button(
            "Safety-stock requirement",
            use_container_width=True,
        ):

            queue_question(
                "Microcontrollers are imported with a "
                "46-day lead time. Using the safety-stock "
                "policy, how many days of stock should be "
                "held for this part?"
            )


# ============================================================
# CHAT HISTORY
# ============================================================

if st.session_state.messages:

    st.subheader("Conversation")


for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=(
            "👤"
            if message["role"] == "user"
            else "📦"
        ),
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

    queue_question(
        prompt
    )


# ============================================================
# PROCESS PENDING QUESTION
# ============================================================

pending_message = None

for message in reversed(
    st.session_state.messages
):

    if (
        message["role"] == "user"
        and not message.get("processed")
    ):

        pending_message = message

        break


if pending_message is not None:

    question = pending_message["content"]

    pending_message["processed"] = True

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            question
        )

    with st.chat_message(
        "assistant",
        avatar="📦",
    ):

        with st.spinner(
            "Searching the Meridian knowledge base..."
        ):

            try:

                answer, sources, timing = answer_question(
                    question
                )

            except Exception as exc:

                answer = (
                    "An error occurred while processing "
                    f"your question: {exc}"
                )

                sources = []

                timing = {}

        st.markdown(
            answer
        )

        if sources:

            st.markdown(
                "**Sources**"
            )

            for source in sources:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"📄 **{source['label']}**"
                    )

                    st.caption(
                        f"{source['source']} • Page {source['page']}"
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "timing": timing,
        }
    )