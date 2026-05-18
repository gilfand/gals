from core.service.db_service import DatabaseService

class Container:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_services()
        return cls._instance

    def _init_services(self):
        self.database = DatabaseService()

container = Container()
