# main.py
import os
import sys
from nicegui import ui

print("=== Industrial Platform Starting ===")
print(f"DATABASE_URL: {'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")

try:
    from core.config import AppConfig
    from core.database import Database
    from core.auth import Auth
    from core.plugin import Plugin

    from plugins.dashboard.dashboard import DashboardPlugin
    from plugins.settings.settings import SettingsPlugin

    class IndustrialApp:
        def __init__(self):
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                raise ValueError("DATABASE_URL environment variable is not set!")

            print("Connecting to PostgreSQL...")
            self.db = Database(db_url)
            print("Database connection successful.")

            self.auth = Auth()
            self.config = AppConfig()
            self.plugins = {}
            self.content_area = None

            self.register_plugins()
            self.setup_ui()

    def register_plugins(self):
        self.plugins = {
            "dashboard": DashboardPlugin(),
            "settings": SettingsPlugin(),
        }

    def setup_ui(self):
        ui.colors(primary='#00C853', secondary='#1EB980')

        if not self.auth.is_authenticated():
            self.show_login_page()
        else:
            self.show_main_app()

    def show_login_page(self):
        with ui.page('/login'):
            with ui.card().classes("absolute-center w-full max-w-md p-8 bg-[#1E2A24]"):
                ui.label("Вход в систему").classes("text-2xl font-bold text-center mb-6 text-white")

                username = ui.input("Имя пользователя").classes("w-full")
                password = ui.input("Пароль", password=True).classes("w-full")

                def try_login():
                    user = self.db.login(username.value, password.value)
                    if user:
                        self.auth.login(user)
                        ui.navigate.to('/')
                    else:
                        ui.notify("Неверный логин или пароль", type="negative")

                ui.button("Войти", on_click=try_login).classes("w-full mt-6")
                ui.button("Регистрация", on_click=lambda: ui.notify("Регистрация в разработке")).classes("w-full mt-2")

    def show_main_app(self):
        with ui.header().classes("items-center justify-between px-4 py-2 bg-[#1E2A24]"):
            ui.label("Промышленная Платформа").classes("text-h6 font-bold")
            with ui.row():
                ui.label(f"{self.auth.current_user} ({self.auth.current_role})").classes("text-sm")
                ui.button(icon="logout", on_click=self.logout).props("flat")

        with ui.left_drawer(value=True).classes("bg-[#0F1A14] text-white") as self.drawer:
            self.build_sidebar()

        self.content_area = ui.column().classes("w-full p-6 gap-6")

        # Открываем дашборд по умолчанию
        ui.timer(0.1, lambda: self.show_plugin("dashboard"), once=True)

    def build_sidebar(self):
        with ui.column().classes("w-full p-2 gap-1"):
            for key, plugin in self.plugins.items():
                if self.auth.has_role(plugin.allowed_roles):
                    ui.button(
                        plugin.title,
                        icon=plugin.icon,
                        on_click=lambda _, k=key: self.show_plugin(k)
                    ).props("flat align=left").classes("w-full")

    def show_plugin(self, name: str):
        plugin = self.plugins.get(name)
        if not plugin or not self.auth.has_role(plugin.allowed_roles):
            ui.notify("Доступ запрещён", type="negative")
            return

        self.content_area.clear()
        with self.content_area:
            plugin.build()

    def logout(self):
        self.auth.logout()
        ui.navigate.to('/login')

    if __name__ in {"__main__", "__mp_main__"}:
        IndustrialApp()
        ui.run(
            host="0.0.0.0",
            port=80,
            reload=False,
            dark=True,
            title="Промышленная Платформа"
        )

except Exception as e:
    print(f"CRITICAL STARTUP ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)