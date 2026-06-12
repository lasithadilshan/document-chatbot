import os
# Must be set before importing sentence_transformers / tokenizers / torch
# to prevent segmentation faults caused by:
#   1. Rust tokenizers forking threads inside Streamlit's process model
#   2. OpenMP spawning threads that conflict with fork()
#   3. PyTorch MPS (Metal) backend holding GPU memory across forks
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"

import streamlit as st
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore
from chat_handler import ChatHandler
from datetime import datetime

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DocChat AI — Smart Document Assistant",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Premium custom CSS
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* ── Google Fonts ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════════════════════════════════════
   LIGHT MODE (default)
   ══════════════════════════════════════════════════════════════════════ */
:root {
    /* Accent palette */
    --accent: #6C5CE7;
    --accent-light: #a29bfe;
    --accent-dark: #4834d4;
    --accent-bg: rgba(108,92,231,0.1);

    /* Surfaces - Dynamic but tinted to avoid pure white */
    --surface: color-mix(in srgb, var(--background-color) 97%, var(--accent-dark));
    --surface-alt: color-mix(in srgb, var(--secondary-background-color) 95%, var(--accent-dark));
    --surface-raised: color-mix(in srgb, var(--background-color) 94%, var(--accent-dark));
    --surface-hover: color-mix(in srgb, var(--background-color) 95%, var(--text-color) 5%);

    /* Text - Dynamic based on Streamlit Theme */
    --text-primary: var(--text-color);
    --text-secondary: color-mix(in srgb, var(--text-color) 70%, transparent);
    --text-muted: color-mix(in srgb, var(--text-color) 45%, transparent);
    --text-on-accent: #ffffff;

    /* Borders - Dynamic based on Streamlit Theme */
    --border: color-mix(in srgb, var(--text-color) 15%, transparent);
    --border-light: color-mix(in srgb, var(--text-color) 8%, transparent);

    /* Semantic */
    --success: #00b894;
    --success-bg: rgba(0,184,148,0.1);
    --warning: #fdcb6e;
    --danger: #e17055;

    /* Effects */
    --gradient-1: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 100%);
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.2);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;

    /* Chat */
    --chat-user-bg: rgba(108,92,231,0.08);
    --chat-user-border: rgba(108,92,231,0.12);
    --chat-assistant-bg: var(--surface);
    --chat-assistant-border: var(--border-light);

    /* Onboarding */
    --card-bg: var(--surface);
    --card-border: var(--border-light);
    --step-bg: var(--surface-alt);
    --step-border: var(--border-light);

    /* Expander */
    --expander-header-bg: rgba(108,92,231,0.08);
    --expander-header-color: var(--accent-light);
    --expander-bg: var(--surface);
    --expander-border: var(--border-light);
}

/* ── Global ────────────────────────────────────────────────────────────── */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: var(--surface-alt) !important;
}

/* ── Sidebar (always dark) ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1d2e 0%, #2d3250 100%) !important;
    border-right: none !important;
    box-shadow: var(--shadow-lg);
}
[data-testid="stSidebar"] * {
    color: #e2e5f0 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 1rem 0 !important;
}
[data-testid="stSidebar"] .sidebar-section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.4) !important;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

/* File uploader inside sidebar */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-md) !important;
    border: 1px dashed rgba(255,255,255,0.15) !important;
    padding: 0.75rem !important;
    transition: border-color 0.2s, background 0.2s;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: var(--accent-light) !important;
    background: rgba(108,92,231,0.08) !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    transition: transform 0.15s, box-shadow 0.15s;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] section > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(108,92,231,0.4);
}

/* ── Sidebar buttons ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: var(--gradient-1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 8px rgba(108,92,231,0.25);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108,92,231,0.4) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"],
[data-testid="stSidebar"] .stButton > button:not([kind]) {
    background: rgba(255,255,255,0.07) !important;
    color: #e2e5f0 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: background 0.2s, border-color 0.2s, transform 0.15s;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
[data-testid="stSidebar"] .stButton > button:not([kind]):hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: var(--accent-light) !important;
    transform: translateY(-1px);
}

/* ── Sidebar metrics ───────────────────────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem !important;
    border: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: var(--accent-light) !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: rgba(255,255,255,0.55) !important;
}
/* Sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: rgba(255,255,255,0.45) !important;
}

/* ── Main content ──────────────────────────────────────────────────────── */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}

/* ── Hero header card ──────────────────────────────────────────────────── */
.hero-card {
    background: var(--gradient-1);
    border-radius: var(--radius-xl);
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(108,92,231,0.2);
}
.hero-card::before {
    content: '';
    position: absolute;
    right: -40px; top: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.hero-card::after {
    content: '';
    position: absolute;
    right: 60px; bottom: -30px;
    width: 120px; height: 120px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-card h1 {
    margin: 0 0 0.3rem 0;
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #fff !important;
}
.hero-card p {
    margin: 0;
    opacity: 0.88;
    font-size: 0.95rem;
    font-weight: 400;
    line-height: 1.5;
    color: #fff !important;
}
.hero-card .badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(8px);
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    color: #fff !important;
}

/* ── Onboarding card ───────────────────────────────────────────────────── */
.onboarding-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    box-shadow: var(--shadow-sm);
}
.onboarding-card h3 {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
}

/* Step cards */
.step-row {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
@media (max-width: 768px) {
    .step-row { flex-wrap: wrap; }
    .step-card { min-width: 45%; }
}
.step-card {
    flex: 1;
    background: var(--step-bg);
    border: 1px solid var(--step-border);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.step-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}
.step-card .step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px; height: 32px;
    border-radius: 50%;
    background: var(--gradient-1);
    color: #fff;
    font-weight: 700;
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
}
.step-card .step-icon {
    font-size: 1.5rem;
    margin-bottom: 0.4rem;
}
.step-card h4 {
    margin: 0 0 0.25rem 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
}
.step-card p {
    margin: 0;
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* ── Chat area ─────────────────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: var(--chat-assistant-bg) !important;
    border: 1px solid var(--chat-assistant-border) !important;
    border-radius: var(--radius-md) !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.6rem !important;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s;
}
[data-testid="stChatMessage"]:hover {
    box-shadow: var(--shadow-md);
}
/* User messages accent tint */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--chat-user-bg) !important;
    border-color: var(--chat-user-border) !important;
}
/* Ensure chat text is always readable */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] div {
    color: var(--text-primary) !important;
}

/* Chat input */
[data-testid="stChatInput"] > div {
    border-radius: var(--radius-md) !important;
    border: 2px solid var(--border) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    background: var(--surface) !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-bg) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
}

/* ── Expander (Sources) ────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--expander-header-color) !important;
    border-radius: var(--radius-sm) !important;
    background: var(--expander-header-bg) !important;
    padding: 0.5rem 0.75rem !important;
}
[data-testid="stExpander"] {
    border: 1px solid var(--expander-border) !important;
    border-radius: var(--radius-sm) !important;
    background: var(--expander-bg) !important;
}
[data-testid="stExpander"] p,
[data-testid="stExpander"] span {
    color: var(--text-secondary) !important;
}

/* ── Alerts ────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    font-size: 0.88rem !important;
    border: none !important;
}

/* ── Progress bar ──────────────────────────────────────────────────────── */
.stProgress > div > div {
    background: var(--gradient-1) !important;
    border-radius: 999px !important;
}

/* ── File chips in sidebar ─────────────────────────────────────────────── */
.file-chip {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: var(--radius-sm);
    padding: 0.4rem 0.65rem;
    margin-bottom: 0.35rem;
    font-size: 0.8rem;
    color: #e2e5f0 !important;
    transition: background 0.2s;
}
.file-chip:hover {
    background: rgba(255,255,255,0.1);
}
.file-chip .file-icon { font-size: 1rem; }
.file-chip .file-name {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.file-chip .file-badge {
    font-size: 0.65rem;
    text-transform: uppercase;
    background: rgba(108,92,231,0.25);
    padding: 0.1rem 0.4rem;
    border-radius: 4px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #c8c3ff !important;
}

/* ── Status dot ────────────────────────────────────────────────────────── */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 0.4rem;
    animation: pulse-dot 2s ease-in-out infinite;
}
.status-dot.active { background: #55efc4; }
.status-dot.inactive { background: rgba(255,255,255,0.3); animation: none; }
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Suggested question buttons ────────────────────────────────────────── */
.suggested-q-btn {}
[data-testid="stSidebar"] .suggested-q-btn button {
    text-align: left !important;
    font-size: 0.82rem !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: var(--radius-sm) !important;
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    transition: background 0.2s, border-color 0.2s;
}
[data-testid="stSidebar"] .suggested-q-btn button:hover {
    background: rgba(108,92,231,0.15) !important;
    border-color: rgba(162,155,254,0.4) !important;
}

/* ── Main-area buttons ─────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: var(--gradient-1) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease, box-shadow 0.2s ease;
    box-shadow: 0 2px 8px rgba(108,92,231,0.25);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(108,92,231,0.4) !important;
}

/* ── Hide footer only, keep menu for theme switching ───────────────────── */
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
}
</style>
"""




# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def initialize_session_state():
    """Initialize session state variables."""
    defaults = {
        "vector_store": None,
        "chat_history": [],
        "documents_processed": False,
        "processed_files": [],
        "suggested_questions": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# UI Components
# ---------------------------------------------------------------------------
def render_hero():
    """Render the hero / header card."""
    st.markdown(
        """
        <div class="hero-card">
            <div class="badge">AI-Powered Document Analysis</div>
            <h1>💎 DocChat AI</h1>
            <p>Upload your documents and start an intelligent conversation — powered by
            Llama 3.1 &amp; FAISS vector search.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_onboarding():
    """Render the getting-started steps when no documents are loaded."""
    st.markdown(
        """
        <div class="onboarding-card">
            <h3>Get started in 4 easy steps</h3>
            <div class="step-row">
                <div class="step-card">
                    <div class="step-icon">📂</div>
                    <div class="step-num">1</div>
                    <h4>Upload</h4>
                    <p>Drag &amp; drop PDF, DOCX, or TXT files into the sidebar.</p>
                </div>
                <div class="step-card">
                    <div class="step-icon">⚙️</div>
                    <div class="step-num">2</div>
                    <h4>Process</h4>
                    <p>Click <strong>Process Documents</strong> to index your content.</p>
                </div>
                <div class="step-card">
                    <div class="step-icon">💬</div>
                    <div class="step-num">3</div>
                    <h4>Ask</h4>
                    <p>Type any question about your documents below.</p>
                </div>
                <div class="step-card">
                    <div class="step-icon">📖</div>
                    <div class="step-num">4</div>
                    <h4>Verify</h4>
                    <p>Expand <strong>Sources</strong> to see the original excerpts.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(api_key: str, chat_handler: "ChatHandler"):
    """Build the full sidebar UI and return uploaded files."""
    with st.sidebar:
        # ── Branding ──
        st.markdown(
            "<h2 style='text-align:center; margin-bottom:0;'>💎 DocChat AI</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; font-size:0.75rem; opacity:0.5; margin-top:0;'>"
            "Smart Document Assistant</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        # ── Upload section ──
        st.markdown(
            '<p class="sidebar-section-label">📄 Document Upload</p>',
            unsafe_allow_html=True,
        )
        uploaded_files = st.file_uploader(
            "Drop files here",
            accept_multiple_files=True,
            type=["pdf", "docx", "txt"],
            help="Supported: PDF, DOCX, TXT — up to 200 MB each",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns(2)
        with col1:
            process_clicked = st.button(
                "⚡ Process", type="primary", use_container_width=True
            )
        with col2:
            clear_clicked = st.button(
                "🗑️ Clear", type="secondary", use_container_width=True
            )

        if process_clicked:
            if uploaded_files:
                process_documents(uploaded_files, chat_handler)
            else:
                st.warning("Upload files first.")
        if clear_clicked:
            clear_all_data()

        st.divider()

        # ── Document status ──
        st.markdown(
            '<p class="sidebar-section-label">📋 Status</p>',
            unsafe_allow_html=True,
        )
        render_document_status()

        st.divider()

        # ── Analytics in sidebar ──
        st.markdown(
            '<p class="sidebar-section-label">📊 Analytics</p>',
            unsafe_allow_html=True,
        )
        render_analytics()

        # ── Quick actions ──
        if st.session_state.documents_processed:
            st.divider()
            st.markdown(
                '<p class="sidebar-section-label">💡 Quick Actions</p>',
                unsafe_allow_html=True,
            )
            if st.button("✨ Suggest Questions", use_container_width=True):
                generate_suggested_questions(chat_handler)

            if st.session_state.suggested_questions:
                render_suggested_questions()

    return uploaded_files


def render_document_status():
    """Display processed-files list with styled chips."""
    if st.session_state.documents_processed:
        st.markdown(
            '<span class="status-dot active"></span> <strong>Ready</strong>',
            unsafe_allow_html=True,
        )
        if st.session_state.processed_files:
            for fname in st.session_state.processed_files:
                ext = fname.rsplit(".", 1)[-1].upper() if "." in fname else "FILE"
                icon = {"PDF": "📕", "DOCX": "📘", "TXT": "📄"}.get(ext, "📄")
                st.markdown(
                    f'<div class="file-chip">'
                    f'<span class="file-icon">{icon}</span>'
                    f'<span class="file-name">{fname}</span>'
                    f'<span class="file-badge">{ext}</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

        if hasattr(st.session_state, "processing_info"):
            total_chunks = sum(
                info["chunks"] for info in st.session_state.processing_info
            )
            total_chars = sum(
                info["characters"] for info in st.session_state.processing_info
            )
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Chunks", total_chunks)
            with c2:
                st.metric("Chars", f"{total_chars:,}")
    else:
        st.markdown(
            '<span class="status-dot inactive"></span> No documents loaded',
            unsafe_allow_html=True,
        )


def render_analytics():
    """Display chat / vector-store analytics."""
    if st.session_state.documents_processed:
        total = len(st.session_state.chat_history)
        questions = len(
            [m for m in st.session_state.chat_history if m["role"] == "user"]
        )
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Messages", total)
        with c2:
            st.metric("Questions", questions)

        if st.session_state.vector_store:
            stats = st.session_state.vector_store.get_stats()
            st.metric("Index Size", stats["total_chunks"])
    else:
        st.caption("Process documents to unlock analytics.")


def render_suggested_questions():
    """Display suggested questions as styled buttons."""
    for i, question in enumerate(st.session_state.suggested_questions):
        st.markdown('<div class="suggested-q-btn">', unsafe_allow_html=True)
        if st.button(
            f"❓ {question}", key=f"suggested_{i}", use_container_width=True
        ):
            st.session_state.chat_history.append(
                {"role": "user", "content": question}
            )
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Chat interface
# ---------------------------------------------------------------------------
def render_chat(chat_handler: "ChatHandler"):
    """Full chat area — history + input."""
    if not st.session_state.documents_processed:
        render_onboarding()
        return

    # History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📖 View sources"):
                    for idx, source in enumerate(message["sources"]):
                        st.caption(f"**Source {idx + 1}:** {source}")

    # Input
    if prompt := st.chat_input("Ask anything about your documents…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                context_chunks = st.session_state.vector_store.search(prompt, k=5)
                response = chat_handler.generate_response(prompt, context_chunks)

                st.markdown(response)

                if context_chunks:
                    sources = []
                    with st.expander("📖 Sources Used", expanded=False):
                        for i, (chunk, score, metadata) in enumerate(
                            context_chunks[:3]
                        ):
                            source_name = metadata.get("source", "Unknown")
                            st.caption(
                                f"**Source {i + 1}** — *{source_name}* "
                                f"(relevance {score:.0%})"
                            )
                            st.markdown(
                                f"<small style='color:var(--text-secondary)'>"
                                f"{chunk[:300]}{'…' if len(chunk) > 300 else ''}"
                                f"</small>",
                                unsafe_allow_html=True,
                            )
                            sources.append(
                                f"{source_name} — relevance {score:.0%}"
                            )
                            if i < 2:
                                st.divider()

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": response,
                            "sources": sources,
                        }
                    )
                else:
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response}
                    )


# ---------------------------------------------------------------------------
# Document processing
# ---------------------------------------------------------------------------
def process_documents(uploaded_files, chat_handler):
    """Process uploaded documents with progress feedback."""
    processor = DocumentProcessor()
    all_chunks = []
    processed_files = []
    processing_info = []

    progress_bar = st.progress(0, text="Preparing…")

    for i, uploaded_file in enumerate(uploaded_files):
        progress_bar.progress(
            (i) / len(uploaded_files),
            text=f"Reading {uploaded_file.name}…",
        )
        text = processor.process_uploaded_file(uploaded_file)

        if text:
            chunks = processor.chunk_text(text)
            for j, chunk in enumerate(chunks):
                _ = {
                    "source": uploaded_file.name,
                    "chunk_id": j,
                    "file_type": uploaded_file.name.rsplit(".", 1)[-1].lower(),
                    "processed_at": datetime.now().isoformat(),
                }
            all_chunks.extend(chunks)
            processed_files.append(uploaded_file.name)
            processing_info.append(
                {
                    "file": uploaded_file.name,
                    "chunks": len(chunks),
                    "characters": len(text),
                }
            )

        progress_bar.progress((i + 1) / len(uploaded_files), text="Indexing…")

    if all_chunks:
        st.session_state.vector_store.clear()
        metadata_list = [
            {"source": info["file"], "chunk_id": ci}
            for info in processing_info
            for ci in range(info["chunks"])
        ]
        success = st.session_state.vector_store.add_documents(
            all_chunks, metadata_list
        )

        if success:
            st.session_state.documents_processed = True
            st.session_state.processed_files = processed_files
            st.session_state.processing_info = processing_info
            st.session_state.chat_history = []
            progress_bar.progress(1.0, text="✅ Done!")
            st.success(
                f"Successfully processed **{len(processed_files)}** file(s) "
                f"into **{len(all_chunks)}** searchable chunks."
            )
        else:
            st.error("Failed to process documents. Please try again.")
    else:
        st.error("No content could be extracted from the uploaded files.")


def generate_suggested_questions(chat_handler):
    """Generate suggested questions from document content."""
    if not st.session_state.documents_processed:
        return

    with st.spinner("Generating questions…"):
        sample_chunks = st.session_state.vector_store.search(
            "summary main topics", k=3
        )

        if not sample_chunks and st.session_state.vector_store.texts:
            sample_chunks = [
                (text, 1.0, {"source": f"Document {i + 1}"})
                for i, text in enumerate(st.session_state.vector_store.texts[:3])
            ]

        if sample_chunks:
            questions = chat_handler.suggest_questions(sample_chunks)
            st.session_state.suggested_questions = questions
            if questions:
                st.success(f"Generated {len(questions)} questions!")
            else:
                st.warning("Could not generate questions — try more documents.")
        else:
            st.warning("No content available for question generation.")


def clear_all_data():
    """Reset all application state."""
    if st.session_state.vector_store:
        st.session_state.vector_store.clear()

    st.session_state.documents_processed = False
    st.session_state.processed_files = []
    st.session_state.chat_history = []
    st.session_state.suggested_questions = []

    if hasattr(st.session_state, "processing_info"):
        del st.session_state.processing_info

    st.toast("🗑️ All data cleared!", icon="✅")
    st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    load_dotenv()
    api_key = os.getenv("HUGGINGFACE_API_KEY", "").strip()

    if not api_key:
        st.error(
            "🔑 **Hugging Face API key not found.** "
            "Set `HUGGINGFACE_API_KEY` in your `.env` file."
        )
        st.info("Get a key → https://huggingface.co/settings/tokens")
        st.stop()

    initialize_session_state()

    if st.session_state.vector_store is None:
        st.session_state.vector_store = VectorStore(api_key)

    chat_handler = ChatHandler(api_key)

    # ── Layout ──
    render_hero()
    render_sidebar(api_key, chat_handler)
    render_chat(chat_handler)


if __name__ == "__main__":
    main()
