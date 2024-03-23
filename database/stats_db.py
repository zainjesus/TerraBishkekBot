import sqlite3


def sql_create_stats():
    global db, cursor
    db = sqlite3.connect("bot_stats.sqlite3")
    cursor = db.cursor()

    if db:
        print('База данных подключена!')

    tables = ["insta_official", "insta_roman", "insta_nastavniki", "insta_wb", "insta_sm", "insta_shodim", "insta_repost",
              "tg_official", "tg_chats", "tg_ataliev", "site", "whatsapp", "events", "qr",
              
              "insta_official_reg", "insta_roman_reg", "insta_nastavniki_reg", "insta_wb_reg", "insta_sm_reg", "insta_shodim_reg", "insta_repost_reg",
              "tg_official_reg", "tg_chats_reg", "tg_ataliev_reg", "site_reg", "whatsapp_reg",  "events_reg", "qr_reg"]
    for table in tables:
        db.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE)")
    db.commit()

async def insert_user(table, user_id):
    cursor.execute(f"INSERT OR IGNORE INTO {table} (user_id) VALUES (?)", (user_id,))
    db.commit()

async def get_all_users(table):
    results = cursor.execute(f"SELECT user_id FROM {table}").fetchall()
    user_ids = [row[0] for row in results]
    return user_ids

