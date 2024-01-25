from app.db import Database

def get_database():
    database = Database()
    yield database
    del database
