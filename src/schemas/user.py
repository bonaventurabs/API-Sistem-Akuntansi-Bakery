from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    admin = "admin"
    CEO = "CEO"

class User(BaseModel):
    username: str
    password: str
    role: Role