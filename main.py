# main.py
import os
from nicegui import ui
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ====================== FASTAPI ======================
# CORS (чтобы можно было обращаться из браузера)
fastapi_app = FastAPI(title="Industrial Platform API")
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.users import router as users_router
fastapi_app.include_router(users_router)

print("=== Industrial Platform Starting ===")

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
            raise ValueError("DATABASE_URL не найден!")

        print(db_url)
        self.db = Database(db_url)
        print("✅ База данных подключена")

        self.auth = Auth()
        self.config = AppConfig()
        self.plugins: dict[str, Plugin] = {}

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

        @ui.page('/register')
        def register_page():
            self.show_register_page()

        @ui.page('/')
        def main_page():
            if not self.auth.is_authenticated():
                ui.navigate.to('/login')
                return
            self.show_main_app()

    def show_login_page(self):
        with ui.column().classes("absolute-center items-center gap-6 w-full max-w-md"):
            ui.label("Промышленная Платформа").classes("text-4xl font-bold text-[#00C853]")
            ui.label("Вход в систему").classes("text-2xl")

            with ui.card().classes("w-full p-8 bg-[#1E2A24]"):
                username = ui.input("Имя пользователя").classes("w-full mb-4")
                password = ui.input("Пароль", password=True).classes("w-full mb-6")

                def try_login():
                    user = self.db.login(username.value.strip(), password.value)
                    if user:
                        self.auth.login(user)
                        ui.notify("Успешный вход!", type="positive")
                        ui.navigate.to('/')
                    else:
                        ui.notify("Неверный логин или пароль", type="negative")

                ui.button("Войти", on_click=try_login).classes("w-full py-3")

                ui.button("Зарегистрироваться", 
                         on_click=lambda: ui.navigate.to('/register')
                ).props("flat").classes("w-full mt-2 text-[#00C853]")

    def show_register_page(self):
        with ui.column().classes("absolute-center items-center gap-6 w-full max-w-md"):
            ui.label("Регистрация").classes("text-3xl font-bold")

            with ui.card().classes("w-full p-8 bg-[#1E2A24]"):
                username = ui.input("Имя пользователя").classes("w-full mb-4")
                password = ui.input("Пароль", password=True).classes("w-full mb-4")
                password2 = ui.input("Повторите пароль", password=True).classes("w-full mb-6")

                def try_register():
                    if password.value != password2.value:
                        ui.notify("Пароли не совпадают", type="negative")
                        return
                    success = self.db.register(username.value.strip(), password.value)
                    if success:
                        ui.notify("Регистрация успешна!", type="positive")
                        ui.navigate.to('/login')
                    else:
                        ui.notify("Пользователь уже существует", type="negative")

                ui.button("Зарегистрироваться", on_click=try_register).classes("w-full py-3")
                ui.button("Уже есть аккаунт? Войти", on_click=lambda: ui.navigate.to('/login')).props("flat").classes("w-full")

    def show_main_app(self):
        with ui.header().classes("items-center justify-between px-4 py-2 bg-[#1E2A24]"):
            ui.label("Промышленная Платформа").classes("text-h6 font-bold")
            with ui.row():
                ui.label(f"{self.auth.current_user} ({self.auth.current_role})").classes("text-sm")
                ui.button(icon="logout", on_click=self.logout).props("flat")

        with ui.left_drawer(value=True, fixed=False).classes("bg-[#0F1A14] text-white"):
            self.build_sidebar()

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


if __name__ in {"__main__", "__mp_main__"}:
    try:
        IndustrialApp()
        ui.run(
            host="0.0.0.0",
            port=80,
            reload=False,
            dark=True,
            title="Промышленная Платформа"
        )
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()