"""
GameVerse Browse Page - Redesigned
Clean filter interface with modern game cards
"""

import streamlit as st
from utils.helpers import add_to_cart, add_to_wishlist, format_price
from data.games_data import filter_games, get_categories


def render(games_df):
    """Render the browse page with modern filters"""
    
    st.markdown('<div class="section-header">Browse All Games</div>', unsafe_allow_html=True)
    
    # Modern filter controls
    render_filters(games_df)
    
    # Get filtered results
    filtered_df = apply_filters(games_df)
    
    # Display result count
    st.markdown(f"""
    <div style="color: #a1a1aa; font-size: 0.875rem; margin: 1rem 0;">
        Found <span style="color: #fafafa; font-weight: 600;">{len(filtered_df)}</span> games
    </div>
    """, unsafe_allow_html=True)
    
    # Display games
    if filtered_df.empty:
        st.info("No games found matching your criteria. Try adjusting the filters.")
    else:
        for _, game in filtered_df.iterrows():
            render_browse_game_card(game.to_dict())
            st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)


def render_filters(games_df):
    """Render modern filter interface"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text_input(
            "Search games",
            key="search_input",
            placeholder="Enter game title...",
            label_visibility="collapsed"
        )
    
    with col2:
        categories = ["All Categories"] + get_categories(games_df)
        st.selectbox(
            "Category",
            categories,
            key="category_filter",
            label_visibility="collapsed"
        )
    
    with col3:
        st.selectbox(
            "Price Range",
            ["All Prices", "Free", "Under $20", "$20-$40", "$40+"],
            key="price_filter",
            label_visibility="collapsed"
        )
    
    st.markdown('<div style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)


def apply_filters(games_df):
    """Apply filter selections to games dataframe"""
    search = st.session_state.get("search_input", "")
    category = st.session_state.get("category_filter", "All Categories")
    price_range = st.session_state.get("price_filter", "All Prices")
    
    # Adjust category name for filter function
    if category == "All Categories":
        category = "All"
    
    # Adjust price range name
    if price_range == "All Prices":
        price_range = "All"
    
    return filter_games(
        games_df,
        search=search,
        category=category,
        price_range=price_range
    )


def render_browse_game_card(game):
    """
    Render a game card optimized for browse view
    
    Design notes:
    - Horizontal layout for easy scanning
    - Image, title, price, description visible at once
    - Actions readily accessible
    - Consistent with overall modern aesthetic
    """
    
    # Card container
    st.markdown('<div class="game-card-modern" style="display: flex; flex-direction: row; overflow: visible;">', unsafe_allow_html=True)
    
    # Left side - Image
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            st.image(game.get('image_url', ''), use_container_width=True)
        except:
            st.markdown("""
            <div style="background: #27272a; 
                        height: 180px;
                        border-radius: 8px;
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        color: #71717a;
                        font-size: 0.75rem;">
                No Image
            </div>
            """, unsafe_allow_html=True)
    
    # Right side - Content
    with col2:
        # Title and price
        col_title, col_price = st.columns([3, 1])
        with col_title:
            st.markdown(f"### {game['title']}")
        with col_price:
            price_text = format_price(game['price'])
            st.markdown(f'<div class="game-card-price" style="text-align: right;">{price_text}</div>', unsafe_allow_html=True)
        
        # Metadata
        stars = "⭐" * int(game.get('rating', 0))
        st.markdown(f"""
        <div style="color: #a1a1aa; font-size: 0.875rem; margin-bottom: 0.75rem;">
            {game['category']} · {game['developer']} · {stars} ({game.get('rating', 0)})
        </div>
        """, unsafe_allow_html=True)
        
        # Description
        st.markdown(f"<p style='color: #a1a1aa; font-size: 0.875rem; line-height: 1.5;'>{game['description'][:180]}...</p>", unsafe_allow_html=True)
        
        # Tags
        tags_html = " ".join([
            f"<span class='game-tag-modern'>{tag}</span>" 
            for tag in game.get('tags', [])[:4]
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
        
        # Actions
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 1, 2])
        
        with col_a:
            if st.button("Add to Cart", key=f"cart_browse_{game['id']}", use_container_width=True):
                if add_to_cart(game):
                    st.success("✓ Added")
                else:
                    st.info("In cart")
        
        with col_b:
            if st.button("Wishlist", key=f"wish_browse_{game['id']}", use_container_width=True):
                if add_to_wishlist(game):
                    st.success("✓ Saved")
                else:
                    st.info("Saved")
        
        with col_c:
            if st.button("View Details", key=f"details_{game['id']}", use_container_width=True):
                show_game_details(game)
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_game_details(game):
    """Show detailed game information in an expander"""
    with st.expander("📋 Game Details", expanded=True):
        st.markdown(f"""
        **Full Description:**  
        {game['description']}
        
        **Game Information:**
        - **Category:** {game['category']}
        - **Developer:** {game['developer']}
        - **Release Date:** {game.get('release_date', 'N/A')}
        - **Rating:** {game.get('rating', 0)}/5.0
        
        **Tags:** {', '.join(game.get('tags', []))}
        """)