from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.auth import UserCreate, UserResponse, Token
from services.auth_service import (
    verify_password, create_access_token,
    get_user_by_username, create_user, decode_token
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# This tells FastAPI where clients send their token (the /auth/login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency that extracts and validates the current user from a JWT token.
    Used on protected routes with: current_user = Depends(get_current_user)
    """
    username = decode_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register", response_model=UserResponse, status_code=201)
def register(body: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, body.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    return create_user(db, body.username, body.email, body.password)


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    """Returns the currently logged-in user's info."""
    return current_user