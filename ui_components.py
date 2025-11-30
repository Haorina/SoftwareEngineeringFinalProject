# ui_components.py
import streamlit as st
from data_manager import add_to_cart_callback, update_quantity, clear_cart_callback, submit_order_callback
from database import get_user_info 

# ==========================================
# 介面渲染：美化 CSS
# ==========================================
def apply_styles():
    st.markdown("""
    <style>
        .stButton > button {
            background-color: #7D9BA1;
            color: white !important;
            border-radius: 20px;
            border: none;
            font-weight: bold;
            transition: 0.3s;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
            padding: 0.5rem 1rem;
        }
        .stButton > button:hover {
            background-color: #5D7B81;
            transform: translateY(-2px);
            color: white !important;
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] { gap: 0 !important; }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"] { padding: 0 !important; min-width: 0 !important; }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button {
            background-color: transparent !important; border: none !important; box-shadow: none !important;
            color: var(--text-color) !important; height: 40px !important; width: 100% !important;
            display: flex !important; align-items: center !important; font-size: 24px !important;
            font-weight: bold !important; padding: 0 !important; margin: 0 !important; padding-top: 3px !important;
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) .stButton > button { justify-content: flex-start !important; }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(3) .stButton > button { justify-content: flex-end !important; }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:hover { color: #7D9BA1 !important; transform: scale(1.2); }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:active { color: var(--text-color) !important; transform: scale(0.9); }
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: var(--secondary-background-color); border-radius: 15px; border: 1px solid rgba(128, 128, 128, 0.2); padding: 15px !important; }
        [data-testid="stSidebar"] { background-color: var(--secondary-background-color); border-right: 1px solid rgba(128, 128, 128, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 介面渲染：商品展示
# ==========================================
def display_products(df):
    st.title("🌿 Shop") 
    st.markdown("---")
    
    categories = ["全部"] + list(df['category'].unique())
    selected_cat = st.radio("分類篩選 (Category)", categories, horizontal=True)
    
    if selected_cat != "全部":
        df = df[df['category'] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True) 

    cols = st.columns(3)
    for i, (index, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(row['image'], use_container_width=True)
                st.subheader(row['name'])
                c1, c2 = st.columns([1,1])
                c1.caption(row['category'])
                c2.markdown(f"**NT$ {row['price']:,}**")
                
                st.button("加入購物車 (Add)", key=f"add_{row['id']}", on_click=add_to_cart_callback, args=(row,))

# ==========================================
# 介面渲染：購物車側邊欄
# ==========================================
def display_cart():
    st.sidebar.title("🛒 Your Cart")
    st.sidebar.markdown("---")
    
    if not st.session_state.cart:
        st.sidebar.info("購物車目前是空的")
        return

    total_price = 0
    for item_id, item in list(st.session_state.cart.items()):
        with st.sidebar.container(border=True):
            st.markdown(f"**{item['name']}**")
            c1, c2, c3 = st.columns([1, 6, 1])
            with c1: st.button("－", key=f"dec_{item_id}", on_click=update_quantity, args=(item_id, -1))
            with c2: 
                st.markdown(f"""<div style='width: 100%; height: 40px; display: flex; justify-content: center; align-items: center; font-size: 18px; font-weight: bold; margin: 0; padding: 0;'>{item['quantity']}</div>""", unsafe_allow_html=True)
            with c3: st.button("＋", key=f"inc_{item_id}", on_click=update_quantity, args=(item_id, 1))
            
            item_total = item['price'] * item['quantity']
            st.markdown(f"<div style='text-align: right; color: gray; font-size: 0.9em; margin-top: -10px;'>${item_total:,}</div>", unsafe_allow_html=True)
            total_price += item_total
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"Total: NT$ {total_price:,}")
    if st.sidebar.button("🗑️ 清空購物車", use_container_width=True):
        clear_cart_callback() 

# ==========================================
# 介面渲染：結帳區塊 (已修改：快速結帳)
# ==========================================
def checkout_section():
    """
    展示結帳表單。
    邏輯：
    1. 若未登入 -> 顯示警告，隱藏表單。
    2. 若已登入且資料完整 -> 顯示確認資訊 + 一鍵下單按鈕 (不顯示輸入框)。
    3. 若已登入但資料缺漏 -> 顯示輸入框讓使用者補填。
    """
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.cart:
        # 1. 強制登入檢查
        if not st.session_state.get('current_user'):
            st.sidebar.warning("🔒 請先登入會員才能結帳")
            return 

        with st.sidebar.expander("💳 結帳確認 (Checkout)", expanded=True):
            
            # 嘗試抓取資料
            user_info = get_user_info(st.session_state.current_user)
            saved_name = user_info.get('real_name') if user_info else ""
            saved_email = user_info.get('email') if user_info else ""
            saved_addr = user_info.get('address') if user_info else ""

            # 2. 如果資料完整 -> 顯示快速結帳介面 (無輸入框)
            if saved_name and saved_addr:
                st.info("📦 將配送至以下地址：")
                st.markdown(f"**收件人：** {saved_name}")
                st.markdown(f"**Email：** {saved_email}")
                st.markdown(f"**地址：** {saved_addr}")
                
                # 直接顯示按鈕
                if st.button("🚀 確認下單 (Place Order)", use_container_width=True):
                    submit_order_callback(saved_name, saved_email, saved_addr)
            
            # 3. 資料不完整 -> 顯示原本的表單讓使用者補填
            else:
                st.warning("⚠️ 您的會員資料不完整，請手動填寫")
                with st.form("checkout_form"):
                    name = st.text_input("收件人姓名", value=saved_name)
                    email = st.text_input("Email", value=saved_email)
                    address = st.text_input("收件地址", value=saved_addr)
                    
                    submitted = st.form_submit_button("確認下單")
                    if submitted:
                        submit_order_callback(name, email, address)