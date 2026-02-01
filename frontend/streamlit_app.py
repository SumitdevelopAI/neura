import streamlit as st
import time
import uuid

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="Neural Ledger",
    page_icon="static/favicon.png", # Use a local file or standard emoji if needed
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- IMPORT API ----------------
try:
    from api import create_chat, send_message, get_messages
except ImportError:
    st.error("⚠️ 'api.py' not found.")
    st.stop()

# ---------------- CSS (Minimal & Clean) ----------------
st.markdown("""
<style>
    /* 1. Global Font - System Standard */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. Google-style Loading Animation */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        margin-left: 0px; 
        padding: 8px 0;
    }
    .dot {
        width: 6px;
        height: 6px;
        margin: 0 3px;
        background-color: #5f6368;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    .dot:nth-child(1) { animation-delay: -0.32s; background-color: #4285F4; } /* Blue */
    .dot:nth-child(2) { animation-delay: -0.16s; background-color: #EA4335; } /* Red */
    .dot:nth-child(3) { animation-delay: 0s;     background-color: #FBBC05; } /* Yellow */
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }

    /* 3. Sidebar Polish */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    /* 4. Chat Bubble Spacing */
    .stChatMessage {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "chat_history_list" not in st.session_state:
    st.session_state.chat_history_list = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- LOGIC ----------------

def stream_text(text):
    """Smooth text streaming"""
    if not text: text = "..."
    for i in range(0, len(text), 3):
        yield text[i:i+3]
        time.sleep(0.008)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("Neural Ledger")
    
    if st.button("＋ New Conversation", type="primary", use_container_width=True):
        st.session_state.current_chat_id = None
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Recent")
    if st.session_state.chat_history_list:
        for chat in reversed(st.session_state.chat_history_list):
            if st.button(chat['title'][:25], key=chat['id'], use_container_width=True):
                st.session_state.current_chat_id = chat['id']
                # Load msgs logic
                try:
                    msgs = get_messages(chat['id'], st.session_state.user_id)
                    st.session_state.messages = msgs if isinstance(msgs, list) else []
                except:
                    st.session_state.messages = []
                st.rerun()

# ---------------- MAIN CHAT ----------------

# 1. MESSAGES DISPLAY
# Note: By NOT passing the 'avatar=' argument, Streamlit uses its 
# standard, professional vector icons automatically.
if st.session_state.messages:
    for msg in st.session_state.messages:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        
        with st.chat_message(role):
            st.markdown(content)

# 2. EMPTY STATE
else:
    st.markdown("""
    <div style="text-align: center; margin-top: 15vh; opacity: 0.6;">
        <h2 style="font-weight: 500;">How can I help you today?</h2>
    </div>
    """, unsafe_allow_html=True)

# 3. INPUT HANDLING
prompt = st.chat_input("Message Neural Ledger...")

if prompt:
    # A. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # B. Init Chat ID (Lazy)
    if not st.session_state.current_chat_id:
        try:
            new_chat = create_chat(prompt[:30])
            st.session_state.current_chat_id = new_chat["id"]
            st.session_state.chat_history_list.append(new_chat)
        except:
            st.stop()

    # C. Assistant Response
    with st.chat_message("assistant"):
        # The loading animation inside the bubble
        placeholder = st.empty()
        placeholder.markdown("""
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            # API Call
            api_response = send_message(
                chat_id=st.session_state.current_chat_id,
                user_id=st.session_state.user_id,
                content=prompt
            )

            # Smart Content Extraction
            final_content = ""
            if isinstance(api_response, list) and api_response:
                final_content = api_response[-1].get("content", "")
            elif isinstance(api_response, dict):
                 if api_response.get("role") == "assistant":
                    final_content = api_response.get("content", "")
                 elif api_response.get("role") == "user":
                    updated = get_messages(st.session_state.current_chat_id, st.session_state.user_id)
                    if updated: final_content = updated[-1]["content"]

            # Output
            if final_content:
                placeholder.write_stream(stream_text(final_content))
                st.session_state.messages.append({"role": "assistant", "content": final_content})
            else:
                placeholder.error("No response.")

        except Exception:
            placeholder.error("Connection failed.")