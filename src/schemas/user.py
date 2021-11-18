from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    admin = 1
    CEO = 2

class User(BaseModel):
    username: str
    password: str
    role: Role