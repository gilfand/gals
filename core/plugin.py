from abc import ABC, abstractmethod
from nicegui import ui

class Plugin(ABC):
    name: str = ""
    title: str = ""
    icon: str = ""

    def build(self):
        """Основной метод, который строит интерфейс"""
        pass