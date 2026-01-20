import streamlit as st
import pandas as pd
from datetime import date
import os

st.set_page_config(page_title="小遣い管理アプリ", layout="wide")

st.title("💰 小遣い管理アプリ")

FILE = "money.csv"

# データ読み込み
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["日付", "内容", "金額"])

# ===== 入力欄（横並び）=====
c1, c2, c3, c4 = st.columns([2, 4, 2, 1])

with c1:
    d = st.date_input("日付", date.today())
with c2:
    memo = st.text_input("内容")
with c3:
    money = st.number_input("金額", step=100)
with c4:
    add = st.button("追加")

if add:
    new = pd.DataFrame([[d, memo, money]], columns=df.columns)
    df = pd.concat([df, new], ignore_index=True)
    df.to_csv(FILE, index=False)
    st.success("追加しました")

# ===== 下段（左右分割）=====
left, right = st.columns([2, 1])

with left:
    st.subheader("履歴")
    st.dataframe(df, height=300)  # ← 高さ固定（スクロール防止）

with right:
    total = df["金額"].sum()
    st.subheader("残高")
    st.metric("現在の残高", f"{total} 円")

# ===== グラフ（1つだけ）=====
if not df.empty:
    chart = df.copy()
    chart["日付"] = pd.to_datetime(chart["日付"])
    chart = chart.groupby("日付")["金額"].sum()
    st.line_chart(chart, height=250)
