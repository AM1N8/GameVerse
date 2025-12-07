"""
GameVerse Styling Module
Modern minimal design inspired by Steam/Xbox Store
"""

import streamlit as st


def load_custom_css():
    """Load modern minimal CSS with clean design principles"""
    st.markdown("""
    <style>
    /* ========================================
       GLOBAL FOUNDATION
       ======================================== */
    
    .stApp {
        background: #0e0e10;
        color: #e4e4e7;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* ========================================
       TYPOGRAPHY
       ======================================== */
    
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* ========================================
       HEADER - Clean & Minimal
       ======================================== */
    
    .main-header {
        background: #18181b;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2.5rem;
        border: 1px solid #27272a;
    }
    
    .main-header h1 {
        color: #fafafa;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
        letter-spacing: -0.03em;
    }
    
    .main-header p {
        color: #a1a1aa;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* ========================================
       SIDEBAR - Compact Minimalist Navigation
       ======================================== */
    
    [data-testid="stSidebar"] {
        background: #18181b;
        border-right: 1px solid #27272a;
        padding: 0.5rem 0.5rem;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }
    
    /* Style radio buttons as compact nav buttons */
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 6px;
        padding: 0.625rem 0.75rem;
        margin: 0;
        cursor: pointer;
        transition: all 0.15s ease;
        color: #a1a1aa;
        font-weight: 500;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
        width: 100%;
        gap: 0.625rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: #1e3a8a;
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] > div:first-child {
        display: none; /* Hide radio circle */
    }
    
    /* Active navigation item */
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: #3b82f6;
        color: #ffffff;
        border-color: #3b82f6;
    }
    
    /* Icon styling within sidebar */
    [data-testid="stSidebar"] .nav-icon {
        font-size: 1.125rem;
        line-height: 1;
        min-width: 1.125rem;
        text-align: center;
    }
    
    /* Sidebar metrics styling - compact */
    [data-testid="stSidebar"] .stMetric {
        background: #27272a;
        padding: 0.625rem 0.75rem;
        border-radius: 6px;
        border: 1px solid #3f3f46;
    }
    
    [data-testid="stSidebar"] .stMetric label {
        color: #a1a1aa;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"] {
        color: #fafafa;
        font-size: 1.25rem;
        font-weight: 600;
    }
    
    /* Compact sidebar sections */
    [data-testid="stSidebar"] h3 {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #71717a;
        margin: 1rem 0 0.5rem 0.75rem;
        font-weight: 600;
    }
    
    /* Remove extra spacing */
    [data-testid="stSidebar"] .element-container {
        margin: 0;
    }
    
    /* ========================================
       GAME CARDS - Featured & Browse
       ======================================== */
    
    .game-card-modern {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .game-card-modern:hover {
        border-color: #3b82f6;
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(59, 130, 246, 0.15);
    }
    
    .game-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        background: #27272a;
    }
    
    .game-card-content {
        padding: 1.25rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    .game-card-title {
        color: #fafafa;
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    .game-card-description {
        color: #a1a1aa;
        font-size: 0.875rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        flex-grow: 1;
    }
    
    .game-card-price {
        color: #10b981;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .game-card-actions {
        display: flex;
        gap: 0.5rem;
        margin-top: auto;
    }
    
    /* ========================================
       BUTTONS - Modern Minimal Style
       ======================================== */
    
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.625rem 1.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #2563eb;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Secondary button variant */
    .stButton.secondary > button {
        background: transparent;
        border: 1px solid #52525b;
        color: #e4e4e7;
    }
    
    .stButton.secondary > button:hover {
        background: #27272a;
        border-color: #71717a;
    }
    
    /* ========================================
       INPUT FIELDS - Clean & Modern
       ======================================== */
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: #18181b;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        color: #fafafa;
        padding: 0.625rem 0.875rem;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #71717a;
    }
    
    /* ========================================
       TAGS - Minimal Badge Style
       ======================================== */
    
    .game-tag-modern {
        background: #27272a;
        color: #e4e4e7;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid #3f3f46;
    }
    
    /* ========================================
       STATS CARDS - Clean Information Display
       ======================================== */
    
    .stat-card-modern {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .stat-card-modern:hover {
        border-color: #3f3f46;
    }
    
    .stat-number-modern {
        font-size: 2rem;
        font-weight: 700;
        color: #fafafa;
        margin-bottom: 0.5rem;
    }
    
    .stat-label-modern {
        color: #a1a1aa;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* ========================================
       CHAT INTERFACE - Clean Message Design
       ======================================== */
    
    .stChatMessage {
        background: #18181b;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: #1e3a5f;
        border-color: #2563eb;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: #18181b;
        border-color: #3f3f46;
    }
    
    /* ========================================
       SECTIONS & CONTAINERS
       ======================================== */
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #fafafa;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #27272a;
    }
    
    /* ========================================
       SCROLLBAR - Minimal Design
       ======================================== */
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #18181b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3f3f46;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #52525b;
    }
    
    /* ========================================
       RESPONSIVE ADJUSTMENTS
       ======================================== */
    
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .game-card-image {
            height: 160px;
        }
        
        .stat-number-modern {
            font-size: 1.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)