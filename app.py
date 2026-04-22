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

# --- ✨ 新增的：更改清單名稱功能 ✨ ---
with st.expander("✏️ 更改目前清單名稱"):
    col_rename1, col_rename2 = st.columns([3, 1])
    with col_rename1:
        # 預設顯示目前的名稱
        new_list_name = st.text_input("輸入新名稱：", value=current_place, label_visibility="collapsed")
    with col_rename2:
        if st.button("💾 儲存名稱", use_container_width=True):
            new_list_name = new_list_name.strip()
            if new_list_name and new_list_name != current_place:
                if new_list_name in st.session_state.food_lists:
                    st.error("⚠️ 這個清單名稱已經存在囉！")
                else:
                    # 將舊清單的食物轉移給新名稱，並刪除舊名稱
                    st.session_state.food_lists[new_list_name] = st.session_state.food_lists.pop(current_place)
                    st.rerun() # 重新整理網頁套用新名稱
# -----------------------------------

# 顯示目前清單內容
# 使用 get 避免重新整理時的短暫錯誤
current_list = st.session_state.food_lists.get(current_place, []) 
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
    if st.button("🗑️ 清空目前食物", use_container_width=True):
        st.session_state.food_lists[current_place].clear()
        st.rerun()
