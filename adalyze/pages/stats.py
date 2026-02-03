import streamlit as st

st.set_page_config(page_title="Adalyze | Stats", layout="wide")

from utils import inject_global_css
inject_global_css()

from tinydb import TinyDB
from dateutil import parser
from datetime import datetime, timedelta
import pandas as pd

# ----------------------------
# データ読み込み
# ----------------------------
db = TinyDB("data/result.json")
records = db.all()

st.title("📊 統計・傾向分析")

if not records:
    st.info("まだ診断ログがありません。先に診断を実行してください。")
    st.stop()

def safe_parse_dt(ts):
    try:
        return parser.parse(ts) if ts else None
    except Exception:
        return None

# DataFrame化（最低限の列に整形）
rows = []
for r in records:
    dt = safe_parse_dt(r.get("timestamp"))
    score = r.get("score")
    score = int(score) if isinstance(score, (int, float)) else None
    rows.append({
        "doc_id": getattr(r, "doc_id", None),
        "timestamp": dt,
        "date": dt.date() if dt else None,
        "category": r.get("category", "未分類"),
        "score": score,
        "ad_text": r.get("ad_text", ""),
    })

df = pd.DataFrame(rows)

# timestamp/score がない行は統計から除外（表示テーブルには残してもよいが、ここでは除外）
df_stats = df.dropna(subset=["timestamp", "score"]).copy()

if df_stats.empty:
    st.warning("統計に使えるデータがありません（timestamp/score が欠損）。")
    st.stop()

# ----------------------------
# フィルターUI（サイドバー）
# ----------------------------
with st.sidebar:
    st.header("🔎 統計フィルター")

    # 期間：デフォルトは直近30日
    today = datetime.now().date()
    default_from = today - timedelta(days=30)
    date_range = st.date_input(
        "期間（from/to）",
        value=(default_from, today)
    )
    if isinstance(date_range, tuple) and len(date_range) == 2:
        date_from, date_to = date_range
    else:
        date_from, date_to = default_from, today

    cats = sorted(df_stats["category"].unique().tolist())
    selected_cats = st.multiselect("カテゴリ", cats, default=cats)

    score_min, score_max = st.slider("スコア範囲", 0, 100, (0, 100))

# フィルター適用
mask = (
    (df_stats["date"] >= date_from) &
    (df_stats["date"] <= date_to) &
    (df_stats["category"].isin(selected_cats)) &
    (df_stats["score"] >= score_min) &
    (df_stats["score"] <= score_max)
)
f = df_stats[mask].copy()

# ----------------------------
# 件数・KPI
# ----------------------------
st.caption(f"対象期間: {date_from} 〜 {date_to} / 対象件数: {len(f)} 件（全体: {len(df_stats)} 件）")

if f.empty:
    st.warning("条件に合致するデータがありません。フィルター条件を広げてください。")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("件数", f"{len(f)}")
c2.metric("平均スコア", f"{f['score'].mean():.1f}")
c3.metric("中央値", f"{f['score'].median():.1f}")
c4.metric("高危険(≥70)", f"{(f['score'] >= 70).sum()}")

st.divider()

# ----------------------------
# チャート：カテゴリ別 件数・平均
# ----------------------------
left, right = st.columns(2)

with left:
    st.subheader("カテゴリ別 件数")
    cat_count = f.groupby("category")["score"].count().sort_values(ascending=False)
    st.bar_chart(cat_count)

with right:
    st.subheader("カテゴリ別 平均スコア")
    cat_mean = f.groupby("category")["score"].mean().sort_values(ascending=False)
    st.bar_chart(cat_mean)

st.divider()

# ----------------------------
# チャート：スコア分布（ヒストグラム）
# ----------------------------
st.subheader("スコア分布（10点刻み）")
bins = list(range(0, 101, 10))
labels = [f"{b:02d}-{b+9:02d}" for b in bins[:-1]]
f["score_bin"] = pd.cut(f["score"], bins=bins, right=False, labels=labels, include_lowest=True)
hist = f.groupby("score_bin")["score"].count()
hist = hist.reindex(labels).fillna(0)
st.bar_chart(hist)

st.divider()

# ----------------------------
# チャート：日別 推移（平均・件数）
# ----------------------------
st.subheader("日別推移（平均スコア / 件数）")
daily = f.groupby("date").agg(avg_score=("score", "mean"), count=("score", "count")).sort_index()

t1, t2 = st.columns(2)
with t1:
    st.write("平均スコア（日別）")
    st.line_chart(daily["avg_score"])
with t2:
    st.write("件数（日別）")
    st.line_chart(daily["count"])

st.divider()

# ----------------------------
# テーブル：サンプル表示
# ----------------------------
st.subheader("ログ（サンプル表示）")
show_cols = ["timestamp", "category", "score", "ad_text"]
preview = f.sort_values("timestamp", ascending=False)[show_cols].head(50)
st.dataframe(preview, use_container_width=True)
