from nicegui import ui
from core.plugin import Plugin

class SettingsPlugin(Plugin):
    name = "settings"
    title = "Настройки"
    icon = "settings"
    allowed_roles = "admin"

    def build(self):
        ui.label("Настройки приложения").classes("text-3xl font-bold text-[#00C853]")

        with ui.card().classes("w-full max-w-md p-6"):
            ui.switch("Тёмная тема", value=True).classes("mb-4")
            ui.button("Сохранить настройки", on_click=lambda: ui.notify("Настройки сохранены", type="positive"))