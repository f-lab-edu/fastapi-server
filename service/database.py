import sqlite3

conn = sqlite3.connect("posts.db")

cur = conn.cursor()

cur.execute("""
            SELECT * FROM posts
            """)

rows = cur.fetchall()

for row in rows:
    print(row)
    
conn.close()