import streamlit as st


def footer_home():
    logo_url = "https://i.ibb.co/rGQdVNJh/Chat-GPT-Image-Oct-7-2026-12-40-10-AM.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content: center;
            align-items: center;
            margin-top: 2rem;
        ">
        <p> Create with ❤️ by </p>
            <img src="{logo_url}" style="max-height: 35px;">
        </div>
    """, unsafe_allow_html=True)