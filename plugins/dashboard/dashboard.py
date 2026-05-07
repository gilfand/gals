
from nicegui import ui
import plotly.express as px
import pandas as pd
from core.plugin import Plugin
from core.ui_components import kpi_card

class DashboardPlugin(Plugin):
    name = "dashboard"
    title = "Дашборд"
    icon = "dashboard"

    def build(self):
        ui.label("Производственный Дашборд").classes("text-3xl font-bold text-[#00C853]")

        with ui.row().classes("w-full gap-4"):
            kpi_card("Общая выработка", "12 450", "т/сут")
            kpi_card("Эффективность", "94.8", "%", "#1EB980")
            kpi_card("Температура", "68.4", "°C", "#4ADE80")
            kpi_card("Коэффициент OEE", "87.3", "%")

        # Plotly График
        df = pd.DataFrame({
            "Время": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
            "Факт": [8200, 9400, 11800, 13200, 10900, 8500],
            "План": [8000, 9000, 11000, 12500, 10500, 9000]
        })

        fig = px.line(df, x="Время", y=["Факт", "План"], markers=True,
                      title="Выработка за сутки")
        fig.update_layout(template="plotly_dark", height=450)

        ui.plotly(fig).classes("w-full")