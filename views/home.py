"""
GameVerse Home Page - Redesigned
Clean, modern layout with integrated action buttons
"""

import streamlit as st
from utils.helpers import add_to_cart, add_to_wishlist, format_price
from data.games_data import get_featured_games, get_free_games


def render(games_df):
    """Render the redesigned home page"""
    
    # Featured Games Section
    st.markdown('<div class="section-header">Featured Games</div>', unsafe_allow_html=True)
    
    featured = get_featured_games(games_df, n=3)
    
    cols = st.columns(3)
    for idx, (_, game) in enumerate(featured.iterrows()):
        with cols[idx]:
            render_featured_game_card(game.to_dict(), idx)
    
    # Special Offers Section
    st.markdown("---")
    st.markdown('<div class="section-header">Special Offers</div>', unsafe_allow_html=True)
    
    free_games = get_free_games(games_df)
    if not free_games.empty:
        cols = st.columns(min(len(free_games), 4))
        for idx, (_, game) in enumerate(free_games.iterrows()):
            with cols[idx]:
                render_free_game_card(game.to_dict(), idx)
    
    # Information Cards
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="stat-card-modern">
            <h3 style="color: #fafafa; margin-bottom: 1rem; font-size: 1.25rem;">Welcome to GameVerse</h3>
            <p style="color: #a1a1aa; font-size: 0.875rem; line-height: 1.6;">
                Discover thousands of games, from indie gems to AAA blockbusters.
                Get personalized recommendations from our AI assistant.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card-modern">
            <h3 style="color: #fafafa; margin-bottom: 1rem; font-size: 1.25rem;">Quick Actions</h3>
            <p style="color: #a1a1aa; font-size: 0.875rem; line-height: 1.6;">
                Browse our catalog, chat with our AI assistant for recommendations,
                or check out today's deals and discounts.
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_featured_game_card(game, idx):
    """
    Render a modern featured game card with integrated buttons
    
    Design notes:
    - Image at top for visual hierarchy
    - Title and description in content area
    - Price prominently displayed
    - Action buttons integrated within card, not external
    - Consistent spacing and sizing
    """
    
    # Card container
    st.markdown('<div class="game-card-modern">', unsafe_allow_html=True)
    
    # Image
    try:
        st.image(game.get('image_url', ''), use_container_width=True, output_format="auto")
    except:
        st.markdown("""
        <div class="game-card-image" style="display: flex; align-items: center; justify-content: center; color: #71717a;">
            No Image Available
        </div>
        """, unsafe_allow_html=True)
    
    # Content section
    st.markdown('<div class="game-card-content">', unsafe_allow_html=True)
    
    # Title
    st.markdown(f'<div class="game-card-title">{game["title"]}</div>', unsafe_allow_html=True)
    
    # Description (truncated)
    description = game.get('description', '')[:100] + '...'
    st.markdown(f'<div class="game-card-description">{description}</div>', unsafe_allow_html=True)
    
    # Price
    price_text = format_price(game['price'])
    st.markdown(f'<div class="game-card-price">{price_text}</div>', unsafe_allow_html=True)
    
    # Action buttons - INTEGRATED within card
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Add to Cart", key=f"cart_feat_{idx}_{game['id']}", use_container_width=True):
            if add_to_cart(game):
                st.success("✓ Added", icon="✅")
            else:
                st.info("Already in cart")
    
    with col2:
        if st.button("Wishlist", key=f"wish_feat_{idx}_{game['id']}", use_container_width=True):
            if add_to_wishlist(game):
                st.success("✓ Saved", icon="❤️")
            else:
                st.info("Already saved")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close content
    st.markdown('</div>', unsafe_allow_html=True)  # Close card


def render_free_game_card(game, idx):
    """Render a compact card for free games"""
    
    st.markdown(f"""
    <div class="stat-card-modern" style="text-align: left;">
        <div style="color: #10b981; font-weight: 700; font-size: 1.125rem; margin-bottom: 0.5rem;">
            FREE
        </div>
        <div style="color: #fafafa; font-weight: 600; margin-bottom: 0.5rem;">
            {game['title']}
        </div>
        <div style="color: #a1a1aa; font-size: 0.75rem;">
            {game['category']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Get Now", key=f"free_{idx}_{game['id']}", use_container_width=True):
        if add_to_cart(game):
            st.success("✓ Added to cart")
        else:
            st.info("Already in cart")