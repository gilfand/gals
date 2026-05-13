# core/database.py
import psycopg2
import bcrypt
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict

class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None
        self.create_tables()

    def get_connection(self):
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
        return self.conn

    def create_tables(self):
        """Создаём таблицу users"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role VARCHAR(20) DEFAULT 'viewer',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()

        self._create_default_admin()

    def _create_default_admin(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users WHERE username = 'admin'")
                if not cur.fetchone():
                    hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
                    cur.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        ("admin", hashed.decode(), "admin")
                    )
                    conn.commit()

    def login(self, username: str, password: str) -> Optional[Dict]:
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, role, password FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                    return {"username": user['username'], "role": user['role']}
        return None

    def register(self, username: str, password: str, role: str = "viewer") -> bool:
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username, hashed.decode(), role)
                    )
                    conn.commit()
            return True
        except Exception:
            return False

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()