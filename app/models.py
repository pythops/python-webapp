from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.future import select

from app.database import Base, db
from app.exceptions import UserAlreadyExists


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)

    @classmethod
    async def create(cls, email: str, username: str):
        user = await cls.get(username=username)
        if user:
            raise UserAlreadyExists(username=username)
        new_user = cls(
            user_id=str(uuid4()),
            email=email,
            username=username,
        )
        try:
            db.add(new_user)
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def get(cls, username: str) -> list:
        query = select(cls).where(cls.username == username)
        result = await db.execute(query)
        user = result.one_or_none()
        return user

    @classmethod
    async def get_all(cls) -> list:
        query = select(cls)
        result = await db.execute(query)
        users = result.all()
        return [user.User for user in users]

    async def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
        }
