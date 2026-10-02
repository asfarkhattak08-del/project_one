from enum import Enum
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class RegistorUser(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None