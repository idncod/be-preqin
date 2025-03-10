from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    uuid: Optional[str] = None
    name: str
    surname: str
    email: EmailStr
    company: Optional[str] = None
    jobTitle: Optional[str] = None
