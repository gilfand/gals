from nicegui import ui, app
from core.config import AppConfig
from core.database import Database
from plugins.dashboard.dashboard import DashboardPlugin
from plugins.settings.settings import SettingsPlugin

class IndustrialApp:
    def __init__(self):
        self.config = AppConfig()
        self.db = Database()
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

        with ui.header().classes("items-center justify-between px-4 py-2 bg-[#1E2A24]"):
            ui.label("Промышленная Платформа").classes("text-h6 font-bold")
            ui.button(icon="logout", on_click=self.logout).props("flat")

        with ui.left_drawer(value=True).classes("bg-[#0F1A14]") as self.drawer:
            self.build_sidebar()

        self.content_area = ui.column().classes("w-full p-6 gap-6")

        # Автозагрузка дашборда
        ui.timer(0.2, lambda: self.show_plugin("dashboard"), once=True)

    def build_sidebar(self):
        with ui.column().classes("w-full p-2 gap-1"):
            for key, plugin in self.plugins.items():
                ui.button(
                    plugin.title,
                    icon=plugin.icon,
                    on_click=lambda _, k=key: self.show_plugin(k)
                ).props("flat align=left").classes("w-full")

    def show_plugin(self, name: str):
        self.content_area.clear()
        with self.content_area:
            self.plugins[name].build()

    def logout(self):
        ui.notify("Вы вышли из системы", type="info")

if __name__ in {"__main__", "__mp_main__"}:
    IndustrialApp()
    ui.run(
        host="0.0.0.0",      # Обязательно для Runsite
        port=8080,
        reload=False,         # Отключаем в продакшене
        dark=True,
        title="Промышленная Платформа",
        favicon="🚀"
    )