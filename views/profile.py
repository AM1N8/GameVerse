"""
GameVerse User Profile Page - Enhanced
Complete profile management with stats and edit functionality
"""

import streamlit as st
from datetime import datetime


def render(games_df):
    """Render the enhanced user profile page"""
    
    # Initialize user profile if not exists
    if st.session_state.user is None:
        init_default_user()
    
    st.markdown('<div class="section-header">User Profile</div>', unsafe_allow_html=True)
    
    # Profile header section
    render_profile_header()
    
    st.markdown("---")
    
    # Statistics section
    render_profile_stats()
    
    st.markdown("---")
    
    # Edit profile section
    render_edit_profile()
    
    st.markdown("---")
    
    # Purchase history section
    render_purchase_history()


def init_default_user():
    """Initialize default user profile"""
    st.session_state.user = {
        'username': 'GamerPro',
        'email': 'gamer@gameverse.com',
        'member_since': '2024',
        'total_spent': 0.0,
        'games_owned': 0,
        'avatar_url': 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400'
    }


def render_profile_header():
    """Render profile header with avatar and basic info"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        user = st.session_state.user
        try:
            st.image(
                user.get('avatar_url', 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=400'),
                width=200
            )
        except:
            st.markdown("""
            <div style="width: 200px; height: 200px; background: #27272a; 
                        border-radius: 12px; display: flex; align-items: center; 
                        justify-content: center; color: #71717a; font-size: 3rem;">
                👤
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        user = st.session_state.user
        st.markdown(f"### {user.get('username', 'Unknown User')}")
        st.markdown(f"📧 {user.get('email', 'No email')}")
        st.markdown(f"📅 Member since {user.get('member_since', 'Unknown')}")
        
        # Quick status
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 0.75rem; background: #18181b; 
                    border: 1px solid #27272a; border-radius: 8px;">
            <span style="color: #10b981; font-weight: 600;">● Active</span>
            <span style="color: #a1a1aa; margin-left: 1rem;">Account in good standing</span>
        </div>
        """, unsafe_allow_html=True)


def render_profile_stats():
    """Render profile statistics"""
    st.markdown("### 📊 Profile Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    user = st.session_state.user
    
    with col1:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-number-modern">${user.get('total_spent', 0.0):.2f}</div>
            <div class="stat-label-modern">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-number-modern">{user.get('games_owned', 0)}</div>
            <div class="stat-label-modern">Games Owned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card-modern">
            <div class="stat-number-modern">{len(st.session_state.wishlist)}</div>
            <div class="stat-label-modern">Wishlist Items</div>
        </div>
        """, unsafe_allow_html=True)


def render_edit_profile():
    """Render edit profile form"""
    st.markdown("### ⚙️ Edit Profile")
    
    user = st.session_state.user
    
    with st.form("profile_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input(
                "Username",
                value=user.get('username', ''),
                placeholder="Enter your username"
            )
        
        with col2:
            new_email = st.text_input(
                "Email",
                value=user.get('email', ''),
                placeholder="your.email@example.com"
            )
        
        # Avatar URL (optional)
        new_avatar = st.text_input(
            "Avatar URL (optional)",
            value=user.get('avatar_url', ''),
            placeholder="https://example.com/avatar.jpg"
        )
        
        col_submit, col_cancel = st.columns([1, 3])
        
        with col_submit:
            submitted = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )
        
        if submitted:
            # Update user profile
            st.session_state.user['username'] = new_username
            st.session_state.user['email'] = new_email
            if new_avatar:
                st.session_state.user['avatar_url'] = new_avatar
            
            st.success("✅ Profile updated successfully!")
            st.rerun()


def render_purchase_history():
    """Render purchase history section"""
    st.markdown("### 📋 Purchase History")
    
    user = st.session_state.user
    games_owned = user.get('games_owned', 0)
    
    if games_owned == 0:
        st.info("No purchases yet. Start shopping to build your library!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎮 Browse Games", use_container_width=True):
                st.info("Navigate to Browse Games from the sidebar!")
        
        with col2:
            if st.button("🏠 Go to Home", use_container_width=True):
                st.info("Navigate to Home from the sidebar!")
    
    else:
        st.markdown(f"""
        <div class="stat-card-modern" style="text-align: left;">
            <p style="color: #fafafa; font-size: 1rem; margin-bottom: 0.5rem;">
                You have purchased <strong>{games_owned}</strong> games.
            </p>
            <p style="color: #a1a1aa; font-size: 0.875rem;">
                Total lifetime spending: <strong style="color: #10b981;">${user.get('total_spent', 0.0):.2f}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Additional purchase history features
        with st.expander("📜 View Detailed Transaction History"):
            st.markdown("""
            **Recent Transactions:**
            
            Your complete transaction history will appear here, including:
            - Game title and purchase date
            - Transaction ID
            - Payment method
            - Refund eligibility status
            
            *This feature tracks all your purchases and allows you to request refunds 
            within 14 days if you've played less than 2 hours.*
            """)
        
        with st.expander("📥 Download Purchase Receipts"):
            st.markdown("""
            Download email receipts for any of your purchases:
            - PDF format invoices
            - Detailed pricing breakdown
            - Payment confirmation
            - Game license keys (where applicable)
            """)
        
        with st.expander("🔄 Request Refund"):
            st.markdown("""
            **Refund Policy:**
            
            You can request a refund for any game that meets ALL criteria:
            - ⏰ Purchased within the last **14 days**
            - 🎮 Less than **2 hours** of playtime
            
            **How to request:**
            1. Select the game from your purchase history
            2. Click "Request Refund"
            3. Provide a brief reason
            4. Submit request
            
            Refunds are processed within 3-5 business days.
            """)


def render_account_settings():
    """Render account settings section (optional expansion)"""
    st.markdown("### 🔒 Account Settings")
    
    with st.expander("🔐 Security Settings"):
        st.markdown("**Change Password**")
        
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Update Password"):
                if new_password == confirm_password:
                    st.success("✅ Password updated successfully!")
                else:
                    st.error("❌ Passwords do not match!")
    
    with st.expander("🔔 Notification Preferences"):
        st.checkbox("Email notifications for new game releases")
        st.checkbox("Wishlist price drop alerts")
        st.checkbox("Weekly game recommendations")
        st.checkbox("Promotional offers and discounts")
        
        if st.button("Save Preferences"):
            st.success("✅ Notification preferences saved!")
    
    with st.expander("🗑️ Account Management"):
        st.warning("**Danger Zone**")
        st.markdown("Permanently delete your account and all associated data.")
        
        if st.button("Delete Account", type="secondary"):
            st.error("This action cannot be undone. Please contact support to proceed.")