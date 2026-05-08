# main.py
import os
#from dotenv import load_dotenv
from nicegui import ui

#load_dotenv()

print("=== Industrial Platform Starting (Local) ===")

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
            raise ValueError("DATABASE_URL не найден в .env файле!")

        print("Подключение к PostgreSQL...")
        self.db = Database(db_url)
        print("✅ База данных подключена")

        self.auth = Auth()
        self.config = AppConfig()
        self.plugins: dict[str, Plugin] = {}
        self.main_content = None

        self.register_plugins()
        self.create_routes()

    def register_plugins(self):
        self.plugins = {
            "dashboard": DashboardPlugin(),
            "settings": SettingsPlugin(),
        }

    def create_routes(self):
        @ui.page('/login')
        def login_page():
            self.show_login_page()

        @ui.page('/')
        def main_page():
            if not self.auth.is_authenticated():
                ui.navigate.to('/login')
                return
            self.show_main_app()

    def show_login_page(self):
        """Страница логина"""
        with ui.column().classes("absolute-center items-center gap-8 w-full max-w-md"):
            ui.label("Промышленная Платформа").classes("text-4xl font-bold text-[#00C853]")
            ui.label("Вход в систему").classes("text-2xl")

            with ui.card().classes("w-full p-8 bg-[#1E2A24]"):
                username = ui.input("Имя пользователя").classes("w-full mb-4")
                password = ui.input("Пароль", password=True).classes("w-full mb-6")

                def try_login():
                    user = self.db.login(username.value, password.value)
                    if user:
                        self.auth.login(user)
                        ui.notify("Успешный вход!", type="positive")
                        ui.navigate.to('/')
                    else:
                        ui.notify("Неверный логин или пароль", type="negative")

                ui.button("Войти", on_click=try_login).classes("w-full py-3")

    def show_main_app(self):
        """Главное приложение"""
        with ui.header().classes("items-center justify-between px-4 py-2 bg-[#1E2A24]"):
            ui.label("Промышленная Платформа").classes("text-h6 font-bold")
            with ui.row():
                ui.label(f"{self.auth.current_user} ({self.auth.current_role})").classes("text-sm")
                ui.button(icon="logout", on_click=self.logout).props("flat")

        with ui.left_drawer(value=True, fixed=False).classes("bg-[#0F1A14] text-white"):
            self.build_sidebar()

        # Основной контейнер контента
        self.main_content = ui.column().classes("w-full p-6 gap-6")
        self.show_plugin("dashboard")

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

        if self.main_content:
            self.main_content.clear()
            with self.main_content:
                plugin.build()

    def logout(self):
        self.auth.logout()
        ui.navigate.to('/login')


# ====================== ЗАПУСК ======================
if __name__ in {"__main__", "__mp_main__"}:
    try:
        IndustrialApp()
        ui.run(
            host="127.0.0.1",
            port=8080,
            reload=True,
            dark=True,
            title="Промышленная Платформа"
        )
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()