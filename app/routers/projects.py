from fastapi import APIRouter, Request, Depends
from app.models.models import Project, Applicants
from app.dependencies import Database, get_current_user
from app.services import service
import base64
from PIL import Image
import io

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
        project_data = {field: form_data.get(field, None) for field in Project().fields}

        # Check if the image field is a base64 string
        if 'image' in project_data and project_data['image'] is not None:
            # Check if the image is a string
            if isinstance(project_data['image'], str):
                # Remove the base64 prefix
                base64_str = project_data['image'].split(',')[1]
                # Convert the base64 string to bytes
                image_bytes = base64.b64decode(base64_str)
                # Convert bytes to image
                image = Image.open(io.BytesIO(image_bytes))
                # Save the image
                image.save('image.png')
                # Store the bytes directly, not as a BytesIO object
                project_data['image'] = image_bytes
            else:
                project_data['image'] = None
                # return {"Error": "Image is not a base64 string"}

        project = Project(**project_data)
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