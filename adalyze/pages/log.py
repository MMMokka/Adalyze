import streamlit as st

st.set_page_config(page_title="Adalyze | Log", layout="wide")

from utils import inject_global_css
inject_global_css()

from tinydb import TinyDB
from dateutil import parser
from datetime import datetime, timedelta
import io
import csv
import json

# ----------------------------
# DB読み込み
# ----------------------------
db = TinyDB("data/result.json")
records = db.all()  # TinyDB Document（dict互換）で doc_id を持つ

st.title("📚 診断ログ一覧")

if not records:
    st.info("まだ診断結果が保存されていません。")
    st.stop()

# ----------------------------
# ユーティリティ
# ----------------------------
def safe_parse_dt(ts: str):
    try:
        return parser.parse(ts) if ts else None
    except Exception:
        return None

def to_export_rows(docs):
    rows = []
    for d in docs:
        rows.append({
            "doc_id": getattr(d, "doc_id", None),
            "timestamp": d.get("timestamp"),
            "category": d.get("category", "未分類"),
            "score": d.get("score"),
            "ad_text": d.get("ad_text", ""),
            "result_text": d.get("result_text", "")
        })
    return rows

# ----------------------------
# フィルターUI（サイドバー）
# ----------------------------
with st.sidebar:
    st.header("🔎 フィルター")

    # 期間フィルター
    period = st.selectbox(
        "期間",
        ["全期間", "直近7日", "直近30日", "直近90日"],
        index=0
    )

    keyword = st.text_input("キーワード検索（広告文 or 結果）")

    categories = sorted(set(r.get("category", "未分類") for r in records))
    selected_category = st.selectbox("カテゴリで絞り込む", ["すべて"] + categories)

    min_score = st.slider("スコア下限（以上）", 0, 100, 0)

    # ソート切替
    sort_mode = st.selectbox(
        "並び替え",
        ["日時（新しい順）", "日時（古い順）", "スコア（高い順）", "スコア（低い順）"],
        index=0
    )

# ----------------------------
# フィルタ適用
# ----------------------------
kw = keyword.strip().lower() if keyword else ""

# 期間の下限日時を決める
now = datetime.now()
if period == "直近7日":
    min_dt = now - timedelta(days=7)
elif period == "直近30日":
    min_dt = now - timedelta(days=30)
elif period == "直近90日":
    min_dt = now - timedelta(days=90)
else:
    min_dt = None  # 全期間

filtered = []
for r in records:
    # timestamp フィルタ
    dt = safe_parse_dt(r.get("timestamp"))
    if min_dt and dt and dt < min_dt:
        continue
    if min_dt and dt is None:
        # 期間指定があるのにtimestampが無い/壊れているものは除外
        continue

    # カテゴリフィルタ
    if selected_category != "すべて" and r.get("category", "未分類") != selected_category:
        continue

    # スコア下限
    score_val = r.get("score")
    score_val = score_val if isinstance(score_val, (int, float)) else 0
    if score_val < min_score:
        continue

    # キーワード検索（広告文 or 結果）
    if kw:
        ad = (r.get("ad_text") or "").lower()
        res = (r.get("result_text") or "").lower()
        if kw not in ad and kw not in res:
            continue

    filtered.append(r)

# ----------------------------
# ソート適用
# ----------------------------
def sort_key_datetime(x):
    dt = safe_parse_dt(x.get("timestamp"))
    # Noneは末尾へ
    return dt or datetime.min

def sort_key_score(x):
    s = x.get("score")
    return s if isinstance(s, (int, float)) else -1

if sort_mode == "日時（新しい順）":
    filtered.sort(key=sort_key_datetime, reverse=True)
elif sort_mode == "日時（古い順）":
    filtered.sort(key=sort_key_datetime, reverse=False)
elif sort_mode == "スコア（高い順）":
    filtered.sort(key=sort_key_score, reverse=True)
else:  # "スコア（低い順）"
    filtered.sort(key=sort_key_score, reverse=False)

# ----------------------------
# 件数表示（見出し）
# ----------------------------
st.caption(f"表示件数: {len(filtered)} 件 / 全件: {len(records)} 件")

st.divider()

# ----------------------------
# エクスポート（フィルター結果）
# ----------------------------
st.subheader("📤 エクスポート（フィルター結果）")

rows = to_export_rows(filtered)

# CSV生成
csv_buf = io.StringIO()
fieldnames = list(rows[0].keys()) if rows else ["doc_id", "timestamp", "category", "score", "ad_text", "result_text"]
writer = csv.DictWriter(csv_buf, fieldnames=fieldnames)
writer.writeheader()
for r in rows:
    writer.writerow(r)
csv_data = csv_buf.getvalue().encode("utf-8")

# JSON生成
json_data = json.dumps(rows, ensure_ascii=False, indent=2).encode("utf-8")

c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    st.caption(f"エクスポート対象: {len(rows)} 件")
with c2:
    st.download_button(
        label="CSVをダウンロード",
        data=csv_data,
        file_name="adalyze_logs.csv",
        mime="text/csv",
        disabled=(len(rows) == 0),
        use_container_width=True
    )
with c3:
    st.download_button(
        label="JSONをダウンロード",
        data=json_data,
        file_name="adalyze_logs.json",
        mime="application/json",
        disabled=(len(rows) == 0),
        use_container_width=True
    )

st.divider()

# ----------------------------
# 削除（選択/表示中/全件）
# ----------------------------
st.subheader("🗑️ 削除")

with st.sidebar:
    st.header("🗑️ 削除操作")
    mode = st.radio(
        "削除モード",
        ["選択削除", "表示中（フィルター結果）を一括削除", "全件削除"],
        index=0
    )

    confirm = st.text_input("確認用：DELETE と入力（誤操作防止）", value="")

    if mode == "選択削除":
        options = []
        option_map = {}  # label -> doc_id
        for d in filtered:
            doc_id = getattr(d, "doc_id", None)
            dt = safe_parse_dt(d.get("timestamp"))
            dt_str = dt.strftime("%Y-%m-%d %H:%M") if dt else "-"
            score = d.get("score", "N/A")
            cat = d.get("category", "未分類")
            summary = (d.get("ad_text", "")[:24].replace("\n", " ") + "…") if d.get("ad_text") else ""
            label = f"[{doc_id}] {dt_str} | {cat} | {score} | {summary}"
            options.append(label)
            option_map[label] = doc_id

        selected = st.multiselect("削除するログを選択（表示中から）", options)

        if st.button("選択したログを削除", type="primary", use_container_width=True):
            if confirm != "DELETE":
                st.error("確認用テキストが一致しません（DELETE と入力してください）")
            elif not selected:
                st.warning("削除対象が選択されていません。")
            else:
                doc_ids = [option_map[x] for x in selected if option_map.get(x) is not None]
                if doc_ids:
                    db.remove(doc_ids=doc_ids)
                    st.success(f"{len(doc_ids)} 件を削除しました。")
                    st.rerun()

    elif mode == "表示中（フィルター結果）を一括削除":
        st.write(f"対象: 表示中 {len(filtered)} 件")
        if st.button("フィルター結果を一括削除", type="primary", use_container_width=True):
            if confirm != "DELETE":
                st.error("確認用テキストが一致しません（DELETE と入力してください）")
            else:
                doc_ids = [getattr(d, "doc_id", None) for d in filtered]
                doc_ids = [x for x in doc_ids if x is not None]
                if not doc_ids:
                    st.warning("削除対象がありません。")
                else:
                    db.remove(doc_ids=doc_ids)
                    st.success(f"{len(doc_ids)} 件を一括削除しました。")
                    st.rerun()

    else:  # 全件削除
        st.write(f"対象: 全件 {len(records)} 件")
        if st.button("全件削除（復元不可）", type="primary", use_container_width=True):
            if confirm != "DELETE":
                st.error("確認用テキストが一致しません（DELETE と入力してください）")
            else:
                db.truncate()
                st.success("全件削除しました。")
                st.rerun()

st.divider()

# ----------------------------
# ログ表示
# ----------------------------
st.subheader("🧾 ログ一覧")

if not filtered:
    st.warning("条件に合致する診断ログがありません。")
else:
    for record in filtered:
        doc_id = getattr(record, "doc_id", "-")
        dt = safe_parse_dt(record.get("timestamp"))
        dt_str = dt.strftime("%Y-%m-%d %H:%M") if dt else "-"
        summary = (record.get("ad_text", "")[:30].replace("\n", " ") + "...") if record.get("ad_text") else ""
        score = record.get("score", "N/A")
        category = record.get("category", "未分類")

        with st.expander(f"🕒 {dt_str}｜ID:{doc_id}｜スコア:{score}｜カテゴリ:{category}｜{summary}"):
            st.markdown(f"**広告文**\n\n```\n{record.get('ad_text','')}\n```")
            st.markdown("---")
            st.markdown(f"**診断結果**\n\n{record.get('result_text','')}")
