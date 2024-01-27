import psycopg2
from psycopg2 import OperationalError, ProgrammingError
from app.utils.helperFunctions import loadEnv

env = loadEnv()

class Database:
    def __init__(self):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        try:
            return psycopg2.connect(
                host = env['DB_HOST'],
                database = env['DB_NAME'],
                user = env['DB_USER'],
                password = env['DB_PASSWORD']
            )
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            return None

    def query(self, query, params=None):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                try:
                    return cursor.fetchall()
                except ProgrammingError:
                    return None

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        self.connection.commit()