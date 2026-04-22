import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="雲端午餐抽獎機", page_icon="🍽️")

# 建立 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # 讀取試算表資料
    df = conn.read(spreadsheet=st.secrets["spreadsheet_url"], ttl="0")
    # 清理資料：移除空行與空值
    df = df.dropna(how='all')
    data_dict = {}
    for _, row in df.iterrows():
        cat = str(row['category']).strip()
        food = str(row['food']).strip()
        if cat not in data_dict: data_dict[cat] = []
        if food and food != "nan": data_dict[cat].append(food)
    return data_dict if data_dict else {"預設清單": []}

def save_to_sheets(data_dict):
    # 轉換為 DataFrame 格式
    rows = []
    for cat, foods in data_dict.items():
        if not foods:
            rows.append({"category": cat, "food": ""})
        else:
            for f in foods:
                rows.append({"category": cat, "food": f})
    new_df = pd.DataFrame(rows)
    # 更新回 Google Sheets
    conn.update(spreadsheet=st.secrets["spreadsheet_url"], data=new_df)

# 初始化資料
if 'food_lists' not in st.session_state:
    st.session_state.food_lists = get_data()

st.title("🍽️ 雲端午餐抽獎機")

# --- UI 功能區 ---
with st.expander("⚙️ 管理清單分類"):
    new_cat = st.text_input("新增分類名稱：")
    if st.button("➕ 建立分類"):
        if new_cat.strip() and new_cat not in st.session_state.food_lists:
            st.session_state.food_lists[new_cat] = []
            save_to_sheets(st.session_state.food_lists)
            st.rerun()

# 選擇分類
places = list(st.session_state.food_lists.keys())
current_place = st.selectbox("📍 請選擇地點：", places)
current_list = st.session_state.food_lists.get(current_place, [])

st.info(f"**目前清單：** {', '.join(current_list) if current_list else '空'}")

# 新增食物
col1, col2 = st.columns([3, 1])
with col1:
    new_food = st.text_input("新增食物：", label_visibility="collapsed")
with col2:
    if st.button("➕ 加入", use_container_width=True):
        if new_food.strip():
            st.session_state.food_lists[current_place].append(new_food.strip())
            save_to_sheets(st.session_state.food_lists)
            st.rerun()

st.divider()

# 抽獎
if st.button("🎲 抽出午餐！", type="primary", use_container_width=True):
    if current_list:
        winner = random.choice(current_list)
        st.success(f"✨ 決定是你了：【 {winner} 】！")
        st.balloons()
