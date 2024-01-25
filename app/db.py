import psycopg2

class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            database="cv_database",
            user="postgres",
            password="example"
        )
        self.cursor = self.connection.cursor()

    def query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()