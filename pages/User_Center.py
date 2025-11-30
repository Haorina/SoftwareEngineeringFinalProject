# pages/2_User_Center.py
import streamlit as st
from database import get_user_orders

st.set_page_config(page_title="會員中心", page_icon="👤")
st.title("📦 我的訂單")

current_user = st.session_state.get('current_user')

if not current_user:
    st.warning("請先在首頁側邊欄 **登入** 才能查看訂單。")
else:
    st.write(f"歡迎回來，**{current_user}**")
    df = get_user_orders(current_user)
    
    if not df.empty:
        for i, row in df.iterrows():
            # 顯示訂單與狀態
            status_color = "🟢" if row['status']=="已出貨" else "🟡"
            with st.expander(f"{status_color} {row['order_date']} - ${row['total_amount']:,}"):
                st.write(f"**商品：** {row['items_summary']}")
                st.write(f"**狀態：** {row['status']}")
                st.write(f"**收件資訊：** {row['customer_name']} / {row['customer_address']}")
    else:
        st.info("您還沒有購買紀錄。")