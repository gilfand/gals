# core/auth.py
from nicegui import app, ui
from typing import Optional
import time

class Auth:

    def __init__(self):
        self.TIMEOUT_MINUTES = 30

    def login(self, user_data: dict):
        """Логиним пользователя с полной диагностикой"""
        print(f"🔐 Auth.login called for: {user_data.get('username')}")

        # Проверка контекста
        context_client = getattr(ui.context, 'client', None)
        print(f"   ui.context.client exists: {context_client is not None}")

        # Основное хранилище
        storage = app.storage.user
        print(f"   app.storage.user before: {dict(storage)}")

        storage['authenticated'] = True
        storage['username'] = user_data["username"]
        storage['role'] = user_data.get("role", "viewer")
        storage['last_activity'] = time.time() 

        print(f"✅ Login: {user_data['username']} (timeout: {self.TIMEOUT_MINUTES} min)")
        print(f"✅ User logged in: {user_data['username']} ({user_data.get('role')})")

    def logout(self):
        print("🔓 Auth.logout called")
        app.storage.user.clear()
        print("✅ Session cleared")

    def is_authenticated(self) -> bool:
        print("🔍 is_authenticated() called")

        # Проверка разных источников
        context_client = getattr(ui.context, 'client', None)
        print(f"   ui.context.client: {context_client is not None}")

        user_storage = app.storage.user
        authenticated = user_storage.get('authenticated', False)
        username = user_storage.get('username')
        last_activity = user_storage.get('last_activity', 0)

        print(f"   app.storage.user['authenticated']: {authenticated}")
        print(f"   app.storage.user['username']: {username}")
        print(f"   app.storage.user['last_activity']: {last_activity}")

        if time.time() - last_activity > self.TIMEOUT_MINUTES * 60:
            print("⏰ Session timeout")
            self.logout()
            return False

        return authenticated

    def current_user(self) -> Optional[str]:
        return app.storage.user.get('username')

    def current_role(self) -> str:
        return app.storage.user.get('role', 'viewer')

    def has_role(self, allowed_roles: list) -> bool:
        role = self.current_role()
        return role in allowed_roles if role else False