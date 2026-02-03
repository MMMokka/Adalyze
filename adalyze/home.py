import streamlit as st
import base64
import os
from utils import inject_global_css

st.set_page_config(page_title="Adalyze | Home", layout="wide")
inject_global_css()

# --- ロゴ画像（base64エンコードで表示）
def load_svg(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as file:
            svg = file.read()
            b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
            return f'<img src="data:image/svg+xml;base64,{b64}" width="200" style="margin-right: 1rem;" />'
    return ""

# --- サイドバーに遷移リンクを追加
#with st.sidebar:
    st.header("🔗 メニュー")
    st.success("左のサイドバーから『危険スコア診断ページ』をご利用ください。")

# --- ヘッダー（ロゴ + タイトル）
st.markdown(
    f"""
    <div style='display: flex; align-items: center; margin-bottom: 2rem;'>
        {load_svg("img/logo.svg")}
    </div>
    """,
    unsafe_allow_html=True
)

# --- メインコンテンツ（1カラム）
st.markdown("""
### 🔍 Adalyzeとは？
Adalyzeは、広告文に潜む**詐欺的・誇張的な表現**をAIが判定し、危険スコアを可視化するツールです。

---
#### 主な機能
- **広告文の危険スコア診断**
- **履歴管理と検索**
- **CSV/JSONエクスポート**
- **統計グラフによる傾向分析**

---
#### 📌 ご注意
- 広告文に**個人情報や機密情報は含めない**でください
- 本サービスの結果はあくまで**参考情報**です
""")

st.success("左のサイドバーから『危険スコア診断ページ』をご利用ください。")
