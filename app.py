import streamlit as st
import random

# 設定網頁的標題與圖示
st.set_page_config(page_title="今天吃什麼？", page_icon="🍽️")

st.title("🍽️ 午餐抽獎機")
st.write("把想吃的加進去，交給命運來決定！")

# 讓網頁記住清單資料
if 'food_lists' not in st.session_state:
    st.session_state.food_lists = {
        "彰師大附近": ["便當店", "學餐", "炒飯", "麵店"],
        "大肚山附近": ["小吃攤", "超商", "滷味"],
        "彰化市區": ["麥當勞", "拉麵", "火鍋", "壽司"],
        "自訂清單": []
    }

# 1. 選擇地點
places = list(st.session_state.food_lists.keys())
current_place = st.selectbox("📍 選擇地點清單：", places)

# 顯示目前清單
current_list = st.session_state.food_lists[current_place]
if current_list:
    st.info(f"**目前清單：** {', '.join(current_list)}")
else:
    st.warning("清單空空的，先加點食物吧！")

st.divider()

# 2. 新增食物區
col1, col2 = st.columns([3, 1])
with col1:
    new_food = st.text_input("輸入想吃的食物：", label_visibility="collapsed", placeholder="例如：義大利麵...")
with col2:
    if st.button("➕ 加入", use_container_width=True):
        if new_food.strip():
            st.session_state.food_lists[current_place].append(new_food.strip())
            st.rerun()

st.divider()

# 3. 抽獎與清空區
col_draw, col_clear = st.columns(2)
with col_draw:
    if st.button("🎲 抽出午餐！", type="primary", use_container_width=True):
        if current_list:
            winner = random.choice(current_list)
            st.success(f"✨ 決定是你了：【 {winner} 】！ ✨")
            st.balloons() 
        else:
            st.error("沒有食物可以抽啦！")

with col_clear:
    if st.button("🗑️ 清空目前清單", use_container_width=True):
        st.session_state.food_lists[current_place].clear()
        st.rerun()
