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

        # ... (весь остальной код класса IndustrialApp)

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