from sqlalchemy.orm import Session

from . import schemas, models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(name=user.name, email=user.email, picture=user.picture)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
