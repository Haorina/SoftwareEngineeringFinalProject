# app.py
import streamlit as st
from data_manager import load_data
from ui_components import apply_styles, display_products, display_cart, checkout_section
from database import init_db, register_user, check_login 

st.set_page_config(page_title="期末專題", page_icon="🌿", layout="wide")

init_db()
if 'cart' not in st.session_state: st.session_state.cart = {} 
if 'current_user' not in st.session_state: st.session_state.current_user = None 

def main():
    apply_styles()
    
    with st.sidebar:
        st.markdown("## 👤 會員專區")
        if st.session_state.current_user:
            st.success(f"Hi, {st.session_state.current_user}")
            if st.button("登出"):
                st.session_state.current_user = None
                st.rerun()
        else:
            with st.expander("會員登入/註冊", expanded=True):
                tab1, tab2 = st.tabs(["登入", "註冊"])
                with tab1: 
                    u = st.text_input("帳號", key="login_user")
                    p = st.text_input("密碼", type="password", key="login_pwd")
                    if st.button("登入", key="btn_login"):
                        if check_login(u, p):
                            st.session_state.current_user = u
                            st.rerun()
                        else:
                            st.error("錯誤")
                with tab2: 
                    # 【修改】註冊表單增加欄位
                    nu = st.text_input("設定帳號", key="reg_user")
                    np = st.text_input("設定密碼", type="password", key="reg_pwd")
                    ne = st.text_input("Email", key="reg_email")
                    # 👇 新增這兩行
                    nn = st.text_input("真實姓名 (收件人)", key="reg_name")
                    na = st.text_input("收件地址", key="reg_addr")
                    
                    if st.button("註冊", key="btn_reg"):
                        if nu and np:
                            # 呼叫新的 register_user
                            if register_user(nu, np, ne, nn, na):
                                st.success("註冊成功！請登入")
                            else:
                                st.error("帳號已存在")
                        else:
                            st.warning("請填寫完整")
        st.markdown("---")

    df = load_data()
    display_cart()
    checkout_section()
    if not df.empty:
        display_products(df)

if __name__ == "__main__":
    main()