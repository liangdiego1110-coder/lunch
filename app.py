import streamlit as st
import random

# 設定網頁的標題與圖示
st.set_page_config(page_title="今天吃什麼？", page_icon="🍽️", layout="centered")

st.title("🍽️ 午餐抽獎機")
st.write("把想吃的加進去，交給命運來決定！")

# 初始化 session_state
if 'food_lists' not in st.session_state:
    st.session_state.food_lists = {
        "彰師大附近": ["便當店", "學餐", "炒飯", "麵店"],
        "大肚山附近": ["小吃攤", "超商", "滷味"],
        "彰化市區": ["麥當勞", "拉麵", "火鍋", "壽司"],
        "自訂清單": []
    }

# --- 📂 清單管理區區 ---
with st.expander("⚙️ 管理清單分類"):
    # 1. 新增分類
    st.subheader("新增全新分類")
    new_cat_col1, new_cat_col2 = st.columns([3, 1])
    with new_cat_col1:
        new_category = st.text_input("輸入新分類名稱：", placeholder="例如：消夜、手搖飲...", key="add_new_cat")
    with new_cat_col2:
        if st.button("➕ 建立", use_container_width=True):
            if new_category.strip():
                if new_category not in st.session_state.food_lists:
                    st.session_state.food_lists[new_category] = []
                    st.success(f"已建立「{new_category}」")
                    st.rerun()
                else:
                    st.error("名稱重複了！")

    st.divider()

    # 2. 重新命名與刪除目前選中的分類
    st.subheader("修改目前選中的分類")
    # 先讓使用者選一個要修改的
    target_list = st.selectbox("選擇要管理的清單：", list(st.session_state.food_lists.keys()), key="manage_select")
    
    rename_col1, rename_col2 = st.columns([3, 1])
    with rename_col1:
        rename_input = st.text_input("重新命名為：", value=target_list, key="rename_input")
    with rename_col2:
        if st.button("💾 儲存", use_container_width=True):
            rename_input = rename_input.strip()
            if rename_input and rename_input != target_list:
                st.session_state.food_lists[rename_input] = st.session_state.food_lists.pop(target_list)
                st.rerun()

    # 3. 刪除分類 (多加一個保險功能)
    if st.button(f"🔥 刪除「{target_list}」整個分類", use_container_width=True):
        if len(st.session_state.food_lists) > 1:
            del st.session_state.food_lists[target_list]
            st.rerun()
        else:
            st.error("至少要保留一個分類喔！")

st.divider()

# --- 🎮 主要抽獎區 ---
# 獲取所有分類名稱
places = list(st.session_state.food_lists.keys())
current_place = st.selectbox("📍 請選擇地點：", places)

# 顯示目前清單
current_list = st.session_state.food_lists.get(current_place, [])
if current_list:
    st.info(f"**目前清單：** {', '.join(current_list)}")
else:
    st.warning("這個分類目前沒有食物，快加點東西吧！")

# 新增食物
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    new_food = st.text_input("新增食物到此分類：", placeholder="輸入食物名稱...", label_visibility="collapsed")
with col_f2:
    if st.button("➕ 加入", use_container_width=True):
        if new_food.strip():
            st.session_state.food_lists[current_place].append(new_food.strip())
            st.rerun()

st.divider()

# 抽獎按鈕
col_draw, col_clear = st.columns(2)
with col_draw:
    if st.button("🎲 抽出午餐！", type="primary", use_container_width=True):
        if current_list:
            winner = random.choice(current_list)
            st.success(f"✨ 決定是你了：【 {winner} 】！ ✨")
            st.balloons()
        else:
            st.error("清單是空的！")

with col_clear:
    if st.button("🗑️ 清空目前食物內容", use_container_width=True):
        st.session_state.food_lists[current_place].clear()
        st.rerun()
