"""
将 users 表中的明文密码迁移为 bcrypt 哈希。
使用方法: cd server && python migrate_passwords.py
"""

import pymysql
from passlib.hash import bcrypt

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"
MYSQL_DB = "Game"

conn = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, username, password FROM users")
        users = cursor.fetchall()

        for user in users:
            raw = user["password"]
            if raw.startswith("$2b$"):
                print(f"  skip {user['username']}: already hashed")
                continue
            hashed = bcrypt.hash(raw)
            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s",
                (hashed, user["id"]),
            )
            print(f"  migrated {user['username']}: {raw} -> {hashed}")

        conn.commit()
        print(f"\nDone. {len(users)} users processed.")
finally:
    conn.close()
