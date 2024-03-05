from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    picture: str


class UserCreate(UserBase):
    email: str
    pass


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
