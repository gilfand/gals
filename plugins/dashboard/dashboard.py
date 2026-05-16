# plugins/dashboard/dashboard.py
from nicegui import ui
from core.plugin import Plugin

class DashboardPlugin(Plugin):
    name = "dashboard"
    title = "Dashboard"
    icon = "dashboard"
    allowed_roles = ["viewer", "operator", "admin"]

    def build(self):
        # Заголовок
        ui.label("Dashboard").classes("text-3xl font-bold text-[#00C853] mb-6")

        # KPI Карточки (4 штуки)
        with ui.row().classes("w-full gap-4"):
            self.kpi_card("Total Output", "12 450", "т/сут", "trending_up", "#00C853")
            self.kpi_card("Эффективность", "94.8", "%", "speed", "#1EB980")
            self.kpi_card("Температура", "68.4", "°C", "thermostat", "#4ADE80")
            self.kpi_card("Время работы", "98.2", "%", "schedule", "#00C853")

        # Простая информация
        with ui.card().classes("w-full p-6 mt-6 bg-[#1E2A24]"):
            ui.label("Статус производства").classes("text-xl font-bold mb-4")
            with ui.row().classes("gap-8"):
                ui.label("✅ Линия №1: Работает").classes("text-green-400")
                ui.label("✅ Линия №2: Работает").classes("text-green-400")
                ui.label("⏸️  Линия №3: Остановлена").classes("text-orange-400")

        # Последние обновления
        with ui.card().classes("w-full p-6 mt-4 bg-[#1E2A24]"):
            ui.label("Последние события").classes("text-lg font-bold mb-3")
            with ui.column().classes("gap-2"):
                ui.label("• 14:32 — Выработка за час: 1240 т").classes("text-sm")
                ui.label("• 14:15 — Температура в норме").classes("text-sm")
                ui.label("• 13:58 — Завершена смена А").classes("text-sm")

    def kpi_card(self, title: str, value: str, unit: str, icon: str, color: str = "#00C853"):
        with ui.card().classes("flex-1 p-5 bg-[#1E2A24] hover:bg-[#2A3A34] transition-colors"):
            with ui.row().classes("items-center gap-3"):
                ui.icon(icon, color=color).classes("text-3xl")
                with ui.column().classes("gap-1"):
                    ui.label(title).classes("text-sm text-gray-400")
                    with ui.row().classes("items-baseline gap-1"):
                        ui.label(value).classes(f"text-3xl font-bold text-{color.replace('#', '')}")
                        ui.label(unit).classes("text-gray-400 text-sm")