from pydantic import BaseModel, EmailStr, Field


# --------------------------------------------------
# Register
# --------------------------------------------------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)


# --------------------------------------------------
# Login
# --------------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


# --------------------------------------------------
# User response
# --------------------------------------------------

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True