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
        <p style="font-weight:bold; color:white;"> Create with ❤️ by </p>
            <img src="{logo_url}" style="max-height: 35px;">
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    logo_url = "https://i.ibb.co/rGQdVNJh/Chat-GPT-Image-Oct-7-2026-12-40-10-AM.png"

    st.markdown(f"""
        <div style="
            display:flex;
            justify-content: center;
            align-items: center;
            margin-top: 2rem;
        ">
        <p style="font-weight:bold; color:black;"> Create with ❤️ by </p>
            <img src="{logo_url}" style="max-height: 35px;">
        </div>
    """, unsafe_allow_html=True)