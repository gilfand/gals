from abc import ABC, abstractmethod
from core.container import container

class Plugin(ABC):
    name: str = ""
    title: str = ""
    icon: str = ""
    allowed_roles: list[str] = ["viewer", "operator", "admin"]

    def __init__(self):
        self.db = container.database

    def build(self):
        """Основной метод, который строит интерфейс"""
        pass