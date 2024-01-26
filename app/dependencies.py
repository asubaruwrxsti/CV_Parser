from app.db import Database

database = None

def get_database():
    global database
    if database is None:
        database = Database()
    yield database