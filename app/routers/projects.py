from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.models import Project, Applicants
from app.dependencies import Database, get_current_user
from app.services import service

router = APIRouter(dependencies=[Depends(service.CORS), Depends(get_current_user)])
project = Project()
applicants = Applicants()

@router.get("/")
async def read():    
    return await project.get_records(Database())

@router.get("/{project_id}", dependencies=[Depends(service.CORS)])
async def read(project_id: int):
	p = await project.get_records(Database(), project_id)
    
	projectParticipants = p[0]['participants']
	projectParticipants = projectParticipants.split(',')

	participants = []
	for participant in projectParticipants:
		participant = await applicants.get_records(Database(), int(participant))
		participants.append(participant)

	p[0]['participants'] = participants
	return p

@router.post("/")
async def create(request: Request):
    try:
        form_data = await request.form()
        project = Project(
            name=form_data['name'],
            description=form_data['description'],
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