from app.dependencies import Singleton
from fastapi import Request, Response, Depends
from app.utils.helperFunctions import loadEnv
import redis
import jwt
import time
import uuid

env = loadEnv()

# SessionManager class
class SessionManager(metaclass=Singleton):
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
    
    def generate_session_id(self):
        return str(uuid.uuid4())
    
    def clear_all_sessions(self):
        Redis().redis.flushall()

def CORS(request: Request, response: Response):
    # TODO: Apply the CORS policy from the environment
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'


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