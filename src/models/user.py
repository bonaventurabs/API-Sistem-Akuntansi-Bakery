from sqlalchemy.sql.expression import null
from sqlalchemy import Column,  DateTime, ForeignKey, Integer, String ,Boolean, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.database import Base
import enum


class enum_roles(enum.Enum):
    admin = "admin"
    CEO = "CEO"

class Pengguna(Base):
    __tablename__ = "pengguna"

    username = Column(String(15), primary_key=True)
    password = Column(String(127), nullable=False)
    role = Column(Enum(enum_roles), nullable=False)