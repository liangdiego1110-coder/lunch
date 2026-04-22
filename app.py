import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

st.set_page_config(page_title="雲端午餐抽獎機", page_icon="🍽️")

# 建立 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    df = conn.read(spreadsheet=st.secrets["spreadsheet_url"], ttl="0")
    df = df.dropna(how='all')
    data_dict = {}
    for _, row in df.iterrows():
        cat = str(row['category']).strip()
        food = str(row['food']).strip()
        if cat not in data_dict: data_dict[cat] = []
        if food and food != "nan": data_dict[cat].append(food)
    return data_dict if data_dict else {"預設清單": []}

def save_to_sheets(data_dict):
    rows = []
    for cat, foods in data_dict.items():
        if not foods:
            rows.append({"category": cat, "food": ""})
        else:
            for f in foods:
                rows.append({"category": cat, "food": f})
    new_df = pd.DataFrame(rows)
    conn.update(spreadsheet=st.secrets["spreadsheet_url"], data=new_df)

if 'food_lists' not in st.session_state:
    st.session_state.food_lists = get_data()

st.title("🍽️ 雲端午餐抽獎機")

# --- ⚙️ 分類管理區 ---
with st.expander("⚙️ 管理清單分類"):
    st.subheader("新增分類")
    new_cat_col1, new_cat_col2 = st.columns([3, 1])
    with new_cat_col1:
        new_cat = st.text_input("名稱：", label_visibility="collapsed", key="new_cat_input")
    with new_cat_col2:
        if st.button("➕ 建立", use_container_width=True):
            if new_cat.strip() and new_cat not in st.session_state.food_lists:
                st.session_state.food_lists[new_cat] = []
                save_to_sheets(st.session_state.food_lists)
                st.rerun()
                
    st.divider()
    
    st.subheader("刪除分類")
    del_cat_col1, del_cat_col2 = st.columns([3, 1])
    with del_cat_col1:
        del_target = st.selectbox("選擇要刪除的分類：", list(st.session_state.food_lists.keys()), label_visibility="collapsed")
    with del_cat_col2:
        if st.button("🗑️ 刪除", use_container_width=True):
            if len(st.session_state.food_lists) > 1:
                del st.session_state.food_lists[del_target]
                save_to_sheets(st.session_state.food_lists)
                st.rerun()
            else:
                st.error("至少要留一個分類喔！")

# --- 📍 主畫面選擇區 ---
places = list(st.session_state.food_lists.keys())
current_place = st.selectbox("📍 請選擇地點：", places)
current_list = st.session_state.food_lists.get(current_place, [])

# --- 📝 新增食物區 ---
col1, col2 = st.columns([3, 1])
with col1:
    new_food = st.text_input("新增食物：", label_visibility="collapsed", placeholder="想吃什麼？")
with col2:
    if st.button("➕ 加入", use_container_width=True):
        if new_food.strip():
            st.session_state.food_lists[current_place].append(new_food.strip())
            save_to_sheets(st.session_state.food_lists)
            st.rerun()

st.divider()

# --- 📋 食物清單與單筆刪除 ---
st.markdown("### 📋 目前清單內容")
if not current_list:
    st.warning("這個分類還沒有食物，快加一點吧！")
else:
    # 建立多欄位來顯示食物和對應的刪除按鈕
    for food in current_list:
        col_text, col_btn = st.columns([4, 1])
        with col_text:
            st.write(f"• {food}")
        with col_btn:
            # 每個食物旁邊都有一個專屬的刪除按鈕
            if st.button("❌", key=f"del_{current_place}_{food}"):
                st.session_state.food_lists[current_place].remove(food)
                save_to_sheets(st.session_state.food_lists)
                st.rerun()

st.divider()

# --- 🎲 抽獎區 ---
if st.button("🎲 抽出午餐！", type="primary", use_container_width=True):
    if current_list:
        winner = random.choice(current_list)
        st.success(f"✨ 決定是你了：【 {winner} 】！")
        st.balloons()
    else:
        st.error("清單是空的，抽不出來啦！")

# 加上一鍵清空整個分類食物的功能 (選用)
with st.expander("危險操作區"):
    if st.button("🗑️ 清空此分類所有食物", type="primary"):
        st.session_state.food_lists[current_place].clear()
        save_to_sheets(st.session_state.food_lists)
        st.rerun()
