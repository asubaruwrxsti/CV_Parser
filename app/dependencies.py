from app.db import Database

class DatabaseSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if DatabaseSingleton._instance is None:
            DatabaseSingleton._instance = Database()
        return DatabaseSingleton._instance