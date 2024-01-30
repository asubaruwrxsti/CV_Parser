import jwt
from fastapi import Request, HTTPException
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from app.utils.helperFunctions import loadEnv

env = loadEnv()

SECRET_KEY = env["JWT_SECRET"]
ALGORITHM = env["JWT_ALGORITHM"]

class checkJWT(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=403, detail="Not authenticated")
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (ValueError, jwt.PyJWTError):
            raise HTTPException(status_code=403, detail="Invalid token or expired token")
        response = await call_next(request)
        return response