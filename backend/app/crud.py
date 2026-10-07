from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# --------------------------------------------------
# Password functions
# --------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# --------------------------------------------------
# Find user by email
# --------------------------------------------------

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


# --------------------------------------------------
# Find user by username
# --------------------------------------------------

def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


# --------------------------------------------------
# Create user
# --------------------------------------------------

def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):
    hashed_password = hash_password(password)

    user = models.User(
        username=username,
        email=email,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user