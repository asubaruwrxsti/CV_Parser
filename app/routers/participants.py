from fastapi import APIRouter, Request, Depends
from app.models.models import Applicants
from app.dependencies import Database, get_current_user
from app.services import service

router = APIRouter(dependencies=[Depends(service.CORS), Depends(get_current_user)])
applicants = Applicants()

@router.get("/")
async def read():
    applicantFields = [field for field in applicants.fields if field != 'cv_id']
    return Database().query(f'SELECT {", ".join(applicantFields)} FROM applicants')

@router.post("/search")
async def search(request: Request):
    fields = await request.json()
    query = "SELECT * FROM applicants WHERE " + " AND ".join([f"CAST(applicants.{key} AS TEXT) ILIKE '%{value}%' LIMIT 3" for key, value in fields.items()])

    return Database().query(query)