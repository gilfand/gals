from nicegui import ui

def kpi_card(title: str, value: str, unit: str = "", color: str = "#00C853"):
    with ui.card().classes("w-full p-4 bg-[#1E2A24]"):
        ui.label(title).classes("text-sm text-gray-400")
        with ui.row().classes("items-baseline gap-2"):
            ui.label(value).classes(f"text-3xl font-bold text-[{color}]")
            ui.label(unit).classes("text-gray-400")