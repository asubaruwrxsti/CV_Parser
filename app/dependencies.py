from .db import Database as BaseDatabase
from fastapi import Request, Response, Header, HTTPException
from typing import Annotated
from app.utils.helperFunctions import loadEnv
import uuid
import time
import jwt
import redis

env = loadEnv()

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
    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def create_session(self, session_id, data):
        encoded_jwt = jwt.encode(
            {
                "session_id": session_id, 
                "exp": time.time() + 3600,
                "data": data
            },
            env["JWT_SECRET"],
            algorithm=env["JWT_ALGORITHM"]
        )
        Redis().write_to_redis(session_id, (encoded_jwt, data))
        return encoded_jwt

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def clear_all_sessions(self):
        self.sessions = {}
    
    def generate_session_id(self):
        return str(uuid.uuid4())

def CORS(request: Request, response: Response):
    # TODO: Apply the CORS policy from the environment
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

def get_current_user(Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Session token is missing")

    Authorization = Authorization.strip("Bearer ")
    Authorization = Authorization.strip('"')

    try:
        userId = jwt.decode(Authorization, "secret", algorithms=["HS256"])["data"]["id"]
        return userId
    except:
        raise HTTPException(status_code=400, detail="Invalid token")

class Redis(metaclass=Singleton):
    def __init__(self):
        self.redis = redis.Redis(
            host="redis",
            port=6379
        )
    
    def write_to_redis(self, key, value):
        if isinstance(value, tuple):
            value = str(value)
        self.redis.set(key, value)
    
    def read_from_redis(self, key):
        return self.redis.get(key)

    def delete_from_redis(self, key):
        self.redis.delete(key)
