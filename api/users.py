# api/users.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

import os
import psycopg2

from psycopg2.extras import RealDictCursor
import bcrypt

router = APIRouter(prefix="/api/users", tags=["users"])

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "viewer"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

def get_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL not configured")
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

@router.get("/", response_model=List[UserResponse])
def get_all_users(db=Depends(get_db)):
    """Получить всех пользователей"""
    with db.cursor() as cur:
        cur.execute("SELECT id, username, role FROM users ORDER BY id")
        return cur.fetchall()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_db)):
    """Получить пользователя по ID"""
    with db.cursor() as cur:
        cur.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    """Создать нового пользователя"""
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    with db.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING id, username, role",
                (user.username, hashed.decode(), user.role)
            )
            new_user = cur.fetchone()
            db.commit()
            return new_user
        except Exception:
            db.rollback()
            raise HTTPException(status_code=400, detail="Username already exists")

router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db=Depends(get_db)):
    """Обновить пользователя"""
    with db.cursor() as cur:
        updates = []
        params = []
        
        if user.username:
            updates.append("username = %s")
            params.append(user.username)
        if user.role:
            updates.append("role = %s")
            params.append(user.role)
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s RETURNING id, username, role"
        params.append(user_id)
        
        cur.execute(query, params)
        updated = cur.fetchone()
        db.commit()
        
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated

@router.delete("/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    """Удалить пользователя"""
    with db.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
        deleted = cur.fetchone()
        db.commit()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": f"User {user_id} deleted successfully"}
