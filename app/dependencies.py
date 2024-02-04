import uuid
from .db import Database as BaseDatabase
from fastapi import Request, Response

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
# Database class
class Database(BaseDatabase, metaclass=Singleton):
    pass

def get_db():
    return Database()

# SessionManager class
class SessionManager(metaclass=Singleton):
    def __init__(self):
        self.sessions = {}

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def create_session(self, session_id, data):
        self.sessions[session_id] = data

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def get_current_user(self):
        return self.sessions
    
    def generate_session_id(self):
        return str(uuid.uuid4())

async def CORS(request: Request, response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
