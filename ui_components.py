# ui_components.py
import streamlit as st
import pandas as pd
from data_manager import add_to_cart_callback, update_quantity, clear_cart_callback, submit_order_callback

# ==========================================
# 介面渲染：美化 CSS (包含購物車按鈕樣式)
# ==========================================
def apply_styles():
    """
    應用頁面所需的 CSS 樣式。
    """
    st.markdown("""
    <style>
        /* 1. 全局字體與設定 */
        h1, h2, h3, h4, span, p, div {
            font-family: 'Helvetica Neue', sans-serif;
        }
        img {
            border-radius: 8px;
        }

        /* 2. 一般按鈕 (維持原樣) */
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

        /* ============================================================
           3. 側邊欄購物車數量控制按鈕樣式
           目標： - 靠最左， + 靠最右，數字居中
        ============================================================ */
        
        /* (A) 移除水平區塊間距 */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            gap: 0 !important;
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"] {
            padding: 0 !important;
            min-width: 0 !important;
        }

        /* (B) 共通按鈕樣式 (去背、字體大) */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: var(--text-color) !important;
            height: 40px !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            font-size: 24px !important;
            font-weight: bold !important;
            padding: 0 !important;
            margin: 0 !important;
            padding-top: 3px !important;
        }

        /* (C) [關鍵] 分別指定對齊方向 */
        
        /* 第一欄 (減號) -> 靠左對齊 (Flex-start) */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(1) .stButton > button {
            justify-content: flex-start !important; /* 靠左 */
        }

        /* 第三欄 (加號) -> 靠右對齊 (Flex-end) */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:nth-of-type(3) .stButton > button {
            justify-content: flex-end !important; /* 靠右 */
        }

        /* Hover 效果 */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:hover {
            color: #7D9BA1 !important;
            transform: scale(1.2);
        }
        
        /* 其他互動效果 */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:active {
            color: var(--text-color) !important;
            transform: scale(0.9);
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] .stButton > button:focus {
            outline: none !important;
            box-shadow: none !important;
            color: var(--text-color) !important;
        }
        
        /* 4. 側邊欄背景設定 */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--secondary-background-color); 
            border-radius: 15px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            padding: 15px !important;
        }
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background-color);
            border-right: 1px solid rgba(128, 128, 128, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 介面渲染：商品展示 (保持不變)
# ==========================================
def display_products(df):
    """
    展示商品清單，包含分類篩選和加入購物車按鈕。
    """
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
                
                st.button(
                    "加入購物車 (Add)", 
                    key=f"add_{row['id']}", 
                    on_click=add_to_cart_callback,
                    args=(row,)
                )

# ==========================================
# 介面渲染：購物車側邊欄 (整合 +/- 邏輯和 UI)
# ==========================================
def display_cart():
    """
    展示側邊欄的購物車內容、總價和清空按鈕。
    """
    st.sidebar.title("🛒 Your Cart")
    st.sidebar.markdown("---")
    
    if not st.session_state.cart:
        st.sidebar.info("購物車目前是空的")
        return

    total_price = 0
    
    # 購物車結構為 {item_id: item_dict}
    for item_id, item in list(st.session_state.cart.items()):
        with st.sidebar.container(border=True):
            st.markdown(f"**{item['name']}**")
            
            # [修改重點] 欄位比例調整
            c1, c2, c3 = st.columns([1, 6, 1])
            
            with c1:
                st.button("－", key=f"dec_{item_id}", on_click=update_quantity, args=(item_id, -1))
            
            with c2:
                # 數字區塊 (使用 HTML 確保居中和高度)
                st.markdown(
                    f"""
                    <div style='
                        width: 100%;
                        height: 40px; 
                        display: flex; 
                        justify-content: center; 
                        align-items: center; 
                        font-size: 18px; 
                        font-weight: bold;
                        margin: 0; 
                        padding: 0;'>
                        {item['quantity']}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            with c3:
                st.button("＋", key=f"inc_{item_id}", on_click=update_quantity, args=(item_id, 1))
            
            item_total = item['price'] * item['quantity']
            st.markdown(f"<div style='text-align: right; color: gray; font-size: 0.9em; margin-top: -10px;'>${item_total:,}</div>", unsafe_allow_html=True)
            
            total_price += item_total
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"Total: NT$ {total_price:,}")
    
    # 綁定 clear_cart_callback
    if st.sidebar.button("🗑️ 清空購物車", use_container_width=True):
        clear_cart_callback() 

# ==========================================
# 介面渲染：結帳區塊 (修改計算邏輯)
# ==========================================
def checkout_section():
    """
    展示結帳表單。
    """
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.cart:
        with st.sidebar.expander("💳 前往結帳 (Checkout)", expanded=True):
            with st.form("checkout_form"):
                name = st.text_input("收件人姓名")
                email = st.text_input("Email")
                address = st.text_input("收件地址")
                submitted = st.form_submit_button("確認下單")
                
                # 在提交後，將資料傳遞給 submit_order_callback 處理
                if submitted:
                    submit_order_callback(name, email, address)