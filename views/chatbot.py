"""
GameVerse AI Chatbot - FIXED POLLING
Uses reliable polling instead of hanging streams for instant responses.
"""

import streamlit as st
import time
from utils.botpress_client import BotpressClient 
import re


def render(games_df):
    """Render the chatbot page with proper HTML rendering."""
    st.markdown("## AI Game Assistant")
    st.markdown("Ask me anything about games, get recommendations, or browse our catalog!")
    
    # 1. Initialize Client
    client = get_or_create_client()
    if client is None:
        st.error("⚠️ Chatbot not configured. Please set up your Botpress credentials.")
        return
    
    # 2. Authenticate User
    try:
        user = client.get_user()
        if "error" in user:
            st.error(f"Failed to authenticate: {user['error']}")
            return
        user_id = user["user"]["id"]
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return
    
    # 3. Initialize Global State
    initialize_global_state(client)
    
    # 4. Render Selector
    render_conversation_selector(client)
    
    st.markdown("---")
    
    # 5. Get Current Conversation ID
    conversation_id = st.session_state.active_conversation
    
    # 6. Ensure History is Loaded
    if conversation_id not in st.session_state.conversation_history:
        with st.spinner("Loading history..."):
            messages = fetch_messages_from_api(client, conversation_id, user_id)
            st.session_state.conversation_history[conversation_id] = messages
            
    # 7. Display Messages
    current_messages = st.session_state.conversation_history[conversation_id]
    
    for message in current_messages:
        with st.chat_message(message["role"]):
            if contains_html(message["content"]):
                st.markdown(message["content"], unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
    
    # 8. Handle Input
    handle_chat_input(client, conversation_id, user_id)


def contains_html(text):
    """Check if text contains HTML tags"""
    html_pattern = re.compile(r'<[^>]+>')
    return bool(html_pattern.search(text))


@st.cache_resource
def get_or_create_client():
    """Create and cache Botpress client."""
    try:
        api_id = st.secrets.get("CHAT_API_ID")
        user_key = st.secrets.get("users", [{}])[0].get("key") 
        if not api_id or not user_key:
            return None
        return BotpressClient(api_id=api_id, user_key=user_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {str(e)}")
        return None


def initialize_global_state(client):
    """Initialize history and load conversation list."""
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = {}
    if "conversations_loaded" not in st.session_state:
        st.session_state.conversations_loaded = False
    
    if not st.session_state.conversations_loaded:
        conversations_data = client.list_conversations()
        conversations = conversations_data.get("conversations", [])
        if not conversations:
            res = client.create_conversation()
            if "conversation" in res:
                conversations = [res["conversation"]]
        
        st.session_state.conversations = conversations
        st.session_state.conversations_loaded = True
        
        if conversations and "active_conversation" not in st.session_state:
            st.session_state.active_conversation = conversations[0]["id"]


def render_conversation_selector(client):
    """Render selector."""
    conversations = st.session_state.get("conversations", [])
    if not conversations: return
    
    conversation_ids = [conv["id"] for conv in conversations]
    col1, col2 = st.columns([5, 1])
    
    with col1:
        current_id = st.session_state.get("active_conversation")
        try:
            current_index = conversation_ids.index(current_id)
        except (ValueError, IndexError):
            current_index = 0
        
        selected_id = st.selectbox(
            "Select Conversation",
            options=conversation_ids,
            index=current_index,
            format_func=lambda x: f"Conversation {conversation_ids.index(x) + 1}",
            key="conversation_selector"
        )
        if selected_id != current_id:
            st.session_state.active_conversation = selected_id
            st.rerun()
    
    with col2:
        st.markdown("<div style='height: 1.9em'></div>", unsafe_allow_html=True)
        if st.button("➕ New"):
            create_new_conversation(client)


def create_new_conversation(client):
    """Create new conversation."""
    res = client.create_conversation()
    if "conversation" in res:
        new_conv = res["conversation"]
        cid = new_conv["id"]
        st.session_state.conversations.append(new_conv)
        st.session_state.conversation_history[cid] = []
        st.session_state.active_conversation = cid
        st.rerun()


def fetch_messages_from_api(client, conversation_id, user_id):
    """Fetch messages and format."""
    try:
        messages_data = client.list_messages(conversation_id, limit=50)
        messages = messages_data.get("messages", [])
        chat_messages = []
        for message in reversed(messages):
            role = "user" if message.get("userId") == user_id else "assistant"
            text = message.get("payload", {}).get("text", "")
            if text:
                chat_messages.append({"role": role, "content": text})
        return chat_messages
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return []


def handle_chat_input(client, conversation_id, user_id):
    """Handle input, send message, and POLL for response."""
    if prompt := st.chat_input("Ask me about games..."):
        
        # 1. Update LOCAL cache (User message)
        user_msg = {"role": "user", "content": prompt}
        st.session_state.conversation_history[conversation_id].append(user_msg)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 2. Send to Botpress
        try:
            client.create_message(prompt, conversation_id=conversation_id)
        except Exception as e:
            st.error(f"Failed to send: {e}")
            return
        
        # 3. Poll for Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Poll for up to 10 seconds (20 checks)
                for _ in range(20):
                    time.sleep(0.5)
                    
                    # Fetch latest messages, BYPASSING CACHE
                    messages_data = client.list_messages(conversation_id, limit=5, ignore_cache=True)
                    messages = messages_data.get("messages", [])
                    
                    if messages:
                        # API returns newest first. Check the latest message.
                        last_msg = messages[0]
                        
                        # Verify it's from the bot and it's new (not the user message we just sent)
                        if last_msg.get("userId") != user_id:
                            
                            text = last_msg.get("payload", {}).get("text", "")
                            
                            # Update LOCAL cache (Assistant message)
                            bot_msg = {"role": "assistant", "content": text}
                            st.session_state.conversation_history[conversation_id].append(bot_msg)
                            
                            if "chatbot_messages" not in st.session_state:
                                st.session_state.chatbot_messages = 0
                            st.session_state.chatbot_messages += 1
                            
                            # Rerun immediately to show the new state
                            st.rerun()
                            return
                            
                st.warning("⚠️ No response received within timeout.")