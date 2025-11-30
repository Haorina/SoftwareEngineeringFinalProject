# pages/1_Admin_View.py
import streamlit as st
import pandas as pd
from ui_components import apply_styles
# 👇 記得引入資料庫函式，不然等等讀不到訂單會報錯
from database import get_all_orders, update_order_status 

# 硬編碼的帳號密碼
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# 👇 【關鍵修正】這行就是解決報錯的重點！
# 如果 session 中還沒有 logged_in 這個變數，就先設為 False (未登入)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# 登入函數
# ==========================================
def login_form():
    """
    顯示登入表單並處理驗證邏輯。
    """
    st.title("🛡️ 管理員登入")
    st.markdown("請輸入帳號密碼以查看訂單紀錄。")

    with st.form("admin_login_form"):
        username = st.text_input("帳號 (Username)")
        password = st.text_input("密碼 (Password)", type="password")
        login_button = st.form_submit_button("登入")

        if login_button:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ 登入成功！")
                st.rerun()
            else:
                st.error("❌ 帳號或密碼錯誤。")

# ==========================================
# 管理員後台主頁面邏輯 (資料庫版)
# ==========================================
def admin_page_content():
    """
    登入成功後顯示的訂單管理內容。
    """
    st.title("🛡️ 賣家管理後台")
    st.markdown("---")
    
    # 從資料庫讀取最新資料
    df = get_all_orders()
    
    st.subheader("📦 訂單管理")
    
    if not df.empty:
        # --- 顯示數據概況 ---
        col1, col2 = st.columns(2)
        col1.metric("累積訂單數", f"{len(df)} 筆")
        col2.metric("總營業額", f"NT$ {df['total_amount'].sum():,}")
        
        # --- 顯示詳細表格 ---
        st.dataframe(
            df, 
            column_config={
                "id": "訂單編號",
                "order_date": "下單時間",
                "username": "會員帳號",
                "customer_name": "收件人",
                "status": "目前狀態",
                "total_amount": st.column_config.NumberColumn("金額", format="$%d"),
            },
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # --- 賣家操作區：更新出貨狀態 ---
        st.subheader("🚚 更新出貨狀態")
        
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            # 讓賣家選擇要修改哪一筆訂單 (顯示 ID)
            order_id_to_update = st.selectbox("選擇訂單編號", df['id'].tolist())
        
        with c2:
            # 選擇新的狀態
            new_status = st.selectbox("設定新狀態", ["處理中", "已出貨", "已完成", "取消訂單"])
            
        with c3:
            st.write("") # 排版用
            st.write("") 
            if st.button("更新狀態", use_container_width=True):
                update_order_status(order_id_to_update, new_status)
                st.success(f"訂單 #{order_id_to_update} 已更新為：{new_status}")
                st.rerun()

        # 下載報表
        st.download_button(
            "📥 下載 Excel 報表",
            df.to_csv(index=False).encode('utf-8-sig'),
            "orders_report.csv",
            "text/csv"
        )

    else:
        st.info("目前尚無訂單紀錄。")
        
    st.markdown("---")
    if st.button("🚪 登出系統"):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# 頁面主執行區塊
# ==========================================
def admin_view():
    """
    檢查登入狀態並決定顯示登入表單或後台內容。
    """
    apply_styles() 
    
    if st.session_state.logged_in:
        admin_page_content()
    else:
        login_form()

if __name__ == "__main__":
    admin_view()