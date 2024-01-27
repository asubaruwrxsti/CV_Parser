from fastapi import APIRouter, Request
from app.models.models import Project
from app.dependencies import Database
router = APIRouter()

project = Project()

@router.get("/")
async def read():    
    return await project.get_records(Database())

@router.get("/{project_id}")
async def read_project(project_id: int):
    return await project.get_records(Database(), project_id)

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