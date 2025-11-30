# pages/1_Admin_View.py
import streamlit as st
import pandas as pd
from ui_components import apply_styles

# 硬編碼的帳號密碼 (實際應用中應使用安全的方式儲存)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

# ==========================================
# 登入函數
# ==========================================
def login_form():
    """
    顯示登入表單並處理驗證邏輯。
    """
    st.title("🛡️ 管理員登入")
    st.markdown("請輸入帳號密碼以查看訂單紀錄。")

    # 使用 Form 確保輸入不會在每次按鍵時重新執行
    with st.form("admin_login_form"):
        username = st.text_input("帳號 (Username)")
        password = st.text_input("密碼 (Password)", type="password")
        login_button = st.form_submit_button("登入")

        if login_button:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                # 登入成功，設置狀態為 True
                st.session_state.logged_in = True
                st.success("✅ 登入成功！")
                st.rerun() # 重新運行頁面以顯示內容
            else:
                st.error("❌ 帳號或密碼錯誤。")

# ==========================================
# 管理員後台主頁面邏輯
# ==========================================
def admin_page_content():
    """
    登入成功後顯示的訂單管理內容。
    """
    st.title("🛡️ 管理員後台 (Admin View)")
    st.markdown("---")
    
    st.subheader("📦 訂單紀錄")
    
    if 'orders' in st.session_state and st.session_state.orders:
        order_df = pd.DataFrame(st.session_state.orders)
        
        st.info(f"目前總共有 **{len(order_df)}** 筆訂單紀錄。")
        st.dataframe(order_df, use_container_width=True)
        
        st.markdown("---")
        
        # 登出按鈕
        if st.button("🚪 登出", help="登出後將返回登入畫面"):
            st.session_state.logged_in = False
            st.rerun()

        # 清空歷史訂單的按鈕
        if st.button("🗑️ 清空所有歷史訂單", help="此操作不可逆"):
            st.session_state.orders = []
            st.warning("所有歷史訂單已清除。")
            st.rerun()

    else:
        st.info("目前尚無訂單紀錄。")
        
        # 登出按鈕
        if st.button("🚪 登出"):
            st.session_state.logged_in = False
            st.rerun()

# ==========================================
# 頁面主執行區塊
# ==========================================
def admin_view():
    """
    檢查登入狀態並決定顯示登入表單或後台內容。
    """
    apply_styles() # 應用樣式
    
    if st.session_state.logged_in:
        admin_page_content()
    else:
        login_form()

if __name__ == "__main__":
    admin_view()