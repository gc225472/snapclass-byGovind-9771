import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: #5865F2 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 1.5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>
            .stApp {
                 background: #E0E3FF !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');

            #MainMenu,
            footer,
            header {
                visibility: hidden;
            }

            .block-container {
                padding-top: 1.5rem !important;
            }

            h1,
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: #0F172A !important;
            }

            
            h3,
            h4,
            p {
                font-family: 'Outfit', sans-serif !important;
            }

            /* Secondary Button */
            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            /* Primary Button */
            button[kind="primary"] {
                border-radius: 1.5rem !important;
                background-color: #2563EB !important;
                color: white !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            /* Tertiary Button */
            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: transparent !important;
                color: #5865F2 !important;
                border: none !important;
                transition: transform 0.2s ease-in-out !important;
            }

            /* Hover Effect */
            button[kind="primary"]:hover,
            button[kind="secondary"]:hover,
            button[kind="tertiary"]:hover {
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)