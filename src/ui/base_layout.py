import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: #5865F2 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background: #e8eded !important;
                padding: 2.5rem !important;
                border-radius: 1.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background: #ADD8E6 !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');

            /*
            #MainMenu,
            footer,
            header {
                visibility: hidden;
            }

            .block-container {
                padding-top: 1.5rem !important;
            }
            */

            h1, h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: #111112 !important;
            }

            h3, h4, p {
                font-family: 'Outfit', sans-serif !important;
            }

            /* Secondary Button */
            .stButton button[kind="secondary"],
            .stButton button[data-testid="stBaseButton-secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            /* Primary Button */
            .stButton button[kind="primary"],
            .stButton button[data-testid="stBaseButton-primary"] {
                border-radius: 1.5rem !important;
                background-color: #2563EB !important;
                color: white !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            /* Tertiary Button */
            .stButton button[kind="tertiary"],
            .stButton button[data-testid="stBaseButton-tertiary"] {
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                border: none !important;
                box-shadow: none !important;
                transition: transform 0.2s ease-in-out,
                            background-color 0.2s ease-in-out !important;
            }

            /* Hover Effect */
            .stButton button[kind="primary"]:hover,
            .stButton button[kind="secondary"]:hover,
            .stButton button[kind="tertiary"]:hover,
            .stButton button[data-testid="stBaseButton-primary"]:hover,
            .stButton button[data-testid="stBaseButton-secondary"]:hover,
            .stButton button[data-testid="stBaseButton-tertiary"]:hover {
                transform: scale(1.05);
            }

            /* Tertiary Hover */
            
        </style>
    """, unsafe_allow_html=True)