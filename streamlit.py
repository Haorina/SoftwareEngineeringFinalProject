import streamlit as st
import pandas as pd

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
    st.session_state.cart = []

if 'orders' not in st.session_state:
    st.session_state.orders = []

# ---------------------------------------------------------
# 美化區塊
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 1. 按鈕美化 */
    .stButton>button {
        background-color: #7D9BA1; /* 北歐風霧藍 */
        color: white !important;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5D7B81;
        transform: translateY(-2px);
    }

    /* 2. 卡片樣式 (使用變數適應深淺色) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color); 
        border-radius: 15px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px !important;
    }

    /* 3. 側邊欄 */
    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
        border-right: 1px solid rgba(128, 128, 128, 0.1);
    }

    /* 4. 字體設定 */
    h1, h2, h3, h4, span, p, div {
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 5. 圖片圓角 */
    img {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 資料讀取
# ==========================================
def load_data():
    data = [
        {"id": 1, "name": "高階機械鍵盤", "category": "3C周邊", "price": 3500, "image": "https://dlcdnwebimgs.asus.com/gain/848074E4-FB9F-414D-BFCA-70DB410AD363/fwebp"},
        {"id": 2, "name": "電競無線滑鼠", "category": "3C周邊", "price": 1800, "image": "https://blog.shopping.gamania.com/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F3wl0vtkq%2Fproduction%2Fc27c7cb593c30cb7e67a49a8df41cb3e3d3804ab-1200x720.png&w=3840&q=75"},
        {"id": 3, "name": "降噪耳機", "category": "影音設備", "price": 5200, "image": "https://helios-i.mashable.com/imagery/comparisons/27.fill.size_1200x675.v1751067039.jpg"},
        {"id": 4, "name": "人體工學椅", "category": "辦公家具", "price": 8000, "image": "https://piinterior-net.sfo3.digitaloceanspaces.com/wp-content/uploads/2024/12/scimgFhtCHm.webp"},
        {"id": 5, "name": "Type-C集線器", "category": "3C周邊", "price": 900, "image": "https://i0.wp.com/lpcomment.com/wp-content/uploads/2017/04/%E6%83%85%E5%A2%83%E5%9C%967.jpg?fit=760%2C438&ssl=1"},
        {"id": 6, "name": "4K螢幕", "category": "影音設備", "price": 12000, "image": "https://attach.mobile01.com/attach/202411/mobile01-457221a9759255cc1832ddffa7d8e2f9.jpg"},
         {"id": 7, "name": "音響", "category": "影音設備", "price": 6000, "image": "https://attach.mobile01.com/attach/202411/mobile01-457221a9759255cc1832ddffa7d8e2f9.jpg"},
    ]
    return pd.DataFrame(data)

# [FIX 1] 定義一個「加入購物車」的 callback 函數
# 這個函數會在按鈕按下時「優先」執行，確保購物車在畫面更新前就已經拿到資料
def add_to_cart_callback(item):
    st.session_state.cart.append(item)
    st.toast(f"✅ 已將 {item['name']} 加入購物車！")

def display_products(df):
    st.title("🌿 Shop") 
    st.markdown("---")
    
    # 篩選器
    categories = ["全部"] + list(df['category'].unique())
    selected_cat = st.radio("分類篩選 (Category)", categories, horizontal=True)
    
    if selected_cat != "全部":
        df = df[df['category'] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True) 

    # 商品展示
    cols = st.columns(3)
    for i, (index, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.image(row['image'], use_container_width=True)
                st.subheader(row['name'])
                
                c1, c2 = st.columns([1,1])
                c1.caption(row['category'])
                c2.markdown(f"**NT$ {row['price']:,}**")
                
                # [FIX 2] 改用 on_click 參數
                # 注意：這裡不直接寫邏輯，而是呼叫上面的 callback 函數
                st.button(
                    "加入購物車 (Add)", 
                    key=f"add_{row['id']}", 
                    on_click=add_to_cart_callback,  # 指定 callback
                    args=(row,)  # 傳遞參數給 callback
                )

# ==========================================
# [Member C] 購物車與側邊欄邏輯
# ==========================================
def display_cart():
    st.sidebar.title("🛒 Your Cart")
    st.sidebar.markdown("---")
    
    if not st.session_state.cart:
        st.sidebar.info("購物車目前是空的")
        return

    total_price = 0
    
    for i, item in enumerate(st.session_state.cart):
        with st.sidebar.container(border=True):
            col1, col2 = st.columns([2, 1])
            col1.write(f"**{item['name']}**")
            col2.write(f"${item['price']}")
        total_price += item['price']
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"Total: NT$ {total_price:,}")
    
    if st.sidebar.button("🗑️ 清空購物車"):
        st.session_state.cart = []
        st.rerun()

# ==========================================
# [Member D] 結帳與後台
# ==========================================
def checkout_section():
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.cart:
        with st.sidebar.expander("💳 前往結帳 (Checkout)", expanded=True):
            with st.form("checkout_form"):
                name = st.text_input("收件人姓名")
                email = st.text_input("Email")
                address = st.text_input("收件地址")
                submitted = st.form_submit_button("確認下單")
                
                if submitted:
                    if name and address:
                        order_info = {
                            "Name": name,
                            "Email": email,
                            "Total": sum(item['price'] for item in st.session_state.cart),
                            "Items": len(st.session_state.cart)
                        }
                        st.session_state.orders.append(order_info)
                        st.session_state.cart = [] 
                        st.success("🎉 訂單已送出！")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("請填寫完整資訊")

def admin_view():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    if st.checkbox("🔧 管理員後台 (Admin View)"):
        st.subheader("📦 訂單紀錄")
        if st.session_state.orders:
            order_df = pd.DataFrame(st.session_state.orders)
            st.dataframe(order_df, use_container_width=True)
        else:
            st.info("目前尚無訂單")

# ==========================================
# 主程式
# ==========================================
def main():
    df = load_data()
    display_cart()
    checkout_section()
    
    if not df.empty:
        display_products(df)
    
    admin_view()

if __name__ == "__main__":
    main()