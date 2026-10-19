
import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
    <div style="
        background: white;
        border-left: 8px solid #EB459E;
        padding: 25px;
        border: 1px solid black;
        margin-bottom: 20px;
        border-radius: 8px;
        color: #1e293b;
    ">
        <h3 style="
            margin: 0;
            color: #1e293b;
            font-size: 1.5rem;
        ">{name}</h3>

        <p style="color: #64748b; margin: 10px 0;">
            Code:
            <span style="
                background: #E0E3FF;
                color: #5865F2;
                padding: 2px 8px;
                border-radius: 5px;
            ">{code}</span>
            | Section: {section}
        </p>
    """

    if stats:
        html += """
        <div style="
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 15px;
        ">
        """

        for icon, label, value in stats:
            html += f"""
            <div style="
                background: #fce7f3;
                padding: 8px 12px;
                border-radius: 12px;
                font-size: 0.9rem;
                color: #1e293b;
            ">
                {icon} <b>{value}</b> {label}
            </div>
            """

        html += "</div>"

    html += "</div>"

    # Render HTML directly
    st.html(html)

    if footer_callback:
        footer_callback()
