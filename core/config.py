import yaml
from pathlib import Path

CONFIG_PATH = Path("config.yaml")

DEFAULT_CONFIG = {
    "app": {"theme": "dark", "title": "Промышленная Платформа"},
    "user": {"last_username": "", "remember_me": True}
}

class AppConfig:
    def __init__(self):
        self.config = self._load_or_create()

    def _load_or_create(self):
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, encoding="utf-8") as f:
                    loaded = yaml.safe_load(f) or {}
                config = DEFAULT_CONFIG.copy()
                for k, v in loaded.items():
                    if isinstance(v, dict):
                        config[k].update(v)
                return config
            except:
                pass
        self.save(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    def save(self, data=None):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(data or self.config, f, allow_unicode=True, default_flow_style=False)

    def get(self, section: str, key: str, default=None):
        return self.config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value):
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save()