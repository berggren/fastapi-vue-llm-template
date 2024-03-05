from sqlalchemy import Boolean, Column, Integer, Unicode, UnicodeText

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode, unique=False, index=True)
    email = Column(Unicode, unique=True, index=True)
    picture = Column(Unicode, unique=False, index=False)
    preferences = Column(UnicodeText, unique=False, index=False)
    is_active = Column(Boolean, default=True)
