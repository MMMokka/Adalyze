import streamlit as st
import openai
import os
from dotenv import load_dotenv
import re
from tinydb import TinyDB
from datetime import datetime
from utils import inject_global_css

st.set_page_config(page_title="Adalyze | Fraudcheck", layout="wide")
inject_global_css()

# --- 環境変数読み込み
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db = TinyDB("data/result.json")

st.title("⚠️ 広告文の危険スコア診断（詳細版）")

# --- カテゴリ選択
category = st.selectbox("カテゴリを選択してください", [
    "副業・投資", "健康・医療", "美容・ダイエット", "自己啓発", "生活雑貨", "その他"
])

# --- 広告文入力
ad_text = st.text_area("広告文を入力してください", height=200)

# --- スコア抽出
def extract_score(result_text):
    match = re.search(r"危険スコア[:：]?\s*(\d{1,3})", result_text)
    if match:
        score = int(match.group(1))
        color = "#2EB8B2" if score < 40 else "#FBB360" if score < 70 else "#CD4246"
        return score, color
    return None, "#CCCCCC"

# --- 診断
if st.button("診断する") and ad_text.strip():
    with st.spinner("AIが診断中です..."):
        system_prompt = """
あなたは詐欺広告や誇張表現の専門家です。以下の広告文が詐欺的または誇大広告である可能性を分析し、指定の出力形式に沿って診断してください。

【分析項目】
1. 危険スコア（0～100）を数値で示してください（高いほど危険）
2. 危険と判断した理由を3点程度挙げてください
3. よくある詐欺的表現・誇張表現が含まれていれば列挙してください
4. ユーザーが注意すべきポイントを1〜2行でアドバイスしてください

【出力形式】

---

危険スコア: 〇〇/100  

理由:  
- 理由1  
- 理由2  
- 理由3  

詐欺的・誇張表現:  
- ○○  
- △△  

アドバイス:  
○○○○○○

---
        """.strip()

        user_prompt = f"【カテゴリ】：{category}\n【広告文】：\n{ad_text}"

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        result_text = response.choices[0].message.content
        score, color = extract_score(result_text)

        st.markdown(f"<h2 style='color:{color}'>危険スコア: {score}/100</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(result_text)

        # --- 保存（カテゴリも含める）
        db.insert({
            "category": category,
            "ad_text": ad_text.strip(),
            "score": score,
            "result_text": result_text.strip(),
            "timestamp": datetime.now().isoformat()
        })
