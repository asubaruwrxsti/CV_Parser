from fastapi import APIRouter, Depends
from app.dependencies import Database, get_current_user
from app.services import service

router = APIRouter(dependencies=[Depends(service.CORS)])
session_manager = service.SessionManager()

@router.get("/")
async def dashboard(userId: str = Depends(get_current_user)):
    # Active Project
        # Project Participants
    projectColumnName = [column[0] for column in Database().query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'projects' ORDER BY ORDINAL_POSITION")]
    
    active_project = Database().query(f"SELECT *, participants FROM projects WHERE status = 'active'")
    active_project = [{projectColumnName[i]: project[i] for i in range(len(projectColumnName))} for project in active_project]

    for project in active_project:
        participantsID = project['participants'].split(",")
        participants = Database().query(f"SELECT id, username FROM users WHERE id IN ({','.join(participantsID)})")
        project['participants'] = participants

    applicantsColumnName = [column[0] for column in Database().query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'applicants' ORDER BY ORDINAL_POSITION")]
    new_applicants = Database().query(f"SELECT * FROM applicants ORDER BY id DESC")
    new_applicants = [{applicantsColumnName[i]: applicant[i] for i in range(len(applicantsColumnName))} for applicant in new_applicants]

    return {"active_project": active_project, "new_applicants": new_applicants}