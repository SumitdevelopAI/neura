import streamlit as st
from datetime import datetime
# Assuming api.py exists in your directory
from api import create_chat, get_chat

# Page configuration
st.set_page_config(
    page_title="Neural Ledger",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GEMINI-INSPIRED CSS ---
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

<style>
    /* Global Settings */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #f0f4f9;
        border-right: none;
    }
    
    /* Sidebar New Chat Button */
    [data-testid="stSidebar"] .stButton button {
        background-color: #dde3ea;
        color: #1f1f1f;
        border: none;
        border-radius: 24px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 14px;
        width: 100%;
        text-align: left;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #cdd6e0;
        color: #000;
    }

    /* HEADER */
    .app-header {
        padding: 1rem 0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .logo-text {
        font-size: 22px;
        font-weight: 600;
        background: linear-gradient(90deg, #4285F4, #9B72CB, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* CHAT MESSAGES */
    .chat-container {
        margin-bottom: 80px; /* Space for the bottom input bar */
    }

    /* Message Bubbles */
    .user-msg-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }
    
    .user-bubble {
        background-color: #f0f4f9;
        color: #1f1f1f;
        padding: 12px 20px;
        border-radius: 24px;
        max-width: 80%;
        font-size: 16px;
        line-height: 1.5;
    }

    .ai-msg-container {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
    }
    
    .ai-icon {
        color: #4285F4;
        margin-top: 4px;
    }
    
    .ai-text {
        color: #1f1f1f;
        font-size: 16px;
        line-height: 1.6;
        padding-top: 2px;
    }

    /* EMPTY STATE */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 60vh;
        text-align: center;
        opacity: 0.8;
    }
    
    .empty-state h3 {
        font-weight: 500;
        font-size: 24px;
        margin-top: 10px;
        background: linear-gradient(90deg, #4285F4, #D96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### New Conversation")
    
    # Input for creating a specific named chat
    new_chat_title = st.text_input("Topic", placeholder="Chat Topic...", label_visibility="collapsed")
    
    if st.button("＋ Create New Chat"):
        if new_chat_title.strip():
            try:
                chat = create_chat(new_chat_title)
                st.session_state.chat_id = chat["id"]
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    if st.session_state.chat_id:
        st.caption(f"Active Chat ID: {st.session_state.chat_id}")
        if st.button("Reset / Clear"):
            st.session_state.chat_id = None
            st.rerun()

# --- MAIN CONTENT ---
col1, col2, col3 = st.columns([1, 10, 1])

with col2:
    # Header
    st.markdown("""
        <div class='app-header'>
            <span class="material-icons-outlined" style="font-size: 28px; color: #4285F4;">auto_awesome</span>
            <span class="logo-text">Neural Ledger</span>
        </div>
    """, unsafe_allow_html=True)

    # Chat Logic
    if st.session_state.chat_id:
        try:
            chat = get_chat(st.session_state.chat_id)
            messages = chat.get("messages", [])
            
            if messages:
                for msg in messages:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    
                    if role == "user":
                        st.markdown(f"""
                            <div class="user-msg-container">
                                <div class="user-bubble">{content}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="ai-msg-container">
                                <span class="material-icons-outlined ai-icon">auto_awesome</span>
                                <div class="ai-text">{content}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                 st.markdown("""
                    <div class='empty-state'>
                        <h3>Hello, human</h3>
                        <p style="color: #666;">I'm ready to help.</p>
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error loading chat: {e}")
    else:
        # Welcome Screen (No ID selected)
        st.markdown("""
            <div class='empty-state'>
                <span class="material-icons-outlined" style="font-size: 48px; color: #4285F4;">psychology</span>
                <h3>Welcome to Neural Ledger</h3>
                <p style="color: #666;">Type a message below to start.</p>
            </div>
        """, unsafe_allow_html=True)

# --- INPUT AREA (Fixed at bottom) ---
# st.chat_input handles the sticky bottom bar automatically
user_query = st.chat_input("Enter a prompt here")

if user_query:
    if not st.session_state.chat_id:
        # If no chat exists, create one automatically
        try:
            # Create a generic chat or use the first message as title
            chat = create_chat(user_query[:30]) 
            st.session_state.chat_id = chat["id"]
            # Ideally, you would also post the message to the API here
            # e.g., post_message(chat['id'], user_query)
            st.rerun()
        except Exception as e:
            st.error(f"Could not create chat: {e}")
    else:
        # If chat exists, handle sending the message
        # e.g., post_message(st.session_state.chat_id, user_query)
        st.write(f"User sent: {user_query}") # Placeholder for your API logic