# database.py (最終完整版)
import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "shop.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # 1. 使用者資料表：含真實姓名與地址
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            real_name TEXT,
            address TEXT
        )
    ''')
    # 2. 訂單資料表
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_date TEXT, username TEXT, customer_name TEXT,
            customer_email TEXT, customer_address TEXT,
            total_amount INTEGER, items_summary TEXT, status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 註冊：存入 5 個欄位
def register_user(username, password, email, real_name, address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', 
                  (username, password, email, real_name, address))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# 登入驗證
def check_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# 抓取個資 (給結帳自動填寫用)
def get_user_info(username):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM users WHERE username = ?", conn, params=(username,))
    conn.close()
    if not df.empty:
        return df.iloc[0].to_dict()
    return None

# 儲存訂單
def save_order_to_db(username, name, email, address, total, items):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO orders (order_date, username, customer_name, customer_email, 
                 customer_address, total_amount, items_summary, status) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
              (date, username, name, email, address, total, items, "處理中"))
    conn.commit()
    conn.close()

# 讀取所有訂單 (給管理員)
def get_all_orders():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM orders ORDER BY id DESC", conn)
    conn.close()
    return df

# 讀取個人訂單 (給會員)
def get_user_orders(username):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM orders WHERE username = ? ORDER BY id DESC", conn, params=(username,))
    conn.close()
    return df

# 👇【補回來的函式】更新訂單狀態 (給管理員修改出貨用)
def update_order_status(order_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()