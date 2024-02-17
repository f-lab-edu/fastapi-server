import sqlite3
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = None

    async def init_db(self):
        client = sqlite3.connect(self.DATABASE_URL)
        cur = conn.cursor()
    
    class Config:
        env_file = ".env"

def get_session():
    return

conn = sqlite3.connect("posts.db")

cur = conn.cursor()

cur.execute("SELECT * FROM posts")

rows = cur.fetchall()

for row in rows:
    print(row)
    
conn.close()