from nicegui import app

class Auth:
    def login(self, user_data: dict):
        """Логиним текущего клиента (браузер)"""
        client = app.storage.client
        client['authenticated'] = True
        client['username'] = user_data["username"]
        client['role'] = user_data.get("role", "viewer")

    def logout(self):
        app.storage.client.clear()

    def is_authenticated(self) -> bool:
        return app.storage.client.get('authenticated', False)

    def current_user(self) -> str:
        return app.storage.client.get('username', None)

    def current_role(self) -> str:
        return app.storage.client.get('role', 'viewer')

    def has_role(self, allowed_roles: list) -> bool:
        role = self.current_role()
        return role in allowed_roles if role else False