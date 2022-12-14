import datetime
from typing import List

from fastapi.encoders import jsonable_encoder

from .base import BaseRepository
from core.security import hash_password
from db.users import users
from models.user import User, UserIn


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)

        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> User:
        query = users.select().where(users.c.id==id).first()
        user = await self.database.fetch_one(query=query)

        if user is None:

            return None

        return User.parse_obj(user)

    async def get_by_email(self, email: str) -> User:
        query = users.select().where(users.c.email==email)
        user = await self.database.fetch_one(query=query)
        
        if user is None:

            return None

        return User.parse_obj(user)

    async def update(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            hashed_password=hash_password(u.password),
            email=u.email,
        )

        values = {**user.dict()}
        values.pop('id', None)

        query = users.update().where(users.c.id==id).values(**values)
        await self.database.execute(query)
        return user

    async def create(self, u: UserIn) -> User:
        user = User(
            name=u.name,
            hashed_password=hash_password(u.password),
            email=u.email,
            created_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop('id', None)
        query = users.insert().values(**values)
        await self.database.execute(query)

        return user.dict()