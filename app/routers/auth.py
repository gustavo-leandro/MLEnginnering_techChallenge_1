"""
Authentication router: Endpoints for JWT login, refresh, and user validation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.schemas import LoginResponse
import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "8*DrPteyaKzC>7m3[m1="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
http_bearer = HTTPBearer()


def fake_verify_user(username: str, password: str):
    """
    Mock user verification for demonstration purposes.
    """
    return username == "admin" and password == "admin"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_router.post("/login", response_model=LoginResponse)
def login(username: str, password: str):
    """
    Login endpoint: verifies user and returns JWT token.
    """
    if not fake_verify_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/refresh", response_model=LoginResponse)
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """
    Refresh endpoint: validates token and returns a new JWT token.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        new_token = create_access_token({"sub": username})
        return {"access_token": new_token, "token_type": "bearer"}
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    """
    Dependency to get current user from JWT token.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return username
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
