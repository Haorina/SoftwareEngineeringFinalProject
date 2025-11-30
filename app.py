# app.py (主頁：商品商城)
import streamlit as st
from data_manager import load_data
from ui_components import (
    apply_styles, 
    display_products, 
    display_cart, 
    checkout_section
)

# ==========================================
# 系統初始化與架構設定
# ==========================================
st.set_page_config(
    page_title="期末專題",
    page_icon="🌿",
    layout="wide"
)

# 初始化 Session State 
if 'cart' not in st.session_state:
    st.session_state.cart = {} 

if 'orders' not in st.session_state:
    st.session_state.orders = []

# 【新增】初始化登入狀態
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def main():
    # 1. 應用樣式
    apply_styles()
    
    # 2. 載入資料
    df = load_data()
    
    # 3. 渲染介面 (側邊欄)
    display_cart()
    checkout_section()
    
    # 4. 渲染介面 (主內容：商品)
    if not df.empty:
        display_products(df)

if __name__ == "__main__":
    main()