from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.dependencies import Database, SessionManager, CORS
import hashlib

router = APIRouter(dependencies=[Depends(CORS)])
session_manager = SessionManager()

@router.post("/login")
async def login(request: Request):
    form_data = await request.form()
    username = form_data['username']
    hashed_password = hashlib.sha256(form_data['password'].encode()).hexdigest()
    user = Database().query(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    if user:
        # Fetch column names dynamically
        column_names = [column[0] for column in Database().query("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users' ORDER BY ORDINAL_POSITION")]
        # Convert user data into a dictionary with column names
        user_dict = {column_names[i]: user[0][i] for i in range(len(column_names))}
        session_id = session_manager.generate_session_id()
        JWT_token = session_manager.create_session(session_id, user_dict)
        return {"message": "Logged in successfully", "session_id": session_id, "token": JWT_token, "user": user_dict}
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