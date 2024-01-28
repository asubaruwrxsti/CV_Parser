from fastapi import APIRouter, Request
from app.models.models import Users
from app.dependencies import Database
import hashlib

router = APIRouter()

user = Users()

@router.get("/")
async def read():    
    return await user.get_records(Database())

@router.get("/{user_id}")
async def read_user(user_id: int):
    return await user.get_records(Database(), user_id)

@router.post("/")
async def create(request: Request):
    try:
        form_data = await request.form()
        hashed_password = hashlib.sha256(form_data['password'].encode()).hexdigest()
        user = Users(
            username = form_data['username'],
            password = hashed_password, 
            projects = form_data.get('projects', None), 
            group_id = form_data.get('group_id', None)
        )
        await user.create_record(Database())
        return {"Create": "User"}
    except Exception as e:
        return {"Error": str(e)}

@router.put("/{user_id}")
async def update(user_id: int, request: Request):
    try:
        form_data = await request.form()
        updated_fields = {}
        for key in form_data.keys():
            updated_fields[key] = form_data[key]
        await user.update_record(Database(), user_id, updated_fields)
        return {"Update": "User"}
    except Exception as e:
        return {"Error": str(e)}

@router.delete("/{user_id}")
async def delete(user_id: int):
    await user.delete_record(Database(), user_id)
    return {"Delete": "User"}