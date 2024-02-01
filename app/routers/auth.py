from fastapi import APIRouter, HTTPException, status, Request
from app.dependencies import Database, SessionManager
import hashlib

router = APIRouter()
session_manager = SessionManager()

@router.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data['username']
    hashed_password = hashlib.sha256(form_data['password'].encode()).hexdigest()
    user = Database().query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    if user:
        session_id = session_manager.generate_session_id()
        session_manager.create_session(session_id, user[0])
        return {"message": "Logged in successfully", "session_id": session_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@router.post("/logout/{session_id}")
def logout(session_id: str):
	session_manager.delete_session(session_id)
	return {"message": "Logged out successfully"}

@router.get("/getusers/me")
def get_user():
	session = session_manager.get_current_user()
	return session
	if session:
		return session
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Not logged in",
			headers={"WWW-Authenticate": "Basic"},
		)