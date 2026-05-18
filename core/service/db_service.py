import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
from typing import Optional, Dict

class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return

        load_dotenv() if os.path.exists(".env") else None
        
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL не найден в окружении!")

        self.conn = None
        self._initialized = True
        self.create_tables()
        print("✅ DatabaseService initialized (Singleton)")

    def get_conn(self):
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)
        return self.conn

    def create_tables(self):
        with self.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(80) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role VARCHAR(20) DEFAULT 'viewer',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
        self._create_default_admin()

    def _create_default_admin(self):
        with self.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM users WHERE username = 'admin'")
                if not cur.fetchone():
                    hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
                    cur.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        ("admin", hashed.decode(), "admin")
                    )
                    conn.commit()

    # CRUD
    def login(self, username: str, password: str) -> Optional[Dict]:
        with self.get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT username, role, password FROM users WHERE username = %s", (username,))
                user = cur.fetchone()
                if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                    return {"username": user['username'], "role": user['role']}
        return None

    def register(self, username: str, password: str, role: str = "viewer") -> bool:
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            with self.get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                        (username.strip(), hashed.decode(), role)
                    )
                    conn.commit()
            return True
        except:
            return False

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()  