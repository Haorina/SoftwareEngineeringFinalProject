# data_manager.py
import pandas as pd
import streamlit as st
# 👇 引入資料庫存檔功能 與 讀取商品功能
from database import save_order_to_db, get_all_products

# ==========================================
# 資料讀取
# ==========================================
def load_data():
    """
    載入商品資料並返回 pandas DataFrame。
    現在改為從資料庫讀取。
    """
    return get_all_products()

# ==========================================
# Callback 函數 (維持不變)
# ==========================================
def add_to_cart_callback(item):
    item_id = item['id']
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]['quantity'] += 1
        st.toast(f"✅ {item['name']} 數量增加！")
    else:
        new_item = item.to_dict() if isinstance(item, pd.Series) else item
        new_item['quantity'] = 1
        st.session_state.cart[item_id] = new_item
        st.toast(f"✅ 已將 {item['name']} 加入購物車！")

def update_quantity(item_id, change):
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]['quantity'] += change
        if st.session_state.cart[item_id]['quantity'] <= 0:
            del st.session_state.cart[item_id]

def clear_cart_callback():
    st.session_state.cart = {}

def submit_order_callback(name, email, address):
    """
    結帳表單提交後執行的 callback。
    """
    if name and address:
        buyer_account = st.session_state.get('current_user')
        current_total = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
        
        # 整理商品清單文字
        order_details_str = ", ".join([f"{v['name']} x{v['quantity']}" for v in st.session_state.cart.values()])

        # 寫入資料庫
        save_order_to_db(buyer_account, name, email, address, current_total, order_details_str)
        
        st.session_state.cart = {} 
        st.success("🎉 訂單已送出！(已存入資料庫)")
        st.balloons()
    else:
        st.error("請填寫完整資訊")