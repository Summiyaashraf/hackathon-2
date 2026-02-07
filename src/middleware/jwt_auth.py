from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from functools import wraps
from pydantic import BaseModel
import uuid


class JWTPayload(BaseModel):
    sub: str  # user_id
    email: str
    exp: int
    iat: int


class JWTManager:
    def __init__(self):
        self.secret = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def create_access_token(self, user_id: str, email: str) -> str:
        """Create a new JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": user_id,
            "email": email,
            "exp": expire.timestamp(),
            "iat": datetime.utcnow().timestamp()
        }

        encoded_jwt = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[JWTPayload]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return JWTPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=401, detail="Could not validate credentials")


# Initialize JWT Manager
jwt_manager = JWTManager()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            decoded_token = jwt_manager.verify_token(credentials.credentials)
            request.state.user_id = decoded_token.sub
            request.state.email = decoded_token.email

            return decoded_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def get_current_user_from_request(request: Request) -> str:
    """Get current user from JWT token in request state"""
    if request and hasattr(request.state, 'user_id'):
        return request.state.user_id
    raise HTTPException(status_code=401, detail="Not authenticated")


def require_same_user(user_id_from_path: str):
    """Check if the user in the token matches the user in the path"""
    def check_user_match(request: Request):
        current_user_id = getattr(request.state, 'user_id', None)
        if not current_user_id or str(current_user_id) != str(user_id_from_path):
            raise HTTPException(
                status_code=403,
                detail="Access forbidden: User does not have permission to access this resource"
            )
        return True

    return check_user_match