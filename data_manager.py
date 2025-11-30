# data_manager.py
import pandas as pd
import streamlit as st

# ==========================================
# 資料讀取
# ==========================================
def load_data():
    """
    載入商品資料並返回 pandas DataFrame。
    """
    data = [
        {"id": 1, "name": "高階機械鍵盤", "category": "3C周邊", "price": 3500, "image": "https://dlcdnwebimgs.asus.com/gain/848074E4-FB9F-414D-BFCA-70DB410AD363/fwebp"},
        {"id": 2, "name": "電競無線滑鼠", "category": "3C周邊", "price": 1800, "image": "https://blog.shopping.gamania.com/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F3wl0vtkq%2Fproduction%2Fc27c7cb593c30cb7e67a49a8df41cb3e3d3804ab-1200x720.png&w=3840&q=75"},
        {"id": 3, "name": "降噪耳機", "category": "影音設備", "price": 5200, "image": "https://helios-i.mashable.com/imagery/comparisons/27.fill.size_1200x675.v1751067039.jpg"},
        {"id": 4, "name": "人體工學椅", "category": "辦公家具", "price": 8000, "image": "https://piinterior-net.sfo3.digitaloceanspaces.com/wp-content/uploads/2024/12/scimgFhtCHm.webp"},
        {"id": 5, "name": "Type-C集線器", "category": "3C周邊", "price": 900, "image": "https://i0.wp.com/lpcomment.com/wp-content/uploads/2017/04/%E6%83%85%E5%A2%83%E5%9C%967.jpg?fit=760%2C438&ssl=1"},
        {"id": 6, "name": "4K螢幕", "category": "影音設備", "price": 12000, "image": "https://attach.mobile01.com/attach/202411/mobile01-457221a9759255cc1832ddffa7d8e2f9.jpg"},
        {"id": 7, "name": "音響", "category": "影音設備", "price": 6000, "image": "https://attach.mobile01.com/attach/202411/mobile01-457221a9759255cc1832ddffa7d8e2f9.jpg"},
        {"id": 8, "name": "麥克風", "category": "影音設備", "price": 3000, "image": "https://attach.mobile01.com/attach/202411/mobile01-457221a9759255cc1832ddffa7d8e2f9.jpg"},
        {"id": 9, "name": "派大星", "category": "玩具", "price": 300, "image": "https://images.seeklogo.com/logo-png/32/1/patrick-star-logo-png_seeklogo-320105.png"},
    ]
    return pd.DataFrame(data)

# ==========================================
# Callback 函數：處理狀態變更 (新增數量邏輯)
# ==========================================
def add_to_cart_callback(item):
    """
    商品點擊加入購物車時執行的 callback。
    將商品加入 st.session_state.cart 字典，或增加數量。
    """
    item_id = item['id']
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]['quantity'] += 1
        st.toast(f"✅ {item['name']} 數量增加！")
    else:
        # 將 DataFrame Series 轉換為字典並初始化數量
        new_item = item.to_dict() if isinstance(item, pd.Series) else item
        new_item['quantity'] = 1
        st.session_state.cart[item_id] = new_item
        st.toast(f"✅ 已將 {item['name']} 加入購物車！")

def update_quantity(item_id, change):
    """
    更新購物車中商品的數量 (+/-)。
    """
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id]['quantity'] += change
        if st.session_state.cart[item_id]['quantity'] <= 0:
            del st.session_state.cart[item_id]
    # 手動重載側邊欄以反映變化
     

def clear_cart_callback():
    """
    清空購物車的 callback。
    """
    st.session_state.cart = {}
    

def submit_order_callback(name, email, address):
    """
    結帳表單提交後執行的 callback。
    """
    if name and address:
        # 計算總價和總數，適應新的購物車結構
        current_total = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
        total_items = sum(item['quantity'] for item in st.session_state.cart.values())

        order_info = {
            "Name": name,
            "Email": email,
            "Total": current_total,
            "Items_Count": total_items,
            "Order_Details": str([f"{v['name']} x{v['quantity']}" for v in st.session_state.cart.values()])
        }
        st.session_state.orders.append(order_info)
        st.session_state.cart = {} 
        st.success("🎉 訂單已送出！")
        st.balloons()
        st.rerun()
    else:
        st.error("請填寫完整資訊")