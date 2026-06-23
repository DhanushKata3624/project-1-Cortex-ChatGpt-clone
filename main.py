import streamlit as st

from services.get_models_list import get_ollama_models_list
from services.get_title import get_chat_title
from services.chat_utilities import get_answer
from db.conversations import (
    create_new_conversation,
    add_message,
    get_conversation,
    get_all_conversations,
)

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="CORTEX",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CUSTOM CSS  — all the visual magic lives here
# =====================================================================
st.markdown(
    """
<style>
/* ---- Import a clean modern font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

/* ---- Animated gradient background ---- */
.stApp {
    background: linear-gradient(-45deg, #0f0c29, #1a1a2e, #16213e, #0f3460);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    font-family: 'Inter', sans-serif;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ---- Hide default Streamlit chrome (but KEEP the sidebar reopen arrow) ---- */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}
/* keep the collapsed-sidebar control clickable & visible */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    z-index: 999999;
}
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="collapsedControl"] button {
    background: rgba(123, 47, 247, 0.35) !important;
    border: 1px solid rgba(0, 210, 255, 0.5) !important;
    border-radius: 10px !important;
    color: #fff !important;
    box-shadow: 0 0 14px rgba(123, 47, 247, 0.4);
}

/* ---- Hero title ---- */
.cortex-hero {
    text-align: center;
    margin: 0.5rem 0 1.5rem 0;
}
.cortex-hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.4rem;
    font-weight: 700;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #00d2ff, #7b2ff7, #f72585, #00d2ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shine 6s linear infinite;
    margin-bottom: 0.2rem;
}
@keyframes shine {
    to { background-position: 300% center; }
}
.cortex-hero p {
    color: #9aa5c4;
    font-size: 0.95rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-weight: 300;
}

/* ---- Glass card wrapper for the model selector area ---- */
.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

/* ---- Selectbox styling ---- */
div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(123, 47, 247, 0.4) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(12px);
    color: #e6e9f5 !important;
    transition: all 0.3s ease;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(0, 210, 255, 0.7) !important;
    box-shadow: 0 0 18px rgba(0, 210, 255, 0.25);
}
label, .stSelectbox label {
    color: #b8c1e0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

/* ---- Chat bubbles ---- */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 0.4rem 0.6rem;
    margin: 0.5rem 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.25);
    animation: fadeUp 0.45s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"] p {
    color: #e9ecf7 !important;
    font-size: 1.02rem;
    line-height: 1.6;
}

/* ---- Chat input ---- */
[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(123, 47, 247, 0.5);
    border-radius: 16px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 24px rgba(123, 47, 247, 0.2);
}
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.75);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(123, 47, 247, 0.25);
}
[data-testid="stSidebar"] h2 {
    font-family: 'Space Grotesk', sans-serif;
    background: linear-gradient(90deg, #00d2ff, #f72585);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.4rem;
}

/* ---- Buttons ---- */
.stButton > button {
    width: 100%;
    background: rgba(255, 255, 255, 0.04);
    color: #d7ddf0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0.55rem 0.9rem;
    font-weight: 500;
    text-align: left;
    transition: all 0.25s ease;
    margin-bottom: 0.35rem;
}
.stButton > button:hover {
    background: linear-gradient(90deg, rgba(123,47,247,0.25), rgba(0,210,255,0.2));
    border-color: rgba(0, 210, 255, 0.6);
    color: #ffffff;
    transform: translateX(4px);
    box-shadow: 0 0 16px rgba(0, 210, 255, 0.2);
}

/* ---- New Chat button (primary look) ---- */
[data-testid="stSidebar"] .stButton:first-of-type > button {
    background: linear-gradient(90deg, #7b2ff7, #f72585);
    color: #fff;
    border: none;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 18px rgba(247, 37, 133, 0.35);
}
[data-testid="stSidebar"] .stButton:first-of-type > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(247, 37, 133, 0.5);
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(#7b2ff7, #00d2ff);
    border-radius: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# HERO HEADER
# =====================================================================
st.markdown(
    """
<div class="cortex-hero">
    <h1>🧠 CORTEX</h1>
    <p>Your Private AI Companion</p>
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================================
# MODELS
# =====================================================================
if "OLLAMA_MODELS" not in st.session_state:
    st.session_state.OLLAMA_MODELS = get_ollama_models_list()

selected_model = st.selectbox("⚙️ Select Model", st.session_state.OLLAMA_MODELS)

# =====================================================================
# SESSION STATE
# =====================================================================
st.session_state.setdefault("conversation_id", None)
st.session_state.setdefault("conversation_title", None)
st.session_state.setdefault("chat_history", [])  # [{role, content}]

# =====================================================================
# SIDEBAR: CONVERSATIONS
# =====================================================================
with st.sidebar:
    st.header("💬 Chat History")
    conversations = get_all_conversations()  # {conv_id: title}

    if st.button("➕  New Chat"):
        st.session_state.conversation_id = None
        st.session_state.conversation_title = None
        st.session_state.chat_history = []

    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    if not conversations:
        st.markdown(
            "<p style='color:#6b739a; font-size:0.85rem; text-align:center;'>"
            "No conversations yet.<br>Start chatting below 👇</p>",
            unsafe_allow_html=True,
        )

    for cid, title in conversations.items():
        is_current = cid == st.session_state.conversation_id
        # clean + shorten any messy title for display
        clean = (title or "Untitled").strip().strip('"').strip("'")
        for prefix in ("Task:", "Summary:", "Title:"):
            if clean.lower().startswith(prefix.lower()):
                clean = clean[len(prefix):].strip()
        if len(clean) > 32:
            clean = clean[:32].rstrip() + "…"
        label = f"🔹 {clean}" if is_current else f"💭 {clean}"
        if st.button(label, key=f"conv_{cid}"):
            doc = get_conversation(cid) or {}
            st.session_state.conversation_id = cid
            st.session_state.conversation_title = doc.get("title", "Untitled")
            st.session_state.chat_history = [
                {"role": m["role"], "content": m["content"]}
                for m in doc.get("messages", [])
            ]

# =====================================================================
# EMPTY-STATE WELCOME (only when no messages yet)
# =====================================================================
if not st.session_state.chat_history:
    st.markdown(
        """
<div style="text-align:center; margin-top:2.5rem; opacity:0.85;">
    <div style="font-size:3rem;">✨</div>
    <h3 style="color:#c3cbe8; font-family:'Space Grotesk',sans-serif; font-weight:500;">
        How can I help you today?
    </h3>
    <p style="color:#7e87ad;">Pick a model above and ask me anything.</p>
</div>
""",
        unsafe_allow_html=True,
    )

# =====================================================================
# SHOW CHAT SO FAR
# =====================================================================
for msg in st.session_state.chat_history:
    avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# =====================================================================
# CHAT INPUT
# =====================================================================
user_query = st.chat_input("Ask CORTEX anything...")
if user_query:
    # 1) Show + store user message in UI state
    st.chat_message("user", avatar="🧑‍💻").markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # 2) Persist to DB (create convo on first message, else append)
    if st.session_state.conversation_id is None:
        try:
            title = get_chat_title(selected_model, user_query) or "New Chat"
        except Exception:
            title = "New Chat"
        conv_id = create_new_conversation(title=title, role="user", content=user_query)
        st.session_state.conversation_id = conv_id
        st.session_state.conversation_title = title
    else:
        add_message(st.session_state.conversation_id, "user", user_query)

    # 3) Get assistant response (direct service)
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Cortex is thinking..."):
            try:
                assistant_text = get_answer(selected_model, st.session_state.chat_history)
            except Exception as e:
                assistant_text = f"[Error getting response: {e}]"
        st.markdown(assistant_text)

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_text})

    # 4) Persist assistant message
    if st.session_state.conversation_id:
        add_message(st.session_state.conversation_id, "assistant", assistant_text)