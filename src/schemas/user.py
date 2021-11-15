from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    CEO = 1
    admin = 2

class User(BaseModel):
    username: str
    password: str
    role: Role