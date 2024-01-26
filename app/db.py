import psycopg2
from psycopg2 import OperationalError, ProgrammingError

class Database:
    def __init__(self):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        self.create_schema()

    def connect(self):
        try:
            return psycopg2.connect(
                host="db",
                database="cv_database",
                user="postgres",
                password="example"
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

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def create_schema(self):
        self.query("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, user_agent TEXT, ip TEXT);")

    def commit(self):
        self.connection.commit()