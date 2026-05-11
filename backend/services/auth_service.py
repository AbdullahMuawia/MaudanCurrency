import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.models import User

# Secret key used to sign tokens — in production use a long random string
# NEVER hardcode this in production, use environment variables
SECRET_KEY  = os.getenv("SECRET_KEY", "REDACTED")
ALGORITHM   = "HS256"        # Hashing algorithm
TOKEN_EXPIRE_MINUTES = 60    # Token valid for 1 hour

# CryptContext handles hashing and verifying passwords using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Turn 'myREDACTED' into '$2b$12$...' (bcrypt hash)"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Check if a plain password matches a stored hash"""
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict) -> str:
    """
    Create a JWT token.
    The token contains the username and an expiry time.
    It's signed with SECRET_KEY — any tampering breaks the signature.
    """
    to_encode = data.copy()
    expire    = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str | None:
    """Verify a token and extract the username. Returns None if invalid."""
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")  # "sub" = subject = who this token is for
        return username
    except JWTError:
        return None


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, email: str, password: str) -> User:
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user