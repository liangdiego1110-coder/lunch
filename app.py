import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

# 網頁基礎設定
st.set_page_config(page_title="午餐抽獎機", layout="centered")

# 1. 建立 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 核心資料處理函式 ---
def get_data():
    """從雲端讀取資料並轉為字典格式"""
    try:
        df = conn.read(spreadsheet=st.secrets["spreadsheet_url"], ttl="0")
        df = df.dropna(how='all')
        data_dict = {}
        for _, row in df.iterrows():
            cat = str(row['category']).strip()
            food = str(row['food']).strip()
            if cat not in data_dict:
                data_dict[cat] = []
            if food and food != "nan" and food != "":
                data_dict[cat].append(food)
        return data_dict if data_dict else {"預設清單": []}
    except Exception:
        return {"預設清單": []}

def save_to_sheets(data_dict):
    """將目前的字典資料同步回雲端試算表"""
    rows = []
    for cat, foods in data_dict.items():
        if not foods:
            # 即使沒有食物也保留分類，放一個空值
            rows.append({"category": cat, "food": ""})
        else:
            for f in foods:
                rows.append({"category": cat, "food": f})
    new_df = pd.DataFrame(rows)
    conn.update(spreadsheet=st.secrets["spreadsheet_url"], data=new_df)

# 2. 初始化資料 (存於 session_state 避免重複讀取)
if 'food_lists' not in st.session_state:
    st.session_state.food_lists = get_data()

st.title("午餐抽獎機")
st.write("資料已與雲端同步")

# --- 區段一：管理清單分類 ---
with st.expander("管理清單分類 (新增/改名/刪除)"):
    # A. 新增分類
    st.subheader("新增分類")
    new_cat_name = st.text_input("輸入新分類名稱：", key="input_new_cat")
    if st.button("建立新分類"):
        if new_cat_name.strip() and new_cat_name not in st.session_state.food_lists:
            st.session_state.food_lists[new_cat_name] = []
            save_to_sheets(st.session_state.food_lists)
            st.rerun()

    st.divider()

    # B. 修改與刪除目前分類
    st.subheader("修改目前分類")
    all_cats = list(st.session_state.food_lists.keys())
    target_cat = st.selectbox("選擇要管理的分類：", all_cats, key="select_manage_cat")
    
    # 改名
    rename_val = st.text_input("重新命名為：", value=target_cat, key="rename_input")
    if st.button("儲存新名稱"):
        new_name = rename_val.strip()
        if new_name and new_name != target_cat:
            st.session_state.food_lists[new_name] = st.session_state.food_lists.pop(target_cat)
            save_to_sheets(st.session_state.food_lists)
            st.rerun()
            
    # 刪除整個分類
    if st.button(f"刪除整個 {target_cat} 分類", type="secondary"):
        if len(st.session_state.food_lists) > 1:
            del st.session_state.food_lists[target_cat]
            save_to_sheets(st.session_state.food_lists)
            st.rerun()
        else:
            st.error("至少需要保留一個分類")

st.divider()

# --- 區段二：主要抽獎與食物管理 ---
places = list(st.session_state.food_lists.keys())
current_place = st.selectbox("選擇目前地點：", places)
current_list = st.session_state.food_lists.get(current_place, [])

# 新增食物
st.subheader("新增食物")
f_col1, f_col2 = st.columns([3, 1])
with f_col1:
    new_food = st.text_input("輸入食物名稱：", label_visibility="collapsed", placeholder="例如：牛肉麵", key="input_new_food")
with f_col2:
    if st.button("加入", use_container_width=True):
        if new_food.strip():
            st.session_state.food_lists[current_place].append(new_food.strip())
            save_to_sheets(st.session_state.food_lists)
            st.rerun()

# 顯示清單與單筆刪除
st.subheader("目前清單內容")
if not current_list:
    st.write("目前沒有食物")
else:
    for i, food in enumerate(current_list):
        row_col1, row_col2 = st.columns([4, 1])
        with row_col1:
            st.write(f"{i+1}. {food}")
        with row_col2:
            # 使用索引 i 確保 key 唯一
            if st.button("刪除", key=f"btn_del_{current_place}_{i}", use_container_width=True):
                st.session_state.food_lists[current_place].pop(i)
                save_to_sheets(st.session_state.food_lists)
                st.rerun()

st.divider()

# --- 區段三：抽獎按鈕 ---
if st.button("開始抽獎", type="primary", use_container_width=True):
    if current_list:
        winner = random.choice(current_list)
        st.subheader(f"抽獎結果：{winner}")
        st.balloons()
    else:
        st.error("清單中沒有食物可以抽獎")

# 危險操作：清空該分類所有食物
with st.expander("進階操作"):
    if st.button("清空此分類所有食物"):
        st.session_state.food_lists[current_place] = []
        save_to_sheets(st.session_state.food_lists)
        st.rerun()
