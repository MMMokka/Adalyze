# utils.py

import streamlit as st

def inject_global_css():
    st.markdown("""
        <style>
            /* Google Fonts 読み込み */
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+JP&display=swap');

            /* メイン背景 + フォント */
            .stApp {
                background-color: #202123;
                font-family: 'IBM Plex Sans JP', sans-serif !important;
            }

            /* サイドバー背景 + フォント */
            [data-testid="stSidebar"] {
                background-color: #000;
                font-family: 'IBM Plex Sans JP', sans-serif !important;
            }

            /* 全体フォント強制 */
            html, body, [class*="css"] {
                font-family: 'IBM Plex Sans JP', sans-serif !important;
                font-size: 16px;
            }

            /* その他の共通要素にフォント強制 */
            * {
                font-family: 'IBM Plex Sans JP', sans-serif !important;
            }

            /* ボタンなど */
            button, .stButton>button, .stSelectbox>div {
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)


