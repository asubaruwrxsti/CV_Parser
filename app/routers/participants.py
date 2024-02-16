from fastapi import APIRouter, Request, HTTPException, Depends
from app.models.models import Project, Applicants
from app.dependencies import Database, get_current_user
from app.services import service

router = APIRouter(dependencies=[Depends(service.CORS), Depends(get_current_user)])
applicants = Applicants()

@router.get("/")
async def read():    
    return await applicants.get_records(Database())