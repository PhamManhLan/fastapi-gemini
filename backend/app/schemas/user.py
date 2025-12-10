from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    email: EmailStr
    full_name: str | None = None