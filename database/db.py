import sqlite3


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print('База данных подключена!')
    # cursor.execute("DROP TABLE IF EXISTS users")
    db.execute("CREATE TABLE IF NOT EXISTS users"
               "(id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE)")
    db.commit()


async def sql_command_insert(user_id):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    db.commit()


async def sql_command_all():
    results = cursor.execute("SELECT user_id FROM users").fetchall()
    user_ids = [row[0] for row in results]
    return user_ids
