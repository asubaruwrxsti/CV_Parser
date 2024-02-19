from fastapi import APIRouter, Depends
from app.dependencies import Database, get_current_user
from app.services import service
import json

router = APIRouter(dependencies=[Depends(service.CORS)])
session_manager = service.SessionManager()

@router.get("/")
async def dashboard(userId: str = Depends(get_current_user)):
    # Active Project
        # Project Participants
    
    active_project = Database().query(f"SELECT *, participants FROM projects WHERE status = 'active'")

    for project in active_project:
        participants = json.loads(project['participants'])
        project['participants'] = len(participants[0])

    # New Applicants
    new_applicants = Database().query(f"SELECT * FROM applicants ORDER BY id DESC")

    # All Projects
    all_projects = Database().query(f"SELECT * FROM projects")

    return {"active_project": active_project, "new_applicants": new_applicants, "all_projects": all_projects}