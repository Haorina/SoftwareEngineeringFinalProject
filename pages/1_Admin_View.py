import streamlit as st
import pandas as pd
from database import check_login, get_all_orders, update_order_status, add_new_product

st.set_page_config(page_title="管理員後台", page_icon="🔧", layout="wide")

# CSS 美化 (簡單版)
st.markdown("""
<style>
    div[data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# 初始化管理員登入狀態
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==========================================
# 登入介面
# ==========================================
def login_section():
    st.title("🔐 管理員後台登入")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.info("請輸入管理員帳號密碼")
            account = st.text_input("管理員帳號", key="admin_user")
            password = st.text_input("密碼", type="password", key="admin_pwd")
            
            if st.button("登入", use_container_width=True):
                # 這裡設定：必須是 admin 帳號，且密碼驗證通過
                if account == "admin" and check_login(account, password):
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ 權限不足或帳號密碼錯誤")

# ==========================================
# 後台主功能
# ==========================================
def admin_dashboard():
    # 側邊欄顯示狀態
    with st.sidebar:
        st.success("✅ 管理員已登入")
        if st.button("登出後台"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
    st.title("🔧 管理員儀表板")
    
    # 使用 Tabs 分頁管理不同功能
    tab1, tab2 = st.tabs(["📋 訂單管理 (Order Management)", "➕ 商品上架 (Add Product)"])
    
    # --- Tab 1: 訂單管理 ---
    with tab1:
        st.subheader("訂單列表")
        df_orders = get_all_orders()
        
        if df_orders.empty:
            st.info("目前沒有任何訂單")
        else:
            # 顯示 KPI
            total_rev = df_orders['total_amount'].sum()
            c1, c2 = st.columns(2)
            c1.metric("總營收 (Revenue)", f"NT$ {total_rev:,}")
            c2.metric("總訂單數 (Orders)", len(df_orders))
            
            st.markdown("---")
            
            # 顯示每一筆訂單
            for index, row in df_orders.iterrows():
                # 狀態圖示
                status_icon = "🟢" if row['status'] == "已完成" else "🚚" if row['status'] == "已出貨" else "⏳"
                
                with st.expander(f"{status_icon} 訂單 #{row['id']} - {row['customer_name']} (${row['total_amount']:,})"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**購買帳號：** {row['username']}")
                        st.markdown(f"**商品內容：** {row['items_summary']}")
                        st.markdown(f"**配送地址：** {row['customer_address']}")
                        st.caption(f"下單時間：{row['order_date']}")
                    
                    with col2:
                        current_status = row['status']
                        opts = ["處理中", "已出貨", "已完成", "取消"]
                        try:
                            idx = opts.index(current_status)
                        except:
                            idx = 0
                        
                        new_status = st.selectbox("更新狀態", opts, index=idx, key=f"s_{row['id']}")
                        if st.button("更新", key=f"upd_{row['id']}"):
                            update_order_status(row['id'], new_status)
                            st.toast("狀態已更新！")
                            st.rerun()

    # --- Tab 2: 商品上架 ---
    with tab2:
        st.subheader("新增上架商品")
        with st.container(border=True):
            # 商品上架表單
            with st.form("add_product_form"):
                name = st.text_input("商品名稱 (Product Name)")
                category = st.selectbox("分類 (Category)", ["3C周邊", "影音設備", "辦公家具", "玩具", "其他"])
                
                c1, c2 = st.columns(2)
                with c1:
                    price = st.number_input("價格 (Price)", min_value=1, step=100)
                with c2:
                    image = st.text_input("圖片網址 (Image URL)", placeholder="https://...")

                submitted = st.form_submit_button("確認上架")
                
                if submitted:
                    if name and price and image:
                        if add_new_product(name, category, int(price), image):
                            st.success(f"✅ 已成功上架：{name}")
                        else:
                            st.error("上架失敗，請檢查資料庫連線")
                    else:
                        st.warning("⚠️ 請填寫完整資訊")

# ==========================================
# 頁面邏輯入口
# ==========================================
if not st.session_state.admin_logged_in:
    login_section()
else:
    admin_dashboard()