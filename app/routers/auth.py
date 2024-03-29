from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.dependencies import Database, get_current_user
from app.services import service
import hashlib

router = APIRouter(dependencies=[Depends(service.CORS)])
session_manager = service.SessionManager()

@router.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data['username']
    hashed_password = hashlib.sha256(form_data['password'].encode()).hexdigest()
    user = Database().query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    if user:
        session_id = session_manager.generate_session_id()
        JWT_token = session_manager.create_session(session_id, user[0])
        return {"message": "Logged in successfully", "session_id": session_id, "token": JWT_token, "user": user[0]}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.get("/logout")
def logout():
	# TODO: Implement the logout functionality correctly
	# DEBUG
	session_manager.clear_all_sessions()
	return {"message": "Logged out successfully"}

@router.get("/me")
def session_expired(userId: str = Depends(get_current_user)):
     return {"user": userId}