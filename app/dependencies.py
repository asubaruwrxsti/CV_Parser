from .db import Database as BaseDatabase
# TODO: Fix Redis import
# from app.services.service import Redis
from fastapi import Header, HTTPException
from typing import Annotated
from app.utils.helperFunctions import loadEnv
import jwt

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

def get_current_user(Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Session token is missing")

    Authorization = Authorization.strip("Bearer ")
    Authorization = Authorization.strip('"')

    try:
        return jwt.decode(Authorization, "secret", algorithms=["HS256"])["data"]["id"]
    except:
        # Redis().delete_from_redis(jwt.decode(Authorization, "secret", algorithms=["HS256"])["data"]["session_id"])
        raise HTTPException(status_code=400, detail="Invalid token")
