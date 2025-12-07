"""
GameVerse Helper Functions - Redesigned
Modern UI components with clean styling
"""

import streamlit as st
import re


def init_session_state():
    """Initialize session state variables"""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'wishlist' not in st.session_state:
        st.session_state.wishlist = []
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'chatbot_messages' not in st.session_state:
        st.session_state.chatbot_messages = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def render_header():
    """Render the modern minimal header"""
    st.markdown("""
    <div class="main-header">
        <h1>GAMEVERSE</h1>
        <p>Your Ultimate Digital Game Store</p>
    </div>
    """, unsafe_allow_html=True)


def render_navigation():
    """
    Render compact minimalist sidebar navigation
    
    Design notes:
    - Beautiful icons for visual clarity
    - Compact spacing throughout
    - Full-width buttons
    - Dark blue hover (#1e3a8a)
    - White text on hover
    
    Returns:
        str: The key of the selected page
    """
    
    pages = {
        "🏠  Home": "home",
        "🎮  Browse Games": "browse",
        "🛒  My Cart": "cart",
        "💙  Wishlist": "wishlist",
        "👤  Profile": "profile",
        "📊  Analytics": "analytics",
        "🤖  AI Assistant": "chatbot"
    }
    
    selected_page = st.sidebar.radio(
        "Navigation",
        list(pages.keys()),
        label_visibility="collapsed"
    )
    
    # Quick stats section - compact
    st.sidebar.markdown('<div style="margin: 1.25rem 0 0.625rem 0; padding-top: 1rem; border-top: 1px solid #27272a;"></div>', unsafe_allow_html=True)
    st.sidebar.markdown("### Stats")
    
    # Compact metrics
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Cart", len(st.session_state.cart))
    with col2:
        st.metric("Wishlist", len(st.session_state.wishlist))
    
    st.sidebar.metric("AI Queries", st.session_state.chatbot_messages)
    
    return pages[selected_page]


def add_to_cart(game):
    """Add a game to the shopping cart"""
    game_ids = [g['id'] for g in st.session_state.cart]
    if game['id'] not in game_ids:
        st.session_state.cart.append(game)
        return True
    return False


def add_to_wishlist(game):
    """Add a game to the wishlist"""
    game_ids = [g['id'] for g in st.session_state.wishlist]
    if game['id'] not in game_ids:
        st.session_state.wishlist.append(game)
        return True
    return False


def remove_from_cart(index):
    """Remove a game from cart by index"""
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)
        return True
    return False


def remove_from_wishlist(index):
    """Remove a game from wishlist by index"""
    if 0 <= index < len(st.session_state.wishlist):
        st.session_state.wishlist.pop(index)
        return True
    return False


def calculate_cart_total():
    """Calculate total price of items in cart"""
    return sum(game['price'] for game in st.session_state.cart)


def format_price(price):
    """Format price for display"""
    return "FREE" if price == 0 else f"${price:.2f}"


def render_game_card(game, context="browse"):
    """
    Render a modern game card for browse/list views
    
    Design notes:
    - Horizontal layout for list views
    - Image on left, content on right
    - Actions integrated within card
    - Clean, scannable design
    """
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            st.image(game.get('image_url', ''), use_container_width=True)
        except:
            st.markdown("""
            <div style="background: #27272a; 
                        padding: 3rem; 
                        border-radius: 8px; 
                        text-align: center;
                        color: #71717a;
                        font-size: 0.75rem;">
                No Image
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### {game['title']}")
        st.markdown(f"**{format_price(game['price'])}** · {game['category']}")
        st.markdown(f"<p style='color: #a1a1aa; font-size: 0.875rem;'>{game['description'][:120]}...</p>", unsafe_allow_html=True)
        
        # Action buttons
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Add to Cart", key=f"cart_{context}_{game['id']}", use_container_width=True):
                if add_to_cart(game):
                    st.success("✓ Added to cart")
                else:
                    st.info("Already in cart")
        
        with col_b:
            if st.button("Wishlist", key=f"wish_{context}_{game['id']}", use_container_width=True):
                if add_to_wishlist(game):
                    st.success("✓ Added to wishlist")
                else:
                    st.info("Already in wishlist")