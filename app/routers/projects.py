from fastapi import APIRouter, Request, Header, HTTPException
from typing import Annotated
from app.models.models import Project
from app.dependencies import Database
import jwt

router = APIRouter()
project = Project()

@router.get("/")
async def read():    
    return await project.get_records(Database())

@router.get("/user/participants")
async def read_participants_of_user_leading(Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Session token is missing")

    Authorization = Authorization.strip("Bearer ")
    Authorization = Authorization.strip('"')

    try:
        userId = jwt.decode(Authorization, "secret", algorithms=["HS256"])["data"]["id"]

        participants = Database().query(f"SELECT participants FROM projects WHERE leader = '{userId}'")
        participants = [participant[0].split(",") for participant in participants]

        participant_names = []
        for participant in participants:
            result = Database().query(f"SELECT id, username FROM users WHERE id IN ({','.join(participant)})")
            participant_names.append(result)
        
        return {'participants': participant_names}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error: {str(e)}')

@router.get("/user")
async def read_items(Authorization: Annotated[str | None, Header()] = None):
    if Authorization is None:
        raise HTTPException(status_code=400, detail="Session token is missing")

    Authorization = Authorization.strip("Bearer ")
    Authorization = Authorization.strip('"')

    try:
        userId = jwt.decode(Authorization, "secret", algorithms=["HS256"])["data"]["id"]

        # Fetch column names from the projects table
        column_names = [column[0] for column in Database().query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'projects' ORDER BY ORDINAL_POSITION")]

        userLeadingProjects = Database().query(f"SELECT * FROM projects WHERE leader = '{userId}'")
        userParticipatingProjects = Database().query(f"SELECT * FROM projects WHERE ',' || participants || ',' LIKE '%,{userId},%'")

        # Convert project data into dictionaries with column names
        userLeadingProjects = [{column_names[i]: project[i] for i in range(len(column_names))} for project in userLeadingProjects]
        userParticipatingProjects = [{column_names[i]: project[i] for i in range(len(column_names))} for project in userParticipatingProjects]

        return {'userLeadingProjects': userLeadingProjects, 'userParticipatingProjects': userParticipatingProjects }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Error: {str(e)}')

@router.post("/")
async def create(request: Request):
    try:
        form_data = await request.form()
        project = Project(
            name=form_data['name'],
            description=form_data['description'],
            leader=form_data['leader'],
            participants=form_data['participants'],
            status=form_data['status']
        )
        # return {"Create": form_data}
        await project.create_record(Database())
        return {"Create": "project"}
    except Exception as e:
        return {"Error": str(e)}

@router.put("/{project_id}")
async def update(project_id: int, request: Request):
    try:
        form_data = await request.form()
        updated_fields = {}
        for key in form_data.keys():
            updated_fields[key] = form_data[key]
        await project.update_record(Database(), project_id, updated_fields)
        return {"Update": "project"}
    except Exception as e:
        return {"Error": str(e)}

@router.delete("/{project_id}")
async def delete(project_id: int):
    await project.delete_record(Database(), project_id)
    return {"Delete": "project"}