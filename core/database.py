from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import bcrypt
from core.models import Base
from typing import Optional, Dict

class Database:
    def __init__(self, db_url: str):
        self.engine = create_engine(
            db_url,
            poolclass=QueuePool,
            pool_size=15,
            max_overflow=25,
            pool_timeout=30,
        )
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Авторизация"""
        session = self.Session()
        try:
            result = session.execute(text(
                "SELECT username, role, password FROM users WHERE username = :username"
            ), {"username": username})
            row = result.fetchone()

            if row and bcrypt.checkpw(password.encode(), row.password.encode()):
                return {"username": row.username, "role": row.role}
            return None
        finally:
            session.close()

    def register(self, username: str, password: str, role: str = "viewer") -> bool:
        """Регистрация нового пользователя"""
        session = self.Session()
        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            session.execute(text(
                "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
            ), {"username": username, "password": hashed.decode(), "role": role})
            session.commit()
            return True
        except Exception:
            return False
        finally:
            session.close()

    def get_user_role(self, username: str) -> str:
        session = self.Session()
        try:
            result = session.execute(text(
                "SELECT role FROM users WHERE username = :username"
            ), {"username": username})
            row = result.fetchone()
            return row.role if row else "viewer"
        finally:
            session.close()

    def close(self):
        self.engine.dispose()    