from nicegui import app

class Auth:
    def __init__(self):
        self.current_user = None
        self.current_role = None

    def login(self, user_data: dict):
        self.current_user = user_data["username"]
        self.current_role = user_data["role"]
        app.storage.user['username'] = self.current_user
        app.storage.user['role'] = self.current_role

    def logout(self):
        self.current_user = None
        self.current_role = None
        app.storage.user.clear()

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def has_role(self, allowed_roles: list) -> bool:
        if not self.current_role:
            return False
        return self.current_role in allowed_roles